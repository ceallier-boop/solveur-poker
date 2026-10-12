'use strict';
// Interface mobile du quiz : consomme l'API /sessions, /quiz/next, /attempts, /sessions/{id}/summary.
const $ = (id) => document.getElementById(id);
const SUIT = { '♠': 's', '♥': 'h', '♦': 'd', '♣': 'c' };
const SUIT_NAME = { s: 'pique', h: 'cœur', d: 'carreau', c: 'trèfle' };
const BLINDS = { 3: [0, 0.5, 1], 2: [0.5, 1] };
const VERDICT = { 'correct': ['correct', 'Bonne réponse'], 'imprécision': ['imprecision', 'Imprécision'], 'erreur': ['erreur', 'Erreur'] };
const state = { sid: null, q: null, index: 0, size: 5, busy: false };

const store = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* stockage indisponible : rien à faire */ } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { /* idem */ } },
};
const bb = (x) => String(Math.round(x * 100) / 100).replace('.', ',');

async function api(path, opts = {}) {
  const r = await fetch(path, { headers: { 'content-type': 'application/json' }, ...opts });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) throw Object.assign(new Error(body.detail || `Erreur ${r.status}`), { status: r.status });
  return body;
}

function show(name) {
  for (const s of document.querySelectorAll('.screen')) s.hidden = s.id !== `screen-${name}`;
  $('loading').hidden = true;
  window.scrollTo(0, 0);
}
function loading(on) { $('loading').hidden = !on; }
function progress(text) { $('progress').textContent = text || ''; }

// ------------------------------------------------------------------ accueil
function filters() {
  const f = {};
  for (const group of document.querySelectorAll('.chips')) {
    const v = group.querySelector('[aria-pressed="true"]').dataset.value;
    if (!v) continue;
    if (group.dataset.name === 'depth') { const [a, b] = v.split('-').map(Number); f.min_stack = a; f.max_stack = b + 0.5; }
    else f[group.dataset.name] = v;
  }
  return f;
}
for (const group of document.querySelectorAll('.chips')) {
  group.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    for (const x of group.querySelectorAll('button')) x.setAttribute('aria-pressed', String(x === b));
  });
}

async function start(f) {
  $('home-error').hidden = true; loading(true);
  try {
    const s = await api('/sessions', { method: 'POST', body: JSON.stringify({ filters: f }) });
    state.sid = s.session_id; state.size = s.size; store.set('sid', s.session_id);
    await next();
  } catch (e) {
    loading(false); $('home-error').textContent = e.status === 422 ? 'Pas assez de situations pour ce thème : élargis les filtres.' : e.message;
    $('home-error').hidden = false;
  }
}

// ------------------------------------------------------------------ question
function contributions(q) {
  const n = q.players.length, c = BLINDS[n].slice(), folded = new Array(n).fill(false);
  for (const h of q.history) {
    const i = q.players.indexOf(h.position);
    if (h.action === 'fold') folded[i] = true;
    else if (h.to_bb !== undefined) c[i] = h.to_bb;
  }
  return { c, folded };
}

function renderTable(q) {
  const view = $('table-view'); view.innerHTML = '';
  const n = q.players.length, hero = q.players.indexOf(q.hero), { c, folded } = contributions(q);
  const spots = n === 3 ? [[50, 80], [15, 32], [85, 32]] : [[50, 80], [50, 18]];
  for (let k = 0; k < n; k++) {
    const i = (hero + k) % n, [x, y] = spots[k];
    const seat = document.createElement('div');
    seat.className = 'seat' + (i === hero ? ' hero' : '') + (folded[i] ? ' folded' : '');
    seat.style.left = x + '%'; seat.style.top = y + '%';
    const left = q.stacks_bb[i] - c[i];
    seat.innerHTML = `<b>${q.players[i]}${i === hero ? ' · toi' : ''}</b>${bb(left)} BB` + (c[i] > 0 && !folded[i] ? `<span class="bet">mise ${bb(c[i])}</span>` : (folded[i] ? '<span class="bet">fold</span>' : ''));
    view.appendChild(seat);
  }
  const pot = document.createElement('div'); pot.className = 'pot'; pot.textContent = `Pot ${bb(q.pot_bb)} BB`; view.appendChild(pot);
}

function renderCards(display) {
  const box = $('hero-cards'); box.innerHTML = ''; const names = [];
  const cards = [...display.matchAll(/([2-9TJQKA])([♠♥♦♣])/g)];
  for (const [, r, s] of cards) {
    const el = document.createElement('div'); const k = SUIT[s];
    el.className = `card ${k}`; el.innerHTML = `${r === 'T' ? '10' : r}<small>${s}</small>`; box.appendChild(el);
    names.push(`${r === 'T' ? '10' : r} de ${SUIT_NAME[k]}`);
  }
  box.setAttribute('aria-label', 'Ta main : ' + names.join(' et '));
}

function renderQuestion(data) {
  state.q = data.question; state.index = data.question_index; state.size = data.size;
  const q = state.q;
  progress(`Question ${state.index + 1} / ${state.size}`);
  renderTable(q); renderCards(q.hand_display);
  $('history').innerHTML = q.history_fr.length ? q.history_fr.map((t) => `<li>${t}</li>`).join('') : '<li>Tu parles en premier</li>';
  $('prompt').textContent = q.prompt_fr;
  const box = $('actions'); box.innerHTML = '';
  q.options.forEach((o, k) => {
    const b = document.createElement('button');
    b.innerHTML = `${o.label_fr}<span class="key">${k + 1}</span>`; b.dataset.id = o.id;
    if (q.options.length % 2 === 1 && k === q.options.length - 1) b.classList.add('only');
    b.addEventListener('click', () => answer(o.id));
    box.appendChild(b);
  });
  show('question');
  box.querySelector('button').focus({ preventScroll: true });
}

async function next() {
  loading(true);
  const data = await api(`/quiz/next?session_id=${encodeURIComponent(state.sid)}`);
  if (data.done) return summary();
  renderQuestion(data);
}

// ------------------------------------------------------------------ correction
async function answer(id) {
  if (state.busy) return; state.busy = true;
  for (const b of $('actions').querySelectorAll('button')) b.disabled = true;
  try {
    const r = await api('/attempts', { method: 'POST', body: JSON.stringify({ session_id: state.sid, question_index: state.index, action_id: id }) });
    renderAnswer(r);
  } catch (e) {
    for (const b of $('actions').querySelectorAll('button')) b.disabled = false;
    alert(e.status ? e.message : 'Connexion perdue : ta réponse n\'a pas été enregistrée, réessaie.');
  } finally { state.busy = false; }
}

function renderAnswer(r) {
  const [cls, title] = VERDICT[r.verdict];
  const v = $('a-verdict'); v.className = `verdict ${cls}`;
  v.innerHTML = `${title}<small>${r.chosen_label === r.best_label ? 'Meilleure action jouée.' : `Meilleure action : ${r.best_label}`}</small>`;
  $('a-recap').textContent = state.q.prompt_fr.replace(' Que fais-tu ?', '');
  $('a-choice').textContent = r.chosen_label === r.best_label ? '' : `Ton choix : ${r.chosen_label} (${Math.round(r.regret_mbb)} mBB de moins).`;
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  $('a-explanation').textContent = r.explanation_fr;
  $('next-btn').textContent = state.index + 1 >= state.size ? 'Voir le bilan' : 'Question suivante';
  show('answer'); v.focus({ preventScroll: true });
}

// ------------------------------------------------------------------ bilan
async function summary() {
  const s = await api(`/sessions/${encodeURIComponent(state.sid)}/summary`);
  store.del('sid'); progress('');
  $('s-score').innerHTML = `${bb(s.points)} / ${s.questions}<small>${s.score_pct} % des points</small>`;
  $('s-verdicts').innerHTML = [['correct', 'Bonnes'], ['imprécision', 'Imprécisions'], ['erreur', 'Erreurs']]
    .map(([k, t]) => `<li><b>${s.verdicts[k] || 0}</b>${t}</li>`).join('');
  $('s-errors').innerHTML = s.errors.length
    ? s.errors.map((e) => `<li>${e.prompt_fr}<br>Joué : ${e.chosen} · Mieux : <b>${e.best}</b> (${Math.round(e.regret_mbb)} mBB)</li>`).join('')
    : '<li>Aucune erreur sur cette série.</li>';
  show('summary');
}

// ------------------------------------------------------------------ navigation
$('quick-start').addEventListener('click', () => start({}));
$('custom-start').addEventListener('click', () => start(filters()));
$('next-btn').addEventListener('click', () => next().catch((e) => alert(e.message)));
$('again-btn').addEventListener('click', () => start({}));
$('back-home').addEventListener('click', home);
$('home-btn').addEventListener('click', home);
$('resume').addEventListener('click', () => { state.sid = store.get('sid'); next().catch(home); });
document.addEventListener('keydown', (e) => {
  if ($('screen-question').hidden || e.altKey || e.ctrlKey || e.metaKey) return;
  const k = Number(e.key); const btns = $('actions').querySelectorAll('button');
  if (k >= 1 && k <= btns.length) btns[k - 1].click();
});

async function home() {
  progress(''); show('home');
  const sid = store.get('sid');
  $('resume').hidden = true;
  if (!sid) return;
  try {
    const s = await api(`/sessions/${encodeURIComponent(sid)}/summary`);
    if (!s.complete) $('resume').hidden = false; else store.del('sid');
  } catch (e) { store.del('sid'); }
}
home();

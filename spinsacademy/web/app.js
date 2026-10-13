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
const pc = (x) => String(x).replace('.', ',') + ' %';

// identifiant anonyme de l'appareil (mode invité) : relie les séries d'un même joueur pour les statistiques
function playerId() {
  let id = store.get('player_id');
  if (!id) {
    id = (crypto.randomUUID ? crypto.randomUUID() : Array.from(crypto.getRandomValues(new Uint8Array(16)), (b) => b.toString(16).padStart(2, '0')).join(''));
    store.set('player_id', id);
  }
  return id;
}

async function api(path, opts = {}) {
  const r = await fetch(path, { ...opts, headers: { 'content-type': 'application/json', 'X-Player-Id': playerId() } });
  const body = r.status === 204 ? {} : await r.json().catch(() => ({}));
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
function mode() { return document.querySelector('.mode-switch [aria-pressed="true"]').dataset.value; }
function filters() {
  const f = {};
  for (const group of document.querySelectorAll('.filters .chips')) {
    if (group.closest('fieldset').hidden) continue;
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
    const s = await api('/sessions', { method: 'POST', body: JSON.stringify({ mode: f.mode || mode(), filters: Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode')) }) });
    state.sid = s.session_id; state.size = s.size; state.mode = s.mode; store.set('sid', s.session_id);
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
  const v = q.villain; $('villain').hidden = !v;
  const pr = q.profile;
  if (v) $('villain').innerHTML = (pr ? `<span class="profile">Profil fictif : <b>${pr.name_fr}</b></span><small>${pr.description_fr}</small>` : '')
    + `Le <b>${v.position}</b> part à tapis avec <b>${bb(v.observed_pct)} %</b> de ses mains ici (GTO : ${bb(v.gto_pct)} %).`;
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
  $('a-choice').textContent = r.chosen_label === r.best_label ? '' : `Ton choix : ${r.chosen_label} (${r.regret_mbb < 100 ? Math.round(r.regret_mbb) + ' mBB' : bb(r.regret_mbb / 1000) + ' BB'} de moins).`;
  $('a-strategy-title').textContent = r.gto_label ? `Contre ce joueur : ${r.best_label} · contre un joueur GTO : ${r.gto_label}` : 'Stratégie de référence';
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  const ex = r.exploit; $('a-exploit').hidden = !ex;
  if (ex) {
    const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
    $('a-exploit').innerHTML = [['Référence GTO', ex.reference_fr], ['Tendance supposée', ex.tendency_fr], ['Adaptation', ex.adaptation_fr],
      [`Confiance ${ex.confidence}`, ex.confidence_fr.replace(/^Confiance [^:]+: /, '')]]
      .map(([k, t]) => `<div><dt>${k}</dt><dd>${cap(t)}</dd></div>`).join('');
  }
  $('a-explanation').textContent = ex && r.core_fr ? r.core_fr : r.explanation_fr;
  $('next-btn').textContent = state.index + 1 >= state.size ? 'Voir le bilan' : 'Question suivante';
  resetReport();
  show('answer'); v.focus({ preventScroll: true });
}

// ------------------------------------------------------------------ signalement d'une question
function resetReport() {
  const done = (state.reported || new Set()).has(`${state.sid}:${state.index}`);
  $('report').open = false; $('report-form').reset();
  $('report-form').hidden = done; $('report-done').hidden = !done;
}

async function sendReport(e) {
  e.preventDefault();
  const reason = new FormData($('report-form')).get('reason');
  if (!reason || state.busy) return; state.busy = true;
  try {
    await api('/reports', { method: 'POST', body: JSON.stringify({ session_id: state.sid, question_index: state.index, reason, comment: $('report-comment').value || null }) });
  } catch (err) {
    if (err.status !== 409) { alert(err.message); return; }                  // 409 : déjà signalée, on remercie quand même
  } finally { state.busy = false; }
  (state.reported = state.reported || new Set()).add(`${state.sid}:${state.index}`);
  $('report-form').hidden = true; $('report-done').hidden = false;
}

// ------------------------------------------------------------------ bilan
async function summary() {
  const s = await api(`/sessions/${encodeURIComponent(state.sid)}/summary`);
  store.del('sid'); progress('');
  $('s-score').innerHTML = `${bb(s.points)} / ${s.questions}<small>${pc(s.score_pct)} des points</small>`;
  $('s-verdicts').innerHTML = [['correct', 'Bonnes'], ['imprécision', 'Imprécisions'], ['erreur', 'Erreurs']]
    .map(([k, t]) => `<li><b>${s.verdicts[k] || 0}</b>${t}</li>`).join('');
  $('s-errors').innerHTML = s.errors.length
    ? s.errors.map((e) => `<li>${e.prompt_fr}<br>Joué : ${e.chosen} · Mieux : <b>${e.best}</b> (${Math.round(e.regret_mbb)} mBB)</li>`).join('')
    : '<li>Aucune erreur sur cette série.</li>';
  show('summary');
}

// ------------------------------------------------------------------ progression
const DIM_FR = { mode: 'Mode', family: 'Situation', hero: 'Position', table: 'Format', depth: 'Profondeur' };
function themeRow(x, min) {
  const low = x.reliable && x.score_pct < 60, cls = !x.reliable ? ' unreliable' : (low ? ' low' : '');
  const right = x.reliable ? pc(x.score_pct) : `${x.questions} / ${min} questions`;
  return `<div class="trow${cls}"><span>${x.label}</span><span>${right}</span><div class="sbar"><i style="width:${x.reliable ? x.score_pct : 0}%"></i></div></div>`;
}
async function stats() {
  loading(true);
  const s = await api('/users/me/stats');
  progress('');
  if (!s.questions) {
    $('st-score').innerHTML = '—<small>Joue une première série pour voir ta progression.</small>';
    for (const id of ['st-evolution', 'st-weakest', 'st-themes', 'st-recurring']) $(id).innerHTML = '';
    $('st-note').textContent = ''; show('stats'); return;
  }
  $('st-score').innerHTML = `${pc(s.score_pct)}<small>${s.questions} questions · ${s.sessions} séries</small>`;
  $('st-evolution').innerHTML = s.evolution.length > 1
    ? s.evolution.map((e) => `<i style="height:${Math.max(4, e.score_pct)}%" title="${pc(e.score_pct)}"></i>`).join('')
    : '<span>L\'évolution s\'affiche après deux séries.</span>';
  const w = s.weakest;
  $('st-weakest').innerHTML = w ? `<div class="weak"><span>Point à travailler : <b>${w.label}</b> (${pc(w.score_pct)} sur ${w.questions} questions)</span>`
    + `<button class="primary" id="train-weak">M'entraîner sur ce thème</button></div>` : '';
  if (w) $('train-weak').addEventListener('click', () => start(w.filters));
  $('st-themes').innerHTML = Object.entries(s.by).map(([k, rows]) =>
    `<div class="theme-group"><b>${DIM_FR[k]}</b>${rows.map((x) => themeRow(x, s.min_sample)).join('')}</div>`).join('');
  $('st-recurring').innerHTML = s.recurring_errors.length
    ? s.recurring_errors.map((e, k) => `<li><b>${e.label}</b> : ${e.errors} erreurs sur ${e.questions} questions (${e.regret_mbb} mBB perdus)<br>${e.examples[0] || ''}<br><button class="link" data-k="${k}">S'entraîner sur ce thème</button></li>`).join('')
    : '<li>Pas d\'erreur répétée pour l\'instant.</li>';
  for (const b of $('st-recurring').querySelectorAll('button[data-k]')) b.addEventListener('click', () => start(s.recurring_errors[Number(b.dataset.k)].filters));
  $('st-note').textContent = `Un score n'est affiché qu'à partir de ${s.min_sample} questions sur le thème. Tes données restent anonymes : elles sont liées à cet appareil, pas à ton identité.`;
  show('stats');
}

// ------------------------------------------------------------------ navigation
$('stats-btn').addEventListener('click', () => stats().catch((e) => alert(e.message)));
$('st-back').addEventListener('click', home);
$('st-delete').addEventListener('click', async () => {
  if (!confirm('Effacer définitivement toutes tes séries et ta progression ?')) return;
  await api('/users/me', { method: 'DELETE' }); store.del('sid'); stats();
});
$('quick-start').addEventListener('click', () => start({}));
const MODE_NOTE = { gto: 'Stratégie de référence, contre des adversaires qui jouent juste.',
  exploit: 'Payer ou non un tapis contre des profils fictifs (Serré, Prudent, Agressif, Maniaque) qui poussent moins ou plus souvent que le GTO. Hypothèses de simulation, pas de vrais joueurs.' };
document.querySelector('.mode-switch').addEventListener('click', () => {
  $('mode-note').textContent = MODE_NOTE[mode()]; $('profile-filter').hidden = mode() !== 'exploit';
});
$('custom-start').addEventListener('click', () => start(filters()));
$('report-form').addEventListener('submit', sendReport);
$('next-btn').addEventListener('click', () => next().catch((e) => alert(e.message)));
$('again-btn').addEventListener('click', () => start({ mode: state.mode || mode() }));
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

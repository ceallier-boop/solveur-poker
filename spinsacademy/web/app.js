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
const gainBB = (mbb) => (Math.abs(mbb) < 50 ? '<0,05 BB' : bb(Math.abs(mbb) / 1000) + ' BB');   // gains toujours en BB
// profils fictifs : symbole (sens et force de l'écart de tapis avec le GTO) et couleur, pour les reconnaître d'un coup d'œil
const PROFILE_VIS = { nit: '▼▼', prudent: '▼', agressif: '▲', maniac: '▲▲' };
const pbadge = (pr, small) => `<span class="pbadge p-${pr.id}${small ? ' sm' : ''}" aria-hidden="true">${PROFILE_VIS[pr.id] || '?'}</span>`;
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
  const kind = c.map((x) => (x > 0 ? 'blind' : null));               // dernière action de chaque joueur, pour son jeton
  for (const h of q.history) {
    const i = q.players.indexOf(h.position);
    if (h.action === 'fold') folded[i] = true;
    else if (h.to_bb !== undefined) c[i] = h.to_bb;
    if (h.action !== 'fold' && h.action !== 'check') kind[i] = h.action === 'call_allin' ? 'call' : h.action;
  }
  return { c, folded, kind };
}

// jetons : un symbole et une couleur par type de mise (légende sous la table)
const CHIP = { blind: ['', 'Blinde'], limp: ['=', 'Limp'], call: ['✓', 'Call'], raise: ['▲', 'Relance'], allin: ['★', 'Tapis'] };
function chip(kind, amount, x, y) {
  const el = document.createElement('div'); el.className = `chip k-${kind}`;
  el.style.left = x + '%'; el.style.top = y + '%';
  el.innerHTML = `<i>${CHIP[kind][0]}</i><span>${bb(amount)}</span>`;
  return el;
}

function renderTable(q) {
  const view = $('table-view'); view.innerHTML = '';
  const n = q.players.length, hero = q.players.indexOf(q.hero), { c, folded, kind } = contributions(q);
  const spots = n === 3 ? [[50, 84], [17, 22], [83, 22]] : [[50, 84], [50, 18]];
  const chips = n === 3 ? [[27, 84], [17, 43], [83, 43]] : [[27, 84], [73, 20]];      // devant chaque place, hors du pot et des cartes
  for (let k = 0; k < n; k++) {
    const i = (hero + k) % n, [x, y] = spots[k];
    const seat = document.createElement('div');
    seat.className = 'seat' + (i === hero ? ' hero' : '') + (folded[i] ? ' folded' : '');
    seat.style.left = x + '%'; seat.style.top = y + '%';
    const left = q.stacks_bb[i] - c[i];
    const backs = i !== hero && !folded[i] ? '<span class="backs"><i></i><i></i></span>' : '';      // cartes cachées des adversaires en jeu
    const tag = q.profile && q.villain && q.villain.position === q.players[i] ? pbadge(q.profile, true) : '';   // profil du vilain à sa place
    seat.innerHTML = tag + backs + `<b>${q.players[i]}${i === hero ? ' · toi' : ''}</b>${bb(left)} BB` + (folded[i] ? '<span class="bet">fold</span>' : '');
    view.appendChild(seat);
    if (c[i] > 0 && kind[i]) view.appendChild(chip(kind[i], c[i], ...chips[k]));     // un joueur couché laisse sa mise devant lui
  }
  const pot = document.createElement('div'); pot.className = 'pot'; pot.textContent = `Pot ${bb(q.pot_bb)} BB`; view.appendChild(pot);
  const used = [...new Set(kind.filter((k, i) => k && c[i] > 0))];
  $('chip-legend').innerHTML = used.map((k) => `<span class="chip k-${k}"><i>${CHIP[k][0]}</i></span>${CHIP[k][1]}`).join('');
  const hole = document.createElement('div'); hole.className = 'cards hole'; hole.id = 'hero-cards'; view.appendChild(hole);   // tes cartes, devant ta place
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
  $('purpose').hidden = !data.purpose_fr; $('purpose').textContent = data.purpose_fr || '';
  $('purpose').className = `purpose ${data.purpose || ''}`;
  const q = state.q;
  progress(`Question ${state.index + 1} / ${state.size}`);
  renderTable(q); renderCards(q.hand_display);
  $('history').innerHTML = q.history_fr.length ? q.history_fr.map((t) => `<li>${t}</li>`).join('') : '<li>Tu parles en premier</li>';
  const fmt = q.table === '3-handed' ? '3 joueurs' : 'Heads-up';
  $('seat-line').innerHTML = `Tu es au <b>${q.hero}</b> · ${fmt}`;
  $('prompt-full').textContent = q.prompt_fr;                        // énoncé complet pour les lecteurs d'écran
  const v = q.villain; $('villain').hidden = !v;
  const pr = q.profile;
  if (v) {
    const [lo, hi] = (pr && pr.band_pct) || [null, null];
    const top = Math.min(100, Math.max(v.observed_pct, v.gto_pct, hi || 0) * 1.15);
    const w = (x) => (100 * x / top).toFixed(1) + '%';
    const zone = pr && pr.band_pct ? `<u style="left:${w(lo || 0)};width:${(100 * ((hi == null ? top : hi) - (lo || 0)) / top).toFixed(1)}%"></u>` : '';
    const bar = (label, x, cls, z) => `<div class="vbar ${cls}"><span>${label}</span><em>${z || ''}<i style="width:${w(x)}"></i></em><b>${bb(x)} %</b></div>`;
    const bandTxt = lo == null ? `moins de ${bb(hi)} %` : hi == null ? `plus de ${bb(lo)} %` : `entre ${bb(lo)} et ${bb(hi)} %`;
    $('villain').innerHTML = (pr ? `<div class="vhead">${pbadge(pr)}<span>Profil fictif · <b>${pr.name_fr}</b></span></div><small>${pr.description_fr}</small>` : '')
      + `<p class="vstat">Tapis du ${v.position} dans cette situation :</p>${bar(pr ? pr.name_fr.split(' (')[0] : v.position, v.observed_pct, 'obs', zone)}${bar('GTO', v.gto_pct, 'gto')}`
      + (pr && pr.band_pct ? `<p class="vband"><span class="swatch"></span>Ce type de profil : tapis ${bandTxt} des mains ici.</p>` : '');
  }
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
  $('a-recap').textContent = state.q.prompt_fr.replace(' Que fais-tu ?', '').split('\n').filter((l) => !l.startsWith('Profil fictif')).join('\n');
  $('a-choice').textContent = r.chosen_label === r.best_label ? '' : `Ton choix : ${r.chosen_label} (${gainBB(r.regret_mbb)} de moins).`;
  $('a-strategy-title').textContent = r.gto_label ? `Contre ce joueur : ${r.best_label} · contre un joueur GTO : ${r.gto_label}` : 'Stratégie de référence';
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  const ex = r.exploit; $('a-exploit').hidden = !ex;
  for (const id of ['a-choice', 'a-strategy-title', 'a-strategy']) $(id).hidden = !!ex;   // exploitant : correction courte
  if (ex) {
    $('a-exploit').innerHTML = `<div class="ref"><dt>${pbadge(ex.profile, true)} Contre ce type de profil · <b>${ex.profile.name_fr}</b><span class="conf ${ex.confidence === 'élevée' ? 'net' : ''}">${ex.confidence_fr}</span></dt><dd>${ex.reference_fr}</dd></div>`

      + `<div><dt>Par rapport au GTO</dt><dd>${ex.comparison_fr}</dd></div><p class="note">${ex.note_fr}</p>`;
  }
  $('a-explanation').hidden = !!ex; $('a-explanation').textContent = r.core_fr || r.explanation_fr;
  const why = r.why_fr || []; $('a-why-box').hidden = !why.length; $('a-why-box').open = false;
  $('a-why').innerHTML = why.map((l) => `<p>${l}</p>`).join('');
  renderNext(r.next);
  $('a-grid-box').hidden = !r.range; $('a-grid-box').open = false; if (r.range) renderGrid(r.range, state.q.hand, !!ex);
  $('next-btn').textContent = state.index + 1 >= state.size ? 'Voir le bilan' : 'Question suivante';
  resetReport();
  show('answer'); v.focus({ preventScroll: true });
}

// ------------------------------------------------------------------ « Et ensuite ? » : la main après le flop, comparée à la moyenne
function renderNext(n) {
  $('a-next-box').hidden = !n; $('a-next-box').open = false; if (!n) return;
  const p100 = (x) => Math.round(100 * x);
  const top = Math.max(...(n.metrics || []).map((m) => Math.max(m.value, m.average)), 0.01);
  const TAG = { above: '▲ au-dessus', below: '▼ en dessous', equal: '= dans' };
  const rows = (n.metrics || []).map((m) => `<div class="mrow ${m.compare} ${m.tone || (m.compare === 'above' ? 'good' : m.compare === 'below' ? 'bad' : 'neutral')}">
      <span class="mlabel">${m.label_fr}</span>
      <span class="mtrack"><i style="width:${(100 * m.value / top).toFixed(1)}%"></i><b style="left:${(100 * m.average / top).toFixed(1)}%" title="moyenne"></b></span>
      <span class="mval">${p100(m.value)} %</span>
      <span class="mtag">${TAG[m.compare]} de la moyenne (${p100(m.average)} %)</span></div>`).join('');
  const list = (xs, cls, title) => (xs && xs.length ? `<h4 class="${cls}">${title}</h4><ul class="${cls}">${xs.map((x) => `<li>${x}</li>`).join('')}</ul>` : '');
  $('a-next').innerHTML = `<p>${n.intro}</p>` + (n.position ? `<p class="pos">${n.position}</p>` : '')
    + (rows ? `<div class="metrics"><p class="mhead">Au flop, comparé à la moyenne ${n.metrics[0].reference_fr} (repère vertical) :</p>${rows}</div>` : '')
    + list(n.forces, 'plus', 'Forces') + list(n.weaknesses, 'minus', 'Faiblesses');
}

// ------------------------------------------------------------------ grille 13 x 13 de la stratégie de référence
const RANKS = 'AKQJT98765432';
const ACT_COLOR = { fold: 'var(--a-fold)', check: 'var(--a-passive)', limp: 'var(--a-passive)', call: 'var(--a-call)', call_allin: 'var(--a-call)', raise: 'var(--a-raise)', allin: 'var(--a-allin)' };
function renderGrid(range, hand, exploit) {
  const acts = range.actions; const cells = [];
  for (let r = 0; r < 13; r++) {
    for (let c = 0; c < 13; c++) {
      const h = r === c ? RANKS[r] + RANKS[c] : r < c ? RANKS[r] + RANKS[c] + 's' : RANKS[c] + RANKS[r] + 'o';
      const mix = range.hands[h]; let bg = 'var(--line)';
      if (mix) {
        let at = 0; const stops = [];
        acts.forEach((a, j) => { if (mix[j] > 0) { stops.push(`${ACT_COLOR[a.type]} ${at}% ${at + mix[j]}%`); at += mix[j]; } });
        bg = `linear-gradient(90deg, ${stops.join(', ')})`;
      }
      cells.push(`<span class="${h === hand ? 'me' : ''}${mix ? '' : ' out'}" style="background:${bg}">${h}</span>`);
    }
  }
  $('a-grid').innerHTML = cells.join('');
  $('a-grid').setAttribute('aria-label', `Grille des 169 mains ; ta main ${hand} est entourée`);
  $('a-grid-title').textContent = exploit ? 'Voir la décision contre ce type de profil sur toutes les mains' : 'Voir la stratégie sur toutes les mains';
  $('a-grid-legend').innerHTML = acts.map((a, j) => `<span><i style="background:${ACT_COLOR[a.type]}"></i>${a.label_fr} ${range.share_pct[j]} %</span>`).join('')
    + '<span><i class="me-key"></i>ta main</span>';
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
    ? s.errors.map((e) => `<li>${e.prompt_fr}<br>Joué : ${e.chosen} · Mieux : <b>${e.best}</b> (${gainBB(e.regret_mbb)} de moins)</li>`).join('')
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
  await adaptation();
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
    ? s.recurring_errors.map((e, k) => `<li><b>${e.label}</b> : ${e.errors} erreurs sur ${e.questions} questions (${gainBB(e.regret_mbb)} perdus)<br>${e.examples[0] || ''}<br><button class="link" data-k="${k}">S'entraîner sur ce thème</button></li>`).join('')
    : '<li>Pas d\'erreur répétée pour l\'instant.</li>';
  for (const b of $('st-recurring').querySelectorAll('button[data-k]')) b.addEventListener('click', () => start(s.recurring_errors[Number(b.dataset.k)].filters));
  $('st-note').textContent = `Un score n'est affiché qu'à partir de ${s.min_sample} questions sur le thème. Tes données restent anonymes : elles sont liées à cet appareil, pas à ton identité.`;
  show('stats');
}

async function adaptation() {
  const modes = { gto: 'GTO', exploit: 'Exploitant' }; const parts = []; let first = null;
  for (const m of Object.keys(modes)) {
    let a; try { a = await api(`/users/me/adaptation?mode=${m}`); } catch (e) { continue; }       // mode sans dataset publié : ignoré
    first = first || a;
    const list = (xs, kind) => xs.map((x) => `<li>${x.label_fr} <small>${x.errors} erreur${x.errors > 1 ? 's' : ''} sur ${x.answers} · difficulté ${x.difficulty_pct} %</small></li>`).join('');
    parts.push(`<div class="adapt-mode"><b>${modes[m]}</b>${a.weak.length
      ? `<p>À retravailler :</p><ul>${list(a.weak)}</ul>` : '<p>Aucun thème à retravailler pour l\'instant.</p>'}${a.review.length ? `<p>En révision :</p><ul>${list(a.review)}</ul>` : ''}</div>`);
  }
  if (!first) { $('st-adapt').hidden = true; return; }
  $('st-adapt').hidden = false; $('adapt-on').checked = first.enabled;
  $('adapt-rule').textContent = first.rule_fr + (first.since ? ` Réinitialisée le ${new Date(first.since).toLocaleDateString('fr-FR')}.` : '');
  $('adapt-themes').innerHTML = parts.join('');
}
$('adapt-on').addEventListener('change', async (e) => {
  try { await api('/users/me/preferences', { method: 'PUT', body: JSON.stringify({ adaptive: e.target.checked }) }); }
  catch (err) { e.target.checked = !e.target.checked; alert(err.message); }
});
$('adapt-reset').addEventListener('click', async () => {
  if (!confirm('Réinitialiser l\'adaptation ? Ta progression et ton historique sont conservés.')) return;
  await api('/users/me/adaptation/reset', { method: 'POST' }); await adaptation();
});

// ------------------------------------------------------------------ lexique : termes de l'écran affiché, puis tout le lexique
let LEX = null;
async function lexique() {
  if (LEX) return LEX;
  LEX = window.SA_LEXIQUE || await (await fetch('/static/lexique.json')).json();
  for (const t of LEX.terms) {                                     // bornes de mot compatibles avec les accents
    const alt = t.match.map((m) => m.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
    t.re = new RegExp(`(?<![\\p{L}\\d])(?:${alt})(?![\\p{L}\\d])`, t.case ? 'u' : 'iu');
  }
  return LEX;
}
const escT = (x) => String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const termHtml = (t) => `<dt>${escT(t.term)}</dt><dd>${escT(t.def)}</dd>`;
function screenText() {
  const s = document.querySelector('.screen:not([hidden])');
  return s ? s.innerText + ' ' + ($('progress').innerText || '') : '';
}
async function renderLex() {
  const L = await lexique(); const q = $('lex-search').value.trim().toLowerCase(); const body = $('lex-body');
  if (q) {
    const hits = L.terms.filter((t) => (t.term + ' ' + t.def + ' ' + t.match.join(' ')).toLowerCase().includes(q));
    body.innerHTML = hits.length ? `<dl>${hits.map(termHtml).join('')}</dl>` : '<p class="note">Aucun terme ne correspond.</p>';
    return;
  }
  const text = screenText(); const here = L.terms.filter((t) => t.re.test(text));
  const groups = Object.entries(L.categories).map(([k, label]) => {
    const ts = L.terms.filter((t) => t.cat === k);
    return `<details><summary>${label} (${ts.length})</summary><dl>${ts.map(termHtml).join('')}</dl></details>`;
  }).join('');
  body.innerHTML = (here.length ? `<h3>Sur cet écran</h3><dl>${here.map(termHtml).join('')}</dl>` : '<p class="note">Aucun terme technique repéré sur cet écran.</p>')
    + `<h3>Tout le lexique</h3>${groups}<p class="note">Lexique ${L.version} : ${L.note_fr}</p>`;
}
let lexReturn = null;
async function openLex() {
  lexReturn = document.activeElement; $('lex-search').value = '';
  await renderLex(); $('lex').hidden = false; $('lex-body').scrollTop = 0; $('lex-close').focus();
}
function closeLex() { $('lex').hidden = true; if (lexReturn) lexReturn.focus(); }
$('lex-btn').addEventListener('click', () => openLex().catch((e) => alert(e.message)));
$('lex-close').addEventListener('click', closeLex);
$('lex').addEventListener('click', (e) => { if (e.target === $('lex')) closeLex(); });
$('lex-search').addEventListener('input', () => renderLex());
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !$('lex').hidden) closeLex(); });

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
  if ($('screen-question').hidden || !$('lex').hidden || e.altKey || e.ctrlKey || e.metaKey) return;
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

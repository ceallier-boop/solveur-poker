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
const gainBB = (mbb) => { const a = Math.abs(mbb);                 // gains toujours en BB ; 3 décimales autour de 0,06 BB (limite d'imprécision)
  return a < 20 ? '<0,02 BB' : Math.abs(a - 60) < 5 ? (a / 1000).toFixed(3).replace('.', ',') + ' BB' : bb(a / 1000) + ' BB'; };
// profils fictifs : symbole (sens et force de l'écart de tapis avec le GTO) et couleur, pour les reconnaître d'un coup d'œil
const PROFILE_VIS = { nit: '▼▼', prudent: '▼', agressif: '▲', maniac: '▲▲', station: '◆' };
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

// messages dans l'écran (pas de boîte de dialogue du navigateur) : erreur avec « Réessayer », confirmation en deux temps
function notify(msg, retry) {
  const n = $('notice'); $('notice-text').textContent = msg; n.hidden = false;
  $('notice-retry').hidden = !retry;
  $('notice-retry').onclick = () => { n.hidden = true; retry(); };
  clearTimeout(notify.t); if (!retry) notify.t = setTimeout(() => { n.hidden = true; }, 6000);
}
const netMsg = (e, what) => (e && e.status ? e.message : `Connexion perdue : ${what}. Vérifie ta connexion, puis réessaie.`);
const retryable = (e) => !e || !e.status || e.status === 429;                 // coupure réseau ou trop de requêtes : « Réessayer »
function confirmTwice(btn, question) {                              // 1er appui : demande ; 2e appui dans les 5 s : confirme
  if (btn.dataset.armed) { clearTimeout(btn._t); delete btn.dataset.armed; btn.textContent = btn.dataset.label; return true; }
  btn.dataset.label = btn.dataset.label || btn.textContent; btn.dataset.armed = '1'; btn.textContent = question;
  btn._t = setTimeout(() => { delete btn.dataset.armed; btn.textContent = btn.dataset.label; }, 5000);
  return false;
}
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

async function start(f, review = false) {
  $('home-error').hidden = true; loading(true);
  try {
    const s = await api('/sessions', { method: 'POST', body: JSON.stringify({ mode: f.mode || mode(), review, filters: Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode')) }) });
    state.sid = s.session_id; state.size = s.size; state.mode = s.mode; store.set('sid', s.session_id);
    await next();
  } catch (e) {
    loading(false); $('home-error').textContent = e.status === 422 ? 'Pas assez de situations pour ce thème : élargis les filtres.' : e.message;
    $('filters').open = true; $('home-error').hidden = false;
    $('home-error').scrollIntoView({ block: 'center' }); $('home-error').focus({ preventScroll: true });
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
    const backs = i !== hero && !folded[i] ? '<span class="backs"><i></i><i></i></span>' : '';      // cartes cachées des adversaires en jeu
    const tag = q.profile && q.villain && q.villain.position === q.players[i] ? pbadge(q.profile, true) : '';   // profil du vilain à sa place
    seat.innerHTML = tag + backs + `<b>${q.players[i]}${i === hero ? ' · toi' : ''}</b>${bb(q.stacks_bb[i])} BB` + (folded[i] ? '<span class="bet">fold</span>' : '');
    view.appendChild(seat);
    if (c[i] > 0 && kind[i]) view.appendChild(chip(kind[i], c[i], ...chips[k]));     // un joueur couché laisse sa mise devant lui
  }
  const pot = document.createElement('div'); pot.className = 'pot'; pot.textContent = `Pot ${bb(q.pot_bb)} BB`; view.appendChild(pot);
  const used = [...new Set(kind.filter((k, i) => k && c[i] > 0))];
  $('chip-legend').innerHTML = used.map((k) => `<span class="chip k-${k}"><i>${CHIP[k][0]}</i></span>${CHIP[k][1]}`).join('');
  const hole = document.createElement('div'); hole.className = 'cards hole'; hole.id = 'hero-cards'; view.appendChild(hole);   // tes cartes, devant ta place
}

function renderCards(display, id = 'hero-cards') {
  const box = $(id); box.innerHTML = ''; const names = [];
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
  const noHand = !q.hand || !!(q.field && q.field.ask_fr); $('hero-cards').hidden = noHand;   // mode Field : questions de lecture, sans main
  for (const id of ['seat-line', 'table-view', 'chip-legend', 'history']) $(id).hidden = noHand;   // pas de coup joué : ni table ni historique
  $('history').innerHTML = q.history_fr.length ? q.history_fr.map((t) => `<li>${t}</li>`).join('') : '<li>Tu parles en premier</li>';
  const fmt = q.table === '3-handed' ? '3 joueurs' : 'Heads-up';
  $('seat-line').innerHTML = `Tu es au <b>${q.hero}</b> · ${fmt}`;
  $('prompt-full').textContent = q.prompt_fr;                        // énoncé complet pour les lecteurs d'écran
  $('ask').innerHTML = !noHand ? `Avec ${q.hand_display.replace(/([♠♥♦♣])/g, (m) => `<span class="suit-${SUIT[m]}">${m}\uFE0E</span>`)}, que fais-tu ?` : escT(q.field.ask_fr);
  $('kbd-hint').textContent = `Raccourcis clavier : touches 1 à ${q.options.length}.`;
  const v = q.villain; $('villain').hidden = !v && !q.field;
  const pr = q.profile;
  $('villain').className = 'villain';
  if (q.field) renderFieldStats(q.field, noHand ? q.prompt_fr.split('\n').filter((l) => !/^Sur \d+ occasions|\?$/.test(l)).join(' ') : '');
  else if (v) {
    const [lo, hi] = (pr && pr.band_pct) || [null, null];
    const top = Math.min(100, Math.max(v.observed_pct, v.gto_pct, hi || 0) * 1.15);
    const w = (x) => (100 * x / top).toFixed(1) + '%';
    const zone = pr && pr.band_pct ? `<u style="left:${w(lo || 0)};width:${(100 * ((hi == null ? top : hi) - (lo || 0)) / top).toFixed(1)}%"></u>` : '';
    const bar = (label, x, cls, z) => `<div class="vbar ${cls}"><span>${label}</span><em>${z || ''}<i style="width:${w(x)}"></i></em><b>${bb(x)} %</b></div>`;
    const bandTxt = lo == null ? `moins de ${bb(hi)} %` : hi == null ? `plus de ${bb(lo)} %` : `entre ${bb(lo)} et ${bb(hi)} %`;
    $('villain').innerHTML = (pr ? `<div class="vhead">${pbadge(pr)}<span>Profil fictif · <b>${pr.name_fr}</b></span></div><small>${pr.description_fr}</small>` : '')
      + `<p class="vstat">${v.stat === 'call_pct' ? `Calls du ${v.position} face à un tapis` : `Tapis du ${v.position}`} dans cette situation :</p>${bar(pr ? pr.name_fr.split(' (')[0] : v.position, v.observed_pct, 'obs', zone)}${bar(v.reference === 'nash_pushfold' ? 'Équilibre' : 'GTO', v.gto_pct, 'gto')}`
      + (pr && pr.band_pct ? `<p class="vband"><span class="swatch"></span>Ce type de profil : ${v.stat === 'call_pct' ? 'paie' : 'tapis'} ${bandTxt} des mains ici.</p>` : '')
      + (pr && pr.recognize ? `<details class="recognize"><summary>Reconnaître ce profil</summary><ul>${pr.recognize.signs_fr.map((x) => `<li>${x}</li>`).join('')}</ul>`
        + (pr.recognize.sample_fr ? `<p>${pr.recognize.sample_fr}</p>` : '') + `<p class="caution">${pr.recognize.caution_fr}</p></details>` : '');
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

// mode Field : ce qui est observé sur le vilain (k sur n), comparé à la théorie ; jamais son profil interne
function renderFieldStats(f, context) {
  const bars = f.stats.map((s) => {
    const top = Math.min(100, Math.max(s.observed_pct, s.gto_pct) * 1.15), w = (x) => (100 * x / top).toFixed(1) + '%';
    return `<p class="vstat">${s.label_fr} : ${s.k} sur ${s.n}</p>`
      + `<div class="vbar obs"><span>Observé</span><em><i style="width:${w(s.observed_pct)}"></i></em><b>${bb(s.observed_pct)} %</b></div>`
      + `<div class="vbar gto"><span>Théorie</span><em><i style="width:${w(s.gto_pct)}"></i></em><b>${bb(s.gto_pct)} %</b></div>`;
  }).join('');
  $('villain').className = 'fstats';
  $('villain').innerHTML = `<span class="ftype">${f.type_fr}</span>` + (context ? `<p class="fnone">${escT(context)}</p>` : '')
    + (f.stats.length ? bars + `<p class="fn">${f.observations} occasions : plus il y en a, plus la tendance est fiable.</p>`
      : `<p class="fnone">Aucune information sur ce vilain : compte sur le profil le plus fréquent du field (rec passif).</p>`);
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
    notify(netMsg(e, "ta réponse n'a pas été enregistrée"), retryable(e) ? () => answer(id) : null);
  } finally { state.busy = false; }
}

function renderAnswer(r) {
  const [cls, title] = VERDICT[r.verdict]; const ex0 = !!r.exploit;
  const v = $('a-verdict'); v.className = `verdict ${cls}`;
  const many = (r.good_labels || []).length > 1 && (r.good_actions || []).includes(r.chosen_action);
  const sub = r.field && r.field.read ? (r.chosen_label === r.best_label ? `Bonne lecture : ${r.best_label}.` : `Ta lecture : ${r.chosen_label}\nLa bonne : ${r.best_label}`)
    : many ? `Plusieurs bonnes décisions : ${r.good_labels.join(' ou ')}. Ton choix en fait partie.`
    : r.chosen_label === r.best_label ? `Tu as joué l'action de référence : ${r.best_label}.`
    : `Tu as joué : ${r.chosen_label}${r.loss_fr ? ` (${r.loss_fr} de moins)` : ''}\nRéférence : ${r.best_label}`;
  v.innerHTML = title + `<small>${sub}</small>`;
  renderCards(state.q.hand_display, 'a-cards'); $('a-cards').hidden = !state.q.hand || !!(state.q.field && state.q.field.ask_fr);
  $('a-recap').textContent = state.q.prompt_fr.replace(' Que fais-tu ?', '').split('\n').filter((l) => !l.startsWith('Profil fictif')).join('\n');
  $('a-choice').hidden = true;                                       // ton choix et son coût sont dans l'explication (pas de redite)
  $('a-strategy-title').textContent = r.gto_label ? `Contre ce joueur : ${r.best_label} · contre un joueur GTO : ${r.gto_label}` : 'Stratégie de référence';
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}${s.chosen ? ' mine' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  const ex = r.exploit, fd = r.field; $('a-exploit').hidden = !ex && !fd;
  for (const id of ['a-strategy-title', 'a-strategy']) $(id).hidden = !!ex || !!fd;   // exploitant, field : correction courte
  if (fd) {
    $('a-exploit').innerHTML = `<div class="ref"><dt>${fd.read ? 'Bonne lecture' : 'Contre ce vilain'}${fd.gain_fr ? `<span class="conf net">${fd.gain_fr} de plus que la théorie</span>` : ''}</dt><dd>${escT(r.best_label)}</dd></div>`
      + (fd.gto_label ? `<div><dt>En théorie (HRC)</dt><dd>${escT(fd.gto_label)}</dd></div>` : '')
      + (fd.evs.length ? `<div><dt>EV par rapport au fold</dt><dd>${fd.evs.map((e) => `${escT(e.label_fr)} : ${e.ev_fr}`).join('\n')}</dd></div>` : '')
      + `<p class="note">${fd.type_fr} · règle ${fd.rule}</p>`;
  } else if (ex) {
    $('a-exploit').innerHTML = `<div class="ref"><dt>${pbadge(ex.profile, true)} Contre ce type de profil · <b>${ex.profile.name_fr}</b><span class="conf ${ex.confidence === 'élevée' ? 'net' : ''}">${ex.confidence_fr}</span></dt><dd>${ex.reference_fr}</dd></div>`

      + `<div><dt>Par rapport au GTO</dt><dd>${ex.comparison_fr}</dd></div><p class="note">${ex.note_fr}</p>`;
  }
  $('a-explanation').hidden = !!ex; $('a-explanation').textContent = r.core_fr || r.explanation_fr;
  $('a-recap').textContent = state.q.prompt_fr.replace(' Que fais-tu ?', '').replace(/\n(Quelle pastille lui donnes-tu|Quel est le défaut de ce vilain) \?$/, '').split('\n').filter((l) => !l.startsWith('Profil fictif')).join('\n');
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
  const TAG = { above: '▲ au-dessus de la moyenne', below: '▼ en dessous de la moyenne', equal: '= dans la moyenne' };
  const rows = (n.metrics || []).map((m) => `<div class="mrow ${m.compare} ${m.tone || (m.compare === 'above' ? 'good' : m.compare === 'below' ? 'bad' : 'neutral')}">
      <span class="mlabel">${m.label_fr}</span>
      <span class="mtrack"><i style="width:${(100 * m.value / top).toFixed(1)}%"></i><b style="left:${(100 * m.average / top).toFixed(1)}%" title="moyenne"></b></span>
      <span class="mval">${p100(m.value)} %</span>
      <span class="mtag">${TAG[m.compare]} (${p100(m.average)} %)</span></div>`).join('');
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
      const mix = range.hands[h]; let bg = 'var(--line)'; let light = false;
      if (mix) {
        let at = 0; const stops = [];
        acts.forEach((a, j) => { if (mix[j] > 0) { stops.push(`${ACT_COLOR[a.type]} ${at}% ${at + mix[j]}%`); at += mix[j]; } });
        bg = `linear-gradient(90deg, ${stops.join(', ')})`;
        const main = mix.indexOf(Math.max(...mix)); light = ['fold', 'raise'].includes(acts[main].type);
      }
      cells.push(`<span data-h="${h}" class="${h === hand ? 'me' : ''}${mix ? '' : ' out'}${light ? ' lt' : ''}" style="background:${bg}">${h}</span>`);
    }
  }
  $('a-grid').innerHTML = cells.join('');
  $('a-grid').setAttribute('aria-label', `Grille des 169 mains ; ta main ${hand} est entourée`);
  $('a-grid-title').textContent = exploit ? 'Voir la décision contre ce type de profil sur toutes les mains' : 'Voir la stratégie sur toutes les mains';
  $('a-grid-legend').innerHTML = '<span class="lg-head">Sur les mains qui arrivent à cette décision :</span>'
    + acts.map((a, j) => `<span><i style="background:${ACT_COLOR[a.type]}"></i>${a.label_fr} ${range.share_pct[j]} %</span>`).join('')
    + '<span><i class="out-key"></i>n\'arrive pas ici (jouée autrement plus tôt)</span><span><i class="me-key"></i>ta main</span>';
  const line = (h) => { const m = range.hands[h];                      // une case touchée : sa stratégie en clair
    return m ? `${h} : ` + acts.map((a, j) => (m[j] ? `${a.label_fr} ${m[j]} %` : '')).filter(Boolean).join(', ')
      : `${h} : n'arrive pas à cette décision (jouée autrement plus tôt dans le coup).`; };
  const me = $('a-grid-me') || Object.assign(document.createElement('p'), { id: 'a-grid-me', className: 'grid-me' });
  me.setAttribute('aria-live', 'polite'); me.textContent = line(hand);
  $('a-grid').after(me);
  $('a-grid').onclick = (e) => { const c = e.target.closest('[data-h]'); if (c) me.textContent = line(c.dataset.h); };
  $('a-grid').setAttribute('aria-label', `Grille des 169 mains. ` + acts.map((a, j) => `${a.label_fr} : ${range.share_pct[j]} % des mains`).join(', ') + `. ${me.textContent}`);
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
    if (err.status !== 409) { notify(netMsg(err, "le signalement n'a pas été envoyé"), retryable(err) ? () => $('report-form').requestSubmit() : null); return; }   // 409 : déjà signalée
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
    ? s.errors.map((e) => `<li>${e.prompt_fr}<br>Joué : ${e.chosen} · Référence : <b>${e.best}</b> (${e.loss_fr || gainBB(e.regret_mbb)} de moins)</li>`).join('')
    : '<li>Aucune erreur sur cette série.</li>';
  $('s-review').hidden = !s.errors.length;
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
    for (const id of ['st-evolution', 'st-themes']) $(id).innerHTML = '';
    $('st-focus').className = 'focus none'; $('st-focus').innerHTML = '<p class="focus-title">À travailler maintenant</p><p>Joue une première série pour un diagnostic.</p>';
    $('st-note').textContent = ''; show('stats'); return;
  }
  $('st-score').innerHTML = `${pc(s.score_pct)}<small>${s.questions} questions · ${s.sessions} série${s.sessions > 1 ? 's' : ''}</small>`;
  $('st-evolution').innerHTML = s.evolution.length > 1
    ? s.evolution.map((e) => `<i style="height:${Math.max(4, e.score_pct)}%" title="${pc(e.score_pct)}"></i>`).join('')
    : '<span>L\'évolution s\'affiche après deux séries.</span>';
  const f = s.focus || { kind: 'none', reason_fr: '' };                // un seul diagnostic (même règle que les séries adaptées)
  $('st-focus').className = `focus ${f.kind}`;
  $('st-focus').innerHTML = `<p class="focus-title">À travailler maintenant</p>`
    + (f.label ? `<p><b>${f.label}</b></p>` : '') + `<p>${f.reason_fr}</p>`
    + (f.examples && f.examples[0] ? `<p class="note">Exemple : ${f.examples[0].replace(' Que fais-tu ?', '')}</p>` : '')
    + (f.filters ? '<button class="primary" id="train-focus">M\'entraîner sur ce thème</button>' : '');
  if (f.filters) $('train-focus').addEventListener('click', () => start(f.filters));
  $('st-themes').innerHTML = Object.entries(s.by).map(([k, rows]) =>
    `<div class="theme-group"><b>${DIM_FR[k]}</b>${rows.map((x) => themeRow(x, s.min_sample)).join('')}</div>`).join('');
  $('st-note').textContent = `Un score n'est affiché qu'à partir de ${s.min_sample} questions sur le thème. Tes données restent anonymes : elles sont liées à cet appareil, pas à ton identité.`;
  show('stats');
}

async function adaptation() {
  const modes = { gto: 'GTO', exploit: 'Exploitant' }; const parts = []; let first = null;   // le mode Field n'a pas de série adaptée
  for (const m of Object.keys(modes)) {
    let a; try { a = await api(`/users/me/adaptation?mode=${m}`); } catch (e) { continue; }       // mode sans dataset publié : ignoré
    first = first || a;
    const list = (xs, kind) => xs.map((x) => `<li>${x.label_fr} <small>${x.errors} erreur${x.errors > 1 ? 's' : ''} sur ${x.answers} · difficulté ${x.difficulty_pct} %</small></li>`).join('');
    if (a.review.length) parts.push(`<div class="adapt-mode"><b>${modes[m]}</b><p>En révision :</p><ul>${list(a.review)}</ul></div>`);   // à retravailler : bloc « À travailler maintenant »
  }
  if (!first) { $('st-adapt').hidden = true; return; }
  $('st-adapt').hidden = false; $('adapt-on').checked = first.enabled;
  $('adapt-rule').textContent = first.rule_fr + (first.since ? ` Réinitialisée le ${new Date(first.since).toLocaleDateString('fr-FR')}.` : '');
  $('adapt-themes').innerHTML = parts.join('');
}
$('adapt-on').addEventListener('change', async (e) => {
  try { await api('/users/me/preferences', { method: 'PUT', body: JSON.stringify({ adaptive: e.target.checked }) }); }
  catch (err) { e.target.checked = !e.target.checked; notify(netMsg(err, "le réglage n'a pas été enregistré")); }
});
$('adapt-reset').addEventListener('click', async () => {
  if (!confirmTwice($('adapt-reset'), 'Confirmer la réinitialisation (progression conservée)')) return;
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
$('lex-btn').addEventListener('click', () => openLex().catch((e) => notify(netMsg(e, "le lexique n'a pas pu s'ouvrir"))));
$('lex-close').addEventListener('click', closeLex);
$('lex').addEventListener('click', (e) => { if (e.target === $('lex')) closeLex(); });
$('lex-search').addEventListener('input', () => renderLex());
document.addEventListener('keydown', (e) => {
  if ($('lex').hidden) return;
  if (e.key === 'Escape') { closeLex(); return; }
  if (e.key !== 'Tab') return;                                       // fenêtre modale : le focus reste dans le lexique
  const f = [...$('lex').querySelectorAll('button, input, [href], [tabindex]:not([tabindex="-1"])')].filter((x) => !x.hidden && x.offsetParent !== null);
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
  else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
});

// ------------------------------------------------------------------ navigation
const openStats = () => stats().catch((e) => { loading(false); notify(netMsg(e, "ta progression n'a pas pu être chargée"), openStats); });
$('stats-btn').addEventListener('click', openStats);
$('st-back').addEventListener('click', home);
$('notice-close').addEventListener('click', () => { $('notice').hidden = true; });
$('st-export').addEventListener('click', async () => {              // droit d'accès et de portabilité : fichier JSON
  try {
    const data = await api('/users/me/export');
    const a = document.createElement('a'); a.download = 'spinsacademy-mes-donnees.json';
    a.href = URL.createObjectURL(new Blob([JSON.stringify(data, null, 1)], { type: 'application/json' }));
    document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  } catch (e) { notify(netMsg(e, "l'export n'a pas pu être préparé")); }
});
$('st-delete').addEventListener('click', async () => {
  if (!confirmTwice($('st-delete'), 'Confirmer : tout effacer définitivement')) return;
  await api('/users/me', { method: 'DELETE' }); store.del('sid'); stats();
});
$('quick-start').addEventListener('click', () => start({}));
$('review-btn').addEventListener('click', () => start({}, true));

// révision espacée : bouton quand des mains ratées sont arrivées à échéance (1, 3 puis 7 jours)
async function reviews() {
  $('review-btn').hidden = true; $('review-note').hidden = true;
  let r; try { r = await api(`/users/me/reviews?mode=${mode()}`); } catch (e) { return; }
  if (r.due > 0) {
    $('review-btn').textContent = `Revoir mes erreurs (${r.due} main${r.due > 1 ? 's' : ''} prête${r.due > 1 ? 's' : ''})`;
    $('review-btn').title = r.rule_fr; $('review-btn').hidden = false;
  } else if (r.pending > 0 && r.next_due_at) {
    const d = new Date(r.next_due_at);
    $('review-note').textContent = `Prochaine révision de tes erreurs : ${d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })} (${r.pending} main${r.pending > 1 ? 's' : ''}).`;
    $('review-note').hidden = false;
  }
}
const MODE_NOTE = { gto: 'Stratégie de référence, contre des adversaires qui jouent juste.',
  field: "Contre les joueurs du field Expresso, de 4 à 12 BB : le vilain inconnu est un rec passif ; ses statistiques observées (k sur n) disent s'il pousse ou paie trop. Profils tirés de l'expérience de coachs, pas des mesures.",
  exploit: "Contre des profils fictifs : payer ou non un tapis de joueurs qui poussent moins ou plus souvent qu'un joueur équilibré en push/fold (Serré, Prudent, Agressif, Maniaque), ou pousser contre un joueur qui paie trop (Station d'appel). Hypothèses de simulation, pas de vrais joueurs." };
const FAMILIES_OF = { gto: ['', 'first_in', 'vs_limp', 'vs_raise', 'vs_allin'], exploit: ['', 'vs_allin', 'first_in'],    // calls de tapis et tapis du SB
  field: ['', 'first_in', 'vs_allin', 'read'] };                    // field : tapis, calls de tapis, lecture du vilain
const DEPTHS_OF = { gto: ['', '0-9', '10-16', '17-25'], exploit: ['', '0-9', '10-16', '17-25'], field: ['', '0-9', '10-16'] };   // field : 4 à 12 BB
document.querySelector('.mode-switch').addEventListener('click', () => {
  reviews();
  $('mode-note').textContent = MODE_NOTE[mode()]; $('profile-filter').hidden = mode() !== 'exploit';
  for (const [name, allowed] of [['family', FAMILIES_OF[mode()]], ['depth', DEPTHS_OF[mode()]]]) {
    const grp = document.querySelector(`.chips[data-name="${name}"]`);
    for (const b of grp.querySelectorAll('button')) {
      const off = !allowed.includes(b.dataset.value);
      b.setAttribute('aria-disabled', String(off));
      if (off && b.getAttribute('aria-pressed') === 'true') { b.setAttribute('aria-pressed', 'false'); grp.querySelector('[data-value=""]').setAttribute('aria-pressed', 'true'); }
    }
  }
});
$('custom-start').addEventListener('click', () => start(filters()));
$('report-form').addEventListener('submit', sendReport);
const goNext = () => next().catch((e) => { loading(false); notify(netMsg(e, "la question suivante n'a pas pu être chargée"), goNext); });
$('next-btn').addEventListener('click', goNext);
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
  $('resume').hidden = true; reviews();
  if (!sid) return;
  try {
    const s = await api(`/sessions/${encodeURIComponent(sid)}/summary`);
    if (!s.complete) $('resume').hidden = false; else store.del('sid');
  } catch (e) { store.del('sid'); }
}
home();

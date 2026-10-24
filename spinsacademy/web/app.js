'use strict';
// Interface mobile du quiz : consomme l'API /sessions, /quiz/next, /attempts, /sessions/{id}/summary.
const $ = (id) => document.getElementById(id);
const SUIT = { '♠': 's', '♥': 'h', '♦': 'd', '♣': 'c' };
const SUIT_NAME = { s: 'pique', h: 'cœur', d: 'carreau', c: 'trèfle' };
const BLINDS = { 3: [0, 0.5, 1], 2: [0.5, 1] };
const VERDICT = { 'correct': ['correct', 'Bonne réponse'], 'imprécision': ['imprecision', 'Imprécision'], 'erreur': ['erreur', 'Erreur'] };
const state = { sid: null, q: null, index: 0, size: 5, busy: false };
// A' : écran tactile sans souris : pas de raccourcis clavier affichés (certains téléphones annoncent un survol)
if ((navigator.maxTouchPoints || 0) > 0 && !matchMedia('(pointer: fine)').matches) document.documentElement.classList.add('touch');
addEventListener('touchstart', () => document.documentElement.classList.add('touch'), { once: true, passive: true });

const store = {
  get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* stockage indisponible : rien à faire */ } },
  del(k) { try { localStorage.removeItem(k); } catch (e) { /* idem */ } },
};
const bb = (x) => String(Math.round(x * 100) / 100).replace('.', ',');

// pastilles (lot 1) : la couleur que le joueur donne à chaque profil, comme dans son client ; une lettre pour les daltoniens
const PROFILES = ['Rec passif', 'Calling station', 'Dégène', 'Nit', 'Reg'];
const PAST_LETTER = { 'Rec passif': 'P', 'Calling station': 'S', 'Dégène': 'D', 'Nit': 'N', 'Reg': 'R' };
const PALETTE = ['#e5484d', '#f76b15', '#f5c518', '#30a46c', '#0091ff', '#8e4ec6', '#e93d82', '#8b8d98'];
const PALETTE_FR = { '#e5484d': 'rouge', '#f76b15': 'orange', '#f5c518': 'jaune', '#30a46c': 'vert', '#0091ff': 'bleu', '#8e4ec6': 'violet', '#e93d82': 'rose', '#8b8d98': 'gris' };
const PAST_DEFAULT = { 'Rec passif': '#f5c518', 'Calling station': '#e5484d', 'Dégène': '#f76b15', 'Nit': '#0091ff', 'Reg': '#8b8d98' };
function pastilles() { try { return { ...PAST_DEFAULT, ...JSON.parse(store.get('pastilles') || '{}') }; } catch (e) { return { ...PAST_DEFAULT }; } }
const inkOn = (hex) => { const v = parseInt(hex.slice(1), 16), l = 0.299 * (v >> 16) + 0.587 * ((v >> 8) & 255) + 0.114 * (v & 255); return l > 150 ? '#111' : '#fff'; };
function pastilleDot(label) {
  if (!PROFILES.includes(label)) return '';
  const c = pastilles()[label];
  return `<i class="pastille" style="--p:${c};--pi:${inkOn(c)}" aria-hidden="true">${PAST_LETTER[label]}</i>`;
}
function renderPastilles() {
  const p = pastilles();
  $('past-rows').innerHTML = PROFILES.map((name) => `<div class="past-row"><span>${pastilleDot(name)} ${name}</span><span class="swatches" role="group" aria-label="Couleur : ${name}">`
    + PALETTE.map((c) => `<button type="button" class="swatch" style="--p:${c}" data-name="${name}" data-color="${c}" aria-pressed="${p[name] === c}" aria-label="${PALETTE_FR[c]}"></button>`).join('')
    + '</span></div>').join('');
}
const gainBB = (mbb) => { const a = Math.abs(mbb);                 // gains toujours en BB ; 3 décimales autour de 0,06 BB (limite d'imprécision)
  return a < 20 ? '<0,02 BB' : Math.abs(a - 60) < 5 ? (a / 1000).toFixed(3).replace('.', ',') + ' BB' : bb(a / 1000) + ' BB'; };
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
const netMsg = (e, what) => (e && e.status >= 500 ? `Le serveur ne répond pas : ${what}. Ce n'est pas ta connexion ; réessaie dans un instant.`   // A' : panne serveur ≠ coupure réseau
  : e && e.status ? e.message
  : navigator.onLine === false ? `Pas de réseau : ${what}. Vérifie ta connexion, puis réessaie.`
  : `Le serveur est injoignable : ${what}. Vérifie ta connexion ou réessaie dans un instant.`);
const retryable = (e) => !e || !e.status || e.status === 429 || e.status >= 500;                 // coupure réseau ou trop de requêtes : « Réessayer »
function confirmTwice(btn, question) {                              // 1er appui : demande ; 2e appui dans les 5 s : confirme
  if (btn.dataset.armed) { clearTimeout(btn._t); delete btn.dataset.armed; btn.textContent = btn.dataset.label; return true; }
  btn.dataset.label = btn.dataset.label || btn.textContent; btn.dataset.armed = '1'; btn.textContent = question;
  btn._t = setTimeout(() => { delete btn.dataset.armed; btn.textContent = btn.dataset.label; }, 5000);
  return false;
}
function progress(text) { $('progress').textContent = text || ''; }

// ------------------------------------------------------------------ accueil
function mode() { return document.querySelector('.mode-switch [aria-pressed="true"]').dataset.value; }   // gto ou exploit (joueurs du field)
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
  if (state.starting) return; state.starting = true;                 // A' : un double appui ne lance pas deux séries
  $('home-error').hidden = true; loading(true);
  try {
    const s = await api('/sessions', { method: 'POST', body: JSON.stringify({ mode: f.mode || mode(), review, filters: Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode')) }) });
    state.sid = s.session_id; state.size = s.size; state.mode = s.mode; store.set('sid', s.session_id);
    state.filters = review ? (state.filters || {}) : Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode'));   // A1 : « Nouvelle série » les reprend
    store.set('filters', JSON.stringify(state.filters));
    await next();
  } catch (e) {
    loading(false); $('home-error').textContent = e.status === 422 ? 'Pas assez de situations pour ce thème : élargis les filtres.'
      : e.status && e.status < 500 ? e.message : netMsg(e, "la série n'a pas pu démarrer");            // jamais « Failed to fetch »
    $('filters').open = true; $('home-error').hidden = false;
    $('home-error').scrollIntoView({ block: 'center' }); $('home-error').focus({ preventScroll: true });
  } finally { state.starting = false; }
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

// lot 1 (table du client) : l'action sous le joueur, la mise en chiffres devant lui, le tapis restant, le bouton D
const ACT_TAG = { fold: 'FOLD', check: 'CHECK', limp: 'CALL', call: 'CALL', call_allin: 'CALL', raise: 'RAISE', allin: 'ALL-IN' };
const HUD_FR = { shove_pct: 'Tapis', call_pct: 'Call tapis', call_pct_bb_sb_fold: 'Call tapis', limp_pct: 'Limp', call_after_limp_pct: 'Call tapis après limp',
  jam_over_limp_pct: 'Tapis sur limp', open_pct: 'Open', defend_pct: 'Défense' };
function lastActions(q) {
  const last = {};
  for (const h of q.history) last[h.position] = h.action;
  return last;
}

function renderTable(q) {
  const view = $('table-view'); view.innerHTML = '';
  const n = q.players.length, hero = q.players.indexOf(q.hero), { c, folded } = contributions(q), last = lastActions(q);
  view.classList.toggle('hu', n === 2);
  const seats = n === 3 ? [[50, 0], [21, 5], [79, 5]] : [[50, 0], [50, 4]];          // héros en bas (placé à part), adversaires en haut
  const button = n === 3 ? 'BTN' : 'SB';                                                // en heads-up, le SB a le bouton
  const hud = hudLines(q);
  for (let k = 0; k < n; k++) {
    const i = (hero + k) % n, pos = q.players[i], left = q.stacks_bb[i] - c[i];
    const covers = last[pos] === 'allin' && left > 1e-9;                     // il pousse plus que ton tapis : il te couvre
    const act = left <= 1e-9 ? '' : covers ? 'ALL-IN · te couvre' : ACT_TAG[last[pos]] || '';   // tapis : « ALL-IN » à la place du tapis restant
    const stack = left <= 1e-9 ? 'ALL-IN' : `${bb(left)} BB`;
    if (k === 0) {
      $('hero-seat').innerHTML = `<b>${pos} · toi</b><span class="stack">${stack}</span>` + (act ? `<span class="act a-${last[pos]}">${act}</span>` : '');   // ton action, comme pour les autres
    } else {
      const seat = document.createElement('div');
      seat.className = 'seat' + (folded[i] ? ' folded' : '');
      seat.style.left = seats[k][0] + '%'; seat.style.top = seats[k][1] + '%';
      const backs = !folded[i] ? '<span class="backs"><i></i><i></i></span>' : '';           // cartes cachées des adversaires encore dans le coup
      seat.innerHTML = backs + `<b>${pos}</b><span class="stack">${stack}</span>` + (act ? `<span class="act a-${last[pos]}">${act}</span>` : '')
        + (hud[pos] ? `<span class="hud">${hud[pos]}</span>` : '') + (c[i] > 0 ? `<span class="betnum">${bb(c[i])}</span>` : '');   // sa mise, devant lui
      view.appendChild(seat);
    }
    if (k === 0 && c[i] > 0) {
      const b = document.createElement('span'); b.className = 'betnum hero-bet'; b.textContent = bb(c[i]); view.appendChild(b);
    }
    if (pos === button) {
      const d = document.createElement('span'); d.className = 'dealer'; d.textContent = 'D'; d.title = 'Bouton';
      const [x, y] = k === 0 ? [72, 84] : [seats[k][0] + (seats[k][0] < 50 ? 17 : seats[k][0] > 50 ? -17 : 17), seats[k][1] + 8];
      d.style.left = x + '%'; d.style.top = y + '%'; view.appendChild(d);
    }
  }
  const pot = document.createElement('div'); pot.className = 'pot'; pot.innerHTML = `<small>Pot total</small>${bb(q.pot_bb)} BB`; view.appendChild(pot);
}

// stats du vilain en une ligne sous son siège (comme le HUD du client) ; le détail (observé / théorie) se déplie sous la table
// arrondi « au pair » comme l'énoncé et la correction (12,5 % -> 12 %), pour que les chiffres concordent
const rnd0 = (x) => { const f = Math.floor(x), d = x - f; return d > 0.5 + 1e-9 ? f + 1 : d < 0.5 - 1e-9 ? f : (f % 2 === 0 ? f : f + 1); };
function hudLines(q) {
  const f = q.field, out = {};
  if (!f || !q.hand || f.ask_fr) return out;
  const main = (f.villains || [])[0];
  if (!f.stats.length) { if (main) out[main] = 'Inconnu'; return out; }
  for (const s of f.stats) {                                            // une ligne par stat : observé, théorie et échantillon (k/n)
    const who = s.stat === 'call_pct_bb_sb_fold' ? 'BB' : main;
    const line = `<span class="hl"><b>${HUD_FR[s.stat] || s.label_fr} ${rnd0(s.observed_pct)} %</b> <small>th. ${rnd0(s.gto_pct)} % · ${s.k}/${s.n}</small></span>`;
    out[who] = (out[who] || '') + line;
  }
  return out;
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

// bouton d'action : le montant en gros, le verbe du client en dessous (« 0,5 BB / CALL »), comme à la table
const VERB_RE = /^(FOLD|CHECK|CALL|RAISE TO|ALL-IN)(?: (.+))?$/i;
function actionHTML(label) {
  const m = VERB_RE.exec(label);
  if (!m) return `${pastilleDot(label)}<b>${escT(label)}</b>`;
  return m[2] ? `<b>${escT(m[2])}</b><small>${m[1].toUpperCase()}</small>` : `<b>${m[1].toUpperCase()}</b>`;
}

function renderQuestion(data) {
  state.q = data.question; state.index = data.question_index; state.size = data.size;
  $('purpose').hidden = !data.purpose_fr; $('purpose').textContent = data.purpose_fr || '';
  $('purpose').className = `purpose ${data.purpose || ''}`;
  const q = state.q;
  progress(`Question ${state.index + 1} / ${state.size}`);
  const noHand = !q.hand || !!(q.field && q.field.ask_fr);           // questions de lecture du vilain : sans main ni table
  $('table-wrap').hidden = noHand;
  if (!noHand) { renderTable(q); renderCards(q.hand_display); }
  $('history').innerHTML = q.history_fr.length ? q.history_fr.map((t) => `<li>${t}</li>`).join('') : '<li>Tu parles en premier</li>';   // lecteurs d'écran
  const fmt = q.table === '3-handed' ? '3 joueurs' : 'Heads-up';
  $('seat-line').hidden = noHand; $('seat-line').innerHTML = `Tu es au <b>${q.hero}</b> · ${fmt}`;
  $('prompt-full').textContent = q.prompt_fr;                        // énoncé complet pour les lecteurs d'écran
  $('ask').className = noHand ? 'ask' : 'ask sr-only';               // la table suffit ; la question reste lue par les lecteurs d'écran
  $('ask').innerHTML = !noHand ? `Avec ${q.hand_display.replace(/([♠♥♦♣])/g, (m) => `<span class="suit-${SUIT[m]}">${m}︎</span>`)}, que fais-tu ?` : escT(q.field.ask_fr);
  $('kbd-hint').textContent = `Raccourcis clavier : touches 1 à ${q.options.length}.`;
  renderFieldStats(q, noHand);
  const box = $('actions'); box.innerHTML = '';
  const main = document.createElement('div'); main.className = 'mainrow';
  const extra = document.createElement('div'); extra.className = 'presets';           // au-delà de trois actions : colonne à droite, au-dessus
  const read = noHand; box.classList.toggle('read', read);
  q.options.forEach((o, k) => {
    const b = document.createElement('button');
    b.innerHTML = actionHTML(o.label_fr) + `<span class="key">${k + 1}</span>`; b.dataset.id = o.id; b.dataset.k = k + 1;
    if (/^Fold$/.test(o.label_fr)) b.classList.add('fold');
    b.addEventListener('click', () => answer(o.id));
    (read || k < 3 ? main : extra).appendChild(b);
  });
  main.style.setProperty('--n', String(main.children.length));
  box.appendChild(main); if (extra.children.length) box.appendChild(extra);
  show('question');
  box.querySelector('button').focus({ preventScroll: true });
}

// mode exploitant : la ligne de stats est sous le siège du vilain ; ici, le détail (k sur n, observé contre théorie), replié.
// Jamais son profil interne. Questions de lecture : le contexte et les stats restent affichés en entier.
function renderFieldStats(q, noHand) {
  const f = q.field, box = $('villain');
  box.hidden = !f; if (!f) return;
  const context = noHand ? q.prompt_fr.split('\n').filter((l) => !/^Sur \d+ occasions|\?$/.test(l)).join(' ') : '';
  const bars = f.stats.map((s) => {
    const top = Math.min(100, Math.max(s.observed_pct, s.gto_pct) * 1.15), w = (x) => (100 * x / top).toFixed(1) + '%';
    return `<p class="vstat">${s.label_fr} : ${s.k} sur ${s.n}</p>`
      + `<div class="vbar obs"><span>Observé</span><em><i style="width:${w(s.observed_pct)}"></i></em><b>${bb(s.observed_pct)} %</b></div>`
      + `<div class="vbar gto"><span>Théorie</span><em><i style="width:${w(s.gto_pct)}"></i></em><b>${bb(s.gto_pct)} %</b></div>`;
  }).join('');
  const body = (context ? `<p class="fnone">${escT(context)}</p>` : '')
    + (f.stats.length ? bars + `<p class="fn">${f.observations} occasions : plus il y en a, plus la tendance est fiable.</p>`
      : `<p class="fnone">Aucune information sur ce vilain : compte sur le profil le plus fréquent du field (rec passif).</p>`);
  box.className = 'fstats';
  box.innerHTML = noHand ? `<span class="ftype">${f.type_fr}</span>` + body
    : `<details class="vdetails"><summary><span class="ftype">${f.type_fr}</span> ${f.observations ? `Stats du vilain · ${f.observations} mains` : 'Aucune information'}</summary>${body}</details>`;
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
    if (!e.status) console.error(e);                              // erreur d'affichage : visible dans la console
    for (const b of $('actions').querySelectorAll('button')) b.disabled = false;
    notify(netMsg(e, "ta réponse n'a pas été enregistrée"), retryable(e) ? () => answer(id) : null);
  } finally { state.busy = false; }
}

function renderAnswer(r) {
  const [cls, title] = VERDICT[r.verdict];
  const v = $('a-verdict'); v.className = `verdict ${cls}`;
  const many = (r.good_labels || []).length > 1 && (r.good_actions || []).includes(r.chosen_action);
  const mixPct = ((r.strategy.find((x) => x.chosen) || {}).pct || 0);
  const short = (l) => l.replace(/ \(.*\)$/, '');                     // « Tapis », pas « Tapis (12 BB) » dans la phrase courte
  const sub = r.field && r.field.read ? (r.chosen_label === r.best_label ? `Bonne lecture : ${pastilleDot(r.best_label)}${r.best_label}.` : `La bonne lecture : ${pastilleDot(r.best_label)}${r.best_label}.`)
    : many ? 'Ton choix fait partie des bons coups.'
    : r.chosen_label === r.best_label ? `Le bon coup : ${r.best_label}.`
    : r.verdict === 'correct' && !r.field && mixPct > 0 ? `La théorie joue aussi ce coup (${mixPct} % du temps).`   // A5 : stratégie mixte
    : r.verdict === 'correct' ? `Presque aussi bon que le meilleur coup : ${short(r.best_label)}.`
    : `Le bon coup : ${r.best_label}.${r.loss_fr ? ` Ton choix coûte ${r.loss_fr}.` : ''}`;   // message essentiel : le bon coup, le coût
  v.innerHTML = title + `<small>${sub}</small>`;
  renderCards(state.q.hand_display, 'a-cards'); $('a-cards').hidden = !state.q.hand || !!(state.q.field && state.q.field.ask_fr);
  $('a-choice').hidden = true;                                       // ton choix et son coût sont dans l'explication (pas de redite)
  $('a-strategy-title').textContent = r.gto_label ? `Contre ce joueur : ${r.best_label} · contre un joueur GTO : ${r.gto_label}` : 'Stratégie de référence';
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}${s.chosen ? ' mine' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  const fd = r.field; $('a-exploit').hidden = !fd;
  for (const id of ['a-strategy-title', 'a-strategy']) $(id).hidden = !!fd;         // exploitant : correction courte
  if (fd) {
    $('a-exploit').innerHTML = `<div class="ref"><dt>${fd.read ? 'Bonne lecture' : 'Contre ce vilain'}${fd.gain_fr ? `<span class="conf net">${fd.gain_fr} de plus que la théorie</span>` : ''}</dt><dd>${escT(r.best_label)}</dd></div>`
      + (fd.gto_label ? `<div><dt>En théorie</dt><dd>${escT(fd.gto_label)}</dd></div>` : '')
      + (fd.evs.length ? `<div><dt>Gain par rapport au fold <small>(ajusté à ce vilain)</small></dt><dd>${fd.evs.map((e) => `${escT(e.label_fr)} : ${e.ev_fr}`).join('\n')}</dd></div>` : '')
      + `<p class="note">${fd.type_fr}</p>`;
  }
  // d'abord l'essentiel (une phrase, puis la règle à retenir), ensuite les précisions, repliées
  $('a-essential').textContent = r.essential_fr || '';
  const rem = (r.remember_fr || '').replace(/^À retenir : /, '');
  $('a-remember').hidden = !rem; $('a-remember').innerHTML = rem ? `<b>À retenir</b><span class="eline">${escT(rem.charAt(0).toUpperCase() + rem.slice(1))}</span>` : '';
  const det = r.details_fr || []; $('a-more').open = false;
  $('a-details').innerHTML = det.map((l) => `<p class="eline">${escT(l)}</p>`).join('');
  $('a-recap').textContent = state.q.prompt_fr.replace(' Que fais-tu ?', '').replace(/\n(Quelle pastille lui donnes-tu|Quel est le défaut de ce vilain) \?$/, '');
  renderNext(r.next);
  $('a-grid-box').hidden = !r.range; $('a-grid-box').open = false; if (r.range) renderGrid(r.range, state.q.hand, false);
  $('next-btn').textContent = state.index + 1 >= state.size ? 'Voir le bilan' : 'Question suivante';
  resetReport();
  for (const id of ['a-essential', 'a-remember', 'a-details', 'a-next']) glossify($(id));    // A7 : définition au toucher des mots du lexique
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
    + list(n.plan, 'plan', n.plan_fr || 'Ton plan') + list(n.forces, 'plus', n.plus_fr || 'Forces') + list(n.weaknesses, 'minus', n.minus_fr || 'Faiblesses');
  $('a-next-title').textContent = n.title_fr || 'Potentiel de la main au flop';
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
    ? s.errors.map((e) => `<li><em class="vtag ${e.verdict === 'erreur' ? 'bad' : 'warn'}">${e.verdict === 'erreur' ? 'Erreur' : 'Imprécision'}</em> ${e.prompt_fr}<br>Ton coup : ${e.chosen} (coûte ${e.loss_fr || gainBB(e.regret_mbb)}) · Meilleur coup : <b>${e.best}</b></li>`).join('')
    : '<li>Rien à revoir sur cette série.</li>';
  $('s-review').hidden = !s.errors.length;
  show('summary');
  refreshStats();                                                    // la progression hors connexion suit la dernière série
}

// ------------------------------------------------------------------ progression
const DIM_FR = { mode: 'Mode', family: 'Situation', hero: 'Position', table: 'Format', depth: 'Profondeur' };
function themeRow(x, min) {
  const cls = !x.reliable ? ' unreliable' : x.score_pct < 40 ? ' low' : x.score_pct < 60 ? ' mid' : '';   // A' : rouge sous 40 %, orange de 40 à 60 %
  if (!x.reliable) {                                                // A8 : pas de barre vide, qui se lit comme un zéro
    const need = Math.max(min - x.questions, 1);
    return `<div class="trow unreliable"><span>${x.label}</span><span>encore ${need} question${need > 1 ? 's' : ''} pour un score</span></div>`;
  }
  return `<div class="trow${cls}"><span>${x.label}</span><span>${pc(x.score_pct)}</span><div class="sbar"><i style="width:${x.score_pct}%"></i></div></div>`;
}
// progression hors connexion : la dernière progression reçue est gardée sur l'appareil et réaffichée, datée, si le réseau
// ou le serveur manque ; elle se met à jour à chaque ouverture en ligne et à la fin de chaque série
const STATS_KEY = 'stats_cache';
function cacheStats(s) { store.set(STATS_KEY, JSON.stringify({ at: new Date().toISOString(), s })); }
function cachedStats() { try { return JSON.parse(store.get(STATS_KEY) || 'null'); } catch (e) { return null; } }
function refreshStats() { api('/users/me/stats').then(cacheStats).catch(() => { /* hors ligne : on garde la dernière */ }); }

async function stats() {
  loading(true);
  let s, offline = null;
  try { s = await api('/users/me/stats'); cacheStats(s); }
  catch (e) {
    const c = (!e || !e.status || e.status >= 500) ? cachedStats() : null;      // coupure réseau ou panne du serveur
    if (!c) throw e;
    s = c.s; offline = c.at;
  }
  progress('');
  const when = offline && new Date(offline);
  $('st-offline').hidden = !offline;
  if (offline) {
    $('st-offline').textContent = `Hors connexion : ta progression au ${when.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })} `
      + `à ${when.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}. Elle se mettra à jour dès que la connexion reviendra.`;
  }
  for (const id of ['st-export', 'st-delete']) $(id).hidden = !!offline;   // ces actions demandent le serveur
  if (offline) $('st-adapt').hidden = true; else await adaptation();
  $('st-adapt-title').hidden = $('st-adapt').hidden;                // pas de titre sans le bloc
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
    + (f.filters && !offline ? '<button class="primary" id="train-focus">M\'entraîner sur ce thème</button>' : '');
  if (f.filters && !offline) $('train-focus').addEventListener('click', () => start(f.filters));
  const groups = Object.entries(s.by).filter(([, rows]) => rows.length);          // pas de carte vide
  const old = s.untracked_questions || 0;                                         // démo : réponses d'une version précédente, sans description
  $('st-themes').innerHTML = groups.map(([k, rows]) =>
    `<div class="theme-group"><b>${DIM_FR[k]}</b>${rows.map((x) => themeRow(x, s.min_sample)).join('')}</div>`).join('')
    + (old ? `<p class="note">${old} réponse${old > 1 ? 's' : ''} d'une version précédente de la démo compte${old > 1 ? 'nt' : ''} dans ton score, mais pas par thème : `
      + `elles ont été enregistrées sans leur situation. ${groups.length ? 'Les thèmes ci-dessus viennent de tes séries récentes.' : 'Le détail par thème commence avec ta prochaine série.'}</p>` : '')
    + (!groups.length && !old ? '<p class="note">Le détail par thème s\'affiche après ta première série.</p>' : '');
  $('st-note').textContent = `Un score n'est affiché qu'à partir de ${s.min_sample} questions sur le thème. Tes données restent anonymes : elles sont liées à cet appareil, pas à ton identité.`;
  show('stats');
}

async function adaptation() {
  const modes = { gto: 'GTO' }; const parts = []; let first = null;   // pas de série adaptée en mode exploitant
  for (const m of Object.keys(modes)) {
    let a; try { a = await api(`/users/me/adaptation?mode=${m}`); } catch (e) { continue; }       // mode sans dataset publié : ignoré
    first = first || a;
    const list = (xs, kind) => xs.map((x) => `<li>${x.label_fr} <small>${x.errors} erreur${x.errors > 1 ? 's' : ''} sur ${x.answers}</small></li>`).join('');
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
    + `<h3>Tout le lexique</h3>${groups}<p class="note">${L.note_fr}</p>`;
}
let lexReturn = null;
// A7 : dans la correction, les mots techniques s'expliquent au toucher (première occurrence de chaque terme)
const GLOSS = { 'Range': ['range'], 'Équité': ['équité'], 'Cote du pot': ['cote du pot', 'la cote'], 'SPR (rapport tapis / pot)': ['SPR'],
  'Fold equity': ['fold equity'], 'Limp (compléter)': ['limp', 'limps'], 'Isoler (iso)': ['iso'], 'Rec passif': ['rec passif'],
  'Tapis effectif': ['tapis effectif'], 'Stratégie mixte': ['stratégie mixte'], 'Paire max (top pair)': ['paire max'], 'Kicker': ['kicker'], 'Read': ['read'] };
async function glossify(root) {
  let L; try { L = await lexique(); } catch (e) { return; }                 // lexique indisponible : texte brut
  const terms = L.terms.filter((t) => GLOSS[t.term]).map((t) => ({ ...t, re: new RegExp(`(?<![\\p{L}\\d])(?:${GLOSS[t.term].join('|')})(?![\\p{L}\\d])`, 'iu') }));
  const done = new Set();
  const wrap = (tn) => {
    for (const t of terms) {
      if (done.has(t.term)) continue;
      const m = t.re.exec(tn.data); if (!m) continue;
      done.add(t.term);
      const after = tn.splitText(m.index); after.data = after.data.slice(m[0].length);
      const b = document.createElement('button'); b.type = 'button'; b.className = 'term'; b.textContent = m[0];
      b.dataset.def = t.def; b.setAttribute('aria-expanded', 'false');
      tn.parentNode.insertBefore(b, after); wrap(after); return;
    }
  };
  const walk = (node) => { for (const c of [...node.childNodes]) { if (c.nodeType === 3) wrap(c); else if (c.nodeType === 1 && !c.matches('button, .term-def')) walk(c); } };
  walk(root);
}
document.addEventListener('click', (e) => {
  const b = e.target.closest('button.term'); if (!b) return;
  if (b._def) { b._def.remove(); b._def = null; b.setAttribute('aria-expanded', 'false'); return; }
  const box = document.createElement('div'); box.className = 'term-def'; box.textContent = `${b.textContent} : ${b.dataset.def}`;
  const block = b.closest('.eline, li, p, dd') || b.parentNode;               // A' : sous la phrase, jamais au milieu
  (block.matches('.eline, li, p, dd') ? block : b).after(box); b._def = box; b.setAttribute('aria-expanded', 'true');
});

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
  await api('/users/me', { method: 'DELETE' }); store.del('sid'); store.del(STATS_KEY); stats();
});
$('quick-start').addEventListener('click', () => start({}));
$('review-btn').addEventListener('click', () => start({}, true));

// révision espacée : bouton quand des mains ratées sont arrivées à échéance (1, 3 puis 7 jours)
async function reviews() {
  $('review-btn').hidden = true; $('review-note').hidden = true;
  let r; try { r = await api(`/users/me/reviews?mode=${mode()}`); } catch (e) { return; }
  if (r.due > 0) {
    $('review-btn').textContent = `Revoir mes mains (${r.due} main${r.due > 1 ? 's' : ''} prête${r.due > 1 ? 's' : ''})`;
    $('review-btn').title = r.rule_fr; $('review-btn').hidden = false;
  } else if (r.pending > 0 && r.next_due_at) {
    const d = new Date(r.next_due_at);
    $('review-note').textContent = `Prochaine révision de tes mains à revoir : ${d.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })} (${r.pending} main${r.pending > 1 ? 's' : ''}).`;
    $('review-note').hidden = false;
  }
}
const MODE_NOTE = { gto: 'La stratégie théorique, contre des joueurs qui jouent juste.',
  exploit: "Contre les vrais joueurs d'Expresso (4 à 25 BB). Sans info, le vilain est un joueur passif. Ses stats te disent s'il pousse, relance, limpe ou paie trop." };
const FAMILIES_OF = { gto: ['', 'first_in', 'vs_limp', 'vs_raise', 'vs_allin'], exploit: ['', 'first_in', 'vs_limp', 'vs_raise', 'vs_allin', 'read'] };
const DEPTHS_OF = { gto: ['', '0-9', '10-16', '17-25'], exploit: ['', '0-9', '10-16', '17-25'] };   // v4.5 : exploitant de 4 à 25 BB
function onMode() {
  store.set('mode', mode());                                         // gardé après un rechargement
  reviews();
  $('mode-note').textContent = MODE_NOTE[mode()];
  for (const [name, allowed] of [['family', FAMILIES_OF[mode()]], ['depth', DEPTHS_OF[mode()]]]) {
    const grp = document.querySelector(`.chips[data-name="${name}"]`);
    for (const b of grp.querySelectorAll('button')) {
      const off = !allowed.includes(b.dataset.value);
      b.setAttribute('aria-disabled', String(off));
      if (off && b.getAttribute('aria-pressed') === 'true') { b.setAttribute('aria-pressed', 'false'); grp.querySelector('[data-value=""]').setAttribute('aria-pressed', 'true'); }
    }
  }
}
document.querySelector('.mode-switch').addEventListener('click', onMode);
$('custom-start').addEventListener('click', () => start(filters()));
$('report-form').addEventListener('submit', sendReport);
const goNext = () => next().catch((e) => { loading(false); notify(netMsg(e, "la question suivante n'a pas pu être chargée"), goNext); });
$('next-btn').addEventListener('click', goNext);
$('again-btn').addEventListener('click', () => {                 // A1 : même mode, mêmes filtres
  let f = state.filters; if (!f) { try { f = JSON.parse(store.get('filters') || '{}'); } catch (e) { f = {}; } }
  start({ ...f, mode: state.mode || mode() });
});
$('back-home').addEventListener('click', home);
$('home-btn').addEventListener('click', home);
$('resume').addEventListener('click', () => { state.sid = store.get('sid'); next().catch(home); });
document.addEventListener('keydown', (e) => {
  if ($('screen-question').hidden || !$('lex').hidden || e.altKey || e.ctrlKey || e.metaKey) return;
  const b = $('actions').querySelector(`button[data-k="${Number(e.key)}"]`);
  if (b) b.click();
});

async function home() {
  progress(''); show('home');
  const sid = store.get('sid');
  $('resume').hidden = true; reviews();
  if (!sid) return;
  try {
    const s = await api(`/sessions/${encodeURIComponent(sid)}/summary`);
    if (!s.complete) $('resume').hidden = false; else store.del('sid');
  } catch (e) { if (e && e.status && e.status < 500) store.del('sid'); }     // hors ligne : la série en cours reste reprenable
}
$('past-rows').addEventListener('click', (e) => {
  const b = e.target.closest('.swatch'); if (!b) return;
  const p = pastilles(); p[b.dataset.name] = b.dataset.color; store.set('pastilles', JSON.stringify(p)); renderPastilles();
});
renderPastilles();
// test joueurs du 24/10 : le mode et le thème choisis restent après un rechargement
(function restoreHome() {
  const m = store.get('mode'); const btn = m && document.querySelector(`.mode-switch [data-value="${m}"]`);
  if (btn) { for (const b of document.querySelectorAll('.mode-switch [data-value]')) b.setAttribute('aria-pressed', String(b === btn)); }
  let f = {}; try { f = JSON.parse(store.get('filters') || '{}') || {}; } catch (e) { f = {}; }
  const want = { family: f.family, hero: f.hero, table: f.table, depth: f.min_stack !== undefined ? `${f.min_stack}-${f.max_stack - 0.5}` : undefined };
  for (const [name, v] of Object.entries(want)) {
    const grp = document.querySelector(`.chips[data-name="${name}"]`); const b = v && grp && grp.querySelector(`[data-value="${v}"]`);
    if (b) for (const x of grp.querySelectorAll('button')) x.setAttribute('aria-pressed', String(x === b));
  }
  onMode();
}());
home();

// l'application s'ouvre aussi sans connexion (service worker) ; pas dans la démo autonome, qui est déjà une seule page
const canSW = 'serviceWorker' in navigator && !window.SA_LEXIQUE
  && (location.protocol === 'https:' || ['localhost', '127.0.0.1'].includes(location.hostname));
if (canSW) addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => { /* navigateur sans service worker : en ligne seulement */ }));

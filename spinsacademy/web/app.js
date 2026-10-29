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
const PAST_LETTER = { 'Rec passif': 'P', 'Calling station': 'S', 'Dégène': '!', 'Nit': 'N', 'Reg': 'R' };   // pas de « D » : c'est le bouton
const PALETTE = ['#e5484d', '#f76b15', '#f5c518', '#30a46c', '#0091ff', '#8e4ec6', '#e93d82', '#8b8d98'];
const PALETTE_FR = { '#e5484d': 'rouge', '#f76b15': 'orange', '#f5c518': 'jaune', '#30a46c': 'vert', '#0091ff': 'bleu', '#8e4ec6': 'violet', '#e93d82': 'rose', '#8b8d98': 'gris' };
const PAST_DEFAULT = { 'Rec passif': '#f5c518', 'Calling station': '#e5484d', 'Dégène': '#f76b15', 'Nit': '#0091ff', 'Reg': '#8e4ec6' };   // analyse des écrans : plus de gris, réservé à « pas de pastille »
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
  if (name !== 'question' && state.timer) stopTimer();
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
const closed = (e) => !!(e && e.status === 503 && /aucun dataset publié/.test(e.message));   // test joueurs 6 : rien en ligne, réessayer ne sert à rien
const netMsg = (e, what) => (closed(e) ? `L'entraînement n'est pas ouvert sur ce serveur : ${what}, aucune banque de questions n'est en ligne. Réessayer ne changera rien : préviens l'équipe.`
  : e && e.status >= 500 ? `Le serveur ne répond pas : ${what}. Ce n'est pas ta connexion ; réessaie dans un instant.`   // A' : panne serveur ≠ coupure réseau
  : e && e.status ? e.message
  : navigator.onLine === false ? `Pas de réseau : ${what}. Vérifie ta connexion, puis réessaie.`
  : `Le serveur est injoignable : ${what}. Vérifie ta connexion ou réessaie dans un instant.`);
const retryable = (e) => !closed(e) && (!e || !e.status || e.status === 429 || e.status >= 500);                 // coupure réseau ou trop de requêtes : « Réessayer »
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
    if (group.dataset.name === 'chrono') store.set('chrono', b.dataset.value);       // réglage gardé sur l'appareil
  });
}

async function start(f, review = false, plan = null, challenge = null) {
  if (!challenge) { state.challenge = null; state.forceChrono = null; }
  if (state.starting) return; state.starting = true;                 // A' : un double appui ne lance pas deux séries
  $('home-error').hidden = true; loading(true);
  try {
    const s = await api('/sessions', { method: 'POST', body: JSON.stringify({ mode: f.mode || mode(), review, plan, challenge, tz: tzOffset(), filters: Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode')) }) });
    state.sid = s.session_id; state.size = s.size; state.mode = s.mode; store.set('sid', s.session_id);
    state.filters = review ? (state.filters || {}) : Object.fromEntries(Object.entries(f).filter(([k]) => k !== 'mode'));   // A1 : « Nouvelle série » les reprend
    store.set('filters', JSON.stringify(state.filters));
    await next();
  } catch (e) {
    loading(false); $('home-error').textContent = e.status === 422 ? 'Pas assez de situations pour ce thème : élargis les filtres.'
      : e.status && e.status < 500 ? e.message : netMsg(e, "la série n'a pas pu démarrer");            // jamais « Failed to fetch »
    if (e.status === 409 && challenge) { state.challenge = null; state.forceChrono = null; loadChallenges(); }   // défi du jour déjà relevé
    else $('filters').open = true;
    $('home-error').hidden = false;
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
const HUD_FR = { shove_pct: 'Tapis', call_pct: 'Call', call_pct_bb_sb_fold: 'Call', limp_pct: 'Limp', call_after_limp_pct: 'Call après limp',
  jam_over_limp_pct: 'Tapis/limp', open_pct: 'Open', defend_pct: 'Déf.' };
function lastActions(q) {
  const last = {};
  for (const h of q.history) last[h.position] = h.action;
  return last;
}

function renderTable(q) {
  const view = $('table-view'); view.innerHTML = '';
  const n = q.players.length, hero = q.players.indexOf(q.hero), { c: c0, folded } = contributions(q), last = lastActions(q);
  view.classList.toggle('hu', n === 2);
  // une mise au-delà du plus gros tapis adverse encore en jeu ne peut pas être payée : on l'affiche plafonnée, comme le pot de la correction
  const c = c0.map((x, i) => Math.min(x, Math.max(...q.stacks_bb.map((s, j) => (j !== i && !folded[j] ? s : 0)), 0) || x));
  const potShown = c.reduce((a, x) => a + x, 0);
  const seats = n === 3 ? [[50, 0], [21, 5], [79, 5]] : [[50, 0], [50, 4]];          // héros en bas (placé à part), adversaires en haut
  const button = n === 3 ? 'BTN' : 'SB';                                                // en heads-up, le SB a le bouton
  const hud = hudLines(q);
  for (let k = 0; k < n; k++) {
    const i = (hero + k) % n, pos = q.players[i], left = q.stacks_bb[i] - c[i];
    const covers = last[pos] === 'allin' && left > 1e-9;                     // il pousse plus que ton tapis : il te couvre
    const allin = left <= 1e-9 || last[pos] === 'allin';                     // test joueurs 6 : un joueur à tapis n'affiche plus de jetons derrière
    const act = allin ? '' : ACT_TAG[last[pos]] || '';                        // tapis : « ALL-IN » à la place du tapis restant
    const stack = allin ? 'ALL-IN' : `${bb(left)} BB`;
    if (k === 0) {
      $('hero-seat').innerHTML = `<b>${pos} · toi</b><span class="stack">${stack}</span>` + (act ? `<span class="act a-${last[pos]}">${act}</span>` : '');   // ton action, comme pour les autres
    } else {
      const seat = document.createElement('div');
      seat.className = 'seat' + (folded[i] ? ' folded' : '');
      seat.style.left = seats[k][0] + '%'; seat.style.top = seats[k][1] + '%';
      const backs = !folded[i] ? '<span class="backs"><i></i><i></i></span>' : '';           // cartes cachées des adversaires encore dans le coup
      const marked = q.field && q.field.pastille && (q.field.villains || []).includes(pos);
      const tag = q.field ? (marked ? pastilleDot(q.field.pastille) : '<i class="pastille none" title="Pas de pastille">?</i>') : '';
      const pname = marked ? `<span class="pname" style="--p:${pastilles()[q.field.pastille]};--pi:${inkOn(pastilles()[q.field.pastille])}">${q.field.pastille}</span>` : '';   // analyse des écrans : le nom de la pastille sous le siège
      seat.innerHTML = backs + `<b>${tag}${pos}</b><span class="stack">${stack}${covers ? ' <small>te couvre</small>' : ''}</span>` + (act ? `<span class="act a-${last[pos]}">${act}</span>` : '') + pname
        + (hud[pos] ? `<span class="hud">${hud[pos]}</span>` : '') + (c[i] > 0 ? `<span class="betnum">${bb(c[i])}<small> BB</small></span>` : '');   // sa mise, devant lui (en BB)
      view.appendChild(seat);
    }
    if (k === 0 && c[i] > 0) {
      const b = document.createElement('span'); b.className = 'betnum hero-bet'; b.innerHTML = `${bb(c[i])}<small> BB</small>`; view.appendChild(b);
    }
    if (pos === button) {
      const d = document.createElement('span'); d.className = 'dealer'; d.textContent = 'D'; d.title = 'Bouton';
      const [x, y] = k === 0 ? [72, 84] : [seats[k][0] + (seats[k][0] < 50 ? 17 : seats[k][0] > 50 ? -17 : 17), seats[k][1] + 8];
      d.style.left = x + '%'; d.style.top = y + '%'; view.appendChild(d);
    }
  }
  const pot = document.createElement('div'); pot.className = 'pot'; pot.innerHTML = `<small>Pot total</small>${bb(potShown)} BB`; view.appendChild(pot);
}

// stats du vilain en une ligne sous son siège (comme le HUD du client) ; le détail (observé / théorie) se déplie sous la table
// arrondi « au pair » comme l'énoncé et la correction (12,5 % -> 12 %), pour que les chiffres concordent
const rnd0 = (x) => { const f = Math.floor(x), d = x - f; return d > 0.5 + 1e-9 ? f + 1 : d < 0.5 - 1e-9 ? f : (f % 2 === 0 ? f : f + 1); };
function hudLines(q) {
  const f = q.field, out = {};
  if (!f || !q.hand || f.ask_fr || f.pastille) return out;            // pastille posée : elle résume ses stats (détail sous la table)
  const main = (f.villains || [])[0];
  if (!f.stats.length) { if (main) out[main] = 'Inconnu'; return out; }
  for (const s of f.stats) {                                            // une ligne courte, comme le HUD du client ; théorie et k/n dans « Stats du vilain »
    const who = s.stat === 'call_pct_bb_sb_fold' ? 'BB' : main;
    const item = `${HUD_FR[s.stat] || s.label_fr} ${rnd0(s.observed_pct)}`;
    out[who] = out[who] ? `${out[who]} · ${item}` : item;
  }
  if (main && out[main]) out[main] += ` (${f.observations})`;                // nombre de coups observés, comme le compteur du client
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

// mode chrono (chantier 5) : comme au client, le temps est compté ; à zéro, fold automatique (check s'il n'y a rien à payer)
const chrono = () => { if (state.forceChrono) return state.forceChrono;   // défi au chrono imposé
  const v = Number(store.get('chrono') ?? 15); return [0, 8, 15].includes(v) ? v : 15; };   // 15 s par défaut
function stopTimer() { clearInterval(state.timer); state.timer = null; $('q-timer').hidden = true; }
function startTimer(q) {
  stopTimer(); state.timedOut = false;
  const secs = chrono(); if (!secs || !q.hand || (q.field && q.field.ask_fr)) return;   // pas de chrono pour la lecture du vilain
  const end = Date.now() + secs * 1000, box = $('q-timer'); box.hidden = false;
  const tick = () => {
    const left = Math.max(0, end - Date.now());
    box.querySelector('i').style.width = `${100 * left / (secs * 1000)}%`; box.querySelector('span').textContent = `${Math.ceil(left / 1000)} s`;
    box.classList.toggle('late', left < 3000);
    if (left > 0) return;
    stopTimer();
    const auto = q.options.find((o) => /^FOLD$/i.test(o.label_fr)) || q.options.find((o) => /^CHECK$/i.test(o.label_fr)) || q.options[0];
    state.timedOut = auto.label_fr.toLowerCase(); answer(auto.id, true);
  };
  tick(); state.timer = setInterval(tick, 100);
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
  show('question'); startTimer(q);
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
      + `<div class="vbar obs"><span>Observé</span><em><i style="width:${w(s.observed_pct)}"></i></em><b>${rnd0(s.observed_pct)} %</b></div>`   // mêmes arrondis que le texte
      + `<div class="vbar gto"><span>Théorie</span><em><i style="width:${w(s.gto_pct)}"></i></em><b>${rnd0(s.gto_pct)} %</b></div>`;
  }).join('');
  const body = (context ? `<p class="fnone">${escT(context)}</p>` : '')
    + (f.stats.length ? bars + `<p class="fn">${f.observations} occasions : plus il y en a, plus la tendance est fiable.</p>`
      : `<p class="fnone">Aucune information sur ce vilain : compte sur le profil le plus fréquent du field (rec passif).</p>`);
  box.className = 'fstats';
  box.innerHTML = noHand ? `<span class="ftype">${f.type_fr}</span>` + body
    : `<details class="vdetails"><summary><span class="ftype">${f.type_fr}</span> ${f.pastille ? `${pastilleDot(f.pastille)}<b>${f.pastille}</b> <small>voir ses stats (${f.observations} mains)</small>` : f.observations ? `Stats du vilain · ${f.observations} mains` : 'Aucune information'}</summary>${body}</details>`;   // analyse des écrans : la pastille nommée
}

async function next() {
  loading(true);
  const data = await api(`/quiz/next?session_id=${encodeURIComponent(state.sid)}`);
  if (data.done) return summary();
  renderQuestion(data);
}

// ------------------------------------------------------------------ correction
async function answer(id, timedOut = false) {
  if (state.busy) return; state.busy = true; clearInterval(state.timer); state.timer = null;
  for (const b of $('actions').querySelectorAll('button')) b.disabled = true;
  try {
    const r = await api('/attempts', { method: 'POST', body: JSON.stringify({ session_id: state.sid, question_index: state.index, action_id: id, timed_out: timedOut }) });
    renderAnswer(r);
  } catch (e) {
    if (!e.status) console.error(e);                              // erreur d'affichage : visible dans la console
    for (const b of $('actions').querySelectorAll('button')) b.disabled = false;
    notify(netMsg(e, "ta réponse n'a pas été enregistrée"), retryable(e) ? () => answer(id) : null);
  } finally { state.busy = false; }
}

function recapLine(q) {
  const i = q.players.indexOf(q.hero), st = q.stacks_bb, eff = Math.min(st[i], Math.max(...st.filter((_, k) => k !== i)));
  const hist = (q.history_fr || []).map((t) => t.replace(/^Le /, '')).join(' · ') || 'premier à parler';
  return `<b>${q.hero}</b> · ${q.table === 'heads-up' ? 'heads-up' : '3 joueurs'} · ${bb(eff)} BB effectifs<br><span>${escT(hist)}</span>`;
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
    : (r.good_labels || []).length > 1 ? `Les bons coups : ${r.good_labels.join(' ou ')}.${r.loss_fr ? ` Ton choix coûte ${r.loss_fr}.` : ''}`   // analyse des écrans : une seule formulation
    : `Le bon coup : ${r.best_label}.${r.loss_fr ? ` Ton choix coûte ${r.loss_fr}.` : ''}`;   // message essentiel : le bon coup, le coût
  v.innerHTML = title + `<small>${state.timedOut ? `Temps écoulé : ${state.timedOut} automatique, compté comme une erreur.\n` : ''}${sub}</small>`;
  stopTimer();
  renderCards(state.q.hand_display, 'a-cards'); $('a-cards').hidden = !state.q.hand || !!(state.q.field && state.q.field.ask_fr);
  $('a-choice').hidden = true;                                       // ton choix et son coût sont dans l'explication (pas de redite)
  $('a-strategy-title').textContent = r.gto_label ? `Contre ce joueur : ${r.best_label} · contre un joueur GTO : ${r.gto_label}` : 'Stratégie de référence';
  $('a-strategy').innerHTML = r.strategy.map((s) =>
    `<div class="srow${s.id === r.best_action ? ' best' : ''}${s.chosen ? ' mine' : ''}"><span>${s.label_fr}</span><span class="pct">${s.pct} %</span><div class="sbar"><i style="width:${s.pct}%"></i></div></div>`).join('');
  const fd = r.field; $('a-exploit').hidden = !fd;
  for (const id of ['a-strategy-title', 'a-strategy']) $(id).hidden = !!fd;         // exploitant : correction courte
  if (fd) {
    $('a-exploit').innerHTML = `<div class="ref"><dt>${fd.read ? 'Bonne lecture' : 'Contre ce vilain'}${fd.gain_fr ? `<span class="conf net">${fd.gain_fr} de plus que la théorie</span>` : ''}</dt><dd>${escT(r.best_label)}</dd></div>`
      + (fd.gto_label ? `<div><dt>Théorie estimée (sans read)</dt><dd>${escT(fd.gto_label)}</dd></div>` : '')   // test joueurs 7 : moteur exploitant, pas la référence du mode GTO
      + (fd.evs.length ? `<div><dt>Gain par rapport au fold <small>(ajusté à ce vilain)</small></dt><dd>${fd.evs.map((e) => `${escT(e.label_fr)} : ${e.ev_fr}`).join('\n')}</dd></div>` : '')
      + `<p class="note">${fd.type_fr}</p>`;
  }
  // d'abord l'essentiel (une phrase, puis la règle à retenir), ensuite les précisions, repliées
  $('a-essential').textContent = r.essential_fr || '';
  const rem = (r.remember_fr || '').replace(/^À retenir : /, '');
  const q = state.q, cl = $('a-conseil');                                // étape 2 : la même situation dans le conseiller
  cl.hidden = !!(r.field || !q.node_key || typeof DEMO !== 'undefined');      // la démo autonome n'a pas le conseiller
  if (!cl.hidden) cl.href = `conseil?t=${encodeURIComponent(q.table)}&s=${q.stacks_bb.join('-')}&k=${encodeURIComponent(q.node_key)}&h=${encodeURIComponent(q.hand)}`;
  $('a-remember').hidden = !rem; $('a-remember').innerHTML = rem ? `<b>À retenir</b><span class="eline">${escT(rem.charAt(0).toUpperCase() + rem.slice(1))}</span>` : '';
  const det = r.details_fr || []; $('a-more').open = false;
  const full = state.q.prompt_fr.replace(' Que fais-tu ?', '').replace(/\n(Quelle pastille lui donnes-tu|Quel est le défaut de ce vilain) \?$/, '');
  $('a-details').innerHTML = `<p class="eline note">Énoncé : ${escT(full)}</p>` + det.map((l) => `<p class="eline">${escT(l)}</p>`).join('');
  $('a-recap').innerHTML = recapLine(state.q);                       // analyse des écrans : rappel en une ligne, l'énoncé complet dans les précisions
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
  $('s-score').innerHTML = `${bb(s.points)} / ${s.questions}<small>${pc(s.score_pct)} des points</small>`
    + (s.ev_questions ? `<small class="bblost">${s.bb_lost > 0 ? `Cette série t'a coûté ${bb(s.bb_lost)} BB, soit ${bb(s.bb_per_100)} BB pour 100 décisions` : 'Aucun BB perdu sur cette série'}.`
      + (s.bb_lost > 0 && s.ev_questions < 100 ? ` Échantillon faible (${s.ev_questions} décisions) : ce chiffre varie beaucoup d'une série à l'autre, regarde plutôt « Ma progression ».` : '') + '</small>' : '')
    + (s.timeouts ? `<small class="bblost">${s.timeouts} coup${s.timeouts > 1 ? 's' : ''} joué${s.timeouts > 1 ? 's' : ''} au temps, compté${s.timeouts > 1 ? 's' : ''} comme erreur${s.timeouts > 1 ? 's' : ''}.</small>` : '');
  $('s-verdicts').innerHTML = [['correct', 'Bonnes'], ['imprécision', 'Imprécisions'], ['erreur', 'Erreurs']]
    .map(([k, t]) => `<li><b>${s.verdicts[k] || 0}</b>${t}</li>`).join('');
  $('s-errors').innerHTML = s.errors.length
    ? s.errors.map((e) => `<li><em class="vtag ${e.verdict === 'erreur' ? 'bad' : 'warn'}">${e.verdict === 'erreur' ? 'Erreur' : 'Imprécision'}</em> ${e.prompt_fr}<br>${e.timed_out ? `Temps écoulé (${e.chosen} automatique)` : `Ton coup : ${e.chosen} (coûte ${e.loss_fr || gainBB(e.regret_mbb)})`} · Meilleur coup : <b>${e.best}</b></li>`).join('')
    : '<li>Rien à revoir sur cette série.</li>';
  $('s-review').hidden = !s.errors.length;
  $('again-btn').textContent = state.inToday ? 'Suite de la séance' : 'Nouvelle série';
  if (state.challenge) {                                               // étape 5 : résultat du défi
    const kind = state.challenge; state.challenge = null; state.forceChrono = null;
    loadChallenges().then((c) => { const x = c && [...c.daily, ...c.weekly].find((y) => y.kind === kind); if (!x) return;
      const msg = x.status === 'won' ? `${escT(x.title_fr)} : réussi !${x.next_fr ? ` ${escT(x.next_fr)}` : ''}`   // test joueurs 9 : le défi du jour ne se retente pas
        : x.next_fr ? `${escT(x.title_fr)} : ${escT(x.result_fr || '')}. ${escT(x.next_fr)}` : `${escT(x.title_fr)} : ${escT(x.result_fr || '')}, pas encore réussi. Tu peux le retenter.`;
      $('s-score').insertAdjacentHTML('beforeend', `<small class="ch-result ${x.status}">${msg}</small>`); });
  }
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
  return `<div class="trow${cls}"><span>${x.label}</span><span>${pc(x.score_pct)}${x.bb_per_100 != null ? ` <small class="bb100">· ${bb(x.bb_per_100)} BB/100</small>` : ''}</span><div class="sbar"><i style="width:${x.score_pct}%"></i></div></div>`;
}
// progression hors connexion : la dernière progression reçue est gardée sur l'appareil et réaffichée, datée, si le réseau
// ou le serveur manque ; elle se met à jour à chaque ouverture en ligne et à la fin de chaque série
const STATS_KEY = 'stats_cache';
function cacheStats(s) { store.set(STATS_KEY, JSON.stringify({ at: new Date().toISOString(), s })); homeSummary(); }
function homeSummary() {                                            // analyse des écrans (29/10) : où tu en es, dès l'accueil
  const c = cachedStats(), s = c && c.s, b = $('stats-btn');
  if (!s || !s.questions) { b.textContent = 'Ma progression'; return; }
  const f = s.focus && s.focus.label ? ` · à travailler : ${s.focus.label.split(' · ').slice(1).join(' · ') || s.focus.label}` : '';
  b.innerHTML = `Ma progression<small>${pc(s.score_pct)} de réussite${s.bb_per_100 != null ? ` · ${bb(s.bb_per_100)} BB perdus / 100` : ''}${escT(f)}</small>`;
}
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
  if (!offline) api(`/users/me/challenges?mode=${mode()}&tz=${tzOffset()}`).then((c) => {     // étape 5 : mes défis réussis
    $('st-challenges').hidden = false;
    $('st-ch-list').innerHTML = c.history.length ? c.history.map((h) => `<li class="${h.won ? 'won' : 'tried'}">${h.won ? '✓' : '·'} <b>${escT(h.title_fr)}</b> <small>${new Date(h.date + 'T12:00').toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' })} · ${escT(h.result_fr)}${h.won ? '' : ' · tenté'}</small></li>`).join('')
      : '<li class="note">Pas encore de défi relevé : commence par le défi du jour depuis l\'accueil.</li>';
  }).catch(() => { $('st-challenges').hidden = true; });
  else $('st-challenges').hidden = true;
  if (offline) renderLevel(null);                                   // étape 4 : mon niveau (aussi avant la première série)
  else api('/users/me/level').then((lv) => { renderLevel(lv); if (state.scrollLevel) { state.scrollLevel = false; $('st-level').scrollIntoView({ block: 'start' }); } }).catch(() => renderLevel(null));
  if (!s.questions) {
    $('st-score').innerHTML = '—<small>Joue une première série pour voir ta progression.</small>';
    for (const id of ['st-evolution', 'st-themes']) $(id).innerHTML = '';
    $('st-focus').className = 'focus none'; $('st-focus').innerHTML = '<p class="focus-title">À travailler maintenant</p><p>Joue une première série pour un diagnostic.</p>';
    $('st-note').textContent = ''; show('stats'); return;
  }
  // analyse des écrans (29/10) : le score en grand, puis deux ou trois tuiles au lieu d'un paragraphe
  $('st-score').innerHTML = `${pc(s.score_pct)}<small>${s.questions} questions · ${s.sessions} série${s.sessions > 1 ? 's' : ''}</small>`
    + '<div class="st-tiles">'
    + (s.bb_per_100 != null ? `<div><b>${bb(s.bb_per_100)} BB</b><span>perdus pour 100 décisions</span><small>${s.ev_questions < 100 ? `échantillon faible (${s.ev_questions})` : 'plus c\'est bas, mieux c\'est'}</small></div>` : '')   // chantier 5
    + (s.ranges && s.ranges.count ? `<div><b>${pc(s.ranges.accuracy_pct)}</b><span>ranges bien classées</span><small>${s.ranges.count} range${s.ranges.count > 1 ? 's' : ''}${s.ranges.count > s.ranges.recent ? ` (${s.ranges.recent} dernières)` : ''}</small></div>` : '')
    + (s.timeouts ? `<div><b>${s.timeouts}</b><span>coup${s.timeouts > 1 ? 's' : ''} joué${s.timeouts > 1 ? 's' : ''} au temps</span></div>` : '')
    + '</div>';
  $('st-evolution').innerHTML = s.evolution.length > 1
    ? s.evolution.map((e) => `<i style="height:${Math.max(4, e.score_pct)}%" title="${pc(e.score_pct)}${e.date ? ` · ${new Date(e.date).toLocaleDateString('fr-FR')}` : ''}"><span>${Math.round(e.score_pct)}</span></i>`).join('')
    : '<span>L\'évolution s\'affiche après deux séries.</span>';
  const f = s.focus || { kind: 'none', reason_fr: '' };                // un seul diagnostic (même règle que les séries adaptées)
  $('st-focus').className = `focus ${f.kind}`;
  $('st-focus').innerHTML = `<p class="focus-title">À travailler maintenant</p>`
    + (f.label ? `<p><b>${f.label}</b></p>` : '') + `<p>${f.reason_fr}</p>`
    + (f.examples && f.examples[0] ? `<p class="note">Exemple : ${f.examples[0].replace(' Que fais-tu ?', '')}</p>` : '')
    + (f.filters && !offline ? '<button class="primary" id="train-focus">M\'entraîner sur ce thème</button>' : '');
  if (f.filters && !offline) $('train-focus').addEventListener('click', () => { state.inToday = false; start(f.filters); });
  const groups = Object.entries(s.by).filter(([, rows]) => rows.length);          // pas de carte vide
  const old = s.untracked_questions || 0;                                         // démo : réponses d'une version précédente, sans description
  const cards = groups.map(([k, rows]) => `<div class="theme-group"><b>${DIM_FR[k]}</b>${rows.map((x) => themeRow(x, s.min_sample)).join('')}</div>`).join('');
  const anyScore = groups.some(([k, rows]) => k !== 'mode' && rows.some((x) => x.reliable));
  $('st-themes').innerHTML = (anyScore || !cards ? cards                        // analyse des écrans : pas de mur de « encore N questions »
    : `<details class="themes-wait"><summary>Aucun thème n'a encore ${s.min_sample} questions : voir l'avancement</summary>${cards}</details>`)
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
$('quick-start').addEventListener('click', () => { state.inToday = false; start({}); });
$('review-btn').addEventListener('click', () => { state.inToday = false; start({}, true); });

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
  $('range-btn').textContent = mode() === 'gto' ? 'Construis ta range' : 'Construis ta range (théorie)';   // test joueurs 7 : aussi en exploitant, sur la stratégie de référence
  reviews(); if (!$('screen-home').hidden) { loadToday().then(loadRecs); loadGoals(); loadChallenges(); }   // séance, recommandations et objectifs suivent le mode
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
$('custom-start').addEventListener('click', () => { state.inToday = false; start(filters()); });
$('report-form').addEventListener('submit', sendReport);
const goNext = () => next().catch((e) => { loading(false); notify(netMsg(e, "la question suivante n'a pas pu être chargée"), goNext); });
$('next-btn').addEventListener('click', goNext);
$('again-btn').addEventListener('click', () => {                 // A1 : même mode, mêmes filtres
  if (state.inToday) { todayContinue(); return; }
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
  if (!state.levelChecked) {                                          // étape 4 : premier lancement en trois écrans
    state.levelChecked = true;
    try { const lv = await api('/users/me/level'); state.level = lv; state.promo = lv.promoted_to; if (!lv.onboarded) { onboard(lv); return; } } catch (e) { /* hors ligne : accueil normal */ }
  }
  progress(''); show('home'); homeSummary(); loadToday().then(loadRecs); loadGoals(); loadLevel(); loadChallenges();
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
// ------------------------------------------------------------------ séance du jour (programme de travail, étape 1)
// révision, thème du jour (2 séries), range du jour ; le serveur (ou la démo) construit le plan, l'application l'enchaîne
const tzOffset = () => -new Date().getTimezoneOffset();
async function loadToday() {
  let t; try { t = await api(`/users/me/today?mode=${mode()}&tz=${tzOffset()}`); } catch (e) { $('today').hidden = true; $('free-title').hidden = true; return null; }
  state.today = t; renderToday(t); return t;
}
function renderToday(t) {
  $('today').hidden = false; $('free-title').hidden = false; $('home-lead').hidden = true;
  $('quick-start').className = 'secondary';                          // un seul bouton plein sur l'accueil : la séance
  $('today-streak').textContent = t.streak ? `${t.streak} jour${t.streak > 1 ? 's' : ''} de suite` : 'Première séance : c\'est parti';
  const d = t.bb7 != null && t.bb7_prev != null ? t.bb7 - t.bb7_prev : null;
  $('today-bb').innerHTML = t.bb7 != null ? `BB perdus / 100 sur 7 jours : <b>${bb(t.bb7)}</b>${d != null && Math.abs(d) >= 0.05 ? ` <span class="${d < 0 ? 'up' : 'down'}">${d < 0 ? '▼' : '▲'} ${bb(Math.abs(d))}</span>` : ''}` : '';
  $('today-steps').innerHTML = t.steps.map((x, i) => `<li class="${x.done ? 'done' : i === t.next ? 'now' : ''}"><span class="tick" aria-hidden="true">${x.done ? '✓' : ''}</span>`
    + `<span>${escT(x.label_fr)}${x.total ? ` <small>${x.count}/${x.total} séries</small>` : ''}</span></li>`).join('');
  $('today-note').hidden = !t.done;
  $('today-note').textContent = t.done ? 'Séance faite. Reviens demain : tes révisions et un nouveau thème t\'attendent.' : '';
  $('today-go').textContent = t.done ? 'Une série en plus' : t.started ? 'Continuer la séance' : 'Commencer la séance';
  $('today').classList.toggle('is-done', t.done);
}
function todayGo() {
  const t = state.today; if (!t) return;
  if (t.done) { state.inToday = false; start(t.steps[1].filters); return; }
  const st = t.steps[t.next]; state.inToday = true;
  if (st.kind === 'review') start({}, true, 'review');
  else if (st.kind === 'theme') start(st.filters, false, 'theme');
  else rangeStart(st.filters);
}
async function todayContinue() {
  const t = await loadToday(); if (!t) { home(); return; }
  if (t.done) showTodayDone(t); else todayGo();
}
function showTodayDone(t) {
  state.inToday = false; progress('');
  $('td-score').innerHTML = `✓<small>${t.minutes} minutes de travail · ${t.streak} jour${t.streak > 1 ? 's' : ''} de suite</small>`;
  $('td-lines').innerHTML = [`Thème travaillé : <b>${escT(t.theme_fr)}</b>`,
    t.bb7 != null ? `BB perdus pour 100 décisions sur 7 jours : <b>${bb(t.bb7)}</b>${t.bb7_prev != null ? ` (semaine précédente : ${bb(t.bb7_prev)})` : ''}` : '',
    'Demain : tes mains ratées reviennent en révision, et la séance choisit ton thème le plus fragile.'].filter(Boolean).map((l) => `<li>${l}</li>`).join('');
  show('today'); refreshStats();
  loadGoals().then((g) => { if (!g) return;                          // étape 3 : où en sont les objectifs de la semaine
    $('td-lines').insertAdjacentHTML('beforeend', `<li>Objectifs de la semaine : ${g.items.map((x) => `${escT(x.label_fr.toLowerCase())} ${escT(x.text_fr.split(' · ')[0])}${x.done ? ' ✓' : ''}`).join(' ; ')}</li>`); });
}
$('today-go').addEventListener('click', todayGo);

// ------------------------------------------------------------------ niveaux et premier lancement (programme de travail, étape 4)
function onboard(lv) {
  const ob = state.ob = { step: 1, exp: null, goal: null, level: null, lv };
  const chips = (id, map, key) => { $(id).innerHTML = Object.entries(map).map(([k, t]) => `<button type="button" data-v="${k}" aria-pressed="false">${escT(t)}</button>`).join('');
    $(id).onclick = (e) => { const b = e.target.closest('button'); if (!b) return; ob[key] = b.dataset.v; for (const x of $(id).querySelectorAll('button')) x.setAttribute('aria-pressed', String(x === b)); obButton(); }; };
  chips('ob-exp', lv.experiences, 'exp'); chips('ob-goal', lv.goals, 'goal');
  obShow(); show('onboard'); progress('Bienvenue');
}
function obButton() { const ob = state.ob; $('ob-next').disabled = ob.step === 1 && !(ob.exp && ob.goal); }
function obShow() {
  const ob = state.ob;
  for (const k of [1, 2, 3]) $(`ob-${k}`).hidden = k !== ob.step;
  $('ob-steps').textContent = `Étape ${ob.step} sur 3`;
  $('ob-next').textContent = ob.step === 3 ? "C'est parti" : 'Suivant';
  if (ob.step === 2) {
    ob.level = ob.level || ({ debut: 1, confirme: 2, gros_volume: 2 })[ob.exp] || 1;
    $('ob-levels').innerHTML = ob.lv.levels.filter((l) => l.number <= 3).map((l) => `<button type="button" class="ob-level" data-v="${l.number}" aria-pressed="${l.number === ob.level}"><b>Niveau ${l.number}</b> ${escT(l.name)}</button>`).join('');
    $('ob-levels').onclick = (e) => { const b = e.target.closest('button'); if (!b) return; ob.level = +b.dataset.v; for (const x of $('ob-levels').querySelectorAll('button')) x.setAttribute('aria-pressed', String(x === b)); };
  }
  obButton();
}
async function obFinish(skip) {
  const ob = state.ob;
  const body = skip ? { experience: 'debut', goal: 'bases' } : { experience: ob.exp, goal: ob.goal, level: ob.level };
  try { state.level = await api('/users/me/onboarding', { method: 'POST', body: JSON.stringify(body) }); } catch (e) { /* le niveau 1 s'appliquera */ }
  home();
}
$('ob-next').addEventListener('click', () => { const ob = state.ob; if (ob.step < 3) { ob.step += 1; obShow(); } else obFinish(false); });
$('ob-skip').addEventListener('click', () => obFinish(true));

async function loadLevel() {
  let lv; try { lv = await api('/users/me/level'); } catch (e) { $('today-level').hidden = true; return null; }
  state.level = lv;
  if (lv.promoted_to || state.promo) { state.promo = null; notify(`Bravo : tu passes au niveau ${lv.level}, « ${lv.name} ». Ta séance du jour suit ce nouveau niveau.`); }
  const b = $('today-level'), m = mode() === 'gto';
  b.hidden = false;
  b.innerHTML = m ? `<b>Niveau ${lv.level} · ${escT(lv.name)}</b>${lv.status.final ? '' : `<small>${lv.status.criteria.map((c) => `${c.ok ? '✓ ' : ''}${critText(c)}`).join(' · ')}</small>`}`
    : '<b>Niveau 4 · Exploiter le field</b><small>mode exploitant, ouvert en continu</small>';
  return lv;
}
function critText(c) {
  if (c.kind === 'decisions') return `${Math.min(c.value, c.target)}/${c.target} décisions`;
  if (c.kind === 'bb') return `${c.value == null ? '—' : bb(c.value)} BB/100 (cible < ${bb(c.target)})`;
  if (c.kind === 'ranges') return `${c.value}/${c.target} ranges à 85 %`;
  return c.ok ? 'aucun thème fragile' : c.value ? `thème fragile : ${c.value}` : 'pas encore de décision';
}
function renderLevel(lv) {
  $('st-level').hidden = !lv;
  if (!lv) return;
  $('st-level-name').innerHTML = `<b>Niveau ${lv.level} · ${escT(lv.name)}</b>` + (lv.status.final ? ' : dernier niveau GTO. Le niveau 4 se joue en mode Exploitant.' : ' : pour passer au suivant');
  $('st-level-crit').innerHTML = lv.status.final ? '' : lv.status.criteria.map((c) => `<li class="${c.ok ? 'ok' : ''}">${c.ok ? '✓' : '○'} ${escT(c.label_fr)} <small>${escT(critText(c))}</small></li>`).join('');
  $('st-level-pick').innerHTML = lv.levels.filter((l) => l.number <= 3).map((l) => `<button type="button" data-v="${l.number}" aria-pressed="${l.number === lv.level}">${l.number} · ${escT(l.name)}</button>`).join('');
}
$('st-level-pick').addEventListener('click', async (e) => {
  const b = e.target.closest('button'); if (!b) return;
  try { state.level = await api('/users/me/level', { method: 'PUT', body: JSON.stringify({ level: +b.dataset.v }) }); renderLevel(state.level); }
  catch (err) { notify(netMsg(err, "le niveau n'a pas été changé")); }
});
$('today-level').addEventListener('click', () => { state.scrollLevel = true; $('stats-btn').click(); });

// recommandations (programme de travail, étape 2) : au plus deux, un constat chiffré et une action en un toucher
async function loadRecs() {
  let r; try { r = await api(`/users/me/recommendations?mode=${mode()}&tz=${tzOffset()}`); } catch (e) { $('recs').hidden = true; return; }
  state.recs = r.items || [];
  $('recs').hidden = !state.recs.length;
  $('recs-list').innerHTML = state.recs.map((x, i) => `<li class="rec rec-${x.kind}"><p>${escT(x.text_fr)}</p><button class="secondary small" data-i="${i}">${escT(x.label_fr)}</button></li>`).join('');
}
// objectifs de la semaine (programme de travail, étape 3) : trois cibles, modifiables, et le bilan de la semaine passée
async function loadGoals() {
  let g; try { g = await api(`/users/me/goals?mode=${mode()}&tz=${tzOffset()}`); } catch (e) { $('goals').hidden = true; return null; }
  renderGoals(g); return g;
}
function renderGoals(g) {
  state.goals = g; $('goals').hidden = false;
  const edit = !!state.goalsEdit;
  $('goals-edit').textContent = edit ? 'terminé' : 'modifier';
  $('goals-list').innerHTML = g.items.map((x) => `<li class="goal${x.done ? ' done' : ''}"><div class="goal-top"><span>${x.done ? '✓ ' : ''}${escT(x.label_fr)}</span>`
    + (edit ? `<span class="goal-step"><button class="secondary small" data-k="${x.kind}" data-d="-1" aria-label="Baisser la cible">−</button><b>${String(x.target).replace('.', ',')}</b><button class="secondary small" data-k="${x.kind}" data-d="1" aria-label="Monter la cible">+</button></span>` : '')
    + `</div><div class="sbar"><i style="width:${Math.round(100 * x.progress)}%"></i></div><small>${escT(x.text_fr)}</small></li>`).join('');
  $('goals-note').textContent = g.days_left > 0 ? `Encore ${g.days_left} jour${g.days_left > 1 ? 's' : ''} cette semaine.` : 'Dernier jour de la semaine.';
  const lw = g.last_week, seen = store.get('goals_seen') === g.week;
  $('last-week').hidden = !lw || seen;
  if (lw && !seen) $('last-week').innerHTML = `<b>Semaine dernière : ${lw.done} objectif${lw.done > 1 ? 's' : ''} sur ${lw.total} tenu${lw.done > 1 ? 's' : ''}.</b> `
    + `${lw.days} séance${lw.days > 1 ? 's' : ''}${lw.bb != null ? ` · ${bb(lw.bb)} BB perdus pour 100 décisions${lw.bb_before != null ? ` (la semaine d'avant : ${bb(lw.bb_before)})` : ''}` : ''}.`
    + (lw.done < lw.total ? ' Les objectifs manqués sont reconduits un peu plus faciles.' : '') + ' <button class="link" id="lw-ok">OK</button>';
  if (lw && !seen) $('lw-ok').addEventListener('click', () => { store.set('goals_seen', g.week); $('last-week').hidden = true; });
}
$('goals-edit').addEventListener('click', () => { state.goalsEdit = !state.goalsEdit; if (state.goals) renderGoals(state.goals); });
$('goals-list').addEventListener('click', async (e) => {
  const b = e.target.closest('button[data-k]'); if (!b) return;
  const x = state.goals.items.find((i) => i.kind === b.dataset.k), step = x.kind === 'precision' ? 1 : 1;
  const t = Math.min(x.max, Math.max(x.min, x.target + step * +b.dataset.d)); if (t === x.target) return;
  try { renderGoals(await api('/users/me/goals', { method: 'PUT', body: JSON.stringify({ mode: mode(), kind: x.kind, target: t, tz: tzOffset() }) })); }
  catch (err) { notify(netMsg(err, "l'objectif n'a pas été changé")); }
});
// défis (programme de travail, étape 5)
async function loadChallenges() {
  let c; try { c = await api(`/users/me/challenges?mode=${mode()}&tz=${tzOffset()}`); } catch (e) { $('challenges').hidden = true; return null; }
  state.ch = c; const all = [...c.daily, ...c.weekly, ...c.monthly];
  $('challenges').hidden = false;
  $('ch-list').innerHTML = all.map((x, i) => `<li class="ch ch-${x.status}"><div class="ch-top"><span><small>${escT(x.window === 'jour' ? "Aujourd'hui" : x.window === 'semaine' ? 'Cette semaine' : 'Ce mois-ci')}</small><b>${x.status === 'won' ? '✓ ' : ''}${escT(x.title_fr)}</b></span>`
    + (x.action && x.status !== 'won' ? `<button class="secondary small" data-i="${i}">Relever</button>` : '') + `</div>`
    + `<p>${escT(x.rule_fr)}${x.theme_fr ? ` Thème : ${escT(x.theme_fr)}.` : ''}</p>${x.result_fr ? `<small>${x.status === 'won' ? 'Réussi' : 'Ton résultat'} : ${escT(x.result_fr)}${x.next_fr ? ` · ${escT(x.next_fr)}` : ''}</small>` : ''}</li>`).join('');
  return c;
}
$('ch-list').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-i]'); if (!b) return;
  const x = [...state.ch.daily, ...state.ch.weekly, ...state.ch.monthly][+b.dataset.i], a = x.action; state.inToday = false;
  if (a.type === 'range') { rangeStart(); return; }
  state.challenge = a.challenge; state.forceChrono = a.chrono || null;
  start({}, false, null, a.challenge);
});
$('recs-list').addEventListener('click', (e) => {
  const b = e.target.closest('button[data-i]'); if (!b) return;
  const a = state.recs[+b.dataset.i].action; state.inToday = false;
  if (a.chrono) { store.set('chrono', String(a.chrono)); for (const x of document.querySelectorAll('.chips[data-name="chrono"] button')) x.setAttribute('aria-pressed', String(x.dataset.value === String(a.chrono))); }
  if (a.type === 'review') start({}, true);
  else if (a.type === 'range') rangeStart({ spot: a.spot_id });
  else if (a.type === 'level') { state.scrollLevel = true; $('stats-btn').click(); }
  else start(a.filters || {});
});
$('td-more').addEventListener('click', () => start((state.today && state.today.steps[1].filters) || {}));
$('td-home').addEventListener('click', home);

// ------------------------------------------------------------------ « Construis ta range » (chantier 2) : colorier une range, correction main par main
const RK13 = 'AKQJT98765432';
const cellName = (i, j) => (i === j ? RK13[i] + RK13[j] : i < j ? RK13[i] + RK13[j] + 's' : RK13[j] + RK13[i] + 'o');
const combos = (h) => (h.length === 2 ? 6 : h.endsWith('s') ? 4 : 12);
const RG_STATUS = { ok_in: 'à jouer : bien vu', ok_out: 'pas avec cette action : bien vu', extra: 'jouée à tort', missing: 'oubliée',
  mixed: 'mixte (action demandée de 25 à 75 % du temps) : les deux sont acceptés', close: 'écart négligeable (moins de 0,01 BB) : les deux sont acceptés' };
async function rangeStart(forced) {
  const f = forced ? { ...forced } : filters(); delete f.mode;          // séance du jour : la situation du thème
  if (f.family === 'read') delete f.family;
  let recent = []; try { recent = JSON.parse(store.get('ranges_recent') || '[]'); } catch (e) { recent = []; }
  f.exclude = recent.join(',');                                          // pas deux fois la même situation de suite
  const qs = Object.entries(f).filter(([, v]) => v !== '').map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&');
  loading(true);
  let t;
  try { t = await api('/ranges/next' + (qs ? `?${qs}` : '')); }
  catch (e) { loading(false); notify(e.status === 422 ? 'Pas de range à construire pour ce thème : élargis les filtres.' : netMsg(e, "l'exercice n'a pas pu démarrer"), retryable(e) ? rangeStart : null); return; }
  state.range = { t, sel: new Set(), done: false };
  store.set('ranges_recent', JSON.stringify([t.spot_id, ...recent.filter((x) => x !== t.spot_id)].slice(0, 15)));
  $('rg-situation').textContent = t.situation_fr; $('rg-question').innerHTML = `${escT(t.question_fr)}<small>${escT(t.others_fr || '')}</small>`;
  $('rg-cellinfo').hidden = true;
  $('rg-result').hidden = true; $('rg-edit').hidden = false; $('rg-after').hidden = true; $('rg-help').hidden = false;
  renderRangeGrid(); show('range'); progress('Construis ta range');
}
function renderRangeGrid(result) {
  const g = $('rg-grid'), r = state.range, live = new Set(r.t.hands); g.innerHTML = '';
  for (let i = 0; i < 13; i++) for (let j = 0; j < 13; j++) {
    const h = cellName(i, j), b = document.createElement('button'); b.type = 'button'; b.dataset.h = h; b.textContent = h;
    b.className = 'rc' + (live.has(h) ? '' : ' off') + (r.sel.has(h) ? ' on' : '') + (result && result.cells[h] ? ` st-${result.cells[h]}` : '');
    if (!live.has(h)) { b.disabled = true; b.title = "Main qui n'arrive pas à cette décision"; }
    else if (result && result.cells[h]) b.title = cellInfo(h, result);
    b.setAttribute('aria-pressed', String(r.sel.has(h)));
    g.appendChild(b);
  }
  rangeCount();
}
function rangeCount() {                                              // même calcul que la correction : combinaisons pondérées
  const r = state.range, w = r.t.weights || {}; let n = 0, tot = 0;
  for (const h of r.t.hands) { tot += w[h] || combos(h); if (r.sel.has(h)) n += w[h] || combos(h); }
  $('rg-count').textContent = `Ta range : ${tot ? Math.round(100 * n / tot) : 0} % des mains (${r.sel.size} cases).`;
}
function cellInfo(h, g) {
  const st = g.cells[h], ref = (g.reference_fr || {})[h], pct = Math.round(100 * g.reference[h]);
  return `${h} : ${RG_STATUS[st]}. La référence ${ref || ''} (action demandée : ${pct} % du temps).`;
}
function paint(b, on) {
  const r = state.range; if (!b || !b.dataset.h || b.disabled || r.done) return;
  if (on) r.sel.add(b.dataset.h); else r.sel.delete(b.dataset.h);
  b.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on)); rangeCount();
}
(function rangePainting() {                                          // toucher une case, ou glisser le doigt pour en colorier plusieurs
  const g = $('rg-grid'); let mode = null;
  g.addEventListener('pointerdown', (e) => {
    const b = e.target.closest('.rc');
    if (b && state.range.done && state.range.result) { const i = $('rg-cellinfo'); i.textContent = cellInfo(b.dataset.h, state.range.result); i.hidden = false; return; }
    if (!b || b.disabled || state.range.done) return;
    mode = !state.range.sel.has(b.dataset.h); paint(b, mode); e.preventDefault();
  });
  g.addEventListener('pointermove', (e) => { if (mode === null) return; paint(document.elementFromPoint(e.clientX, e.clientY)?.closest('.rc'), mode); });
  addEventListener('pointerup', () => { mode = null; }); addEventListener('pointercancel', () => { mode = null; });
  g.addEventListener('keydown', (e) => { if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('.rc')) { const b = e.target.closest('.rc'); paint(b, !state.range.sel.has(b.dataset.h)); e.preventDefault(); } });
}());
async function rangeSubmit() {
  const r = state.range; if (r.done) return;
  loading(true);
  let g;
  try { g = await api('/ranges/answer', { method: 'POST', body: JSON.stringify({ spot_id: r.t.spot_id, hands: [...r.sel] }) }); }
  catch (e) { loading(false); notify(netMsg(e, "ta range n'a pas pu être corrigée"), retryable(e) ? rangeSubmit : null); return; }
  loading(false); r.done = true; r.result = g; renderRangeGrid(g);
  const worst = g.worst.length ? `<ul class="rg-worst">${g.worst.map((w) => `<li><b>${w.hand}</b> ${w.kind === 'extra' ? 'jouée à tort' : 'oubliée'} : la référence ${w.ref_fr}, ${bb(w.cost_bb)} BB perdus à chaque fois</li>`).join('')}</ul>` : '';
  const rem = (g.rule_fr || '').replace(/^À retenir : /, '');
  // analyse des écrans : le diagnostic (trop serrée, trop large) d'abord, le score ensuite
  const ratio = g.ref_share_pct ? g.my_share_pct / g.ref_share_pct : 1;
  const diag = ratio < 0.75 ? ['bad', 'Trop serrée'] : ratio > 1.33 ? ['bad', 'Trop large'] : g.extra + g.missing > 0 ? ['ok', 'Bonne taille, quelques mains à revoir'] : ['ok', 'Bien vu'];
  $('rg-result').innerHTML = `<p class="rg-diag ${diag[0]}"><b>${diag[1]}</b><span>Ta range fait ${g.my_share_pct} % des mains, la référence ${g.ref_share_pct} %.</span>`
    + `<small>${g.missing} main${g.missing > 1 ? 's' : ''} oubliée${g.missing > 1 ? 's' : ''}, ${g.extra} en trop.</small></p>`
    + `<p class="rg-score2">${pc(g.accuracy_pct)} des mains bien classées · ${bb(g.bb_per_100)} BB perdus pour 100 mains jouées ici</p>`
    + (g.worst.length ? `<p class="rg-worst-title">${g.worst.length < g.extra + g.missing ? `Les ${g.worst.length} erreurs les plus coûteuses :` : 'Tes erreurs :'}</p>` : '') + worst
    + `<p class="rg-legend"><span class="st-ok_in">à jouer</span><span class="st-extra">en trop</span><span class="st-missing">oubliée</span><span class="st-mixed">mixte (les deux acceptés)</span><span class="st-close">écart négligeable</span><span class="st-chosen">ton choix</span></p><p class="note">Touche une case pour voir ce que fait la référence.</p>`
    + (rem ? `<p class="remember"><b>À retenir</b><span class="eline">${escT(rem.charAt(0).toUpperCase() + rem.slice(1))}</span></p>` : '');
  $('rg-result').hidden = false; $('rg-edit').hidden = true; $('rg-after').hidden = false; $('rg-help').hidden = true;
  $('rg-again').textContent = state.inToday ? 'Suite de la séance' : 'Nouvelle range';
  glossify($('rg-result'));
  refreshStats();
}
$('range-btn').addEventListener('click', () => { state.inToday = false; rangeStart(); });
$('rg-clear').addEventListener('click', () => { state.range.sel.clear(); renderRangeGrid(); });
$('rg-submit').addEventListener('click', rangeSubmit);
$('rg-again').addEventListener('click', () => (state.inToday ? todayContinue() : rangeStart()));
$('rg-home').addEventListener('click', home);

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
  for (const c of document.querySelectorAll('.chips[data-name="chrono"] button')) c.setAttribute('aria-pressed', String(Number(c.dataset.value) === chrono()));
  onMode();
}());
home();

// l'application s'ouvre aussi sans connexion (service worker) ; pas dans la démo autonome, qui est déjà une seule page
const canSW = 'serviceWorker' in navigator && !window.SA_LEXIQUE
  && (location.protocol === 'https:' || ['localhost', '127.0.0.1'].includes(location.hostname));
if (canSW) addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => { /* navigateur sans service worker : en ligne seulement */ }));

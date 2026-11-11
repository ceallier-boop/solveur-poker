// Recette des défis par catégorie (option A provisoire du 10/11, docs/produit/CATEGORIES_ET_EQUITES_2026-11-10.md), application ou démo :
//   une carte de la semaine par catégorie disponible (Préflop GTO, Préflop exploitant, Profils, Ranges), avec category et access ;
//   Équités réservée : dans la liste des catégories (available false), jamais affichée ;
//   défi du jour et Sous pression tirés dans la banque GTO même depuis l'onglet Exploitant ; défi du jour : les mêmes mains,
//   dans le même ordre, pour un joueur venu de l'onglet GTO et un joueur venu de l'onglet Exploitant ;
//   Série parfaite (banque exploitante, sans publicité) ; Lecteur de vilain (banque exploitante, au moins 2 « Quelle pastille ? ») ;
//   seule Range au cordeau est dans la zone publicité ; by_category dans /users/me/wins ; category sur les étapes de la séance et les objectifs.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_categories_recette.cjs [dossier]      (ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const CATS = { gto: 'Préflop GTO', exploit: 'Préflop exploitant', profils: 'Profils', ranges: 'Ranges' };

const api = (p, route) => p.evaluate(async (r) => (await window.fetch('/' + r, { headers: { 'X-Player-Id': localStorage.getItem('player_id') } })).json(), route);
const watch = (p) => p.evaluate(() => {                              // séries créées (banque servie) et questions reçues, application ou démo
  const f = window.fetch; window.__made = []; window.__qs = [];
  window.fetch = async (path, opts) => {
    const r = await f(path, opts); const u = String(path).split('?')[0];
    if (/\/sessions$/.test(u) && opts && opts.method === 'POST') { const j0 = r.json.bind(r); r.json = async () => { const j = await j0(); if (j && j.session_id) window.__made.push({ version: j.dataset_version, body: JSON.parse(opts.body || '{}') }); return j; }; }
    if (u.endsWith('/quiz/next')) { const j0 = r.json.bind(r); r.json = async () => { const j = await j0(); if (j && j.question) window.__qs.push({ spot: j.question.spot_id, hand: j.question.hand, prompt: j.question.prompt_fr || '', mode: j.question.mode }); return j; }; }
    return r;
  };
});
const made = (p) => p.evaluate(() => window.__made); const qs = (p) => p.evaluate(() => window.__qs);
const reset = (p) => p.evaluate(() => { window.__made = []; window.__qs = []; });
async function onboard(p) {
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await watch(p);
  await p.click('#ob-exp button[data-v="confirme"]'); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); await p.click('#ob-next'); await p.click('#ob-next');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(800);
}
const tab = async (p, t) => { await p.evaluate((x) => { const side = x === 'gto' || x === 'expl' ? x : null;   // 11/11 : gto / expl = onglet Quiz + bouton GTO ou Exploitant
  document.querySelector(`.tab[data-tab="${side ? 'quiz' : x}"]`).click();
  if (side) { const q = [...document.querySelectorAll(`.quiz-switch [data-side="${side}"]`)].find((y) => y.offsetParent); if (q && q.getAttribute('aria-pressed') !== 'true') q.click(); } }, t); await p.waitForTimeout(800); };
async function openChallenges(p) {
  await tab(p, 'defis'); await p.waitForSelector('#challenges:not([hidden])', { timeout: 15000 });
  if (await p.isVisible('#ch-box summary') && !(await p.$eval('#ch-box', (d) => d.open))) await p.click('#ch-box summary');
  await p.waitForTimeout(400);
}
async function relever(p, title) {                                  // le bouton de la carte dont le titre est donné
  const i = await p.$$eval('#ch-list li', (xs, t) => { const li = xs.find((x) => x.innerText.includes(t)); const b = li && li.querySelector('button[data-i]'); return b ? b.dataset.i : null; }, title);
  if (i === null) return false; await p.click(`#ch-list button[data-i="${i}"]`); return true;
}
async function play(p, n) {
  for (let k = 0; k < n; k++) {
    await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(150);
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
}
const isGto = (v) => v && !String(v).startsWith('exploit');
const bankGto = (m) => (m.version ? isGto(m.version) : m.body.mode === 'gto');   // la démo ne renvoie pas dataset_version : le mode de la série

(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => { const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage(); p.on('pageerror', (e) => errs.push(String(e))); return p; };

  // joueur venu de l'onglet Exploitant
  const p = await page(); await onboard(p); await tab(p, 'expl'); await openChallenges(p);
  const ch = await api(p, 'users/me/challenges?mode=exploit&tz=0');
  const weekly = ch.weekly.map((c) => [c.kind, c.category, c.access]);
  ok('API : une carte de la semaine par catégorie disponible, avec category et access',
    JSON.stringify(weekly) === JSON.stringify([['pressure', 'gto', 'free'], ['perfect', 'exploit', 'paid'], ['reader', 'profils', 'paid'], ['range', 'ranges', 'ad']])
    && ch.daily.every((c) => c.category === 'gto' && c.access === 'free') && ch.monthly.every((c) => c.category === null), { daily: ch.daily.map((c) => [c.kind, c.category, c.access]), weekly, monthly: ch.monthly.map((c) => [c.kind, c.category]) });
  ok('API : Équités réservée (non disponible, sans défi)', ch.categories.some((c) => c.key === 'equites' && c.available === false && c.challenge === null)
    && ![...ch.daily, ...ch.weekly, ...ch.monthly].some((c) => c.category === 'equites'), ch.categories);
  const box = await p.innerText('#challenges');
  ok('écran : Équités jamais affichée', !/Équités/.test(box), box.slice(0, 600));
  console.error('observation : catégories nommées à l\'écran :', Object.values(CATS).filter((l) => box.includes(l)).join(', ') || 'aucune');
  const zone = await p.$$eval('#ch-list li', (xs) => xs.map((x) => [x.innerText.split('\n').find((l) => /Défi du jour|Sous pression|Série parfaite|Lecteur de vilain|Range au cordeau|Semaine pleine/.test(l)) || '', !!x.closest('.ch-zone, [data-zone="ad"]') || /publicité/i.test(x.innerText)]));
  ok('écran : seule Range au cordeau est liée à la publicité ; Série parfaite sans cadenas', zone.filter(([, ad]) => ad).every(([t]) => /Range au cordeau/.test(t)) && zone.some(([t, ad]) => /Série parfaite/.test(t) && !ad), zone);

  // défi du jour depuis l'onglet Exploitant : banque GTO
  await reset(p); ok('défi du jour : bouton trouvé', await relever(p, 'Défi du jour')); await play(p, 5);
  const daily1 = await qs(p); const m1 = await made(p);
  ok('défi du jour depuis Exploitant : banque GTO', m1.length === 1 && bankGto(m1[0]) && daily1.every((q) => q.mode !== 'exploit'), m1);
  await p.waitForSelector('#screen-summary:not([hidden])', { timeout: 15000 }); await p.click('#back-home'); await p.waitForTimeout(1000);

  // Sous pression depuis l'onglet Exploitant : banque GTO (abandon après une main)
  await tab(p, 'expl'); await openChallenges(p); await reset(p);
  ok('Sous pression : bouton trouvé', await relever(p, 'Sous pression')); await play(p, 1);
  const m2 = await made(p); const q2 = await qs(p); ok('Sous pression depuis Exploitant : banque GTO', m2.length === 1 && bankGto(m2[0]) && q2.every((q) => q.mode !== 'exploit'), m2);
  await p.click('#home-btn'); await p.waitForTimeout(1000);

  // Série parfaite : banque exploitante
  await openChallenges(p); await reset(p);
  ok('Série parfaite : bouton trouvé', await relever(p, 'Série parfaite')); await play(p, 1);
  const m3 = await made(p); ok('Série parfaite : banque exploitante', m3.length === 1 && !bankGto(m3[0]), m3);
  await p.click('#home-btn'); await p.waitForTimeout(1000);

  // Lecteur de vilain : banque exploitante, au moins 2 « Quelle pastille ? »
  await openChallenges(p); await reset(p);
  ok('Lecteur de vilain : bouton trouvé', await relever(p, 'Lecteur de vilain'));
  const prompts = [];
  for (let k = 0; k < 5; k++) { await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(150); prompts.push(await p.innerText('#screen-question')); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  const m4 = await made(p);
  ok('Lecteur de vilain : banque exploitante, au moins 2 « Quelle pastille ? »', m4.length === 1 && !bankGto(m4[0]) && prompts.filter((t) => /pastille/i.test(t)).length >= 2, { version: m4[0] && m4[0].version, pastille: prompts.filter((t) => /pastille/i.test(t)).length });
  await p.waitForSelector('#screen-summary:not([hidden])', { timeout: 15000 }); await p.click('#back-home'); await p.waitForTimeout(1000);

  // by_category, étapes de la séance, objectifs
  const w = await api(p, 'users/me/wins?mode=exploit&tz=0');
  ok('API : by_category dans /users/me/wins (4 catégories disponibles, Équités réservée)', Array.isArray(w.by_category)
    && JSON.stringify(w.by_category.map((c) => [c.category, c.available])) === JSON.stringify([['gto', true], ['exploit', true], ['profils', true], ['ranges', true], ['equites', false]]), w.by_category && w.by_category.map((c) => [c.category, c.available]));
  const t = await api(p, 'users/me/today?mode=exploit&tz=0'); const g = await api(p, 'users/me/goals?mode=gto&tz=0');
  ok('API : category sur les étapes de la séance', t.steps.every((s) => ['gto', 'exploit', 'profils', 'ranges'].includes(s.category)) && t.steps.some((s) => s.kind === 'range' && s.category === 'ranges'), t.steps.map((s) => [s.kind, s.category]));
  const gl = g.goals || g.items || [];
  ok('API : category sur les objectifs (jours hors catégorie)', gl.length && gl.every((x) => x.kind === 'days' ? x.category === null : !!x.category), gl.map((x) => [x.kind, x.category]));
  // depuis l'écran des équités (Plan, 10/11) : Progression a sa ligne « Équités » (tableau par catégorie) ; aucun défi ni gain Équités en revanche
  await tab(p, 'prog'); ok('Progression : aucun défi ni gain Équités', !/Équités/.test(await p.$eval('#st-challenges', (x) => x.innerText).catch(() => ''))
    && !/Équités/.test(await p.$eval('#st-wins', (x) => x.innerText).catch(() => '')));

  // un autre joueur, venu de l'onglet GTO : les mêmes mains au défi du jour
  const p2 = await page(); await onboard(p2); await tab(p2, 'gto'); await openChallenges(p2); await reset(p2);
  await relever(p2, 'Défi du jour'); await play(p2, 5); const daily2 = await qs(p2);
  ok('défi du jour : mêmes mains, même ordre, depuis GTO et depuis Exploitant', daily2.length === 5 && JSON.stringify(daily2.map((q) => [q.spot, q.hand])) === JSON.stringify(daily1.map((q) => [q.spot, q.hand])),
    { gto: daily2.map((q) => q.hand), exploitant: daily1.map((q) => q.hand) });
  await p.screenshot({ path: `${OUT}/categories_progression.png`, fullPage: true });

  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

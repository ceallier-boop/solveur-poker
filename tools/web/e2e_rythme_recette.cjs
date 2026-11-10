// Recette indépendante de N1 (séance de 10 minutes) et N2 (3 erreurs les plus coûteuses du jour, rejeu), en complément de
// e2e_rythme.cjs (Interface), sans réponse simulée : les réponses sont choisies côté serveur (meilleure ou pire option,
// e2e_audit_helper.py), le rejeu est joué pour de vrai. Application (contrôles croisés par l'API) ou démo (file://…).
//   N1 : étapes affichées = étapes du serveur, en 15 et en 10 minutes ;
//   N2 : rien de coûteux après une série juste ; après une série fausse, 3 erreurs triées par coût ; « Les rejouer » sert ces 3 mains
//        dans l'ordre, chacune annoncée avec son coût ; rejouée juste = « Rattrapée », rejouée fausse = non ; liste stable (ni le
//        rejeu ni une nouvelle série fausse ne la changent) ; le rejeu compte dans les statistiques.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_rythme_recette.cjs [dossier]
//         BASE_URL=file:///…/demo.html node tools/web/e2e_rythme_recette.cjs [dossier]   (démo : python tools/web/build_offline.py demo.html)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.'; const DEMO = BASE.startsWith('file:');
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });

const helper = spawn(process.env.PYTHON || 'python3', [path.join(__dirname, 'e2e_audit_helper.py'), 'picks'], { stdio: ['pipe', 'pipe', 'inherit'] });
const waiting = []; readline.createInterface({ input: helper.stdout }).on('line', (l) => waiting.shift()(JSON.parse(l)));
const pick = (which, q) => new Promise((res) => { waiting.push(res); helper.stdin.write(`${which} ${q.spot_id} ${q.hand}\n`); });

const home = (p) => p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
const api = async (p, route) => {
  const pid = await p.evaluate(() => localStorage.getItem('player_id'));
  return (await fetch(new URL(route, BASE), { headers: { 'X-Player-Id': pid } })).json();
};
const cost = (t) => Number((t.match(/([\d,]+) BB\)?\s*$/) || t.match(/([\d,]+) BB/) || [0, '0'])[1].replace(',', '.'));
const worstList = (p) => p.$$eval('#worst-list li', (xs) => xs.map((x) => x.innerText.replace(/\n+/g, ' | ').trim()));
const plain = (xs) => xs.map((t) => t.replace(/^✓\s*Rattrapée\s*\|?\s*/, '').trim());

async function play(p, choices) {                                  // une question par choix ('best' | 'worst') ; renvoie [question, bannière]
  const seen = [];
  for (const which of choices) {
    await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(150);
    const q = await p.evaluate(() => ({ spot_id: window.__lastQ.spot_id, hand: window.__lastQ.hand }));
    const banner = await p.isVisible('#purpose') ? await p.textContent('#purpose') : '';
    const c = await pick(which, q); seen.push({ ...q, banner, verdict: c.verdict });
    await p.click(`#actions button[data-id="${c.action_id}"]`); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  return seen;
}
async function series(p, which) {
  await p.click('#quick-start'); const s = await play(p, Array(5).fill(which));
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await home(p); await p.waitForTimeout(1200); return s;
}

(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await home(p); await p.waitForTimeout(800);
  await p.evaluate(() => {                                          // dernière question reçue, application ou démo (qui remplace fetch)
    const f = window.fetch;
    window.fetch = async (path, opts) => {
      const r = await f(path, opts);
      if (String(path).includes('/quiz/next')) { const j0 = r.json.bind(r); r.json = async () => { const j = await j0(); if (j && j.question) window.__lastQ = j.question; return j; }; }
      return r;
    };
  });

  // N1 : étapes affichées = étapes du serveur
  const uiSteps = () => p.$$eval('#today-steps li', (xs) => xs.length);
  const s15 = await uiSteps();
  await p.click('#len-switch [data-min="10"]'); await p.waitForFunction(() => /10 min/.test(document.getElementById('today-len').textContent), null, { timeout: 10000 });
  const s10 = await uiSteps();
  if (DEMO) ok('N1 démo : 15 minutes = 3 étapes, 10 minutes = 2 étapes', s15 === 3 && s10 === 2, { s15, s10 });
  else {
    const [t15, t10] = [await api(p, 'users/me/today?mode=gto&tz=0&minutes=15'), await api(p, 'users/me/today?mode=gto&tz=0&minutes=10')];
    ok('N1 : étapes affichées = étapes du serveur (15 et 10 minutes)', s15 === t15.steps.length && s10 === t10.steps.length && t10.minutes === 10 && t10.steps.length < t15.steps.length,
      { ui: [s15, s10], serveur: [t15.steps.length, t10.steps.length] });
  }

  // N2 : série juste → rien de coûteux
  await series(p, 'best');
  await p.openTab('gto');                                            // I9 : les erreurs du jour sont dans l'onglet GTO
  const w0 = await p.isVisible('#worst') ? await worstList(p) : [];
  ok('N2 : après une série juste, « Aucune erreur coûteuse aujourd\'hui », pas de rejeu', w0.length === 1 && /Aucune erreur coûteuse aujourd'hui/.test(w0[0]) && !(await p.isVisible('#worst-replay')), w0);

  // N2 : série fausse → 3 erreurs triées par coût
  const bad = await series(p, 'worst');
  await p.openTab('gto'); const w1 = await worstList(p); const c1 = w1.map(cost);   // I9 : lue onglet affiché (le texte d'un bloc caché se lit autrement)
  ok('N2 : série fausse jouée (5 erreurs ou imprécisions)', bad.every((x) => x.verdict !== 'correct'), bad.map((x) => x.verdict));
  ok('N2 : 3 erreurs, de la plus coûteuse à la moins coûteuse', w1.length === 3 && c1[0] >= c1[1] && c1[1] >= c1[2] && c1[2] > 0, w1);
  let server = null;
  if (!DEMO) {
    server = (await api(p, 'users/me/worst-today?mode=gto&tz=0')).errors;
    ok('N2 : la liste affichée est celle du serveur (coût et terme de ton choix, traduit au niveau 1)', server.length === 3 && server.every((e, k) => w1[k].includes(e.cost_fr) && w1[k].includes(e.chosen_fr.split(' ')[0])), { ui: w1, serveur: server.map((e) => [e.chosen_fr, e.cost_fr]) });
  }
  await p.screenshot({ path: `${OUT}/rythme_recette_worst.png`, fullPage: true });

  // N2 : « Les rejouer » : les 3 mêmes mains, dans l'ordre ; juste, faux, juste
  await p.click('#worst-replay');
  const rp = await play(p, ['best', 'worst', 'best']);
  await p.waitForSelector('#screen-summary:not([hidden])');
  ok('N2 : rejeu de 3 questions, chacune annoncée avec son coût, dans l\'ordre de la liste',
    rp.every((x, k) => /Rejeu de ton erreur du jour/.test(x.banner) && cost(x.banner) === c1[k]), rp.map((x) => x.banner));
  if (server) ok('N2 : le rejeu sert les mêmes situations et mains que la liste du serveur', rp.every((x, k) => x.spot_id === server[k].spot_id && x.hand === server[k].hand));
  await p.click('#back-home'); await home(p); await p.waitForTimeout(1200);
  await p.openTab('gto'); const w2 = await worstList(p);
  ok('N2 : la liste ne change pas après le rejeu (ses erreurs n\'y entrent pas)', JSON.stringify(plain(w2)) === JSON.stringify(plain(w1)), { avant: w1, après: w2 });
  ok('N2 : rejouée juste « Rattrapée », rejouée fausse non', /Rattrapée/.test(w2[0]) && !/Rattrapée/.test(w2[1]) && /Rattrapée/.test(w2[2]), w2);
  ok('N2 : « Les rejouer » reste proposé pour l\'erreur non rattrapée', await p.isVisible('#worst-replay'));

  // N2 : une nouvelle série fausse ne change pas la liste du jour
  await series(p, 'worst');
  await p.openTab('gto');
  ok('N2 : liste stable après une nouvelle série fausse', JSON.stringify(plain(await worstList(p))) === JSON.stringify(plain(w1)), await worstList(p));
  if (!DEMO) ok('N2 : le rejeu compte dans les statistiques (5 + 5 + 3 + 5 questions)', (await api(p, 'users/me/stats')).questions === 18);
  await p.screenshot({ path: `${OUT}/rythme_recette_caught.png`, fullPage: true });

  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  helper.stdin.end(); await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Décisions du 05/11 (I8, P13) : quand les experts sont partagés, la correction montre les deux stratégies comme possibles,
// la plus recommandée avec sa nuance (« 2 experts sur 3 ») et le choix du joueur. Le champ `avis` de la correction est
// injecté (réponse réelle du serveur complétée ; au niveau 1, les libellés sont en français, AU8) pour ne pas dépendre du tirage. Application seulement (la démo n'a pas de réseau).
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_avis.cjs [dossier]
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
// cas : 'rec' (choix le plus recommandé), 'autre' (choix d'un seul expert), 'aucun' (choix qu'aucun expert n'a joué : nuance_fr null)
const avisOf = (chosen, k) => ({ split: true, experts: 3, nuance_fr: k === 'rec' ? '2 experts sur 3' : k === 'autre' ? '1 expert sur 3' : null, recommended: k === 'rec', recommended_label: 'RAISE TO 7,6 BB',
  options: [{ id: k === 'rec' ? chosen : 'R7.59', label_fr: 'RAISE TO 7,6 BB', experts: 2 }, { id: k === 'autre' ? chosen : 'A', label_fr: 'ALL-IN 25 BB', experts: 1 }] });
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const k of ['rec', 'autre', 'aucun']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e)));
    await p.route('**/attempts', async (route) => {
      const res = await route.fetch(); const body = await res.json();
      body.avis = avisOf(body.chosen_action, k); body.details_fr = [...(body.details_fr || []), "Les experts ne sont pas d'accord sur cette main : phrase déjà dans le bloc."];
      route.fulfill({ response: res, json: body });
    });
    await p.goto(BASE);
    await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
    if (await p.isVisible('#screen-onboard')) { await p.click('#ob-skip'); await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])'); }
    await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    const box = await p.innerText('#a-avis'), verdict = await p.innerText('#a-verdict');
    const tag = { rec: 'recommandé', autre: 'autre stratégie', aucun: 'aucun expert' }[k];
    ok(`${tag} : bloc des experts visible`, await p.isVisible('#a-avis') && (k === 'aucun' ? /Les experts sont partagés entre (RAISE TO 7,6 BB|Relancer à 7,6 BB \(RAISE TO\)) et (ALL-IN 25 BB|Tapis 25 BB \(ALL-IN\)) ; ton choix n'a été retenu par aucun\./.test(box) : /deux stratégies sont possibles/.test(box)), box);
    ok(`${tag} : nuance et plus recommandé`, /2 experts sur 3 · le plus recommandé/.test(box) && /1 expert sur 3/.test(box), box);
    ok(`${tag} : ton choix marqué une fois`, (box.match(/ton choix/g) || []).length === 1, box);   // « aucun » : dans le titre, pas sur une option
    ok(`${tag} : bandeau du verdict`, k === 'rec' ? /le plus recommandé par les experts \(2 experts sur 3\)/.test(verdict)
      : k === 'autre' ? /Une stratégie possible \(1 expert sur 3\) ; les experts recommandent plutôt (RAISE TO 7,6 BB|Relancer à 7,6 BB \(RAISE TO\))/.test(verdict)
      : !/expert/.test(verdict), verdict);                                                         // « aucun » : le verdict du solveur, tel quel
    await p.click('#a-more summary');
    ok(`${tag} : pas de redite dans les précisions`, !/Les experts ne sont pas d'accord/.test(await p.innerText('#a-details')));
    ok(`${tag} : ni « coach » ni nom à l'écran`, !/coach|lucho|lucky|\bPA\b/i.test(box + verdict));
    await p.screenshot({ path: `${OUT}/avis_${k}.png`, fullPage: true });
    await p.unroute('**/attempts'); await p.click('#next-btn'); await p.waitForSelector('#screen-question:not([hidden])');
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    ok(`${tag} : main sans avis, pas de bloc`, !(await p.isVisible('#a-avis')));
    await ctx.close();
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

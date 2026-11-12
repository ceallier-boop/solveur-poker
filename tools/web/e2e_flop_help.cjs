// Équités v2, sorte « flop_help » (ce flop t'aide-t-il ?), avec assertions : série depuis la carte Équités ; question : le flop au-dessus de
// ta main, la range adverse en grille, trois réponses en texte sur une colonne ; correction : verdict sans « tranche », l'écart en points
// sur la bonne ligne, équité avant le flop puis au flop, ce que la main a, jamais de BB perdus.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_flop_help.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  await p.openTab('exos');
  ok('carte Équités : « Ce flop t\'aide-t-il ? »', await p.isVisible('#equity-kinds [data-kind="flop_help"]'));
  await p.click('#equity-kinds [data-kind="flop_help"]'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  const q = await p.evaluate(() => ({ kind: document.getElementById('eq-kind').textContent, flop: document.querySelectorAll('#eq-board .street.flop .card').length,
    hand: document.querySelectorAll('#eq-cards .card').length, cells: document.querySelectorAll('#eq-range .mini-grid i').length,
    stmts: document.getElementById('actions').classList.contains('stmts'), bands: document.getElementById('actions').classList.contains('bands'),
    opts: [...document.querySelectorAll('#actions button b')].map((x) => x.textContent) }));
  ok('question : flop, ta main, la range adverse en grille', q.kind === 'Ce flop t\'aide-t-il ?' && q.flop === 3 && q.hand === 2 && q.cells === 169, q);
  ok('question : trois réponses en texte, sur une colonne', q.opts.length === 3 && q.stmts && !q.bands && q.opts.every((t) => /(augmente|change|monte|baisse)/.test(t)), q.opts);
  await p.screenshot({ path: `${OUT}/flop_help_question.png` });
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  const a = await p.evaluate(() => ({ verdict: document.getElementById('a-verdict').innerText, good: (document.querySelector('#a-equity .eq-bands li.good small') || {}).textContent || '',
    rows: [...document.querySelectorAll('#a-equity .st-row')].length, essential: document.getElementById('a-essential').textContent, text: document.getElementById('screen-answer').innerText }));
  ok('correction : verdict sans « tranche »', !/tranche/i.test(a.verdict) && /(Bonne réponse|La bonne réponse)/.test(a.verdict), a.verdict);
  ok('correction : l\'écart en points sur la bonne ligne', /✓ [+−]?[\d,]+ points?( · ta réponse)?$/.test(a.good), a.good);
  ok('correction : avant le flop puis au flop, et la phrase de l\'écart', a.rows === 2 && /avant le flop .* points?\)/.test(a.essential), a.essential);
  ok('correction : jamais de BB perdus', !/BB perdus|coûte/.test(a.text));
  await p.screenshot({ path: `${OUT}/flop_help_correction.png`, fullPage: true });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

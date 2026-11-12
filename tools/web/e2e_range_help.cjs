// Équités v2, sorte « range_help » (range contre range), avec assertions : série depuis la carte Équités ; question : le flop, pas de main
// du héros, les deux ranges côte à côte (« Ta range » puis « Contre »), chacune en grille 13 × 13, trois réponses en texte sur une colonne ;
// correction : verdict sans « tranche », l'écart en points, le tableau des deux ranges avant et au flop et leur part de double paire ou
// mieux, sans « null » nulle part, jamais de BB perdus.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_range_help.cjs [dossier]   (application ou file://…/demo.html)
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
  ok('carte Équités : « Range contre range »', await p.isVisible('#equity-kinds [data-kind="range_help"]'));
  await p.click('#equity-kinds [data-kind="range_help"]'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  const q = await p.evaluate(() => ({ kind: document.getElementById('eq-kind').textContent, flop: document.querySelectorAll('#eq-board .street.flop .card').length,
    handShown: !document.getElementById('eq-cards').hidden, grids: document.querySelectorAll('#eq-range .mini-grid').length,
    cells: [...document.querySelectorAll('#eq-range .mini-grid')].map((g) => g.querySelectorAll('i').length),
    titles: [...document.querySelectorAll('#eq-range .eq-range-title')].map((t) => t.textContent), two: document.getElementById('eq-range').classList.contains('two'),
    stmts: document.getElementById('actions').classList.contains('stmts'), opts: [...document.querySelectorAll('#actions button b')].map((x) => x.textContent),
    page: document.getElementById('screen-question').innerText }));
  ok('question : le flop, pas de main du héros', q.kind === 'Range contre range' && q.flop === 3 && !q.handShown, q);
  ok('question : les deux ranges côte à côte, « Ta range » puis « Contre », en grilles 13 × 13', q.grids === 2 && q.two && q.cells.every((n) => n === 169)
    && /^Ta range : /.test(q.titles[0]) && /^Contre : /.test(q.titles[1]) && !/Toi, /.test(q.titles[0]), q.titles);
  ok('question : trois réponses en texte sur une colonne', q.opts.length === 3 && q.stmts, q.opts);
  ok('question : jamais « null » à l\'écran', !/\bnull\b/.test(q.page));
  await p.screenshot({ path: `${OUT}/range_help_question.png` });
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  const a = await p.evaluate(() => ({ verdict: document.getElementById('a-verdict').innerText, good: (document.querySelector('#a-equity .eq-bands li.good small') || {}).textContent || '',
    rows: [...document.querySelectorAll('#a-equity .eq-vs tbody tr')].map((r) => r.innerText.replace(/\s+/g, ' ').trim()),
    hand: !document.getElementById('a-cards').hidden, essential: document.getElementById('a-essential').textContent, recap: document.getElementById('a-recap').textContent, text: document.getElementById('screen-answer').innerText }));
  ok('correction : verdict sans « tranche »', !/tranche/i.test(a.verdict) && /(Bonne réponse|La bonne réponse)/.test(a.verdict), a.verdict);
  ok('correction : l\'écart en points sur la bonne ligne', /✓ [+−]?[\d,]+ points?( · ta réponse)?$/.test(a.good), a.good);
  const num = (t) => ((t || '').match(/([+−]?[\d,]+) points?/) || [])[1];   // l'écart de la bonne ligne = celui de la phrase du serveur
  ok('correction : même écart que la phrase du serveur', num(a.good) && num(a.good).replace('+', '') === (num(a.essential) || '').replace('+', ''), [a.good, a.essential]);
  ok('correction : les deux ranges avant et au flop, double paire ou mieux', a.rows.length === 3 && /^Avant le flop [\d,]+ % [\d,]+ %$/.test(a.rows[0])
    && /^Au flop [\d,]+ % [\d,]+ %$/.test(a.rows[1]) && /^Double paire ou mieux [\d,]+ % [\d,]+ %$/.test(a.rows[2]), a.rows);
  ok('correction : pas de main, pas de « null », jamais de BB perdus', !a.hand && !/\bnull\b/.test(a.text + a.recap) && !/BB perdus|coûte/.test(a.text), a.recap);
  ok('correction : la nuance visible (l\'équité n\'est pas l\'argent / améliorer n\'est pas passer devant), pas répétée dans les précisions', await p.isVisible('#a-equity .eq-caveat') && /argent|passer devant/i.test(await p.textContent('#a-equity .eq-caveat')) && !(await p.textContent('#a-details')).includes(await p.textContent('#a-equity .eq-caveat')));
  await p.screenshot({ path: `${OUT}/range_help_correction.png`, fullPage: true });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Équités v2, sorte « nut_help » (qui a le plus de mains très fortes sur ce flop ?), avec assertions : série depuis la carte Équités ;
// question : le flop, pas de main du héros, les deux ranges côte à côte en grilles 13 × 13, trois réponses en texte ; correction : verdict
// sans « tranche », l'écart en points identique à la phrase du serveur, la part de mains très fortes de chaque range, pas de ligne
// d'équité avant / au flop, jamais « null » ni BB perdus.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_nut_help.cjs [dossier]   (application ou file://…/demo.html)
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
  ok('carte Équités : « Mains très fortes »', await p.isVisible('#equity-kinds [data-kind="nut_help"]'));
  await p.click('#equity-kinds [data-kind="nut_help"]'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  const q = await p.evaluate(() => ({ kind: document.getElementById('eq-kind').textContent, flop: document.querySelectorAll('#eq-board .street.flop .card').length,
    handShown: !document.getElementById('eq-cards').hidden, grids: document.querySelectorAll('#eq-range .mini-grid').length,
    titles: [...document.querySelectorAll('#eq-range .eq-range-title')].map((t) => t.textContent),
    stmts: document.getElementById('actions').classList.contains('stmts'), opts: [...document.querySelectorAll('#actions button b')].map((x) => x.textContent),
    page: document.getElementById('screen-question').innerText }));
  ok('question : le flop, pas de main du héros, les deux ranges', q.kind === 'Mains très fortes' && q.flop === 3 && !q.handShown && q.grids === 2
    && /^Toi, /.test(q.titles[0]) && /^Lui : /.test(q.titles[1]), q);
  ok('question : trois réponses en texte sur une colonne, jamais « null »', q.opts.length === 3 && q.stmts && !/\bnull\b/.test(q.page), q.opts);
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  const a = await p.evaluate(() => ({ verdict: document.getElementById('a-verdict').innerText, good: (document.querySelector('#a-equity .eq-bands li.good small') || {}).textContent || '',
    head: (document.querySelector('#a-equity h4') || {}).textContent || '', rows: [...document.querySelectorAll('#a-equity .eq-vs tbody tr')].map((r) => r.innerText.replace(/\s+/g, ' ').trim()),
    essential: document.getElementById('a-essential').textContent, text: document.getElementById('screen-answer').innerText }));
  const num = (t) => ((t || '').match(/([+−]?[\d,]+) points?/) || [])[1];
  ok('correction : verdict sans « tranche »', !/tranche/i.test(a.verdict) && /(Bonne réponse|La bonne réponse)/.test(a.verdict), a.verdict);
  ok('correction : même écart que la phrase du serveur', num(a.good) && num(a.good).replace('+', '') === (num(a.essential) || '').replace('+', ''), [a.good, a.essential]);
  ok('correction : la part de mains très fortes de chaque range, sans équité avant / au flop', /mains très fortes/i.test(a.head) && a.rows.length === 1
    && /^Mains très fortes [\d,]+ % [\d,]+ %$/.test(a.rows[0]), [a.head, a.rows]);
  ok('correction : jamais « null » ni BB perdus', !/\bnull\b/.test(a.text) && !/BB perdus|coûte/.test(a.text));
  await p.screenshot({ path: `${OUT}/nut_help_correction.png`, fullPage: true });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

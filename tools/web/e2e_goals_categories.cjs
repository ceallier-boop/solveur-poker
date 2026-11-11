// Objectifs de la semaine indépendants de l'onglet ouvert (10/11, même règle que le niveau), avec assertions : toujours ceux de GTO, objectif
// « BB perdus » libellé « … de Préflop GTO » ; après une série exploitante, l'objectif « … de Préflop exploitant » s'ajoute (jours et ranges
// une seule fois) ; ouvrir l'onglet Exploitant ne change pas la liste ; modifier la cible exploitante ne touche pas celle de GTO.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_goals_categories.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const goals = (p) => p.$$eval('#goals-list li', (xs) => xs.map((x) => ({ cat: x.dataset.cat, label: x.querySelector('.goal-top span').textContent.replace(/^✓ /, '') })));
const series = async (p) => { for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); } await p.waitForSelector('#screen-summary:not([hidden])'); };
const openProg = async (p) => { await p.openTab('prog'); await p.waitForSelector('#screen-stats:not([hidden]) #goals:not([hidden])', { timeout: 15000 }); await p.waitForTimeout(1200); };
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });

  await openProg(p);
  const g0 = await goals(p);
  ok('nouveau joueur : les trois objectifs de GTO', g0.length === 3 && g0.some((x) => /de Préflop GTO$/.test(x.label)) && !g0.some((x) => /exploitant/.test(x.label)), g0);
  ok('pas de « · GTO » ni « · Exploitant » dans le titre', !(await p.textContent('#goals-mode')).trim());
  // l'onglet Exploitant ouvert avant Progression ne change rien
  await p.openTab('expl'); await p.waitForTimeout(800); await openProg(p);
  ok('après l\'onglet Exploitant : toujours les objectifs de GTO', JSON.stringify(await goals(p)) === JSON.stringify(g0), await goals(p));
  // une série exploitante : l'objectif de Préflop exploitant s'ajoute
  await p.openTab('expl'); await p.click('#quick-start'); await series(p); await p.click('#back-home');
  await openProg(p);
  const g1 = await goals(p);
  ok('après une série exploitante : quatre objectifs, dont « … de Préflop exploitant »', g1.length === 4 && g1.filter((x) => /de Préflop exploitant$/.test(x.label)).length === 1
    && g1.filter((x) => /de Préflop GTO$/.test(x.label)).length === 1, g1);
  ok('jours et ranges une seule fois', g1.filter((x) => x.cat === '' || x.cat === 'ranges').length === 2, g1);
  await p.screenshot({ path: `${OUT}/goals_categories.png`, fullPage: true });
  // modifier la cible exploitante seulement
  const target = (m) => p.$eval(`#goals-list button[data-k="precision"][data-m="${m}"][data-d="1"]`, (x) => x.previousElementSibling.textContent).catch(() => null);
  await p.click('#goals-edit');
  const gtoBefore = await target('gto'), xBefore = await target('exploit');
  await p.click('#goals-list button[data-k="precision"][data-m="exploit"][data-d="1"]'); await p.waitForTimeout(1200);
  const gtoAfter = await target('gto'), xAfter = await target('exploit');
  ok('cible exploitante modifiée, celle de GTO intacte', xBefore !== null && xAfter !== xBefore && gtoAfter === gtoBefore, { gtoBefore, gtoAfter, xBefore, xAfter });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

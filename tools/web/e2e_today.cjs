// Séance du jour (programme de travail, étape 1) : accueil, enchaînement révision / thème (2 séries) / range, écran de fin.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_today.cjs [dossier]
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => {          // étape 4 : un nouveau joueur voit d'abord le premier lancement
  try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
    if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ }
};
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForSelector('#today:not([hidden])', { timeout: 15000 });
  const res = { home: await p.innerText('#today'), primary: await p.$$eval('#screen-home .primary', (x) => x.filter((y) => y.offsetParent).map((y) => y.textContent.trim())) };
  await p.screenshot({ path: `${OUT}/today_home.png` });
  const series = async () => { for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); } await p.waitForSelector('#screen-summary:not([hidden])'); };
  await p.click('#today-go'); await series(); res.after1 = await p.textContent('#again-btn');
  await p.click('#again-btn'); await series(); res.after2 = await p.textContent('#again-btn');
  await p.click('#again-btn'); await p.waitForSelector('#screen-range:not([hidden])'); res.range = await p.textContent('#rg-question');
  await p.click('#rg-grid .rc:not([disabled]) >> nth=0'); await p.click('#rg-submit'); await p.waitForSelector('#rg-result:not([hidden])');
  res.rangeBtn = await p.textContent('#rg-again'); await p.click('#rg-again'); await p.waitForSelector('#screen-today:not([hidden])');
  res.done = await p.innerText('#screen-today'); await p.screenshot({ path: `${OUT}/today_done.png` });
  await p.click('#td-home'); await p.waitForTimeout(1200); res.homeAfter = await p.innerText('#today');
  await p.screenshot({ path: `${OUT}/today_home_done.png` });
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

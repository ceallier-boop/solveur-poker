// Objectifs de la semaine (programme de travail, étape 3) : affichage, modification d'une cible, effet d'une séance.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_goals.cjs [dossier]
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await p.waitForSelector('#goals:not([hidden])', { timeout: 15000 });
  const goals = () => p.$$eval('#goals-list li', (x) => x.map((y) => y.innerText.replace(/\n+/g, ' | ')));
  const res = { before: await goals() };
  await p.click('#goals-edit'); await p.click('#goals-list button[data-k="days"][data-d="-1"]'); await p.waitForTimeout(600);
  res.edited = await goals(); await p.click('#goals-edit');
  await p.click('#today-go');
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(1500);
  res.after = await goals(); await p.screenshot({ path: `${OUT}/goals_home.png`, fullPage: true });
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

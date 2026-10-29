// Défis (programme de travail, étape 5 ; test joueurs 9) : défis repliés, défi du jour au chrono 15 s, « Nouveau défi demain », une seule tentative, « Mes défis ».
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_challenges.cjs [dossier]
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => { try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
  if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ } };
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForSelector('#challenges:not([hidden])', { timeout: 15000 });
  const list = () => p.$$eval('#ch-list li', (x) => x.map((y) => y.innerText.replace(/\n+/g, ' | ')));
  const res = { folded: await p.innerText('#ch-box summary'), before: await list() };          // test joueurs 9 : défis repliés en une ligne
  await p.click('#ch-box summary');
  await p.click('#ch-list li:first-child button'); await p.waitForSelector('#screen-question:not([hidden])');
  res.timer = await p.textContent('#q-timer').catch(() => null);
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=-1'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.waitForSelector('.ch-result', { timeout: 10000 }); res.result = await p.textContent('.ch-result');
  await p.click('#back-home'); await p.waitForTimeout(1500); res.after = await list(); res.foldedAfter = await p.innerText('#ch-box summary');
  if (!(await p.getAttribute('#ch-box', 'open'))) await p.click('#ch-box summary');
  res.dailyButton = await p.isVisible('#ch-list li:first-child button');
  await p.screenshot({ path: `${OUT}/ch_home.png`, fullPage: true });
  await p.click('#stats-btn'); await p.waitForSelector('#st-challenges:not([hidden])', { timeout: 10000 }); res.mine = (await p.innerText('#st-challenges')).replace(/\n+/g, ' | ');
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

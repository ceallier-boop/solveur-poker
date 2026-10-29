// Corrections du test joueurs 9 : mode en haut et niveau qui le suit, chrono en pause pendant une erreur « trop de requêtes ».
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_retest9.cjs [dossier]
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => { try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
  if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ } };
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForSelector('#today:not([hidden])', { timeout: 15000 });
  const res = { modeFirst: await p.evaluate(() => !!(document.querySelector('.mode-switch').compareDocumentPosition(document.getElementById('today')) & Node.DOCUMENT_POSITION_FOLLOWING)) };
  res.homeHeight = await p.evaluate(() => document.getElementById('screen-home').scrollHeight);
  await p.screenshot({ path: `${OUT}/r9_home.png`, fullPage: true });
  await p.click('.mode-switch [data-value="exploit"]'); await p.waitForTimeout(1500);
  res.levelExploit = await p.innerText('#today-level');
  await p.click('#stats-btn'); await p.waitForSelector('#st-level:not([hidden])', { timeout: 10000 });
  res.progressExploit = await p.innerText('#st-level-name'); res.picked = await p.textContent('#st-level-pick [aria-pressed="true"]');
  await p.click('#st-back'); await p.click('.mode-switch [data-value="gto"]'); await p.waitForTimeout(1500);
  res.levelGto = await p.innerText('#today-level');
  // erreur 429 sur la réponse : le chrono s'arrête derrière le message et repart à la fermeture
  let fail = true;
  await p.route('**/attempts', (r) => (fail ? (fail = false, r.fulfill({ status: 429, contentType: 'application/json', body: JSON.stringify({ detail: 'Trop de requêtes en peu de temps : attends 5 s avant de réessayer.' }) })) : r.continue()));
  await p.click('.chrono-row [data-value="15"]'); await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  await p.waitForTimeout(1200); await p.click('#actions button >> nth=0'); await p.waitForSelector('#notice:not([hidden])');
  const t1 = await p.textContent('#q-timer span'); await p.waitForTimeout(3000); const t2 = await p.textContent('#q-timer span');
  res.pausedDuringError = t1 === t2; res.timerAtError = t1;
  await p.click('#notice-close'); await p.waitForTimeout(2200); res.runsAgain = (await p.textContent('#q-timer span')) !== t2;
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); res.verdict = await p.innerText('#a-verdict');
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

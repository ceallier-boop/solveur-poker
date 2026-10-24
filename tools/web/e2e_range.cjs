// Chantiers 2 et 5 : « Construis ta range » (colorier en glissant, correction), mode chrono à 8 s (fold automatique),
// BB perdus dans le bilan et la progression, réglage du chrono gardé. Usage : BASE_URL=http://localhost:8061/ node tools/web/e2e_range.cjs [dossier]
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2] || '.'; const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const b = await chromium.launch(); const res = {};
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true })).newPage();
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); if (process.argv[2]) await p.screenshot({ path: `${out}/accueil.png` });
  // range
  await p.tap('#range-btn'); await p.waitForSelector('#screen-range:not([hidden])');
  res.question = await p.textContent('#rg-question');
  const box = await p.locator('#rg-grid').boundingBox(); const cell = box.width / 13;
  // glisser sur la première ligne (A) puis sur la diagonale des paires par touchers
  await p.mouse.move(box.x + cell * 0.5, box.y + cell * 0.5); await p.mouse.down();
  for (let j = 1; j < 13; j++) await p.mouse.move(box.x + cell * (j + 0.5), box.y + cell * 0.5);
  await p.mouse.up();
  for (let i = 0; i < 12; i++) await p.locator('#rg-grid .rc:not([disabled]):not(.on)').first().click();   // 12 cases de plus, parmi celles en jeu
  res.count = await p.textContent('#rg-count');
  if (process.argv[2]) await p.screenshot({ path: `${out}/range_edit.png` });
  await p.tap('#rg-submit'); await p.waitForSelector('#rg-result:not([hidden])');
  res.score = (await p.textContent('.rg-score')).trim();
  if (process.argv[2]) await p.screenshot({ path: `${out}/range_result.png` });
  // chrono 8 s
  await p.tap('#rg-home'); await p.click('.chips[data-name="chrono"] [data-value="8"]'); await p.tap('#quick-start');
  await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(1500); if (process.argv[2]) await p.screenshot({ path: `${out}/chrono.png` });
  await p.waitForSelector('#screen-answer:not([hidden])', { timeout: 15000 }); res.timeout = (await p.textContent('#a-verdict')).trim().slice(0, 120);
  for (let i = 1; i < 5; i++) { await p.tap('#next-btn'); await p.waitForSelector('#screen-question:not([hidden])'); await p.locator('#actions button').last().tap(); await p.waitForSelector('#screen-answer:not([hidden])'); }
  await p.tap('#next-btn'); await p.waitForSelector('#screen-summary:not([hidden])'); res.summary = (await p.textContent('#s-score')).trim();
  await p.tap('#back-home'); await p.tap('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.waitForTimeout(300);
  res.stats = (await p.textContent('#st-score')).trim(); if (process.argv[2]) await p.screenshot({ path: `${out}/stats.png` });
  res.chronoKept = await (async () => { await p.goto(BASE); return p.getAttribute('.chips[data-name="chrono"] [data-value="8"]', 'aria-pressed'); })();
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

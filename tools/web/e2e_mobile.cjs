// Parcours complet sur mobile (390 x 844) : accueil, 5 questions, bilan ; captures d'écran et erreurs JavaScript.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_mobile.cjs <dossier_captures> [light|dark]
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const out = process.argv[2]; const errors = [];
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: process.argv[3] || 'light' });
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(String(e))); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await p.goto(process.env.BASE_URL || 'http://localhost:8000/'); await p.screenshot({ path: out + '/1_accueil.png' });
  await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  await p.screenshot({ path: out + '/2_question.png' });
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])');
    const n = await p.locator('#actions button').count();
    await p.locator('#actions button').nth(i % n).click();
    await p.waitForSelector('#screen-answer:not([hidden])');
    if (i === 0) await p.screenshot({ path: out + '/3_correction.png', fullPage: true });
    await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.screenshot({ path: out + '/4_bilan.png', fullPage: true });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  console.log(JSON.stringify({ errors, horizontalOverflow: overflow }));
  await b.close();
})();

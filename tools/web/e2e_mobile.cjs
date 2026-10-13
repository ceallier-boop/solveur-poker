// Parcours complet sur mobile (390 x 844) : accueil, 5 questions (dont un signalement), bilan ; captures d'écran et erreurs JavaScript.
// Usage : BASE_URL=http://localhost:8000/ [MODE=exploit] [EXTRA_SERIES=n] node tools/web/e2e_mobile.cjs <dossier_captures> [light|dark]
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const out = process.argv[2]; const errors = [];
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: process.argv[3] || 'light' });
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(String(e))); p.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await p.goto(process.env.BASE_URL || 'http://localhost:8000/'); await p.screenshot({ path: out + '/1_accueil.png' });
  if (process.env.MODE === 'exploit') await p.click('.mode-switch [data-value="exploit"]');
  await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  await p.screenshot({ path: out + '/2_question.png' });
  await p.click('#lex-btn'); await p.waitForSelector('#lex:not([hidden]) #lex-body dl');            // lexique de l'écran
  const lexOk = await p.evaluate(() => document.getElementById('lex-body').innerText.includes('Sur cet écran'));
  if (!lexOk) errors.push('lexique : aucun terme repéré sur l\'écran de question');
  await p.screenshot({ path: out + '/2b_lexique.png' });
  await p.fill('#lex-search', 'équité'); await p.waitForTimeout(100);
  if (!(await p.locator('#lex-body dt').count())) errors.push('lexique : recherche sans résultat');
  await p.keyboard.press('Escape'); await p.waitForSelector('#lex', { state: 'hidden' });
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])');
    const n = await p.locator('#actions button').count();
    await p.locator('#actions button').nth(i % n).click();
    await p.waitForSelector('#screen-answer:not([hidden])');
    if (i === 0) {
      await p.screenshot({ path: out + '/3_correction.png', fullPage: true });
      if (await p.locator('#a-why-box').isVisible()) await p.click('#a-why-box summary');
      if (await p.locator('#a-next-box').isVisible()) await p.click('#a-next-box summary');
      if (await p.locator('#a-grid-box').isVisible()) await p.click('#a-grid-box summary');
      await p.screenshot({ path: out + '/3c_pourquoi_grille.png', fullPage: true });
      if (await p.locator('#report').isVisible()) {
      await p.click('#report summary'); await p.check('input[value="unclear"]'); await p.fill('#report-comment', 'test e2e');
      await p.click('#report-form button[type=submit]');
      await p.waitForSelector('#report-done:not([hidden]), #demo-toast:not([hidden])');   // démo hors claude.ai : message d'indisponibilité
      await p.screenshot({ path: out + '/3b_signalement.png', fullPage: true });
      }
    }
    if (i === 1 && !(await p.locator('#report-done').isHidden())) errors.push('signalement affiché comme envoyé sur une autre question');
    await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.screenshot({ path: out + '/4_bilan.png', fullPage: true });
  for (let s = 0; s < Number(process.env.EXTRA_SERIES || 0); s++) {              // séries supplémentaires pour remplir les statistiques
    await p.click('#again-btn');
    for (let i = 0; i < 5; i++) {
      await p.waitForSelector('#screen-question:not([hidden])');
      const n = await p.locator('#actions button').count(); await p.locator('#actions button').nth((i + s) % n).click();
      await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
    }
    await p.waitForSelector('#screen-summary:not([hidden])');
  }
  await p.click('#back-home'); await p.click('#stats-btn');
  await p.waitForSelector('#screen-stats:not([hidden])'); await p.screenshot({ path: out + '/5_progression.png', fullPage: true });
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  console.log(JSON.stringify({ errors, horizontalOverflow: overflow }));
  await b.close();
})();

// Hors connexion : après une série en ligne, la page s'ouvre sans réseau (service worker) et « Ma progression » affiche la dernière
// progression gardée sur l'appareil, datée ; export et effacement sont masqués.
// Usage : BASE_URL=http://localhost:8061/ node tools/web/e2e_offline.cjs [dossier_captures]
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => {          // étape 4 : un nouveau joueur voit d'abord le premier lancement
  try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
    if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ }
};
(async () => {
  const out = process.argv[2] || '.'; const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const b = await chromium.launch(); const res = {};
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForFunction(() => navigator.serviceWorker && navigator.serviceWorker.controller || false, null, { timeout: 5000 }).catch(() => {});
  await p.tap('#quick-start');
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.locator('#actions button').first().tap(); await p.waitForSelector('#screen-answer:not([hidden])'); await p.tap('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.waitForTimeout(800);
  res.cached = await p.evaluate(() => !!localStorage.getItem('stats_cache'));
  res.swControlled = await p.evaluate(() => !!navigator.serviceWorker.controller);
  await ctx.setOffline(true);
  await p.reload(); await p.waitForSelector('#screen-home:not([hidden])');
  res.homeOffline = true;
  await p.tap('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])');
  res.note = await p.textContent('#st-offline'); res.score = (await p.textContent('#st-score')).trim();
  res.exportHidden = await p.isHidden('#st-export');
  if (process.argv[2]) await p.screenshot({ path: `${out}/progression_hors_ligne.png`, fullPage: true });
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

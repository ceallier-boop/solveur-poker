// Recommandations de l'accueil et conseiller ouvert depuis une correction (programme de travail, étape 2).
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_recs.cjs [dossier] ; PLAYER=<id> pour un joueur existant
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => {          // étape 4 : un nouveau joueur voit d'abord le premier lancement
  try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
    if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ }
};
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  if (process.env.PLAYER) await ctx.addInitScript((id) => localStorage.setItem('player_id', id), process.env.PLAYER);
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForSelector('#recs:not([hidden])', { timeout: 15000 });
  const res = { recs: await p.$$eval('#recs-list li', (x) => x.map((y) => y.innerText.replace(/\n+/g, ' | '))) };
  await p.screenshot({ path: `${OUT}/recs_home.png`, fullPage: true });
  await p.click('#recs-list button >> nth=0'); await p.waitForSelector('#screen-question:not([hidden]), #screen-range:not([hidden])', { timeout: 15000 });
  res.started = await p.evaluate(() => [...document.querySelectorAll('.screen')].find((s) => !s.hidden).id);
  if (res.started === 'screen-question') {
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    res.conseilLink = (await p.isVisible('#a-conseil')) ? await p.getAttribute('#a-conseil', 'href') : null;
    if (res.conseilLink && !/\.html/.test(BASE)) {
      await p.click('#a-conseil'); await p.waitForSelector('#verdict', { timeout: 15000 }); await p.waitForTimeout(1200);
      res.conseil = (await p.innerText('#verdict')).replace(/\n+/g, ' | '); res.hand = await p.inputValue('#hand');
      await p.screenshot({ path: `${OUT}/recs_conseil.png` });
    }
  }
  res.errs = errs; console.log(JSON.stringify(res, null, 1)); await b.close();
})();

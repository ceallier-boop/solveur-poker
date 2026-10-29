// Contrôles avant la bêta (lot A, 23/10/2026), sur un serveur de test lancé avec SPINSACADEMY_ADMIN_TOKEN :
//   A10 signalement de bout en bout : envoi depuis la correction, lecture et clôture côté administration ;
//   A11 premier chargement en 4G simulée (application servie par l'API, et démo autonome si DEMO_URL est donné) ;
//   A12 coupure réseau pendant une réponse : message, réessai, une seule réponse enregistrée.
// Usage : BASE_URL=http://localhost:8061/ ADMIN_TOKEN=... [DEMO_URL=http://localhost:8052/spinsacademy.html] node tools/web/e2e_beta.cjs
const { chromium } = require('playwright');
const skipOnboarding = async (pg) => {          // étape 4 : un nouveau joueur voit d'abord le premier lancement
  try { await pg.waitForSelector('#screen-onboard:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
    if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); } } catch (e) { /* page sans accueil */ }
};
const BASE = process.env.BASE_URL || 'http://localhost:8061/', TOKEN = process.env.ADMIN_TOKEN;
const FOUR_G = { offline: false, latency: 70, downloadThroughput: 4e6 / 8, uploadThroughput: 3e6 / 8 };   // « 4G » : 4 Mbit/s, 70 ms

async function mobile(browser) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const errors = [];
  p.on('pageerror', (e) => errors.push(String(e)));
  return { ctx, p, errors };
}

async function firstQuestion(p, url) {
  await p.goto(url); await skipOnboarding(p); await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
}

(async () => {
  const browser = await chromium.launch(); const out = {};
  // ---- A10 : signalement
  {
    const { ctx, p, errors } = await mobile(browser);
    await firstQuestion(p, BASE);
    await p.locator('#actions button').first().click(); await p.waitForSelector('#screen-answer:not([hidden])');
    await p.click('#report summary'); await p.check('input[value="wrong_answer"]'); await p.fill('#report-comment', 'contrôle bêta A10');
    await p.click('#report-form button[type=submit]'); await p.waitForSelector('#report-done:not([hidden])');
    const headers = { 'X-Admin-Token': TOKEN };
    const list = await (await p.request.get(BASE + 'admin/reports', { headers })).json();
    const rows = Array.isArray(list) ? list : [];
    const mine = rows.find((r) => (r.comment || '').includes('contrôle bêta A10'));
    let resolved = false;
    if (mine) {
      const r = await p.request.post(BASE + `admin/reports/${mine.id}/resolve`, { headers, data: { status: 'rejected', resolution: 'contrôle bêta A10 (test)' } });
      resolved = r.ok();
    }
    const left = await (await p.request.get(BASE + 'admin/reports', { headers })).json();
    out.A10 = { sent: true, seen_by_admin: !!mine, reason: mine && mine.reason_fr, comment: mine && mine.comment, has_correction: !!(mine && mine.correction),
                resolved, still_open: Array.isArray(left) && left.some((r) => mine && r.id === mine.id), errors };
    await ctx.close();
  }
  // ---- A11 : chargement en 4G simulée
  out.A11 = {};
  for (const [name, url] of [['application', BASE], ['demo', process.env.DEMO_URL]]) {
    if (!url) continue;
    const { ctx, p } = await mobile(browser);
    const cdp = await ctx.newCDPSession(p); await cdp.send('Network.enable'); await cdp.send('Network.emulateNetworkConditions', FOUR_G);
    let bytes = 0; p.on('response', async (r) => { try { bytes += (await r.body()).length; } catch (e) { /* redirection */ } });
    const t0 = Date.now();
    await p.goto(url); await skipOnboarding(p); const tPage = Date.now() - t0;
    await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 120000 });
    out.A11[name] = { page_s: +(tPage / 1000).toFixed(1), first_question_s: +((Date.now() - t0) / 1000).toFixed(1), kio: Math.round(bytes / 1024) };
    await ctx.close();
  }
  // ---- A12 : coupure réseau pendant une réponse
  {
    const { ctx, p, errors } = await mobile(browser);
    await firstQuestion(p, BASE);
    await ctx.setOffline(true);
    await p.locator('#actions button').first().click();
    await p.waitForSelector('#notice:not([hidden])');
    const msg = await p.textContent('#notice');
    const retry = p.locator('#notice-retry');
    await ctx.setOffline(false);
    await retry.click(); await p.waitForSelector('#screen-answer:not([hidden])');
    const sid = await p.evaluate(() => localStorage.getItem('sid'));
    const summary = await (await p.request.get(BASE + `sessions/${sid}/summary`)).json();
    await p.click('#next-btn'); await p.waitForSelector('#screen-question:not([hidden])');
    out.A12 = { message: (msg || '').trim().slice(0, 90), recovered: true, answers_saved: summary.questions, errors };
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(out, null, 1));
})();

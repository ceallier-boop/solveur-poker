// Démo autonome : séries gardées par une version précédente (numéros de questions d'une autre construction, sans description).
// La progression doit s'ouvrir, compter leurs réponses dans le score, et ne pas proposer de reprendre une série devenue invalide.
// Usage : DEMO_URL=http://localhost:8072/spinsacademy.html node tools/web/e2e_demo_storage.cjs
const { chromium } = require('playwright');
(async () => {
  const URL = process.env.DEMO_URL || 'http://localhost:8072/spinsacademy.html'; const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const logs = []; p.on('pageerror', (e) => logs.push('pageerror ' + e.message));
  const ans = (v) => ({ action_id: 'F', at: '2026-10-20T10:00:00+00:00', verdict: v, points: v === 'correct' ? 1 : v === 'erreur' ? 0 : 0.5, regret_mbb: 80, chosen_label: 'Fold', best_label: 'Tapis (8 BB)' });
  const old = { sessions: {
    a: { id: 'a', created_at: '2026-10-20T10:00:00+00:00', mode: 'gto', items: [999990, 999991, 3, 4, 5], answers: { 0: ans('erreur'), 1: ans('correct'), 2: ans('correct'), 3: ans('imprécision'), 4: ans('correct') }, purposes: {} },
    b: { id: 'b', created_at: '2026-10-21T10:00:00+00:00', mode: 'exploit', items: [999992, 7, 8, 9, 10], answers: { 0: ans('correct') }, purposes: {} } } };
  await p.goto(URL);
  await p.evaluate((o) => { localStorage.setItem('spinsacademy_demo_v1', JSON.stringify(o)); localStorage.setItem('sid', 'b'); }, old);
  await p.goto(URL); await p.waitForTimeout(800);
  logs.push('reprise visible : ' + await p.isVisible('#resume'));
  await p.click('#stats-btn'); await p.waitForTimeout(1200);
  logs.push('notice : ' + JSON.stringify(await p.textContent('#notice-text')) + ' | progression : ' + await p.isVisible('#screen-stats') + ' | ' + (await p.textContent('#st-score')).trim());
  // nouvelle série après les anciennes, puis progression par thème
  await p.goto(URL); await p.click('#quick-start');
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.locator('#actions button').first().click(); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.click('#stats-btn'); await p.waitForTimeout(1000);
  logs.push('après série : ' + (await p.textContent('#st-score')).trim() + ' | thèmes : ' + (await p.locator('#st-themes .trow').count()));
  const meta = await p.evaluate(() => { const d = JSON.parse(localStorage.getItem('spinsacademy_demo_v1')); const s = Object.values(d.sessions).find((x) => x.build); return !!(s && s.answers[0].meta); });
  logs.push('meta enregistrée : ' + meta);
  console.log(logs.join('\n')); await b.close();
})();

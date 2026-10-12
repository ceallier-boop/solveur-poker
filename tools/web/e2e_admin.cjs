// Page d'administration sur mobile (390 x 844) : connexion, acceptation d'un signalement avec retrait du spot,
// remise en service, journal. Il faut au moins un signalement ouvert (voir e2e_mobile.cjs).
// Usage : BASE_URL=http://localhost:8000/ ADMIN_TOKEN=... node tools/web/e2e_admin.cjs <dossier_captures>
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async () => {
  const out = process.argv[2]; const errors = []; const base = process.env.BASE_URL || 'http://localhost:8000/';
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(String(e))); p.on('console', m => { if (m.type() === 'error' && !m.text().includes('403')) errors.push(m.text()); });
  await p.goto(base + 'admin');
  await p.fill('#token', 'mauvais'); await p.fill('#actor', 'Expert test'); await p.click('#login-form button');
  await p.waitForSelector('#login-error:not([hidden])');
  await p.fill('#token', process.env.ADMIN_TOKEN); await p.click('#login-form button');
  await p.waitForSelector('.item form.resolve'); await p.screenshot({ path: out + '/a1_a_traiter.png', fullPage: true });
  const f = p.locator('form.resolve').first();
  await f.locator('details, summary').count();
  await f.locator('textarea').fill('Énoncé ambigu : spot retiré en attendant la prochaine version');
  await f.locator('[name=disable]').check(); await f.locator('button[value=accepted]').click();
  await p.waitForFunction(() => !document.querySelector('#list').textContent.includes('Chargement'));
  await p.click('[data-tab=disabled]'); await p.waitForSelector('form.enable'); await p.screenshot({ path: out + '/a2_retires.png', fullPage: true });
  await p.locator('form.enable textarea').first().fill('Vérifié avec HRC'); await p.locator('form.enable button').first().click();
  await p.waitForFunction(() => document.querySelector('#list').textContent.includes('Rien ici'));
  await p.click('[data-tab=log]'); await p.waitForSelector('.item'); await p.screenshot({ path: out + '/a3_journal.png', fullPage: true });
  const log = await p.locator('.item').count();
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  console.log(JSON.stringify({ errors, log, horizontalOverflow: overflow }));
  await b.close();
})();

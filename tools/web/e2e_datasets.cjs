// Publication des datasets depuis la page d'administration (390 x 844) : contrôle, rapport, publication du GTO puis
// de l'exploitant. À lancer sur une base neuve, sans SPINSACADEMY_ALLOW_STAGING (rien n'est servi avant publication).
// Usage : BASE_URL=http://localhost:8000/ ADMIN_TOKEN=... node tools/web/e2e_datasets.cjs <dossier_captures>
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs'), path = require('path');
// versions à publier : la dernière ligne de docs/dataset/PUBLICATIONS.md pour chaque dataset (jamais codées en dur)
const pubs = {};
for (const m of fs.readFileSync(path.join(__dirname, '../../docs/dataset/PUBLICATIONS.md'), 'utf8').matchAll(/\| `(gto_preflop|exploit_calls)` \| `([\d.-]+)` \|/g)) pubs[m[1]] = `${m[1]}/${m[2]}`;
const GTO = process.env.GTO_REF || pubs.gto_preflop, EXP = process.env.EXP_REF || pubs.exploit_calls;
const OLD = 'gto_preflop/2026.10.12-1';            // version historique refusée au contrôle : vérifie l'affichage d'un rapport en échec
(async () => {
  const out = process.argv[2]; const errors = []; const base = process.env.BASE_URL || 'http://localhost:8000/';
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const p = await ctx.newPage();
  p.on('pageerror', e => errors.push(String(e))); p.on('console', m => { if (m.type() === 'error' && !/40[39]|503/.test(m.text())) errors.push(m.text()); });
  p.on('dialog', d => d.accept());
  const before = await (await ctx.request.post(base + 'sessions', { data: {} })).status();
  await p.goto(base + 'admin');
  await p.fill('#token', process.env.ADMIN_TOKEN); await p.fill('#actor', 'Expert test'); await p.click('#login-form button');
  await p.waitForSelector('[data-ref]'); await p.screenshot({ path: out + '/d1_datasets.png', fullPage: true });
  const card = (ref) => p.locator(`[data-ref="${ref}"]`);
  async function act(ref, what, reason) {
    if (reason) await card(ref).locator('textarea').fill(reason);
    const reload = p.waitForResponse(r => r.url().endsWith('/admin/datasets') && r.request().method() === 'GET');
    await card(ref).locator(`button[value=${what}]`).click(); await reload; await p.waitForTimeout(200);
  }
  await act(OLD, 'validate');
  await act(GTO, 'validate');
  await act(EXP, 'validate');
  await card(OLD).locator('summary').click(); await p.waitForSelector(`[data-ref="${OLD}"] .checks`);
  await p.screenshot({ path: out + '/d2_rapport_refuse.png', fullPage: true });
  await act(GTO, 'publish', 'Contrôles réussis, validé pour la recette');
  await act(EXP, 'publish', 'Contrôles réussis, source GTO publiée');
  await p.screenshot({ path: out + '/d3_publies.png', fullPage: true });
  const status = await p.evaluate(() => Object.fromEntries([...document.querySelectorAll('[data-ref]')].map(e => [e.dataset.ref, e.querySelector('.tag').textContent])));
  const after = await (await ctx.request.post(base + 'sessions', { data: {} })).status();
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  console.log(JSON.stringify({ published: [GTO, EXP], errors, before, after, status, horizontalOverflow: overflow }));
  await b.close();
})();

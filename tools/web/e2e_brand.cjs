// Nom de l'application (23/11 : SpinXpresso, « Poker Trainer »), avec assertions : une seule source (<meta name="application-name">
// d'index.html) ; en-tête « Spin » + « Xpresso », titre de l'onglet, accueil du premier lancement, manifest servi (application) ;
// l'ancien nom nulle part à l'écran ; l'export de « Mes données » au nouveau nom ; la progression gardée (clé player_id inchangée).
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_brand.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, acceptDownloads: true });
  const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  const first = await p.evaluate(() => ({ brand: document.getElementById('home-btn').textContent, part: (document.querySelector('#home-btn span') || {}).textContent,
    title: document.title, ob: document.getElementById('ob-title').textContent, body: document.body.innerText, wide: document.documentElement.scrollWidth }));
  ok('en-tête : « SpinXpresso », la deuxième partie en couleur', first.brand === 'SpinXpresso' && first.part === 'Xpresso', first.brand);
  ok('titre de l\'onglet : « SpinXpresso · Poker Trainer »', /^SpinXpresso( · Poker Trainer)?$/.test(first.title) && (BASE.startsWith('file:') || first.title === 'SpinXpresso · Poker Trainer'), first.title);
  ok('premier lancement : « Bienvenue sur SpinXpresso »', first.ob === 'Bienvenue sur SpinXpresso', first.ob);
  ok('l\'ancien nom n\'apparaît pas à l\'écran ; la barre tient dans l\'écran', !/Spins ?Academy/i.test(first.body + first.title) && (BASE.startsWith('file:') || first.wide <= 390), first.wide);   // la démo n'a pas de viewport avant publication
  await p.screenshot({ path: `${OUT}/brand_onboard.png` });
  if (!BASE.startsWith('file:')) {
    const m = await p.evaluate(async () => { const r = await fetch(document.querySelector('link[rel="manifest"]').getAttribute('href')); return { status: r.status, j: await r.json() }; });
    ok('manifest servi avec le nom d\'index.html', m.status === 200 && m.j.short_name === 'SpinXpresso' && m.j.name === 'SpinXpresso · Poker Trainer', m);
  }
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  const pid = await p.evaluate(() => localStorage.getItem('player_id'));
  ok('progression : identifiant du joueur sous la clé player_id (inchangée)', BASE.startsWith('file:') || /^[A-Za-z0-9-]{8,}$/.test(pid || ''), pid);
  ok('lexique : sans l\'ancien nom', !/Spins ?Academy/i.test(await p.evaluate(async () => { try { return JSON.stringify(await (await fetch('/static/lexique.json')).json()); } catch (e) { return ''; } })));
  if (!BASE.startsWith('file:')) {                                   // la démo n'a pas l'export (route absente)
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 15000 }).catch(() => null), p.click('#st-export')]);
    ok('export de « Mes données » : spinxpresso-mes-donnees.json', dl && dl.suggestedFilename() === 'spinxpresso-mes-donnees.json', dl && dl.suggestedFilename());
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

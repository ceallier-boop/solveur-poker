// « Importer mes mains » (onglet Outils), avec assertions : fichier d'exemple sans pseudo (tools/web/fixtures/winamax_exemple.txt :
// 5 mains Expresso, 2 heads-up et 3 à 3 joueurs, plus 1 Sit&Go ignorée), progression, résultat en nombres seuls, aucun pseudo
// affiché ni enregistré, aucune requête réseau pendant la lecture, deux fichiers enregistrés, case d'offre désactivée et décochée,
// « Effacer », rien dans localStorage, pas de débordement à 390 px ; dans la démo, message à la place du bouton.
// Tant que spinsacademy/web/winamax.js (Moteur exploitant) n'est pas livré, un lecteur provisoire au format annoncé le remplace.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_import.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const FIXTURE = path.join(__dirname, 'fixtures', 'winamax_exemple.txt');
const PSEUDOS = ['JoueurA', 'JoueurB', 'JoueurC'];
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
// lecteur provisoire : même interface que winamax.js (analyze(files, onProgress) → Promise, toCsv(result) → { nom: texte })
const STAND_IN = `window.Winamax = { provisional: true,
  async analyze(files, onProgress) { const r = { files: files.length, hands: 0, skipped: 0, kinds: { hu: 0, '3w': 0 } };
    let i = 0; for (const f of files) { const t = await f.text();
      for (const h of t.split(/\\n(?=Winamax Poker - )/)) { if (!/^Winamax Poker - /.test(h.trim())) continue;
        if (!/Tournament "Expresso/.test(h) || !/\\(real money\\)/.test(h)) { r.skipped++; continue; }
        r.hands++; r.kinds[(h.match(/^Seat \\d+: /gm) || []).length === 2 ? 'hu' : '3w']++; }
      onProgress && onProgress(++i, files.length); await new Promise((s) => setTimeout(s)); }
    return r; },
  toCsv(r) { return { 'comptages.csv': 'groupe,kind,decision,action,stack,n,k\\n', 'volume.csv': 'parametre,stack,n,statut\\nmains,,' + r.hands + ',insuffisant\\n' }; } };`;
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, acceptDownloads: true });
  const demo = BASE.startsWith('file:');
  let provisional = false;
  if (demo) await ctx.addInitScript(STAND_IN);                       // la démo n'embarque pas encore le lecteur
  else await ctx.route('**/static/winamax.js', async (r) => {
    const real = await r.fetch().catch(() => null);
    if (real && real.ok()) return r.fulfill({ response: real });
    provisional = true; return r.fulfill({ status: 200, contentType: 'application/javascript', body: STAND_IN });
  });
  const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  await p.openTab('outils');
  ok('bouton dans l\'onglet Outils', await p.isVisible('#import-btn') && /Importer mes mains/.test(await p.textContent('#import-btn')));
  await p.click('#import-btn'); await p.waitForSelector('#screen-import:not([hidden])');
  ok('explication : rien n\'est envoyé, pas de pseudo', /restent sur cet appareil\. Rien n'est envoyé\. Les pseudos ne sont jamais conservés\./.test(await p.textContent('#im-private')));
  ok('aide repliée, puis dépliable', (await p.getAttribute('#im-help', 'open')) === null && !(await p.isVisible('#im-help li')));
  await p.click('#im-help summary'); ok('aide : où trouver les historiques', await p.isVisible('#im-help li') && /winamax/i.test(await p.innerText('#im-help')));
  ok('barre d\'onglets masquée sur l\'écran d\'import', await p.isHidden('#tabs'));
  ok('choix multiple de fichiers .txt', await p.$eval('#im-files', (x) => x.multiple && /\.txt/.test(x.accept)));
  ok('case d\'offre visible, désactivée, décochée, « bientôt »', await p.$eval('#im-offer', (x) => x.disabled && !x.checked) && /bientôt/.test(await p.innerText('.im-offer')));
  // lecture : aucune requête réseau autre que le lecteur lui-même
  const reqs = []; p.on('request', (r) => { if (!/winamax\.js/.test(r.url()) && !r.url().startsWith('data:') && !r.url().startsWith('blob:')) reqs.push(r.method() + ' ' + r.url()); });
  await p.setInputFiles('#im-files', FIXTURE);
  await p.waitForSelector('#im-result:not([hidden])', { timeout: 20000 });
  const nums = await p.$$eval('#im-result dd', (xs) => xs.map((x) => x.textContent));
  ok('résultat : 5 lues, 1 ignorée, 2 heads-up, 3 à 3 joueurs', JSON.stringify(nums) === JSON.stringify(['5', '1', '2', '3']), nums);
  ok('mains ignorées expliquées', await p.isVisible('#im-skip-note'));
  ok('ligne de volume', /^5 mains : .*premier aperçu/.test(await p.textContent('#im-volume')), await p.textContent('#im-volume'));
  const shown = await p.innerText('#screen-import');
  ok('aucun pseudo affiché', PSEUDOS.every((x) => !shown.includes(x)));
  ok('aucune requête réseau pendant la lecture', !reqs.length, reqs);
  ok('pas de débordement horizontal', await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  await p.screenshot({ path: `${OUT}/import_result.png`, fullPage: true });
  if (demo) {
    ok('démo : message à la place du bouton', !(await p.isVisible('#im-save')) && /disponible dans l'application/.test(await p.textContent('#im-demo')));
  } else {
    const files = [];
    p.on('download', (d) => files.push(d));
    await p.click('#im-save');
    await p.waitForFunction(() => true); for (let i = 0; i < 20 && files.length < 2; i++) await p.waitForTimeout(150);
    const names = files.map((d) => d.suggestedFilename()).sort();
    const bodies = await Promise.all(files.map(async (d) => fs.readFileSync(await d.path(), 'utf8')));
    ok('enregistrement : comptages.csv et volume.csv', JSON.stringify(names) === '["comptages.csv","volume.csv"]', names);
    ok('fichiers enregistrés sans pseudo', bodies.length === 2 && bodies.every((t) => PSEUDOS.every((x) => !t.includes(x))));
  }
  ok('rien gardé dans localStorage', await p.evaluate((ps) => { const all = JSON.stringify(Object.assign({}, localStorage)); return ps.every((x) => !all.includes(x)) && !/winamax|hand/i.test(Object.keys(localStorage).join(' ')); }, PSEUDOS));
  await p.click('#im-clear');
  ok('« Effacer » vide l\'écran', await p.isHidden('#im-result') && await p.evaluate(() => document.getElementById('im-files').value === ''));
  await p.setInputFiles('#im-files', { name: 'image.png', mimeType: 'image/png', buffer: Buffer.from('x') });
  ok('fichier qui n\'est pas un .txt : message clair', await p.isVisible('#im-error') && /\.txt/.test(await p.textContent('#im-error')));
  await p.click('#im-back'); await p.waitForSelector('#screen-outils:not([hidden])');
  ok('retour aux outils', await p.isVisible('#tabs'));
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, lecteur: provisional || demo ? 'provisoire (winamax.js pas encore livré)' : 'winamax.js', passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

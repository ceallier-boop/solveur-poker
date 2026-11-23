// Import de mains dans la page de test ouverte à part (fichier SpinsAcademy_test.html, hors visualiseur de claude.ai) :
// le bouton « Enregistrer mes comptages » télécharge comptages.csv et volume.csv ; ils ne contiennent aucun pseudo.
// Usage : BASE_URL=file:///…/demo.html node tools/web/e2e_import_fichier.cjs [dossier]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE_URL; const FIXTURE = path.join(__dirname, 'fixtures', 'winamax_exemple.txt');
const PSEUDOS = ['JoueurA', 'JoueurB', 'JoueurC'];
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, acceptDownloads: true });
  const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  ok('page ouverte à part : pas de visualiseur claude.ai', await p.evaluate(() => !(window.claude && window.claude.use)));
  await p.openTab('outils'); await p.click('#import-btn'); await p.waitForSelector('#screen-import:not([hidden])');
  await p.setInputFiles('#im-files', FIXTURE); await p.waitForSelector('#im-result:not([hidden])', { timeout: 20000 });
  ok('bouton d\'enregistrement visible, message de démo caché', await p.isVisible('#im-save') && !(await p.isVisible('#im-demo')));
  const got = []; p.on('download', (d) => got.push(d));
  await p.click('#im-save'); await p.waitForTimeout(1500);
  const names = got.map((d) => d.suggestedFilename()).sort();
  ok('deux fichiers téléchargés : comptages.csv et volume.csv', JSON.stringify(names) === JSON.stringify(['comptages.csv', 'volume.csv']), names);
  let text = ''; for (const d of got) text += fs.readFileSync(await d.path(), 'utf-8');
  ok('aucun pseudo dans les CSV', text.length > 0 && PSEUDOS.every((x) => !text.includes(x)));
  ok('aucune erreur de page', !errs.length, errs);
  const failed = checks.filter((c) => !c.ok);
  console.log(JSON.stringify({ base: BASE, passed: checks.length - failed.length, failed }, null, 1));
  await b.close(); process.exit(failed.length ? 1 : 0);
})();

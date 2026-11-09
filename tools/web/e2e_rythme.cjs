// Chantiers de rythme (N1, puis N2 et N3) côté interface, avec assertions.
// N1 : séance de 15 ou 10 minutes, choix discret gardé sur l'appareil, libellés et étapes qui suivent la réponse du serveur.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_rythme.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const home = (p) => p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await home(p); await p.waitForTimeout(800);
  const steps = () => p.$$eval('#today-steps li', (xs) => xs.length);
  ok('N1 : 15 minutes par défaut, trois étapes', /15 min/.test(await p.textContent('#today-len')) && await steps() === 3 && /séance de 15 minutes/.test(await p.textContent('#today-go')));
  await p.click('#len-switch [data-min="10"]'); await p.waitForFunction(() => /10 min/.test(document.getElementById('today-len').textContent), null, { timeout: 10000 });
  ok('N1 : 10 minutes, deux étapes, libellés qui suivent', await steps() === 2 && /séance de 10 minutes/.test(await p.textContent('#today-go'))
    && /une série sur ton thème/.test(await p.textContent('#today-explain')), [await steps(), await p.textContent('#today-go')]);
  await p.screenshot({ path: `${OUT}/rythme_10min.png` });
  await p.reload(); await home(p); await p.waitForTimeout(800);
  ok('N1 : choix gardé sur l\'appareil', /10 min/.test(await p.textContent('#today-len')) && await p.getAttribute('#len-switch [data-min="10"]', 'aria-pressed') === 'true');
  // la séance de 10 minutes jusqu'au bout : révision (rien à revoir pour un nouveau joueur), une série du thème
  await p.click('#today-go');
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#again-btn');
  await p.waitForSelector('#screen-today:not([hidden])', { timeout: 15000 });
  ok('N1 : séance faite après une seule série', /10 minutes de travail/.test(await p.innerText('#td-score')), await p.innerText('#td-score'));
  await p.click('#td-home'); await home(p); await p.waitForTimeout(1000);
  ok('N1 : accueil « séance de 10 minutes faite »', /Séance de 10 minutes faite/.test(await p.textContent('#today-note')), await p.textContent('#today-note'));
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

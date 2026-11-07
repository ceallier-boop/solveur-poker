// Audit AU7 : test de placement de 10 mains, côté interface, avec assertions. Proposé seulement aux joueurs confirmés à la fin du
// premier lancement, et depuis « Ma progression » ; résultat par tranche, « Prendre ce niveau » / « Garder le niveau N » ; une
// reprise après abandon mène aussi au résultat ; les 10 réponses ne comptent pas dans la progression.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_placement.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const ready = (p) => p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
async function toStep3(p, exp) {
  await p.goto(BASE); await ready(p);
  await p.click(`#ob-exp button[data-v="${exp}"]`); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); await p.click('#ob-next');
}
const answer = async (p, k) => { await p.waitForSelector('#screen-question:not([hidden])'); await p.click(`#actions button >> nth=${k}`); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); };
(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => { const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage(); p.on('pageerror', (e) => errs.push(String(e))); return p; };

  // débutant : pas de test proposé
  let p = await page(); await toStep3(p, 'debut');
  ok('débutant : pas de test proposé', !(await p.isVisible('#ob-placement')));
  await p.context().close();

  // confirmé : test depuis le premier lancement, 10 mains, résultat
  p = await page(); await toStep3(p, 'confirme');
  ok('confirmé : test proposé (facultatif)', await p.isVisible('#ob-placement') && /facultatif/.test(await p.textContent('#ob-placement')));
  await p.click('#ob-placement'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 });
  ok('10 mains', /1 \/ 10/.test(await p.textContent('#progress')), await p.textContent('#progress'));
  for (let i = 0; i < 10; i++) await answer(p, i % 2);
  await p.waitForSelector('#screen-placement:not([hidden])', { timeout: 15000 });
  const bands = await p.$$eval('#pl-bands tr', (xs) => xs.map((x) => x.innerText.replace(/\s+/g, ' ').trim()));
  ok('résultat : niveau proposé et trois tranches', /Niveau [123]/.test(await p.textContent('#pl-level')) && bands.length === 3 && /sur 4$/.test(bands[0]) && /sur 3$/.test(bands[2]), bands);
  ok('résultat : sans reproche', !/erreur|raté|mauvais/i.test(await p.innerText('#screen-placement')));
  await p.screenshot({ path: `${OUT}/placement_result.png`, fullPage: true });
  const proposed = Number((await p.textContent('#pl-level')).match(/Niveau (\d)/)[1]);
  const take = await p.isVisible('#pl-take');
  ok('boutons : prendre / garder', take ? /Garder le niveau 2/.test(await p.textContent('#pl-keep')) : /Continuer au niveau/.test(await p.textContent('#pl-keep')));
  await p.click(take ? '#pl-take' : '#pl-keep'); await p.waitForSelector('#screen-home:not([hidden])', { timeout: 15000 }); await p.waitForTimeout(1200);
  ok('niveau appliqué', (await p.innerText('#today-level')).includes(`Niveau ${proposed}`), await p.innerText('#today-level'));
  await p.click('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.waitForTimeout(1200);
  ok('hors progression', /Joue une première série/.test(await p.innerText('#st-score')), await p.innerText('#st-score'));

  // depuis « Ma progression », abandon après 3 mains, reprise : le résultat s'affiche quand même
  ok('test proposé dans « Ma progression »', await p.isVisible('#st-placement'));
  await p.click('#st-placement'); for (let i = 0; i < 3; i++) await answer(p, 0);
  await p.click('#home-btn'); await p.waitForSelector('#resume:not([hidden])', { timeout: 15000 }); await p.click('#resume');
  ok('reprise à la 4e main', await p.waitForSelector('#screen-question:not([hidden])').then(async () => /4 \/ 10/.test(await p.textContent('#progress'))), await p.textContent('#progress'));
  for (let i = 3; i < 10; i++) await answer(p, 0);
  await p.waitForSelector('#screen-placement:not([hidden])', { timeout: 15000 });
  ok('reprise : écran du résultat', true);
  await p.click('#pl-keep'); await p.waitForSelector('#screen-home:not([hidden])');
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Chantiers de rythme (N1, N2, puis N3) côté interface, avec assertions.
// N2 : les 3 erreurs les plus coûteuses du jour sur l'accueil, état « rattrapée », bouton « Les rejouer ».
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
  // N2 : les 3 erreurs les plus coûteuses du jour, après la série jouée (premier coup à chaque main)
  const demoNoRoute = BASE.startsWith('file:') && !(await p.evaluate(() => fetch('/users/me/worst-today?mode=gto&tz=0').then((r) => r.ok)));
  if (demoNoRoute) ok('N2 démo sans la route : bloc caché, pas d\'erreur', !(await p.isVisible('#worst')));
  else {
  await p.waitForSelector('#worst:not([hidden])', { timeout: 10000 });
  const wl = await p.$$eval('#worst-list li', (xs) => xs.map((x) => x.innerText.replace(/\n+/g, ' | ')));
  ok('N2 : bloc du jour, jamais vide', wl.length >= 1 && wl.length <= 3 && wl.every((t) => /Ton choix : .* · le bon coup : .* · .*BB|Aucune erreur coûteuse aujourd'hui/.test(t)), wl);
  ok('N2 : bouton « Les rejouer » seulement s\'il y a des erreurs', (await p.isVisible('#worst-replay')) === !/Aucune erreur/.test(wl[0]));
  await p.screenshot({ path: `${OUT}/rythme_worst.png` });
  if (!BASE.startsWith('file:')) {                                   // état « rattrapée » : réponse injectée au format annoncé
    await p.route('**/users/me/worst-today*', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ mode: 'gto', date: '2026-11-09', errors: [
      { session_id: 's', question_index: 0, spot_id: 'x', hand: 'K9o', prompt_fr: 'SB · 3 joueurs · 8 BB. Que fais-tu ?', chosen_fr: 'FOLD', best_fr: 'ALL-IN 8 BB', verdict: 'erreur', regret_mbb: 1300, cost_bb: 1.3, cost_fr: '1,3 BB', answered_at: '2026-11-09T10:00:00+00:00', replayed_ok: true },
      { session_id: 's', question_index: 1, spot_id: 'y', hand: 'Q4o', prompt_fr: 'BB · heads-up · 6 BB. Que fais-tu ?', chosen_fr: 'CALL 5 BB', best_fr: 'FOLD', verdict: 'erreur', regret_mbb: 400, cost_bb: 0.4, cost_fr: '0,4 BB', answered_at: '2026-11-09T10:01:00+00:00' }] }) }));
    await p.click('#home-btn'); await home(p); await p.waitForTimeout(1200);
    const caught = await p.innerText('#worst-list li.caught').catch(() => '');
    ok('N2 : erreur rejouée juste « rattrapée », sans reproche', /Rattrapée/.test(caught) && /Tapis 8 BB \(ALL-IN\)/.test(caught), caught);
    ok('N2 : le rejeu reste proposé pour les autres', await p.isVisible('#worst-replay'));
    await p.unroute('**/users/me/worst-today*');
  }
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

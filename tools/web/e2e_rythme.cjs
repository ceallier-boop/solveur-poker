// Chantiers de rythme (N1, N2, puis N3) côté interface, avec assertions.
// N2 : les 3 erreurs les plus coûteuses du jour sur l'accueil, état « rattrapée », bouton « Les rejouer ».
// N3 : fiches à emporter (réglages, liste groupée, grille, fiabilité, impression d'une page A4).
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
  if (await p.isVisible('#worst-replay')) {                          // « Les rejouer », de bout en bout : les mêmes situations, puis retour au bloc
    const n = wl.length; await p.click('#worst-replay'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
    ok('N2 : le rejeu sert les erreurs du jour', /Rejeu de ton erreur du jour/.test(await p.textContent('#purpose')) && new RegExp(`1 / ${n}$`).test((await p.textContent('#progress')).trim()), [await p.textContent('#purpose'), await p.textContent('#progress')]);
    for (let i = 0; i < n; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=-1'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
    await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await home(p); await p.waitForSelector('#worst:not([hidden])');
    const after = await p.$$eval('#worst-list li', (xs) => xs.map((x) => x.className));
    ok('N2 : après le rejeu, la même liste (rattrapées marquées)', after.length === n, after);
  }
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
  // N3 : fiches à emporter : trois réglages, liste groupée, fiche, impression d'une page A4
  await p.click('#home-btn'); await home(p); await p.click('#fiches-btn'); await p.waitForSelector('#screen-fiches:not([hidden]) #fi-table button');
  await p.click('#fi-table [data-v="3-handed"]'); await p.click('#fi-stack [data-v="10"]'); await p.click('#fi-hero [data-v="BB"]');
  const groups = await p.$$eval('#fi-list .fi-group h3', (xs) => xs.map((x) => x.textContent));
  const items = await p.$$eval('#fi-list .fi-item', (xs) => xs.length);
  ok('N3 : trois réglages puis fiches groupées par situation', groups.length >= 2 && groups.some((g) => /Face à un tapis/.test(g)) && items > 0 && items < 40, [groups, items]);
  await p.click('#fi-list .fi-item >> nth=0'); await p.waitForSelector('#fi-sheet:not([hidden]) svg.fi-grid');
  const texts = await p.$$eval('#fi-sheet svg.fi-grid text', (xs) => xs.length);
  ok('N3 : fiche 13 × 13, légende, fiabilité', texts === 169 && (await p.$$('#fi-sheet .fi-legend span')).length >= 2 && /Fiable|Approximation/.test(await p.textContent('#fi-sheet .fi-head .fi-rel')), texts);
  await p.screenshot({ path: `${OUT}/rythme_fiche.png`, fullPage: true });
  // une fiche « Approximation » (mène au flop) : la note d'écart, discrète
  await p.click('#fi-back'); await p.click('#fi-table [data-v="heads-up"]'); await p.click('#fi-stack [data-v="10"]');
  const approx = await p.$$eval('#fi-list .fi-item', (xs) => xs.findIndex((x) => /Approximation/.test(x.textContent)));
  if (approx >= 0) { await p.click(`#fi-list .fi-item >> nth=${approx}`); await p.waitForSelector('#fi-sheet:not([hidden])');
    ok('N3 : « Approximation » avec la note d\'écart mesuré', /Approximation : à 10 BB/.test(await p.textContent('#fi-sheet .fi-note')), await p.textContent('#fi-sheet .fi-note')); }
  else ok('N3 : une fiche « Approximation » à 10 BB en heads-up', false);
  const pages = ((await p.pdf({ format: 'A4', printBackground: true })).toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  ok('N3 : impression sur une seule page A4', pages === 1, pages);
  await p.emulateMedia({ media: 'print' }); await p.screenshot({ path: `${OUT}/rythme_fiche_print.png`, fullPage: true }); await p.emulateMedia({ media: 'screen' });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Corrections du neuvième test joueurs (docs/produit/RETEST9_JOUEURS_2026-10-29.md) : vérifications avec assertions.
// Accueil (ordre, défis repliés, un seul chiffre BB), thème du jour figé, défi du jour repris et non recommencé, niveau qui suit
// le mode, range « corrigée sur la théorie », objectifs plafonnés, blocs en erreur, chrono en pause pendant une erreur réseau.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_retest9.cjs [dossier]      (application)
//         BASE_URL=file:///chemin/demo.html node tools/web/e2e_retest9.cjs [dossier]    (démo autonome : sans les contrôles réseau)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const DEMO = BASE.startsWith('file:');
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const skipOnboarding = async (pg) => {
  await pg.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });   // l'accueil s'affiche avant la réponse du niveau
  if (await pg.isVisible('#screen-onboard')) { await pg.click('#ob-skip'); await pg.waitForSelector('#screen-home:not([hidden])'); }
};
const answer = async (p, k = 0) => { await p.waitForSelector('#screen-question:not([hidden])'); await p.click(`#actions button >> nth=${k}`); await p.waitForSelector('#screen-answer:not([hidden])'); };
const series = async (p) => { for (let i = 0; i < 5; i++) { await answer(p, 0); await p.click('#next-btn'); } await p.waitForSelector('#screen-summary:not([hidden])'); };
const home = async (p) => { await p.click('#home-btn'); await p.waitForSelector('#screen-home:not([hidden])'); await p.waitForTimeout(1200); };

(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE); await skipOnboarding(p); await p.waitForSelector('#today:not([hidden])', { timeout: 20000 }); await p.waitForSelector('#challenges:not([hidden])');

  // accueil : mode en haut, « Jouer librement » avant objectifs et défis, défis repliés, un seul chiffre BB
  const order = await p.$$eval('#screen-home .mode-switch, #today, #free-title, #goals, #challenges', (xs) => xs.map((x) => x.id || 'mode'));
  ok('ordre de l\'accueil', JSON.stringify(order) === JSON.stringify(['mode', 'today', 'free-title', 'goals', 'challenges']), order);
  ok('défi du jour seul visible, les autres repliés', (await p.$$('#ch-list li')).length === 1 && !(await p.isVisible('#ch-others')), await p.textContent('#ch-more-title'));
  ok('pas de BB sur la carte de la séance', !(await p.innerText('#today')).includes('BB perdus') && !(await p.innerText('#today')).includes('BB/100'), await p.innerText('#today'));
  await p.screenshot({ path: `${OUT}/r9_home.png`, fullPage: true });

  // thème du jour figé : le même après une série ratée
  const theme0 = await p.textContent('#today-steps li:nth-child(2)');
  await p.click('#today-go'); await series(p); await home(p);
  const theme1 = await p.textContent('#today-steps li:nth-child(2)');
  ok('thème du jour figé', theme0.replace(/\d\/2 séries/, '') === theme1.replace(/\d\/2 séries/, ''), [theme0, theme1]);

  // défi du jour : abandonné après 2 mains, il se reprend (même série), puis ne se relance plus
  await p.click('#ch-list li:first-child button'); await answer(p); await p.click('#next-btn'); await answer(p); await home(p);
  const daily = await p.innerText('#ch-list li:first-child');
  ok('défi entamé : « Reprendre »', /Reprendre/.test(daily) && /2\/5 mains jouées/.test(daily), daily);
  await p.click('#ch-list li:first-child button'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('reprise à la 3e main', (await p.textContent('#progress')).includes('3 / 5'), await p.textContent('#progress'));
  ok('chrono 15 s imposé à la reprise', await p.isVisible('#q-timer'));
  for (let i = 2; i < 5; i++) { await answer(p); await p.click('#next-btn'); }
  await p.waitForSelector('.ch-result', { timeout: 10000 }); const res = await p.textContent('.ch-result');
  ok('bilan du défi du jour', /Nouveau défi demain|réussi/.test(res) && !/pas encore réussi/.test(res), res);
  await home(p);
  ok('défi du jour : plus de bouton', !(await p.isVisible('#ch-list li:first-child button')), await p.innerText('#ch-list li:first-child'));

  // objectifs : « + » des séances bloqué au plafond
  await p.click('#goals-edit');
  const days = await p.$eval('#goals-list li:first-child', (li) => ({ t: li.querySelector('.goal-step b').textContent, plus: li.querySelector('[data-d="1"]').disabled }));
  ok('objectif de séances plafonné', days.plus === (Number(days.t) >= 7 - ((new Date().getDay() + 6) % 7)), days);
  await p.click('#goals-edit');
  ok('objectifs : mode et séances dits', /objectifs du mode GTO/.test(await p.textContent('#goals-note')), await p.textContent('#goals-note'));

  // le niveau suit le mode ; range « corrigée sur la théorie » en exploitant
  await p.click('.mode-switch [data-value="exploit"]'); await p.waitForTimeout(1500);
  ok('niveau 4 en exploitant (accueil)', (await p.innerText('#today-level')).includes('Niveau 4'), await p.innerText('#today-level'));
  await p.click('#stats-btn'); await p.waitForSelector('#st-level:not([hidden])', { timeout: 10000 });
  ok('niveau 4 en exploitant (progression)', (await p.innerText('#st-level-name')).includes('Niveau 4'), await p.innerText('#st-level-name'));
  ok('« Mes défis » montre les tentatives', (await p.innerText('#st-challenges')).includes('Défi du jour'), await p.innerText('#st-challenges'));
  await p.click('#st-back'); await p.waitForSelector('#screen-home:not([hidden])');
  await p.click('#range-btn'); await p.waitForSelector('#screen-range:not([hidden])');
  ok('range corrigée sur la théorie, dit en exploitant', await p.isVisible('#rg-theory'));
  await home(p); await p.click('.mode-switch [data-value="gto"]'); await p.waitForTimeout(1500);
  ok('niveau GTO revenu', !(await p.innerText('#today-level')).includes('Niveau 4'), await p.innerText('#today-level'));

  if (!DEMO) {
    // chrono en pause pendant une erreur réseau (429), puis reprise
    let fail = true;
    await p.route('**/attempts', (r) => (fail ? r.fulfill({ status: 429, contentType: 'application/json', body: JSON.stringify({ detail: 'Trop de requêtes en peu de temps : attends 5 s avant de réessayer.' }) }) : r.continue()));
    await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
    if (await p.isVisible('#q-timer')) {
      await p.click('#actions button >> nth=0'); await p.waitForSelector('#notice:not([hidden])');
      const t1 = await p.textContent('#q-timer span'); await p.waitForTimeout(2500); const t2 = await p.textContent('#q-timer span');
      ok('chrono en pause pendant le message', t1 === t2, [t1, t2]);
      fail = false; await p.click('#notice-retry'); await p.waitForSelector('#screen-answer:not([hidden])');
      ok('réponse enregistrée après « Réessayer », pas « Temps écoulé »', !(await p.innerText('#a-verdict')).includes('Temps écoulé'), await p.innerText('#a-verdict'));
    } else ok('chrono visible pour le test de pause', false);
    await p.unroute('**/attempts');
    // bloc d'objectifs en erreur : un message, pas un cadre vide
    const q = await ctx.newPage();
    await q.route('**/users/me/goals*', (r) => r.fulfill({ status: 429, contentType: 'application/json', body: JSON.stringify({ detail: 'Trop de requêtes en peu de temps : attends 5 s avant de réessayer.' }) }));
    await q.goto(BASE); await q.waitForSelector('#screen-home:not([hidden])'); await q.waitForSelector('#goals-error:not([hidden])', { timeout: 10000 });
    ok('objectifs indisponibles : message et « Réessayer »', /Trop de requêtes/.test(await q.textContent('#goals-error')) && await q.isVisible('#goals-error button'), await q.textContent('#goals-error'));
    await q.close();
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

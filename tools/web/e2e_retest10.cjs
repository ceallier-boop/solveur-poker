// Corrections du dixième test joueurs (navigation à cinq onglets, I9), avec assertions : refus 422 jamais silencieux (séance, placement),
// série abandonnée reprenable depuis Défis avec badge et retour vers l'onglet de départ, niveau de Progression indépendant de
// l'onglet ouvert, erreurs du jour sur Défis, titre « Défis », plus de « accueil » dans les liens, bilan en mots français au niveau 1,
// placement visible sans défiler et objectifs dépliés, profil (libellé, Échap, historique), lexique une seule fois par écran.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_retest10.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const home = (p) => p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
const tabOf = (p, sel) => p.evaluate((s) => { const el = document.querySelector(s); const pg = el && el.closest('.tab-page'); return pg ? pg.dataset.tab : null; }, sel);
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  const demo = BASE.startsWith('file:');
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await home(p); await p.waitForTimeout(800);

  // 7 : l'onglet central s'appelle « Défis », la séance du jour GTO en tête
  ok('7 : titre « Défis », séance GTO en tête', (await p.textContent('#home-title')).trim() === 'Défis' && /GTO/.test(await p.textContent('#today-len')) && await tabOf(p, '#today') === 'defis');
  // 14 : lexique une seule fois (Outils) sur les pages des onglets ; 13 : profil avec libellé, Échap, historique
  ok('14 : lexique dans Outils, pas en double dans l\'en-tête', !(await p.isVisible('#lex-btn')));
  ok('13 : libellé sous l\'icône du profil', await p.isVisible('#profile-btn .avatar-label') && /Profil/.test(await p.textContent('#profile-btn')));
  await p.click('#profile-btn'); await p.waitForSelector('#profile:not([hidden])');
  ok('13 : feuille du profil : historique, pastilles repliées', await p.isVisible('#pf-history') && (await p.getAttribute('#past-box', 'open')) === null);
  await p.keyboard.press('Escape'); await p.waitForTimeout(200);
  ok('13 : Échap ferme la feuille', await p.isHidden('#profile'));

  // 3 : un refus 422 au démarrage d'une séance ou d'un placement s'affiche, quel que soit l'onglet
  if (!demo) {
    await p.route('**/sessions', (r) => (r.request().method() === 'POST'
      ? r.fulfill({ status: 422, contentType: 'application/json', body: JSON.stringify({ detail: '3 spots disponibles pour ces filtres, 5 demandés.' }) }) : r.continue()));
    await p.click('#today-go'); await p.waitForSelector('#notice:not([hidden])', { timeout: 10000 });
    const n1 = await p.textContent('#notice-text');
    ok('3 : séance refusée : message visible depuis Défis', /La séance du jour n'a pas pu démarrer : 3 spots disponibles/.test(n1) && await p.isVisible('#screen-home'), n1);
    await p.click('#notice-close');
    await p.openTab('prog'); await p.waitForSelector('#st-placement'); await p.click('#st-placement');
    await p.waitForSelector('#notice:not([hidden])', { timeout: 10000 });
    const n2 = await p.textContent('#notice-text');
    ok('3 : placement refusé : message visible', /Le test de placement n'a pas pu démarrer/.test(n2), n2);
    await p.click('#notice-close'); await p.unroute('**/sessions');
    await p.click('#home-btn'); await home(p);
  }

  // 5 : le niveau de Progression ne suit pas l'onglet ouvert
  await p.openTab('expl'); await p.waitForTimeout(800); await p.openTab('prog'); await p.waitForSelector('#st-level:not([hidden])', { timeout: 10000 });
  const lvName = await p.innerText('#st-level-name'), picked = await p.textContent('#st-level-pick [aria-pressed="true"]');
  ok('5 : après l\'onglet Exploitant, Progression montre le niveau GTO', /^Niveau GTO 1/.test(lvName) && /^1 ·/.test(picked) && !/Exploiter le field/.test(picked), [lvName, picked]);
  ok('5 : le mode Exploitant à part, avec son libellé', await p.isVisible('#st-level-expl') && /Niveau 4/.test(await p.textContent('#st-level-expl-name')));
  // 11-12 : placement visible sans défiler, objectifs dépliés
  const plY = await p.$eval('#st-placement', (x) => x.getBoundingClientRect().bottom);
  ok('11 : test de placement visible sans défiler', plY > 0 && plY <= 844, plY);
  ok('12 : objectifs de la semaine dépliés', (await p.getAttribute('#extras', 'open')) !== null);
  ok('8 : retour de Progression nommé', /Retour aux défis/.test(await p.textContent('#st-back')));
  await p.screenshot({ path: `${OUT}/retest10_progression.png` });

  // 4 : série rapide abandonnée après 2 mains : « Reprendre » sur Défis avec badge ; le retour ramène à l'onglet GTO
  await p.openTab('gto'); await p.click('#quick-start');
  for (let i = 0; i < 2; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-question:not([hidden])');
  ok('14 : lexique dans l\'en-tête pendant une série', await p.isVisible('#lex-btn'));
  await p.click('#home-btn'); await home(p); await p.waitForSelector('#resume-card:not([hidden])', { timeout: 10000 });
  ok('4 : « Reprendre » sur Défis, avec où en est la série', /2 décisions sur 5/.test(await p.textContent('#resume-card-text')), await p.textContent('#resume-card-text'));
  ok('4 : badge sur l\'onglet Défis', await p.isVisible('#badge-defis'));
  await p.screenshot({ path: `${OUT}/retest10_resume.png` });
  await p.click('#resume-card-go'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('4 : reprise à la 3e main', /3 \/ 5/.test(await p.textContent('#progress')), await p.textContent('#progress'));
  for (let i = 2; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])');
  // 10 : bilan en mots français au niveau 1 ; 9 : plus d'« accueil »
  const mist = await p.innerText('#screen-summary');
  ok('10 : bilan en mots français au niveau 1', !/Ton coup : (FOLD|CALL|ALL-IN|RAISE TO|CHECK)\b/.test(mist) && !/Meilleur coup : (FOLD|CALL|ALL-IN|RAISE TO|CHECK)\b/.test(mist), mist.slice(0, 400));
  ok('8-9 : plus de « accueil » sur le bilan', !/accueil/i.test(mist));
  ok('8 : le retour nomme l\'onglet de départ', /Retour au quiz GTO/.test(await p.textContent('#back-home')), await p.textContent('#back-home'));
  await p.click('#back-home'); await p.waitForSelector('#screen-gto:not([hidden])', { timeout: 10000 });
  ok('4 : retour sur l\'onglet d\'où la série est partie (GTO)', true);
  ok('4 : plus de « Reprendre » une fois la série finie', await p.isHidden('#resume-card') && await p.isHidden('#badge-defis') || !(await p.isVisible('#resume-card')));
  // 6 : les erreurs du jour sur l'écran d'arrivée (Défis)
  await p.click('#home-btn'); await home(p); await p.waitForTimeout(1200);
  const demoNoRoute = demo && !(await p.evaluate(() => fetch('/users/me/worst-today?mode=gto&tz=0').then((r) => r.ok).catch(() => false)));
  if (!demoNoRoute) {
    await p.waitForSelector('#screen-home #worst:not([hidden])', { timeout: 10000 });
    ok('6 : erreurs du jour sur l\'onglet Défis', await tabOf(p, '#worst') === 'defis' && await p.isVisible('#worst'));
    await p.screenshot({ path: `${OUT}/retest10_defis.png`, fullPage: true });
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

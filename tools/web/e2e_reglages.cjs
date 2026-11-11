// Réglages et données dans la feuille du profil, plus de « mode » à choisir (10/11), avec assertions : « Chrono des questions » dans le
// profil (8 s choisi vaut pour la série suivante, gardé après rechargement), exercices adaptatifs dans le profil, exporter et effacer
// seulement dans le profil ; Progression sans ces blocs ni groupe « Mode » dans Par thème ; aucun texte visible ne parle d'un « mode »
// GTO ou Exploitant (onglets, profil, premier lancement).
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_reglages.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const MODE_RE = /\bmode (gto|exploit|exploitant)\b/i;
const visible = (p, sel) => p.$eval(sel, (x) => x.innerText).catch(() => '');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage();   // sans nav_helper : la feuille s'ouvre à la main
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  const ob = await p.isVisible('#screen-onboard') ? await visible(p, '#screen-onboard') : '';
  let ob2 = '', ob3 = '';
  if (ob) { await p.click('#ob-exp button[data-v="debut"]'); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); ob2 = await visible(p, '#screen-onboard');
    await p.click('#ob-next'); ob3 = await visible(p, '#screen-onboard'); }
  ok('premier lancement : « Quiz Exploitant », pas de « mode »', !ob || (/Quiz Exploitant/.test(ob2) && !MODE_RE.test(ob + ob2 + ob3)), ob2.slice(0, 400));
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  const texts = {};
  for (const tab of ['defis', 'quiz', 'quiz:expl', 'exos', 'outils', 'prog']) {      // 11/11 : Quiz (GTO puis Exploitant), Exercices
    const [t, side] = tab.split(':');
    await p.click(`.tab[data-tab="${t}"]`); await p.waitForTimeout(900);
    if (side) { await p.click(`.quiz-switch [data-side="${side}"] >> visible=true`); await p.waitForTimeout(900); }
    texts[tab] = await visible(p, '.tab-page:not([hidden])');
  }
  ok('onglets : aucun « mode » GTO ou Exploitant', Object.values(texts).every((t) => !MODE_RE.test(t)), Object.entries(texts).filter(([, t]) => MODE_RE.test(t)).map(([k, t]) => [k, t.match(/.{0,40}mode.{0,40}/i)[0]]));
  ok('carte Préflop : plus de chrono', !(await p.$('#screen-gto .chrono-row')) && !(await p.$('#train .chrono-row')));
  ok('Progression : ni exporter, ni effacer, ni exercices adaptatifs', !(await p.$('#screen-stats #st-export, #screen-stats #st-delete, #screen-stats #st-adapt')) && !/Exporter mes données|Exercices adaptatifs/.test(texts.prog));
  ok('Progression : pas de groupe « Mode » dans Par thème', !(await p.$$eval('#st-themes .theme-group > b', (xs) => xs.map((x) => x.textContent))).includes('Mode'));
  // la feuille du profil
  await p.click('#profile-btn'); await p.waitForSelector('#profile:not([hidden])');
  const pf = await visible(p, '#profile');
  ok('profil : « Chrono des questions » et ses trois choix', /Chrono des questions/.test(pf) && (await p.$$('#profile .chips[data-name="chrono"] button')).length === 3);
  const demo = BASE.startsWith('file:');                                // la démo n'a ni adaptation, ni export, ni effacement (choix de la démo)
  await p.waitForSelector('#profile #st-adapt:not([hidden])', { timeout: 5000 }).catch(() => {});
  const pf2 = await visible(p, '#profile');
  if (!demo) ok('profil : exercices adaptatifs', /Exercices adaptatifs/.test(pf2) && await p.isVisible('#profile #adapt-on'));
  else ok('démo : pas d\'exercices adaptatifs, ni leur titre seul', !/Exercices adaptatifs/.test(pf2));
  if (!demo) ok('profil : exporter et effacer mes données', await p.isVisible('#profile #st-export') && await p.isVisible('#profile #st-delete'));
  else ok('démo : les boutons de données restent dans le profil (masqués par la démo)', !!(await p.$('#profile #st-export')) && !!(await p.$('#profile #st-delete')));
  ok('profil : aucun « mode »', !MODE_RE.test(pf), pf.match(/.{0,40}mode.{0,40}/i));
  await p.screenshot({ path: `${OUT}/reglages_profil.png`, fullPage: true });
  await p.click('#profile .chips[data-name="chrono"] [data-value="8"]'); await p.click('#pf-close');
  // le chrono choisi vaut pour la série suivante, et reste après rechargement
  await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(500); await p.click('.quiz-switch [data-side="gto"] >> visible=true'); await p.waitForTimeout(500); await p.click('#quick-start');
  await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForSelector('#q-timer:not([hidden])', { timeout: 5000 }).catch(() => {});
  const t = await p.textContent('#q-timer span').catch(() => '');
  ok('chrono à 8 s appliqué à la série', /^[1-8] s$/.test(t.trim()), t);
  await p.reload(); await p.waitForSelector('#today:not([hidden])', { timeout: 20000 });
  ok('chrono gardé après rechargement', await p.getAttribute('#profile .chips[data-name="chrono"] [data-value="8"]', 'aria-pressed') === 'true');
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

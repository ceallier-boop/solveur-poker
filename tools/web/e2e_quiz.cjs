// Onglets du 11/11, avec assertions : Quiz · Exercices · Défis · Progression · Outils ; dans Quiz, deux boutons en haut GTO | Exploitant
// (GTO par défaut, dernier choix gardé sur l'appareil, y compris après rechargement) ; Exercices = Ranges, Équités, Profils ; barre et
// boutons masqués pendant une série ; retour d'une série sur le bon côté du Quiz ; avec l'offre verrouillée (window.SA_EXPLOIT_LOCKED),
// cadenas sur le bouton Exploitant, qui ne s'ouvre pas, et Profils annoncé payant.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_quiz.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const shown = (p) => p.evaluate(() => { const s = document.querySelector('.tab-page:not([hidden])'); return s ? s.id : null; });
const pressed = (p) => p.evaluate(() => { const q = [...document.querySelectorAll('.quiz-switch [aria-pressed="true"]')].find((x) => x.offsetParent); return q ? q.dataset.side : null; });
async function boot(b, locked) {
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
  if (locked) await ctx.addInitScript(() => { window.SA_EXPLOIT_LOCKED = true; });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  return { p, errs };
}
(async () => {
  const b = await chromium.launch();
  let { p, errs } = await boot(b, false);
  const bar = await p.$$eval('#tabs .tab', (xs) => xs.map((x) => [...x.querySelectorAll('span')].map((s) => s.textContent).filter((t) => t.trim()).pop()));   // sans le badge
  ok('cinq onglets : Quiz, Exercices, Défis, Progression, Outils', bar.join('|') === 'Quiz|Exercices|Défis|Progression|Outils', bar);
  await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(600);
  ok('Quiz : côté GTO par défaut', await shown(p) === 'screen-gto' && await pressed(p) === 'gto');
  await p.click('.quiz-switch [data-side="expl"] >> visible=true'); await p.waitForTimeout(800);
  ok('bouton Exploitant : le quiz exploitant, onglet Quiz toujours actif', await shown(p) === 'screen-expl' && await pressed(p) === 'expl'
    && await p.getAttribute('.tab[data-tab="quiz"]', 'aria-current') === 'page');
  await p.screenshot({ path: `${OUT}/quiz_exploitant.png` });
  await p.click('.tab[data-tab="defis"]'); await p.waitForTimeout(500); await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(600);
  ok('le dernier choix est gardé (retour sur Exploitant)', await shown(p) === 'screen-expl');
  await p.reload(); await p.waitForSelector('#today:not([hidden])', { timeout: 20000 }); await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(600);
  ok('gardé après rechargement', await shown(p) === 'screen-expl');
  await p.click('.tab[data-tab="exos"]'); await p.waitForTimeout(600);
  ok('Exercices : Ranges, Équités, Profils', await shown(p) === 'screen-exos'
    && (await p.$$eval('#screen-exos .cat-card', (xs) => xs.map((x) => x.dataset.cat))).join() === 'ranges,equites,profils');
  // une série depuis le côté Exploitant : barre et boutons masqués, retour au quiz Exploitant
  await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(600); await p.click('#quick-start');
  await p.waitForSelector('#screen-question:not([hidden])');
  ok('pendant une série : ni barre ni boutons GTO | Exploitant', await p.isHidden('#tabs') && !(await p.$$eval('.quiz-switch', (xs) => xs.some((x) => x.offsetParent))));
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])');
  ok('retour nommé « quiz Exploitant »', /Retour au quiz Exploitant/.test(await p.textContent('#back-home')));
  await p.click('#back-home'); await p.waitForTimeout(800);
  ok('retour sur le quiz Exploitant', await shown(p) === 'screen-expl');
  ok('aucune erreur JavaScript', !errs.length, errs);
  await p.context().close();
  // offre verrouillée : cadenas sur le bouton Exploitant, qui ne s'ouvre pas ; Profils annoncé payant
  ({ p, errs } = await boot(b, true));
  await p.click('.tab[data-tab="quiz"]'); await p.waitForTimeout(600);
  ok('verrouillé : cadenas sur le bouton Exploitant', /🔒/.test(await p.textContent('.quiz-switch [data-side="expl"] >> visible=true')));
  await p.click('.quiz-switch [data-side="expl"] >> visible=true'); await p.waitForTimeout(600);
  ok('verrouillé : Exploitant ne s\'ouvre pas, message de l\'offre', await shown(p) === 'screen-gto' && await p.isVisible('#notice') && /offre payante/.test(await p.textContent('#notice-text')));
  await p.click('.tab[data-tab="exos"]'); await p.waitForTimeout(600); await p.click('#profils-start'); await p.waitForTimeout(500);
  ok('verrouillé : Profils annoncé payant, pas de série', /offre payante/i.test(await p.textContent('#profils-paid')) && await p.isHidden('#screen-question'));
  ok('aucune erreur JavaScript (verrouillé)', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

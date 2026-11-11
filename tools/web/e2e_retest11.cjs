// Corrections du onzième test joueurs (11/11), avec assertions : (1) sur Défis, un lien « Séance du jour Exploitant » qui ouvre le Quiz
// Exploitant, sans second bloc de séance ; (2) une série GTO abandonnée se reprend côté GTO du Quiz, pas côté Exploitant, et depuis Défis ;
// (3) Équités sans mention d'offre payante, l'étiquette de Profils nomme Profils ; (4) plus d'« onglet GTO / Exploitant » dans les textes ;
// (5) « % des points » sur la carte, la ligne de Progression et le bilan ; (6) depuis le Quiz Exploitant, un lien vers Exercices → Profils.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_retest11.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const shown = (p) => p.evaluate(() => { const s = document.querySelector('.tab-page:not([hidden])'); return s ? s.id : null; });
const tab = async (p, t, side) => { await p.click(`.tab[data-tab="${t}"]`); await p.waitForTimeout(600); if (side) { await p.click(`.quiz-switch [data-side="${side}"] >> visible=true`); await p.waitForTimeout(700); } };
const answer = async (p) => { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); };
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage();
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(800);

  // (1) la séance exploitante annoncée sur Défis
  ok('1 : sur Défis, un seul bloc de séance et le lien « Séance du jour Exploitant »', (await p.$$('#screen-home .today')).length === 1 && await p.isVisible('#defis-expl-today')
    && /Séance du jour Exploitant/.test(await p.textContent('#defis-expl-today')));
  await p.click('#defis-expl-today'); await p.waitForTimeout(900);
  ok('1 : le lien ouvre le Quiz Exploitant, avec sa séance', await shown(p) === 'screen-expl' && await p.isVisible('#screen-expl #today'));
  // (6) depuis le Quiz Exploitant, vers Profils
  ok('6 : lien « Lire les profils des adversaires »', await p.isVisible('#expl-to-profils'));
  await p.click('#expl-to-profils'); await p.waitForTimeout(800);
  ok('6 : il ouvre Exercices, la carte Profils en vue', await shown(p) === 'screen-exos' && await p.evaluate(() => { const r = document.getElementById('cat-profils').getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; }));
  // (3) Équités sans offre payante ; l'étiquette de Profils nomme Profils
  ok('3 : Équités sans mention d\'offre payante', !/payante/i.test(await p.innerText('#cat-equites')));
  ok('3 : l\'étiquette de Profils est dans sa carte et nomme Profils', /^Profils : offre payante/.test(await p.textContent('#profils-paid')) && await p.evaluate(() => !!document.querySelector('#cat-profils .cat-head #profils-paid')));
  await p.screenshot({ path: `${OUT}/retest11_exercices.png`, fullPage: true });
  // (2) série GTO abandonnée après 2 mains
  await tab(p, 'quiz', 'gto'); await p.click('#quick-start'); await answer(p); await answer(p); await p.waitForSelector('#screen-question:not([hidden])');
  await p.click('#home-btn'); await p.waitForSelector('#resume-card:not([hidden])', { timeout: 10000 });
  ok('2 : la carte « Reprendre » reste sur Défis', await p.isVisible('#resume-card'));
  await tab(p, 'quiz', 'expl');
  ok('2 : côté Exploitant, pas de « Reprendre la série en cours » d\'une série GTO', await shown(p) === 'screen-expl' && await p.isHidden('#resume'));
  await tab(p, 'quiz', 'gto');
  ok('2 : côté GTO, « Reprendre la série en cours »', await shown(p) === 'screen-gto' && await p.isVisible('#resume'));
  await p.click('#resume'); for (let i = 2; i < 5; i++) await answer(p);
  await p.waitForSelector('#screen-summary:not([hidden])');
  // (5) « % des points » sur le bilan ; (4) texte de révision
  const sum = await p.innerText('#screen-summary');
  ok('5 : bilan en « % des points »', /\d+ % des points/.test(sum) && !/bonnes réponses/.test(sum), sum.slice(0, 200));
  const rev = await p.textContent('#s-review');
  ok('4 : révision « dans le Quiz, côté GTO ou Exploitant »', /dans le Quiz, côté GTO ou Exploitant/.test(rev) && !/onglet/.test(rev), rev);
  await p.click('#back-home'); await p.waitForSelector('#screen-gto:not([hidden])'); await p.waitForTimeout(1500);
  ok('5 : carte Préflop en « % des points »', /^\d+ % des points · 5 décisions/.test(await p.textContent('#cat-gto-meter')), await p.textContent('#cat-gto-meter'));
  await tab(p, 'prog'); await p.waitForSelector('#st-cats:not([hidden])', { timeout: 10000 }); await p.waitForTimeout(800);
  const row = await p.innerText('#st-cats-list li[data-cat="gto"]');
  ok('5 : ligne Préflop GTO de Progression en « % des points »', /% des points/.test(row) && !/bonnes réponses/.test(row), row);
  // (4) Progression : niveau 4 et son bouton
  const lv = await p.innerText('#st-level-expl');
  ok('4 : « le côté Exploitant du Quiz » et « Ouvrir le Quiz Exploitant »', /le côté Exploitant du Quiz, ouvert en continu/.test(lv) && /Ouvrir le Quiz Exploitant/.test(lv) && !/onglet Exploitant/.test(lv), lv);
  const all = (await p.innerText('body'));
  ok('4 : plus d\'« onglet GTO » ni d\'« onglet Exploitant » à l\'écran', !/onglet (GTO|Exploitant)/i.test(all), all.match(/.{0,30}onglet (GTO|Exploitant).{0,30}/i));
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

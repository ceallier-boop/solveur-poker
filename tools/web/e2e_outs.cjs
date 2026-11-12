// Équités v2, sorte « outs » (tirages et cartes qui améliorent la main), avec assertions : série lancée depuis la carte Équités
// (Exercices) ; question : le tableau (3 cartes du flop, puis turn et river s'il y en a) au-dessus de ta main, réponses en grille ;
// correction : le tableau et ta main, les cartes qui t'améliorent groupées par main obtenue (leur total = le nombre annoncé), le turn,
// la river et la règle des 2 et 4, jamais de BB perdus ; une question sans tableau n'en montre pas.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_outs.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  await p.openTab('exos');
  ok('carte Équités : « Tirages et outs »', await p.isVisible('#equity-kinds [data-kind="outs"]'));
  await p.click('#equity-kinds [data-kind="outs"]'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  const q = await p.evaluate(() => ({
    kind: document.getElementById('eq-kind').textContent, board: !document.getElementById('eq-board').hidden,
    flop: document.querySelectorAll('#eq-board .street.flop .card').length, all: document.querySelectorAll('#eq-board .card').length,
    hand: document.querySelectorAll('#eq-cards .card').length, ask: document.getElementById('ask').textContent,
    bands: document.getElementById('actions').classList.contains('bands'), n: document.querySelectorAll('#actions button').length, firstOpt: (document.querySelector('#actions button b') || {}).textContent, table: !document.getElementById('table-wrap').hidden }));
  ok('question : le flop (3 cartes) au-dessus de ta main (2 cartes)', q.kind === 'Tirages et outs' && q.board && q.flop === 3 && q.all >= 3 && q.all <= 5 && q.hand === 2 && !q.table, q);
  ok('question : énoncé avec le flop, réponses en grille', /le flop est/.test(q.ask) && q.bands && q.n >= 4, q);
  await p.screenshot({ path: `${OUT}/outs_question.png` });
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  const a = await p.evaluate(() => {
    const head = (document.querySelector('#a-equity h4') || {}).textContent || '';
    const per = [...document.querySelectorAll('#a-equity .eq-outs li')].map((li) => ({ cat: li.querySelector('.oc-cat').textContent, cards: li.querySelectorAll('.card').length, n: li.querySelector(':scope > small').textContent }));
    return { head, per, board: document.querySelectorAll('#a-board .card').length, hand: document.querySelectorAll('#a-cards .card').length,
      odds: (document.querySelector('#a-equity .eq-odds') || {}).textContent || '', text: document.getElementById('screen-answer').innerText,
      essential: document.getElementById('a-essential').textContent, verdict: document.getElementById('a-verdict').innerText };
  });
  const total = a.per.reduce((s, x) => s + x.cards, 0), announced = Number((a.head.match(/Les (\d+) cartes?/) || [])[1]);
  ok('correction : le tableau et ta main', a.board >= 3 && a.hand === 2, a);
  ok('correction : verdict en nombre (pas de « tranche ») quand la réponse est un nombre de cartes', !/^\d+ cartes$/.test(q.firstOpt || '') || !/tranche/i.test(a.verdict), a.verdict);
  ok('correction : cartes groupées par main obtenue, total = nombre annoncé', a.per.length >= 1 && total === announced && a.per.every((x) => x.n.startsWith(String(x.cards))), { head: a.head, per: a.per });
  ok('correction : la valeur exacte (cartes sur 47)', /sur 47 améliorent ta main/.test(a.essential) || /%/.test(a.essential), a.essential);
  ok('correction : turn, river et règle des 2 et 4', /Au turn : [\d,]+ %/.test(a.odds) && /Règle des 2 et 4/.test(a.odds), a.odds);
  ok('correction : jamais de BB perdus', !/BB perdus|coûte/.test(a.text));
  ok('correction : la nuance visible (l\'équité n\'est pas l\'argent / améliorer n\'est pas passer devant), pas répétée dans les précisions', await p.isVisible('#a-equity .eq-caveat') && /argent|passer devant/i.test(await p.textContent('#a-equity .eq-caveat')) && !(await p.textContent('#a-details')).includes(await p.textContent('#a-equity .eq-caveat')));
  await p.screenshot({ path: `${OUT}/outs_correction.png`, fullPage: true });
  // une question sans tableau : pas de tableau affiché
  await p.click('#home-btn'); await p.openTab('exos'); await p.click('#equity-kinds [data-kind="hit"]'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('question sans tableau : pas de tableau', await p.isHidden('#eq-board'));
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  ok('correction sans tableau : pas de tableau ni d\'outs', await p.isHidden('#a-board') && !(await p.$('#a-equity .eq-outs')));
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

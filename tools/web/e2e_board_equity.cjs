// Équités v2, sorte « board_equity » (équité d'une main sur un flop connu), avec assertions : série depuis la carte Équités ; question :
// le flop au-dessus de ta main, la range adverse en grille 13 × 13 (teintée selon le poids, son libellé) quand il y en a une, tranches ;
// correction : l'équité avant le flop puis au flop (barres et valeurs), ce que la main a et ses cartes qui l'améliorent, jamais de BB perdus.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_board_equity.cjs [dossier]   (application ou file://…/demo.html)
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
  ok('carte Équités : « Équité sur le flop »', await p.isVisible('#equity-kinds [data-kind="board_equity"]'));
  await p.click('#equity-kinds [data-kind="board_equity"]'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  let withRange = null, plain = null;
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])');
    const q = await p.evaluate(() => {
      const cells = [...document.querySelectorAll('#eq-range .mini-grid i')];
      return { kind: document.getElementById('eq-kind').textContent, flop: document.querySelectorAll('#eq-board .street.flop .card').length,
        hand: document.querySelectorAll('#eq-cards .card').length, range: !document.getElementById('eq-range').hidden, cells: cells.length,
        weighted: cells.filter((c) => parseFloat(c.style.getPropertyValue('--w')) > 0).length, label: (document.querySelector('#eq-range .eq-range-title') || {}).textContent || '',
        ask: document.getElementById('ask').textContent, bands: document.getElementById('actions').classList.contains('bands') };
    });
    if (q.range && !withRange) { withRange = q; await p.screenshot({ path: `${OUT}/board_equity_question.png` }); }
    if (!q.range && !plain) plain = q;
    if (i === 0) ok('question : le flop au-dessus de ta main, réponses en tranches', q.kind === 'Équité sur le flop' && q.flop === 3 && q.hand === 2 && q.bands, q);
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    if (i === 0) {
      const a = await p.evaluate(() => ({ rows: [...document.querySelectorAll('#a-equity .st-row')].map((r) => r.innerText.replace(/\s+/g, ' ')),
        note: [...document.querySelectorAll('#a-equity p.note')].map((x) => x.textContent).join(' '), text: document.getElementById('screen-answer').innerText,
        board: document.querySelectorAll('#a-board .card').length }));
      ok('correction : avant le flop puis au flop, avec leurs valeurs', a.rows.length === 2 && /^Avant le flop .*[\d,]+ %$/.test(a.rows[0]) && /^Au flop .*[\d,]+ %$/.test(a.rows[1]), a.rows);
      ok('correction : ce que la main a et ses cartes qui l\'améliorent', /Ta main pour l'instant : .+ ; \d+ cartes? l'améliore/.test(a.note), a.note);
      ok('correction : le tableau, jamais de BB perdus', a.board === 3 && !/BB perdus|coûte/.test(a.text));
      ok('correction : la nuance visible (l\'équité n\'est pas l\'argent / améliorer n\'est pas passer devant), pas répétée dans les précisions', await p.isVisible('#a-equity .eq-caveat') && /argent|passer devant/i.test(await p.textContent('#a-equity .eq-caveat')) && !(await p.textContent('#a-details')).includes(await p.textContent('#a-equity .eq-caveat')));
      await p.screenshot({ path: `${OUT}/board_equity_correction.png`, fullPage: true });
    }
    await p.click('#next-btn');
  }
  if (withRange) ok('range adverse : grille 13 × 13 teintée et son libellé', withRange.cells === 169 && withRange.weighted > 0 && withRange.weighted < 169 && /Contre : .+ %/.test(withRange.label), withRange);
  else ok('au moins une question contre une range sur 5 (sinon : relancer)', !!plain, { plain });   // les deux sujets alternent ; « contre une main au hasard » n'a pas de grille
  if (plain) ok('contre une main au hasard : pas de grille', plain.cells === 0, plain);
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, withRange: !!withRange, plain: !!plain, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

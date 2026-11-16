// Corrections du douzième test joueurs (docs/produit/RETEST12_JOUEURS_2026-11-16.md), avec assertions :
//   1. niveau 1 : titres d'équité sans jargon, à l'écran et sur les boutons de la carte (« Chances de gagner avant le flop », « Cartes qui
//      améliorent ta main », « Tes mains possibles contre les siennes ») ; niveau 2 : les termes reviennent (« Tirages et outs ») ;
//   2. range contre range : la légende des grilles (case foncée / claire, toi en bleu, lui en vert) ;
//   3. Progression : pas de BB perdus sous 30 décisions (« pas assez de décisions pour mesurer (N sur 30) ») ; au-dessus, sans
//      décimales superflues (109 BB, 12,4 BB) ;
//   4. import : l'étape suivante annoncée ; 5. « Importer mes mains » sur une ligne dans la barre du haut ;
//   6. lecture du vilain : contexte long replié (« Voir la suite »), les barres de stats toujours visibles ;
//   7. placement d'un niveau 2 proposé au niveau 1 : « Revenir au niveau 1 », une phrase, « Garder le niveau 2 » en bouton plein.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_retest12.cjs [dossier]   (application ; les points 3 et 7 simulent
// la réponse du serveur, la démo n'est pas couverte)
const { chromium } = require('playwright');
const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const L1 = { equity: 'Chances de gagner avant le flop', outs: 'Cartes qui améliorent ta main', range_help: 'Tes mains possibles contre les siennes' };   // titres du serveur (equity_quiz.KIND_FR_L1)

(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' });
    const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e))); return p;
  };
  const start = async (p) => {
    await p.goto(BASE);
    await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
    if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
    await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  };
  const kindTitle = async (p, k) => {
    await p.click('#home-btn').catch(() => {}); await p.openTab('exos');
    await p.click(`#equity-kinds [data-kind="${k}"]`, { timeout: 8000 }).catch(async (e) => { await p.screenshot({ path: `${OUT}/retest12_fail.png`, fullPage: true }); throw e; }); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
    return p.evaluate(() => ({ kind: document.getElementById('eq-kind').dataset.kind, title: document.getElementById('eq-kind').textContent }));
  };

  // --- joueur de niveau 1
  const p = await page(); await start(p);
  await p.openTab('exos');
  const btns = await p.$$eval('#equity-kinds [data-kind]', (xs) => Object.fromEntries(xs.map((x) => [x.dataset.kind, x.textContent])));
  ok('niveau 1 : boutons de la carte Équités sans jargon', Object.keys(L1).every((k) => btns[k] === L1[k]) && !/range|outs|équité/i.test(Object.values(btns).join(' ')), btns);
  for (const k of ['equity', 'outs', 'range_help']) {
    const t = await kindTitle(p, k);
    ok(`niveau 1 : titre sans jargon (${k})`, t.kind === k && t.title === L1[k], t);
    if (k === 'range_help') {
      const lg = await p.evaluate(() => { const l = document.querySelector('#eq-range .mini-legend'); return l && { text: l.innerText.replace(/\s+/g, ' '), sw: l.querySelectorAll('.sw').length }; });
      ok('range contre range : légende foncée / claire, toi et lui', lg && /Case foncée : main jouée souvent/.test(lg.text) && /Case claire : rarement/.test(lg.text)
        && /Toi en bleu/.test(lg.text) && /Lui en vert/.test(lg.text) && lg.sw === 4, lg);
      await p.screenshot({ path: `${OUT}/retest12_range_legend.png` });
    }
  }
  // 3. sous 30 décisions : pas de BB perdus
  await p.click('#home-btn').catch(() => {}); await p.openTab('gto'); await p.click('#quick-start');
  for (let i = 0; i < 40; i++) {
    await p.waitForSelector('#screen-question:not([hidden]), #screen-summary:not([hidden])', { timeout: 15000 });
    if (await p.isVisible('#screen-summary')) break;
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  await p.openTab('prog'); await p.waitForSelector('#st-score .st-tiles', { timeout: 15000 });
  const tile = await p.innerText('#st-score .st-tiles');
  ok('Progression sous 30 décisions : pas de BB perdus, « pas assez de décisions pour mesurer (N sur 30) »',
    /pas assez de décisions pour mesurer \(\d+ sur 30\)/.test(tile) && !/\d+(,\d+)? BB/.test(tile), tile);
  // 4 et 5. import : la suite annoncée ; le titre sur une ligne
  await p.openTab('outils'); await p.click('#import-btn'); await p.waitForSelector('#screen-import:not([hidden])');
  const bar = await p.evaluate(() => { const e = document.getElementById('progress'), cs = getComputedStyle(e);
    return { text: e.textContent, lines: Math.round(e.getBoundingClientRect().height / parseFloat(cs.lineHeight || 20)), h: e.getBoundingClientRect().height, lh: cs.lineHeight, clipped: e.scrollWidth > e.clientWidth }; });
  ok('barre du haut : « Importer mes mains » sur une ligne, sans coupure', bar.text === 'Importer mes mains' && bar.h < 30 && !bar.clipped, bar);
  const dir = path.join(__dirname, '../../tests/data/winamax');
  const fs = require('fs'); const files = fs.readdirSync(dir).filter((f) => f.endsWith('.txt') && !/summary/i.test(f)).map((f) => path.join(dir, f));
  await p.setInputFiles('#im-files', files); await p.waitForSelector('#im-result:not([hidden])', { timeout: 20000 });
  ok('import : l\'étape suivante annoncée avant l\'enregistrement', await p.isVisible('#im-next')
    && /Étape suivante : le bilan de tes mains, bientôt\. Pour l'instant, enregistre tes comptages\./.test(await p.innerText('#im-next')));
  await p.screenshot({ path: `${OUT}/retest12_import.png`, fullPage: true });
  // 6. lecture du vilain : contexte replié, stats visibles
  await p.click('#im-back'); await p.openTab('exos'); await p.click('#profils-start'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  let read = null;
  for (let i = 0; i < 5 && !read; i++) {
    const v = await p.evaluate(() => { const c = document.getElementById('fctx'); return c && { long: c.classList.contains('clamp'), h: c.getBoundingClientRect().height, full: c.scrollHeight,
      bars: document.querySelectorAll('#villain .vbar').length, more: !!document.getElementById('fmore') }; });
    if (v && v.long) read = v;
    else { await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
      await p.waitForSelector('#screen-question:not([hidden]), #screen-summary:not([hidden])'); if (await p.isVisible('#screen-summary')) break; }
  }
  ok('lecture du vilain : contexte long replié, « Voir la suite », barres visibles', read && read.more && read.h < read.full && read.bars >= 2, read);
  if (read) {
    await p.screenshot({ path: `${OUT}/retest12_lecture.png` });
    await p.click('#fmore');
    const after = await p.evaluate(() => ({ clamp: document.getElementById('fctx').classList.contains('clamp'), btn: document.getElementById('fmore').textContent }));
    ok('lecture du vilain : « Voir la suite » déplie le texte', !after.clamp && after.btn === 'Voir moins', after);
  }

  // --- joueur de niveau 2 (confirmé) : placement simulé à un niveau en dessous, puis les termes reviennent
  const q = await page();
  await q.goto(BASE);
  await q.waitForSelector('#screen-onboard:not([hidden])', { timeout: 20000 });
  await q.click('#ob-exp button[data-v="confirme"]'); await q.click('#ob-goal button[data-v="bases"]'); await q.click('#ob-next'); await q.click('#ob-next');
  await q.click('#ob-placement');                                     // le test de placement proposé au joueur confirmé
  await q.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  await q.route('**/users/me/placement?*', async (route) => {
    const res = await route.fetch(); const j = await res.json();
    await route.fulfill({ response: res, json: { ...j, proposed_level: 1, current_level: 2, proposed_name: 'Tapis courts', proposed_depth_fr: 'moins de 10 BB' } });
  });
  for (let i = 0; i < 12; i++) {
    await q.waitForSelector('#screen-question:not([hidden]), #screen-placement:not([hidden]), #screen-home:not([hidden])', { timeout: 15000 });
    if (!(await q.isVisible('#screen-question'))) break;
    await q.click('#actions button >> nth=0'); await q.waitForSelector('#screen-answer:not([hidden])'); await q.click('#next-btn');
  }
  ok('placement : écran du résultat', await q.isVisible('#screen-placement'));
  if (await q.isVisible('#screen-placement')) {
    const pl = await q.evaluate(() => ({ take: document.getElementById('pl-take').textContent, takeCls: document.getElementById('pl-take').className,
      keep: document.getElementById('pl-keep').textContent, keepCls: document.getElementById('pl-keep').className,
      keepFirst: !!(document.getElementById('pl-keep').compareDocumentPosition(document.getElementById('pl-take')) & Node.DOCUMENT_POSITION_FOLLOWING),
      down: document.getElementById('pl-down').hidden ? '' : document.getElementById('pl-down').textContent }));
    ok('placement en baisse : « Revenir au niveau 1 » avec sa phrase, « Garder le niveau 2 » en bouton plein, en premier',
      pl.take === 'Revenir au niveau 1' && /secondary/.test(pl.takeCls) && pl.keep === 'Garder le niveau 2' && /primary/.test(pl.keepCls) && pl.keepFirst
      && /tapis courts/.test(pl.down), pl);
    await q.screenshot({ path: `${OUT}/retest12_placement.png`, fullPage: true });
    await q.click('#pl-keep'); await q.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 15000 }); await q.waitForTimeout(1200);   // accueil fini de charger
  }
  const t2 = await kindTitle(q, 'outs');
  const btn2 = await q.textContent('#equity-kinds [data-kind="outs"]');
  ok('niveau 2 : bouton « Tirages et outs »', btn2 === 'Tirages et outs', btn2);
  ok('niveau 2 : les termes reviennent (« Tirages et outs »)', t2.kind === 'outs' && t2.title === 'Tirages et outs', t2);
  // 3 bis. au-dessus de 30 décisions : sans décimales superflues (réponse du serveur simulée)
  await q.unroute('**/users/me/placement?*');
  for (const [v, want] of [[108.888, '109 BB'], [12.44, '12,4 BB']]) {
    await q.route('**/users/me/stats*', async (route) => { const res = await route.fetch(); const j = await res.json();
      await route.fulfill({ response: res, json: { ...j, bb_per_100: v, ev_questions: 150, questions: Math.max(j.questions || 0, 150) } }); });
    await q.click('#home-btn').catch(() => {}); await q.openTab('prog'); await q.waitForSelector('#st-score .st-tiles', { timeout: 15000 });
    await q.waitForTimeout(300);
    const t = await q.innerText('#st-score .st-tiles');
    ok(`Progression au-dessus de 30 décisions : ${want}`, t.includes(want) && /perdus pour 100 décisions/.test(t), t);
    await q.unroute('**/users/me/stats*'); await q.openTab('defis');
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

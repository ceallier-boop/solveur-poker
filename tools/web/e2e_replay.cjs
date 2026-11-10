// Rejouée de la main avant chaque question (décision du porteur, 10/11), avec assertions : table vide avec les tapis, cartes, blindes,
// puis chaque action de question.history dans l'ordre avec sa bulle, jusqu'au héros ; options et chrono seulement à la fin ; jetons
// par type d'action (limp ou blinde : un jeton ; relance : une pile ; tapis : plusieurs colonnes) ; « Passer » ; réduction des
// mouvements : état final direct ; énoncé et historique texte toujours présents.
// Sur l'application, deux questions sont réécrites à l'affichage (historique choisi) pour couvrir chaque type de jeton ; dans la démo
// (pas de réseau à intercepter), les contrôles portent sur les questions telles qu'elles viennent.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_replay.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const demo = BASE.startsWith('file:');
// historiques imposés (3 joueurs, héros au BB) : relance puis tapis ; limp puis fold
const PATCHES = [
  { history: [{ position: 'BTN', action: 'raise', to_bb: 2.5 }, { position: 'SB', action: 'allin', to_bb: 10 }],
    history_fr: ['Le BTN relance à 2,5 BB', 'Le SB part à tapis (10 BB)'], bubbles: ['Relance à 2,5 BB', 'Tapis 10 BB'] },
  { history: [{ position: 'BTN', action: 'limp', to_bb: 1 }, { position: 'SB', action: 'fold' }],
    history_fr: ['Le BTN limpe', 'Le SB se couche'], bubbles: ['Limp', 'Se couche'] },
];
async function boot(ctxOpts) {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, ...ctxOpts });
  const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  return { b, p, errs };
}
// relève, pendant la rejouée, chaque étape affichée (data-step), la bulle, et si les options ou le chrono sont visibles
const watch = (p) => p.evaluate(() => new Promise((resolve) => {
  const seen = []; let last = null; const t0 = performance.now();
  const iv = setInterval(() => {
    const v = document.getElementById('table-view'), step = v.dataset.step, bub = v.parentElement.querySelector('.bubble');
    const key = step + '|' + (bub ? bub.textContent : '');
    const optsShown = !document.getElementById('actions').hidden, timer = !document.getElementById('q-timer').hidden;
    if (key !== last) { seen.push({ step, bubble: bub ? bub.textContent : null, optsShown, timer, ms: Math.round(performance.now() - t0) }); last = key; }
    if (step === 'final') { clearInterval(iv); resolve(seen); }
  }, 30);
}));
const chipsAt = (p) => p.evaluate(() => {
  const out = {};
  for (const s of document.querySelectorAll('#table-view .seat')) {
    const pos = s.querySelector('b').textContent.replace(/[^A-Z]/g, '').slice(-3).replace(/^.*(BTN|SB|BB)$/, '$1');
    const c = s.querySelector('.stake'); out[pos] = c ? { type: c.dataset.chips, piles: c.querySelectorAll('.pile').length, chips: c.querySelectorAll('i').length } : null;
  }
  const h = document.querySelector('#table-view .hero-bet .stake');
  out.hero = h ? { type: h.dataset.chips, piles: h.querySelectorAll('.pile').length, chips: h.querySelectorAll('i').length } : null;
  return out;
});
const answerAndNext = async (p) => { await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); };

(async () => {
  let { b, p, errs } = await boot({});
  let n = 0;
  if (!demo) await p.route('**/quiz/next*', async (r) => {
    const res = await r.fetch(); const d = await res.json(); const q = d.question;
    const patch = d.question_index >= 1 && d.question_index <= PATCHES.length ? PATCHES[d.question_index - 1] : null;
    if (patch && q && q.hand && !(q.field && q.field.ask_fr)) {
      Object.assign(q, { players: ['BTN', 'SB', 'BB'], stacks_bb: [20, 10, 15], hero: 'BB', table: '3-handed', history: patch.history, history_fr: patch.history_fr });
      n++;
    }
    r.fulfill({ response: res, body: JSON.stringify(d) });
  });
  await p.openTab('gto'); await p.click('#quick-start');
  // question 1, telle qu'elle vient : la séquence complète et l'ordre
  await p.waitForSelector('#screen-question:not([hidden])');
  const q0 = await p.evaluate(() => {                                 // depuis la page (dans la démo, l'état de l'application n'est pas global)
    const li = [...document.querySelectorAll('#history li')].map((x) => x.textContent);
    const hfr = li.length === 1 && /Tu parles en premier/.test(li[0]) ? [] : li;
    return { history: hfr, hfr };
  });
  const seen0 = await watch(p);
  const steps0 = seen0.map((x) => x.step);
  const want0 = ['0', 'c0', 'cb0', ...q0.history.map((_, k) => `cb${k + 1}`), 'final'];
  ok('séquence : table vide, cartes, blindes, puis chaque action, puis l\'état final', JSON.stringify(steps0.filter((x, i) => x !== steps0[i - 1])) === JSON.stringify(want0), [steps0, want0]);
  ok('options et chrono cachés pendant la rejouée, visibles à la fin',
    seen0.filter((x) => x.step !== 'final').every((x) => !x.optsShown && !x.timer) && await p.isVisible('#actions button'), seen0);
  const total0 = seen0[seen0.length - 1].ms;
  ok('durée courte (moins de 3,5 s)', total0 < 3500, total0);
  ok('énoncé et historique texte présents', (await p.textContent('#prompt-full')).length > 10 && (await p.$$('#history li')).length === Math.max(1, q0.hfr.length));
  await p.screenshot({ path: `${OUT}/replay_final.png` });
  if (!demo) {
    // question 2 : relance (une pile) puis tapis (plusieurs colonnes), bulles dans l'ordre
    await answerAndNext(p); await p.waitForSelector('#screen-question:not([hidden])');
    const seen1 = await watch(p);
    ok('bulles dans l\'ordre de l\'historique', JSON.stringify(seen1.map((x) => x.bubble).filter(Boolean)) === JSON.stringify(PATCHES[0].bubbles), seen1);
    const blinds = seen1.find((x) => x.step === 'cb0');
    const c1 = await chipsAt(p);
    ok('relance : une pile de plusieurs jetons', c1.BTN && c1.BTN.type === 'bet' && c1.BTN.piles === 1 && c1.BTN.chips >= 2, c1);
    ok('tapis : plusieurs colonnes de jetons', c1.SB && c1.SB.type === 'allin' && c1.SB.piles >= 2, c1);
    ok('blinde du héros : un seul jeton', c1.hero && c1.hero.type === 'blind' && c1.hero.chips === 1, c1);
    ok('montants en BB sous les jetons', /2,5\s*BB/.test(await p.textContent('#table-view')) && /10\s*BB/.test(await p.textContent('#table-view')));
    ok('l\'étape des blindes existe avant toute action', !!blinds);
    await p.screenshot({ path: `${OUT}/replay_raise_allin.png` });
    // question 3 : « Passer » tout de suite ; limp = un jeton ; le joueur qui se couche n'a plus de cartes
    await answerAndNext(p); await p.waitForSelector('#screen-question:not([hidden])');
    await p.click('#replay-skip');
    const st = await p.evaluate(() => ({ step: document.getElementById('table-view').dataset.step, opts: !document.getElementById('actions').hidden, skip: !document.getElementById('replay-skip').hidden }));
    ok('« Passer » : état final tout de suite, options visibles', st.step === 'final' && st.opts && !st.skip, st);
    const c2 = await chipsAt(p);
    ok('limp : un seul jeton', c2.BTN && c2.BTN.type === 'limp' && c2.BTN.piles === 1 && c2.BTN.chips === 1, c2);
    ok('joueur couché : plus de cartes', await p.evaluate(() => { const s = [...document.querySelectorAll('#table-view .seat')].find((x) => /SB/.test(x.querySelector('b').textContent)); return s && s.classList.contains('folded') && !s.querySelector('.backs'); }));
    ok('deux questions réécrites pour le test', n === 2, n);
    await p.screenshot({ path: `${OUT}/replay_limp.png` });
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  await b.close();
  // réduction des mouvements : état final direct, sans bouton « Passer »
  ({ b, p, errs } = await boot({ reducedMotion: 'reduce' }));
  await p.openTab('gto'); await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  const rm = await p.evaluate(() => ({ step: document.getElementById('table-view').dataset.step, opts: !document.getElementById('actions').hidden, skip: !document.getElementById('replay-skip').hidden }));
  ok('réduction des mouvements : état final direct', rm.step === 'final' && rm.opts && !rm.skip, rm);
  ok('aucune erreur JavaScript (mouvements réduits)', !errs.length, errs);
  await b.close();
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

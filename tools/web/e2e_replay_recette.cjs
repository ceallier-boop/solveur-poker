// Recette de la main rejouée à la table (10/11), en complément de e2e_replay.cjs (Interface, qui contrôle les jetons sur deux
// historiques imposés) : ici, uniquement des questions réellement servies, sur l'application ou la démo :
//   au moins 15 questions (3 séries rapides, puis d'autres séries, 8 au plus, tant que moins de 5 sièges adverses ont misé) : une bulle par action de question.history, dans l'ordre et au bon siège, puis l'état final ;
//   à l'état final, les jetons de chaque adversaire suivent sa dernière action (tapis → plusieurs colonnes, relance → une pile,
//   limp → un jeton) ; options et chrono cachés jusqu'à la fin ;
//   chrono à 8 s : il démarre à la fin de la rejouée (le joueur ne perd pas de temps) ;
//   pendant la rejouée, la touche « 1 » ne répond pas ; à la fin, elle répond.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_replay_recette.cjs      (ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const CHIP_OF = { allin: 'allin', raise: 'bet', limp: 'limp' };      // dernière action → jetons attendus (call, fold : pas contrôlés)

const watchQ = (p) => p.evaluate(() => {                              // la question reçue (application ou démo, qui remplace fetch)
  const f = window.fetch;
  window.fetch = async (path, opts) => {
    const r = await f(path, opts);
    if (String(path).includes('/quiz/next')) { const j0 = r.json.bind(r); r.json = async () => { const j = await j0(); if (j && j.question) window.__q = j.question; return j; }; }
    return r;
  };
});
const replay = (p) => p.evaluate(() => new Promise((resolve) => {     // bulles (siège, texte) et visibilité des options / du chrono jusqu'à l'état final
  const bubbles = []; let last = null, hidden = true; const t0 = performance.now();
  const iv = setInterval(() => {
    const v = document.getElementById('table-view'); const b = document.querySelector('#table-wrap .bubble');
    const key = v.dataset.step + '|' + (b ? b.dataset.pos + b.textContent : '');
    if (v.dataset.step !== 'final' && (!document.getElementById('actions').hidden || !document.getElementById('q-timer').hidden)) hidden = false;
    if (key !== last && b && v.dataset.step !== 'final') bubbles.push(b.dataset.pos);
    last = key;
    if (v.dataset.step === 'final' || performance.now() - t0 > 8000) { clearInterval(iv); resolve({ bubbles, hidden, final: v.dataset.step === 'final', ms: Math.round(performance.now() - t0) }); }
  }, 25);
}));
const chips = (p) => p.evaluate(() => Object.fromEntries([...document.querySelectorAll('#table-view .seat')].map((s) => {
  const pos = (s.querySelector('b').textContent.match(/BTN|SB|BB/) || [''])[0]; const c = s.querySelector('.stake');
  return [pos, c ? { type: c.dataset.chips, piles: c.querySelectorAll('.pile').length, chips: c.querySelectorAll('i').length } : null];
})));

(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await watchQ(p);
  await p.openTab('gto'); await p.click('.chips[data-name="chrono"] button[data-value="8"]');
  const orderErr = [], chipErr = [], hideErr = [], timerErr = []; let n = 0, withHistory = 0, keyOk = null, checkedChips = 0;
  for (let s = 0; s < 3 || (checkedChips < 5 && s < 8); s++) {          // séries en plus tant que les mises adverses manquent (échec aléatoire du 11/11)
    await p.openTab('gto'); await p.click('#quick-start');
    for (let i = 0; i < 5; i++) {
      await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(40);
      if (s === 0 && i === 0) {                                     // la touche « 1 » pendant la rejouée
        const step = await p.evaluate(() => document.getElementById('table-view').dataset.step);
        await p.keyboard.press('1'); await p.waitForTimeout(250);
        keyOk = { pendant: step, reste: await p.isVisible('#screen-question') && !(await p.isVisible('#screen-answer')) };
      }
      const r = await replay(p); const q = await p.evaluate(() => window.__q); n += 1;
      const hist = (q.history || []).filter((h) => h.position !== q.hero || true);
      if (hist.length) withHistory += 1;
      if (!r.final) orderErr.push({ q: q.spot_id, bloqué: r });
      if (JSON.stringify(r.bubbles) !== JSON.stringify(hist.map((h) => h.position))) orderErr.push({ q: q.spot_id, bulles: r.bubbles, historique: hist.map((h) => `${h.position} ${h.action}`) });
      if (!r.hidden) hideErr.push(q.spot_id);
      const t = await p.textContent('#q-timer'); const secs = Number((t.match(/(\d+)/) || [0, 0])[1]);
      if (!(secs >= 7)) timerErr.push({ q: q.spot_id, chrono: t.trim(), rejouée_ms: r.ms });
      const c = await chips(p); const lastOf = {};
      for (const h of hist) lastOf[h.position] = h.action;
      for (const [pos, act] of Object.entries(lastOf)) {
        if (pos === q.hero || !CHIP_OF[act]) continue; checkedChips += 1;
        const got = c[pos]; const want = CHIP_OF[act];
        if (!got || got.type !== want || (want === 'allin' && got.piles < 2) || (want === 'bet' && got.piles !== 1) || (want === 'limp' && got.chips !== 1)) chipErr.push({ q: q.spot_id, siège: pos, action: act, jetons: got });
      }
      if (s === 0 && i === 0) { await p.keyboard.press('1'); await p.waitForSelector('#screen-answer:not([hidden])', { timeout: 5000 }); keyOk.apres = true; }
      else { await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); }
      await p.click('#next-btn');
    }
    await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(600);
  }
  ok(`bulles : une par action, dans l'ordre et au bon siège (${n} questions, ${withHistory} avec un historique)`, n >= 15 && n % 5 === 0 && withHistory >= 5 && !orderErr.length, orderErr.slice(0, 5));
  ok(`jetons de l'état final conformes à la dernière action de chaque adversaire (${checkedChips} sièges contrôlés)`, checkedChips >= 5 && !chipErr.length, chipErr.slice(0, 5));
  ok('options et chrono cachés pendant toute la rejouée', !hideErr.length, hideErr);
  ok('chrono à 8 s : il démarre à la fin de la rejouée (au moins 7 s affichées)', !timerErr.length, timerErr.slice(0, 5));
  ok('touche « 1 » sans effet pendant la rejouée, active à la fin', keyOk && keyOk.pendant !== 'final' && keyOk.reste && keyOk.apres, keyOk);
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

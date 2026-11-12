// CE3 : questions d'équités dans la démo autonome, par le moteur local (mêmes routes que l'API ; l'écran dédié viendra d'Interface).
// Vérifie : série « equity » de cinq questions, les trois sortes, catégorie « Équités », la bonne tranche contient la valeur exacte,
// notation plein / demi-point / zéro, bilan sans BB perdus, et une série GTO ne tire jamais d'équités ni ne les compte dans son BB/100.
// Usage : DEMO_URL=http://localhost:8072/spinsacademy.html node tools/web/e2e_equity_demo.cjs
const { chromium } = require('playwright');
(async () => {
  const URL = process.env.DEMO_URL || 'http://localhost:8072/spinsacademy.html'; const b = await chromium.launch();
  const p = await b.newPage(); const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(URL); await p.waitForFunction(() => typeof DEMO !== 'undefined', null, { timeout: 30000 }); await p.evaluate(() => DEMO.ready);
  const res = await p.evaluate(async () => {
    const api = async (path, body) => { const r = await fetch(path, body ? { method: 'POST', body: JSON.stringify(body) } : undefined); return [r.status, await r.json()]; };
    const out = { kinds: [], checks: [] };
    const [st, s] = await api('/sessions', { mode: 'equity', size: 5 }); out.create = st;
    for (let i = 0; i < 5; i++) {
      const [, n] = await api(`/quiz/next?session_id=${s.session_id}`); const q = n.question;
      out.kinds.push(q.kind); if (q.category_fr !== 'Équités' || q.mode !== 'equity') out.checks.push('catégorie ' + q.category_fr);
      const [, a] = await api('/attempts', { session_id: s.session_id, question_index: i, action_id: q.options[0].id });
      if (a.regret_mbb !== 0) out.checks.push('regret non nul');
      if (q.kind !== 'labels') {
        const c = q.options.findIndex((o) => o.id === a.best_action), v = a.equity.value_bp / 100, lab = q.options[c].label_fr, nums = (lab.match(/\d+/g) || []).map(Number);
        const ok = lab.startsWith('moins') ? v < nums[0] : lab.includes('ou plus') ? v >= nums[0] : v >= nums[0] && v < nums[1];
        if (!ok) out.checks.push(`tranche ${lab} sans ${v}`);
        const d = Math.abs(c), want = d === 0 ? 'correct' : d === 1 ? 'imprécision' : 'erreur';
        if (a.verdict !== want) out.checks.push(`verdict ${a.verdict} au lieu de ${want}`);
      }
    }
    const [, sum] = await api(`/sessions/${s.session_id}/summary`); out.summary = { complete: sum.complete, bb: sum.bb_per_100, cat: sum.category_fr };
    const [, g] = await api('/sessions', { mode: 'gto', size: 5 }); let gtoEq = 0;
    for (let i = 0; i < 5; i++) {
      const [, n] = await api(`/quiz/next?session_id=${g.session_id}`); if (n.question.mode === 'equity') gtoEq += 1;
      await api('/attempts', { session_id: g.session_id, question_index: i, action_id: n.question.options[0].id });
    }
    out.gtoEquity = gtoEq;
    const [, stats] = await api('/users/me/stats'); out.stats = { questions: stats.questions, ev: stats.ev_questions, equity: stats.equity.questions, modes: stats.by.mode.map((m) => m.filters.mode) };
    const [bad] = await api('/sessions', { mode: 'equity', filters: { table: 'heads-up' } }); out.badFilter = bad;
    const [, one] = await api('/sessions', { mode: 'equity', size: 3, filters: { kind: 'labels' } }); const [, n1] = await api(`/quiz/next?session_id=${one.session_id}`); out.labelsOnly = n1.question.kind;
    const [, o] = await api('/sessions', { mode: 'equity', size: 3, filters: { kind: 'outs' } }); out.outs = [];      // v2 : outs avec tableau
    for (let i = 0; i < 3; i++) {
      const [, n] = await api(`/quiz/next?session_id=${o.session_id}`); const q = n.question;
      const [, a] = await api('/attempts', { session_id: o.session_id, question_index: i, action_id: q.options[0].id });
      out.outs.push(q.kind === 'outs' && q.board.length === 3 && q.hero_cards.length === 2 && a.equity.outs_count >= 2 && a.regret_mbb === 0);
    }
    const [, be] = await api('/sessions', { mode: 'equity', size: 2, filters: { kind: 'board_equity' } }); out.boardEq = [];      // v2 : équité sur le flop
    for (let i = 0; i < 2; i++) {
      const [, n] = await api(`/quiz/next?session_id=${be.session_id}`); const q = n.question;
      const [, a] = await api('/attempts', { session_id: be.session_id, question_index: i, action_id: q.options[0].id });
      out.boardEq.push(q.kind === 'board_equity' && q.board.length === 3 && a.equity.by_street.length === 2 && a.regret_mbb === 0);
    }
    const [, fh] = await api('/sessions', { mode: 'equity', size: 2, filters: { kind: 'flop_help' } }); out.flopHelp = [];      // v2 : ce flop t'aide-t-il ?
    for (let i = 0; i < 2; i++) {
      const [, n] = await api(`/quiz/next?session_id=${fh.session_id}`); const q = n.question;
      const [, a] = await api('/attempts', { session_id: fh.session_id, question_index: i, action_id: q.options[0].id });
      out.flopHelp.push(q.kind === 'flop_help' && q.options.length === 3 && q.ranges.length === 1 && typeof a.equity.delta_bp === 'number');
    }
    return out;
  });
  const ok = res.create === 201 && new Set(res.kinds).size === 3 && !res.checks.length && res.summary.complete && res.summary.bb === null && res.gtoEquity === 0
    && res.stats.questions === 5 && res.stats.ev === 5 && res.stats.equity === 5 && res.stats.modes.join() === 'gto' && res.badFilter === 422 && res.labelsOnly === 'labels' && res.outs.length === 3 && res.outs.every(Boolean) && res.boardEq.length === 2 && res.boardEq.every(Boolean) && res.flopHelp.length === 2 && res.flopHelp.every(Boolean) && !res.kinds.includes('outs') && !errs.length;
  console.log(JSON.stringify(Object.assign(res, { errs, ok }), null, 1)); await b.close(); process.exit(ok ? 0 : 1);
})();

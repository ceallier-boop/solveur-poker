// Recette par l'interface de l'écran des équités et du rangement par catégorie (10/11), application ou démo, en complément de
// e2e_equity.cjs et e2e_categories.cjs (Interface). Les attendus ne viennent pas de l'interface :
//   équités : bonne tranche et affirmations recalculées depuis spinsacademy/data/equites.json brut ; on répond exprès juste, à côté
//   (tranche voisine) ou faux, et le verdict, la valeur exacte affichée et le bilan sont comparés à ces attendus ; ni table, ni chrono,
//   ni rejouée, ni BB ; une série « d'une seule sorte » ne pose que cette sorte ;
//   catégories : chiffres des cartes (GTO, Exploitant) et tableau « Par catégorie » (cinq lignes) comparés au décompte des réponses
//   jouées par ce script ; étiquette de catégorie sur la question, le bilan et les cartes de défi de la semaine.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_ui_categories_recette.cjs [dossier]      (ou file://…/demo.html)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const { spawn } = require('child_process'); const readline = require('readline');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const T = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'spinsacademy', 'data', 'equites.json'), 'utf8'));
const IDX = Object.fromEntries(T.hands.map((h, i) => [h, i]));
const HIT_KEYS = { suite: ['suite', 'quinte_flush'], couleur: ['couleur', 'quinte_flush'] };
const CAT_FR = { gto: 'Préflop GTO', exploit: 'Préflop exploitant', profils: 'Profils', ranges: 'Ranges', equites: 'Équités' };
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const helper = spawn(process.env.PYTHON || 'python3', [path.join(__dirname, 'e2e_audit_helper.py'), 'picks'], { stdio: ['pipe', 'pipe', 'inherit'] });
const waiting = []; readline.createInterface({ input: helper.stdout }).on('line', (l) => waiting.shift()(JSON.parse(l)));
const pick = (which, q) => new Promise((res) => { waiting.push(res); helper.stdin.write(`${which} ${q.spot_id} ${q.hand}\n`); });

function rawValue(q) {
  if (q.kind === 'hit') { const row = Object.fromEntries(T.keys.map((k, i) => [k, T.flop[IDX[q.hand]][i]])); return (HIT_KEYS[q.topic] || [q.topic]).reduce((s, k) => s + row[k], 0); }
  if (['random', 'hasard', 'au_hasard'].includes(q.topic)) return T.equity_random[IDX[q.hand]];
  return T.ranges.find((r) => r.id === q.topic).equity[IDX[q.hand]];
}
function bounds(label) {
  const n = (label.match(/\d+(?:,\d+)?/g) || []).map((x) => Math.round(100 * Number(x.replace(',', '.'))));
  if (label.startsWith('moins')) return [0, n[0]]; if (/ou plus/.test(label)) return [n[0], 10001]; return [n[0], n[1]];
}
const fmt = (x) => `${x.toFixed(1).replace(/\.0$/, '').replace('.', ',')} %`;
const pctFr = (bp) => fmt(Math.round(bp / 10) / 10);
const pctAll = (bp) => [...new Set([pctFr(bp), fmt(Math.floor(bp / 10) / 10)])].filter((x, _, a) => bp % 10 === 5 || x === a[0]);   // à 5 près : les deux arrondis (observation)
const showsValue = (text, bp) => pctAll(bp).some((x) => text.includes(x));
function truth(q) {                                                   // bonne option recalculée depuis la table brute
  if (q.answer === 'statement') {
    const on = new Set(T.labels[IDX[q.hand]].map(([l]) => l)); const ids = q.statement_ids || null;
    return { kind: 'labels', on };
  }
  const v = rawValue(q); const k = q.options.findIndex((o) => { const [lo, hi] = bounds(o.label_fr); return lo <= v && v < hi; });
  return { kind: 'band', v, k };
}
const watch = (p) => p.evaluate(() => {                              // questions et corrections reçues, application ou démo
  const f = window.fetch; window.__q = null; window.__att = [];
  window.fetch = async (path, opts) => {
    const r = await f(path, opts); const u = String(path).split('?')[0];
    const tap = (fn) => { const j0 = r.json.bind(r); r.json = async () => { const j = await j0(); fn(j); return j; }; };
    if (u.endsWith('/quiz/next')) tap((j) => { if (j && j.question) window.__q = j.question; });
    if (u.endsWith('/attempts') && opts && opts.method === 'POST') tap((j) => { if (j && j.verdict) window.__att.push({ q: window.__q, a: j }); });
    return r;
  };
});
const lastQ = (p) => p.evaluate(() => window.__q); const atts = (p) => p.evaluate(() => window.__att);
const tab = async (p, t) => { await p.evaluate((x) => document.querySelector(`.tab[data-tab="${x}"]`).click(), t); await p.waitForTimeout(700); };

(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await watch(p);
  await p.click('#ob-exp button[data-v="confirme"]'); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); await p.click('#ob-next'); await p.click('#ob-next');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(600);

  // ---------------------------------------------------------------- équités : une série mêlée, réponses voulues
  await tab(p, 'gto'); await p.click('#equity-start');
  const plan = ['juste', 'voisine', 'loin', 'juste', 'loin']; const eqErr = [], uiErr = []; const expect = [];
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(200);
    const q = await lastQ(p); const tr = truth(q); let choice, want;
    const ui = await p.evaluate(() => ({ table: !!document.querySelector('#table-wrap') && getComputedStyle(document.querySelector('#table-wrap')).display !== 'none' && !document.querySelector('#table-wrap').hidden,
      timer: !document.getElementById('q-timer').hidden, skip: !document.getElementById('replay-skip').hidden, cat: document.getElementById('q-cat').textContent }));
    if (ui.table || ui.timer || ui.skip || ui.cat !== 'Équités') uiErr.push({ q: q.spot_id, ...ui });
    if (tr.kind === 'band') {
      if (tr.k < 0) { eqErr.push({ q: q.spot_id, hand: q.hand, valeur: tr.v, options: q.options.map((o) => o.label_fr), défaut: 'aucune tranche ne contient la valeur' }); choice = 0; want = null; }
      else {
        const n = q.options.length; const far = tr.k < n / 2 ? n - 1 : 0; const near = tr.k + 1 < n ? tr.k + 1 : tr.k - 1;
        choice = plan[i] === 'juste' ? tr.k : plan[i] === 'voisine' ? near : far;
        want = plan[i] === 'juste' ? 'correct' : plan[i] === 'voisine' ? 'imprécision' : (Math.abs(far - tr.k) === 1 ? 'imprécision' : 'erreur');
      }
    } else {                                                          // affirmations : « laquelle est vraie / fausse ? »
      const sts = q.options.map((o) => o.label_fr); const askFalse = /fausse/i.test(q.prompt_fr);
      // l'identifiant porte les quatre étiquettes dans l'ordre : eq:labels:<vraie|fausse>:L<n>:a.b.c.d
      const ids = (q.spot_id.split(':')[4] || '').split('.'); const good = ids.findIndex((l) => tr.on.has(l) !== askFalse);
      choice = plan[i] === 'juste' ? good : (good + 1) % sts.length; want = plan[i] === 'juste' ? 'correct' : 'erreur';
      if (ids.length !== 4 || good < 0 || ids.filter((l) => tr.on.has(l) !== askFalse).length !== 1) eqErr.push({ q: q.spot_id, hand: q.hand, défaut: 'pas exactement une bonne affirmation selon la table' });
    }
    await p.click(`#actions button >> nth=${choice}`); await p.waitForSelector('#screen-answer:not([hidden])');
    const a = (await atts(p)).slice(-1)[0].a; const shown = await p.innerText('#screen-answer');
    if (want && a.verdict !== want) eqErr.push({ q: q.spot_id, hand: q.hand, réponse: plan[i], attendu: want, servi: a.verdict });
    if (tr.kind === 'band' && !showsValue(shown, tr.v)) eqErr.push({ q: q.spot_id, hand: q.hand, valeur_attendue: pctFr(tr.v), écran: shown.slice(0, 300) });
    if (/BB perdu/i.test(shown)) uiErr.push({ q: q.spot_id, bb: true });           // « BB » seul peut venir d'une range (« le BB paie »)
    expect.push({ q, tr, verdict: a.verdict, points: a.points });
    await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])', { timeout: 15000 });
  const sum = await p.innerText('#screen-summary');
  const missing = expect.filter((x) => x.verdict !== 'correct' && x.tr.kind === 'band' && !showsValue(sum, x.tr.v));
  ok('équités : verdicts conformes à la table brute (juste, voisine, loin)', !eqErr.length, eqErr);
  ok('équités : question sans table, sans chrono, sans rejouée, étiquette « Équités », jamais de BB', !uiErr.length, uiErr);
  ok('équités : le bilan donne la valeur exacte de chaque erreur, sans BB ni révision', !missing.length && !/BB perdu/i.test(sum) && !/révision/i.test(sum) && (await p.textContent('#s-cat')) === 'Équités', { manquent: missing.map((x) => pctFr(x.tr.v)), bilan: sum.slice(0, 400) });
  await p.screenshot({ path: `${OUT}/ui_equity_summary.png`, fullPage: true });
  await p.click('#back-home'); await p.waitForTimeout(800);

  // une seule sorte
  await tab(p, 'gto'); const before = (await atts(p)).length; await p.click('#equity-kinds [data-kind="hit"]');
  for (let i = 0; i < 5; i++) { await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(150); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(800);
  const one = (await atts(p)).slice(before).map((x) => x.q.kind);
  ok('équités : « Toucher le flop » seulement, 5 questions', one.length === 5 && one.every((k) => k === 'hit'), one);

  // ---------------------------------------------------------------- une série GTO avec des imprécisions, une série exploitante
  await tab(p, 'gto'); await p.click('#quick-start');
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(150);
    if (i === 0) ok('question GTO : étiquette « Préflop GTO »', (await p.textContent('#q-cat')) === CAT_FR.gto, await p.textContent('#q-cat'));
    const c = await pick(i % 2 ? 'imprecise' : 'best', await lastQ(p));
    await p.click(`#actions button[data-id="${c.action_id}"]`); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])'); ok('bilan GTO : étiquette « Préflop GTO »', (await p.textContent('#s-cat')) === CAT_FR.gto); await p.click('#back-home'); await p.waitForTimeout(800);
  await tab(p, 'expl'); await p.click('#expl-quick, #screen-expl .primary.big, #screen-expl button.primary').catch(() => {});
  let exploitDone = 0;
  for (let i = 0; i < 5; i++) {
    if (!(await p.waitForSelector('#screen-question:not([hidden])', { timeout: 8000 }).catch(() => null))) break;
    await p.waitForTimeout(150); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); exploitDone += 1;
  }
  if (exploitDone) { await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(800); }

  // ---------------------------------------------------------------- chiffres attendus, d'après les réponses jouées
  const all = await atts(p); const tally = {};
  for (const { q, a } of all) {
    const cat = q.mode === 'equity' ? 'equites' : q.field && q.field.ask_fr ? 'profils' : q.mode === 'exploit' ? 'exploit' : 'gto';
    const t = tally[cat] = tally[cat] || { q: 0, pts: 0, correct: 0 }; t.q += 1; t.pts += a.points; t.correct += a.verdict === 'correct' ? 1 : 0;
  }
  await tab(p, 'prog'); await p.waitForSelector('#st-cats:not([hidden])', { timeout: 15000 });
  const rows = await p.$$eval('#st-cats-list .cat-row', (xs) => xs.map((x) => [x.dataset.cat, x.innerText.replace(/\s+/g, ' ').trim()]));
  ok('Progression : tableau « Par catégorie » à cinq lignes', JSON.stringify(rows.map((r) => r[0])) === JSON.stringify(['gto', 'exploit', 'profils', 'ranges', 'equites']), rows);
  const numErr = [];
  for (const [cat, t] of Object.entries(tally)) {
    const row = (rows.find((r) => r[0] === cat) || [, ''])[1]; const pct = Math.round(100 * t.pts / t.q);
    if (!row.includes(`${pct} %`) || !new RegExp(`\\b${t.q} (décision|question|lecture)`).test(row) && !(cat === 'profils' && row.includes(`sur ${t.q}`))) numErr.push({ cat, attendu: `${pct} % · ${t.q}`, ligne: row });
  }
  ok('Progression : pourcentage et nombre de chaque ligne = décompte des réponses jouées', !numErr.length, { numErr, tally });
  const g = tally.gto; const wording = rows.find((r) => r[0] === 'gto');
  if (g && g.pts !== g.correct) console.error(`observation : Préflop GTO affiche ${Math.round(100 * g.pts / g.q)} % (points, imprécision = 1/2) sous le libellé « de bonnes réponses » ; bonnes réponses : ${Math.round(100 * g.correct / g.q)} %. Ligne : ${wording && wording[1]}`);
  await tab(p, 'gto');
  const meters = await p.evaluate(() => Object.fromEntries(['gto', 'ranges', 'equites', 'exploit', 'profils'].map((k) => [k, (document.getElementById(`cat-${k}-meter`) || {}).textContent || null])));
  ok('cartes de catégorie : même chiffre que le tableau de Progression', ['gto', 'equites', 'exploit'].every((k) => !tally[k] || (rows.find((r) => r[0] === k) || [, ''])[1].includes(meters[k])), { meters, rows });
  // cartes de défi de la semaine : leur catégorie
  await tab(p, 'defis'); if (await p.isVisible('#ch-box summary') && !(await p.$eval('#ch-box', (d) => d.open))) await p.click('#ch-box summary');
  const cards = await p.$$eval('#ch-list li', (xs) => xs.map((x) => x.innerText.replace(/\s+/g, ' ')));
  const want = { 'Sous pression': CAT_FR.gto, 'Série parfaite': CAT_FR.exploit, 'Lecteur de vilain': CAT_FR.profils, 'Range au cordeau': CAT_FR.ranges, 'Défi du jour': CAT_FR.gto };
  const badCards = Object.entries(want).filter(([t, c]) => { const li = cards.find((x) => x.includes(t)); return li && !li.toLowerCase().includes(c.toLowerCase()); });   // écrit en capitales à l'écran
  ok('cartes de défi : chacune porte sa catégorie', !badCards.length, { badCards, cards: cards.map((c) => c.slice(0, 90)) });
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  helper.stdin.end(); await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Recette des questions d'équités (CE3, 10/11) dans la démo autonome ou l'application, en complément de tests/test_equites_recette.py
// (serveur) et de e2e_equity_demo.cjs : les séries passent par le fetch de la page (moteur local de la démo, ou serveur), et chaque
// réponse est comparée à la table brute spinsacademy/data/equites.json lue ici, sans le code du module :
//   valeur exacte, bonne tranche qui la contient à 1,5 point au moins de chaque frontière, notation des tranches voisines ;
//   affirmations vraies si et seulement si la main porte l'étiquette ; jamais de règle à deux rangs sur une paire (affirmations,
//   forces, faiblesses) ; aucune question d'équités dans une série GTO ou exploitante ; bloc « equity » séparé des statistiques ;
//   aucun nom d'expert, aucun « BB perdus ».
// Usage : BASE_URL=file:///…/demo.html node tools/web/e2e_equites_recette.cjs      (ou BASE_URL=http://localhost:8000/)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/';
const T = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'spinsacademy', 'data', 'equites.json'), 'utf8'));
const IDX = Object.fromEntries(T.hands.map((h, i) => [h, i]));
const HIT_KEYS = { suite: ['suite', 'quinte_flush'], couleur: ['couleur', 'quinte_flush'] };
const PAIR_UNCLEAR = ['cartes_hautes', 'depareillee', 'top_paire_souvent', 'top_paire_rarement', 'paire_faible'];
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const isPair = (h) => h.length === 2;
function rawValue(kind, topic, hand) {
  if (kind === 'hit') { const row = Object.fromEntries(T.keys.map((k, i) => [k, T.flop[IDX[hand]][i]])); return (HIT_KEYS[topic] || [topic]).reduce((s, k) => s + row[k], 0); }
  if (['random', 'hasard', 'au_hasard'].includes(topic)) return T.equity_random[IDX[hand]];
  return T.ranges.find((r) => r.id === topic).equity[IDX[hand]];
}
function bounds(label) {
  const n = (label.match(/\d+(?:,\d+)?/g) || []).map((x) => Math.round(100 * Number(x.replace(',', '.'))));
  if (label.startsWith('moins')) return [0, n[0]]; if (/ou plus/.test(label)) return [n[0], 10001]; return [n[0], n[1]];
}
const call = (p, route, body) => p.evaluate(async ([r, b]) => {
  const opts = { method: b ? 'POST' : 'GET', headers: { 'content-type': 'application/json', 'X-Player-Id': localStorage.getItem('player_id') || 'eq-recette-demo-01' } };
  if (b) opts.body = JSON.stringify(b);
  const res = await window.fetch('/' + r, opts); return { status: res.status, json: await res.json() };
}, [route, body]);

(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage();
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForTimeout(800);
  const bandErr = []; const labErr = []; const texts = []; let nBand = 0, nLab = 0, pairs = 0;
  for (const kind of ['hit', 'equity', 'labels']) {
    for (let seed = 0; seed < 8; seed++) {
      const s = await call(p, 'sessions', { mode: 'equity', size: 5, seed, filters: { kind } });
      if (s.status !== 201) { bandErr.push({ kind, seed, status: s.status, json: s.json }); continue; }
      for (let i = 0; i < 5; i++) {
        const q = (await call(p, `quiz/next?session_id=${s.json.session_id}`)).json.question;
        const a = (await call(p, 'attempts', { session_id: s.json.session_id, question_index: i, action_id: q.options[0].id })).json;
        texts.push(JSON.stringify([q, a]));
        if (kind !== 'labels') {
          nBand += 1; const e = a.equity; const v = rawValue(kind, q.topic, q.hand); const ids = q.options.map((o) => o.id); const k = ids.indexOf(e.correct_option);
          const [lo, hi] = bounds(q.options[k].label_fr); const d = Math.abs(0 - k);
          if (e.value_bp !== v || !(lo <= v && v < hi) || (lo && v - lo < 150) || (hi !== 10001 && hi - v < 150)) bandErr.push({ spot: q.spot_id, hand: q.hand, table: v, servi: e.value_bp, tranche: q.options[k].label_fr });
          if (a.verdict !== (d === 0 ? 'correct' : d === 1 ? 'imprécision' : 'erreur')) bandErr.push({ spot: q.spot_id, verdict: a.verdict, écart: d });
        } else {
          nLab += 1; const on = Object.fromEntries(T.labels[IDX[q.hand]]);
          for (const st of a.equity.statements) {
            if (st.true !== (st.label_id in on)) labErr.push({ hand: q.hand, label: st.label_id, servi: st.true, table: st.label_id in on });
            if (isPair(q.hand) && PAIR_UNCLEAR.includes(st.label_id)) labErr.push({ hand: q.hand, label: st.label_id, paire: true });
          }
        }
        if (isPair(q.hand)) { pairs += 1; const t = [...(a.strengths_fr || []), ...(a.weaknesses_fr || [])].join(' '); if (/top paire|cartes hautes|dépareillée|paire faible/i.test(t)) labErr.push({ hand: q.hand, forces: t }); }
      }
    }
  }
  ok(`tranches = table brute, marge de 1,5 point, notation des voisines (${nBand} questions)`, nBand >= 70 && !bandErr.length, bandErr.slice(0, 6));
  ok(`affirmations = étiquettes de la table, rien de flou sur les paires (${nLab} questions, ${pairs} paires)`, nLab >= 35 && !labErr.length, labErr.slice(0, 6));
  // séparation : séries GTO et exploitantes sans équités, statistiques à part
  const mixed = [];
  for (const mode of ['gto', 'exploit']) for (let seed = 0; seed < 4; seed++) {
    const s = await call(p, 'sessions', { mode, seed }); if (s.status !== 201) continue;
    for (let i = 0; i < s.json.size; i++) { const q = (await call(p, `quiz/next?session_id=${s.json.session_id}`)).json.question; if (q && (String(q.spot_id).startsWith('eq:') || q.mode === 'equity')) mixed.push([mode, q.spot_id]); }
  }
  ok('aucune question d\'équités dans une série GTO ou exploitante', !mixed.length, mixed);
  const st = (await call(p, 'users/me/stats')).json;
  ok('statistiques : bloc « equity » séparé, hors score GTO / exploitant', st.equity && st.equity.questions === nBand + nLab && (st.questions || 0) === 0, { equity: st.equity && st.equity.questions, gto_exploit: st.questions });
  const blob = texts.join('\n');
  ok('aucun nom d\'expert, aucun « BB perdus »', !/lucho|lucky|pasg8|\bPA\b|coach/i.test(blob) && !/BB perdu/i.test(blob));
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

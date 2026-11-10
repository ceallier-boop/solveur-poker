// Recette indépendante des fiches à emporter (rythme N3), en complément de e2e_rythme.cjs (Interface), sur l'application ou la démo :
//   tous les réglages (table × tapis × position) : la liste affichée = les fiches du réglage, toutes atteignables ;
//   grilles relues case par case dans le SVG affiché et comparées à la banque du solveur elle-même (e2e_audit_helper.py fiche),
//   pas à fiches.json : part de chaque famille d'action à 2 points près, mains jamais atteintes grisées ;
//   « Fiable » / « Approximation » et la note d'écart ; avis des experts sans nom ; légende en mots français au niveau 1 ;
//   impression : la fiche seule, sur une page ; réglage gardé après rechargement.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_fiches_recette.cjs [dossier]      (ou file://…/demo.html)
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const DATA = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', 'spinsacademy', 'data', 'fiches.json'), 'utf8'));
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const NODES = ['first_in', 'vs_limp', 'vs_raise', 'vs_allin'];
const bankOf = (ids) => JSON.parse(execFileSync(process.env.PYTHON || 'python3', [path.join(__dirname, 'e2e_audit_helper.py'), 'fiche', DATA.bank, ...ids], { encoding: 'utf8', maxBuffer: 1 << 26 }));
const home = (p) => p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
const pressed = (p, id) => p.$eval(`#${id} button[aria-pressed="true"]`, (b) => b.dataset.v).catch(() => null);
const chips = (p, id) => p.$$eval(`#${id} button`, (xs) => xs.map((b) => b.dataset.v));

function readGrid() {                                              // dans la page : part affichée de chaque famille d'action, par case
  const C = 26, svg = document.querySelector('#fi-sheet svg.fi-grid'); const out = {}; const at = {};
  const KIND = { '#f3f4f2': 'fold', '#dfe6e2': 'check', 'url(#fp-call)': 'call', 'url(#fp-raise)': 'raise', '#1f3f73': 'allin', 'url(#fp-dead)': 'dead' };
  for (const t of svg.querySelectorAll(':scope > text')) {
    const k = `${Math.floor(+t.getAttribute('y') / C)},${Math.floor(+t.getAttribute('x') / C)}`;
    out[t.textContent] = { dead: t.classList.contains('dead'), share: {} }; at[k] = out[t.textContent];
  }
  for (const r of svg.querySelectorAll(':scope > rect')) {
    const cell = at[`${Math.round(+r.getAttribute('y') / C)},${Math.floor(+r.getAttribute('x') / C + 1e-6)}`]; const kind = KIND[r.getAttribute('fill')];
    if (cell && kind !== 'dead') cell.share[kind] = (cell.share[kind] || 0) + 100 * +r.getAttribute('width') / C;
  }
  return out;
}

(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await home(p); await p.click('#fiches-btn'); await p.waitForSelector('#screen-fiches:not([hidden])', { timeout: 20000 });

  // tous les réglages : la liste affichée = les fiches du réglage, groupées par situation, avec leur fiabilité
  const seen = new Set(); const wrong = [];
  for (const table of await chips(p, 'fi-table')) {
    await p.click(`#fi-table button[data-v="${table}"]`);
    for (const stack of await chips(p, 'fi-stack')) {
      await p.click(`#fi-stack button[data-v="${stack}"]`);
      for (const hero of await chips(p, 'fi-hero')) {
        await p.click(`#fi-hero button[data-v="${hero}"]`);
        const ui = await p.$$eval('#fi-list .fi-item', (xs) => xs.map((x) => [x.dataset.id, x.querySelector('.fi-rel').textContent]));
        const want = DATA.fiches.filter((f) => f.table === table && f.stack === +stack && f.hero === hero)
          .sort((x, y) => NODES.indexOf(x.node) - NODES.indexOf(y.node) || x.order - y.order).map((f) => [f.id, f.reliability === 'tapis' ? 'Fiable' : 'Approximation']);
        if (JSON.stringify(ui) !== JSON.stringify(want)) wrong.push({ table, stack, hero, ui: ui.length, want: want.length });
        ui.forEach(([id]) => seen.add(id));
      }
    }
  }
  ok('chaque réglage liste exactement ses fiches, dans l\'ordre des situations, avec leur fiabilité', !wrong.length, wrong.slice(0, 5));
  ok(`toutes les fiches atteignables par les réglages (${DATA.fiches.length})`, seen.size === DATA.fiches.length, { vues: seen.size });

  // grilles comparées à la banque : un échantillon varié (table, situation, fiabilité) et toutes les fiches avec un avis d'experts
  const sample = []; const key = new Set();
  for (const f of DATA.fiches) { const k = `${f.table}|${f.node}|${f.reliability}`; if (!key.has(k) || (f.expert_hands || []).length) { key.add(k); sample.push(f); } }
  const bank = bankOf(sample.map((f) => f.id)); const gridErr = []; const metaErr = []; let cells = 0;
  for (const f of sample) {
    await p.click(`#fi-table button[data-v="${f.table}"]`); await p.click(`#fi-stack button[data-v="${f.stack}"]`); await p.click(`#fi-hero button[data-v="${f.hero}"]`);
    await p.click(`#fi-list .fi-item[data-id="${f.id}"]`); await p.waitForSelector('#fi-sheet:not([hidden]) svg.fi-grid');
    const ui = await p.evaluate(readGrid); const ref = bank[f.id].hands;
    for (const [h, x] of Object.entries(ref)) {
      cells += 1; const u = ui[h];
      if (!u || u.dead !== x.dead) { gridErr.push({ fiche: f.id, main: h, attendu: x.dead ? 'grisée' : 'jouée', affiché: u && u.dead ? 'grisée' : 'jouée' }); continue; }
      if (x.dead) continue;
      for (const k of new Set([...Object.keys(x.share), ...Object.keys(u.share)])) {
        if (Math.abs((x.share[k] || 0) - (u.share[k] || 0)) > 2) gridErr.push({ fiche: f.id, main: h, action: k, banque: x.share[k] || 0, affiché: +(u.share[k] || 0).toFixed(1) });
      }
    }
    const sheet = await p.innerText('#fi-sheet');
    const rel = await p.textContent('#fi-sheet .fi-head .fi-rel');
    const note = await p.$eval('#fi-sheet .fi-note', (n) => ({ quiet: n.classList.contains('quiet'), text: n.textContent }));
    const experts = await p.$$eval('#fi-sheet .fi-experts li', (xs) => xs.length);
    if (rel !== (f.reliability === 'tapis' ? 'Fiable' : 'Approximation')) metaErr.push({ fiche: f.id, fiabilité: rel });
    if (f.reliability === 'flop' && (note.quiet || !/écart/i.test(note.text))) metaErr.push({ fiche: f.id, note: note.text });
    if (experts !== (f.expert_hands || []).length) metaErr.push({ fiche: f.id, experts, attendu: (f.expert_hands || []).length });
    if (/lucho|lucky|\bPA\b|pasg8|coach/i.test(sheet)) metaErr.push({ fiche: f.id, nom: true });
    if (!/Se coucher|Parole|Payer|Relancer|Tapis/.test(await p.innerText('#fi-sheet .fi-legend'))) metaErr.push({ fiche: f.id, légende: await p.innerText('#fi-sheet .fi-legend') });
    await p.click('#fi-back'); await p.waitForSelector('#fi-pick:not([hidden])');
  }
  ok(`grilles affichées = banque ${DATA.bank} (${sample.length} fiches, ${cells} cases)`, !gridErr.length, gridErr.slice(0, 8));
  ok('fiabilité, note d\'écart, avis des experts sans nom, légende en mots français', !metaErr.length, metaErr.slice(0, 8));

  // impression : la fiche seule, sur une page
  const f0 = sample.find((f) => f.reliability === 'flop' && (f.expert_hands || []).length) || sample[0];
  await p.click(`#fi-table button[data-v="${f0.table}"]`); await p.click(`#fi-stack button[data-v="${f0.stack}"]`); await p.click(`#fi-hero button[data-v="${f0.hero}"]`);
  await p.click(`#fi-list .fi-item[data-id="${f0.id}"]`); await p.waitForSelector('#fi-sheet:not([hidden])');
  await p.emulateMedia({ media: 'print' });
  const vis = (el) => getComputedStyle(el).visibility === 'visible' && getComputedStyle(el).display !== 'none' && !el.hidden;   // la feuille d'impression masque par visibility
  const shown = await p.evaluate((src) => { const vis = eval(src); return ['fi-sheet', 'fi-pick', 'fi-actions', 'fi-home'].map((id) => [id, vis(document.getElementById(id))])
    .concat([['barre', vis(document.querySelector('header.bar'))]]); }, vis.toString());
  const pdf = await p.pdf({ format: 'A4', printBackground: true }); const pages = (pdf.toString('latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  fs.writeFileSync(path.join(OUT, 'fiche_impression.pdf'), pdf);
  ok('impression : la fiche seule, sans réglages ni boutons ni barre', JSON.stringify(shown) === JSON.stringify([['fi-sheet', true], ['fi-pick', false], ['fi-actions', false], ['fi-home', false], ['barre', false]]), shown);
  ok('impression : une page A4', pages === 1, { pages, fiche: f0.id });
  await p.emulateMedia({ media: 'screen' });

  // réglage gardé sur l'appareil
  await p.click('#fi-back'); await p.click('#fi-table button[data-v="3-handed"]');
  const st = (await chips(p, 'fi-stack')).slice(-1)[0]; await p.click(`#fi-stack button[data-v="${st}"]`);
  const hr = (await chips(p, 'fi-hero')).slice(-1)[0]; await p.click(`#fi-hero button[data-v="${hr}"]`);
  await p.reload(); await home(p); await p.click('#fiches-btn'); await p.waitForSelector('#screen-fiches:not([hidden])');
  ok('réglage gardé après rechargement', await pressed(p, 'fi-table') === '3-handed' && await pressed(p, 'fi-stack') === st && await pressed(p, 'fi-hero') === hr, [await pressed(p, 'fi-table'), await pressed(p, 'fi-stack'), await pressed(p, 'fi-hero')]);

  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Test fermé (P15, 07/11) : avec la banque du solveur servie, aucune question hors de 8 à 16 BB effectifs.
// Joueur de niveau 2 sur 5 séries rapides ; niveaux 1 et 3 en plus (leur tranche ne recouvre qu'en partie la plage, ou pas du
// tout : c'est là qu'un débordement se verrait). Tapis effectifs contrôlés côté serveur (e2e_audit_helper.py).
// La banque n'est pas publiée pour ce test : le serveur jetable la sert comme version par défaut.
//   SPINSACADEMY_ALLOW_STAGING=1 SPINSACADEMY_DATASET=2026.11.07-s2 SPINSACADEMY_DB=/tmp/e2e.sqlite python -m uvicorn spinsacademy.api:app --port 8000
//   BASE_URL=http://localhost:8000/ SPINSACADEMY_DATASET=2026.11.07-s2 node tools/web/e2e_test_ferme.cjs [dossier]
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const BANK = process.env.SPINSACADEMY_DATASET; const RANGE = [8, 16];
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const depth = (ids) => JSON.parse(execFileSync(process.env.PYTHON || 'python3', [path.join(__dirname, 'e2e_audit_helper.py'), 'depth', '1', ...ids], { encoding: 'utf8' }));

async function onboard(p, exp) {
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await p.click(`#ob-exp button[data-v="${exp}"]`); await p.click('#ob-goal button[data-v="bases"]');
  await p.click('#ob-next'); await p.click('#ob-next'); await p.click('#ob-next');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(800);
}
async function quickSeries(p) {
  await p.click('#quick-start');
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0');
    await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(800);
}

(async () => {
  if (!BANK) { console.error('SPINSACADEMY_DATASET : la banque servie par le serveur de test (ex. 2026.11.07-s2) est nécessaire'); process.exit(2); }
  const b = await chromium.launch(); const errs = [];
  for (const [label, exp, level, series] of [['niveau 2', 'confirme', null, 5], ['niveau 1', 'debut', null, 2], ['niveau 3', 'confirme', 3, 2]]) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage().then(require('./nav_helper.cjs').wire);
    p.on('pageerror', (e) => errs.push(String(e))); const served = []; const versions = new Set();
    p.on('response', async (r) => {
      if (r.url().includes('/quiz/next') && r.ok()) { const q = (await r.json()).question; if (q) served.push(q.spot_id); }
      if (r.url().endsWith('/sessions') && r.request().method() === 'POST' && r.status() === 201) versions.add((await r.json()).dataset_version);
    });
    await onboard(p, exp);
    if (level) {                                                     // le joueur choisit son niveau (comme dans « Ma progression »)
      const pid = await p.evaluate(() => localStorage.getItem('player_id'));
      await fetch(new URL('users/me/level', BASE), { method: 'PUT', headers: { 'X-Player-Id': pid, 'content-type': 'application/json' }, body: JSON.stringify({ level }) });
      await p.reload(); await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
    }
    for (let k = 0; k < series; k++) await quickSeries(p);
    const stacks = depth([...new Set(served)]).spots.map((s) => s.effective_stack_bb);
    const out = stacks.filter((e) => e < RANGE[0] || e > RANGE[1]);
    ok(`${label} : banque servie ${BANK}`, [...versions].every((v) => v.endsWith(BANK)) && versions.size === 1, [...versions]);
    ok(`${label} : ${series} séries, aucune question hors de 8 à 16 BB`, served.length === 5 * series && !out.length, { questions: served.length, min: Math.min(...stacks), max: Math.max(...stacks), outside: out });
    await ctx.close();
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok), all: checks.map((c) => [c.name, c.info]) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

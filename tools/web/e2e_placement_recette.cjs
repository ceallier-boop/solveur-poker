// Recette indépendante du test de placement (audit AU7, responsable des tests), en complément de e2e_placement.cjs (Interface),
// avec des réponses choisies côté serveur (meilleure ou pire option) et des contrôles par l'API :
//   proposé au premier lancement à un joueur confirmé ou « je joue beaucoup », jamais à un débutant ;
//   meilleures réponses → le niveau le plus haut que la banque permet (3 ; 2 sur la banque du test fermé 8-16 BB, dont la tranche
//   17-25 BB est annoncée à 0), rien d'appliqué avant le choix du joueur, niveau enregistré par le serveur après ;
//   les 10 réponses hors de /users/me/stats, aussi quand le joueur a d'autres séries ;
//   abandon après 3 mains depuis « Ma progression », reprise de la même série (pas de nouvelle série), pires réponses → niveau 1.
// Serveur de test (base jetable) puis :
//   BASE_URL=http://localhost:8000/ node tools/web/e2e_placement_recette.cjs [dossier]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });

// utilitaire côté serveur, chargé une fois : « best|worst spot main » → option à jouer
const helper = spawn(process.env.PYTHON || 'python3', [path.join(__dirname, 'e2e_audit_helper.py'), 'picks'], { stdio: ['pipe', 'pipe', 'inherit'] });
const lines = readline.createInterface({ input: helper.stdout }); const waiting = [];
lines.on('line', (l) => waiting.shift()(JSON.parse(l)));
const pick = (which, q) => new Promise((res) => { waiting.push(res); helper.stdin.write(`${which} ${q.spot_id} ${q.hand}\n`); });

const api = (p, route) => p.evaluate(async (r) => {                // par le fetch de la page : le serveur, ou le moteur local de la démo
  const res = await window.fetch('/' + r, { headers: { 'X-Player-Id': localStorage.getItem('player_id') } }); return res.json();
}, route);
const watch = (p) => p.evaluate(() => {                              // dernière question, série en cours, séries créées (application et démo)
  const f = window.fetch; window.__saSessions = 0;
  window.fetch = async (path, opts) => {
    const r = await f(path, opts); const u = String(path);
    if (u.includes('/quiz/next')) { const sid = new URL(u, location.href).searchParams.get('session_id'); const j0 = r.json.bind(r);
      r.json = async () => { const j = await j0(); if (j && j.question) { window.__lastQ = j.question; window.__lastSid = sid; } return j; }; }
    if (/\/sessions$/.test(u.split('?')[0]) && opts && opts.method === 'POST') window.__saSessions += 1;   // toute demande de nouvelle série
    return r;
  };
});
const lastQ = (p) => p.evaluate(() => window.__lastQ); const lastSid = (p) => p.evaluate(() => window.__lastSid);
const sessionsCreated = (p) => p.evaluate(() => window.__saSessions);
async function toStep3(p, exp) {
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await watch(p);
  await p.click(`#ob-exp button[data-v="${exp}"]`); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); await p.click('#ob-next');
}
async function play(p, which, n) {                                  // n mains, l'option choisie par le serveur ; renvoie les verdicts
  const verdicts = [];
  for (let i = 0; i < n; i++) {
    await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(150);
    const choice = await pick(which, await lastQ(p)); verdicts.push(choice.verdict);
    await p.click(`#actions button[data-id="${choice.action_id}"]`); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  return verdicts;
}

(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e)));
    return p;
  };

  // proposition au premier lancement
  for (const [exp, shown] of [['debut', false], ['confirme', true], ['gros_volume', true]]) {
    const p = await page(); await toStep3(p, exp);
    ok(`premier lancement « ${exp} » : test ${shown ? 'proposé' : 'non proposé'}`, (await p.isVisible('#ob-placement')) === shown);
    await p.context().close();
  }

  // confirmé, meilleures réponses : le niveau le plus haut que la banque permet, appliqué seulement par le choix du joueur
  let p = await page(); await toStep3(p, 'confirme'); await p.click('#ob-placement');
  const best = await play(p, 'best', 10);
  await p.waitForSelector('#screen-placement:not([hidden])', { timeout: 15000 });
  const res = await api(p, `users/me/placement?session_id=${await lastSid(p)}`);
  const empty = res.bands.filter((x) => x.expected === 0).map((x) => x.level);       // banque étroite : tranche non servie, annoncée à 0
  const top = empty.length ? Math.min(...empty) - 1 : 3;
  ok('meilleures réponses : 10 réponses justes', best.every((v) => v === 'correct'), best);
  ok(`résultat du serveur : complet, 10 mains${empty.length ? `, tranche ${empty} à 0` : ' en 4 / 3 / 3'}, niveau ${top} proposé`,
    res.complete && res.bands.reduce((n, x) => n + x.questions, 0) === 10 && empty.every((lv) => res.bands[lv - 1].questions === 0)
    && (empty.length || res.bands.map((x) => x.questions).join() === '4,3,3') && res.proposed_level === top, res);
  const rows = await p.$$eval('#pl-bands tr', (xs) => xs.map((x) => x.innerText.replace(/\s+/g, ' ').trim()));
  const shownBands = res.bands.filter((x) => x.expected > 0 || x.questions > 0);   // retest 10 (point 3) : une tranche à 0 question n'est pas montrée
  ok('écran : une ligne par tranche servie, points sur les mains posées', rows.length === shownBands.length
    && shownBands.every((x, i) => rows[i].endsWith(` sur ${Math.max(x.questions, x.expected)}`)), rows);
  const over = rows.filter((t) => { const m = t.match(/([\d,]+) sur (\d+)/); return m && Number(m[1].replace(',', '.')) > Number(m[2]); });
  ok('écran : jamais plus de points que de mains dans une tranche (« 6 sur 3 » interdit)', !over.length, rows);
  ok(`écran : « Niveau ${top} »`, new RegExp(`Niveau ${top}`).test(await p.textContent('#pl-level')), await p.textContent('#pl-level'));
  ok('rien d\'appliqué avant le choix du joueur', (await api(p, 'users/me/level')).level === 2);
  if (top > 2) {
    ok('« Prendre ce niveau » proposé', await p.isVisible('#pl-take'));
    await p.click('#pl-take');
  } else {                                                          // niveau proposé = niveau actuel : rien à prendre
    ok('niveau proposé = niveau actuel : pas de « Prendre ce niveau », on continue', !(await p.isVisible('#pl-take')) && await p.isVisible('#pl-keep'), await p.textContent('#pl-keep'));
    await p.click('#pl-keep');
  }
  await p.waitForSelector('#screen-home:not([hidden])', { timeout: 15000 }); await p.waitForTimeout(1000);
  ok(`niveau ${top} enregistré par le serveur`, (await api(p, 'users/me/level')).level === top);
  ok(`accueil au niveau ${top}`, new RegExp(`Niveau ${top}`).test(await p.innerText('#today-level')), await p.innerText('#today-level'));
  ok('les 10 réponses du test hors de /users/me/stats', (await api(p, 'users/me/stats')).questions === 0);

  // une vraie série, puis le test depuis « Ma progression » : abandon après 3 mains, reprise, pires réponses
  await p.click('#quick-start'); await play(p, 'best', 5); await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(800);
  ok('une vraie série compte : 5 questions dans /users/me/stats', (await api(p, 'users/me/stats')).questions === 5);
  await p.click('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.click('#st-placement');
  await play(p, 'worst', 3); const sid = await lastSid(p); const before = await sessionsCreated(p);   // après l'abandon
  await p.click('#home-btn'); await p.waitForSelector('#resume:not([hidden])', { timeout: 15000 }); await p.click('#resume');
  await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(300);
  const nowSid = await lastSid(p), made = await sessionsCreated(p);
  ok('reprise : même série, aucune série créée, à la 4e main', nowSid === sid && made === before && /4 \/ 10/.test(await p.textContent('#progress')), { sid, now: nowSid, séries: made - before, progress: await p.textContent('#progress') });
  const worst = await play(p, 'worst', 7);
  await p.waitForSelector('#screen-placement:not([hidden])', { timeout: 15000 });
  const res2 = await api(p, `users/me/placement?session_id=${sid}`);
  ok('pires réponses : niveau 1 proposé sur 10 réponses', res2.complete && res2.proposed_level === 1, { proposed: res2.proposed_level, verdicts: worst });
  await p.click(await p.isVisible('#pl-take') ? '#pl-take' : '#pl-keep'); await p.waitForSelector('#screen-home:not([hidden])', { timeout: 15000 });
  ok('niveau 1 enregistré après le second test', (await api(p, 'users/me/level')).level === 1);
  ok('toujours 5 questions dans /users/me/stats après deux tests de placement', (await api(p, 'users/me/stats')).questions === 5);
  await p.screenshot({ path: `${OUT}/placement_recette_home.png`, fullPage: true });

  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  helper.stdin.end(); await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

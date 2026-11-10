// Recette indépendante du test de placement (audit AU7, responsable des tests), en complément de e2e_placement.cjs (Interface),
// avec des réponses choisies côté serveur (meilleure ou pire option) et des contrôles par l'API :
//   proposé au premier lancement à un joueur confirmé ou « je joue beaucoup », jamais à un débutant ;
//   meilleures réponses → niveau 3 proposé, rien d'appliqué avant « Prendre ce niveau », niveau 3 enregistré par le serveur après ;
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

const api = async (p, route) => {
  const pid = await p.evaluate(() => localStorage.getItem('player_id'));
  const r = await fetch(new URL(route, BASE), { headers: { 'X-Player-Id': pid } }); return r.json();
};
async function toStep3(p, exp) {
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await p.click(`#ob-exp button[data-v="${exp}"]`); await p.click('#ob-goal button[data-v="bases"]'); await p.click('#ob-next'); await p.click('#ob-next');
}
async function play(p, which, n) {                                  // n mains, l'option choisie par le serveur ; renvoie les verdicts
  const verdicts = [];
  for (let i = 0; i < n; i++) {
    await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(150);
    const choice = await pick(which, p.lastQ); verdicts.push(choice.verdict);
    await p.click(`#actions button[data-id="${choice.action_id}"]`); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn');
  }
  return verdicts;
}

(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e))); p.sessionsCreated = 0;
    p.on('response', async (r) => {
      if (r.url().includes('/quiz/next') && r.ok()) { const j = await r.json(); if (j.question) { p.lastQ = j.question; p.lastSid = new URL(r.url()).searchParams.get('session_id'); } }
      if (r.url().endsWith('/sessions') && r.request().method() === 'POST' && r.status() === 201) p.sessionsCreated += 1;
    });
    return p;
  };

  // proposition au premier lancement
  for (const [exp, shown] of [['debut', false], ['confirme', true], ['gros_volume', true]]) {
    const p = await page(); await toStep3(p, exp);
    ok(`premier lancement « ${exp} » : test ${shown ? 'proposé' : 'non proposé'}`, (await p.isVisible('#ob-placement')) === shown);
    await p.context().close();
  }

  // confirmé, meilleures réponses : niveau 3 proposé, appliqué seulement par « Prendre ce niveau »
  let p = await page(); await toStep3(p, 'confirme'); await p.click('#ob-placement');
  const best = await play(p, 'best', 10);
  await p.waitForSelector('#screen-placement:not([hidden])', { timeout: 15000 });
  const res = await api(p, `users/me/placement?session_id=${p.lastSid}`);
  ok('meilleures réponses : 10 réponses justes', best.every((v) => v === 'correct'), best);
  ok('résultat du serveur : complet, 4 / 3 / 3 mains, niveau 3 proposé', res.complete && res.bands.map((x) => x.questions).join() === '4,3,3' && res.proposed_level === 3, res);
  ok('écran : « Niveau 3 » et « Prendre ce niveau »', /Niveau 3/.test(await p.textContent('#pl-level')) && await p.isVisible('#pl-take'), await p.textContent('#pl-level'));
  ok('rien d\'appliqué avant le choix du joueur', (await api(p, 'users/me/level')).level === 2);
  await p.click('#pl-take'); await p.waitForSelector('#screen-home:not([hidden])', { timeout: 15000 }); await p.waitForTimeout(1000);
  ok('« Prendre ce niveau » : niveau 3 enregistré par le serveur', (await api(p, 'users/me/level')).level === 3);
  ok('« Prendre ce niveau » : accueil au niveau 3', /Niveau 3/.test(await p.innerText('#today-level')), await p.innerText('#today-level'));
  ok('les 10 réponses du test hors de /users/me/stats', (await api(p, 'users/me/stats')).questions === 0);

  // une vraie série, puis le test depuis « Ma progression » : abandon après 3 mains, reprise, pires réponses
  await p.click('#quick-start'); await play(p, 'best', 5); await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(800);
  ok('une vraie série compte : 5 questions dans /users/me/stats', (await api(p, 'users/me/stats')).questions === 5);
  await p.click('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.click('#st-placement');
  const before = p.sessionsCreated; await play(p, 'worst', 3); const sid = p.lastSid;
  await p.click('#home-btn'); await p.waitForSelector('#resume:not([hidden])', { timeout: 15000 }); await p.click('#resume');
  await p.waitForSelector('#screen-question:not([hidden])'); await p.waitForTimeout(300);
  ok('reprise : même série, à la 4e main', p.lastSid === sid && p.sessionsCreated === before + 1 && /4 \/ 10/.test(await p.textContent('#progress')), { sid, now: p.lastSid, progress: await p.textContent('#progress') });
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

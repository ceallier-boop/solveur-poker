// Recette indépendante de l'audit du 06/11 (responsable des tests), en complément de e2e_audit.cjs (Interface) :
//   AU3 série rapide au niveau 1 : chaque spot servi reste sous 10 BB effectifs (contrôlé côté serveur) ;
//   AU8 niveau 1 : « équité » hors de la phrase principale ; contre-épreuve : un joueur confirmé (niveau 2) garde les termes habituels ;
//   AU4 seconde moitié : objectifs et défis dépliés dès 3 jours d'entraînement ;
//   AU5 de bout en bout : historique réel en base → GET /users/me/wins → accueil et « Ma progression » (sans réponse simulée).
// Serveur de test sur une base jetable, le même chemin dans SPINSACADEMY_DB pour le serveur et pour ce script :
//   SPINSACADEMY_ALLOW_STAGING=1 SPINSACADEMY_DB=/tmp/e2e.sqlite python -m uvicorn spinsacademy.api:app --port 8000
//   BASE_URL=http://localhost:8000/ SPINSACADEMY_DB=/tmp/e2e.sqlite node tools/web/e2e_audit_recette.cjs [dossier]
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const HELPER = path.join(__dirname, 'e2e_audit_helper.py');
const helper = (...args) => JSON.parse(execFileSync(process.env.PYTHON || 'python3', [HELPER, ...args], { encoding: 'utf8' }));
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const pressed = (p) => p.getAttribute('.mode-switch [data-value="exploit"]', 'aria-pressed');

async function onboard(p, exp, goal) {
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  await p.click(`#ob-exp button[data-v="${exp}"]`); await p.click(`#ob-goal button[data-v="${goal}"]`);
  await p.click('#ob-next'); await p.click('#ob-next'); await p.click('#ob-next');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 }); await p.waitForTimeout(800);
}

async function quickSeries(p, served, onAnswer) {                 // une série rapide, premier bouton à chaque question
  await p.click('#quick-start');
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])');
    if (onAnswer) await onAnswer('question', i);
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    if (onAnswer) await onAnswer('answer', i);
    await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])'); await p.click('#back-home'); await p.waitForTimeout(1000);
}

(async () => {
  if (!process.env.SPINSACADEMY_DB) { console.error('SPINSACADEMY_DB : le chemin de la base du serveur de test est nécessaire (AU4, AU5)'); process.exit(2); }
  const b = await chromium.launch(); const errs = [];
  const page = async () => {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e)));
    p.on('response', async (r) => { if (r.url().includes('/quiz/next') && r.ok()) { const q = (await r.json()).question; if (q) p.served.push(q.spot_id); } });
    p.served = []; return p;
  };

  // AU3 et AU8 : débutant (niveau 1), deux séries rapides
  let p = await page(); await onboard(p, 'debut', 'bases');
  const essentials = []; const buttons = [];
  const look = async (where) => {
    if (where === 'question') buttons.push(...await p.$$eval('#actions button', (xs) => xs.map((x) => x.innerText.replace(/\n+/g, ' | '))));
    else essentials.push(await p.innerText('#a-essential'));
  };
  await quickSeries(p, p.served, look); await quickSeries(p, p.served, look);
  const d = helper('depth', '1', ...new Set(p.served));
  const out = d.spots.filter((s) => !s.in_band);
  ok('AU3 : série rapide au niveau 1, tous les spots sous 10 BB effectifs', d.spots.length >= 8 && !out.length, { served: d.spots.length, outside: out });
  ok('AU8 : « équité » hors de la phrase principale au niveau 1', essentials.length === 10 && essentials.every((t) => !/équité/i.test(t)), essentials.filter((t) => /équité/i.test(t)));
  ok('AU8 : boutons en français, terme anglais dessous', buttons.every((t) => /^(Se coucher|Parole|Payer|Relancer à|Tapis)/.test(t)), [...new Set(buttons)].slice(0, 6));
  await p.context().close();

  // AU8, contre-épreuve : joueur confirmé (niveau 2), termes habituels sur les boutons
  p = await page(); await onboard(p, 'confirme', 'bases');
  await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  const b2 = await p.$$eval('#actions button', (xs) => xs.map((x) => x.innerText.replace(/\n+/g, ' | ')));
  ok('AU8 contre-épreuve : au niveau 2, libellés habituels', b2.every((t) => /^(FOLD|CHECK|CALL|RAISE TO|ALL-IN|\d)/.test(t) || /(FOLD|CHECK|CALL|RAISE TO|ALL-IN)/.test(t.split(' | ')[0])), b2);
  await p.context().close();

  // AU4 seconde moitié et AU5 de bout en bout : historique réel de 4 jours (progrès net), puis rechargement
  p = await page(); await onboard(p, 'debut', 'bases');
  ok('AU4 : nouveau joueur, objectifs et défis repliés', (await p.getAttribute('#extras', 'open')) === null);
  const pid = await p.evaluate(() => localStorage.getItem('player_id'));
  helper('seed', pid);
  await p.reload(); await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
  await p.click('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.waitForTimeout(1500);   // met à jour les statistiques gardées
  const sw = await p.isVisible('#st-wins') ? await p.innerText('#st-wins') : '';
  ok('AU5 de bout en bout : « Ma progression » montre les BB récupérés calculés par le serveur', /récupérés/.test(sw) && /120 décisions|60 décisions/.test(sw), sw);
  ok('AU5 : aucun chiffre négatif affiché', !/[-−–]\s?\d/.test(sw), sw);
  await p.click('#st-back'); await p.waitForSelector('#screen-home:not([hidden])'); await p.waitForTimeout(1500);
  const hw = await p.$$eval('#home-wins li', (xs) => xs.map((x) => x.textContent));
  ok('AU5 de bout en bout : gain affiché sur l\'accueil (deux au plus)', hw.length >= 1 && hw.length <= 2 && hw.some((t) => /récupérés/.test(t)), hw);
  ok('AU4 : après 3 jours d\'entraînement, objectifs et défis dépliés', (await p.getAttribute('#extras', 'open')) !== null, await p.innerText('#extras-sum'));
  await p.screenshot({ path: `${OUT}/recette_home_seeded.png`, fullPage: true });
  await p.context().close();

  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

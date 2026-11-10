// Chantiers de l'audit du 06/11 côté interface (AU1, AU2, AU4, AU5, AU6, AU8), avec assertions.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_audit.cjs [dossier]      (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const ready = (p) => p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
const homeReady = (p) => p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });
async function onboard(p, goal) {                                    // premier lancement : expérience « moins de 3 mois », but choisi, niveau proposé
  await p.goto(BASE); await ready(p);
  await p.click('#ob-exp button[data-v="debut"]'); await p.click(`#ob-goal button[data-v="${goal}"]`);
  await p.click('#ob-next'); await p.click('#ob-next'); await p.click('#ob-next'); await homeReady(p); await p.waitForTimeout(800);
}
const pressed = (p) => p.getAttribute('.mode-switch [data-value="exploit"]', 'aria-pressed');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async () => { const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true }); const p = await ctx.newPage().then(require('./nav_helper.cjs').wire); p.on('pageerror', (e) => errs.push(String(e))); return p; };

  // AU1 : récréatifs → l'onglet central met l'onglet Exploitant en avant (I9 : l'application s'ouvre toujours au même endroit)
  let p = await page(); await onboard(p, 'recreatifs');
  ok('AU1 récréatifs : carte de l\'onglet Exploitant sur l\'onglet central', /récréatifs/.test(await p.innerText('#goal-card')) && await p.isVisible('#goal-go'), await p.innerText('#goal-card'));
  await p.click('#goal-go'); await p.waitForTimeout(800);
  ok('AU1 récréatifs : la carte ouvre l\'onglet Exploitant', await pressed(p) === 'true' && await p.isVisible('#screen-expl'));
  await p.context().close();
  // AU1 : ranges → « Construis ta range » mis en avant ; bases → rien de plus, mode GTO
  p = await page(); await onboard(p, 'ranges');
  ok('AU1 ranges : mode GTO, carte « Construis ta range »', await pressed(p) === 'false' && /affûter tes ranges/.test(await p.innerText('#goal-card')));
  await p.click('#goal-go'); await p.waitForSelector('#screen-range:not([hidden])', { timeout: 10000 });
  ok('AU1 ranges : la carte ouvre l\'exercice', true);
  await p.context().close();
  p = await page(); await onboard(p, 'bases');
  ok('AU1 bases : mode GTO, pas de carte', await pressed(p) === 'false' && !(await p.isVisible('#goal-card')));

  // AU4 : accueil d'un nouveau joueur
  const primaries = await p.$$eval('#screen-home .primary', (xs) => xs.filter((x) => x.checkVisibility()).map((x) => x.textContent.trim()));   // un bouton dans un bloc replié ne compte pas
  ok('AU4 : un seul bouton principal', primaries.length === 1 && /séance/.test(primaries[0]), primaries);
  const todayExplained = await p.isVisible('#today-explain'); await p.openTab('gto');                    // I9 : la série rapide est dans l'onglet GTO
  ok('AU4 : séance et série rapide expliquées', todayExplained && await p.isVisible('#quick-explain'));
  await p.openTab('prog');                                                                              // I9 : les objectifs sont dans l'onglet Progression
  ok('AU4 : objectifs repliés', (await p.getAttribute('#extras', 'open')) === null && await p.isVisible('#extras-sum') && !(await p.isVisible('#goals-list')));
  await p.click('#home-btn'); await homeReady(p);
  await p.screenshot({ path: `${OUT}/audit_home_new.png`, fullPage: true });

  // AU8 : vocabulaire du niveau 1 sur les boutons et dans le verdict
  await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  const btns = await p.$$eval('#actions button', (xs) => xs.map((x) => x.innerText.replace(/\n+/g, ' | ')));
  ok('AU8 : mots français, terme anglais dessous', btns.every((t) => /^(Se coucher|Parole|Payer|Relancer à|Tapis)/.test(t) && /(FOLD|CHECK|CALL|RAISE TO|ALL-IN)/.test(t)), btns);
  await p.screenshot({ path: `${OUT}/audit_question_n1.png` });
  // une série (premier coup à chaque fois), pour AU2 et AU6
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    if (i === 0) { const v = await p.innerText('#a-verdict'); ok('AU8 : verdict avec les mêmes mots', !/\b(FOLD|CALL|ALL-IN|RAISE TO|CHECK) \d/.test(v.replace(/\((FOLD|CHECK|CALL|RAISE TO|ALL-IN)\)/g, '')), v); }
    await p.click('#next-btn');
  }
  await p.waitForSelector('#screen-summary:not([hidden])');
  const sum = await p.innerText('#s-score');
  ok('AU2 bilan : un seul chiffre BB, son périmètre dit', !/pour 100 décisions/.test(sum) && (/t'a coûté .* BB par rapport aux meilleurs coups \(ses \d+ décisions\)/.test(sum) || /Aucun BB perdu/.test(sum)), sum);
  await p.click('#back-home'); await p.waitForTimeout(1200); await p.click('#stats-btn'); await p.waitForSelector('#screen-stats:not([hidden])'); await p.waitForTimeout(1500);
  const st = await p.innerText('#screen-stats');
  ok('AU2 progression : périmètre de la tuile BB', /sur toutes tes décisions \(\d+\), GTO et Exploitant/.test(st), st.slice(0, 300));
  ok('AU2 progression : pas de second chiffre BB (niveau, thèmes)', !/BB\/100/.test(st) && /pour 100 décisions à moins de 10 BB/.test(await p.innerText('#st-level')), await p.innerText('#st-level'));
  ok('AU6 : courbe dès la première série', (await p.$$('#st-evolution i')).length === 1);
  const foc = await p.innerText('#st-focus');
  ok('AU6 : un premier retour dès la première série', /Premier aperçu · provisoire|À travailler maintenant\s+\S/i.test(foc), foc);   // aperçu provisoire, ou déjà le diagnostic du serveur (3 erreurs sur un thème)
  ok('AU5 : pas de bloc « Tes progrès » sans indicateurs du serveur', !(await p.isVisible('#st-wins')) || /Tes progrès/.test(await p.innerText('#st-wins')));
  await p.screenshot({ path: `${OUT}/audit_stats_first.png`, fullPage: true });
  // AU5 (application) : réponse de GET /users/me/wins injectée, au format de Défis et rétention
  if (!BASE.startsWith('file:')) {
    const W = { mode: 'gto', as_of: '2026-11-06', wins: [
      { kind: 'level_up', from_level: 1, to_level: 2, level_name_fr: 'Le jeu à 10-16 BB', at: '2026-11-06T10:00:00+00:00', text_fr: 'Niveau 2 atteint : Le jeu à 10-16 BB.' },
      { kind: 'bb_recovered', window_days: 7, text_fr: 'Tu perds 6,5 BB de moins pour 100 décisions que la semaine passée : environ 4,5 BB récupérés sur tes 70 décisions.' },
      { kind: 'fewer_errors', window_days: 15, text_fr: '20 erreurs de moins pour 100 décisions qu\'il y a 15 jours.' },
      { kind: 'review_recovered', window_days: 7, stage_ups: 6, mastered: 2, paid_feature: true, text_fr: '6 mains ratées réussies en révision, dont 2 acquises.' }],
      effort: { window_days: 7, decisions: 70, active_days: 1, text_fr: '70 décisions sur 1 jour cette semaine.' }, not_enough: [] };
    await p.route('**/users/me/wins*', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(W) }));
    await p.click('#st-back'); await p.waitForSelector('#screen-home:not([hidden])'); await p.waitForTimeout(1200);
    ok('AU5 : passage de niveau fêté', /niveau 2 débloqué/.test(await p.innerText('#celebrate')), await p.innerText('#celebrate'));
    const hw = await p.$$eval('#home-wins li', (xs) => xs.map((x) => x.textContent));
    ok('AU5 : au plus deux gains sur l\'accueil', hw.length === 2 && /récupérés/.test(hw[0]), hw);
    await p.click('#celebrate-ok'); await p.click('#home-btn'); await p.waitForTimeout(1200);
    ok('AU5 : fêté une seule fois', !(await p.isVisible('#celebrate')));
    await p.click('#stats-btn'); await p.waitForSelector('#st-wins:not([hidden])', { timeout: 10000 });
    const sw = await p.innerText('#st-wins');
    ok('AU5 : tous les gains et l\'effort dans « Ma progression »', (sw.match(/✓/g) || []).length === 4 && /70 décisions sur 1 jour/.test(sw), sw);
    await p.screenshot({ path: `${OUT}/audit_wins.png`, fullPage: true });
    await p.unroute('**/users/me/wins*');
  }
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

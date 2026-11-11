// Rangement par catégorie (10/11, maquette retenue), avec assertions : GTO = Préflop, Ranges, Équités ; Exploitant =
// Préflop contre le field, Profils ; « Construis ta range » quitte Outils pour la carte Ranges ; étiquette de catégorie sur la question et
// le bilan ; chiffres de chaque carte et tableau « Par catégorie » dans Progression, Profils compté à part du Préflop exploitant ;
// catégorie sur les défis de la semaine, défi du jour en Préflop GTO.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_categories.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
const series = async (p, n = 5) => { for (let i = 0; i < n; i++) { await p.waitForSelector('#screen-question:not([hidden])'); await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])'); await p.click('#next-btn'); } await p.waitForSelector('#screen-summary:not([hidden])'); };
const cards = (p, tab) => p.$$eval(`#screen-${tab} .cat-card`, (xs) => xs.map((x) => x.dataset.cat));
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, reducedMotion: 'reduce' })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });

  await p.openTab('gto');
  ok('Quiz GTO : la carte Préflop', JSON.stringify(await cards(p, 'gto')) === '["gto"]', await cards(p, 'gto'));   // 11/11 : les autres formats sont dans Exercices
  await p.openTab('exos');
  ok('Exercices : Ranges, Équités, Profils', JSON.stringify(await cards(p, 'exos')) === '["ranges","equites","profils"]', await cards(p, 'exos'));
  ok('Équités : une série possible depuis sa carte', await p.isVisible('#equity-start'));
  ok('la série rapide est dans la carte Préflop', await p.evaluate(() => !!document.querySelector('#cat-gto #quick-start')));
  ok('nouveau joueur : « Pas encore commencé »', /Pas encore commencé/.test(await p.textContent('#cat-gto-meter')));
  await p.openTab('outils');
  ok('Outils : plus de « Construis ta range »', !(await p.$('#screen-outils #range-btn')) && !/Construis ta range/.test(await p.innerText('#screen-outils')));
  await p.openTab('expl');
  ok('Quiz Exploitant : la carte Préflop contre le field', JSON.stringify(await cards(p, 'expl')) === '["exploit"]', await cards(p, 'expl'));

  // une série Préflop GTO : étiquette sur la question et le bilan, puis les chiffres de la carte et de Progression
  await p.openTab('gto'); await p.click('#quick-start'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('question : étiquette Préflop GTO', (await p.textContent('#q-cat')).trim() === 'Préflop GTO');
  await series(p);
  ok('bilan : étiquette Préflop GTO', (await p.textContent('#s-cat')).trim() === 'Préflop GTO');
  await p.click('#back-home'); await p.waitForSelector('#screen-gto:not([hidden])');
  await p.waitForFunction(() => /des points · 5 décisions/.test(document.getElementById('cat-gto-meter').textContent), null, { timeout: 10000 }).catch(() => {});
  const gm = await p.textContent('#cat-gto-meter');
  ok('carte Préflop : score et décisions', /^\d+ % des points · 5 décisions/.test(gm), gm);
  await p.screenshot({ path: `${OUT}/categories_gto.png`, fullPage: true });

  // une série Profils (lecture du vilain) : étiquette Profils, comptée à part du Préflop exploitant
  await p.openTab('expl'); await p.click('#profils-start'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('Profils : une question de lecture, étiquette Profils', (await p.textContent('#q-cat')).trim() === 'Profils' && await p.isHidden('#table-wrap'));
  await series(p);
  ok('bilan : étiquette Profils', (await p.textContent('#s-cat')).trim() === 'Profils');
  await p.click('#back-home'); await p.waitForSelector('#screen-exos:not([hidden])');   // Profils : retour à l'onglet Exercices
  await p.waitForFunction(() => /sur 5$/.test(document.getElementById('cat-profils-meter').textContent), null, { timeout: 10000 }).catch(() => {});
  ok('carte Profils : lectures justes sur 5', /lectures? justes? sur 5$/.test(await p.textContent('#cat-profils-meter')), await p.textContent('#cat-profils-meter'));
  ok('Préflop exploitant : la lecture n\'y compte pas', /Pas encore commencé/.test(await p.textContent('#cat-exploit-meter')), await p.textContent('#cat-exploit-meter'));
  await p.screenshot({ path: `${OUT}/categories_expl.png`, fullPage: true });

  // Progression : une ligne par catégorie
  await p.openTab('prog'); await p.waitForSelector('#st-cats:not([hidden])', { timeout: 10000 });
  const rows = await p.$$eval('#st-cats-list li', (xs) => xs.map((x) => x.dataset.cat + ':' + x.innerText.replace(/\s+/g, ' ').trim()));
  ok('Progression : cinq catégories dans l\'ordre', rows.map((r) => r.split(':')[0]).join() === 'gto,exploit,profils,ranges,equites', rows);
  ok('Progression : chiffres de Préflop GTO et Profils', /^gto:Préflop GTO .*5 décisions.* \d+ %$/.test(rows[0]) && /^profils:Profils .*sur 5 \d+ %$/.test(rows[2]), rows);
  await p.$eval('#st-cats', (x) => x.scrollIntoView()); await p.screenshot({ path: `${OUT}/categories_prog.png` });

  // défis : catégorie sur les défis de la semaine ; défi du jour en Préflop GTO
  await p.click('#home-btn'); await p.waitForSelector('#ch-list li', { timeout: 15000 });
  if (!(await p.$eval('#ch-box', (d) => d.open))) await p.click('#ch-box summary');
  const ch = await p.$$eval('#ch-list li.ch small:first-child', (xs) => xs.map((x) => x.textContent));
  ok('défi du jour : Préflop GTO', /Aujourd'hui · Préflop GTO/.test(ch[0] || ''), ch);
  ok('défis de la semaine : leur catégorie', ch.filter((t) => /^Cette semaine · (Préflop GTO|Préflop exploitant|Profils|Ranges)$/.test(t)).length >= 2, ch);
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

// Écran des questions d'équité (catégorie « Équités », onglet GTO), avec assertions : carte de catégorie active, série de 5 questions ou
// d'une seule sorte ; question sans table, la main en grand, énoncé visible, tranches en grille ou affirmations en liste, ni chrono ni
// rejouée ; correction : bonne tranche ou bonne affirmation, valeur exacte, calcul, forces et faiblesses, jamais de BB ; bilan sans BB
// ni révision, la valeur exacte sur chaque erreur ; chiffres de la carte et détail par sorte dans Progression.
// Usage : BASE_URL=http://localhost:8000/ node tools/web/e2e_equity.cjs [dossier]   (application ou file://…/demo.html)
const { chromium } = require('playwright');
const BASE = process.env.BASE_URL || 'http://localhost:8000/'; const OUT = process.argv[2] || '.';
const checks = []; const ok = (name, cond, info) => checks.push({ name, ok: !!cond, info });
(async () => {
  const b = await chromium.launch(); const errs = [];
  const p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true })).newPage().then(require('./nav_helper.cjs').wire);
  p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(BASE);
  await p.waitForFunction(() => !document.getElementById('screen-onboard').hidden || !document.getElementById('today').hidden, null, { timeout: 20000 });
  if (await p.isVisible('#screen-onboard')) await p.click('#ob-skip');
  await p.waitForSelector('#screen-home:not([hidden]) #today:not([hidden])', { timeout: 20000 });

  await p.openTab('exos');                                           // 11/11 : la carte Équités est dans l'onglet Exercices
  ok('carte Équités active : série et trois sortes', await p.isVisible('#equity-start') && (await p.$$('#equity-kinds [data-kind]')).length === 7 && !/bientôt/i.test(await p.innerText('#cat-equites')));
  ok('nouveau joueur : « Pas encore commencé »', /Pas encore commencé/.test(await p.textContent('#cat-equites-meter')));
  await p.click('#equity-start'); await p.waitForSelector('#screen-question:not([hidden])', { timeout: 15000 });
  // série par défaut (12/11) : 5 questions de sortes différentes parmi les six ; chaque question contrôlée selon sa sorte
  const KIND = { 'Toucher le flop': 'hit', 'Équité contre une range': 'equity', 'Forces et faiblesses': 'labels', 'Tirages et outs': 'outs', 'Équité sur le flop': 'board_equity', 'Ce flop t\'aide-t-il ?': 'flop_help' };
  const look = () => p.evaluate(() => ({
    kind: document.getElementById('eq-kind').textContent, cat: document.getElementById('q-cat').textContent, table: !document.getElementById('table-wrap').hidden,
    hand: !document.getElementById('eq-hand').hidden, cards: document.querySelectorAll('#eq-cards .card').length, ask: document.getElementById('ask').className,
    askText: document.getElementById('ask').textContent, bands: document.getElementById('actions').classList.contains('bands'),
    stmts: document.getElementById('actions').classList.contains('stmts'), n: document.querySelectorAll('#actions button').length,
    timer: !document.getElementById('q-timer').hidden, skip: !document.getElementById('replay-skip').hidden, opts: !document.getElementById('actions').hidden }));
  const layoutOk = (k, q) => (k === 'labels' ? q.stmts && q.n === 4 : k === 'flop_help' ? q.stmts && q.n === 3 : q.bands && q.n >= 4 && q.n <= 6);
  const readAnswer = () => p.evaluate(() => ({
    verdict: document.getElementById('a-verdict').innerText, essential: document.getElementById('a-essential').textContent,
    calc: document.getElementById('a-remember').innerText, box: !document.getElementById('a-equity').hidden, text: document.getElementById('screen-answer').innerText,
    good: document.querySelectorAll('#a-equity .eq-bands li.good, #a-equity .eq-statements li.good').length,
    mine: document.querySelectorAll('#a-equity .eq-bands li.mine, #a-equity .eq-statements li.mine').length, strategy: !document.getElementById('a-strategy').hidden }));
  const ans = [], kinds = [], badLayout = [];
  for (let i = 0; i < 5; i++) {
    await p.waitForSelector('#screen-question:not([hidden])');
    const q = await look(), k = KIND[q.kind] || q.kind; kinds.push(k);
    if (i === 0) {
      ok('question : étiquette Équités, sans table, la main en grand', q.cat === 'Équités' && !q.table && q.hand && q.cards === 2, q);
      ok('question : énoncé visible, ni chrono ni rejouée', q.ask === 'ask' && q.askText.length > 30 && !q.timer && !q.skip && q.opts, q);
      await p.screenshot({ path: `${OUT}/equity_question.png` });
    }
    if (!layoutOk(k, q)) badLayout.push({ k, q });
    await p.click(`#actions button >> nth=${i % 2 ? -1 : 0}`); await p.waitForSelector('#screen-answer:not([hidden])');
    ans.push({ k, ...(await readAnswer()) });
    await p.click('#next-btn');
  }
  ok('série par défaut : 5 sortes différentes, connues', new Set(kinds).size === 5 && kinds.every((k) => Object.values(KIND).includes(k)), kinds);
  ok('réponses selon la sorte : tranches en grille, affirmations ou phrases sur une colonne', !badLayout.length, badLayout);
  ok('correction : verdict et bonne réponse dite', ans.every((a) => /(Bonne tranche|Bon nombre|Bonne réponse|Imprécision|Erreur)/.test(a.verdict) && /(tranche|réponse|nombre)/i.test(a.verdict)), ans.map((a) => [a.k, a.verdict]));
  ok('correction : la valeur exacte en une phrase (hors affirmations)', ans.filter((a) => a.k !== 'labels').every((a) => /\d+(,\d)? %|\d+ cartes? sur 47/.test(a.essential)), ans.map((a) => [a.k, a.essential]));
  ok('correction : le calcul', ans.every((a) => /le calcul/i.test(a.calc) && a.calc.length > 30), ans.map((a) => [a.k, a.calc]));
  ok('correction : une seule bonne ligne, ta réponse marquée', ans.every((a) => a.box && a.good === 1 && a.mine === 1), ans.map((a) => [a.k, a.good, a.mine]));
  ok('correction : jamais de BB perdus, pas de stratégie de référence', ans.every((a) => !/BB perdus|coûte/.test(a.text) && !a.strategy), ans.map((a) => a.text.match(/.{0,30}(BB perdus|coûte).{0,30}/)));   // « à 8 BB » d'un énoncé reste permis
  await p.waitForSelector('#screen-summary:not([hidden])');
  const sum = await p.innerText('#screen-summary');
  ok('bilan : étiquette Équités, sans BB perdus ni révision', (await p.textContent('#s-cat')).trim() === 'Équités' && !/BB perdus|t'a coûté|coûte/.test(sum) && await p.isHidden('#s-review'), sum.slice(0, 400));
  const errs2 = await p.innerText('#s-errors');
  ok('bilan : ta réponse et la bonne, sans coût', !(await p.$$('#s-errors li em')).length || (/Ta réponse : .* · bonne réponse : /.test(errs2) && !/coûte|Meilleur coup/.test(errs2)), errs2);
  if (!BASE.startsWith('file:')) ok('bilan : la valeur exacte sur chaque erreur (serveur)', !(await p.$$('#s-errors li em')).length || /valeur exacte : [\d,]+ %/.test(errs2), errs2);   // la démo ne l'envoie pas encore
  await p.screenshot({ path: `${OUT}/equity_summary.png`, fullPage: true });
  // une seule sorte à la fois (filters.kind) : « Toucher le flop » et « Équité contre une range » ; forces et faiblesses dans la main
  for (const k of ['hit', 'equity']) {
    await p.click('#home-btn'); await p.openTab('exos'); await p.click(`#equity-kinds [data-kind="${k}"]`); await p.waitForSelector('#screen-question:not([hidden])');
    const q = await look();
    await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
    const a = await readAnswer();
    ok(`une seule sorte (${k}) : tranches en grille, valeur exacte, forces et faiblesses`, KIND[q.kind] === k && layoutOk(k, q) && /\d+(,\d)? %/.test(a.essential)
      && /Forces de la main|Faiblesses de la main/.test(a.text), { kind: q.kind, essential: a.essential });
  }
  // une seule sorte : « Forces et faiblesses »
  await p.click('#home-btn'); await p.openTab('exos');
  await p.click('#equity-kinds [data-kind="labels"]'); await p.waitForSelector('#screen-question:not([hidden])');
  ok('une seule sorte : Forces et faiblesses', /Forces et faiblesses/.test(await p.textContent('#eq-kind')) && (await p.$$('#actions button')).length === 4);
  await p.click('#actions button >> nth=0'); await p.waitForSelector('#screen-answer:not([hidden])');
  ok('affirmations : vrai ou faux sur chacune, avec la raison', (await p.$$('#a-equity .eq-statements li')).length === 4 && (await p.$$('#a-equity .eq-statements .why')).length === 4);
  await p.screenshot({ path: `${OUT}/equity_labels.png`, fullPage: true });
  // la carte et Progression
  await p.click('#home-btn'); await p.openTab('gto');
  await p.waitForFunction(() => /% des points · \d+ questions?/.test(document.getElementById('cat-equites-meter').textContent), null, { timeout: 10000 }).catch(() => {});
  ok('carte Équités : score et questions', /^\d+ % des points · \d+ questions?$/.test(await p.textContent('#cat-equites-meter')), await p.textContent('#cat-equites-meter'));
  await p.openTab('prog'); await p.waitForSelector('#st-cats:not([hidden])', { timeout: 10000 });
  const row = await p.innerText('#st-cats-list li[data-cat="equites"]');
  ok('Progression : Équités avec le détail par sorte', /Équités/.test(row) && /(Toucher le flop|Équité contre une range|Forces et faiblesses)/.test(row) && /\d+ %/.test(row), row);
  const gtoRow = await p.innerText('#st-cats-list li[data-cat="gto"]');
  ok('Progression : les équités ne comptent pas en Préflop GTO', /Pas encore commencé/.test(gtoRow), gtoRow);
  ok('aucune erreur JavaScript', !errs.length, errs);
  console.log(JSON.stringify({ base: BASE, kinds, passed: checks.filter((c) => c.ok).length, failed: checks.filter((c) => !c.ok) }, null, 1));
  await b.close(); process.exit(checks.every((c) => c.ok) ? 0 : 1);
})();

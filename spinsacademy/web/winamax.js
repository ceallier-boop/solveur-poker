/* Lecteur d'historique Winamax (Expresso) dans le navigateur : portage de tools/field/winamax_counts.py (même VERSION, mêmes
   situations SITU, mêmes tapis GRID, héros = joueur de « Dealt to »). Sans dépendance, chargé par <script> : window.Winamax.
   - analyze(files, onProgress) -> Promise du résultat ; files = [{name, text}] ; rend la main au navigateur entre deux fichiers
     (et toutes les 2000 mains dans un gros fichier) ; onProgress({done, total, hands}).
   - toCsv(result) -> {'comptages.csv', 'volume.csv'}, identiques octet pour octet à ceux de winamax_counts.py sur les mêmes mains
     (fichiers dans le même ordre).
   Vie privée : les pseudos ne servent qu'en mémoire (séparer héros et adversaires) ; aucun pseudo, numéro de main, de table ou de
   tournoi, aucune date plus fine que le mois n'est rendu ; une vérification refuse de rendre un résultat qui en contiendrait un.
   Ce module n'écrit rien (ni stockage, ni réseau). */
(function (root) {
  'use strict';
  var VERSION = '1.0.1';
  var GRID = [2, 4, 6, 8, 10, 12, 15, 18, 20, 25];
  var FIABLE = 200, INDICATIF = 50;
  var SITU = {
    '3w||BTN': 'BTN premier à parler',
    '3w|BTN:fold|SB': 'SB premier à parler (BTN fold)',
    '3w|BTN:fold SB:tapis|BB': 'BB face au tapis du SB (BTN fold)',
    '3w|BTN:fold SB:limp|BB': 'BB face au limp du SB (BTN fold)',
    '3w|BTN:fold SB:limp BB:tapis|SB': 'SB face au tapis du BB après son limp (BTN fold)',
    '3w|BTN:fold SB:limp BB:relance|SB': 'SB face à la relance du BB après son limp (BTN fold)',
    '3w|BTN:fold SB:relance|BB': "BB face à l'open du SB (BTN fold)",
    '3w|BTN:tapis|SB': 'SB face au tapis du BTN',
    '3w|BTN:tapis SB:fold|BB': 'BB face au tapis du BTN (SB fold)',
    '3w|BTN:tapis SB:paie|BB': 'BB face au tapis du BTN et au call du SB',
    '3w|BTN:relance|SB': "SB face à l'open du BTN",
    '3w|BTN:relance SB:fold|BB': "BB face à l'open du BTN (SB fold)",
    '3w|BTN:limp|SB': 'SB face au limp du BTN',
    '3w|BTN:limp SB:fold|BB': 'BB face au limp du BTN (SB fold)',
    '3w|BTN:limp SB:limp|BB': 'BB face à deux limps',
    'hu||SB': 'SB premier à parler',
    'hu|SB:tapis|BB': 'BB face au tapis du SB',
    'hu|SB:limp|BB': 'BB face au limp du SB',
    'hu|SB:limp BB:tapis|SB': 'SB face au tapis du BB après son limp',
    'hu|SB:limp BB:relance|SB': 'SB face à la relance du BB après son limp',
    'hu|SB:relance|BB': "BB face à l'open du SB"
  };
  // (kind, décision, action comptée) des décisions de calibrage, dans l'ordre de winamax_counts.CALIB
  var CALIB = [
    ['3w', 'BTN premier à parler', 'tapis', 'shove'],
    ['3w', 'SB premier à parler (BTN fold)', 'tapis', 'shove'],
    ['3w', 'SB face au tapis du BTN', 'paie', 'call'],
    ['3w', 'BB face au tapis du BTN (SB fold)', 'paie', 'call'],
    ['3w', 'BB face au tapis du SB (BTN fold)', 'paie', 'call'],
    ['hu', 'SB premier à parler', 'tapis', 'shove'],
    ['hu', 'BB face au tapis du SB', 'paie', 'call']
  ];
  var PARAMS = [
    ['shove (tapis en premier)', CALIB.filter(function (c) { return c[3] === 'shove'; })],
    ['call (payer un tapis)', CALIB.filter(function (c) { return c[3] === 'call'; })],
    ['limp_k (limp du SB)', [['hu', 'SB premier à parler', 'limp'], ['3w', 'SB premier à parler (BTN fold)', 'limp']]],
    ['iso (le BB isole un limp)', [['hu', 'BB face au limp du SB', 'relance'], ['hu', 'BB face au limp du SB', 'tapis'],
      ['3w', 'BB face au limp du SB (BTN fold)', 'relance'], ['3w', 'BB face au limp du SB (BTN fold)', 'tapis']]],
    ['call du tapis après limp', [['hu', 'SB face au tapis du BB après son limp', 'paie'], ['3w', 'SB face au tapis du BB après son limp (BTN fold)', 'paie']]],
    ['open (relance non all-in)', [['hu', 'SB premier à parler', 'relance'], ['3w', 'BTN premier à parler', 'relance'], ['3w', 'SB premier à parler (BTN fold)', 'relance']]]
  ];

  var NUM = '([0-9][0-9\\s.,]*)';
  var RE_HEAD = /^Winamax Poker - (?:Tournament|Tournoi) "([^"]*)"/;
  var RE_TABLE = /^Table: '.*' .*Seat #(\d+) is the button/;
  var RE_SEAT = new RegExp('^Seat (\\d+): (.+) \\(' + NUM + '(?:€)?(?:,[^)]*)?\\)\\s*$');
  var RE_DEALT = /^Dealt to (.+?) \[([^\]]*)\]?/;
  var RE_MONTH = /(\d{4})\/(\d{2})\/\d{2} \d{2}:\d{2}:\d{2}/;
  var RE_FLOAT = /^[0-9]+(\.[0-9]*)?$/;
  var RANKS = 'AKQJT98765432';

  function Unreadable(msg) { this.message = msg; }

  function num(s) {
    s = s.split('\u202f').join('').split('\u00a0').join('').split(' ').join('').replace(/€+$/, '');
    if (s.indexOf(',') >= 0 && s.indexOf('.') < 0) {
      var last = s.split(',').pop();
      s = last.length !== 3 ? s.split(',').join('.') : s.split(',').join('');
    }
    s = s.split(',').join('');
    if (!RE_FLOAT.test(s)) throw new Unreadable('montant');
    return parseFloat(s);
  }

  function bucket(bb) {
    var x = Math.min(bb, 25), best = GRID[0];
    for (var i = 1; i < GRID.length; i++) if (Math.abs(GRID[i] - x) < Math.abs(best - x)) best = GRID[i];
    return best;
  }

  function splitLines(text) {
    var a = text.split(/\r\n|[\n\r\v\f\x1c\x1d\x1e\x85\u2028\u2029]/);
    if (a.length && a[a.length - 1] === '') a.pop();
    return a;
  }

  function splitHands(text) {
    var out = [], hand = [], lines = splitLines(text);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      if (line.indexOf('Winamax Poker - ') === 0 && hand.length) { out.push(hand); hand = []; }
      if (line.trim() || hand.length) hand.push(line.replace(/\s+$/, ''));
    }
    if (hand.length) out.push(hand);
    return out;
  }

  function handName(cards) {
    var c = cards.trim().split(/\s+/);
    if (c.length !== 2) return null;
    var r = c.map(function (x) { return (x.length === 3 && x.slice(0, 2) === '10' ? 'T' : x[0]).toUpperCase(); });
    var s = c.map(function (x) { return x.slice(-1).toLowerCase(); });
    if (RANKS.indexOf(r[0]) < 0 || RANKS.indexOf(r[1]) < 0) return null;
    if (RANKS.indexOf(r[1]) < RANKS.indexOf(r[0])) { r.reverse(); }
    return r[0] === r[1] ? r[0] + r[1] : r[0] + r[1] + (s[0] === s[1] ? 's' : 'o');
  }

  // main -> objet, null (autre format, partie fictive) ; lève Unreadable pour une main illisible
  function parse(lines) {
    var m = RE_HEAD.exec(lines[0]);
    if (!m || m[1].toLowerCase().indexOf('expresso') !== 0) return null;
    for (var j = 0; j < Math.min(3, lines.length); j++) if (lines[j].toLowerCase().indexOf('play money') >= 0) return null;
    var mo = RE_MONTH.exec(lines[0]);
    var seats = new Map(), hero = null, cards = null, posts = {}, i = 1, l, t, s, d;
    for (var k = 1; k < lines.length; k++) {
      i = k; l = lines[k];
      t = RE_TABLE.exec(l); s = RE_SEAT.exec(l);
      if (t) { /* bouton : les positions viennent des blindes */ }
      else if (s) seats.set(s[2], num(s[3]));
      else if (l.indexOf('*** PRE-FLOP') === 0) break;
      else {
        d = RE_DEALT.exec(l);
        if (d) { hero = d[1]; cards = d[2]; }
        seats.forEach(function (_, nm) {
          ['small blind', 'big blind'].forEach(function (kw) {
            var p = nm + ' posts ' + kw + ' ';
            if (l.indexOf(p) === 0) {
              var w = l.slice(p.length).trim().split(/\s+/);
              if (!w[0]) throw new Unreadable('blinde');
              posts[kw] = [nm, num(w[0])];
            }
          });
        });
      }
    }
    if ((seats.size !== 2 && seats.size !== 3) || !posts['big blind'] || !posts['small blind']) throw new Unreadable('table');
    var pos = new Map(); pos.set(posts['small blind'][0], 'SB'); pos.set(posts['big blind'][0], 'BB');
    if (seats.size === 3) {
      var rest = []; seats.forEach(function (_, nm) { if (!pos.has(nm)) rest.push(nm); });
      if (rest.length !== 1) throw new Unreadable('positions');
      pos.set(rest[0], 'BTN');
    }
    var acts = [];
    for (var q = i + 1; q < lines.length; q++) {
      l = lines[q];
      if (l.indexOf('***') === 0) break;
      var nm = null;
      seats.forEach(function (_, n) { if (l.indexOf(n + ' ') === 0 && (nm === null || n.length > nm.length)) nm = n; });
      if (nm === null) continue;
      var rest2 = l.slice(nm.length + 1).trim(), w = rest2 ? rest2.split(/\s+/) : [];
      if (!w.length || ['folds', 'checks', 'calls', 'bets', 'raises'].indexOf(w[0]) < 0) continue;
      var allin = /is all-in$/.test(l);
      var to = (w[0] === 'raises' && w.length > 3 && w[2] === 'to') ? num(w[3]) : ((w.length > 1 && (w[0] === 'calls' || w[0] === 'bets')) ? num(w[1]) : 0);
      acts.push([nm, w[0], to, allin]);
    }
    return { kind: seats.size === 3 ? '3w' : 'hu', hero: hero, hand: cards === null ? null : handName(cards), stacks: seats, pos: pos,
      bb: posts['big blind'][1], acts: acts, month: mo ? mo[1] + '-' + mo[2] : null, sb: posts['small blind'], bbp: posts['big blind'] };
  }

  // décisions préflop : {nm, kind, decision (null hors SITU), action, eff, history, position, to}
  function decisions(h) {
    var stacks = h.stacks, pos = h.pos, bb = h.bb, put = new Map(), allin = new Map(), folded = new Set();
    var raised = false, aggr = null, hist = [], out = [];
    stacks.forEach(function (_, n) { put.set(n, 0); });
    put.set(h.sb[0], h.sb[1]); put.set(h.bbp[0], h.bbp[1]);
    stacks.forEach(function (st, n) { allin.set(n, put.get(n) >= st - 1e-9); });
    for (var i = 0; i < h.acts.length; i++) {
      var a = h.acts[i], nm = a[0], verb = a[1], amount = a[2], flag = a[3], cat;
      if (allin.get(nm) || folded.has(nm)) return out;
      var oth = null;
      if (aggr) oth = stacks.get(aggr);
      else stacks.forEach(function (st, n) { if (n !== nm && !folded.has(n) && (oth === null || st > oth)) oth = st; });
      var eff = Math.min(stacks.get(nm), oth === null ? stacks.get(nm) : oth) / bb;
      if (verb === 'folds') { cat = 'fold'; folded.add(nm); }
      else if (verb === 'checks') cat = 'check';
      else if (verb === 'calls') { put.set(nm, put.get(nm) + amount); cat = raised ? 'paie' : 'limp'; }
      else {
        put.set(nm, verb === 'raises' ? amount : put.get(nm) + amount);
        var shove = flag || put.get(nm) >= stacks.get(nm) - 1e-9;
        cat = (aggr && allin.get(aggr)) ? 'paie' : (shove ? 'tapis' : 'relance');
        if (cat !== 'paie') { raised = true; aggr = nm; }
      }
      allin.set(nm, allin.get(nm) || flag || put.get(nm) >= stacks.get(nm) - 1e-9);
      var history = hist.join(' ');
      out.push({ nm: nm, kind: h.kind, decision: SITU[h.kind + '|' + history + '|' + pos.get(nm)] || null, action: cat, eff: eff,
        history: history, position: pos.get(nm), to: (verb === 'raises' || verb === 'bets') ? put.get(nm) / bb : null });
      hist.push(pos.get(nm) + ':' + cat);
    }
    return out;
  }

  function cmp(a, b) { return a < b ? -1 : a > b ? 1 : 0; }
  function status(n) { return n >= FIABLE ? 'fiable' : n >= INDICATIF ? 'indicatif' : 'insuffisant'; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function keep(name) { var n = String(name || '').toLowerCase(); return /\.txt$/.test(n) && n.split(/[\\/]/).pop().indexOf('summary') < 0; }
  function tick() { return new Promise(function (r) { setTimeout(r, 0); }); }

  // aucun pseudo dans le résultat ; un pseudo qui est un mot des libellés, une main (« AKs ») ou un nombre n'est pas cherché
  var WORD = /[\p{L}\p{N}_]+/gu, VOCAB = null;
  function vocab() {
    if (VOCAB) return VOCAB;
    var txt = JSON.stringify([SITU, CALIB, PARAMS]) + ' field fold check limp paie relance tapis fiable indicatif insuffisant SB BB BTN hu 3w '
      + 'group kind decision action stack n k parameter status table position stack_bb history hero_hand month to_bb version hands '
      + 'unreadable ignored by_table counts volume hero_decisions files skipped_files months groupe parametre statut';
    VOCAB = new Set((txt.toLowerCase().match(WORD) || []));
    for (var i = 0; i < 13; i++) for (var j = 0; j < 13; j++) {
      var a = RANKS[i], b = RANKS[j];
      VOCAB.add((a + b).toLowerCase()); VOCAB.add((a + b + 's').toLowerCase()); VOCAB.add((a + b + 'o').toLowerCase());
    }
    return VOCAB;
  }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function assertNoNames(obj, names) {
    var body = JSON.stringify(obj), v = vocab();
    names.forEach(function (n) {
      if (n.length < 3 || v.has(n.toLowerCase()) || /^[\d\W_]+$/u.test(n)) return;
      if (new RegExp('(?<![\\p{L}\\p{N}_])' + esc(n) + '(?![\\p{L}\\p{N}_])', 'u').test(body))
        throw new Error('Arrêt : un pseudo apparaîtrait dans le résultat. Rien n\'est rendu.');
    });
    return obj;
  }

  function analyze(files, onProgress) {
    var cnt = new Map(), occ = new Map(), heroes = new Set(), names = new Set(), months = new Set();
    var res = { version: VERSION, files: 0, skipped_files: 0, hands: 0, unreadable: 0, ignored: 0, by_table: { hu: 0, '3w': 0 },
      months: null, counts: [], volume: [], hero_decisions: [] };
    var list = (files || []).filter(function (f) { if (keep(f.name)) return true; res.skipped_files++; return false; });
    var seen = 0;
    function doHand(lines) {
      seen++;
      var h;
      try { h = parse(lines); }
      catch (e) { if (e instanceof Unreadable) { res.unreadable++; return; } throw e; }
      if (h === null) { res.ignored++; return; }
      if (h.hero === null) { res.unreadable++; return; }
      res.hands++; res.by_table[h.kind]++;
      if (h.month) months.add(h.month);
      heroes.add(h.hero); h.stacks.forEach(function (_, n) { names.add(n); });
      decisions(h).forEach(function (d) {
        if (d.nm === h.hero) res.hero_decisions.push({ table: d.kind, position: d.position, stack_bb: r2(d.eff), history: d.history,
          decision: d.decision, hero_hand: h.hand, action: d.action, to_bb: d.to === null ? null : r2(d.to), month: h.month });
        if (!d.decision || heroes.has(d.nm)) return;
        var s = bucket(d.eff), ko = d.kind + '\u0000' + d.decision + '\u0000' + s, kc = ko + '\u0000' + d.action;
        occ.set(ko, (occ.get(ko) || 0) + 1); cnt.set(kc, (cnt.get(kc) || 0) + 1);
      });
    }
    return (async function () {
      for (var f = 0; f < list.length; f++) {
        var text = String(list[f].text || '').replace(/^\ufeff/, ''), hands = splitHands(text);
        res.files++;
        for (var i = 0; i < hands.length; i++) { doHand(hands[i]); if (i % 2000 === 1999) await tick(); }
        if (onProgress) onProgress({ done: f + 1, total: list.length, hands: seen });
        await tick();
      }
      var keys = Array.from(occ.keys()).map(function (k) { var p = k.split('\u0000'); return [p[0], p[1], +p[2]]; });
      keys.sort(function (a, b) { return cmp(a[0], b[0]) || cmp(a[1], b[1]) || a[2] - b[2]; });
      keys.forEach(function (key) {
        var ko = key[0] + '\u0000' + key[1] + '\u0000' + key[2], acts = new Set();
        cnt.forEach(function (_, kc) { var p = kc.split('\u0000'); if (p[0] === key[0] && p[1] === key[1] && +p[2] === key[2]) acts.add(p[3]); });
        CALIB.forEach(function (c) { if (c[0] === key[0] && c[1] === key[1]) acts.add(c[2]); });
        Array.from(acts).sort(cmp).forEach(function (a) {
          res.counts.push({ group: 'field', kind: key[0], decision: key[1], action: a, stack: key[2], n: occ.get(ko), k: cnt.get(ko + '\u0000' + a) || 0 });
        });
      });
      PARAMS.forEach(function (p) {
        var decs = [];
        p[1].forEach(function (c) { if (!decs.some(function (x) { return x[0] === c[0] && x[1] === c[1]; })) decs.push([c[0], c[1]]); });
        GRID.forEach(function (s) {
          var n = 0; decs.forEach(function (x) { n += occ.get(x[0] + '\u0000' + x[1] + '\u0000' + s) || 0; });
          res.volume.push({ parameter: p[0], stack: s, n: n, status: status(n) });
        });
      });
      var ms = Array.from(months).sort(); res.months = ms.length ? [ms[0], ms[ms.length - 1]] : null;
      var all = Array.from(names); heroes.forEach(function (n) { if (!names.has(n)) all.push(n); });
      return assertNoNames(res, all);
    })();
  }

  function csvField(v) { var s = String(v); return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  function csvRow(a) { return a.map(csvField).join(',') + '\n'; }
  function toCsv(r) {
    var c = csvRow(['groupe', 'kind', 'decision', 'action', 'stack', 'n', 'k']);
    r.counts.forEach(function (x) { c += csvRow([x.group, x.kind, x.decision, x.action, x.stack, x.n, x.k]); });
    var v = csvRow(['parametre', 'stack', 'n', 'statut']);
    r.volume.forEach(function (x) { v += csvRow([x.parameter, x.stack, x.n, x.status]); });
    return { 'comptages.csv': c, 'volume.csv': v };
  }

  root.Winamax = { VERSION: VERSION, GRID: GRID.slice(), analyze: analyze, toCsv: toCsv,
    _internal: { parse: parse, splitHands: splitHands, decisions: decisions, bucket: bucket, num: num, handName: handName, assertNoNames: assertNoNames } };
})(typeof window !== 'undefined' ? window : globalThis);

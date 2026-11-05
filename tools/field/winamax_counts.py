"""Comptages du field à partir d'un historique de mains Winamax (Expresso), pour calibrer les profils (calibrate_profiles.py).

Lit les fichiers d'historique en local (dossier ou archive .zip) et n'écrit que des comptages agrégés :
  comptages.csv   groupe, kind, decision, action, stack, n, k : n occasions de la décision, k fois l'action, adversaires du
                  héros seulement (le héros est le joueur de « Dealt to ») ;
  volume.csv      pour chaque paramètre des profils et chaque tapis : occasions et statut (fiable, indicatif, insuffisant) ;
  adversaires.csv répartition des adversaires assez observés selon leur écart au field (cases de moins de 5 joueurs regroupées) ;
  rapport.txt     résumé lisible.
Aucun pseudo, numéro de main, de table ou de tournoi, aucune date plus fine que le mois n'est écrit : les pseudos ne servent
qu'en mémoire, pour séparer héros et adversaires et compter chaque adversaire, et une vérification refuse d'écrire un fichier
qui en contiendrait un. Les fichiers bruts ne doivent jamais entrer dans le dépôt.

Bibliothèque standard seulement (Windows, macOS, Linux ; pas de processus parallèles).
Usage : python winamax_counts.py <dossier ou archive .zip> [--sortie dossier] [--tous-formats]
"""
import argparse, csv, io, json, math, os, re, sys, zipfile
from collections import defaultdict

VERSION = '1.0.0'
GRID = (2, 4, 6, 8, 10, 12, 15, 18, 20, 25)          # tapis du moteur (BB) ; au-delà de 25 BB : 25
FIABLE, INDICATIF = 200, 50                           # occasions par case : facteur à ± 15 % environ à 200, tendance à 50
MIN_SHOVE, MIN_CALL, K_ANON = 50, 20, 5               # adversaires : occasions minimales ; cases de moins de 5 joueurs regroupées

# situation (actions précédentes, position de celui qui parle) -> décision ; positions 3w : BTN, SB, BB ; hu : SB (bouton), BB
SITU = {
    ('3w', '', 'BTN'): 'BTN premier à parler',
    ('3w', 'BTN:fold', 'SB'): 'SB premier à parler (BTN fold)',
    ('3w', 'BTN:fold SB:tapis', 'BB'): 'BB face au tapis du SB (BTN fold)',
    ('3w', 'BTN:fold SB:limp', 'BB'): 'BB face au limp du SB (BTN fold)',
    ('3w', 'BTN:fold SB:limp BB:tapis', 'SB'): 'SB face au tapis du BB après son limp (BTN fold)',
    ('3w', 'BTN:fold SB:limp BB:relance', 'SB'): 'SB face à la relance du BB après son limp (BTN fold)',
    ('3w', 'BTN:fold SB:relance', 'BB'): "BB face à l'open du SB (BTN fold)",
    ('3w', 'BTN:tapis', 'SB'): 'SB face au tapis du BTN',
    ('3w', 'BTN:tapis SB:fold', 'BB'): 'BB face au tapis du BTN (SB fold)',
    ('3w', 'BTN:tapis SB:paie', 'BB'): 'BB face au tapis du BTN et au call du SB',
    ('3w', 'BTN:relance', 'SB'): "SB face à l'open du BTN",
    ('3w', 'BTN:relance SB:fold', 'BB'): "BB face à l'open du BTN (SB fold)",
    ('3w', 'BTN:limp', 'SB'): 'SB face au limp du BTN',
    ('3w', 'BTN:limp SB:fold', 'BB'): 'BB face au limp du BTN (SB fold)',
    ('3w', 'BTN:limp SB:limp', 'BB'): 'BB face à deux limps',
    ('hu', '', 'SB'): 'SB premier à parler',
    ('hu', 'SB:tapis', 'BB'): 'BB face au tapis du SB',
    ('hu', 'SB:limp', 'BB'): 'BB face au limp du SB',
    ('hu', 'SB:limp BB:tapis', 'SB'): 'SB face au tapis du BB après son limp',
    ('hu', 'SB:limp BB:relance', 'SB'): 'SB face à la relance du BB après son limp',
    ('hu', 'SB:relance', 'BB'): "BB face à l'open du SB",
}
# décisions de calibrate_profiles.DECISIONS : (kind, décision ici, action comptée) -> (type, nom dans calibrate_profiles)
CALIB = {
    ('3w', 'BTN premier à parler', 'tapis'): ('shove', 'BTN all-in en premier'),
    ('3w', 'SB premier à parler (BTN fold)', 'tapis'): ('shove', 'SB all-in (BTN fold)'),
    ('3w', 'SB face au tapis du BTN', 'paie'): ('call', "SB paie l'all-in du BTN"),
    ('3w', 'BB face au tapis du BTN (SB fold)', 'paie'): ('call', "BB paie l'all-in du BTN (SB fold)"),
    ('3w', 'BB face au tapis du SB (BTN fold)', 'paie'): ('call', "BB paie l'all-in du SB (BTN fold)"),
    ('hu', 'SB premier à parler', 'tapis'): ('shove', 'SB all-in'),
    ('hu', 'BB face au tapis du SB', 'paie'): ('call', "BB paie l'all-in du SB"),
}
# paramètres des profils (profils_field.PROFILES) et décisions qui les mesurent
PARAMS = {
    'shove (tapis en premier)': [(k, d, a) for (k, d, a), (t, _) in CALIB.items() if t == 'shove'],
    'call (payer un tapis)': [(k, d, a) for (k, d, a), (t, _) in CALIB.items() if t == 'call'],
    'limp_k (limp du SB)': [('hu', 'SB premier à parler', 'limp'), ('3w', 'SB premier à parler (BTN fold)', 'limp')],
    'iso (le BB isole un limp)': [('hu', 'BB face au limp du SB', 'relance'), ('hu', 'BB face au limp du SB', 'tapis'),
                                  ('3w', 'BB face au limp du SB (BTN fold)', 'relance'), ('3w', 'BB face au limp du SB (BTN fold)', 'tapis')],
    'call du tapis après limp': [('hu', 'SB face au tapis du BB après son limp', 'paie'), ('3w', 'SB face au tapis du BB après son limp (BTN fold)', 'paie')],
    'open (relance non all-in)': [('hu', 'SB premier à parler', 'relance'), ('3w', 'BTN premier à parler', 'relance'), ('3w', 'SB premier à parler (BTN fold)', 'relance')],
}

NUM = r'([\d][\d\s.,]*)'
RE_HEAD = re.compile(r'^Winamax Poker - (?:Tournament|Tournoi) "([^"]*)"')
RE_TABLE = re.compile(r"^Table: '.*' .*Seat #(\d+) is the button")
RE_SEAT = re.compile(r'^Seat (\d+): (.+) \(' + NUM + r'(?:€)?(?:,[^)]*)?\)\s*$')
RE_DEALT = re.compile(r'^Dealt to (.+?) \[')
RE_MONTH = re.compile(r'(\d{4})/(\d{2})/\d{2} \d{2}:\d{2}:\d{2}')


def num(s):
    """montant Winamax : « 1 000 », « 1,000 », « 12.5 » ou « 12,5 »"""
    s = s.replace(' ', '').replace('\xa0', '').replace(' ', '').rstrip('€')
    if ',' in s and '.' not in s: s = s.replace(',', '.') if len(s.split(',')[-1]) != 3 else s.replace(',', '')
    return float(s.replace(',', ''))


def bucket(bb):
    """tapis effectif (BB) -> case du moteur la plus proche"""
    return min(GRID, key=lambda g: abs(g - min(bb, 25)))


def split_hands(text):
    hand = []
    for line in text.splitlines():
        if line.startswith('Winamax Poker - ') and hand:
            yield hand; hand = []
        if line.strip() or hand: hand.append(line.rstrip())
    if hand: yield hand


def parse(lines, all_formats=False):
    """main -> dict(kind, hero, stacks, bb, month, actions) ou None (hors Expresso, partie fictive, main illisible)"""
    m = RE_HEAD.match(lines[0])
    if not m or (not all_formats and not m.group(1).lower().startswith('expresso')): return None
    if any('play money' in l.lower() for l in lines[:3]): return None
    mo = RE_MONTH.search(lines[0])
    seats, names, button, hero, posts, i = {}, {}, None, None, {}, 1
    for i, l in enumerate(lines[1:], 1):
        t = RE_TABLE.match(l); s = RE_SEAT.match(l)
        if t: button = int(t.group(1))
        elif s: seats[s.group(2)] = num(s.group(3)); names[int(s.group(1))] = s.group(2)
        elif l.startswith('*** PRE-FLOP'): break
        else:
            d = RE_DEALT.match(l)
            if d: hero = d.group(1)
            for nm in seats:
                for kw in ('small blind', 'big blind'):
                    if l.startswith(nm + ' posts ' + kw + ' '): posts[kw] = (nm, num(l[len(nm + ' posts ' + kw + ' '):].split()[0]))
    if len(seats) not in (2, 3) or 'big blind' not in posts or 'small blind' not in posts: return None
    bb = posts['big blind'][1]
    pos = {posts['small blind'][0]: 'SB', posts['big blind'][0]: 'BB'}
    if len(seats) == 3:
        rest = [n for n in seats if n not in pos]
        if len(rest) != 1: return None
        pos[rest[0]] = 'BTN'
    acts = []
    for l in lines[i + 1:]:
        if l.startswith('***'): break
        nm = max((n for n in seats if l.startswith(n + ' ')), key=len, default=None)
        if nm is None: continue
        w = l[len(nm) + 1:].split()
        if not w or w[0] not in ('folds', 'checks', 'calls', 'bets', 'raises'): continue
        allin = l.endswith('is all-in')
        to = num(w[3]) if w[0] == 'raises' and len(w) > 3 and w[2] == 'to' else (num(w[1]) if len(w) > 1 and w[0] in ('calls', 'bets') else 0.0)
        acts.append((nm, w[0], to, allin))
    return dict(kind='3w' if len(seats) == 3 else 'hu', hero=hero, stacks=seats, pos=pos, bb=bb, acts=acts,
                month=f'{mo.group(1)}-{mo.group(2)}' if mo else None, sb=posts['small blind'], bbp=posts['big blind'])


def decisions(h):
    """décisions préflop des joueurs : (joueur, kind, décision, action, tapis effectif en BB)"""
    kind, stacks, pos, bb = h['kind'], h['stacks'], h['pos'], h['bb']
    put = {n: 0.0 for n in stacks}; put[h['sb'][0]] = h['sb'][1]; put[h['bbp'][0]] = h['bbp'][1]
    allin = {n: put[n] >= stacks[n] - 1e-9 for n in stacks}
    folded, bet, raised, aggr, hist, out = set(), bb, False, None, [], []
    for nm, verb, amount, flag in h['acts']:
        if allin[nm] or nm in folded: return out                        # action incohérente : on s'arrête là
        live = [n for n in stacks if n != nm and n not in folded]
        eff = min(stacks[nm], stacks[aggr] if aggr else max((stacks[n] for n in live), default=stacks[nm])) / bb
        if verb == 'folds': cat = 'fold'; folded.add(nm)
        elif verb == 'checks': cat = 'check'
        elif verb == 'calls':
            put[nm] += amount; cat = 'paie' if raised else 'limp'
        else:                                                            # bets ou raises : montant total engagé
            put[nm] = amount if verb == 'raises' else put[nm] + amount
            shove = flag or put[nm] >= stacks[nm] - 1e-9
            cat = 'paie' if (aggr and allin[aggr]) else ('tapis' if shove else 'relance')
            if cat != 'paie': bet, raised, aggr = put[nm], True, nm
        allin[nm] = allin[nm] or flag or put[nm] >= stacks[nm] - 1e-9
        d = SITU.get((kind, ' '.join(hist), pos[nm]))
        if d: out.append((nm, kind, d, cat, eff))
        hist.append(f'{pos[nm]}:{cat}')
    return out


def read_texts(src):
    """(nom, texte) de chaque fichier d'historique d'un dossier (récursif) ou d'une archive .zip ; résumés de tournoi exclus"""
    keep = lambda p: p.lower().endswith('.txt') and 'summary' not in os.path.basename(p).lower()
    if os.path.isfile(src) and src.lower().endswith('.zip'):
        with zipfile.ZipFile(src) as z:
            for n in z.namelist():
                if keep(n): yield n, z.read(n).decode('utf-8-sig', errors='replace')
        return
    for root, _, files in os.walk(src):
        for f in sorted(files):
            p = os.path.join(root, f)
            if keep(p):
                with open(p, encoding='utf-8-sig', errors='replace') as fh: yield p, fh.read()


def collect(src, all_formats=False):
    cnt = defaultdict(lambda: [0, 0])                                  # (kind, décision, action, tapis) -> occasions, fois
    occ = defaultdict(int)                                             # (kind, décision, tapis) -> occasions
    per = defaultdict(lambda: defaultdict(lambda: [0, 0]))             # adversaire (en mémoire) -> (type, kind, décision, tapis) -> n, k
    meta = dict(files=0, hands=0, expresso=0, unreadable=0, hu=0, three=0, months=set(), heroes=set(), names=set())
    for _, text in read_texts(src):
        meta['files'] += 1
        for lines in split_hands(text):
            meta['hands'] += 1
            try: h = parse(lines, all_formats)
            except (ValueError, IndexError): h = None; meta['unreadable'] += 1
            if h is None: continue
            if h['hero'] is None: meta['unreadable'] += 1; continue
            meta['expresso'] += 1; meta['hu' if h['kind'] == 'hu' else 'three'] += 1
            if h['month']: meta['months'].add(h['month'])
            meta['heroes'].add(h['hero']); meta['names'].update(h['stacks'])
            for nm, kind, d, cat, eff in decisions(h):
                if nm in meta['heroes']: continue                     # le field seulement
                s = bucket(eff); occ[(kind, d, s)] += 1; cnt[(kind, d, cat, s)][1] += 1
                for (k, dd, a), (typ, _) in CALIB.items():
                    if (k, dd) == (kind, d):
                        c = per[nm][(typ, kind, d, s)]; c[0] += 1; c[1] += cat == a
    return cnt, occ, per, meta


def status(n): return 'fiable' if n >= FIABLE else 'indicatif' if n >= INDICATIF else 'insuffisant'


def opponent_factors(per, occ, cnt):
    """écart de chaque adversaire assez observé au field (log du facteur de cotes, par type), sans identifiant"""
    pop = {}
    for (k, d, a), (typ, _) in CALIB.items():
        for s in GRID:
            n = occ.get((k, d, s), 0)
            if n: pop[(typ, k, d, s)] = min(max(cnt.get((k, d, a, s), [0, 0])[1] / n, 0.01), 0.99)
    out = []
    for cells in per.values():
        b = {}
        for typ, nmin in (('shove', MIN_SHOVE), ('call', MIN_CALL)):
            r = [(math.log(pop[c] / (1 - pop[c])), n, k) for c, (n, k) in cells.items() if c[0] == typ and c in pop]
            if sum(x[1] for x in r) < nmin: break
            beta = 0.0
            for _ in range(30):                                       # maximum de vraisemblance d'un décalage commun des log-cotes
                p = [1 / (1 + math.exp(-(o + beta))) for o, _, _ in r]
                g = sum(k - n * q for (_, n, k), q in zip(r, p)); hh = sum(n * q * (1 - q) for (_, n, _), q in zip(r, p))
                step = max(-2.0, min(2.0, g / hh)) if hh > 1e-9 else 0.0
                beta += step
                if abs(step) < 1e-6: break
            b[typ] = max(-2.5, min(2.5, beta))
        if len(b) == 2: out.append((b['shove'], b['call']))
    return out


def write(cnt, occ, per, meta, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    files = {}
    buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
    w.writerow(['groupe', 'kind', 'decision', 'action', 'stack', 'n', 'k'])
    for (kind, d, s), n in sorted(occ.items()):
        acts = sorted({a for (k, dd, a, ss) in cnt if (k, dd, ss) == (kind, d, s)})
        for a in acts: w.writerow(['field', kind, d, a, s, n, cnt[(kind, d, a, s)][1]])
    files['comptages.csv'] = buf.getvalue()
    buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n'); w.writerow(['parametre', 'stack', 'n', 'statut'])
    summary = {}
    for p, cells in PARAMS.items():
        decs = {(k, d) for k, d, _ in cells}
        for s in GRID:
            n = sum(occ.get((k, d, s), 0) for k, d in decs)
            w.writerow([p, s, n, status(n)]); summary.setdefault(p, []).append((s, n))
    files['volume.csv'] = buf.getvalue()
    opp = opponent_factors(per, occ, cnt)
    bins = defaultdict(int)
    for bs, bc in opp: bins[(round(bs * 2) / 2, round(bc * 2) / 2)] += 1
    buf = io.StringIO(); w = csv.writer(buf, lineterminator='\n')
    w.writerow(['log_facteur_tapis', 'log_facteur_call', 'adversaires']); small = 0
    for (bs, bc), n in sorted(bins.items()):
        if n >= K_ANON: w.writerow([bs, bc, n])
        else: small += n
    w.writerow(['autres', 'autres', small])
    files['adversaires.csv'] = buf.getvalue()
    months = sorted(meta['months'])
    lines = [f"Comptages Winamax (winamax_counts {VERSION})",
             f"Fichiers lus : {meta['files']} ; mains : {meta['hands']} ; mains Expresso lues : {meta['expresso']} "
             f"(heads-up {meta['hu']}, 3 joueurs {meta['three']}) ; illisibles : {meta['unreadable']}",
             f"Période : {months[0]} à {months[-1]}" if months else "Période : inconnue",
             f"Adversaires distincts : {len(meta['names'] - meta['heroes'])} ; assez observés pour la répartition : {len(opp)}", '',
             "Volume par paramètre (occasions par tapis ; fiable ≥ 200, indicatif ≥ 50) :"]
    for p, rows in summary.items():
        ok = [s for s, n in rows if n >= FIABLE]; mid = [s for s, n in rows if INDICATIF <= n < FIABLE]
        lines.append(f"- {p} : fiable à {', '.join(map(str, ok)) or 'aucun tapis'} BB ; indicatif à {', '.join(map(str, mid)) or 'aucun tapis'} BB")
    lines += ['', "Aucun pseudo ni identifiant n'est écrit dans ces fichiers. Envoie le dossier entier (5 fichiers) au projet."]
    files['rapport.txt'] = '\n'.join(lines) + '\n'
    files['rapport.json'] = json.dumps(dict(version=VERSION, files=meta['files'], hands=meta['hands'], expresso=meta['expresso'],
                                            hu=meta['hu'], three=meta['three'], unreadable=meta['unreadable'], months=[months[0], months[-1]] if months else None,
                                            opponents=len(meta['names'] - meta['heroes']), opponents_profiled=len(opp)), ensure_ascii=False, indent=1)
    # aucun pseudo ne sort : vérification avant écriture. Un pseudo qui est un mot de ce programme (« fold », « field »…) ou un
    # nombre ne peut venir que des libellés ou des comptages : il n'est pas cherché
    with open(__file__, encoding='utf-8') as fh: vocab = set(re.findall(r'\w+', fh.read().lower()))
    names = [n for n in meta['names'] | meta['heroes'] if len(n) >= 3 and n.lower() not in vocab and not re.fullmatch(r'[\d\W_]+', n)]
    for f, body in files.items():
        leak = [n for n in names if re.search(r'(?<!\w)' + re.escape(n) + r'(?!\w)', body)]
        if leak: raise SystemExit(f"Arrêt : un pseudo apparaîtrait dans {f}. Rien n'a été écrit pour ce fichier.")
    for f, body in files.items():
        with open(os.path.join(out_dir, f), 'w', encoding='utf-8', newline='') as fh: fh.write(body)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description="Comptages agrégés du field (Expresso) depuis un historique Winamax, sans pseudo.")
    ap.add_argument('source', help="dossier d'historique Winamax (lu avec ses sous-dossiers) ou archive .zip")
    ap.add_argument('--sortie', default='comptages_winamax', help='dossier des résultats (créé si besoin)')
    ap.add_argument('--tous-formats', action='store_true', help='lire aussi les tournois autres que les Expresso')
    a = ap.parse_args(argv)
    try: sys.stdout.reconfigure(errors='replace')                  # console Windows sans « ≥ » : pas d'arrêt à l'affichage
    except (AttributeError, ValueError): pass
    if not os.path.exists(a.source): raise SystemExit(f"Introuvable : {a.source}")
    cnt, occ, per, meta = collect(a.source, a.tous_formats)
    if not meta['expresso']: raise SystemExit("Aucune main Expresso lue : vérifie le dossier (fichiers .txt de l'historique Winamax).")
    files = write(cnt, occ, per, meta, a.sortie)
    print(files['rapport.txt']); print(f"Résultats dans : {os.path.abspath(a.sortie)}")


if __name__ == '__main__':
    main()

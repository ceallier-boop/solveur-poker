"""Mode exploitant : questions contre les joueurs du field Expresso (moteur exploitant v4.5, tools/field).

Le moteur (tools/field, porté du moteur exploitant v4.1 et corrigé après l'audit Lucho / PA / Lucky du 2026-10-20)
part des exports HRC (stacks de 4 à 25 BB), déforme la stratégie du vilain selon un profil du field (rec passif par
défaut, calling station, dégène, nit, reg) et calcule la meilleure réponse en EV. Il produit une banque de questions
fixes ; ce module la convertit en jeu de données de l'application (data/datasets/exploit_field/<version>/), au format
des spots (une question = un spot, une seule main) pour que séries, progression, révision et signalements restent
communs, puis sert les questions et leurs corrections.

Types de questions : adaptation (la décision change contre ce vilain), inconnu (aucune information : rec passif),
piège (la décision ne change pas), échantillon (read trop mince), identification (« quel est son défaut ? ») et
profil (« quelle pastille ? »). Les deux derniers n'ont pas de main.
Montants affichés en BB (jamais en mBB). Le profil interne du vilain n'est jamais envoyé au joueur : il voit les
statistiques observées (k sur n), comme à la table.
Usage : python -m spinsacademy.field --version 2026.10.20-1
"""
import argparse, datetime, hashlib, json, os, random, sys
from . import grading
from .hrc import ROOT

BUILDER_VERSION = '4.5.0'
OUT = os.path.join(ROOT, 'data', 'datasets', 'exploit_field')
TOOLS = os.path.join(ROOT, 'tools', 'field')
SEED = 11
HU_SHARE = 0.35
MAX_TRAPS, MAX_READ = 2, 1             # par série de 5 : au plus 2 pièges ou échantillons, 1 question de lecture (sauf série « lecture du vilain »)
READ = ('identification', 'profil')
READ_RULE_FR = "Regarde ses stats ET le nombre de coups : quelques coups ne prouvent rien, plusieurs dizaines oui. Sans info solide, joue contre un rec passif."

TYPE_FR = {'adaptation': 'Adaptation', 'inconnu': 'Vilain inconnu', 'piège': 'Piège', 'échantillon': 'Petit échantillon',
           'identification': 'Défaut du vilain', 'profil': 'Quelle pastille ?'}
DIFF = {'facile': 'facile', 'moyen': 'moyen', 'piège': 'difficile'}
# situation du moteur -> table, joueurs, héros, historique (positions, actions), famille, positions des vilains
SITU = {
    ('3w', "BB face à l'all-in du SB (BTN fold)"): ('BB', [('BTN', 'fold'), ('SB', 'allin')], ['SB']),
    ('3w', "BB face à l'all-in du BTN (SB fold)"): ('BB', [('BTN', 'allin'), ('SB', 'fold')], ['BTN']),
    ('3w', "SB face à l'all-in du BTN"): ('SB', [('BTN', 'allin')], ['BTN']),
    ('3w', 'SB pousse (BTN fold) face au BB'): ('SB', [('BTN', 'fold')], ['BB']),
    ('3w', 'BTN pousse face au SB et au BB'): ('BTN', [], ['SB', 'BB']),
    ('hu', "BB face à l'all-in du SB"): ('BB', [('SB', 'allin')], ['SB']),
    ('hu', 'SB pousse face au BB'): ('SB', [], ['BB']),
    ('hu', 'Heads-up : lecture du vilain'): ('BB', [], ['SB']),
    ('hu', 'BB face au limp du SB'): ('BB', [('SB', 'limp')], ['SB']),
    ('3w', 'BB face au limp du SB (BTN fold)'): ('BB', [('BTN', 'fold'), ('SB', 'limp')], ['SB']),
    ('3w', 'BB face au limp du BTN (SB fold)'): ('BB', [('BTN', 'limp'), ('SB', 'fold')], ['BTN']),
    ('hu', 'SB face au tapis du BB après son limp'): ('SB', [('SB', 'limp'), ('BB', 'allin')], ['BB']),
    ('3w', "BB face à l'open du BTN (SB fold)"): ('BB', [('BTN', 'raise'), ('SB', 'fold')], ['BTN']),
}
ACTION = {'Payer': ('C', 'call_allin'), 'Pousser all-in': ('A', 'allin'), 'Limp': ('L', 'limp'), 'Fold': ('F', 'fold'), 'Check': ('X', 'check'),
          'Relancer': ('R', 'raise')}
ENGINE = {'paie': 'Payer', 'pousse': 'Pousser all-in', 'limpe': 'Limp', 'fold': 'Fold', 'checke': 'Check'}
VERB = {'C': 'payer', 'A': 'tapis', 'L': 'compléter (limp)', 'F': 'fold', 'X': 'check', 'R': 'relancer'}
LEAK_FR = {'pousse trop souvent': 'part à tapis trop souvent', 'ne pousse pas assez': 'ne part pas assez à tapis',
           'paie trop souvent': 'paie trop souvent', 'ne paie pas assez': 'ne paie pas assez',
           'complète trop souvent': 'complète trop souvent', 'ne complète pas assez': 'ne complète pas assez',
           'paie souvent ton tapis': 'paie souvent ton tapis après son limp', 'se couche souvent face au tapis': 'se couche souvent face au tapis après son limp',
           'ouvre trop souvent': 'ouvre trop souvent', "n'ouvre pas assez": "n'ouvre pas assez",
           'défend trop face à ta relance': 'défend trop face à ta relance', 'se couche trop face à ta relance': 'se couche trop face à ta relance'}


def _engine():
    if TOOLS not in sys.path: sys.path.insert(0, TOOLS)
    import quiz_generator as qg
    return qg


def bbx(mbb, signed=False):
    """montant en BB, à partir de mBB : 2 décimales (3 sous 0,1 BB), virgule décimale"""
    x = mbb / 1000; a = abs(x)
    s = (f'{a:.3f}' if a < 0.1 else f'{a:.2f}').rstrip('0').rstrip(',').rstrip('.').replace('.', ',')
    if s in ('0', ''): s = '0'
    return (('+' if x >= 0 else '−') + s if signed else s) + ' BB'


def pct(x):
    """pourcentage affiché : entier, virgule décimale si besoin"""
    return f'{x:.0f}'


def _stats(q, hero, vill):
    """statistiques observées, avec leur libellé : tapis du vilain, ou ses calls d'un tapis"""
    out = []
    for j, s in enumerate(q.get('stats') or []):
        if q['type'] == 'profil':
            label = {'shove_pct': 'Tapis quand il est au SB', 'limp_pct': 'Limps quand il est au SB'}.get(s['stat'], 'Calls d\'un tapis quand il est au BB')
        elif s['stat'] == 'shove_pct':
            label = f'Tapis du {vill[0]}'
        elif s['stat'] == 'call_pct_bb_sb_fold':
            label = 'Calls du BB face à ton tapis (SB couché)'
        elif s['stat'] == 'limp_pct':
            label = f'Limps du {vill[0]} (il complète)'
        elif s['stat'] == 'call_after_limp_pct':
            label = 'Calls de ton tapis après son limp'
        elif s['stat'] == 'jam_over_limp_pct':
            label = 'Tapis du BB sur ton limp'
        elif s['stat'] == 'open_pct':
            label = f'Relances du {vill[0]} (ouverture)'
        elif s['stat'] == 'defend_pct':
            label = 'Défense face à ta relance'
        else:
            label = f'Calls du {vill[0]} face à ton tapis'
        out.append(dict(stat=s['stat'], label_fr=label, k=s['k'], n=s['n'], observed_pct=s['observed_pct'], gto_pct=s['gto_pct']))
    return out


def _read_sentence(q, stats, vill):
    n = q['observations']
    if q['type'] == 'profil' or n == 0:
        return "Tu n'as aucune information sur ce vilain." if n == 0 else ''
    parts = []
    for s in stats:
        if s['stat'] == 'call_after_limp_pct':
            parts.append(f"face à un tapis après son limp, il a payé {s['k']} fois sur {s['n']} ({pct(s['observed_pct'])} % ; théorie : {pct(s['gto_pct'])} %)")
            continue
        verb = {'shove_pct': 'est parti à tapis', 'call_pct': 'a payé ton tapis', 'limp_pct': 'a complété', 'jam_over_limp_pct': 'est parti à tapis sur ton limp',
                'open_pct': 'a relancé', 'defend_pct': 'a défendu face à ta relance'}.get(s['stat'], "a payé ton tapis quand le SB s'était couché")
        who = f"le {vill[0]}" if s['stat'] != 'call_pct_bb_sb_fold' else 'le BB'
        parts.append(f"{who} {verb} {s['k']} fois ({pct(s['observed_pct'])} % ; théorie : {pct(s['gto_pct'])} %)")
    return f"Sur {n} occasions dans cette situation, " + ' ; '.join(parts) + '.'


def _hand_display(h):
    from .quiz import hand_display
    return hand_display(h) if h else ''


COVER_SHARE = 0.4        # v4.5 : part des questions heads-up affichées avec des tapis inégaux


def _cover(q):
    """tapis du joueur qui couvre (heads-up), ou None : tirage déterministe par question"""
    h = int(hashlib.md5(q['id'].encode()).hexdigest()[:8], 16)
    if q['type'] == 'profil' or (h % 1000) / 1000 >= COVER_SHARE: return None
    S = float(q['stack']); r = (1.5, 2.0, 3.0)[h % 3]
    return float(min(round(S * r), 60))


def cover_seat(q, hero, vill):
    """qui couvre l'autre : le héros ou le vilain, à parts égales"""
    return hero if int(hashlib.md5(q['id'].encode()).hexdigest()[8:16], 16) % 2 else vill[0]


def to_spot(q, qg):
    """une question de la banque du moteur -> un spot de l'application"""
    from .quiz import PREFLOP_ORDER, bb
    kind, S = q['kind'], float(q['stack'])
    hero, hist0, vill = SITU[(kind, q['situation'])]
    players = list(PREFLOP_ORDER[3 if kind == '3w' else 2]); stacks = [S] * len(players)
    cover = _cover(q) if kind == 'hu' else None            # v4.5 : tapis inégaux en heads-up (en chip EV, seul le tapis effectif compte)
    if cover: stacks = [cover if p == cover_seat(q, hero, vill) else S for p in players]
    opened = q.get('open_bb') or 2.3
    history = [dict(position=p, action=a, **({'to_bb': stacks[players.index(p)]} if a == 'allin' else {'to_bb': 1.0} if a == 'limp'
                                              else {'to_bb': opened} if a == 'raise' else {})) for p, a in hist0]
    commit = dict(zip(players, [0.0, 0.5, 1.0] if len(players) == 3 else [0.5, 1.0]))
    for h in history:
        if 'to_bb' in h: commit[h['position']] = h['to_bb']
    pot = sum(commit.values()); to_call = min(max(commit.values()), S) - commit[hero]
    hand = q.get('hero_hand') or ''
    stats = _stats(q, hero, vill)
    table = '3 joueurs' if kind == '3w' else 'Heads-up'
    lines = [f"{table}, tapis {' / '.join(bb(x) for x in stacks)} BB ({' / '.join(players)})." + (f" Tapis effectif : {bb(S)} BB." if cover else '')]
    for h in history:
        me = h['position'] == hero
        a = h['action']
        lines.append(f"Le {h['position']} se couche." if a == 'fold' else ('Tu complètes.' if me else f"Le {h['position']} complète.") if a == 'limp'
                     else f"Le {h['position']} relance à {bb(h['to_bb'])} BB." if a == 'raise' else f"Le {h['position']} part à tapis ({bb(h['to_bb'])} BB).")
    read = _read_sentence(q, stats, vill)
    if q['type'] == 'profil':
        lines.append(f"Sur {q['observations']} occasions, ce vilain est parti à tapis {stats[0]['k']} fois quand il était au SB "
                     f"({pct(stats[0]['observed_pct'])} % ; théorie : {pct(stats[0]['gto_pct'])} %) et a payé {stats[1]['k']} tapis sur {stats[1]['n']} au BB "
                     f"({pct(stats[1]['observed_pct'])} % ; théorie : {pct(stats[1]['gto_pct'])} %).")
        ask = 'Quelle pastille lui donnes-tu ?'
    else:
        if read: lines.append(read)
        ask = 'Quel est le défaut de ce vilain ?' if q['type'] == 'identification' else None
    if ask: lines.append(ask)
    else: lines.append(f"Tu es au {hero} avec {_hand_display(hand)}. Que fais-tu ?")
    if hand and q['type'] != 'identification':
        options = []; evo = q.get('ev_options_mBB') or {}
        for lab in q['options']:
            aid, typ = ACTION[lab]
            if typ == 'call_allin' and not any(a == 'allin' for _, a in hist0): typ = 'call'      # payer une relance, pas un tapis
            ev = evo[lab] if lab in evo else 0.0 if aid == 'F' else (q['ev_limp_vs_fold_mBB'] if aid == 'L' else q['ev_check_vs_fold_mBB'] if aid == 'X' else q['ev_jeu_vs_fold_mBB'])
            to = (S if typ in ('allin', 'call_allin') else 1.0 if typ in ('limp', 'check') else q.get('relance_bb') if typ == 'raise'
                  else opened if typ == 'call' else None)
            options.append(dict(id=aid, type=typ, to_bb=to, ev_mbb=ev))
        correct = ACTION[q['bonne_reponse']][0]; gto = ACTION[q['action_GTO']][0] if q.get('action_GTO') else None
        acceptable = [ACTION[x][0] for x in q.get('acceptables', [])]
    else:
        options = [dict(id='ABCDE'[k], type='choice', label_fr=lab, ev_mbb=None) for k, lab in enumerate(q['options'])]
        correct = next(o['id'] for o in options if o['label_fr'] == q['bonne_reponse']); gto = None; acceptable = []
    fam = ('read' if q['type'] in ('profil', 'identification') else 'vs_allin' if any(a == 'allin' for _, a in hist0)
           else 'vs_raise' if any(a == 'raise' for _, a in hist0) else 'vs_limp' if any(a == 'limp' for _, a in hist0) else 'first_in')
    sp = dict(spot_id=q['id'], dataset_kind='field', table='3-handed' if kind == '3w' else 'heads-up', players=players, stacks_bb=stacks,
              blinds_bb={'sb': 0.5, 'bb': 1.0}, ante_bb=0.0, model='chip_ev', hero=hero, node_key=q['situation'], history=history,
              pot_bb=pot, to_call_bb=to_call, hero_committed_bb=commit[hero], effective_stack_bb=S, field_family=fam,
              actions=[{k: v for k, v in o.items() if k != 'ev_mbb' and v is not None} for o in options], ev_reference='field',
              hands={hand: dict(reach=1.0, quiz_eligible=True)}, eligible_hands=1, prompt_fr='\n'.join(lines),
              field=dict(type=q['type'], type_fr=TYPE_FR[q['type']], difficulty=DIFF.get(q.get('difficulte', 'moyen'), 'moyen'),
                         situation=q['situation'], villains=vill, observations=q['observations'], stats=stats, ask_fr=ask,
                         options=options, correct=correct, gto=gto, acceptable=acceptable,
                         rule=q['regle'], rule_fr=qg.RULES[q['regle']], leak=q.get('leak', ''),
                         gain_mbb=q.get('gain_mBB', 0), noise_mbb=q.get('seuil_bruit_mBB', 0), margin_mbb=q.get('marge_mBB'),
                         gto_freq_pct=q.get('freq_gto_reponse_pct'), iso_pct=q.get('iso_pct'), iso_pct_gto=q.get('iso_pct_gto'),
                         limp_estimate=bool(q.get('ev_limp_vs_fold_mBB') is not None and kind == 'hu'),
                         theory=q.get('theorie') if q['type'] not in READ else None, postflop=q.get('postflop') if q['type'] not in READ else None,
                         engine_explanation_fr=q['explication'], data_level=q['niveau_donnees'], weight=q.get('poids', 1.0),
                         internal_profile=q['profil']),
              provenance=dict(builder=BUILDER_VERSION, engine='tools/field (moteur exploitant v4.5)', engine_id=q['id'],
                              intensity=q.get('intensite', 1.0), factors=q.get('facteurs')))
    return sp


def build(seed=SEED, n_target=None):
    qg = _engine()
    if n_target: qg.N_TARGET = n_target                       # taille visée enregistrée dans le manifeste (reconstruction)
    return [to_spot(q, qg) for q in sorted(qg.make(seed=seed), key=lambda q: q['id'])]


def publish(version, out=OUT, seed=SEED):
    target = os.path.join(out, version)
    if os.path.exists(target): raise SystemExit(f'{target} existe déjà : une version publiée est immuable')
    items = build(seed); qg = _engine()
    os.makedirs(target)
    with open(os.path.join(target, 'spots.jsonl'), 'w') as f:
        for it in items: f.write(json.dumps(it, ensure_ascii=False, separators=(',', ':')) + '\n')
    digest = hashlib.sha256(open(os.path.join(target, 'spots.jsonl'), 'rb').read()).hexdigest()
    from collections import Counter
    m = dict(dataset='exploit_field', version=version, created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
             builder=BUILDER_VERSION, scale=qg.SCALE, n_target=qg.N_TARGET, seed=seed, spots=len(items), questions_eligible=len(items), spots_sha256=digest,
             by_type=dict(Counter(i['field']['type'] for i in items)), by_rule=dict(Counter(i['field']['rule'] for i in items)),
             noise_mbb={str(k): round(1000 * v) for k, v in qg.ee.NOISE_BB.items()}, rules=qg.RULES,
             reference_fr="Exports HRC (chip EV, blinds 0,5 / 1, sans ante), stacks de 4 à 25 BB ; profils du field (hypothèses, non mesurées)",
             caveats_fr=["Facteurs des profils : hypothèses, à recaler sur de vraies mains (tools/field/calibrate_profiles.py). Au-delà de 12 BB, ceux de 12 BB.",
                         "Range de tapis du rec passif et de la station : la moitié des monstres limpés, les As faibles gardés (compromis Lucho / Lucky).",
                         "Limp du SB : EV estimée en heads-up (décomposition de l'EV HRC), borne basse en BvB à 3 joueurs. Check du BB sur un limp, call d'un open : EV HRC corrigée de l'écart d'équité.",
                         "Relance non all-in (open, iso) : EV HRC décomposée en fold equity (pot gagné quand tout le monde se couche) et valeur quand on est payé ; "
                         "la réponse du limpeur à l'iso est lue dans l'arbre heads-up. Tailles des arbres HRC : open 2,3 BB au BTN, 3,5 BB au SB et en heads-up, iso 3 BB.",
                         "Au-delà de 16 BB, les arbres HRC n'ont pas de tapis au SB ni face au limp : fold, limp, check ou relance.",
                         "Tapis inégaux affichés en heads-up seulement : en chip EV, seul le tapis effectif compte.",
                         "Seuil de bruit : max(ancien plancher, P90 du regret propre de HRC à la même profondeur)."],
             audit='docs/audit/AUDIT_COACHS_FIELD_2026-10-20.md', status='staging')
    json.dump(m, open(os.path.join(target, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    return m


# ------------------------------------------------------------------ service
def question(sp):
    """ce que voit le joueur : état du jeu, statistiques observées, options ; ni solution ni profil interne"""
    from .quiz import hand_display, history_text, action_label
    f = sp['field']; hand = next(iter(sp['hands']))
    opts = [dict(id=o['id'], label_fr=o.get('label_fr') or action_label(sp, o)) for o in f['options']]
    return dict(spot_id=sp['spot_id'], hand=hand, hand_display=hand_display(hand) if hand else '', prompt_fr=sp['prompt_fr'], table=sp['table'],
                players=sp['players'], stacks_bb=sp['stacks_bb'], hero=sp['hero'], history=sp['history'], history_fr=history_text(sp),
                pot_bb=sp['pot_bb'], to_call_bb=sp['to_call_bb'], family=sp['field_family'], difficulty=f['difficulty'], mode='exploit',
                villain=None, profile=None, options=opts,
                field=dict(type=shown_type(f), type_fr=SHOWN_FR[shown_type(f)], observations=f['observations'], villains=f['villains'], stats=f['stats'], ask_fr=f['ask_fr']))


SHOWN_FR = {'inconnu': 'Vilain inconnu', 'observé': 'Vilain observé', 'identification': 'Défaut du vilain', 'profil': 'Quelle pastille ?'}


def shown_type(f):
    """v4.4 (audit Lucho) : avant la réponse, seul ce que le joueur sait est affiché (vilain inconnu ou observé) ; le type de la
    question (adaptation, piège, petit échantillon) se découvre à la correction"""
    if f['type'] in READ: return f['type']
    return 'inconnu' if not f['observations'] else 'observé'


def _label(sp, aid):
    from .quiz import action_label
    o = next(o for o in sp['field']['options'] if o['id'] == aid)
    return o.get('label_fr') or action_label(sp, o)


def theory_lines(sp, f, lab, hand):
    """le « pourquoi » en deux ou trois lignes : la stat qui compte, l'équité de ta main, ce que ça implique"""
    t = f.get('theory')
    if not t or not hand: return []
    out = []
    if t['kind'] == 'call':
        out.append((f"Tu as déjà mis 1 BB en complétant : tu paies {num(t['call_bb'])} BB de plus pour un pot de {num(t['pot_bb'])} BB, il te faut {pct(t['need_pct'])} % d'équité."
                    if t.get('after_limp') else f"Tu paies {num(t['call_bb'])} BB pour un pot de {num(t['pot_bb'])} BB : il te faut {pct(t['need_pct'])} % d'équité."))
        behind = sp['hero'] == 'SB' and sp['table'] == '3-handed'          # v4.4 (audit) : le BB peut encore payer ou surenchérir
        verdict = (("au-dessus de la cote, mais le BB parle encore derrière : il faut une marge." if t['eq_pct'] >= t['need_pct'] else "pas assez, même sans le BB derrière.")
                   if behind else ("assez pour payer." if t['eq_pct'] >= t['need_pct'] else "pas assez pour payer."))
        out.append(f"Il pousse environ {pct(t['range_pct'])} % de ses mains (théorie : {pct(t['range_gto_pct'])} %). Contre ces mains, {hand} a "
                   f"{pct(t['eq_pct'])} % d'équité : " + verdict)
    elif t['kind'] in ('shove', 'open'):
        if t['kind'] == 'shove':
            who = 'tout le monde se couche' if t['win_bb'] == 1.5 else 'il se couche'
            out.append(f"Face à ton tapis, {who} environ {pct(t['fold_pct'])} % du temps (théorie : {pct(t['fold_gto_pct'])} %) : "
                       f"tu gagnes {'1,5 BB' if t['win_bb'] == 1.5 else '1 BB'} sans abattage.")
            out.append(f"Quand il paie, {hand} a {pct(t['eq_called_pct'])} % d'équité.")
        else:
            out.append(f"Il défend environ {pct(t['defend_pct'])} % de ses mains face à une relance (théorie : {pct(t['defend_gto_pct'])} %). "
                       f"Quand il défend, {hand} a {pct(t['eq_called_pct'])} % d'équité.")
        if t.get('raise_bb'):
            out.append(f"Face à une relance à {num(t['raise_bb'])} BB, tout le monde se couche environ {pct(t['raise_fold_pct'])} % du temps "
                       f"(théorie : {pct(t['raise_fold_gto_pct'])} %) : une petite relance gagne les mêmes blindes pour moins cher.")
        if t.get('iso_pct') is not None:
            out.append(f"Si tu complètes, il relance environ {pct(t['iso_pct'])} % du temps (théorie : {pct(t['iso_gto_pct'])} %) : "
                       "moins il relance, plus le limp est rentable.")
    elif t['kind'] == 'iso':
        who = t.get('limper', 'SB')
        out.append(f"Le {who} complète environ {pct(t['limp_pct'])} % de ses mains (théorie : {pct(t['limp_gto_pct'])} %). Contre ces mains, {hand} a "
                   f"{pct(t['eq_limp_pct'])} % d'équité.")
        if t.get('has_jam', True):
            out.append(f"Face à ton tapis, il se couche {pct(t['fold_pct'])} % du temps (théorie : {pct(t['fold_gto_pct'])} %) : tu prends le pot de "
                       f"{num(t.get('win_bb', 2.0))} BB. Quand il paie, {hand} a {pct(t['eq_called_pct'])} % d'équité.")
        if t.get('raise_bb'):
            out.append(f"Face à une iso à {num(t['raise_bb'])} BB, il se couche environ {pct(t['raise_fold_pct'])} % du temps (théorie : "
                       f"{pct(t['raise_fold_gto_pct'])} %).")
        out.append("Après un check, tu parles en premier au flop : ta main rapporte moins. D'où plus d'agressivité."
                   if (f.get('postflop') or {}).get('position') == 'OOP' or (sp['table'] == 'heads-up' and not f.get('postflop')) else
                   "Après un check, tu parles en dernier au flop : tes mains jouables rapportent plus.")
    elif t['kind'] == 'vsopen':
        out.append(f"Le BTN ouvre environ {pct(t['open_pct'])} % de ses mains (théorie : {pct(t['open_gto_pct'])} %). Contre ces mains, {hand} a "
                   f"{pct(t['eq_open_pct'])} % d'équité.")
        out.append(f"Face à ton tapis, il se couche {pct(t['fold_pct'])} % du temps (théorie : {pct(t['fold_gto_pct'])} %) : tu prends {num(t['win_bb'])} BB. "
                   f"Quand il paie, {hand} a {pct(t['eq_called_pct'])} % d'équité.")
    return out


def num(x):
    return str(x).replace('.', ',').rstrip('0').rstrip(',') if '.' in str(x) else str(x)


R = 'AKQJT98765432'


def _plan(ip, hero, table):
    """trois consignes concrètes pour le flop, selon la position"""
    if ip:
        return ["Il checke : mise environ 1 BB (la moitié du pot) très souvent, il a souvent raté.",
                "Il mise : un joueur passif mise surtout quand il a touché. Couche tes mains faibles.",
                "Paire max ou mieux : mise pour la valeur à chaque tour, il paie trop."]
    return ["Tu as touché (paire max ou mieux) : mise toi-même environ 1 BB, il paie avec trop de mains.",
            "Tu as raté : checke. S'il mise peu, paie avec une paire ou un tirage, couche le reste.",
            "AA ou KK : mise dès le flop pour la valeur, n'attends pas."]


def postflop_section(sp, f, hand):
    """« Gérer le postflop » : le tapis qui reste, ta position, un plan simple, ce qui aide ta main et ce qui aide la sienne"""
    from .quiz import postflop_profile, bb
    p = f.get('postflop')
    if not p or not hand: return None
    pf = postflop_profile(hand); pc = lambda x: f"{round(100 * x)} %"
    S = sp['effective_stack_bb']; hero = sp['hero']; hu = sp['table'] == 'heads-up'
    ip = p['position'] == 'IP' if p.get('line') else (hero == 'SB') == hu   # v4.5 : position fournie par le moteur (BB face au BTN : hors de position)
    line = ("tu paies son ouverture" if p.get('line') == 'vsopen' else "tu checkes son limp" if hero == 'BB' else "il checke derrière ton limp")
    pot, left = p.get('pot_bb', 2.0), p.get('left_bb', S - 1)
    intro = (f"Si le coup va au flop ({line}) : pot de {num(round(pot, 2))} BB, il reste {bb(left)} BB chacun, soit {num(p['spr'])} fois le pot (SPR). "
             + ("Une paire max ou un gros tirage suffit pour mettre tapis." if p['spr'] <= 3
                else "Paire max bon kicker : tapis. Paire moyenne : petites mises."))
    position = ("Tu parles en dernier : tu vois ce qu'il fait avant de jouer." if ip
                else "Tu parles en premier : joue simple.")
    mine, his = [], []
    if len(hand) == 2:
        mine.append(f"Paire servie : brelan ou mieux {pc(pf['set_plus'])} du temps.")
        if pf['overpair'] < 0.3: his.append(f"Ta paire est rarement au-dessus du board ({pc(pf['overpair'])} du temps).")
    else:
        if pf['top_pair_plus'] >= 0.25: mine.append(f"Paire max ou mieux {pc(pf['top_pair_plus'])} du temps.")
        if hand.endswith('s'): mine.append(f"Assorties : tirage couleur ou mieux {pc(pf['flush_draw_plus'])} du temps.")
        if pf['oesd_plus'] >= 0.1: mine.append(f"Connectées : tirage quinte ou mieux {pc(pf['oesd_plus'])} du temps.")
        if pf['miss'] >= 0.5: his.append(f"Tu rates le flop {pc(pf['miss'])} du temps (ni paire ni tirage).")
        if R.index(hand[0]) <= R.index('T') and R.index(hand[1]) >= R.index('7'):
            his.append(f"Kicker faible : quand ton {hand[0]} touche, ses {hand[0]}x plus forts te battent.")
    if p['eq_hand_pct'] >= 50: mine.append(f"Contre ses mains, {hand} a {pct(p['eq_hand_pct'])} % d'équité : tu es devant.")
    else: his.append(f"Contre ses mains, {hand} n'a que {pct(p['eq_hand_pct'])} % d'équité : tu es derrière.")
    if p['strong_pct'] >= p['strong_gto_pct'] + 3:
        his.append(f"Il a {pct(p['strong_pct'])} % de grosses mains (théorie : {pct(p['strong_gto_pct'])} %) : "
                   + ("il complète aussi ses grosses mains." if hero == 'BB' else "il checke aussi ses grosses mains."))
    elif p['strong_pct'] <= p['strong_gto_pct'] - 3:
        mine.append(f"Il a peu de grosses mains ({pct(p['strong_pct'])} %, théorie : {pct(p['strong_gto_pct'])} %) : il les a relancées.")
    if ip: mine.append("La position : tu joues après lui à chaque tour.")
    if not mine: mine.append("Il se couche souvent face à une mise : un flop raté se gagne aussi.")
    return dict(title_fr='Gérer le postflop', intro=intro, position=position, plan=_plan(ip, hero, sp['table']), plan_fr='Ton plan',
                metrics=[], forces=mine[:3], weaknesses=his[:3], plus_fr='Ce qui aide ta main', minus_fr='Ce qui aide la sienne')


def correct(sp, action_id):
    """correction : verdict sur l'EV (mêmes seuils que l'application), explication et théorie en BB, règle à retenir,
    « Gérer le postflop » quand la main peut voir un flop"""
    from .quiz import _low
    f = sp['field']; ids = [o['id'] for o in f['options']]
    if action_id not in ids: raise ValueError(f'action inconnue : {action_id}')
    best = f['correct']; ev = {o['id']: o['ev_mbb'] for o in f['options']}; hand = next(iter(sp['hands']))
    if ev[best] is not None:
        regret = max(0.0, ev[best] - ev[action_id])
        if action_id == best or regret <= grading.TOLERANCE_MBB: verdict = 'correct'
        elif regret <= 3 * grading.TOLERANCE_MBB or action_id in f['acceptable']: verdict = 'imprécision'
        else: verdict = 'erreur'
    else:
        regret = 0.0; verdict = 'correct' if action_id == best else 'erreur'
    lab = {a: _label(sp, a) for a in ids}; v = f['villains'][0]; n = f['observations']
    rule_fr = READ_RULE_FR if f['type'] in READ else f['rule_fr']
    rule = f"À retenir : {rule_fr}"
    short = lambda a: _low(lab[a]).split(' (')[0]                  # « tapis », pas « tapis (6 BB) » dans une phrase
    lines = []; best_l, gto_l = short(best), (short(f['gto']) if f['gto'] else '')
    if f['type'] in ('profil', 'identification', 'échantillon'):
        lines.append(f['engine_explanation_fr'].split(' Règle R')[0])
    elif f['type'] == 'adaptation':
        sample = next((f"{st['n']} {'limps' if st['stat'] == 'call_after_limp_pct' else 'folds du SB'} observés" for st in f['stats']
                       if 'après son limp' in LEAK_FR.get(f['leak'], '') and st['stat'] == 'call_after_limp_pct'), f"{n} coups observés")   # v4.4 : le bon échantillon
        lines.append(f"Il {LEAK_FR.get(f['leak'], f['leak'])} ({sample}). Contre lui, {best_l} rapporte {bbx(f['gain_mbb'])} de plus "
                     f"que la théorie ({gto_l}).")
    elif f['type'] == 'inconnu':
        lines.append(f"Sans info, joue contre un rec passif. Contre lui, {best_l} rapporte {bbx(f['gain_mbb'])} de plus que la théorie ({gto_l}).")
    elif f['rule'] == 'R11':
        lines.append(f"Ses stats collent à la théorie : {best_l} reste le meilleur coup ({bbx(f['margin_mbb'])} d'avance).")
    else:
        who = 'un rec passif' if n == 0 else 'lui'
        lines.append(f"Même contre {who}, {best_l} reste le meilleur coup ({bbx(f['margin_mbb'])} d'avance) : l'écart de stats ne change pas la décision.")
    if action_id != best:
        lines.append(f"Ton choix ({short(action_id)}) " + (f"rapporte {bbx(regret)} de moins." if ev[best] is not None else "n'est pas la bonne lecture."))
    if ev[best] is not None and f['type'] not in READ and f['margin_mbb'] < 100:
        lines.append(f"Écart faible ({bbx(f['margin_mbb'])}) : les deux options sont proches.")
    lines.append(rule)
    why = theory_lines(sp, f, lab, hand)
    if ev[best] is not None:
        if f['gto'] and f['gto'] != best and (f['gto_freq_pct'] or 0) >= 5:
            why.append(f"La théorie joue déjà {best_l} {pct(f['gto_freq_pct'])} % du temps avec cette main.")
    gto_label = lab[f['gto']] if f['gto'] else None
    return dict(verdict=verdict, points=grading.POINTS[verdict], regret_mbb=round(regret, 1), best_action=best, best_label=lab[best],
                top_action=best, chosen_action=action_id, gto_action=f['gto'], gto_label=gto_label, good_actions=[], good_labels=[],
                chosen_label=lab[action_id], strategy=[dict(id=a, label_fr=lab[a], pct=100 if a == best else 0, chosen=a == action_id,
                                                             ev_mbb=ev[a]) for a in ids],
                loss_fr=(bbx(regret) if action_id != best and ev[best] is not None else None), ev_source='field', exploit=None,
                field=dict(type=f['type'], type_fr=f['type_fr'], rule=f['rule'], rule_fr=rule_fr, gto_label=gto_label, read=f['type'] in READ,
                           gain_fr=(bbx(f['gain_mbb']) if f['type'] in ('adaptation', 'inconnu') else None), evs=[dict(label_fr=lab[a], ev_fr=bbx(ev[a], True)) for a in ids if ev[a] is not None and a != 'F']),
                why_fr=why, next=postflop_section(sp, f, hand), range=None, explanation_fr='\n'.join(lines), core_fr='\n'.join(lines))


FAMILY_SHARE = {'first_in': 0.31, 'vs_allin': 0.33, 'vs_limp': 0.21, 'vs_raise': 0.10, 'read': 0.05}   # v4.4 (audit), v4.5 : face à l'open


def draw(spots, size, seed=None, filters=None):
    """série : rotation heads-up / 3 joueurs (HU_SHARE), puis famille de décision selon FAMILY_SHARE, tapis tiré à parts égales,
    bonne réponse tirée à parts égales (on ne peut pas répondre « tapis » sans réfléchir), enfin question pondérée par la
    fréquence du profil dans le field. Au plus MAX_TRAPS pièges et MAX_READ question de lecture (sans limite si les filtres ne
    laissent que de la lecture), jamais deux fois la même main ni la même question"""
    rnd = random.Random(seed); out = []; seen = set(); traps = reads = 0; used = set()
    max_read = MAX_READ if any(s['field']['type'] not in READ for s in spots) else size
    max_traps = MAX_TRAPS if any(s['field']['type'] not in ('piège', 'échantillon') for s in spots) else size
    by_table = {t: [s for s in spots if s['table'] == t] for t in ('heads-up', '3-handed')}
    fam = lambda s: 'read' if s['field']['type'] in READ else s['field_family']
    pick = lambda xs, key: rnd.choice(sorted({key(x) for x in xs}, key=str))
    for k in range(size):
        want = 'heads-up' if rnd.random() < HU_SHARE else '3-handed'
        for table in (want, '3-handed' if want == 'heads-up' else 'heads-up'):
            cand = [s for s in by_table[table] if s['spot_id'] not in used
                    and (s['field']['type'] in READ or next(iter(s['hands'])) not in seen)
                    and not (s['field']['type'] in ('piège', 'échantillon') and traps >= max_traps)
                    and not (s['field']['type'] in READ and reads >= max_read)]
            if cand: break
        if not cand: break
        fams = sorted({fam(s) for s in cand}); f0 = rnd.choices(fams, [FAMILY_SHARE.get(x, 0.1) for x in fams])[0]
        cand = [s for s in cand if fam(s) == f0]
        st = pick(cand, lambda s: s['effective_stack_bb']); cand = [s for s in cand if s['effective_stack_bb'] == st]
        ans = pick(cand, lambda s: s['field']['correct']); cand = [s for s in cand if s['field']['correct'] == ans]
        sp = rnd.choices(cand, [max(s['field']['weight'], 1e-3) for s in cand])[0]
        h = next(iter(sp['hands'])); out.append(sp); used.add(sp['spot_id'])
        if h and sp['field']['type'] not in READ: seen.add(h)
        traps += sp['field']['type'] in ('piège', 'échantillon'); reads += sp['field']['type'] in READ
    return [(s['spot_id'], next(iter(s['hands']))) for s in out]


def problems(sp):
    """anomalies d'une question du field (contrôle de publication)"""
    from .cards import NAMES
    p = []; f = sp.get('field')
    if not f: return ['bloc field manquant']
    ids = [o['id'] for o in f['options']]
    if not 2 <= len(ids) <= 5 or len(set(ids)) != len(ids): p.append('de 2 à 5 options distinctes attendues')
    if f['correct'] not in ids: p.append('bonne réponse absente des options')
    if any(a not in ids or a == f['correct'] for a in f['acceptable']): p.append('alternatives acceptées incohérentes')
    hand = next(iter(sp['hands']), None)
    if hand not in NAMES and hand != '': p.append('main inconnue')
    if hand and f['type'] not in ('identification',):
        ev = {o['id']: o['ev_mbb'] for o in f['options']}
        if any(v is None for v in ev.values()): p.append('EV manquante')
        elif ev[f['correct']] < max(ev.values()) - 1e-6: p.append("la bonne réponse n'est pas l'action la plus rentable")
    if f['type'] not in TYPE_FR: p.append('type inconnu')
    if 'mBB' in sp['prompt_fr'] or 'mBB' in ' '.join(f['stats'][i]['label_fr'] for i in range(len(f['stats']))): p.append('montant en mBB affiché')
    if not 4 <= sp['effective_stack_bb'] <= 25: p.append('tapis hors périmètre')
    if f['internal_profile'] and f['internal_profile'] in sp['prompt_fr']: p.append("profil interne visible dans l'énoncé")
    return p


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--version', required=True); ap.add_argument('--seed', type=int, default=SEED)
    a = ap.parse_args(); m = publish(a.version, seed=a.seed)
    print(f"{m['spots']} questions du field ({m['version']}, staging) : {m['by_type']}")

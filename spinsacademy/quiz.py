"""Séries de questions préflop : tirage, énoncé, correction expliquée et bilan.

Une question = un couple (spot, main) parmi les mains proposables (`quiz_eligible`) d'une version de dataset.
Tirage (reproductible avec une graine) :
  - les spots retenus par les filtres sont groupés par famille de décision ; chaque question tire d'abord une
    famille (au hasard, sans remise tant que toutes n'ont pas servi), puis un spot de cette famille, puis une main
    pondérée par sa fréquence naturelle (combos x atteinte) ;
  - pas deux fois le même spot dans une série.
La question envoyée au joueur ne contient jamais la solution.
"""
import json, os, random
from functools import lru_cache
from . import grading, profiles
from .cards import NAMES, W
from .hrc import ROOT

DATASETS = os.path.join(ROOT, 'data', 'datasets')
DEFAULT_VERSION = os.environ.get('SPINSACADEMY_DATASET', '2026.10.13-1')                       # gto_preflop
DEFAULT_EXPLOIT = os.environ.get('SPINSACADEMY_EXPLOIT', 'exploit_calls/2026.10.13-2')
ADAPTATION_SHARE = 0.6            # mode exploitant : part des questions où la bonne réponse diffère du GTO
SERIES_SIZE = 5
SUITS = {'pair': ('♠', '♥'), 's': ('♠', '♠'), 'o': ('♠', '♥')}
FAMILIES = {'premier à parler': 'first_in', 'face à un limp': 'vs_limp', 'face à une relance': 'vs_raise', 'face à un tapis': 'vs_allin'}


def ref_path(ref):
    """« version » (dataset GTO) ou « dataset/version »"""
    return os.path.join(DATASETS, *(ref.split('/', 1) if '/' in ref else ('gto_preflop', ref)))


def is_exploit(ref): return ref.startswith('exploit_')


@lru_cache(maxsize=8)
def load(version=DEFAULT_VERSION):
    d = ref_path(version)
    spots = [json.loads(l) for l in open(os.path.join(d, 'spots.jsonl'))]
    return json.load(open(os.path.join(d, 'manifest.json'))), {s['spot_id']: s for s in spots}


def family(sp):
    prior = [h for h in sp['history'] if h['action'] != 'fold']
    if not prior: return 'first_in'
    if any(h['action'] == 'allin' for h in prior): return 'vs_allin'
    if any(h['action'] == 'raise' for h in prior): return 'vs_raise'
    return 'vs_limp'


# ------------------------------------------------------------------ texte
def bb(x):
    s = f'{x:.2f}'.rstrip('0').rstrip('.')
    return s.replace('.', ',')


GAIN_MIN_BB = grading.TOLERANCE_MBB / 1000   # en dessous : « <0,02 BB », la limite entre réponse acceptée et imprécision (pas de mBB affichés)


def gain_bb(x, signed=False):
    """montant de gain ou de perte affiché au joueur, toujours en BB"""
    s = f'<{bb(GAIN_MIN_BB)} BB' if abs(x) < GAIN_MIN_BB else f'{bb(abs(x))} BB'
    return (('+' if x >= 0 else '−') + s) if signed else s


IMPRECISION_BB = 3 * grading.TOLERANCE_MBB / 1000   # limite entre imprécision et erreur
RANGE_BOUNDS_BB = (GAIN_MIN_BB, IMPRECISION_BB, 0.5, 1, 2, 5)


def gain_range(x):
    """fourchette d'un montant (valeur absolue, en BB) : mode exploitant, où l'hypothèse de profil rend un montant exact trompeur"""
    x = abs(x); b = RANGE_BOUNDS_BB
    if x < b[0]: return f'moins de {bb(b[0])} BB'
    for lo, hi in zip(b, b[1:]):
        if x < hi: return f'entre {bb(lo)} et {bb(hi)} BB'
    return f'plus de {bb(b[-1])} BB'


def hand_display(h):
    if len(h) == 2: a, b = SUITS['pair']
    else: a, b = SUITS[h[2]]
    return f'{h[0]}{a}{h[1]}{b}'


def action_label(sp, a):
    t = a['type']; to = a.get('to_bb')
    if t == 'fold': return 'Fold'
    if t == 'check': return 'Check'
    if t == 'limp': return 'Compléter (1 BB)' if sp['hero'] == 'SB' else 'Limper (1 BB)'
    if t == 'call': return f"Payer ({bb(sp['to_call_bb'])} BB de plus)"
    if t == 'call_allin': return f"Payer le tapis ({bb(sp['to_call_bb'])} BB de plus)"
    if t == 'raise': return f'Relancer à {bb(to)} BB'
    return f'Tapis ({bb(to)} BB)'


def history_text(sp):
    out = []; mine = sp['stacks_bb'][sp['players'].index(sp['hero'])]
    for h in sp['history']:
        p = h['position']; a = h['action']; to = h.get('to_bb')
        if a == 'fold': out.append(f'Le {p} se couche')
        elif a == 'check': out.append(f'Le {p} checke')
        elif a == 'limp': out.append(f"Le {p} {'complète' if p == 'SB' else 'limpe'}")
        elif a == 'call': out.append(f'Le {p} paie {bb(to)} BB')
        elif a == 'call_allin': out.append(f'Le {p} paie le tapis')
        elif a == 'raise': out.append(f'Le {p} relance à {bb(to)} BB')
        elif to is not None and to > mine: out.append(f'Le {p} part à tapis ({bb(to)} BB, soit {bb(mine)} BB effectifs)')   # tapis qui te couvre
        else: out.append(f'Le {p} part à tapis ({bb(to)} BB)')
    return out


def prompt(sp, hand):
    table = '3 joueurs' if sp['table'] == '3-handed' else 'Heads-up'
    stacks = ' / '.join(bb(x) for x in sp['stacks_bb']); pos = ' / '.join(sp['players'])
    hist = history_text(sp)
    parts = [f'{table}, tapis {stacks} BB ({pos}).'] + [h + '.' for h in hist]
    if not hist: parts.append('Personne n\'a encore parlé.')
    v = sp.get('villain')
    if v:
        pr = profiles.for_villain(v)
        parts.append((f"Profil fictif « {pr['name_fr']} » : ce " if pr else 'Ce ') +
                     f"{v['position']} part à tapis avec {bb(v['observed_pct'])} % de ses mains dans cette situation (GTO : {bb(v['gto_pct'])} %).")
    parts.append(f"Tu es au {sp['hero']} avec {hand_display(hand)}. Que fais-tu ?")
    return '\n'.join(parts)                                     # une phrase par ligne (lisibilité sur mobile)


# ------------------------------------------------------------------ tirage
def candidates(spots, filters=None):
    f = filters or {}
    out = []
    for sp in spots.values():
        if f.get('table') and sp['table'] != f['table']: continue
        if f.get('hero') and sp['hero'] != f['hero']: continue
        if f.get('family') and family(sp) != f['family']: continue
        eff = sp['effective_stack_bb']
        if f.get('min_stack') is not None and eff < f['min_stack']: continue
        if f.get('max_stack') is not None and eff > f['max_stack']: continue
        if f.get('profile') and (profiles.for_villain(sp.get('villain')) or {}).get('id') != f['profile']: continue
        if sp['eligible_hands'] > 0: out.append(sp)
    return out


def pool(version, filters=None, excluded=frozenset()):
    """spots proposables d'une version : filtres, spots désactivés (et exploitants dérivés), profil obligatoire en exploitant"""
    _, spots = load(version)
    out = [sp for sp in candidates(spots, filters) if sp['spot_id'] not in excluded and sp.get('base_spot_id') not in excluded]
    if is_exploit(version): out = [sp for sp in out if sp.get('adaptations', 0) > 0 and profiles.for_villain(sp['villain'])]   # pas de profil : pas de conseil
    return out


EASY_MBB = 1000          # la première action sanctionnée coûte plus de 1 BB : question facile, tirée 4 fois moins souvent
HARD_MBB = 200           # moins de 0,2 BB : question difficile
EASY_WEIGHT = 0.25


def lesson_gap(sp, hand):
    """écart (mBB) de l'action sanctionnée la moins coûteuse ; None si toutes les actions sont acceptées (rien à apprendre)"""
    ids = [a['id'] for a in sp['actions']]; gaps = []
    for a in ids:
        g = grading.grade(sp, hand, a)
        if g['verdict'] != 'correct': gaps.append(g['regret_mbb'])
    return min(gaps) if gaps else None


def difficulty(gap):
    if gap is None: return None
    return 'facile' if gap > EASY_MBB else 'difficile' if gap < HARD_MBB else 'moyen'


def _pick_hand(sp, exploit, rnd):
    hands = [h for h in NAMES if sp['hands'][h]['quiz_eligible']]
    if exploit:
        adapt = [h for h in hands if sp['hands'][h]['kind'] == 'adaptation']
        other = [h for h in hands if sp['hands'][h]['kind'] != 'adaptation']
        hands = adapt if adapt and (not other or rnd.random() < ADAPTATION_SHARE) else other
    gaps = {h: lesson_gap(sp, h) for h in hands}
    useful = [h for h in hands if gaps[h] is not None] or hands       # une question où tout est accepté n'apprend rien
    weights = [W[NAMES.index(h)] * sp['hands'][h]['reach'] * (EASY_WEIGHT if (gaps[h] or 0) > EASY_MBB else 1.0) for h in useful]
    return rnd.choices(useful, weights)[0]


def _use(sp, items, used, exploit):
    used.add(sp['spot_id'])
    if exploit:                                                  # pas deux fois la même situation de base (facteurs différents)
        used.update(x['spot_id'] for x in items if x.get('base_spot_id') == sp.get('base_spot_id'))


def draw_series(version=DEFAULT_VERSION, filters=None, size=SERIES_SIZE, seed=None, excluded=frozenset()):
    """[(spot_id, main)] ; ValueError si les filtres ne laissent pas assez de spots.
    excluded : spots désactivés par l'administration (un spot GTO désactivé exclut aussi les spots exploitants qui en dérivent)"""
    rnd = random.Random(seed); items = pool(version, filters, excluded); exploit = is_exploit(version)
    if len(items) < size: raise ValueError(f'{len(items)} spots disponibles pour ces filtres, {size} demandés')
    # rotation sur la position du joueur (BTN, SB, BB), puis sur la famille de décision : sans elle, le BB domine
    by_pos = {}
    for sp in items: by_pos.setdefault(sp['hero'], {}).setdefault(family(sp), []).append(sp)
    pos_order = []; fam_order = {}; used = set(); out = []
    while len(out) < size and by_pos:
        if not pos_order: pos_order = sorted(by_pos); rnd.shuffle(pos_order)
        pos = pos_order.pop(); fams = by_pos.get(pos)
        if not fams: continue
        if not fam_order.get(pos): fam_order[pos] = sorted(fams); rnd.shuffle(fam_order[pos])
        fam = fam_order[pos].pop()
        choices = [sp for sp in fams.get(fam, []) if sp['spot_id'] not in used]
        if not choices:
            fams.pop(fam, None)
            if not fams: by_pos.pop(pos)
            continue
        sp = rnd.choice(choices); _use(sp, items, used, exploit)
        out.append((sp['spot_id'], _pick_hand(sp, exploit, rnd)))
    return out


def draw_plan(version, slots, theme_of, seed=None, excluded=frozenset()):
    """série suivant un plan (spinsacademy.adaptive) : [(spot_id, main, emplacement, thème respecté)].
    Un emplacement sans spot libre pour son thème est complété par un spot quelconque (thème respecté = False)."""
    rnd = random.Random(seed); items = pool(version, None, excluded); exploit = is_exploit(version)
    if len(items) < len(slots): raise ValueError(f'{len(items)} spots disponibles, {len(slots)} demandés')
    used = set(); out = []
    for slot in slots:
        t = tuple(slot['theme']) if slot.get('theme') else None
        choices = [sp for sp in items if sp['spot_id'] not in used and (t is None or theme_of(sp) == t)]
        ok = bool(choices) and t is not None
        if not choices: choices = [sp for sp in items if sp['spot_id'] not in used]
        if not choices: break
        sp = rnd.choice(choices); _use(sp, items, used, exploit)
        out.append((sp['spot_id'], _pick_hand(sp, exploit, rnd), slot, ok))
    return out


def question(version, spot_id, hand):
    """ce que voit le joueur : état du jeu et options, sans solution"""
    _, spots = load(version); sp = spots[spot_id]
    return dict(spot_id=spot_id, hand=hand, hand_display=hand_display(hand), prompt_fr=prompt(sp, hand), table=sp['table'],
                players=sp['players'], stacks_bb=sp['stacks_bb'], hero=sp['hero'], history=sp['history'], history_fr=history_text(sp),
                pot_bb=sp['pot_bb'], to_call_bb=sp['to_call_bb'], family=family(sp), difficulty=difficulty(lesson_gap(sp, hand)), mode='exploit' if sp.get('villain') else 'gto',
                villain=({k: sp['villain'][k] for k in ('position', 'stat', 'observed_pct', 'gto_pct')} if sp.get('villain') else None),
                profile=(profiles.public(profiles.for_villain(sp['villain']), sp['villain']['gto_pct']) if sp.get('villain') else None),
                options=[dict(id=a['id'], label_fr=action_label(sp, a)) for a in sp['actions']])


VERB_FR = {'fold': 'se couche', 'check': 'checke', 'limp': 'limpe', 'call': 'paie', 'call_allin': 'paie', 'raise': 'relance', 'allin': 'part à tapis'}
BASE_FR = 'des mains qui arrivent à cette décision'


def range_grid(sp):
    """stratégie de référence sur les 169 mains (grille 13 x 13) : pourcentages arrondis par action, et part de chaque action"""
    acts = [dict(id=a['id'], type=a['type'], label_fr=action_label(sp, a)) for a in sp['actions']]
    hands = {}; share = [0.0] * len(acts); tot = 0.0
    for i, h in enumerate(NAMES):
        x = sp['hands'][h]
        if x.get('reach', 0) <= 0 or not x.get('freq'): continue
        mix = dict(grading.displayed_mix(sp, h)); hands[h] = [mix.get(a['id'], 0) for a in acts]
        m = W[i] * x['reach']; tot += m
        for j, f in enumerate(x['freq']): share[j] += m * f
    return dict(actions=acts, hands=hands, share_pct=[round(100 * v / tot) if tot else 0 for v in share])


def _pct(x): return f"{round(100 * x)} %"


def _pct1(x): return f"{100 * x:.1f} %".replace('.', ',')


def _low(t): return t[0].lower() + t[1:]


def to_do(sp, aid):
    """l'action à l'infinitif, pour « il fallait … »"""
    a = next(x for x in sp['actions'] if x['id'] == aid); t = a['type']
    if t == 'fold': return 'te coucher'
    if t == 'check': return 'checker'
    if t == 'limp': return 'compléter' if sp['hero'] == 'SB' else 'limper'
    if t == 'allin': return f"partir à tapis ({bb(a['to_bb'])} BB)"
    return _low(action_label(sp, a))


def _named(t):
    """une action citée dans une phrase : entre parenthèses, ou entre guillemets si son libellé en contient déjà"""
    return f'« {_low(t)} »' if '(' in t else f'({_low(t)})'


def _points(x):
    """écart en points d'équité, à une décimale (la bande serrée / moyen / large est calculée sur cette valeur affichée)"""
    n = round(x, 1); return f"{n:.1f} point{'s' if n >= 2 else ''}".replace('.', ',')


CHEAP_BB = IMPRECISION_BB        # « coûte peu » seulement en dessous de la limite d'imprécision


def why(sp, hand, ev, best, labels, grid, chosen=None):
    """« pourquoi », tiré des données : calcul, marge, limites de la décision.
    Call d'un tapis à EV exacte : cote du pot, équité de la main, marge en points, mains qui paient ou se couchent tout juste.
    Ailleurs : part de la stratégie, marge sur la deuxième action, jeu mixte, mains à la frontière."""
    ids = [a['id'] for a in sp['actions']]; types = {a['id']: a['type'] for a in sp['actions']}
    exploit = bool(sp.get('villain')); out = []
    if sp['ev_reference'] == 'exact' and ids == ['F', 'C'] and types['C'] == 'call_allin' and sp['to_call_bb'] > 0:
        call, final = sp['to_call_bb'], sp['pot_bb'] + sp['to_call_bb']; need = call / final
        eq = {}
        for h, x in sp['hands'].items():
            e = (x.get('ev_exact') or [None, None])[1]
            if e is not None and x.get('reach', 0) > 0: eq[h] = (e + call) / final
        have = eq[hand]; margin = round(round(100 * have, 1) - round(100 * need, 1), 1)   # cohérent avec les valeurs affichées
        whose = 'la range de ce type de profil' if exploit else 'sa range de tapis'
        out.append(f"Cote du pot : {bb(call)} BB à payer pour un pot final de {bb(final)} BB, il faut {_pct1(need)} d'équité pour payer.")
        out.append(f"Contre {whose}, {hand} a {_pct1(have)} d'équité : "             # le gain est déjà donné par la ligne principale
                   + (f"marge de {_points(margin)} au-dessus du seuil." if margin >= 0 else f"{_points(-margin)} sous le seuil."))
        right = chosen is None or chosen == best; act = to_do(sp, best)
        loss = 0.0 if right else ev[ids.index(best)] - ev[ids.index(chosen)]
        if abs(margin) < 5:
            out.append("Décision serrée (moins de 5 points d'écart) : " + ("bien vu, mais un petit changement de range adverse ou de tapis peut la renverser." if right else
                       ("ton erreur coûte peu" if loss < CHEAP_BB else f"même serrée, ton erreur coûte {gain_range(loss) if exploit else gain_bb(loss)}")
                       + " ; retiens surtout le seuil d'équité, c'est lui qui tranche."))
        elif abs(margin) <= 10:
            out.append("Écart moyen (5 à 10 points) : " + ("la décision est claire dès que tu estimes bien la range adverse."
                       if right else f"il fallait {act} ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse."))
        else:
            out.append("Écart large (plus de 10 points) : " + ("c'est une décision de principe, à prendre sans hésiter."
                       if right else f"erreur nette, il fallait {act} sans hésiter : la main est loin du seuil."))
        callers = sorted((v, h) for h, v in eq.items() if v >= need); folders = sorted(((v, h) for h, v in eq.items() if v < need), reverse=True)
        if callers and folders:
            out.append(f'À la limite (seuil {_pct1(need)}), payent encore : ' + ', '.join(f'{h} ({_pct1(v)})' for v, h in callers[:3])
                       + ' ; se couchent déjà : ' + ', '.join(f'{h} ({_pct1(v)})' for v, h in folders[:3]) + '.')
        mass = lambda f: sum(W[NAMES.index(h)] * sp['hands'][h]['reach'] for h in eq if f(h)) / max(sum(W[NAMES.index(h)] * sp['hands'][h]['reach'] for h in eq), 1e-12)
        share = mass(lambda h: eq[h] >= need)
        if exploit:
            g = mass(lambda h: (sp['hands'][h].get('ev_gto') or [0, -1])[1] > 0)
            out.append(f"Contre ce type de profil, on paie avec {_pct(share)} {BASE_FR} ; contre un joueur GTO, avec {_pct(g)}.")
        else:
            out.append(f"Ici, on paie avec {_pct(share)} {BASE_FR}.")
        return out
    j = ids.index(best); verb = 'complète' if types[best] == 'limp' and sp['hero'] == 'SB' else VERB_FR[types[best]]
    f = sp['hands'][hand]['freq']; shown = grading.displayed_mix(sp, hand); pj = dict(shown).get(best, 0)
    if f[j] >= 0.5: tail = f"{hand} en fait partie."
    elif pj: tail = f"{hand} le fait {pj} % du temps."
    else: tail = f"{hand} le fait rarement : les actions ont une valeur quasi égale."
    out.append(f"Ici, on {verb} avec {grid['share_pct'][j]} % {BASE_FR} ; {tail}")
    if 'call_allin' in types.values() and sp['to_call_bb'] > 0:       # HRC : la cote du pot n'est qu'un repère
        need = sp['to_call_bb'] / (sp['pot_bb'] + sp['to_call_bb'])
        out.append(f"Repère : il faut environ {_pct(need)} d'équité pour payer (cote du pot ; approximatif quand un joueur reste à parler ou qu'un tapis est couvert).")
    order = sorted(range(len(ids)), key=lambda k: -ev[k]); base_id = 'F' if 'F' in ids else 'X'
    if len(order) > 1:
        second = ids[order[1]]
        if second != chosen and second != base_id:                 # sinon déjà dit dans l'explication principale
            out.append(f"Deuxième option : {_low(labels[second])}, {gain_bb(ev[j] - ev[order[1]])} de moins.")
    if len(shown) > 1:
        mix = ', '.join(f'{_low(labels[a])} {p} %' for a, p in shown); played = dict(shown)
        if chosen is not None and chosen not in played:
            out.append(f"{hand} est jouée en mixte ({mix}) : ces actions ont une valeur proche. Ton choix {_named(labels[chosen])} n'en fait pas partie.")
        else:
            out.append(f"{hand} est jouée en mixte ({mix}) : ces actions ont une valeur proche, chacune est acceptée.")
    edge = sorted(((abs(x['freq'][j] - 0.5), h) for h, x in sp['hands'].items()
                   if x.get('reach', 0) >= 0.05 and x.get('freq') and 0.2 <= x['freq'][j] <= 0.8 and h != hand))
    if edge:
        out.append(f"Mains jouées en mixte pour l'action « {_low(labels[best])} » : {', '.join(h for _, h in edge[:5])}.")
    else:
        out.append(f"Aucune main n'est jouée en mixte pour l'action « {_low(labels[best])} » : la frontière est nette.")
    return out


_POSTFLOP = None
POSTFLOP_FILE = os.path.join(os.path.dirname(__file__), 'data', 'postflop_profiles.json')
POSTFLOP_ORDER = {3: ('SB', 'BB', 'BTN'), 2: ('BB', 'SB')}       # ordre de parole après le flop
_R = '23456789TJQKA'


def postflop_profile(hand):
    global _POSTFLOP
    if _POSTFLOP is None: _POSTFLOP = json.load(open(POSTFLOP_FILE))
    return _POSTFLOP['hands'][hand]


def overcard_prob(hand):
    """paire servie : probabilité qu'au moins une carte du flop soit plus haute que la paire (52 - 2 cartes connues)"""
    from math import comb
    higher = 4 * (12 - _R.index(hand[0]))
    return 1 - comb(50 - higher, 3) / comb(50, 3)


_OVERCARD_AVG = None


def _overcard_avg():
    global _OVERCARD_AVG
    if _OVERCARD_AVG is None: _OVERCARD_AVG = sum(overcard_prob(r + r) for r in _R) / 13
    return _OVERCARD_AVG


def next_steps(sp, hand, best, chosen=None, labels=None):
    """« Et ensuite ? » : forces et faiblesses de la main après le flop (énumération exacte des flops, data/postflop_profiles.json).
    Le sujet est toujours la bonne action ; quand le joueur en a choisi une autre, l'intro le dit."""
    t = {a['id']: a['type'] for a in sp['actions']}[best]
    p = postflop_profile(hand); pc = lambda x: f"{round(100 * x)} %"
    pair = len(hand) == 2; suited = hand.endswith('s'); hi, lo = _R.index(hand[0]), _R.index(hand[1])
    subject = (f"Avec la bonne action {_named(labels[best])} : " if labels and chosen and chosen != best else '')
    say = lambda x: subject + (_low(x) if subject else x)
    empty = dict(position=None, metrics=[], forces=[], weaknesses=[])
    if family(sp) == 'vs_allin':
        return dict(empty, intro=say("Face à un tapis, seule compte ton équité contre sa range : voir la cote du pot."))
    if t == 'allin':
        return dict(empty, intro=say("Tu pousses : soit l'adversaire se couche et tu prends le pot, soit il paie et tout se joue à l'équité, sans décision après le flop."))
    if t == 'call_allin':
        return dict(empty, intro=say("Tu paies le tapis : plus aucune décision après le flop, seule compte ton équité contre sa range."))
    intro = say("Tu te couches : pas de postflop ici. Voici ce que cette main ferait au flop, pour comprendre pourquoi." if t == 'fold' else
                       "Après le flop, voici ce que tu peux attendre de cette main (sur tous les flops possibles).")
    folded = {h['position'] for h in sp['history'] if h['action'] == 'fold'}
    order = [x for x in POSTFLOP_ORDER[len(sp['players'])] if x not in folded]
    position = None
    if t != 'fold' and sp['hero'] in order and len(order) > 1:
        position = ("Tu joueras en position : tu parles en dernier à chaque tour, tu vois ce que font les autres avant de décider." if order[-1] == sp['hero'] else
                    "Tu joueras hors position : tu parles en premier à chaque tour, ce qui rend la main plus difficile à jouer et réduit l'équité que tu réalises.")
    postflop_profile(hand); au, ap = _POSTFLOP['average_unpaired'], _POSTFLOP['average_pairs']
    forces, weak = [], []
    if pair:
        over = overcard_prob(hand)
        forces.append(f"Brelan ou mieux au flop {pc(p['set_plus'])} du temps (environ 1 fois sur 8).")
        if p['overpair'] >= 0.3: forces.append(f"Ta paire reste plus haute que les trois cartes du board {pc(p['overpair'])} du temps.")
        if over >= 0.5: weak.append(f"Au moins une carte plus haute que ta paire arrive au flop {pc(over)} du temps.")
    else:
        if p['top_pair_plus'] >= 0.25: forces.append(f"Paire max ou mieux au flop {pc(p['top_pair_plus'])} du temps.")
        if suited: forces.append(f"Tirage couleur ou couleur faite au flop {pc(p['flush_draw_plus'])} du temps.")
        if p['oesd_plus'] >= 0.05 or p['gutshot'] >= 0.12:
            forces.append(f"Potentiel de quinte : tirage par les deux bouts ou mieux {pc(p['oesd_plus'])} du temps, tirage ventral {pc(p['gutshot'])}.")
        if p['miss'] > au['miss'] + 0.005:
            weak.append(f"Tu rates le flop {pc(p['miss'])} du temps, sans paire ni tirage fort (moyenne des mains non pairées : {pc(au['miss'])}).")
        if hi >= _R.index('T') and lo <= _R.index('7'):
            weak.append(f"Quand ton {hand[0]} touche, ton kicker {hand[1]} est faible : tu risques d'être dominé par les {hand[0]}x plus forts.")
        elif p['top_pair_plus'] < au['top_pair_plus'] - 0.005:
            weak.append(f"Paire max ou mieux seulement {pc(p['top_pair_plus'])} du temps (moyenne des mains non pairées : {pc(au['top_pair_plus'])}) : tes paires seront souvent battues.")
        if not suited and p['oesd_plus'] < 0.05 and hi - lo >= 4:
            weak.append("Peu de potentiel de tirage : main dépareillée et déconnectée.")
    eq = float(_VSR()[NAMES.index(hand)])
    if eq >= 0.55: forces.append(f"Contre une main au hasard, {hand} a {pc(eq)} d'équité (tapis préflop).")
    elif eq < 0.42: weak.append(f"Main faible à l'abattage : contre une main au hasard, {hand} n'a que {pc(eq)} d'équité (tapis préflop).")
    cmp = lambda v, a: 'equal' if abs(v - a) < 0.005 else 'above' if v > a else 'below'
    tone = lambda c, lower: 'neutral' if c == 'equal' else ('good' if (c == 'above') != lower else 'bad')
    if pair:                                                     # une paire se compare aux paires, une main non pairée aux non pairées
        ref = 'des paires servies'
        rows = (('set_plus', 'Brelan ou mieux', p['set_plus'], ap['set_plus'], False),
                ('overpair', 'Paire plus haute que le board', p['overpair'], ap['overpair'], False),
                ('overcard', 'Carte plus haute que ta paire au board (moins, c\'est mieux)', overcard_prob(hand), _overcard_avg(), True))
    else:
        ref = 'des mains non pairées'
        rows = tuple((k, l, p[k], au[k], False) for k, l in (('top_pair_plus', 'Paire max ou mieux'), ('two_pair_plus', 'Deux paires ou mieux'),
                                                             ('draw_plus', 'Tirage couleur ou quinte (ou mieux)')))
    metrics = [dict(key=k, label_fr=l, value=v, average=a, compare=cmp(v, a), tone=tone(cmp(v, a), lower), lower_is_better=lower, reference_fr=ref)
               for k, l, v, a, lower in rows]
    return dict(intro=intro, position=position, metrics=metrics, forces=forces[:3], weaknesses=weak[:3])


_VSR_CACHE = None


def _VSR():
    """équité de chaque classe contre une main au hasard, en tenant compte des cartes retirées (combos disjoints)"""
    global _VSR_CACHE
    if _VSR_CACHE is None:
        from .allin import E
        from .cards import DISJOINT
        _VSR_CACHE = (E * DISJOINT).sum(1) / DISJOINT.sum(1)
    return _VSR_CACHE


def correct(version, spot_id, hand, action_id):
    """correction et explication structurée (données du dataset uniquement)"""
    _, spots = load(version); sp = spots[spot_id]
    g = grading.grade(sp, hand, action_id)
    labels = {a['id']: action_label(sp, a) for a in sp['actions']}
    ev = grading.reference_ev(sp, hand)
    mix = grading.displayed_mix(sp, hand)
    best = g['best_action']; ids = [a['id'] for a in sp['actions']]
    base_id = 'F' if 'F' in ids else 'X'                     # référence : fold, ou check quand rien n'est à payer
    evb = ev[ids.index(best)] - ev[ids.index(base_id)]
    ref = 'fold' if base_id == 'F' else 'check'
    if best == base_id or abs(evb) < 0.005: lines = [f'Meilleure action : {labels[best]}.']
    elif evb < GAIN_MIN_BB: lines = [f"Meilleure action : {labels[best]}, à peine mieux que le {ref} (moins de {bb(GAIN_MIN_BB)} BB)."]
    else: lines = [f"Meilleure action : {labels[best]}, {gain_bb(evb, signed=True)} par rapport au {ref}."]
    grid = range_grid(sp); because = why(sp, hand, ev, best, labels, grid, action_id); after = next_steps(sp, hand, best, action_id, labels)
    if action_id == best:
        lines.append('Tu as choisi la meilleure action.')
    else:
        r = g['regret_mbb']
        lines.append(f"Ton choix {_named(labels[action_id])} rapporte {gain_bb(r / 1000)} de moins.")
        tol, imp = bb(grading.TOLERANCE_MBB / 1000).replace('.', ','), bb(3 * grading.TOLERANCE_MBB / 1000).replace('.', ',')
        if g['verdict'] == 'correct' and g['regret_mbb'] > grading.TOLERANCE_MBB:
            lines.append(f"La stratégie de référence joue cette action {_pct(g['chosen_frequency'])} du temps (jeu mixte) : elle est acceptée.")
        elif g['verdict'] == 'correct':
            lines.append(f'Écart sous {tol} BB, dans le bruit de calcul : réponse acceptée.')
        elif g['verdict'] == 'imprécision':
            lines.append(f'Écart entre {tol} et {imp} BB : imprécision, pas erreur.')
        else:
            lines.append(f'Écart au-delà de {imp} BB : erreur.')
    v = sp.get('villain'); h = sp['hands'][hand]; ex = None; core = None
    if v:
        pr = profiles.for_villain(v)
        if pr is None: raise ValueError('aucun profil fictif ne correspond à ce spot : pas de conseil exploitant')
        eg, ee = h['ev_gto'][1], h['ev_exact'][1]; gto = h['gto_action']; changed = gto != best
        conf = profiles.confidence(1000 * ee); verb = 'gagne' if ee >= 0 else 'perd'
        ex = dict(profile=dict(profiles.public(pr, v['gto_pct']), adaptation_fr=pr['adaptation_fr'], tendency_rule_fr=pr['tendency']['rule_fr'], scope_fr=pr['scope_fr']),
                  # 1. référence exploitante : la bonne action contre ce profil, et l'enjeu en fourchette
                  reference_fr=(f"{labels[best]}.\nTon choix {_named(labels[action_id])} perd {gain_range(g['regret_mbb'] / 1000)}." if action_id != best
                                else f"{labels[best]}.\nContre ce type de profil, le call {verb} {gain_range(ee)}."),
                  # 2. comparaison avec la référence GTO
                  comparison_fr=(f"En GTO, ce serait {labels[gto]}.\n{pr['adaptation_fr']}" if changed else
                                 "Même décision qu'en GTO : l'écart de range ne suffit pas à la changer."),
                  tendency_fr=f"Ce {v['position']} part à tapis avec {bb(v['observed_pct'])} % de ses mains (GTO : {bb(v['gto_pct'])} %).",
                  choice_loss_fr=(gain_range(g['regret_mbb'] / 1000) if action_id != best else None),
                  changed=changed, confidence=conf, confidence_fr='enjeu net' if conf == 'élevée' else 'enjeu faible',
                  note_fr="Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.")
        core = [f"Contre ce type de profil « {pr['name_fr']} » : {ex['reference_fr']}", ex['comparison_fr'], ex['note_fr']]
        lines = core[:1] + because + core[1:]
    else:
        core = list(lines); lines += because                     # la stratégie arrondie est affichée à part (barres et grille)
    return dict(verdict=g['verdict'], points=g['points'], regret_mbb=g['regret_mbb'], best_action=best, best_label=labels[best],
                gto_action=(h['gto_action'] if v else None), gto_label=(labels[h['gto_action']] if v else None),
                chosen_label=labels[action_id], strategy=[dict(id=a, label_fr=labels[a], pct=p) for a, p in mix],
                ev_source=g['ev_source'], exploit=ex, why_fr=because, next=after, range=grid, explanation_fr='\n'.join(lines),   # une phrase par ligne
                core_fr='\n'.join(core) if core is not None else None)


def summary(version, answers):
    """answers : [(spot_id, main, résultat de correct())] -> bilan de la série"""
    _, spots = load(version); n = len(answers)
    pts = sum(r['points'] for _, _, r in answers)
    by = {}
    for sid, h, r in answers:
        k = (family(spots[sid]), spots[sid]['hero']); b = by.setdefault(k, [0, 0.0]); b[0] += 1; b[1] += r['points']
    errors = sorted([dict(spot_id=sid, hand=h, prompt_fr=prompt(spots[sid], h), chosen=r['chosen_label'], best=r['best_label'], regret_mbb=r['regret_mbb'])
                     for sid, h, r in answers if r['verdict'] != 'correct'], key=lambda e: -e['regret_mbb'])
    return dict(questions=n, points=pts, score_pct=round(100 * pts / n, 1) if n else 0.0,
                verdicts={v: sum(1 for *_, r in answers if r['verdict'] == v) for v in grading.POINTS},
                by_theme=[dict(family=f, hero=p, questions=c, points=s) for (f, p), (c, s) in sorted(by.items())],
                errors=errors, review=[e['prompt_fr'] for e in errors[:3]])

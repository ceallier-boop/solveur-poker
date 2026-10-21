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
from . import field, grading, profiles
from .cards import NAMES, W
from .hrc import ROOT

DATASETS = os.path.join(ROOT, 'data', 'datasets')
DEFAULT_VERSION = os.environ.get('SPINSACADEMY_DATASET', '2026.10.13-3')                       # gto_preflop
DEFAULT_EXPLOIT = os.environ.get('SPINSACADEMY_EXPLOIT', 'exploit_calls/2026.10.14-1')
DEFAULT_FIELD = os.environ.get('SPINSACADEMY_FIELD', 'exploit_field/2026.10.20-4')                 # mode « Field » (spinsacademy.field)
MODES = ('gto', 'exploit', 'field')
ADAPTATION_SHARE = 0.6            # mode exploitant : part des questions où la bonne réponse diffère du GTO
SERIES_SIZE = 5
SUITS = {'pair': ('♠', '♥'), 's': ('♠', '♠'), 'o': ('♠', '♥')}
FAMILIES = {'premier à parler': 'first_in', 'face à un limp': 'vs_limp', 'face à une relance': 'vs_raise', 'face à un tapis': 'vs_allin'}


def ref_path(ref):
    """« version » (dataset GTO) ou « dataset/version »"""
    return os.path.join(DATASETS, *(ref.split('/', 1) if '/' in ref else ('gto_preflop', ref)))


def is_exploit(ref): return ref.startswith('exploit_calls')


def is_field(ref): return ref.startswith('exploit_field')


def mode_of(ref):
    """mode d'entraînement d'une version de dataset : gto, exploit (profils fictifs) ou field (joueurs du field)"""
    return 'field' if is_field(ref) else 'exploit' if is_exploit(ref) else 'gto'


@lru_cache(maxsize=8)
def load(version=DEFAULT_VERSION):
    d = ref_path(version)
    spots = [json.loads(l) for l in open(os.path.join(d, 'spots.jsonl'))]
    by_id = {s['spot_id']: s for s in spots}; _index_nodes(by_id)
    return json.load(open(os.path.join(d, 'manifest.json'))), by_id


def family(sp):
    if sp.get('field_family'): return sp['field_family']        # mode Field : famille portée par la question (« read » sans main)
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


IMPRECISION_BB = 3 * grading.TOLERANCE_MBB / 1000   # limite entre imprécision et erreur
PERTINENT_BB = grading.PERTINENT_MBB / 1000   # EV HRC : en dessous, l'autre action reste « pertinente » (nuance)
NEAR_BB = 0.005                   # autour de la limite d'imprécision : 3 décimales, pour que montant et verdict concordent


def gain_bb(x, signed=False):
    """montant de gain ou de perte affiché au joueur, toujours en BB. Les bornes suivent la notation : jusqu'à 0,02 BB
    compris « <0,02 BB » (accepté) ; tout près de 0,06 BB, on dit de quel côté on est (imprécision jusqu'à 0,06 inclus)."""
    a = abs(x)
    if a <= GAIN_MIN_BB + 1e-12: s = f'<{bb(GAIN_MIN_BB)} BB'
    elif a - GAIN_MIN_BB < 0.0005: s = f'un peu plus de {bb(GAIN_MIN_BB)} BB'
    elif abs(a - IMPRECISION_BB) < 0.0005: s = f"un peu {'plus' if a > IMPRECISION_BB + 1e-12 else 'moins'} de {bb(IMPRECISION_BB)} BB"
    elif abs(a - IMPRECISION_BB) < NEAR_BB or a - GAIN_MIN_BB < NEAR_BB or abs(a - PERTINENT_BB) < NEAR_BB: s = f'{a:.3f} BB'.replace('.', ',')
    else: s = f'{bb(a)} BB'
    return (('+' if x >= 0 else '−') + s) if signed else s


RANGE_BOUNDS_BB = (GAIN_MIN_BB, IMPRECISION_BB, 0.5, 1, 2, 5)


def gain_range(x):
    """fourchette d'un montant (valeur absolue, en BB) : mode exploitant, où l'hypothèse de profil rend un montant exact trompeur.
    Les deux premières bornes sont incluses dans la fourchette du dessous, comme dans la notation."""
    x = abs(x); b = RANGE_BOUNDS_BB
    if x <= b[0] + 1e-12: return f'moins de {bb(b[0])} BB'
    for lo, hi in zip(b, b[1:]):
        if x < hi or (hi == IMPRECISION_BB and x <= hi + 1e-12): return f'entre {bb(lo)} et {bb(hi)} BB'
    return f'plus de {bb(b[-1])} BB'


def hand_display(h):
    if len(h) == 2: a, b = SUITS['pair']
    else: a, b = SUITS[h[2]]
    return f'{h[0]}{a}{h[1]}{b}'


def bb1(x):
    return f'{x:.1f}'.rstrip('0').rstrip('.').replace('.', ',')


def call_terms(sp):
    """(à payer, pot final) d'un call, plafonnés au tapis du joueur : l'excédent d'un tapis qui le couvre lui est rendu"""
    a = next((x for x in sp['actions'] if x['type'] in ('call', 'call_allin')), None)
    call = sp['to_call_bb']
    if a and a.get('to_bb') is not None: call = min(call, a['to_bb'] - sp['hero_committed_bb'])
    return call, sp['pot_bb'] - (sp['to_call_bb'] - call) + call


PREFLOP_ORDER = {3: ('BTN', 'SB', 'BB'), 2: ('SB', 'BB')}


def commitments(sp):
    """mise engagée par chaque joueur, blindes comprises, à ce point du coup"""
    n = len(sp['players']); c = dict(zip(sp['players'], [0.0, 0.5, 1.0] if n == 3 else [0.5, 1.0]))
    for h in sp['history']:
        if h.get('to_bb') is not None: c[h['position']] = h['to_bb']
    return c


def to_act_after(sp):
    """adversaires qui auront encore à parler après le joueur dans ce tour : ceux qui n'ont pas encore parlé, et ceux qui
    ont déjà parlé mais doivent compléter une mise plus haute (ni couchés, ni à tapis)"""
    acted = {h['position'] for h in sp['history']}; c = commitments(sp); top = max(c.values())
    allin = {h['position'] for h in sp['history'] if h['action'] in ('allin', 'call_allin')}
    return [p for p in opponents_in(sp) if p not in allin and (p not in acted or c[p] < top - 1e-9)]


def opponents_in(sp):
    folded = {h['position'] for h in sp['history'] if h['action'] == 'fold'}
    return [p for p in sp['players'] if p != sp['hero'] and p not in folded]


def stack_of(sp, pos): return sp['stacks_bb'][sp['players'].index(pos)]


def hero_effective(sp):
    """tapis effectif du joueur : le plus petit entre son tapis et le plus gros tapis adverse encore dans le coup"""
    return min(stack_of(sp, sp['hero']), max(stack_of(sp, p) for p in opponents_in(sp)))


def action_label(sp, a):
    t = a['type']; to = a.get('to_bb')
    if t == 'fold': return 'Fold'
    if t == 'check': return 'Check'
    if t == 'limp': return 'Compléter (0,5 BB de plus)' if sp['hero'] == 'SB' else 'Limper (1 BB)'
    if t == 'call': return f"Payer ({bb(call_terms(sp)[0])} BB de plus)"
    if t == 'call_allin': return f"Payer le tapis ({bb(call_terms(sp)[0])} BB de plus)"
    if t == 'raise': return f'Relancer à {bb1(to)} BB'
    eff = hero_effective(sp)
    return f'Tapis ({bb(to)} BB, {bb(eff)} BB effectifs)' if to > eff + 1e-9 else f'Tapis ({bb(to)} BB)'


def history_text(sp):
    """historique ; le joueur à la 2e personne ; un tapis plus gros que le tien est dit en BB effectifs"""
    out = []; mine = stack_of(sp, sp['hero'])
    for h in sp['history']:
        p = h['position']; a = h['action']; to = h.get('to_bb'); me = p == sp['hero']
        if a == 'fold': out.append('Tu te couches' if me else f'Le {p} se couche')
        elif a == 'check': out.append('Tu checkes' if me else f'Le {p} checke')
        elif a == 'limp': out.append(('Tu complètes' if p == 'SB' else 'Tu limpes') if me else f"Le {p} {'complète' if p == 'SB' else 'limpe'}")
        elif a == 'call': out.append(f'Tu paies {bb(to)} BB' if me else f'Le {p} paie {bb(to)} BB')
        elif a == 'call_allin': out.append('Tu paies le tapis' if me else f'Le {p} paie le tapis')
        elif a == 'raise': out.append(f'Tu relances à {bb1(to)} BB' if me else f'Le {p} relance à {bb1(to)} BB')
        elif me: out.append(f'Tu pars à tapis ({bb(to)} BB)')
        else:
            full = stack_of(sp, p)
            out.append(f'Le {p} part à tapis ({bb(full)} BB, soit {bb(mine)} BB effectifs)' if full > mine + 1e-9 else f'Le {p} part à tapis ({bb(full)} BB)')
    return out


def prompt(sp, hand):
    if sp.get('field'): return sp['prompt_fr']
    table = '3 joueurs' if sp['table'] == '3-handed' else 'Heads-up'
    stacks = ' / '.join(bb(x) for x in sp['stacks_bb']); pos = ' / '.join(sp['players'])
    hist = history_text(sp)
    parts = [f'{table}, tapis {stacks} BB ({pos}).'] + [h + '.' for h in hist]
    if not hist: parts.append('Personne n\'a encore parlé.')
    v = sp.get('villain')
    if v:
        pr = profiles.for_villain(v)
        parts.append((f"Profil fictif « {pr['name_fr']} » : ce " if pr else 'Ce ') + f"{v['position']} {tendency_text(v)}"
                     f" ({ref_names(sp)['short']} : {bb(v['gto_pct'])} %).")
    if sp.get('push_fold'): parts.append('Tu joues en tapis ou fold.')
    parts.append(f"Tu es au {sp['hero']} avec {hand_display(hand)}. Que fais-tu ?")
    return '\n'.join(parts)                                     # une phrase par ligne (lisibilité sur mobile)


def tendency_text(v, here='dans cette situation'):
    """statistique observée du vilain, après « ce BB » : « part à tapis avec 54 % de ses mains dans cette situation »"""
    what = 'paie un tapis' if v['stat'] == 'call_pct' else 'part à tapis'
    return f"{what} avec {bb(v['observed_pct'])} % de ses mains {here}"


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
        if not MIN_STACK_BB <= hero_effective(sp) <= MAX_STACK_BB: continue   # périmètre : de 4 à 25 BB de tapis effectif
        if sp.get('villain') and not adapts(sp): continue          # mode exploitant : le profil ne change pas la part de calls
        if sp['eligible_hands'] > 0 and teachable(sp): out.append(sp)
    return out


MIN_ADAPT_POINTS = 2              # mode exploitant : écart minimal de part de calls entre le profil et le GTO


def call_shares(sp):
    """(part des mains qui paient contre le profil, part contre un joueur GTO), pondérées par combos et atteinte"""
    tot = prof = gto = 0.0
    for h, x in sp['hands'].items():
        if x.get('reach', 0) <= 0 or not x.get('ev_exact') or x['ev_exact'][1] is None: continue
        m = W[NAMES.index(h)] * x['reach']; tot += m
        prof += m * (x['ev_exact'][1] > 0); gto += m * ((x.get('ev_gto') or [0, -1])[1] > 0)
    return (prof / tot, gto / tot) if tot else (0.0, 0.0)


def adapts(sp):
    a, b = call_shares(sp); return abs(a - b) * 100 >= MIN_ADAPT_POINTS


def pool(version, filters=None, excluded=frozenset()):
    """spots proposables d'une version : filtres, spots désactivés (et exploitants dérivés), profil obligatoire en exploitant"""
    _, spots = load(version)
    out = [sp for sp in candidates(spots, filters) if sp['spot_id'] not in excluded and sp.get('base_spot_id') not in excluded]
    if is_exploit(version): out = [sp for sp in out if sp.get('adaptations', 0) > 0 and profiles.for_villain(sp['villain'])]   # pas de profil : pas de conseil
    return out


EASY_MBB = 1000          # la première action sanctionnée coûte plus de 1 BB : question facile, tirée 4 fois moins souvent
HARD_MBB = 200           # moins de 0,2 BB : question difficile


def lesson_gap(sp, hand):
    """écart (mBB) de l'action sanctionnée la moins coûteuse ; None si toutes les actions sont acceptées (rien à apprendre)"""
    ids = [a['id'] for a in sp['actions']]; gaps = []
    for a in ids:
        g = grading.grade(sp, hand, a)
        if g['verdict'] != 'correct': gaps.append(g['regret_mbb'])
    return min(gaps) if gaps else None


def error_gap(sp, hand):
    """écart (mBB) de l'action notée « erreur » la moins coûteuse ; None s'il n'y en a pas"""
    gaps = [g['regret_mbb'] for g in (grading.grade(sp, hand, a['id']) for a in sp['actions']) if g['verdict'] == 'erreur']
    return min(gaps) if gaps else None


def difficulty(gap):
    if gap is None: return None
    return 'facile' if gap > EASY_MBB else 'difficile' if gap < HARD_MBB else 'moyen'


MIN_STACK_BB, MAX_STACK_BB = 4, 25
HRC_NOISE_MBB = 150      # EV HRC : écart médian avec l'EV exacte ≈ 58 mBB, 90e centile ≈ 250 mBB (relecture du 2026-10-13)
_TEACH = {}


def impossible_ev(sp, hand):
    """vrai si l'EV de référence d'un call perd plus que le montant à payer : impossible en chip EV (au pire on perd sa mise),
    c'est un artefact du calcul HRC (évaluation du 2026-10-14 : 304 cas). La main n'est pas tirée."""
    ev = grading.reference_ev(sp, hand); call = None
    for a, e in zip(sp['actions'], ev):
        if a['type'] in ('call', 'call_allin') and e is not None:
            call = call if call is not None else call_terms(sp)[0]
            if -e > call + 0.005: return True
    return False


def teachable(sp):
    """mains proposables dont la leçon dépasse le bruit du calcul : une action sanctionnée existe et, sur une EV HRC,
    la moins chère coûte au moins HRC_NOISE_MBB. Les seuils de notation ne changent pas : on ne tire simplement pas les
    questions dont le verdict tiendrait dans l'imprécision de HRC. Le seuil porte sur la moins chère des vraies erreurs : une
    action proche (moins de grading.PERTINENT_MBB) n'empêche pas la question, elle reçoit une nuance."""
    if sp.get('field'): return list(sp['hands'])                  # mode Field : une question = une main (ou aucune)
    k = id(sp)
    if k not in _TEACH:
        floor = 0.0 if sp['ev_reference'] == 'exact' else HRC_NOISE_MBB
        out = []
        for h in NAMES:
            if not sp['hands'][h].get('quiz_eligible') or impossible_ev(sp, h): continue
            g = error_gap(sp, h)                       # la moins chère des vraies erreurs (les actions « pertinentes » ont une nuance)
            if g is not None and g >= floor: out.append(h)
        _TEACH[k] = (sp, out)                                      # garder sp : l'identifiant reste valable
    return _TEACH[k][1]


EASY_SHARE = 0.06         # part visée des questions faciles tirées à dessein ; avec les spots qui n'offrent que des faciles, le total reste sous le plafond validé de 15 %
HU_SHARE = 0.35          # part visée de questions heads-up (validée le 2026-10-14)


def _pick_hand(sp, exploit, rnd, seen=frozenset()):
    """main d'une question : jamais deux fois la même main dans une série si possible ; une question facile
    (la moins chère des réponses fausses coûte plus de 1 BB) seulement EASY_SHARE du temps quand le spot offre mieux"""
    hands = list(teachable(sp))
    if exploit:
        adapt = [h for h in hands if sp['hands'][h]['kind'] == 'adaptation']
        other = [h for h in hands if sp['hands'][h]['kind'] != 'adaptation']
        hands = adapt if adapt and (not other or rnd.random() < ADAPTATION_SHARE) else other
    hands = [h for h in hands if h not in seen] or hands
    gaps = {h: lesson_gap(sp, h) for h in hands}
    useful = [h for h in hands if gaps[h] is not None] or hands       # une question où tout est accepté n'apprend rien
    easy = [h for h in useful if (gaps[h] or 0) > EASY_MBB]; rest = [h for h in useful if h not in easy]
    pool_ = easy if easy and (not rest or rnd.random() < EASY_SHARE) else rest
    weights = [W[NAMES.index(h)] * sp['hands'][h]['reach'] ** 0.5 for h in pool_]   # racine : les mains qui atteignent tous les nœuds (AA…) ne dominent plus
    return rnd.choices(pool_, weights)[0]


def _use(sp, items, used, exploit):
    used.add(sp['spot_id'])
    if exploit:                                                  # pas deux fois la même situation de base (facteurs différents)
        used.update(x['spot_id'] for x in items if x.get('base_spot_id') == sp.get('base_spot_id'))


def draw_series(version=DEFAULT_VERSION, filters=None, size=SERIES_SIZE, seed=None, excluded=frozenset()):
    """[(spot_id, main)] ; ValueError si les filtres ne laissent pas assez de spots.
    Mode Field : tirage propre aux questions fixes (spinsacademy.field.draw).
    excluded : spots désactivés par l'administration (un spot GTO désactivé exclut aussi les spots exploitants qui en dérivent).
    Tirage : format (heads-up HU_SHARE du temps quand les filtres le permettent), puis rotation sur la position du joueur
    et sur la famille de décision (sans elle, le BB domine) ; une main ne revient pas deux fois dans la série."""
    rnd = random.Random(seed); items = pool(version, filters, excluded); exploit = is_exploit(version)
    if len(items) < size: raise ValueError(f'{len(items)} spots disponibles pour ces filtres, {size} demandés')
    if is_field(version):
        out = field.draw(items, size, seed)
        if len(out) < size: raise ValueError(f'{len(out)} questions du field disponibles pour ces filtres, {size} demandées')
        return out
    tree = {}
    for sp in items: tree.setdefault(sp['table'], {}).setdefault(sp['hero'], {}).setdefault(family(sp), []).append(sp)
    pos_order = {}; fam_order = {}; used = set(); seen = set(); out = []
    while len(out) < size and tree:
        tables = sorted(tree)
        table = (('heads-up' if rnd.random() < HU_SHARE else '3-handed') if set(tables) == {'heads-up', '3-handed'} else tables[0])
        by_pos = tree[table]
        if not pos_order.get(table): pos_order[table] = sorted(by_pos); rnd.shuffle(pos_order[table])
        pos = pos_order[table].pop(); fams = by_pos.get(pos)
        if not fams: continue
        key = (table, pos)
        if not fam_order.get(key): fam_order[key] = sorted(fams); rnd.shuffle(fam_order[key])
        fam = fam_order[key].pop()
        choices = [sp for sp in fams.get(fam, []) if sp['spot_id'] not in used]
        if not choices:
            fams.pop(fam, None)
            if not fams: by_pos.pop(pos, None)
            if not by_pos: tree.pop(table)
            continue
        sp = rnd.choice(choices); _use(sp, items, used, exploit)
        h = _pick_hand(sp, exploit, rnd, seen); seen.add(h)
        out.append((sp['spot_id'], h))
    return out


def draw_plan(version, slots, theme_of, seed=None, excluded=frozenset()):
    """série suivant un plan (spinsacademy.adaptive) : [(spot_id, main, emplacement, thème respecté)].
    Un emplacement sans spot libre pour son thème est complété par un spot quelconque (thème respecté = False)."""
    rnd = random.Random(seed); items = pool(version, None, excluded); exploit = is_exploit(version)
    if len(items) < len(slots): raise ValueError(f'{len(items)} spots disponibles, {len(slots)} demandés')
    used = set(); seen = set(); out = []
    for slot in slots:
        t = tuple(slot['theme']) if slot.get('theme') else None
        choices = [sp for sp in items if sp['spot_id'] not in used and (t is None or theme_of(sp) == t)]
        ok = bool(choices) and t is not None
        if not choices: choices = [sp for sp in items if sp['spot_id'] not in used]
        if not choices: break
        sp = rnd.choice(choices); _use(sp, items, used, exploit)
        h = _pick_hand(sp, exploit, rnd, seen); seen.add(h)
        out.append((sp['spot_id'], h, slot, ok))
    return out


def question(version, spot_id, hand):
    """ce que voit le joueur : état du jeu et options, sans solution"""
    _, spots = load(version); sp = spots[spot_id]
    if sp.get('field'): return field.question(sp)
    return dict(spot_id=spot_id, hand=hand, hand_display=hand_display(hand), prompt_fr=prompt(sp, hand), table=sp['table'],
                players=sp['players'], stacks_bb=sp['stacks_bb'], hero=sp['hero'], history=sp['history'], history_fr=history_text(sp),
                pot_bb=sp['pot_bb'], to_call_bb=sp['to_call_bb'], family=family(sp), difficulty=difficulty(lesson_gap(sp, hand)), mode='exploit' if sp.get('villain') else 'gto',
                villain=({k: sp['villain'].get(k) for k in ('position', 'stat', 'observed_pct', 'gto_pct', 'reference')} if sp.get('villain') else None),
                profile=(profiles.public(profiles.for_villain(sp['villain']), sp['villain']['gto_pct']) if sp.get('villain') else None),
                options=[dict(id=a['id'], label_fr=action_label(sp, a)) for a in sp['actions']])


VERB_FR = {'fold': 'se couche', 'check': 'checke', 'limp': 'limpe', 'call': 'paie', 'call_allin': 'paie', 'raise': 'relance', 'allin': 'part à tapis'}
BASE_FR = 'des mains qui arrivent à cette décision'
# mode exploitant : la référence à laquelle le profil est comparé (générateur 2.0.0 : l'équilibre push/fold)
REF_NAMES = {'nash_pushfold': dict(player="un joueur équilibré en push/fold", compare="À l'équilibre push/fold", same="qu'à l'équilibre push/fold",
                                   short='équilibre push/fold'),
             None: dict(player='un joueur GTO', compare='En GTO', same="qu'en GTO", short='GTO')}


def ref_names(sp):
    return REF_NAMES.get((sp.get('villain') or {}).get('reference'), REF_NAMES[None])


def range_grid(sp):
    """stratégie de référence sur les 169 mains (grille 13 x 13) : pourcentages arrondis par action, et part de chaque action"""
    acts = [dict(id=a['id'], type=a['type'], label_fr=action_label(sp, a)) for a in sp['actions']]
    hands = {}; share = [0.0] * len(acts); tot = 0.0
    for i, h in enumerate(NAMES):
        x = sp['hands'][h]
        if x.get('reach', 0) <= 0 or not x.get('freq'): continue
        mix = dict(grading.displayed_mix(sp, h)); hands[h] = [mix.get(a['id'], 0) for a in acts]
        m = W[i] * x['reach']; tot += m
        for j, f in enumerate(grading.reference_freq(sp, h)): share[j] += m * f
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
NEAR_POINTS = 2                   # « à la limite » : mains à moins de 2 points d'équité du seuil


def _pct_eq(v, need):
    """équité affichée à une décimale, ou deux quand elle tomberait sur la même valeur que le seuil"""
    return (f"{100 * v:.2f} %" if round(100 * v, 1) == round(100 * need, 1) else f"{100 * v:.1f} %").replace('.', ',')


def _token(sp, a):
    t = a['type']
    return {'fold': 'fold', 'check': 'check', 'limp': 'call', 'call': 'call', 'call_allin': 'call', 'allin': 'allin'}.get(t) or f"raise{a['to_bb']:g}"


def fold_equity(sp, aid):
    """probabilité (environ, sans retrait de cartes) que tous les adversaires se couchent après l'action aid, tirée des
    spots suivants du même dataset ; None si un de ces spots manque"""
    spots = _BY_NODE.get(id(sp))
    if spots is None: return None
    a = next(x for x in sp['actions'] if x['id'] == aid)
    key = (sp['node_key'] + '_' if sp['node_key'] != 'root' else '') + f"{sp['hero']}-{_token(sp, a)}"
    p = 1.0
    for _ in opponents_in(sp):
        nxt = spots.get((sp.get('preflop_tree'), tuple(sp['stacks_bb']), key))
        if nxt is None: return None
        ids = [x['id'] for x in nxt['actions']]
        if 'F' not in ids: return None
        p *= range_grid(nxt)['share_pct'][ids.index('F')] / 100
        key += f"_{nxt['hero']}-fold"
        if key.count('_') + 1 >= len(sp['players']): break
    return p


_BY_NODE = {}


def _index_nodes(spots):
    idx = {(x.get('preflop_tree'), tuple(x['stacks_bb']), x['node_key']): x for x in spots.values()}
    for x in spots.values(): _BY_NODE[id(x)] = idx


PREMIUM_VSR = 0.70                # au-dessus : main très forte (AA à 99, AK) pour la phrase « piège »


def principle(sp, hand, best, labels):
    """une phrase de principe, tirée des données quand c'est possible : pourquoi cette action plutôt qu'une autre"""
    t = {a['id']: a['type'] for a in sp['actions']}[best]; eff = hero_effective(sp); fam = family(sp)
    strong = float(_VSR()[NAMES.index(hand)]) >= PREMIUM_VSR
    if t in ('allin', 'raise'):
        fe = fold_equity(sp, best); who = 'tout le monde se couche' if len(opponents_in(sp)) > 1 else "l'adversaire se couche"
        if t == 'allin':
            if to_act_after(sp) and fam == 'vs_allin':
                return "Partir à tapis par-dessus fait coucher le joueur derrière : tu joues seul contre le premier tapis, avec le pot mort en plus."
            return (f"Ton tapis met la pression maximale : {who} environ {round(100 * fe)} % du temps et tu prends le pot sans abattage ; sinon, il te reste ton équité."
                    if fe is not None else f"À {bb(eff)} BB, partir à tapis met la pression maximale : il faut payer tout son tapis pour voir le flop.")
        return (f"Relancer construit le pot avec une main qui joue bien : {who} environ {round(100 * fe)} % du temps, et sinon tu gardes l'initiative."
                if fe is not None else "Relancer construit le pot avec une main qui joue bien, et garde l'initiative après le flop.")
    if t == 'limp':
        if strong: return "Avec une main très forte, compléter sert de piège : l'adversaire relancera ou partira à tapis avec des mains moins fortes."
        return ("Compléter ne coûte que 0,5 BB : la main vaut un flop bon marché, sans payer une relance trop chère." if sp['hero'] == 'SB' else
                "Limper ne coûte que 1 BB : la main vaut un flop bon marché, sans s'exposer seule à une relance.")
    if t == 'check':
        return "Tu vois le flop gratuitement : relancer ferait surtout coucher les mains que tu domines et garder celles qui te battent."
    if t == 'call':
        call, final = call_terms(sp)
        return f"Payer {bb(call)} BB pour un pot de {bb(final)} BB : la cote est bonne, et la main joue assez bien après le flop pour ne pas tout risquer maintenant."
    if t == 'call_allin':
        return "Ton équité contre sa range dépasse ce que demande la cote du pot : payer rapporte plus que se coucher."
    if fam == 'vs_allin':
        return "Ton équité contre sa range ne suffit pas pour la cote du pot : payer perdrait des jetons à long terme."
    if fam == 'vs_raise':
        return "Face à une relance, la main est trop souvent dominée ou hors de la cote : se coucher évite de perdre davantage."
    return ("Avec des joueurs encore à parler derrière, la main gagne trop rarement quand elle est payée : se coucher ne coûte que ce qui est déjà misé."
            if to_act_after(sp) else "La main ne rapporte pas assez par rapport au risque : aucune action ne fait mieux que se coucher.")


def why(sp, hand, ev, best, labels, grid, chosen=None, verdict=None):
    """« pourquoi », tiré des données : calcul, marge, limites de la décision.
    best : l'action de référence affichée ; verdict : celui de la réponse du joueur.
    Call d'un tapis à EV exacte : cote du pot, équité de la main, marge en points, mains qui paient ou se couchent tout juste.
    Ailleurs : part de la stratégie, autre option, jeu mixte, mains jouées en mixte."""
    ids = [a['id'] for a in sp['actions']]; types = {a['id']: a['type'] for a in sp['actions']}
    exploit = bool(sp.get('villain')); out = []; accepted = verdict == 'correct'
    money = (lambda x: gain_range(x)) if exploit else (lambda x: gain_bb(x))
    top = ids[max(range(len(ev)), key=lambda k: ev[k])]
    if sp.get('push_fold') and ids == ['F', 'A']:
        x = sp['hands'][hand]; e, g = x['ev_exact'][1], x['ev_gto'][1]; L = hero_effective(sp)
        out.append(f"Il se couche {_pct(x['fold_pct'] / 100)} du temps face à ton tapis ({ref_names(sp)['short']} : {_pct(x['fold_pct_gto'] / 100)}) : "
                   f"tu gagnes alors sa blinde (1 BB).")
        out.append(f"Quand il paie, {hand} a {_pct1(x['equity_called'])} d'équité contre sa range de call ({ref_names(sp)['short']} : {_pct1(x['equity_called_gto'])}) "
                   f"et tout se joue à tapis ({bb(L)} BB effectifs).")
        if (e > 0) != (g > 0):
            out.append("Contre ce profil, " + ("ses calls trop larges rendent ton tapis rentable : tu gagnes plus quand il paie avec pire que ce que tu perds en folds."
                       if e > 0 else "tu perds trop de folds : ton tapis vivait de ses abandons, et ta main est trop faible quand il paie."))
        tot = sum(W[NAMES.index(h)] * y['reach'] for h, y in sp['hands'].items()) or 1.0
        mass = lambda f: sum(W[NAMES.index(h)] * y['reach'] for h, y in sp['hands'].items() if f(y)) / tot
        out.append(f"Contre ce profil, on part à tapis avec {_pct(mass(lambda y: y['ev_exact'][1] > 0))} {BASE_FR} ; "
                   f"contre {ref_names(sp)['player']}, avec {_pct(mass(lambda y: y['ev_gto'][1] > 0))}.")
        return out
    if sp['ev_reference'] == 'exact' and ids == ['F', 'C'] and types['C'] == 'call_allin' and sp['to_call_bb'] > 0:
        call, final = call_terms(sp); need = call / final
        eq = {}
        for h, x in sp['hands'].items():
            e = (x.get('ev_exact') or [None, None])[1]
            if e is not None and x.get('reach', 0) > 0: eq[h] = (e + call) / final
        have = eq[hand]; margin = round(round(100 * have, 1) - round(100 * need, 1), 1)   # cohérent avec les valeurs affichées
        out.append(f"Cote du pot : {bb(call)} BB à payer pour un pot final de {bb(final)} BB, il faut {_pct1(need)} d'équité pour payer.")
        out.append(f"Contre {'sa range' if exploit else 'sa range de tapis'}, {hand} a {_pct_eq(have, need)} d'équité : "   # le gain est déjà dans la ligne principale
                   + ("pile au seuil." if margin == 0 else f"marge de {_points(margin)} au-dessus du seuil." if margin > 0 else f"{_points(-margin)} sous le seuil."))
        best_choice = chosen is None or chosen == best; act = to_do(sp, best)
        right = best_choice or accepted
        stake = ('soit ' if exploit else 'soit environ ') + f"{money(abs(ev[1]))} sur ce pot"   # les points d'équité, convertis en BB (= EV du call)
        if abs(margin) < 5:
            out.append(f"Décision serrée (moins de 5 points d'équité, {stake}) : " + (
                "bien vu, mais un petit changement de range adverse ou de tapis peut la renverser." if best_choice else
                f"ton choix coûte moins de {bb(GAIN_MIN_BB)} BB, il est accepté ; retiens surtout le seuil d'équité, c'est lui qui tranche." if accepted else
                "retiens surtout le seuil d'équité, c'est lui qui tranche."))
        elif abs(margin) <= 10:
            out.append(f"Écart moyen (5 à 10 points, {stake}) : " + ("la décision est claire dès que tu estimes bien la range adverse." if right else
                       f"il fallait {act} ; l'écart est assez grand pour ne pas hésiter si tu estimes bien la range adverse."))
        else:
            out.append(f"Écart large (plus de 10 points, {stake}) : " + ("c'est une décision de principe, à prendre sans hésiter." if right else
                       f"erreur nette, il fallait {act} sans hésiter, la main est loin du seuil."))
        near = {h: v for h, v in eq.items() if abs(v - need) <= NEAR_POINTS / 100 and h != hand}
        callers = sorted((v, h) for h, v in near.items() if v >= need); folders = sorted(((v, h) for h, v in near.items() if v < need), reverse=True)
        if callers or folders:
            out.append(f'À la limite (seuil {_pct1(need)}, à {NEAR_POINTS} points près), '
                       + ' ; '.join(x for x in (('paient encore : ' + ', '.join(f'{h} ({_pct_eq(v, need)})' for v, h in callers[:3])) if callers else '',
                                                 ('se couchent déjà : ' + ', '.join(f'{h} ({_pct_eq(v, need)})' for v, h in folders[:3])) if folders else '') if x) + '.')
        else:
            out.append(f'Aucune main à moins de {NEAR_POINTS} points du seuil : la frontière est nette.')
        mass = lambda f: sum(W[NAMES.index(h)] * sp['hands'][h]['reach'] for h in eq if f(h)) / max(sum(W[NAMES.index(h)] * sp['hands'][h]['reach'] for h in eq), 1e-12)
        share = mass(lambda h: eq[h] >= need)
        if exploit:
            g = mass(lambda h: (sp['hands'][h].get('ev_gto') or [0, -1])[1] > 0)
            out.append(f"Contre ce profil, on paie avec {_pct(share)} {BASE_FR} ; contre {ref_names(sp)['player']}, avec {_pct(g)}.")
        else:
            out.append(f"Ici, on paie avec {_pct(share)} {BASE_FR}.")
        return out
    j = ids.index(best); verb = 'complète' if types[best] == 'limp' and sp['hero'] == 'SB' else VERB_FR[types[best]]
    f = grading.reference_freq(sp, hand); shown = grading.displayed_mix(sp, hand); pj = dict(shown).get(best, 0)
    if f[j] >= 0.5: tail = f"{hand} en fait partie."
    elif pj: tail = f"{hand} le fait {pj} % du temps."
    else: tail = f"{hand} le fait rarement : les actions ont une valeur quasi égale."
    out.append(f"Ici, on {verb} avec {grid['share_pct'][j]} % {BASE_FR} ; {tail}")
    if 'call_allin' in types.values() and sp['to_call_bb'] > 0:       # HRC : la cote du pot n'est qu'un repère
        call, final = call_terms(sp); exact = not to_act_after(sp) and call >= sp['to_call_bb'] - 1e-9
        out.append(f"Repère : il faut {'' if exact else 'environ '}{_pct(call / final)} d'équité pour payer (cote du pot"
                   + ('' if exact else ' ; approximatif, car ' + ('un joueur reste à parler' if to_act_after(sp) else 'le tapis adverse te couvre')) + ').')
    base_id = 'F' if 'F' in ids else 'X'
    tied = {ids[k] for k in range(len(ids)) if 1000 * (max(ev) - ev[k]) <= grading.TOLERANCE_MBB + 1e-9}   # déjà dans « plusieurs bonnes décisions »
    if sp['ev_reference'] == 'hrc': tied |= {ids[k] for k in range(len(ids)) if 1000 * (max(ev) - ev[k]) <= grading.PERTINENT_MBB + 1e-9}   # déjà dans la nuance
    others = sorted((k for k in range(len(ids)) if ids[k] not in (best, chosen, base_id, top) and ids[k] not in tied), key=lambda k: -ev[k])
    if others:                                                     # le choix du joueur, le fold et l'action la plus rentable sont déjà dans l'explication
        d = ev[j] - ev[others[0]]
        out.append(f"Autre option : {_low(labels[ids[others[0]]])}, {gain_bb(d)} {'de moins' if d >= 0 else 'de plus en EV'}.")
    if len(shown) > 1:
        mix = ', '.join(f'{_low(labels[a])} {p} %' for a, p in shown); played = dict(shown)
        if chosen is not None and chosen not in played:
            out.append(f"{hand} est jouée de plusieurs façons ({mix}) : ces actions ont une valeur proche. Ton choix {_named(labels[chosen])} n'en fait pas partie"
                       + (f", mais il coûte moins de {bb(GAIN_MIN_BB)} BB : accepté." if accepted else '.'))
        else:
            out.append(f"{hand} est jouée de plusieurs façons ({mix}) : ces actions ont une valeur proche, chacune est acceptée.")
    elif chosen is not None and chosen != best and accepted and chosen not in dict(shown):
        out.append(f"Ton choix {_named(labels[chosen])} ne fait pas partie de la stratégie de référence, mais il coûte moins de {bb(GAIN_MIN_BB)} BB : accepté.")
    rf = {h: grading.reference_freq(sp, h) for h, x in sp['hands'].items() if x.get('reach', 0) >= 0.05 and x.get('freq') and h != hand}
    edge = sorted((abs(v[j] - 0.5), h) for h, v in rf.items() if 0.2 <= v[j] <= 0.8)
    if edge:
        out.append(f"Mains jouées en partie seulement pour l'action « {_low(labels[best])} » : {', '.join(h for _, h in edge[:5])}.")
    elif grid['share_pct'][j] >= 100:
        out.append(f"Toutes les mains le font ici : pas de frontière.")
    else:
        out.append(f"Aucune main n'est jouée en partie seulement pour l'action « {_low(labels[best])} » : la frontière est nette.")
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


def r100(x): return round(100 * x)


SHORT_BB = 5                      # sous ce tapis restant après l'action, pas de vrai jeu après le flop


_AVG = {}


def _kind_average(kind):
    """moyenne des fréquences au flop sur les classes du même type : 'pair', 's' (assorties) ou 'o' (dépareillées)"""
    if kind not in _AVG:
        postflop_profile('AA'); hs = _POSTFLOP['hands']
        sel = [h for h in hs if (len(h) == 2) == (kind == 'pair') and (kind == 'pair' or h.endswith(kind))]
        _AVG[kind] = {k: sum(hs[h][k] for h in sel) / len(sel) for k in hs[sel[0]]}
    return _AVG[kind]


SIGNIF = 3                        # « Et ensuite ? » : force ou faiblesse seulement à 3 points de la moyenne ou plus


def next_steps(sp, hand, best, chosen=None, labels=None):
    """« Et ensuite ? » : forces et faiblesses de la main après le flop (énumération exacte des flops, data/postflop_profiles.json).
    Toujours au sujet de l'action de référence. None quand il n'y a rien d'utile à dire (fold, tapis payé sans joueur
    derrière) : la section est alors masquée."""
    t = {a['id']: a['type'] for a in sp['actions']}[best]
    p = postflop_profile(hand); pc = lambda x: f"{round(100 * x)} %"
    pair = len(hand) == 2; suited = hand.endswith('s'); hi, lo = _R.index(hand[0]), _R.index(hand[1])
    subject = (f"Avec l'action de référence {_named(labels[best])} : " if labels and chosen and chosen != best else '')
    say = lambda x: subject + (_low(x) if subject else x)
    empty = dict(position=None, metrics=[], forces=[], weaknesses=[])
    if t == 'fold': return None
    behind = to_act_after(sp); several = len(opponents_in(sp)) > 1
    if family(sp) == 'vs_allin':
        if not behind: return None                                  # tout est dans « Pourquoi ? » (cote du pot, équité)
        return dict(empty, intro=say("Un joueur parle encore derrière toi. Il faut plus que la cote du pot, car il peut payer ou partir à tapis à son tour."
                                     + (" Partir à tapis par-dessus sert à le faire coucher." if t == 'allin' else '')))
    if t == 'allin':
        return dict(empty, intro=say("Tu pousses. Soit tout le monde se couche et tu prends le pot, soit quelqu'un paie et tout se joue à l'équité, sans décision après le flop."
                                     if several else
                                     "Tu pousses. Soit l'adversaire se couche et tu prends le pot, soit il paie et tout se joue à l'équité, sans décision après le flop."))
    act = next(a for a in sp['actions'] if a['id'] == best)
    put = {'raise': act.get('to_bb'), 'limp': 1.0, 'call': sp['hero_committed_bb'] + call_terms(sp)[0]}.get(t, sp['hero_committed_bb'])
    left = hero_effective(sp) - (put or 0)
    if left < SHORT_BB:
        intro = say(f"Tapis trop court pour vraiment jouer après le flop (il restera environ {bb1(left)} BB). L'argent part vite au milieu, l'essentiel se joue à l'équité. "
                    "Voici ce que la main touche au flop.")
    else:
        intro = say("Après le flop, voici ce que tu peux attendre de cette main (sur tous les flops possibles).")
    folded = {h['position'] for h in sp['history'] if h['action'] == 'fold'}
    order = [x for x in POSTFLOP_ORDER[len(sp['players'])] if x not in folded]
    position = None
    if left >= SHORT_BB and sp['hero'] in order and len(order) > 1:
        seen = 'ce que font les autres' if len(order) > 2 else "ce que fait l'adversaire"
        position = (f"Tu joueras en position : tu parles en dernier à chaque tour, tu vois {seen} avant de décider."
                    if order[-1] == sp['hero'] else
                    "Tu joueras hors position : tu parles en premier à chaque tour, ce qui rend la main plus difficile à jouer et réduit l'équité que tu réalises.")
    kind = 'pair' if pair else 's' if suited else 'o'; av = _kind_average(kind)
    ref = {'pair': 'des paires servies', 's': 'des mains assorties', 'o': 'des mains dépareillées'}[kind]
    above = lambda k, v=None: r100(p[k] if v is None else v) - r100(av[k]) >= SIGNIF
    below = lambda k: r100(av[k]) - r100(p[k]) >= SIGNIF
    forces, weak = [], []
    if pair:
        over = overcard_prob(hand)
        forces.append(f"Brelan ou mieux au flop {pc(p['set_plus'])} du temps (environ 1 fois sur 8).")
        if p['overpair'] >= 0.3: forces.append(f"Ta paire reste plus haute que les trois cartes du board {pc(p['overpair'])} du temps.")
        if over >= 0.5: weak.append(f"Au moins une carte plus haute que ta paire arrive au flop {pc(over)} du temps.")
    else:
        if p['top_pair_plus'] >= 0.25: forces.append(f"Paire max ou mieux au flop {pc(p['top_pair_plus'])} du temps.")
        if suited: forces.append(f"Tirage couleur ou couleur faite au flop {pc(p['flush_draw_plus'])} du temps.")
        if above('oesd_plus') or above('gutshot'):
            forces.append(f"Potentiel de quinte au-dessus de la moyenne {ref} : tirage par les deux bouts ou mieux {pc(p['oesd_plus'])} du temps, tirage ventral {pc(p['gutshot'])}.")
        if above('miss'):
            weak.append(f"Tu rates le flop {pc(p['miss'])} du temps, sans paire ni tirage fort (moyenne {ref} : {pc(av['miss'])}).")
        if hi >= _R.index('T') and lo <= _R.index('7'):
            weak.append(f"Quand ton {hand[0]} touche, ton kicker {hand[1]} est faible : tu risques d'être dominé par les {hand[0]}x plus forts.")
        elif below('top_pair_plus'):
            weak.append(f"Paire max ou mieux seulement {pc(p['top_pair_plus'])} du temps (moyenne {ref} : {pc(av['top_pair_plus'])}) : "
                        "tu touches rarement la paire max, tes paires seront souvent des paires moyennes ou basses.")
        if below('oesd_plus') and below('gutshot'):
            weak.append("Peu de potentiel de quinte : les deux cartes sont trop éloignées pour se compléter souvent.")
    eq = float(_VSR()[NAMES.index(hand)])
    if eq >= 0.55: forces.append(f"Contre une main au hasard, {hand} a {pc(eq)} d'équité (tapis préflop).")
    elif eq < 0.42: weak.append(f"Main faible à l'abattage : contre une main au hasard, {hand} n'a que {pc(eq)} d'équité (tapis préflop).")
    cmp = lambda v, a: 'equal' if r100(v) == r100(a) else 'above' if v > a else 'below'   # sur les valeurs affichées
    tone = lambda c, lower: 'neutral' if c == 'equal' else ('good' if (c == 'above') != lower else 'bad')
    if pair:                                                     # une main se compare aux mains du même type
        rows = (('set_plus', 'Brelan ou mieux', p['set_plus'], av['set_plus'], False),
                ('overpair', 'Paire plus haute que le board', p['overpair'], av['overpair'], False),
                ('overcard', 'Carte plus haute que ta paire au board (moins, c\'est mieux)', overcard_prob(hand), _overcard_avg(), True))
    else:
        draw = ('draw_plus', 'Tirage couleur ou quinte (ou mieux)') if suited else ('oesd_plus', 'Tirage quinte par les deux bouts (ou mieux)')
        rows = tuple((k, l, p[k], av[k], False) for k, l in (('top_pair_plus', 'Paire max ou mieux'), ('two_pair_plus', 'Deux paires ou mieux'), draw))
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


def reference_action(sp, hand):
    """action de référence affichée : la plus jouée par la stratégie quand elle vaut, à la limite d'imprécision près, la plus
    rentable en EV (écarts de calcul HRC) ; sinon la plus rentable. En mode exploitant : toujours la plus rentable (EV exacte)."""
    ev = grading.reference_ev(sp, hand); ids = [a['id'] for a in sp['actions']]; top = max(range(len(ev)), key=lambda k: ev[k])
    f = sp['hands'][hand].get('freq') and grading.reference_freq(sp, hand)
    if sp.get('villain') or not f: return ids[top]
    m = max(range(len(f)), key=lambda k: f[k])
    return ids[m] if f[m] > f[top] and ev[top] - ev[m] <= IMPRECISION_BB + 1e-9 else ids[top]


_RK = 'AKQJT98765432'


def range_text(hands, max_groups=8):
    """une range en notation poker : 22+, A2+, KTs+, 76s… (groupes contigus ; assorties et dépareillées fusionnées quand
    elles coïncident) ; None si elle est trop longue pour être lisible"""
    hs = set(hands); out = []
    def runs(idx):
        rr = [[idx[0]]]
        for i in idx[1:]:
            if i == rr[-1][-1] + 1: rr[-1].append(i)
            else: rr.append([i])
        return rr
    pairs = sorted(_RK.index(r) for r in _RK if r + r in hs)
    if pairs:
        for run in runs(pairs):
            hi, lo = _RK[run[0]], _RK[run[-1]]
            out.append(f'{lo}{lo}+' if hi == 'A' and lo != 'A' else (f'{hi}{hi}' if hi == lo else f'{lo}{lo}-{hi}{hi}'))
    for i, h in enumerate(_RK[:-1]):
        groups = {}
        for suit in ('s', 'o'):
            idx = [_RK.index(k) for k in _RK[i + 1:] if h + k + suit in hs]
            for run in (runs(idx) if idx else []):
                top, bot = _RK[run[0]], _RK[run[-1]]
                key = (f'{h}{bot}+' if run[0] == i + 1 and len(run) > 1 else f'{h}{top}' if len(run) == 1 else f'{h}{bot}-{h}{top}')
                groups.setdefault(key, set()).add(suit)
        for key, suits in groups.items():
            if len(suits) == 2: out.append(key)                                   # assorties et dépareillées : « A2+ »
            else:
                sfx = suits.pop(); out.append(key.replace('+', sfx + '+') if key.endswith('+') else '-'.join(x + sfx for x in key.split('-')))
    return ', '.join(out) if len(out) <= max_groups else None


SITUATION_FR = {'first_in': 'premier à parler', 'vs_limp': 'face à un limp', 'vs_raise': 'face à une relance', 'vs_allin': 'face à un tapis'}


RULE_MAX_GROUPS = 12             # au-delà, la règle n'est plus « simple » : on donne la part des mains
RULE_MIN_FIT = 0.93               # « À retenir » : la règle à seuils doit classer au moins 93 % des mains (pondérées) comme la référence


def threshold_rule(inside, weight):
    """règle à seuils la plus fidèle : pour les paires et pour chaque carte haute (assorties, dépareillées), un kicker
    minimal (« A7+ », « K9s+ », « 55+ ») ; renvoie (texte, part des mains bien classées). inside : {main: bool} ; weight : {main: poids}"""
    groups = [('pair', [r + r for r in _RK])] + [(h + sfx, [h + k + sfx for k in _RK[i + 1:]]) for i, h in enumerate(_RK[:-1]) for sfx in ('s', 'o')]
    tot = sum(weight.values()) or 1; good = 0.0; parts = {}
    for name, hs in groups:                                   # hs du plus fort au plus faible : seuil = nombre de mains gardées
        hs = [h for h in hs if h in weight]
        if not hs: continue
        best = max(range(len(hs) + 1), key=lambda n: sum(weight[h] for h in hs[:n] if inside[h]) + sum(weight[h] for h in hs[n:] if not inside[h]))
        good += sum(weight[h] for h in hs[:best] if inside[h]) + sum(weight[h] for h in hs[best:] if not inside[h])
        if best: parts[name] = hs[best - 1]
    out = []
    if 'pair' in parts: out.append(f"{parts['pair']}+" if parts['pair'] != 'AA' else 'AA')
    for i, h in enumerate(_RK[:-1]):
        s_, o_ = parts.get(h + 's'), parts.get(h + 'o')
        last = lambda x: x[1]
        if s_ and o_ and last(s_) == last(o_): out.append(f"{h}{last(s_)}+" if last(s_) != _RK[i + 1] else f"{h}{last(s_)}")
        else:
            for x, sfx in ((s_, 's'), (o_, 'o')):
                if x: out.append(f"{h}{last(x)}{sfx}+" if last(x) != _RK[i + 1] else f"{h}{last(x)}{sfx}")
    return ', '.join(out), good / tot


def rule_to_remember(sp, best, labels):
    """« À retenir » : la range de l'action de référence (mains qui la jouent au moins 50 %) résumée en règle à seuils,
    affichée seulement si elle est fidèle (RULE_MIN_FIT) ; sinon la part des mains. Pour un fold : ce qu'on joue."""
    j = [a['id'] for a in sp['actions']].index(best)
    live = {h: x for h, x in sp['hands'].items() if x.get('reach', 0) >= 0.05 and x.get('freq')}
    t = {a['id']: a['type'] for a in sp['actions']}[best]
    plays = {h: grading.reference_freq(sp, h)[j] >= 0.5 for h in live}
    weight = {h: W[NAMES.index(h)] * live[h]['reach'] for h in live}
    share = round(100 * sum(weight[h] for h in live if plays[h]) / (sum(weight.values()) or 1))
    verb = {'fold': 'on se couche', 'check': 'on checke', 'limp': 'on complète' if sp['hero'] == 'SB' else 'on limpe', 'call': 'on paie',
            'call_allin': 'on paie', 'raise': 'on relance', 'allin': 'on part à tapis'}[t]
    where = f"au {sp['hero']} {SITUATION_FR[family(sp)]} à {bb(hero_effective(sp))} BB" + (' (heads-up)' if sp['table'] == 'heads-up' else '')
    target = {h: not v for h, v in plays.items()} if t == 'fold' else plays
    txt, fit = threshold_rule(target, weight)
    if txt and fit >= RULE_MIN_FIT and 0 < share < 100 and txt.count(',') < RULE_MAX_GROUPS:
        n = 100 - share if t == 'fold' else share
        what = f"on ne joue que {txt}" if t == 'fold' else f"{verb} avec {txt}"
        exact = '' if fit >= 0.995 else f" ; règle simplifiée, exacte pour {round(100 * fit)} % d'entre elles"
        return f"À retenir : {where}, {what} (environ {n} % des mains qui arrivent ici{exact})."
    return f"À retenir : {where}, {verb} avec environ {share} % des mains qui arrivent ici."


def _option(sp, labels, aid):
    """une action en sujet de phrase : « Le fold », « Le check », « L'option (…) »"""
    t = {a['id']: a['type'] for a in sp['actions']}[aid]
    return 'Le fold' if t == 'fold' else 'Le check' if t == 'check' else f"L'option {_named(labels[aid])}"


def correct(version, spot_id, hand, action_id):
    """correction et explication structurée (données du dataset uniquement)"""
    _, spots = load(version); sp = spots[spot_id]
    if sp.get('field'): return field.correct(sp, action_id)
    g = grading.grade(sp, hand, action_id)
    labels = {a['id']: action_label(sp, a) for a in sp['actions']}
    ev = grading.reference_ev(sp, hand)
    mix = grading.displayed_mix(sp, hand); shown = dict(mix)
    ids = [a['id'] for a in sp['actions']]; top = g['best_action']          # top : la plus rentable en EV
    best = reference_action(sp, hand)                                       # best : l'action de référence affichée
    base_id = 'F' if 'F' in ids else 'X'                     # référence : fold, ou check quand rien n'est à payer
    E_ = lambda a: ev[ids.index(a)]
    raw = 1000 * (E_(top) - E_(action_id))                   # regret non arrondi : montant et verdict concordent aux bornes
    evb = E_(best) - E_(base_id); ref = 'fold' if base_id == 'F' else 'check'
    played = '' if best == top else f", jouée {shown.get(best, 0)} % du temps"
    # écart d'EV sous la tolérance : plusieurs bonnes décisions, sans détailler des centièmes de BB
    good = [a for a in ids if 1000 * (E_(top) - E_(a)) <= grading.TOLERANCE_MBB + 1e-9]
    good.sort(key=lambda a: (a != best, ids.index(a)))
    if len(good) > 1:
        names = [_low(labels[a]) for a in good]
        lines = [f"Plusieurs bonnes décisions : {', '.join(names[:-1])} ou {names[-1]} (moins de {bb(GAIN_MIN_BB)} BB d'écart)."]
    elif best == base_id or abs(evb) < 0.005 or evb < 0: lines = [f'Action de référence : {labels[best]}{played}.']
    elif evb <= GAIN_MIN_BB: lines = [f"Action de référence : {labels[best]}{played}, à peine mieux que le {ref} (moins de {bb(GAIN_MIN_BB)} BB)."]
    else: lines = [f"Action de référence : {labels[best]}{played}, {gain_bb(evb, signed=True)} par rapport au {ref}."]
    if best != top and len(good) == 1:
        lines.append(f"{_option(sp, labels, top)} vaut presque autant : {gain_bb(E_(top) - E_(best))} de plus en EV ; les deux sont acceptés.")
    # EV HRC : une autre action à moins de PERTINENT_MBB de la plus rentable reste pertinente (nuance, sans changer la référence)
    near = [x for x in ids if x not in good and x != best and sp['ev_reference'] == 'hrc' and 1000 * (E_(top) - E_(x)) <= grading.PERTINENT_MBB + 1e-9
            and grading.grade(sp, hand, x)['verdict'] != 'correct']                 # une action acceptée (jeu mixte) est déjà dite ailleurs
    if near and not sp.get('villain'):
        names = ' ou '.join(_low(labels[x]) for x in near)
        lines.append(f"Nuance : {names} {'est aussi pertinente' if len(near) == 1 else 'sont aussi pertinentes'} "
                     f"(moins de {bb(grading.PERTINENT_MBB / 1000)} BB d'écart).")
    grid = range_grid(sp); because = why(sp, hand, ev, best, labels, grid, action_id, g['verdict']); after = next_steps(sp, hand, best, action_id, labels)
    if action_id == best or (len(good) > 1 and action_id in good): pass       # le bandeau le dit déjà
    elif action_id == top:
        lines.append(f"Ton choix {_named(labels[action_id])} est le plus rentable en EV : réponse acceptée.")
    else:
        than = '' if best == top or len(good) > 1 else f" que {_low(labels[top])}, la plus rentable"
        lines.append(f"Ton choix {_named(labels[action_id])} " + (f"coûte moins de {bb(GAIN_MIN_BB)} BB{than}." if raw <= grading.TOLERANCE_MBB + 1e-9
                                                                  else f"rapporte {gain_bb(raw / 1000)} de moins{than}."))
        tol, imp = bb(GAIN_MIN_BB), bb(IMPRECISION_BB)
        if g['verdict'] == 'correct' and raw > grading.TOLERANCE_MBB:
            lines.append(f"La stratégie de référence joue cette action {shown.get(action_id, round(100 * g['chosen_frequency']))} % du temps : elle est acceptée.")
        elif g['verdict'] == 'correct':
            lines.append(f"Écart d'au plus {tol} BB, négligeable : réponse acceptée.")
        elif g['verdict'] == 'imprécision' and g.get('pertinent') and raw > 3 * grading.TOLERANCE_MBB:
            lines.append(f"Écart sous {bb(grading.PERTINENT_MBB / 1000)} BB : ton choix reste pertinent, mais la référence est meilleure. Imprécision, pas erreur.")
        elif g['verdict'] == 'imprécision':
            lines.append(f'Écart entre {tol} et {imp} BB : imprécision, pas erreur.')
        else:
            lines.append(f'Écart au-delà de {imp} BB : erreur.')
    v = sp.get('villain'); h = sp['hands'][hand]; ex = None; core = None
    if v:
        pr = profiles.for_villain(v)
        if pr is None: raise ValueError('aucun profil fictif ne correspond à ce spot : pas de conseil exploitant')
        eg, ee = h['ev_gto'][1], h['ev_exact'][1]; gto = h['gto_action']; changed = gto != best
        conf = profiles.confidence(1000 * ee); verb = 'gagne' if ee >= 0 else 'perdrait'
        ex = dict(profile=dict(profiles.public(pr, v['gto_pct']), adaptation_fr=pr['adaptation_fr'], tendency_rule_fr=pr['tendency']['rule_fr'], scope_fr=pr['scope_fr']),
                  # 1. référence exploitante : la bonne action contre ce profil, et l'enjeu en fourchette
                  reference_fr=(f"{labels[best]}.\nTon choix {_named(labels[action_id])} perd {gain_range(raw / 1000)}." if action_id != best
                                else f"{labels[best]}.\n{'Partir à tapis' if sp.get('push_fold') else 'Payer'} {verb} {gain_range(ee)}."),
                  # 2. comparaison avec la référence
                  comparison_fr=(f"{ref_names(sp)['compare']}, ce serait {_low(labels[gto])}.\n{pr['adaptation_fr']}" if changed else
                                 f"Même décision {ref_names(sp)['same']} : l'écart de range ne suffit pas à la changer."),
                  tendency_fr=f"Ce {v['position']} {tendency_text(v, '')}".rstrip() + f" ({ref_names(sp)['short']} : {bb(v['gto_pct'])} %).",
                  choice_loss_fr=(gain_range(raw / 1000) if action_id != best else None),
                  changed=changed, confidence=conf, confidence_fr='enjeu net' if conf == 'élevée' else 'enjeu faible',
                  note_fr="Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.")
        core = [f"Contre ce type de profil « {pr['name_fr']} » : {ex['reference_fr']}", ex['comparison_fr'], ex['note_fr']]
        lines = core[:1] + because + core[1:]
    else:
        core = list(lines) + [principle(sp, hand, best, labels)]
        if g['verdict'] != 'correct': core.append(rule_to_remember(sp, best, labels))      # après une erreur ou une imprécision : une règle simple
        lines = core + because                                     # la stratégie arrondie est affichée à part
    loss = max(0.0, E_(best) - E_(action_id)) if best != top else raw / 1000
    return dict(verdict=g['verdict'], points=g['points'], regret_mbb=g['regret_mbb'], best_action=best, best_label=labels[best],
                top_action=top, chosen_action=action_id, gto_action=(h['gto_action'] if v else None), gto_label=(labels[h['gto_action']] if v else None),
                good_actions=(good if len(good) > 1 and not v else []), good_labels=([labels[a] for a in good] if len(good) > 1 and not v else []),
                chosen_label=labels[action_id], strategy=[dict(id=a, label_fr=labels[a], pct=shown.get(a, 0), chosen=a == action_id) for a in ids],
                loss_fr=(None if action_id == best or (len(good) > 1 and action_id in good) else (gain_range(loss) if v else gain_bb(loss))),
                ev_source=g['ev_source'], exploit=ex, why_fr=because, next=after, range=grid, explanation_fr='\n'.join(lines),   # une phrase par ligne
                core_fr='\n'.join(core) if core is not None else None)


def summary(version, answers):
    """answers : [(spot_id, main, résultat de correct())] -> bilan de la série"""
    _, spots = load(version); n = len(answers)
    pts = sum(r['points'] for _, _, r in answers)
    by = {}
    for sid, h, r in answers:
        k = (family(spots[sid]), spots[sid]['hero']); b = by.setdefault(k, [0, 0.0]); b[0] += 1; b[1] += r['points']
    errors = sorted([dict(spot_id=sid, hand=h, prompt_fr=prompt(spots[sid], h), chosen=r['chosen_label'], best=r['best_label'], regret_mbb=r['regret_mbb'],
                          loss_fr=r.get('loss_fr'))
                     for sid, h, r in answers if r['verdict'] != 'correct'], key=lambda e: -e['regret_mbb'])
    return dict(questions=n, points=pts, score_pct=round(100 * pts / n, 1) if n else 0.0,
                verdicts={v: sum(1 for *_, r in answers if r['verdict'] == v) for v in grading.POINTS},
                by_theme=[dict(family=f, hero=p, questions=c, points=s) for (f, p), (c, s) in sorted(by.items())],
                errors=errors, review=[e['prompt_fr'] for e in errors[:3]])

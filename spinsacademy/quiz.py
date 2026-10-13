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
DEFAULT_VERSION = os.environ.get('SPINSACADEMY_DATASET', '2026.10.12-2')                       # gto_preflop
DEFAULT_EXPLOIT = os.environ.get('SPINSACADEMY_EXPLOIT', 'exploit_calls/2026.10.13-1')
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


GAIN_MIN_BB = 0.05                # en dessous : « <0,05 BB » (pas de mBB affichés au joueur)


def gain_bb(x, signed=False):
    """montant de gain ou de perte affiché au joueur, toujours en BB"""
    s = f'<{bb(GAIN_MIN_BB)} BB' if abs(x) < GAIN_MIN_BB else f'{bb(abs(x))} BB'
    return (('+' if x >= 0 else '−') + s) if signed else s


RANGE_BOUNDS_BB = (0.05, 0.25, 0.5, 1, 2, 5)


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
    if t == 'call': return f'Payer ({bb(to)} BB)'
    if t == 'call_allin': return f'Payer le tapis ({bb(to)} BB)'
    if t == 'raise': return f'Relancer à {bb(to)} BB'
    return f'Tapis ({bb(to)} BB)'


def history_text(sp):
    out = []
    for h in sp['history']:
        p = h['position']; a = h['action']; to = h.get('to_bb')
        if a == 'fold': out.append(f'Le {p} fold')
        elif a == 'check': out.append(f'Le {p} checke')
        elif a == 'limp': out.append(f"Le {p} {'complète' if p == 'SB' else 'limpe'}")
        elif a == 'call': out.append(f'Le {p} paie {bb(to)} BB')
        elif a == 'call_allin': out.append(f'Le {p} paie le tapis')
        elif a == 'raise': out.append(f'Le {p} relance à {bb(to)} BB')
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


def _pick_hand(sp, exploit, rnd):
    hands = [h for h in NAMES if sp['hands'][h]['quiz_eligible']]
    if exploit:
        adapt = [h for h in hands if sp['hands'][h]['kind'] == 'adaptation']
        other = [h for h in hands if sp['hands'][h]['kind'] != 'adaptation']
        hands = adapt if adapt and (not other or rnd.random() < ADAPTATION_SHARE) else other
    weights = [W[NAMES.index(h)] * sp['hands'][h]['reach'] for h in hands]
    return rnd.choices(hands, weights)[0]


def _use(sp, items, used, exploit):
    used.add(sp['spot_id'])
    if exploit:                                                  # pas deux fois la même situation de base (facteurs différents)
        used.update(x['spot_id'] for x in items if x.get('base_spot_id') == sp.get('base_spot_id'))


def draw_series(version=DEFAULT_VERSION, filters=None, size=SERIES_SIZE, seed=None, excluded=frozenset()):
    """[(spot_id, main)] ; ValueError si les filtres ne laissent pas assez de spots.
    excluded : spots désactivés par l'administration (un spot GTO désactivé exclut aussi les spots exploitants qui en dérivent)"""
    rnd = random.Random(seed); items = pool(version, filters, excluded); exploit = is_exploit(version)
    if len(items) < size: raise ValueError(f'{len(items)} spots disponibles pour ces filtres, {size} demandés')
    by_fam = {}
    for sp in items: by_fam.setdefault(family(sp), []).append(sp)
    order = []; used = set(); out = []
    while len(out) < size:
        if not order: order = list(by_fam); rnd.shuffle(order)
        fam = order.pop()
        choices = [sp for sp in by_fam[fam] if sp['spot_id'] not in used]
        if not choices:
            by_fam.pop(fam)
            if not by_fam: break
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
                pot_bb=sp['pot_bb'], to_call_bb=sp['to_call_bb'], family=family(sp), mode='exploit' if sp.get('villain') else 'gto',
                villain=({k: sp['villain'][k] for k in ('position', 'stat', 'observed_pct', 'gto_pct')} if sp.get('villain') else None),
                profile=(profiles.public(profiles.for_villain(sp['villain'])) if sp.get('villain') else None),
                options=[dict(id=a['id'], label_fr=action_label(sp, a)) for a in sp['actions']])


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
    if best == base_id or abs(evb) < 0.005: lines = [f'Meilleure action : {labels[best]}.']
    else: lines = [f"Meilleure action : {labels[best]} ({gain_bb(evb, signed=True)} par rapport au {'fold' if base_id == 'F' else 'check'})."]
    if action_id == best:
        lines.append('Tu as choisi la meilleure action.')
    else:
        r = g['regret_mbb']
        lines.append(f"Ton choix, {labels[action_id]}, rapporte {gain_bb(r / 1000)} de moins.")
        if g['verdict'] == 'correct' and g['regret_mbb'] > grading.TOLERANCE_MBB:
            lines.append('C\'est une action de la stratégie mixte de référence : elle est acceptée.')
        elif g['verdict'] == 'correct':
            lines.append('L\'écart est trop faible pour être significatif : réponse acceptée.')
        elif g['verdict'] == 'imprécision':
            lines.append('Les deux actions ont une valeur proche : imprécision, pas erreur.')
    v = sp.get('villain'); h = sp['hands'][hand]; ex = None; core = None
    if v:
        pr = profiles.for_villain(v)
        if pr is None: raise ValueError('aucun profil fictif ne correspond à ce spot : pas de conseil exploitant')
        eg, ee = h['ev_gto'][1], h['ev_exact'][1]; gto = h['gto_action']; changed = gto != best
        conf = profiles.confidence(1000 * ee); verb = 'gagne' if ee >= 0 else 'perd'
        ex = dict(profile=dict(profiles.public(pr), adaptation_fr=pr['adaptation_fr'], tendency_rule_fr=pr['tendency']['rule_fr'], scope_fr=pr['scope_fr']),
                  # 1. référence exploitante : la bonne action contre ce profil, et l'enjeu en fourchette
                  reference_fr=(f"{labels[best]}.\nTon choix, {labels[action_id]}, perd {gain_range(g['regret_mbb'] / 1000)}." if action_id != best
                                else f"{labels[best]}.\nContre ce profil, le call {verb} {gain_range(ee)}."),
                  # 2. comparaison avec la référence GTO
                  comparison_fr=(f"En GTO, ce serait {labels[gto]}.\n{pr['adaptation_fr']}" if changed else
                                 "Même décision qu'en GTO : l'écart de range ne suffit pas à la changer."),
                  tendency_fr=f"Ce {v['position']} part à tapis avec {bb(v['observed_pct'])} % de ses mains (GTO : {bb(v['gto_pct'])} %).",
                  choice_loss_fr=(gain_range(g['regret_mbb'] / 1000) if action_id != best else None),
                  changed=changed, confidence=conf, confidence_fr='écart net' if conf == 'élevée' else 'écart modéré',
                  note_fr="Profil fictif : une hypothèse de simulation, pas la lecture d'un vrai joueur.")
        lines = [f"Contre ce profil « {pr['name_fr']} » : {ex['reference_fr']}", ex['comparison_fr'], ex['note_fr']]
        core = []
    else:
        lines.append('Stratégie de référence : ' + ', '.join(f'{labels[a]} {p} %' for a, p in mix) + '.')
    return dict(verdict=g['verdict'], points=g['points'], regret_mbb=g['regret_mbb'], best_action=best, best_label=labels[best],
                gto_action=(h['gto_action'] if v else None), gto_label=(labels[h['gto_action']] if v else None),
                chosen_label=labels[action_id], strategy=[dict(id=a, label_fr=labels[a], pct=p) for a, p in mix],
                ev_source=g['ev_source'], exploit=ex, explanation_fr='\n'.join(lines),            # une phrase par ligne
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

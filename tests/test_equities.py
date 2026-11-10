"""CE2 : bibliothèque d'équités (spinsacademy/equities.py, table spinsacademy/data/equites.json) : valeurs connues, cohérence, recalcul indépendant."""
import itertools, json, os, subprocess, sys
import pytest
from spinsacademy import equities as E

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = '23456789TJQKA'
SUITS = 'cdhs'


def card(s): return 4 * R.index(s[0]) + SUITS.index(s[1])


def brute(h1, h2):
    """recalcul indépendant (sans numba, sans kernels) sur les 19 600 flops d'une combinaison : touche (au moins une paire ou mieux), set, tirage couleur, couleur"""
    deck = [c for c in range(52) if c not in (h1, h2)]; n = hit = sets = fd = flush = 0
    pocket = h1 // 4 == h2 // 4; suited = h1 % 4 == h2 % 4
    for fl in itertools.combinations(deck, 3):
        n += 1; ranks = {c // 4 for c in fl}; fsuits = [c % 4 for c in fl]
        match = bool({h1 // 4, h2 // 4} & ranks)
        allr = {h1 // 4, h2 // 4} | ranks
        straight = any(all(r in allr for r in range(lo, lo + 5)) for lo in range(9)) or all(r in allr for r in (12, 0, 1, 2, 3))
        suitcount = [([h1 % 4, h2 % 4] + fsuits).count(s) for s in range(4)]
        isflush = any(c == 5 for c in suitcount)
        draw = any(suitcount[s] == 4 and ((h1 % 4 == s) or (h2 % 4 == s)) for s in range(4)) and not isflush and not straight      # déjà une suite : plus de tirage
        if pocket or match or straight or isflush: hit += 1
        if pocket:
            k = [c // 4 for c in fl].count(h1 // 4); other = [c // 4 for c in fl if c // 4 != h1 // 4]
            if k == 1 and other[0] != other[1]: sets += 1                    # set exact : une carte du rang de la paire, pas de paire au tableau (sinon full)
        fd += draw; flush += isflush
    return n, hit, sets, fd, flush


@pytest.fixture(scope='module')
def t():
    return E.table()


def test_known_values():
    c = E.hit_chances('AKs')
    assert abs(c['tirage_couleur'] - 1090) <= 5 and abs(c['couleur'] - 84) <= 2          # 10,9 % et 0,84 %
    aa = E.hit_chances('AA')
    assert abs(aa['set'] - 1078) <= 2 and abs(aa['carre'] - 24) <= 1 and aa['au_moins_paire'] == 10000
    assert abs(E.hit_chances('72o')['brelan'] - 135) <= 1                               # brelan avec une paire du tableau : 1,35 %
    assert E.hit_chances('72o')['au_moins_paire'] == round(10000 * (1 - 13244 / 19600))  # 32,43 % : aucun des 6 rangs de la main sur le tableau
    assert abs(E.equity_random('AA') - 8520) <= 5 and abs(E.equity_random('AKs') - 6705) <= 5 and abs(E.equity_random('72o') - 3458) <= 5


def test_exclusive_categories_sum_to_100_and_cumulatives_are_consistent(t):
    for h in t['hands']:
        c = E.hit_chances(h)
        assert sum(c[k] for k in E.HITS) == 10000, h
        for k, (_, parts) in E.CUMUL.items(): assert c[k] == sum(c[p] for p in parts), (h, k)
        assert c['au_moins_paire'] >= c['au_moins_top_paire'] >= c['au_moins_double_paire'] >= c['au_moins_brelan'] >= c['au_moins_suite'] >= c['au_moins_couleur'] >= c['au_moins_full']
        assert all(0 <= c[k] <= 10000 for k in E.KEYS)
        assert c['tirage_couleur_et_quinte'] <= min(c['tirage_couleur'], c['tirage_quinte_8'] + c['tirage_quinte_4'])
    assert all(E.hit_chances(h)['set'] == 0 for h in t['hands'] if len(h) == 3)           # pas de set sans paire de poche
    assert all(E.hit_chances(h)['paire_poche_sur_tableau'] == 0 for h in t['hands'] if len(h) == 3)


def test_hand_is_removed_from_the_deck_and_matches_an_independent_count():
    from spinsacademy.cards import W
    from spinsacademy.postflop import flop_hits
    _, _, n = flop_hits.counts()
    assert all(int(n[i]) == int(W[i]) * 19600 for i in range(169))                     # 19 600 flops par combinaison (50 cartes restantes)
    for name, (a, b) in {'AKs': ('As', 'Ks'), '72o': ('7d', '2c'), '99': ('9h', '9c'), 'T9s': ('Td', '9d')}.items():
        total, hit, sets, fd, flush = brute(card(a), card(b)); assert total == 19600
        c = E.hit_chances(name)
        assert abs(c['au_moins_paire'] - 10000 * hit / total) <= 1.5, name
        assert abs(c['set'] - 10000 * sets / total) <= 1.5, name
        assert abs(c['tirage_couleur'] - 10000 * fd / total) <= 1.5, name
        assert abs(c['couleur'] + c['quinte_flush'] - 10000 * flush / total) <= 1.5, name


def test_equity_against_bank_ranges():
    ids = [r['id'] for r in E.ranges()]
    assert {'hu8_sb_tapis', 'hu8_bb_paie', '3j8_btn_tapis'} <= set(ids)
    for r in E.ranges(): assert 0 < r['share'] <= 10000 and r['label_fr'] and r['spot']
    for rid in ids:
        vals = {h: E.equity_vs_range(h, rid) for h in E.table()['hands']}
        assert all(v is None or 0 <= v <= 10000 for v in vals.values())
        assert vals['AA'] > vals['KK'] > vals['72o'], rid
    assert E.equity_vs_range('AA', 'hu8_sb_tapis') > E.equity_random('72o')


def test_labels_carry_their_rule_threshold_and_measured_value(t):
    defs = t['labels_def']; assert len({d['id'] for d in defs}) == len(defs) >= 12
    for d in defs:
        assert d['groupe'] in ('force', 'faiblesse') and d['fr'] and d['regle_fr'] and d['seuil'] is not None and 'sens' in d
    by = {d['id']: d for d in defs}
    for h in t['hands']:
        for l in E.labels(h):
            d = by[l['id']]; seuil = d['seuil'] if isinstance(d['seuil'], list) else [d['seuil']]
            if d['sens'] == '>=': assert l['valeur'] >= min(seuil), (h, l['id'])
            if d['sens'] == '<': assert l['valeur'] < max(seuil), (h, l['id'])
    ids = lambda h: {l['id'] for l in E.labels(h)}
    assert {'assortie', 'bloque_les_as', 'forte_contre_au_hasard'} <= ids('AKs') and 'dominee' not in ids('AKs')
    assert {'dominee', 'depareillee'} <= ids('K5o') and 'connectee' in ids('98s') and 'paire_de_poche' in ids('77')
    assert {'faible_contre_au_hasard', 'cartes_eloignees', 'top_paire_rarement'} <= ids('72o')


def test_runtime_does_not_need_numpy_and_size_is_bounded():
    code = "import sys; from spinsacademy import equities as e; e.hit_chances('AA'); e.labels('AKs'); e.equity_vs_range('AA','hu8_sb_tapis'); assert 'numpy' not in sys.modules and 'numba' not in sys.modules"
    subprocess.run([sys.executable, '-c', code], cwd=ROOT, check=True)
    assert os.path.getsize(E.PATH) < 60_000


def test_table_is_regenerated_identically():
    assert E._dump(E.build()) == open(E.PATH, encoding='utf-8').read()


def test_pairs_do_not_carry_labels_that_make_no_sense_for_them(t):
    """retour de la session Équité : 22 était « fait souvent la top paire ou mieux » (la double paire comprend la paire du tableau)"""
    for h in t['hands']:
        if len(h) == 2:
            ids = {l['id'] for l in E.labels(h)}
            assert ids.isdisjoint({'top_paire_souvent', 'top_paire_rarement', 'paire_faible', 'cartes_hautes', 'depareillee', 'cartes_eloignees', 'dominee', 'connectee'}), (h, ids)
            assert 'paire_de_poche' in ids


def test_measures_are_given_for_every_hand_even_when_no_label_applies(t):
    for h in t['hands']:
        m = E.measures_of(h)
        assert {'domination', 'part_paire_faible', 'equity_random', 'au_moins_top_paire', 'tirage_couleur'} <= set(m)
        for l in E.labels(h): assert l['valeur'] == m[{'top_paire_souvent': 'au_moins_top_paire', 'top_paire_rarement': 'au_moins_top_paire', 'dominee': 'domination',
                                                    'paire_faible': 'part_paire_faible', 'forte_contre_au_hasard': 'equity_random', 'faible_contre_au_hasard': 'equity_random'}[l['id']]] \
            if l['id'] in ('top_paire_souvent', 'top_paire_rarement', 'dominee', 'paire_faible', 'forte_contre_au_hasard', 'faible_contre_au_hasard') else True

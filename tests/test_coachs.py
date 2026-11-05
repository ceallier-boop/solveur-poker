"""T8 (décision du porteur du 05/11, docs/produit/DECISIONS_2026-11-05.md §3) : les réponses des trois coachs (relecture du
30/10, docs/relecture/solveur_2026-10-30) rejouées contre la correction servie, désaccords compris. Chaque action donnée par au
moins un coach doit être acceptée ; quand ils se partagent 2 contre 1, la majorité est la recommandée (« 2 coachs sur 3 »).

Les coachs ont répondu sur la banque pilote du solveur (gto_preflop/2026.10.29-s1). La banque du test fermé (2026.11.02-s2) a un
autre arbre : ses situations sont retrouvées par leur nom sans l'empreinte de l'arbre, et une relance des coachs est rapportée à
la seule relance non all-in proposée quand la taille diffère (2,3 BB → 2 BB au BTN)."""
import collections, csv, json, os, re
import pytest
from spinsacademy import quiz

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(ROOT, 'docs', 'relecture', 'solveur_2026-10-30')
EXPECTED = os.path.join(REVIEW, 'attendu_correction.csv')
COACHES = ('Lucho', 'Lucky', 'PA')
PILOT = 'gto_preflop/2026.10.29-s1'
CLOSED_TEST = 'gto_preflop/2026.11.02-s2'
TYPES = {'FOLD': ('fold',), 'CHECK': ('check',), 'CALL': ('call', 'call_allin', 'limp'), 'ALL-IN': ('allin',), 'RAISE': ('raise',)}


def _csv(name):
    with open(os.path.join(REVIEW, name), encoding='utf-8-sig') as f: return list(csv.DictReader(f, delimiter=';'))


def key(): return {r['id']: r for r in _csv('cle.csv')}


def answers():
    out = collections.defaultdict(dict)
    for c in COACHES:
        for r in _csv(f'reponses_{c.lower()}.csv'): out[r['id']][r['coach']] = r['meilleure_action']
    return out


def action_id(sp, label):
    """l'option du spot que désigne le libellé d'un coach (« RAISE TO 2,3 BB », « CALL 0,5 BB »…), None si aucune ou plusieurs"""
    word = label.split()[0]
    c = [a for a in sp['actions'] if a['type'] in TYPES[word]]
    if word == 'RAISE' and len(c) > 1:
        to = float(re.search(r'([\d,]+) BB', label).group(1).replace(',', '.'))
        c = [a for a in c if abs(a['to_bb'] - to) < 0.01]
    return c[0]['id'] if len(c) == 1 else None


def situation(spot_id): return spot_id.rsplit('-', 1)[0]           # nom de la situation sans l'empreinte de l'arbre


def spot_in(version, spot_id):
    _, spots = quiz.load(version)
    if spot_id in spots: return spots[spot_id]
    by = {situation(s): sp for s, sp in spots.items()}
    return by.get(situation(spot_id))


def expected_rows():
    """une ligne par situation : actions des coachs, recommandée et nuance (table attendue de la correction)"""
    k, ans = key(), answers(); rows = []
    for sid in sorted(k):
        votes = collections.Counter(ans[sid].values()); (top, n), = votes.most_common(1)
        rows.append(dict(id=sid, spot=k[sid]['spot'], main=k[sid]['main'], acceptees=' | '.join(sorted(votes)),
                         recommandee=top, nuance=f'{n} coachs sur 3',
                         minoritaire=' | '.join(f'{a} ({", ".join(c for c in COACHES if ans[sid][c] == a)})' for a in sorted(votes) if a != top)))
    return rows


def coach_cases(version):
    """(situation, main, action des coachs, option du spot) pour chaque action distincte, là où la main est proposable"""
    k, ans = key(), answers(); cases, missing = [], []
    for sid in sorted(k):
        sp = spot_in(version, k[sid]['spot']); hand = k[sid]['main']
        if sp is None or not sp['hands'].get(hand, {}).get('quiz_eligible', True): missing.append(sid); continue
        for label in sorted(set(ans[sid].values())): cases.append((sid, sp['spot_id'], hand, label, action_id(sp, label)))
    return cases, missing


def test_corpus_complete_and_labels_legal():
    k, ans = key(), answers()
    assert len(k) == 60 and sorted(ans) == sorted(k)
    assert all(sorted(a) == sorted(COACHES) for a in ans.values()), 'chaque situation a une réponse de chaque coach'
    split = collections.Counter(tuple(sorted(collections.Counter(a.values()).values(), reverse=True)) for a in ans.values())
    assert split == {(3,): 47, (2, 1): 13}, f'répartition des votes changée : {split}'
    cases, missing = coach_cases(PILOT)
    assert not missing, f'situations ou mains absentes de la banque pilote : {missing}'
    assert len(cases) == 73
    assert all(c[4] for c in cases), [c[:4] for c in cases if not c[4]]


def test_expected_table_matches_coach_answers():
    """attendu_correction.csv se régénère à l'identique depuis les réponses : python -m tests.test_coachs pour le réécrire"""
    with open(EXPECTED, encoding='utf-8') as f: assert list(csv.DictReader(f, delimiter=';')) == expected_rows()


def test_closed_test_bank_covers_most_situations():
    cases, missing = coach_cases(CLOSED_TEST)
    assert len(missing) <= 12, missing                     # 11 situations absentes de l'arbre, 1 main non proposable (05/11)
    assert all(c[4] for c in cases), [c[:4] for c in cases if not c[4]]


@pytest.mark.xfail(strict=True, reason="P7 (règle des désaccords) pas encore fusionnée : au 05/11, 53 actions sur 73 acceptées, 11 imprécisions, 9 erreurs")
def test_every_coach_action_is_accepted_pilot_bank():
    cases, _ = coach_cases(PILOT)
    refused = [(sid, hand, label, quiz.correct(PILOT, spot, hand, aid)['verdict']) for sid, spot, hand, label, aid in cases
               if quiz.correct(PILOT, spot, hand, aid)['verdict'] != 'correct']
    assert not refused, refused


@pytest.mark.xfail(strict=True, reason="P7 (règle des désaccords) pas encore fusionnée : au 05/11, 43 actions sur 56 acceptées, 12 imprécisions, 1 erreur")
def test_every_coach_action_is_accepted_closed_test_bank():
    cases, _ = coach_cases(CLOSED_TEST)
    refused = [(sid, hand, label, quiz.correct(CLOSED_TEST, spot, hand, aid)['verdict']) for sid, spot, hand, label, aid in cases
               if quiz.correct(CLOSED_TEST, spot, hand, aid)['verdict'] != 'correct']
    assert not refused, refused


if __name__ == '__main__':
    rows = expected_rows()
    with open(EXPECTED, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=';', lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print(f'{EXPECTED} : {len(rows)} situations')

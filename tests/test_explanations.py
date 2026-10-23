"""lot 1 de l'évaluation du MVP : nuance des 0,1 BB, règle à retenir, questions retenues, diagnostic unique"""
from spinsacademy import grading, progress, quiz
from spinsacademy.cards import NAMES


def _spots():
    _, spots = quiz.load(quiz.DEFAULT_VERSION)
    return spots


def test_pertinent_nuance_under_a_tenth_of_bb():
    seen = 0
    for sp in list(_spots().values())[:400]:
        if sp['ev_reference'] != 'hrc' or sp.get('villain'): continue
        for h in quiz.teachable(sp):
            ev = grading.reference_ev(sp, h); top = max(ev)
            for j, a in enumerate(sp['actions']):
                gap = 1000 * (top - ev[j])
                if not (3 * grading.TOLERANCE_MBB < gap <= grading.PERTINENT_MBB): continue
                g = grading.grade(sp, h, a['id']); r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, a['id'])
                assert g['verdict'] in ('correct', 'imprécision') and r['verdict'] != 'erreur'
                best = max(range(len(ev)), key=lambda k: ev[k])
                rb = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, sp['actions'][best]['id'])
                assert 'Nuance' in rb['explanation_fr'] and 'jouable' in rb['explanation_fr']
                seen += 1
                if seen >= 20: return
    assert seen > 0


def test_teachable_hands_keep_a_real_error():
    for sp in list(_spots().values())[:300]:
        for h in quiz.teachable(sp):
            assert any(grading.grade(sp, h, a['id'])['verdict'] == 'erreur' for a in sp['actions'])


def test_rule_to_remember_after_an_error():
    n = 0
    for sp in list(_spots().values())[:200]:
        hs = sorted(quiz.teachable(sp))
        if not hs: continue
        h = hs[0]
        bad = next(a['id'] for a in sp['actions'] if grading.grade(sp, h, a['id'])['verdict'] == 'erreur')
        r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, bad)
        assert 'À retenir :' in r['explanation_fr'] and f"au {sp['hero']}" in r['explanation_fr']
        n += 1
    assert n > 20


def test_threshold_rule_and_range_text():
    inside = {h: (h[0] == h[1]) or h.startswith('A') for h in NAMES}
    txt, fit = quiz.threshold_rule(inside, {h: 1.0 for h in NAMES})
    assert fit == 1.0 and txt.startswith('22+') and 'A2+' in txt
    assert quiz.range_text(['AA', 'KK', 'QQ', 'AKs', 'AQs']) == 'QQ+, AQs+'


def test_single_focus():
    assert progress.compute([])['focus']['kind'] == 'none'
    assert 'encore' in progress.compute([])['focus']['reason_fr']

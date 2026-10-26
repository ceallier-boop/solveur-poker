"""corrections du sixième test joueurs (26/10/2026)"""
import pytest
from fastapi.testclient import TestClient
from spinsacademy import field, quiz, ranges

FIELD = 'exploit_field/2026.10.23-1'
H = {'X-Player-Id': 's' * 32}


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv('SPINSACADEMY_DB', str(tmp_path / 'test.sqlite'))
    from spinsacademy.api import app
    return TestClient(app)


def test_range_only_from_main_tree_and_close_status():
    v = quiz.DEFAULT_VERSION; _, spots = quiz.load(v)
    assert 'hu-8-8-SB-call_BB-raise2-4cafcb' not in ranges.drawable(v)            # ATs grisée, A6s en jeu (Kevin)
    assert all(quiz.in_main_tree(v, spots[s]) for s in ranges.drawable(v))
    seen = set()
    for k in range(12):
        t = ranges.pick(v, seed=k)
        g = ranges.grade(t, [h for h, x in t['hands'].items() if x[0] < 0.5])      # tout à l'envers
        for h, st in g['cells'].items():
            f = t['hands'][h][0]; seen.add(st)
            if st == 'mixed': assert 0.25 < f < 0.75                                  # « mixte » respecte la légende
            if st == 'close': assert min(t['hands'][h][1], t['hands'][h][2]) < ranges.CLOSE_BB
    assert {'extra', 'missing'} & seen


def test_polarized_range_is_said():
    v = quiz.DEFAULT_VERSION; _, spots = quiz.load(v)
    t = ranges.task(spots['3w-10-10-10-root-45a7e8'])
    g = ranges.grade(t, [])
    assert 'les très grosses mains' in g['rule_fr'] and 'relancent' in g['rule_fr']


def test_rule_says_when_hand_is_an_exception():
    v = quiz.DEFAULT_VERSION; _, spots = quiz.load(v); n = 0
    for sp in list(spots.values())[:400]:
        for h, x in sp['hands'].items():
            if not x.get('quiz_eligible'): continue
            best = quiz.reference_action(sp, h); labels = {a['id']: quiz.action_label(sp, a) for a in sp['actions']}
            r = quiz.rule_to_remember(sp, best, labels, h)
            if 'exception' in r: n += 1; assert f"{h} est une exception" in r
    assert n > 0


def test_pastille_matches_stats_and_prompt_counts():
    _, spots = quiz.load(FIELD); shown = 0
    for sp in spots.values():
        f = sp['field']; p = field.pastille(f, sp['spot_id'])
        if p:
            shown += 1; assert field.fits(p, f)
            for st in f['stats']:
                if p == 'Dégène' and st['stat'] == 'limp_pct': assert st['observed_pct'] >= st['gto_pct'] - field.SENSE_TOL
        txt = field.served_prompt(sp)
        assert 'occasions dans cette situation' not in txt
        for st in f['stats']:
            if st.get('n') and st['n'] != f['observations'] and f" {st['k']} fois (" in sp['prompt_fr']:
                assert f" {st['k']} fois sur {st['n']} (" in txt
    assert shown > 300


def test_exploit_texts():
    _, spots = quiz.load(FIELD)
    for sp in spots.values():
        f = sp['field']
        if f['type'] in field.READ: continue
        r = quiz.correct(FIELD, sp['spot_id'], next(iter(sp['hands'])), f['correct'])
        txt = ' '.join([r['essential_fr'], r['remember_fr'] or ''] + r['why_fr'])
        assert 'checker ou pousser' not in txt and r['field']['type_fr'] != 'Piège'
        if sp['table'] == 'heads-up': assert 'tout le monde se couche' not in txt
        if field.pastille(f, sp['spot_id']): assert 'écart de stats' not in txt
        if f['rule'] == 'R15' and next(iter(sp['hands'])) in field.PREMIUM: assert 'son limp est fort' not in txt


def test_series_avoid_recent_hands(client):
    firsts = []; overlap = 0; prev = set()
    for k in range(4):
        s = client.post('/sessions', json={'mode': 'gto'}, headers=H).json(); cur = set()
        for i in range(s['size']):
            q = client.get(f"/quiz/next?session_id={s['session_id']}").json()['question']; cur.add((q['spot_id'], q['hand']))
            if i == 0: firsts.append(q['hand'])
        overlap += len(cur & prev); prev |= cur
    assert overlap == 0 and len(set(firsts)) == len(firsts)

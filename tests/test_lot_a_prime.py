"""lot A' (second test des 5 joueurs, 23/10/2026) : textes servis sans HRC ni coachs, corrections sans contradiction"""
import json, os, random, re
from spinsacademy import field, grading, quiz
from spinsacademy.hrc import ROOT

BANNED = re.compile(r'hrc|holdem resources|coach|lucho|lucky|pasg8|spinpro|kill tilt|professionnels', re.I)
WEB = os.path.join(ROOT, 'spinsacademy', 'web')


def _sample(ref, k, seed=3):
    pool = quiz.pool(ref); rnd = random.Random(seed)
    for sp in rnd.sample(pool, min(k, len(pool))):
        hands = list(sp['hands']) if sp.get('field') else list(quiz.teachable(sp))
        if not hands: continue
        h = rnd.choice(hands); q = quiz.question(ref, sp['spot_id'], h)
        yield sp, h, q, {o['id']: quiz.correct(ref, sp['spot_id'], h, o['id']) for o in q['options']}


def test_no_solver_brand_nor_coach_in_served_texts():
    for ref in (quiz.DEFAULT_FIELD, quiz.DEFAULT_VERSION):
        for sp, h, q, rs in _sample(ref, 400):
            blob = json.dumps([q, rs], ensure_ascii=False)
            m = BANNED.search(blob)
            assert not m, (sp['spot_id'], blob[max(0, m.start() - 80):m.end() + 40])
    for f in ('app.js', 'index.html', 'lexique.json'):
        m = BANNED.search(open(os.path.join(WEB, f), encoding='utf-8').read())
        assert not m, (f, m.group(0))
    assert 'À faire relire' not in open(os.path.join(WEB, 'lexique.json'), encoding='utf-8').read()


def test_corrections_are_consistent():
    for ref in (quiz.DEFAULT_FIELD, quiz.DEFAULT_VERSION):
        for sp, h, q, rs in _sample(ref, 300, seed=5):
            for aid, r in rs.items():
                text = r['explanation_fr'] + '\n' + '\n'.join(r['why_fr'])
                assert not re.search(r'\d,\d{3} BB', text), text                     # jamais 3 décimales
                assert 'Des joueurs parlent encore' not in text and 'Il semble ouvre' not in text
                assert not re.search(r'environ 0 % du temps|se couche 0 %', text), text
                assert 'aussi pertinente' not in text
                limits = set(re.findall(r'moins de (0,06|0,1) BB\)', text))
                assert len(limits) <= 1, text                                          # une seule limite du barème par correction
                if r['verdict'] == 'erreur': assert not text.startswith('Plusieurs bonnes décisions'), text
                if not sp.get('field'):
                    on = re.search(r'^On \w+(?: \w+)? avec (\d+) % ', text, re.M); keep = re.search(r'environ (\d+) % des mains', text)
                    if on and keep and 'on ne joue que' not in text: assert on.group(1) == keep.group(1), text


def test_exploit_lesson_postflop_and_cap():
    spots = list(quiz.load(quiz.DEFAULT_FIELD)[1].values()); capped = 0
    for sp in spots:
        f = sp['field']
        if f['type'] in field.READ: continue
        best_t = next(o['type'] for o in f['options'] if o['id'] == f['correct'])
        if f['rule'] == 'R13' and best_t == 'raise':
            r = field.correct(sp, f['correct']); assert 'pousse plus large' not in r['field']['rule_fr']
        if f['type'] == 'inconnu' and f['gto'] and f['gto'] != f['correct']:
            r = field.correct(sp, f['gto'])
            assert r['verdict'] in ('correct', 'imprécision'); capped += r['verdict'] == 'imprécision' and 'coup théorique' in r['explanation_fr']
    assert capped > 50
    for sp in spots[::11]:
        f = sp['field']
        if f['type'] in field.READ: continue
        best_t = next(o['type'] for o in f['options'] if o['id'] == f['correct'])
        r = field.correct(sp, f['correct'])
        assert (r['next'] is not None) == (best_t in field.FLOP_MOVES and bool(f.get('postflop')))
        text = r['explanation_fr'] + ' '.join(r['why_fr'])
        if best_t == 'check': assert "D'où plus d'agressivité" not in text
        if r['next'] and next(iter(sp['hands'])) not in ('AA', 'KK', 'QQ'): assert not any('AA ou KK' in l for l in r['next']['plan'])
    sample = [s for s in spots if s['field']['type'] == 'échantillon'][:40]
    for sp in sample:
        line = field.correct(sp, sp['field']['correct'])['explanation_fr'].split('\n')[0]
        st = max(sp['field']['stats'], key=lambda x: abs(x['observed_pct'] - x['gto_pct']))
        assert ('plus que la théorie' in line) == (st['observed_pct'] > st['gto_pct']), line


def test_amount_format_near_limits():
    assert field.bbx(62) == 'un peu plus de 0,06 BB' and field.bbx(140) == '0,14 BB' and field.bbx(3) == 'moins de 0,01 BB'
    assert quiz.verdict_line('erreur', 80) == "Plus de 0,06 BB d'écart : c'est une erreur."
    assert quiz.verdict_line('imprécision', 80, grading.PERTINENT_MBB) == 'Petit écart (moins de 0,1 BB) : imprécision, pas erreur.'

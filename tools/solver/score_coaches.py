"""Rejoue les actions des coachs (60 situations, tests/test_coachs.py) contre un dossier de résultats du solveur, sans publier de banque.

Les spots sont reconstruits depuis les résultats enregistrés (dataset.spots_of), écrits dans un dataset temporaire, puis chaque
action donnée par au moins un coach est notée par la correction de l'application (quiz.correct) : « correct » ou non.

Usage : python tools/solver/score_coaches.py data/solver/runs/sf3dc2e6_48fa0906 [data/solver/runs/<autre> ...] [--detail]
"""
import argparse, collections, glob, json, os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import grading, quiz  # noqa: E402
from spinsacademy.solver import dataset as ds  # noqa: E402
from tests import test_coachs as tc  # noqa: E402

CONFIGS = ('hu_25-25', 'hu_12-12', '3w_25-25-25', '3w_12-12-12')


def temp_bank(run_dir, tmp, real):
    name = 'run_' + os.path.basename(run_dir.rstrip('/'))
    d = os.path.join(tmp, 'gto_preflop', name); os.makedirs(d, exist_ok=True)
    base = json.load(open(os.path.join(real, 'gto_preflop', tc.CLOSED_TEST.split('/')[1], 'manifest.json')))
    spots = []
    for c in CONFIGS:
        p = os.path.join(run_dir, c + '.json')
        if os.path.isfile(p): spots += ds.spots_of(json.load(open(p)), p)[0]
    with open(os.path.join(d, 'spots.jsonl'), 'w') as f:
        for sp in spots: f.write(json.dumps(sp, ensure_ascii=False, separators=(',', ':')) + '\n')
    json.dump(dict(base, version=name, spots=len(spots)), open(os.path.join(d, 'manifest.json'), 'w'))
    return 'gto_preflop/' + name


def score(run_dir, detail=False):
    with tempfile.TemporaryDirectory() as tmp:
        real = quiz.DATASETS; quiz.DATASETS = tmp
        try:
            ref = temp_bank(run_dir, tmp, real); quiz.load.cache_clear()
            cases, missing = tc.coach_cases(ref)
            ok = []; ko = []
            for sid, spot, hand, label, aid in cases:
                # le verdict du solveur seul : quiz.correct accepte de force toute action d'un coach (décision du 05/11), ce qui vaut 100 % par construction
                v = grading.grade(quiz.load(ref)[1][spot], hand, aid)['verdict'] if aid else 'sans option'
                (ok if v == 'correct' else ko).append((sid, hand, label, v))
        finally:
            quiz.DATASETS = real; quiz.load.cache_clear()
    return len(cases), ok, ko, missing


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('runs', nargs='+'); ap.add_argument('--detail', action='store_true'); a = ap.parse_args()
    for r in a.runs:
        n, ok, ko, missing = score(r)
        rec = {x['id']: x['recommandee'] for x in tc.expected_rows()}
        maj_ok = [x for x in ok if x[2] == rec[x[0]]]; maj_n = len({x[0] for x in ok + ko})
        print(f'{os.path.basename(r.rstrip("/"))} : {len(ok)} actions de coachs acceptées par le solveur seul sur {n} ; '
              f'action recommandée acceptée dans {len(maj_ok)} situations sur {maj_n} ({len(missing)} situations absentes)')
        if a.detail:
            for sid, hand, label, v in ko: print(f'   refusée {sid} {hand} {label} ({v})' + ('  [recommandée]' if label == rec[sid] else ''))


if __name__ == '__main__':
    main()

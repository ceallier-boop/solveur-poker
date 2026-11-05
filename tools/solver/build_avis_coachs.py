"""Avis des coachs (relecture du 30/10/2026) -> spinsacademy/data/avis_coachs.json, lu par spinsacademy/coachs.py.

Une entrée par situation et par main : le nombre de coachs derrière chaque action (jamais leur nom : l'application ne cite
aucun coach). Se relance à l'identique : python tools/solver/build_avis_coachs.py ; tests/test_avis_coachs.py le vérifie."""
import collections, csv, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REVIEW = os.path.join(ROOT, 'docs', 'relecture', 'solveur_2026-10-30')
OUT = os.path.join(ROOT, 'spinsacademy', 'data', 'avis_coachs.json')
COACHES = ('lucho', 'lucky', 'pa')


def _csv(name):
    with open(os.path.join(REVIEW, name), encoding='utf-8-sig') as f: return list(csv.DictReader(f, delimiter=';'))


def build():
    key = {r['id']: r for r in _csv('cle.csv')}; votes = collections.defaultdict(collections.Counter)
    for c in COACHES:
        for r in _csv(f'reponses_{c}.csv'): votes[r['id']][r['meilleure_action']] += 1
    avis = {}
    for sid in sorted(key):
        spot = key[sid]['spot'].rsplit('-', 1)[0]                      # nom de la situation, sans l'empreinte de l'arbre
        avis[f"{spot}|{key[sid]['main']}"] = dict(coachs=sum(votes[sid].values()), votes=dict(sorted(votes[sid].items())))
    return dict(source='relecture du 30/10/2026 (docs/relecture/solveur_2026-10-30)', avis=avis)


if __name__ == '__main__':
    data = build()
    with open(OUT, 'w', encoding='utf-8', newline='') as f: json.dump(data, f, ensure_ascii=False, indent=1, sort_keys=True); f.write('\n')
    print(f"{OUT} : {len(data['avis'])} situations")

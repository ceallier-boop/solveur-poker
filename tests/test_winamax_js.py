"""lecteur Winamax du navigateur (spinsacademy/web/winamax.js) lancé sous Node : mêmes sorties que tools/field/winamax_counts.py
sur les mains d'exemple (tests/data/winamax, pseudos inventés), décisions du héros sans pseudo, fichiers illisibles et hors Expresso"""
import json, os, re, shutil, subprocess, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'field'))
import winamax_counts as wc

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'winamax')
RUN = os.path.join(HERE, 'js', 'winamax_run.cjs')
NODE = shutil.which('node')
pytestmark = pytest.mark.skipif(NODE is None, reason='Node absent')
PSEUDOS = ('Alpha_Test', 'Beta Joueur', 'Gamma77')


def run_js(folder):
    out = subprocess.run([NODE, RUN, folder], capture_output=True, text=True, encoding='utf-8', timeout=60)
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout)


@pytest.fixture(scope='module')
def both(tmp_path_factory):
    py = tmp_path_factory.mktemp('py')
    wc.main([DATA, '--sortie', str(py)])
    return run_js(DATA), py


def test_csv_identical_to_python(both):
    js, py = both
    for f in ('comptages.csv', 'volume.csv'):
        assert js['csv'][f] == (py / f).read_text(encoding='utf-8'), f
    assert js['version'] == wc.VERSION and js['result']['version'] == wc.VERSION


def test_every_situation_covered(both):
    js, _ = both
    assert {(c['kind'], c['decision']) for c in js['result']['counts']} == {(k, d) for (k, _, _), d in wc.SITU.items()}


def test_counts_and_files(both):
    js, py = both
    r = js['result']
    rep = json.loads((py / 'rapport.json').read_text(encoding='utf-8'))
    assert r['hands'] == rep['expresso'] and r['unreadable'] == rep['unreadable'] == 1      # fichier sans grosse blinde
    assert r['by_table'] == {'hu': rep['hu'], '3w': rep['three']} and r['months'] == rep['months']
    assert r['ignored'] == 1                                                                 # tournoi « Monster Stack »
    assert r['files'] == rep['files'] and r['skipped_files'] == 2                            # résumé de tournoi, generer.py
    assert js['progress'] == r['files']


def test_hero_decisions_without_any_pseudo(both):
    js, _ = both
    r = js['result']
    body = json.dumps(r, ensure_ascii=False)
    for p in PSEUDOS + ('424242', '777'):
        assert p not in body
    hd = r['hero_decisions']
    assert hd and set(hd[0]) == {'table', 'position', 'stack_bb', 'history', 'decision', 'hero_hand', 'action', 'to_bb', 'month'}
    assert {d['position'] for d in hd} == {'BTN', 'SB', 'BB'} and {d['table'] for d in hd} == {'hu', '3w'}
    assert all(re.fullmatch(r'[AKQJT2-9]{2}[so]?', d['hero_hand']) for d in hd)
    assert all(re.fullmatch(r'\d{4}-\d{2}', d['month']) for d in hd)
    assert {d['action'] for d in hd} <= {'fold', 'check', 'limp', 'paie', 'relance', 'tapis'}
    first = [d for d in hd if d['table'] == '3w' and d['position'] == 'BTN' and d['history'] == '']
    assert first and all(d['decision'] == 'BTN premier à parler' for d in first)
    opens = [d for d in hd if d['action'] == 'relance' and d['history'] == '' and d['table'] == '3w']
    assert opens and all(d['to_bb'] == 2.0 for d in opens)                                  # BTN « raises 20 to 40 » : 2 BB


def test_unreadable_and_other_format_alone(tmp_path):
    for name in ('20261004_Expresso(7799)_real_holdem_no-limit.txt', '20261005_Monster Stack(1)_real_holdem_no-limit.txt'):
        shutil.copy(os.path.join(DATA, name), tmp_path / name)
    r = run_js(str(tmp_path))['result']
    assert (r['hands'], r['unreadable'], r['ignored'], r['counts'], r['hero_decisions']) == (0, 1, 1, [], [])
    assert all(v['n'] == 0 and v['status'] == 'insuffisant' for v in r['volume'])


def test_leak_check_refuses(tmp_path):
    js = (f"const fs=require('fs'),vm=require('vm');const c={{window:{{}},setTimeout,Promise}};vm.createContext(c);"
          f"vm.runInContext(fs.readFileSync({json.dumps(os.path.join(HERE, '..', 'spinsacademy', 'web', 'winamax.js'))},'utf8'),c);"
          "const a=c.window.Winamax._internal.assertNoNames;let refused=false;"
          "try{a({x:'Gamma77 a payé'},['Gamma77'])}catch(e){refused=true}"
          "a({x:'fold AKs 12'},['fold','AKs','12']);process.stdout.write(String(refused))")
    out = subprocess.run([NODE, '-e', js], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0, out.stderr
    assert out.stdout == 'true'


def test_samples_are_reproducible(tmp_path):
    """les mains d'exemple versionnées sont celles que produit generer.py"""
    gen = os.path.join(DATA, 'generer.py')
    shutil.copy(gen, tmp_path / 'generer.py')
    subprocess.run([sys.executable, str(tmp_path / 'generer.py')], check=True)
    for f in os.listdir(DATA):
        if f.endswith('.txt'):
            assert (tmp_path / f).read_bytes() == open(os.path.join(DATA, f), 'rb').read(), f

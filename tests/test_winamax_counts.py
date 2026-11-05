"""lecteur d'historique Winamax (tools/field/winamax_counts.py) : décisions, tapis, agrégation, aucun pseudo écrit"""
import csv, os, sys, zipfile
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools', 'field'))
import winamax_counts as wc


def hand3(acts, stacks=(500, 500, 500), hero='Moi', names=('Moi', 'Zorglub77', 'Bidule Truc'), hid=1):
    """main Expresso à 3 joueurs : siège 1 au bouton, 2 au SB, 3 au BB ; blinds 10 / 20"""
    n = names
    return '\n'.join([
        f'Winamax Poker - Tournament "Expresso" buyIn: 4.65€ + 0.35€ level: 1 - HandId: #99887766-{hid}-1667487600 - Holdem no limit (10/20) - 2026/10/03 15:00:00 UTC',
        "Table: 'Expresso(612345678)#0' 3-max (real money) Seat #1 is the button",
        f'Seat 1: {n[0]} ({stacks[0]})', f'Seat 2: {n[1]} ({stacks[1]})', f'Seat 3: {n[2]} ({stacks[2]})',
        '*** ANTE/BLINDS ***', f'{n[1]} posts small blind 10', f'{n[2]} posts big blind 20', f'Dealt to {hero} [Ah 7c]',
        '*** PRE-FLOP *** '] + acts + ['*** SUMMARY ***', 'Total pot 40 | No rake', ''])


def hand_hu(acts, stacks=(300, 700), names=('Moi', 'Zorglub77')):
    """heads-up : siège 1 au bouton (SB), siège 2 au BB"""
    n = names
    return '\n'.join([
        'Winamax Poker - Tournament "Expresso Nitro" buyIn: 4.65€ + 0.35€ level: 2 - HandId: #99887766-9-1667487600 - Holdem no limit (15/30) - 2026/11/01 15:00:00 UTC',
        "Table: 'Expresso(612345678)#0' 3-max (real money) Seat #1 is the button",
        f'Seat 1: {n[0]} ({stacks[0]})', f'Seat 2: {n[1]} ({stacks[1]})',
        '*** ANTE/BLINDS ***', f'{n[0]} posts small blind 15', f'{n[1]} posts big blind 30', f'Dealt to {n[0]} [Kd Qs]',
        '*** PRE-FLOP *** '] + acts + ['*** SUMMARY ***', ''])


def decs(text):
    return [d[1:] for d in wc.decisions(wc.parse(next(wc.split_hands(text)).copy()))]


def test_three_way_shove_and_calls():
    t = hand3(['Moi raises 480 to 500 and is all-in', 'Zorglub77 folds', 'Bidule Truc calls 480 and is all-in'])
    assert decs(t) == [('3w', 'BTN premier à parler', 'tapis', 25.0), ('3w', 'SB face au tapis du BTN', 'fold', 25.0),
                       ('3w', 'BB face au tapis du BTN (SB fold)', 'paie', 25.0)]


def test_limp_iso_and_effective_stack():
    t = hand3(['Moi folds', 'Zorglub77 calls 10', 'Bidule Truc raises 140 to 160 and is all-in', 'Zorglub77 calls 140'],
              stacks=(500, 400, 160))
    assert decs(t) == [('3w', 'BTN premier à parler', 'fold', 20.0), ('3w', 'SB premier à parler (BTN fold)', 'limp', 8.0),
                       ('3w', 'BB face au limp du SB (BTN fold)', 'tapis', 8.0),
                       ('3w', 'SB face au tapis du BB après son limp (BTN fold)', 'paie', 8.0)]
    assert wc.bucket(8.0) == 8 and wc.bucket(13.4) == 12 and wc.bucket(40) == 25 and wc.bucket(3.2) == 4


def test_heads_up_open_and_short_blind():
    assert decs(hand_hu(['Moi raises 30 to 60', 'Zorglub77 calls 30'])) == \
        [('hu', 'SB premier à parler', 'relance', 10.0), ('hu', "BB face à l'open du SB", 'paie', 10.0)]
    assert decs(hand_hu(['Moi raises 255 to 300 and is all-in', 'Zorglub77 folds'])) == \
        [('hu', 'SB premier à parler', 'tapis', 10.0), ('hu', 'BB face au tapis du SB', 'fold', 10.0)]
    assert wc.num('1 000') == 1000 and wc.num('1,000') == 1000 and wc.num('12,5') == 12.5 and wc.num('0.40€') == 0.4


def test_other_formats_and_play_money_skipped():
    assert wc.parse(hand3([]).replace('"Expresso"', '"Monster Stack"').splitlines()) is None
    assert wc.parse(hand3([]).replace('"Expresso"', '"Monster Stack"').splitlines(), all_formats=True) is not None
    assert wc.parse(hand3([]).replace('real money', 'play money').splitlines()) is None


def test_counts_written_without_any_pseudo(tmp_path):
    src = tmp_path / 'history' / 'compte'; src.mkdir(parents=True)
    hands = [hand3(['Moi folds', 'Zorglub77 raises 480 to 500 and is all-in', 'Bidule Truc folds'], hid=i) for i in range(60)]
    hands += [hand3(['Bidule Truc raises 480 to 500 and is all-in', 'Moi folds', 'Zorglub77 calls 480 and is all-in'],
                    names=('Bidule Truc', 'Moi', 'Zorglub77'), hid=100 + i) for i in range(30)]
    (src / '20261003_Expresso(612345678)_real_holdem_no-limit.txt').write_text('\n\n'.join(hands), encoding='utf-8-sig')
    (src / '20261003_Expresso(612345678)_real_holdem_no-limit_summary.txt').write_text('Zorglub77 finished 1st', encoding='utf-8')
    out = tmp_path / 'sortie'
    wc.main([str(tmp_path / 'history'), '--sortie', str(out)])
    body = ''.join((out / f).read_text(encoding='utf-8') for f in os.listdir(out))
    assert 'Zorglub77' not in body and 'Bidule' not in body and 'Moi' not in body and '612345678' not in body and '99887766' not in body
    rows = {(r['kind'], r['decision'], r['action'], r['stack']): (int(r['n']), int(r['k'])) for r in csv.DictReader(open(out / 'comptages.csv', encoding='utf-8'))}
    assert rows[('3w', 'SB premier à parler (BTN fold)', 'tapis', '25')] == (60, 60)
    assert rows[('3w', 'BB face au tapis du SB (BTN fold)', 'fold', '25')] == (60, 60)
    assert rows[('3w', 'BTN premier à parler', 'tapis', '25')] == (30, 30)              # le héros (Moi) n'est jamais compté
    assert ('3w', 'BTN premier à parler', 'fold', '25') not in rows and ('3w', 'SB face au tapis du BTN', 'fold', '25') not in rows
    assert rows[('3w', 'BB face au tapis du BTN (SB fold)', 'paie', '25')] == (30, 30)
    vol = list(csv.DictReader(open(out / 'volume.csv', encoding='utf-8')))
    assert {r['statut'] for r in vol} <= {'fiable', 'indicatif', 'insuffisant'} and any(r['statut'] == 'indicatif' for r in vol)
    assert 'Période : 2026-10 à 2026-10' in (out / 'rapport.txt').read_text(encoding='utf-8')
    z = tmp_path / 'h.zip'
    with zipfile.ZipFile(z, 'w') as f: f.write(src / '20261003_Expresso(612345678)_real_holdem_no-limit.txt', 'a/b.txt')
    wc.main([str(z), '--sortie', str(tmp_path / 's2')])
    assert (tmp_path / 's2' / 'comptages.csv').read_text(encoding='utf-8') == (out / 'comptages.csv').read_text(encoding='utf-8')


def test_leak_check_refuses_to_write(tmp_path, monkeypatch):
    meta = dict(files=1, hands=1, expresso=1, unreadable=0, hu=0, three=1, months=set(), heroes={'Moi'}, names={'Zorglub77'})
    monkeypatch.setattr(wc, 'VERSION', 'Zorglub77')                    # simule un pseudo qui se glisserait dans le rapport
    with pytest.raises(SystemExit):
        wc.write({}, {}, {}, meta, str(tmp_path / 'x'))
    assert not (tmp_path / 'x' / 'rapport.txt').exists()

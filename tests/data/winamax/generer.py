"""Génère les mains d'exemple (pseudos inventés) des tests du lecteur Winamax : python tests/data/winamax/generer.py
Couvre chaque situation de winamax_counts.SITU, le héros à chaque place, des tapis inégaux, une blinde à tapis, des fins de
ligne Windows avec BOM, un fichier illisible, un tournoi autre que l'Expresso et un résumé de tournoi (ignoré)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = ('Alpha_Test', 'Beta Joueur', 'Gamma77')
CARDS = ('[Ah Kd]', '[7c 7d]', '[Qs Js]', '[9h 2c]', '[Td 8d]', '[As 5s]')

# (table, séquence d'actions) : {B}, {S}, {G} = BTN, SB, BB à 3 joueurs ; {S}, {G} = SB (bouton), BB en heads-up ; T = tapis du joueur
SEQ3 = [
    ['{B} folds', '{S} raises {TS} to {AS} and is all-in', '{G} folds'],
    ['{B} folds', '{S} calls 10', '{G} raises {TG} to {AG} and is all-in', '{S} calls {CS} and is all-in'],
    ['{B} folds', '{S} calls 10', '{G} raises 40 to 60', '{S} folds'],
    ['{B} folds', '{S} raises 30 to 40', '{G} calls 20'],
    ['{B} raises {TB} to {AB} and is all-in', '{S} calls {CS} and is all-in', '{G} folds'],
    ['{B} raises {TB} to {AB} and is all-in', '{S} folds', '{G} calls {CG} and is all-in'],
    ['{B} raises 20 to 40', '{S} folds', '{G} raises {TG} to {AG} and is all-in', '{B} calls {CB} and is all-in'],
    ['{B} calls 20', '{S} folds', '{G} checks'],
    ['{B} calls 20', '{S} calls 10', '{G} checks'],
]
SEQHU = [
    ['{S} raises {TS} to {AS} and is all-in', '{G} calls {CG} and is all-in'],
    ['{S} calls 10', '{G} raises {TG} to {AG} and is all-in', '{S} folds'],
    ['{S} calls 10', '{G} raises 40 to 60', '{S} calls 40'],
    ['{S} raises 20 to 40', '{G} folds'],
    ['{S} calls 10', '{G} checks'],
]


def hand(hid, title, seats, hero, seq, card, month='2026/10/03'):
    """seats : [(pseudo, tapis)] dans l'ordre BTN, SB, BB (3 joueurs) ou SB, BB (heads-up) ; blinds 10 / 20"""
    three = len(seats) == 3
    pos = dict(zip(('B', 'S', 'G') if three else ('S', 'G'), seats))
    sb, bb = (seats[1], seats[2]) if three else (seats[0], seats[1])
    posted = {sb[0]: min(10, sb[1]), bb[0]: min(20, bb[1])}
    v = {}
    for k, (nm, st) in pos.items():
        v[k] = nm; v['A' + k] = st; v['T' + k] = st - 20; v['C' + k] = st - posted.get(nm, 0)
    lines = [f'Winamax Poker - Tournament "{title}" buyIn: 4.65€ + 0.35€ level: 1 - HandId: #424242-{hid}-1667487600 - Holdem no limit (10/20) - {month} 15:00:00 UTC',
             f"Table: '{title}(777)#0' 3-max (real money) Seat #1 is the button"]
    lines += [f'Seat {i + 1}: {nm} ({st})' for i, (nm, st) in enumerate(seats)]
    lines += ['*** ANTE/BLINDS ***', f'{sb[0]} posts small blind {posted[sb[0]]}', f'{bb[0]} posts big blind {posted[bb[0]]}',
              f'Dealt to {hero} {card}', '*** PRE-FLOP *** ']
    lines += [a.format(**v) for a in seq]
    lines += ['*** FLOP *** [2c 7h Kd]', f'{seats[-1][0]} checks', '*** SUMMARY ***', 'Total pot 40 | No rake', '']
    return '\n'.join(lines)


def main():
    hid, files = 0, {}
    for f, stacks in enumerate([(500, 500, 500), (160, 400, 240), (90, 300, 610), (200, 15, 785)]):
        out = []
        for rot in range(3):
            seats = [(NAMES[(i + rot) % 3], stacks[i]) for i in range(3)]
            for s, seq in enumerate(SEQ3):
                hid += 1; out.append(hand(hid, 'Expresso', seats, NAMES[0], seq, CARDS[(hid + s) % len(CARDS)]))
        files[f'20261003_Expresso(777{f})_real_holdem_no-limit.txt'] = '\n\n'.join(out)
    out = []
    for stacks in [(300, 300), (120, 700), (640, 180)]:
        for rot in range(2):
            seats = [(NAMES[(i + rot) % 2], stacks[i]) for i in range(2)]
            for s, seq in enumerate(SEQHU):
                hid += 1; out.append(hand(hid, 'Expresso Nitro', seats, NAMES[0], seq, CARDS[(hid + s) % len(CARDS)], month='2026/11/01'))
    files['20261101_Expresso Nitro(7790)_real_holdem_no-limit.txt'] = '\r\n\r\n'.join(x.replace('\n', '\r\n') for x in out)
    bad = hand(900, 'Expresso', [(NAMES[0], 500), (NAMES[1], 500), (NAMES[2], 500)], NAMES[0], SEQ3[0], CARDS[0]).split('\n')
    files['20261004_Expresso(7799)_real_holdem_no-limit.txt'] = '\n'.join(l for l in bad if 'big blind' not in l)
    files['20261005_Monster Stack(1)_real_holdem_no-limit.txt'] = hand(901, 'Monster Stack', [(NAMES[0], 500), (NAMES[1], 500), (NAMES[2], 500)], NAMES[0], SEQ3[4], CARDS[1])
    files['20261003_Expresso(7770)_real_holdem_no-limit_summary.txt'] = 'Winamax Poker - Tournament summary : Expresso(7770)\nPlayer : Alpha_Test\n'
    for name, body in files.items():
        with open(os.path.join(HERE, name), 'w', encoding='utf-8-sig' if 'Nitro' in name else 'utf-8', newline='') as fh: fh.write(body)


if __name__ == '__main__':
    main()

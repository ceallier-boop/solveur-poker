"""Exporte, à partir des exports HRC, les ranges des lignes de flop principales (fréquences par classe de main) : fichier d'entrée autonome pour les tests."""
import json, numpy as np
import hrc_surrogate as hs
import flop_lines as fl
from hrcdata import W

def node_of(kind, S, key):
    base = hs.EQ3 if kind == '3w' else hs.EQHU
    v = base[S]; loc = v[0] if isinstance(v, list) else v
    return hs.sol(kind, loc)[1][key], hs._loc(kind, loc)

def freq(node, label):
    return [round(float(x), 5) for x in node['w'] * node['played'][:, node['labels'].index(label)]]

SPEC = [
 ('hu', 'SB paie ; BB check', 'Heads-up : SB limp, BB check', [('SB', 'IP', '', 'C'), ('BB', 'OOP', '0C', 'X')]),
 ('hu', 'SB raise 3.5 ; BB paie', 'Heads-up : SB raise 3,5, BB call', [('SB', 'IP', '', 'R3.5'), ('BB', 'OOP', '0R3.5', 'C')]),
 ('3w', 'BTN fold ; SB paie ; BB check', '3 joueurs, BTN fold : SB limp, BB check', [('SB', 'OOP', '0F', 'C'), ('BB', 'IP', '0F-1C', 'X')]),
 ('3w', 'BTN fold ; SB raise 3.5 ; BB paie', '3 joueurs, BTN fold : SB raise 3,5, BB call', [('SB', 'OOP', '0F', 'R3.5'), ('BB', 'IP', '0F-1R3.5', 'C')]),
 ('3w', 'BTN raise 2.3 ; SB fold ; BB paie', '3 joueurs : BTN raise 2,3, SB fold, BB call', [('BTN', 'IP', '', 'R2.3'), ('BB', 'OOP', '0R2.3-1F', 'C')]),
]
out = []
for kind, linetxt, title, players in SPEC:
    for S in (10, 12, 15):
        base = hs.EQ3 if kind == '3w' else hs.EQHU
        v = base[S]; loc = v[0] if isinstance(v, list) else v
        kd, h = hs._loc(kind, loc)
        st, L, leaves, am = fl.lines(kd, h)
        m = [r for r in L if r['line'] == linetxt]
        if not m: continue
        r = m[0]; ps = []
        ok = True
        for pos, role, key, lab in players:
            try: nd, _ = node_of(kind, S, key); ps.append(dict(position=pos, role=role, class_freq=freq(nd, lab), source_node=key, source_action=lab))
            except Exception as e: ok = False
        if not ok: continue
        out.append(dict(line_id=f"{kind}_{S}bb_{len(out)}", table='heads-up' if kind == 'hu' else '3-handed', stack_bb=S, description_fr=title, line_probability=round(r['prob'], 5),
                        pot_bb=r['pot'], remaining_stack_bb=r['rem'], spr=round(r['spr'], 2), players=ps))
json.dump(dict(meta=dict(note="Fréquences préflop par classe de main (169, grille 13x13 : indice = ligne*13 + colonne), poids d'atteinte inclus. Source : exports HRC (chip EV, sans ante).",
                         class_order='AA, AKs, AQs, ... (voir postflop_core.CLASS_NAMES)'), lines=out), open('/home/claude/postflop_pkg/ranges_export.json', 'w'), ensure_ascii=False)
print(len(out), "lignes exportées :", [x['line_id'] for x in out])

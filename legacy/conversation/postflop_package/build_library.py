"""Bibliothèque pédagogique : profils de flops représentatifs pour deux lignes de flop principales (à partir de ranges_export.json)."""
import json, sys, time, collections
import postflop_core as pc

def pick_flops(extra=15):
    cf = pc.canonical_flops(); groups = collections.defaultdict(list)
    for fl, n in cf:
        t = pc.flop_texture(fl); groups[(t['high_group'], t['structure'], t['pattern'])].append((n, fl))
    chosen = []
    for g, lst in sorted(groups.items()):
        lst.sort(key=lambda x: (-x[0], x[1])); chosen.append(lst[0][1])
    rest = sorted([(n, fl) for lst in groups.values() for n, fl in lst[1:3]], key=lambda x: (-x[0], x[1]))
    chosen += [fl for n, fl in rest[:extra]]
    return chosen

def main(out='library_profiles.json'):
    data = json.load(open('ranges_export.json')); flops = pick_flops()
    lines = [[x for x in data['lines'] if x['table'] == 'heads-up' and x['stack_bb'] == 12 and 'limp' in x['description_fr']][0],
             [x for x in data['lines'] if x['table'] == '3-handed' and x['stack_bb'] == 12 and 'limp' in x['description_fr']][0]]
    res = []
    t0 = time.time()
    for L in lines:
        wa = pc.range_from_class_freq(L['players'][0]['class_freq']); wb = pc.range_from_class_freq(L['players'][1]['class_freq'])
        for i, fl in enumerate(flops):
            p = pc.pedagogical_profile(fl, wa, wb); p['line_id'] = L['line_id']; p['line'] = L['description_fr']; p['role_A'] = L['players'][0]['role']
            res.append(p)
            if i % 5 == 0:
                json.dump(res, open(out, 'w')); print(f"{L['line_id']} {i+1}/{len(flops)} ({time.time()-t0:.0f} s)", flush=True)
    json.dump(res, open(out, 'w')); print("FIN", len(res), "profils", f"{time.time()-t0:.0f} s", flush=True)

if __name__ == '__main__': main()

"""Bilan des quizz : situations couvertes, nombre de questions, fréquence réelle de chaque situation et part servie.

Fréquence réelle d'une situation (point de décision du héros) : probabilité, sur une main jouée, que l'historique se
produise, calculée avec les stratégies HRC du dataset GTO (produit des fréquences agrégées de chaque action de
l'historique, pondérées par les combos et l'atteinte). Part servie : part des questions tirées sur 3000 séries simulées.

Usage : python tools/audit/bilan_quiz.py docs/relecture/bilan_2026-10-21
Sorties : bilan_gto_situations.csv, bilan_exploit_situations.csv, exports pour les coachs (gto_spots.csv,
exploit_questions.csv, gto_corrections_echantillon.csv) et bilan_chiffres.json.
"""
import collections, csv, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from spinsacademy import quiz, grading, field
from spinsacademy.cards import NAMES, W

BANDS = ((0, 6, '≤ 6 BB'), (6.01, 10, '7-10 BB'), (10.01, 15, '11-15 BB'), (15.01, 30, '16-25 BB'))
band = lambda s: next(l for a, b, l in BANDS if a <= s <= b)


def hist_key(sp):
    return tuple((h['position'], h['action'], h.get('to_bb') if h['action'] in ('raise',) else None) for h in sp['history'])


def hist_txt(sp):
    return ' > '.join(f"{p} {a}" + (f" {t:g}" if t else '') for p, a, t in hist_key(sp)) or '(premier à parler)'


def situation(sp):
    """libellé joueur : position, ce qui s'est passé avant (tailles regroupées)"""
    h = [(p, {'call': 'limp' if a == 'call' else a}.get(a, a)) for p, a, _ in hist_key(sp)]
    return f"{sp['hero']} · " + (' > '.join(f'{p} {a}' for p, a in h) if h else 'premier à parler')


def agg_freq(sp, aid):
    j = [a['id'] for a in sp['actions']].index(aid); num = den = 0.0
    for h, x in sp['hands'].items():
        w = W[NAMES.index(h)] * x.get('reach', 0)
        if x.get('freq'): num += w * x['freq'][j]; den += w
    return num / den if den else 0.0


def action_id(sp, step):
    p, a, t = step
    for x in sp['actions']:
        if x['type'] == a and (t is None or abs((x.get('to_bb') or 0) - t) < 1e-6): return x['id']
        if a == 'limp' and x['type'] in ('limp', 'call') and x.get('to_bb') == 1.0: return x['id']
    return None


def real_freq(spots):
    """probabilité de chaque historique (par main jouée), à partir des nœuds du dataset"""
    idx = {(sp['table'], tuple(sp['stacks_bb']), hist_key(sp), sp['hero']): sp for sp in spots.values()}
    out = {}
    for sid, sp in spots.items():
        p = 1.0; hk = hist_key(sp)
        for i, step in enumerate(hk):
            node = idx.get((sp['table'], tuple(sp['stacks_bb']), hk[:i], step[0]))
            aid = node and action_id(node, step)
            if not aid: p = None; break
            p *= agg_freq(node, aid)
        out[sid] = p
    return out


def served(version, n=3000, size=5):
    c = collections.Counter()
    for seed in range(n):
        try:
            for sid, _ in quiz.draw_series(version, None, size, seed): c[sid] += 1
        except ValueError:
            pass
    return c


def main(out):
    os.makedirs(out, exist_ok=True)
    _, gs = quiz.load(quiz.DEFAULT_VERSION); _, fs = quiz.load(quiz.DEFAULT_FIELD)
    rf = real_freq(gs); sv = served(quiz.DEFAULT_VERSION); svf = served(quiz.DEFAULT_FIELD, 2000)
    tot_sv = sum(sv.values()) or 1
    # --- GTO : par situation et tranche de tapis
    rows = collections.defaultdict(lambda: dict(spots=0, questions=0, real=0.0, real_n=0, served=0, stacks=set(), unequal=0))
    for sid, sp in gs.items():
        k = (sp['table'], situation(sp), quiz.family(sp), band(sp['effective_stack_bb']))
        r = rows[k]; r['spots'] += 1; r['questions'] += len(quiz.teachable(sp)); r['served'] += sv[sid]; r['stacks'].add(sp['effective_stack_bb'])
        r['unequal'] += len(set(sp['stacks_bb'])) > 1
        if rf[sid] is not None and len(set(sp['stacks_bb'])) == 1: r['real'] += rf[sid]; r['real_n'] += 1
    # fréquence réelle moyenne par tapis égal (moyenne sur les profondeurs de la tranche), normalisée par table
    realn = {k: (r['real'] / r['real_n'] if r['real_n'] else None) for k, r in rows.items()}
    norm = collections.defaultdict(float)
    for (t, s, f, b), v in realn.items():
        if v: norm[(t, b)] += v
    with open(os.path.join(out, 'bilan_gto_situations.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['table', 'situation', 'famille', 'tapis', 'spots', 'questions', 'part_servie_pct', 'freq_reelle_par_main_pct', 'part_reelle_dans_tranche_pct', 'spots_tapis_inegaux'])
        for k in sorted(rows, key=lambda k: (k[0], k[3], -(realn[k] or 0))):
            r = rows[k]; v = realn[k]
            w.writerow([k[0], k[1], k[2], k[3], r['spots'], r['questions'], f"{100 * r['served'] / tot_sv:.2f}".replace('.', ','),
                        '' if v is None else f"{100 * v:.2f}".replace('.', ','),
                        '' if not v else f"{100 * v / norm[(k[0], k[3])]:.1f}".replace('.', ','), r['unequal']])
    # --- exploitant
    erows = collections.defaultdict(lambda: collections.Counter())
    tot_f = sum(svf.values()) or 1
    for sid, sp in fs.items():
        f = sp['field']; k = (sp['table'], f.get('situation_fr') or situation(sp), sp['effective_stack_bb'])
        erows[k][f['type']] += 1; erows[k]['_total'] += 1; erows[k]['_served'] += svf[sid]
    with open(os.path.join(out, 'bilan_exploit_situations.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';'); types = list(field.TYPE_FR)
        w.writerow(['table', 'situation', 'tapis', 'questions'] + types + ['part_servie_pct'])
        for k in sorted(erows):
            c = erows[k]; w.writerow([k[0], k[1], k[2], c['_total']] + [c[t] for t in types] + [f"{100 * c['_served'] / tot_f:.2f}".replace('.', ',')])
    # --- exports pour les coachs
    with open(os.path.join(out, 'gto_spots.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['spot_id', 'table', 'heros', 'tapis', 'tapis_effectif', 'historique', 'pot_bb', 'a_payer_bb', 'actions', 'questions',
                    'strategie_reference (mains jouant l action >= 50 %)', 'freq_reelle_pct'])
        for sid, sp in sorted(gs.items()):
            labels = {a['id']: quiz.action_label(sp, a) for a in sp['actions']}; strat = []
            for j, a in enumerate(sp['actions']):
                inside = {h: grading.reference_freq(sp, h)[j] >= 0.5 for h, x in sp['hands'].items() if x.get('reach', 0) >= 0.05 and x.get('freq')}
                hs = [h for h, v in inside.items() if v]
                if hs: strat.append(f"{labels[a['id']]} : {quiz.range_text(hs)}")
            w.writerow([sid, sp['table'], sp['hero'], '/'.join(f'{x:g}' for x in sp['stacks_bb']), sp['effective_stack_bb'], hist_txt(sp), sp['pot_bb'],
                        sp['to_call_bb'], ' | '.join(labels.values()), len(quiz.teachable(sp)), ' || '.join(strat),
                        '' if rf[sid] is None else f"{100 * rf[sid]:.3f}".replace('.', ',')])
    with open(os.path.join(out, 'exploit_questions.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['spot_id', 'type', 'table', 'tapis', 'main', 'enonce', 'options', 'bonne_reponse', 'acceptees', 'action_theorique', 'regle',
                    'ev_options_bb', 'gain_vs_theorie_bb', 'correction', 'pourquoi', 'postflop'])
        for sid, sp in sorted(fs.items()):
            f = sp['field']; h = next(iter(sp['hands'])); q = quiz.question(quiz.DEFAULT_FIELD, sid, h)
            r = quiz.correct(quiz.DEFAULT_FIELD, sid, h, f['correct']); lab = {o['id']: o['label_fr'] for o in q['options']}
            n = r['next']
            w.writerow([sid, f['type'], sp['table'], sp['effective_stack_bb'], h, q['prompt_fr'].replace('\n', ' '), ' | '.join(lab.values()),
                        lab[f['correct']], ' | '.join(lab[a] for a in f['acceptable']), lab.get(f['gto'], ''), f['rule'],
                        ' | '.join(f"{lab[o['id']]} {o['ev_mbb'] / 1000:+.2f}" for o in f['options'] if o['ev_mbb'] is not None),
                        f"{(f.get('gain_mbb') or 0) / 1000:.2f}", r['core_fr'].replace('\n', ' / '), ' / '.join(r['why_fr']),
                        '' if not n else ' / '.join([n['intro'], n['position']] + n.get('plan', []) + ['+ ' + x for x in n['forces']] + ['- ' + x for x in n['weaknesses']])])
    rnd = random.Random(7); sample = []
    by = collections.defaultdict(list)
    for sid, sp in gs.items(): by[(sp['table'], situation(sp), band(sp['effective_stack_bb']))].append(sp)
    for k in sorted(by):
        for sp in rnd.sample(by[k], min(2, len(by[k]))):
            hs = sorted(quiz.teachable(sp))
            if hs: sample.append((sp, rnd.choice(hs)))
    with open(os.path.join(out, 'gto_corrections_echantillon.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.writer(fh, delimiter=';')
        w.writerow(['spot_id', 'table', 'tapis', 'main', 'enonce', 'action_jouee', 'verdict', 'correction', 'pourquoi', 'postflop'])
        for sp, h in sample:
            wrong = next((a['id'] for a in sp['actions'] if grading.grade(sp, h, a['id'])['verdict'] == 'erreur'), sp['actions'][0]['id'])
            r = quiz.correct(quiz.DEFAULT_VERSION, sp['spot_id'], h, wrong); n = r['next']
            w.writerow([sp['spot_id'], sp['table'], sp['effective_stack_bb'], h, quiz.prompt(sp, h).replace('\n', ' '), r['chosen_label'], r['verdict'],
                        r['explanation_fr'].replace('\n', ' / '), '', '' if not n else ' / '.join(x for x in [n['intro'], n.get('position') or ''] + n['forces'] + n['weaknesses'] if x)])
    fam = collections.Counter(); fam_real = collections.defaultdict(float); fam_sv = collections.Counter()
    for k, r in rows.items():
        fam[(k[0], k[2])] += r['questions']; fam_sv[(k[0], k[2])] += r['served']
        if realn[k]: fam_real[(k[0], k[2])] += realn[k]
    json.dump(dict(gto=dict(version=quiz.DEFAULT_VERSION, spots=len(gs), questions=sum(len(quiz.teachable(s)) for s in gs.values())),
                   exploit=dict(version=quiz.DEFAULT_FIELD, questions=len(fs)),
                   familles={f"{t} {f}": dict(questions=fam[(t, f)], servie_pct=round(100 * fam_sv[(t, f)] / tot_sv, 1)) for t, f in fam},
                   gto_echantillon_corrections=len(sample)),
              open(os.path.join(out, 'bilan_chiffres.json'), 'w'), ensure_ascii=False, indent=1)
    print(out, len(gs), 'spots GTO,', len(fs), 'questions exploitantes,', len(sample), 'corrections GTO en échantillon')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'docs/relecture/bilan_2026-10-21')

"""Audit v4 : grille Lucho / PA / Lucky codée sur leurs skills (usage : python3 audit_quiz.py quiz.json audit.csv).
Le verdict de chaque coach est celui que sa doctrine donnerait ; ✅ = d'accord, ⚠️ = juste en théorie mais le coach dévie / nuance, ❌ = désaccord."""
import json, csv, collections, sys
qs = json.load(open(sys.argv[1]))

def hero(q):
    s = q['situation']
    return 'BB' if s.startswith('BB') else 'SB' if s.startswith('SB') else 'BTN' if s.startswith('BTN') else ''

rows = []
for q in qs:
    S, kind, t, ans, gto, pr, h = q['stack'], q['kind'], q['type'], q['bonne_reponse'], q.get('action_GTO', ''), q['profil'], hero(q)
    sp = 'call' if 'face à' in q['situation'] else 'shove'
    L = P = K = ('✅', ''); corr = ''
    if 'limp du SB' in q['situation'] and t not in ('identification', 'profil'):    # v4.2 : situation nouvelle, hors de la grille des coachs
        L = P = K = ('·', 'situation nouvelle (BB face au limp) : non couverte par la grille')
    elif t == 'profil':
        L = ('✅', 'pastille selon le comportement (§4) ; rec passif et reg séparés (v4.2)')
        P = ('✅', '« 3 occurrences ne font pas une tendance » : l\'énoncé donne n [fNlp-ULrS30]')
        K = ('✅', 'pastille + nombre d\'observations, ~5 % d\'erreur acceptés [qhmDZMrzgH8]')
    elif t == 'identification':
        L = ('✅', 'logique juste ; Lucho préfère pastilles/notes aux stats aux micros')
        P = ('✅', 'échantillon précisé [fNlp-ULrS30]'); K = ('✅', 'nombre d\'observations indiqué [qhmDZMrzgH8]')
    elif t == 'échantillon':
        L = ('✅', 'pas de décision sur 3 mains'); P = ('✅', '« 3 occurrences ne font pas une tendance »'); K = ('✅', 'rester sur le profil par défaut')
    elif q['regle'] == 'R11':
        L = ('✅', 'plus l\'adversaire est fort, plus on se rapproche de la théorie (§2)')
        P = ('✅', 'agresseur initial : coller aux ranges théoriques sauf read [Wkd0Uq0i2FE]')
        K = ('✅', 'vs reg : revenir vers la théorie dans les spots fréquents [xHK36BcO1cc]')
    elif ans == 'Limp':
        if kind == 'hu':
            L = ('✅', 'vs rec qui iso peu : limper (HU) §3.4'); P = ('✅', 'HU 9 BB : limp ~100 % vs field [2nfSDHmiWfc]'); K = ('✅', 'recs iso 11-16 % : limper large ok [nPgYD_IWRR0]')
        else:
            L = ('✅', 'SB BvB vs passif : oui, pas les poubelles'); P = ('⚠️', 'BvB : range limp-call / limp-fold structurée [fNlp-ULrS30]')
            K = ('⚠️', 'BvB 3-way : « on limpe trop », open 2 bb prioritaire ; limp seulement les mains correctes vs station [nPgYD_IWRR0]')
            corr = 'Limp défendable (2 coachs sur 3) ; l\'open 2 bb est l\'alternative de Lucky.'
    elif q['regle'] == 'R0':
        L = ('✅', 'rec présumé par défaut (§1)'); P = ('✅' if S >= 8 or S == 4 else '⚠️', 'field trop tight à 8-10 BB, paie tout vers 3-4 BB ; proche de la théorie vers 5-6 BB [27YoUVv32Ag]')
        K = ('✅', '99 % des joueurs sont trop passifs ; côté call du Nash horrible vs recs [u_1FYt4QbmM]')
    elif sp == 'call' and ans == 'Fold' and gto == 'Payer':     # R2
        L = ('✅', 'exception d\'overfold vs field qui ne push pas assez (§3.1)')
        P = ('✅' if S >= 8 else '⚠️', 'field BTN trop serré à 8-10 BB → call plus serré [Wkd0Uq0i2FE]' if S >= 8 else 'le field rejoint la théorie vers 5-6 BB [27YoUVv32Ag]')
        K = ('✅' if S >= 8 else '⚠️', 'côté call du Nash horrible vs recs (K9o ≈ 6 bb) [u_1FYt4QbmM]' if S >= 8 else '4-6 bb : calls larges, ~40 % d\'équité [R4l6ToWXD8w]')
        if S == 6: corr = 'Read d\'au moins 40 occasions exigé à 6 BB.'
    elif sp == 'call' and ans == 'Payer' and gto == 'Fold':      # R1
        L = ('✅', 'overfolder vs fish qui push large = catastrophe'); P = ('✅', 'vs shoveur fréquent : caller TP, T9o, K9 [27YoUVv32Ag]'); K = ('✅', 'vs jam trop large : call plus large [xHK36BcO1cc]')
    elif sp == 'shove' and ans.startswith('Pousser') and gto != 'Pousser all-in':   # R3
        L = ('✅', 'serpillère : on push beaucoup car il overfold'); P = ('✅', 'folder n\'est pas ne pas faire d\'erreur [oCayNJbtxqw]'); K = ('✅', '« je pars toujours à tapis devant » = tu folds trop ; 94s jam 7 bb [R4l6ToWXD8w]')
        if kind == 'hu' and S >= 8:
            P = ('⚠️', 'push ok mais à 8-10 BB HU PA limpe l\'essentiel vs passif [XIxCrh3PBKc]'); corr = 'Le limp est une alternative acceptable.'
    elif sp == 'shove' and ans == 'Fold':
        if pr == 'Dégène':
            L = ('✅', 'vs dégène : on ne limp-fold pas, bas de range fold'); P = ('✅', 'bas de range → fold vs iso-shove fréquent [27YoUVv32Ag]'); K = ('✅', 'vs joueur qui iso > 50 % : arrêter les poubelles [pJDcCB-G0r0]')
        elif h == 'BTN':
            L = ('⚠️', 'vs passif, Lucho maximise le VPIP (limp possible) ; vs station zéro bluff'); P = ('✅' if S <= 8 else '⚠️', 'BTN 3-way : fold ou shove ' + ('[Wkd0Uq0i2FE]' if S <= 8 else '; 10 BB min-raise/fold du pack KT [Fky7qYndP14]'))
            K = ('✅', 'BTN 3-way : interdit de limper [kc99KQepkKs]')
        else:
            L = ('⚠️', 'fold d\'un push GTO sans limp'); P = ('⚠️', 'ne pas folder un shove théorique [oCayNJbtxqw]'); K = ('⚠️', '4-6 bb : être très agressif'); corr = 'À revoir.'
    else:     # pièges R9 : la décision ne change pas
        L = ('✅', 'même action que la théorie'); P = ('✅', 'ne pas sur-exploiter [fNlp-ULrS30]'); K = ('✅', 'écart de fréquence trop faible pour dévier')
        if sp == 'shove' and kind == 'hu' and S >= 10 and ans.startswith('Pousser') and pr == 'Calling station':
            P = ('⚠️', '9-10 BB vs passif : limper les As-x plutôt que shove [XIxCrh3PBKc]'); K = ('⚠️', 'vs station : limper beaucoup [pJDcCB-G0r0]'); corr = 'Push n\'est pas une erreur, le limp est au moins aussi bon.'
    cons = [L[0], P[0], K[0]]; c = collections.Counter(cons)
    consensus = '·' if c['·'] == 3 else '❌' if c['❌'] >= 2 else ('⚠️' if c['❌'] + c['⚠️'] >= 2 else '✅')
    rows.append(dict(id=q['id'], type=t, kind=kind, stack=S, situation=q['situation'], main=q.get('hero_hand', ''), profil=pr, observations=q['observations'],
                     action_GTO=gto, reponse_quiz=ans, gain_mBB=q.get('gain_mBB', ''), regle=q['regle'],
                     lucho=L[0], lucho_motif=L[1], pa=P[0], pa_motif=P[1], lucky=K[0], lucky_motif=K[1], consensus=consensus, correction=corr))
with open(sys.argv[2], 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter=';'); w.writeheader(); w.writerows(rows)
print('total', len(rows), dict(collections.Counter(r['consensus'] for r in rows)))
for k, v in sorted(collections.Counter((r['type'], r['consensus']) for r in rows).items()): print(k, v)

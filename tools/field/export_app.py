"""Export v2.0 des questions exploitantes pour l'application : JSON (+ schéma), CSV à plat, SQLite.
Usage : python3 export_app.py quiz_exploit_v3.json dossier_sortie"""
import json, csv, sqlite3, sys, os, hashlib, datetime, collections
qs = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)

SPOTS = {
 ('3w', "BB face à l'all-in du SB (BTN fold)"): ('3W_BB_VS_SB_SHOVE', '3-handed', 'BB', ['SB'], ['BTN fold', 'SB all-in'], 'CALL_OR_FOLD', 'SHOVE_PCT'),
 ('3w', "BB face à l'all-in du BTN (SB fold)"): ('3W_BB_VS_BTN_SHOVE', '3-handed', 'BB', ['BTN'], ['BTN all-in', 'SB fold'], 'CALL_OR_FOLD', 'SHOVE_PCT'),
 ('3w', "SB face à l'all-in du BTN"): ('3W_SB_VS_BTN_SHOVE', '3-handed', 'SB', ['BTN'], ['BTN all-in'], 'CALL_OR_FOLD', 'SHOVE_PCT'),
 ('3w', 'SB pousse (BTN fold) face au BB'): ('3W_SB_OPEN_BVB', '3-handed', 'SB', ['BB'], ['BTN fold'], 'SHOVE_LIMP_OR_FOLD', 'CALL_PCT'),
 ('3w', 'BTN pousse face au SB et au BB'): ('3W_BTN_OPEN', '3-handed', 'BTN', ['SB', 'BB'], [], 'SHOVE_OR_FOLD', 'CALL_PCT'),
 ('hu', "BB face à l'all-in du SB"): ('HU_BB_VS_SB_SHOVE', 'heads-up', 'BB', ['SB'], ['SB all-in'], 'CALL_OR_FOLD', 'SHOVE_PCT'),
 ('hu', 'SB pousse face au BB'): ('HU_SB_OPEN', 'heads-up', 'SB', ['BB'], [], 'SHOVE_LIMP_OR_FOLD', 'CALL_PCT'),
}
DESC = {'3W_BB_VS_SB_SHOVE': "3 joueurs, {S} BB chacun. Le BTN fold et le SB pousse all-in. Tu es au BB.",
        '3W_BB_VS_BTN_SHOVE': "3 joueurs, {S} BB chacun. Le BTN pousse all-in et le SB fold. Tu es au BB.",
        '3W_SB_VS_BTN_SHOVE': "3 joueurs, {S} BB chacun. Le BTN pousse all-in. Tu es au SB (le BB est derrière).",
        '3W_SB_OPEN_BVB': "3 joueurs, {S} BB chacun. Le BTN fold. Tu es au SB, le BB est derrière.",
        '3W_BTN_OPEN': "3 joueurs, {S} BB chacun. Tu es au BTN, le SB et le BB sont derrière.",
        'HU_BB_VS_SB_SHOVE': "Heads-up, {S} BB chacun. Le SB pousse all-in. Tu es au BB.",
        'HU_SB_OPEN': "Heads-up, {S} BB chacun. Tu es au SB (bouton), le BB est derrière."}
TYPE = {'adaptation': 'ADAPTATION', 'piège': 'TRAP', 'identification': 'IDENTIFICATION', 'inconnu': 'UNKNOWN_VILLAIN', 'échantillon': 'THIN_SAMPLE', 'profil': 'PROFILE_READ'}
DIFF = {'facile': 'EASY', 'moyen': 'MEDIUM', 'piège': 'HARD'}
ACT = {'Payer': 'CALL', 'Fold': 'FOLD', 'Pousser all-in': 'SHOVE', 'Limp': 'LIMP', '': ''}
LEAK = {'pousse trop souvent': 'SHOVES_TOO_OFTEN', 'ne pousse pas assez': 'SHOVES_TOO_RARELY', 'paie trop souvent': 'CALLS_TOO_OFTEN', 'ne paie pas assez': 'CALLS_TOO_RARELY', '': ''}
PROFILE_CODE = {'Rec passif (défaut)': 'DEFAULT_REC', 'Calling station': 'STATION', 'Dégène': 'DEGENE', 'Nit': 'NIT', 'Reg': 'REG'}

def hand(code):
    if not code: return None
    return dict(code=code, rank_high=code[0], rank_low=code[1], pair=len(code) == 2, suited=code.endswith('s'))

questions = []
for q in qs:
    key = (q['kind'], q['situation'])
    sid = SPOTS[key][0] if key in SPOTS else 'HU_PROFILE_READ'
    opts = [dict(id='ABCD'[i], label_fr=o) for i, o in enumerate(q['options'])]
    cid = next(o['id'] for o in opts if o['label_fr'] == q['bonne_reponse'])
    z = dict(id=q['id'], type=TYPE[q['type']], difficulty=DIFF.get(q.get('difficulte', 'moyen'), 'MEDIUM'), stack_bb=q['stack'],
             table='heads-up' if q['kind'] == 'hu' else '3-handed', spot_id=sid,
             hero=dict(position=SPOTS[key][2] if key in SPOTS else None, hand=hand(q.get('hero_hand', ''))),
             action_history=SPOTS[key][4] if key in SPOTS else [],
             villain_stats=[dict(villain=(SPOTS[key][3][0] if key in SPOTS else 'SB'), stat=s['stat'], observations=s['n'], hits=s['k'], observed_pct=s['observed_pct'], gto_pct=s['gto_pct']) for s in q.get('stats', [])],
             observations=q['observations'], villain_known=q['observations'] > 0,
             prompt_fr=q['enonce'], options=opts, correct_option_id=cid, explanation_fr=q['explication'],
             rule_code=q['regle'], gto_action=ACT.get(q.get('action_GTO', ''), ''), exploit_action=ACT.get(q['bonne_reponse'], ''),
             gain_mbb=q.get('gain_mBB', 0), noise_threshold_mbb=q.get('seuil_bruit_mBB', 0), margin_mbb=q.get('marge_mBB'),
             play_ev_vs_fold_mbb=q.get('ev_jeu_vs_fold_mBB'), limp_ev_vs_fold_mbb=q.get('ev_limp_vs_fold_mBB'),
             leak_code=LEAK.get(q.get('leak', ''), ''), internal_profile=PROFILE_CODE[q['profil']], intensity=q.get('intensite', 1.0),
             data_level=q['niveau_donnees'])
    z['content_hash'] = hashlib.sha1(json.dumps([z['type'], z['spot_id'], z['stack_bb'], z['hero']['hand'], z['prompt_fr'], sorted(o['label_fr'] for o in opts)], ensure_ascii=False).encode()).hexdigest()[:12]
    questions.append(z)
assert len({z['id'] for z in questions}) == len(questions) and len({z['content_hash'] for z in questions}) == len(questions)
spots = [dict(spot_id=v[0], table=v[1], hero_position=v[2], villain_positions=v[3], action_history=v[4], decision_type=v[5], villain_stat=v[6], description_fr=DESC[v[0]], name_fr=k[1]) for k, v in SPOTS.items()]
meta = dict(export_version='2.0', generated_at=datetime.date.today().isoformat(), locale='fr-FR',
            source=dict(gto_base='HRC (chip EV, blinds 0,5 / 1, sans ante), niveau A : stacks résolus par HRC', exploit_engine='moteur exploitant v4 (rec passif par défaut selon la profondeur, limp au SB, EV différentielle, seuils de bruit par stack)',
                        generator='quiz_generator.py', verification='verify_quiz.py : 0 échec ; audit_quiz.py : grille Lucho / PA / Lucky'),
            units=dict(ev='mBB = millième de big blind', stack='BB'), thresholds_mbb={'4': 37, '6': 60, '8': 77, '10': 242, '12': 332},
            rules={'R0': 'vilain inconnu = rec passif', 'R1': 'vs vilain qui pousse trop : payer plus large', 'R2': 'vs vilain qui pousse peu : payer plus serré', 'R3': 'vs vilain qui paie peu : pousser plus large',
                   'R4': 'SB vs passif : la main qui ne se pousse plus se limpe', 'R5': 'ne pas folder un push théorique sans read solide (3 x bruit, 20 occasions ; jamais à 4 BB ou moins)',
                   'R7': 'BTN 3-way : fold ou push', 'R9': 'écart de fréquence qui ne retourne pas la décision : ne rien changer', 'R10': 'quelques occasions ne font pas une tendance', 'R11': 'vs reg identifié : théorie'},
            counts=dict(questions=len(questions), by_type=dict(collections.Counter(z['type'] for z in questions)), by_rule=dict(collections.Counter(z['rule_code'] for z in questions))),
            caveats=["Les facteurs des profils sont des hypothèses tirées de déclarations de coachs, non mesurées : afficher les statistiques (k sur n), jamais un nom de profil.",
                     "Domaine : décisions tout ou rien et limp au SB, stacks égaux de 4 à 12 BB ; min-raise et iso non all-in exclus.",
                     "Le limp est évalué par une borne basse (EV HRC) ; les paires premium limpées entre 6 et 10 BB sont exclues (désaccord des coachs, R8).",
                     "internal_profile ne doit jamais être affiché au joueur."])
json.dump(dict(meta=meta, spots=spots, questions=questions), open(os.path.join(out, 'spinsacademy_quiz_export_v2.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(out, 'spinsacademy_quiz_export_v2.csv'), 'w', newline='', encoding='utf-8-sig') as f:
    cols = ['id', 'type', 'difficulty', 'stack_bb', 'table', 'spot_id', 'hero_position', 'hero_hand', 'observations', 'prompt_fr', 'option_A', 'option_B', 'option_C', 'option_D', 'correct_option_id', 'correct_label',
            'explanation_fr', 'rule_code', 'gto_action', 'exploit_action', 'gain_mbb', 'noise_threshold_mbb', 'margin_mbb', 'play_ev_vs_fold_mbb', 'limp_ev_vs_fold_mbb', 'leak_code', 'internal_profile', 'villain_stat_1', 'villain_stat_2', 'data_level', 'content_hash']
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for z in questions:
        r = {k: z.get(k) for k in cols}; r['hero_position'] = z['hero']['position']; r['hero_hand'] = (z['hero']['hand'] or {}).get('code', '')
        for i, o in enumerate(z['options']): r['option_' + o['id']] = o['label_fr']
        r['correct_label'] = next(o['label_fr'] for o in z['options'] if o['id'] == z['correct_option_id'])
        for j, s in enumerate(z['villain_stats'][:2]): r[f'villain_stat_{j+1}'] = f"{s['stat']} {s['hits']}/{s['observations']} = {s['observed_pct']} % (GTO {s['gto_pct']} %)"
        w.writerow(r)
db = os.path.join(out, 'spinsacademy_quiz_v2.sqlite')
if os.path.exists(db): os.remove(db)
c = sqlite3.connect(db)
c.executescript("""CREATE TABLE spots(spot_id TEXT PRIMARY KEY, table_type TEXT, name_fr TEXT, hero_position TEXT, villain_positions TEXT, action_history TEXT, decision_type TEXT, villain_stat TEXT, description_fr TEXT);
CREATE TABLE questions(id TEXT PRIMARY KEY, type TEXT NOT NULL, difficulty TEXT NOT NULL, stack_bb INTEGER NOT NULL, table_type TEXT NOT NULL, spot_id TEXT NOT NULL, hero_position TEXT, hero_hand TEXT, observations INTEGER NOT NULL, prompt_fr TEXT NOT NULL,
 correct_option_id TEXT NOT NULL, explanation_fr TEXT, rule_code TEXT NOT NULL, gto_action TEXT, exploit_action TEXT, gain_mbb REAL, noise_threshold_mbb REAL, margin_mbb REAL, play_ev_vs_fold_mbb REAL, limp_ev_vs_fold_mbb REAL, leak_code TEXT, internal_profile TEXT, intensity REAL, data_level TEXT, content_hash TEXT UNIQUE);
CREATE TABLE options(question_id TEXT REFERENCES questions(id), option_id TEXT, label_fr TEXT NOT NULL, PRIMARY KEY(question_id, option_id));
CREATE TABLE villain_stats(question_id TEXT REFERENCES questions(id), villain TEXT, stat TEXT, observations INTEGER, hits INTEGER, observed_pct REAL, gto_pct REAL);
CREATE INDEX idx_q_stack ON questions(stack_bb, type); CREATE INDEX idx_q_rule ON questions(rule_code);""")
for s in spots: c.execute('INSERT INTO spots VALUES(?,?,?,?,?,?,?,?,?)', (s['spot_id'], s['table'], s['name_fr'], s['hero_position'], json.dumps(s['villain_positions']), json.dumps(s['action_history'], ensure_ascii=False), s['decision_type'], s['villain_stat'], s['description_fr']))
c.execute("INSERT OR IGNORE INTO spots VALUES('HU_PROFILE_READ','heads-up','Lecture du vilain',NULL,'[\"SB\"]','[]','PROFILE_READ','SHOVE_PCT','Heads-up : lecture du vilain')")
for z in questions:
    c.execute('INSERT INTO questions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (z['id'], z['type'], z['difficulty'], z['stack_bb'], z['table'], z['spot_id'], z['hero']['position'], (z['hero']['hand'] or {}).get('code'), z['observations'], z['prompt_fr'], z['correct_option_id'], z['explanation_fr'],
              z['rule_code'], z['gto_action'], z['exploit_action'], z['gain_mbb'], z['noise_threshold_mbb'], z['margin_mbb'], z['play_ev_vs_fold_mbb'], z['limp_ev_vs_fold_mbb'], z['leak_code'], z['internal_profile'], z['intensity'], z['data_level'], z['content_hash']))
    for o in z['options']: c.execute('INSERT INTO options VALUES(?,?,?)', (z['id'], o['id'], o['label_fr']))
    for s in z['villain_stats']: c.execute('INSERT INTO villain_stats VALUES(?,?,?,?,?,?,?)', (z['id'], s['villain'], s['stat'], s['observations'], s['hits'], s['observed_pct'], s['gto_pct']))
c.commit(); c.close()
print(len(questions), 'questions exportées dans', out)

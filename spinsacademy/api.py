"""API du quiz (FastAPI + SQLite), routes du cahier des charges §13.1.

  POST /sessions                 créer une série (mode gto ou exploit, filtres, taille, graine) liée à une version de dataset
  GET  /quiz/next?session_id=    question suivante non répondue (sans solution) ; done=true à la fin
  POST /attempts                 répondre à une question : correction et explication ; une réponse est définitive
  GET  /sessions/{id}/summary    bilan : score, verdicts, thèmes, erreurs à revoir
  GET  /users/me/reviews         révision espacée des erreurs (J+1, J+3, J+7) ; POST /sessions avec review=true pour la lancer
  GET  /users/me/stats           progression du joueur (en-tête X-Player-Id) ; GET /users/me/export, DELETE /users/me
  POST /reports                  signaler une erreur sur une question répondue (une fois par question)
  GET  /admin/reports, POST /admin/reports/{id}/resolve, GET /admin/disabled, DELETE /admin/disabled/{spot_id},
  GET  /admin/log                administration (en-tête X-Admin-Token = SPINSACADEMY_ADMIN_TOKEN ; désactivée sans jeton)
  GET  /health
  GET  /                         interface web mobile (spinsacademy/web)
Mode invité au MVP : pas d'authentification (cahier des charges §19, question 22, à trancher). L'appareil génère un
identifiant anonyme envoyé dans l'en-tête X-Player-Id ; il relie les séries d'un même joueur pour les statistiques.
Base : SPINSACADEMY_DB (par défaut data/app/spinsacademy.sqlite) ; dataset : SPINSACADEMY_DATASET.
"""
import threading, datetime, hmac, json, os, re, sqlite3, uuid
from contextlib import closing
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from . import adaptive, catalog, challenges, goals, levels, progress, quiz, ranges, ratelimit, recommend, review, today
from .hrc import ROOT

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, dataset_version TEXT NOT NULL,
  filters TEXT NOT NULL, seed INTEGER, size INTEGER NOT NULL, player_id TEXT);
CREATE TABLE IF NOT EXISTS questions(session_id TEXT NOT NULL REFERENCES sessions(id), idx INTEGER NOT NULL,
  spot_id TEXT NOT NULL, hand TEXT NOT NULL, served_at TEXT, PRIMARY KEY(session_id, idx));
CREATE TABLE IF NOT EXISTS attempts(session_id TEXT NOT NULL, idx INTEGER NOT NULL, action_id TEXT NOT NULL,
  verdict TEXT NOT NULL, points REAL NOT NULL, regret_mbb REAL NOT NULL, result TEXT NOT NULL, answered_at TEXT NOT NULL,
  PRIMARY KEY(session_id, idx), FOREIGN KEY(session_id, idx) REFERENCES questions(session_id, idx));
CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, player_id TEXT,
  session_id TEXT NOT NULL, question_index INTEGER NOT NULL, dataset_version TEXT NOT NULL, spot_id TEXT NOT NULL,
  hand TEXT NOT NULL, action_id TEXT, reason TEXT NOT NULL, comment TEXT, status TEXT NOT NULL DEFAULT 'open',
  resolution TEXT, resolved_at TEXT, UNIQUE(session_id, question_index));
CREATE TABLE IF NOT EXISTS disabled_spots(spot_id TEXT PRIMARY KEY, dataset_version TEXT NOT NULL, reason TEXT NOT NULL,
  report_id INTEGER, disabled_at TEXT NOT NULL, actor TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS preferences(player_id TEXT PRIMARY KEY, adaptive INTEGER NOT NULL DEFAULT 1, adaptation_reset_at TEXT,
  updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS range_attempts(id INTEGER PRIMARY KEY AUTOINCREMENT, player_id TEXT, dataset_version TEXT NOT NULL,
  spot_id TEXT NOT NULL, hands TEXT NOT NULL, accuracy_pct REAL NOT NULL, bb_per_100 REAL NOT NULL, answered_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS goals(player_id TEXT NOT NULL, mode TEXT NOT NULL, week TEXT NOT NULL, kind TEXT NOT NULL,
  target REAL NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY(player_id, mode, week, kind));
CREATE TABLE IF NOT EXISTS player_level(player_id TEXT PRIMARY KEY, level INTEGER NOT NULL, experience TEXT, goal TEXT,
  onboarded_at TEXT, promoted_at TEXT, updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS admin_log(id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, actor TEXT NOT NULL,
  action TEXT NOT NULL, details TEXT NOT NULL);
"""
REASONS = {'wrong_answer': 'La réponse de référence me semble inadaptée', 'unclear': "L'énoncé est incompréhensible",
           'illegal_action': 'Une action proposée est impossible', 'other': 'Autre'}


def _now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def db_path(): return os.environ.get('SPINSACADEMY_DB', os.path.join(ROOT, 'data', 'app', 'spinsacademy.sqlite'))


def connect():
    path = db_path(); os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path, timeout=10); con.row_factory = sqlite3.Row; con.execute('PRAGMA foreign_keys = ON')
    con.execute('PRAGMA journal_mode = WAL')                       # lectures pendant les écritures (plusieurs processus uvicorn)
    con.executescript(SCHEMA)
    if 'player_id' not in {r[1] for r in con.execute('PRAGMA table_info(sessions)')}:      # migration d'une base antérieure
        con.execute('ALTER TABLE sessions ADD COLUMN player_id TEXT')
    if 'purpose' not in {r[1] for r in con.execute('PRAGMA table_info(questions)')}:      # migration : objectif de la question
        con.execute('ALTER TABLE questions ADD COLUMN purpose TEXT'); con.execute('ALTER TABLE questions ADD COLUMN purpose_fr TEXT')
    if 'timed_out' not in {r[1] for r in con.execute('PRAGMA table_info(attempts)')}:      # migration : coup joué au temps (chrono)
        con.execute('ALTER TABLE attempts ADD COLUMN timed_out INTEGER NOT NULL DEFAULT 0')
    if 'plan' not in {r[1] for r in con.execute('PRAGMA table_info(sessions)')}:           # migration : étape de la séance du jour
        con.execute('ALTER TABLE sessions ADD COLUMN plan TEXT')
    con.execute('CREATE INDEX IF NOT EXISTS sessions_player ON sessions(player_id)')
    catalog.sync(con); con.commit()
    return con


DATASET_OF = {'gto': 'gto_preflop', 'exploit': 'exploit_field'}
DEFAULT_OF = {'gto': quiz.DEFAULT_VERSION, 'exploit': quiz.DEFAULT_FIELD}


def serving_version(con, mode):
    """version publiée du mode ; SPINSACADEMY_ALLOW_STAGING=1 (développement, tests) : version par défaut si rien n'est publié"""
    ref = catalog.active(con, DATASET_OF[mode])
    if ref: return ref
    if os.environ.get('SPINSACADEMY_ALLOW_STAGING') == '1': return DEFAULT_OF[mode]
    raise HTTPException(503, 'aucun dataset publié pour ce mode : l\'administration doit en publier un')


PLAYER_RE = re.compile(r'^[A-Za-z0-9-]{8,64}$')


def player(x_player_id, required=False):
    if x_player_id is None:
        if required: raise HTTPException(400, 'en-tête X-Player-Id manquant')
        return None
    if not PLAYER_RE.match(x_player_id): raise HTTPException(400, 'X-Player-Id invalide')
    return x_player_id


class Filters(BaseModel):
    table: Optional[str] = Field(None, pattern='^(3-handed|heads-up)$')
    hero: Optional[str] = Field(None, pattern='^(BTN|SB|BB)$')
    family: Optional[str] = Field(None, pattern='^(first_in|vs_limp|vs_raise|vs_allin|read)$')     # read : lecture du vilain (mode Field)
    min_stack: Optional[float] = None
    max_stack: Optional[float] = None


class NewSession(BaseModel):
    mode: str = Field('gto', pattern='^(gto|exploit)$')
    filters: Filters = Filters()
    size: int = Field(quiz.SERIES_SIZE, ge=1, le=20)
    seed: Optional[int] = None
    adaptive: Optional[bool] = None       # None : préférence du joueur ; ignoré si des filtres sont choisis
    review: bool = False                  # révision espacée : les mains ratées arrivées à échéance d'abord, complétées par un tirage normal
    plan: Optional[str] = Field(None, pattern='^(review|theme)$')   # étape de la séance du jour (spinsacademy.today)
    challenge: Optional[str] = Field(None, pattern='^(daily|perfect|pressure|reader)$')   # défi (spinsacademy.challenges)


class Attempt(BaseModel):
    session_id: str
    question_index: int = Field(ge=0)
    action_id: str
    timed_out: bool = False          # chrono écoulé : le coup automatique compte comme une erreur, même s'il tombe sur le bon coup


app = FastAPI(title='SpinsAcademy', version='0.1.0')


@app.on_event('startup')
def _warm():
    """préchargement des datasets servis, en arrière-plan : les premières requêtes attendent ce chargement (verrou de
    quiz.load) au lieu d'en lancer chacune un"""
    def run():
        try:
            with closing(connect()) as con:
                versions = {serving_version(con, m) for m in DATASET_OF}
        except Exception:
            return                                            # rien de publié : chargé à la demande
        for v in versions:
            try:
                quiz.load(v)
                if quiz.mode_of(v) == 'gto': quiz.situation_weights(v); ranges.drawable(v)
            except Exception:
                pass
    threading.Thread(target=run, daemon=True).start()
WEB = os.path.join(os.path.dirname(__file__), 'web')
app.mount('/static', StaticFiles(directory=WEB), name='static')


@app.middleware('http')
async def rate_limit(request: Request, call_next):
    pid = request.headers.get('x-player-id')
    wait = ratelimit.check(request.method, request.url.path, ratelimit.client_ip(request.headers, request.client.host if request.client else None),
                           pid if pid and PLAYER_RE.match(pid) else None)
    if wait: return JSONResponse({'detail': ratelimit.MESSAGE_FR.format(s=wait)}, status_code=429, headers={'Retry-After': str(wait)})
    return await call_next(request)


@app.get('/', include_in_schema=False)
def index():
    return FileResponse(os.path.join(WEB, 'index.html'))


@app.get('/sw.js', include_in_schema=False)
def service_worker():
    """service worker servi à la racine (portée « / ») : l'application s'ouvre hors connexion"""
    return FileResponse(os.path.join(WEB, 'sw.js'), media_type='application/javascript', headers={'Cache-Control': 'no-cache'})


@app.get('/conseil', include_in_schema=False)
def conseil_page():
    """conseiller préflop : la stratégie de référence d'une main, à tapis et action donnés (données : tools/web/build_conseil.py)"""
    return FileResponse(os.path.join(WEB, 'conseil.html'))


@app.get('/admin', include_in_schema=False)
def admin_page():
    return FileResponse(os.path.join(WEB, 'admin.html'))


def _release():
    """version déployée (RELEASE.json écrit par tools/ops/release.sh), None hors paquet de version"""
    path = os.path.join(ROOT, 'RELEASE.json')
    try: return json.load(open(path))
    except (OSError, ValueError): return None


@app.get('/health')
def health():
    with closing(connect()) as con:
        return dict(status='ok', release=_release(), published={ds: catalog.active(con, ds) for ds in catalog.KINDS},
                    staging_fallback=os.environ.get('SPINSACADEMY_ALLOW_STAGING') == '1')


def _prefs(con, pid):
    r = con.execute('SELECT adaptive, adaptation_reset_at FROM preferences WHERE player_id = ?', (pid,)).fetchone() if pid else None
    return dict(adaptive=bool(r['adaptive']) if r else True, adaptation_reset_at=r['adaptation_reset_at'] if r else None)


def _mode_rows(con, pid, mode, since):
    rows = _player_rows(con, pid)
    return [r for r in rows if quiz.mode_of(r['dataset_version']) == mode and (since is None or (r['answered_at'] or '') > since)]


def _excluded(con):
    return frozenset(r[0] for r in con.execute('SELECT spot_id FROM disabled_spots'))


def _adaptation(con, pid, mode, version, size, seed):
    rows = _mode_rows(con, pid, mode, _prefs(con, pid)['adaptation_reset_at'])
    available = {adaptive.theme_of(sp) for sp in quiz.pool(version, None, _excluded(con))}
    return adaptive.plan(rows, available, size, seed)


RECENT_QUESTIONS = 30      # test joueurs 6 : une série évite les situations et les mains des dernières séries du joueur
REDRAWS = 6


def _recent(con, pid):
    """(spots, mains, première main de la dernière série) des dernières questions servies au joueur"""
    if pid is None: return set(), set(), None
    rows = con.execute('SELECT q.spot_id, q.hand, q.idx FROM questions q JOIN sessions s ON s.id = q.session_id WHERE s.player_id = ? '
                       'ORDER BY s.created_at DESC, q.idx LIMIT ?', (pid, RECENT_QUESTIONS)).fetchall()
    first = next((r['hand'] for r in rows if r['idx'] == 0), None)
    return {r['spot_id'] for r in rows}, {r['hand'] for r in rows}, first


def _least_repeated(draw, seed, recent):
    """tire jusqu'à REDRAWS séries et garde celle qui répète le moins les dernières (le premier tirage s'il ne répète rien)"""
    spots, hands, first = recent
    if not spots: return draw(seed)
    score = lambda ser: (2 * sum(x[0] in spots for x in ser) + sum(x[1] in hands for x in ser) + 3 * bool(ser and ser[0][1] == first))
    best = None
    for k in range(REDRAWS):
        ser = draw(seed if k == 0 or seed is None else seed * 1000 + k)
        if best is None or score(ser) < score(best): best = ser
        if score(best) == 0: break
    return best


@app.post('/sessions', status_code=201)
def create_session(body: NewSession, x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=body.review or bool(body.challenge)); filters = body.filters.model_dump(exclude_none=True); info = None
    plan = body.plan; fixed_seed = None
    if body.challenge:                                                     # étape 5 : la série du défi
        plan = challenges.SERIES[body.challenge]; utc_day = datetime.datetime.now(datetime.timezone.utc).date()
        if body.challenge == 'daily': filters, fixed_seed = {}, challenges.daily_seed(utc_day)      # les mêmes mains pour tous
        elif body.challenge == 'perfect': filters = dict(challenges.perfect_theme(utc_day)[1])
        elif body.challenge == 'pressure': filters = {}
        elif body.challenge == 'reader':
            if body.mode != 'exploit': raise HTTPException(422, 'le défi « Lecteur de vilain » se joue en mode exploitant')
            filters = dict(family='read')
        body.filters = Filters(**filters); body.size = quiz.SERIES_SIZE
    try:
        with closing(connect()) as con:
            version = serving_version(con, body.mode); excluded = _excluded(con)
            want = pid is not None and not filters and not body.review and not body.challenge and body.mode != 'exploit' and (body.adaptive if body.adaptive is not None else _prefs(con, pid)['adaptive'])
            info = _adaptation(con, pid, body.mode, version, body.size, body.seed) if want else None
            due = review.summary(_mode_rows(con, pid, body.mode, None), version)['due_items'] if body.review else None
            recent = _recent(con, pid)
        if due is not None:
            series = [(x['spot_id'], x['hand'], 'spaced', review.purpose_fr(x)) for x in due if x['spot_id'] not in excluded][:body.size]
            taken = {(s, h) for s, h, _, _ in series}
            for s, h in quiz.draw_series(version, filters, body.size, body.seed, excluded):
                if len(series) < body.size and (s, h) not in taken: series.append((s, h, None, None)); taken.add((s, h))
        elif info and info['active']:
            drawn = _least_repeated(lambda sd: quiz.draw_plan(version, info['slots'], adaptive.theme_of, sd, excluded), body.seed, recent)
            series = [(s, h, slot['kind'] if ok or slot['kind'] == 'discovery' else 'complement',
                       (f"{adaptive.PURPOSE_FR[slot['kind']]} : {adaptive.label(tuple(slot['theme']))}" if ok else
                        adaptive.PURPOSE_FR['discovery'] if slot['kind'] == 'discovery' else 'Complément : plus de situation libre sur ce thème'))
                      for s, h, slot, ok in drawn]
        elif fixed_seed is not None:
            series = [(s, h, None, None) for s, h in quiz.draw_series(version, filters, body.size, fixed_seed, excluded)]
        else:
            series = [(s, h, None, None) for s, h in _least_repeated(lambda sd: quiz.draw_series(version, filters, body.size, sd, excluded), body.seed, recent)]
    except ValueError as e:
        raise HTTPException(422, str(e))
    sid = uuid.uuid4().hex
    with closing(connect()) as con, con:
        con.execute('INSERT INTO sessions(id, created_at, dataset_version, filters, seed, size, player_id, plan) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (sid, _now(), version, body.filters.model_dump_json(exclude_none=True), body.seed if fixed_seed is None else fixed_seed, len(series), pid, plan))
        con.executemany('INSERT INTO questions(session_id, idx, spot_id, hand, purpose, purpose_fr) VALUES (?, ?, ?, ?, ?, ?)',
                        [(sid, i, s, h, k, t) for i, (s, h, k, t) in enumerate(series)])
    adapt = None if info is None else dict(active=info['active'], reason_fr=info['reason_fr'], rule_fr=info['rule_fr'])
    return dict(session_id=sid, dataset_version=version, mode=body.mode, size=len(series), adaptive=adapt)


def _session(con, sid):
    row = con.execute('SELECT * FROM sessions WHERE id = ?', (sid,)).fetchone()
    if row is None: raise HTTPException(404, 'session inconnue')
    return row


@app.get('/quiz/next')
def next_question(session_id: str):
    with closing(connect()) as con, con:
        s = _session(con, session_id)
        if catalog.status_of(con, s['dataset_version']) == 'disabled':
            raise HTTPException(410, 'cette série utilise un dataset retiré pour correction : commence une nouvelle série')
        row = con.execute('SELECT q.* FROM questions q LEFT JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx '
                          'WHERE q.session_id = ? AND a.idx IS NULL ORDER BY q.idx LIMIT 1', (session_id,)).fetchone()
        if row is None: return dict(done=True, session_id=session_id)
        if row['served_at'] is None:
            con.execute('UPDATE questions SET served_at = ? WHERE session_id = ? AND idx = ?', (_now(), session_id, row['idx']))
        q = quiz.question(s['dataset_version'], row['spot_id'], row['hand'])
        return dict(done=False, session_id=session_id, question_index=row['idx'], size=s['size'], question=q,
                    purpose=row['purpose'], purpose_fr=row['purpose_fr'])


@app.post('/attempts')
def answer(body: Attempt):
    with closing(connect()) as con, con:
        s = _session(con, body.session_id)
        q = con.execute('SELECT * FROM questions WHERE session_id = ? AND idx = ?', (body.session_id, body.question_index)).fetchone()
        if q is None: raise HTTPException(404, 'question inconnue')
        prev = con.execute('SELECT * FROM attempts WHERE session_id = ? AND idx = ?', (body.session_id, body.question_index)).fetchone()
        if prev is not None:                                  # réponse définitive : on renvoie la correction déjà enregistrée
            if prev['action_id'] != body.action_id: raise HTTPException(409, 'question déjà répondue')
            return dict(json.loads(prev['result']), already_answered=True)
        try:
            r = quiz.correct(s['dataset_version'], q['spot_id'], q['hand'], body.action_id)
        except ValueError as e:
            raise HTTPException(422, str(e))
        if body.timed_out:                                    # décision du porteur du projet : à la table, le temps dépassé n'est jamais un choix
            r = dict(r, verdict='erreur', points=0.0, timed_out=True)
        con.execute('INSERT INTO attempts(session_id, idx, action_id, verdict, points, regret_mbb, result, answered_at, timed_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (body.session_id, body.question_index, body.action_id, r['verdict'], r['points'], r['regret_mbb'],
                     json.dumps(r, ensure_ascii=False), _now(), int(body.timed_out)))
        return dict(r, already_answered=False)


@app.get('/sessions/{session_id}/summary')
def session_summary(session_id: str):
    with closing(connect()) as con:
        s = _session(con, session_id)
        rows = con.execute('SELECT q.spot_id, q.hand, a.result FROM questions q JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx '
                           'WHERE q.session_id = ? ORDER BY q.idx', (session_id,)).fetchall()
        res = quiz.summary(s['dataset_version'], [(r['spot_id'], r['hand'], json.loads(r['result'])) for r in rows])
        return dict(res, session_id=session_id, dataset_version=s['dataset_version'], size=s['size'], complete=len(rows) == s['size'])


def _player_rows(con, pid):
    return [dict(r) for r in con.execute(
        'SELECT s.id AS session_id, s.created_at AS session_created_at, s.dataset_version, q.spot_id, q.hand, a.action_id, a.verdict, '
        'a.points, a.regret_mbb, a.answered_at, a.timed_out FROM sessions s JOIN questions q ON q.session_id = s.id '
        'JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx WHERE s.player_id = ? ORDER BY a.answered_at', (pid,))]


@app.get('/users/me/stats')
def my_stats(x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=True)
    with closing(connect()) as con:
        out = progress.compute(_player_rows(con, pid))
        out['ranges'] = _range_stats(con, pid)
        return out


# ------------------------------------------------------------------ exercice « Construis ta range » (chantier 2)
def _range_stats(con, pid):
    rows = [dict(r) for r in con.execute('SELECT accuracy_pct, bb_per_100 FROM range_attempts WHERE player_id = ? ORDER BY id DESC LIMIT 20', (pid,))]
    n = con.execute('SELECT COUNT(*) FROM range_attempts WHERE player_id = ?', (pid,)).fetchone()[0]
    if not rows: return dict(count=0)
    return dict(count=n, recent=len(rows), accuracy_pct=round(sum(r['accuracy_pct'] for r in rows) / len(rows), 1),
                bb_per_100=round(sum(r['bb_per_100'] for r in rows) / len(rows), 2))


@app.get('/ranges/next')
def range_next(table: Optional[str] = None, hero: Optional[str] = None, family: Optional[str] = None, min_stack: Optional[float] = None,
               max_stack: Optional[float] = None, seed: Optional[int] = None, exclude: str = '', spot: Optional[str] = None):
    """une situation à dessiner ; les fréquences de référence restent sur le serveur jusqu'à la réponse"""
    f = Filters(table=table, hero=hero, family=family, min_stack=min_stack, max_stack=max_stack).model_dump(exclude_none=True)
    with closing(connect()) as con:
        version = serving_version(con, 'gto')
        recent = {x for x in exclude.split(',') if x}                      # dernières situations vues : pas deux fois de suite
        t = None
        if spot and spot in ranges.drawable(version) and spot not in _excluded(con):     # étape 2 : « Refaire cette range »
            t = ranges.task(quiz.load(version)[1][spot])
        t = t or ranges.pick(version, f or None, seed, set(_excluded(con)) | recent)
    if not t: raise HTTPException(422, 'pas de situation à dessiner pour ces filtres')
    return dict(dataset_version=version, **{k: v for k, v in t.items() if k not in ('hands', 'where_fr', 'verb_fr', 'polar_fr')},
                hands=sorted(t['hands']), weights={h: x[3] for h, x in t['hands'].items()})      # poids : la part de range, sans la réponse


class RangeAnswer(BaseModel):
    spot_id: str
    hands: list[str] = Field(default_factory=list, max_length=169)


@app.post('/ranges/answer')
def range_answer(body: RangeAnswer, x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id)
    with closing(connect()) as con, con:
        version = serving_version(con, 'gto'); _, spots = quiz.load(version)
        sp = spots.get(body.spot_id); t = sp and ranges.task(sp)
        if not t: raise HTTPException(404, 'situation inconnue')
        g = ranges.grade(t, [h for h in body.hands if h in t['hands']])
        con.execute('INSERT INTO range_attempts(player_id, dataset_version, spot_id, hands, accuracy_pct, bb_per_100, answered_at) VALUES (?,?,?,?,?,?,?)',
                    (pid, version, body.spot_id, json.dumps(sorted(set(body.hands))), g['accuracy_pct'], g['bb_per_100'], _now()))
    return dict(g, reference={h: x[0] for h, x in t['hands'].items()}, reference_fr={h: x[5] for h, x in t['hands'].items()},
                situation_fr=t['situation_fr'], question_fr=t['question_fr'])


class Preferences(BaseModel):
    adaptive: bool


@app.get('/users/me/preferences')
def get_preferences(x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=True)
    with closing(connect()) as con: return _prefs(con, pid)


@app.put('/users/me/preferences')
def put_preferences(body: Preferences, x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=True)
    with closing(connect()) as con, con:
        con.execute('INSERT INTO preferences(player_id, adaptive, updated_at) VALUES (?, ?, ?) '
                    'ON CONFLICT(player_id) DO UPDATE SET adaptive = excluded.adaptive, updated_at = excluded.updated_at', (pid, int(body.adaptive), _now()))
        return _prefs(con, pid)


@app.get('/users/me/adaptation')
def my_adaptation(mode: str = 'gto', x_player_id: Optional[str] = Header(None)):
    """règle, thèmes à retravailler et thèmes en révision, tels que la prochaine série les utiliserait"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    with closing(connect()) as con:
        info = _adaptation(con, pid, mode, serving_version(con, mode), quiz.SERIES_SIZE, 0); prefs = _prefs(con, pid)
    return dict(mode=mode, enabled=prefs['adaptive'], since=prefs['adaptation_reset_at'], active=info['active'], rule_fr=info['rule_fr'],
                reason_fr=info['reason_fr'], weak=info['weak'], review=info['review'])


@app.get('/users/me/reviews')
def my_reviews(mode: str = 'gto', x_player_id: Optional[str] = Header(None)):
    """révision espacée (1, 3 puis 7 jours) : mains ratées prêtes à revoir, et date de la prochaine"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    with closing(connect()) as con:
        res = review.summary(_mode_rows(con, pid, mode, None), serving_version(con, mode))
    return dict(res, mode=mode, due_items=res['due_items'][:quiz.SERIES_SIZE * 4])


@app.get('/users/me/today')
def my_today(mode: str = 'gto', tz: int = 0, x_player_id: Optional[str] = Header(None)):
    """séance du jour (programme de travail, étape 1) : révision, thème du jour, range du jour ; série de jours ; BB perdus sur 7 jours"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    tz = max(-840, min(840, tz))
    with closing(connect()) as con:
        version = serving_version(con, mode)
        sess = [dict(r) for r in con.execute(
            'SELECT s.created_at, s.plan, s.filters, s.size, s.dataset_version, (SELECT COUNT(*) FROM attempts a WHERE a.session_id = s.id) AS answered '
            'FROM sessions s WHERE s.player_id = ?', (pid,))]
        sess = [x for x in sess if quiz.mode_of(x['dataset_version']) == mode]
        rngs = [r[0] for r in con.execute('SELECT answered_at FROM range_attempts WHERE player_id = ?', (pid,))]
        rows = _mode_rows(con, pid, mode, None)
        due = review.summary(rows, version)['due']
        gto = serving_version(con, 'gto')                                  # l'exercice de range est toujours sur la référence GTO
    now = datetime.datetime.now(datetime.timezone.utc); day = today.local_day(now.isoformat(), tz)
    week = lambda a, b: [r for r in rows if (now - datetime.timedelta(days=b)).isoformat() < (r['answered_at'] or '') <= (now - datetime.timedelta(days=a)).isoformat()]
    stats = progress.compute(rows) if rows else {}
    with closing(connect()) as con, con: lv = _level_row(con, pid)['level'] if mode == 'gto' else 4      # étape 4 : thèmes du niveau
    focus = stats.get('focus')
    if focus and focus.get('filters') and not levels.fits(lv, focus['filters']): focus = None          # un thème fragile hors du niveau attend
    out = today.build(sess, rngs, due, focus, day, tz,
                      progress.compute(week(0, 7)).get('bb_per_100') if week(0, 7) else None,
                      progress.compute(week(7, 14)).get('bb_per_100') if week(7, 14) else None,
                      themes=levels.LEVELS[lv]['themes'], level=dict(number=lv, name=levels.LEVELS[lv]['name']), mode=mode)
    rs = out['steps'][2]
    for f in (rs['filters'], {k: v for k, v in rs['filters'].items() if k != 'hero'},          # range du thème, sinon la plus proche
              {k: v for k, v in rs['filters'].items() if k in ('family', 'table')}, {}):
        if ranges.pick(gto, f or None, seed=0): rs['filters'] = f; break
    return dict(out, mode=mode)


@app.get('/users/me/recommendations')
def my_recommendations(mode: str = 'gto', tz: int = 0, x_player_id: Optional[str] = Header(None)):
    """recommandations de l'accueil (programme de travail, étape 2) : au plus deux, chacune avec un constat chiffré et une action"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    t = my_today(mode, tz, x_player_id)                                  # pour ne pas recommander le thème déjà dans la séance
    with closing(connect()) as con:
        version = serving_version(con, mode); rows = _mode_rows(con, pid, mode, None)
        last = con.execute('SELECT spot_id, hands, accuracy_pct, dataset_version FROM range_attempts WHERE player_id = ? ORDER BY id DESC LIMIT 1', (pid,)).fetchone()
    stats = progress.compute(rows) if rows else {}
    last = dict(last, hands=json.loads(last['hands'])) if last else None
    msg = None
    if mode == 'gto':
        with closing(connect()) as con, con: lvl = _level_info(con, pid)
        msg = levels.almost(lvl['status'])
    return dict(mode=mode, items=recommend.build(stats, review.items(rows, version), last, rows, t['steps'][1]['filters'], level_msg=msg))


# ------------------------------------------------------------------ niveaux et premier lancement (programme de travail, étape 4)
def _level_row(con, pid):
    r = con.execute('SELECT * FROM player_level WHERE player_id = ?', (pid,)).fetchone()
    if r: return dict(r)
    played = con.execute('SELECT 1 FROM sessions WHERE player_id = ? LIMIT 1', (pid,)).fetchone()
    if played:                                                             # joueur d'avant les niveaux : niveau 1, il monte d'après ses résultats
        con.execute('INSERT OR IGNORE INTO player_level(player_id, level, onboarded_at, updated_at) VALUES (?, 1, ?, ?)', (pid, _now(), _now()))
        return dict(player_id=pid, level=1, experience=None, goal=None, onboarded_at=_now(), promoted_at=None)
    return dict(player_id=pid, level=1, experience=None, goal=None, onboarded_at=None, promoted_at=None)


def _level_info(con, pid):
    """niveau du joueur, passage automatique au suivant quand les critères sont tenus, avancement"""
    row = _level_row(con, pid); promoted = None
    rows = _player_rows(con, pid)
    rr = [dict(r) for r in con.execute('SELECT spot_id, accuracy_pct FROM range_attempts WHERE player_id = ?', (pid,))]
    gto = serving_version(con, 'gto')
    while True:
        st = levels.status(row['level'], rows, rr, levels.level_spots(gto, row['level']) if row['level'] == 1 else set())
        if not st['ready'] or not row['onboarded_at']: break
        row['level'] += 1; promoted = row['level']
        con.execute('UPDATE player_level SET level = ?, promoted_at = ?, updated_at = ? WHERE player_id = ?', (row['level'], _now(), _now(), pid))
    lv = levels.LEVELS[row['level']]
    return dict(level=row['level'], name=lv['name'], onboarded=bool(row['onboarded_at']), experience=row['experience'], goal=row['goal'],
                promoted_to=promoted, status=st, levels=[dict(number=k, name=v['name'], mode=v['mode']) for k, v in levels.LEVELS.items()],
                experiences=levels.EXPERIENCE_FR, goals=levels.GOAL_FR)


@app.get('/users/me/level')
def my_level(x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=True)
    with closing(connect()) as con, con: return _level_info(con, pid)


class Onboarding(BaseModel):
    experience: str = Field(pattern='^(debut|confirme|gros_volume)$')
    goal: str = Field(pattern='^(bases|recreatifs|ranges)$')
    level: Optional[int] = Field(None, ge=1, le=3)


@app.post('/users/me/onboarding')
def onboarding(body: Onboarding, x_player_id: Optional[str] = Header(None)):
    """premier lancement : expérience, but, niveau de départ (proposé d'après l'expérience, modifiable)"""
    pid = player(x_player_id, required=True)
    lv = body.level or levels.START_LEVEL[body.experience]
    with closing(connect()) as con, con:
        con.execute('INSERT INTO player_level(player_id, level, experience, goal, onboarded_at, updated_at) VALUES (?, ?, ?, ?, ?, ?) '
                    'ON CONFLICT(player_id) DO UPDATE SET level = excluded.level, experience = excluded.experience, goal = excluded.goal, '
                    'onboarded_at = excluded.onboarded_at, updated_at = excluded.updated_at', (pid, lv, body.experience, body.goal, _now(), _now()))
        return _level_info(con, pid)


class LevelChange(BaseModel):
    level: int = Field(ge=1, le=3)


@app.put('/users/me/level')
def set_level(body: LevelChange, x_player_id: Optional[str] = Header(None)):
    """le joueur choisit son niveau GTO (1 à 3) ; le niveau exploitant se joue en mode exploitant"""
    pid = player(x_player_id, required=True)
    with closing(connect()) as con, con:
        _level_row(con, pid)
        con.execute('INSERT INTO player_level(player_id, level, onboarded_at, updated_at) VALUES (?, ?, ?, ?) '
                    'ON CONFLICT(player_id) DO UPDATE SET level = excluded.level, updated_at = excluded.updated_at', (pid, body.level, _now(), _now()))
        return _level_info(con, pid)


def _goal_data(con, pid, mode):
    sess = [dict(r) for r in con.execute(
        'SELECT s.created_at, s.plan, s.size, s.dataset_version, (SELECT COUNT(*) FROM attempts a WHERE a.session_id = s.id) AS answered '
        'FROM sessions s WHERE s.player_id = ?', (pid,))]
    sess = [x for x in sess if quiz.mode_of(x['dataset_version']) == mode]
    rgs = [dict(r) for r in con.execute('SELECT answered_at, accuracy_pct FROM range_attempts WHERE player_id = ?', (pid,))]
    return _mode_rows(con, pid, mode, None), sess, rgs


def _targets(con, pid, mode, week):
    return {r['kind']: r['target'] for r in con.execute('SELECT kind, target FROM goals WHERE player_id = ? AND mode = ? AND week = ?', (pid, mode, week))}


@app.get('/users/me/goals')
def my_goals(mode: str = 'gto', tz: int = 0, x_player_id: Optional[str] = Header(None)):
    """objectifs de la semaine (programme de travail, étape 3) et bilan de la semaine passée"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    tz = max(-840, min(840, tz))
    day = today.local_day(datetime.datetime.now(datetime.timezone.utc).isoformat(), tz); start = goals.week_start(day)
    wk = lambda k: start - datetime.timedelta(days=7 * k)
    with closing(connect()) as con, con:
        rows, sess, rgs = _goal_data(con, pid, mode)
        vals = lambda k: goals.week_values(rows, sess, rgs, wk(k), tz)
        cur = _targets(con, pid, mode, start.isoformat())
        prev_t = _targets(con, pid, mode, wk(1).isoformat()); prev_v = vals(1)
        if len(cur) < len(goals.KINDS):                                    # première visite de la semaine : cibles proposées, puis gardées
            prop = goals.propose(prev_t, prev_v if prev_t else None, [vals(k)['precision'] if vals(k)['decisions'] >= goals.MIN_DECISIONS else None for k in (1, 2, 3, 4)])
            for k, t in prop.items():
                if k not in cur:
                    con.execute('INSERT OR IGNORE INTO goals(player_id, mode, week, kind, target, updated_at) VALUES (?, ?, ?, ?, ?, ?)', (pid, mode, start.isoformat(), k, t, _now()))
                    cur[k] = t
    last = None
    if prev_v['days'] or prev_v['ranges'] or prev_v['decisions']:                  # bilan seulement si la semaine passée a servi
        items = goals.view({k: prev_t.get(k, goals.DEFAULT.get(k, goals.DEFAULT_BB)) for k in goals.KINDS}, prev_v)
        last = dict(week=wk(1).isoformat(), done=sum(x['done'] for x in items), total=len(items), bb=prev_v['precision'],
                    bb_before=vals(2)['precision'], days=prev_v['days'], decisions=prev_v['decisions'])
    return dict(mode=mode, week=start.isoformat(), days_left=6 - day.weekday(), items=goals.view(cur, vals(0)), last_week=last)


class GoalChange(BaseModel):
    mode: str = Field('gto', pattern='^(gto|exploit)$')
    kind: str = Field(pattern='^(days|precision|ranges)$')
    target: float
    tz: int = 0


@app.put('/users/me/goals')
def set_goal(body: GoalChange, x_player_id: Optional[str] = Header(None)):
    """le joueur change une cible de la semaine en cours (dans les bornes de l'objectif)"""
    pid = player(x_player_id, required=True)
    lo, hi = goals.BOUNDS[body.kind]
    t = round(body.target * 2) / 2 if body.kind == 'precision' else round(body.target)
    if not lo <= t <= hi: raise HTTPException(422, f'cible hors des bornes ({lo} à {hi})')
    day = today.local_day(datetime.datetime.now(datetime.timezone.utc).isoformat(), max(-840, min(840, body.tz)))
    with closing(connect()) as con, con:
        con.execute('INSERT INTO goals(player_id, mode, week, kind, target, updated_at) VALUES (?, ?, ?, ?, ?, ?) '
                    'ON CONFLICT(player_id, mode, week, kind) DO UPDATE SET target = excluded.target, updated_at = excluded.updated_at',
                    (pid, body.mode, goals.week_start(day).isoformat(), body.kind, t, _now()))
    return my_goals(body.mode, body.tz, x_player_id)


@app.get('/users/me/challenges')
def my_challenges(mode: str = 'gto', tz: int = 0, x_player_id: Optional[str] = Header(None)):
    """défis du jour, de la semaine et du mois, et historique « Mes défis » (programme de travail, étape 5)"""
    pid = player(x_player_id, required=True)
    if mode not in quiz.MODES: raise HTTPException(422, 'mode inconnu')
    tz = max(-840, min(840, tz)); now = datetime.datetime.now(datetime.timezone.utc); day = today.local_day(now.isoformat(), tz)
    with closing(connect()) as con:
        sess = [dict(r) for r in con.execute(
            'SELECT s.created_at, s.plan, s.size, s.dataset_version, '
            '(SELECT COUNT(*) FROM attempts a WHERE a.session_id = s.id) AS answered, '
            "(SELECT COUNT(*) FROM attempts a WHERE a.session_id = s.id AND a.verdict = 'correct') AS correct, "
            '(SELECT COALESCE(SUM(a.timed_out), 0) FROM attempts a WHERE a.session_id = s.id) AS timeouts '
            'FROM sessions s WHERE s.player_id = ?', (pid,))]
        rgs = [dict(r) for r in con.execute('SELECT answered_at, bb_per_100 FROM range_attempts WHERE player_id = ?', (pid,))]
    mine = [x for x in sess if quiz.mode_of(x['dataset_version']) == mode]
    active = {today.local_day(x['created_at'], tz) for x in sess if x['answered'] >= x['size']} | {today.local_day(r['answered_at'], tz) for r in rgs}
    return dict(mode=mode, **challenges.build(mine, rgs, active, day, tz, mode, now.date()))


@app.post('/users/me/adaptation/reset')
def reset_adaptation(x_player_id: Optional[str] = Header(None)):
    """l'adaptation repart de zéro (les statistiques et l'historique sont conservés)"""
    pid = player(x_player_id, required=True); now = _now()
    with closing(connect()) as con, con:
        con.execute('INSERT INTO preferences(player_id, adaptive, adaptation_reset_at, updated_at) VALUES (?, 1, ?, ?) '
                    'ON CONFLICT(player_id) DO UPDATE SET adaptation_reset_at = excluded.adaptation_reset_at, updated_at = excluded.updated_at', (pid, now, now))
        return _prefs(con, pid)


@app.get('/users/me/export')
def my_export(x_player_id: Optional[str] = Header(None)):
    """toutes les données enregistrées pour ce joueur (droit d'accès et de portabilité)"""
    pid = player(x_player_id, required=True)
    with closing(connect()) as con:
        sessions = [dict(r) for r in con.execute('SELECT id, created_at, dataset_version, filters, seed, size FROM sessions WHERE player_id = ?', (pid,))]
        ranges_done = [dict(r) for r in con.execute('SELECT dataset_version, spot_id, hands, accuracy_pct, bb_per_100, answered_at FROM range_attempts WHERE player_id = ?', (pid,))]
        goals_set = [dict(r) for r in con.execute('SELECT mode, week, kind, target, updated_at FROM goals WHERE player_id = ?', (pid,))]
        return dict(player_id=pid, exported_at=_now(), preferences=_prefs(con, pid), sessions=sessions, answers=_player_rows(con, pid), ranges=ranges_done, goals=goals_set,
                    level=dict(r) if (r := con.execute('SELECT level, experience, goal, onboarded_at, promoted_at FROM player_level WHERE player_id = ?', (pid,)).fetchone()) else None)


@app.delete('/users/me', status_code=204)
def delete_me(x_player_id: Optional[str] = Header(None)):
    """efface définitivement les séries et réponses de ce joueur (droit à l'effacement)"""
    pid = player(x_player_id, required=True)
    with closing(connect()) as con, con:
        ids = [r[0] for r in con.execute('SELECT id FROM sessions WHERE player_id = ?', (pid,))]
        for sid in ids:
            con.execute('DELETE FROM attempts WHERE session_id = ?', (sid,)); con.execute('DELETE FROM questions WHERE session_id = ?', (sid,))
        con.execute('DELETE FROM sessions WHERE player_id = ?', (pid,))
        con.execute('DELETE FROM range_attempts WHERE player_id = ?', (pid,))
        con.execute('DELETE FROM preferences WHERE player_id = ?', (pid,))
        con.execute('DELETE FROM goals WHERE player_id = ?', (pid,))
        con.execute('DELETE FROM player_level WHERE player_id = ?', (pid,))


# ------------------------------------------------------------------ signalements (cahier des charges §7 et §14)
class Report(BaseModel):
    session_id: str
    question_index: int = Field(ge=0)
    reason: str = Field(pattern='^(' + '|'.join(REASONS) + ')$')
    comment: Optional[str] = Field(None, max_length=1000)


@app.post('/reports', status_code=201)
def report(body: Report, x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id)
    with closing(connect()) as con, con:
        s = _session(con, body.session_id)
        q = con.execute('SELECT q.spot_id, q.hand, a.action_id FROM questions q JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx '
                        'WHERE q.session_id = ? AND q.idx = ?', (body.session_id, body.question_index)).fetchone()
        if q is None: raise HTTPException(409, 'on ne peut signaler qu\'une question à laquelle on a répondu')
        try:
            cur = con.execute('INSERT INTO reports(created_at, player_id, session_id, question_index, dataset_version, spot_id, hand, action_id, reason, comment) '
                              'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (_now(), pid, body.session_id, body.question_index, s['dataset_version'],
                                                                      q['spot_id'], q['hand'], q['action_id'], body.reason, (body.comment or '').strip() or None))
        except sqlite3.IntegrityError:
            raise HTTPException(409, 'cette question a déjà été signalée')
        return dict(report_id=cur.lastrowid, status='open')


def admin(token):
    expected = os.environ.get('SPINSACADEMY_ADMIN_TOKEN')
    if not expected: raise HTTPException(403, 'administration désactivée (SPINSACADEMY_ADMIN_TOKEN non défini)')
    if not hmac.compare_digest((token or '').encode(), expected.encode()):          # comparaison à temps constant
        raise HTTPException(403, 'jeton d\'administration invalide')
    return 'admin'


def _log(con, actor, action, **details):
    con.execute('INSERT INTO admin_log(at, actor, action, details) VALUES (?, ?, ?, ?)', (_now(), actor, action, json.dumps(details, ensure_ascii=False)))


@app.get('/admin/reports')
def list_reports(status: str = 'open', x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con:
        rows = [dict(r) for r in con.execute('SELECT * FROM reports WHERE status = ? ORDER BY created_at', (status,))]
    for r in rows:
        r['reason_fr'] = REASONS[r['reason']]
        try:
            r['prompt_fr'] = quiz.question(r['dataset_version'], r['spot_id'], r['hand'])['prompt_fr']
            r['correction'] = quiz.correct(r['dataset_version'], r['spot_id'], r['hand'], r['action_id'])   # ce que le joueur a vu
        except (KeyError, ValueError): r['prompt_fr'] = r['correction'] = None
        same = sum(1 for x in rows if x['spot_id'] == r['spot_id']); r['reports_on_spot'] = same
    return rows


class Resolution(BaseModel):
    status: str = Field(pattern='^(accepted|rejected)$')
    resolution: str = Field(min_length=3, max_length=1000)
    disable_spot: bool = False
    actor: str = Field('admin', max_length=80)


@app.post('/admin/reports/{report_id}/resolve')
def resolve(report_id: int, body: Resolution, x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con, con:
        r = con.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
        if r is None: raise HTTPException(404, 'signalement inconnu')
        if r['status'] != 'open': raise HTTPException(409, 'signalement déjà traité')
        con.execute('UPDATE reports SET status = ?, resolution = ?, resolved_at = ? WHERE id = ?', (body.status, body.resolution, _now(), report_id))
        if body.disable_spot:
            con.execute('INSERT OR REPLACE INTO disabled_spots VALUES (?, ?, ?, ?, ?, ?)', (r['spot_id'], r['dataset_version'], body.resolution, report_id, _now(), body.actor))
        _log(con, body.actor, 'resolve_report', report_id=report_id, status=body.status, resolution=body.resolution,
             disabled_spot=r['spot_id'] if body.disable_spot else None)
    return dict(report_id=report_id, status=body.status, disabled_spot=r['spot_id'] if body.disable_spot else None)


@app.get('/admin/disabled')
def list_disabled(x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con:
        return [dict(r) for r in con.execute('SELECT * FROM disabled_spots ORDER BY disabled_at')]


@app.delete('/admin/disabled/{spot_id}')
def enable_spot(spot_id: str, reason: str, actor: str = 'admin', x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con, con:
        if con.execute('DELETE FROM disabled_spots WHERE spot_id = ?', (spot_id,)).rowcount == 0: raise HTTPException(404, 'spot non désactivé')
        _log(con, actor, 'enable_spot', spot_id=spot_id, reason=reason)
    return dict(spot_id=spot_id, enabled=True)


@app.get('/admin/log')
def admin_log(x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con:
        return [dict(r, details=json.loads(r['details'])) for r in con.execute('SELECT * FROM admin_log ORDER BY id')]


# ------------------------------------------------------------------ datasets (cahier des charges §2, §13.1 et §16)
class DatasetAction(BaseModel):
    reason: str = Field(min_length=3, max_length=1000)
    actor: str = Field('admin', max_length=80)


class Actor(BaseModel):
    actor: str = Field('admin', max_length=80)


def _lifecycle(fn):
    try: return fn()
    except catalog.LifecycleError as e: raise HTTPException(409, str(e))


@app.get('/admin/datasets')
def list_datasets(x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con: return catalog.listing(con)


@app.get('/admin/datasets/{dataset}/{version}/report')
def dataset_report(dataset: str, version: str, x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token)
    with closing(connect()) as con:
        rep = _lifecycle(lambda: catalog.report(con, f'{dataset}/{version}'))
    if rep is None: raise HTTPException(404, 'pas encore contrôlé')
    return rep


@app.post('/admin/datasets/{dataset}/{version}/validate')
def validate_dataset(dataset: str, version: str, body: Actor, x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token); ref = f'{dataset}/{version}'
    with closing(connect()) as con, con:
        rep, status = _lifecycle(lambda: catalog.run_validation(con, ref, body.actor))
        _log(con, body.actor, 'validate_dataset', ref=ref, ok=rep['ok'], status=status, summary=rep['summary_fr'])
    return dict(rep, status=status)


@app.post('/admin/datasets/{dataset}/{version}/publish')
def publish_dataset(dataset: str, version: str, body: DatasetAction, x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token); ref = f'{dataset}/{version}'
    with closing(connect()) as con, con:
        prev = _lifecycle(lambda: catalog.publish(con, ref, body.actor, body.reason))
        _log(con, body.actor, 'publish_dataset', ref=ref, replaced=prev, reason=body.reason)
    return dict(ref=ref, status='published', replaced=prev)


@app.post('/admin/datasets/{dataset}/{version}/disable')
def disable_dataset(dataset: str, version: str, body: DatasetAction, x_admin_token: Optional[str] = Header(None)):
    admin(x_admin_token); ref = f'{dataset}/{version}'
    with closing(connect()) as con, con:
        deps = _lifecycle(lambda: catalog.disable(con, ref, body.actor, body.reason))
        _log(con, body.actor, 'disable_dataset', ref=ref, also_disabled=deps, reason=body.reason)
    return dict(ref=ref, status='disabled', also_disabled=deps)

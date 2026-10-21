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
import datetime, hmac, json, os, re, sqlite3, uuid
from contextlib import closing
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from . import adaptive, catalog, progress, quiz, ratelimit, review
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


class Attempt(BaseModel):
    session_id: str
    question_index: int = Field(ge=0)
    action_id: str


app = FastAPI(title='SpinsAcademy', version='0.1.0')
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


@app.post('/sessions', status_code=201)
def create_session(body: NewSession, x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=body.review); filters = body.filters.model_dump(exclude_none=True); info = None
    try:
        with closing(connect()) as con:
            version = serving_version(con, body.mode); excluded = _excluded(con)
            want = pid is not None and not filters and not body.review and body.mode != 'exploit' and (body.adaptive if body.adaptive is not None else _prefs(con, pid)['adaptive'])
            info = _adaptation(con, pid, body.mode, version, body.size, body.seed) if want else None
            due = review.summary(_mode_rows(con, pid, body.mode, None), version)['due_items'] if body.review else None
        if due is not None:
            series = [(x['spot_id'], x['hand'], 'spaced', review.purpose_fr(x)) for x in due if x['spot_id'] not in excluded][:body.size]
            taken = {(s, h) for s, h, _, _ in series}
            for s, h in quiz.draw_series(version, filters, body.size, body.seed, excluded):
                if len(series) < body.size and (s, h) not in taken: series.append((s, h, None, None)); taken.add((s, h))
        elif info and info['active']:
            drawn = quiz.draw_plan(version, info['slots'], adaptive.theme_of, body.seed, excluded)
            series = [(s, h, slot['kind'] if ok or slot['kind'] == 'discovery' else 'complement',
                       (f"{adaptive.PURPOSE_FR[slot['kind']]} : {adaptive.label(tuple(slot['theme']))}" if ok else
                        adaptive.PURPOSE_FR['discovery'] if slot['kind'] == 'discovery' else 'Complément : plus de situation libre sur ce thème'))
                      for s, h, slot, ok in drawn]
        else:
            series = [(s, h, None, None) for s, h in quiz.draw_series(version, filters, body.size, body.seed, excluded)]
    except ValueError as e:
        raise HTTPException(422, str(e))
    sid = uuid.uuid4().hex
    with closing(connect()) as con, con:
        con.execute('INSERT INTO sessions(id, created_at, dataset_version, filters, seed, size, player_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (sid, _now(), version, body.filters.model_dump_json(exclude_none=True), body.seed, len(series), pid))
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
        con.execute('INSERT INTO attempts VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (body.session_id, body.question_index, body.action_id, r['verdict'],
                                                                           r['points'], r['regret_mbb'], json.dumps(r, ensure_ascii=False), _now()))
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
        'a.points, a.regret_mbb, a.answered_at FROM sessions s JOIN questions q ON q.session_id = s.id '
        'JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx WHERE s.player_id = ? ORDER BY a.answered_at', (pid,))]


@app.get('/users/me/stats')
def my_stats(x_player_id: Optional[str] = Header(None)):
    pid = player(x_player_id, required=True)
    with closing(connect()) as con:
        return progress.compute(_player_rows(con, pid))


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
        return dict(player_id=pid, exported_at=_now(), preferences=_prefs(con, pid), sessions=sessions, answers=_player_rows(con, pid))


@app.delete('/users/me', status_code=204)
def delete_me(x_player_id: Optional[str] = Header(None)):
    """efface définitivement les séries et réponses de ce joueur (droit à l'effacement)"""
    pid = player(x_player_id, required=True)
    with closing(connect()) as con, con:
        ids = [r[0] for r in con.execute('SELECT id FROM sessions WHERE player_id = ?', (pid,))]
        for sid in ids:
            con.execute('DELETE FROM attempts WHERE session_id = ?', (sid,)); con.execute('DELETE FROM questions WHERE session_id = ?', (sid,))
        con.execute('DELETE FROM sessions WHERE player_id = ?', (pid,))
        con.execute('DELETE FROM preferences WHERE player_id = ?', (pid,))


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

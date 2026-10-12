"""API du quiz (FastAPI + SQLite), routes du cahier des charges §13.1.

  POST /sessions                 créer une série (filtres, taille, graine) liée à une version de dataset
  GET  /quiz/next?session_id=    question suivante non répondue (sans solution) ; done=true à la fin
  POST /attempts                 répondre à une question : correction et explication ; une réponse est définitive
  GET  /sessions/{id}/summary    bilan : score, verdicts, thèmes, erreurs à revoir
  GET  /health
Mode invité au MVP : pas d'authentification (cahier des charges §19, question 22, à trancher).
Base : SPINSACADEMY_DB (par défaut data/app/spinsacademy.sqlite) ; dataset : SPINSACADEMY_DATASET.
"""
import datetime, json, os, sqlite3, uuid
from contextlib import closing
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from . import quiz
from .hrc import ROOT

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, dataset_version TEXT NOT NULL,
  filters TEXT NOT NULL, seed INTEGER, size INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS questions(session_id TEXT NOT NULL REFERENCES sessions(id), idx INTEGER NOT NULL,
  spot_id TEXT NOT NULL, hand TEXT NOT NULL, served_at TEXT, PRIMARY KEY(session_id, idx));
CREATE TABLE IF NOT EXISTS attempts(session_id TEXT NOT NULL, idx INTEGER NOT NULL, action_id TEXT NOT NULL,
  verdict TEXT NOT NULL, points REAL NOT NULL, regret_mbb REAL NOT NULL, result TEXT NOT NULL, answered_at TEXT NOT NULL,
  PRIMARY KEY(session_id, idx), FOREIGN KEY(session_id, idx) REFERENCES questions(session_id, idx));
"""


def _now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def db_path(): return os.environ.get('SPINSACADEMY_DB', os.path.join(ROOT, 'data', 'app', 'spinsacademy.sqlite'))


def connect():
    path = db_path(); os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path); con.row_factory = sqlite3.Row; con.execute('PRAGMA foreign_keys = ON'); con.executescript(SCHEMA)
    return con


class Filters(BaseModel):
    table: Optional[str] = Field(None, pattern='^(3-handed|heads-up)$')
    hero: Optional[str] = Field(None, pattern='^(BTN|SB|BB)$')
    family: Optional[str] = Field(None, pattern='^(first_in|vs_limp|vs_raise|vs_allin)$')
    min_stack: Optional[float] = None
    max_stack: Optional[float] = None


class NewSession(BaseModel):
    filters: Filters = Filters()
    size: int = Field(quiz.SERIES_SIZE, ge=1, le=20)
    seed: Optional[int] = None


class Attempt(BaseModel):
    session_id: str
    question_index: int = Field(ge=0)
    action_id: str


app = FastAPI(title='SpinsAcademy', version='0.1.0')


@app.get('/health')
def health():
    m, spots = quiz.load(quiz.DEFAULT_VERSION)
    return dict(status='ok', dataset_version=m['version'], spots=len(spots))


@app.post('/sessions', status_code=201)
def create_session(body: NewSession):
    version = quiz.DEFAULT_VERSION
    try:
        series = quiz.draw_series(version, body.filters.model_dump(exclude_none=True), body.size, body.seed)
    except ValueError as e:
        raise HTTPException(422, str(e))
    sid = uuid.uuid4().hex
    with closing(connect()) as con, con:
        con.execute('INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)', (sid, _now(), version, body.filters.model_dump_json(exclude_none=True), body.seed, len(series)))
        con.executemany('INSERT INTO questions(session_id, idx, spot_id, hand) VALUES (?, ?, ?, ?)', [(sid, i, s, h) for i, (s, h) in enumerate(series)])
    return dict(session_id=sid, dataset_version=version, size=len(series))


def _session(con, sid):
    row = con.execute('SELECT * FROM sessions WHERE id = ?', (sid,)).fetchone()
    if row is None: raise HTTPException(404, 'session inconnue')
    return row


@app.get('/quiz/next')
def next_question(session_id: str):
    with closing(connect()) as con, con:
        s = _session(con, session_id)
        row = con.execute('SELECT q.* FROM questions q LEFT JOIN attempts a ON a.session_id = q.session_id AND a.idx = q.idx '
                          'WHERE q.session_id = ? AND a.idx IS NULL ORDER BY q.idx LIMIT 1', (session_id,)).fetchone()
        if row is None: return dict(done=True, session_id=session_id)
        if row['served_at'] is None:
            con.execute('UPDATE questions SET served_at = ? WHERE session_id = ? AND idx = ?', (_now(), session_id, row['idx']))
        q = quiz.question(s['dataset_version'], row['spot_id'], row['hand'])
        return dict(done=False, session_id=session_id, question_index=row['idx'], size=s['size'], question=q)


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

"""Limitation du nombre de requêtes sur les routes publiques (évaluation du MVP, remarque 25).

Fenêtre glissante d'une minute, en mémoire (un seul processus : c'est le déploiement du MVP), par adresse IP et par
identifiant de joueur (en-tête X-Player-Id). Au-delà : 429 avec Retry-After et un message en français.
Réglages (variables d'environnement) :
  SPINSACADEMY_RATE_LIMIT   multiplicateur des plafonds (1 par défaut ; 0 désactive, utilisé par les tests)
  SPINSACADEMY_TRUST_PROXY  1 : l'adresse du client est la dernière de X-Forwarded-For (derrière Caddy) ; sinon l'adresse de connexion
Les plafonds sont larges pour un joueur réel (une série de 5 questions fait une douzaine de requêtes) et coupent les scripts.
L'administration a son jeton et n'est pas limitée ici ; le proxy peut ajouter sa propre limite (docs/exploitation/SECURITE.md).
"""
import collections, math, os, threading, time

WINDOW_S = 60.0
LIMITS = {                                   # (clé, requêtes par minute)
    'ip': 300,                               # toutes routes publiques confondues, par adresse
    'player': 120,                           # par joueur
    'player:POST /sessions': 30,             # créations de séries
    'player:POST /reports': 10,              # signalements
}
EXEMPT_PREFIXES = ('/static/', '/admin', '/health')
MESSAGE_FR = 'Trop de requêtes en peu de temps : attends {s} s avant de réessayer.'

_hits = collections.defaultdict(collections.deque); _lock = threading.Lock()


def factor():
    try: return float(os.environ.get('SPINSACADEMY_RATE_LIMIT', '1'))
    except ValueError: return 1.0


def client_ip(headers, peer):
    if os.environ.get('SPINSACADEMY_TRUST_PROXY') == '1':
        fwd = [x.strip() for x in headers.get('x-forwarded-for', '').split(',') if x.strip()]
        if fwd: return fwd[-1]
    return peer or '?'


def check(method, path, ip, player, now=None):
    """None si la requête passe, sinon le nombre de secondes à attendre"""
    f = factor()
    if f <= 0 or path == '/' or path.startswith(EXEMPT_PREFIXES): return None
    now = time.monotonic() if now is None else now
    keys = [('ip', ip, LIMITS['ip'])]
    if player:
        keys.append(('player', player, LIMITS['player']))
        route = f'player:{method} {path}'
        if route in LIMITS: keys.append((route, player, LIMITS[route]))
    with _lock:
        wait = 0.0
        for name, who, cap in keys:
            q = _hits[(name, who)]
            while q and q[0] <= now - WINDOW_S: q.popleft()
            if len(q) >= max(1, int(cap * f)): wait = max(wait, q[0] + WINDOW_S - now)
        if wait > 0: return max(1, math.ceil(wait))
        for name, who, _ in keys: _hits[(name, who)].append(now)
        if len(_hits) > 50_000:                                         # ménage : clés inactives
            for k in [k for k, q in _hits.items() if not q or q[-1] <= now - WINDOW_S]: del _hits[k]
    return None


def reset():
    with _lock: _hits.clear()

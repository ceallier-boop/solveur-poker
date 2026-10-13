"""Profils exploitants fictifs (cahier des charges §6) : catalogue versionné data/profiles/exploit_profiles_<version>.json.

Chaque profil disponible porte une tendance chiffrée (facteur sur la cote de tapis, règle de spinsacademy.exploit) ;
un spot exploitant est rattaché au profil dont le facteur est celui de sa range déformée. Le profil affiché n'est
qu'une hypothèse de simulation. La confiance d'une adaptation est tirée de l'écart d'EV du spot : « élevée » au-delà
de exploit.CLEAR_MBB, « moyenne » en dessous ; elle suppose toujours que le profil est exact.
"""
import glob, json, os
from functools import lru_cache
from .hrc import ROOT

DIR = os.path.join(ROOT, 'data', 'profiles')


def _key(path):
    return tuple(int(x) for x in os.path.basename(path)[len('exploit_profiles_'):-len('.json')].split('.'))


@lru_cache(maxsize=4)
def catalog(version=None):
    """catalogue d'une version (par défaut : la plus récente)"""
    files = sorted(glob.glob(os.path.join(DIR, 'exploit_profiles_*.json')), key=_key)
    if version: files = [f for f in files if os.path.basename(f) == f'exploit_profiles_{version}.json']
    if not files: raise FileNotFoundError(f'catalogue de profils introuvable ({version or "aucune version"})')
    return json.load(open(files[-1]))


def for_villain(villain, version=None):
    """profil disponible dont la tendance correspond au vilain d'un spot, ou None"""
    if not villain: return None
    c = catalog(version)
    for p in c['profiles']:
        t = p.get('tendency')
        if p['available'] and t and t['stat'] == villain['stat'] and abs(t['odds_factor'] - villain['factor']) < 1e-9:
            return dict(p, catalog_version=c['version'])
    return None


def _freq(k, p):
    """fréquence (0..1) d'un joueur dont la cote de tapis vaut k fois celle du GTO (fréquence GTO p)"""
    return k * p / (1 + (k - 1) * p) if p < 1 else 1.0


def band(p, gto_pct):
    """fourchette de reconnaissance du profil dans une situation : (min %, max %), None pour une borne ouverte"""
    idf = p.get('identification') or {}; q = gto_pct / 100
    lo, hi = idf.get('odds_factor_min'), idf.get('odds_factor_max')
    return (None if lo is None else round(100 * _freq(lo, q), 1), None if hi is None else round(100 * _freq(hi, q), 1))


def public(p, gto_pct=None):
    """ce que voit le joueur avant de répondre (pas de conseil d'adaptation) ; avec gto_pct : fourchette de reconnaissance"""
    out = {k: p[k] for k in ('id', 'name_fr', 'description_fr', 'difficulty', 'catalog_version')}
    if gto_pct is not None and p.get('identification'): out['band_pct'] = list(band(p, gto_pct))
    return out


def confidence(ev_mbb):
    from .exploit import CLEAR_MBB
    return 'élevée' if abs(ev_mbb) >= CLEAR_MBB else 'moyenne'

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


def public(p):
    """ce que voit le joueur avant de répondre (pas de conseil d'adaptation)"""
    return {k: p[k] for k in ('id', 'name_fr', 'description_fr', 'difficulty', 'catalog_version')}


def confidence(ev_mbb):
    from .exploit import CLEAR_MBB
    return 'élevée' if abs(ev_mbb) >= CLEAR_MBB else 'moyenne'

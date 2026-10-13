"""Sauvegarde, vérification et restauration de la base SQLite de l'application (cahier des charges §14 et §15.2).

  python tools/ops/backup.py backup  [--db BASE] [--dir DOSSIER] [--keep 30]   copie à chaud (API de sauvegarde SQLite), compressée
  python tools/ops/backup.py verify  FICHIER                                   intégrité et tables attendues
  python tools/ops/backup.py restore FICHIER [--db BASE]                       service arrêté : remplace la base (l'ancienne est conservée)
  python tools/ops/backup.py list    [--dir DOSSIER]
La base est SPINSACADEMY_DB (ou --db). La sauvegarde à chaud est cohérente même si l'application écrit pendant la copie.
Les sauvegardes de plus de --keep jours sont supprimées, mais on en garde toujours au moins --min (7 par défaut).
"""
import argparse, datetime, glob, gzip, hashlib, os, shutil, sqlite3, sys, tempfile

TABLES = {'sessions', 'questions', 'attempts', 'reports', 'disabled_spots', 'admin_log', 'datasets', 'preferences'}


def _db(a): return a.db or os.environ.get('SPINSACADEMY_DB') or sys.exit('base inconnue : --db ou SPINSACADEMY_DB')


def _check(path):
    """(ok, message) pour un fichier SQLite non compressé"""
    con = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        res = con.execute('PRAGMA integrity_check').fetchone()[0]
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        counts = {t: con.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0] for t in sorted(TABLES & tables)}
    finally:
        con.close()
    missing = TABLES - tables
    ok = res == 'ok' and not (missing - {'datasets', 'preferences'})          # bases antérieures : tables ajoutées depuis
    return ok, f"intégrité {res} ; " + ', '.join(f'{t} {n}' for t, n in counts.items()) + (f" ; tables absentes : {', '.join(sorted(missing))}" if missing else '')


def _unpack(path, tmpdir):
    if not path.endswith('.gz'): return path
    out = os.path.join(tmpdir, 'base.sqlite')
    with gzip.open(path, 'rb') as f, open(out, 'wb') as g: shutil.copyfileobj(f, g)
    return out


def backup(a):
    db = _db(a); os.makedirs(a.dir, exist_ok=True)
    if not os.path.isfile(db): sys.exit(f'base absente : {db}')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, 'copie.sqlite')
        src = sqlite3.connect(db); dst = sqlite3.connect(raw)
        with dst: src.backup(dst)
        src.close(); dst.close()
        ok, msg = _check(raw)
        if not ok: sys.exit(f'sauvegarde refusée, copie invalide : {msg}')
        out = os.path.join(a.dir, f'spinsacademy-{stamp}.sqlite.gz')
        with open(raw, 'rb') as f, gzip.open(out + '.part', 'wb') as g: shutil.copyfileobj(f, g)
        os.replace(out + '.part', out)
    digest = hashlib.sha256(open(out, 'rb').read()).hexdigest()
    open(out + '.sha256', 'w').write(f'{digest}  {os.path.basename(out)}\n')
    files = sorted(glob.glob(os.path.join(a.dir, 'spinsacademy-*.sqlite.gz')))
    limit = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=a.keep)
    for f in files[:-a.min] if len(files) > a.min else []:
        when = datetime.datetime.strptime(os.path.basename(f)[13:29], '%Y%m%dT%H%M%SZ').replace(tzinfo=datetime.timezone.utc)
        if when < limit:
            os.remove(f)
            if os.path.exists(f + '.sha256'): os.remove(f + '.sha256')
    print(f'{out} ({os.path.getsize(out) // 1024} Kio) : {msg}')


def verify(a):
    if os.path.exists(a.file + '.sha256'):
        want = open(a.file + '.sha256').read().split()[0]
        if hashlib.sha256(open(a.file, 'rb').read()).hexdigest() != want: sys.exit('empreinte SHA-256 différente : fichier altéré')
    with tempfile.TemporaryDirectory() as tmp:
        ok, msg = _check(_unpack(a.file, tmp))
    print(('OK ' if ok else 'ÉCHEC ') + msg)
    if not ok: sys.exit(1)


def restore(a):
    db = _db(a); verify(a)
    with tempfile.TemporaryDirectory() as tmp:
        src = _unpack(a.file, tmp)
        if os.path.exists(db):
            keep = f"{db}.avant-restauration-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
            shutil.copy2(db, keep); print(f'base actuelle conservée : {keep}')
        for ext in ('-wal', '-shm'):                                # journal WAL de l'ancienne base : à écarter
            if os.path.exists(db + ext): os.remove(db + ext)
        shutil.copyfile(src, db + '.part'); os.replace(db + '.part', db)
    print(f'base restaurée depuis {a.file}')


def listing(a):
    for f in sorted(glob.glob(os.path.join(a.dir, 'spinsacademy-*.sqlite.gz'))):
        print(f'{os.path.basename(f)}  {os.path.getsize(f) // 1024} Kio')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    default_dir = os.environ.get('SPINSACADEMY_BACKUPS', 'sauvegardes')
    b = sub.add_parser('backup'); b.add_argument('--db'); b.add_argument('--dir', default=default_dir)
    b.add_argument('--keep', type=int, default=30); b.add_argument('--min', type=int, default=7)
    v = sub.add_parser('verify'); v.add_argument('file')
    r = sub.add_parser('restore'); r.add_argument('file'); r.add_argument('--db')
    l = sub.add_parser('list'); l.add_argument('--dir', default=default_dir)
    a = ap.parse_args()
    dict(backup=backup, verify=verify, restore=restore, list=listing)[a.cmd](a)

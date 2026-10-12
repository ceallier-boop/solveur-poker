"""Calibration des facteurs de profil à partir de fréquences observées.

Entrée : un tableau de comptages (un joueur ou un groupe de joueurs) :
    groupe, kind ('3w' ou 'hu'), decision, stack (BB), n (occasions), k (fois où le joueur a fait l'action : all-in ou call)
Modèle : k ~ Binomial(n, p),  logit(p) = logit(p_GTO) + beta_type,   type in {shove, call}
Le facteur de cotes du profil est exp(beta) : c'est exactement le facteur utilisé par le moteur exploitant.
p_GTO vient des stratégies HRC (fréquence globale de l'action à ce nœud et ce stack).
"""
import numpy as np
import exploit_engine as ee

# décisions observables de l'adversaire (type d'action, nœud HRC, étiquette)
DECISIONS = {
    ('3w', 'BTN all-in en premier'):           ('shove', '', 'A'),
    ('3w', 'SB all-in (BTN fold)'):            ('shove', '0F', 'A'),
    ('3w', 'SB paie l\'all-in du BTN'):        ('call', '0RA', 'C'),
    ('3w', 'BB paie l\'all-in du BTN (SB fold)'): ('call', '0RA-1F', 'C'),
    ('3w', 'BB paie l\'all-in du SB (BTN fold)'): ('call', '0F-1RA', 'C'),
    ('hu', 'SB all-in'):                       ('shove', '', 'A'),
    ('hu', 'BB paie l\'all-in du SB'):         ('call', '0RA', 'C'),
}
STACKS = (4, 6, 8, 10, 12)


def p_gto(kind, decision, stack):
    typ, key, lab = DECISIONS[(kind, decision)]
    v = ee.action_vec(kind, stack, key, lab)
    vec, mass = v[0], v[1]
    return float((mass * vec).sum() / mass.sum())


def logit(p): return np.log(p / (1 - p))
def expit(z): return 1 / (1 + np.exp(-z))


def fit(rows, slope=False):
    """rows : liste de (type, p0, stack, n, k). Retourne beta par type, erreur-type, et déviance.
    slope=True ajoute une pente sur le stack (beta + gamma*(stack-8)/4) pour chaque type."""
    out = {}
    for typ in ('shove', 'call'):
        r = [x for x in rows if x[0] == typ and x[3] > 0]
        if not r:
            continue
        p0 = np.array([x[1] for x in r]); st = (np.array([x[2] for x in r]) - 8) / 4.0
        n = np.array([x[3] for x in r], float); k = np.array([x[4] for x in r], float)
        X = np.column_stack([np.ones(len(r))] + ([st] if slope else []))
        off = logit(np.clip(p0, 1e-4, 1 - 1e-4))
        th = np.zeros(X.shape[1])
        for _ in range(50):
            p = expit(off + X @ th)
            g = X.T @ (k - n * p)
            H = (X * (n * p * (1 - p))[:, None]).T @ X + 1e-9 * np.eye(X.shape[1])
            step = np.linalg.solve(H, g)
            th = th + np.clip(step, -3, 3)
            if np.abs(step).max() < 1e-8:
                break
        p = expit(off + X @ th)
        H = (X * (n * p * (1 - p))[:, None]).T @ X
        cov = np.linalg.inv(H + 1e-9 * np.eye(X.shape[1]))
        ll = float((k * np.log(np.clip(p, 1e-12, 1)) + (n - k) * np.log(np.clip(1 - p, 1e-12, 1))).sum())
        p00 = expit(off)
        ll0 = float((k * np.log(np.clip(p00, 1e-12, 1)) + (n - k) * np.log(np.clip(1 - p00, 1e-12, 1))).sum())
        out[typ] = dict(beta=th, se=np.sqrt(np.diag(cov)), lr=2 * (ll - ll0), n=float(n.sum()))
    return out


def rows_from_counts(counts):
    """counts : liste de (kind, decision, stack, n, k)"""
    rows = []
    for kind, dec, S, n, k in counts:
        typ = DECISIONS[(kind, dec)][0]
        rows.append((typ, p_gto(kind, dec, S), S, n, k))
    return rows


# ---------- validation sur données synthétiques : on simule des joueurs dont les facteurs sont connus
def simulate_group(rng, ks, kc, mean_n):
    counts = []
    for (kind, dec), (typ, key, lab) in DECISIONS.items():
        for S in STACKS:
            p0 = p_gto(kind, dec, S)
            k_ = ks if typ == 'shove' else kc
            p = expit(logit(p0) + np.log(k_))
            n = rng.poisson(mean_n)
            counts.append((kind, dec, S, n, int(rng.binomial(n, p))))
    return counts


def classify(bs, bc):
    """profil le plus proche dans le plan (log facteur d'all-in, log facteur de call)"""
    best, bd = None, 1e9
    for name, f in ee.PROFILES.items():
        d = (bs - np.log(f['shove'])) ** 2 + (bc - np.log(f['call'])) ** 2
        if d < bd:
            best, bd = name, d
    return best


def validation(mean_ns=(0.5, 1, 2, 5, 10, 20, 50), reps=60, seed=7):
    rng = np.random.default_rng(seed)
    res = []
    for mn in mean_ns:
        err_s = []; err_c = []; cov_s = 0; cov_c = 0; ok = 0; tot = 0; nobs = []
        for pname, f in ee.PROFILES.items():
            for _ in range(reps):
                counts = simulate_group(rng, f['shove'], f['call'], mn)
                fitr = fit(rows_from_counts(counts))
                if 'shove' not in fitr or 'call' not in fitr:
                    continue
                bs, bc = fitr['shove']['beta'][0], fitr['call']['beta'][0]
                ses, sec = fitr['shove']['se'][0], fitr['call']['se'][0]
                ts, tc = np.log(f['shove']), np.log(f['call'])
                err_s.append(bs - ts); err_c.append(bc - tc)
                cov_s += abs(bs - ts) <= 1.96 * ses; cov_c += abs(bc - tc) <= 1.96 * sec
                ok += classify(bs, bc) == pname; tot += 1
                nobs.append(sum(c[3] for c in counts))
        res.append(dict(mean_n=mn, N=float(np.mean(nobs)), rmse_s=float(np.sqrt(np.mean(np.square(err_s)))), rmse_c=float(np.sqrt(np.mean(np.square(err_c)))),
                        cov_s=cov_s / tot, cov_c=cov_c / tot, acc=ok / tot))
    return res


if __name__ == '__main__':
    import json
    res = validation()
    print("occasions par joueur | erreur (log-cotes) all-in / call | couverture IC 95 % | classement correct")
    for r in res:
        print(f"{r['N']:8.0f} | {r['rmse_s']:.2f} / {r['rmse_c']:.2f} | {100*r['cov_s']:.0f} % / {100*r['cov_c']:.0f} % | {100*r['acc']:.0f} %")
    json.dump(res, open('/home/claude/calibration_validation.json', 'w'))

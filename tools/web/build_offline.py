"""Version autonome de l'interface (une seule page HTML, sans serveur) pour une démonstration dans un navigateur.

Les questions et leurs corrections sont calculées ici par spinsacademy.quiz (mêmes énoncés, mêmes corrections que
l'API) sur un échantillon de mains de chaque spot proposable, puis embarquées compressées dans la page. Dans la page,
un petit moteur local remplace les routes de l'API utilisées par l'interface (séries, questions, réponses, bilan,
progression) ; la progression reste dans le navigateur (localStorage). Pas de signalement, pas d'adaptation, pas
d'administration : ce n'est pas l'application de production.
Usage : python tools/web/build_offline.py sortie.html [--hands-gto 3] [--exploit-max 2500]   (A11 : 3,6 Mo, première question en 9 s en 4G ; l'application servie charge question par question)
"""
import argparse, base64, gzip, hashlib, json, os, random, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from spinsacademy import adaptive, field, quiz, ranges, review
from spinsacademy.cards import NAMES, W

WEB = os.path.join(os.path.dirname(__file__), '..', '..', 'spinsacademy', 'web')


def items(gto_ref, k_gto, seed=1, field_ref=None, field_max=None):
    rnd = random.Random(seed); out = []
    if field_ref:                                                  # mode Field : toutes les questions fixes de la banque
        fs = quiz.pool(field_ref)
        if field_max and len(fs) > field_max: fs = sorted(random.Random(seed).sample(fs, field_max), key=lambda s: s['spot_id'])   # démo : un échantillon (taille de la page)
        for sp in fs:
            h = next(iter(sp['hands'])); q = quiz.question(field_ref, sp['spot_id'], h)
            f = sp['field']
            out.append(dict(m='exploit', q=q, eff=sp['effective_stack_bb'], base=None,
                            g=('read' if f['type'] in field.READ else sp['field_family']), a=f['correct'], w=max(f['weight'], 1e-3),
                            rd=f['type'] in field.READ, tr=f['type'] in ('piège', 'échantillon'),
                            c={o['id']: slim(quiz.correct(field_ref, sp['spot_id'], h, o['id'])) for o in q['options']}))
    weights = quiz.situation_weights(gto_ref)
    for ref, k in ((gto_ref, k_gto),):
        for sp in quiz.pool(ref):
            key = (sp['table'], quiz.stack_band(sp), quiz.situation_key(sp))
            hands = list(quiz.teachable(sp))                       # mêmes mains que l'application (bruit HRC, EV impossibles exclus)
            picked = sorted(set(rnd.choices(hands, [W[NAMES.index(h)] * sp['hands'][h]['reach'] ** 0.5 for h in hands], k=k)))
            for h in picked:
                q = quiz.question(ref, sp['spot_id'], h)
                out.append(dict(m=quiz.mode_of(ref), q=q, eff=sp['effective_stack_bb'], base=sp.get('base_spot_id'),
                                b=key[1], g=json.dumps(key[2]), w=weights.get(key, quiz.RARE_FLOOR),
                                c={o['id']: slim(quiz.correct(ref, sp['spot_id'], h, o['id'])) for o in q['options']}))
    return out


SLIM = ('explanation_fr', 'core_fr', 'why_fr')       # la page affiche essential_fr, remember_fr et details_fr : le reste alourdirait la démo


def slim(c): return {k: v for k, v in c.items() if k not in SLIM}


RANGE_TASKS = 240          # exercices « Construis ta range » embarqués dans la démo (tirés selon la fréquence des situations)


def range_tasks(ref, n=RANGE_TASKS, seed=5):
    rnd = random.Random(seed); weights = quiz.situation_weights(ref); ok = ranges.drawable(ref)
    spots = [sp for sp in quiz.pool(ref) if sp['spot_id'] in ok]
    rnd.shuffle(spots)
    spots.sort(key=lambda sp: -rnd.random() * weights.get((sp['table'], quiz.stack_band(sp), quiz.situation_key(sp)), quiz.RARE_FLOOR))
    out = []
    for sp in spots:
        t = ranges.task(sp)
        if t: out.append(t)
        if len(out) >= n: break
    return out


def theme_css(css):
    """thème de l'hôte : prefers-color-scheme sans choix explicite, data-theme sinon ; barre collante sous l'encoche"""
    m = re.search(r'@media \(prefers-color-scheme: dark\) \{\s*:root \{(.*?)\}\s*\}', css, re.S)
    if not m: raise SystemExit('bloc sombre introuvable dans app.css')
    dark = m.group(1).strip()
    css = css.replace(m.group(0), '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { ' + dark + ' color-scheme: dark; } }\n'
                      ':root[data-theme="dark"] { ' + dark + ' color-scheme: dark; }')
    return css.replace('.bar { position: sticky; top: 0;', '.bar { position: sticky; top: env(safe-area-inset-top, 0px);')


SHIM = r"""
// ---------------------------------------------------------------- moteur local (remplace l'API dans la version autonome)
const DEMO = (() => {
  let ITEMS = null; let GRIDS = {}; let RTASKS = [];
  const ready = (async () => {
    const bin = Uint8Array.from(atob(document.getElementById('demo-data').textContent.trim()), (c) => c.charCodeAt(0));
    const txt = await new Response(new Blob([bin]).stream().pipeThrough(new DecompressionStream('gzip'))).text();
    const d = JSON.parse(txt); ITEMS = d.items; GRIDS = d.grids; RTASKS = d.ranges || [];
  })();
  const KEY = 'spinsacademy_demo_v1';
  let mem = null;
  function load() { if (mem) return mem; try { mem = JSON.parse(localStorage.getItem(KEY)) || null; } catch (e) { mem = null; } return (mem = mem || { sessions: {} }); }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(mem)); } catch (e) { /* stockage indisponible : la série reste en mémoire */ } }
  const now = () => new Date().toISOString().slice(0, 19) + '+00:00';
  const FAMILY_FR = { first_in: 'Premier à parler', vs_limp: 'Face à un limp', vs_raise: 'Face à une relance', vs_allin: 'Face à un tapis', read: 'Lecture du vilain' };
  const TABLE_FR = { '3-handed': '3 joueurs', 'heads-up': 'Heads-up' }; const MODE_FR = { gto: 'GTO', exploit: 'Exploitant' };
  const DEPTHS = [['lt10', 'Moins de 10 BB', 0, 9.5], ['10_16', '10 à 16 BB', 9.5, 16.5], ['17_25', '17 à 25 BB', 16.5, 99]];
  const depthOf = (s) => (DEPTHS.find(([, , lo, hi]) => s >= lo && s < hi) || DEPTHS[2])[0];
  const MIN_SAMPLE = 10;
  const rnd = (a) => a[Math.floor(Math.random() * a.length)];

  // mêmes règles que l'application : GTO = quiz.draw_series (format HU_SHARE, tranche de tapis à parts égales, situation selon
  // sa fréquence réelle) ; exploitant = field.draw (famille selon FAMILY_SHARE, tapis puis bonne réponse à parts égales, profil
  // pondéré par sa part dans le field). Une main ne revient pas dans la série.
  const HU_SHARE = __HU_SHARE__, EASY_SHARE = __EASY_SHARE__, FAMILY_SHARE = __FAMILY_SHARE__, MAX_TRAPS = __MAX_TRAPS__, MAX_READ = __MAX_READ__;
  const wpick = (xs, w) => { let t = xs.reduce((a, x) => a + w(x), 0) * Math.random(); for (const x of xs) { t -= w(x); if (t <= 0) return x; } return xs[xs.length - 1]; };
  const uniq = (xs) => [...new Set(xs)];
  function draw(mode, f, size) {
    const pool = ITEMS.map((it, i) => [it, i]).filter(([it]) => it.m === mode
      && (!f.table || it.q.table === f.table) && (!f.hero || it.q.hero === f.hero) && (!f.family || (it.g === 'read' ? 'read' : it.q.family) === f.family)
      && (f.min_stack == null || it.eff >= f.min_stack) && (f.max_stack == null || it.eff <= f.max_stack)).map(([, i]) => i);
    if (uniq(pool.map((i) => ITEMS[i].q.spot_id)).length < size) return null;
    const used = new Set(), seen = new Set(), out = []; let traps = 0, reads = 0;
    const maxRead = pool.some((i) => !ITEMS[i].rd) ? MAX_READ : size, maxTraps = pool.some((i) => !ITEMS[i].tr) ? MAX_TRAPS : size;
    while (out.length < size) {
      const tables = uniq(pool.map((i) => ITEMS[i].q.table));
      const want = tables.length === 2 ? (Math.random() < HU_SHARE ? 'heads-up' : '3-handed') : tables[0];
      let cand = [];
      for (const t of [want, ...tables.filter((x) => x !== want)]) {
        cand = pool.filter((i) => { const it = ITEMS[i]; return it.q.table === t && !used.has(it.q.spot_id) && !(it.q.hand && seen.has(it.q.hand))
          && !(mode === 'exploit' && ((it.tr && traps >= maxTraps) || (it.rd && reads >= maxRead))); });
        if (cand.length) break;
      }
      if (!cand.length) break;
      let i;
      if (mode === 'exploit') {
        const fam = wpick(uniq(cand.map((x) => ITEMS[x].g)).sort(), (g) => FAMILY_SHARE[g] || 0.1); cand = cand.filter((x) => ITEMS[x].g === fam);
        if (fam === 'read') {                                       // « Quelle pastille ? » autant que « Défaut du vilain », sur les deux tables
          cand = pool.filter((x) => ITEMS[x].rd && !used.has(ITEMS[x].q.spot_id));
          const ty = rnd(uniq(cand.map((x) => ITEMS[x].q.field.type)).sort()); cand = cand.filter((x) => ITEMS[x].q.field.type === ty);
        }
        const st = rnd(uniq(cand.map((x) => ITEMS[x].eff))); cand = cand.filter((x) => ITEMS[x].eff === st);
        const a = rnd(uniq(cand.map((x) => ITEMS[x].a))); cand = cand.filter((x) => ITEMS[x].a === a);
        i = wpick(cand, (x) => ITEMS[x].w); traps += ITEMS[i].tr ? 1 : 0; reads += ITEMS[i].rd ? 1 : 0;
      } else {
        const band = rnd(uniq(cand.map((x) => ITEMS[x].b))); cand = cand.filter((x) => ITEMS[x].b === band);
        const g = wpick(uniq(cand.map((x) => ITEMS[x].g)).sort(), (k) => ITEMS[cand.find((x) => ITEMS[x].g === k)].w); cand = cand.filter((x) => ITEMS[x].g === g);
        const sid = rnd(uniq(cand.map((x) => ITEMS[x].q.spot_id))); cand = cand.filter((x) => ITEMS[x].q.spot_id === sid);
        const easy = cand.filter((x) => ITEMS[x].q.difficulty === 'facile'), rest = cand.filter((x) => ITEMS[x].q.difficulty !== 'facile');
        i = rnd(easy.length && (!rest.length || Math.random() < EASY_SHARE) ? easy : rest);
      }
      used.add(ITEMS[i].q.spot_id); if (ITEMS[i].q.hand) seen.add(ITEMS[i].q.hand); out.push(i);
    }
    return out.length === size ? out : null;
  }

  // une série garde des numéros de questions, valables seulement pour la démo qui l'a créée (BUILD) : après une reconstruction,
  // ses réponses comptent encore dans le score, et par thème si elles portent leur description (meta, depuis le 24/10/2026)
  const BUILD = '__BUILD__';
  const own = (s) => s.build === BUILD;
  const metaOf = (it) => ({ m: it.m, eff: it.eff, family: it.q.family, hero: it.q.hero, table: it.q.table, prompt_fr: it.q.prompt_fr });
  const fromMeta = (x) => ({ m: x.m, eff: x.eff, q: { family: x.family, hero: x.hero, table: x.table, prompt_fr: x.prompt_fr } });
  function answered(s) {
    return s.items.map((i, k) => { const r = s.answers[k]; return [r && r.meta ? fromMeta(r.meta) : own(s) ? ITEMS[i] || null : null, r]; }).filter(([, r]) => r);
  }

  function summary(s) {
    const rows = answered(s); const n = rows.length; const pts = rows.reduce((a, [, r]) => a + r.points, 0);
    const errors = rows.filter(([, r]) => r.verdict !== 'correct').map(([it, r]) => ({ prompt_fr: it ? it.q.prompt_fr.replace(' Que fais-tu ?', '') : 'Question d\'une version précédente de la démo',
      chosen: r.chosen_label, best: r.best_label, regret_mbb: r.regret_mbb })).sort((a, b) => b.regret_mbb - a.regret_mbb);
    const verdicts = { correct: 0, 'imprécision': 0, erreur: 0 }; for (const [, r] of rows) verdicts[r.verdict] += 1;
    const ev = rows.filter(([, r]) => !(r.field && r.field.read)); const lost = ev.reduce((a, [, r]) => a + (r.regret_mbb || 0), 0) / 1000;
    return { questions: n, points: pts, score_pct: n ? Math.round(1000 * pts / n) / 10 : 0, bb_lost: Math.round(100 * lost) / 100, ev_questions: ev.length, verdicts, errors, review: errors.slice(0, 3).map((e) => e.prompt_fr),
      session_id: s.id, size: s.items.length, complete: n === s.items.length };
  }

  function stats() {
    const bucket = () => ({ questions: 0, points: 0, errors: 0, evq: 0, regret: 0 });
    const addEv = (b, r) => { if (!(r.field && r.field.read)) { b.evq += 1; b.regret += r.regret_mbb || 0; } };   // BB perdus : sans la lecture du vilain
    const per100 = (b) => (b.evq ? Math.round(b.regret / 1000 * 100 / b.evq * 100) / 100 : null);
    const total = bucket(); const verdicts = { correct: 0, 'imprécision': 0, erreur: 0 };
    const dims = { mode: {}, family: {}, hero: {}, table: {}, depth: {} }; const sessions = []; const themes = {}; let untracked = 0;
    const sess = Object.values(load().sessions).sort((a, b) => a.created_at.localeCompare(b.created_at));
    for (const s of sess) {
      const rows = answered(s); if (!rows.length) continue;
      let sp = 0; const sb = bucket();
      for (const [it, r] of rows) {
        addEv(sb, r);
        if (!it) {                                                    // version précédente, sans description : score seulement
          untracked += 1; total.questions += 1; total.points += r.points; total.errors += r.verdict === 'erreur'; verdicts[r.verdict] += 1; sp += r.points; addEv(total, r); continue;
        }
        const keys = { mode: it.m, family: it.q.family, hero: it.q.hero, table: it.q.table, depth: depthOf(it.eff) };
        const err = r.verdict === 'erreur';
        for (const b of [total, ...Object.entries(keys).map(([d, k]) => (dims[d][k] = dims[d][k] || bucket()))]) { b.questions += 1; b.points += r.points; b.errors += err; addEv(b, r); }
        verdicts[r.verdict] += 1; sp += r.points;
        const tk = [it.m, it.q.family, it.q.hero, keys.depth].join('|');
        const t = (themes[tk] = themes[tk] || { errors: 0, imprecisions: 0, questions: 0, regret: 0, examples: [] }); t.questions += 1; t.imprecisions += r.verdict === 'imprécision';
        if (err) { t.errors += 1; t.regret += r.regret_mbb; if (t.examples.length < 2) t.examples.push(it.q.prompt_fr); }
      }
      sessions.push({ session_id: s.id, date: s.created_at, questions: rows.length, score_pct: Math.round(1000 * sp / rows.length) / 10, bb_per_100: per100(sb) });
    }
    const close = (b, label, filters) => ({ label, questions: b.questions, score_pct: b.questions ? Math.round(1000 * b.points / b.questions) / 10 : null,
      errors: b.errors, reliable: b.questions >= MIN_SAMPLE, filters, bb_per_100: per100(b) });
    const df = Object.fromEntries(DEPTHS.map(([k, , lo, hi]) => [k, { min_stack: lo, max_stack: hi }]));
    const by = {
      mode: Object.keys(MODE_FR).filter((k) => dims.mode[k]).map((k) => close(dims.mode[k], MODE_FR[k], { mode: k })),
      family: Object.keys(FAMILY_FR).filter((k) => dims.family[k]).map((k) => close(dims.family[k], FAMILY_FR[k], { family: k })),
      hero: ['BTN', 'SB', 'BB'].filter((k) => dims.hero[k]).map((k) => close(dims.hero[k], k, { hero: k })),
      table: Object.keys(TABLE_FR).filter((k) => dims.table[k]).map((k) => close(dims.table[k], TABLE_FR[k], { table: k })),
      depth: DEPTHS.filter(([k]) => dims.depth[k]).map(([k, l]) => close(dims.depth[k], l, df[k])) };
    const reliable = Object.values(by).flat().filter((x) => x.reliable);
    const weakest = reliable.length ? reliable.reduce((a, b) => (b.score_pct < a.score_pct ? b : a)) : null;
    const dl = Object.fromEntries(DEPTHS.map(([k, l]) => [k, l]));
    const recurring = Object.entries(themes).filter(([, t]) => t.errors >= 2).map(([k, t]) => {
      const [m, f, h, d] = k.split('|');
      return { label: `${MODE_FR[m]} · ${FAMILY_FR[f]} · ${h} · ${dl[d]}`, errors: t.errors, questions: t.questions, regret_mbb: Math.round(t.regret),
        examples: t.examples, filters: Object.assign({ mode: m, hero: h }, df[d], { family: f }) };
    }).sort((a, b) => b.errors - a.errors || b.regret_mbb - a.regret_mbb).slice(0, 3);
    const n = total.questions;
    // un seul diagnostic, même règle que progress.focus et les séries adaptées (taux lissé, 3 réponses et 2 erreurs au moins)
    const smooth = (t) => (t.errors + 0.5 * t.imprecisions + 1) / (t.questions + 3);
    const cand = Object.entries(themes).filter(([, t]) => t.questions >= __MIN_ANSWERS__ && t.errors >= __MIN_ERRORS__)
      .sort((a, b) => smooth(b[1]) - smooth(a[1]) || b[1].errors - a[1].errors);
    let focus;
    if (cand.length) {
      const [k, t] = cand[0]; const [m, f, h, d] = k.split('|'); const weak = smooth(t) >= __WEAK_RATE__;
      focus = { kind: weak ? 'weak' : 'watch', label: `${MODE_FR[m]} · ${FAMILY_FR[f]} · ${h} · ${dl[d]}`, examples: t.examples.slice(0, 1),
        reason_fr: `${t.errors} erreurs sur ${t.questions} questions (taux lissé ${Math.round(100 * smooth(t))} %) : `
          + (weak ? "c'est ton thème le plus fragile." : 'à surveiller, sans être encore un point faible.'),
        filters: Object.assign({ mode: m, hero: h }, df[d], { family: f }) };
    } else if (weakest) {
      focus = { kind: 'dimension', label: weakest.label, filters: weakest.filters, examples: [],
        reason_fr: `Ton score le plus bas : ${String(weakest.score_pct).replace('.', ',')} % sur ${weakest.questions} questions.` };
    } else {
      const need = Math.max(MIN_SAMPLE - n, 0);
      focus = { kind: 'none', label: null, filters: null, examples: [], reason_fr: need
        ? `Pas encore assez de réponses pour un diagnostic : encore ${need} question${need > 1 ? 's' : ''}.` : "Rien à retravailler pour l'instant : continue avec des séries rapides." };
    }
    return { sessions: sessions.length, questions: n, points: Math.round(10 * total.points) / 10, score_pct: n ? Math.round(1000 * total.points / n) / 10 : null, bb_per_100: per100(total),
      verdicts, min_sample: MIN_SAMPLE, by, untracked_questions: untracked, evolution: sessions.slice(-20), recurring_errors: recurring, weakest, focus };
  }

  // signalements : base de données partagée de l'artefact (lue par le porteur du projet), un document par signalement
  let dbp = null;
  async function report(body) {
    const s = load().sessions[body.session_id]; if (!s || !own(s)) return [404, { detail: 'session inconnue' }];
    const k = body.question_index, ans = s.answers[k]; const it = ITEMS[s.items[k]];
    if (!it || !ans) return [409, { detail: "réponds d'abord à la question" }];
    if ((s.reported || {})[k]) return [409, { detail: 'question déjà signalée' }];
    dbp = dbp || (async () => {
      const c = window.claude && window.claude.use; if (!c) return null;
      const [db, user] = await Promise.all([c('db'), c('user')]);
      const uid = user ? await user.id() : null;
      return db && uid ? { db, uid } : null;
    })();
    const x = await dbp;
    if (!x) return [503, { detail: 'Signalement indisponible ici : ouvre la démo connecté à claude.ai, avec un accès qui permet de contribuer.' }];
    const rid = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    try {
      await x.db.doc(`reports/${x.uid}/items/${rid}`).set({ created_at: now(), mode: s.mode, spot_id: it.q.spot_id, hand: it.q.hand,
        action_id: ans.action_id, chosen: ans.chosen_label, reference: ans.best_label, verdict: ans.verdict, reason: body.reason,
        comment: (body.comment || '').slice(0, 1000), prompt: it.q.prompt_fr, dataset: DATASETS[s.mode], status: 'open' });
    } catch (e) {
      return [503, { detail: e && e.code === 'permission_denied' ? "Ton accès à cette page ne permet pas d'envoyer de signalement : demande un accès « contributeur »." : "Le signalement n'a pas pu être envoyé, réessaie." }];
    }
    (s.reported = s.reported || {})[k] = true; save();
    return [201, { report_id: rid, status: 'open' }];
  }

  // révision espacée, même règle que l'application (spinsacademy/review.py) : 1 jour, puis 3, puis 7 ; une erreur fait repartir à 1 jour
  const DAY = 864e5, INTERVALS = __INTERVALS__;
  function reviewItems(mode) {
    const st = {}; const ev = [];
    for (const s of Object.values(load().sessions)) if (s.mode === mode && own(s)) s.items.forEach((i, k) => { const a = s.answers[k]; if (a && a.at) ev.push([a.at, i, a.verdict]); });
    ev.sort((a, b) => (a[0] < b[0] ? -1 : 1));
    for (const [at, i, v] of ev) {
      const t = Date.parse(at);
      if (v !== 'correct') st[i] = { stage: 0, since: t, miss: t };
      else if (st[i] && st[i].stage < INTERVALS.length && t >= st[i].since + INTERVALS[st[i].stage] * DAY) { st[i].stage += 1; st[i].since = t; }
    }
    return Object.entries(st).filter(([, x]) => x.stage < INTERVALS.length)
      .map(([i, x]) => ({ i: Number(i), stage: x.stage + 1, miss: x.miss, due_at: x.since + INTERVALS[x.stage] * DAY })).sort((a, b) => a.due_at - b.due_at);
  }
  function reviews(mode) {
    const it = reviewItems(mode), t = Date.now(), due = it.filter((x) => x.due_at <= t), later = it.filter((x) => x.due_at > t);
    return { rule_fr: __REVIEW_RULE__, due: due.length, pending: later.length, next_due_at: later.length ? new Date(later[0].due_at).toISOString() : null, mode };
  }

  // « Construis ta range » : même règle que spinsacademy.ranges.grade
  function rangeGrade(t, selected) {
    const sel = new Set(selected); const cells = {}; let wt = 0, good = 0, lost = 0, refw = 0, myw = 0; const extra = [], missing = [];
    for (const [h, [f, cin, cout, w]] of Object.entries(t.hands)) {
      const played = sel.has(h), ref = f >= 0.75 ? 'in' : f <= 0.25 ? 'out' : 'mixed'; const cost = played ? cin : cout; let st, ok;
      if (ref === 'mixed') { st = 'mixed'; ok = true; } else if (ref === 'in') { st = played ? 'ok_in' : 'missing'; ok = played; } else { st = played ? 'extra' : 'ok_out'; ok = !played; }
      cells[h] = st; wt += w; good += ok ? w : 0; lost += w * cost; refw += w * f; if (played) myw += w;
      if (st === 'extra') extra.push([cost, h]); if (st === 'missing') missing.push([cost, h]);
    }
    const worst = extra.concat(missing).sort((a, b) => b[0] - a[0] || (a[1] < b[1] ? 1 : -1)).slice(0, 5);
    return { spot_id: t.spot_id, cells, accuracy_pct: wt ? Math.round(1000 * good / wt) / 10 : 0, bb_per_100: wt ? Math.round(10000 * lost / wt) / 100 : 0,
      extra: extra.length, missing: missing.length, worst: worst.map(([c, h]) => ({ hand: h, cost_bb: Math.round(100 * c) / 100, kind: cells[h] })),
      ref_share_pct: wt ? Math.round(100 * refw / wt) : 0, my_share_pct: wt ? Math.round(100 * myw / wt) : 0, rule_fr: t.rule_fr,
      reference: Object.fromEntries(Object.entries(t.hands).map(([h, x]) => [h, x[0]])), situation_fr: t.situation_fr, question_fr: t.question_fr };
  }

  async function route(path, opts) {
    await ready;
    const url = new URL(path, 'https://demo.local/'); const p = url.pathname; const method = (opts && opts.method) || 'GET';
    const body = opts && opts.body ? JSON.parse(opts.body) : {};
    const db = load();
    if (p === '/sessions' && method === 'POST') {
      const f = Object.assign({}, body.filters || {}); const mode = f.mode || body.mode || 'gto'; delete f.mode;
      const size = body.size || 5; let picked = draw(mode, f, size); const purposes = {};
      if (body.review) {
        const due = reviewItems(mode).filter((x) => x.due_at <= Date.now()).slice(0, size);
        const rest = (picked || []).filter((i) => !due.some((x) => x.i === i));
        due.forEach((x, k) => { purposes[k] = `Révision de ton erreur du ${new Date(x.miss).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })} (étape ${x.stage} sur ${INTERVALS.length})`; });
        picked = due.map((x) => x.i).concat(rest).slice(0, size);
      }
      if (!picked || !picked.length) return [422, { detail: 'pas assez de situations pour ces filtres' }];
      const id = Math.random().toString(16).slice(2) + Date.now().toString(16);
      db.sessions[id] = { id, build: BUILD, created_at: now(), mode, items: picked, answers: {}, purposes }; save();
      return [201, { session_id: id, mode, size: picked.length, adaptive: null }];
    }
    const sm = p.match(/^\/sessions\/([^/]+)\/summary$/);
    if (sm) { const s = db.sessions[decodeURIComponent(sm[1])]; return s && own(s) ? [200, summary(s)] : [404, { detail: 'session inconnue' }]; }
    if (p === '/quiz/next') {
      const s = db.sessions[url.searchParams.get('session_id')]; if (!s || !own(s)) return [404, { detail: 'session inconnue' }];
      const k = s.items.findIndex((_, i) => !s.answers[i]);
      if (k < 0) return [200, { done: true, session_id: s.id }];
      return [200, { done: false, session_id: s.id, question_index: k, size: s.items.length, question: ITEMS[s.items[k]].q,
        purpose: (s.purposes || {})[k] ? 'spaced' : null, purpose_fr: (s.purposes || {})[k] || null }];
    }
    if (p === '/attempts' && method === 'POST') {
      const s = db.sessions[body.session_id]; if (!s || !own(s)) return [404, { detail: 'session inconnue' }];
      const it = ITEMS[s.items[body.question_index]]; if (!it) return [404, { detail: 'question inconnue' }];
      const prev = s.answers[body.question_index];
      if (prev) return prev.action_id === body.action_id ? [200, Object.assign({}, prev, { range: GRIDS[it.q.spot_id] || null, already_answered: true })] : [409, { detail: 'question déjà répondue' }];
      const r0 = it.c[body.action_id]; if (!r0) return [422, { detail: 'action non proposée' }];
      const r = Object.assign({}, r0, { range: GRIDS[it.q.spot_id] || null });
      s.answers[body.question_index] = Object.assign({ action_id: body.action_id, at: now(), meta: metaOf(it) }, r0); save();       // sans la grille : stockage léger
      return [200, Object.assign({}, r, { already_answered: false })];
    }
    if (p === '/reports' && method === 'POST') return report(body);
    if (p === '/ranges/next') {
      const q = url.searchParams, lo = Number(q.get('min_stack') || 0), hi = Number(q.get('max_stack') || 999);
      const c = RTASKS.filter((t) => (!q.get('table') || t.table === q.get('table')) && (!q.get('hero') || t.hero === q.get('hero'))
        && (!q.get('family') || t.family === q.get('family')) && t.effective_stack_bb >= lo && t.effective_stack_bb <= hi);
      if (!c.length) return [422, { detail: 'pas de situation à dessiner pour ces filtres' }];
      const t = rnd(c); const { hands, rule_fr, ...rest } = t; return [200, Object.assign(rest, { hands: Object.keys(hands).sort() })];
    }
    if (p === '/ranges/answer' && method === 'POST') {
      const t = RTASKS.find((x) => x.spot_id === body.spot_id); if (!t) return [404, { detail: 'situation inconnue' }];
      const g = rangeGrade(t, (body.hands || []).filter((h) => h in t.hands));
      db.ranges = (db.ranges || []).concat([{ spot_id: t.spot_id, accuracy_pct: g.accuracy_pct, bb_per_100: g.bb_per_100, at: now() }]); save();
      return [200, g];
    }
    if (p === '/users/me/stats') {
      const s = stats(), rs = (load().ranges || []).slice(-20);
      s.ranges = rs.length ? { count: (load().ranges || []).length, recent: rs.length, accuracy_pct: Math.round(10 * rs.reduce((a, r) => a + r.accuracy_pct, 0) / rs.length) / 10,
        bb_per_100: Math.round(100 * rs.reduce((a, r) => a + r.bb_per_100, 0) / rs.length) / 100 } : { count: 0 };
      return [200, s];
    }
    if (p === '/users/me/export') return [200, { exported_at: now(), note_fr: 'Version de démonstration : données gardées dans ce navigateur.', sessions: load().sessions }];
    if (p === '/users/me/reviews') return [200, reviews(url.searchParams.get('mode') || 'gto')];
    if (p === '/users/me' && method === 'DELETE') { mem = { sessions: {} }; save(); return [204, null]; }
    return [404, { detail: 'indisponible dans la version de démonstration' }];
  }
  window.fetch = async (path, opts) => {
    const [status, data] = await route(String(path), opts);
    return new Response(status === 204 ? null : JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
  };
  // la page hébergée n'affiche pas les boîtes de dialogue du navigateur : message dans l'écran (filet de sécurité)
  window.alert = (msg) => { const t = document.getElementById('demo-toast'); t.textContent = msg; t.hidden = false; setTimeout(() => { t.hidden = true; }, 5000); };
  return { ready };
})();
"""

EXTRA_CSS = """
#st-export { display: none; }   /* l'hôte de la démo n'autorise pas les téléchargements : export réservé à l'application */
.demo-note { margin: 0; font-size: .85rem; color: var(--muted); background: var(--surface); border: 1px dashed var(--line); border-radius: 10px; padding: 8px 12px; }
#demo-toast { position: fixed; left: 16px; right: 16px; bottom: calc(16px + env(safe-area-inset-bottom, 0px)); z-index: 5; background: var(--text); color: var(--bg);
  padding: 12px 14px; border-radius: 12px; font-size: .92rem; }
"""


def build(out, k_gto, exploit_max=2500):
    html = open(os.path.join(WEB, 'index.html')).read(); css = open(os.path.join(WEB, 'app.css')).read(); js = open(os.path.join(WEB, 'app.js')).read()
    data = items(quiz.DEFAULT_VERSION, k_gto, field_ref=quiz.DEFAULT_FIELD, field_max=exploit_max)
    grids = {}                                                    # grille de stratégie : une par spot, pas une par réponse
    for it in data:
        for r in it['c'].values(): grids[it['q']['spot_id']] = r.pop('range', None)
    build_id = hashlib.sha256(json.dumps([(it['q']['spot_id'], it['q']['hand'], it['m']) for it in data]).encode()).hexdigest()[:12]   # ordre des questions
    rtasks = range_tasks(quiz.DEFAULT_VERSION)
    blob = base64.b64encode(gzip.compress(json.dumps(dict(items=data, grids=grids, ranges=rtasks), ensure_ascii=False, separators=(',', ':')).encode(), 9)).decode()
    body = re.search(r'<body>(.*)</body>', html, re.S).group(1)
    body = re.sub(r'<script[^>]*></script>', '', body)
    gto, fld = (quiz.load(r)[0]['version'] for r in (quiz.DEFAULT_VERSION, quiz.DEFAULT_FIELD))
    note = (f'<p class="demo-note">Version de démonstration : {len(data)} questions : datasets {gto} (GTO) et {fld} (exploitant). '
            'Ta progression reste dans ce navigateur ; tes signalements sont transmis au porteur du projet. Adaptation et administration sont réservées à l\'application complète.</p>')
    body = body.replace('<section id="screen-home" class="screen" aria-labelledby="home-title">',
                        '<section id="screen-home" class="screen" aria-labelledby="home-title">\n      ' + note, 1)
    for hide in ('id="st-delete"',):                               # pas d'effacement sans confirmation possible
        body = body.replace(hide, hide + ' hidden', 1)
    body = body.replace('<h3>Exercices adaptatifs</h3>', '<h3 hidden>Exercices adaptatifs</h3>', 1)
    body = body.replace('id="quick-start">Série recommandée<', 'id="quick-start">Série rapide<', 1)
    page = (f'<meta charset="utf-8">\n<title>SpinsAcademy</title>\n<meta name="theme-color" content="#0f3d2e">\n<style>\n{theme_css(css)}\n{EXTRA_CSS}</style>\n'
            f'{body}\n<div id="demo-toast" role="status" hidden></div>\n<script type="application/octet-stream" id="demo-data">{blob}</script>\n'
            f'<script>window.SA_LEXIQUE = {open(os.path.join(WEB, "lexique.json")).read()};</script>\n'
            f'<script>const DATASETS = {json.dumps(dict(gto=gto, exploit=fld))};</script>\n'
            f'<script>\n{SHIM.replace("__HU_SHARE__", str(quiz.HU_SHARE)).replace("__FAMILY_SHARE__", json.dumps(field.FAMILY_SHARE)).replace("__MAX_TRAPS__", str(field.MAX_TRAPS)).replace("__MAX_READ__", str(field.MAX_READ)).replace("__EASY_SHARE__", str(quiz.EASY_SHARE)).replace("__MIN_ANSWERS__", str(adaptive.MIN_ANSWERS)).replace("__MIN_ERRORS__", str(adaptive.MIN_ERRORS)).replace("__WEAK_RATE__", str(adaptive.WEAK_RATE)).replace("__INTERVALS__", json.dumps(list(review.INTERVALS_DAYS))).replace("__BUILD__", build_id).replace("__REVIEW_RULE__", json.dumps(review.RULE_FR, ensure_ascii=False))}\nDEMO.ready.then(() => {{\n{js}\n}});\n</script>\n')
    open(out, 'w').write(page)
    return len(data), len(page)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--hands-gto', type=int, default=3); ap.add_argument('--exploit-max', type=int, default=2500)
    a = ap.parse_args(); n, size = build(a.out, a.hands_gto, a.exploit_max)
    print(f'{a.out} : {n} questions, {size // 1024} Kio')

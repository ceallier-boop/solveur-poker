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
from spinsacademy import adaptive, challenges, field, goals, levels, quiz, ranges, review, today
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
    per = {}                                                       # même nombre d'exercices par famille et tranche de tapis
    for sp in spots: per.setdefault((quiz.family(sp), quiz.stack_band(sp)), []).append(sp)
    out = []; quota = max(1, n // max(1, len(per)))
    for group in per.values():
        k = 0
        for sp in group:
            t = ranges.task(sp)
            if t: out.append(t); k += 1
            if k >= quota: break
    return out[:n]


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
      chosen: r.chosen_label, best: r.best_label, regret_mbb: r.regret_mbb, verdict: r.verdict, timed_out: !!r.timed_out })).sort((a, b) => b.regret_mbb - a.regret_mbb);
    const verdicts = { correct: 0, 'imprécision': 0, erreur: 0 }; for (const [, r] of rows) verdicts[r.verdict] += 1;
    const ev = rows.filter(([, r]) => !(r.field && r.field.read)); const lost = ev.reduce((a, [, r]) => a + Math.round((r.regret_mbb || 0) / 10) / 100, 0);   // somme des coûts affichés
    return { questions: n, points: pts, score_pct: n ? Math.round(1000 * pts / n) / 10 : 0, bb_lost: Math.round(100 * lost) / 100, ev_questions: ev.length,
      bb_per_100: ev.length ? Math.round(10000 * lost / ev.length) / 100 : null, timeouts: rows.filter(([, r]) => r.timed_out).length, verdicts, errors, review: errors.slice(0, 3).map((e) => e.prompt_fr),
      session_id: s.id, size: s.items.length, complete: n === s.items.length };
  }

  function stats() {
    const bucket = () => ({ questions: 0, points: 0, errors: 0, evq: 0, regret: 0 });
    const addEv = (b, r) => { if (!(r.field && r.field.read)) { b.evq += 1; b.regret += 10 * Math.round((r.regret_mbb || 0) / 10); } };   // BB perdus : sans la lecture du vilain
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
      const DIMN = { family: 'Situation', hero: 'Position', table: 'Format', depth: 'Profondeur' };
      const near = Object.entries(by).filter(([k]) => k !== 'mode').flatMap(([k, v]) => v.map((x) => ({ ...x, label: `${DIMN[k]} : ${x.label}` }))).filter((x) => !x.reliable).sort((x, y) => y.questions - x.questions)[0];
      if (!need && near) focus = { kind: 'none', label: near.label, filters: near.filters, examples: [],
        reason_fr: `Pas encore de diagnostic : un thème compte à partir de ${MIN_SAMPLE} questions. Le plus avancé : ${near.questions} sur ${MIN_SAMPLE}. Joue-le pour un premier diagnostic.` };
      else focus = { kind: 'none', label: null, filters: null, examples: [], reason_fr: need
        ? `Pas encore assez de réponses pour un diagnostic : encore ${need} question${need > 1 ? 's' : ''}.` : "Rien à retravailler pour l'instant : continue avec des séries rapides." };
    }
    return { sessions: sessions.length, questions: n, points: Math.round(10 * total.points) / 10, score_pct: n ? Math.round(1000 * total.points / n) / 10 : null, bb_per_100: per100(total),
      ev_questions: total.evq, timeouts: sess.reduce((a, s) => a + answered(s).filter(([, r]) => r.timed_out).length, 0),
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
    const it = reviewItems(mode), td = dayBack(0), due = it.filter((x) => dayOf(new Date(x.due_at).toISOString()) <= td), later = it.filter((x) => dayOf(new Date(x.due_at).toISOString()) > td);   // en jours du joueur
    return { rule_fr: __REVIEW_RULE__, due: due.length, pending: later.length, next_due_at: later.length ? new Date(later[0].due_at).toISOString() : null, mode };
  }

  // séance du jour : même règle que spinsacademy.today (jour local du navigateur)
  const THEMES = __THEMES__;
  const pad = (x) => String(x).padStart(2, '0');
  const dayOf = (iso) => { const d = new Date(iso); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`; };
  const dayBack = (k) => dayOf(new Date(Date.now() - k * DAY).toISOString());
  function streak(days, ref) {                                     // un jour manqué par période de 7 jours est pardonné ; ref : jour de référence
    let n = 0, miss = null; const oldest = [...days].sort()[0], base = ref ? Date.parse(ref + 'T12:00:00') : Date.now();
    const back = (k) => dayOf(new Date(base - k * DAY).toISOString());
    for (let k = days.has(back(0)) ? 0 : 1; k < 800; k++) {
      const d = back(k);
      if (days.has(d)) n += 1;
      else if (miss === null || k - miss >= 7) { if (!oldest || d < oldest) break; miss = k; } else break;
    }
    return n;
  }
  function activeDays() {                                          // jours d'activité, tous modes (série de jours)
    const db = load();
    return new Set([...Object.values(db.sessions).filter((s) => own(s) && Object.keys(s.answers).length >= s.items.length).map((s) => dayOf(s.created_at)), ...(db.ranges || []).map((r) => dayOf(r.at))]);
  }
  function bbWindow(mode, a, b) {                                  // BB perdus pour 100 décisions entre a et b jours en arrière
    let n = 0, lost = 0; const lo = Date.now() - b * DAY, hi = Date.now() - a * DAY;
    for (const s of Object.values(load().sessions)) if (s.mode === mode && own(s)) for (const r of Object.values(s.answers)) {
      const t = Date.parse(r.at); if (!(t > lo && t <= hi) || (r.field && r.field.read)) continue; n += 1; lost += 10 * Math.round((r.regret_mbb || 0) / 10);
    }
    return n ? Math.round(lost / 1000 * 100 / n * 100) / 100 : null;
  }
  // défis : mêmes règles que spinsacademy.challenges (jour, semaine et mois dans l'heure du navigateur ; défi du jour par jour UTC)
  const CH = __CHALLENGES__;
  const utcDay = (iso) => new Date(iso).toISOString().slice(0, 10);
  const dailyAttempt = () => Object.values(load().sessions).filter((s) => own(s) && s.plan === 'challenge_daily' && utcDay(s.created_at) === new Date().toISOString().slice(0, 10))
    .sort((a, b) => (a.created_at < b.created_at ? -1 : 1))[0] || null;      // une seule tentative par jour UTC, tous modes, finie ou non
  const rangeWon = (r) => r.bb_per_100 < CH.range_bb && (r.accuracy_pct == null || r.accuracy_pct >= CH.range_acc);
  function challengesOf(mode) {
    const db = load(), td0 = dayBack(0), mon = iso(mondayOf(Date.now()));
    const sx = (s) => ({ s, day: dayOf(s.created_at), answered: Object.keys(s.answers).length, correct: Object.values(s.answers).filter((r) => r.verdict === 'correct').length, timeouts: Object.values(s.answers).filter((r) => r.timed_out).length, size: s.items.length });
    const done = Object.values(db.sessions).filter((s) => s.mode === mode && own(s) && Object.keys(s.answers).length >= s.items.length).map(sx)
      .sort((a, b) => (a.s.created_at < b.s.created_at ? -1 : 1));
    const won = (k, x) => x.answered >= x.size && (k === 'daily' ? x.correct >= CH.daily_win : k === 'pressure' ? x.timeouts === 0 && x.correct >= CH.pressure_win : x.correct === x.size);
    const res = (x) => (x.answered < x.size ? `en cours : ${x.answered}/${x.size} répondues, ${x.correct} bonne${x.correct > 1 ? 's' : ''}` : `${x.correct}/${x.size}` + (x.timeouts ? `, ${x.timeouts} au temps` : ''));
    const card = (k, xs, window, action) => {
      const win = xs.some((x) => won(k, x)), best = xs.slice().sort((a, b) => (won(k, b) - won(k, a)) || (b.correct - a.correct))[0];
      return { kind: k, window, title_fr: CH.info[k][0], rule_fr: CH.info[k][1], status: win ? 'won' : xs.length ? 'tried' : 'todo', result_fr: best ? res(best) : null, action };
    };
    const of = (k) => done.filter((x) => x.s.plan === `challenge_${k}`), today_ = (xs) => xs.filter((x) => x.day === td0), week_ = (xs) => xs.filter((x) => x.day >= mon);
    const da = dailyAttempt(), dx = da && sx(da), open = dx && dx.answered < dx.size;
    const dcard = !dx ? { kind: 'daily', window: 'jour', title_fr: CH.info.daily[0], rule_fr: CH.info.daily[1], status: 'todo', result_fr: null, action: { type: 'challenge', challenge: 'daily', chrono: 15 } }
      : { kind: 'daily', window: 'jour', title_fr: CH.info.daily[0], rule_fr: CH.info.daily[1], status: won('daily', dx) ? 'won' : 'tried', result_fr: res(dx),
        action: open ? { type: 'resume', session_id: da.id, challenge: 'daily', chrono: 15 } : null, next_fr: open ? null : 'Nouveau défi demain.' };
    const daily = [dcard, Object.assign(card('perfect', today_(of('perfect')), 'jour', { type: 'challenge', challenge: 'perfect' }), { theme_fr: today(mode).theme_fr })];
    const weekly = [card('pressure', week_(of('pressure')), 'semaine', { type: 'challenge', challenge: 'pressure', chrono: 8 })];
    const rw = (db.ranges || []).filter((r) => dayOf(r.at) >= mon), bestR = rw.slice().sort((a, b) => (rangeWon(b) - rangeWon(a)) || (a.bb_per_100 - b.bb_per_100))[0];
    weekly.push({ kind: 'range', window: 'semaine', title_fr: CH.info.range[0], rule_fr: CH.info.range[1], status: bestR && rangeWon(bestR) ? 'won' : rw.length ? 'tried' : 'todo',
      result_fr: bestR ? `meilleure : ${nfr(bestR.bb_per_100)} BB pour 100, ${nfr(bestR.accuracy_pct || 0)} % bien classées` : null, action: { type: 'range' } });
    if (mode === 'exploit') weekly.push(card('reader', week_(of('reader')), 'semaine', { type: 'challenge', challenge: 'reader' }));
    const month = new Set([...activeDays()].filter((d) => d >= td0.slice(0, 8) + '01'));
    let best = 0; for (const d of month) best = Math.max(best, streak(month, d));   // comptée comme la série de jours
    const monthly = [{ kind: 'full_week', window: 'mois', title_fr: CH.info.full_week[0], rule_fr: CH.info.full_week[1], status: best >= 7 ? 'won' : best ? 'tried' : 'todo', result_fr: `meilleure série du mois : ${best} jour${best > 1 ? 's' : ''}`, action: null }];
    const hist = [];
    for (const k of ['daily', 'perfect', 'pressure', 'reader']) { const seen = new Set(); for (const x of of(k)) { const u = utcDay(x.s.created_at); if (k === 'daily' && seen.has(u)) continue; seen.add(u); hist.push({ kind: k, title_fr: CH.info[k][0], date: x.day, result_fr: res(x), won: won(k, x) }); } }
    for (const r of db.ranges || []) if (rangeWon(r)) hist.push({ kind: 'range', title_fr: CH.info.range[0], date: dayOf(r.at), result_fr: `${nfr(r.bb_per_100)} BB pour 100`, won: true });
    return { mode, daily, weekly, monthly, history: hist.sort((a, b) => (a.date < b.date ? 1 : -1)).slice(0, 30) };
  }

  // niveaux et premier lancement : mêmes règles que spinsacademy.levels
  const LV = __LEVELS__;
  function levelRow() {
    const db = load();
    if (!db.level) { if (!Object.keys(db.sessions).length) return { level: 1, onboarded_at: null }; db.level = { level: 1, onboarded_at: now() }; save(); }
    return db.level;
  }
  const inLevel = (lv, eff, fam) => { const L = LV.levels[lv]; return eff >= L.depth[0] && eff < L.depth[1] && L.themes.some(([, f]) => f.family === fam); };
  const levelFits = (lv, f) => lv >= 4 || ((f.min_stack ?? 0) >= LV.levels[lv].depth[0] && (f.max_stack ?? 99) <= LV.levels[lv].depth[1]);
  function levelStatus(lv) {
    if (!LV.decisions[lv]) return { level: lv, ready: false, criteria: [], final: true };
    const xs = [];
    for (const s of Object.values(load().sessions)) if (s.mode === 'gto' && own(s)) s.items.forEach((i, k) => { const r = s.answers[k]; if (!r) return;
      const m = r.meta || (ITEMS[i] && metaOf(ITEMS[i])); if (m && inLevel(lv, m.eff, m.family)) xs.push([r.at, r]); });
    const mine = xs.sort((a, b) => (a[0] < b[0] ? -1 : 1)).slice(-LV.recent).map(([, r]) => r);
    const dec = mine.length, lost = mine.reduce((a, r) => a + 10 * Math.round((r.regret_mbb || 0) / 10), 0), bbv = dec ? Math.round(lost / 1000 * 100 / dec * 100) / 100 : null;
    const crit = [{ kind: 'decisions', label_fr: `${LV.decisions[lv]} décisions à ${LV.depth_fr[lv]}`, depth_fr: LV.depth_fr[lv], value: dec, target: LV.decisions[lv], ok: dec >= LV.decisions[lv] },
      { kind: 'bb', label_fr: `Moins de ${String(LV.bb_target[lv]).replace('.', ',')} BB perdus pour 100 décisions`, value: bbv, target: LV.bb_target[lv], ok: bbv != null && dec >= LV.decisions[lv] && bbv < LV.bb_target[lv] }];
    if (lv === 1) { const good = (load().ranges || []).filter((r) => { const t = RTASKS.find((x) => x.spot_id === r.spot_id); return r.accuracy_pct >= LV.range_good && t && inLevel(1, t.effective_stack_bb, t.family); }).length;
      crit.push({ kind: 'ranges', label_fr: `${LV.ranges_l1} ranges du niveau à ${LV.range_good} % ou plus`, value: good, target: LV.ranges_l1, ok: good >= LV.ranges_l1 }); }
    if (lv === 2) { const weak = (stats().focus || {}).kind === 'weak'; crit.push({ kind: 'fragile', label_fr: 'Aucun thème du niveau fragile', value: weak ? stats().focus.label : null, target: null, ok: dec > 0 && !weak }); }
    return { level: lv, ready: crit.every((c) => c.ok), criteria: crit, final: false };
  }
  function levelInfo() {
    const row = levelRow(); let promoted = null, st;
    for (;;) { st = levelStatus(row.level); if (!st.ready || !row.onboarded_at) break; row.level += 1; promoted = row.level; const db = load(); db.level = row; resetPlan(); save(); }
    return { level: row.level, name: LV.levels[row.level].name, depth_fr: LV.depth_fr[row.level], onboarded: !!row.onboarded_at, experience: row.experience || null, goal: row.goal || null, promoted_to: promoted, status: st,
      levels: Object.entries(LV.levels).map(([k, v]) => ({ number: +k, name: v.name, mode: v.mode, depth_fr: LV.depth_fr[k] })), experiences: LV.experiences, goals: LV.goals };
  }
  function setLevel(body, onboarding) {
    const db = load(), lv = onboarding ? (body.level || LV.start[body.experience] || 1) : body.level;
    if (!(lv >= 1 && lv <= 3)) return [422, { detail: 'niveau de 1 à 3' }];
    db.level = Object.assign(db.level || {}, { level: lv }, onboarding ? { experience: body.experience, goal: body.goal, onboarded_at: now() } : { onboarded_at: (db.level || {}).onboarded_at || now() }); resetPlan(); save();
    return [200, levelInfo()];
  }
  function resetPlan() {                                           // le niveau change : séance GTO du jour recalculée, sauf si son thème est commencé
    const db = load(), td = dayBack(0);
    if (!Object.values(db.sessions).some((s) => own(s) && s.plan === 'theme' && dayOf(s.created_at) === td) && db.plans) delete db.plans[`gto:${td}`];
  }
  function rangeOk(f) { return RTASKS.some((t) => (!f.table || t.table === f.table) && (!f.hero || t.hero === f.hero) && (!f.family || t.family === f.family)
    && t.effective_stack_bb >= (f.min_stack || 0) && t.effective_stack_bb <= (f.max_stack || 999)); }
  function today(mode) {                                           // test joueurs 9 : thème et range fixés au premier affichage du jour
    const db = load(), td = dayBack(0);
    const ss = Object.values(db.sessions).filter((s) => s.mode === mode && own(s));
    const done = ss.filter((s) => Object.keys(s.answers).length >= s.items.length), doneToday = done.filter((s) => dayOf(s.created_at) === td);
    const rgs = (db.ranges || []).map((r) => r.at);
    const lvn = mode === 'gto' ? levelRow().level : 4, themes = LV.levels[lvn].themes;     // étape 4 : thèmes du niveau
    const plans = (db.plans = db.plans || {}), key = `${mode}:${td}`;
    if (!plans[key]) {
      const active = new Set([...done.map((s) => dayOf(s.created_at)), ...rgs.map(dayOf)]);
      const firstTheme = ss.filter((s) => s.plan === 'theme' && dayOf(s.created_at) === td).sort((a, b) => (a.created_at < b.created_at ? -1 : 1))[0];
      let focus = stats().focus; if (focus && focus.filters && !levelFits(lvn, focus.filters)) focus = null; let label, f;
      const ff = (focus && focus.filters) || {};
      if (firstTheme) { f = firstTheme.filters || {}; label = (themes.concat(THEMES).find(([, x]) => JSON.stringify(x) === JSON.stringify(f)) || [focus && focus.label || 'Ton thème du jour'])[0]; }
      else if (ff.family && ff.max_stack != null) { f = Object.fromEntries(Object.entries(ff).filter(([k]) => k !== 'mode')); label = (focus.label || 'Ton thème à travailler').replace(/^(GTO|Exploitant) · /, ''); }
      else [label, f] = themes[[...active].filter((d) => d !== td).length % themes.length];
      let rf = Object.fromEntries(['table', 'hero', 'family', 'min_stack', 'max_stack'].filter((k) => f[k] != null).map((k) => [k, f[k]])); if (rf.family === 'read') delete rf.family;
      for (const g of [rf, { ...rf, hero: undefined }, { family: rf.family, table: rf.table }, {}]) { const c = Object.fromEntries(Object.entries(g).filter(([, v]) => v != null)); if (rangeOk(c)) { rf = c; break; } }
      const cands = RTASKS.filter((t) => (!rf.table || t.table === rf.table) && (!rf.hero || t.hero === rf.hero) && (!rf.family || t.family === rf.family) && t.effective_stack_bb >= (rf.min_stack || 0) && t.effective_stack_bb <= (rf.max_stack || 999));
      plans[key] = { theme_fr: label, filters: f, range_filters: rf, range_spot: cands.length ? cands[Number(td.replace(/-/g, '')) % cands.length].spot_id : null }; save();
    }
    const plan = plans[key], label = plan.theme_fr, f = plan.filters;
    const rv = reviews(mode), due = rv.due, revs = doneToday.filter((s) => s.plan === 'review').length, themed = doneToday.filter((s) => s.plan === 'theme').length;
    const ranged = rgs.filter((r) => dayOf(r) === td).length;
    let rlabel = due ? `Révision : ${due} main${due > 1 ? 's' : ''} à revoir` : "Révision : rien à revoir aujourd'hui";
    if (!due && rv.next_due_at && dayOf(rv.next_due_at) === td) { const h = new Date(rv.next_due_at); rlabel = `Révision : rien à revoir pour l'instant (${rv.pending} main${rv.pending > 1 ? 's' : ''} à partir de ${h.getHours()} h${h.getMinutes() ? ' ' + pad(h.getMinutes()) : ''})`; }
    const depth = lvn < 4 ? { min_stack: LV.levels[lvn].depth[0], max_stack: LV.levels[lvn].depth[1] } : {};
    const steps = [
      { kind: 'review', done: due === 0 || revs >= LV.review_cap, count: due, label_fr: rlabel, filters: depth },
      { kind: 'theme', done: themed >= 2, count: Math.min(themed, 2), total: 2, label_fr: `Thème : ${label}`, filters: f },
      { kind: 'range', done: ranged >= 1, label_fr: mode === 'gto' ? __RANGE_FR__ : __RANGE_EXPLOIT_FR__, filters: plan.range_filters, spot_id: plan.range_spot }];
    const nxt = steps.findIndex((x) => !x.done), act = activeDays();
    return { minutes: 15, date: td, steps, next: nxt < 0 ? null : nxt, done: nxt < 0, started: (revs > 0 || themed > 0 || ranged > 0) && nxt >= 0,
      streak: streak(act), active_today: act.has(td), played_before: act.size > 0, theme_fr: label, level: { number: lvn, name: LV.levels[lvn].name, depth_fr: LV.depth_fr[lvn] },
      bb7: bbWindow(mode, 0, 7), bb7_prev: bbWindow(mode, 7, 14), mode };
  }

  // objectifs de la semaine : mêmes règles que spinsacademy.goals (semaine du lundi au dimanche, heure du navigateur)
  const G = __GOALS__;
  const mondayOf = (d) => { const x = new Date(d); x.setHours(0, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; };
  const iso = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const nfr = (x) => String(Math.round(x * 100) / 100).replace('.', ',');
  function weekValues(mode, start) {
    const lo = start.getTime(), hi = lo + 7 * DAY, inw = (at) => { const t = Date.parse(at); return t >= lo && t < hi; }, db = load();
    const days = new Set((db.ranges || []).filter((r) => inw(r.at)).map((r) => dayOf(r.at))); let n = 0, lost = 0;   // jours d'entraînement : séries finies et ranges
    for (const s of Object.values(db.sessions)) if (s.mode === mode && own(s)) {
      if (Object.keys(s.answers).length >= s.items.length && inw(s.created_at)) days.add(dayOf(s.created_at));
      for (const r of Object.values(s.answers)) if (r.at && inw(r.at) && !(r.field && r.field.read)) { n += 1; lost += 10 * Math.round((r.regret_mbb || 0) / 10); }
    }
    const good = (db.ranges || []).filter((r) => inw(r.at) && r.accuracy_pct >= G.range_good).length;
    return { days: days.size, day_set: days, precision: n ? Math.round(lost / 1000 * 100 / n * 100) / 100 : null, decisions: n, ranges: good };
  }
  const gDone = (k, t, v) => (k === 'precision' ? v.precision != null && v.decisions >= G.min_decisions && v.precision <= t : v[k] >= t);
  const daysCap = (v) => { const td = dayBack(0), wd = (new Date().getDay() + 6) % 7;     // jours encore atteignables cette semaine
    return Math.max(G.bounds.days[0], Math.min(G.bounds.days[1], [...(v.day_set || [])].filter((d) => d < td).length + 7 - wd)); };
  function gView(t, v, cap) {
    return G.kinds.map((k) => {
      let text, frac;
      if (k === 'precision') {
        const cur = v.precision; text = (cur != null ? `${nfr(cur)} cette semaine (${v.decisions} décisions) · cible : moins de ${nfr(t[k])}` : `cible : moins de ${nfr(t[k])}`) + (v.decisions < G.min_decisions ? ` (au moins ${G.min_decisions} décisions)` : '');
        frac = cur == null ? 0 : Math.min(1, v.decisions / G.min_decisions) * (cur <= t[k] ? 1 : Math.max(0, Math.min(1, t[k] / cur)));
      } else { text = `${v[k]} / ${t[k]}`; frac = Math.min(1, v[k] / t[k]); }
      return { kind: k, label_fr: G.label[k], target: t[k], value: k === 'precision' ? v.precision : v[k], text_fr: text, progress: Math.round(frac * 100) / 100,
        done: gDone(k, t[k], v), min: G.bounds[k][0], max: k === 'days' && cap ? Math.min(G.bounds[k][1], cap) : G.bounds[k][1] };
    });
  }
  function goals(mode) {
    const db = load(), start = mondayOf(Date.now()), wk = (k) => new Date(start.getTime() - 7 * k * DAY), store = (db.goals = db.goals || {});
    const key = (k) => `${mode}:${iso(wk(k))}`, prevT = store[key(1)], prevV = weekValues(mode, wk(1));
    const v0 = weekValues(mode, start), cap = daysCap(v0);
    if (!store[key(0)]) {
      const t = {}, isNew = !Object.keys(store).some((k) => k.startsWith(mode + ':'));      // premier passage : cibles plus basses
      for (const k of ['days', 'ranges']) { const p = (prevT || {})[k] ?? (isNew ? G.default_new : G.default)[k]; t[k] = prevT && !gDone(k, p, prevV) ? Math.max(G.bounds[k][0], p - 1) : p; }
      const hist = [1, 2, 3, 4].map((k) => weekValues(mode, wk(k))).filter((v) => v.decisions >= G.min_decisions).map((v) => v.precision);
      t.precision = hist.length ? Math.max(G.bounds.precision[0], Math.round(hist.reduce((a, b) => a + b, 0) / hist.length * 0.9 * 2) / 2) : G.default_bb;
      if (prevT && !gDone('precision', prevT.precision, prevV)) t.precision = Math.max(t.precision, Math.round(prevT.precision * 1.1 * 2) / 2);
      t.days = Math.min(t.days, cap); store[key(0)] = t; save();
    }
    let last = null;
    if (prevT && (prevV.days || prevV.ranges || prevV.decisions)) {                      // bilan seulement s'il y avait des objectifs
      const items = gView(prevT, prevV);
      last = { week: iso(wk(1)), done: items.filter((x) => x.done).length, total: items.length, bb: prevV.precision, bb_before: weekValues(mode, wk(2)).precision, days: prevV.days, decisions: prevV.decisions };
    }
    const today0 = new Date(); return { mode, week: iso(start), days_left: 6 - ((today0.getDay() + 6) % 7), items: gView(store[key(0)], v0, cap), last_week: last };
  }
  function setGoal(body) {
    const k = body.kind, lo = (G.bounds[k] || [0])[0], t = k === 'precision' ? Math.round(body.target * 2) / 2 : Math.round(body.target);
    const hi = k === 'days' ? daysCap(weekValues(body.mode || 'gto', mondayOf(Date.now()))) : (G.bounds[k] || [0, -1])[1];
    if (!(t >= lo && t <= hi)) return [422, { detail: `cible hors des bornes (${lo} à ${hi})` }];
    goals(body.mode || 'gto'); const db = load(); db.goals[`${body.mode || 'gto'}:${iso(mondayOf(Date.now()))}`][k] = t; save();
    return [200, goals(body.mode || 'gto')];
  }

  // recommandations : mêmes règles que spinsacademy.recommend (sans le sens des erreurs)
  function recommendations(mode) {
    const out = [], st = stats(), td = today(mode), tf = td.steps[1].filters || {};
    const late = reviewItems(mode).filter((x) => x.due_at <= Date.now() - 2 * DAY).length;
    if (late) out.push({ kind: 'review', text_fr: `${late} main${late > 1 ? 's' : ''} ratée${late > 1 ? 's' : ''} attend${late > 1 ? 'ent leur' : ' sa'} révision depuis plus de 2 jours.`, label_fr: 'Revoir mes mains', action: { type: 'review' } });
    const fr = (st.recurring_errors || []).find((t) => { const f = Object.fromEntries(Object.entries(t.filters).filter(([k]) => k !== 'mode')); return !Object.entries(f).every(([k, v]) => tf[k] === v); });
    if (fr) out.push({ kind: 'theme', text_fr: `${fr.label.replace(/^(GTO|Exploitant) · /, '')} : ${fr.errors} erreurs sur ${fr.questions}.`, label_fr: 'Une série ciblée',
      action: { type: 'series', filters: Object.fromEntries(Object.entries(fr.filters).filter(([k]) => k !== 'mode')) } });
    const lr = (load().ranges || []).slice(-1)[0];
    if (lr && lr.ref) {
      const ratio = lr.my / lr.ref, where = (lr.where || '').charAt(0).toUpperCase() + (lr.where || '').slice(1);
      const msg = ratio < 0.75 ? `Ta dernière range était trop serrée : ${lr.my} % des mains au lieu de ${lr.ref} % (${where}).`
        : ratio > 1.33 ? `Ta dernière range était trop large : ${lr.my} % des mains au lieu de ${lr.ref} % (${where}).`
        : lr.accuracy_pct < 80 ? `Ta dernière range : ${String(lr.accuracy_pct).replace('.', ',')} % de mains bien classées (${where}).` : null;
      if (msg) out.push({ kind: 'range', text_fr: msg, label_fr: 'Refaire cette range', action: { type: 'range', spot_id: lr.spot_id } });
    }
    let to = 0; for (const s of Object.values(load().sessions)) if (s.mode === mode && own(s)) for (const r of Object.values(s.answers)) if (r.timed_out && Date.parse(r.at) > Date.now() - 7 * DAY) to += 1;
    if (to >= 2) out.push({ kind: 'chrono', text_fr: `${to} coups joués au temps cette semaine : une série au chrono 15 s pour prendre le rythme.`, label_fr: 'Série au chrono 15 s', action: { type: 'series', filters: {}, chrono: 15 } });
    const played = new Set(((st.by || {}).family || []).map((r) => r.filters.family));
    const disc = [['first_in', 'premier à parler'], ['vs_allin', 'face à un tapis'], ['vs_limp', 'face à un limp'], ['vs_raise', 'face à une relance']].find(([f]) => !played.has(f) && tf.family !== f);
    if (disc) out.push({ kind: 'discover', text_fr: `Découvre une situation que tu n'as jamais jouée ici : ${disc[1]}.`, label_fr: 'Découvrir', action: { type: 'series', filters: { family: disc[0] } } });
    return { mode, items: out.slice(0, 2) };
  }

  // « Construis ta range » : même règle que spinsacademy.ranges.grade
  function rangeGrade(t, selected) {
    const sel = new Set(selected); const cells = {}; let wt = 0, good = 0, lost = 0, refw = 0, myw = 0; const errs = [];
    for (const [h, [f, cin, cout, w, unstable]] of Object.entries(t.hands)) {
      const played = sel.has(h); const cost = played ? cin : cout; const ref = unstable ? 'mixed' : f >= 0.75 ? 'in' : f <= 0.25 ? 'out' : 'mixed'; let st, ok;
      if (ref === 'mixed') { st = 'mixed'; ok = true; } else if (ref === 'in') { st = played ? 'ok_in' : 'missing'; ok = played; } else { st = played ? 'extra' : 'ok_out'; ok = !played; }
      if ((st === 'extra' || st === 'missing') && cost < 0.01) { st = 'close'; ok = true; }      // erreur sans coût mesurable
      cells[h] = st; wt += w; good += ok ? w : 0; lost += w * cost; refw += w * f; if (played) myw += w;
      if (st === 'extra' || st === 'missing') errs.push([cost, h]);
    }
    const worst = errs.sort((a, b) => b[0] - a[0] || (a[1] < b[1] ? 1 : -1)).slice(0, 5);
    const ref = wt ? Math.round(100 * refw / wt) : 0, n = (k) => Object.values(cells).filter((x) => x === k).length;
    return { spot_id: t.spot_id, cells, accuracy_pct: wt ? Math.round(1000 * good / wt) / 10 : 0, bb_per_100: wt ? Math.round(10000 * lost / wt) / 100 : 0,
      extra: n('extra'), missing: n('missing'), worst: worst.map(([c, h]) => ({ hand: h, cost_bb: Math.round(100 * c) / 100, kind: cells[h], ref_fr: t.hands[h][5] })),
      ref_share_pct: ref, my_share_pct: wt ? Math.round(100 * myw / wt) : 0, rule_fr: `À retenir : ${t.where_fr}, ${t.verb_fr} avec environ ${ref} % des mains.${t.polar_fr || ''}`,
      reference: Object.fromEntries(Object.entries(t.hands).map(([h, x]) => [h, x[0]])), reference_fr: Object.fromEntries(Object.entries(t.hands).map(([h, x]) => [h, x[5]])),
      situation_fr: t.situation_fr, question_fr: t.question_fr };
  }

  async function route(path, opts) {
    await ready;
    const url = new URL(path, 'https://demo.local/'); const p = url.pathname; const method = (opts && opts.method) || 'GET';
    const body = opts && opts.body ? JSON.parse(opts.body) : {};
    const db = load();
    if (p === '/sessions' && method === 'POST') {
      let f = Object.assign({}, body.filters || {}); const mode = f.mode || body.mode || 'gto'; delete f.mode;
      const size = body.size || 5; const purposes = {}; let plan = body.plan || null, seeded = null;
      if (body.challenge) {                                            // défis : mêmes règles que le serveur
        plan = `challenge_${body.challenge}`; const ud = new Date(); const utc = `${ud.getUTCFullYear()}${pad(ud.getUTCMonth() + 1)}${pad(ud.getUTCDate())}`;
        if (body.challenge === 'daily') { if (dailyAttempt()) return [409, { detail: "défi du jour déjà tenté aujourd'hui : nouveau défi demain" }]; f = {}; seeded = Number(utc); }
        else if (body.challenge === 'perfect') f = Object.assign({}, today(mode).steps[1].filters);      // le thème de la séance du jour
        else if (body.challenge === 'reader') { if (mode !== 'exploit') return [422, { detail: 'le défi « Lecteur de vilain » se joue en mode exploitant' }]; f = { family: 'read' }; }
        else f = {};
      }
      const last = Object.values(db.sessions).filter((x) => x.build === BUILD).sort((x, y) => (x.created_at < y.created_at ? 1 : -1)).slice(0, 6);
      const rSpots = new Set(last.flatMap((x) => x.items.map((i) => ITEMS[i] && ITEMS[i].q.spot_id))), rHands = new Set(last.flatMap((x) => x.items.map((i) => ITEMS[i] && ITEMS[i].q.hand)));
      const first = last.length && ITEMS[last[0].items[0]] ? ITEMS[last[0].items[0]].q.hand : null;
      const score = (xs) => xs.reduce((a, i) => a + 2 * rSpots.has(ITEMS[i].q.spot_id) + rHands.has(ITEMS[i].q.hand), 0) + (xs.length && ITEMS[xs[0]].q.hand === first ? 3 : 0);
      let picked;
      if (seeded !== null) {                                           // défi du jour : tirage fixé par la date, le même pour tous
        const rnd0 = Math.random; let t = seeded >>> 0;
        Math.random = () => { t = (t + 0x6D2B79F5) >>> 0; let r = Math.imul(t ^ (t >>> 15), 1 | t); r ^= r + Math.imul(r ^ (r >>> 7), 61 | r); return ((r ^ (r >>> 14)) >>> 0) / 4294967296; };
        try { picked = draw(mode, f, size); } finally { Math.random = rnd0; }
      } else if (body.challenge === 'reader') {                        // au moins deux « Quelle pastille ? »
        const prof = (xs) => xs.filter((i) => ITEMS[i].q.field && ITEMS[i].q.field.type === 'profil').length;
        for (let k = 0; k < 40 && !(picked && prof(picked) >= CH.reader_profiles); k++) picked = draw(mode, f, size);
      } else {
        picked = draw(mode, f, size);                                  // test joueurs 6 : la série qui répète le moins les dernières
        for (let k = 1; picked && score(picked) && k < 6; k++) { const o = draw(mode, f, size); if (o && score(o) < score(picked)) picked = o; }
      }
      if (body.review) {
        const due = reviewItems(mode).filter((x) => dayOf(new Date(x.due_at).toISOString()) <= dayBack(0)).slice(0, size);
        const rest = (picked || []).filter((i) => !due.some((x) => x.i === i));
        due.forEach((x, k) => { purposes[k] = `Révision de ton erreur du ${new Date(x.miss).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })} (étape ${x.stage} sur ${INTERVALS.length})`; });
        picked = due.map((x) => x.i).concat(rest).slice(0, size);
      }
      if (!picked || !picked.length) return [422, { detail: 'pas assez de situations pour ces filtres' }];
      const id = Math.random().toString(16).slice(2) + Date.now().toString(16);
      db.sessions[id] = { id, build: BUILD, created_at: now(), mode, items: picked, answers: {}, purposes, plan, filters: f }; save();
      return [201, { session_id: id, mode, size: picked.length, adaptive: null }];
    }
    const sm = p.match(/^\/sessions\/([^/]+)\/summary$/);
    if (sm) { const s = db.sessions[decodeURIComponent(sm[1])]; return s && own(s) ? [200, summary(s)] : [404, { detail: 'session inconnue' }]; }
    if (p === '/quiz/next') {
      const s = db.sessions[url.searchParams.get('session_id')]; if (!s || !own(s)) return [404, { detail: 'session inconnue' }];
      const k = s.items.findIndex((_, i) => !s.answers[i]);
      if (k < 0) return [200, { done: true, session_id: s.id }];
      return [200, { done: false, session_id: s.id, question_index: k, size: s.items.length, question: ITEMS[s.items[k]].q,
        purpose: (s.purposes || {})[k] ? 'spaced' : null, purpose_fr: (s.purposes || {})[k] || null, plan: s.plan || null }];
    }
    if (p === '/attempts' && method === 'POST') {
      const s = db.sessions[body.session_id]; if (!s || !own(s)) return [404, { detail: 'session inconnue' }];
      const it = ITEMS[s.items[body.question_index]]; if (!it) return [404, { detail: 'question inconnue' }];
      const prev = s.answers[body.question_index];
      if (prev) return prev.action_id === body.action_id ? [200, Object.assign({}, prev, { range: GRIDS[it.q.spot_id] || null, already_answered: true })] : [409, { detail: 'question déjà répondue' }];
      let r0 = it.c[body.action_id]; if (!r0) return [422, { detail: 'action non proposée' }];
      if (body.timed_out) r0 = Object.assign({}, r0, { verdict: 'erreur', points: 0, timed_out: true });     // chrono écoulé : erreur
      const r = Object.assign({}, r0, { range: GRIDS[it.q.spot_id] || null });
      s.answers[body.question_index] = Object.assign({ action_id: body.action_id, at: now(), meta: metaOf(it) }, r0); save();       // sans la grille : stockage léger
      return [200, Object.assign({}, r, { already_answered: false })];
    }
    if (p === '/reports' && method === 'POST') return report(body);
    if (p === '/ranges/next') {
      const q = url.searchParams, lo = Number(q.get('min_stack') || 0), hi = Number(q.get('max_stack') || 999);
      const bySpot = q.get('spot') && RTASKS.find((t) => t.spot_id === q.get('spot'));        // « Refaire cette range »
      const c = bySpot ? [bySpot] : RTASKS.filter((t) => (!q.get('table') || t.table === q.get('table')) && (!q.get('hero') || t.hero === q.get('hero'))
        && (!q.get('family') || t.family === q.get('family')) && t.effective_stack_bb >= lo && t.effective_stack_bb <= hi);
      if (!c.length) return [422, { detail: 'pas de situation à dessiner pour ces filtres' }];
      const recent = new Set((q.get('exclude') || '').split(',')); let pool = c.filter((t) => !recent.has(t.spot_id)); if (!pool.length) pool = c;
      const fam = rnd(uniq(pool.map((t) => t.family)).sort()); pool = pool.filter((t) => t.family === fam);       // famille, puis tapis, à parts égales
      const band = rnd(uniq(pool.map((t) => t.band)).sort()); pool = pool.filter((t) => t.band === band);
      const t = rnd(pool); const { hands, where_fr, verb_fr, polar_fr, ...rest } = t;
      return [200, Object.assign(rest, { hands: Object.keys(hands).sort(), weights: Object.fromEntries(Object.entries(hands).map(([h, x]) => [h, x[3]])) })];
    }
    if (p === '/ranges/answer' && method === 'POST') {
      const t = RTASKS.find((x) => x.spot_id === body.spot_id); if (!t) return [404, { detail: 'situation inconnue' }];
      const g = rangeGrade(t, (body.hands || []).filter((h) => h in t.hands));
      db.ranges = (db.ranges || []).concat([{ spot_id: t.spot_id, accuracy_pct: g.accuracy_pct, bb_per_100: g.bb_per_100, my: g.my_share_pct, ref: g.ref_share_pct, where: t.where_fr, at: now() }]); save();
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
    if (p === '/users/me/today') return [200, today(url.searchParams.get('mode') || 'gto')];
    if (p === '/users/me/recommendations') return [200, recommendations(url.searchParams.get('mode') || 'gto')];
    if (p === '/users/me/goals' && method === 'PUT') return setGoal(body);
    if (p === '/users/me/preferences') {                              // le mode choisi (test joueurs 9) ; pas d'adaptation dans la démo
      if (method === 'PUT' && body.mode) { db.prefs = Object.assign(db.prefs || {}, { mode: body.mode }); save(); }
      return [200, { adaptive: false, adaptation_reset_at: null, mode: (db.prefs || {}).mode || null }];
    }
    if (p === '/users/me/level' && method === 'PUT') return setLevel(body, false);
    if (p === '/users/me/onboarding' && method === 'POST') return setLevel(body, true);
    if (p === '/users/me/level') return [200, levelInfo()];
    if (p === '/users/me/challenges') return [200, challengesOf(url.searchParams.get('mode') || 'gto')];
    if (p === '/users/me/goals') return [200, goals(url.searchParams.get('mode') || 'gto')];
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
    body = body.replace('<a class="secondary conseil-link" href="conseil">', '<a class="secondary conseil-link" href="conseil" hidden>', 1)   # conseiller : seulement sur le serveur
    body = body.replace('id="quick-start">Série recommandée<', 'id="quick-start">Série rapide<', 1)
    page = (f'<meta charset="utf-8">\n<title>SpinsAcademy</title>\n<meta name="theme-color" content="#0f3d2e">\n<style>\n{theme_css(css)}\n{EXTRA_CSS}</style>\n'
            f'{body}\n<div id="demo-toast" role="status" hidden></div>\n<script type="application/octet-stream" id="demo-data">{blob}</script>\n'
            f'<script>window.SA_LEXIQUE = {open(os.path.join(WEB, "lexique.json")).read()};</script>\n'
            f'<script>const DATASETS = {json.dumps(dict(gto=gto, exploit=fld))};</script>\n'
            f'<script>\n{SHIM.replace("__HU_SHARE__", str(quiz.HU_SHARE)).replace("__RANGE_FR__", json.dumps(today.RANGE_FR, ensure_ascii=False)).replace("__RANGE_EXPLOIT_FR__", json.dumps(today.RANGE_EXPLOIT_FR, ensure_ascii=False)).replace("__FAMILY_SHARE__", json.dumps(field.FAMILY_SHARE)).replace("__MAX_TRAPS__", str(field.MAX_TRAPS)).replace("__MAX_READ__", str(field.MAX_READ)).replace("__EASY_SHARE__", str(quiz.EASY_SHARE)).replace("__MIN_ANSWERS__", str(adaptive.MIN_ANSWERS)).replace("__MIN_ERRORS__", str(adaptive.MIN_ERRORS)).replace("__WEAK_RATE__", str(adaptive.WEAK_RATE)).replace("__INTERVALS__", json.dumps(list(review.INTERVALS_DAYS))).replace("__BUILD__", build_id).replace("__REVIEW_RULE__", json.dumps(review.RULE_FR, ensure_ascii=False)).replace("__THEMES__", json.dumps(today.THEMES, ensure_ascii=False)).replace("__CHALLENGES__", json.dumps(dict(info=challenges.INFO, daily_win=challenges.DAILY_WIN, pressure_win=challenges.PRESSURE_WIN, range_bb=challenges.RANGE_BB, range_acc=challenges.RANGE_ACC, reader_profiles=challenges.READER_PROFILES), ensure_ascii=False)).replace("__LEVELS__", json.dumps(dict(levels={k: dict(name=v['name'], depth=v['depth'], mode=v['mode'], themes=v['themes']) for k, v in levels.LEVELS.items()}, decisions=levels.DECISIONS, bb_target=levels.BB_TARGET, ranges_l1=levels.RANGES_L1, range_good=levels.RANGE_GOOD, recent=levels.RECENT, start=levels.START_LEVEL, experiences=levels.EXPERIENCE_FR, goals=levels.GOAL_FR, depth_fr=levels.DEPTH_FR, review_cap=today.REVIEW_CAP), ensure_ascii=False)).replace("__GOALS__", json.dumps(dict(kinds=goals.KINDS, default=goals.DEFAULT, default_new=goals.DEFAULT_NEW, default_bb=goals.DEFAULT_BB, min_decisions=goals.MIN_DECISIONS, range_good=goals.RANGE_GOOD, bounds=goals.BOUNDS, label=goals.LABEL), ensure_ascii=False))}\nDEMO.ready.then(() => {{\n{js}\n}});\n</script>\n')
    open(out, 'w').write(page)
    return len(data), len(page)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--hands-gto', type=int, default=3); ap.add_argument('--exploit-max', type=int, default=2500)
    a = ap.parse_args(); n, size = build(a.out, a.hands_gto, a.exploit_max)
    print(f'{a.out} : {n} questions, {size // 1024} Kio')

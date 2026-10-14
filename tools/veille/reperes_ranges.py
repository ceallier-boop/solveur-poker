"""Repère dans les transcriptions (sortie de vtt2txt.py) les minutes où une range est probablement affichée à l'écran.

Usage : python3 -I tools/veille/reperes_ranges.py meta.txt txt/*.txt > reperes.md
meta.txt : lignes « id|chaîne|date|durée|… |titre » écrites par youtube_subs.sh.
Un repère = indice visuel fort (tableau, chart, « à l'écran », couleurs de grille…) dans une minute qui parle de range.
"""
import re, sys, pathlib

FORT = re.compile(r"tableau|tableaux|\bcharts?\b|\bgrid\b|à l'écran|a l'ecran|on screen|range (à|a) l'écran|j'affiche|je l'affiche|affich(é|e|er) |je (vous|te) (montre|remonte) (la|le|les|ma|sa|ta) (range|tableau)|en (vert|rouge|bleu|jaune|orange|violet)|in (green|red|blue|yellow)|code couleur|légende|color code", re.I)
FAIBLE = re.compile(r"vous voyez|tu vois ici|on voit (ici|là)|regardez|you can see|let's look|as you can see|voilà la range|here is the range", re.I)
CONTEXTE = re.compile(r"\brange|\bcombos?\b|\bmains?\b|\bhands?\b|open|shove|chauve|tapis|push|jam|call|col(le|ler)?\b|limp|iso|3.?bet|trois.?b|fold|% ", re.I)
POS = [("BTN", r"bouton|\bbtn\b|button|\bbu\b"), ("SB", r"small ?blind|\bsb\b|petite blinde"), ("BB", r"big ?blind|\bbb\b|bébé|grosse blinde"), ("HU", r"heads?.?up|\bhu\b|\bhead\b")]
ACT = [("open shove", r"open ?sh|open shove|open jam|chauve|richov|shove|tapis direct"), ("call vs tapis", r"col(le|ler|lé)? (le|un|son|face)|call(ing)? (vs|a|the|against) (shove|jam|all)|range de col|calling range"), ("limp", r"limp"), ("iso", r"\biso"), ("open / raise", r"\bopen\b|min.?rai|raise|relanc"), ("3-bet", r"3.?bet|trois.?b|tr(i|ê)s? ?b(e|ê)t")]
STACK = re.compile(r"(\d+(?:[.,]\d)?) ?(?:bb|big blinds?|blindes?|bébés?|b\b)", re.I)

meta = {}
for l in pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    f = l.split("|")
    if len(f) >= 5: meta[f[0]] = (f[1], f[2], f[-1])
print("| Vidéo | Minute | Lien | Indices | Situation probable | Extrait |\n|---|---|---|---|---|---|")
for p in sys.argv[2:]:
    vid = pathlib.Path(p).stem
    chaine, date, titre = meta.get(vid, ("?", "?", vid))
    for l in pathlib.Path(p).read_text(encoding="utf-8").splitlines():
        m = re.match(r"\[(\d+)min\] (.*)", l)
        if not m: continue
        t, txt = int(m.group(1)), m.group(2)
        fort, faible = FORT.findall(txt), FAIBLE.findall(txt)
        if not CONTEXTE.search(txt) or not (fort or len(faible) >= 2): continue
        pos = "/".join(n for n, r in POS if re.search(r, txt, re.I))
        act = ", ".join(n for n, r in ACT if re.search(r, txt, re.I))
        stacks = sorted({s.replace(",", ".") for s in STACK.findall(txt) if 0 < float(s.replace(",", ".")) <= 30}, key=float)
        situation = " ; ".join(x for x in (pos, act, " ".join(f"{s} BB" for s in stacks[:4])) if x)
        mf = FORT.search(txt) or FAIBLE.search(txt)
        a = max(0, mf.start() - 120); extrait = txt[a:mf.end() + 160].replace("|", "/")
        indices = f"{len(fort)} fort(s), {len(faible)} faible(s)"
        print(f"| {chaine} – {titre[:60]} | {t} | [▶](https://youtu.be/{vid}?t={t * 60}) | {indices} | {situation} | …{extrait}… |")

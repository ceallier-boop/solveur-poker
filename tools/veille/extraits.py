"""Extraits de ±R caractères autour des indices de tendance de population (FR/EN), fusionnés s'ils se chevauchent."""
import re, sys, pathlib
R = 260
CUE = re.compile(r"récréa|recrea|\bfish|\bfiche|field|population|\bpool\b|\bregs?\b|trop (tight|large|serr|loose|passif|agress)|pas assez|too (tight|loose|wide|passive|much|often)|overfold|overcall|over-?limp|calling station|station|nit\b|maniac|limp(ent|e|ing|s)? (trop|beaucoup|too|a lot)|(paient|payent|call(ent)?) (trop|beaucoup|tout)|(shove|push|jam)s? (trop|too|tighter|wider|plus serr|moins)|que la théorie|than (gto|nash|theory)|par rapport (à|au) (la théorie|gto|nash)", re.I)
for p in sys.argv[1:]:
    lines = pathlib.Path(p).read_text(encoding="utf-8").splitlines()
    out = []
    for l in lines:
        m = re.match(r"\[(\d+)min\] (.*)", l)
        if not m: continue
        t, txt = m.group(1), m.group(2)
        spans = []
        for c in CUE.finditer(txt):
            a, b = max(0, c.start() - R), min(len(txt), c.end() + R)
            if spans and a <= spans[-1][1]: spans[-1][1] = b
            else: spans.append([a, b])
        out += [f"[{t}min] …{txt[a:b]}…" for a, b in spans]
    print(f"===== {pathlib.Path(p).stem} ({len(out)} extraits)")
    print("\n".join(out))

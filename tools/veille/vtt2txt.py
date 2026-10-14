"""Convertit un .vtt YouTube (sous-titres automatiques, lignes répétées) en texte par minute : [NNNmin] texte."""
import re, sys, pathlib
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
ts = re.compile(r"^(\d+):(\d+):(\d+)\.\d+ -->")
blocks, cur, seen = {}, 0, set()
for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
    m = ts.match(line)
    if m:
        h, mi, s = map(int, m.groups()); cur = (h * 3600 + mi * 60 + s) // 60; continue
    t = re.sub(r"<[^>]+>", "", line).strip()
    if not t or t in seen or t.startswith(("WEBVTT", "Kind:", "Language:")): continue
    seen.add(t); blocks.setdefault(cur, []).append(t)
dst.write_text("\n".join(f"[{k:03d}min] " + " ".join(v) for k, v in sorted(blocks.items())), encoding="utf-8")

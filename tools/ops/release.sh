#!/usr/bin/env bash
# Paquet de version : archive d'un tag git limitée à ce que le serveur exécute.
# Exclus : exports HRC bruts (data/hrc), scripts historiques (legacy), outils de génération, tests, documentation.
# Usage : tools/ops/release.sh v1.0.0 [dossier_de_sortie]
set -euo pipefail
TAG=${1:?usage : release.sh TAG [dossier]}; OUT=${2:-dist}
cd "$(git rev-parse --show-toplevel)"
git rev-parse -q --verify "refs/tags/$TAG" >/dev/null || { echo "tag $TAG introuvable (git tag -a $TAG -m ...)"; exit 1; }
INCLUDE=(spinsacademy data/datasets data/profiles requirements-app.txt requirements-app.lock tools/ops deploy)
NAME="spinsacademy-$TAG"; mkdir -p "$OUT"; TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
git archive --format=tar --prefix="$NAME/" "$TAG" "${INCLUDE[@]}" | tar -x -C "$TMP"
# le solveur (numba) n'est pas exécuté par le serveur : on le retire du paquet
rm -rf "$TMP/$NAME/spinsacademy/solver" "$TMP/$NAME/spinsacademy/postflop"
if find "$TMP/$NAME" -path '*/hrc/raw*' | grep -q .; then echo "exports HRC bruts présents dans le paquet : refus"; exit 1; fi
cat > "$TMP/$NAME/RELEASE.json" <<JSON
{"tag": "$TAG", "commit": "$(git rev-list -n1 "$TAG")", "built_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"}
JSON
tar -czf "$OUT/$NAME.tar.gz" -C "$TMP" "$NAME"
(cd "$OUT" && sha256sum "$NAME.tar.gz" > "$NAME.tar.gz.sha256")
echo "$OUT/$NAME.tar.gz ($(du -h "$OUT/$NAME.tar.gz" | cut -f1))"

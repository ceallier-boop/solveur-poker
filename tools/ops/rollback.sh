#!/usr/bin/env bash
# Retour à une version déjà déployée (par défaut : celle qui précède la version en service).
# Usage (root) : tools/ops/rollback.sh [nom_de_version]   ; tools/ops/rollback.sh --list
# La base n'est pas modifiée : les évolutions de schéma sont additives, une version antérieure ignore les colonnes et
# tables ajoutées depuis. Restaurer une sauvegarde seulement si des données doivent être annulées (tools/ops/backup.py).
set -euo pipefail
BASE=${BASE:-/opt/spinsacademy}; RESTART=${RESTART:-systemctl restart spinsacademy}; HEALTH_URL=${HEALTH_URL:-http://127.0.0.1:8000/health}
CUR=$(basename "$(readlink -f "$BASE/current")")
mapfile -t ALL < <(ls -1tr "$BASE/releases")
if [ "${1:-}" = "--list" ]; then for r in "${ALL[@]}"; do [ "$r" = "$CUR" ] && echo "$r (en service)" || echo "$r"; done; exit 0; fi
TARGET=${1:-}
if [ -z "$TARGET" ]; then
  for i in "${!ALL[@]}"; do [ "${ALL[$i]}" = "$CUR" ] && [ "$i" -gt 0 ] && TARGET=${ALL[$((i - 1))]}; done
fi
[ -n "$TARGET" ] && [ -d "$BASE/releases/$TARGET" ] || { echo "version cible introuvable"; exit 1; }
TTAG=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['tag'])" "$BASE/releases/$TARGET/RELEASE.json")
ln -sfn "$BASE/releases/$TARGET" "$BASE/current.new" && mv -Tf "$BASE/current.new" "$BASE/current"
eval "$RESTART"
for _ in $(seq 1 30); do
  out=$(curl -fsS "$HEALTH_URL" 2>/dev/null || true)
  if echo "$out" | grep -q '"status":"ok"' && echo "$out" | grep -q "\"tag\":\"$TTAG\""; then
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) rollback $CUR -> $TARGET" >> "$BASE/shared/deploy.log"; echo "version $TARGET en service"; exit 0
  fi; sleep 1
done
echo "la version $TARGET ne répond pas"; exit 1

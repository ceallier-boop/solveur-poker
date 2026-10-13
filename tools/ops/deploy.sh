#!/usr/bin/env bash
# Déploiement d'un paquet de version sur le serveur, avec retour arrière automatique si le contrôle de santé échoue.
#   1. vérifie l'empreinte du paquet et l'extrait dans $BASE/releases/<nom> ;
#   2. crée l'environnement Python de la version (versions figées de requirements-app.lock) ;
#   3. sauvegarde la base (tools/ops/backup.py) ;
#   4. bascule le lien $BASE/current, redémarre le service, contrôle /health ;
#   5. en cas d'échec : rebascule sur la version précédente et redémarre.
# Usage (root) : tools/ops/deploy.sh dist/spinsacademy-v1.0.0.tar.gz
# Variables : BASE (/opt/spinsacademy), ENV_FILE (/etc/spinsacademy.env), RESTART (systemctl restart spinsacademy),
#             HEALTH_URL (http://127.0.0.1:8000/health), PYTHON (python3.13)
set -euo pipefail
ARCHIVE=${1:?usage : deploy.sh paquet.tar.gz}
BASE=${BASE:-/opt/spinsacademy}; ENV_FILE=${ENV_FILE:-/etc/spinsacademy.env}
RESTART=${RESTART:-systemctl restart spinsacademy}; HEALTH_URL=${HEALTH_URL:-http://127.0.0.1:8000/health}; PYTHON=${PYTHON:-python3.13}
[ -f "$ARCHIVE.sha256" ] && (cd "$(dirname "$ARCHIVE")" && sha256sum -c "$(basename "$ARCHIVE").sha256" >/dev/null) || { echo "empreinte du paquet absente ou fausse"; exit 1; }
NAME=$(basename "$ARCHIVE" .tar.gz); DEST="$BASE/releases/$NAME"
[ -e "$DEST" ] && { echo "$DEST existe déjà : une version déployée est immuable"; exit 1; }
mkdir -p "$BASE/releases" "$BASE/shared/backups"
set -a; [ -f "$ENV_FILE" ] && . "$ENV_FILE"; set +a
tar -xzf "$ARCHIVE" -C "$BASE/releases"
"$PYTHON" -m venv "$DEST/.venv"
"$DEST/.venv/bin/pip" install -q --disable-pip-version-check -r "$DEST/requirements-app.lock"
"$DEST/.venv/bin/python" -c "import spinsacademy.api" || { echo "la version ne se charge pas"; rm -rf "$DEST"; exit 1; }
PREV=$(readlink -f "$BASE/current" 2>/dev/null || true)
if [ -n "${SPINSACADEMY_DB:-}" ] && [ -f "$SPINSACADEMY_DB" ]; then
  "$DEST/.venv/bin/python" "$DEST/tools/ops/backup.py" backup --db "$SPINSACADEMY_DB" --dir "$BASE/shared/backups"
fi
health() {
  for _ in $(seq 1 30); do
    if curl -fsS "$HEALTH_URL" 2>/dev/null | grep -q '"status":"ok"'; then return 0; fi; sleep 1
  done; return 1
}
ln -sfn "$DEST" "$BASE/current.new" && mv -Tf "$BASE/current.new" "$BASE/current"
eval "$RESTART"
if health; then
  echo "version $NAME en service ; précédente : ${PREV:-aucune}"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) deploy $NAME (précédente ${PREV:-aucune})" >> "$BASE/shared/deploy.log"
else
  echo "contrôle de santé en échec : retour à ${PREV:-aucune version}"
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) échec $NAME, retour ${PREV:-aucune}" >> "$BASE/shared/deploy.log"
  if [ -n "$PREV" ]; then ln -sfn "$PREV" "$BASE/current.new" && mv -Tf "$BASE/current.new" "$BASE/current"; eval "$RESTART"; health || echo "ATTENTION : la version précédente ne répond pas non plus"; fi
  exit 1
fi

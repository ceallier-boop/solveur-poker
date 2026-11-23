#!/usr/bin/env bash
# Première installation d'un serveur Debian/Ubuntu pour l'application (docs/exploitation/DEPLOIEMENT.md, « Première installation »).
# À lancer UNE fois, en root, depuis la racine du dépôt cloné sur le serveur :  sudo bash tools/ops/bootstrap_server.sh <nom-de-domaine>
# Idempotent : on peut le relancer sans dégât. NON TESTÉ sur un vrai serveur (écrit le 23/11/2026) : à essayer d'abord sur une machine neuve.
set -euo pipefail
DOMAIN="${1:-}"
[ "$(id -u)" -eq 0 ] || { echo "À lancer avec sudo."; exit 1; }
[ -n "$DOMAIN" ] || { echo "Usage : sudo bash tools/ops/bootstrap_server.sh <nom-de-domaine>   (ex. app.exemple.fr)"; exit 1; }
[ -f deploy/Caddyfile ] || { echo "Lancer depuis la racine du dépôt (dossier qui contient deploy/)."; exit 1; }

echo "1/6 Paquets"
apt-get update -y
apt-get install -y curl caddy ufw unattended-upgrades
if ! command -v python3.13 >/dev/null 2>&1; then
  apt-get install -y python3.13 python3.13-venv || { echo "Python 3.13 absent des dépôts : voir docs/exploitation/DEPLOIEMENT.md (installer Python 3.13 puis relancer)."; exit 1; }
fi

echo "2/6 Utilisateur et dossiers"
id spinsacademy >/dev/null 2>&1 || useradd --system --home /opt/spinsacademy --shell /usr/sbin/nologin spinsacademy
mkdir -p /opt/spinsacademy/shared/backups /opt/spinsacademy/releases
chown -R spinsacademy: /opt/spinsacademy/shared

echo "3/6 Configuration et jeton d'administration"
if [ ! -f /etc/spinsacademy.env ]; then
  install -m 640 -o root -g spinsacademy deploy/spinsacademy.env.example /etc/spinsacademy.env
  TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
  sed -i "s|^SPINSACADEMY_ADMIN_TOKEN=.*|SPINSACADEMY_ADMIN_TOKEN=${TOKEN}|" /etc/spinsacademy.env
  echo "   Jeton d'administration créé dans /etc/spinsacademy.env (le noter dans un gestionnaire de mots de passe)."
else
  echo "   /etc/spinsacademy.env existe déjà : conservé."
fi

echo "4/6 Services"
cp deploy/spinsacademy.service deploy/spinsacademy-backup.service deploy/spinsacademy-backup.timer /etc/systemd/system/
sed "s/spinsacademy\.example\.fr/${DOMAIN}/" deploy/Caddyfile > /etc/caddy/Caddyfile
systemctl daemon-reload
systemctl enable spinsacademy spinsacademy-backup.timer
systemctl reload caddy || systemctl restart caddy

echo "5/6 Pare-feu (SSH, HTTP, HTTPS) et mises à jour de sécurité automatiques"
ufw allow OpenSSH >/dev/null; ufw allow 80/tcp >/dev/null; ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null
dpkg-reconfigure -f noninteractive unattended-upgrades || true

echo "6/6 Terminé."
echo "Prochaines étapes (docs/exploitation/DEPLOIEMENT.md) : déployer le paquet de version (tools/ops/deploy.sh), puis publier la banque dans /admin."
echo "Vérifier que ${DOMAIN} pointe vers ce serveur (enregistrement DNS) : Caddy obtient le certificat HTTPS tout seul."

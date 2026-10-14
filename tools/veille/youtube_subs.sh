#!/usr/bin/env bash
# Récupère les sous-titres d'origine (fr puis en) d'une liste de vidéos YouTube et les convertit en texte horodaté.
# Usage : tools/veille/youtube_subs.sh ids.txt DOSSIER_SORTIE   (une id de vidéo par ligne)
# Prérequis : pip install yt-dlp ; node pour l'extraction YouTube. Les transcriptions sont des contenus protégés :
# les garder hors du dépôt, ne versionner que la synthèse (docs/produit/VEILLE_FORUMS_*.md).
set -u
ids=$1; out=$2; here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out/vtt" "$out/txt"
for id in $(cat "$ids"); do
  ls "$out/vtt/$id".*.vtt >/dev/null 2>&1 && continue
  yt-dlp --js-runtimes node --skip-download --ignore-no-formats-error --write-auto-subs --write-subs \
    --sub-langs "fr-orig,fr-FR-orig,en-orig,en-US-orig" \
    --print-to-file "%(id)s|%(channel)s|%(upload_date)s|%(duration_string)s|%(title)s" "$out/meta.txt" \
    -o "$out/vtt/%(id)s" "https://www.youtube.com/watch?v=$id" > "$out/vtt/$id.log" 2>&1
  grep -q "confirm your age" "$out/vtt/$id.log" && echo "$id : réservée aux adultes (cookies YouTube nécessaires)"
  grep -q "429" "$out/vtt/$id.log" && echo "$id : limite de débit YouTube, relancer plus tard"
  sleep 60   # YouTube répond 429 si les demandes sont trop rapprochées
done
for f in "$out"/vtt/*.vtt; do
  [ -e "$f" ] || continue
  id=$(basename "$f" | cut -d. -f1)
  [ -e "$out/txt/$id.txt" ] || python3 -I "$here/vtt2txt.py" "$f" "$out/txt/$id.txt"
done
echo "Extraits utiles : python3 $here/extraits.py $out/txt/*.txt"

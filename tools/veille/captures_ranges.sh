#!/usr/bin/env bash
# Capture des images des passages où une range est affichée (liste : docs/produit/reperes_ranges_youtube.csv).
# À lancer sur un ordinateur personnel (YouTube bloque les serveurs) :
#   tools/veille/captures_ranges.sh docs/produit/reperes_ranges_youtube.csv captures/ [priorité max, défaut 1] [cookies.txt]
# Pour chaque passage : télécharge seulement cette portion en 720p, puis une image par changement d'écran (au plus une toutes les 3 s).
# Prérequis : pip install yt-dlp ; ffmpeg. Les images restent hors du dépôt (contenus protégés).
set -u
csv=$1; out=$2; prio=${3:-1}; cookies=${4:-}
mkdir -p "$out"
tail -n +2 "$csv" | while IFS=, read -r id debut fin p _; do
  [ "$p" -le "$prio" ] || continue
  dir="$out/${id}_${debut}-${fin}"; mkdir -p "$dir"
  ls "$dir"/*.png >/dev/null 2>&1 && continue
  yt-dlp ${cookies:+--cookies "$cookies"} -f "bv[height<=720]/b[height<=720]" \
    --download-sections "*$((debut * 60))-$((fin * 60 + 60))" -o "$dir/extrait.%(ext)s" \
    "https://www.youtube.com/watch?v=$id" || { echo "échec $id (cookies nécessaires ?)"; continue; }
  # une image toutes les 3 s, puis suppression des images quasi identiques (table qui ne change pas)
  ffmpeg -loglevel error -i "$dir"/extrait.* -vf "fps=1/3,mpdecimate=hi=64*48:lo=64*20:frac=0.5" -fps_mode vfr "$dir/img_%03d.png"
  rm -f "$dir"/extrait.*
  sleep 30
done
echo "Images dans $out : déposez le dossier (ou les images où une grille est lisible) pour lecture des ranges."

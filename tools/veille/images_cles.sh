#!/usr/bin/env bash
# Extrait d'une vidéo complète les images clés (changement de main, grille de range affichée…),
# nommées par leur temps dans la vidéo pour être rapprochées de la transcription (vtt2txt.py).
# Usage : tools/veille/images_cles.sh video.mp4 DOSSIER_SORTIE [seuil de changement, défaut 0.12]
# Une image est gardée quand l'écran change assez (nouvelle main, tableau qui s'affiche), au plus une toutes les 2 s.
# Prérequis : ffmpeg. Les images restent hors du dépôt (contenus protégés).
set -eu
video=$1; out=$2; seuil=${3:-0.12}
mkdir -p "$out"
ffmpeg -hide_banner -nostats -loglevel info -i "$video" \
  -vf "fps=1/2,select='gt(scene,$seuil)',showinfo" -fps_mode vfr "$out/tmp_%05d.png" 2> "$out/showinfo.log"
# Renommage : tmp_00001.png -> t0012m34s.png (temps de la vidéo)
grep -o 'pts_time:[0-9.]*' "$out/showinfo.log" | cut -d: -f2 | nl -nln | while read -r n t; do
  s=${t%.*}; printf -v nom "t%03dm%02ds.png" $((s / 60)) $((s % 60))
  printf -v src "tmp_%05d.png" "$n"
  [ -e "$out/$src" ] && mv "$out/$src" "$out/$nom"
done
rm -f "$out/showinfo.log"
echo "$(ls "$out" | wc -l) images clés dans $out"

#!/usr/bin/env bash
# Перекодовує майстер-файл static/videos/hero.mp4 у веб-варіант.
#
#   bash scripts/build_video.sh
#
# Джерело — 3840x2160 @ 3.2 Мбіт/с (4.5 МБ). Це декоративне фонове відео під
# темним скримом, яке показується лише на екранах від 900px. У 4K там немає
# жодного сенсу — різниця не видна, а трафік витрачається.
#
# Чому лише H.264, без WebM/VP9: на однаковій якості VP9 дав 586 КБ проти
# 613 КБ у x264 — 4% виграшу за другий формат, другий <source> і другий
# прогін кодування. Не варте того для ассета, який вантажиться у простої
# і лише на десктопі. Якщо колись зʼявиться довше відео — сенс перевірити ще раз.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=static/videos/hero.mp4
OUT=static/videos/derived
mkdir -p "$OUT"

ffmpeg -y -v error -i "$SRC" -an \
  -vf "scale=1280:-2,fps=24" \
  -c:v libx264 -profile:v high -preset slow -crf 34 \
  -pix_fmt yuv420p -movflags +faststart \
  "$OUT/hero-720.mp4"

printf 'Джерело: %s KB\nРезультат: %s KB\n' \
  "$(( $(stat -c%s "$SRC" 2>/dev/null || stat -f%z "$SRC") / 1024 ))" \
  "$(( $(stat -c%s "$OUT/hero-720.mp4" 2>/dev/null || stat -f%z "$OUT/hero-720.mp4") / 1024 ))"

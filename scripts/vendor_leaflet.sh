#!/usr/bin/env bash
# Кладе Leaflet 1.9.4 локально в static/vendor/leaflet/.
#
#   bash scripts/vendor_leaflet.sh
#
# Навіщо: зараз Leaflet тягнеться з unpkg.com. Це зайвий DNS + TLS до чужого
# домену перед тим, як карта взагалі почне малюватись, і залежність від
# доступності CDN. Локальний файл їде тим самим зʼєднанням, що й решта сайту,
# і кешується назавжди (?v=<хеш>).
#
# Шаблон calculate_km.html сам перевіряє, чи файли на місці: доки їх немає,
# працює CDN. Тому запуск цього скрипта нічого не ламає — лише покращує.
#
# Хеші нижче — офіційні SRI з leafletjs.com. Якщо перевірка не проходить,
# файл побився або підмінився: краще впасти, ніж покласти таке в репозиторій.
set -euo pipefail
cd "$(dirname "$0")/.."
DEST=static/vendor/leaflet
BASE=https://unpkg.com/leaflet@1.9.4/dist
mkdir -p "$DEST/images"

check() {  # файл, очікуваний sha256-base64
  actual="sha256-$(openssl dgst -sha256 -binary "$1" | openssl base64 -A)"
  if [ "$actual" != "$2" ]; then
    echo "ПОМИЛКА: $1"; echo "  очікували: $2"; echo "  отримали:  $actual"
    rm -f "$1"; exit 1
  fi
  echo "  OK  $1"
}

curl -fsSL "$BASE/leaflet.css" -o "$DEST/leaflet.css"
check "$DEST/leaflet.css" "sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="

curl -fsSL "$BASE/leaflet.js" -o "$DEST/leaflet.js"
check "$DEST/leaflet.js" "sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="

# Іконки, на які посилається leaflet.css відносними шляхами.
for f in marker-icon.png marker-icon-2x.png marker-shadow.png layers.png layers-2x.png; do
  curl -fsSL "$BASE/images/$f" -o "$DEST/images/$f"
done

echo
echo "Готово. Шаблон перемкнеться на локальний Leaflet сам — перезапустіть Flask."

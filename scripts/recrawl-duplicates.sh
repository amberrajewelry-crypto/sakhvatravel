#!/bin/bash
set -euo pipefail

TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

PAGES="
/tour/soviet/
/ru/ekskursiya/transfer-iz-aeroporta-tbilisi/
/ru/ekskursiya/transfer-aeroport-tbilisi/
/ru/ekskursiya/truso-valley-tour/
/ru/ekskursiya/ekskursiya-truso/
/ru/ekskursiya/sighnaghi-tour-from-tbilisi/
/ru/ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/
/en/ekskursiya/vardzia-tour/
/en/ekskursiya/ekskursiya-vardzia/
/en/ekskursiya/wine-tour-tbilisi/
/en/ekskursiya/vinniy-tur-tbilisi/
/en/ekskursiya/kazbegi-tour-from-tbilisi/
/ru/ekskursiya/kazbegi-tour-from-tbilisi/
/ru/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/
/ru/ekskursiya/shopping-tour-tbilisi/
/ru/ekskursiya/shopping-tur-tbilisi/
/ru/ekskursiya/vin-tour-tbilisi/
/ru/ekskursiya/vinniy-tur-tbilisi/
"

for path in $PAGES; do
  url="https://sakhva-travel.com${path}"
  result=$(/usr/bin/curl -s -X POST \
    -H "Authorization: OAuth $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$url\"}" \
    "$BASE/recrawl/queue")
  echo "$path: $result"
done

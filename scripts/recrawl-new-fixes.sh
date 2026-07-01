#!/bin/bash
set -euo pipefail
TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

for path in \
  /ekskursiya/shopping-tour-tbilisi/ \
  /ekskursiya/transfer-iz-aeroporta-tbilisi/ \
  /ekskursiya/truso-valley-tour/ \
  /ekskursiya/vin-tour-tbilisi/ \
  /blog/car-rental-tbilisi/ \
  /ekskursiya/transfer-aeroport-tbilisi/; do
  url="https://sakhva-travel.com${path}"
  result=$(/usr/bin/curl -s -X POST \
    -H "Authorization: OAuth $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$url\"}" \
    "$BASE/recrawl/queue")
  echo "$path: $result"
done

#!/bin/bash
set -euo pipefail

TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

PAGES="
/ru/blog/kogda-ekhat-v-kazbegi/
/ru/blog/skrytye-mesta-tbilisi/
/ru/blog/car-rental-tbilisi/
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

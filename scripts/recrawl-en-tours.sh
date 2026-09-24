#!/bin/bash
set -euo pipefail

TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

for path in \
  /en/ekskursiya/vardzia-tour/ \
  /en/ekskursiya/wine-tour-tbilisi/ \
  /en/ekskursiya/kazbegi-tour-from-tbilisi/ \
  /en/ekskursiya/sighnaghi-tour-from-tbilisi/ \
  /en/ekskursiya/truso-valley-tour/ \
  /en/ekskursiya/shopping-tour-tbilisi/ \
  /en/ekskursiya/wine-tour-kakheti/ \
  /en/ekskursiya/gori-tour-from-tbilisi/ \
  /en/ekskursiya/borjomi-tour-from-tbilisi/ \
  /en/ekskursiya/mtskheta-tour-from-tbilisi/ \
  /en/ekskursiya/batumi-tour-from-tbilisi/ \
  /en/ekskursiya/kutaisi-tour-from-tbilisi/ \
  /en/ekskursiya/night-tour-tbilisi/ \
  /en/ekskursiya/old-tbilisi-walking-tour/ \
  /en/ekskursiya/kakheti-tour-from-tbilisi/ \
  /en/ekskursiya/jvari-tour-from-tbilisi/; do
  url="https://sakhva-travel.com${path}"
  result=$(/usr/bin/curl -s -X POST \
    -H "Authorization: OAuth $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$url\"}" \
    "$BASE/recrawl/queue")
  echo "$path: $result"
done

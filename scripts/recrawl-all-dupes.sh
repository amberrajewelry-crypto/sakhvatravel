#!/bin/bash
set -euo pipefail

TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

# All /ru/ekskursiya/ URLs that Yandex might have
PAGES="
/ru/ekskursiya/sighnaghi-tour-from-tbilisi/
/ru/ekskursiya/jvari-tour-from-tbilisi/
/ru/ekskursiya/kazbegi-tour-from-tbilisi/
/ru/ekskursiya/kakheti-tour-from-tbilisi/
/ru/ekskursiya/batumi-tour-from-tbilisi/
/ru/ekskursiya/kutaisi-tour-from-tbilisi/
/ru/ekskursiya/night-tour-tbilisi/
/ru/ekskursiya/old-tbilisi-walking-tour/
/ru/ekskursiya/wine-tour-kakheti/
/ru/ekskursiya/gori-tour-from-tbilisi/
/ru/ekskursiya/borjomi-tour-from-tbilisi/
/ru/ekskursiya/transfer-iz-aeroporta-tbilisi/
/ru/ekskursiya/transfer-aeroport-tbilisi/
/ru/ekskursiya/truso-valley-tour/
/ru/ekskursiya/ekskursiya-truso/
/ru/ekskursiya/vardzia-tour/
/ru/ekskursiya/ekskursiya-vardzia/
/ru/ekskursiya/shopping-tour-tbilisi/
/ru/ekskursiya/shopping-tur-tbilisi/
/ru/ekskursiya/vin-tour-tbilisi/
/ru/ekskursiya/vinniy-tur-tbilisi/
/ru/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/
/ru/ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/
/en/ekskursiya/vardzia-tour/
/en/ekskursiya/wine-tour-tbilisi/
/en/ekskursiya/kazbegi-tour-from-tbilisi/
/en/ekskursiya/sighnaghi-tour-from-tbilisi/
/en/ekskursiya/truso-valley-tour/
/en/ekskursiya/shopping-tour-tbilisi/
/en/ekskursiya/wine-tour-kakheti/
/en/ekskursiya/gori-tour-from-tbilisi/
/en/ekskursiya/borjomi-tour-from-tbilisi/
/en/ekskursiya/mtskheta-tour-from-tbilisi/
/en/ekskursiya/batumi-tour-from-tbilisi/
/en/ekskursiya/kutaisi-tour-from-tbilisi/
/en/ekskursiya/night-tour-tbilisi/
/en/ekskursiya/old-tbilisi-walking-tour/
/en/ekskursiya/kakheti-tour-from-tbilisi/
/en/ekskursiya/jvari-tour-from-tbilisi/
/tour/gori/
/tour/soviet/
/tour/kazbegi/
/tour/kakheti/
/tour/batumi/
/tour/mtskheta/
/tour/kutaisi/
/tour/old-tbilisi/
/tour/night-tbilisi/
/tour/dinner/
/ru/blog/kogda-ekhat-v-kazbegi/
/ru/blog/skrytye-mesta-tbilisi/
/ru/blog/car-rental-tbilisi/
"

ok=0
fail=0
for path in $PAGES; do
  url="https://sakhva-travel.com${path}"
  result=$(/usr/bin/curl -s -X POST \
    -H "Authorization: OAuth $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$url\"}" \
    "$BASE/recrawl/queue")
  if echo "$result" | grep -q "quota_remainder"; then
    ok=$((ok+1))
  else
    fail=$((fail+1))
    echo "FAIL: $path — $result"
  fi
done
echo "Done: $ok OK, $fail failed"

# Show remaining quota
/usr/bin/curl -s -H "Authorization: OAuth $TOKEN" "$BASE/recrawl/quota"

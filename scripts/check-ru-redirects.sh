#!/bin/bash
set -euo pipefail

echo "=== /ru/ekskursiya/ redirects ==="
for path in \
  /ru/ekskursiya/sighnaghi-tour-from-tbilisi/ \
  /ru/ekskursiya/jvari-tour-from-tbilisi/ \
  /ru/ekskursiya/kazbegi-tour-from-tbilisi/ \
  /ru/ekskursiya/kakheti-tour-from-tbilisi/ \
  /ru/ekskursiya/batumi-tour-from-tbilisi/ \
  /ru/ekskursiya/kutaisi-tour-from-tbilisi/ \
  /ru/ekskursiya/night-tour-tbilisi/ \
  /ru/ekskursiya/old-tbilisi-walking-tour/ \
  /ru/ekskursiya/wine-tour-kakheti/ \
  /ru/ekskursiya/gori-tour-from-tbilisi/ \
  /ru/ekskursiya/borjomi-tour-from-tbilisi/ \
  /ru/ekskursiya/transfer-iz-aeroporta-tbilisi/ \
  /ru/ekskursiya/transfer-aeroport-tbilisi/ \
  /ru/ekskursiya/truso-valley-tour/ \
  /ru/ekskursiya/ekskursiya-truso/ \
  /ru/ekskursiya/vardzia-tour/ \
  /ru/ekskursiya/ekskursiya-vardzia/ \
  /ru/ekskursiya/shopping-tour-tbilisi/ \
  /ru/ekskursiya/shopping-tur-tbilisi/ \
  /ru/ekskursiya/vin-tour-tbilisi/ \
  /ru/ekskursiya/vinniy-tur-tbilisi/ \
  /ru/ekskursiya/ekskursiya-kazbegi-iz-tbilisi/ \
  /ru/ekskursiya/ekskursiya-sighnaghi-iz-tbilisi/; do
  code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com${path}")
  echo "$code $path"
done

echo ""
echo "=== /en/ekskursiya/ old slugs ==="
for path in \
  /en/ekskursiya/vardzia-tour/ \
  /en/ekskursiya/ekskursiya-vardzia/ \
  /en/ekskursiya/wine-tour-tbilisi/ \
  /en/ekskursiya/vinniy-tur-tbilisi/ \
  /en/ekskursiya/kazbegi-tour-from-tbilisi/; do
  code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com${path}")
  echo "$code $path"
done

echo ""
echo "=== /tour/ old slugs ==="
for path in /tour/gori/ /tour/soviet/ /tour/kazbegi/ /tour/kakheti/; do
  code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com${path}")
  echo "$code $path"
done

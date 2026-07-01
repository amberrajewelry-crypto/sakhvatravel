#!/bin/bash
set -euo pipefail

TOKEN=$(security find-generic-password -a "$USER" -s "yandex-webmaster-token" -w)
BASE="https://api.webmaster.yandex.net/v4/user/1997617080/hosts/https:sakhva-travel.com:443"

echo "=== TITLE DUPLICATES ==="
/usr/bin/curl -s -H "Authorization: OAuth $TOKEN" "$BASE/diagnostics/titles-duplicates" > /tmp/ywm_titles.json
python3 -m json.tool /tmp/ywm_titles.json

echo ""
echo "=== DESCRIPTION DUPLICATES ==="
/usr/bin/curl -s -H "Authorization: OAuth $TOKEN" "$BASE/diagnostics/descriptions-duplicates" > /tmp/ywm_desc.json
python3 -m json.tool /tmp/ywm_desc.json

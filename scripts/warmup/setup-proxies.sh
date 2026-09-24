#!/bin/bash
set -euo pipefail

# Setup SOCKS5 proxies for all 20 SEO profiles via MLX Cloud API
# HTTP proxy doesn't work with HTTPS in Mimic, SOCKS5 does

XCLI="/Users/vladimir/mlx/deps/cli/xcli"
FOLDER="7866c289-662f-43d3-893d-0c640c4be923"

# Sign in and get token
MLX_EMAIL=$(security find-generic-password -s "mlx-email" -w 2>/dev/null)
MLX_PASS=$(security find-generic-password -s "mlx-password" -w 2>/dev/null)
MLX_PASS_HASH=$(echo -n "$MLX_PASS" | md5 2>/dev/null)

curl -s 'https://api.multilogin.com/user/signin' \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$MLX_EMAIL\",\"password\":\"$MLX_PASS_HASH\"}" > /tmp/mlx_signin.json

MLX_TOKEN=$(python3 -c "import json; print(json.load(open('/tmp/mlx_signin.json'))['data']['token'])")

if [[ -z "$MLX_TOKEN" ]]; then
  echo "FATAL: failed to get MLX token"
  exit 1
fi

# Profile ID:Name:Country
declare -a PROFILES=(
  "eaf28266-7fd6-4c52-893f-97bbecf95fd1:SEO-User-01:ru"
  "5eb8e97b-5523-4e23-8db6-cc12cfd1cf97:SEO-User-02:ru"
  "bb690360-c68f-4fd2-9f07-f82572383402:SEO-User-03:ru"
  "819d7628-3b4b-456f-8e48-91f217458e2c:SEO-User-04:ru"
  "cacac083-4a93-4895-9c68-949c065424b3:SEO-User-05:ru"
  "0e0dd9e6-65cf-424a-833b-3103572ff5d6:SEO-User-06:ru"
  "60b5c79f-da4f-4298-b097-6d305239d143:SEO-User-07:ru"
  "f4baf31a-8fd8-4c06-b5f4-90a9b7411023:SEO-User-08:ru"
  "3c412a60-9fe7-4782-ab8d-40a1a714ba80:SEO-User-09:ru"
  "d1ceb77f-324f-42dd-be57-dae994036b39:SEO-User-10:ru"
  "5554c22e-a6af-495d-990a-961c92c1e10d:SEO-User-11:ru"
  "3320fe22-3a05-4f33-8b7f-abe1830076ee:SEO-User-12:ru"
  "79d33eec-2ad0-4a01-a1fe-a0111bac2054:SEO-User-13:de"
  "f0b97fd1-2943-481a-b497-ef1b366ebce3:SEO-User-14:gb"
  "5ce8f669-03ca-4871-82a7-315366533d35:SEO-User-15:fr"
  "28ade7ff-48f4-4bee-b73c-ee7c66658e86:SEO-User-16:tr"
  "fe2b8a88-5750-449f-be48-b069fb0ef308:SEO-User-17:ae"
  "a20935b9-46a7-4e71-88dd-1e135d9be28a:SEO-User-18:us"
  "e2d0dd54-6c75-4f1e-b061-79e2b6cf7d42:SEO-User-19:de"
  "3791ae24-c304-4a88-aaa4-af1fcd93ab71:SEO-User-20:gb"
)

OK=0
FAIL=0

for entry in "${PROFILES[@]}"; do
  PID=$(echo "$entry" | cut -d: -f1)
  NAME=$(echo "$entry" | cut -d: -f2)
  COUNTRY=$(echo "$entry" | cut -d: -f3)

  # Get SOCKS5 proxy
  PROXY_RAW=$($XCLI proxy-get --country-code "$COUNTRY" --protocol socks5 --type sticky 2>&1)

  if [[ -z "$PROXY_RAW" || "$PROXY_RAW" == *"rror"* ]]; then
    echo "FAIL: $NAME ($COUNTRY) - proxy-get failed"
    FAIL=$((FAIL + 1))
    continue
  fi

  P_HOST=$(echo "$PROXY_RAW" | cut -d: -f1)
  P_PORT=$(echo "$PROXY_RAW" | cut -d: -f2)
  P_USER=$(echo "$PROXY_RAW" | cut -d: -f3)
  P_PASS=$(echo "$PROXY_RAW" | cut -d: -f4)

  # Update via MLX Cloud API
  RESULT=$(curl -s -X POST "https://api.multilogin.com/profile/update" \
    -H "Authorization: Bearer $MLX_TOKEN" \
    -H 'Content-Type: application/json' \
    -d "{
      \"profile_id\": \"$PID\",
      \"folder_id\": \"$FOLDER\",
      \"name\": \"$NAME\",
      \"browser_type\": \"mimic\",
      \"os_type\": \"windows\",
      \"parameters\": {
        \"fingerprint\": {},
        \"proxy\": {
          \"host\": \"$P_HOST\",
          \"port\": $P_PORT,
          \"username\": \"$P_USER\",
          \"password\": \"$P_PASS\",
          \"type\": \"socks5\",
          \"save_traffic\": false
        },
        \"flags\": {
          \"audio_masking\": \"natural\",
          \"canvas_noise\": \"natural\",
          \"fonts_masking\": \"mask\",
          \"geolocation_masking\": \"mask\",
          \"geolocation_popup\": \"prompt\",
          \"graphics_masking\": \"natural\",
          \"graphics_noise\": \"natural\",
          \"localization_masking\": \"mask\",
          \"media_devices_masking\": \"natural\",
          \"navigator_masking\": \"natural\",
          \"ports_masking\": \"mask\",
          \"proxy_masking\": \"custom\",
          \"quic_mode\": \"disabled\",
          \"screen_masking\": \"natural\",
          \"timezone_masking\": \"mask\",
          \"webrtc_masking\": \"mask\"
        },
        \"storage\": {
          \"is_local\": false,
          \"save_service_worker\": true
        }
      }
    }" 2>&1)

  if echo "$RESULT" | grep -q "successfully updated"; then
    echo "OK: $NAME ($COUNTRY) -> $P_HOST:$P_PORT"
    OK=$((OK + 1))
  else
    echo "FAIL: $NAME ($COUNTRY) -> $RESULT"
    FAIL=$((FAIL + 1))
  fi
done

echo ""
echo "===== Done: $OK ok, $FAIL failed ====="

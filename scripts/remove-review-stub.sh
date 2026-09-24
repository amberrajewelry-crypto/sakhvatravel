#!/bin/bash
set -uo pipefail
# Снятие временной заглушки отзывов (поставлена 28.06.2026, снять через сутки).
# Запускается one-shot через launchd 29.06.2026 16:50.

cd "$HOME/sakhva-travel" || exit 1
LOG="$HOME/sakhva-travel/scripts/_remove-review-stub.log"
exec >>"$LOG" 2>&1
echo "===== $(date '+%Y-%m-%d %H:%M:%S %Z') START ====="

notify() { osascript -e "display notification \"$1\" with title \"Sakhva: заглушка отзывов\"" 2>/dev/null || true; }

# 1. Удалить блок TEMP review-block (от комментария до первого </script>) в обоих файлах
for f in index.html en/index.html; do
  if grep -q "TEMP review-block" "$f"; then
    perl -0777 -i -pe 's/\n<!-- TEMP review-block.*?<\/script>//s' "$f"
    echo "removed stub from $f"
  else
    echo "no stub in $f (already clean)"
  fi
done

# 2. Predeploy-check
if ! node scripts/predeploy-check.js en/index.html index.html | grep -q "ошибок 0"; then
  echo "PREDEPLOY-CHECK FAILED — деплой отменён"
  notify "Ошибка predeploy-check, деплой отменён. См. лог."
  exit 1
fi
echo "predeploy-check OK"

# 3. Deploy
DEPLOY=$(npx vercel deploy --prod --scope amberrajewelry-cryptos-projects 2>&1 | grep -E "readyState|ready\." | tr '\n' ' ')
echo "deploy: $DEPLOY"

# 4. Verify на проде (блоков быть не должно)
sleep 5
RU=$(curl -s -L https://sakhva-travel.com/ | grep -c "TEMP review-block")
EN=$(curl -s -L https://sakhva-travel.com/en/ | grep -c "TEMP review-block")
echo "prod check: RU=$RU EN=$EN (ожидается 0/0)"

if [ "$RU" = "0" ] && [ "$EN" = "0" ]; then
  notify "Заглушка снята, ссылки на отзывы снова активны на проде."
  echo "SUCCESS"
else
  notify "Внимание: заглушка ещё видна на проде (RU=$RU EN=$EN). Проверь вручную."
  echo "WARN: stub still on prod"
fi

# 5. Самоудаление launchd-таймера
launchctl unload "$HOME/Library/LaunchAgents/com.vladimir.sakhva-remove-stub.plist" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/com.vladimir.sakhva-remove-stub.plist"
echo "===== DONE ====="

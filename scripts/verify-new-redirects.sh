#!/bin/bash
for path in \
  /ekskursiya/shopping-tour-tbilisi/ \
  /ekskursiya/transfer-iz-aeroporta-tbilisi/ \
  /ekskursiya/truso-valley-tour/ \
  /ekskursiya/vin-tour-tbilisi/ \
  /blog/car-rental-tbilisi/; do
  code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com${path}")
  echo "$code $path"
done

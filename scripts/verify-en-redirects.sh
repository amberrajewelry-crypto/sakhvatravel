#!/bin/bash
for path in \
  /en/ekskursiya/vardzia-tour/ \
  /en/ekskursiya/wine-tour-tbilisi/ \
  /en/ekskursiya/kazbegi-tour-from-tbilisi/ \
  /en/ekskursiya/sighnaghi-tour-from-tbilisi/ \
  /en/ekskursiya/truso-valley-tour/ \
  /en/ekskursiya/shopping-tour-tbilisi/ \
  /en/ekskursiya/gori-tour-from-tbilisi/ \
  /en/ekskursiya/jvari-tour-from-tbilisi/; do
  code=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" "https://sakhva-travel.com${path}")
  echo "$code $path"
done

#!/bin/sh
# Passa il sito dalla modalità DEMO a quella definitiva.
#   ./go-live.sh                      -> spegne la demo
#   ./go-live.sh https://dominio.it   -> spegne la demo e imposta il dominio definitivo
# Cosa fa, in index.html e privacy.html:
#   1. data-demo="on"  ->  data-demo="off"  (nasconde barra, filigrana, badge e righe "Tramontis"/demo)
#   2. toglie <meta name="robots" content="noindex, nofollow">
#   3. toglie il prefisso "[DEMO] " dal <title>
#   4. (opzionale) sostituisce https://www.colosseumazzate.it con il dominio indicato
set -eu
cd "$(dirname "$0")"

for f in index.html privacy.html; do
  sed -i \
    -e 's/data-demo="on"/data-demo="off"/' \
    -e '/id="demo-robots"/d' \
    -e '/<!-- DEMO: rimuovere con go-live.sh/d' \
    -e 's/<title>\[DEMO\] /<title>/' \
    "$f"
done

if [ "${1:-}" != "" ]; then
  NEW=$(printf '%s' "$1" | sed 's#/*$##')
  for f in index.html robots.txt sitemap.xml; do
    sed -i "s#https://www.colosseumazzate.it#$NEW#g" "$f"
  done
  echo "Dominio impostato: $NEW"
fi

echo "Demo disattivata. Controlla index.html: data-demo=\"off\", niente noindex."

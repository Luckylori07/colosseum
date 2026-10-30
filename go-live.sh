#!/bin/sh
# Passa il sito dalla modalità DEMO a quella definitiva.
#   ./go-live.sh                         -> spegne la demo
#   ./go-live.sh https://www.dominio.it  -> spegne la demo e imposta il dominio definitivo
#   ./go-live.sh --force ...             -> ignora i controlli preliminari (sconsigliato)
# Cosa fa, in tutte le pagine .html:
#   1. data-demo="on" -> "off"  (nasconde barra e righe di credito/demo)
#   2. toglie <meta name="robots" content="noindex, nofollow"> (resta il noindex della 404)
#   3. toglie il prefisso "[DEMO] " dal <title>
#   4. (opzionale) sostituisce https://www.colosseumazzate.it in pagine, robots, sitemap, web.config
# Prima di tutto controlla che non restino dati da completare.
set -eu
cd "$(dirname "$0")"

FORCE=0; DOMAIN=""
for a in "$@"; do
  case "$a" in
    --force) FORCE=1 ;;
    *) DOMAIN="$a" ;;
  esac
done

if [ "$FORCE" -eq 0 ]; then
  PROBLEMS=0
  if grep -l "TODO-LEGALE" ./*.html >/dev/null 2>&1; then
    echo "STOP: nel footer manca ancora REA / capitale sociale / Registro Imprese (cerca TODO-LEGALE nei file .html, compila e cancella il commento)."; PROBLEMS=1
  fi
  if grep -l "data-price-slot" ./*.html >/dev/null 2>&1; then
    echo "STOP: ci sono ancora prezzi segnaposto in abbonamenti.html (data-price-slot)."; PROBLEMS=1
  fi
  if [ "$PROBLEMS" -ne 0 ]; then echo "Correggi e rilancia, oppure usa --force."; exit 1; fi
fi

for f in ./*.html; do
  sed -i \
    -e 's/data-demo="on"/data-demo="off"/' \
    -e '/id="demo-robots"/d' \
    -e '/<!-- DEMO: rimuovere con go-live.sh/d' \
    -e 's/<title>\[DEMO\] /<title>/' \
    "$f"
done

if [ -n "$DOMAIN" ]; then
  NEW=$(printf '%s' "$DOMAIN" | sed 's#/*$##')
  for f in ./*.html robots.txt sitemap.xml web.config; do
    sed -i "s#https://www.colosseumazzate.it#$NEW#g" "$f"
  done
  echo "Dominio impostato: $NEW"
fi

echo "Demo disattivata. Ora lancia ./make-dist.sh e carica il contenuto di dist/."

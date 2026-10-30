#!/bin/sh
# Prepara la cartella "dist/" (e dist.zip) con SOLO i file da pubblicare:
# niente README, script, .git, .claude o altri file di lavoro.
set -eu
cd "$(dirname "$0")"
rm -rf dist dist.zip
mkdir dist
cp *.html robots.txt sitemap.xml web.config _headers _redirects dist/
cp -r assets dist/assets
if command -v zip >/dev/null 2>&1; then (cd dist && zip -qr ../dist.zip .); echo "Creato dist.zip"; fi
echo "Cartella dist/ pronta: $(find dist -type f | wc -l) file, $(du -sh dist | cut -f1)"

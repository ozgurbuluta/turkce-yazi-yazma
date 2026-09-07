#!/usr/bin/env bash
# Sıklık listelerini ve isteğe bağlı külliyatları indirir, kırpılmış sürümleri
# skills/turkce-yazi/data/ altına yazar. Ham indirmeler tools/cache/ altında
# kalır (gitignore'da).
#
# Kullanım:
#   tools/fetch_data.sh            # yalnızca sıklık listeleri (paketle gelen)
#   tools/fetch_data.sh --hepsi    # + Leipzig cümle dosyaları, TurBLiMP (commit edilmez)
set -euo pipefail

KOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="$KOK/tools/cache"
HEDEF="$KOK/skills/turkce-yazi/data"
mkdir -p "$CACHE" "$HEDEF"

LEIPZIG_AD="tur_news_2024_30K"
LEIPZIG_URL="https://downloads.wortschatz-leipzig.de/corpora/${LEIPZIG_AD}.tar.gz"
HERMITDAVE_URL="https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/tr/tr_50k.txt"

indir() {
  local url="$1" hedef="$2"
  if [ -s "$hedef" ]; then
    echo "var: $hedef"
  else
    echo "indiriliyor: $url"
    curl -sSL --fail --max-time 300 -o "$hedef" "$url"
  fi
}

indir "$HERMITDAVE_URL" "$CACHE/tr_50k.txt"
indir "$LEIPZIG_URL" "$CACHE/${LEIPZIG_AD}.tar.gz"

if [ ! -f "$CACHE/${LEIPZIG_AD}/${LEIPZIG_AD}-words.txt" ]; then
  tar xzf "$CACHE/${LEIPZIG_AD}.tar.gz" -C "$CACHE"
fi

python3 "$KOK/tools/trim_lists.py" \
  --konusma "$CACHE/tr_50k.txt" \
  --yazili "$CACHE/${LEIPZIG_AD}/${LEIPZIG_AD}-words.txt" \
  --hedef "$HEDEF"

if [ "${1:-}" = "--hepsi" ]; then
  mkdir -p "$KOK/corpus/leipzig" "$KOK/corpus/turblimp"
  cp "$CACHE/${LEIPZIG_AD}/${LEIPZIG_AD}-sentences.txt" "$KOK/corpus/leipzig/"
  for ad in tur_wikipedia_2021_30K tur_web_2019_30K; do
    indir "https://downloads.wortschatz-leipzig.de/corpora/${ad}.tar.gz" "$CACHE/${ad}.tar.gz" || true
    tar xzf "$CACHE/${ad}.tar.gz" -C "$CACHE" 2>/dev/null || true
    cp "$CACHE/${ad}/${ad}-sentences.txt" "$KOK/corpus/leipzig/" 2>/dev/null || true
  done
  echo "TurBLiMP için: https://github.com/ezgibasar/TurBLiMP (CC BY 4.0) — corpus/turblimp/ altına klonlayın."
fi

echo "bitti."

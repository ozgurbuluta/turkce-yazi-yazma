#!/usr/bin/env python3
"""Ham sıklık listelerini kırpıp skill içinde dağıtılan TSV biçimine çevirir.

Çıktı biçimi (iki dosya da aynı): kelime<TAB>sayı<TAB>sıra
"""
import argparse
import re
from collections import Counter
from pathlib import Path

HARF = re.compile(r"^[a-zçğıöşüâîû']+$")


def tr_lower(s: str) -> str:
    # Düzeltme işaretli biçimler (hâlâ, zekâ) düz biçime katlanır; sayımlar birleşir.
    return s.replace("I", "ı").replace("İ", "i").lower().translate(str.maketrans("âîû", "aiu"))


def yaz(sayac: Counter, hedef: Path, ust: int, baslik: str) -> None:
    with hedef.open("w", encoding="utf-8") as f:
        f.write(f"# {baslik}\n")
        for sira, (kelime, sayi) in enumerate(sayac.most_common(ust), 1):
            f.write(f"{kelime}\t{sayi}\t{sira}\n")
    print(f"{hedef}: {min(ust, len(sayac))} satır")


def konusma(kaynak: Path) -> Counter:
    sayac: Counter = Counter()
    for satir in kaynak.open(encoding="utf-8"):
        parca = satir.split()
        if len(parca) != 2:
            continue
        kelime = tr_lower(parca[0])
        if HARF.match(kelime):
            sayac[kelime] += int(parca[1])
    return sayac


def yazili(kaynak: Path, en_az: int) -> Counter:
    sayac: Counter = Counter()
    for satir in kaynak.open(encoding="utf-8"):
        parca = satir.rstrip("\n").split("\t")
        if len(parca) != 3:
            continue
        kelime = tr_lower(parca[1])
        sayi = int(parca[2])
        if sayi >= en_az and HARF.match(kelime):
            sayac[kelime] += sayi
    return sayac


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--konusma", type=Path, required=True, help="hermitdave tr_50k.txt")
    ap.add_argument("--yazili", type=Path, required=True, help="Leipzig *-words.txt")
    ap.add_argument("--hedef", type=Path, required=True)
    ap.add_argument("--ust", type=int, default=30000)
    ap.add_argument("--en-az", type=int, default=2)
    a = ap.parse_args()

    yaz(
        konusma(a.konusma),
        a.hedef / "siklik_konusma.tsv",
        a.ust,
        "Kaynak: hermitdave/FrequencyWords, OpenSubtitles 2018 tr — CC BY-SA 4.0. Sütunlar: kelime, sayı, sıra",
    )
    yaz(
        yazili(a.yazili, a.en_az),
        a.hedef / "siklik_yazili.tsv",
        a.ust,
        "Kaynak: Leipzig Corpora Collection tur_news_2024_30K — CC BY 4.0. Sütunlar: kelime, sayı, sıra",
    )


if __name__ == "__main__":
    main()

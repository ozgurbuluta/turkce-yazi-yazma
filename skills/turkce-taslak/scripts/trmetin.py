"""Türkçe metin için ortak yardımcılar: küçük harf, hece, cümle/paragraf/kelime bölme.

Yalnızca standart kütüphane. Aynı dosya kisisel-ses ve turkce-taslak skill'lerinde
de bulunur; her klasör kendi başına çalışsın diye kopyalanmıştır (tests/ birebir
aynı olduklarını denetler).
"""
import json
import re
import sys
from pathlib import Path

SESLI = set("aeıioöuüâîû")
KELIME_RE = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû]+(?:'[A-Za-zÇĞİÖŞÜçğıöşüÂÎÛâîû]+)?")
BUYUK_RE = re.compile(r"[A-ZÇĞİÖŞÜÂÎÛ]")
CUMLE_SONU = "[.!?…]"
KAPANIS = "[\"”’')\\]»]*"
ACILIS = "[\"“‘'(\\[«]?"

BAGLACLAR = [
    "ancak", "fakat", "ayrıca", "bununla birlikte", "öte yandan", "dolayısıyla",
    "bu nedenle", "bu yüzden", "bu sebeple", "sonuç olarak", "özellikle", "aslında",
    "üstelik", "ne var ki", "oysa", "oysaki", "yani", "böylece", "buna karşın",
    "buna ek olarak", "bunun yanı sıra", "elbette", "kısacası", "örneğin", "nitekim",
    "hatta", "zira", "çünkü", "ama", "ve", "bu bağlamda", "bu doğrultuda", "bu noktada",
    "peki", "işte", "öncelikle", "son olarak", "ilk olarak", "genel olarak", "özetle",
    "diğer yandan", "halbuki", "gerçekten de", "tabii", "tabii ki", "nihayetinde",
]

_VARSAYILAN_KISALTMALAR = {
    "dr", "prof", "doç", "yrd", "öğr", "gör", "uzm", "av", "sn", "hz", "vb", "vs", "vd",
    "bkz", "örn", "yy", "s", "c", "no", "sok", "cad", "mah", "apt", "t.c", "a.ş", "ltd",
    "şti", "mr", "mrs", "ms", "st", "km", "cm", "kg", "tel", "m.ö", "m.s",
}


def tr_lower(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


def tr_upper_mi(ch: str) -> bool:
    return bool(BUYUK_RE.match(ch))


def hece_sayisi(kelime: str) -> int:
    n = sum(1 for ch in tr_lower(kelime) if ch in SESLI)
    return max(1, n)


def kisaltmalari_yukle(yol=None) -> set:
    if yol is None:
        aday = Path(__file__).resolve().parent.parent / "data" / "kisaltmalar.txt"
        if not aday.exists():
            return set(_VARSAYILAN_KISALTMALAR)
        yol = aday
    kume = set(_VARSAYILAN_KISALTMALAR)
    for satir in Path(yol).read_text(encoding="utf-8").splitlines():
        satir = satir.strip()
        if satir and not satir.startswith("#"):
            kume.add(tr_lower(satir).rstrip("."))
    return kume


def markdown_temizle(metin: str) -> str:
    metin = re.sub(r"```.*?```", " ", metin, flags=re.S)
    metin = re.sub(r"^\s{0,3}#{1,6}\s+", "", metin, flags=re.M)
    metin = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", metin, flags=re.M)
    metin = re.sub(r"^\s*>\s?", "", metin, flags=re.M)
    metin = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", metin)
    metin = re.sub(r"[*_]{1,3}([^*_\n]+)[*_]{1,3}", r"\1", metin)
    metin = re.sub(r"`([^`\n]+)`", r"\1", metin)
    metin = re.sub(r"^\s*[-*_]{3,}\s*$", "", metin, flags=re.M)
    return metin


def paragraflara_bol(metin: str) -> list:
    parcalar = re.split(r"\n\s*\n", metin.strip())
    return [p.strip() for p in parcalar if p.strip()]


def cumlelere_bol(metin: str, kisaltmalar=None) -> list:
    if kisaltmalar is None:
        kisaltmalar = kisaltmalari_yukle()
    cumleler = []
    for satir in metin.splitlines():
        satir = satir.strip()
        if not satir:
            continue
        bas = 0
        for m in re.finditer(r"\s+", satir):
            once = satir[bas:m.start()]
            sonra = satir[m.end():m.end() + 2]
            if not re.search(CUMLE_SONU + KAPANIS + "$", once):
                continue
            if not sonra or not re.match(ACILIS + r"[A-ZÇĞİÖŞÜÂÎÛ0-9]", sonra):
                continue
            son_kelime = re.search(r"([\wçğıöşüâîû.]+)\.[\"”’')\]»]*$", once)
            if son_kelime:
                sk = tr_lower(son_kelime.group(1)).rstrip(".")
                if sk in kisaltmalar or (len(sk) == 1 and not sk.isdigit()):
                    continue
            cumleler.append(once.strip())
            bas = m.end()
        kalan = satir[bas:].strip()
        if kalan:
            cumleler.append(kalan)
    return cumleler


def kelimeler(metin: str) -> list:
    return KELIME_RE.findall(metin)


def dosya_oku(yol: str) -> str:
    if yol == "-" or yol is None:
        return sys.stdin.read()
    return Path(yol).read_text(encoding="utf-8")


def yaz(sonuc: dict, json_mu: bool, ozet: str) -> None:
    if json_mu:
        print(json.dumps(sonuc, ensure_ascii=False, indent=2))
    else:
        print(ozet)


def bin_basina(sayi: int, kelime: int) -> float:
    return round(1000.0 * sayi / kelime, 2) if kelime else 0.0


def yuz_basina(sayi: int, kelime: int) -> float:
    return round(100.0 * sayi / kelime, 2) if kelime else 0.0


def ortalama(xs) -> float:
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def std(xs) -> float:
    xs = list(xs)
    if len(xs) < 2:
        return 0.0
    m = ortalama(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def cv(xs) -> float:
    m = ortalama(xs)
    return round(std(xs) / m, 3) if m else 0.0

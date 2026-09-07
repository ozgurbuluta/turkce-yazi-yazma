#!/usr/bin/env python3
"""Göreve en yakın k onaylanmış metni seçer (TF-IDF kosinüs, stdlib).

Kullanım:
  python3 ornek_sec.py --gorev "uzaktan çalışma, ofise dönüş, plaza" --tur deneme -k 3
  python3 ornek_sec.py --gorev-dosya brief.md --tur reel -k 2 --tam
  python3 ornek_sec.py --gorev "..." --json

Türkçe için gövde: sözcüğün ilk 6 harfi (ek soymadan kaba ama işe yarar kök).
Aynı türden metinler her zaman önce gelir; tür verilmezse ya da aynı türden k
metin yoksa diğer türler de girer (benzerlik 0,7 ile çarpılır, "farklı tür" etiketiyle).
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import kelimeler, markdown_temizle, tr_lower  # noqa: E402

DURAK = set("""
ve bir bu da de ile için çok daha o ne gibi ben sen biz siz onlar şu ama ki mi mı mu mü en ya her hem ise var yok değil
kadar sonra önce göre olan olarak olduğu diye hiç ancak fakat çünkü artık bile hep şey şeyi şeyler bunu bunun buna bundan
onu onun ona ama zaten belki yani şimdi böyle öyle nasıl neden kim hangi bütün tüm başka aynı kendi
""".split())


def frontmatter(metin: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", metin, flags=re.S)
    if not m:
        return {}, metin
    meta = {}
    for satir in m.group(1).splitlines():
        if ":" in satir:
            k, v = satir.split(":", 1)
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
            meta[k.strip()] = v
    return meta, metin[m.end():]


def govdeler(metin: str) -> Counter:
    c = Counter()
    for k in kelimeler(markdown_temizle(metin)):
        k = tr_lower(k.split("'")[0])
        if len(k) < 3 or k in DURAK:
            continue
        c[k[:6]] += 1
    return c


def tfidf(dokumanlar: list) -> list:
    df = Counter()
    for d in dokumanlar:
        df.update(d.keys())
    n = len(dokumanlar)
    vek = []
    for d in dokumanlar:
        toplam = sum(d.values()) or 1
        vek.append({t: (f / toplam) * (math.log((n + 1) / (df[t] + 1)) + 1) for t, f in d.items()})
    return vek


def kosinus(a: dict, b: dict) -> float:
    pay = sum(v * b.get(t, 0) for t, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return pay / (na * nb) if na and nb else 0.0


def sec(gorev: str, arsiv: Path, tur=None, k=3, eski_haric=False) -> list:
    kayitlar = []
    for yol in sorted(arsiv.rglob("*.md")):
        meta, govde = frontmatter(yol.read_text(encoding="utf-8"))
        t = meta.get("tür") or meta.get("tur") or yol.parent.name
        etiket = meta.get("etiketler", [])
        if isinstance(etiket, str):
            etiket = [x.strip() for x in etiket.split(",")]
        if eski_haric and "eski" in etiket:
            continue
        kayitlar.append({"yol": str(yol), "tur": t, "tarih": meta.get("tarih", ""), "konu": meta.get("konu", ""), "etiketler": etiket, "govde": govde.strip()})
    if not kayitlar:
        return []
    dok = [govdeler(r["govde"] + " " + r["konu"] + " " + " ".join(r["etiketler"])) for r in kayitlar]
    vek = tfidf(dok + [govdeler(gorev)])
    g = vek[-1]
    for r, v in zip(kayitlar, vek[:-1]):
        ham = kosinus(g, v)
        r["benzerlik"] = round(ham if (tur is None or r["tur"] == tur) else ham * 0.7, 3)
        r["ayni_tur"] = tur is None or r["tur"] == tur
    kayitlar.sort(key=lambda r: (not r["ayni_tur"], -r["benzerlik"], r["tarih"]))
    return kayitlar[:k]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--gorev", help="konu / brief metni")
    g.add_argument("--gorev-dosya", type=Path)
    ap.add_argument("--arsiv", type=Path, default=Path("voice/onaylanan"))
    ap.add_argument("--tur")
    ap.add_argument("-k", type=int, default=3)
    ap.add_argument("--tam", action="store_true", help="metinlerin tamamını bas (bağlama yapıştırmak için)")
    ap.add_argument("--eski-haric", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.arsiv.exists():
        sys.exit(f"arşiv yok: {a.arsiv}")
    gorev = a.gorev if a.gorev else a.gorev_dosya.read_text(encoding="utf-8")
    secilen = sec(gorev, a.arsiv, a.tur, a.k, a.eski_haric)
    if a.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "govde" or a.tam} for r in secilen], ensure_ascii=False, indent=2))
        return
    if not secilen:
        print("arşivde metin yok")
        return
    for i, r in enumerate(secilen, 1):
        print(f"[Örnek {i} — {r['tur']}, {r['tarih'] or 'tarihsiz'}, konu: {r['konu'] or '-'}; benzerlik {r['benzerlik']}{'' if r['ayni_tur'] else ', farklı tür'}] {r['yol']}")
        if a.tam:
            print(r["govde"] + "\n")
        else:
            print("  " + r["govde"][:200].replace("\n", " ") + ("..." if len(r["govde"]) > 200 else ""))


if __name__ == "__main__":
    main()

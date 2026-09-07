#!/usr/bin/env python3
"""AI kalıbı ve çeviri kokusu taraması.

data/ai_kaliplari.tsv ve data/ceviri_kokusu.tsv içindeki düzenli ifadeleri cümle
cümle uygular; her bulgu için cümle, kategori, şiddet ve düzeltme ipucu verir.
0-100 arası "iz puanı" üretir (0 temiz, 100 makine kokusu).

Kullanım:
  python3 kalip_tara.py metin.md
  python3 kalip_tara.py metin.md --liste ceviri --json
  python3 kalip_tara.py metin.md --ek voice/tercihler.tsv   # kişisel yasak listesi
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import cumlelere_bol, dosya_oku, kelimeler, kisaltmalari_yukle, markdown_temizle, paragraflara_bol, tr_lower, yaz  # noqa: E402

VERI = Path(__file__).resolve().parent.parent / "data"
LISTELER = {"ai": VERI / "ai_kaliplari.tsv", "ceviri": VERI / "ceviri_kokusu.tsv"}
BANTLAR = [(15, "temiz"), (35, "hafif iz"), (60, "belirgin iz"), (85, "yoğun iz"), (100, "makine kokusu")]
CARPAN = 100 / 60  # 1000 kelime başına 60 ağırlık puanı = 100


def tsv_yukle(yol: Path, kaynak: str) -> list:
    kaliplar = []
    for no, satir in enumerate(yol.read_text(encoding="utf-8").splitlines(), 1):
        if not satir.strip() or satir.startswith("#"):
            continue
        parca = satir.rstrip("\n").split("\t")
        if len(parca) < 4:
            print(f"uyarı: {yol.name}:{no} eksik sütun, atlandı", file=sys.stderr)
            continue
        try:
            rx = re.compile(parca[0], re.M)
        except re.error as e:
            print(f"uyarı: {yol.name}:{no} geçersiz regex ({e}), atlandı", file=sys.stderr)
            continue
        kaliplar.append({"rx": rx, "kalip": parca[0], "kategori": parca[1], "siddet": int(parca[2]), "ipucu": parca[3], "kaynak": kaynak})
    return kaliplar


def bant(puan: float) -> str:
    for ust, ad in BANTLAR:
        if puan <= ust:
            return ad
    return BANTLAR[-1][1]


def tara(metin: str, kaliplar: list) -> dict:
    metin = markdown_temizle(metin)
    kisaltmalar = kisaltmalari_yukle()
    n_kel = len(kelimeler(metin))
    bulgular = []
    for p_no, paragraf in enumerate(paragraflara_bol(metin), 1):
        for cumle in cumlelere_bol(paragraf, kisaltmalar):
            kucuk = tr_lower(cumle)
            for k in kaliplar:
                for m in k["rx"].finditer(kucuk):
                    bulgular.append({
                        "paragraf": p_no,
                        "cumle": cumle,
                        "eslesen": m.group(0).strip(),
                        "kategori": k["kategori"],
                        "siddet": k["siddet"],
                        "ipucu": k["ipucu"],
                        "kaynak": k["kaynak"],
                    })
                    break  # aynı kalıp aynı cümlede bir kez sayılır
    agirlik = sum(b["siddet"] for b in bulgular)
    agirlik_bin = 1000 * agirlik / n_kel if n_kel else 0
    puan = min(100, round(agirlik_bin * CARPAN))
    alt = {}
    for kaynak in ("ai", "ceviri", "ek"):
        a = sum(b["siddet"] for b in bulgular if b["kaynak"] == kaynak)
        alt[kaynak] = min(100, round((1000 * a / n_kel if n_kel else 0) * CARPAN))
    return {
        "kelime": n_kel,
        "bulgu_sayisi": len(bulgular),
        "puan": puan,
        "bant": bant(puan),
        "alt_puan": alt,
        "kategori_sayilari": dict(Counter(b["kategori"] for b in bulgular).most_common()),
        "en_sik": [{"eslesen": e, "sayi": n} for e, n in Counter(e for _, e in {(b["cumle"], b["eslesen"]) for b in bulgular}).most_common(8)],
        "bulgular": sorted(bulgular, key=lambda b: (-b["siddet"], b["paragraf"])),
    }


def ozet(s: dict) -> str:
    satirlar = [
        f"AI/çeviri izi: {s['puan']}/100 ({s['bant']}) — AI kalıbı {s['alt_puan']['ai']}, çeviri kokusu {s['alt_puan']['ceviri']}"
        + (f", kişisel yasaklar {s['alt_puan']['ek']}" if s["alt_puan"].get("ek") else "")
        + f"; {s['bulgu_sayisi']} bulgu / {s['kelime']} kelime",
    ]
    if s["kategori_sayilari"]:
        satirlar.append("Kategoriler: " + ", ".join(f"{k} {v}" for k, v in s["kategori_sayilari"].items()))
    if s["en_sik"]:
        satirlar.append("En sık: " + ", ".join(f"\"{e['eslesen']}\" ×{e['sayi']}" for e in s["en_sik"]))
    if s["bulgular"]:
        satirlar.append("Bulgular (şiddete göre):")
    for b in s["bulgular"]:
        c = b["cumle"] if len(b["cumle"]) <= 140 else b["cumle"][:137] + "..."
        satirlar.append(f"  [{b['siddet']}] ¶{b['paragraf']} \"{b['eslesen']}\" ({b['kategori']}): {c}")
        satirlar.append(f"      → {b['ipucu']}")
    return "\n".join(satirlar)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?", default="-")
    ap.add_argument("--liste", choices=["ai", "ceviri", "hepsi"], default="hepsi")
    ap.add_argument("--ek", type=Path, action="append", default=[], help="ek TSV (ör. voice/tercihler.tsv)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    kaliplar = []
    for ad, yol in LISTELER.items():
        if a.liste in ("hepsi", ad):
            kaliplar += tsv_yukle(yol, ad)
    for yol in a.ek:
        if yol.exists():
            kaliplar += tsv_yukle(yol, "ek")
        else:
            print(f"uyarı: {yol} yok, atlandı", file=sys.stderr)
    sonuc = tara(dosya_oku(a.dosya), kaliplar)
    yaz(sonuc, a.json, ozet(sonuc))


if __name__ == "__main__":
    main()

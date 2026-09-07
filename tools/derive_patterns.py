#!/usr/bin/env python3
"""LLM külliyatı ile insan külliyatını karşılaştırıp kalıp adayları ve metrik eşikleri üretir.

1. n-gram (1-3) log-odds (Monroe ve ark. 2008, Dirichlet önselli) → LLM tarafında
   aşırı temsil edilen ifadeler, z-skoruna göre sıralı: corpus/aday_kaliplar.tsv.
   Elle gözden geçirilip skills/turkce-editor/data/ai_kaliplari.tsv'ye eklenir.
2. İnsan ve LLM metinlerinde metrik dağılımları (Ateşman, cümle CV, -maktadır payı,
   bağlaç başı, "bir" oranı...) ve yüzdelikleri: corpus/esikler.json. metrik.py
   içindeki TUR_HEDEF ve uyarı eşikleri buna göre elle güncellenir.

Kullanım:
  python3 tools/derive_patterns.py --llm corpus/llm --insan corpus/leipzig --insan-belgeler corpus/insan_belgeler
  --insan: Leipzig *-sentences.txt dosyaları (cümle düzeyi, n-gram için)
  --insan-belgeler: paragraflı gerçek metinler (belge düzeyi metrikler için; isteğe bağlı)
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "skills" / "turkce-editor" / "scripts"))
from trmetin import kelimeler, tr_lower  # noqa: E402
import metrik  # noqa: E402


def belgeler(klasor: Path, sentences=False) -> list:
    metinler = []
    for yol in sorted(klasor.rglob("*")):
        if not yol.is_file() or yol.suffix not in (".txt", ".md"):
            continue
        if sentences or yol.name.endswith("-sentences.txt"):
            for satir in yol.read_text(encoding="utf-8", errors="ignore").splitlines():
                p = satir.split("\t", 1)
                metinler.append(p[1] if len(p) == 2 else p[0])
        else:
            metinler.append(yol.read_text(encoding="utf-8", errors="ignore"))
    return metinler


def ngramlar(metinler: list, n_max=3) -> Counter:
    c = Counter()
    for m in metinler:
        kel = [tr_lower(k) for k in kelimeler(m)]
        for n in range(1, n_max + 1):
            for i in range(len(kel) - n + 1):
                c[" ".join(kel[i:i + n])] += 1
    return c


def log_odds(a: Counter, b: Counter, onsel: Counter, alpha0=0.01) -> list:
    """Monroe, Colaresi, Quinn (2008): 'fightin' words' z-skorları; pozitif = a'da (LLM) fazla."""
    na, nb, n0 = sum(a.values()), sum(b.values()), sum(onsel.values())
    sonuc = []
    for g in set(a) | set(b):
        if a[g] + b[g] < 5:
            continue
        ag = alpha0 * n0 * (onsel[g] / n0) if n0 else alpha0
        da = math.log((a[g] + ag) / (na + alpha0 * n0 - a[g] - ag))
        db = math.log((b[g] + ag) / (nb + alpha0 * n0 - b[g] - ag))
        var = 1 / (a[g] + ag) + 1 / (b[g] + ag)
        sonuc.append((g, (da - db) / math.sqrt(var), a[g], b[g]))
    sonuc.sort(key=lambda x: -x[1])
    return sonuc


def yuzdelikler(xs: list) -> dict:
    if not xs:
        return {}
    s = sorted(xs)
    return {f"p{p}": round(s[min(len(s) - 1, int(p / 100 * len(s)))], 3) for p in (5, 10, 25, 50, 75, 90, 95)}


def metrikler(metinler: list) -> dict:
    alanlar = {"atesman": [], "cumle_cv": [], "cumle_ort": [], "maktadir": [], "dir": [], "baglac_basi": [], "bir_yuz": [], "tarafindan_bin": [], "adlastirma_bin": [], "cesitlilik": []}
    for m in metinler:
        s = metrik.hesapla(m)
        if "hata" in s or s["cumle"] < 5:
            continue
        alanlar["atesman"].append(s["okunabilirlik"]["atesman"])
        alanlar["cumle_cv"].append(s["cumle_uzunlugu"]["cv"])
        alanlar["cumle_ort"].append(s["cumle_uzunlugu"]["ortalama"])
        alanlar["maktadir"].append(s["yuklem"]["paylar"].get("-maktadır", 0))
        alanlar["dir"].append(s["yuklem"]["paylar"].get("-dır", 0))
        alanlar["baglac_basi"].append(s["ceviri_izleri"]["baglac_basi_pay"])
        alanlar["bir_yuz"].append(s["ceviri_izleri"]["bir_yuz"])
        alanlar["tarafindan_bin"].append(s["ceviri_izleri"]["tarafindan_bin"])
        alanlar["adlastirma_bin"].append(s["ceviri_izleri"]["adlastirma_bin"])
        alanlar["cesitlilik"].append(s["yuklem"]["cesitlilik"])
    return {k: {"n": len(v), **yuzdelikler(v)} for k, v in alanlar.items()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--llm", type=Path, default=KOK / "corpus" / "llm")
    ap.add_argument("--insan", type=Path, default=KOK / "corpus" / "leipzig")
    ap.add_argument("--insan-belgeler", type=Path)
    ap.add_argument("--ust", type=int, default=400)
    ap.add_argument("--cikti", type=Path, default=KOK / "corpus")
    a = ap.parse_args()

    llm = belgeler(a.llm)
    insan = belgeler(a.insan)
    if not llm or not insan:
        sys.exit(f"külliyat boş: llm={len(llm)} insan={len(insan)} (tools/generate_corpus.py ve tools/fetch_data.sh --hepsi)")
    print(f"LLM {len(llm)} belge, insan {len(insan)} cümle/belge")

    ng_llm, ng_insan = ngramlar(llm), ngramlar(insan)
    onsel = ng_llm + ng_insan
    aday = log_odds(ng_llm, ng_insan, onsel)
    a.cikti.mkdir(exist_ok=True)
    with (a.cikti / "aday_kaliplar.tsv").open("w", encoding="utf-8") as f:
        f.write("#ngram\tz\tllm_sayi\tinsan_sayi\tllm_bin\tinsan_bin\n")
        nl, ni = sum(ng_llm.values()), sum(ng_insan.values())
        for g, z, ca, cb in aday[:a.ust]:
            f.write(f"{g}\t{z:.2f}\t{ca}\t{cb}\t{1000 * ca / nl:.3f}\t{1000 * cb / ni:.3f}\n")
    print(f"aday kalıplar → {a.cikti / 'aday_kaliplar.tsv'} (ilk 20):")
    for g, z, ca, cb in aday[:20]:
        print(f"  {z:6.1f}  {g}  ({ca} / {cb})")

    esik = {"llm": metrikler(llm)}
    if a.insan_belgeler and a.insan_belgeler.exists():
        esik["insan"] = metrikler(belgeler(a.insan_belgeler))
    else:
        print("uyarı: --insan-belgeler yok; insan belge düzeyi metrikleri hesaplanmadı (Leipzig cümleleri karışık, belge ritmi vermez)")
    (a.cikti / "esikler.json").write_text(json.dumps(esik, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"eşikler → {a.cikti / 'esikler.json'}")


if __name__ == "__main__":
    main()

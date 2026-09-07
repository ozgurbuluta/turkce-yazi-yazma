#!/usr/bin/env python3
"""Türkçe metin metrikleri: okunabilirlik, ritim, yüklem çeşitliliği, çeviri izleri.

Kullanım:
  python3 metrik.py metin.md            # Türkçe özet
  python3 metrik.py metin.md --json     # makine okur JSON
  python3 metrik.py - --tur reel < metin.txt

Yalnızca standart kütüphane.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import (BAGLACLAR, bin_basina, cumlelere_bol, cv, dosya_oku, hece_sayisi,  # noqa: E402
                     kelimeler, kisaltmalari_yukle, markdown_temizle, ortalama,
                     paragraflara_bol, std, tr_lower, yaz, yuz_basina)

# Tür hedefleri; tur-profilleri skill'indeki profillerle aynı tutulur.
# Kalibrasyon: docs/yontem.md — Faz 6'da insan külliyatı yüzdelikleriyle güncellenir.
TUR_HEDEF = {
    "reel": {"atesman": (70, 95), "cumle_ort": (5, 12), "cv_min": 0.45, "kelime": (60, 220)},
    "deneme": {"atesman": (45, 75), "cumle_ort": (9, 18), "cv_min": 0.50, "kelime": (500, 1500)},
    "makale": {"atesman": (35, 60), "cumle_ort": (12, 20), "cv_min": 0.45, "kelime": (700, 2500)},
    "blog": {"atesman": (50, 75), "cumle_ort": (8, 16), "cv_min": 0.45, "kelime": (400, 1200)},
}

ZAMIRLER = {"ben", "biz", "siz", "sen", "onlar"}
EDILGEN_RE = re.compile(
    r"\w{2,}(ıl|il|ul|ül|ın|in|un|ün)(dı|di|du|dü|mış|miş|muş|müş|makta|mekte|ma|me|an|en|arak|erek|ır|ir|ur|ür|acak|ecek|malı|meli|sa|se)\w*$"
)
SOYUT_RE = re.compile(r"\w{3,}(lık|lik|luk|lük)\w*$")
ADLASTIRMA_RE = re.compile(r"\w{3,}(ması|mesi|masının|mesinin|masına|mesine|masıyla|mesiyle|maları|meleri)$")

YUKLEM_KURALLARI = [
    ("maktadir", re.compile(r"(makta|mekte)d[ıi]r(lar|ler)?$")),
    ("mistir", re.compile(r"(mış|miş|muş|müş)t[ıi]r(lar|ler)?$")),
    ("dir", re.compile(r"(dır|dir|dur|dür|tır|tir|tur|tür)(lar|ler)?$")),
    ("yor", re.compile(r"yor(um|sun|uz|sunuz|lar|)$")),
    ("di", re.compile(r"(dı|di|du|dü|tı|ti|tu|tü)(m|n|k|nız|niz|nuz|nüz|lar|ler|)$")),
    ("ecek", re.compile(r"((ecek|acak)(sın|sin|sınız|siniz|ler|lar|)|(eceğ|acağ)(im|ım|iz|ız))$")),
    ("mis", re.compile(r"(mış|miş|muş|müş)(ım|im|um|üm|sın|sin|ız|iz|lar|ler|)$")),
    ("meli", re.compile(r"(malı|meli)(yım|yim|sın|sin|yız|yiz|lar|ler|)$")),
    ("ir", re.compile(r"\w{2,}(ır|ir|ur|ür|ar|er)(ım|im|um|üm|sın|sin|ız|iz|lar|ler|)$")),
]

YUKLEM_ADI = {
    "maktadir": "-maktadır", "mistir": "-mıştır", "dir": "-dır", "yor": "-yor", "di": "-dı",
    "ecek": "-ecek", "mis": "-mış", "meli": "-meli", "ir": "-ır (geniş)", "soru": "soru", "diger": "diğer/ad",
}


def atesman_bant(puan: float) -> str:
    if puan >= 90:
        return "çok kolay"
    if puan >= 70:
        return "kolay"
    if puan >= 50:
        return "orta"
    if puan >= 30:
        return "zor"
    return "çok zor"


def bezirci_bant(puan: float) -> str:
    if puan <= 8:
        return "ilköğretim"
    if puan <= 12:
        return "lise"
    if puan <= 16:
        return "lisans"
    return "akademik"


def yuklem_turu(cumle: str) -> str:
    kel = kelimeler(cumle)
    if not kel:
        return "diger"
    son = tr_lower(kel[-1])
    if cumle.rstrip().endswith("?"):
        return "soru"
    for ad, rx in YUKLEM_KURALLARI:
        if rx.search(son):
            return ad
    return "diger"


def simpson_cesitlilik(sayac: Counter) -> float:
    n = sum(sayac.values())
    if n == 0:
        return 0.0
    return round(1 - sum((v / n) ** 2 for v in sayac.values()), 3)


def baglacla_basliyor(cumle: str) -> bool:
    c = tr_lower(cumle).lstrip("\"“‘'(")
    for b in BAGLACLAR:
        if c.startswith(b + " ") or c.startswith(b + ","):
            return True
    return False


def hesapla(metin: str, tur=None) -> dict:
    metin = markdown_temizle(metin)
    kisaltmalar = kisaltmalari_yukle()
    paragraflar = paragraflara_bol(metin)
    cumleler = cumlelere_bol(metin, kisaltmalar)
    kel = kelimeler(metin)
    kel_l = [tr_lower(k) for k in kel]
    n_kel = len(kel)
    n_cum = len(cumleler)

    if n_kel == 0 or n_cum == 0:
        return {"hata": "metin boş"}

    heceler = [hece_sayisi(k) for k in kel]
    hece_kelime = sum(heceler) / n_kel
    kelime_cumle = n_kel / n_cum
    atesman = 198.825 - 40.175 * hece_kelime - 2.610 * kelime_cumle
    atesman = max(0.0, min(100.0, atesman))

    cum_kel = [kelimeler(c) for c in cumleler]
    cum_uz = [len(c) for c in cum_kel]
    h3 = ortalama(sum(1 for k in c if hece_sayisi(k) == 3) for c in cum_kel)
    h4 = ortalama(sum(1 for k in c if hece_sayisi(k) == 4) for c in cum_kel)
    h5 = ortalama(sum(1 for k in c if hece_sayisi(k) == 5) for c in cum_kel)
    h6 = ortalama(sum(1 for k in c if hece_sayisi(k) >= 6) for c in cum_kel)
    bezirci = (kelime_cumle * (h3 * 0.84 + h4 * 1.5 + h5 * 3.5 + h6 * 26.25)) ** 0.5

    par_cum = [len(cumlelere_bol(p, kisaltmalar)) for p in paragraflar]
    par_kel = [len(kelimeler(p)) for p in paragraflar]

    yuklemler = Counter(yuklem_turu(c) for c in cumleler)
    yuklem_pay = {YUKLEM_ADI[k]: round(v / n_cum, 3) for k, v in yuklemler.most_common()}

    tarafindan = kel_l.count("tarafından")
    edilgen = sum(1 for k in kel_l if len(k) >= 6 and EDILGEN_RE.search(k))
    bir = kel_l.count("bir")
    zamir = sum(1 for k in kel_l if k in ZAMIRLER) + len(re.findall(r"(?:^|[.!?…]\s+)O,\s", metin, flags=re.M))
    soyut = sum(1 for k in kel_l if len(k) >= 6 and SOYUT_RE.search(k))
    adlastirma = sum(1 for k in kel_l if ADLASTIRMA_RE.search(k))
    baglac_bas = sum(1 for c in cumleler if baglacla_basliyor(c))
    bu_bas = sum(1 for c in cumleler if re.match(r"^[\"“‘'(]?bu\b", tr_lower(c)))

    sonuc = {
        "kelime": n_kel,
        "cumle": n_cum,
        "paragraf": len(paragraflar),
        "okunabilirlik": {
            "hece_kelime": round(hece_kelime, 2),
            "kelime_cumle": round(kelime_cumle, 2),
            "atesman": round(atesman, 1),
            "atesman_bant": atesman_bant(atesman),
            "bezirci_yilmaz": round(bezirci, 1),
            "bezirci_bant": bezirci_bant(bezirci),
        },
        "cumle_uzunlugu": {
            "ortalama": round(ortalama(cum_uz), 1),
            "std": round(std(cum_uz), 1),
            "cv": cv(cum_uz),
            "en_kisa": min(cum_uz),
            "en_uzun": max(cum_uz),
            "kisa_pay": round(sum(1 for u in cum_uz if u <= 6) / n_cum, 2),
            "uzun_pay": round(sum(1 for u in cum_uz if u >= 20) / n_cum, 2),
        },
        "paragraf_uzunlugu": {
            "ortalama_cumle": round(ortalama(par_cum), 1),
            "ortalama_kelime": round(ortalama(par_kel), 1),
            "cv_kelime": cv(par_kel),
            "tek_cumlelik": sum(1 for p in par_cum if p == 1),
        },
        "yuklem": {
            "paylar": yuklem_pay,
            "cesitlilik": simpson_cesitlilik(yuklemler),
        },
        "ceviri_izleri": {
            "tarafindan_bin": bin_basina(tarafindan, n_kel),
            "edilgen_bin_yaklasik": bin_basina(edilgen, n_kel),
            "bir_yuz": yuz_basina(bir, n_kel),
            "zamir_yuz": yuz_basina(zamir, n_kel),
            "soyut_ek_bin": bin_basina(soyut, n_kel),
            "adlastirma_bin": bin_basina(adlastirma, n_kel),
            "baglac_basi_pay": round(baglac_bas / n_cum, 2),
            "bu_basi_pay": round(bu_bas / n_cum, 2),
        },
        "uyarilar": [],
    }

    u = sonuc["uyarilar"]
    if n_cum >= 8 and sonuc["cumle_uzunlugu"]["cv"] < 0.35:
        u.append(f"Cümle uzunlukları tekdüze (CV={sonuc['cumle_uzunlugu']['cv']}). İnsan yazısında genelde 0,5 üstü: kısa cümleyi uzunun yanına koy.")
    if len(paragraflar) >= 4 and sonuc["paragraf_uzunlugu"]["cv_kelime"] < 0.25:
        u.append("Paragraflar aynı boyda. Birini tek cümleye indir, birini uzat.")
    if yuklem_pay.get("-maktadır", 0) > 0.15:
        u.append(f"Cümlelerin %{int(yuklem_pay['-maktadır'] * 100)}'i -maktadır ile bitiyor: rapor sesi. -yor / -ır / -dı ile değiştir.")
    if yuklem_pay.get("-dır", 0) > 0.4:
        u.append(f"Cümlelerin %{int(yuklem_pay['-dır'] * 100)}'i -dır ile bitiyor: tanım cümlesi üst üste. Bazılarını fiil cümlesi yap.")
    if yuklem_pay.get("-mıştır", 0) > 0.2:
        u.append("-mıştır yoğun: ansiklopedi sesi. -dı ya da -mış.")
    baskin = next(iter(yuklem_pay), None)
    if n_cum >= 8 and sonuc["yuklem"]["cesitlilik"] < 0.5 and baskin not in ("-dı", "-yor"):
        u.append(f"Yüklem çeşitliliği düşük ({sonuc['yuklem']['cesitlilik']}), baskın bitiş {baskin}. Aynı bitiş üst üste geliyor.")
    if sonuc["ceviri_izleri"]["tarafindan_bin"] > 2:
        u.append("'tarafından' sık: özneyi başa alıp etken yaz.")
    if sonuc["ceviri_izleri"]["edilgen_bin_yaklasik"] > 50:
        u.append(f"Edilgen fiil yoğun (~{sonuc['ceviri_izleri']['edilgen_bin_yaklasik']}/1000; haber dilinde ~35). Kim yaptı? Etken yaz.")
    if sonuc["ceviri_izleri"]["bir_yuz"] > 3.5:
        u.append(f"'bir' yoğun (%{sonuc['ceviri_izleri']['bir_yuz']}): İngilizce 'a' kopyası olanları sil.")
    if zamir >= 3 and sonuc["ceviri_izleri"]["zamir_yuz"] > 2.0:
        u.append("Açık özne zamiri sık (ben/biz/siz/o,): Türkçe zamiri düşürür; vurgu yoksa sil.")
    if sonuc["ceviri_izleri"]["baglac_basi_pay"] > 0.25:
        u.append(f"Cümlelerin %{int(sonuc['ceviri_izleri']['baglac_basi_pay'] * 100)}'i bağlaçla başlıyor. Bağlaçları sil; cümleler kendi kendine bağlansın.")
    if sonuc["ceviri_izleri"]["bu_basi_pay"] > 0.25:
        u.append("Çok cümle 'Bu' ile başlıyor: 'bu' neyi gösteriyor, adını yaz.")
    if sonuc["ceviri_izleri"]["adlastirma_bin"] > 15:
        u.append("Adlaştırma (-ması/-mesi) yoğun: fiile çevir.")

    if tur and tur in TUR_HEDEF:
        h = TUR_HEDEF[tur]
        sonuc["tur"] = tur
        sonuc["tur_hedef"] = h
        if not (h["atesman"][0] <= atesman <= h["atesman"][1]):
            u.append(f"[{tur}] Ateşman {atesman:.0f}, hedef {h['atesman'][0]}–{h['atesman'][1]}.")
        oc = sonuc["cumle_uzunlugu"]["ortalama"]
        if not (h["cumle_ort"][0] <= oc <= h["cumle_ort"][1]):
            u.append(f"[{tur}] Ortalama cümle {oc} kelime, hedef {h['cumle_ort'][0]}–{h['cumle_ort'][1]}.")
        if n_cum >= 6 and sonuc["cumle_uzunlugu"]["cv"] < h["cv_min"]:
            u.append(f"[{tur}] Ritim düz (CV {sonuc['cumle_uzunlugu']['cv']} < {h['cv_min']}).")
        if not (h["kelime"][0] <= n_kel <= h["kelime"][1]):
            u.append(f"[{tur}] {n_kel} kelime, hedef {h['kelime'][0]}–{h['kelime'][1]}.")
    return sonuc


def ozet(s: dict) -> str:
    if "hata" in s:
        return s["hata"]
    o, c, p, y, z = s["okunabilirlik"], s["cumle_uzunlugu"], s["paragraf_uzunlugu"], s["yuklem"], s["ceviri_izleri"]
    satirlar = [
        f"Metin: {s['kelime']} kelime, {s['cumle']} cümle, {s['paragraf']} paragraf" + (f" (tür: {s['tur']})" if "tur" in s else ""),
        f"Okunabilirlik: Ateşman {o['atesman']} ({o['atesman_bant']}), Bezirci-Yılmaz {o['bezirci_yilmaz']} ({o['bezirci_bant']}); {o['hece_kelime']} hece/kelime, {o['kelime_cumle']} kelime/cümle",
        f"Cümle ritmi: ortalama {c['ortalama']} kelime, std {c['std']}, CV {c['cv']}, aralık {c['en_kisa']}–{c['en_uzun']}; kısa (≤6) %{int(c['kisa_pay'] * 100)}, uzun (≥20) %{int(c['uzun_pay'] * 100)}",
        f"Paragraf: ortalama {p['ortalama_cumle']} cümle / {p['ortalama_kelime']} kelime, CV {p['cv_kelime']}, tek cümlelik {p['tek_cumlelik']}",
        "Yüklem payları: " + ", ".join(f"{k} %{int(v * 100)}" for k, v in y["paylar"].items()) + f"; çeşitlilik {y['cesitlilik']}",
        f"Çeviri izleri: tarafından {z['tarafindan_bin']}/1000, edilgen ~{z['edilgen_bin_yaklasik']}/1000, bir %{z['bir_yuz']}, zamir %{z['zamir_yuz']}, -lık {z['soyut_ek_bin']}/1000, -ması {z['adlastirma_bin']}/1000, bağlaçla başlayan %{int(z['baglac_basi_pay'] * 100)}, 'Bu' ile başlayan %{int(z['bu_basi_pay'] * 100)}",
    ]
    if s["uyarilar"]:
        satirlar.append("Uyarılar:")
        satirlar += [f"  - {u}" for u in s["uyarilar"]]
    else:
        satirlar.append("Uyarı yok.")
    return "\n".join(satirlar)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?", default="-", help="metin dosyası ya da - (stdin)")
    ap.add_argument("--tur", choices=sorted(TUR_HEDEF), help="tür hedefleriyle karşılaştır")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sonuc = hesapla(dosya_oku(a.dosya), a.tur)
    yaz(sonuc, a.json, ozet(sonuc))


if __name__ == "__main__":
    main()

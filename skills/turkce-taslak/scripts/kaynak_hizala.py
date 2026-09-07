#!/usr/bin/env python3
"""Kaynak-taslak hizalama: aynalama ve uydurma denetimi.

İngilizce (ya da Türkçe) bir kaynak metinle ondan yazılmış Türkçe taslağı karşılaştırır:

1. Aynalama: taslak paragrafları kaynağın paragraf sırasını izliyor mu? Ortak sayılar
   ve özel adlar üzerinden her taslak paragrafını bir kaynak paragrafına bağlar,
   sıranın tekdüzeliğini ve bire bir eşleşme oranını ölçer.
2. Uydurma: taslakta olup kaynakta olmayan sayılar ve özel adlar.
3. Kayıp: kaynakta olup taslağa girmeyen sayılar ve adlar (bilgi; hata değil).

Kullanım:
  python3 kaynak_hizala.py kaynak.md taslak.md
  python3 kaynak_hizala.py kaynak.md taslak.md --json
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import cumlelere_bol, dosya_oku, kelimeler, markdown_temizle, paragraflara_bol, tr_lower, tr_upper_mi, yaz  # noqa: E402

SAYI_RE = re.compile(r"(?<![\w.,])[-+]?\d+(?:[.,]\d{3})*(?:[.,]\d+)?(?:\s?%|\s?(?:milyon|milyar|bin|trilyon|million|billion|thousand|trillion))?(?![\w])|%\s?\d+(?:[.,]\d+)?", re.I)
BUYUK_KELIME_RE = re.compile(r"\b[A-ZÇĞİÖŞÜ][\wçğıöşüâîû]+(?:'[\wçğıöşü]+)?")
CARPAN = {"bin": 1e3, "thousand": 1e3, "milyon": 1e6, "million": 1e6, "milyar": 1e9, "billion": 1e9, "trilyon": 1e12, "trillion": 1e12}
DURAK_BUYUK = set("""
the a an in on of and or but for with at by from to as is was were are be this that these those it its he she they we you i
bu şu o ve ile ama fakat ancak için de da ki bir her hiç çok en daha ne nasıl neden hangi kim kimse ben sen biz siz onlar
ayrıca örneğin sonuç özetle ancak oysa peki evet hayır belki ceo cto genel müdür başkan dr prof
ocak şubat mart nisan mayıs haziran temmuz ağustos eylül ekim kasım aralık
january february march april may june july august september october november december
pazartesi salı çarşamba perşembe cuma cumartesi pazar monday tuesday wednesday thursday friday saturday sunday
""".split())


def sayi_normalize(s: str):
    s = s.strip().lower().replace(" ", "")
    yuzde = "%" in s
    s = s.replace("%", "")
    carpan = 1.0
    for ad, c in CARPAN.items():
        if s.endswith(ad):
            s = s[: -len(ad)]
            carpan = c
            break
    if s.count(",") and s.count("."):
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif s.count(","):
        p = s.split(",")
        s = s.replace(",", "") if all(len(x) == 3 for x in p[1:]) else s.replace(",", ".")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3 and len(s.split(".")[0]) <= 3):
        s = s.replace(".", "")
    try:
        deger = float(s) * carpan
    except ValueError:
        return None
    return (round(deger, 4), yuzde)


def sayilar(metin: str) -> set:
    kume = set()
    for m in SAYI_RE.finditer(metin):
        n = sayi_normalize(m.group(0))
        if n is not None:
            kume.add(n)
    return kume


def adlar(metin: str, comert=False) -> set:
    """Büyük harfle başlayan sözcükler. Cümle başındakiler: kesme işaretliyse ("Microsoft'un"),
    başka yerde de büyükse ya da `comert` modundaysa (kaynak metin için) sayılır."""
    ic, bas = set(), set()
    for cumle in cumlelere_bol(metin):
        kel = kelimeler(cumle)
        for i, k in enumerate(kel):
            if not tr_upper_mi(k[0]) or tr_lower(k.split("'")[0]) in DURAK_BUYUK or len(k) < 3:
                continue
            anahtar = ad_anahtari(k)
            if i == 0 and "'" not in k and not comert:
                bas.add(anahtar)
            else:
                ic.add(anahtar)
    return ic | {b for b in bas if b in ic}


TAKMA = {"abd": "united", "amerika": "united", "birleşik": "united", "devletleri": "states", "devlet": "states"}


def ad_anahtari(k: str) -> str:
    govde = tr_lower(k.split("'")[0])
    govde = TAKMA.get(govde, govde)
    return govde[:6] if len(govde) > 6 else govde


def paragraf_izleri(p: str) -> set:
    return {("s", *s) for s in sayilar(p)} | {("a", a) for a in adlar(p)}


def hizala(kaynak: str, taslak: str) -> dict:
    kaynak, taslak = markdown_temizle(kaynak), markdown_temizle(taslak)
    kp, tp = paragraflara_bol(kaynak), paragraflara_bol(taslak)
    k_iz = [paragraf_izleri(p) for p in kp]
    t_iz = [paragraf_izleri(p) for p in tp]

    esleme = []
    for i, tiz in enumerate(t_iz):
        if not tiz:
            esleme.append(None)
            continue
        en_iyi, en_iyi_puan = None, 0
        for j, kiz in enumerate(k_iz):
            ortak = len(tiz & kiz)
            if ortak > en_iyi_puan:
                en_iyi, en_iyi_puan = j, ortak
        esleme.append(en_iyi)
    eslesen = [e for e in esleme if e is not None]
    artan = sum(1 for a, b in zip(eslesen, eslesen[1:]) if b >= a)
    tekduzelik = round(artan / (len(eslesen) - 1), 2) if len(eslesen) > 1 else 0.0
    bire_bir = round(len(set(eslesen)) / len(tp), 2) if tp else 0.0
    paragraf_orani = round(len(tp) / len(kp), 2) if kp else 0.0
    cumle_orani = round(len(cumlelere_bol(taslak)) / max(1, len(cumlelere_bol(kaynak))), 2)

    aynalama = bool(len(eslesen) >= 3 and tekduzelik >= 0.8 and 0.75 <= paragraf_orani <= 1.3 and bire_bir >= 0.6)

    ks, ts = sayilar(kaynak), sayilar(taslak)
    ka, ta = adlar(kaynak, comert=True), adlar(taslak)
    uydurma_sayi = sorted(ts - ks)
    uydurma_ad = sorted(ta - ka)
    kayip_sayi = sorted(ks - ts)
    kayip_ad = sorted(ka - ta)

    def goster(s):
        d, y = s
        d = int(d) if float(d).is_integer() else d
        return f"%{d}" if y else str(d)

    sonuc = {
        "kaynak_paragraf": len(kp), "taslak_paragraf": len(tp),
        "paragraf_orani": paragraf_orani, "cumle_orani": cumle_orani,
        "esleme": esleme, "sira_tekduzeligi": tekduzelik, "bire_bir_oran": bire_bir,
        "aynalama": aynalama,
        "uydurma_sayilar": [goster(s) for s in uydurma_sayi],
        "uydurma_adlar": uydurma_ad,
        "kayip_sayilar": [goster(s) for s in kayip_sayi],
        "kayip_adlar": kayip_ad,
        "uyarilar": [],
    }
    u = sonuc["uyarilar"]
    if aynalama:
        u.append(f"Aynalama: taslak paragrafları kaynağın sırasını izliyor (tekdüzelik {tekduzelik}, paragraf oranı {paragraf_orani}). Bilgi kartından yeniden yaz; sırayı Türk okur için kur.")
    if 0.85 <= cumle_orani <= 1.15 and len(tp) >= 3 and tekduzelik >= 0.8:
        u.append(f"Cümle sayısı kaynağa çok yakın ({cumle_orani}): cümle cümle çeviri izi.")
    if uydurma_sayi:
        u.append("Kaynakta olmayan sayı: " + ", ".join(goster(s) for s in uydurma_sayi) + ". Kaynağı göster ya da sil.")
    if uydurma_ad:
        u.append("Kaynakta olmayan ad (yaklaşık, ilk 6 harf): " + ", ".join(uydurma_ad) + ". Kendi eklediğin bağlam mı, uydurma mı? Belirt.")
    return sonuc


def ozet(s: dict) -> str:
    L = [
        f"Hizalama: kaynak {s['kaynak_paragraf']} paragraf, taslak {s['taslak_paragraf']} paragraf (oran {s['paragraf_orani']}), cümle oranı {s['cumle_orani']}",
        f"Sıra tekdüzeliği {s['sira_tekduzeligi']}, bire bir eşleşme {s['bire_bir_oran']}, eşleme {s['esleme']} → aynalama: {'VAR' if s['aynalama'] else 'yok'}",
        "Uydurma sayılar: " + (", ".join(s["uydurma_sayilar"]) or "yok"),
        "Uydurma adlar: " + (", ".join(s["uydurma_adlar"]) or "yok"),
        "Kaynakta olup taslakta olmayan sayılar: " + (", ".join(s["kayip_sayilar"]) or "yok"),
        "Kaynakta olup taslakta olmayan adlar: " + (", ".join(s["kayip_adlar"]) or "yok"),
    ]
    L.append("Uyarılar:" if s["uyarilar"] else "Uyarı yok.")
    L += [f"  - {x}" for x in s["uyarilar"]]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kaynak")
    ap.add_argument("taslak")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sonuc = hizala(dosya_oku(a.kaynak), dosya_oku(a.taslak))
    yaz(sonuc, a.json, ozet(sonuc))


if __name__ == "__main__":
    main()

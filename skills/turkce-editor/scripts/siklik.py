#!/usr/bin/env python3
"""Sıklık denetimi: sözlük dışı / nadir / aşırı tekrar eden sözcükler.

Sözcükleri paketle gelen sıklık listesine göre denetler. Türkçe eklemeli olduğu için
listede olmayan biçimler önce yaklaşık bir ek soyucuyla köke indirilir; kök de yoksa
"tanınmayan" sayılır (uydurma, çok nadir ya da yazım hatası olabilir; kesin hüküm
değildir, gözle bak).

Kullanım:
  python3 siklik.py metin.md                 # yazılı dil listesi (Leipzig haber)
  python3 siklik.py metin.md --konusma       # konuşma listesi (OpenSubtitles); reel için
  python3 siklik.py metin.md --zeyrek        # zeyrek kuruluysa gerçek morfoloji
  python3 siklik.py metin.md --json
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import cumlelere_bol, kelimeler, kisaltmalari_yukle, markdown_temizle, tr_lower, tr_upper_mi, dosya_oku, yaz  # noqa: E402

VERI = Path(__file__).resolve().parent.parent / "data"

# Uzun ek önce; her biri bir kez soyulur, en fazla 4 katman.
EKLER = sorted({
    "larından", "lerinden", "larına", "lerine", "larını", "lerini", "larıyla", "leriyle", "ların", "lerin",
    "ları", "leri", "lar", "ler", "ının", "inin", "unun", "ünün", "nın", "nin", "nun", "nün", "ın", "in", "un", "ün",
    "dan", "den", "tan", "ten", "da", "de", "ta", "te", "ya", "ye", "na", "ne", "yı", "yi", "yu", "yü",
    "ı", "i", "u", "ü", "yla", "yle", "la", "le", "ım", "im", "um", "üm", "ımız", "imiz", "umuz", "ümüz",
    "ınız", "iniz", "unuz", "ünüz", "sı", "si", "su", "sü", "ki", "daki", "deki", "taki", "teki",
    "dır", "dir", "dur", "dür", "tır", "tir", "tur", "tür", "dı", "di", "du", "dü", "tı", "ti", "tu", "tü",
    "mış", "miş", "muş", "müş", "yor", "yorum", "yorsun", "yoruz", "yorsunuz", "yorlar", "ıyor", "iyor", "uyor", "üyor",
    "ecek", "acak", "eceğ", "acağ", "mek", "mak", "me", "ma", "mez", "maz", "ir", "ır", "ur", "ür", "ar", "er",
    "en", "an", "erek", "arak", "ince", "ınca", "unca", "ünce", "meli", "malı", "se", "sa", "ken", "ip", "ıp", "up", "üp",
    "lı", "li", "lu", "lü", "sız", "siz", "suz", "süz", "lık", "lik", "luk", "lük", "cı", "ci", "cu", "cü", "çı", "çi", "çu", "çü",
    "ce", "ca", "çe", "ça", "m", "n", "k", "z", "sın", "sin", "sun", "sün", "ız", "iz", "uz", "üz", "dik", "dık", "duk", "dük",
    "tik", "tık", "tuk", "tük", "diğ", "dığ", "duğ", "düğ", "tiğ", "tığ", "tuğ", "tüğ", "meye", "maya", "meyi", "mayı",
    "mesi", "ması", "mesin", "masın", "il", "ıl", "ul", "ül", "ış", "iş", "uş", "üş", "dir", "tir", "ebil", "abil",
    "leş", "laş", "len", "lan", "lat", "let", "yken", "ydi", "ydı", "ydu", "ydü", "ymış", "ymiş", "yse", "ysa",
}, key=len, reverse=True)
YUMUSAMA = {"ğ": "k", "b": "p", "c": "ç", "d": "t", "g": "k"}
DURAK = set("""
ve bir bu da de ile için çok daha o ne gibi ben sen biz siz onlar şu ama ki mi mı mu mü en ya her hem ise
var yok değil kadar sonra önce göre olan olarak olduğu diye hiç ancak fakat çünkü ya artık bile hep şey şeyi şeyler
""".split())


def liste_yukle(yol: Path) -> dict:
    d = {}
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if satir.startswith("#") or not satir.strip():
            continue
        p = satir.split("\t")
        if len(p) >= 3:
            d[p[0]] = int(p[2])
    return d


def kok_bul(kelime: str, sozluk: dict, derinlik=4, yeterli=3000):
    """Yaklaşık ek soyma. Sözlükte bulunan en sık kökü (kök, sıra) olarak döner, yoksa None.

    Sözcük sözlükte olsa bile sırası `yeterli`nin üstündeyse ek soyarak daha sık bir
    kök aranır; "sunmaktadır" için "sunmak"ın sırası döner.
    """
    en_iyi = (kelime, sozluk[kelime]) if kelime in sozluk else None
    if en_iyi and en_iyi[1] <= yeterli:
        return en_iyi
    if derinlik == 0 or len(kelime) < 3:
        return en_iyi
    for ek in EKLER:
        if kelime.endswith(ek) and len(kelime) - len(ek) >= 2:
            govde = kelime[: -len(ek)]
            adaylar = [govde]
            if govde[-1] in YUMUSAMA:
                adaylar.append(govde[:-1] + YUMUSAMA[govde[-1]])
            if len(govde) >= 3 and govde[-1] in "aeıioöuü" and ek[0] in "aeıioöuü":
                adaylar.append(govde + "y")  # araba-y-ı gibi kaynaştırma kalıntısı
            for aday in adaylar:
                r = kok_bul(aday, sozluk, derinlik - 1, yeterli)
                if r and (en_iyi is None or r[1] < en_iyi[1]):
                    en_iyi = r
                    if en_iyi[1] <= yeterli:
                        return en_iyi
    return en_iyi


def zeyrek_yukle():
    try:
        import zeyrek  # type: ignore
    except ImportError:
        return None
    try:
        import logging
        logging.getLogger("zeyrek").setLevel(logging.ERROR)
        return zeyrek.MorphAnalyzer()
    except Exception:
        return None


def denetle(metin: str, kayit: str, zeyrek_kullan=False, nadir_esik=20000, tekrar_esik=3) -> dict:
    metin = markdown_temizle(metin)
    ana = liste_yukle(VERI / ("siklik_konusma.tsv" if kayit == "konusma" else "siklik_yazili.tsv"))
    diger = liste_yukle(VERI / ("siklik_yazili.tsv" if kayit == "konusma" else "siklik_konusma.tsv"))
    analizci = zeyrek_yukle() if zeyrek_kullan else None

    cumleler = cumlelere_bol(metin, kisaltmalari_yukle())
    sayac, ornek, ozel_ad = Counter(), {}, Counter()
    toplam = 0
    for cumle in cumleler:
        for i, k in enumerate(kelimeler(cumle)):
            toplam += 1
            if "'" in k:
                ozel_ad[k.split("'")[0]] += 1
                continue
            if i > 0 and tr_upper_mi(k[0]):
                ozel_ad[k] += 1
                continue
            kl = tr_lower(k)
            if len(kl) < 3:
                continue
            sayac[kl] += 1
            ornek.setdefault(kl, cumle)

    taninmayan, nadir, yazi_dili, coz_hatasi = [], [], [], []
    for kelime, n in sayac.most_common():
        r = kok_bul(kelime, ana)
        if analizci is not None:
            try:
                lemmalar = analizci.lemmatize(kelime)
                koker = [l for _, ls in lemmalar for l in ls] if lemmalar else []
            except Exception:
                koker = []
            if not koker:
                coz_hatasi.append({"kelime": kelime, "sayi": n, "ornek": ornek[kelime]})
            elif r is None:
                for kok in koker:
                    kok = tr_lower(kok)
                    if kok in ana:
                        r = (kok, ana[kok])
                        break
        if r is None:
            r_diger = kok_bul(kelime, diger)
            if r_diger is None:
                taninmayan.append({"kelime": kelime, "sayi": n, "ornek": ornek[kelime]})
            elif kayit == "konusma":
                yazi_dili.append({"kelime": kelime, "sayi": n, "yazili_sira": r_diger[1], "ornek": ornek[kelime]})
            continue
        kok, sira = r
        if sira > nadir_esik:
            nadir.append({"kelime": kelime, "kok": kok, "sira": sira, "sayi": n})
        if kayit == "konusma" and kok_bul(kelime, diger) and sira > 8000 and kok_bul(kelime, diger)[1] < 3000:
            yazi_dili.append({"kelime": kelime, "sayi": n, "yazili_sira": kok_bul(kelime, diger)[1], "konusma_sira": sira, "ornek": ornek[kelime]})

    tekrar = []
    for kelime, n in sayac.most_common():
        if n < tekrar_esik or kelime in DURAK or len(kelime) < 4:
            continue
        r = kok_bul(kelime, ana)
        if r and r[1] <= 300:
            continue
        pay = 100 * n / toplam if toplam else 0
        if pay >= 0.8 or n >= 5:
            tekrar.append({"kelime": kelime, "sayi": n, "yuz": round(pay, 2)})

    return {
        "kayit": kayit,
        "kelime": toplam,
        "farkli_kelime": len(sayac),
        "zeyrek": analizci is not None,
        "taninmayan": taninmayan,
        "nadir": nadir[:30],
        "yazi_dili_sozcugu": yazi_dili[:30],
        "asiri_tekrar": tekrar[:20],
        "cozumlenemeyen": coz_hatasi,
        "ozel_ad_sayisi": sum(ozel_ad.values()),
    }


def ozet(s: dict) -> str:
    L = [f"Sıklık denetimi ({'konuşma' if s['kayit'] == 'konusma' else 'yazılı'} listesi{', zeyrek' if s['zeyrek'] else ', yaklaşık ek soyma'}): {s['kelime']} kelime, {s['farkli_kelime']} farklı biçim"]
    if s["taninmayan"]:
        L.append(f"Tanınmayan ({len(s['taninmayan'])}) — uydurma, yazım hatası ya da çok nadir olabilir; gözle bak:")
        for t in s["taninmayan"][:25]:
            L.append(f"  - {t['kelime']} ×{t['sayi']}: {t['ornek'][:100]}")
    else:
        L.append("Tanınmayan sözcük yok.")
    if s["nadir"]:
        L.append("Nadir (listede sırası " + f"> eşik): " + ", ".join(f"{n['kelime']} (kök {n['kok']}, sıra {n['sira']})" for n in s["nadir"][:15]))
    if s["yazi_dili_sozcugu"]:
        L.append("Konuşmada yabancı duran yazı dili sözcükleri: " + ", ".join(y["kelime"] for y in s["yazi_dili_sozcugu"][:15]))
    if s["asiri_tekrar"]:
        L.append("Aşırı tekrar: " + ", ".join(f"{t['kelime']} ×{t['sayi']} (%{t['yuz']})" for t in s["asiri_tekrar"]))
    if s["cozumlenemeyen"]:
        L.append("Zeyrek çözümleyemedi: " + ", ".join(c["kelime"] for c in s["cozumlenemeyen"][:20]))
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?", default="-")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--yazili", action="store_true", help="Leipzig haber listesi (varsayılan)")
    g.add_argument("--konusma", action="store_true", help="OpenSubtitles listesi; reel/konuşma metni için")
    ap.add_argument("--zeyrek", action="store_true", help="zeyrek kuruluysa morfolojik çözümleme")
    ap.add_argument("--nadir-esik", type=int, default=20000)
    ap.add_argument("--tekrar-esik", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sonuc = denetle(dosya_oku(a.dosya), "konusma" if a.konusma else "yazili", a.zeyrek, a.nadir_esik, a.tekrar_esik)
    yaz(sonuc, a.json, ozet(sonuc))


if __name__ == "__main__":
    main()

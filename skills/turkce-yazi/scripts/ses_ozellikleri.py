#!/usr/bin/env python3
"""Onaylanmış metin arşivinden yazar özellikleri çıkarır, voice/profil.md üretir.

Özellikler: cümle uzunluğu dağılımı, paragraf uzunluğu, yüklem ekleri, hitap
(sen/siz), zamir ve "bir" oranı, noktalama alışkanlıkları, sevilen bağlaçlar ve
yüklemler, açılış ve kapanış hareketleri. Tür başına ve toplam.

Kullanım:
  python3 ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
  python3 ses_ozellikleri.py --arsiv voice/onaylanan --json

profil.md içinde <!-- otomatik başlangıç --> ... <!-- otomatik son --> arası
yenilenir; dışındaki "Elle notlar" korunur.
"""
import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import BAGLACLAR, cumlelere_bol, cv, hece_sayisi, kelimeler, kisaltmalari_yukle, markdown_temizle, ortalama, paragraflara_bol, std, tr_lower  # noqa: E402

BAS = "<!-- otomatik başlangıç"
SON = "<!-- otomatik son -->"
SEN = {"sen", "sana", "seni", "senin", "sende", "senden"}
SIZ = {"siz", "size", "sizi", "sizin", "sizde", "sizden"}
BEN = {"ben", "bana", "beni", "benim", "bende", "benden"}
BIZ = {"biz", "bize", "bizi", "bizim", "bizde", "bizden"}
SEN_EK = re.compile(r"\w+(sın|sin|sun|sün|yorsun|acaksın|eceksin|dın|din|dun|dün|mışsın|mişsin|malısın|melisin)$")
SIZ_EK = re.compile(r"\w+(sınız|siniz|sunuz|sünüz|yorsunuz|acaksınız|eceksiniz|dınız|diniz|dunuz|dünüz|malısınız|melisiniz|ın|in|un|ün|yın|yin|yun|yün)$")
YUKLEM = [
    ("-maktadır", re.compile(r"(makta|mekte)d[ıi]r(lar|ler)?$")),
    ("-mıştır", re.compile(r"(mış|miş|muş|müş)t[ıi]r(lar|ler)?$")),
    ("-dır", re.compile(r"(dır|dir|dur|dür|tır|tir|tur|tür)(lar|ler)?$")),
    ("-yor", re.compile(r"yor(um|sun|uz|sunuz|lar|)$")),
    ("-dı", re.compile(r"(dı|di|du|dü|tı|ti|tu|tü)(m|n|k|nız|niz|nuz|nüz|lar|ler|)$")),
    ("-ecek", re.compile(r"((ecek|acak)(sın|sin|sınız|siniz|ler|lar|)|(eceğ|acağ)(im|ım|iz|ız))$")),
    ("-mış", re.compile(r"(mış|miş|muş|müş)(ım|im|um|üm|sın|sin|ız|iz|lar|ler|)$")),
    ("-meli", re.compile(r"(malı|meli)(yım|yim|sın|sin|yız|yiz|lar|ler|)$")),
    ("-ır", re.compile(r"\w{2,}(ır|ir|ur|ür|ar|er)(ım|im|um|üm|sın|sin|ız|iz|lar|ler|)$")),
]
NOKTALAMA = {"?": "soru", "!": "ünlem", ":": "iki nokta", ";": "noktalı virgül", "—": "uzun tire", "(": "parantez", "\"": "tırnak", "…": "üç nokta"}
DURAK = set("ve bir bu da de ile için çok daha o ne gibi ben sen biz siz onlar şu ama ki mi mı mu mü en ya her hem ise var yok değil kadar sonra önce göre olan olarak olduğu diye hiç ancak fakat çünkü artık bile hep şey şeyi şeyler bunu bunun buna bundan onu onun ona".split())


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


def yuklem_turu(cumle: str) -> str:
    kel = kelimeler(cumle)
    if not kel:
        return "diğer"
    if cumle.rstrip().endswith("?"):
        return "soru"
    son = tr_lower(kel[-1])
    for ad, rx in YUKLEM:
        if rx.search(son):
            return ad
    return "ad cümlesi/diğer"


def acilis_turu(cumle: str) -> str:
    c = cumle.strip()
    k = tr_lower(c)
    kel = [tr_lower(x) for x in kelimeler(c)]
    if c.endswith("?"):
        return "soru"
    if c[:1] in "\"“‘'«":
        return "alıntı/diyalog"
    if re.search(r"\d", c[:15]):
        return "sayı/tarih"
    if kel and (kel[0] in SEN | SIZ or (len(kel) > 1 and (SEN_EK.search(kel[-1]) or SIZ_EK.search(kel[-1])))):
        return "okura hitap"
    if kel and kel[0] in BEN | BIZ:
        return "ben/biz"
    if re.search(r"(dır|dir|dur|dür|tır|tir|tur|tür)\.?$", k) or " anlamına gel" in k or " demektir" in k:
        return "tanım"
    if yuklem_turu(c) == "-dı":
        return "anlatı/sahne"
    return "gözlem/iddia"


def metin_ozellikleri(metin: str) -> dict:
    metin = markdown_temizle(metin)
    kis = kisaltmalari_yukle()
    par = paragraflara_bol(metin)
    cum = cumlelere_bol(metin, kis)
    kel = kelimeler(metin)
    kl = [tr_lower(k) for k in kel]
    if not cum or not kel:
        return {}
    uz = [len(kelimeler(c)) for c in cum]
    sen = sum(1 for k in kl if k in SEN) + sum(1 for c in cum if SEN_EK.search(tr_lower(kelimeler(c)[-1])) if kelimeler(c))
    siz = sum(1 for k in kl if k in SIZ) + sum(1 for c in cum if SIZ_EK.search(tr_lower(kelimeler(c)[-1])) if kelimeler(c))
    return {
        "kelime": len(kel), "cumle": len(cum), "paragraf": len(par),
        "uzunluklar": uz,
        "par_cumle": [len(cumlelere_bol(p, kis)) for p in par],
        "yuklem": Counter(yuklem_turu(c) for c in cum),
        "hitap": "sen" if sen > siz and sen > 0 else "siz" if siz > 0 else "yok",
        "zamir": sum(1 for k in kl if k in BEN | BIZ | SEN | SIZ),
        "ben": sum(1 for k in kl if k in BEN),
        "bir": kl.count("bir"),
        "noktalama": Counter(ad for ch, ad in NOKTALAMA.items() for _ in range(metin.count(ch))),
        "baglac_bas": Counter(b for c in cum for b in BAGLACLAR if tr_lower(c).lstrip("\"“‘'(").startswith(b + " ") or tr_lower(c).lstrip("\"“‘'(").startswith(b + ",")),
        "baglac": Counter(k for k in kl if k in {"ama", "sonra", "çünkü", "yani", "ancak", "fakat", "oysa", "üstelik", "hatta", "belki", "zaten", "aslında", "meğer", "neyse", "işte", "bir de", "ayrıca", "öte yandan", "bununla birlikte", "dolayısıyla"}),
        "son_kelime": Counter(tr_lower(kelimeler(c)[-1]) for c in cum if kelimeler(c)),
        "acilis": acilis_turu(cum[0]),
        "kapanis_kisa": len(kelimeler(cum[-1])) <= 5,
        "kapanis_soru": cum[-1].rstrip().endswith("?"),
        "hece_kelime": sum(hece_sayisi(k) for k in kel) / len(kel),
        "icerik": Counter(k for k in kl if len(k) >= 4 and k not in DURAK),
    }


def birlestir(ozellikler: list) -> dict:
    if not ozellikler:
        return {}
    n = len(ozellikler)
    uz = [u for o in ozellikler for u in o["uzunluklar"]]
    kel = sum(o["kelime"] for o in ozellikler)
    cum = sum(o["cumle"] for o in ozellikler)
    yuk = sum((o["yuklem"] for o in ozellikler), Counter())
    nok = sum((o["noktalama"] for o in ozellikler), Counter())
    bag = sum((o["baglac"] for o in ozellikler), Counter())
    bag_bas = sum((o["baglac_bas"] for o in ozellikler), Counter())
    son = sum((o["son_kelime"] for o in ozellikler), Counter())
    par_cum = [p for o in ozellikler for p in o["par_cumle"]]
    uz_s = sorted(uz)
    return {
        "metin": n, "kelime": kel, "cumle": cum,
        "cumle_ort": round(ortalama(uz), 1), "cumle_std": round(std(uz), 1), "cumle_cv": cv(uz),
        "cumle_p10": uz_s[int(0.1 * (len(uz_s) - 1))], "cumle_p50": uz_s[len(uz_s) // 2], "cumle_p90": uz_s[int(0.9 * (len(uz_s) - 1))],
        "kisa_pay": round(sum(1 for u in uz if u <= 4) / len(uz), 2),
        "par_cumle_ort": round(ortalama(par_cum), 1), "tek_cumle_par_pay": round(sum(1 for p in par_cum if p == 1) / max(1, len(par_cum)), 2),
        "yuklem_pay": {k: round(v / cum, 2) for k, v in yuk.most_common()},
        "hitap": dict(Counter(o["hitap"] for o in ozellikler)),
        "zamir_yuz": round(100 * sum(o["zamir"] for o in ozellikler) / kel, 2),
        "ben_yuz": round(100 * sum(o["ben"] for o in ozellikler) / kel, 2),
        "bir_yuz": round(100 * sum(o["bir"] for o in ozellikler) / kel, 2),
        "noktalama_bin": {k: round(1000 * v / kel, 1) for k, v in nok.most_common()},
        "baglac_bin": {k: round(1000 * v / kel, 1) for k, v in bag.most_common(8)},
        "baglac_basi_pay": round(sum(bag_bas.values()) / cum, 2),
        "sik_yuklem": [k for k, _ in son.most_common(12)],
        "acilis": dict(Counter(o["acilis"] for o in ozellikler).most_common()),
        "kapanis_kisa_pay": round(sum(1 for o in ozellikler if o["kapanis_kisa"]) / n, 2),
        "kapanis_soru_pay": round(sum(1 for o in ozellikler if o["kapanis_soru"]) / n, 2),
        "hece_kelime": round(ortalama(o["hece_kelime"] for o in ozellikler), 2),
        "atesman": round(198.825 - 40.175 * ortalama(o["hece_kelime"] for o in ozellikler) - 2.610 * ortalama(uz), 1),
    }


def arsivi_oku(arsiv: Path):
    dosyalar = []
    uyarilar = []
    for yol in sorted(arsiv.rglob("*.md")):
        meta, govde = frontmatter(yol.read_text(encoding="utf-8"))
        tur = meta.get("tür") or meta.get("tur") or yol.parent.name
        if yol.parent.name != tur and yol.parent != arsiv:
            uyarilar.append(f"{yol}: frontmatter tür '{tur}', klasör '{yol.parent.name}'")
        o = metin_ozellikleri(govde)
        if o:
            o["tur"], o["yol"], o["meta"] = tur, str(yol), meta
            dosyalar.append(o)
        else:
            uyarilar.append(f"{yol}: boş ya da okunamadı")
    return dosyalar, uyarilar


def profil_metni(genel: dict, turler: dict, uyarilar: list, arsiv: Path) -> str:
    def blok(b: dict, baslik: str) -> str:
        if not b:
            return ""
        L = [f"### {baslik} ({b['metin']} metin, {b['kelime']} kelime)"]
        L.append(f"- Cümle: ortalama {b['cumle_ort']} kelime, std {b['cumle_std']}, CV {b['cumle_cv']}; %10–%50–%90: {b['cumle_p10']}–{b['cumle_p50']}–{b['cumle_p90']}; ≤4 kelimelik cümle payı %{int(b['kisa_pay'] * 100)}")
        L.append(f"- Paragraf: ortalama {b['par_cumle_ort']} cümle; tek cümlelik paragraf payı %{int(b['tek_cumle_par_pay'] * 100)}")
        L.append("- Yüklem: " + ", ".join(f"{k} %{int(v * 100)}" for k, v in b["yuklem_pay"].items()))
        L.append("- Hitap (metin başına): " + ", ".join(f"{k} {v}" for k, v in b["hitap"].items()) + f"; zamir %{b['zamir_yuz']} (ben %{b['ben_yuz']}); \"bir\" %{b['bir_yuz']}")
        L.append("- Noktalama (1000 kelimede): " + (", ".join(f"{k} {v}" for k, v in b["noktalama_bin"].items()) or "yok"))
        L.append("- Bağlaçlar (1000 kelimede): " + (", ".join(f"{k} {v}" for k, v in b["baglac_bin"].items()) or "yok") + f"; bağlaçla başlayan cümle %{int(b['baglac_basi_pay'] * 100)}")
        L.append("- Sık yüklemler: " + ", ".join(b["sik_yuklem"]))
        L.append("- Açılış hareketleri: " + ", ".join(f"{k} {v}" for k, v in b["acilis"].items()))
        L.append(f"- Kapanış: kısa cümleyle biten %{int(b['kapanis_kisa_pay'] * 100)}, soruyla biten %{int(b['kapanis_soru_pay'] * 100)}")
        L.append(f"- Okunabilirlik: {b['hece_kelime']} hece/kelime, Ateşman {b['atesman']}")
        return "\n".join(L)

    L = [f"{BAS}: ses_ozellikleri.py, {dt.date.today().isoformat()}, arşiv {arsiv} -->", "## Ölçüler", blok(genel, "Tüm türler")]
    if genel.get("metin", 0) < 5:
        L.append("\n> Uyarı: 5 metnin altında; ölçüler güvenilir değil.")
    for tur, b in turler.items():
        if b.get("metin", 0) >= 3:
            L.append("\n" + blok(b, tur))
        else:
            L.append(f"\n### {tur} ({b.get('metin', 0)} metin) — 3 metnin altında, genel profil kullanılır")
    if uyarilar:
        L.append("\n### Arşiv uyarıları\n" + "\n".join(f"- {u}" for u in uyarilar))
    L.append(SON)
    return "\n".join(L)


def profil_yaz(cikti: Path, otomatik: str) -> None:
    if cikti.exists():
        eski = cikti.read_text(encoding="utf-8")
        if BAS in eski and SON in eski:
            yeni = eski[: eski.index(BAS)] + otomatik + eski[eski.index(SON) + len(SON):]
        else:
            yeni = eski.rstrip() + "\n\n" + otomatik + "\n"
    else:
        yeni = "# Ses profili\n\n" + otomatik + "\n\n## Elle notlar\n\n- İmza hareketleri:\n- Yasaklar:\n- Hitap tercihi:\n- Sevmediğim sözcükler:\n"
    cikti.parent.mkdir(parents=True, exist_ok=True)
    cikti.write_text(yeni, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arsiv", type=Path, default=Path("voice/onaylanan"))
    ap.add_argument("--cikti", type=Path, help="profil.md yolu; verilmezse stdout")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.arsiv.exists():
        sys.exit(f"arşiv yok: {a.arsiv}")
    dosyalar, uyarilar = arsivi_oku(a.arsiv)
    genel = birlestir(dosyalar)
    turler = {t: birlestir([d for d in dosyalar if d["tur"] == t]) for t in sorted({d["tur"] for d in dosyalar})}
    if a.json:
        print(json.dumps({"genel": genel, "turler": turler, "uyarilar": uyarilar}, ensure_ascii=False, indent=2))
        return
    otomatik = profil_metni(genel, turler, uyarilar, a.arsiv)
    if a.cikti:
        profil_yaz(a.cikti, otomatik)
        print(f"yazıldı: {a.cikti} ({genel.get('metin', 0)} metin)")
    else:
        print(otomatik)


if __name__ == "__main__":
    main()

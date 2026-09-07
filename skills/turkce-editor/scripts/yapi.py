#!/usr/bin/env python3
"""Yapı denetimi: üçlü listeler, "X değil Y" karşıtlıkları, giriş-sonuç tekrarı,
markdown/liste yoğunluğu, uzun tire ve tuhaf unicode, cümle/paragraf açılış tekrarı.

Kullanım:
  python3 yapi.py metin.md
  python3 yapi.py metin.md --tur reel     # reel'de başlık/liste yasak
  python3 yapi.py metin.md --json
"""
import argparse
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trmetin import cumlelere_bol, dosya_oku, kelimeler, kisaltmalari_yukle, paragraflara_bol, tr_lower, yaz  # noqa: E402

UCLU_RE = re.compile(r",\s((?:\S+\s){0,2}\S+),?\s(?:ve|veya|ya da)\s\S+")
UCLU_BAGLAC = {"çünkü", "ama", "ancak", "fakat", "diye", "ki", "yani", "hem", "ne", "hatta", "sonra", "oysa", "eğer", "belki"}
YUKLEM_SONU_RE = re.compile(r"(d[ıiuü]r|t[ıiuü]r|yor\w*|m[ıiuü]ş\w*|[ae]c[ae]k\w*|d[ıiuü]|t[ıiuü]|d[ıiuü][km]|t[ıiuü][km]|mal[ıi]\w*|mel[ıi]\w*)$")


def uclu_mu(cumle: str) -> bool:
    for m in UCLU_RE.finditer(cumle):
        orta = tr_lower(m.group(1)).split()
        if UCLU_BAGLAC & set(orta):
            continue
        son = orta[-1]
        if len(son) >= 4 and YUKLEM_SONU_RE.search(son):
            continue
        return True
    return False


DEGIL_RE = re.compile(r"\bdeğil,?\s(?:aynı zamanda|ama|fakat|tam tersine|aksine|bilakis|\w+)")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF⭐✅❌]")
TUHAF = {" ": "bölünmez boşluk", "​": "sıfır genişlikli boşluk", "‌": "ZWNJ", "‍": "ZWJ", "﻿": "BOM", " ": "satır ayırıcı", "•": "madde imi", "→": "ok", "✓": "onay işareti"}
DURAK = set("ve bir bu da de ile için çok daha o ne gibi ben sen biz siz onlar şu ama ki mi mı mu mü en ya her hem ise var yok değil kadar sonra önce göre olan olarak olduğu diye hiç ancak fakat çünkü artık bile hep şey şeyi şeyler bunu bunun buna bundan onu onun ona".split())


def icerik_kumesi(paragraf: str) -> set:
    return {tr_lower(k) for k in kelimeler(paragraf) if len(k) >= 4 and tr_lower(k) not in DURAK}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return round(len(a & b) / len(a | b), 3)


def incele(ham: str, tur=None) -> dict:
    satirlar = ham.splitlines()
    basliklar = [s for s in satirlar if re.match(r"^\s{0,3}#{1,6}\s", s)]
    maddeler = [s for s in satirlar if re.match(r"^\s*(?:[-*+]|\d+[.)])\s", s)]
    kalin = len(re.findall(r"\*\*[^*\n]+\*\*|__[^_\n]+__", ham))
    emoji = len(EMOJI_RE.findall(ham))
    uzun_tire = ham.count("—")
    kisa_tire = ham.count("–")
    kivrik_tirnak = sum(ham.count(c) for c in "“”‘’")
    duzeltme_isareti = sum(ham.count(c) for c in "âîûÂÎÛ")
    tuhaf = {ad: ham.count(ch) for ch, ad in TUHAF.items() if ham.count(ch)}
    kontrol = [f"U+{ord(ch):04X} {unicodedata.name(ch, '?')}" for ch in set(ham) if unicodedata.category(ch) in ("Cf", "Co") and ch not in TUHAF]

    metin = re.sub(r"^\s{0,3}#{1,6}\s+", "", ham, flags=re.M)
    metin = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", metin, flags=re.M)
    metin = re.sub(r"\*\*|__", "", metin)
    kisaltmalar = kisaltmalari_yukle()
    paragraflar = paragraflara_bol(metin)
    cumleler = cumlelere_bol(metin, kisaltmalar)
    n_cum = len(cumleler) or 1
    n_kel = len(kelimeler(metin)) or 1

    uclu = [c for c in cumleler if uclu_mu(c)]
    degil = [c for c in cumleler if DEGIL_RE.search(tr_lower(c))]
    soru = [c for c in cumleler if c.rstrip().endswith("?")]
    par_ilk_cumle_soru = sum(1 for p in paragraflar if (cumlelere_bol(p, kisaltmalar) or [""])[0].rstrip().endswith("?"))

    ilk_kelime = [tr_lower(kelimeler(c)[0]) if kelimeler(c) else "" for c in cumleler]
    ardisik_ayni = sum(1 for a, b in zip(ilk_kelime, ilk_kelime[1:]) if a and a == b)
    bas_sayac = Counter(k for k in ilk_kelime if k)
    par_ilk = Counter(tr_lower(kelimeler(p)[0]) for p in paragraflar if kelimeler(p))

    giris_sonuc = jaccard(icerik_kumesi(paragraflar[0]), icerik_kumesi(paragraflar[-1])) if len(paragraflar) >= 2 else 0.0
    son_par = paragraflar[-1] if paragraflar else ""
    ozet_kapanis = bool(re.search(r"\b(sonuç olarak|özetle|kısacası|netice itibar|sonuçta|özetlemek gerekirse)\b", tr_lower(son_par)))

    s = {
        "kelime": n_kel,
        "cumle": n_cum,
        "paragraf": len(paragraflar),
        "biçim": {
            "baslik": len(basliklar), "madde": len(maddeler), "kalin": kalin, "emoji": emoji,
            "uzun_tire": uzun_tire, "kisa_tire": kisa_tire, "kivrik_tirnak": kivrik_tirnak, "duzeltme_isareti": duzeltme_isareti,
            "tuhaf_unicode": tuhaf, "diger_gorunmez": kontrol,
            "madde_yuz": round(100 * len(maddeler) / max(1, len([x for x in satirlar if x.strip()])), 1),
        },
        "uclu_liste": {"sayi": len(uclu), "yuz_cumle": round(100 * len(uclu) / n_cum, 1), "ornek": uclu[:5]},
        "degil_karsitlik": {"sayi": len(degil), "yuz_cumle": round(100 * len(degil) / n_cum, 1), "ornek": degil[:5]},
        "soru": {"sayi": len(soru), "yuz_cumle": round(100 * len(soru) / n_cum, 1), "paragraf_basi": par_ilk_cumle_soru},
        "acilis": {
            "ardisik_ayni_kelime": ardisik_ayni,
            "en_sik_cumle_basi": bas_sayac.most_common(5),
            "en_sik_paragraf_basi": par_ilk.most_common(3),
        },
        "giris_sonuc_jaccard": giris_sonuc,
        "ozet_kapanisi": ozet_kapanis,
        "uyarilar": [],
    }
    u = s["uyarilar"]
    if tur == "reel":
        if basliklar or maddeler:
            u.append("[reel] Başlık/madde var: reel metni düz konuşmadır, hepsini cümleye çevir.")
        if kalin:
            u.append("[reel] Kalın yazı var; sesli okumada karşılığı yok, sil.")
        if len(paragraflar) > 8:
            u.append("[reel] Paragraf çok; reel tek fikir, 3-6 nefes.")
    if s["uclu_liste"]["yuz_cumle"] > 15:
        u.append(f"Cümlelerin %{s['uclu_liste']['yuz_cumle']}'inde 'A, B ve C' üçlemesi var. İkiye indir ya da tek somut örnek ver.")
    if s["degil_karsitlik"]["sayi"] >= 2:
        u.append(f"'X değil Y' karşıtlığı {s['degil_karsitlik']['sayi']} kez. Birini bırak, diğerlerini düz cümle yap.")
    if s["soru"]["paragraf_basi"] >= 2:
        u.append("Birden çok paragraf soruyla açılıyor: retorik soru tekniği tekrarlanıyor.")
    if giris_sonuc >= 0.25:
        u.append(f"Sonuç paragrafı girişi yineliyor (benzerlik {giris_sonuc}). Sonucu ya kes ya yeni bir şey söyle.")
    if ozet_kapanis:
        u.append("Son paragraf 'sonuç olarak / özetle' ile açılıyor: özet paragrafını sil.")
    if ardisik_ayni >= 2:
        u.append(f"Art arda {ardisik_ayni} kez aynı sözcükle başlayan cümle çifti.")
    if bas_sayac and bas_sayac.most_common(1)[0][1] / n_cum > 0.2 and n_cum >= 8:
        k, n = bas_sayac.most_common(1)[0]
        u.append(f"Cümlelerin %{int(100 * n / n_cum)}'i '{k}' ile başlıyor.")
    if uzun_tire >= 3 or (n_kel and 1000 * uzun_tire / n_kel > 4):
        u.append(f"Uzun tire (—) {uzun_tire} kez: Türkçe düzyazıda seyrek. Virgül, iki nokta ya da ayrı cümle.")
    if emoji:
        u.append(f"{emoji} emoji.")
    if duzeltme_isareti:
        u.append(f"Düzeltme işareti (â/î/û) {duzeltme_isareti} kez: düz yaz (zeka, hala, kağıt).")
    if tuhaf or kontrol:
        u.append("Görünmez/tuhaf karakter var: " + ", ".join(list(tuhaf) + kontrol))
    if kalin >= 3 and tur in (None, "deneme", "makale"):
        u.append("Kalın vurgu sık: düzyazıda vurgu cümle düzeniyle yapılır.")
    return s


def ozet(s: dict) -> str:
    b = s["biçim"]
    L = [
        f"Yapı: {s['kelime']} kelime, {s['cumle']} cümle, {s['paragraf']} paragraf",
        f"Biçim: başlık {b['baslik']}, madde {b['madde']} (%{b['madde_yuz']} satır), kalın {b['kalin']}, emoji {b['emoji']}, uzun tire {b['uzun_tire']}, kısa tire {b['kisa_tire']}, kıvrık tırnak {b['kivrik_tirnak']}, düzeltme işareti {b['duzeltme_isareti']}",
        f"Üçlü liste: {s['uclu_liste']['sayi']} (%{s['uclu_liste']['yuz_cumle']} cümle); 'değil' karşıtlığı: {s['degil_karsitlik']['sayi']}; soru: {s['soru']['sayi']} (paragraf başı {s['soru']['paragraf_basi']})",
        f"Açılış: art arda aynı sözcük {s['acilis']['ardisik_ayni_kelime']}; en sık cümle başı " + ", ".join(f"{k} ×{n}" for k, n in s["acilis"]["en_sik_cumle_basi"]),
        f"Giriş-sonuç benzerliği: {s['giris_sonuc_jaccard']}; özet kapanışı: {'var' if s['ozet_kapanisi'] else 'yok'}",
    ]
    for c in s["uclu_liste"]["ornek"][:3]:
        L.append(f"  üçlü: {c[:120]}")
    for c in s["degil_karsitlik"]["ornek"][:3]:
        L.append(f"  değil: {c[:120]}")
    L.append("Uyarılar:" if s["uyarilar"] else "Uyarı yok.")
    L += [f"  - {x}" for x in s["uyarilar"]]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dosya", nargs="?", default="-")
    ap.add_argument("--tur", choices=["reel", "deneme", "makale", "blog"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sonuc = incele(dosya_oku(a.dosya), a.tur)
    yaz(sonuc, a.json, ozet(sonuc))


if __name__ == "__main__":
    main()

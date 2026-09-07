#!/usr/bin/env python3
"""Karşıt örnek ekler, kural damıtır, tercihler.md ve tercihler.tsv günceller.

Kullanım:
  karsit_ekle.py ekle --tur deneme --reddedilen "..." --yorum "..." --son-hal "..." [--kural "..."] [--kalip REGEX]
  karsit_ekle.py ekle --dosya ucluler.json        # liste: [{"tür","reddedilen","yorum","son_hal","kural_adayı","kalip"}, ...]
  karsit_ekle.py liste
  karsit_ekle.py terfi K7
  karsit_ekle.py birlestir K7 K12
  karsit_ekle.py tsv                               # tercihler.tsv'yi yeniden üret

--voice ile voice/ klasörü verilir (varsayılan ./voice).
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

TERFI_ESIK = 3
DURAK = set("ve bir bu da de ile için çok daha o ne gibi ben sen biz siz onlar şu ama ki mi mı mu mü en ya her hem ise var yok değil kadar sonra önce göre olan olarak yerine değil kurma yazma yaz kullanma kullan".split())
KURAL_RE = re.compile(r"^### (K\d+) — (.*)$")
ALAN_RE = re.compile(r"^- (Kural|Örnek|Karşı örnek|Kalıp|Tür|Görülme|Kaynak): ?(.*)$")


def tr_lower(s: str) -> str:
    return s.replace("I", "ı").replace("İ", "i").lower()


def govde_kumesi(metin: str) -> set:
    return {tr_lower(k)[:6] for k in re.findall(r"[\wçğıöşüâîû]+", metin) if len(k) >= 3 and tr_lower(k) not in DURAK}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


class Tercihler:
    def __init__(self, yol: Path):
        self.yol = yol
        self.kurallar = []  # dict: id, baslik, alanlar, bolum
        self.on_metin = "# Tercihler\n"
        self.liste_giris = "\n## Editör kontrol listesi\n\nBuradaki kurallar `turkce-editor` tarafından her oturumun başında okunur ve genel kurallardan önce gelir.\n"
        self.aday_giris = "\n## Aday kurallar\n\nÜç kez görülünce yukarı taşınır.\n"
        if yol.exists():
            self._oku(yol.read_text(encoding="utf-8"))

    def _oku(self, metin: str) -> None:
        bolum = None
        kural = None
        for satir in metin.splitlines():
            if satir.startswith("## Editör kontrol listesi"):
                bolum = "liste"
                continue
            if satir.startswith("## Aday kurallar"):
                bolum = "aday"
                continue
            m = KURAL_RE.match(satir)
            if m:
                kural = {"id": m.group(1), "baslik": m.group(2).strip(), "alanlar": {}, "bolum": bolum or "aday"}
                self.kurallar.append(kural)
                continue
            m = ALAN_RE.match(satir)
            if m and kural is not None:
                kural["alanlar"][m.group(1)] = m.group(2).strip()

    def bul(self, kid: str):
        for k in self.kurallar:
            if k["id"] == kid:
                return k
        return None

    def benzer(self, kural_metni: str, esik=0.6):
        hedef = govde_kumesi(kural_metni)
        en_iyi, en_puan = None, 0.0
        for k in self.kurallar:
            p = max(jaccard(hedef, govde_kumesi(k["baslik"])), jaccard(hedef, govde_kumesi(k["alanlar"].get("Kural", ""))))
            if p > en_puan:
                en_iyi, en_puan = k, p
        return (en_iyi, en_puan) if en_puan >= esik else (None, en_puan)

    def yeni_id(self) -> str:
        n = max((int(k["id"][1:]) for k in self.kurallar), default=0) + 1
        return f"K{n}"

    def gorulme(self, k) -> int:
        m = re.match(r"(\d+)", k["alanlar"].get("Görülme", "0"))
        return int(m.group(1)) if m else 0

    def gorulme_artir(self, k, tarih: str, karsit_id: int) -> None:
        g = self.gorulme(k) + 1
        tarihler = re.findall(r"\d{4}-\d{2}-\d{2}", k["alanlar"].get("Görülme", "")) + [tarih]
        k["alanlar"]["Görülme"] = f"{g} ({', '.join(tarihler)})"
        kaynak = k["alanlar"].get("Kaynak", "").strip()
        k["alanlar"]["Kaynak"] = (kaynak + ", " if kaynak else "karsit ") + f"#{karsit_id}"
        if g >= TERFI_ESIK and k["bolum"] != "liste":
            k["bolum"] = "liste"
            k["terfi"] = True

    def ekle(self, kural: str, ornek: str, karsi: str, kalip: str, tur: str, tarih: str, karsit_id: int):
        k = {"id": self.yeni_id(), "baslik": kural[:80].rstrip("."), "bolum": "aday", "alanlar": {
            "Kural": kural, "Örnek": ornek.replace("\n", " "), "Karşı örnek": karsi.replace("\n", " "),
            "Kalıp": kalip or "", "Tür": tur or "hepsi", "Görülme": f"1 ({tarih})", "Kaynak": f"karsit #{karsit_id}"}}
        self.kurallar.append(k)
        return k

    def yaz(self) -> None:
        def blok(k):
            L = [f"### {k['id']} — {k['baslik']}"]
            for ad in ("Kural", "Örnek", "Karşı örnek", "Kalıp", "Tür", "Görülme", "Kaynak"):
                L.append(f"- {ad}: {k['alanlar'].get(ad, '')}".rstrip())
            return "\n".join(L)
        liste = [k for k in self.kurallar if k["bolum"] == "liste"]
        aday = [k for k in self.kurallar if k["bolum"] != "liste"]
        metin = self.on_metin + self.liste_giris + "\n" + "\n\n".join(blok(k) for k in liste) + ("\n" if liste else "")
        metin += self.aday_giris + "\n" + "\n\n".join(blok(k) for k in aday) + ("\n" if aday else "")
        self.yol.parent.mkdir(parents=True, exist_ok=True)
        self.yol.write_text(metin, encoding="utf-8")

    def tsv(self, yol: Path) -> int:
        satirlar = ["#kalip\tkategori\tsiddet\tipucu", "# karsit_ekle.py üretti; elle düzenleme tercihler.md'ye yapılır."]
        n = 0
        for k in self.kurallar:
            kalip = k["alanlar"].get("Kalıp", "").strip()
            if not kalip:
                continue
            try:
                re.compile(kalip)
            except re.error as e:
                print(f"uyarı: {k['id']} kalıbı geçersiz ({e}), atlandı", file=sys.stderr)
                continue
            siddet = 3 if k["bolum"] == "liste" else 2
            satirlar.append(f"{kalip}\tkisisel\t{siddet}\t[{k['id']}] {k['alanlar'].get('Kural', k['baslik'])}")
            n += 1
        yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        return n


def karsit_ekle(yol: Path, kayit: dict) -> int:
    yol.parent.mkdir(parents=True, exist_ok=True)
    son_id = 0
    if yol.exists():
        for satir in yol.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                try:
                    son_id = max(son_id, int(json.loads(satir).get("id", 0)))
                except (json.JSONDecodeError, ValueError):
                    continue
    kayit = {"id": son_id + 1, "tarih": kayit.get("tarih") or dt.date.today().isoformat(), **{k: v for k, v in kayit.items() if k not in ("id", "tarih")}}
    with yol.open("a", encoding="utf-8") as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
    return kayit["id"]


def komut_ekle(a) -> None:
    voice = a.voice
    if not voice.exists():
        sys.exit(f"{voice} yok. Önce voice.example/ klasörünü voice/ olarak kopyala (kisisel-ses skill'i).")
    if a.dosya:
        kayitlar = json.loads(a.dosya.read_text(encoding="utf-8"))
        if isinstance(kayitlar, dict):
            kayitlar = [kayitlar]
    else:
        if not (a.reddedilen and a.yorum and a.son_hal):
            sys.exit("--reddedilen, --yorum ve --son-hal zorunlu (ya da --dosya)")
        kayitlar = [{"tür": a.tur, "reddedilen": a.reddedilen, "yorum": a.yorum, "son_hal": a.son_hal, "kural_adayı": a.kural, "kalip": a.kalip}]
    t = Tercihler(voice / "tercihler.md")
    bugun = dt.date.today().isoformat()
    ozet = []
    for r in kayitlar:
        r = {k: v for k, v in r.items() if v}
        r.setdefault("tür", a.tur or "hepsi")
        kid = karsit_ekle(voice / "karsit" / "karsit.jsonl", r)
        satir = f"karsit #{kid} eklendi ({r['tür']})"
        kural = r.get("kural_adayı") or r.get("kural")
        if kural:
            mevcut, puan = t.benzer(kural)
            if mevcut:
                t.gorulme_artir(mevcut, bugun, kid)
                if r.get("kalip") and not mevcut["alanlar"].get("Kalıp"):
                    mevcut["alanlar"]["Kalıp"] = r["kalip"]
                satir += f"; {mevcut['id']} görülme {t.gorulme(mevcut)} (benzerlik {puan:.2f})" + (" — KONTROL LİSTESİNE TERFİ" if mevcut.get("terfi") else "")
            else:
                k = t.ekle(kural, r["reddedilen"], r["son_hal"], r.get("kalip", ""), r["tür"], bugun, kid)
                satir += f"; yeni aday {k['id']}: {kural}"
        ozet.append(satir)
    t.yaz()
    n = t.tsv(voice / "tercihler.tsv")
    print("\n".join(ozet))
    print(f"tercihler.md güncellendi; tercihler.tsv {n} kalıp")


def komut_liste(a) -> None:
    t = Tercihler(a.voice / "tercihler.md")
    for bolum, ad in (("liste", "Editör kontrol listesi"), ("aday", "Aday kurallar")):
        print(f"== {ad}")
        for k in t.kurallar:
            if k["bolum"] == bolum:
                print(f"  {k['id']} ×{t.gorulme(k)} [{k['alanlar'].get('Tür', 'hepsi')}] {k['alanlar'].get('Kural', k['baslik'])}" + (f"  /{k['alanlar']['Kalıp']}/" if k['alanlar'].get('Kalıp') else ""))


def komut_terfi(a) -> None:
    t = Tercihler(a.voice / "tercihler.md")
    k = t.bul(a.kid)
    if not k:
        sys.exit(f"{a.kid} yok")
    k["bolum"] = "liste"
    t.yaz()
    t.tsv(a.voice / "tercihler.tsv")
    print(f"{a.kid} kontrol listesine taşındı")


def komut_birlestir(a) -> None:
    t = Tercihler(a.voice / "tercihler.md")
    hedef, kaynak = t.bul(a.hedef), t.bul(a.kaynak)
    if not hedef or not kaynak:
        sys.exit("kural bulunamadı")
    g = t.gorulme(hedef) + t.gorulme(kaynak)
    tarihler = re.findall(r"\d{4}-\d{2}-\d{2}", hedef["alanlar"].get("Görülme", "") + " " + kaynak["alanlar"].get("Görülme", ""))
    hedef["alanlar"]["Görülme"] = f"{g} ({', '.join(sorted(set(tarihler)))})"
    hedef["alanlar"]["Kaynak"] = hedef["alanlar"].get("Kaynak", "") + ", " + kaynak["alanlar"].get("Kaynak", "").replace("karsit ", "")
    if not hedef["alanlar"].get("Kalıp") and kaynak["alanlar"].get("Kalıp"):
        hedef["alanlar"]["Kalıp"] = kaynak["alanlar"]["Kalıp"]
    if g >= TERFI_ESIK:
        hedef["bolum"] = "liste"
    t.kurallar.remove(kaynak)
    t.yaz()
    t.tsv(a.voice / "tercihler.tsv")
    print(f"{a.kaynak} → {a.hedef} birleşti; görülme {g}")


def komut_tsv(a) -> None:
    t = Tercihler(a.voice / "tercihler.md")
    n = t.tsv(a.voice / "tercihler.tsv")
    print(f"tercihler.tsv: {n} kalıp")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice", type=Path, default=Path("voice"))
    alt = ap.add_subparsers(dest="komut", required=True)
    e = alt.add_parser("ekle")
    e.add_argument("--tur")
    e.add_argument("--reddedilen")
    e.add_argument("--yorum")
    e.add_argument("--son-hal")
    e.add_argument("--kural", help="kural adayı, tek cümle")
    e.add_argument("--kalip", help="regex; tercihler.tsv'ye girer")
    e.add_argument("--dosya", type=Path, help="JSON: tek nesne ya da liste")
    e.set_defaults(f=komut_ekle)
    l = alt.add_parser("liste")
    l.set_defaults(f=komut_liste)
    tf = alt.add_parser("terfi")
    tf.add_argument("kid")
    tf.set_defaults(f=komut_terfi)
    b = alt.add_parser("birlestir")
    b.add_argument("hedef")
    b.add_argument("kaynak")
    b.set_defaults(f=komut_birlestir)
    ts = alt.add_parser("tsv")
    ts.set_defaults(f=komut_tsv)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()

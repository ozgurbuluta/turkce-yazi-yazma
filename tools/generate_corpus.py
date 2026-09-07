#!/usr/bin/env python3
"""Faz 6 kalibrasyonu için LLM külliyatı üretir (ya da yalnızca istemleri yazar).

Dört türde (reel, deneme, makale, blog), nötr konularda, birden çok modelle Türkçe
metin üretir; çıktılar corpus/llm/<model>/<tür>/<n>.txt olarak yazılır (gitignore'da).
Sonra tools/derive_patterns.py bunları Leipzig insan metniyle karşılaştırır.

Kullanım:
  python3 tools/generate_corpus.py --istemler                      # yalnızca corpus/istemler.jsonl yaz
  python3 tools/generate_corpus.py --model claude-opus-5 --adet 300   # Anthropic API ile üret
  python3 tools/generate_corpus.py --model claude-opus-5 --konular konular.txt

Anthropic SDK gerekir (pip install anthropic); kimlik ANTHROPIC_API_KEY ya da
`ant auth login`. Başka sağlayıcı için --istemler ile istemleri alıp kendi
döngünüzde kullanın; dosya düzeni aynı kalırsa derive_patterns.py çalışır.
"""
import argparse
import json
import random
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CORPUS = KOK / "corpus"

# Türkçe Vikipedi başlıklarından seçilmiş nötr konular; --konular ile değiştirilebilir.
KONULAR = """
Kapadokya | Boğaziçi Köprüsü | Simit | Türk kahvesi | Lale | Hattuşa | Efes Antik Kenti | Tuz Gölü | Van Gölü | Bozcaada
Nemrut Dağı | Pamukkale | Kaz Dağları | Uludağ | Ihlara Vadisi | Safranbolu evleri | Ebru sanatı | Karagöz ve Hacivat | Nasreddin Hoca | Yunus Emre
Ney | Bağlama | Türk halk müziği | Zeybek | Horon | Yağlı güreş | Cirit | Okçuluk | Hamam | Çini
Kilim | Halı dokuma | Bakırcılık | Zeytinyağı | Baklava | Kuru fasulye | Mantı | Ayran | Boza | Nar
Fındık | İncir | Kayısı | Çay | Pamuk | Tütün | Buğday | Arıcılık | Zeytin ağacı | Meşe
Karadeniz | Ege Denizi | Marmara Denizi | Fırat Nehri | Kızılırmak | Sakarya Nehri | Ağrı Dağı | Toros Dağları | Erciyes | Palandöken
Ankara Kalesi | Galata Kulesi | Ayasofya | Selimiye Camii | Sümela Manastırı | Göbeklitepe | Çatalhöyük | Troya | Aspendos | Perge
Bisiklet | Satranç | Tavla | Uçurtma | Kâğıt | Matbaa | Pusula | Telgraf | Radyo | Fotoğraf
Deprem | Yağmur | Kar | Rüzgâr enerjisi | Güneş enerjisi | Su döngüsü | Volkan | Gelgit | Kuzey Işıkları | Gökkuşağı
Kedi | Köpek | Leylek | Kaplumbağa | Arı | Karınca | Yunus | Kelebek | Baykuş | At
Uyku | Yürüyüş | Yüzme | Ekmek | Süt | Tuz | Şeker | Bal | Su | Ateş
Kütüphane | Okul | Pazar yeri | Tren istasyonu | Liman | Köy | Mahalle | Sokak | Bahçe | Balkon
""".replace("\n", "|").split("|")
KONULAR = [k.strip() for k in KONULAR if k.strip()]

ISTEM = {
    "reel": "{konu} hakkında 20-40 saniyelik bir Instagram reel metni yaz. Türkçe. Sesli okunacak; başlık ve madde imi kullanma.",
    "deneme": "{konu} üzerine 600-900 kelimelik kişisel bir deneme yaz. Türkçe.",
    "makale": "{konu} hakkında 800-1200 kelimelik bilgilendirici bir makale yaz. Türkçe.",
    "blog": "{konu} hakkında 500-800 kelimelik bir blog yazısı yaz. Türkçe.",
}
SISTEM = "Sen Türkçe yazan bir yazarsın. Yalnızca istenen metni yaz; açıklama, başlık önerisi ya da not ekleme."


def istemleri_uret(konular: list, adet: int, tohum: int) -> list:
    rnd = random.Random(tohum)
    turler = list(ISTEM)
    istemler = []
    for i in range(adet):
        konu = konular[i % len(konular)] if adet <= len(konular) else rnd.choice(konular)
        tur = turler[i % len(turler)]
        istemler.append({"no": i + 1, "tur": tur, "konu": konu, "sistem": SISTEM, "istem": ISTEM[tur].format(konu=konu)})
    return istemler


def uret(istemler: list, model: str, hedef: Path) -> None:
    try:
        import anthropic
    except ImportError:
        sys.exit("anthropic paketi yok: pip install anthropic (ya da --istemler ile yalnızca istemleri yazın)")
    client = anthropic.Anthropic()
    for ist in istemler:
        cikti = hedef / model / ist["tur"] / f"{ist['no']:03d}.txt"
        if cikti.exists():
            continue
        cikti.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Sunucu tarafı fallback: model reddederse (stop_reason "refusal") başka modele yönlendirir.
            r = client.beta.messages.create(
                model=model,
                max_tokens=4000,
                system=ist["sistem"],
                messages=[{"role": "user", "content": ist["istem"]}],
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
        except anthropic.RateLimitError as e:
            print(f"{ist['no']}: hız sınırı, dur ({e})", file=sys.stderr)
            break
        except anthropic.APIStatusError as e:
            print(f"{ist['no']}: API hatası {e.status_code}, atlandı", file=sys.stderr)
            continue
        if r.stop_reason == "refusal":
            print(f"{ist['no']}: reddedildi, atlandı", file=sys.stderr)
            continue
        metin = "".join(b.text for b in r.content if b.type == "text")
        cikti.write_text(metin.strip() + "\n", encoding="utf-8")
        print(f"{ist['no']:03d} {ist['tur']:7s} {ist['konu']} → {cikti.relative_to(KOK)} ({len(metin.split())} kelime)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--adet", type=int, default=300)
    ap.add_argument("--konular", type=Path, help="satır başına bir konu")
    ap.add_argument("--tohum", type=int, default=7)
    ap.add_argument("--istemler", action="store_true", help="üretme; corpus/istemler.jsonl yaz")
    ap.add_argument("--hedef", type=Path, default=CORPUS / "llm")
    a = ap.parse_args()
    konular = [s.strip() for s in a.konular.read_text(encoding="utf-8").splitlines() if s.strip()] if a.konular else KONULAR
    istemler = istemleri_uret(konular, a.adet, a.tohum)
    CORPUS.mkdir(exist_ok=True)
    (CORPUS / "istemler.jsonl").write_text("\n".join(json.dumps(i, ensure_ascii=False) for i in istemler) + "\n", encoding="utf-8")
    print(f"{len(istemler)} istem → {CORPUS / 'istemler.jsonl'}")
    if not a.istemler:
        uret(istemler, a.model, a.hedef)


if __name__ == "__main__":
    main()

"""turkce-editor betikleri için testler. pytest ya da `python3 -m unittest` ile çalışır."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SCRIPTS = KOK / "skills" / "turkce-editor" / "scripts"
ORNEK = KOK / "tests" / "ornekler"
sys.path.insert(0, str(SCRIPTS))

import trmetin  # noqa: E402
import metrik  # noqa: E402
import kalip_tara  # noqa: E402
import siklik  # noqa: E402
import yapi  # noqa: E402


def calistir(betik, *args):
    p = subprocess.run([sys.executable, str(SCRIPTS / betik), *args, "--json"], capture_output=True, text=True, check=True)
    return json.loads(p.stdout)


class TrMetinTest(unittest.TestCase):
    def test_tr_lower(self):
        self.assertEqual(trmetin.tr_lower("IŞIK İnsan"), "ışık insan")

    def test_hece(self):
        self.assertEqual(trmetin.hece_sayisi("İstanbul"), 3)
        self.assertEqual(trmetin.hece_sayisi("kağıt"), 2)
        self.assertEqual(trmetin.hece_sayisi("hâlâ"), 2)

    def test_duz(self):
        self.assertEqual(trmetin.duz("hâlâ zekâ Âdil"), "hala zeka Adil")
        self.assertEqual(trmetin.hece_sayisi("brr"), 1)

    def test_cumle_bolme_kisaltma(self):
        c = trmetin.cumlelere_bol("Prof. Dr. Ayşe geldi. Saat 3.5 sularında gitti. Bkz. madde 4. Tamam mı? Evet!")
        self.assertEqual(c, ["Prof. Dr. Ayşe geldi.", "Saat 3.5 sularında gitti.", "Bkz. madde 4.", "Tamam mı?", "Evet!"])

    def test_cumle_bolme_tirnak(self):
        c = trmetin.cumlelere_bol('"Gelecek bunda," dedi. Annem sordu.')
        self.assertEqual(len(c), 2)

    def test_paragraf(self):
        self.assertEqual(len(trmetin.paragraflara_bol("a\n\nb\n\n\nc")), 3)

    def test_markdown_temizle(self):
        t = trmetin.markdown_temizle("# Başlık\n\n- madde **kalın** [bağ](http://x)\n")
        self.assertNotIn("#", t)
        self.assertNotIn("**", t)
        self.assertIn("kalın", t)
        self.assertIn("bağ", t)

    def test_kopyalar_ayni(self):
        asil = (SCRIPTS / "trmetin.py").read_bytes()
        for skill in ("kisisel-ses", "turkce-taslak"):
            kopya = KOK / "skills" / skill / "scripts" / "trmetin.py"
            self.assertTrue(kopya.exists(), kopya)
            self.assertEqual(kopya.read_bytes(), asil, f"{kopya} asıl dosyadan farklı")


class MetrikTest(unittest.TestCase):
    def test_atesman_bant(self):
        self.assertEqual(metrik.atesman_bant(95), "çok kolay")
        self.assertEqual(metrik.atesman_bant(10), "çok zor")

    def test_yuklem(self):
        self.assertEqual(metrik.yuklem_turu("Bu bir sorundur."), "dir")
        self.assertEqual(metrik.yuklem_turu("Çalışmalar sürmektedir."), "maktadir")
        self.assertEqual(metrik.yuklem_turu("Eve gittim."), "di")
        self.assertEqual(metrik.yuklem_turu("Geliyor musun?"), "soru")
        self.assertEqual(metrik.yuklem_turu("Yarın gelecek."), "ecek")

    def test_golden(self):
        kotu = calistir("metrik.py", str(ORNEK / "ceviri_kokulu.md"))
        iyi = calistir("metrik.py", str(ORNEK / "dogal.md"))
        self.assertGreater(kotu["yuklem"]["paylar"].get("-maktadır", 0), 0.4)
        self.assertLess(iyi["yuklem"]["paylar"].get("-maktadır", 0), 0.05)
        self.assertLess(kotu["cumle_uzunlugu"]["cv"], iyi["cumle_uzunlugu"]["cv"])
        self.assertGreater(kotu["ceviri_izleri"]["tarafindan_bin"], 0)
        self.assertEqual(iyi["ceviri_izleri"]["tarafindan_bin"], 0)
        self.assertEqual(iyi["uyarilar"], [])

    def test_tur(self):
        s = calistir("metrik.py", str(ORNEK / "dogal.md"), "--tur", "reel")
        self.assertEqual(s["tur"], "reel")

    def test_bos(self):
        self.assertIn("hata", metrik.hesapla(""))


class KalipTaraTest(unittest.TestCase):
    def setUp(self):
        self.kaliplar = kalip_tara.tsv_yukle(kalip_tara.LISTELER["ai"], "ai") + kalip_tara.tsv_yukle(kalip_tara.LISTELER["ceviri"], "ceviri")

    def test_listeler_yuklenir(self):
        self.assertGreater(len(self.kaliplar), 100)

    def test_bilinen_kaliplar(self):
        s = kalip_tara.tara("Günümüz dünyasında bu konu önemli bir rol oynamaktadır. Rapor bakanlık tarafından hazırlandı.", self.kaliplar)
        eslesen = {b["eslesen"] for b in s["bulgular"]}
        self.assertIn("günümüz dünyasında", eslesen)
        self.assertIn("tarafından", eslesen)
        self.assertTrue(any("rol oyna" in e for e in eslesen))

    def test_golden_puanlari(self):
        kotu = calistir("kalip_tara.py", str(ORNEK / "ceviri_kokulu.md"))
        iyi = calistir("kalip_tara.py", str(ORNEK / "dogal.md"))
        self.assertGreaterEqual(kotu["puan"], 85)
        self.assertLessEqual(iyi["puan"], 20)
        self.assertEqual(kotu["bant"], "makine kokusu")
        self.assertEqual(iyi["bant"], "temiz")

    def test_ayni_kalip_cumlede_bir_kez(self):
        s = kalip_tara.tara("Bu bağlamda bu bağlamda bu bağlamda.", self.kaliplar)
        self.assertEqual(sum(1 for b in s["bulgular"] if b["eslesen"] == "bu bağlamda"), 1)


class SiklikTest(unittest.TestCase):
    def setUp(self):
        self.yazili = siklik.liste_yukle(siklik.VERI / "siklik_yazili.tsv")

    def test_listeler(self):
        self.assertGreater(len(self.yazili), 20000)
        self.assertIn("ve", self.yazili)

    def test_kok_bul(self):
        self.assertIsNotNone(siklik.kok_bul("kitapları", self.yazili))
        self.assertIsNotNone(siklik.kok_bul("kitabı", self.yazili))
        self.assertIsNotNone(siklik.kok_bul("geliyorum", self.yazili))
        self.assertIsNone(siklik.kok_bul("flurbondamak", self.yazili))

    def test_kok_sik_olani_secer(self):
        kok, sira = siklik.kok_bul("sunmaktadır", self.yazili)
        self.assertLess(sira, self.yazili.get("sunmaktadır", 10 ** 9))

    def test_golden(self):
        s = calistir("siklik.py", str(ORNEK / "dogal.md"))
        taninmayan = {t["kelime"] for t in s["taninmayan"]}
        self.assertNotIn("babam", taninmayan)
        self.assertNotIn("bilgisayarı", taninmayan)

    def test_konusma_yazi_dili(self):
        s = calistir("siklik.py", str(ORNEK / "ceviri_kokulu.md"), "--konusma")
        self.assertEqual(s["kayit"], "konusma")
        self.assertGreater(len(s["yazi_dili_sozcugu"]), 3)


class YapiTest(unittest.TestCase):
    def test_uclu(self):
        self.assertTrue(yapi.uclu_mu("Hızlı, güvenilir ve ekonomik bir araç."))
        self.assertTrue(yapi.uclu_mu("Veri gizliliği, dijital eşitsizlik ve öğretmen eğitimi gibi konular."))
        self.assertFalse(yapi.uclu_mu("Kurmak iki gün sürdü, çünkü kitapçık İngilizceydi ve evde İngilizce bilen yoktu."))
        self.assertFalse(yapi.uclu_mu("Bu araçlar, esnek yapıya sahiptir ve çeşitli ihtiyaçlara cevap verebilmektedir."))

    def test_reel_yasaklari(self):
        s = yapi.incele("# Başlık\n\n- madde bir\n- madde iki\n\nMetin.", "reel")
        self.assertTrue(any("[reel]" in u for u in s["uyarilar"]))

    def test_giris_sonuc(self):
        metin = "Uyku sağlık için önemlidir çünkü beyin dinlenir.\n\nOrta paragraf başka şeyler anlatır.\n\nUyku sağlık için önemlidir; beyin dinlenir."
        s = yapi.incele(metin)
        self.assertGreaterEqual(s["giris_sonuc_jaccard"], 0.25)

    def test_golden(self):
        kotu = calistir("yapi.py", str(ORNEK / "ceviri_kokulu.md"))
        iyi = calistir("yapi.py", str(ORNEK / "dogal.md"))
        self.assertTrue(kotu["ozet_kapanisi"])
        self.assertFalse(iyi["ozet_kapanisi"])
        self.assertEqual(iyi["uyarilar"], [])

    def test_tuhaf_unicode(self):
        s = yapi.incele("Bir metin​ burada — ve — orada — yine.")
        self.assertIn("bölünmez boşluk", s["biçim"]["tuhaf_unicode"])
        self.assertTrue(any("Uzun tire" in u for u in s["uyarilar"]))


if __name__ == "__main__":
    unittest.main()

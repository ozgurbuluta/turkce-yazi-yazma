"""kaynak_hizala.py testleri."""
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "skills" / "turkce-yazi" / "scripts"))
import kaynak_hizala as kh  # noqa: E402

ORNEK = KOK / "tests" / "ornekler"


class SayiTest(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(kh.sayi_normalize("12.000"), (12000.0, False))
        self.assertEqual(kh.sayi_normalize("12,000"), (12000.0, False))
        self.assertEqual(kh.sayi_normalize("1.600"), (1600.0, False))
        self.assertEqual(kh.sayi_normalize("58%"), (58.0, True))
        self.assertEqual(kh.sayi_normalize("%58"), (58.0, True))
        self.assertEqual(kh.sayi_normalize("3,5"), (3.5, False))
        self.assertEqual(kh.sayi_normalize("2 milyon"), (2e6, False))

    def test_sayilar(self):
        s = kh.sayilar("Mart 2024'te 12.000 kişiyle %58 ve 1.600 çalışan")
        self.assertIn((12000.0, False), s)
        self.assertIn((58.0, True), s)
        self.assertIn((2024.0, False), s)


class AdTest(unittest.TestCase):
    def test_adlar(self):
        a = kh.adlar("Dün Ankara'da Gallup ile görüştük. Microsoft'un raporu çıktı. Ancak bu doğru değil.")
        self.assertIn("ankara", a)
        self.assertIn("gallup", a)
        self.assertIn("micros", a)
        self.assertNotIn("ancak", a)
        self.assertNotIn("dün", a)

    def test_ay_adlari_disari(self):
        self.assertNotIn("mart", kh.adlar("Bu Mart ayında oldu, Mart soğuktu."))


class HizalaTest(unittest.TestCase):
    def setUp(self):
        self.kaynak = (ORNEK / "kaynak_en.md").read_text(encoding="utf-8")

    def test_ayna(self):
        s = kh.hizala(self.kaynak, (ORNEK / "taslak_ayna.md").read_text(encoding="utf-8"))
        self.assertTrue(s["aynalama"])
        self.assertIn("%20", s["uydurma_sayilar"])
        self.assertIn("micros", s["uydurma_adlar"])
        self.assertTrue(any("Aynalama" in u for u in s["uyarilar"]))

    def test_serbest(self):
        s = kh.hizala(self.kaynak, (ORNEK / "taslak_serbest.md").read_text(encoding="utf-8"))
        self.assertFalse(s["aynalama"])
        self.assertEqual(s["uydurma_sayilar"], [])
        self.assertNotIn("kastle", s["uydurma_adlar"])
        self.assertNotIn("jamie", s["uydurma_adlar"])

    def test_bos_taslak(self):
        s = kh.hizala(self.kaynak, "")
        self.assertFalse(s["aynalama"])
        self.assertEqual(s["taslak_paragraf"], 0)


if __name__ == "__main__":
    unittest.main()

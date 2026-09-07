"""Ses betikleri: ses_ozellikleri.py ve ornek_sec.py (voice.example üzerinde)."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "skills" / "turkce-yazi" / "scripts"))
import ses_ozellikleri as so  # noqa: E402
import ornek_sec as os_  # noqa: E402

ARSIV = KOK / "voice.example" / "onaylanan"


class FrontmatterTest(unittest.TestCase):
    def test_parse(self):
        meta, govde = so.frontmatter("---\ntür: deneme\ntarih: 2025-03-02\netiketler: [a, b]\n---\n\nMetin.")
        self.assertEqual(meta["tür"], "deneme")
        self.assertEqual(meta["etiketler"], ["a", "b"])
        self.assertEqual(govde.strip(), "Metin.")

    def test_yok(self):
        meta, govde = so.frontmatter("Düz metin.")
        self.assertEqual(meta, {})
        self.assertEqual(govde, "Düz metin.")


class OzellikTest(unittest.TestCase):
    def test_arsiv(self):
        dosyalar, uyarilar = so.arsivi_oku(ARSIV)
        self.assertGreaterEqual(len(dosyalar), 2)
        self.assertEqual(uyarilar, [])
        turler = {d["tur"] for d in dosyalar}
        self.assertIn("deneme", turler)
        self.assertIn("reel", turler)

    def test_birlestir(self):
        dosyalar, _ = so.arsivi_oku(ARSIV)
        g = so.birlestir(dosyalar)
        self.assertGreater(g["cumle_cv"], 0.3)
        self.assertIn("-dı", g["yuklem_pay"])
        self.assertLess(g["yuklem_pay"].get("-maktadır", 0), 0.05)
        self.assertIn("anlatı/sahne", g["acilis"])

    def test_acilis(self):
        self.assertEqual(so.acilis_turu("Hiç düşündün mü?"), "soru")
        self.assertEqual(so.acilis_turu("\"Gel,\" dedi."), "alıntı/diyalog")
        self.assertEqual(so.acilis_turu("Babam 1994'te bilgisayar aldı."), "sayı/tarih")
        self.assertEqual(so.acilis_turu("Deneme, kişisel bir yazı türüdür."), "tanım")
        self.assertEqual(so.acilis_turu("Kutusu buzdolabından büyüktü."), "anlatı/sahne")

    def test_profil_yaz_korur(self):
        with tempfile.TemporaryDirectory() as d:
            yol = Path(d) / "profil.md"
            yol.write_text("# Ses profili\n\n<!-- otomatik başlangıç: x -->\neski\n<!-- otomatik son -->\n\n## Elle notlar\n\n- İmza: kısa cümle\n", encoding="utf-8")
            so.profil_yaz(yol, "<!-- otomatik başlangıç: y -->\nyeni\n<!-- otomatik son -->")
            m = yol.read_text(encoding="utf-8")
            self.assertIn("yeni", m)
            self.assertNotIn("eski", m)
            self.assertIn("İmza: kısa cümle", m)


class SecTest(unittest.TestCase):
    def test_tur_oncelik(self):
        s = os_.sec("babam bilgisayar tablet oğlum", ARSIV, tur="reel", k=2)
        self.assertEqual(s[0]["tur"], "reel")
        self.assertTrue(all(0 <= r["benzerlik"] <= 1 for r in s))

    def test_benzerlik_sirali(self):
        s = os_.sec("babam bilgisayar tablet oğlum", ARSIV, k=5)
        puanlar = [r["benzerlik"] for r in s]
        self.assertEqual(puanlar, sorted(puanlar, reverse=True))

    def test_bos_arsiv(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(os_.sec("x", Path(d)), [])

    def test_eski_haric(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copytree(ARSIV, Path(d) / "a")
            (Path(d) / "a" / "blog").mkdir(exist_ok=True)
            (Path(d) / "a" / "blog" / "eski.md").write_text("---\ntür: blog\netiketler: [eski]\n---\nbabam bilgisayar tablet", encoding="utf-8")
            hepsi = os_.sec("babam bilgisayar tablet", Path(d) / "a", k=10)
            haric = os_.sec("babam bilgisayar tablet", Path(d) / "a", k=10, eski_haric=True)
            self.assertEqual(len(hepsi), len(haric) + 1)


if __name__ == "__main__":
    unittest.main()

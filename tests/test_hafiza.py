"""karsit_ekle.py testleri (geçici voice/ kopyası üzerinde)."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
BETIK = KOK / "skills" / "turkce-yazi" / "scripts" / "karsit_ekle.py"
sys.path.insert(0, str(BETIK.parent))
import karsit_ekle as ke  # noqa: E402


class HafizaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.voice = Path(self.tmp) / "voice"
        shutil.copytree(KOK / "voice.example", self.voice)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def calistir(self, *args):
        p = subprocess.run([sys.executable, str(BETIK), "--voice", str(self.voice), *args], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def test_oku(self):
        t = ke.Tercihler(self.voice / "tercihler.md")
        self.assertEqual({k["id"] for k in t.kurallar}, {"K1", "K2"})
        self.assertEqual(t.bul("K1")["bolum"], "liste")
        self.assertEqual(t.bul("K2")["bolum"], "aday")
        self.assertEqual(t.gorulme(t.bul("K1")), 3)

    def test_benzer_bulur(self):
        t = ke.Tercihler(self.voice / "tercihler.md")
        k, p = t.benzer("Meslek adı verme, süreci anlat")
        self.assertEqual(k["id"], "K1")
        k, p = t.benzer("Uzun tire kullanma, virgül yaz")
        self.assertIsNone(k)

    def test_ekle_yeni_ve_terfi(self):
        out = self.calistir("ekle", "--tur", "blog", "--reddedilen", "Bu — uzun tire.", "--yorum", "tire", "--son-hal", "Bu, virgül.", "--kural", "Uzun tire kullanma, virgül yaz", "--kalip", "—")
        self.assertIn("yeni aday K3", out)
        satirlar = (self.voice / "karsit" / "karsit.jsonl").read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(json.loads(satirlar[-1])["id"], 5)
        self.assertIn("—\tkisisel\t2", (self.voice / "tercihler.tsv").read_text(encoding="utf-8"))

        for _ in range(2):
            out = self.calistir("ekle", "--tur", "reel", "--reddedilen", "x — y", "--yorum", "tire", "--son-hal", "x, y", "--kural", "uzun tire kullanma virgül yaz")
        self.assertIn("TERFİ", out)
        t = ke.Tercihler(self.voice / "tercihler.md")
        self.assertEqual(t.bul("K3")["bolum"], "liste")
        self.assertEqual(t.gorulme(t.bul("K3")), 3)
        self.assertIn("—\tkisisel\t3", (self.voice / "tercihler.tsv").read_text(encoding="utf-8"))

    def test_ekle_dosya(self):
        d = Path(self.tmp) / "u.json"
        d.write_text(json.dumps([{"tür": "deneme", "reddedilen": "a", "yorum": "b", "son_hal": "c"}, {"tür": "deneme", "reddedilen": "d", "yorum": "e", "son_hal": "f", "kural_adayı": "'deneyim' yerine ne yaşandığını yaz"}]), encoding="utf-8")
        out = self.calistir("ekle", "--dosya", str(d))
        self.assertIn("karsit #5 eklendi", out)
        self.assertIn("K2 görülme 2", out)

    def test_liste_ve_terfi(self):
        self.calistir("terfi", "K2")
        out = self.calistir("liste")
        liste, aday = out.split("== Aday kurallar")
        self.assertIn("K2", liste)
        self.assertNotIn("K2", aday)

    def test_birlestir(self):
        self.calistir("ekle", "--tur", "blog", "--reddedilen", "a", "--yorum", "b", "--son-hal", "c", "--kural", "Meslek unvanı yazma, işi yaz")
        t = ke.Tercihler(self.voice / "tercihler.md")
        if t.bul("K3") is None:
            self.skipTest("benzer kural otomatik birleşti")
        self.calistir("birlestir", "K1", "K3")
        t = ke.Tercihler(self.voice / "tercihler.md")
        self.assertIsNone(t.bul("K3"))
        self.assertEqual(t.gorulme(t.bul("K1")), 4)

    def test_voice_yoksa(self):
        p = subprocess.run([sys.executable, str(BETIK), "--voice", str(Path(self.tmp) / "yok"), "ekle", "--reddedilen", "a", "--yorum", "b", "--son-hal", "c"], capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("voice.example", p.stderr)


if __name__ == "__main__":
    unittest.main()

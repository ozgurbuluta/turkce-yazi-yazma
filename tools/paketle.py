#!/usr/bin/env python3
"""dist/ altına dağıtım paketleri üretir.

  dist/turkce-yazi.zip      Claude.ai ve Cowork: Ayarlar → Skills → yükle
  dist/chatgpt/             Custom GPT: instructions.md talimatlara, knowledge/ bilgi dosyalarına, scripts/ Code Interpreter için

Kullanım: python3 tools/paketle.py
"""
import re
import shutil
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SKILL = KOK / "skills" / "turkce-yazi"
DIST = KOK / "dist"


def zip_yap() -> Path:
    hedef = DIST / "turkce-yazi.zip"
    with zipfile.ZipFile(hedef, "w", zipfile.ZIP_DEFLATED) as z:
        for yol in sorted(SKILL.rglob("*")):
            if yol.is_file() and "__pycache__" not in yol.parts:
                z.write(yol, yol.relative_to(SKILL.parent))
        for yol in sorted((KOK / "voice.example").rglob("*")):
            if yol.is_file():
                z.write(yol, Path("turkce-yazi") / yol.relative_to(KOK))
    return hedef


def chatgpt_talimat() -> str:
    metin = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    metin = re.sub(r"^---\n.*?\n---\n", "", metin, flags=re.S)
    # Betik komut bloklarını ve dosya listesini çıkar; GPT'de bilgi dosyaları olarak yüklenir
    metin = re.sub(r"```bash\n.*?```\n", "", metin, flags=re.S)
    metin = re.sub(r"```\n.*?```\n", "", metin, flags=re.S)
    metin = metin.split("## Dosyalar")[0]
    metin = metin.replace("`scripts/` bu dosyanın yanındadır. Metni dosyaya yaz, dördünü çalıştır:", "Code Interpreter açıksa yüklü betikleri çalıştır (metrik.py, kalip_tara.py, siklik.py, yapi.py; --help açıklar). Kapalıysa bilgi dosyalarındaki listeleri elle uygula ve bunu söyle.")
    bas = ("Sen Türkçe yazı editörü ve yazarısın. Aşağıdaki yönergeyi uygula; ayrıntılı kural katalogları "
           "bilgi dosyalarındadır (kaliplar.md, ceviri-kokusu.md, ritim.md, turler.md, puanlama.md, bilgi-karti.md, ses.md); "
           "gerektiğinde onları oku. Kullanıcının kendi kuralları bu talimatın sonundaki 'Kullanıcı tercihleri' bölümündedir "
           "ve her şeyden önce gelir.\n\n")
    son = "\n\n## Kullanıcı tercihleri\n\n(Buraya 'bunu hatırla' çıktılarını yapıştır.)\n"
    return bas + metin.strip() + son


def chatgpt_paketi() -> Path:
    hedef = DIST / "chatgpt"
    if hedef.exists():
        shutil.rmtree(hedef)
    (hedef / "knowledge").mkdir(parents=True)
    (hedef / "scripts").mkdir()
    talimat = chatgpt_talimat()
    (hedef / "instructions.md").write_text(talimat, encoding="utf-8")
    for f in (SKILL / "references").glob("*.md"):
        shutil.copy(f, hedef / "knowledge" / f.name)
    for f in (SKILL / "data").glob("*"):
        if f.suffix in (".tsv", ".txt", ".md"):
            shutil.copy(f, hedef / "knowledge" / f.name)
    for f in (SKILL / "scripts").glob("*.py"):
        shutil.copy(f, hedef / "scripts" / f.name)
    (hedef / "NASIL.md").write_text(
        "# ChatGPT Custom GPT kurulumu\n\n"
        "1. ChatGPT → Explore GPTs → Create → Configure.\n"
        "2. Instructions kutusuna `instructions.md` içeriğini yapıştır"
        f" ({len(talimat)} karakter; sınır 8.000 ise 'Sık düşülen editör hataları' bölümünü kısalt).\n"
        "3. Knowledge'a `knowledge/` içindeki tüm dosyaları yükle.\n"
        "4. Capabilities → Code Interpreter'ı aç ve `scripts/` içindeki .py dosyalarını da Knowledge'a yükle;"
        " GPT betikleri oradan çalıştırır. Kapalıysa betiksiz, listelerle çalışır.\n"
        "5. 'Bunu hatırla' çıktılarını Instructions sonundaki 'Kullanıcı tercihleri' bölümüne yapıştır.\n",
        encoding="utf-8")
    return hedef


def main() -> None:
    DIST.mkdir(exist_ok=True)
    z = zip_yap()
    c = chatgpt_paketi()
    print(f"{z.relative_to(KOK)}  {z.stat().st_size // 1024} KB")
    print(f"{c.relative_to(KOK)}/  instructions.md {len((c / 'instructions.md').read_text(encoding='utf-8'))} karakter")


if __name__ == "__main__":
    main()

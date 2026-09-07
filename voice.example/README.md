# voice.example — kişisel ses arşivi şablonu

Bu klasör, depo ile birlikte dağıtılan **şablondur**; içindeki metinler uydurmadır.
Kendi arşivini kurmak için:

```bash
cp -r voice.example voice
rm voice/onaylanan/*/*.md voice/karsit/karsit.jsonl   # örnekleri at
# kendi metinlerini voice/onaylanan/<tür>/ altına koy (frontmatter ile)
python3 skills/kisisel-ses/scripts/ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
```

`voice/` gitignore'dadır; hiçbir zaman commit edilmez. Yapı ve alanlar için
`skills/kisisel-ses/references/arsiv-yapisi.md`.

```
voice/
├── profil.md              # otomatik bölüm + Elle notlar
├── tercihler.md           # kurallar (geri-bildirim-hafizasi yönetir)
├── tercihler.tsv          # (otomatik) regex listesi
├── onaylanan/{reel,deneme,makale,blog}/*.md
└── karsit/karsit.jsonl
```

# AGENTS.md

Bu depo Türkçe yazı için beş skill taşır. Ajan olarak buradaysan görevine göre
tek bir skill'den başla; skill seni gerekirse diğerlerine yönlendirir.

## Skill kataloğu

| Görev | Başlangıç skill'i | Sonra |
|---|---|---|
| Türkçe metni incele / düzelt / puanla | `skills/turkce-editor/SKILL.md` | `tur-profilleri` (tür belliyse), `kisisel-ses` (voice/ varsa), bitince `geri-bildirim-hafizasi` |
| Notlardan ya da İngilizce kaynaktan Türkçe taslak | `skills/turkce-taslak/SKILL.md` | `tur-profilleri`, `kisisel-ses`, sonra `turkce-editor` |
| "Reel / deneme / makale / blog kurallarına uy" | `skills/tur-profilleri/SKILL.md` + `profiller/<tür>.md` | — |
| "Benim sesimle yaz", ses arşivi kur | `skills/kisisel-ses/SKILL.md` | — |
| "Bunu hatırla / bir daha yapma" | `skills/geri-bildirim-hafizasi/SKILL.md` | — |

Otomatik tetiklenen (kullanıcı ad vermeden) skill'ler: `turkce-editor`,
`turkce-taslak`. Diğer üçü açık istekle ya da bu ikisinin yönlendirmesiyle açılır.

## Düzen

```
skills/<ad>/SKILL.md        # frontmatter (name, description) + Türkçe yönerge
skills/<ad>/references/     # kural katalogları; SKILL.md gerektiğinde işaret eder
skills/<ad>/scripts/        # stdlib Python; hepsi --json alır, --help açıklar
skills/<ad>/data/           # yalnızca turkce-editor: TSV kalıp ve sıklık listeleri
voice/                      # kişisel arşiv; gitignore; şablon voice.example/
tools/                      # veri indirme ve kalibrasyon; skill'ler bunlara bağımlı değil
tests/                      # python3 -m unittest discover tests (pytest de çalışır)
docs/                       # yontem.md (kalibrasyon), kaynaklar.md (lisans), arastirma.md
```

Her skill klasörü kendi başına çalışır (Claude.ai'ye tek klasör zip'lenebilir).
`trmetin.py` üç skill'de birebir kopyadır; `tests/test_editor.py` aynılığı
denetler. Birini değiştirirsen üçünü değiştir:
`skills/{turkce-editor,kisisel-ses,turkce-taslak}/scripts/trmetin.py`.

## Betikleri çalıştırma

Skill klasöründen göreli yol: `python3 scripts/metrik.py metin.md --tur deneme`.
Depo kökünden: `python3 skills/turkce-editor/scripts/metrik.py ...`. Claude.ai'de
`/mnt/skills/<ad>/scripts/...`. Betikler stdin de okur (`-`).

Betik çalıştıramıyorsan `references/` içindeki listeleri elle uygula ve raporda
söyle; betik çıktısı uydurulmaz.

## Kurallar (tüm skill'ler)

1. Kaynakta olmayan olgu, sayı, ad, iddia yazılmaz; kaldırılan iddia listelenir.
2. Skill metni Türkçedir; kullanıcıya Türkçe yanıt verilir (kullanıcı İngilizce
   yazmadıysa).
3. `voice/` içeriği hiçbir çıktıya, commit'e, özet dosyasına kopyalanmaz.
4. Derlem sorgusu yapmış gibi davranılmaz; emin olunamayan kalıp için TNC/TS
   Corpus sorgusu önerilir (`docs/kaynaklar.md`).
5. Uzun tire (—) ve markdown süsü eklenmez; reel'de hiç markdown olmaz.
   Düzeltme işareti (â, î, û) hiçbir metinde kullanılmaz: zeka, hala, kağıt.
6. Tür profili ile kullanıcı profili çelişirse kullanıcı kazanır, çelişki söylenir.

## Değişiklik yaparken

- Kalıp eklerken `data/*.tsv` sütun düzenine uy; `tests/ornekler/dogal.md` üzerinde
  yanlış pozitif verme (`kalip_tara.py` puanı ≤ 20 kalmalı).
- Eşik değiştirirken üç yeri birlikte güncelle: `metrik.py TUR_HEDEF`,
  `tur-profilleri/profiller/*.md`, `turkce-editor/references/ritim.md`.
- Yeni tür eklerken: profil → `TUR_HEDEF` → `voice.example/onaylanan/<tür>/`.
- `python3 -m unittest discover tests` yeşil kalmalı.

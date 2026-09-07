# AGENTS.md

Bu depo tek bir skill taşır: `skills/turkce-yazi/`. Türkçe metin düzeltir, notlardan
ya da İngilizce kaynaktan Türkçe taslak yazar, tür kurallarını ve yazarın kendi
sesini uygular. Ajan olarak buradaysan `skills/turkce-yazi/SKILL.md` ile başla;
gerisini o yönlendirir.

## Düzen

```
skills/turkce-yazi/SKILL.md     # tek giriş: düzelt, incele, puanla, yaz, hatırla
skills/turkce-yazi/references/  # kalıplar, çeviri kokusu, ritim, puanlama, türler, bilgi kartı, ses
skills/turkce-yazi/scripts/     # stdlib Python; hepsi --json ve --help alır
skills/turkce-yazi/data/        # kalıp TSV'leri ve sıklık listeleri (lisanslar data/LICENSES.md)
voice.example/                  # kişisel arşiv şablonu; gerçek arşiv voice/ (gitignore)
tools/                          # veri indirme, kalibrasyon, paketleme (skill bunlara bağımlı değil)
tests/                          # python3 -m unittest discover tests
docs/                           # yontem.md, kaynaklar.md, arastirma.md
dist/                           # tools/paketle.py üretir; gitignore
```

## Betikleri çalıştırma

Skill klasöründen: `python3 scripts/metrik.py metin.md --tur deneme`. Depo
kökünden: `python3 skills/turkce-yazi/scripts/metrik.py ...`. Claude.ai'de
`/mnt/skills/turkce-yazi/scripts/...`. Betikler stdin de okur (`-`). Betik
çalıştıramıyorsan `references/` listelerini elle uygula ve bunu söyle; çıktı
uydurulmaz.

## Kurallar

1. Kaynakta olmayan olgu, sayı, ad, iddia yazılmaz; kaldırılan iddia listelenir.
2. Skill metni Türkçedir; kullanıcıya Türkçe yanıt verilir (kullanıcı İngilizce
   yazmadıysa).
3. `voice/` içeriği hiçbir çıktıya, commit'e, özet dosyasına kopyalanmaz.
4. Derlem sorgusu yapmış gibi davranılmaz; emin olunamayan kalıp için TNC/TS
   Corpus sorgusu önerilir (`docs/kaynaklar.md`).
5. Uzun tire (—) ve markdown süsü eklenmez; reel'de hiç markdown olmaz. Düzeltme
   işareti (â, î, û) hiçbir metinde kullanılmaz: zeka, hala, kağıt.
6. Tür profili ile kullanıcı profili çelişirse kullanıcı kazanır, çelişki söylenir.
7. Kullanıcıya yazarken metin anlatılır, depo değil: betik adı, dosya yolu, skill
   adı, kategori kodu, JSON yanıtta yer almaz. Bulgu kuralın adıyla değil cümleyle
   söylenir.
8. Betik sayıları işarettir, kural değil. Kararı paragraf verir: bağlamak mı bölmek
   mi, vuruş mu gevezelik mi; ölçüt paragraf ya da kullanıcının kendi metniyle
   karşılaştırılarak.

## Değişiklik yaparken

- Kalıp eklerken `data/*.tsv` sütun düzenine uy; `tests/ornekler/dogal.md` üzerinde
  yanlış pozitif verme (`kalip_tara.py` puanı ≤ 20 kalmalı).
- Eşik değiştirirken üç yeri birlikte güncelle: `metrik.py TUR_HEDEF`,
  `references/turler.md`, `references/ritim.md`.
- SKILL.md değişince `python3 tools/paketle.py` ile paketleri yeniden üret ve
  GitHub Release'i güncelle.
- `python3 -m unittest discover tests` yeşil kalmalı.

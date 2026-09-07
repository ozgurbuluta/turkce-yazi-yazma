# Arşiv yapısı

```
voice/                      # gitignore'da; kişisel
├── profil.md               # ses_ozellikleri.py üretir + "Elle notlar" bölümü
├── tercihler.md            # kural listesi; geri-bildirim-hafizasi yönetir
├── tercihler.tsv           # (isteğe bağlı) kalip_tara.py --ek için regex listesi
├── onaylanan/
│   ├── reel/*.md
│   ├── deneme/*.md
│   ├── makale/*.md
│   └── blog/*.md
└── karsit/
    └── karsit.jsonl        # reddedilen / yorum / son_hal üçlüleri
```

Tür klasörü adları `tur-profilleri` skill'indeki profil adlarıyla aynıdır. Yeni
tür eklenirse önce profili yazılır, sonra klasörü açılır.

## Onaylanan metin dosyası

```markdown
---
tür: deneme
tarih: 2025-03-02
konu: babamın 1994'te aldığı ilk bilgisayar
etiketler: [aile, teknoloji, çocukluk]
kaynak: https://... (isteğe bağlı; yayımlandıysa)
---

Babam ilk bilgisayarı eve 1994'te getirdi. ...
```

- `tür` zorunlu; klasörle aynı olmalı (betik uyuşmazlığı söyler).
- `tarih` ISO (YYYY-AA-GG). Profil hesabında yeni metinler ağırlıklı değildir ama
  `ornek_sec.py` eşit puanda yeniyi seçer.
- `konu` tek satır; `ornek_sec.py` bunu içerik sözcükleriyle birlikte kullanır.
- `etiketler` köşeli parantezli virgüllü liste ya da düz virgüllü liste.
- Gövde düz metin/markdown. Başlık gövdeye yazılmaz; `konu` alanı yeter.

## Ne "onaylanmış" sayılır

Evet:
- Yazarın yayımladığı metin (son hâli, editör düzeltmesi yazarın onayıyla).
- Yazarın "bu benim sesim" dediği yayımlanmamış metin.
- `geri-bildirim-hafizasi` oturumundan çıkan, yazarın onayladığı son hâl.

Hayır:
- LLM taslağı, düzeltilmemiş.
- Çeviri.
- Başkasının yazıp yazarın paylaştığı metin.
- Yazarın "eskiden böyle yazardım" dediği metin (isteniyorsa `etiketler: [eski]`
  ile koyulur; `ornek_sec.py --eski-haric` ile dışlanır).

## Boyut

Profil için tür başına 3, toplam 5 metin alt sınır. Üst sınır yok; ama
`ornek_sec.py` her görevde en fazla k=3 seçer, arşiv büyüdükçe seçim iyileşir,
bağlam büyümez.

## Gizlilik

`voice/` gitignore'dadır. Depoyu açık paylaşıyorsan `voice/` asla eklenmez;
`voice.example/` yalnızca şablon ve uydurma örnek taşır. Özel bir üst depo
isteniyorsa `voice/` ayrı bir özel repo olarak klonlanıp bu klasöre bağlanabilir.

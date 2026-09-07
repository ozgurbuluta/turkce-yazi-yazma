# Kişisel ses: arşiv, karşıt örnekler, tercihler


---

## Arşiv yapısı

```
voice/                      # gitignore'da; kişisel
├── profil.md               # ses_ozellikleri.py üretir + "Elle notlar" bölümü
├── tercihler.md            # kural listesi; karsit_ekle.py yönetir
├── tercihler.tsv           # (isteğe bağlı) kalip_tara.py --ek için regex listesi
├── onaylanan/
│   ├── reel/*.md
│   ├── deneme/*.md
│   ├── makale/*.md
│   └── blog/*.md
└── karsit/
    └── karsit.jsonl        # reddedilen / yorum / son_hal üçlüleri
```

Tür klasörü adları `references/turler.md` içindeki tür adlarıyla aynıdır. Yeni
tür eklenirse önce profili yazılır, sonra klasörü açılır.

### Onaylanan metin dosyası

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

### Ne "onaylanmış" sayılır

Evet:
- Yazarın yayımladığı metin (son hali, editör düzeltmesi yazarın onayıyla).
- Yazarın "bu benim sesim" dediği yayımlanmamış metin.
- "hatırla" adımından çıkan, yazarın onayladığı son hal.

Hayır:
- LLM taslağı, düzeltilmemiş.
- Çeviri.
- Başkasının yazıp yazarın paylaştığı metin.
- Yazarın "eskiden böyle yazardım" dediği metin (isteniyorsa `etiketler: [eski]`
  ile koyulur; `ornek_sec.py --eski-haric` ile dışlanır).

### Boyut

Profil için tür başına 3, toplam 5 metin alt sınır. Üst sınır yok; ama
`ornek_sec.py` her görevde en fazla k=3 seçer, arşiv büyüdükçe seçim iyileşir,
bağlam büyümez.

### Gizlilik

`voice/` gitignore'dadır. Depoyu açık paylaşıyorsan `voice/` asla eklenmez;
`voice.example/` yalnızca şablon ve uydurma örnek taşır. Özel bir üst depo
isteniyorsa `voice/` ayrı bir özel repo olarak klonlanıp bu klasöre bağlanabilir.

---

## Karşıt örnekler

Bir metnin nasıl yazıldığını göstermek yetmez; nasıl yazılmadığını da göstermek
gerekir. Karşıt çift, aynı yerde reddedilen ve kabul edilen iki hali yan yana koyar
ve nedenini söyler. Araştırma (Yazan, Verberne, Situmeang 2025; `docs/arastirma.md`)
bu çiftlerin, yalnızca olumlu örnek vermeye göre üslup uyumunu ölçülebilir biçimde
artırdığını gösteriyor.

### Dosya: `voice/karsit/karsit.jsonl`

Satır başına bir JSON nesnesi:

```json
{"id": 12, "tarih": "2026-09-07", "tür": "deneme", "reddedilen": "Bu deneyim bana hayatın her alanında sabırlı olmayı öğretti.", "yorum": "İngilizceden çevrilmiş gibi; 'deneyim' ve 'hayatın her alanında' benim ağzımdan çıkmaz.", "son_hal": "O yaz sabrı öğrendim; başka çare yoktu.", "kural_adayı": "'deneyim' yerine ne yaşandığını yaz"}
```

Alanlar:

| Alan | Zorunlu | Açıklama |
|---|---|---|
| `id` | evet | Artan tam sayı; `karsit_ekle.py` verir |
| `tarih` | evet | ISO |
| `tür` | evet | reel / deneme / makale / blog |
| `reddedilen` | evet | Reddedilen cümle ya da paragraf, olduğu gibi |
| `yorum` | evet | Yazarın ya da editörün nedeni, yazarın sözcükleriyle |
| `son_hal` | evet | Kabul edilen hal |
| `kural_adayı` | hayır | Tek cümlelik genelleme; `tercihler.md`'ye gider |
| `kalip` | hayır | Reddedileni yakalayan regex; `tercihler.tsv`'ye gider |

Ekleme `karsit_ekle.py` ile yapılır; elle
de yazılabilir.

### Bağlamda sunum

Görev öncesi en fazla 4 çift seçilir: önce aynı tür, sonra en yeni. Biçim:

```
#### Karşıt örnekler
1. Reddedilen: "Bu deneyim bana hayatın her alanında sabırlı olmayı öğretti."
   Neden: İngilizceden çevrilmiş gibi; "deneyim" ve "hayatın her alanında" benim ağzımdan çıkmaz.
   Kabul edilen: "O yaz sabrı öğrendim; başka çare yoktu."

2. Reddedilen: ...
```

"Neden" satırı yazarın sesinden aktarılır; editörün yorumu ise "editör:" diye
işaretlenir. Çift sunulurken kural olarak yeniden yazılmaz; kural `tercihler.md`'de
zaten vardır. Çift, kuralın somut kanıtıdır.

### Ne çift olur, ne olmaz

Olur:
- Yazarın yeniden yazdığı ya da "bunu değil şunu" dediği her yer.
- Editörün önerip yazarın kabul ettiği düzeltme (yorum: "editör: ...").

Olmaz:
- Yazım hatası düzeltmeleri.
- Olgu düzeltmeleri (yanlış tarih, yanlış sayı).
- Yazarın "fark etmez" dediği değişiklikler.

Çift toplamaya değecek şey, sesle ilgili olandır.

---

## tercihler.md biçimi

`karsit_ekle.py` bu dosyayı okur ve yazar; elle de düzenlenebilir. Betik yalnızca
`### K<n> — ...` bloklarını tanır; başlık dışı metne dokunmaz.

```markdown
### Tercihler

### Editör kontrol listesi

Buradaki kurallar editör tarafından her oturumun başında okunur ve
genel kurallardan önce gelir.

#### K3 — Meslek adı verme, süreci anlat
- Kural: "Yazılımcıyım" yerine "kod yazıyorum"; kimliği değil işi yaz.
- Örnek: Yazılımcı olarak bunu her gün görüyorum.
- Karşı örnek: Her gün kod yazıyorum, bunu görüyorum.
- Kalıp: \b(yazılımcı|mühendis|tasarımcı)(yım|yim|ım|im)\b
- Tür: hepsi
- Görülme: 4 (2026-08-01, 2026-08-12, 2026-09-01, 2026-09-07)
- Kaynak: karsit #3, #7, #12, #15

### Aday kurallar

Üç kez görülünce yukarı taşınır.

#### K7 — "yalnızca X değil Y" kurma
- Kural: İki iddiayı ayrı cümle yap.
- Örnek: Yalnızca hızlı değil, aynı zamanda ucuz.
- Karşı örnek: Hızlı. Ucuz da.
- Kalıp:
- Tür: hepsi
- Görülme: 1 (2026-09-07)
- Kaynak: karsit #16
```

### Alanlar

| Alan | Zorunlu | Not |
|---|---|---|
| `### K<n> — <başlık>` | evet | `n` artan; başlık kuralın kısa hali |
| Kural | evet | Tek cümle, yerine ne yazılacağı dahil |
| Örnek | evet | Reddedilen cümle (kullanıcının metninden) |
| Karşı örnek | evet | Son hal |
| Kalıp | hayır | Python regex, `tr_lower` uygulanmış metne; boşsa TSV'ye girmez |
| Tür | hayır | `hepsi` ya da tür adı |
| Görülme | evet | Sayı ve tarih listesi; betik günceller |
| Kaynak | evet | `karsit.jsonl` id'leri |

### tercihler.tsv

`Kalıp` alanı dolu kurallardan üretilir; `kalip_tara.py --ek voice/tercihler.tsv`
ile taramaya girer. Sütunlar `ai_kaliplari.tsv` ile aynı:
`kalip<TAB>kategori<TAB>siddet<TAB>ipucu`. Kategori `kisisel`, şiddet kontrol
listesindekiler için 3, adaylar için 2, ipucu kural metnidir.

### Benzer kural birleştirme

Yeni kural eklenirken mevcut kuralların "Kural" ve başlık satırlarıyla sözcük
Jaccard benzerliği hesaplanır (ilk 6 harf gövdesi, durak sözcükler dışarıda).
≥ 0,6 ise aynı kural sayılır, görülme artar. Betik yanlış birleştirirse
`birlestir`/elle düzenleme ile ayrılır; kullanıcı her zaman haklıdır.

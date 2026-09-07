# tercihler.md biçimi

`karsit_ekle.py` bu dosyayı okur ve yazar; elle de düzenlenebilir. Betik yalnızca
`### K<n> — ...` bloklarını tanır; başlık dışı metne dokunmaz.

```markdown
# Tercihler

## Editör kontrol listesi

Buradaki kurallar `turkce-editor` tarafından her oturumun başında okunur ve
genel kurallardan önce gelir.

### K3 — Meslek adı verme, süreci anlat
- Kural: "Yazılımcıyım" yerine "kod yazıyorum"; kimliği değil işi yaz.
- Örnek: Yazılımcı olarak bunu her gün görüyorum.
- Karşı örnek: Her gün kod yazıyorum, bunu görüyorum.
- Kalıp: \b(yazılımcı|mühendis|tasarımcı)(yım|yim|ım|im)\b
- Tür: hepsi
- Görülme: 4 (2026-08-01, 2026-08-12, 2026-09-01, 2026-09-07)
- Kaynak: karsit #3, #7, #12, #15

## Aday kurallar

Üç kez görülünce yukarı taşınır.

### K7 — "yalnızca X değil Y" kurma
- Kural: İki iddiayı ayrı cümle yap.
- Örnek: Yalnızca hızlı değil, aynı zamanda ucuz.
- Karşı örnek: Hızlı. Ucuz da.
- Kalıp:
- Tür: hepsi
- Görülme: 1 (2026-09-07)
- Kaynak: karsit #16
```

## Alanlar

| Alan | Zorunlu | Not |
|---|---|---|
| `### K<n> — <başlık>` | evet | `n` artan; başlık kuralın kısa hâli |
| Kural | evet | Tek cümle, yerine ne yazılacağı dahil |
| Örnek | evet | Reddedilen cümle (kullanıcının metninden) |
| Karşı örnek | evet | Son hâl |
| Kalıp | hayır | Python regex, `tr_lower` uygulanmış metne; boşsa TSV'ye girmez |
| Tür | hayır | `hepsi` ya da tür adı |
| Görülme | evet | Sayı ve tarih listesi; betik günceller |
| Kaynak | evet | `karsit.jsonl` id'leri |

## tercihler.tsv

`Kalıp` alanı dolu kurallardan üretilir; `kalip_tara.py --ek voice/tercihler.tsv`
ile taramaya girer. Sütunlar `ai_kaliplari.tsv` ile aynı:
`kalip<TAB>kategori<TAB>siddet<TAB>ipucu`. Kategori `kisisel`, şiddet kontrol
listesindekiler için 3, adaylar için 2, ipucu kural metnidir.

## Benzer kural birleştirme

Yeni kural eklenirken mevcut kuralların "Kural" ve başlık satırlarıyla sözcük
Jaccard benzerliği hesaplanır (ilk 6 harf gövdesi, durak sözcükler dışarıda).
≥ 0,6 ise aynı kural sayılır, görülme artar. Betik yanlış birleştirirse
`birlestir`/elle düzenleme ile ayrılır; kullanıcı her zaman haklıdır.

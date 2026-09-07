# Karşıt örnekler

Bir metnin nasıl yazıldığını göstermek yetmez; nasıl yazılmadığını da göstermek
gerekir. Karşıt çift, aynı yerde reddedilen ve kabul edilen iki hâli yan yana koyar
ve nedenini söyler. Araştırma (Yazan, Verberne, Situmeang 2025; `docs/arastirma.md`)
bu çiftlerin, yalnızca olumlu örnek vermeye göre üslup uyumunu ölçülebilir biçimde
artırdığını gösteriyor.

## Dosya: `voice/karsit/karsit.jsonl`

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
| `son_hal` | evet | Kabul edilen hâl |
| `kural_adayı` | hayır | Tek cümlelik genelleme; `tercihler.md`'ye gider |
| `kalip` | hayır | Reddedileni yakalayan regex; `tercihler.tsv`'ye gider |

Ekleme `geri-bildirim-hafizasi` skill'indeki `karsit_ekle.py` ile yapılır; elle
de yazılabilir.

## Bağlamda sunum

Görev öncesi en fazla 4 çift seçilir: önce aynı tür, sonra en yeni. Biçim:

```
### Karşıt örnekler
1. Reddedilen: "Bu deneyim bana hayatın her alanında sabırlı olmayı öğretti."
   Neden: İngilizceden çevrilmiş gibi; "deneyim" ve "hayatın her alanında" benim ağzımdan çıkmaz.
   Kabul edilen: "O yaz sabrı öğrendim; başka çare yoktu."

2. Reddedilen: ...
```

"Neden" satırı yazarın sesinden aktarılır; editörün yorumu ise "editör:" diye
işaretlenir. Çift sunulurken kural olarak yeniden yazılmaz; kural `tercihler.md`'de
zaten vardır. Çift, kuralın somut kanıtıdır.

## Ne çift olur, ne olmaz

Olur:
- Yazarın yeniden yazdığı ya da "bunu değil şunu" dediği her yer.
- Editörün önerip yazarın kabul ettiği düzeltme (yorum: "editör: ...").

Olmaz:
- Yazım hatası düzeltmeleri.
- Olgu düzeltmeleri (yanlış tarih, yanlış sayı).
- Yazarın "fark etmez" dediği değişiklikler.

Çift toplamaya değecek şey, sesle ilgili olandır.

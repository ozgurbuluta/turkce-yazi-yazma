# Yöntem: kalıp listeleri ve eşikler nasıl türetilir

Bu depo iki tür bilgi taşır: **kural** (skill metinleri, referanslar) ve **ölçü**
(kalıp listeleri, metrik eşikleri). Kurallar editör deneyimine dayanır; ölçüler
veriden gelmelidir. Bu belge ölçülerin nasıl üretildiğini ve nasıl güncelleneceğini
anlatır.

## Sürüm durumu

| Ölçü | Durum | Kaynak |
|---|---|---|
| `ai_kaliplari.tsv` | **Elle tohumlanmış** (v0) | Editör deneyimi + Türkçe LLM çıktısı gözlemi |
| `ceviri_kokusu.tsv` | Elle; çeviribilim bulgularına dayalı | Türkçe çeviri derlemi çalışmaları (bkz. `arastirma.md`) |
| `metrik.py` uyarı eşikleri | Kısmen kalibre | Leipzig haber tabanı (aşağıda) + editör tahmini |
| `TUR_HEDEF` (tür bantları) | Editör tahmini | Faz 6'da güncellenecek |

## Leipzig tabanı (ölçüldü, 2026-09)

`tur_news_2024_30K-sentences.txt` (30.000 haber cümlesi, 413.581 kelime) üzerinde
`metrik.py` bileşenleri:

| Ölçü | Değer | metrik.py eşiği |
|---|---|---|
| Ortalama cümle | 13,8 kelime (P25 9, P50 13, P75 18, P90 23) | makale bandı 12-20 |
| Cümle uzunluğu CV | 0,47 (karışık cümleler; belge içi CV değil) | uyarı < 0,35 |
| Hece/kelime | 2,84 | — |
| Ateşman | 48,8 | makale 35-60 |
| "bir" | %1,73 | uyarı > %3,5 |
| "tarafından" | 1,77 / 1000 | uyarı > 2 / 1000 |
| Edilgen (yaklaşık) | 35,6 / 1000 | uyarı > 50 / 1000 |
| Açık zamir (ben/biz/siz/sen/onlar) | %0,18 | uyarı > %2 ve ≥ 3 |
| Bağlaçla başlayan cümle | %6,5 | uyarı > %25 |
| "Bu" ile başlayan cümle | %5,5 | uyarı > %25 |
| -maktadır yüklemi | %1,2 | uyarı > %15 |
| -dır yüklemi | %4,8 | uyarı > %40 |
| -dı yüklemi | %49,9 | — |

Haber dili resmi bir kayıttır; deneme ve reel için "bir", bağlaç ve zamir
oranları daha yüksek olabilir. Bu yüzden eşikler tabanın 2-4 katına konmuştur.
Yeniden hesaplamak: `tools/fetch_data.sh --hepsi` sonra
`python3 tools/derive_patterns.py` (yalnızca metrik kısmı için Leipzig yeter).

## Faz 6: LLM külliyatı ile kalibrasyon

Amaç, "hangi ifadeler Türkçede AI izidir" sorusunu tahminle değil sayımla
yanıtlamak.

### 1. Külliyat üret

```bash
python3 tools/generate_corpus.py --model claude-opus-5 --adet 300
python3 tools/generate_corpus.py --model <baska-model> --adet 300   # 3-4 farklı model
```

- 4 tür × ~75 metin, 120 nötr konu (Türkçe Vikipedi başlıkları; `--konular` ile
  değiştirilebilir).
- İstemler sade ("X hakkında blog yazısı yaz"): amaç modellerin **varsayılan**
  Türkçesini görmek. Üslup yönergesi verilmez.
- Çıktı `corpus/llm/<model>/<tür>/NNN.txt`, gitignore'da. Yalnızca türetilen
  listeler depoya girer.
- Başka sağlayıcı için `--istemler` ile `corpus/istemler.jsonl` alınır; aynı dosya
  düzeni korunursa sonraki adımlar çalışır.

### 2. İnsan külliyatı

- n-gram karşılaştırması için Leipzig cümleleri yeter (`corpus/leipzig/`).
- Belge düzeyi metrikler (ritim, paragraf) için paragraflı gerçek metin gerekir:
  Türkçe Vikipedi madde örnekleri (CC BY-SA), Leipzig web/wiki setleri ya da
  yazarın kendi `voice/onaylanan/` arşivi. `--insan-belgeler <klasör>` ile verilir.
  Bu külliyat da depoya girmez.

### 3. Türet

```bash
python3 tools/derive_patterns.py --llm corpus/llm --insan corpus/leipzig --insan-belgeler corpus/insan_belgeler
```

- `corpus/aday_kaliplar.tsv`: 1-3-gram log-odds (Monroe ve ark. 2008, Dirichlet
  önselli) z-skoruna göre. Pozitif z, LLM'de aşırı temsil.
- `corpus/esikler.json`: iki külliyatta metrik yüzdelikleri.

### 4. Elle gözden geçir

Aday listesi otomatik olarak `ai_kaliplari.tsv`'ye **girmez**. Her aday için:

1. Gerçekten kalıp mı, yoksa konu etkisi mi? ("Kapadokya" LLM'de fazla çıkar çünkü
   istemde var; "eşsiz güzellik" kalıptır.)
2. Türkçe konuşan insan bunu hiç demez mi, yoksa seyrek mi der? Seyrekse şiddet 1,
   demezse 2-3.
3. Düzeltme ipucu yazılabiliyor mu? Yazılamıyorsa listeye girmez.
4. Regex'i `kalip_tara.py` ile `tests/ornekler/dogal.md` üzerinde dene; yanlış
   pozitif veriyorsa daralt.

Kabul edilen adaylar `ai_kaliplari.tsv`'ye yorum satırıyla eklenir:
`# kaynak: derive_patterns 2026-xx, z=12.4`.

### 5. Eşikleri güncelle

`esikler.json` içinde insan P90'ı ile LLM P10'u arasında kalan değer, uyarı eşiği
olur. Örnek: insan CV P10 = 0,42, LLM CV P90 = 0,38 ise uyarı eşiği 0,40. Tür
bantları (`TUR_HEDEF`, `tur-profilleri/profiller/*.md`, `references/ritim.md`)
insan külliyatının tür başına P10-P90 aralığıyla değiştirilir. Üç yer birlikte
güncellenir; `tests/test_editor.py` bantların tutarlılığını denetlemez, elle
bakılır.

### 6. Doğrula

`tests/ornekler/` altındaki altın örnekler yeniden puanlanır: `ceviri_kokulu.md`
≥ 85, `dogal.md` ≤ 20 kalmalı. Bozulduysa liste fazla geniş.

## Bilinen sınırlar

- Ek soyma (`siklik.py`) ve edilgen sayımı (`metrik.py`) yaklaşıktır; `zeyrek`
  kuruluysa `--zeyrek` daha iyi sonuç verir ama Claude.ai ortamında yoktur.
- Leipzig cümleleri karışık sırada olduğundan belge ritmi (paragraf CV, giriş-sonuç)
  için taban vermez.
- Kalıp listesi Türkçe LLM çıktısının 2025-26 halini yansıtır; modeller değişince
  liste eskir. Yılda bir Faz 6 tekrarı önerilir.

---
name: geri-bildirim-hafizasi
description: Her düzeltme oturumundaki geri bildirimi kalıcı tercihe çevirir. Kullanıcının satır içi yorumlarını ("bu cümle çeviri gibi", "meslek adı verme, süreci anlat") reddedilen/yorum/onaylanan üçlüsü olarak voice/karsit/ dosyasına ekler (karsit_ekle.py), her yorumdan bir aday kural damıtıp voice/tercihler.md'ye yazar, 3+ kez görülen kuralı turkce-editor'ün başta okuduğu kontrol listesine terfi ettirir. Düzeltme oturumu bittiğinde, kullanıcı "bunu hatırla", "bir daha yapma", "tercihlerime ekle" dediğinde kullan. (Feedback memory, durable style preferences for Turkish writing.)
license: MIT
---

# Geri bildirim hafızası

Aynı düzeltmeyi iki kez yapmak israftır; üç kez yapmak kuraldır. Bu skill,
kullanıcının her yorumunu kayda geçirir, kurala çevirir, tekrar edeni yükseltir.

Üç dosyaya yazar (hepsi `voice/`, gitignore'da):

| Dosya | İçerik | Kim okur |
|---|---|---|
| `voice/karsit/karsit.jsonl` | reddedilen / yorum / son_hal üçlüleri | `kisisel-ses` (bağlama karşıt örnek) |
| `voice/tercihler.md` | Aday kurallar ve editör kontrol listesi | `turkce-editor` (başta), `turkce-taslak` |
| `voice/tercihler.tsv` | Kural regex'leri (isteğe bağlı) | `kalip_tara.py --ek` |

## Ne zaman çalışır

1. **Her düzeltme oturumunun sonunda.** `turkce-editor` düzeltmesi bitince ve
   kullanıcı son hâli onaylayınca — sorulmadan, oturumun son adımı olarak.
2. Kullanıcı bir cümleyi kendisi yeniden yazıp "böyle olacak" dediğinde.
3. Kullanıcı "bunu hatırla / bir daha yapma / tercihlerime ekle" dediğinde.

## İş akışı

### 1. Yorumları topla

Oturumdaki her sesle ilgili yorumu bul: kullanıcının açık cümleleri ("bu çeviri
gibi"), reddettiği öneriler, kendi yeniden yazdığı yerler. Yazım ve olgu düzeltmesi
alınmaz (`kisisel-ses/references/karsit-ornekler.md`).

Her yorum için üçlüyü kur:
- **reddedilen**: hangi cümle/paragraf (olduğu gibi)
- **yorum**: kullanıcının sözcükleriyle neden; editör önerisiyse "editör:" öneki
- **son_hal**: kabul edilen hâl

### 2. Kural damıt

Her üçlüden **tek cümlelik** bir kural adayı çıkar. Kural, o cümleye değil bir
sonraki metne söyler: "meslek adı verme, süreci adlandır", "'deneyim' yerine ne
yaşandığını yaz", "'yalnızca X değil Y' kurma". Kural yazılamıyorsa (tek seferlik
tercih) üçlü yine kaydedilir, kural boş kalır.

Kural mümkünse bir regex'le eşlenir (`kalip`), böylece `kalip_tara.py` bir sonraki
metinde otomatik yakalar. Regex yazılamayan kurallar (ton, yapı) yalnızca listede
kalır.

### 3. Kaydet

```bash
python3 scripts/karsit_ekle.py ekle --tur deneme \
  --reddedilen "Bu deneyim bana hayatın her alanında sabırlı olmayı öğretti." \
  --yorum "İngilizceden çevrilmiş gibi; 'deneyim' benim ağzımdan çıkmaz." \
  --son-hal "O yaz sabrı öğrendim; başka çare yoktu." \
  --kural "'deneyim' yerine ne yaşandığını yaz" \
  --kalip "\bdeneyim\w*\b"
```

Ya da bir JSON dosyasıyla (`--dosya ucluler.json`, liste). Betik:

- Üçlüyü `karsit.jsonl`'a ekler (id ve tarih verir).
- Kural varsa `tercihler.md`'de **benzer kural arar** (sözcük Jaccard ≥ 0,6). Varsa
  görülme sayısını artırır ve karşıt id'sini ekler; yoksa yeni aday açar
  (`references/tercih-formati.md`).
- Görülme 3'e ulaşınca kuralı **"Editör kontrol listesi"** başlığına taşır.
- `--kalip` verildiyse `tercihler.tsv`'yi yeniden üretir.

Teslimde kullanıcıya gösterilir: kaç üçlü eklendi, hangi kurallar yeni, hangileri
terfi etti. Kural metni kullanıcı onaylamadan **yumuşatılmaz, genişletilmez**;
kullanıcı "bir daha 'deneyim' yazma" dediyse kural odur.

### 4. Bakım

- `karsit_ekle.py liste` — kuralları görülme sayısıyla basar.
- `karsit_ekle.py terfi K7` — kullanıcı isterse 3 görülmeden önce terfi.
- `karsit_ekle.py birlestir K7 K12` — iki kural aynıysa birleştir; görülmeler toplanır.
- Onaylanan son hâl, kullanıcı isterse `voice/onaylanan/<tür>/` altına da girer;
  o zaman `kisisel-ses/scripts/ses_ozellikleri.py` yeniden çalıştırılır.

## Kural yazma ölçütleri

- Bir kural, bir örnek, bir karşı örnek. Örnek reddedilen cümle, karşı örnek son
  hâldir; ikisi de kullanıcının metninden.
- Kural olumsuz olabilir ("X yazma") ama yerine ne yazılacağını da söyler.
- Kural türe bağlıysa türü taşır: "[reel] soru cümlesi en fazla bir".
- Genel Türkçe kuralı (`turkce-editor/references/` içinde zaten olan) tekrar
  yazılmaz; kullanıcının kendi tercihi yazılır. "Tarafından kullanma" genel kuraldır;
  "'süreç' sözcüğünü hiç kullanma" kişiseldir.

## Kesin kurallar

- Kullanıcı yorumu uydurulmaz; oturumda söylenmediyse üçlü açılmaz.
- `voice/` yoksa önce `kisisel-ses` kurulumunu öner; `voice.example/` kopyalanmadan
  yazma.
- `tercihler.md` elle düzenlenebilir; betik yalnızca kendi bloklarına dokunur.

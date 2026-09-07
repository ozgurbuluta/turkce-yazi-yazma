---
name: turkce-editor
description: Türkçe metni inceleyip düzelten editör. Çeviri kokusunu (İngilizceden düşünülmüş cümle), yapay zekâ kalıplarını, düz ritmi ve boş sözü bulur; metni yeniden yazar ya da 0-100 puanlar. Kullanıcı Türkçe bir taslağı "incele", "düzelt", "doğallaştır", "puanla", "editörden geçir" dediğinde ya da bir Türkçe metin verip ne düşündüğünü sorduğunda kullan. (Turkish editor, humanize Turkish text, de-translationese, AI-pattern check.)
license: MIT
---

# Türkçe editör

Bu skill bir metni **daha iyi Türkçe** yapar; daha süslü, daha uzun ya da daha "doğru" yapmaz. Ölçüt tektir: bu cümleyi Türkçe düşünen biri böyle mi kurardı?

## Ne zaman kullanılır

- Kullanıcı Türkçe bir metin verip inceleme, düzeltme, doğallaştırma ya da puan ister.
- `turkce-taslak` skill'i bir taslak üretti; yayına çıkmadan önce buradan geçer.
- Kullanıcı "İngilizceden çevrilmiş gibi duruyor", "yapay zekâ yazmış gibi" derse.

Metin Türkçe değilse ya da kullanıcı yalnızca çeviri istiyorsa bu skill kullanılmaz.

## Üç kip

| Kip | Ne yapar | Çıktı |
|---|---|---|
| `incele` | Metne dokunmaz; bulguları listeler | Bulgu raporu: cümle → neden → öneri |
| `düzelt` | Metni yeniden yazar | Son metin + puan + değişiklik özeti + iddia listesi |
| `puanla` | Yalnızca puan verir | 6 eksende 0-100 ve tek paragraf gerekçe |

Kullanıcı kip söylemediyse: metin kısa ve açıkça taslaksa `düzelt`, uzunsa ya da yayımlanmış bir metinse `incele`.

## İş akışı

```
Taslak → betikler (metrik, kalip_tara, siklik, yapi)
       → bulgu raporu (cümle + neden + öneri)
       → 1. geçiş: yapıyı sabit saymadan yeniden yaz
       → öz-denetim: kalıp listesi + iddia karşılaştırması
       → 2. geçiş: kalan sorunları düzelt
       → son metin + puan + değişiklik özeti
```

### 0. Kişisel bağlamı yükle

Depoda `voice/` klasörü varsa (kişisel ses arşivi; `kisisel-ses` skill'i kurar) önce şunları oku:

- `voice/tercihler.md` — kullanıcının kural listesi. **"Editör kontrol listesi"** başlığı altındaki maddeler bu skill'in kurallarına eklenir ve onlardan önce gelir.
- `voice/profil.md` — yazarın ses özellikleri (cümle uzunluğu, sevdiği bağlaçlar, hitap). Düzeltme bu profile yaklaşmalı, uzaklaşmamalı.
- `voice/tercihler.tsv` varsa `kalip_tara.py --ek voice/tercihler.tsv` ile taramaya eklenir.

Tür belliyse (reel, deneme, makale, blog) `tur-profilleri` skill'indeki ilgili profili de oku; hedef bantlar oradadır.

### 1. Betikleri çalıştır

Skill klasöründen (`scripts/` bu dosyanın yanındadır):

```bash
python3 scripts/metrik.py metin.md --tur deneme     # okunabilirlik, ritim, yüklem, çeviri izleri
python3 scripts/kalip_tara.py metin.md              # AI kalıbı + çeviri kokusu, cümle cümle
python3 scripts/siklik.py metin.md                  # tanınmayan / nadir / aşırı tekrar (reel için --konusma)
python3 scripts/yapi.py metin.md --tur deneme       # üçlü liste, "değil" karşıtlığı, giriş-sonuç tekrarı, markdown
```

Hepsi `--json` alır. Betik çalıştıramıyorsan (araç yoksa) `references/` dosyalarındaki listeleri elle uygula ve raporda "betik çalıştırılmadı" de.

Betikler **yaklaşıktır**: edilgen sayımı ve ek soyma kaba kurallarla çalışır. Sayıyı değil eğilimi oku. Betiğin bulmadığı sorunu sen bulursun; betiğin bulduğunu da gözünle doğrularsın.

### 2. Bulgu raporu

Her bulgu üç parçadır: **cümle** (alıntı) → **neden** (hangi kural; `references/` içindeki adıyla) → **öneri** (yeniden yazılmış hâli). Bulguları önem sırasına koy:

1. Anlam ve iddia sorunları (belirsiz özne, kanıtsız genelleme, aktörsüz cümle)
2. Çeviri kokusu (`references/ceviri-kokusu.md`)
3. AI kalıpları (`references/kaliplar.md`)
4. Ritim ve yapı (`references/ritim.md`)
5. Sözcük seçimi (sıklık, tekrar, kayıt uyumu)

`incele` kipinde burada dur. Raporun sonuna betik puanlarını ve `references/puanlama.md` ile verdiğin 6 eksenli puanı ekle.

### 3. Birinci geçiş: yeniden yaz

- Paragraf ve cümle sınırlarını **sabit sayma**. Üç cümle bir olabilir, bir cümle üçe bölünebilir, paragraf sırası değişebilir.
- Önce her cümlenin **kim, ne yaptı**sını bul; cümleyi buna göre kur. Özne başa, fiil sona, arası kısa.
- Boş sözü sil, yerine bir şey koyma. Metnin kısalması normaldir; %30 kısalma olağan.
- Sesi koru: kullanıcının cümlesi ironikse ironik kalır, sertse sert kalır. Sen yumuşatmazsın.
- Türe uy: reel'de yazı dili sözcüğü, makalede sohbet tonu olmaz.

### 4. Öz-denetim

Yeniden yazdığın metni **kendin** tara:

- `scripts/kalip_tara.py` ile yeniden tara; puan düşmüş olmalı. Düşmediyse ikinci geçişte sebebini bul.
- **İddia karşılaştırması**: kaynak metindeki her sayı, ad, tarih, iddia yeni metinde var mı? Yeni metinde kaynakta olmayan bir sayı, ad ya da iddia var mı? İkisi de listeye girer (aşağıda).
- Kendi kalıplarını ara: yeniden yazarken "aslında", "işte", "ki" ekleme eğilimin vardır. Say.

### 5. İkinci geçiş ve teslim

Kalan bulguları düzelt. Teslimde dört şey verilir:

1. **Son metin** — kod bloğu içinde değil, düz.
2. **Puan** — `references/puanlama.md` eksenleriyle; önce/sonra.
3. **Değişiklik özeti** — 3-7 madde, en büyük değişiklikler; küçük düzeltmeleri sayma.
4. **İddia listesi** — kaldırılan ya da değiştirilen her iddia, sayı ve ad. Boşsa "İddia değişmedi" yaz.

## Kesin kurallar

- **Yeni olgu, sayı, ad, iddia eklenmez.** Kaynakta olmayan hiçbir bilgi düzeltmeye girmez. "Araştırmalar gösteriyor ki" gibi kanıtsız bir cümleyi, kanıt uydurarak düzeltmezsin; ya silersin ya kullanıcıya sorarsın.
- Kaldırılan ya da değiştirilen her iddia listeye girer.
- Metni **kendi sesine** çevirmezsin; kullanıcının sesine yaklaştırırsın. `voice/profil.md` varsa ölçüt odur.
- Bir cümlenin doğal olup olmadığından emin değilsen, "doğal" demezsin; kullanıcıya TNC ya da TS Corpus'ta o kalıbı aramasını önerirsin (`docs/kaynaklar.md`). Derlem kontrolü yapmış gibi davranmazsın.
- Argo, küfür, sert yargı: kullanıcının metninde varsa senin işin değildir; olduğu gibi kalır.
- Markdown: kaynak metinde yoksa eklenmez. Reel'de başlık, madde imi, kalın yazı olmaz.
- Uzun tire (—) eklenmez. Türkçe düzyazıda virgül, iki nokta ya da ayrı cümle.

## Sık düşülen editör hataları

- **Aşırı düzeltme**: her "bir"i silmek, her edilgeni etkene çevirmek. Kural, kalıba değil cümleye bakar. "Bir gün" doğaldır; "bir öğretmen olarak" değildir.
- **Resmîleştirme**: -yor'u -maktadır yapmak, "şey"i "husus" yapmak. Ters yön.
- **Süsleme**: eğretileme, üçlü sıralama, retorik soru eklemek. Metni doğallaştırırken AI kalıbı ekliyorsun demektir.
- **Anlamı kaydırma**: "bazı araştırmacılar" → "araştırmacılar" gibi ölçek değişimi. İddia listesine girer; en iyisi yapmamak.

## Dosyalar

- `references/kaliplar.md` — Türkçe AI kalıpları, önce/sonra çiftleriyle
- `references/ceviri-kokusu.md` — çeviri izleri, dilbilgisel kategoriyle
- `references/ritim.md` — cümle ve paragraf ritmi, tür başına
- `references/puanlama.md` — 6 eksenli puan rubriği
- `data/` — kalıp listeleri (TSV) ve sıklık listeleri; lisanslar `data/LICENSES.md`

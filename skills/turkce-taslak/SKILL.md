---
name: turkce-taslak
description: Türkçe taslak yazar. İki giriş yolu vardır — kullanıcının kendi Türkçe notlarından ya da İngilizce bir kaynaktan kopyalamadan. Kaynaktan yazarken önce "bilgi kartı" doldurulur, kaynak metin bağlamdan çıkarılır, yalnızca karttan yazılır; kaynak_hizala.py aynalama ve uydurma denetimi yapar. Kullanıcı "şu notlardan reel/deneme/makale/blog yaz", "bu İngilizce yazıdan Türkçe bir yazı çıkar", "taslak hazırla" dediğinde kullan. (Turkish drafting, write Turkish from English source without translating.)
license: MIT
---

# Türkçe taslak

Bu skill yazar; düzeltmez. Ürettiği taslak yayına çıkmadan önce `turkce-editor`
skill'inden geçer. Amaç, İngilizceden çevrilmiş gibi durmayan, kullanıcının sesiyle
ve türün kurallarıyla yazılmış bir ilk sürüm.

## İki giriş yolu

| Yol | Girdi | Yöntem |
|---|---|---|
| **Notlardan** | Kullanıcının Türkçe notları, madde listesi, sesli düşünceleri | Notları önce sıraya koy, sonra yaz |
| **Kaynaktan** | İngilizce (ya da Türkçe) bir makale, haber, rapor | Bilgi kartı → kaynağı kapat → karttan yaz |

Her iki yolda da yazmadan önce iki şey yüklenir:

1. **Tür profili**: `tur-profilleri` skill'inde `profiller/<tür>.md`. Uzunluk, cümle bandı, hitap, açılış-kapanış hareketleri, yasaklar oradadır. Tür belli değilse kullanıcıya sor; sormadan varsayma.
2. **Ses**: `voice/` varsa `kisisel-ses` skill'i ile profil + 2-3 ilgili onaylanmış metin + karşıt örnekler alınır (`scripts/ornek_sec.py`). `voice/` yoksa nötr ama Türkçe düşünülmüş bir sesle yazılır; bunu kullanıcıya söyle.

## Yol 1: Notlardan

1. Notları oku. Her notu tek cümleyle yeniden söyle; anlamadığın notu sor.
2. Türün açılış hareketlerinden birini seç (profilde listeli). Notların içindeki en somut, en şaşırtıcı şey açılıştır.
3. Notları okurun sırasına koy, yazarın sırasına değil: önce okurun bildiği, sonra yeni olan.
4. Yaz. Notlarda olmayan hiçbir olgu, sayı, ad ekleme. Genel bilgi gerekiyorsa cümleyi `[?]` ile işaretle ve teslimde listele.
5. `turkce-editor` betiklerini çalıştır (`metrik.py --tur`, `kalip_tara.py`, `yapi.py --tur`); uyarıları düzelt.

## Yol 2: Kaynaktan (kopyalamadan)

Kaynağı okuyup "Türkçesini yazmak" çeviridir; cümle sırası, paragraf sırası,
İngilizce sözdizimi taslağa sızar. Bunu engellemenin tek yolu kaynağı bağlamdan
çıkarmaktır.

### Adım 1: Bilgi kartı

Kaynağı bir kez oku. `references/bilgi-karti.md` şablonunu doldur:

```
## Bilgi kartı
Ne oldu:            (bir cümle, kendi sözcüklerinle)
Sayılar / kanıt:    (her sayı kaynağıyla: kim ölçtü, ne zaman)
Kaynağın iddiası:   (kaynak tam olarak ne diyor; abartmadan)
Senin görüşün:      (kullanıcıya sor; boşsa "yok" yaz, uydurma)
Türkiye'deki okur için anlamı: (bağlantı; yoksa "doğrudan yok")
Belirsiz olan:      (kaynağın söylemediği, çelişkili ya da kontrol edilemeyen)
Alıntı adayı:       (en fazla bir cümle, tırnak içinde, kaynaktan)
```

Kartı kullanıcıya göster. "Senin görüşün" satırı boşsa sor: bu satır yazının
omurgasıdır; boş kalırsa yazı kaynağın özeti olur.

### Adım 2: Kaynağı kapat

Kartı yazdıktan sonra kaynak metne bir daha bakma. Yazma sırasında bağlamda kaynak
varsa (kullanıcı yapıştırdıysa) açıkça şunu yaz: "Bundan sonra yalnızca karttan
yazıyorum; kaynağa dönmeyeceğim." Bu kural, çeviri sızmasının tek ilacıdır.

Doğrulama gerekirse (bir sayı, bir ad) kart yeterli olmalı. Yetmiyorsa kartı
eksik doldurmuşsundur: karta dön, düzelt, yazmaya kartla devam et.

### Adım 3: Karttan yaz

- Açılış: kartın "Senin görüşün" ya da "Türkiye'deki okur için anlamı" satırından.
  Kaynağın giriş cümlesinden değil.
- Sıra: Türk okur için mantıklı olan. Kaynak "haber → bağlam → tepki → veri →
  sonuç" gidiyorsa sen "görüş → veri → tepki" gidebilirsin.
- Kaynağın her paragrafına karşılık paragraf yazma. Kartta olmayan şey yazıya girmez;
  kartta olan her şey de girmek zorunda değil.
- Sayıları kartta yazıldığı gibi, kaynağıyla ver: "Gallup'un Mart 2024'te 12.000
  kişiyle yaptığı ankete göre". Kaynaksız sayı yazma.
- Alıntı en fazla bir tane; Türkçesini kendin kur, tırnakla.

### Adım 4: Hizalama denetimi

```bash
python3 scripts/kaynak_hizala.py kaynak.md taslak.md
```

Betik üç şey söyler:

- **Aynalama**: taslak paragrafları kaynağın sırasını izliyorsa (tekdüzelik ≥ 0,8,
  paragraf sayısı yakın) taslak çeviridir. Karttan yeniden yaz; sırayı değiştir.
- **Uydurma**: taslakta olup kaynakta olmayan sayı ve adlar. Kendi bilgin olarak
  eklediysen kaynağını yaz; yoksa sil. Ad denetimi yaklaşıktır (ilk 6 harf); listeyi
  gözle doğrula.
- **Kayıp**: kaynakta olup taslakta olmayanlar. Bilgi amaçlı; hepsi girmek zorunda
  değil.

Ardından `turkce-editor` betikleri (`metrik.py --tur`, `kalip_tara.py`, `yapi.py --tur`).

## Teslim

1. Taslak (düz metin; tür markdown gerektirmiyorsa markdown yok).
2. Bilgi kartı (kaynaktan yazıldıysa).
3. `[?]` işaretli cümleler: kullanıcının doğrulaması gereken bilgi.
4. Betik özetleri: hizalama sonucu, kalıp puanı, metrik uyarıları.
5. "Editörden geçmedi" notu: taslak, `turkce-editor` ile ikinci geçişi bekler.

## Kesin kurallar

- Kaynakta ve kartta olmayan olgu, sayı, ad, alıntı eklenmez.
- Kaynağın cümlesi Türkçeye çevrilip kullanılmaz; yalnızca tek alıntı, tırnakla.
- "Senin görüşün" uydurulmaz; kullanıcıdan alınır ya da boş bırakılır.
- Tür profili yüklenmeden yazılmaz.
- Taslak hiçbir zaman "son metin" olarak sunulmaz.

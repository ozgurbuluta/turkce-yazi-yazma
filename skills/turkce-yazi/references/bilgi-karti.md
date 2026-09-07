# Bilgi kartı

Kaynaktan yazarken kaynağın yerine geçen tek belge. Kart doldurulduktan sonra kaynak
kapanır; yazı yalnızca karttan çıkar. Kart, yazının değil bilginin özetidir: cümle
kurma, madde yaz.

## Şablon

```
## Bilgi kartı — <kaynak adı, tarih, bağlantı>

Ne oldu:
  <bir cümle, kendi sözcüklerinle; kaynağın ilk cümlesini çevirme>

Sayılar / kanıt:
  - <sayı> — <kim ölçtü> — <ne zaman> — <ne örneklem>
  - ...

Kaynağın iddiası:
  <kaynak tam olarak ne diyor; "kanıtladı" mı "öne sürdü" mü, ayır>

Senin görüşün:
  <kullanıcının görüşü; sor. Boşsa "yok" yaz>

Türkiye'deki okur için anlamı:
  <bağlantı: benzer durum, fark, neden umursasın; yoksa "doğrudan yok">

Belirsiz olan:
  - <kaynağın söylemediği>
  - <çelişen ya da kontrol edilemeyen>

Alıntı adayı:
  "<en fazla bir cümle, kaynak dilinde>" — <kim söyledi>
```

## Doldurma kuralları

- **Ne oldu** kaynağın giriş cümlesi değildir. Kaynak "X is here to stay, according
  to a new survey" diyorsa sen "hibrit çalışma ABD'de çoğunluk oldu" yazarsın.
- **Sayılar** kaynak bilgisiyle gelir. Kaynaksız sayı karta girmez; girmeyen sayı
  yazıya girmez.
- **Kaynağın iddiası** ile **senin görüşün** karışmaz. Kaynak "verimlilik aynı"
  diyorsa, "uzaktan çalışma daha iyi" senin görüşündür; öyle yazılır.
- **Belirsiz olan** satırı boş kalmaz. Her kaynak bir şeyi söylemez: örneklem,
  finansman, tarih, karşı görüş. Bulunan belirsizlik yazıda ya söylenir ya
  yazıyı sınırlar ("ABD verisi; Türkiye için bilinmiyor").
- **Alıntı** bir tane. Kaynağın en iyi cümlesi değil, senin yazında işe yarayacak
  cümle. Türkçesi kart doldurulurken değil, yazarken kurulur.

## Örnek

Kaynak: Gallup uzaktan çalışma anketi haberi (tests/ornekler/kaynak_en.md)

```
Ne oldu:
  ABD'de uzaktan çalışabilen işlerin çoğu hibrit oldu; bazı büyük şirketler
  buna direniyor.

Sayılar / kanıt:
  - %58 hibrit — Gallup — Mart 2024 — 12.000 çalışan, ABD
  - %36 ofis boşluğu — San Francisco — 2024 1. çeyrek — rekor
  - %52 ofis katılımı — Kastle Systems kart verisi — en büyük 10 metropol — pandemi öncesine göre
  - hibrit çalışan %35 daha az istifa, verimlilik aynı — Bloom (Stanford) — Trip.com, 1.600 kişi, 2 yıl

Kaynağın iddiası:
  Hibrit kalıcı; verimlilik verisi karışık ama Bloom çalışması aleyhte değil.
  Amazon ve JPMorgan 5 gün ofis istiyor.

Senin görüşün:
  (kullanıcıdan) Ofise dönüş çağrısı verimlilikle değil kontrolle ilgili.

Türkiye'deki okur için anlamı:
  Plaza şirketlerinde aynı tartışma; Türkiye verisi yok.

Belirsiz olan:
  - Gallup örneklemi hangi sektörler? Belirsiz.
  - "Verimlilik karışık" diyen diğer çalışmalar hangileri? Kaynak söylemiyor.
  - Trip.com tek şirket; genellenir mi?

Alıntı adayı:
  "does not work for younger people or for those who want to hustle" — Jamie Dimon, JPMorgan CEO
```

Bu karttan yazılan taslak örneği: `tests/ornekler/taslak_serbest.md`. Aynı kaynağın
çevirisi (yapılmaması gereken): `tests/ornekler/taslak_ayna.md`.

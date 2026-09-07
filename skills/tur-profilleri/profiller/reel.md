# Reel / kısa video metni

## Amaç

İzleyici kaydırırken durur, 20-60 saniye dinler, bir şey öğrenir ya da bir şey
hisseder, belki paylaşır. Metin **sesli okunmak** için yazılır; göz için değil.
Kağıtta iyi duran cümle ağızda takılıyorsa yanlıştır.

## Ölçüler

| Ölçü | Hedef |
|---|---|
| Süre | 20-60 sn (dakikada ~150 kelime) |
| Kelime | 60-220 |
| Ortalama cümle | 5-12 kelime |
| En uzun cümle | 18 kelime; onu da bir nefeste oku, olmuyorsa böl |
| Ritim (CV) | ≥ 0,45; iki uzun cümle art arda gelmez |
| Ateşman | 70-95 (kolay / çok kolay) |
| Paragraf | Nefes başına bir satır; 3-8 satır |
| Soru | En fazla 2; ikisi de gerçek soru, retorik değil |

## Hitap ve kişi

- Varsayılan **sen**. "Siz" yalnızca kullanıcı isterse ya da hedef kitle açıkça resmi ise.
- "Ben" serbest; reel yazarın sesidir.
- "Biz" dikkatli: "hepimiz" genellemesi izleyiciyi dışarıda bırakır.
- Konuşma dili: "-yor", "-dı", ad cümlesi. "-dır", "-maktadır", "-mıştır" yok.
- `siklik.py --konusma` ile sözcük kaydını kontrol et: "araçlar", "kapsamlı",
  "olanak" gibi yazı dili sözcükleri konuşmada yabancıdır.

## Açılış hareketleri (ilk 3 saniye)

İlk cümle kaydırmayı durdurur. Seçenekler:

1. **Somut sahne**: "Dün gece üçte telefonum çaldı."
2. **Tersine iddia**: "Sabah rutini diye bir şey yok."
3. **Sayı + kişi**: "Üç ayda on iki kilo verdim, spor yapmadan."
4. **İzleyiciye doğrudan durum**: "Şu an kaydırıyorsun, biliyorum."
5. **Yarım kalan cümle**: "Babam bana tek bir şey öğretti, o da..."
6. **İtiraf**: "Bunu kimseye söylemedim."

Yasak açılışlar: "Merhaba", "Bugün sizlerle ...", "Biliyor muydunuz?", "Hepimiz
bazen...", "Günümüzde...", kanal tanıtımı.

## Gövde

- **Tek fikir.** İkinci fikir varsa ikinci reel.
- Sıra: açılış → bir somut örnek ya da olay → dönüş noktası ("ama", "sonra",
  "meğer") → ne anladım.
- Her cümle bir şey ekler. Öncekini tekrar eden cümle silinir.
- Geçiş sözcüğü yok. Cümleler yan yana durur; bağ, sıradan çıkar.
- Kanıt: kendi deneyimi, tek bir sayı, tek bir ad. Liste yok.
- Kısa cümle vuruştur: dönüş noktasında iki üç kelimelik bir cümle.

## Kapanış hareketleri (son 3 saniye)

1. **Tek cümlelik ders, sıfat sız**: "Kutuyu al. Ne yapacağını sonra öğrenirsin."
2. **Açılışa dönüş**: ilk cümledeki görüntüye geri bak, anlamı değişmiş olsun.
3. **Tek gerçek soru**: "Sen olsan alır mıydın?" (yorum çağrısı yok; soru yeter)
4. **Kesik bitiş**: son cümle kısa, sonrası sessizlik.

Yasak kapanışlar: "Beğenmeyi unutma", "Yorumlarda paylaş", "Takip et", "Umarım
faydalı olmuştur", özet cümlesi, "Sonuç olarak".

## Yasaklar

- Başlık, madde imi, kalın yazı, emoji (metin sesli okunacak).
- "-dır / -maktadır / -mıştır" yüklemleri.
- Üçlü liste ("hızlı, ucuz ve kolay").
- "Yalnızca X değil aynı zamanda Y."
- Retorik soru zinciri ("Peki neden? Çünkü...").
- Yazı dili sözcükleri: husus, kapsamlı, olanak, gerçekleştirmek, sunmak, süreç.
- 18 kelimeden uzun cümle.
- İkinci fikir.

## Kontrol listesi

- [ ] Sesli okudum (ya da okur gibi düşündüm); takılan yer yok
- [ ] İlk cümle bir sahne, iddia, sayı ya da itiraf; selam değil
- [ ] Tek fikir; ikinci fikir varsa ayrı reel'e not düştüm
- [ ] 60-220 kelime; en uzun cümle ≤ 18
- [ ] Hiç -dır/-maktadır yok
- [ ] Hiç başlık/madde/emoji yok
- [ ] Soru sayısı ≤ 2, hiçbiri retorik değil
- [ ] Kapanış özet değil; ders, dönüş, soru ya da kesik
- [ ] `metrik.py --tur reel`, `yapi.py --tur reel`, `siklik.py --konusma` temiz

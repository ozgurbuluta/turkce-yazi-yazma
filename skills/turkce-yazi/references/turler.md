# Tür profilleri

Reel, deneme, makale, blog. Her profil aynı başlıkları taşır: amaç, ölçüler, hitap, açılış, gövde, kapanış, yasaklar, kontrol listesi. Ölçüler yol göstericidir; kullanıcının kendi profili (voice/profil.md) tür profiliyle çelişirse kullanıcı kazanır, çelişki söylenir.

Tür ipuçları: "video, Instagram, TikTok" → reel; "köşe, kişisel, anı" → deneme; "rapor, analiz, kaynaklı" → makale; "site, Medium, bülten" → blog. Tür belli değilse sor.


---

## Reel / kısa video metni

### Amaç

İzleyici kaydırırken durur, 20-60 saniye dinler, bir şey öğrenir ya da bir şey
hisseder, belki paylaşır. Metin **sesli okunmak** için yazılır; göz için değil.
Kağıtta iyi duran cümle ağızda takılıyorsa yanlıştır.

### Ölçüler

| Ölçü | Hedef |
|---|---|
| Süre | 20-60 sn (dakikada ~150 kelime) |
| Kelime | 60-220 |
| Ortalama cümle | 5-12 kelime |
| En uzun cümle | 18 kelime; onu da bir nefeste oku, olmuyorsa böl |
| Ritim | İki uzun cümle art arda gelmez; üç kesik cümle de art arda gelmez, konuşur gibi bağlanır |
| Ateşman | 70-95 (kolay / çok kolay) |
| Paragraf | Nefes başına bir satır; 3-8 satır |
| Soru | En fazla 2; ikisi de gerçek soru, retorik değil |

### Hitap ve kişi

- Varsayılan **sen**. "Siz" yalnızca kullanıcı isterse ya da hedef kitle açıkça resmi ise.
- "Ben" serbest; reel yazarın sesidir.
- "Biz" dikkatli: "hepimiz" genellemesi izleyiciyi dışarıda bırakır.
- Konuşma dili: "-yor", "-dı", ad cümlesi. "-dır", "-maktadır", "-mıştır" yok.
- `siklik.py --konusma` ile sözcük kaydını kontrol et: "araçlar", "kapsamlı",
  "olanak" gibi yazı dili sözcükleri konuşmada yabancıdır.

### Açılış hareketleri (ilk 3 saniye)

İlk cümle kaydırmayı durdurur. Seçenekler:

1. **Somut sahne**: "Dün gece üçte telefonum çaldı."
2. **Tersine iddia**: "Sabah rutini diye bir şey yok."
3. **Sayı + kişi**: "Üç ayda on iki kilo verdim, spor yapmadan."
4. **İzleyiciye doğrudan durum**: "Şu an kaydırıyorsun, biliyorum."
5. **Yarım kalan cümle**: "Babam bana tek bir şey öğretti, o da..."
6. **İtiraf**: "Bunu kimseye söylemedim."

Yasak açılışlar: "Merhaba", "Bugün sizlerle ...", "Biliyor muydunuz?", "Hepimiz
bazen...", "Günümüzde...", kanal tanıtımı.

### Gövde

- **Tek fikir.** İkinci fikir varsa ikinci reel.
- Sıra: açılış → bir somut örnek ya da olay → dönüş noktası ("ama", "sonra",
  "meğer") → ne anladım.
- Her cümle bir şey ekler. Öncekini tekrar eden cümle silinir.
- Geçiş sözcüğü yok. Cümleler yan yana durur; bağ, sıradan çıkar.
- Kanıt: kendi deneyimi, tek bir sayı, tek bir ad. Liste yok.
- Kısa cümle vuruştur: dönüş noktasında iki üç kelimelik bir cümle.

### Kapanış hareketleri (son 3 saniye)

1. **Tek cümlelik ders, sıfat sız**: "Kutuyu al. Ne yapacağını sonra öğrenirsin."
2. **Açılışa dönüş**: ilk cümledeki görüntüye geri bak, anlamı değişmiş olsun.
3. **Tek gerçek soru**: "Sen olsan alır mıydın?" (yorum çağrısı yok; soru yeter)
4. **Kesik bitiş**: son cümle kısa, sonrası sessizlik.

Yasak kapanışlar: "Beğenmeyi unutma", "Yorumlarda paylaş", "Takip et", "Umarım
faydalı olmuştur", özet cümlesi, "Sonuç olarak".

### Yasaklar

- Başlık, madde imi, kalın yazı, emoji (metin sesli okunacak).
- "-dır / -maktadır / -mıştır" yüklemleri.
- Üçlü liste ("hızlı, ucuz ve kolay").
- "Yalnızca X değil aynı zamanda Y."
- Retorik soru zinciri ("Peki neden? Çünkü...").
- Yazı dili sözcükleri: husus, kapsamlı, olanak, gerçekleştirmek, sunmak, süreç.
- 18 kelimeden uzun cümle.
- İkinci fikir.

### Kontrol listesi

- [ ] Sesli okudum (ya da okur gibi düşündüm); takılan yer yok
- [ ] İlk cümle bir sahne, iddia, sayı ya da itiraf; selam değil
- [ ] Tek fikir; ikinci fikir varsa ayrı reel'e not düştüm
- [ ] 60-220 kelime; en uzun cümle ≤ 18
- [ ] Hiç -dır/-maktadır yok
- [ ] Hiç başlık/madde/emoji yok
- [ ] Soru sayısı ≤ 2, hiçbiri retorik değil
- [ ] Kapanış özet değil; ders, dönüş, soru ya da kesik
- [ ] `metrik.py --tur reel`, `yapi.py --tur reel`, `siklik.py --konusma` temiz

---

## Deneme

### Amaç

Yazar bir deneyimden, bir gözlemden yola çıkar; okuru bir soruya götürür, cevabı
kesinleştirmez. Okur yazarı tanır, kendi hayatını yeniden düşünür. Deneme kanıtla
değil, dürüstlükle ikna eder.

### Ölçüler

| Ölçü | Hedef |
|---|---|
| Kelime | 500-1500 |
| Ortalama cümle | 10-18 kelime |
| Ritim | Cümleler ulaçla bağlı, arada seyrek vuruş; ne metronom ne parçalı |
| Ateşman | 45-75 |
| Paragraf | 2-8 cümle; en az bir tek cümlelik paragraf |
| Yüklem | Hiçbir ek %40'ı geçmez; -maktadır ≤ %5 |

### Hitap ve kişi

- **Ben** omurgadır. Deneme, yazarın "ben"i olmadan makaleye döner.
- Okura hitap seyrek: "sen" ya da "siz", metinde en çok iki üç kez, o da bir soruyla.
- "Biz" yalnızca somut bir topluluk için ("biz kardeşler", "o sınıftakiler");
  "hepimiz" genellemesi yasak.
- Zaman: anlatı -dı, düşünce -yor ve geniş zaman. İkisi arasında geçiş serbest ama
  paragraf içinde tutarlı.

### Açılış hareketleri

1. **Sahne**: bir yer, bir an, bir nesne. "Babam ilk bilgisayarı eve 1994'te getirdi."
2. **Küçük gözlem**: herkesin gördüğü ama söylemediği şey.
3. **Kişisel itiraf**: "Oğluma tablet almak istemiyorum."
4. **Yanlış çıkan inanç**: "Yıllarca X sandım."
5. **Bir cümlelik anı + kesme**: "Kutusu buzdolabından büyüktü."

Yasak açılışlar: tanım ("X, ... anlamına gelir"), "Günümüzde", "İnsanlık tarihi
boyunca", soru ("Hiç düşündünüz mü?"), sözlük/alıntı ile başlamak.

### Gövde

- Hareket: **somut → soyut → somut**. Bir olay, o olaydan çıkan düşünce, düşünceyi
  sınayan ikinci olay.
- Her paragraf bir adım atar. Bir önceki paragrafı özetleyen cümle yoktur.
- Düşünce cümleleri kısa, olay cümleleri uzun olabilir; tersi de. Ritim ikisinin
  değişiminden çıkar. Art arda kısa cümle dizisi denemeyi reklam metnine çevirir;
  ilişkili cümleler "-ip, -ince, -diği için" ile bağlanır (`references/ritim.md`).
- Kanıt: olay, ayrıntı, diyalog. İstatistik olabilir ama bir tane; kaynak adı
  metnin içinde, dipnot yok.
- Çelişki serbest: yazar fikrini değiştirebilir, "bilmiyorum" diyebilir. Deneme
  bunun için var.
- Geçiş sözcükleri yok denecek kadar az. "Ama", "sonra", "şimdi" yeter.

### Kapanış hareketleri

1. **Açılışa dönüş, anlam değişmiş**: ilk sahne son sahnede başka görünür.
2. **Açık soru**: cevap yok, ama soru artık daha keskin.
3. **Küçük eylem**: "Tableti aldım." / "Kutuyu hala saklıyorum."
4. **Kabul**: "Bilmiyorum; babam da bilmiyordu."

Yasak kapanışlar: özet, ders ("Bu bize gösteriyor ki"), genelleme ("Hepimiz..."),
çağrı ("Siz de deneyin"), alıntı.

### Yasaklar

- Başlık altı başlıklar (h2/h3); deneme akar.
- Madde listesi.
- "Sonuç olarak / özetle" ve her tür özet paragrafı.
- Tanım cümleleriyle başlamak.
- Kaynak dipnotu; kaynak varsa cümlenin içinde.
- -maktadır / -mıştır dizisi.
- Eğretileme yığını; bir eğretileme metne yeter.
- "Yolculuk", "dönüşüm", "farkındalık".

### Kontrol listesi

- [ ] "Ben" var; olay var; okur beni görüyor
- [ ] Açılış bir sahne, gözlem ya da itiraf; tanım değil
- [ ] Kısa cümleler bir şey vuruyor; art arda kısa cümle dizisi yok
- [ ] Hiçbir paragraf öncekini özetlemiyor
- [ ] Son paragraf yeni bir şey söylüyor ya da kesiyor; özet değil
- [ ] Kaynak varsa cümle içinde, bir tane
- [ ] Yüksek sesle okununca nefes kesilmiyor ve yetmezlik yok; -maktadır yok
- [ ] `metrik.py --tur deneme`, `kalip_tara.py`, `yapi.py --tur deneme` temiz

---

## Makale

### Amaç

Okur bir konuda ne olduğunu, neden olduğunu ve ne anlama geldiğini öğrenir. Her
iddianın kaynağı vardır; yazarın görüşü varsa görüş olarak işaretlidir. Makale
inandırmaz, gösterir.

### Ölçüler

| Ölçü | Hedef |
|---|---|
| Kelime | 700-2500 |
| Ortalama cümle | 12-20 kelime |
| Ritim (CV) | ≥ 0,45 |
| Ateşman | 35-60 (orta / zor); 30 altı okunmaz |
| Paragraf | 3-7 cümle |
| Yüklem | -dır + -maktadır toplamı ≤ %50; -maktadır tek başına ≤ %25 |
| Kaynak | Her sayı ve her "X'e göre" için ad + yıl; dipnot ya da bağlantı |

Leipzig haber külliyatı tabanı: ortalama cümle 13,8, Ateşman 48,8, -maktadır %1.
Haber dilinden bile daha resmi yazıyorsan sebebi olmalı.

### Hitap ve kişi

- Varsayılan **üçüncü kişi**. "Biz" kurumsal makalede ("biz Türkiye'deki
  okurlar" değil, "biz bu çalışmada" anlamında) olabilir.
- "Ben" yalnızca görüş paragrafında ve açıkça: "Bence", "Bana göre".
- Okura hitap yok; "siz" yok.
- Zaman: geniş zaman ve -dı. -maktadır sınırlı; -mıştır yalnızca tarihsel olgu için.

### Açılış hareketleri

1. **Olgu + gerilim**: "ABD'de uzaktan çalışabilen işlerin %58'i hibrit; Amazon beş gün ofis istiyor."
2. **Somut olay**: bir tarih, bir yer, bir karar.
3. **Sayı ile çelişki**: "Ofisler %36 boş, kira düşmedi."
4. **Soru olarak çerçeve** (tek soru, cevabı makalede): "Ofise dönüş çağrısı verimlilikle mi ilgili, kontrolle mi?"
5. **Karşı görüşü önce vermek**: "Dimon haklı olabilir."

Yasak açılışlar: "Günümüzde", "Tarih boyunca", tanım, "Bu makalede ... ele alınacaktır",
sözlük anlamı, "Hepimiz biliyoruz ki".

### Gövde

- Yapı okura görünür ama başlıklarla değil, paragraf sırasıyla. Ara başlık ancak
  1200 kelime üstünde ve en fazla 3-4.
- Sıra: iddia → kanıt → karşı kanıt → yorum. Her iddia paragrafı kanıt paragrafıyla
  ödenir.
- Kanıt biçimi: "Gallup'un Mart 2024'te 12.000 kişiyle yaptığı ankete göre" —
  kim, ne zaman, kaç kişi, cümlenin içinde. "Araştırmalar gösteriyor ki" yasak.
- Karşı görüş zorunlu: en az bir paragraf, dürüst özetlenmiş.
- Geçişler somut: "Aynı ay", "Buna karşılık Stanford'da", "Bu veri şunu
  söylemiyor". "Öte yandan", "Bu bağlamda" yok.
- Yorum paragrafı ayrı ve işaretli. Olgu ile yorum aynı cümlede olmaz.
- Liste yalnızca gerçekten sıralı ya da paralel öğeler için (adımlar, ölçütler);
  düzyazıya sığan şey listeye girmez.

### Kapanış hareketleri

1. **Sonraki soru**: veri neyi söylemiyor; ne ölçülmeli.
2. **Somut sonuç**: "Şirketler üçe bölünecek: ev, ofis, arası."
3. **Yorumun sınırı**: "ABD verisi; Türkiye için ölçüm yok."
4. **En güçlü olguyu sona saklamak**.

Yasak kapanışlar: "Sonuç olarak" + özet, "Gelecek gösterecek", "Zaman içinde
göreceğiz", öneri listesi, okura çağrı.

### Yasaklar

- Kaynaksız sayı, kaynaksız "uzmanlara göre".
- Chatbot özeti: "Bu makalede X, Y ve Z ele alındı."
- Madde listesi ile düşünce anlatmak.
- "Yalnızca X değil aynı zamanda Y."
- Retorik soru zinciri.
- Olgu ile görüşün aynı cümlede karışması.
- Edilgen + "tarafından" (aktör biliniyorsa).
- Adlaştırma zinciri ("sağlanmasının artırılması").

### Kontrol listesi

- [ ] Her sayı ve her "X'e göre" için ad + yıl var
- [ ] En az bir karşı görüş paragrafı, dürüst
- [ ] Görüş cümleleri işaretli (bence / bana göre / bu yazının görüşü)
- [ ] Açılış olgu ya da olay; tanım ve "günümüzde" yok
- [ ] Ara başlık yalnızca 1200+ kelimede, ≤ 4
- [ ] Son paragraf özet değil; soru, sınır ya da en güçlü olgu
- [ ] -maktadır ≤ %25; "tarafından" ≤ 2/1000
- [ ] `metrik.py --tur makale`, `kalip_tara.py`, `yapi.py --tur makale` temiz; kaynaktan yazıldıysa `kaynak_hizala.py` aynalama yok

---

## Blog yazısı

### Amaç

Okur bir sorunla gelir; yazıdan bir görüş, bir yöntem ya da bir deneyim alır gider.
Deneme kadar kişisel, makale kadar kaynaklı değil: yazar okurla konuşur, kendi
deneyimini söyler, gerektiğinde bir kaynak gösterir. Blog, yazarın masasıdır;
kürsü değil.

### Ölçüler

| Ölçü | Hedef |
|---|---|
| Kelime | 400-1200 |
| Ortalama cümle | 9-16 kelime |
| Ritim | Konuşur gibi bağlı cümleler; kısa cümle seyrek ve bir şey söylüyor |
| Ateşman | 50-75 |
| Paragraf | 1-5 cümle; kısa paragraf serbest, ekranda okunur |
| Ara başlık | 600 kelime üstünde serbest; başlık bir cümle ya da soru, etiket değil |
| Kaynak | Sayı varsa bağlantı; deneyim varsa "ben" |

### Hitap ve kişi

- **Ben + sen/siz**. Kullanıcının profilinde hangisi varsa o; yoksa "siz" ile başla,
  kullanıcıya sor.
- Metin boyunca tek hitap; "sen" ile "siz" karışmaz.
- "Biz" okurla yazarı kapsıyorsa olur ("bu işi yapanlar olarak biz").
- Zaman: -yor ve -dı; geniş zaman öneri cümlelerinde. -maktadır yok.

### Açılış hareketleri

1. **Okurun sorunu, okurun diliyle**: "Gece üçte hala uyuyamıyorsan telefon değil, kafein."
2. **Kendi başarısızlığın**: "Üç yıl yanlış yaptım."
3. **Somut sonuç önden**: "Şu değişiklik faturayı yarıya indirdi."
4. **Karşı iddia**: "Sabah rutini işe yaramıyor, en azından bende."
5. **Kısa sahne**: deneme gibi ama bir paragrafta bitir.

Yasak açılışlar: "Bu yazıda ... anlatacağım", "Merhaba", "Günümüzde", tanım,
"Hepimiz bazen".

### Gövde

- Bir sorun, bir yol, bir sonuç. Yol birden fazla adımsa liste olabilir; adımlar
  gerçekten sıralıysa.
- Deneyim ve öneri ayrı: "bende şöyle oldu" ile "sen şöyle yap" aynı cümlede değil.
- Kanıt: kendi verisi, tek bir dış kaynak (bağlantı ile), somut örnek.
- Ara başlıklar yazının iskeleti değil, okurun nefes yeridir. Başlıksız da okunmalı.
- Kalın yazı: yazı başına en fazla iki üç yerde, gerçek uyarı için. Vurgu cümle
  düzeniyle yapılır.
- Geçişler: "ama", "sonra", "bir de", "şimdi". "Bunun yanı sıra", "öte yandan" yok.
- Okura soru: bir tane, gerçek olsun.

### Kapanış hareketleri

1. **Tek somut adım**: "Bu akşam kahveyi üçten sonra içme, bir hafta bak."
2. **Ne bilmediğini söyle**: "Bende işe yaradı; sende neden yaramayabilir, bilmiyorum."
3. **Açılıştaki soruna dön**: sorun aynı, bakış değişmiş.
4. **Sonraki yazıya kapı** (bir cümle; tanıtım değil).

Yasak kapanışlar: "Umarım faydalı olmuştur", "Yorumlarda paylaşın", "Sonuç
olarak" + özet, "Unutmayın ki", madde madde özet, bülten çağrısı (o, metnin dışında
durur).

### Yasaklar

- Chatbot tonu: "harika", "heyecan verici", "haydi başlayalım", "sizlere".
- "Yalnızca X değil aynı zamanda Y."
- Her paragrafı soruyla açmak.
- Emoji (kullanıcı istemedikçe).
- Aşınmış sözler: yolculuk, dönüşüm, farkındalık, ekosistem, "fark yaratmak".
- Kaynaksız sayı; "araştırmalar gösteriyor".
- Uzun tire (—); Türkçe blogda virgül ve iki nokta.
- Başlık yığını: 1000 kelimede beşten çok ara başlık.

### Kontrol listesi

- [ ] İlk cümle okurun sorunu, benim başarısızlığım, sonuç ya da karşı iddia
- [ ] Hitap tek (sen ya da siz), baştan sona
- [ ] Deneyim ile öneri ayrı cümlelerde
- [ ] Sayı varsa bağlantı; yoksa "bende böyle oldu"
- [ ] Kalın ≤ 3, ara başlık ≤ 5, hepsi cümle ya da soru
- [ ] Kapanış somut adım, itiraf ya da dönüş; özet ve çağrı değil
- [ ] Hiç "-maktadır", hiç uzun tire, hiç "sizlere"
- [ ] `metrik.py --tur blog`, `kalip_tara.py`, `yapi.py --tur blog` temiz

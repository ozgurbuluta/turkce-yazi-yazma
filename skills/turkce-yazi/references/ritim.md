# Ritim

Ritim, cümlelerin birbirine nasıl yaslandığıdır; uzunluk listesi değil. Makine
metni iki biçimde bozuk olur ve ikisi de aynı derecede kötüdür:

- **Metronom**: her cümle 12-18 kelime, her paragraf üç dört cümle. Rapor sesi.
- **Parçalanma**: her cümle üç beş kelime, özne her cümlede yeniden kurulur, nefes
  yok. "Aldı. Bilmiyordu. Öğrendim." Reklam sesi; İngilizce "punchy" stilinin
  kopyası.

İkincisi, birincisini düzeltmeye çalışan editörün en sık düştüğü çukurdur. Bu belge
o çukurdan uzak durmayı da anlatır.

`scripts/metrik.py` cümle uzunluğu dağılımını verir (ortalama, CV, kısa cümle payı);
`scripts/yapi.py` art arda kısa cümle dizilerini gösterir. Bunlar **nereye bakacağını**
söyler. Ne yapacağını paragraf söyler.

## Türkçe cümle nasıl bağlanır

Türkçenin ritmi ulaçtan gelir. İngilizce iki düşünceyi iki cümle yapar ya da "and,
because, when" ile bağlar; Türkçe ikinci düşünceyi birincinin içine katlar:

| Bağ | Ulaç | Örnek |
|---|---|---|
| Ardışıklık | -ip, -erek | Kutuyu **açıp** içine baktı. / **Koşarak** geldi. |
| Zaman | -ince, -diğinde, -ken, -dikten sonra | Eve **gelince** anladım. / **Sorduğumda** güldü. |
| Sebep | -diği için, -diğinden | Kitapçık İngilizce **olduğu için** kuramadık. |
| Koşul | -se, -dikçe | Fişi **çekmezsen** yanar. / **Kullandıkça** öğrendim. |
| Durum | -meden, -e -e, -miş gibi | Ne olduğunu **bilmeden** aldı. / **Düşe kalka** öğrendim. |
| Karşıtlık | -diği halde, -se de | Maaşının üç katı **olduğu halde** aldı. |

Bir de noktalı virgül ve virgül: "Ben dokuz yaşındaydım; ne işe yaradığını
bilmiyordum." İki bağımsız cümle, tek nefes.

**Kural değil, soru:** art arda iki kısa cümle gördüğünde aralarında bu tablodan
bir ilişki var mı? Varsa bağla. Yoksa, ayrı durmalarının bir sebebi var mı (vuruş,
duraklama, ton değişimi)? Yoksa yine bağla ya da birini sil.

## Parçalanma: önce / sonra

> **Parçalı:** Babam bilgisayar aldı. 1994'tü. Kutusu büyüktü. Buzdolabından büyük.
> Kurmak iki gün sürdü. Kitapçık İngilizceydi. Evde İngilizce bilen yoktu.
>
> **Bağlı:** Babam ilk bilgisayarı eve 1994'te getirdi; kutusu buzdolabından
> büyüktü. Kurmak iki gün sürdü, çünkü kitapçık İngilizceydi ve evde İngilizce
> bilen yoktu.

Yedi cümle üçe indi, hiçbir bilgi gitmedi, nefes geldi. "Kutusu buzdolabından
büyüktü" hala kısa ve hala vuruyor; çünkü etrafında uzun cümleler var.

> **Parçalı:** Sordum. Neden diye. "Sen öğrenirsin diye." Öğrendim.
>
> **Bağlı:** Yıllar sonra neden diye sorduğumda "Sen öğrenirsin diye," dedi.
> Öğrendim.

Burada "Öğrendim." tek başına kaldı; kalmalı. Vuruş o. Öncekiler ona yol açıyor.

Parçalanmanın işaretleri:
- Özne her cümlede yeniden kuruluyor ya da her cümle aynı özneyle başlıyor.
- Cümleler noktayla bitiyor ama düşünce bitmiyor ("Buzdolabından büyük." bir
  önceki cümlenin devamı).
- Yüksek sesle okuyunca kesik kesik, nefes nefese.
- Bir paragrafta birden çok "vuruş"; hepsi vuruyorsa hiçbiri vurmuyor.

## Metronom: önce / sonra

> **Metronom:** Bilgisayar 1994 yılında evimize gelmiştir. Kutusu oldukça büyük
> boyutlardaydı. Kurulum süreci iki gün sürmüştür. Kitapçığın İngilizce olması
> zorluk yaratmıştır.
>
> **Dalgalı:** Babam ilk bilgisayarı eve 1994'te getirdi; kutusu buzdolabından
> büyüktü. Kurmak iki gün sürdü, çünkü kitapçık İngilizceydi ve evde İngilizce
> bilen yoktu.

Aynı hedef metin. Metronomdan çıkış da parçalanmadan çıkış da aynı yere varır:
bir uzun, bir kısa, bağlı, nefesli.

## Üç temel hareket

1. **Uzun → kısa** (vuruş): "Babam o kutuyu maaşının üç katına, kimse ne işe
   yaradığını söylememişken, kitapçığı İngilizceyken aldı. Aldı."
2. **Kısa → kısa → uzun** (birikme): "Kutusu büyüktü. Kurmak iki gün sürdü.
   Kurulduğunda da ne yapacağımızı bilmiyorduk, çünkü kitapçık İngilizceydi ve evde
   İngilizce bilen yoktu."
3. **Tek cümlelik paragraf** (durak): metinde bir, en çok iki kez.

Üçü de seyrek olduğu için işe yarar. Her paragrafta bir vuruş varsa vuruş yok
demektir.

## Yüklem çeşitliliği

Art arda gelen cümleler aynı ekle bitince metin monotonlaşır: "...maktadır.
...maktadır." ya da "...dı. ...dı. ...dı." (parçalı metinde ikincisi çok görülür).

- Anlatı: -dı baskın olur, doğaldır. Arada -yor, -mış, ad cümlesi ("Kutusu
  büyüktü.") serpiştirilir; ulaçla bağlanan cümlelerde zaten tek yüklem kalır.
- Deneme: -yor, -dı, geniş zaman, ad cümlesi karışık.
- Makale: -dır ve -maktadır kabul edilir ama üst üste gelince rapor sesi.
- Reel: -yor ve ad cümlesi; -dır neredeyse hiç.

## Ölçüt paragraflar

3b adımında yeniden yazdığın paragrafı bunlardan biriyle yan yana koy (kullanıcının
kendi arşivi varsa onunkiyle). Sayı için değil, kulak için.

**Deneme**
> Şimdi düşünüyorum da, babamın maaşının üç katına o kutuyu almasının bir mantığı
> yoktu. Kimse ne yapacağımızı söylememişti, ama aldı. Yıllar sonra neden diye
> sorduğumda "Sen öğrenirsin diye," dedi. Öğrendim.

**Reel** (sesli)
> Babam 1994'te, maaşının üç katına, ne işe yaradığını bilmediği bir bilgisayar
> aldı. Kitapçık İngilizceydi, evde İngilizce bilen yoktu; kurmak iki gün sürdü.

**Blog**
> Üç yıl sabah beşte kalktım, çünkü herkes öyle diyordu. Verim artmadı, uykum
> azaldı. Sonra bir ay boyunca ne zaman uyanırsam o zaman kalktım ve aynı işi daha
> kısa sürede bitirdiğimi fark ettim. Bende çalışan buydu; sende çalışır mı,
> bilmiyorum.

**Makale**
> Gallup'un Mart 2024'te 12.000 çalışanla yaptığı ankete göre uzaktan çalışabilen
> işlerin %58'i hibrit düzende. Aynı dönemde Amazon ve JPMorgan çalışanlarını
> haftada beş gün ofise çağırdı; iki eğilim aynı anda büyüyor.

## Tür başına ölçüler

Bunlar yol göstericidir, hedef değil; karar paragrafta verilir. `references/turler.md`
ve `metrik.py --tur` aynı sayıları kullanır.

| Tür | Ortalama cümle (kelime) | Paragraf | Ateşman |
|---|---|---|---|
| Reel | 6-12 | nefes başına bir satır | 70-95 |
| Deneme | 10-18 | 2-8 cümle | 45-75 |
| Makale | 12-20 | 3-7 cümle | 35-60 |
| Blog | 9-16 | 1-5 cümle | 50-75 |

Ateşman: `198,825 − 40,175 × (hece/kelime) − 2,610 × (kelime/cümle)`; 90+ çok
kolay, 70-89 kolay, 50-69 orta, 30-49 zor. Bezirci-Yılmaz sınıf düzeyi verir ve
uzun sözcükleri ağırlıklandırdığı için Türkçede daha ayırt edicidir.

## Ritmi düzeltme sırası

1. Önce içeriği düzelt (kalıp, çeviri kokusu). Boş cümleler gidince ritim zaten
   değişir.
2. Paragrafı yüksek sesle oku (ya da okur gibi düşün). Nefesin kesildiği yer
   parçalanma, nefesin yetmediği yer aşırı uzun cümle.
3. Art arda kısa cümleleri ulaçla bağla; ilişki yoksa birini sil.
4. Aşırı uzun cümlede özne ile fiil arasındaki yan cümleyi öne al ya da ayır.
5. Her paragrafın en güçlü cümlesini bul; sona taşı ya da sonrakileri sil. Kısa
   kalacaksa kalsın; vuruş o.
6. Ölçüt paragrafla karşılaştır (3b). Sonra, istersen, `metrik.py` ile bak: ortalama
   tür bandında mı, art arda kısa dizi kaldı mı. Sayı kulağa uymuyorsa kulak kazanır.

## Yapılmayacaklar

- Rastgele kısa cümle serpiştirmek. Kısa cümle vuruştur; vuracak bir şey olmalı.
- Uzun cümleyi "okunabilirlik" için ikiye üçe kesmek. Türkçe uzun cümle taşır;
  yeter ki fiile giden yol açık olsun.
- Her paragrafı soruyla açmak.
- Parçalı cümle ("Ve sonra. Hiçbir şey.") yığmak; bir kez etkili, üç kez tik.
- Anlatıyı şimdiki zamana çevirmek "canlı olsun" diye.

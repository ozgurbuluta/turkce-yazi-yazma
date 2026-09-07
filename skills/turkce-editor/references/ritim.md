# Ritim

Ritim, cümle ve paragraf uzunluklarının dağılımıdır. Makine metni tekdüzedir:
cümleler 12-18 kelime, paragraflar 3-4 cümle, hepsi aynı. İnsan metni dalgalıdır:
uzun bir cümlenin ardından iki kelimelik bir cümle gelir; tek cümlelik bir paragraf
sekiz cümlelik bir paragrafı takip eder.

`scripts/metrik.py` bunu ölçer: cümle uzunluğunun değişim katsayısı (CV = std /
ortalama). İnsan düzyazısında 0,5 üstü olağandır; 0,35 altı tekdüzedir. Paragraf
kelime sayısı için CV 0,25 altı tekdüzedir.

## Türkçede ritim nasıl çalışır

Türkçe fiil sonda olduğu için cümle **sonunda düğümlenir**. Uzun cümle, okuru fiile
kadar bekletir; bu bekleme bilinçli kullanılınca gerilim, kullanılmayınca yorgunluk
yaratır. Kısa cümle, düğümü hemen çözer. İkisinin sırası ritmi kurar.

Üç temel hareket:

1. **Uzun → kısa** (vuruş): "Babam o kutuyu maaşının üç katına, kimse ne işe yaradığını söylememişken, kitapçığı İngilizceyken aldı. Aldı."
2. **Kısa → kısa → uzun** (birikme): "Kutusu büyüktü. Kurmak iki gün sürdü. Kurulduğunda da ne yapacağımızı bilmiyorduk, çünkü kitapçık İngilizceydi ve evde İngilizce bilen yoktu."
3. **Tek cümlelik paragraf** (durak): metinde bir, en çok iki kez.

## Cümle içi ritim

- Fiile giden yol kısa olsun. Özne ile fiil arasına üç kelimeden fazla yan cümle
  girerse okur özneyi unutur. Yan cümleyi öne al ya da ayrı cümle yap.
- Virgül, nefestir; her yan cümleye virgül koymak nefesi keser. Türkçede "ve" ile
  bağlanan iki kısa cümleye virgül gerekmez.
- Devrik cümle vurgudur; paragrafta bir tane etkilidir, üçü özentidir.
- Noktalı virgül ve iki nokta Türkçe düzyazıda seyrek. Uzun tire (—) neredeyse hiç.

## Yüklem çeşitliliği

Art arda gelen cümleler aynı ekle bitince metin monotonlaşır: "...maktadır.
...maktadır. ...maktadır." Ya da "...dır. ...dır. ...dır." `metrik.py` payları verir.

- Anlatı: -dı baskın olur, doğaldır. Arada -yor (şimdiki zamana geçiş), -mış
  (aktarım), ad cümlesi ("Kutusu büyüktü.") serpiştirilir.
- Deneme: -yor, -dı, geniş zaman, ad cümlesi karışık. Hiçbiri %40'ı geçmez.
- Makale: -dır ve -maktadır kabul edilir ama toplamı %50'yi geçince rapor sesi.
- Reel: -yor ve ad cümlesi; -dır neredeyse hiç. Soru cümlesi bir, en çok iki.

## Tür başına hedefler

Bunlar `tur-profilleri` skill'indeki profillerle ve `metrik.py --tur` ile aynıdır.
Faz 6 kalibrasyonunda insan külliyatının yüzdelikleriyle güncellenir (`docs/yontem.md`).

| Tür | Ortalama cümle (kelime) | CV | Paragraf | Ateşman |
|---|---|---|---|---|
| Reel | 5-12 | ≥ 0,45 | 1-2 cümle, nefes başına bir paragraf | 70-95 |
| Deneme | 9-18 | ≥ 0,50 | 2-8 cümle, en az bir tek cümlelik | 45-75 |
| Makale | 12-20 | ≥ 0,45 | 3-7 cümle | 35-60 |
| Blog | 8-16 | ≥ 0,45 | 1-5 cümle | 50-75 |

Ateşman okunabilirlik formülü: `198,825 − 40,175 × (hece/kelime) − 2,610 ×
(kelime/cümle)`. 90-100 çok kolay, 70-89 kolay, 50-69 orta, 30-49 zor, 0-29 çok zor.
Bezirci-Yılmaz ölçüsü sınıf düzeyi verir (1-8 ilköğretim, 9-12 lise, 13-16 lisans,
16+ akademik); Türkçe için Ateşman'dan daha ayırt edicidir çünkü uzun sözcükleri
ağırlıklandırır.

## Ritmi düzeltme sırası

1. Önce içeriği düzelt (kalıp, çeviri kokusu). Boş cümleler gidince ritim zaten değişir.
2. En uzun üç cümleyi bul. Hepsi gerekli mi? Böl ya da kes.
3. Her paragrafın en güçlü cümlesini bul. Sona mı? Değilse sona taşı ya da
   sonrakileri sil.
4. Metinde hiç 1-4 kelimelik cümle yoksa bir tane yaz. Bir cümleyi ikiye bölmek
   yeter: "... aldı. Aldı."
5. Aynı ekle biten art arda üç cümle varsa ortadakini değiştir.
6. `metrik.py` ile yeniden ölç. CV yükselmeli, ortalama uzunluk türe uymalı.

## Ritim düzeltirken yapılmayacaklar

- Rastgele kısa cümle serpiştirmek. Kısa cümle vuruştur; vuracak bir şey olmalı.
- Her paragrafı soruyla açmak.
- Parçalı cümle ("Ve sonra. Hiçbir şey.") yığmak; bir kez etkili, üç kez tik.
- Anlatıyı şimdiki zamana çevirmek "canlı olsun" diye. Kullanıcı hangi zamanı
  seçtiyse odur.

# Puanlama rubriği

`puanla` kipinde ve `düzelt` kipinin önce/sonra karşılaştırmasında kullanılır.
Altı eksen, her biri 0-100. Toplam puan eksenlerin ortalamasıdır; tür belliyse
"tür uyumu", ses arşivi varsa "ses uyumu" ağırlığı iki katıdır.

Puan, betiklerin sayılarıyla senin okumanın birleşimidir. Betik sayısı ipucudur,
puan değil. Her eksen için bir cümle gerekçe yazılır; gerekçe metinden alıntı içerir.

## 1. Çeviri kokusu (0 = çeviri, 100 = Türkçe düşünülmüş)

Kaynak: `kalip_tara.py` çeviri alt puanı (ters çevrilir), `metrik.py` tarafından /
bir / zamir / adlaştırma oranları, kendi okuman.

| Puan | Görünüm |
|---|---|
| 90-100 | Hiçbir cümle İngilizceye geri çevrilemez gibi durmuyor; özne düşük, fiil tek, "bir" yalnız sayarken |
| 70-89 | Bir iki hafif iz (bir "açısından", bir "sağlamak"); genel akış Türkçe |
| 50-69 | Her paragrafta bir çeviri cümlesi; "tarafından", "sahip", "bir şekilde" görünüyor |
| 30-49 | Cümle sırası İngilizce; ki-cümleleri, edilgen+tarafından yaygın |
| 0-29 | Makine çevirisi gibi |

## 2. AI kalıbı (0 = kalıp yığını, 100 = kalıpsız)

Kaynak: `kalip_tara.py` AI alt puanı (ters çevrilir), `yapi.py` üçlü liste / değil
karşıtlığı / giriş-sonuç aynası / iskelet cümlesi.

| Puan | Görünüm |
|---|---|
| 90-100 | Boş geçiş yok, aşınmış söz yok, özet paragrafı yok |
| 70-89 | Bir "günümüzde", bir "önemli rol"; yapısal kalıp yok |
| 50-69 | Her paragrafta bir kalıp; bir üçlü liste; sonuç girişi yineliyor |
| 30-49 | Bağlaçla başlayan cümleler %30 üstü; "yalnızca ... değil aynı zamanda" var; chatbot kapanışı |
| 0-29 | Metin şablon |

## 3. Ritim (0 = tekdüze, 100 = dalgalı ve kasıtlı)

Kaynak: `metrik.py` CV, paragraf CV, yüklem çeşitliliği; `references/ritim.md`.

| Puan | Görünüm |
|---|---|
| 90-100 | CV ≥ 0,5; kısa cümle vuruş olarak kullanılmış; paragraflar farklı boyda; yüklem karışık |
| 70-89 | CV 0,4-0,5; birkaç kısa cümle; hafif tekdüze paragraf |
| 50-69 | CV 0,3-0,4; paragraflar aynı boyda; bir yüklem eki %40 üstü |
| 30-49 | CV < 0,3; her cümle 12-18 kelime; -maktadır dizisi |
| 0-29 | Metronom |

## 4. Somutluk (0 = soyut, 100 = somut)

Betik ölçmez; sen okursun. Sorular: Her paragrafta gözle görülür bir şey var mı
(sayı, ad, yer, nesne, olay)? "Önemli", "etkili", "çeşitli" gibi sıfatların
arkasında olgu var mı? Aktörsüz cümle (kim yaptı belli değil) kaç tane?

| Puan | Görünüm |
|---|---|
| 90-100 | Her iddia bir örnekle, sayıyla ya da olayla yere basıyor |
| 70-89 | Çoğu paragraf somut; bir iki genel cümle |
| 50-69 | Somut ve soyut yarı yarıya; "araştırmalar gösteriyor" ama hangi araştırma belli değil |
| 30-49 | Sıfatlar olguların yerini almış; aktörsüz cümleler yaygın |
| 0-29 | Hiçbir şey görünmüyor |

## 5. Tür uyumu (0 = yanlış tür, 100 = türün kurallarında)

Kaynak: `tur-profilleri` skill'indeki profil; `metrik.py --tur`, `yapi.py --tur`
uyarıları.

| Puan | Görünüm |
|---|---|
| 90-100 | Uzunluk, cümle bandı, hitap, açılış ve kapanış hareketi, yasaklar: hepsi profile uygun |
| 70-89 | Bir ölçü bant dışında (biraz uzun, biraz zor) |
| 50-69 | Hitap karışık (sen/siz), açılış türe ait değil |
| 30-49 | Reel'de başlık/madde, makalede sohbet tonu gibi tür yasağı çiğnenmiş |
| 0-29 | Başka türde yazılmış |

Tür bilinmiyorsa bu eksen puanlanmaz ve ortalamaya girmez.

## 6. Ses uyumu (0 = başka biri yazmış, 100 = yazarın kendi sesi)

Kaynak: `voice/profil.md` özellikleri (cümle uzunluğu dağılımı, sevilen bağlaçlar
ve fiiller, açılış hareketi tipi, zamir oranı, noktalama alışkanlığı), `voice/karsit/`
çiftlerindeki reddedilen kalıplar.

| Puan | Görünüm |
|---|---|
| 90-100 | Profil ölçüleri içinde; reddedilen kalıplardan hiçbiri yok; yazarın imza hareketleri (varsa) görünüyor |
| 70-89 | Ölçüler yakın; bir iki yabancı sözcük |
| 50-69 | Cümle uzunluğu ya da hitap profilden sapıyor |
| 30-49 | Reddedilmiş kalıplar geri gelmiş |
| 0-29 | Yazarla ilgisi yok |

`voice/` yoksa bu eksen puanlanmaz ve ortalamaya girmez.

## Rapor biçimi

```
Puan: 62 → 84 (önce → sonra)
  Çeviri kokusu  48 → 88  "tarafından" 5 → 0; "bir şekilde" 2 → 0
  AI kalıbı      35 → 82  özet paragrafı silindi; "günümüz dünyasında" ×2 → 0
  Ritim          55 → 78  CV 0,26 → 0,52; -maktadır %55 → %6
  Somutluk       60 → 70  "araştırmalar gösteriyor" cümlesi kaynak yokken silindi (iddia listesinde)
  Tür uyumu      80 → 90  deneme; 179 kelime hala kısa
  Ses uyumu      —        voice/ yok
```

Puanı yuvarlak vermekten kaçın (60, 70, 80). Gerçek bir tahmin ver (63, 71, 84);
okur puanın düşünülmüş olduğunu anlar.

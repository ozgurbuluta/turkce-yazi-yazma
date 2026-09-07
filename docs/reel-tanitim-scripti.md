# Reel metni: "Claude senin gibi yazsın istiyorsan"

Süre hedefi: 80–95 sn. Hitap: sen (baştan sona). Parantez içleri seslendirilmez; fact-check ve alt yazı içindir.

---

## [0–5 sn | KANCA]

Claude senin gibi yazsın istiyorsan, bu skill'i indirmelisin. Ama önce bir itiraf.

## [5–25 sn | SORUN]

Bunun gibi onlarca video gördüm. Hep aynı birkaç skill öneriliyor; en bilineni Humanizer (blader/humanizer, GitHub, MIT lisanslı; Vikipedi'nin "Signs of AI writing" sayfasındaki 35 kalıba dayanıyor). Ben de İngilizce yazılarımda kullanıyorum, iyi çalışıyor.

Sorun şu: bu skill'lerin hiçbiri Türkçe için yapılmadı. Türkçe bir yazı yazdırdığında sonuç düzelmiş gibi görünüyor; okuduğun an "Bunu ben yazmazdım" diyorsun. Çünkü model İngilizce düşünüp Türkçe yazıyor. "Bir şekilde", "tarafından", "önemli bir rol oynamaktadır"… hepsi çeviri kokuyor.

## [25–55 sn | ÇÖZÜM]

Ben de tamamen Türkçe için bir skill yazdım.

Önce kalıp listeleri: 111 Türkçe yapay zeka kalıbı, 71 çeviri kokusu kalıbı; her birinin yanında ne yapılacağı yazıyor (`skills/turkce-yazi/data/ai_kaliplari.tsv`: 111 kalıp, 6 kategori; `ceviri_kokusu.tsv`: 71 kalıp, 10 kategori; elle derlendi, MIT).

Sonra gerçek Türkçe: bir kelimenin doğal Türkçede ne kadar yaygın olduğunu iki sıklık listesinden kontrol ediyor. Konuşma dili için 200 milyonu aşkın kelimelik altyazı derlemi (OpenSubtitles 2018 Türkçe; hermitdave/FrequencyWords; paketteki ilk 30.000 kelimenin toplam sayımı 198 milyon; CC BY-SA 4.0). Yazı dili için 2024 tarihli haber derlemi (Leipzig Corpora Collection, `tur_news_2024_30K`: 30.000 cümle, 27.314 kelime biçimi; CC BY 4.0).

Bir de ölçüm: cümle uzunluğu dalgalanmasını ve okunabilirliği Türkçe için geliştirilmiş formüllerle hesaplıyor (Ateşman 1997: 198,825 − 40,175 × hece/kelime − 2,610 × kelime/cümle; Bezirci-Yılmaz 2010). "Kulağa AI gibi geliyor" demiyor; hangi cümlenin neden öyle geldiğini gösteriyor.

## [55–78 sn | KANIT]

Bunu kafamdan uydurmadım. Araştırmalar, modele "benim gibi yaz" deyip örnek yığmanın pek işe yaramadığını gösteriyor (EMNLP 2025 Findings, "Catch Me If You Can? Not Yet": 400'den fazla yazar, model başına 40.000'den fazla üretim; blog ve forum gibi kişisel türlerde başarısız; örnek sayısını artırmak sınırlı fayda sağlıyor).

İşe yarayan şey, yazarın özelliklerini açıkça çıkarmak ve beğenmediğin cümleyi düzelttiğin haliyle yan yana koymak (Yazan, Verberne ve Situmeang, ECIR 2025: yazar özellikleri + karşıt örnekler, standart RAG'e göre %15 göreli iyileşme). Skill tam olarak bunu yapıyor: her düzeltmenden yeni bir tercih öğreniyor.

## [78–92 sn | KAPANIŞ]

Adında "Türkçe" geçen modeller bile genel modellerin gerisinde kaldı (Cetvel, EACL 2026: 23 görev, 33 açık ağırlıklı model; Türkçeye özel eğitilmiş modellerin çoğu Llama 3 ve Mistral gibi genel modellerin gerisinde). Sorun modelde değil, ona Türkçeyi nasıl anlattığında.

Türkçe yazıyorsan bunu kur. Açık kaynak, ücretsiz. Link profilde (GitHub deposu adı yayına almadan önce doğrulanacak).

---

## Ekran yazısı önerileri

- 0 sn: "Claude senin gibi yazsın mı?"
- 8 sn: "Humanizer: 35 İngilizce kalıp"
- 18 sn: "Bunu ben yazmazdım."
- 28 sn: "111 AI kalıbı · 71 çeviri kokusu"
- 38 sn: "200M+ kelime altyazı · 30K haber cümlesi"
- 48 sn: "Ateşman okunabilirlik"
- 60 sn: "400+ yazar, 40.000+ üretim: örnek yığmak işe yaramıyor"
- 70 sn: "Karşıt örnekler: %15 iyileşme"
- 85 sn: "Açık kaynak · Link profilde"

---

## Fact-check notları

### Doğrulanan rakamlar ve kaynakları

- Humanizer 35 kalıp: blader/humanizer README (sürüm 2.11.x). Sayı sürümle değişiyor; Aboudjem/humanizer-skill çatalı 55 kalıp kullanıyor. Çekimden önce README'yi tekrar kontrol et.
- 111 ve 71 kalıp: `grep -vc '^#'` ile sayıldı (`ai_kaliplari.tsv`, `ceviri_kokusu.tsv`). Liste büyürse rakamı güncelle.
- OpenSubtitles listesi: `data/LICENSES.md`; kaynak dosya `content/2018/tr/tr_50k.txt`. Paketteki 30.000 kelimenin sayım toplamı 198.196.602; derlemin tamamı bundan büyük, bu yüzden "200 milyonu aşkın" güvenli bir alt sınır.
- Leipzig: `tur_news_2024_30K`, 30.000 cümle; listede sıklığı ≥ 2 olan 27.314 kelime biçimi (toplam sayım 357.319). Lisans CC BY 4.0; atıf Goldhahn, Eckart, Quasthoff, LREC 2012.
- Ateşman 1997 katsayıları ve Bezirci-Yılmaz 2010: birden çok hakemli Türkçe okunabilirlik makalesiyle doğrulandı.
- EMNLP 2025 Findings: "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors"; 400'den fazla yazar, model başına 40.000'den fazla üretim; haber ve e-postada kısmen başarılı, blog ve forumda başarısız; daha fazla örnek sınırlı kazanç.
- ECIR 2025: Yazan, Verberne, Situmeang, "Improving RAG for Personalization with Author Features and Contrastive Examples"; temel RAG'e göre %15 göreli iyileşme. Kod: github.com/myazann/AP-Bots.
- Cetvel: EACL 2026 (arXiv 2508.16431); 23 görev, 7 kategori, 33 açık ağırlıklı model (70B'ye kadar); Türkçe odaklı komut ayarlı modeller genel modellerin gerisinde.

### Örnek metinden bilerek değiştirdiklerim

- "Kocaman bir Türkçe cümle kütüphanesi entegre ettim" → sıklık listeleri. Pakette cümle değil kelime listesi var; Leipzig cümle dosyaları `fetch_data.sh --hepsi` ile isteğe bağlı iniyor ve depoya girmiyor.
- "Hangi kelimelerin birlikte kullanıldığını araştıran" → çıkarıldı. Eşdizim (collocation) analizi yok; Leipzig'in eşdizim verisi paketlenmiyor.
- "Yüksek lisans ve doktora seviyesinde araştırmalar" → "araştırmalar". Dayandığımız kaynakların çoğu hakemli konferans makalesi (EMNLP, ECIR, EACL, LREC). Çeviri kokusu listesi Türkçede edilgen çatı ve "tarafından" üzerine dilbilim tezlerinden de yararlanıyor; tez künyeleri `docs/arastirma.md`'ye eklenince bu ifade geri konabilir.
- Zemberek'ten söz etmedim: henüz entegre değil; planda isteğe bağlı `zeyrek` (MIT) var. Eklenince "(Zemberek, Apache 2.0)" parantezi eklenebilir.

### Yayından önce tamamlanması gerekenler

Depoda şu an veri listeleri, `trmetin.py`, `fetch_data.sh` ve `trim_lists.py` var. Şu cümleler ancak ilgili faz bitince doğru olur:

- "Hangi cümlenin neden öyle geldiğini gösteriyor" → `metrik.py`, `kalip_tara.py`, `siklik.py`, `yapi.py` ve `turkce-editor/SKILL.md` (2. faz).
- "Her düzeltmenden yeni bir tercih öğreniyor" → `kisisel-ses` ve `geri-bildirim-hafizasi` skill'leri (5. faz).
- "Link profilde" → depo GitHub'a yüklenmiş ve README'de kurulum adımları yazılmış olmalı.

### Metnin kendi kurallarımıza uyumu

"Sonuç olarak", "bu bağlamda", "yalnızca … değil aynı zamanda", "tarafından", "bir şekilde" yok. Cümle uzunlukları 3 ile 25 kelime arasında dalgalanıyor. Girişteki fikir kapanışta tekrar edilmiyor; kapanış yeni bir iddiaya (Cetvel) dayanıyor. Skill bitince metni `kalip_tara.py` ile taramayı unutma.

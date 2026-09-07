# Türkçe yapay zeka kalıpları

Bu liste "yasak sözcükler" listesi değildir. Her kalıp, bir düşünme kısayoludur:
yazar bir şey söylemek yerine söylemiş gibi yapmıştır. Düzeltme, sözcüğü değiştirmek
değil, boşluğu doldurmaktır: kim, ne yaptı, ne oldu?

Makine taraması `data/ai_kaliplari.tsv` üzerinden yapılır; burada kalıpların
neden kalıp olduğu ve nasıl düzeltileceği anlatılır.

## 1. Boş geçişler

Bağlaç, cümleler arasında gerçek bir ilişki varsa gerekir. AI metninde bağlaç,
ilişki yokken varmış gibi göstermek için kullanılır.

| Kalıp | Sorun | Önce | Sonra |
|---|---|---|---|
| bu bağlamda, bu doğrultuda, bu çerçevede | Hangi bağlam? Belirsiz gönderme | Bu bağlamda, şirket yeni bir strateji geliştirdi. | Şirket bunun üzerine satışı durdurdu. |
| sonuç olarak, özetle, kısacası | Etiketli özet; okur zaten okudu | Sonuç olarak, düzenli uyku sağlığı korur. | (paragrafı sil) |
| ilk olarak / ikinci olarak / son olarak | Düzyazıya sızmış liste | İlk olarak fiyatlar arttı. İkinci olarak talep düştü. | Fiyatlar arttı, talep düştü. |
| unutulmamalıdır ki, belirtmek gerekir ki | Aktörsüz uyarı + İngilizce "that" | Unutulmamalıdır ki bu veri eksiktir. | Bu veri eksik. |
| daha da önemlisi | Önemliyse neden sonda? | Daha da önemlisi, ödeme yapılmadı. | Ödeme yapılmadı. |
| bir başka deyişle | Aynı şeyi iki kez | X. Bir başka deyişle Y. | (iyi olanı seç) |
| öte yandan, bununla birlikte | Karşıtlık yokken karşıtlık işareti | Öte yandan ürün başarılı oldu. | Ürün tuttu. |

**Kural**: bağlacı sil, cümleyi oku. Anlam kaybolmadıysa bağlaç gereksizdi. Kayboldu ise
ilişkiyi somut yaz ("bunun üzerine", "aynı hafta", "buna rağmen").

## 2. Aşınmış sözler

| Kalıp | Önce | Sonra |
|---|---|---|
| önemli bir rol oynamak | Aile, çocuğun gelişiminde önemli bir rol oynar. | Çocuk ilk sözcüklerini ailesinden öğrenir. |
| kritik / kilit / hayati önem | Su, yaşam için hayati önem taşır. | Susuz üç gün dayanılır. |
| günümüz dünyasında, modern dünyada, dijital çağda | Günümüz dünyasında bilgiye erişim kolaylaştı. | Telefonda her şey var. |
| hızla değişen | Hızla değişen iş dünyasında... | (sil; ne değişti, onu yaz) |
| dönüşüm yolculuğu, öğrenme yolculuğu | Şirket bir dijital dönüşüm yolculuğuna çıktı. | Şirket faturaları kağıttan e-postaya taşıdı. |
| kapsamlı, çok yönlü, derinlemesine | Kapsamlı bir analiz yaptık. | Üç yılın satış verisine baktık. |
| fark yaratmak, değer katmak, katkı sağlamak | Bu proje topluma değer kattı. | Proje mahalleye bir kütüphane bıraktı. |
| çözüm sunmak, fırsat sunmak | Uygulama kullanıcılara çözümler sunuyor. | Uygulama faturayı ödüyor. |
| potansiyel | Bu pazarın büyük potansiyeli var. | Bu pazarda henüz kimse yok. |
| ekosistem, dinamikler, perspektif | Girişim ekosisteminin dinamikleri | Girişimciler, yatırımcılar ve aralarındaki para |
| farkındalık | Toplumda farkındalık yaratmak | İnsanlara bunu anlatmak |
| yeni ufuklar, kapı aralamak, ışık tutmak, köprü kurmak | Bu çalışma yeni ufuklar açıyor. | Bu çalışma şunu gösterdi: ... |
| hayatın her alanında | Teknoloji hayatın her alanında. | Teknoloji mutfakta, yatak odasında, cebimizde. |

**Kural**: kalıbın arkasındaki somut olguyu sor. Yoksa cümle gereksizdi. Varsa onu yaz.

## 3. Kof yükseltme

Sıfat ve zarfla önem ilan etmek: heyecan verici, benzersiz, eşsiz, muhteşem, kesinlikle,
şüphesiz, inkar edilemez, önemli ölçüde, ciddi anlamda, dikkate değer.

- "Sonuçlar oldukça dikkate değer." → "Satış üç ayda ikiye katlandı."
- "Bu inkar edilemez bir gerçek." → (sil; gerçekse söylemeye gerek yok)
- "Kesinlikle denemelisiniz." → "Deneyin."

**Kural**: yükseltici sıfatı sil. Cümle zayıfladıysa sorun sıfatta değil, kanıtsızlıkta.

## 4. Sohbet robotu tonu

| Kalıp | Neden |
|---|---|
| Umarım bu yazı faydalı olmuştur. | Chatbot kapanışı |
| Düşüncelerinizi yorumlarda paylaşın. | Etkileşim yemi; reel'de bir kez olabilir, yazıda olmaz |
| Sizlere, sizler için | "siz" yeter |
| Haydi başlayalım, gelin birlikte bakalım | Ne yapacağını söyleme, yap |
| Harika!, işte tam da bu yüzden | Kendi kendine alkış |
| Elbette, açıkçası, kesinlikle | Onay sözcüğü; kimseye cevap vermiyorsun |
| Peki ya ...? | Retorik soru; paragrafa bir kez, metne iki kez fazla |

## 5. İskelet cümleleri

Metnin ne yapacağını anlatan cümleler: "Bu yazıda X'i ele alacağız", "Şimdi Y'ye
yakından bakalım", "Aşağıda Z'yi bulacaksınız". Hepsi silinir; konuya girilir.

Önce: "Bu yazıda, uzaktan çalışmanın avantajlarını ve dezavantajlarını ele alacağız."
Sonra: "Uzaktan çalışan arkadaşlarımın yarısı iki yıl içinde ofise döndü."

## 6. Yapısal kalıplar

Bunlar sözcük değil, biçim kalıplarıdır; `scripts/yapi.py` sayar.

### Üçlü sıralama

"Hızlı, güvenilir ve ekonomik." AI metni her sıralamayı üçe tamamlar. Türkçe konuşan
insan ikiyle ya da dörtle de kalır; çoğu zaman tek somut örnek üçlü listeden daha
güçlüdür.

- "Veri gizliliği, dijital eşitsizlik ve öğretmen eğitimi gibi konular" → "Çocuğun kamerasını kim izliyor, o belli değil."

### Yapay karşıtlık: "X değil, Y"

"Sadece bir araç değil, aynı zamanda bir yol arkadaşı." İngilizce "not only... but also"
kopyası. Kimse "sadece araç" dememişti; karşıtlık uydurmadır.

- "Yalnızca bilgi vermekle kalmıyor, aynı zamanda ilham da veriyor." → "Bilgi veriyor." (ilham veriyorsa okur anlar)
- "Bu bir son değil, bir başlangıç." → (sil)

### Giriş-sonuç aynası

Sonuç paragrafı giriş paragrafını başka sözcüklerle tekrar eder. `yapi.py`'deki
Jaccard benzerliği 0,25'i geçince neredeyse kesindir. Sonuç ya kesilir ya yeni bir
şey söyler: bir soru, bir çelişki, bir sonraki adım.

### Aktörsüz cümle

"Önlemler alınmalıdır." Kim alacak? "Bu durum değerlendirilmelidir." Kim? Edilgen +
-malı, sorumluluğu buharlaştırır. Özneyi yaz; bilmiyorsan cümleyi sil.

### Adlaştırma zinciri

"Verimliliğin artırılmasının sağlanması amacıyla" → "verimliliği artırmak için".
Üst üste -ma/-me + iyelik. Fiile çevir.

### Paragraf-sonu özet cümlesi

Her paragrafın son cümlesi paragrafı özetliyorsa (\"Bu da gösteriyor ki...\",
\"Dolayısıyla...\") o cümleler silinir.

## 7. Resmiyet kayması

-yor yerine -maktadır, -dı yerine -mıştır, "var" yerine "bulunmaktadır", "şey" yerine
"husus", "için" yerine "açısından/bakımından/kapsamında". Tek tek doğru, üst üste
gelince rapor sesi. `metrik.py` payı verir: -maktadır cümlelerin %20'sini geçince
uyarı.

- "Şirket yeni ürününü piyasaya sürmüştür." → "Şirket yeni ürünü çıkardı."
- "Bu konuda çeşitli görüşler bulunmaktadır." → "Bu konuda herkes başka bir şey söylüyor."

## 8. Yazım tercihi: düzeltme işareti yok

Bu depo düz yazımı benimser: "zeka", "hala", "kağıt", "imkan", "resmi", "hikaye",
"kar". Şapkalı harf (â, î, û) sözlükte kalır, metne girmez. Kaynak metinde varsa
düzeltmede düz biçime çevrilir. Sebep: gündelik Türkçe böyle yazılıyor; şapkalı
biçim metni olduğundan resmi gösteriyor ve tutarsız kullanılıyor.

## 9. Kılavuz sesi: geniş zaman ve -dir yığını

Okura bir şeyi anlatırken (kurulum, kullanım, "şunu yapınca şu olur") her cümle
geniş zamanla bitince metin insan sesi değil, cihaz kılavuzu sesi verir: "yapar",
"oluşur", "gerekmez", "yeter", "kurarsın", "-dir". Tek tek doğru; üst üste gelince
soğuk ve dikte eder gibi. Konuşan biri ne olacağını -yor ve -acak ile anlatır,
"-dir" demez, iki kelimelik bilgi cümlesi kurmaz. Bunlar okurun kendi düzeltmesinden
alınmış çiftler; hepsi aynı yöne gidiyor:

- "Ayrıca bir şey yapman gerekmez." → "Ayrıca bir şey yapman gerekmiyor."
- "'Düzelt' demen yeter." → "'Düzelt' demen yeterli."
- "Onun yerine kendi GPT'ni kurarsın." → "Onun yerine kendi GPT'ni kurman gerek."
- "`dist/chatgpt/` adında bir klasör oluşur." → "... adında bir klasör oluşacak."
- "Dört şeye bakar:" → "Dört şeye bakarak buna karar veriyor:"
- "Kendi yazılarını verirsen senin gibi yazar." → "... senin sesini anlar ve o
  şekilde yazmaya başlar."
- "'Ses arşivimi kur' de; profilini çıkarır." → "... de; profilini çıkarsın." (İstek
  cümlesinden sonra sonuç -sın ile gelir; -ır ile gelince iki ayrı bildirim olur.)
- "... yazılmış bir metne çeviren bir skill'dir." → "... çeviren bir skill olması
  için tasarlandı."
- "Kod MIT." / "Cevap hep metin hakkındadır: hangi cümle, neden, nasıl." → silindi.
  İki kelimelik bilgi cümlesi ve -dır'lı özet, paragrafın sonuna yapıştırılmış
  etiket gibi durur.
- Başlık "Kullan" → "Kullanım". Emir kipli başlık düğme adı gibi okunur; başlık
  addır.
- "Bu depoyu indir" → "Bu repoyu indir". Okurun kullandığı sözcük neyse o; yaygın
  yabancı sözcüğe zorla Türkçe karşılık koymak da resmileştirmedir.
- Giriş cümlesinde dört tırnaklı örnek üst üste ("önemli bir rol oynamaktadır",
  "bir şekilde", "tarafından", "sonuç olarak") → tek düz cümle: "İngilizce düşünüp
  Türkçe'ye tercüme ediyor." Örnek yığını ilk cümlede okuru yorar; örnek gövdede
  gelir.

Geniş zaman yanlış değildir: genel doğru ("su yüz derecede kaynar") ve öneri ("bunu
akşam yapma") geniş zaman ister. Sorun yığındır; paragraftaki yüklemlerin çoğu -ar/-ır
ve -dir ise, okura ne olacağını anlatan cümleleri -yor/-acak'a çevir, kalanı bırak.

## Kalıp bulunca ne yapılır

1. Kalıbın yerine ne koyacağını değil, kalıbın **neyi gizlediğini** sor.
2. Gizlenen şey somut bir olguysa onu yaz.
3. Gizlenen bir şey yoksa cümleyi sil.
4. Silince paragraf çökerse paragraf zaten boştu.

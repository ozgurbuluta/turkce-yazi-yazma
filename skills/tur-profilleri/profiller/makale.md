# Makale

## Amaç

Okur bir konuda ne olduğunu, neden olduğunu ve ne anlama geldiğini öğrenir. Her
iddianın kaynağı vardır; yazarın görüşü varsa görüş olarak işaretlidir. Makale
inandırmaz, gösterir.

## Ölçüler

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

## Hitap ve kişi

- Varsayılan **üçüncü kişi**. "Biz" kurumsal makalede ("biz Türkiye'deki
  okurlar" değil, "biz bu çalışmada" anlamında) olabilir.
- "Ben" yalnızca görüş paragrafında ve açıkça: "Bence", "Bana göre".
- Okura hitap yok; "siz" yok.
- Zaman: geniş zaman ve -dı. -maktadır sınırlı; -mıştır yalnızca tarihsel olgu için.

## Açılış hareketleri

1. **Olgu + gerilim**: "ABD'de uzaktan çalışabilen işlerin %58'i hibrit; Amazon beş gün ofis istiyor."
2. **Somut olay**: bir tarih, bir yer, bir karar.
3. **Sayı ile çelişki**: "Ofisler %36 boş, kira düşmedi."
4. **Soru olarak çerçeve** (tek soru, cevabı makalede): "Ofise dönüş çağrısı verimlilikle mi ilgili, kontrolle mi?"
5. **Karşı görüşü önce vermek**: "Dimon haklı olabilir."

Yasak açılışlar: "Günümüzde", "Tarih boyunca", tanım, "Bu makalede ... ele alınacaktır",
sözlük anlamı, "Hepimiz biliyoruz ki".

## Gövde

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

## Kapanış hareketleri

1. **Sonraki soru**: veri neyi söylemiyor; ne ölçülmeli.
2. **Somut sonuç**: "Şirketler üçe bölünecek: ev, ofis, arası."
3. **Yorumun sınırı**: "ABD verisi; Türkiye için ölçüm yok."
4. **En güçlü olguyu sona saklamak**.

Yasak kapanışlar: "Sonuç olarak" + özet, "Gelecek gösterecek", "Zaman içinde
göreceğiz", öneri listesi, okura çağrı.

## Yasaklar

- Kaynaksız sayı, kaynaksız "uzmanlara göre".
- Chatbot özeti: "Bu makalede X, Y ve Z ele alındı."
- Madde listesi ile düşünce anlatmak.
- "Yalnızca X değil aynı zamanda Y."
- Retorik soru zinciri.
- Olgu ile görüşün aynı cümlede karışması.
- Edilgen + "tarafından" (aktör biliniyorsa).
- Adlaştırma zinciri ("sağlanmasının artırılması").

## Kontrol listesi

- [ ] Her sayı ve her "X'e göre" için ad + yıl var
- [ ] En az bir karşı görüş paragrafı, dürüst
- [ ] Görüş cümleleri işaretli (bence / bana göre / bu yazının görüşü)
- [ ] Açılış olgu ya da olay; tanım ve "günümüzde" yok
- [ ] Ara başlık yalnızca 1200+ kelimede, ≤ 4
- [ ] Son paragraf özet değil; soru, sınır ya da en güçlü olgu
- [ ] -maktadır ≤ %25; "tarafından" ≤ 2/1000
- [ ] `metrik.py --tur makale`, `kalip_tara.py`, `yapi.py --tur makale` temiz; kaynaktan yazıldıysa `kaynak_hizala.py` aynalama yok

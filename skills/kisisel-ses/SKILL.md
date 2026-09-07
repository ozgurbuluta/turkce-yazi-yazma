---
name: kisisel-ses
description: Yazarın kendi sesiyle yazmak için ses arşivi. Onaylanmış geçmiş metinlerden yazar özellikleri çıkarır (ses_ozellikleri.py), verilen göreve en yakın 2-3 örneği seçer (ornek_sec.py) ve reddedilen/onaylanan karşıt çiftleri sunar. "Benim sesimle yaz", "benim gibi yaz", "ses arşivimi kur", "profilimi güncelle", "hangi yazılarımı örnek al" dendiğinde ya da turkce-taslak / turkce-editor ses bilgisi istediğinde kullan. (Personal voice archive, author style profile, example selection for Turkish writing.)
license: MIT
---

# Kişisel ses

"Benim gibi yaz" ile birlikte on yazı vermek işe yaramaz; araştırma bunu gösteriyor
(bkz. `docs/arastirma.md`): birkaç örnekle üslup taklidi blog ve forum metinlerinde
başarısız, örnek sayısını artırmak kazandırmıyor. İşe yarayan üç şey var:

1. **Seçim**: tüm arşivi değil, bu göreve en yakın 2-3 metni vermek.
2. **Açık özellikler**: "yazar kısa cümle kurar" gibi ölçülmüş, sözle ifade edilmiş
   özellikler.
3. **Karşıt örnekler**: "bunu yazdı, bunu reddetti, sebebi bu" çiftleri.

Bu skill üçünü de üretir. Kişisel arşiv `voice/` klasöründedir, git'e girmez;
şablon `voice.example/` içindedir.

## Kurulum (ilk kez)

1. `voice.example/` klasörünü `voice/` olarak kopyala; örnek dosyaları sil.
2. Onaylanmış metinleri `voice/onaylanan/<tür>/` altına koy. Her dosya frontmatter
   taşır (`references/arsiv-yapisi.md`). "Onaylanmış" = yazarın yayımladığı ya da
   "bu benim" dediği metin; taslak, çeviri ya da başkasının düzeltmesi değil.
3. Profili üret:
   ```bash
   python3 scripts/ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
   ```
4. `voice/profil.md` içindeki "Elle notlar" bölümüne yazarın kendi söylediklerini
   ekle: imza hareketleri, yasakları, hitap tercihi.

En az 5 metin olmadan profil anlamlı değildir; betik bunu söyler. Tür başına 3
metin altındaysa tür profili verilmez, genel profil kullanılır.

## Görev öncesi kullanım

`turkce-taslak` ya da `turkce-editor` çalışmadan önce:

```bash
python3 scripts/ornek_sec.py --gorev "konu ya da brief metni" --tur deneme -k 3 --tam
```

Betik, aynı türden ve içerik sözcükleriyle en çok örtüşen k metni verir. Bunlarla
birlikte şu **ses paketi** kurulur ve yazma/düzeltme bağlamına konur:

```
## Ses paketi
### Yazar özellikleri (voice/profil.md — otomatik + elle notlar)
- Cümle: ortalama 9,8 kelime, CV 0,62; %10-%90 aralığı 3–19
- Yüklem: -dı %41, -yor %22, ad cümlesi %15; -maktadır %0
- Hitap: sen; zamir %1,2; "bir" %2,1
- Sevilen bağlaçlar: ama, sonra, çünkü. Kullanmadığı: öte yandan, bununla birlikte
- Açılış: sahne (%50), itiraf (%20)
- Kapanış: kısa cümle (%58)
- Elle notlar: ...

### Örnekler (ornek_sec.py, k=3)
[Örnek 1 — deneme, 2025-03-02, konu: ...]
<tam metin>
...

### Karşıt örnekler (voice/karsit/karsit.jsonl, aynı türden en yeni 2-4)
Reddedilen: "..."
Neden: "..."
Kabul edilen: "..."
```

Paket, kurallardan **önce** okunur; kural ile örnek çelişirse örnek kazanır (yazarın
gerçek metnidir), ama çelişki kullanıcıya söylenir.

## Ne yapılmaz

- Arşivin tamamı bağlama konmaz. k=3 üst sınırdır; 5+ örnek üslup taklidini
  iyileştirmiyor, bağlamı şişiriyor.
- Örnekler kopyalanmaz; cümle ödünç alınmaz. Örnek ritim ve sözcük dağarcığı için
  okunur.
- Profil, kullanıcının bugün söylediğinin önüne geçmez. Kullanıcı "bu sefer siz
  diye yaz" derse profil "sen" dese de siz yazılır.
- Profil elle düzenlenen bölümüyle birlikte okunur; otomatik bölüm tek başına
  yetmez.

## Profil güncelleme

Yeni onaylanan metin eklendiğinde `ses_ozellikleri.py` yeniden çalıştırılır;
otomatik bölüm yenilenir, "Elle notlar" korunur. `geri-bildirim-hafizasi` skill'i
her düzeltme oturumundan sonra `voice/karsit/` ve `voice/tercihler.md` dosyalarını
günceller; onaylanan son hal `voice/onaylanan/` altına da girer.

## Dosyalar

- `references/arsiv-yapisi.md` — klasör düzeni, frontmatter, ne onaylanmış sayılır
- `references/karsit-ornekler.md` — JSONL biçimi ve çiftlerin bağlamda sunumu
- `scripts/ses_ozellikleri.py` — arşivden profil (stdlib)
- `scripts/ornek_sec.py` — göreve en yakın k metin, TF-IDF kosinüs (stdlib)
- `scripts/trmetin.py` — ortak yardımcılar (turkce-editor ile aynı dosya)

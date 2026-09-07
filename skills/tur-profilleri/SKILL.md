---
name: tur-profilleri
description: Dört Türkçe yazı türünün kuralları — reel (kısa video metni), deneme, makale, blog. Her profil hedef uzunluk, cümle bandı, hitap (sen/siz/biz), açılış ve kapanış hareketleri, ritim ve yasakları verir. Kullanıcı bir tür adı andığında, "bu reel için uygun mu", "makale formatına sok", "türün kurallarını uygula" dediğinde ya da turkce-taslak / turkce-editor bir tür profili istediğinde kullan. (Turkish genre profiles: reel script, essay, article, blog post.)
license: MIT
---

# Tür profilleri

Bir metnin "iyi" olması türüne bağlıdır. Reel'de mükemmel olan cümle makalede
gevşek, makalede iyi olan paragraf reel'de ölüdür. Bu skill dört türün kurallarını
tek biçimde tutar; `turkce-taslak` yazmadan, `turkce-editor` düzeltmeden önce
ilgili profili okur.

## Profiller

| Dosya | Tür | Tek cümleyle |
|---|---|---|
| `profiller/reel.md` | Reel / kısa video metni | Sesli okunan, 20-60 saniyelik, tek fikirli konuşma |
| `profiller/deneme.md` | Deneme | Birinci tekil, kişisel deneyimden genel bir soruya |
| `profiller/makale.md` | Makale | Kaynaklı iddia, açık yapı, üçüncü kişi ya da "biz" |
| `profiller/blog.md` | Blog yazısı | Deneme ile makale arası; okurla konuşan, pratik |

## Nasıl kullanılır

1. Türü belirle. Kullanıcı söylemediyse sor. İpuçları: "video", "Instagram", "TikTok"
   → reel; "köşe", "kişisel", "anı" → deneme; "rapor", "analiz", "kaynaklı" → makale;
   "site", "Medium", "haber bülteni" → blog.
2. Profili oku. Her profilin **kontrol listesi** bölümü, tesliminden önce tek tek
   işaretlenir.
3. Sayısal hedefler (`metrik.py --tur <tür>`, `yapi.py --tur <tür>`) profildeki
   bantlarla aynıdır; betik uyarısı profil ihlalidir.
4. Kullanıcının `voice/profil.md` dosyası tür profiliyle çelişirse **kullanıcı
   kazanır**; profil varsayılandır, kullanıcı ölçüttür. Çelişkiyi söyle, sonra
   kullanıcıya uy.

## Profil biçimi

Her profil aynı başlıkları taşır:

- **Amaç** — okur bu metni neden okur/izler
- **Ölçüler** — kelime, cümle uzunluğu bandı, Ateşman, ritim (CV), paragraf
- **Hitap ve kişi** — sen / siz / biz / ben / üçüncü kişi
- **Açılış hareketleri** — 4-6 seçenek; hepsi somut
- **Gövde** — paragraf düzeni, geçişler, kanıt biçimi
- **Kapanış hareketleri** — 3-5 seçenek; özet yasak
- **Yasaklar** — bu türde olmaması gerekenler
- **Kontrol listesi** — teslim öncesi

## Kalibrasyon notu

Ölçüler ilk sürümde editör deneyimiyle konuldu; Faz 6 kalibrasyonunda
(`docs/yontem.md`) insan külliyatının yüzdelikleriyle güncellenir. Leipzig haber
külliyatı (30.000 cümle) için ölçülen taban: ortalama cümle 13,8 kelime, CV 0,47,
Ateşman 48,8. Makale bandı buna göre kurulmuştur.

# Araştırma dayanağı

Skill'lerdeki tasarım kararları şu bulgulara dayanır. Her madde, hangi karara
dayanak olduğunu söyler.

## Üslup taklidi örnekle öğrenilmiyor

**"Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit
Writing Styles of Everyday Authors"** — Findings of EMNLP 2025.

Az örnekle (few-shot) üslup taklidi blog ve forum yazılarında başarısız; örnek
sayısını artırmak sınırlı kazanç sağlıyor. Modeller yüzey özelliklerini (uzunluk,
noktalama) kısmen yakalıyor, örtük üslubu yakalayamıyor.

→ Ses adımı: "benim gibi yaz" + çok örnek yerine **seçim + açık özellik +
karşıt örnek**. `ornek_sec.py` k ≤ 3 ile sınırlı; profil özellikleri sözle
yazılır.

## Yazar özellikleri + karşıt örnek, düz RAG'den iyi

**Yazan, Verberne, Situmeang — ECIR 2025** (kişiselleştirilmiş metin üretimi).

Açıkça ifade edilmiş yazar özellikleri ve reddedilen/kabul edilen karşıt örnekler,
yalnızca benzer geçmiş metinleri bağlama koymaya (düz RAG) göre yaklaşık %15
göreli iyileşme veriyor.

→ `scripts/ses_ozellikleri.py` (özellikler), `voice/karsit/`
(karşıtlar), "hatırla" kipi (karşıtları biriktirme).

## Yalnızca göreve yarayan geçmiş metni getir

**PEARL** — Mysore ve ark., kişiselleştirilmiş yazma yardımcısı için geri getirme
eğitimi.

Tüm geçmişi değil, mevcut görev için yararlı olan geçmiş metinleri seçmek, üretim
kalitesini artırıyor; benzerlik tek başına yeterli ölçüt değil, tür ve görev
uyumu gerekiyor.

→ `ornek_sec.py`: aynı tür önceliği, içerik sözcükleri üzerinden TF-IDF, k küçük.

## "Türkçe" model adı doğal Türkçe demek değil

**TurBLiMP** (Türkçe minimal çiftler) ve **Cetvel** (Türkçe LLM değerlendirme):
Türkçe için eğitilmiş ya da Türkçe destekli modeller, sözdizimi ve söylem
düzeyinde İngilizce kalıplarını taşıyor; dilbilgisi doğruluğu ile doğallık ayrı
eksenler.

→ Modele güvenilmez, ölçülür: `kalip_tara.py`, `metrik.py`; TurBLiMP çiftleri
`corpus/turblimp/` altında nokta testi olarak kullanılabilir.

## Türkçeye çeviri metinlerinin izleri

Türkçe çeviri derlemi çalışmaları (çeviri Türkçesi ile özgün Türkçe karşılaştırmaları)
tutarlı biçimde şunları buluyor: "tarafından"lı edilgen, belirsiz "bir" fazlalığı,
açık özne zamiri, "-e sahip" ve "bir şekilde" kopyaları, hafif fiiller
(gerçekleştirmek, sağlamak), "ki" yan cümleleri, adlaştırma.

→ `references/ceviri-kokusu.md` ve `ceviri_kokusu.tsv` bu kategorilerle kurulmuştur.

## Okunabilirlik formülleri

- **Ateşman (1997)**: Flesch'in Türkçe uyarlaması; hece/kelime ve kelime/cümle.
- **Bezirci-Yılmaz (2010)**: çok heceli sözcükleri ağırlıklandıran, sınıf düzeyi
  veren ölçü; Türkçe için Ateşman'dan ayırt edici.

→ `metrik.py` ikisini de verir; tür bantları Ateşman ile ifade edilir.

## Makine metni ve ritim

İnsan yazısı ile LLM yazısı arasında en tutarlı yüzey farkı cümle uzunluğu
değişkenliğidir ("burstiness"); LLM metni daha tekdüzedir. Bu Türkçe için ayrıca
yüklem eki tekdüzeliği (-maktadır dizileri) olarak görünür.

→ `metrik.py` CV ve yüklem çeşitliliği; `references/ritim.md`.

## Kapsam dışı bırakılanlar ve nedeni

- **İnce ayar / DPO**: özgün belge öneriyor; bu depo yalnızca istem düzeyinde
  çalışır. Sebep: veri gizliliği (kişisel metinler), maliyet, taşınabilirlik
  (skill her modelde çalışmalı).
- **Sesli notlar**: metin dışı kaynak; ayrı bir hat.
- **"Dedektörü geçmek"**: hedef, doğal Türkçe; algılayıcıyı aldatmak değil. AI
  algılayıcıları ayrı bir sorundur ve çoğu Türkçede güvenilir değildir.

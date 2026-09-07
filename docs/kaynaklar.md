# Veri kaynakları ve hukuki durum

| Kaynak | Ne | Lisans | Depoda | Nasıl kullanılır |
|---|---|---|---|---|
| [Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download/Turkish) — `tur_news_2024_30K` | Haber cümleleri ve sözcük sıklığı | CC BY 4.0 | Sözcük listesi kırpılmış halde `skills/turkce-editor/data/siklik_yazili.tsv`; cümle dosyası değil | `tools/fetch_data.sh` indirir; atıf: Goldhahn, Eckart, Quasthoff, LREC 2012 |
| Leipzig `tur_wikipedia_2021_30K`, `tur_web_2019_30K` | Vikipedi ve web cümleleri | CC BY 4.0 | Hayır | `tools/fetch_data.sh --hepsi` ile `corpus/leipzig/`; kalibrasyon |
| [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords) — `2018/tr/tr_50k.txt` | OpenSubtitles konuşma dili sıklığı | CC BY-SA 4.0 | Kırpılmış: `siklik_konusma.tsv` (aynı lisansla) | `siklik.py --konusma` |
| Türkçe Vikipedi | Madde metinleri | CC BY-SA 4.0 | Hayır | Faz 6 insan külliyatı ve konu başlıkları; dökümden örnek alınır, depoya girmez |
| [TurBLiMP](https://github.com/ezgibasar/TurBLiMP) | Türkçe dilbilgisi minimal çiftleri | CC BY 4.0 | Hayır | Dilbilgisi nokta testleri; `corpus/turblimp/` altına klonlanır |
| Cetvel | Türkçe LLM değerlendirme seti | Açık (bkz. repo) | Hayır | Yalnızca referans; model seçimi için |
| Kendi ürettiğimiz LLM külliyatı | 4 tür × ~300 metin | Kendi üretimimiz | Hayır (`corpus/`, gitignore) | Faz 6; türetilen listeler depoya girer |
| `ai_kaliplari.tsv`, `ceviri_kokusu.tsv` | Elle derlenmiş kalıplar | MIT | Evet | — |

## Yalnızca elle sorgulanan kaynaklar

Toplu indirilemeyen ya da lisansı yeniden dağıtıma izin vermeyen derlemler.
Skill'ler bunları **kullanmış gibi yapmaz**; emin olunamayan bir kalıp için
kullanıcıya sorgu önerir.

| Kaynak | Erişim | Ne için |
|---|---|---|
| [TNC — Türkçe Ulusal Derlemi v3](https://www.tnc.org.tr) | Ücretsiz üyelik, web arayüzü, toplu indirme yok | Bir kalıbın gerçek sıklığı ve hangi türde geçtiği |
| [TS Corpus](https://tscorpus.com) | Ücretsiz üyelik, web sorgu | Aynı; daha büyük, daha az dengeli |
| Türkçe Söylem Bankası (TDB) | Akademik lisans, e-posta ile | Bağlaç ve söylem ilişkileri araştırması |
| METU Türkçe Derlemi | Akademik lisans | Yazılı Türkçe dengeli örneklem |
| Bilkent Turkish Writings | Yalnızca akademik | Öğrenci yazıları; ses profili için değil |

Örnek öneri cümlesi (editör bunu yazar): "'-e sahip olmak' kalıbının bu bağlamda
doğal olup olmadığından emin değilim; TNC'de `sahip` sorgusuyla tür dağılımına
bakabilirsin."

## Araçlar

| Araç | Lisans | Durum |
|---|---|---|
| [zeyrek](https://github.com/obulat/zeyrek) | MIT | İsteğe bağlı; `siklik.py --zeyrek` kuruluysa kullanır |
| [Zemberek-NLP](https://github.com/ahmetaa/zemberek-nlp) | Apache-2.0 (Java) | Belgelenen alternatif; gerekmez |
| Python 3.9+ stdlib | PSF | Tek zorunlu bağımlılık |

## Depoya girmeyenler

`.gitignore`: `voice/` (kişisel arşiv), `corpus/` (üretilen ve indirilen
külliyat), `tools/cache/` (ham indirmeler). Bu üçü hiçbir koşulda commit edilmez;
kişisel metinler ve yeniden dağıtımı belirsiz veriler oradadır.

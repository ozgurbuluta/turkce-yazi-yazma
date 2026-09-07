# Veri lisansları

Bu klasördeki dosyalar, depo geneli için geçerli MIT lisansından ayrı olarak
aşağıdaki lisanslarla dağıtılır.

| Dosya | Kaynak | Lisans | Not |
|---|---|---|---|
| `siklik_konusma.tsv` | [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), `content/2018/tr/tr_50k.txt` (OpenSubtitles 2018) | CC BY-SA 4.0 | İlk 30.000 sözcük; yalnızca harf içeren biçimler, Türkçe küçük harfe çevrilmiş. Türev çalışma olduğundan bu dosya da CC BY-SA 4.0 ile dağıtılır. |
| `siklik_yazili.tsv` | [Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en/download/Turkish), `tur_news_2024_30K-words.txt` | CC BY 4.0 | Sıklığı ≥ 2 olan, yalnızca harf içeren biçimler; büyük/küçük harf birleştirilmiş; ilk 30.000. Atıf: D. Goldhahn, T. Eckart, U. Quasthoff, *Building Large Monolingual Dictionaries at the Leipzig Corpora Collection*, LREC 2012. |
| `ai_kaliplari.tsv`, `ceviri_kokusu.tsv`, `kisaltmalar.txt` | Bu depo | MIT | Elle derlenmiş; `tools/derive_patterns.py` ile üretilen adaylar elle onaylandıktan sonra eklenir. |

Listeleri yeniden üretmek için depo kökünde `tools/fetch_data.sh` çalıştırın.

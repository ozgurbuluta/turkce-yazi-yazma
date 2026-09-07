# turkce-yazi-yazma

Türkçe yazı için beş ajan skill'i: çeviri kokusu ve yapay zekâ kalıbı olmadan,
kendi sesinle, türün kurallarıyla yazmak ve düzeltmek.

| Skill | Ne yapar |
|---|---|
| [`turkce-editor`](skills/turkce-editor/SKILL.md) | Türkçe metni inceler, düzeltir, puanlar: çeviri kokusu, AI kalıbı, ritim, somutluk |
| [`turkce-taslak`](skills/turkce-taslak/SKILL.md) | Notlardan ya da İngilizce kaynaktan **kopyalamadan** taslak yazar (bilgi kartı) |
| [`tur-profilleri`](skills/tur-profilleri/SKILL.md) | Reel, deneme, makale, blog kuralları: uzunluk, hitap, açılış, kapanış, yasaklar |
| [`kisisel-ses`](skills/kisisel-ses/SKILL.md) | Onaylanmış metinlerden yazar profili, göreve en yakın örnekler, karşıt çiftler |
| [`geri-bildirim-hafizasi`](skills/geri-bildirim-hafizasi/SKILL.md) | Her düzeltme yorumunu kalıcı kurala çevirir; 3 kez görüleni editöre öğretir |

Skill metinleri Türkçedir. Betikler yalnızca Python standart kütüphanesiyle çalışır
(Claude.ai sandbox dahil); `zeyrek` isteğe bağlıdır.

## Neden

Türkçe LLM çıktısı çoğu zaman İngilizce düşünülüp Türkçe yazılmış gibi durur:
"tarafından" edilgenleri, "bir şekilde", "-e sahip", "yalnızca X değil aynı zamanda
Y", "günümüz dünyasında", "sonuç olarak". Bu depo o izleri sayar, adlandırır ve
düzeltir; ardından yazarın kendi sesini üç yoldan geri koyar: seçilmiş örnek, açık
özellik, karşıt çift (dayanak: [`docs/arastirma.md`](docs/arastirma.md)).

## Hızlı deneme

```bash
git clone https://github.com/ozgurbuluta/turkce-yazi-yazma && cd turkce-yazi-yazma
python3 skills/turkce-editor/scripts/kalip_tara.py tests/ornekler/ceviri_kokulu.md
python3 skills/turkce-editor/scripts/metrik.py tests/ornekler/dogal.md --tur deneme
python3 -m unittest discover tests
```

## Kurulum

### Claude Code

Depoyu klonla; Claude Code `skills/*/SKILL.md` dosyalarını proje skill'i olarak
görür. Ya da tek komut:

```bash
npx skills add ozgurbuluta/turkce-yazi-yazma
```

### Cursor / Codex / diğer ajanlar

`skills/` klasörünü projene kopyala ya da bağla; [`AGENTS.md`](AGENTS.md) ajanın
hangi skill'i ne zaman okuyacağını anlatır. Skill'ler markdown + Python olduğu için
herhangi bir ajan dosyaları okuyup betikleri çalıştırabilir.

### Claude.ai (Skills)

Her skill klasörü kendi başına çalışır. Klasörü zip'le, Claude.ai → Ayarlar →
Skills → yükle:

```bash
cd skills && zip -r turkce-editor.zip turkce-editor
```

`turkce-editor` zip'i ~1 MB (sıklık listeleri dahil). Diğerleri küçüktür.

## Kişisel ses arşivi

```bash
cp -r voice.example voice          # gitignore'da; asla paylaşılmaz
# kendi onaylanmış metinlerini voice/onaylanan/<tür>/ altına koy
python3 skills/kisisel-ses/scripts/ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
```

Ayrıntı: [`voice.example/README.md`](voice.example/README.md).

## Veri

Sıklık listeleri Leipzig Corpora (CC BY 4.0) ve hermitdave/FrequencyWords
(CC BY-SA 4.0) kaynaklıdır; `tools/fetch_data.sh` ile yeniden üretilir. Kalıp
listeleri elle tohumlanmıştır; veriden türetme yöntemi
[`docs/yontem.md`](docs/yontem.md), hukuki tablo
[`docs/kaynaklar.md`](docs/kaynaklar.md).

## Lisans

Kod ve düzyazı MIT. Veri dosyaları kendi lisanslarıyla:
[`skills/turkce-editor/data/LICENSES.md`](skills/turkce-editor/data/LICENSES.md).

---

## English summary

Five agent skills for writing and editing **Turkish** without translationese or
LLM clichés, in the author's own voice, by genre. `turkce-editor` scans a draft
for translation smell (by-passives, calqued "bir", light verbs, "ki"-clauses),
AI patterns, flat rhythm and empty claims, then rewrites and scores it.
`turkce-taslak` drafts from notes or from an English source via a "fact card"
workflow that prevents sentence-by-sentence mirroring (checked by
`kaynak_hizala.py`). `tur-profilleri` holds rules for reels, essays, articles
and blog posts. `kisisel-ses` builds an author profile from approved texts and
selects the 2-3 most relevant examples plus rejected/accepted contrast pairs
(selection + explicit features + contrast, not "write like me" with many
samples). `geri-bildirim-hafizasi` turns every editing comment into a durable
rule. Skill bodies are in Turkish; scripts are stdlib-only Python. Install with
`npx skills add ozgurbuluta/turkce-yazi-yazma`, or zip any `skills/<name>/` folder
for Claude.ai.

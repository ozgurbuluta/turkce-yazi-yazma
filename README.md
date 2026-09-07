# Daha iyi Türkçe yazı yazma

Yapay zeka Türkçe yazınca çoğu zaman İngilizce düşünüp Türkçe yazar: "önemli bir rol
oynamaktadır", "bir şekilde", "tarafından", "yalnızca X değil aynı zamanda Y",
"sonuç olarak". Bu depo, Claude Code, Cursor, Codex ya da Claude.ai içinde çalışan
beş skill ile o metni Türkçe düşünülmüş, somut, ritimli ve senin sesinle yazılmış
bir metne çevirir.

Skill'ler Türkçedir. Betikler yalnızca Python standart kütüphanesi ister; ek kurulum
yok.

## İyi metin neye benzer

Skill'lerin hepsi aynı ölçüte hizmet eder. Bir Türkçe metin şu dört şeyi sağlıyorsa
iyidir:

1. **Türkçe düşünülmüş.** Özne düşer, fiil sonda, "bir" yalnızca sayarken. "Rapor
   bakanlık tarafından hazırlandı" değil, "Raporu bakanlık hazırladı". "Yüksek hıza
   sahip" değil, "hızlı". "Etkili bir şekilde" değil, "iyi".
2. **Somut.** Her paragrafta gözle görülür bir şey var: sayı, ad, yer, olay.
   "Önemli bir rol oynar" yerine ne yaptığı yazılı. "Araştırmalar gösteriyor" yerine
   hangi araştırma, kaç kişi, ne zaman.
3. **Ritimli.** Uzun cümlenin yanında iki kelimelik cümle. Paragraflar aynı boyda
   değil. Cümleler üst üste "-maktadır" ile bitmiyor. Özet paragrafı yok; sonuç ya
   yeni bir şey söylüyor ya kesiyor.
4. **Türüne ve yazarına uygun.** Reel sesli okunur, başlık ve madde imi olmaz.
   Deneme "ben" der. Makale her sayıya kaynak verir. Blog okurla konuşur. Hepsinde
   yazarın kendi cümle boyu, kendi bağlaçları, kendi hitabı.

Bir de yazım tercihi: düzeltme işareti (â, î, û) kullanılmaz. "Zeka", "hala",
"kağıt", "imkan".


## Beş skill

| Skill | Ne yapar | Nasıl çağrılır |
|---|---|---|
| [`turkce-editor`](skills/turkce-editor/SKILL.md) | Metni inceler, düzeltir, 0-100 puanlar: çeviri kokusu, AI kalıbı, ritim, somutluk, tür ve ses uyumu | Bir Türkçe metin verip "incele", "düzelt" ya da "puanla" de; kendiliğinden de devreye girer |
| [`turkce-taslak`](skills/turkce-taslak/SKILL.md) | Notlardan ya da İngilizce kaynaktan taslak yazar; kaynağı çevirmez, önce bilgi kartı doldurur | "Şu notlardan bir blog yazısı yaz", "bu İngilizce yazıdan Türkçe deneme çıkar" |
| [`tur-profilleri`](skills/tur-profilleri/SKILL.md) | Reel, deneme, makale, blog kuralları: uzunluk, hitap, açılış, kapanış, yasaklar | Tür adını söylemen yeter: "reel için" |
| [`kisisel-ses`](skills/kisisel-ses/SKILL.md) | Onaylanmış metinlerinden ses profili çıkarır; her göreve en yakın 2-3 örneği seçer | "Ses arşivimi kur", "benim sesimle yaz" |
| [`geri-bildirim-hafizasi`](skills/geri-bildirim-hafizasi/SKILL.md) | Her düzeltme yorumunu kalıcı kurala çevirir; 3 kez tekrar edeni editöre öğretir | Düzeltme bitince kendiliğinden; ya da "bunu hatırla", "bir daha yapma" |

## Kullanım: beş adımda

### 1. Kur

**Claude Code** (en kolay yol): depoyu klonla ve içinde aç.

```bash
git clone https://github.com/ozgurbuluta/turkce-yazi-yazma
cd turkce-yazi-yazma
claude
```

Claude Code `skills/` altındaki beş skill'i görür. Başka bir projede kullanmak
istersen tek komut:

```bash
npx skills add ozgurbuluta/turkce-yazi-yazma
```

**Claude.ai**: her skill klasörü kendi başına çalışır. Klasörü zip'le, Claude.ai →
Ayarlar → Skills → yükle. `turkce-editor` zip'i yaklaşık 1 MB, diğerleri küçük.

```bash
cd skills && zip -r turkce-editor.zip turkce-editor
```

**Cursor, Codex, diğer ajanlar**: `skills/` klasörünü projene kopyala ya da bağla.
[`AGENTS.md`](AGENTS.md) ajanın hangi skill'i ne zaman okuyacağını anlatır; skill'ler
markdown ve Python olduğu için her ajan okuyup çalıştırabilir.

### 2. Bir metni düzelt

Metni yapıştır ya da dosya adını ver:

```
Şu yazıyı düzelt, deneme: taslak.md
```

Editör dört betiği çalıştırır, bulguları cümle cümle gösterir (cümle → neden →
öneri), metni yeniden yazar, önce/sonra puanı ve **iddia listesini** verir: kaldırdığı
ya da değiştirdiği her sayı, ad ve iddia listede olur. Yalnızca rapor istiyorsan
"incele", yalnızca puan istiyorsan "puanla" de.

### 3. Sıfırdan yaz

```
Şu notlardan 60 saniyelik bir reel metni yaz: ...
```

ya da İngilizce bir kaynaktan:

```
Bu makaleden Türkçe bir blog yazısı çıkar, çevirme: <kaynak>
```

İkincisinde skill önce bir **bilgi kartı** doldurur (ne oldu, sayılar, kaynağın
iddiası, senin görüşün, Türkiye'deki okur için anlamı), sana gösterir, sonra
kaynağa bir daha bakmadan karttan yazar. `kaynak_hizala.py` taslağın kaynağın
paragraf sırasını kopyalayıp kopyalamadığını ve kaynakta olmayan sayı ekleyip
eklemediğini denetler.

### 4. Kendi sesini ekle

Skill'ler ses arşivi olmadan da çalışır; arşivle senin gibi yazar.

```bash
cp -r voice.example voice        # voice/ gitignore'dadır, paylaşılmaz
# onayladığın metinleri voice/onaylanan/<tür>/ altına koy (frontmatter ile)
python3 skills/kisisel-ses/scripts/ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
```

En az beş metin gerekir. Profil, cümle boyu dağılımından sevdiğin bağlaçlara kadar
ölçülmüş özellikler içerir; `voice/profil.md` içindeki "Elle notlar" bölümüne kendi
yasaklarını ve hitap tercihini yazarsın. Her görevde skill arşivden yalnızca en
yakın 2-3 metni bağlama alır; araştırma daha fazlasının işe yaramadığını gösteriyor
([`docs/arastirma.md`](docs/arastirma.md)).

### 5. Düzeltmelerinden öğrensin

Bir düzeltmeyi beğenmediysen söyle: "bu cümle çeviri gibi", "meslek adı verme, işi
yaz". Oturum bitince `geri-bildirim-hafizasi` her yorumu reddedilen/yorum/onaylanan
üçlüsü olarak `voice/karsit/` altına yazar, bir kural damıtıp `voice/tercihler.md`'ye
ekler. Aynı kural üç kez görülünce editörün her oturum başında okuduğu kontrol
listesine çıkar; bir daha o hatayı yapmaz.

## Betikleri tek başına kullanmak

Skill olmadan da çalışırlar; hepsi `--json` ve `--help` alır.

```bash
python3 skills/turkce-editor/scripts/kalip_tara.py yazi.md            # AI kalıbı + çeviri kokusu, cümle cümle, 0-100
python3 skills/turkce-editor/scripts/metrik.py yazi.md --tur blog     # okunabilirlik, ritim, yüklem, çeviri izleri
python3 skills/turkce-editor/scripts/siklik.py yazi.md --konusma      # tanınmayan / nadir / aşırı tekrar eden sözcük
python3 skills/turkce-editor/scripts/yapi.py yazi.md --tur reel       # üçlü liste, "değil" karşıtlığı, markdown, tuhaf karakter
python3 skills/turkce-taslak/scripts/kaynak_hizala.py kaynak.md taslak.md
```

Denemek için depodaki örnekler: `tests/ornekler/ceviri_kokulu.md` 100/100 iz puanı
alır, `tests/ornekler/dogal.md` 13/100.

## Veri ve yöntem

- Sıklık listeleri: Leipzig Corpora `tur_news_2024_30K` (CC BY 4.0) ve OpenSubtitles
  2018 Türkçe (hermitdave/FrequencyWords, CC BY-SA 4.0). `tools/fetch_data.sh` ile
  yeniden üretilir. Lisanslar: [`skills/turkce-editor/data/LICENSES.md`](skills/turkce-editor/data/LICENSES.md),
  [`docs/kaynaklar.md`](docs/kaynaklar.md).
- Kalıp listeleri elle derlendi (111 AI kalıbı, 70 çeviri kokusu). Veriden türetme
  yöntemi ve ölçülen eşikler: [`docs/yontem.md`](docs/yontem.md).
- Tasarım kararlarının dayanağı: [`docs/arastirma.md`](docs/arastirma.md).
- Testler: `python3 -m unittest discover tests`.

## Lisans

Kod ve düzyazı MIT. Veri dosyaları kendi lisanslarıyla dağıtılır.

---

## English summary

Five agent skills for writing and editing **Turkish** without translationese or
LLM clichés, in the author's own voice, by genre. A good text here means: thought
in Turkish (dropped subjects, verb-final, no calqued "bir" or by-passives),
concrete (numbers, names, events instead of "plays an important role"), rhythmic
(varied sentence and paragraph length, no summary paragraph) and true to its genre
and author. `turkce-editor` scans a draft, reports each finding as
sentence → reason → fix, rewrites, scores before/after and lists every claim it
removed. `turkce-taslak` drafts from notes or from an English source through a
fact-card step that prevents sentence-by-sentence mirroring. `tur-profilleri`
holds rules for reels, essays, articles and blog posts. `kisisel-ses` builds an
author profile from approved texts and selects the 2-3 most relevant examples plus
rejected/accepted contrast pairs. `geri-bildirim-hafizasi` turns each editing
comment into a durable rule. Install: clone and open in Claude Code, or
`npx skills add ozgurbuluta/turkce-yazi-yazma`, or zip any `skills/<name>/` folder
for Claude.ai. Scripts are stdlib-only Python.

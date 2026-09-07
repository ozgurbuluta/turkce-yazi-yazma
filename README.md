# Daha iyi Türkçe yazı yazma

Yapay zeka Türkçe yazınca çoğu zaman İngilizce düşünüp Türkçe yazar: "önemli bir rol
oynamaktadır", "bir şekilde", "tarafından", "yalnızca X değil aynı zamanda Y",
"sonuç olarak". `turkce-yazi`, o metni Türkçe düşünülmüş, somut, ritimli ve senin
sesinle yazılmış bir metne çeviren tek bir skill'dir. Claude.ai, Cowork, Claude Code
ve (Custom GPT olarak) ChatGPT'de çalışır.

## Kur

**Claude.ai ve Cowork** (bir dosya, bir yükleme):

1. [Releases](https://github.com/ozgurbuluta/turkce-yazi-yazma/releases) sayfasından
   `turkce-yazi.zip` indir.
2. Claude.ai → Ayarlar → Capabilities → Skills → zip'i yükle. Cowork aynı listeyi
   kullanır.
3. Yeni sohbette Türkçe bir metin yapıştırıp "düzelt" de.

**Claude Code**:

```bash
npx skills add ozgurbuluta/turkce-yazi-yazma
```

ya da depoyu klonlayıp içinde `claude` aç; `/turkce-yazi` ile de çağrılır.

**ChatGPT** (Custom GPT): `python3 tools/paketle.py` çalıştır, `dist/chatgpt/NASIL.md`
adımlarını izle: `instructions.md` talimatlara, `knowledge/` bilgi dosyalarına,
`scripts/` Code Interpreter için.

## Kullan

| Ne dersin | Ne olur |
|---|---|
| `Şu metni düzelt, deneme: ...` | Metin yeniden yazılır; 3-5 maddelik değişiklik özeti, kaldırılan iddiaların listesi, tek satır puan |
| `İncele: ...` | Metne dokunulmaz; her bulgu cümle → neden → öneri olarak listelenir |
| `Puanla: ...` | 0-100 ve tek paragraf gerekçe |
| `Şu notlardan 45 saniyelik bir reel yaz: ...` | Tür kurallarıyla taslak, sonra düzeltme |
| `Bu İngilizce yazıdan Türkçe blog çıkar, çevirme: ...` | Önce bilgi kartı (sana gösterilir, görüşün sorulur), sonra kaynağa bakmadan yazım; aynalama ve uydurma denetimi |
| `Benim sesimle yaz` | `voice/` arşivin varsa profilin ve en yakın 2-3 metnin kullanılır |
| `Bunu hatırla` / `bir daha yapma` | Yorumun kalıcı kurala çevrilir (aşağıda) |

Tür (reel, deneme, makale, blog) söylemezsen sorar.

## İyi metin neye benzer

Skill'in tek ölçütü: bu cümleyi Türkçe düşünen biri böyle mi kurardı? Dört şeye bakar:

1. **Türkçe düşünülmüş.** Özne düşer, fiil sonda, "bir" yalnızca sayarken. "Rapor
   bakanlık tarafından hazırlandı" değil, "Raporu bakanlık hazırladı". "Etkili bir
   şekilde" değil, "iyi".
2. **Somut.** Her paragrafta gözle görülür bir şey: sayı, ad, yer, olay. "Önemli bir
   rol oynar" yerine ne yaptığı.
3. **Ritimli, ama kesik değil.** Cümleler ulaçla bağlanır (-ip, -ince, -diği için);
   kısa cümle seyrek gelir ve bir şeyi vurur. "Aldı. Bilmiyordu. Öğrendim." de
   İngilizce kopyasıdır, "-maktadır. -maktadır." kadar.
4. **Türüne ve yazarına uygun.** Reel sesli okunur, başlık ve madde imi olmaz.
   Deneme "ben" der. Makale her sayıya kaynak verir. Blog okurla konuşur.

Yazım tercihi: düzeltme işareti (â, î, û) kullanılmaz; zeka, hala, kağıt.

Yanıt hep metin hakkındadır: hangi cümle, neden, nasıl. Betik adı, puan tablosu,
kategori kodu görmezsin; sayı istersen tek satırda alırsın.

## Kendi sesin

Arşiv olmadan da çalışır; arşivle senin gibi yazar.

```bash
cp -r voice.example voice        # voice/ gitignore'dadır, paylaşılmaz
# onayladığın 5+ metni voice/onaylanan/<tür>/ altına koy (frontmatter örneği voice.example'da)
python3 skills/turkce-yazi/scripts/ses_ozellikleri.py --arsiv voice/onaylanan --cikti voice/profil.md
```

Profil, cümle boyu dağılımından sevdiğin bağlaçlara kadar ölçülmüş özellikler
içerir; "Elle notlar" bölümüne kendi yasaklarını yazarsın. Her görevde arşivden
yalnızca en yakın 2-3 metin bağlama alınır; daha fazlası işe yaramıyor
([`docs/arastirma.md`](docs/arastirma.md)).

**"Bunu hatırla"** nerede nasıl çalışır:

- Claude Code ve klasör verilmiş Cowork: kural `voice/tercihler.md`'ye yazılır, üç
  kez görülünce editörün her oturum başında okuduğu listeye çıkar.
- Claude.ai, ChatGPT: dosya kalıcı değildir; skill kuralı hazır blok olarak basar,
  sen Projenin talimatlarına (ya da GPT'nin Instructions'ına) yapıştırırsın.

## Betikleri tek başına kullanmak

```bash
python3 skills/turkce-yazi/scripts/kalip_tara.py yazi.md          # AI kalıbı + çeviri kokusu, cümle cümle, 0-100
python3 skills/turkce-yazi/scripts/metrik.py yazi.md --tur blog   # okunabilirlik, ritim, yüklem, çeviri izleri
python3 skills/turkce-yazi/scripts/yapi.py yazi.md --tur reel     # üçlü liste, kısa cümle dizisi, markdown
python3 skills/turkce-yazi/scripts/kaynak_hizala.py kaynak.md taslak.md
```

Örnekler: `tests/ornekler/ceviri_kokulu.md` 100/100 iz puanı alır, `dogal.md` 13/100,
`parcali.md` kesik cümle uyarısı verir.

## Veri, yöntem, lisans

Sıklık listeleri Leipzig Corpora (CC BY 4.0) ve OpenSubtitles/hermitdave
(CC BY-SA 4.0); kalıp listeleri elle derlendi. Yöntem [`docs/yontem.md`](docs/yontem.md),
kaynaklar [`docs/kaynaklar.md`](docs/kaynaklar.md), dayanak
[`docs/arastirma.md`](docs/arastirma.md). Testler: `python3 -m unittest discover tests`.
Kod ve düzyazı MIT; veri dosyaları kendi lisanslarıyla.

---

## English summary

`turkce-yazi` is a single agent skill for writing and editing **Turkish** without
translationese or LLM clichés, in the author's own voice, by genre (reel, essay,
article, blog). It rewrites a draft and reports changes as sentence → reason → fix,
drafts from notes or from an English source through a fact-card step that prevents
sentence-by-sentence mirroring, and turns editing feedback into durable rules.
Install: download `turkce-yazi.zip` from Releases and upload it under Claude.ai
Settings → Skills (Cowork uses the same list); `npx skills add
ozgurbuluta/turkce-yazi-yazma` for Claude Code; `tools/paketle.py` builds a Custom
GPT bundle for ChatGPT. Scripts are stdlib-only Python.

# Daha iyi Türkçe yazı yazma

Yapay zeka Türkçe yazınca çoğu zaman İngilizce düşünüp Türkçe'ye tercüme ediyor. `turkce-yazi`, o metni
Türkçe düşünülmüş, somut, akıcı ve senin sesinle yazılmış bir metne çeviren bir
skill olması için tasarlandı. Claude.ai, Cowork, Claude Code ve ChatGPT'de çalışır.

## Kur

**Claude.ai ve Cowork**

1. [Releases](https://github.com/ozgurbuluta/turkce-yazi-yazma/releases) sayfasından
   `turkce-yazi.zip` dosyasını indir.
2. Claude.ai'de Ayarlar → Capabilities → Skills bölümüne git, zip'i yükle. Cowork
   aynı listeyi görür; ayrıca bir şey yapman gerekmiyor.
3. Yeni bir sohbet aç, Türkçe bir metin yapıştır, "düzelt" de.

**Claude Code**

Terminalde şunu çalıştır:

```bash
npx skills add ozgurbuluta/turkce-yazi-yazma
```

Sonra Türkçe metin yapıştırıp "düzelt" demen yeterli. İstersen `/turkce-yazi` yazarak
da başlatabilirsin.

**ChatGPT**

ChatGPT'de skill yok; onun yerine kendi GPT'ni kurman gerek:

1. Bu repoyu indir (yeşil "Code" düğmesi → Download ZIP), aç.
2. Terminalde `python3 tools/paketle.py` çalıştır. `dist/chatgpt/` adında bir klasör
   oluşacak.
3. ChatGPT'de "Create a GPT" de. `instructions.md` dosyasının içini Instructions
   kutusuna yapıştır, `knowledge/` klasöründeki dosyaları Knowledge'a yükle.

## Kullanım

| Ne dersin | Ne olur |
|---|---|
| `Şu metni düzelt, deneme: ...` | Metin yeniden yazılır; neyi neden değiştirdiğini kısaca söyler, sildiği iddiaları listeler |
| `İncele: ...` | Metne dokunmaz; her sorunu cümle → neden → öneri olarak gösterir |
| `Puanla: ...` | 0-100 puan ve tek paragraf gerekçe |
| `Şu notlardan bir blog yazısı yaz: ...` | Notlardan taslak yazar, sonra kendi düzeltir |
| `Bu İngilizce yazıdan Türkçe makale çıkar, çevirme: ...` | Önce kaynaktan bir bilgi kartı çıkarır, senin görüşünü sorar, sonra kaynağa bakmadan yazar |
| `Benim sesimle yaz` | Kendi yazılarından çıkarılmış profilini kullanır (aşağıda) |
| `Bunu hatırla` | O yorumu kalıcı kurala çevirir; bir daha aynı hatayı yapmaz |

Tür (deneme, makale, blog) söylemezsen sorar.

## İyi metin neye benzer

Tek ölçüt: bu cümleyi Türkçe düşünen biri böyle mi kurardı? Dört şeye bakarak buna karar veriyor:

1. **Türkçe düşünülmüş.** "Rapor bakanlık tarafından hazırlandı" değil, "Raporu
   bakanlık hazırladı". "Etkili bir şekilde" değil, "iyi".
2. **Somut.** "Önemli bir rol oynar" yerine ne yaptığı. Sayı, ad, yer, olay.
3. **Akıcı, ama kesik değil.** Cümleler birbirine bağlanır (-ip, -ince, -diği için);
   kısa cümle seyrek gelir ve bir şeyi vurur. "Aldı. Bilmiyordu. Öğrendim." de
   yapay durur, "-maktadır. -maktadır." kadar.
4. **Türüne ve yazarına uygun.** Deneme "ben" der. Makale her sayıya kaynak verir.
   Blog okurla konuşur.

Bir de: düzeltme işareti (â, î, û) kullanmaz; zeka, hala, kağıt.

## Kendi sesin

Skill, arşiv olmadan da çalışır; ama beğendiğin kendi yazılarını verirsen senin
sesini anlar ve o şekilde yazmaya başlar.

1. Depodaki `voice.example` klasörünü `voice` adıyla kopyala.
2. İçindeki örnek yazıları sil, kendi yazılarından en az beşini
   `voice/onaylanan/deneme/` (ya da `makale/`, `blog/`) altına koy. Her dosyanın
   başına örnekteki gibi tür ve tarih yaz.
3. Claude'a "ses arşivimi kur" de; yazılarını okuyup profilini çıkarsın.

Bundan sonra her görevde arşivinden konuya en yakın iki üç yazıyı örnek alır.
"Bunu hatırla" dediğin kurallar da `voice/tercihler.md` dosyasında birikir.
Claude.ai ve ChatGPT'de dosya kalıcı olmadığı için kuralı sana hazır verir, sen
Projenin talimatlarına yapıştırırsın.

## Geliştiriciler için

Skill'in içindeki Python araçları (kalıp tarama, ritim ölçümü, kaynak hizalama)
tek başına da çalışır; nasıl olduğu [AGENTS.md](AGENTS.md) ve
[docs/](docs/) içinde. Veri kaynakları ve lisanslar
[docs/kaynaklar.md](docs/kaynaklar.md).

---

## English summary

`turkce-yazi` is a single agent skill for writing and editing **Turkish** without
translationese or LLM clichés, in the author's own voice, by genre (essay, article,
blog). Install: download `turkce-yazi.zip` from Releases and upload it under
Claude.ai Settings → Skills (Cowork shares the list); `npx skills add
ozgurbuluta/turkce-yazi-yazma` for Claude Code; `tools/paketle.py` builds a Custom
GPT bundle for ChatGPT.

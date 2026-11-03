> **Uyarı:** Bu içerik, SCÜ Şarkışla UBYO Doğal Dil İşleme dersi kapsamında tamamen eğitim amaçlı çevrilmiş ve derlenmiştir. Orijinal dokümantasyon kaynakları (Hugging Face LLM Course, Transformers, Datasets, Tokenizers kütüphaneleri) kendi orijinal lisanslarına (Apache 2.0, MIT, CC-BY 4.0) tabidir. Bu çalışmanın hiçbir ticari amacı yoktur.

# Bölüm 4: Bölüm Sonu Değerlendirme Testi (Quiz)

**Takım:** NLP04 (2026 Güz)  
**Kaynak:** [Hugging Face LLM Course — Chapter 4 Quiz](https://huggingface.co/learn/llm-course/chapter4/6)  
**Konu:** Model ve Tokenizer'ların Paylaşılması (Sharing Models and Tokenizers)

---

Bu test, Hugging Face 4. Bölüm boyunca öğrendiğiniz temel kavramları (Hugging Face Hub mimarisi, `push_to_hub` API'si, model kartları ve `huggingface_hub` araçları) pekiştirmek için hazırlanmıştır.

---

### 1. Hub'daki modeller ne ile sınırlıdır?

- [ ] **A)** Sadece 🤗 Transformers kütüphanesindeki modellerle.
- [ ] **B)** 🤗 Transformers ile benzer bir arayüze sahip tüm modellerle.
- [x] **C)** Hiçbir sınırlama yoktur. ✅
- [ ] **D)** Yalnızca Doğal Dil İşleme (NLP) ile ilişkili olan modellerle.

> **📝 Açıklama:**  
> **Doğru Cevap: C.** Hub'a model yüklerken mimari, kütüphane veya alan sınırlaması yoktur. Hub; NLP için Flair ve AllenNLP, ses için Asteroid ve Pyannote, görüntüleme için timm gibi birçok farklı kütüphaneden modelleri barındırır.
> 
> * **A yanlış:** Transformers modelleri desteklenir fakat tek seçenek değildir.
> * **B yanlış:** Herhangi bir arayüz şartı aranmaz.
> * **D yanlış:** Uygulama alanına (NLP, CV, Ses, RL) ilişkin bir kısıtlama yoktur.

---

### 2. Hub'daki modelleri nasıl yönetebilirsiniz?

- [ ] **A)** Bir GCP (Google Cloud Platform) hesabı aracılığıyla.
- [ ] **B)** Uçtan uca (peer-to-peer) dağıtım ağı aracılığıyla.
- [x] **C)** `git` ve `git-lfs` aracılığıyla. ✅

> **📝 Açıklama:**  
> **Doğru Cevap: C.** Hub üzerindeki her bir model deposu (repository) basit birer Git deposudur. Model ağırlıkları gibi büyük boyutlu dosyalar için arka planda `git-lfs` (Large File Storage) altyapısı kullanılır.
> 
> * **A ve B yanlış:** Hub yönetimi bulut sağlayıcı hesaplarıyla veya P2P ağlarla değil, Git protokolü üzerinden yürütülür.

---

### 3. Hugging Face Hub web arayüzünü kullanarak aşağıdakilerden hangilerini yapabilirsiniz? *(Çoktan Seçmeli)*

- [ ] **A)** Mevcut bir depoyu çatallamak (fork).
- [x] **B)** Yeni bir model deposu oluşturmak. ✅
- [x] **C)** Dosyaları yönetmek ve doğrudan tarayıcıda düzenlemek. ✅
- [x] **D)** Dosya yüklemek (drag-and-drop / upload). ✅
- [x] **E)** Sürümler arasındaki farkları (diffs) görüntülemek. ✅

> **📝 Açıklama:**  
> **Doğru Cevaplar: B, C, D ve E.** Hugging Face web arayüzü; depo oluşturma, dosya yükleme, web editörü ile düzenleme ve Git commit diff'lerini inceleme özelliklerinin tamamını destekler.
> 
> * **A yanlış:** Hugging Face Hub arayüzünde GitHub'daki gibi bir "Fork" butonu bulunmaz; modeller doğrudan klonlanıp yeni repo olarak paylaşılır.

---

### 4. Model kartı (Model Card / README.md) nedir?

- [ ] **A)** Modelin kaba bir taslağıdır; bu yüzden model ve tokenizer dosyalarından çok daha önemsizdir.
- [x] **B)** Tekrarlanabilirlik (reproducibility), yeniden kullanılabilirlik (reusability) ve adaleti (fairness) sağlamanın temel yoludur. ✅
- [ ] **C)** Model hakkında bilgi almak için terminalden çalıştırılan bir Python betiğidir (.py).

> **📝 Açıklama:**  
> **Doğru Cevap: B.** Model kartı, kullanıcıların modelin nasıl eğitildiğini, hangi veri kümelerini kullandığını, sınırlarını ve önyargılarını anlamasını sağlayan en kritik dokümandır. Eksik veya tanımsız bir model kartı modelin güvenilirliğini ve kullanılabilirliğini ciddi ölçüde düşürür.
> 
> * **A yanlış:** Model kartı modelin kendisi kadar önemlidir.
> * **C yanlış:** Model kartları çalıştırılabilir Python dosyası değil, biçimlendirilmiş Markdown (`README.md`) dosyalarıdır.

---

### 5. 🤗 Transformers kütüphanesindeki hangi nesneler `push_to_hub()` metoduyla doğrudan Hub'da paylaşılabilir? *(Çoktan Seçmeli)*

- [x] **A)** Bir Tokenizer ✅
- [x] **B)** Bir Model Konfigürasyonu (Configuration) ✅
- [x] **C)** Bir Model (`AutoModelFor...`) ✅
- [x] **D)** Bir `Trainer` (PyTorch) veya `PushToHubCallback` (Keras/TensorFlow) ✅

> **📝 Açıklama:**  
> **Doğru Cevap: Hepsi (A, B, C, D).** 🤗 Transformers kütüphanesinde tokenizer'lar, model sınıfları, konfigürasyon nesneleri ve eğitim yöneticileri (`Trainer` / `PushToHubCallback`) doğrudan `push_to_hub()` metoduna sahiptir. Bu metot çağrıldığında ilgili tüm dosyalar (ağırlıklar, kelime dağarcığı, hiperparametreler ve model kartı taslağı) otomatik olarak repoya gönderilir.

---

### 6. `push_to_hub()` metodunu veya CLI araçlarını kullanırken yapılması gereken İLK adım nedir?

- [ ] **A)** Hugging Face web sitesinde tarayıcıdan oturum açmak.
- [x] **B)** Terminalde `huggingface-cli login` komutunu çalıştırmak. ✅
- [x] **C)** Jupyter/Colab notebook ortamında `notebook_login()` fonksiyonunu çalıştırmak. ✅

> **📝 Açıklama:**  
> **Doğru Cevap: B ve C.** Yerel ortamınızdan veya Colab'dan Hub'a dosya yazabilmek için kişisel erişim belirtecinizin (access token) kimlik doğrulamasından geçmesi ve önbelleğe (cache) alınması şarttır.
> 
> * Terminal kullanıyorsanız: `huggingface-cli login`
> * Notebook kullanıyorsanız: `notebook_login()` fonksiyonu kullanılır.
> * **A yetersizdir:** Tarayıcıda oturum açmak yerel terminalinize veya kodunuza erişim izni sağlamaz.

---

### 7. Elinizde eğitilmiş bir model ve tokenizer var — bunları Hub'a en kolay yoldan nasıl yüklersiniz?

- [x] **A)** Doğrudan model ve tokenizer üzerinde `.push_to_hub()` metodunu çağırarak. ✅
- [ ] **B)** Python kodunda bunları harici bir `huggingface_hub` sınıfı ile tek tek sarmalayarak (wrapping).
- [ ] **C)** Dosyaları diske kaydedip terminalden `transformers-cli upload-model` komutunu çalıştırarak.

> **📝 Açıklama:**  
> **Doğru Cevap: A.** `model.push_to_hub("model-adi")` ve `tokenizer.push_to_hub("model-adi")` çağırmak depoyu otomatik oluşturur ve tüm dosyaları tek seferde yükler.
> 
> * **B gereksizdir:** Transformers nesneleri zaten bu desteğe dahili olarak sahiptir, ek sarmalama gerekmez.
> * **C yanlış:** `transformers-cli upload-model` şeklinde bir komut mevcut değildir.

---

### 8. `Repository` sınıfı ile hangi Git işlemlerini doğrudan Python içerisinden yapabilirsiniz? *(Çoktan Seçmeli)*

- [x] **A)** Commit işlemi (`repo.git_commit()`) ✅
- [x] **B)** Pull işlemi (`repo.git_pull()`) ✅
- [x] **C)** Push işlemi (`repo.git_push()`) ✅
- [ ] **D)** Merge işlemi (`repo.git_merge()`)

> **📝 Açıklama:**  
> **Doğru Cevap: A, B ve C.** `huggingface_hub.Repository` sınıfı dosya ekleme (`git_add`), çekme (`git_pull`), değişiklik kaydetme (`git_commit`) ve gönderme (`git_push`) metotlarını sağlar.
> 
> * **D yanlış:** Çakışma çözme ve birleştirme (merge) karmaşıklığı nedeniyle `Repository` API'si üzerinden doğrudan merge işlemi desteklenmez.

---

# Bizim Sorularımız

Bu bölüm, Bölüm 4 konularını (AutoModel mimarisi, Git-LFS kısıtlamaları ve model kartı meta verileri) derinlemesine pekiştirmek için eklenmiş özgün değerlendirme sorularını içerir.

---

### 1. `AutoModel` Sınıflarının Temel Avantajı

Bir kontrol noktasını (checkpoint) doğrudan `CamembertForMaskedLM` gibi modele özgü bir sınıfla yüklemek yerine `AutoModelForMaskedLM` kullanmanın temel teknik gerekçesi nedir?

- [ ] **A)** Model ağırlıklarını sıkıştırarak RAM tüketimini azaltması.
- [x] **B)** Mimariden bağımsız (architecture-agnostic) olması ve checkpoint değiştiğinde kod değişikliği gerektirmemesi. ✅
- [ ] **C)** Modeli GPU olmadan sadece CPU üzerinde çalışmaya zorlaması.
- [ ] **D)** `pipeline()` fonksiyonuna ihtiyaç duymadan çıkarım yapabilen tek sınıf olması.

> **📝 Açıklama:**  
> **Doğru Cevap: B.** `Auto*` sınıfları mimariden bağımsızdır (architecture-agnostic). `config.json` dosyasını okuyarak doğru mimariyi (BERT, CamemBERT, RoBERTa vb.) arka planda otomatik yükler. Böylece başka bir modele geçerken kodun geri kalanı değiştirilmeden yalnızca checkpoint adının güncellenmesi yeterlidir.

---

### 2. Hub Dosya Yükleme Kısıtlamaları

`huggingface_hub` kütüphanesindeki `upload_file` fonksiyonu yerine Git-LFS kullanılmasını zorunlu kılan temel teknik kısıtlama nedir?

- [x] **A)** `upload_file` fonksiyonunun 5 GB'den büyük dosyaları desteklememesi. ✅
- [ ] **B)** `upload_file` yönteminin yalnızca metin (`.txt` / `.json`) dosyalarını yükleyebilmesi.
- [ ] **C)** `upload_file` ile yüklenen depoların özel (private) yapılamaması.
- [ ] **D)** `upload_file`'ın yalnızca PyTorch tensörlerini kabul etmesi.

> **📝 Açıklama:**  
> **Doğru Cevap: A.** `upload_file` HTTP POST istekleriyle çalışır ve yerel ortamda Git kurulumu gerektirmez; ancak 5 GB üzerindeki dosyaları işleyemez. Büyük model ağırlıkları (büyük `.bin` veya `.safetensors` dosyaları) için Git-LFS kullanımı zorunludur.

---

### 3. Model Kartı (README.md) ve Hub Filtreleri

Bir modelin Hugging Face Hub üzerinde dil/görev filtrelerinde doğru indekslenmesini ve web sayfasındaki canlı test aracının (Hosted Inference API) otomatik açılmasını sağlayan yapı hangisidir?

- [ ] **A)** `config.json` dosyasındaki model mimari parametreleri.
- [x] **B)** `README.md` (Model Kartı) dosyasının en başındaki YAML frontmatter meta veri bloğu. ✅
- [ ] **C)** Model ağırlık dosyasının uzantısı (`.safetensors` veya `.bin`).
- [ ] **D)** `tokenizer_config.json` dosyasındaki özel token haritaları.

> **📝 Açıklama:**  
> **Doğru Cevap: B.** Model kartının başındaki `---` ile ayrılan YAML meta verileri (`language: tr`, `pipeline_tag: text-classification` vb.), Hub arama filtrelerini ve tarayıcıdaki canlı çıkarım widget'ını doğrudan yönetir.


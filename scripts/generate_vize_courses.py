"""Generate source-attributed study courses from reviewed, original question banks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "data"


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def questions(rows, source):
    result = []
    for index, row in enumerate(rows, 1):
        prompt, answer, *wrong = row
        assert len(wrong) == 3 and len({answer, *wrong}) == 4
        choices = [answer, *wrong]
        shift = (index - 1) % 4
        choices = choices[shift:] + choices[:shift]
        result.append({
            "id": index, "question": prompt, "options": choices,
            "correct": choices.index(answer), "source": source
        })
    return result


def course(course_id, name, icon, color, description, units, notes, banks,
           practice=None):
    courses["courses"].append(dict(id=course_id, name=name, icon=icon,
                                   color=color, description=description))
    base = ROOT / course_id
    write(base / "units.json", {
        "courseId": course_id, "courseName": name,
        "specialModes": [{"id": "mixed", "name": "🎲 Karışık Quiz",
                          "description": "Tüm ünitelerden rastgele 20 soru", "icon": "🎲"},
                         {"id": "all", "name": "📚 Tüm Sorular",
                          "description": "Bütün soruları çöz", "icon": "📚"}],
        "units": [{"id": n, "name": title} for n, title in units],
        "extras": [{"id": "notes", "name": "📖 Ders Notları",
                    "description": "Kaynağa dayalı kısa özetler", "icon": "📖"}]
                  + ([{"id": "practice", "name": "✍️ Kısa Cevap",
                       "description": "Yaratıcı kısa cevaplı sorular", "icon": "✍️"}]
                     if practice else [])
    })
    write(base / "notes.json", {"sections": [
        {"icon": "📖", "title": title, "content": content}
        for title, content in notes
    ]})
    for (unit_id, title), bank in zip(units, banks):
        write(base / f"unit{unit_id}.json", {
            "unitId": unit_id, "unitName": title, "questions": bank
        })
    if practice:
        write(base / "practice.json", {"sections": [
            {"icon": "✍️", "title": title, "content": content}
            for title, content in practice
        ]})


courses = json.loads((ROOT / "courses.json").read_text(encoding="utf-8"))
new_ids = {"ibo_ai", "ik_vize", "mesut_nlp_vize"}
courses["courses"] = [x for x in courses["courses"] if x["id"] not in new_ids]

ai_units = [
    (1, "Python temelleri ve veri yapıları"),
    (2, "Python bilimsel ekosistemi"),
    (3, "NumPy, Pandas ve Matplotlib"),
    (4, "CSV ve veri yükleme"),
    (5, "Tanımlayıcı istatistikler"),
    (6, "Veri görselleştirme"),
    (7, "Veri ön işleme"),
    (8, "Özellik seçimi"),
    (9, "Yeniden örnekleme ve doğrulama"),
    (10, "Model değerlendirme metrikleri"),
    (11, "Sınıflandırma algoritmaları"),
    (12, "Regresyon algoritmaları"),
    (13, "Algoritmaları karşılaştırma"),
]
ai_notes = [
    ("1. Python ile makine öğrenmesine giriş", "Defter, Python ile makine öğrenmesini adım adım uygulayan bir çalışma kitabıdır. Temel akış: problemi belirle, veriyi incele, uygun modeli kur, ayrı veride değerlendir. Python'da değişkenler, koşullar, döngüler, listeler, demetler, sözlükler ve fonksiyonlar sonraki örneklerin temelidir."),
    ("2. Ekosistem", "Python genel amaçlı dildir; NumPy sayısal diziler, SciPy bilimsel hesaplama, Pandas tablo verisi, Matplotlib çizim, scikit-learn ise ön işleme, modelleme ve değerlendirme araçları sağlar. Paket sürümleri ve çalışma ortamı tekrarlanabilirliği etkiler."),
    ("3. Sayısal ve tablo verisi", "NumPy dizileri aynı tipte verileri verimli işler; dilimleme ve vektörel işlemler döngü ihtiyacını azaltır. Pandas Series tek boyutlu, DataFrame satır-sütun yapılıdır. Matplotlib çizgi, saçılım, sütun, histogram, kutu ve alan grafikleriyle örüntüleri gösterir."),
    ("4. CSV dosyaları", "CSV yüklerken başlık satırı, yorum satırı, ayraç, tırnaklama, eksik değer ve veri tipi kontrol edilir. Standart csv modülü, NumPy ve Pandas farklı ihtiyaçlara hizmet eder. Yanlış ayraç veya başlık yorumu sütunları bozabilir."),
    ("5. Tanımlayıcı istatistik", "İlk incelemede veri boyutu, türleri, ilk satırlar, merkez ve yayılım ölçüleri, sınıf dağılımı ve özellikler arası ilişkiler görülür. Dengesiz sınıflar yalnızca doğruluk oranına güvenmemeyi gerektirir. Korelasyon nedensellik göstermez."),
    ("6. Görselleştirme", "Histogram ve yoğunluk grafiği dağılımı, kutu grafiği aykırı değerleri, korelasyon matrisi doğrusal ilişkileri, saçılım matrisi iki değişkenli örüntüleri gösterir. Grafik seçimi soruya ve değişken tipine bağlıdır."),
    ("7. Veri dönüşümleri", "MinMaxScaler değerleri seçilen aralığa taşır; StandardScaler ortalamayı sıfıra, standart sapmayı bire yaklaştırır. Normalizer örnek vektörünün normunu ölçekler; Binarizer eşik üstünü 1 yapar. Dönüşüm yalnızca eğitim verisinde öğrenilip test verisine uygulanmalıdır."),
    ("8. Özellik seçimi", "Tek değişkenli seçim her özelliği hedefle ayrı değerlendirir. RFE modeli yineleyerek daha az yararlı özellikleri çıkarır. PCA yeni doğrusal bileşenler üretir; bu yüzden klasik anlamda özellik seçimi değil, boyut indirgemedir. Ağaç tabanlı önem değerleri modele bağlıdır."),
    ("9. Doğrulama", "Eğitim-test ayırımı son değerlendirme için ayrı veri bırakır. K-kat çapraz doğrulama performansın bölmelere göre değişimini gösterir; leave-one-out her gözlemi bir kez test eder. Rastgele tekrar bölme belirsizliği görmeye yarar. Veri sızıntısı ve dengesiz sınıf dağılımı gözetilir."),
    ("10. Performans ölçüleri", "Sınıflandırmada doğruluk, log loss, ROC-AUC, karmaşıklık matrisi ve precision/recall/F1 farklı soruları yanıtlar. Regresyonda MAE mutlak, MSE karesel hatayı ölçer; R² açıklanan varyansla ilişkilidir. Metrik iş hedefiyle seçilir."),
    ("11. Sınıflandırma", "Defter lojistik regresyon, LDA, k-en yakın komşu, Naive Bayes, karar ağacı ve destek vektör makinesini nokta kontrolüyle karşılaştırır. LR doğrusal karar sınırı kurar; k-NN yakınlıklara, ağaçlar bölme kurallarına, SVM marjine dayanır."),
    ("12. Regresyon", "Doğrusal regresyon sürekli hedef tahmin eder. Ridge L2, Lasso L1 cezası uygular; Elastic Net ikisini birleştirir. K-NN regresyon komşu değerleri, karar ağacı bölge ortalamaları, SVR marjin yaklaşımı kullanır."),
    ("13. Adil model karşılaştırması", "Modelleri aynı veri bölmeleri ve aynı değerlendirme metriğiyle karşılaştırmak gerekir. Çapraz doğrulama ortalaması ve dağılımı birlikte incelenir; tek koşudaki küçük fark kesin üstünlük kanıtı değildir. Defterin örneğinde LR ve LDA güçlü sonuç verir, ancak sonuç veri kümesine özgüdür."),
]
ai_rows = [
    [
        ("Python'da anahtar-değer eşleştirmesi hangi yapıyla tutulur?", "Sözlük", "Liste", "Demet", "Küme"),
        ("Değiştirilemeyen sıralı Python koleksiyonu hangisidir?", "Demet", "Liste", "Sözlük", "DataFrame"),
        ("Bir koşula göre farklı kod çalıştıran yapı hangisidir?", "if/else", "for", "import", "return"),
        ("Tekrarlanan işlemler için yeniden kullanılabilir kod bloğu nedir?", "Fonksiyon", "Değişken", "Paket sürümü", "Veri tipi"),
    ],
    [
        ("Tablo verisi için en uygun temel kütüphane hangisidir?", "Pandas", "Matplotlib", "SciPy", "csv.reader"),
        ("scikit-learn esas olarak ne sağlar?", "Makine öğrenmesi modelleri ve değerlendirme araçları", "İşletim sistemi", "Tarayıcı arayüzü", "Veritabanı sunucusu"),
        ("NumPy'nin temel veri yapısı hangisidir?", "ndarray", "DataFrame", "dict", "set"),
        ("Grafik çizimi için defterde hangi kütüphane kullanılır?", "Matplotlib", "scikit-learn", "csv", "os"),
    ],
    [
        ("Pandas'ta satır-sütun biçimli tablo nedir?", "DataFrame", "Series", "ndarray scalar", "tuple"),
        ("Tek boyutlu etiketli Pandas yapısı hangisidir?", "Series", "DataFrame", "Figure", "Estimator"),
        ("İki sayısal değişkenin ilişkisi hangi grafikle görülür?", "Saçılım grafiği", "Pasta grafiği", "Akış şeması", "Alan grafiği"),
        ("NumPy'de dizinin belirli bölümünü seçme işlemine ne denir?", "Dilimleme", "Serileştirme", "İndeksleme kaybı", "Model eğitimi"),
    ],
    [
        ("CSV'de virgül yerine noktalı virgül kullanılmışsa ilk kontrol nedir?", "Ayraç parametresi", "Model türü", "Öğrenme oranı", "Grafik rengi"),
        ("İlk satır sütun adlarıysa yükleme sırasında ne belirtilir?", "Başlık satırı", "Test oranı", "Küme sayısı", "Kayıp fonksiyonu"),
        ("Tırnak içindeki ayraçların doğru okunmasını ne sağlar?", "CSV tırnaklama kuralı", "Korelasyon matrisi", "PCA", "Binarizer"),
        ("CSV'de sayılar metin olarak gelmişse hangi konu incelenir?", "Veri tipi dönüşümü", "Sınıflandırıcı marjini", "Grafik başlığı", "Çapraz doğrulama katı"),
    ],
    [
        ("İlk veri incelemesinde satır ve sütun sayısı neyi verir?", "Veri boyutunu", "Model doğruluğunu", "Hata dağılımını", "Korelasyon yönünü"),
        ("Sınıf dağılımı neden kontrol edilir?", "Dengesiz sınıfları görmek için", "CSV ayıracını bulmak için", "Grafiği kaydetmek için", "Kod hızını ölçmek için"),
        ("Korelasyon katsayısı tek başına neyi kanıtlamaz?", "Nedenselliği", "Doğrusal ilişki yönünü", "Ölçeği", "Değişken sayısını"),
        ("Aykırı değerlerden görece az etkilenen merkez ölçüsü hangisidir?", "Medyan", "Ortalama", "Varyans", "Standart sapma"),
    ],
    [
        ("Dağılımın şeklini görmek için hangi grafik uygundur?", "Histogram", "Akış şeması", "Çubuk kod", "Pasta grafiği"),
        ("Aykırı değerleri ve çeyrekleri birlikte gösteren grafik hangisidir?", "Kutu grafiği", "Çizgi grafiği", "Alan grafiği", "Ağaç diyagramı"),
        ("Çok sayıda özellik çiftini görsel incelemek için ne kullanılır?", "Saçılım matrisi", "Tek histogram", "Doğruluk skoru", "CSV başlığı"),
        ("Özellikler arası doğrusal ilişkiyi renklerle özetleyen görsel nedir?", "Korelasyon ısı haritası", "Kutu grafiği", "Alan grafiği", "Sütun grafiği"),
    ],
    [
        ("MinMaxScaler'in varsayılan hedef aralığı nedir?", "0–1", "−∞–∞", "1–10", "Yalnız tam sayılar"),
        ("StandardScaler hangi iki istatistiği kullanır?", "Ortalama ve standart sapma", "Medyan ve mod", "Minimum ve maksimum", "Çeyrek ve yüzde"),
        ("Normalizer genellikle neyi birim norma getirir?", "Her örnek vektörünü", "Sütun adlarını", "Hedef sınıfları", "CSV ayıracını"),
        ("Binarizer bir değeri hangi kuralla 0 veya 1 yapar?", "Eşik karşılaştırması", "K-kat bölme", "PCA dönüşümü", "Ridge cezası"),
    ],
    [
        ("RFE'nin temel işlemi nedir?", "Özellikleri yinelemeli elemek", "Yeni örnek üretmek", "Sınıfları dengelemek", "Grafik çizmek"),
        ("PCA'nın ürettiği çıktı nedir?", "Yeni temel bileşenler", "Orijinal sütunlardan seçilmiş alt küme", "Sınıf etiketi", "Eksik değer listesi"),
        ("Tek değişkenli özellik seçimi özellikleri nasıl inceler?", "Hedefle ayrı ayrı", "Yalnız ikili gruplar hâlinde", "Yalnız zamana göre", "Sadece görsel olarak"),
        ("Özellik öneminin modele bağlı olması neyi gerektirir?", "Farklı modellerde yeniden yorumlamayı", "Her önemi nedensellik saymayı", "Test verisinde eğitim yapmayı", "Her sütunu silmeyi"),
    ],
    [
        ("K-kat çapraz doğrulamada her gözlem kaç kez doğrulama bölümünde yer alır?", "Bir kez", "Hiç", "K kez", "Her epoch'ta"),
        ("Leave-one-out yönteminde her turdaki test kümesi kaç gözlemdir?", "Bir", "İki", "Yarısı", "Tüm veri"),
        ("Ön işlem ölçekleyicisi hangi veri üzerinde öğrenilmelidir?", "Yalnız eğitim verisi", "Eğitim ve test birlikte", "Yalnız test verisi", "Sonuçlardan sonra"),
        ("Aynı veride tekrar tekrar ayar yapılıyorsa son performans için ne ayrılır?", "Dokunulmamış test kümesi", "Eğitim kaybı", "Grafik başlığı", "CSV yorum satırı"),
    ],
    [
        ("Yanlış pozitifleri azaltmak önemliyse hangi ölçü özellikle izlenir?", "Precision", "Recall", "MAE", "R²"),
        ("Büyük regresyon hatalarını daha fazla cezalandıran ölçü hangisidir?", "MSE", "MAE", "Accuracy", "F1"),
        ("TP, FP, TN, FN değerlerini hangi araç gösterir?", "Karmaşıklık matrisi", "PCA", "Kutu grafiği", "CSV okuyucu"),
        ("Dengesiz sınıflarda tek başına hangi ölçü yanıltabilir?", "Accuracy", "Recall", "Precision", "F1"),
    ],
    [
        ("k-NN yeni örneği nasıl sınıflandırır?", "Yakın komşularının etiketleriyle", "Rastgele etiketle", "Sadece ortalamayla", "PCA bileşeniyle"),
        ("Naive Bayes'in ayırt edici varsayımı nedir?", "Koşullu özellik bağımsızlığı", "Tüm özellikler eşit olmalı", "Yalnız doğrusal ilişki", "Eksik veri bulunmalı"),
        ("SVM hangi karar sınırını arar?", "Marjini en büyük yapan", "En kısa eğitimi yapan", "En çok yapraklı olan", "En çok sınıfı bulan"),
        ("Lojistik regresyon hangi çıktı için kullanılır?", "Sınıf olasılığı", "Kesin gelecek değer", "Küme merkezi", "Eksik sütun"),
    ],
    [
        ("Lasso hangi düzenlileştirmeyi kullanır?", "L1", "L2", "Dropout", "K-kat"),
        ("Ridge hangi cezayı kullanır?", "L2", "L1", "ROC", "F1"),
        ("Elastic Net hangi iki cezayı birleştirir?", "L1 ve L2", "MAE ve ROC", "Accuracy ve F1", "PCA ve RFE"),
        ("Sürekli hedef değişken için hangi model ailesi uygundur?", "Regresyon", "Sınıflandırma", "Kümeleme", "Binarizer"),
    ],
    [
        ("Adil model karşılaştırmasında modeller için ne aynı tutulur?", "Veri bölmeleri ve metrik", "Yalnız model adı", "Yalnız grafik rengi", "Yalnız eğitim süresi"),
        ("Çapraz doğrulama standart sapması neye işaret eder?", "Katlar arası performans değişkenliğine", "Özellik sayısına", "Sınıf adlarına", "CSV boyutuna"),
        ("Tek veri kümesinde en iyi çıkan model için hangi yorum doğrudur?", "Sonuç o veri ve kurulumla sınırlıdır", "Her veri kümesinde en iyidir", "Artık test gerekmez", "Özellik seçimi gereksizdir"),
        ("Kutu grafiğiyle model skorları karşılaştırılırken ne görülebilir?", "Dağılım ve medyan", "Nedensellik", "Sadece eğitim süresi", "Yalnız dosya boyutu"),
    ],
]
assert sum(map(len, ai_rows)) >= 50
course("ibo_ai", "ibo yapay zeka", "🧠", "#7c3aed",
       "Yapay Zeka Uygulamaları defteri: 13 bölüm özeti ve 52 özgün soru",
       ai_units, ai_notes,
       [questions(rows, "Özgün soru · Yapay_Zeka_Uygulamari.ipynb") for rows in ai_rows])

hr_units = [
    (1, "İnsan kaynakları yönetimine giriş · PDF s. 4–28"),
    (2, "İnsan kaynakları yönetimi ve çevre · PDF s. 29–57"),
    (3, "İş analizi ve iş tasarımı · PDF s. 58–73"),
]
hr_notes = [
    ("1. İKY'ye giriş · PDF s. 4–28",
     "İKY; çalışanların bilgi ve becerilerini örgütün amaçlarıyla uyumlu kullanırken refahlarını da gözeten stratejik bir yaklaşımdır. Kadrolama, eğitim, performans, ücret, kariyer, iş ilişkileri ve iş sağlığı temel faaliyetlerdir. Personel yönetiminin dar, idari ve kısa vadeli odağı İKY'de uzun vadeli stratejik bakışa dönüşür. İK departmanı, hat yöneticileri ve çalışanlar ortak sorumluluk taşır. İK uzmanları iş ortağı, değişim ajanı, yenilikçi ve çalışan savunucusu rolleri üstlenir. Politika genel karar ilkesi, izlek ise uygulama yoludur. PDF'nin ünite sonu soruları s. 25–26'dadır; aşağıdaki ilk 10 soru bunların özgün uyarlamasıdır."),
    ("2. İKY ve çevre · PDF s. 29–57",
     "Dış çevre; ulusal kültür, hukuk, politik ekonomi, iş gücü piyasası, teknoloji, sendikalar, müşteriler ve rakipler gibi örgütün zor denetlediği etkenlerdir. İç çevre; misyon, strateji, örgüt yapısı, kültür, çalışanlar, teknoloji ve üst yönetim tutumudur. Hofstede boyutları güç mesafesi, belirsizlikten kaçınma, bireycilik-toplumculuk, erillik-dişillik ve zaman yönelimidir. Teknolojik değişim beceri talebini değiştirir; İK planlaması bunu öngörmelidir. İK stratejisi örgüt hedefleriyle uyumlu olmalıdır. PDF'nin ünite sonu soruları s. 54–55'tedir; aşağıdaki 10 soru bunların özgün uyarlamasıdır."),
    ("3. İş analizi ve tasarımı · PDF s. 58–73",
     "İş analizi işin görevlerini, sorumluluklarını, koşullarını ve gerektirdiği nitelikleri sistemli biçimde belirler. Çıktıları iş tanımı ve iş gerekleridir. Bilgi gözlem, görüşme ve başka yöntemlerle toplanabilir; yetkinlik, ekip ve kişilik temelli yaklaşımlar da ele alınır. İş tasarımı görevin kapsamını ve ilişkilerini düzenler: basitleştirme işi küçük parçalara ayırır; rotasyon iş değiştirerek deneyimi artırır; zenginleştirme dikey yetki ve sorumluluk ekler; genişletme aynı düzeyde yatay görev ekler. Rotasyon monotonluğu azaltabilir ama uyum güçlüğü yaratabilir. PDF'nin 73. sayfası bu ünitenin ortasında biter; ünite sonu soruları kapsam dışında kalır. Aşağıdaki 10 soru özgün olarak yazılmıştır."),
]
hr_rows = [
    [
        ("Uyarlanabilir ve yenilikçi örgütte hangi iletişim tek başına baskın olmamalıdır?", "Yalnız dikey iletişim", "Yatay iletişim", "Açık geri bildirim", "Birimler arası iletişim"),
        ("Hangisi tipik bir İK işlevi değildir?", "Ürün fiyatlandırması", "Eğitim", "Performans değerlendirmesi", "Ücret yönetimi"),
        ("Modern İKY'yi personel yönetiminden ayıran odak nedir?", "Stratejik ve uzun vadeli yaklaşım", "Yalnız bordro", "Çalışanı sadece maliyet görmek", "Sadece evrak takibi"),
        ("Geleneksel personel yönetiminin odağı hangisidir?", "İdari işlem ve iş odaklılık", "Stratejik ortaklık", "Çalışan sermayesi", "Proaktif değişim"),
        ("İKY'nin hedefiyle hangisi çelişir?", "Yasal kuralları bilinçli ihlal etmek", "Verimliliği artırmak", "Etik davranmak", "Çalışma yaşamını iyileştirmek"),
        ("Boş pozisyona uygun aday bulma ve seçme hangi faaliyettir?", "Kadrolama", "Ücretleme", "Performans değerlendirme", "İş güvenliği"),
        ("Etkili İKY'nin beklenen çıktısı hangisidir?", "Çalışan tatmini ve kalite", "Sürekli maliyet artışı", "Sürekli devamsızlık artışı", "Uyum kaybı"),
        ("İK uzmanı için hangisi uygun yetkinlik değildir?", "Hesapsız risk almak", "Değişimi yönetmek", "Stratejiyi anlamak", "Güvenilir olmak"),
        ("İK uzmanının hat yöneticileriyle sorumluluğu paylaşması hangi roldür?", "İş ortağı", "Yalnız kayıt memuru", "Bağımsız denetçi", "Sendika temsilcisi"),
        ("İK biriminin temel kurumsal rolleri arasında hangisi yer almaz?", "Sendikal temsil rolü", "Stratejik rol", "Operasyonel rol", "Çalışan savunuculuğu"),
    ],
    [
        ("İşletmenin çevreye sunduğu çıktı nedir?", "Mal ve hizmetler", "Sermaye", "Emek", "Ham madde"),
        ("Hangisi örgütün iç çevresinde değerlendirilir?", "Çalışanlar", "Ulusal hukuk", "İş gücü piyasası", "Ulusal kültür"),
        ("Bugünkü iş çevresi için hangisi tipik değildir?", "Rekabetin yok denecek kadar az olması", "Hızlı teknoloji değişimi", "Değişen müşteri beklentileri", "Yoğun rekabet"),
        ("Çevre değişimini önceden izleyip hazırlık yapan İK yaklaşımı nedir?", "Proaktif", "Yalnız reaktif", "Durağan", "Rastgele"),
        ("Güç mesafesi yüksek kültürde güç eşitsizliği nasıl algılanır?", "Daha yüksek ve olağan", "Tamamen yok", "Her yerde aynı", "Ölçülemez"),
        ("Bireysel özerkliğe daha çok vurgu yapan kültür eğilimi hangisidir?", "Bireycilik", "Toplumculuk", "Yüksek güç mesafesi", "Yüksek belirsizlikten kaçınma"),
        ("Bireyci-toplumcu farkı hangi İK alanında belirginleşebilir?", "Performans yönetiminde", "Dosya biçiminde", "CSV yüklemede", "Ağ yönlendirmede"),
        ("Klasik anlamda işsizlik hangi durumda artar?", "Emek arzı talebi aştığında", "Talep arzı aştığında", "Arz ve talep eşitlendiğinde", "Teknoloji sabit kaldığında"),
        ("Örgütün varlık nedenini açıklayan kavram nedir?", "Misyon", "Haftalık plan", "Bütçe kalemi", "Pozisyon kodu"),
        ("Görev ve yetkilerin birimler arasındaki düzeni nedir?", "Örgüt yapısı", "Örgüt iklimi", "Ücret paketi", "İş gücü arzı"),
    ],
    [
        ("İş analizi öncelikle neyi inceler?", "İşin görev, koşul ve gereklerini", "Yalnız çalışanın maaşını", "Yalnız piyasa fiyatını", "Yalnız marka adını"),
        ("İş analizinden türeyen yazılı görev açıklaması nedir?", "İş tanımı", "Misyon", "Kâr tablosu", "Toplu sözleşme"),
        ("İşi yapacak kişinin bilgi, beceri ve nitelikleri hangi çıktıdır?", "İş gerekleri", "İş kodu", "İş hacmi", "İşletme logosu"),
        ("Çalışanı farklı görevlere belirli aralıklarla geçirme tekniği nedir?", "İş rotasyonu", "İş basitleştirme", "İş zenginleştirme", "İşten çıkarma"),
        ("Aynı düzeyde yeni görevler eklemek hangi tekniktir?", "İş genişletme", "İş zenginleştirme", "İş analizi", "Kişilik ölçümü"),
        ("Planlama ve denetim yetkisi ekleyerek işi dikey büyütmek nedir?", "İş zenginleştirme", "İş genişletme", "İş basitleştirme", "İş rotasyonu"),
        ("Karmaşık işi küçük ve tekrarlı parçalara ayırma hangi tekniktir?", "İş basitleştirme", "İş rotasyonu", "İş zenginleştirme", "Ekip temelli analiz"),
        ("İş rotasyonunun olası yararı nedir?", "Monotonluğu azaltıp beceri genişletmesi", "Her görevi otomatikleştirmesi", "Yetkiyi daima artırması", "Eğitimi gereksiz kılması"),
        ("Bağlamsal performans örneği hangisidir?", "Çalışma arkadaşına destek olmak", "Yalnız ürün adedini saymak", "Makine hızını ölçmek", "İş kodunu değiştirmek"),
        ("Ekip temelli iş analizinde hangi ilişki önemlidir?", "Görev ve hedef bağımlılığı", "Yalnız bireysel unvan", "Yalnız ofis rengi", "Yalnız bordro tarihi"),
    ],
]
hr_banks = []
for index, rows in enumerate(hr_rows):
    source = ("PDF ünite sonu sorularının özgün uyarlaması · s. 25–26"
              if index == 0 else
              "PDF ünite sonu sorularının özgün uyarlaması · s. 54–55"
              if index == 1 else
              "Özgün soru · PDF s. 58–73")
    hr_banks.append(questions(rows, source))
course("ik_vize", "insan kaynakları vize", "👥", "#0d9488",
       "İnsan Kaynakları Yönetimi PDF s. 1–73: özet ve 30 soru",
       hr_units, hr_notes, hr_banks)

nlp_units = [
    (0, "0. Kurulum ve çalışma ortamı"),
    (1, "1. Transformer modelleri"),
    (2, "2. Transformers ile model kullanımı"),
    (3, "3. Önceden eğitilmiş modeli ince ayar"),
    (4, "4. Model ve tokenizer paylaşımı"),
]
nlp_notes = [
    ("Kaynak ve kapsam",
     "Mesut hocanın NLP_2026 deposunun görülebilen ana dalında 0. kurulum ve 1. Transformer bölümleri vardır. README, Hugging Face LLM Course'u dersin ana omurgası olarak tanımlar. Bu dersteki 2–4. üniteler depoda doğrulanmış ders dosyası değil, resmî Hugging Face kursunun aynı numaralı bölümlerinden hazırlanmış özgün çalışma özetidir. Soruların tamamı bu uygulama için yazılmıştır.<br><a href='https://github.com/mesutpolatgil/NLP_2026' target='_blank' rel='noopener noreferrer'>Mesut hocanın deposu</a> · <a href='https://huggingface.co/learn/llm-course/chapter1/1' target='_blank' rel='noopener noreferrer'>Hugging Face LLM Course</a>"),
    ("0. Kurulum",
     "Python ortamı ve bağımlılıkların doğru sürümleri hazırlanır; örnekler için Transformers, Datasets ve Tokenizers gibi paketler kullanılır. GPU bazı eğitimlerde süreyi kısaltır, ancak küçük çıkarım örnekleri CPU'da da denenebilir. Çalışma ortamı, model sürümü ve rastgele tohumun kaydı tekrarlanabilirliğe yardım eder. Kaynak: NLP_2026 deposundaki kurulum dizini ve Hugging Face kursu."),
    ("1. Transformer modelleri",
     "NLP; sınıflandırma, özetleme, çeviri, soru cevaplama ve metin üretimi gibi görevleri kapsar. Transformer, tokenlar arasındaki ilişkiyi attention ile modeller. Encoder ağırlıklı mimariler metni anlama, decoder ağırlıklı mimariler üretim, encoder-decoder mimariler girdi-çıktı dönüşümü için elverişlidir. Hazır pipeline hızlı başlangıç sağlar; model çıktısı yanlı veya hatalı olabilir. Kaynak: NLP_2026 bölüm 1 ve Hugging Face LLM Course bölüm 1."),
    ("2. Transformers ile kullanım",
     "Pipeline'ın arkasında tokenizer metni token kimliklerine dönüştürür; model sayısal tensörleri işleyip logits üretir; görev başlığı ve son işlem anlamlı çıktı verir. Padding dizileri aynı uzunluğa tamamlar, truncation sınırı aşan bölümü keser. Attention mask dolgu tokenlarını ayırt eder. Model ve tokenizer aynı checkpoint ile eşleşmelidir. Kaynak: Hugging Face LLM Course bölüm 2; NLP_2026 deposunda bu bölüm görünmüyor."),
    ("3. İnce ayar",
     "Önceden eğitilmiş model, görev etiketli veriyle belirli işe uyarlanır. Veri eğitim, doğrulama ve test olarak ayrılır; tokenizer dönüştürmesi tüm bölümlere aynı kuralı uygular. Trainer eğitim döngüsünü kolaylaştırır; metrikler görevle uyumlu seçilir. Test verisi hiperparametre ayarında kullanılmaz. Kaynak: Hugging Face LLM Course bölüm 3; NLP_2026 deposunda bu bölüm görünmüyor."),
    ("4. Paylaşım",
     "Hugging Face Hub model, tokenizer, yapılandırma ve model kartını sürümlü bir depoda tutar. Model kartı amaç, veri, sınırlar ve değerlendirme bilgisini açıklar. Yalnız paylaşma yetkisi bulunan dosyalar yüklenir; erişim anahtarları, kişisel veri ve lisansı uygun olmayan eğitim verileri yayımlanmaz. Kaynak: Hugging Face LLM Course bölüm 4; NLP_2026 deposunda bu bölüm görünmüyor."),
]
nlp_rows = [
    [
        ("Bir örnek notebook başka bilgisayarda çalışmıyorsa önce neyi karşılaştırırsın?", "Python ve paket sürümlerini", "Grafik rengini", "Dosya adının uzunluğunu", "Ekran parlaklığını"),
        ("Küçük çıkarım örneği CPU'da çalışırken eğitim çok yavaşsa en makul hızlandırıcı nedir?", "Uygun GPU", "Daha uzun dosya adı", "Daha çok HTML", "Daha fazla çıktı yazdırma"),
        ("Tekrarlanabilir deneme için hangi bilgi kaydedilmelidir?", "Bağımlılık ve model sürümleri", "Yalnız son ekran görüntüsü", "Yalnız klasör rengi", "Yalnız kullanıcı adı"),
        ("Paket bağımlılıkları çakıştığında hangi araç yaklaşımı yararlıdır?", "Ayrı sanal ortam", "Aynı klasöre tüm sürümleri kopyalamak", "Test verisini silmek", "Tokenları büyütmek"),
        ("Aynı deneyin farklı sonuç vermesini azaltmak için hangi ayar yararlıdır?", "Rastgele tohum", "Pencere boyutu", "Dosya simgesi", "Metin rengi"),
    ],
    [
        ("Bir cümlede uzak iki kelimenin ilişkisini modelleyen temel mekanizma nedir?", "Attention", "CSV ayracı", "Piksel örnekleme", "Dosya sıkıştırma"),
        ("Bir yorumun olumlu veya olumsuz olduğunu bulma hangi NLP görevidir?", "Metin sınıflandırma", "Metin üretimi", "Çeviri", "Konuşma sentezi"),
        ("Verilen istemi sürdürerek metin yazma için hangi mimari eğilimi uygundur?", "Decoder ağırlıklı", "Yalnız encoder", "Karar ağacı", "K-means"),
        ("Bir dilden diğerine çeviri için hangi mimari doğal seçenektir?", "Encoder-decoder", "Yalnız görüntü encoder'ı", "KNN", "PCA"),
        ("Hazır pipeline sonucunda gerçeğe aykırı ama akıcı cevap görülürse ne yapılmalı?", "Çıktıyı doğrulamak", "Otomatik doğru saymak", "Tokenizer'ı silmek", "Veri testini kaldırmak"),
    ],
    [
        ("Model metni doğrudan sayısal girdi olarak alamıyorsa hangi bileşen gerekir?", "Tokenizer", "Kutu grafiği", "CSV yazıcı", "Optik okuyucu"),
        ("Farklı uzunluktaki cümleleri aynı batch'e koyarken hangi işlem gerekir?", "Padding", "Sınıf silme", "PCA", "Dosya bölme"),
        ("Padding tokenlarının gerçek içerik sanılmaması için ne kullanılır?", "Attention mask", "ROC eğrisi", "MAE", "Model kartı"),
        ("Modelin kabul ettiği en uzun girdiyi aşan metinde hangi işlem uygulanabilir?", "Truncation", "Aynı metni iki kez ekleme", "Etiket değiştirme", "Sıcaklığı sıfırlama"),
        ("Farklı checkpoint'ten tokenizer kullanmak niçin sakıncalıdır?", "Token kimlikleri model sözlüğüyle uyuşmayabilir", "Dosya küçülür", "GPU kapanır", "Metrik otomatik artar"),
    ],
    [
        ("Hazır modeli duygu analizi veri kümesine uyarlama işlemi nedir?", "İnce ayar", "Sadece çıkarım", "Dosya arşivleme", "Grafik çizme"),
        ("Hiperparametre seçimi hangi bölümde yapılmalıdır?", "Doğrulama verisinde", "Son test kümesinde", "Yayımlanmış sonuçlarda", "Model kartında"),
        ("Etiketli veride sınıf oranları çok farklıysa hangi değerlendirme daha anlamlıdır?", "Precision, recall ve F1'i incelemek", "Yalnız eğitim kaybı", "Yalnız dosya boyutu", "Yalnız epoch sayısı"),
        ("Trainer sınıfı temelde neyi kolaylaştırır?", "Eğitim ve değerlendirme döngüsünü", "Veri lisansını değiştirmeyi", "Parolayı şifrelemeyi", "Elle HTML yazmayı"),
        ("Test verisiyle birçok kez model seçmek hangi riski artırır?", "Test setine uyum ve iyimser sonuç", "Daha adil ölçüm", "Otomatik veri anonimliği", "Tokenizer eşleşmesi"),
    ],
    [
        ("Başkasının modeli güvenle yeniden kullanması için hangi dosya açıklayıcıdır?", "Model kartı", "Rastgele log", "Ekran resmi", "Ham erişim anahtarı"),
        ("Hub'a model gönderirken ne kesinlikle yüklenmemelidir?", "Erişim tokenı", "Model kartı", "Uygun lisans bilgisi", "Değerlendirme özeti"),
        ("Model ve tokenizer birlikte paylaşılmazsa ne olabilir?", "Yeniden kullanımda uyumsuzluk", "Metrik garantili artar", "Model otomatik küçülür", "Lisans değişir"),
        ("Model kartında hangi bilgi yer almalıdır?", "Amaç, veri, sınırlar ve değerlendirme", "Yalnız emoji", "Yalnız dosya tarihi", "Gizli anahtar"),
        ("Paylaşmadan önce veri için hangi kontrol gerekir?", "Lisans ve kişisel bilgi kontrolü", "Yalnız zip boyutu", "Yalnız görsel tema", "Yalnız batch boyutu"),
    ],
]
nlp_banks = [questions(rows, "Özgün senaryo sorusu · Hugging Face LLM Course")
             for rows in nlp_rows]
nlp_qa = [
    ("0. Kurulum · kısa cevap",
     "1. Aynı notebook bir arkadaşında hata veriyor. İlk üç kontrolün ne olur?<br><strong>Cevap:</strong> Python sürümü, paket sürümleri ve sanal ortam/kurulum adımları.<br><br>2. Rastgele bölme her çalışmada değişiyorsa ne kaydedersin?<br><strong>Cevap:</strong> Rastgele tohumu ve veri bölme ayarını.<br><br>3. CPU'da yavaş eğitimi nasıl hızlandırırsın?<br><strong>Cevap:</strong> Uygun GPU kullanır, küçük örnekle kodu doğrularım."),
    ("1. Transformer · kısa cevap",
     "1. Bir yorumun duygusunu bulmak için hangi görev seçilir?<br><strong>Cevap:</strong> Metin sınıflandırma.<br><br>2. Attention'ın temel yararı nedir?<br><strong>Cevap:</strong> Tokenlar arası bağları, uzak konumlar dahil, ağırlıklandırır.<br><br>3. Akıcı bir model cevabı neden yine de kontrol edilir?<br><strong>Cevap:</strong> Akıcılık doğruluk garantisi değildir; model yanılabilir."),
    ("2. Transformers · kısa cevap",
     "1. Tokenizer ile model neden aynı checkpoint'ten olmalı?<br><strong>Cevap:</strong> Token kimlikleri ve model sözlüğü eşleşmelidir.<br><br>2. Padding ile attention mask farkı nedir?<br><strong>Cevap:</strong> Padding uzunluğu eşitler; mask gerçek tokenları işaretler.<br><br>3. Çok uzun metin girişinde hangi kayıp yaşanır?<br><strong>Cevap:</strong> Truncation kullanılırsa kesilen bölümün bilgisi kaybolur."),
    ("3. İnce ayar · kısa cevap",
     "1. Eğitim, doğrulama ve testin ayrı rolleri nedir?<br><strong>Cevap:</strong> Ağırlık öğrenme, model seçimi ve son tarafsız ölçüm.<br><br>2. Dengesiz veri için tek başına accuracy neden yetmez?<br><strong>Cevap:</strong> Çoğunluk sınıfını tahmin etmek yüksek doğruluk verebilir; sınıf bazlı precision/recall/F1 gerekir.<br><br>3. Test setiyle ayar yaparsan ne olur?<br><strong>Cevap:</strong> Sonuç iyimserleşir; test tarafsızlığını yitirir."),
    ("4. Paylaşım · kısa cevap",
     "1. Model kartına hangi sınırlamayı yazarsın?<br><strong>Cevap:</strong> Bilinen başarısızlık, önyargı ve uygun olmayan kullanım alanlarını.<br><br>2. Hub'a yüklemeden önce hangi gizli bilgi kontrol edilir?<br><strong>Cevap:</strong> Erişim tokenları, anahtarlar ve kişisel veriler.<br><br>3. Tokenizer eksikse kullanıcı ne yaşar?<br><strong>Cevap:</strong> Aynı metin farklı tokenlanabilir; tahminler bozulabilir."),
]
course("mesut_nlp_vize", "mesut hoca nlp dersi vize", "🗣️", "#2563eb",
       "NLP 0–4 kısa özet, 25 özgün test ve 15 kısa cevap",
       nlp_units, nlp_notes, nlp_banks, nlp_qa)

write(ROOT / "courses.json", courses)

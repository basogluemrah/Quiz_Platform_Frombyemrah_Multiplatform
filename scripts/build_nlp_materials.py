"""Build presentation readers, classical questions and concise narration text."""
import json
import re
from pathlib import Path
from urllib.parse import quote
from import_nlp_sources import ROOT, DATA, SOURCE, PATHS, START, OPTION, render, save

def main():
    docs = json.loads((SOURCE / 'presentations.json').read_text(encoding='utf-8'))
    summaries = [
        ('0. Kurulum ve ortam', ['Colab, kurulum gerektirmeden notebook çalıştırır; yerelde venv ile paketleri projeye özel tut.', 'Python ve paket sürümlerini kontrol et; notebook çekirdeğiyle kurulum ortamı aynı olmalı.', 'Transformers model kullanımını, Datasets veri yüklemeyi ve Tokenizers metin dönüşümünü sağlar.', 'Hub erişim belirtecini kaynak koda yazma; yalnız gerekli izinleri ver.']),
        ('1. Transformer modelleri', ['NLP görevleri: sınıflandırma, NER, soru cevaplama, çeviri, özetleme ve üretim.', 'Pipeline akışı: ön işleme → model → son işleme.', 'Encoder anlama/temsil, decoder üretim, encoder-decoder girdi-çıktı dönüşümü için uygundur.', 'Attention tokenlar arası bilgi akışını ağırlıklandırır; multi-head farklı alt uzayları işler.', 'Ön eğitim genel örüntüleri öğrenir; ince ayar belirli göreve uyarlar. Akıcı çıktı doğruluk garantisi değildir.']),
        ('2. Transformers kullanımı', ['Tokenizer metni token kimliklerine dönüştürür; model logits veya gizli temsiller üretir.', 'Padding batch boyutlarını eşitler; attention mask gerçek tokenları dolgudan ayırır; truncation metni keser.', 'AutoModel temel gövdedir; göreve özel sınıflar bir çıktı başlığı ekler. Tokenizer ve model uyumlu olmalı.', 'Softmax sınıf skorlarını normalize eder; temel çıktı boyutları batch, sequence ve hidden size’dır.', 'Ek sunumlar: TGI/vLLM/llama.cpp model sunum araçları ve zafiyet/model davranışı örnekleri. Araç seçimi donanım, hız ve bellek gereksinimine bağlıdır.', 'Soru sunumundaki 13 soru mevcut kaynak soru bankasıyla örtüşür; 3 açık uçlu soru Klasik Sorular bölümündedir.']),
        ('3. Model ince ayarı', ['Veriyi eğitim/doğrulama/test olarak ayır; Dataset.map ve batched işlemlerle tokenize et.', 'Dinamik padding her batch’in en uzun örneğini esas alır ve gereksiz dolguyu azaltır.', 'Trainer eğitim döngüsünü yönetir; TrainingArguments ayarları, compute_metrics ölçümleri belirler.', 'Elle eğitim: forward → loss → backward → optimizer.step → scheduler → zero_grad.', 'Evaluation ağırlıkları güncellemez. Accelerate dağıtık eğitimi kolaylaştırır.', 'Eğitim kaybı düşerken doğrulama kaybı yükselirse overfitting düşünülebilir; erken durdurma ve düzenlileştirme kullanılabilir.']),
        ('4. Model ve tokenizer paylaşımı', ['Hub, model ve tokenizer dosyalarını sürümlü depolarda saklar.', 'Model, tokenizer ve yapılandırmayı uyumlu biçimde kaydet; push_to_hub veya Hub yükleme araçlarını kullan.', 'Model kartı: amaç, veri, eğitim, metrikler, lisans, sınırlar ve önyargılar.', 'YAML meta verileri dil ve görev gibi bilgileri tanımlar; modelin bulunabilirliğini destekler.', 'Paylaşmadan önce token, kişisel veri ve lisans kontrolü yap. Büyük dosya yöntemleri ve CLI komutları sürüme bağlıdır.'])
    ]
    sections = []
    for unit, (title, bullets) in enumerate(summaries):
        sources = [doc for doc in docs if doc['unit'] == unit]
        links = ''.join('<p><a target="_blank" rel="noopener noreferrer" href="https://github.com/mesutpolatgil/NLP_2026/blob/main/' + quote(doc['path'], safe='/') + '">Kaynak: ' + doc['path'].rsplit('/', 1)[-1] + '</a></p>' for doc in sources)
        sections.append(dict(icon='📊', title=title, content='<ul>'+''.join('<li>'+bullet+'</li>' for bullet in bullets)+'</ul>'+links))
    save(DATA / 'presentations.json', dict(title='📊 Sunum Özetleri', description='0–4 kısa tekrar · 11 sunum belgesinden derlendi', sections=sections))

    classics = []
    short_answers = [
        'Self-attention, tokenlar arasındaki ilişkileri matris işlemleriyle hesaplar ve paralel işlemeyi kolaylaştırır. Dikkat ağırlıkları, her tokenın diğer tokenlardan ne kadar bilgi alacağını belirler.',
        'Gelecekteki tokenların skorları softmax öncesinde eksi sonsuzla maskelenir; böylece dikkat ağırlıkları sıfır olur. Model bir sonraki tokenı tahmin ederken gelecekteki cevabı göremez.',
        'Birden fazla dikkat başlığı, girdiyi farklı temsil alt uzaylarında işler. Böylece model aynı anda farklı sözdizimsel ve anlamsal ilişkileri öğrenebilir.',
        'Padding, aynı batch içindeki dizileri eşit uzunluğa getirir. Attention mask, gerçek tokenları dolgudan ayırarak dolgu konumlarının dikkate alınmasını engeller.',
        'AutoModel temel Transformer gövdesini ve gizli temsilleri verir. AutoModelForSequenceClassification buna bir sınıflandırma başlığı ekler ve sınıf skorları üretir.',
        'Temperature, token seçimindeki rastlantısallığı ayarlar. Düşük değer olasılık dağılımını keskinleştirip üretimi daha öngörülebilir; yüksek değer daha çeşitli yapar.'
    ]
    for unit in range(5):
        text = (SOURCE / f'unit{unit}.md').read_text(encoding='utf-8')
        positions = [m.start() for m in START.finditer(text)] + [len(text)]
        for start, end in zip(positions, positions[1:]):
            block = text[start:end]
            if any(OPTION.match(line) for line in block.splitlines()):
                continue
            # Stop at the following document section, not at the answer heading.
            block = re.split(r'\n#{1,2} (?!Soru)', block)[0]
            lines = block.splitlines()
            title = re.sub(r'^[#* ]+', '', lines[0]).replace('**', '')
            if unit == 1:
                title = ['Self-Attention ve dikkat skoru', 'Nedensel dikkat maskesi', 'Multi-Head Attention'][len(classics)]
            question_body = block.split('<details>')[0].split('### Cevap')[0]
            answer = short_answers[len(classics)]
            classics.append(dict(icon='✍️', title=f'Bölüm {unit} · {title}',
                content=render(question_body)+f'<p><strong>Kısa cevap:</strong> {answer}</p><p>Kaynak: NLP_2026 Bölüm {unit}. Cevap, kaynak açıklamasından kısaltılmıştır.</p>'))
    assert len(classics) == 6
    save(DATA / 'classics.json', dict(title='✍️ Klasik Sorular',
         description='Kaynaklardaki 6 açık uçlu soru · 1–3 cümlelik kısa cevaplar', sections=classics))

    notes = json.loads((DATA / 'notes.json').read_text(encoding='utf-8'))
    short = [
        'Bölüm sıfır, kurulum. NLP uygulamalarında ilk hedef tekrarlanabilir bir çalışma ortamıdır. Google Colab tarayıcıdan notebook çalıştırır. Yerel bilgisayarda Python sanal ortamı, projenin paketlerini diğer projelerden ayırır. Sanal ortamı oluşturduktan sonra etkinleştirir, gerekli paketleri aynı Python ortamına kurarız. Transformers modelleri kullanmayı, Datasets veri yüklemeyi, Tokenizers metni sayısallaştırmayı kolaylaştırır. Hub işlemlerinde kişisel erişim belirteci kullanılır; belirteç kaynak koduna veya GitHub deposuna yazılmaz. Bir paket bulunamadığında önce notebook çekirdeğinin doğru ortamı kullanıp kullanmadığı kontrol edilir. Sınav için iki noktayı hatırla: sanal ortam izolasyon sağlar; tarayıcıda oturum açmak terminalde kimlik doğrulamakla aynı işlem değildir.',
        'Bölüm bir, Transformer modelleri. Doğal dil işleme; sınıflandırma, çeviri, özetleme ve metin üretme gibi görevleri kapsar. Büyük dil modelleri bu alanın bir parçasıdır. Hazır pipeline, metni ön işler, modeli çalıştırır ve çıktıyı göreve uygun biçime çevirir. Transformer mimarisinde attention, tokenların birbirinden ne kadar bilgi alacağını hesaplar. Encoder modelleri metni temsil etmeye, decoder modelleri sırayla yeni token üretmeye, encoder decoder modelleri ise girdiyi başka bir çıktıya dönüştürmeye uygundur. Ön eğitim geniş veriden genel bilgi öğrenir. İnce ayar bu ağırlıkları belirli bir işe uyarlar. Metin üretiminde önce istem işlenir, sonra tokenlar ardışık üretilir. Sınav için hatırla: akıcı cevap doğru cevap garantisi değildir; modeller önyargı ve uydurma bilgi üretebilir.',
        'Bölüm iki, Transformers kullanımı. Model ham metin yerine sayısal girdilerle çalışır. Tokenizer metni tokenlara ve kimliklere dönüştürür. Model bu kimliklerden gizli temsiller veya görev başlığı üzerinden logits üretir. Softmax, sınıf skorlarını toplamı bir olan değerlere dönüştürür. Farklı uzunluktaki metinleri aynı yığına koyarken padding uzunlukları eşitler; attention mask gerçek tokenları dolgudan ayırır. Truncation, model sınırını aşan metni keser ve bilgi kaybettirebilir. Tokenizer ile modelin sözlük ve yapılandırmaları uyumlu olmalıdır. AutoModel temel gövdeyi, göreve özgü AutoModel sınıfları ek çıktı başlığını yükler. Sınav ipucu: tokenize token dizeleri verir, tokenizer çağrısı ise model girdilerini hazırlayabilir. Sunumlarda ayrıca model sunumu, performans ve zafiyet örnekleri bulunur.',
        'Bölüm üç, ince ayar. Önceden eğitilmiş model, etiketli görev verisiyle yeniden eğitilir. Veri eğitim, doğrulama ve test bölümlerine ayrılır. Dataset map işlemi tokenizasyonu tüm örneklere uygular; toplu işlem hızı artırabilir. Dinamik padding yalnız o yığındaki en uzun örneğe kadar dolgu yapar. Trainer eğitim ve değerlendirme döngüsünü kolaylaştırır. Elle döngüde ileri yayılım, kayıp hesabı, geriye yayılım, ağırlık güncelleme ve gradyan sıfırlama adımları vardır. Değerlendirmede ağırlıklar güncellenmez. Eğitim kaybı düşerken doğrulama kaybı artıyorsa aşırı uyum düşünülebilir. Erken durdurma ve düzenlileştirme yardımcı olabilir. Sınav için iki ayrımı unutma: backward gradyanı hesaplar; optimizer step ağırlığı günceller. Test kümesi son ölçüm içindir.',
        'Bölüm dört, model ve tokenizer paylaşımı. Hugging Face Hub model dosyaları, yapılandırmalar ve model kartlarını sürümlü depolarda tutar. Hazır modeli kullanırken uygun görev sınıfı, checkpoint ve tokenizer seçilir. Paylaşımda model ve tokenizer birlikte kaydedilir; push to hub veya Hub araçlarıyla yüklenebilir. Model kartında kullanım amacı, eğitim verisi, değerlendirme sonuçları, lisans ve sınırlamalar açıklanır. Başındaki YAML meta verileri dil ve görev gibi bilgileri tanımlar. Paylaşmadan önce erişim tokenları, kişisel bilgiler ve lisans koşulları kontrol edilir. Büyük dosya aktarımı ve komut adları kullanılan araç sürümüne göre değişebilir. Sınav için hatırla: model kartı basit bir tanıtım değildir; yeniden kullanım ve değerlendirme için temel belgedir.'
    ]
    destination = ROOT / 'public/materials/nlp'
    narration = []
    for unit, text in enumerate(short):
        (destination / f'bolum-{unit}-kisa-anlatim.txt').write_text(text+'\n', encoding='utf-8')
        source_path = PATHS[unit].replace('/soru-cevap/', '/ceviri/')
        source_url = 'https://github.com/mesutpolatgil/NLP_2026/blob/main/' + source_path
        title = f'Bölüm {unit} · Kısa anlatım'
        player = f'<p>NotebookLM · Türkçe kısa sesli özet</p><audio controls preload="metadata" style="width:100%" aria-label="Bölüm {unit} kısa sesli anlatım"><source src="/audio/nlp/bolum-{unit}.mp3" type="audio/mpeg">Tarayıcınız ses oynatmayı desteklemiyor.</audio><p><a href="/audio/nlp/bolum-{unit}.mp3" download>Ses dosyasını indir</a></p>'
        narration.append(dict(icon='🎙️', title=title, content=player+'<h3>Kısa çalışma metni</h3>'+render(text)+f'<p><a href="/materials/nlp/bolum-{unit}-kisa-anlatim.txt" download>Anlatım metnini indir</a> · <a href="{source_url}" target="_blank" rel="noopener noreferrer">Çeviri kaynağı</a></p>'))
        notes['sections'][unit+1]['content'] = narration[-1]['content']
    save(DATA / 'narration.json', dict(title='🎙️ Kısa Anlatımlar', description='0–4 hızlı vize tekrarı · kaynaklardan derlenen anlatım metinleri', sections=narration))
    save(DATA / 'notes.json', notes)
    units = json.loads((DATA / 'units.json').read_text(encoding='utf-8'))
    for item in [dict(id='classics', name='✍️ Klasik Sorular', icon='✍️', description='6 kaynak sorusu ve kısa cevap'), dict(id='presentations', name='📊 Sunum Özetleri', icon='📊', description='0–4 kısa, maddeli sunum özetleri'), dict(id='narration', name='🎙️ Kısa Anlatımlar', icon='🎙️', description='Bölüm içinde dinlenebilir beş kısa sesli özet')]:
        units['extras'] = [x for x in units['extras'] if x['id'] != item['id']] + [item]
    save(DATA / 'units.json', units)
    course_path = ROOT / 'src/data/courses.json'
    courses = json.loads(course_path.read_text(encoding='utf-8'))
    for course in courses['courses']:
        if course['id'] == 'mesut_nlp_vize':
            course['description'] = 'NLP 0–4: 81 test, kısa cevaplı 6 klasik, 5 sunum özeti ve 5 sesli anlatım'
    save(course_path, courses)
    print(f'{len(sections)} presentation documents; {len(classics)} classics; 5 narration texts')

if __name__ == '__main__':
    main()

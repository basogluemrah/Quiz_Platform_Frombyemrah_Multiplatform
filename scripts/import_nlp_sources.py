"""Import the five instructor repository documents without executing their HTML/code."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'scripts/sources/nlp'
DATA = ROOT / 'src/data/mesut_nlp_vize'
PATHS = [
    'bolum-00-kurulum/01-ortam-kurulumu/soru-cevap/2026-guz-alfa.md',
    'bolum-01-transformer-modellerine-giris/01-transformer-modelleri/soru-cevap/2026-guz-nlp01.md',
    'bolum-02-transformers-kullanimi/02-transformlarin-kullanimi/soru-cevap/2026-guz-nlp02.md',
    'bolum-03-onceden-egitilmis-bir-modelin-ince-ayarinin-yapilmasi/03-ince-ayar-finetuning/soru-cevap/2026-guz-nlp03.md',
    'bolum-04-modellerin-ve-tokenizerlarin-paylasilmasi/04-modellerin-ve-tokenizerlarin-paylasilmasi/soru-cevap/2026-guz-nlp04.md',
]

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def inline(text):
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

def render(markdown):
    # Escape all upstream markup; only generate a small set of trusted HTML tags.
    result, code = [], False
    for line in markdown.splitlines():
        if line.strip().startswith('```'):
            result.append('</pre>' if code else '<pre style="white-space:pre-wrap;overflow-wrap:anywhere">')
            code = not code
        elif code:
            result.append(html.escape(line) + '\n')
        elif line.strip() in ('<details>', '</details>', '<br>') or line.startswith('<a '):
            continue
        elif line.startswith('<summary>'):
            result.append('<p><strong>Cevap ve açıklamalar</strong></p>')
        elif re.match(r'^#{1,6} ', line):
            result.append('<h3>' + inline(re.sub(r'^#+ ', '', line)) + '</h3>')
        elif line.strip() == '---':
            result.append('<hr>')
        elif line.strip():
            result.append('<p>' + inline(line) + '</p>')
    if code:
        result.append('</pre>')
    return ''.join(result)

def plain(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return text.replace('`', '').strip().strip('*').strip()

START = re.compile(r'(?m)^(?:\*\*Soru \d+[:.]|#{2,3} Soru \d+|### \d+\.)')
OPTION = re.compile(r'^\s*(?:[-*]\s*)?(?:\[[ xX]\]\s*)?(?:\*\*)?([A-F])\)\s*(.*)$')

def extract(text, unit):
    positions = [m.start() for m in START.finditer(text)] + [len(text)]
    questions, omitted = [], []
    for start, end in zip(positions, positions[1:]):
        block = text[start:end]
        options, marked, prompt = {}, [], []
        answer_letters = []
        for line in block.splitlines():
            key = re.search(r'(?:Doğru Cevap(?:lar)?|Cevap)\s*:\s*\**\s*([^<]+)', line, re.I)
            if key:
                value = plain(key.group(1))
                answer_letters = re.findall(r'\b[A-F]\b', value)
                break
            option = OPTION.match(line)
            if option:
                label, value = option.groups()
                if label in options:
                    break
                if '✅' in value or 'DOGRU CEVAP' in value or '[x]' in line.lower():
                    marked.append(label)
                options[label] = plain(re.sub(r'\s*\(DOGRU CEVAP\)|✅', '', value))
            elif not options and line.strip():
                prompt.append(line)
        correct = list(dict.fromkeys(answer_letters or marked))
        title = plain(re.sub(r'^#{1,3}\s*|^\*\*', '', prompt[0])) if prompt else ''
        if len(correct) == 1 and correct[0] in options and 2 <= len(options) <= 5:
            labels = list(options)
            question = '<br>'.join(html.escape(re.sub(r'^#{1,3}\s*', '', plain(x))) for x in prompt
                                  if not x.startswith('```'))
            questions.append(dict(id=len(questions)+1, question=question,
                                  options=[html.escape(options[x]) for x in labels], correct=labels.index(correct[0]),
                                  source=f'NLP_2026 · Bölüm {unit} · kaynak sorusu'))
        else:
            omitted.append(title)
    return questions, omitted, len(positions)-1

def main():
    sections, manifest, total = [], [], 0
    for unit, path in enumerate(PATHS):
        text = (SOURCE / f'unit{unit}.md').read_text(encoding='utf-8')
        url = 'https://github.com/mesutpolatgil/NLP_2026/blob/main/' + path
        bank, omitted, count = extract(text, unit)
        data_path = DATA / f'unit{unit}.json'
        data = json.loads(data_path.read_text(encoding='utf-8'))
        data['questions'] = bank
        assert bank, f'No parsed questions in unit {unit}'
        save(data_path, data)
        sections.append(dict(icon='📚', title=f'{unit}. Bölüm · Kaynaktaki tüm sorular ve cevaplar ({count})',
                             content=f'<p><a href="{url}" target="_blank" rel="noopener noreferrer">Orijinal kaynak</a></p>' + render(text)))
        manifest.append(dict(unit=unit, source=url, sourceQuestions=count, quizQuestions=len(bank),
                             readingOnlyQuestions=omitted))
        total += len(bank)
        print(f'unit {unit}: {count} source questions; {len(bank)} quiz; {len(omitted)} reading only')
    save(DATA / 'practice.json', dict(sections=sections))
    save(SOURCE / 'manifest.json', manifest)
    courses_path = ROOT / 'src/data/courses.json'
    courses = json.loads(courses_path.read_text(encoding='utf-8'))
    for course in courses['courses']:
        if course['id'] == 'mesut_nlp_vize':
            course['description'] = f'NLP 0–4 ders kaynakları: {total} test sorusu ve tüm açıklamalı soru-cevaplar'
    save(courses_path, courses)
    units_path = DATA / 'units.json'
    units = json.loads(units_path.read_text(encoding='utf-8'))
    for extra in units['extras']:
        if extra['id'] == 'practice':
            extra.update(name='📚 Kaynak Soruları ve Cevapları', description='Beş dosyadaki tüm testler, çoklu cevaplar ve mimari soruları')
    save(units_path, units)
    notes_path = DATA / 'notes.json'
    notes = json.loads(notes_path.read_text(encoding='utf-8'))
    notes['sections'][0]['content'] = '0–4. bölümlerin soru-cevap dosyaları, Mesut Polatgil NLP_2026 deposundan aktarılmıştır. Test bölümünde tek doğru cevaplı kaynak soruları bulunur. Kaynak Soruları ve Cevapları bölümünde çoklu doğru cevaplı ve açık uçlu sorular dahil beş dosyanın tamamı, açıklamalarıyla yer alır. Kaynakların cevap anahtarları korunmuştur; sürüme bağlı komut ve API bilgileri ders kaynağının bağlamındadır. Özetler uygulama için derlenmiştir.'
    for section in notes['sections'][1:]:
        section['content'] = re.sub(r'; NLP_2026 deposunda bu bölüm görünmüyor\.', '.', section['content'])
    save(notes_path, notes)

if __name__ == '__main__':
    main()

"""Check the generated course references and quiz answer indexes."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "src" / "data"
courses = json.loads((root / "courses.json").read_text(encoding="utf-8"))["courses"]
assert len({course["id"] for course in courses}) == len(courses)
expected = {"ibo_ai": (13, 52), "ik_vize": (3, 80), "mesut_nlp_vize": (5, 81)}
for course_id, (unit_count, question_count) in expected.items():
    assert any(course["id"] == course_id for course in courses)
    base = root / course_id
    units = json.loads((base / "units.json").read_text(encoding="utf-8"))["units"]
    assert len(units) == unit_count
    questions = []
    for unit in units:
        data = json.loads((base / f"unit{unit['id']}.json").read_text(encoding="utf-8"))
        assert data["unitId"] == unit["id"]
        assert data["unitName"] == unit["name"]
        assert len({q["id"] for q in data["questions"]}) == len(data["questions"])
        questions += data["questions"]
    assert len(questions) == question_count
    assert len({q["question"] for q in questions}) == len(questions)
    assert all(2 <= len(q["options"]) <= 5 and 0 <= q["correct"] < len(q["options"]) and q.get("source")
               for q in questions)
    notes = json.loads((base / "notes.json").read_text(encoding="utf-8"))["sections"]
    assert len(notes) >= unit_count
    print(f"{course_id}: {unit_count} units, {question_count} questions, {len(notes)} notes")

hr_banks = [json.loads((root / f'ik_vize/unit{unit}.json').read_text(encoding='utf-8'))['questions']
            for unit in range(1, 4)]
assert [len(bank) for bank in hr_banks] == [27, 26, 27]
assert sum('Özgün ek soru' in q['source'] for bank in hr_banks for q in bank) == 50
assert all(len(set(q['options'])) == 4 for bank in hr_banks for q in bank)

classics = json.loads((root / 'mesut_nlp_vize/classics.json').read_text(encoding='utf-8'))
assert len(classics['sections']) == 6
assert all('Kısa cevap:' in section['content'] for section in classics['sections'])
assert not (root / 'mesut_nlp_vize/practice.json').exists()
manifest = json.loads((root.parents[1] / 'scripts/sources/nlp/manifest.json').read_text(encoding='utf-8'))
assert [x['sourceQuestions'] for x in manifest] == [3, 24, 13, 36, 11]
assert sum(x['quizQuestions'] for x in manifest) == 81
assert sum(len(x['readingOnlyQuestions']) for x in manifest) == 6
for unit in range(5):
    assert (root.parents[1] / f'public/audio/nlp/bolum-{unit}.mp3').stat().st_size > 100000
narration = json.loads((root / 'mesut_nlp_vize/narration.json').read_text(encoding='utf-8'))
assert len(narration['sections']) == 5
assert all('<audio controls' in x['content'] for x in narration['sections'])
print('NLP: 81 quiz + 6 short classics = all 87 source questions; 5 audio players valid')

"""Check the generated course references and quiz answer indexes."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "src" / "data"
courses = json.loads((root / "courses.json").read_text(encoding="utf-8"))["courses"]
assert len({course["id"] for course in courses}) == len(courses)
expected = {"ibo_ai": (13, 52), "ik_vize": (3, 30), "mesut_nlp_vize": (5, 74)}
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

practice = json.loads((root / "mesut_nlp_vize" / "practice.json").read_text(encoding="utf-8"))
assert len(practice["sections"]) == 5
manifest = json.loads((root.parents[1] / 'scripts/sources/nlp/manifest.json').read_text(encoding='utf-8'))
assert [x['sourceQuestions'] for x in manifest] == [3, 24, 13, 36, 11]
assert sum(x['quizQuestions'] for x in manifest) == 74
assert sum(len(x['readingOnlyQuestions']) for x in manifest) == 13
assert all('Orijinal kaynak' in section['content'] for section in practice['sections'])
assert not any('<script' in section['content'].lower() for section in practice['sections'])
print("NLP: all 87 source questions included; 74 quiz, 13 open/multiple-answer; data valid")

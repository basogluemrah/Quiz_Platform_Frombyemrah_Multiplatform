"""Check the generated course references and quiz answer indexes."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "src" / "data"
courses = json.loads((root / "courses.json").read_text(encoding="utf-8"))["courses"]
assert len({course["id"] for course in courses}) == len(courses)
expected = {"ibo_ai": (13, 52), "ik_vize": (3, 30), "mesut_nlp_vize": (5, 25)}
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
    assert all(len(q["options"]) == 4 and 0 <= q["correct"] < 4 and q.get("source")
               for q in questions)
    notes = json.loads((base / "notes.json").read_text(encoding="utf-8"))["sections"]
    assert len(notes) >= unit_count
    print(f"{course_id}: {unit_count} units, {question_count} questions, {len(notes)} notes")

practice = json.loads((root / "mesut_nlp_vize" / "practice.json").read_text(encoding="utf-8"))
assert len(practice["sections"]) == 5
assert sum(section["content"].count("<strong>Cevap:</strong>") for section in practice["sections"]) == 15
print("NLP: 15 short answers; all course data valid")

import { getCourseData } from './course-data.js';
const KEY = 'quiz-progress-v1';
export function persistQuiz(state) {
  try {
    sessionStorage.setItem(KEY, JSON.stringify({
      course: state.selectedCourse, unit: state.selectedUnit,
      ids: state.questions.map(q => [q.unitId ?? state.selectedUnit, q.id]),
      index: state.currentQuestionIndex, answers: state.answers
    }));
  } catch { /* Storage may be unavailable in private browsers. */ }
}
export function restoreQuiz(state) {
  try {
    const saved = JSON.parse(sessionStorage.getItem(KEY));
    if (!saved || !Array.isArray(saved.ids) || saved.ids.length === 0 || saved.ids.length > 5000) return;
    const units = getCourseData(saved.course, 'units').units;
    const questions = saved.ids.map(([unit, id]) => {
      if (!units.some(u => u.id === unit)) throw new Error('Unknown unit');
      const q = getCourseData(saved.course, `unit${unit}`).questions.find(q => q.id === id);
      if (!q) throw new Error('Unknown question');
      return { ...q, unitId: unit, unitName: units.find(u => u.id === unit).name };
    });
    if (!Number.isInteger(saved.index) || saved.index < 0 || saved.index >= questions.length) return;
    const answers = questions.map((q, i) => Number.isInteger(saved.answers?.[i]) && saved.answers[i] >= 0 && saved.answers[i] < q.options.length ? saved.answers[i] : undefined);
    Object.assign(state, { selectedCourse: saved.course, selectedUnit: saved.unit, questions,
      answers, currentQuestionIndex: saved.index,
      score: questions.filter((q, i) => q.correct === answers[i]).length,
      restoredRoute: `#quiz/${saved.course}/${saved.unit}` });
  } catch { /* Corrupt/stale progress cannot prevent opening the app. */ }
}

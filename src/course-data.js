// Course content is bundled with the app so navigation needs no extra network requests.
const data = import.meta.glob('./data/*/*.json', { eager: true, import: 'default' });
export function getCourseData(course, file) {
  const result = data[`./data/${course}/${file}.json`];
  if (!result) throw new Error('Ders içeriği bulunamadı');
  return result;
}

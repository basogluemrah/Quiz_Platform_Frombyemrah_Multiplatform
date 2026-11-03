import { readdir, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
const assets = (await readdir('dist/assets')).filter(p => /\.(js|css)$/.test(p));
const version = createHash('sha256');
for (const name of assets) version.update(await readFile(`dist/assets/${name}`));
const cache = `quiz-${version.digest('hex').slice(0, 12)}`;
const files = ['/', '/index.html', ...assets.map(p => `/assets/${p}`)];
await writeFile('dist/sw.js', `
const CACHE = ${JSON.stringify(cache)};
const FILES = ${JSON.stringify(files)};
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(FILES)));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('quiz-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;
  if (event.request.mode === 'navigate') {
    event.respondWith(fetch(event.request).catch(() => caches.open(CACHE).then(cache => cache.match('/index.html', { ignoreVary: true }))));
  } else if (FILES.includes(url.pathname)) {
    // The same-origin immutable asset can have Vary: Origin on the host. Module
    // requests carry a different Origin header from precaching requests.
    event.respondWith(caches.open(CACHE).then(cache => cache.match(url.pathname, { ignoreVary: true })).then(hit => hit || fetch(event.request)));
  }
});
`);
console.log(`Offline cache: ${assets.length} assets (${cache})`);

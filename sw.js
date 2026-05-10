const CACHE_NAME = 'aitools-cache-v1';
const urlsToCache = [
  '/aitools-blog/',
  '/aitools-blog/index.html',
  '/aitools-blog/robots.txt',
  '/aitools-blog/sitemap.xml'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => 
      response || fetch(event.request)
    )
  );
});

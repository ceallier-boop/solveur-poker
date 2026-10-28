'use strict';
// Service worker : l'application s'ouvre sans connexion (page, styles, script, lexique). Réseau d'abord, pour que les mises à
// jour arrivent tout de suite ; le cache ne sert qu'en cas de coupure. Les réponses de l'API ne sont jamais mises en cache ici :
// la progression hors ligne est gardée par la page elle-même (localStorage).
const CACHE = 'spinsacademy-shell-v2';
const SHELL = ['/', '/conseil', '/static/app.css', '/static/app.js', '/static/lexique.json', '/static/icon.svg', '/static/manifest.json'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  const shell = url.pathname === '/' || url.pathname === '/conseil' || url.pathname.startsWith('/static/');
  if (!shell) return;                                                  // API : toujours le réseau
  e.respondWith(fetch(e.request).then((r) => {
    if (r.ok) { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(url.pathname === '/' ? '/' : e.request, copy)); }
    return r;
  }).catch(() => caches.match(url.pathname === '/' ? '/' : e.request)));
});

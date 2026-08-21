/* ── Service worker: the offline notebook ──────────────────────────────
   Policy is deliberately simple and honest:

   - Online → serve the current version from the network (network-first),
     and refresh the cached copy while doing it. Every HTML page, the
     post manifest, and every same-origin asset follows this rule, so a
     new article appears the moment the reader is online.
   - Offline or slow network → serve the last known copy from the cache.
     If the network stalls past NETWORK_TIMEOUT_MS with a copy available,
     the copy wins the race; a fresh result, if it ever lands, still
     updates the cache for the next visit.
   - Never seen before and offline → the offline page for navigations.

   The full published library (every post in js/posts.js) is copied into
   the cache in the background: once at activation, then at most once
   every LIBRARY_SYNC_MS while the reader keeps reading. New posts reach
   the offline library either way — through a visit, or through the sync.

   Bump VERSION to invalidate every cached copy at once (new design,
   broken states); ordinary content updates never need it because
   network-first refreshes entries as readers arrive. */

const VERSION = 'v1';
const CACHE = 'vb-notes-' + VERSION;
const NETWORK_TIMEOUT_MS = 4000;
const LIBRARY_SYNC_MS = 24 * 60 * 60 * 1000;
const SYNC_MARKER = '/__vb-library-sync__';

/* The shell: everything a cold offline launch needs before any article
   has ever been opened — the shelf, about, the shared chrome the posts
   link, and the icons. Posts themselves are synced from the manifest. */
const SHELL = [
  '/',
  '/about.html',
  '/offline.html',
  '/site.webmanifest',
  '/css/site.css',
  '/js/site.js',
  '/js/scene.js',
  '/js/vb.js',
  '/js/posts.js',
  '/css/post-progress.css',
  '/js/post-progress.js',
  '/css/post-nav.css',
  '/js/post-nav.js',
  '/img/icon-192.png',
  '/img/icon-512.png',
  '/img/favicon.svg',
  '/img/favicon.ico',
  '/img/apple-touch-icon.png'
];

/* ── Install: cache the shell, don't let one missing file break it ──── */

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await Promise.all(SHELL.map(async (url) => {
      try { await cache.add(url); } catch (err) { /* keep the rest */ }
    }));
    await self.skipWaiting();
  })());
});

/* ── Activate: drop old versions, take control, sync the library ────── */

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((n) => n !== CACHE).map((n) => caches.delete(n)));
    await self.clients.claim();
    await syncLibrary();
  })());
});

/* ── Fetch ─────────────────────────────────────────────────────────────
   Navigations and same-origin GETs are network-first. Google Fonts (the
   only accepted third-party presentation dependency) is cache-first:
   font files are immutable and the browser cache headers do the rest. */

const FONT_HOSTS = /^fonts\.(googleapis|gstatic)\.com$/;

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  if (url.origin === self.location.origin) {
    if (request.mode === 'navigate') {
      event.respondWith(handleNavigation(request));
      event.waitUntil(maybeSyncLibrary());
    } else {
      event.respondWith(networkFirst(request, request));
    }
  } else if (FONT_HOSTS.test(url.hostname)) {
    event.respondWith(cacheFirst(request));
  }
});

/* Serve the page from the network when possible; otherwise the cached
   copy; otherwise the offline page. Navigation cache keys ignore the
   query string (the app launcher appends one). */
async function handleNavigation(request) {
  const key = new URL(request.url).pathname;
  try {
    return await networkFirst(request, key);
  } catch (err) {
    const cache = await caches.open(CACHE);
    return (await cache.match('/offline.html')) || Response.error();
  }
}

/* Network-first with a slow-network escape: if a cached copy exists, it
   wins whenever the network fails fast or stalls past the timeout. A
   late successful response still refreshes the cache. */
async function networkFirst(request, cacheKey) {
  const cache = await caches.open(CACHE);
  const cached = await cache.match(cacheKey, { ignoreSearch: true });

  const network = fetch(request).then((response) => {
    if (response && response.ok) {
      cache.put(cacheKey, response.clone());
    } else if (cached && response) {
      throw new Error('network returned ' + response.status);
    }
    return response;
  });

  if (!cached) return network;

  return Promise.race([
    network.catch(() => cached),
    new Promise((resolve) => setTimeout(() => resolve(cached), NETWORK_TIMEOUT_MS))
  ]);
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response && (response.ok || response.type === 'opaque')) {
    cache.put(request, response.clone());
  }
  return response;
}

/* ── Library sync ──────────────────────────────────────────────────────
   Read the published posts from js/posts.js (its array body is strict
   JSON) and cache any article not already held. Throttled by a timestamp
   stored in the cache itself, so it survives worker restarts. */

let syncing = false;

async function maybeSyncLibrary() {
  try {
    const cache = await caches.open(CACHE);
    const marker = await cache.match(SYNC_MARKER);
    const last = marker ? Number(await marker.text()) : 0;
    if (Date.now() - last > LIBRARY_SYNC_MS) await syncLibrary();
  } catch (err) { /* offline or busy — the next navigation retries */ }
}

async function syncLibrary() {
  if (syncing) return;
  syncing = true;
  try {
    const response = await fetch('/js/posts.js', { cache: 'no-store' });
    if (!response || !response.ok) return;
    const text = await response.text();
    const body = text.slice(text.indexOf('['), text.lastIndexOf(']') + 1);
    const posts = JSON.parse(body);
    const cache = await caches.open(CACHE);
    await Promise.all(posts
      .filter((post) => post.slug && !post.status)
      .map(async (post) => {
        if (await cache.match('/' + post.slug)) return;
        try { await cache.add('/' + post.slug); } catch (err) { /* next time */ }
      }));
    await cache.put(SYNC_MARKER, new Response(String(Date.now())));
  } catch (err) { /* offline or busy — the next navigation retries */ }
  syncing = false;
}

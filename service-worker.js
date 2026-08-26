const VERSION = "reading-room-v42";
const CORE_CACHE = `${VERSION}-core`;
const ARTICLE_CACHE = `${VERSION}-articles`;
const root = new URL("./", self.registration.scope);
const coreFiles = [
  "index.html", "workspace_theme.css", "workspace_skin.js", "mobile_pwa.js",
  "manifest.webmanifest", "icons/reading-room-192.png", "icons/reading-room-512.png"
].map(path => new URL(path, root).href);

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CORE_CACHE).then(cache => cache.addAll(coreFiles)));
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => ![CORE_CACHE, ARTICLE_CACHE].includes(key)).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});

self.addEventListener("fetch", event => {
  if (event.request.method !== "GET" || new URL(event.request.url).origin !== location.origin) return;
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).then(response => {
      const copy = response.clone(); caches.open(ARTICLE_CACHE).then(cache => cache.put(event.request, copy)); return response;
    }).catch(() => caches.match(event.request).then(response => response || caches.match(new URL("index.html", root)))));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
    if (response.ok) caches.open(CORE_CACHE).then(cache => cache.put(event.request, response.clone()));
    return response;
  })));
});

self.addEventListener("message", event => {
  const data = event.data || {};
  if (data.type === "SKIP_WAITING") self.skipWaiting();
  if (data.type === "REFRESH_APP") {
    event.waitUntil(caches.delete(CORE_CACHE)
      .then(() => caches.open(CORE_CACHE))
      .then(cache => cache.addAll(coreFiles.map(url => new Request(url, {cache: "reload"}))))
      .then(() => event.source?.postMessage({type: "APP_REFRESHED"}))
      .catch(error => event.source?.postMessage({type: "APP_REFRESH_ERROR", message: error.message})));
  }
  if (data.type === "CACHE_ARTICLE") {
    event.waitUntil(caches.open(ARTICLE_CACHE).then(cache => cache.addAll(data.urls)).then(() => event.source?.postMessage({type: "ARTICLE_CACHED", url: data.urls[0]})).catch(error => event.source?.postMessage({type: "CACHE_ERROR", message: error.message})));
  }
  if (data.type === "REMOVE_ARTICLE") {
    event.waitUntil(caches.open(ARTICLE_CACHE).then(cache => Promise.all(data.urls.map(url => cache.delete(url)))).then(() => event.source?.postMessage({type: "ARTICLE_REMOVED"})));
  }
});

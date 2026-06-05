const CACHE_NAME = "highway-code-v1";
const OFFLINE_URL = "/offline/";
const STATIC_ASSETS = [
  "/",
  "/rules/",
  "/quiz/",
  "/daily/",
  OFFLINE_URL,
  "/static/css/main.css",
  "/static/js/app.js",
  "/static/icons/icon.svg"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))))
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (url.pathname.includes("/quiz/answer/") || url.pathname.includes("/daily/answer/")) {
    return;
  }
  if (event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).catch(() => caches.match(OFFLINE_URL)));
    return;
  }
  event.respondWith(caches.match(event.request).then(hit => hit || fetch(event.request)));
});

self.addEventListener("push", event => {
  const data = event.data ? event.data.json() : {};
  event.waitUntil(
    self.registration.showNotification(data.title || "UK Highway Code", {
      body: data.body || "Time to practise your road rules.",
      icon: "/static/icons/icon.svg",
      badge: "/static/icons/icon.svg",
      data: { url: data.url || "/daily/" },
      actions: [
        { action: "open", title: "Study now" },
        { action: "dismiss", title: "Later" }
      ]
    })
  );
});

self.addEventListener("notificationclick", event => {
  event.notification.close();
  if (event.action !== "dismiss") {
    event.waitUntil(clients.openWindow(event.notification.data.url));
  }
});

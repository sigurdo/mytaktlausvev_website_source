importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.0.0/workbox-sw.js');

const urls_to_cache = [
    "/manifest.json",
    new RegExp("/static/.*")
]

for (let i = 0; i < urls_to_cache.length; i++) {
    workbox.routing.registerRoute(
        urls_to_cache[i],
        new workbox.strategies.StaleWhileRevalidate(),
    );
}

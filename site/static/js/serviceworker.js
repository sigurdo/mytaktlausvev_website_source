importScripts('https://storage.googleapis.com/workbox-cdn/releases/5.0.0/workbox-sw.js');

if (workbox) {
  console.log(`Yay! Workbox is loaded 🎉`);
} else {
  console.log(`Boo! Workbox didn't load 😬`);
}

const OFFLINE_URL = '/offline';

const urls_to_cache = [
    "/",
    "/omoss/",
    "/manifest.json",
    new RegExp("/static/.*")
]

for (let i = 0; i < urls_to_cache.length; i++) {
    workbox.routing.registerRoute(
        urls_to_cache[i],
        new workbox.strategies.StaleWhileRevalidate({
            // plugins: [
            //     new workbox.expiration.ExpirationPlugin({
            //         maxAgeSeconds: 60 * 60 * 24,
            //     })
            // ]
        })
    );
}

// // Handle offline.
// // From https://developers.google.com/web/tools/workbox/guides/advanced-recipes#provide_a_fallback_response_to_a_route
// workbox.routing.setCatchHandler(({ event }) => {
//     console.log(event)
//     switch (event.request.method) {
//         case 'GET':
//             return caches.match(OFFLINE_URL);
//         default:
//             return Response.error();
//     }
// });

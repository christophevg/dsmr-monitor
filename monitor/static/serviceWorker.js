const staticDevCoffee = "home-energy"
const assets = [
  "/",
  "/index.html",
  "/static/jquery.min.js",
  "/static/moments.js",
  "/static/chart.min.js",
  "/static/chartjs-plugin-streaming.min.js",
  "/static/socket.io.js"
]

self.addEventListener("install", installEvent => {
  installEvent.waitUntil(
    caches.open(staticDevCoffee).then(cache => {
      cache.addAll(assets)
    })
  )
});

self.addEventListener("fetch", fetchEvent => {
  fetchEvent.respondWith(
    caches.match(fetchEvent.request).then(res => {
      return res || fetch(fetchEvent.request)
    })
  )
});


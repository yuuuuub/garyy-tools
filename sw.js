const CACHE_NAME='garyy-tools-v1';
const PRECACHE=['/','/index.html'];

self.addEventListener('install',function(e){
  e.waitUntil(caches.open(CACHE_NAME).then(function(cache){return cache.addAll(PRECACHE)}));
  self.skipWaiting();
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){return k!==CACHE_NAME}).map(function(k){return caches.delete(k)}));
  }));
  self.clients.claim();
});

self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET')return;
  // Network first, cache fallback for HTML
  if(e.request.headers.get('accept')&&e.request.headers.get('accept').indexOf('text/html')>-1){
    e.respondWith(fetch(e.request).then(function(r){
      var clone=r.clone();
      caches.open(CACHE_NAME).then(function(c){c.put(e.request,clone)});
      return r;
    }).catch(function(){return caches.match(e.request)}));
    return;
  }
  // Cache first for static assets
  e.respondWith(caches.match(e.request).then(function(r){
    return r||fetch(e.request).then(function(resp){
      var clone=resp.clone();
      caches.open(CACHE_NAME).then(function(c){c.put(e.request,clone)});
      return resp;
    });
  }));
});

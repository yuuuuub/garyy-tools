var CACHE_NAME='garyy-tools-v2';
var OFFLINE_URL='/offline.html';
var PRECACHE=['/', '/index.html', OFFLINE_URL, '/manifest.json'];

self.addEventListener('install', function(e){
  e.waitUntil(caches.open(CACHE_NAME).then(function(cache){
    // 离线 fallback 页（运行时生成，避免单独维护文件）
    var offlineHtml = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>离线 - Gary\\'s Tools</title><style>body{background:#0d1117;color:#e6edf3;font-family:-apple-system,BlinkMacSystemFont,sans-serif;text-align:center;padding:80px 20px;line-height:1.6}h1{font-size:2rem;margin-bottom:12px;background:linear-gradient(135deg,#58a6ff,#7c3aed,#db61a2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}p{color:#8b949e}a{color:#58a6ff;text-decoration:none;display:inline-block;margin-top:20px;padding:10px 24px;border:1px solid #30363d;border-radius:10px;transition:all .2s}a:hover{border-color:#58a6ff;background:#161b22}</style></head><body><h1>📡 当前离线</h1><p>工具箱需要网络连接，请检查网络后重试。</p><p>已访问过的工具页仍可离线使用。</p><a href="/">← 返回首页</a></body></html>';
    var blob = new Blob([offlineHtml], {type: 'text/html'});
    var offlineResp = new Response(blob, {status: 200, headers: {'Content-Type': 'text/html'}});
    return Promise.all([
      cache.addAll(PRECACHE.filter(function(u){return u!==OFFLINE_URL})),
      cache.put(OFFLINE_URL, offlineResp)
    ]);
  }));
  self.skipWaiting();
});

self.addEventListener('activate', function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){return k!==CACHE_NAME}).map(function(k){return caches.delete(k)}));
  }).then(function(){
    // 清理 PRECACHE 之外的旧 offline.html 引用
    return self.clients.claim();
  }));
});

self.addEventListener('fetch', function(e){
  if(e.request.method!=='GET')return;
  var url=new URL(e.request.url);
  // 仅同源请求走缓存策略
  if(url.origin!==self.location.origin)return;

  // HTML：网络优先，失败回退缓存，再失败回退离线页
  if(e.request.headers.get('accept')&&e.request.headers.get('accept').indexOf('text/html')>-1){
    e.respondWith(fetch(e.request).then(function(r){
      var clone=r.clone();
      caches.open(CACHE_NAME).then(function(c){c.put(e.request,clone)});
      return r;
    }).catch(function(){
      return caches.match(e.request).then(function(r){
        return r||caches.match(OFFLINE_URL);
      });
    }));
    return;
  }
  // 静态资源：缓存优先，回退网络（仅缓存成功响应）
  e.respondWith(caches.match(e.request).then(function(r){
    if(r)return r;
    return fetch(e.request).then(function(resp){
      if(resp&&resp.ok){
        var clone=resp.clone();
        caches.open(CACHE_NAME).then(function(c){c.put(e.request,clone)});
      }
      return resp;
    });
  }));
});

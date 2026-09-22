// 通用 AI 代理 API（deepseek / vision）
// 修复: 路径遍历防护、错误日志、stream keepalive 容错
const ALLOWED_SERVICES = {
  deepseek: 'https://api.deepseek.com',
  vision: 'https://aip.baidubce.com',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}

export async function onRequest(context) {
  const { request, params, env } = context;
  const url = new URL(request.url);

  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
      },
    });
  }

  const segments = params.path || [];
  if (segments.length < 2) {
    return json({ error: 'Invalid proxy path' }, 400);
  }

  const service = segments[0];
  const endpoint = segments.slice(1).join('/');

  // 路径遍历防护：service 必须在白名单，endpoint 不含 .. 或 //
  if (!ALLOWED_SERVICES[service]) {
    return json({ error: `Unknown service: ${service}` }, 400);
  }
  if (/(^|\/)\.\.(\/|$)/.test(endpoint) || endpoint.includes('//')) {
    return json({ error: 'Invalid endpoint' }, 400);
  }

  const baseUrl = ALLOWED_SERVICES[service];
  const targetUrl = `${baseUrl}/${endpoint}${url.search}`;

  const envKeyName = service === 'deepseek' ? 'DEEPSEEK_API_KEY' : 'VISION_API_KEY';
  const apiKey = env[envKeyName] || '';

  if (!apiKey) {
    return json({ error: `缺少 ${service} API Key。请在 Cloudflare Pages 环境变量中设置 ${envKeyName}。` }, 401);
  }

  const proxyHeaders = new Headers();
  proxyHeaders.set('Content-Type', 'application/json');
  proxyHeaders.set('Authorization', `Bearer ${apiKey}`);

  try {
    const bodyText = await request.text();
    const bodyJson = JSON.parse(bodyText);

    const useStream = service === 'deepseek' && endpoint === 'chat/completions';
    if (useStream) {
      bodyJson.stream = true;
      bodyJson.stream_options = { include_usage: true };
    }

    const res = await fetch(targetUrl, {
      method: request.method,
      headers: proxyHeaders,
      body: JSON.stringify(bodyJson),
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`Proxy ${service}/${endpoint} failed:`, res.status, errorText.slice(0, 200));
      return new Response(errorText, {
        status: res.status,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      });
    }

    const responseHeaders = new Headers();
    responseHeaders.set('Access-Control-Allow-Origin', '*');

    if (useStream) {
      responseHeaders.set('Content-Type', 'text/event-stream');
      responseHeaders.set('Cache-Control', 'no-cache');

      const upstreamReader = res.body.getReader();
      const encoder = new TextEncoder();
      const keepaliveMsg = encoder.encode(': keepalive\n\n');
      let lastDataTime = Date.now();

      const keepaliveStream = new ReadableStream({
        async start(controller) {
          const keepaliveTimer = setInterval(() => {
            if (Date.now() - lastDataTime > 25000) {
              try { controller.enqueue(keepaliveMsg); } catch { clearInterval(keepaliveTimer); }
            }
          }, 25000);

          try {
            while (true) {
              const { done, value } = await upstreamReader.read();
              if (done) { clearInterval(keepaliveTimer); controller.close(); break; }
              lastDataTime = Date.now();
              controller.enqueue(value);
            }
          } catch (e) {
            clearInterval(keepaliveTimer);
            console.error('Stream read error:', e.message);
            try { controller.close(); } catch {}
          }
        },
      });

      return new Response(keepaliveStream, {
        status: res.status,
        headers: responseHeaders,
      });
    }

    const upstreamCT = res.headers.get('Content-Type') || 'application/json';
    responseHeaders.set('Content-Type', upstreamCT);

    return new Response(res.body, {
      status: res.status,
      statusText: res.statusText,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error('Proxy request failed:', error.message);
    return json({ error: '代理请求失败', details: error.message }, 502);
  }
}

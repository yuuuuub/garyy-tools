// DeepSeek AI 分析 API（流式）
// 注: [[path]].js 已实现通用代理，此文件为前端直调兼容入口
// 修复: 错误日志
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}

export async function onRequest(context) {
  const { request, env } = context;

  const respHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: respHeaders });
  }

  if (request.method !== 'POST') {
    return json({ error: 'Method not allowed' }, 405);
  }

  const apiKey = env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    return json({ error: '请在 Cloudflare Pages 环境变量中设置 DEEPSEEK_API_KEY' }, 500);
  }

  try {
    const body = await request.json();

    body.stream = true;
    body.stream_options = { include_usage: true };

    const deepseekRes = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify(body),
    });

    if (!deepseekRes.ok) {
      const errorText = await deepseekRes.text();
      console.error('DeepSeek API error:', deepseekRes.status, errorText.slice(0, 200));
      return new Response(errorText, {
        status: deepseekRes.status,
        headers: { ...respHeaders, 'Content-Type': 'application/json' },
      });
    }

    return new Response(deepseekRes.body, {
      headers: {
        ...respHeaders,
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
      },
    });
  } catch (e) {
    console.error('DeepSeek request failed:', e.message);
    return json({ error: `请求失败：${e.message}` }, 500);
  }
}

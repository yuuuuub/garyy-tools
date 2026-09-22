// 百度 OCR 识别八字文字 API
// 修复: imageBase64 大小限制(防 DOS)、token 缓存健壮性、错误日志
const MAX_IMAGE_SIZE = 5 * 1024 * 1024; // 5MB 上限

let cachedToken = null;
let tokenExpiry = 0;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
  });
}

export async function onRequest(context) {
  const { request, env } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (request.method !== 'POST') {
    return json({ error: '方法不允许' }, 405);
  }

  const apiKey = env.BAIDU_OCR_API_KEY;
  const secretKey = env.BAIDU_OCR_SECRET_KEY;

  if (!apiKey || !secretKey) {
    return json({ error: '请在 Cloudflare Pages 环境变量中设置 BAIDU_OCR_API_KEY 和 BAIDU_OCR_SECRET_KEY' }, 500);
  }

  try {
    const body = await request.json();
    const { imageBase64 } = body;

    if (!imageBase64) {
      return json({ error: '缺少 imageBase64 参数' }, 400);
    }

    // 输入大小限制（防 DOS）
    if (typeof imageBase64 !== 'string' || imageBase64.length > MAX_IMAGE_SIZE) {
      return json({ error: `图片数据过大，上限 ${MAX_IMAGE_SIZE / 1024 / 1024}MB` }, 413);
    }

    // token 缓存：失效前 5 分钟提前刷新
    const now = Date.now();
    if (!cachedToken || now >= tokenExpiry) {
      const tokenRes = await fetch(
        `https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=${apiKey}&client_secret=${secretKey}`,
        { method: 'POST' }
      );
      const tokenData = await tokenRes.json();

      if (!tokenData.access_token) {
        console.error('Baidu token auth failed:', tokenData.error_description || tokenData.error);
        return json({ error: `百度鉴权失败：${tokenData.error_description || tokenData.error || '未知错误'}` }, 500);
      }

      cachedToken = tokenData.access_token;
      // 提前 5 分钟过期，避免边界失效
      const ttl = Math.max(60, (tokenData.expires_in || 3600) - 300);
      tokenExpiry = now + ttl * 1000;
    }

    // 调用 OCR
    const formData = new URLSearchParams();
    formData.append('image', imageBase64);

    const ocrRes = await fetch(
      `https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=${cachedToken}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      }
    );

    const ocrData = await ocrRes.json();

    if (ocrData.error_code) {
      console.error('Baidu OCR error:', ocrData.error_code, ocrData.error_msg);
      return json({ error: `百度 OCR 错误：${ocrData.error_msg}` }, 500);
    }

    const words = ocrData.words_result?.map(w => w.words) || [];
    return json({ rawText: words.join('\n') });

  } catch (e) {
    console.error('Baidu OCR request failed:', e.message);
    return json({ error: `请求失败：${e.message}` }, 500);
  }
}

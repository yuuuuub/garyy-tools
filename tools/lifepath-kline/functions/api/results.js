// 命运K线 结果存取 API
// 修复: 隐私泄露(无 key 时不返回姓名/八字)、静默 catch、key 格式校验、写入频率限制
const MAX_KEY_LENGTH = 128;
const MAX_RAW_TEXT_LENGTH = 10000;
const MAX_RESULT_LENGTH = 200000;
const WRITE_COOLDOWN_MS = 5000; // 同一 key 最小写入间隔
const RECENT_LIMIT = 10;

// 简单内存级写入限流（按 key）— Cloudflare workers 实例级缓存
const lastWriteMap = new Map();

function isValidKey(key) {
  return typeof key === 'string' && key.length > 0 && key.length <= MAX_KEY_LENGTH && /^[a-zA-Z0-9_-]+$/.test(key);
}

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
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }

  if (!env.DB) {
    return json({ error: 'D1 数据库未绑定' }, 500);
  }

  // 自动建表 + 兼容字段（修复静默 catch：记录错误到 stderr）
  try {
    await env.DB.prepare(`
      CREATE TABLE IF NOT EXISTS results (
        cache_key TEXT PRIMARY KEY,
        name TEXT NOT NULL DEFAULT '',
        gender TEXT NOT NULL DEFAULT '',
        raw_text TEXT NOT NULL DEFAULT '',
        result_json TEXT NOT NULL,
        created_at INTEGER NOT NULL
      )
    `).run();
  } catch (e) {
    console.error('CREATE TABLE failed:', e.message);
  }
  for (const col of ['image_base64 TEXT', 'bazi_sections TEXT']) {
    try {
      await env.DB.prepare(`ALTER TABLE results ADD COLUMN ${col}`).run();
    } catch (e) {
      // 字段已存在属正常情况；其他错误才记录
      if (!/duplicate column|already exists/i.test(e.message)) {
        console.error('ALTER TABLE failed:', e.message);
      }
    }
  }

  if (request.method === 'GET') {
    const url = new URL(request.url);
    const key = url.searchParams.get('key');

    try {
      // 无 key → 仅返回总数和最近记录的时间戳，不泄露姓名/八字（修复隐私泄露）
      if (!key) {
        const { results: countResult } = await env.DB.prepare(
          'SELECT COUNT(*) as total FROM results'
        ).all();
        const { results: latest } = await env.DB.prepare(
          'SELECT created_at FROM results ORDER BY created_at DESC LIMIT ?'
        ).bind(RECENT_LIMIT).all();
        return json({
          total: countResult[0]?.total || 0,
          latest: latest.map(r => ({ time: new Date(r.created_at).toISOString() })),
        });
      }

      // 有 key → 校验格式后返回完整结果
      if (!isValidKey(key)) {
        return json({ error: 'key 格式不合法' }, 400);
      }
      const { results } = await env.DB.prepare(
        'SELECT result_json FROM results WHERE cache_key = ?'
      ).bind(key).all();

      if (results.length > 0) {
        return new Response(results[0].result_json, {
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        });
      }
      return json(null);
    } catch (e) {
      console.error('GET results failed:', e.message);
      return json({ error: '查询失败' }, 500);
    }
  }

  if (request.method === 'POST') {
    try {
      const body = await request.json();
      const { key, name, gender, rawText, result, sections } = body;

      // key 校验
      if (!isValidKey(key)) {
        return json({ error: '缺少 key 或 key 格式不合法' }, 400);
      }

      // 写入限流：同一 key 5 秒内只能写一次
      const now = Date.now();
      const last = lastWriteMap.get(key) || 0;
      if (now - last < WRITE_COOLDOWN_MS) {
        return json({ error: '写入过于频繁，请稍后再试' }, 429);
      }
      lastWriteMap.set(key, now);

      // 输入长度限制
      const safeName = String(name || '').slice(0, 50);
      const safeGender = String(gender || '').slice(0, 10);
      const safeRaw = String(rawText || '').slice(0, MAX_RAW_TEXT_LENGTH);

      if (sections && !result) {
        const safeSections = JSON.stringify(sections).slice(0, MAX_RESULT_LENGTH);
        await env.DB.prepare(
          'INSERT OR REPLACE INTO results (cache_key, name, gender, raw_text, result_json, bazi_sections, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
        ).bind(key, safeName, safeGender, safeRaw, '{}', safeSections, now).run();
        return json({ ok: true });
      }

      if (!result) {
        return json({ error: '缺少 result' }, 400);
      }
      const safeResult = JSON.stringify(result).slice(0, MAX_RESULT_LENGTH);
      await env.DB.prepare(
        'INSERT OR REPLACE INTO results (cache_key, name, gender, raw_text, result_json, created_at) VALUES (?, ?, ?, ?, ?, ?)'
      ).bind(key, safeName, safeGender, safeRaw, safeResult, now).run();

      return json({ ok: true });
    } catch (e) {
      console.error('POST results failed:', e.message);
      return json({ error: '写入失败' }, 500);
    }
  }

  return json({ error: '不允许的方法' }, 405);
}

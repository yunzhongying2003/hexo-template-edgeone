// EdgeOne Pages Function — 文章阅读计数
// KV binding: blog_count
// KV key 限制：仅支持数字、字母及下划线 → 用 _ 替代 : / 等非法字符
//
// GET /api/views?slug=2026_05_28_post-title  → 记录+1并返回
// GET /api/views?slug=xxx&readonly=true       → 只读不计数

export async function onRequest({ request, env }) {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');
  const readonly = url.searchParams.get('readonly') === 'true';

  if (!slug) {
    return new Response(JSON.stringify({ error: 'Missing slug' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // KV key 仅支持数字、字母及下划线
  const key = `views_${slug}`;

  try {
    const raw = await env.blog_count.get(key);
    let count = parseInt(raw || '0', 10);

    if (!readonly) {
      count += 1;
      await env.blog_count.put(key, String(count));
    }

    return new Response(JSON.stringify({ slug, count }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

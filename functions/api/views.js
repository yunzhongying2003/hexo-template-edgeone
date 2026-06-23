// EdgeOne Pages Function — 文章阅读计数
// KV binding: blog_count
// GET /api/views?slug=2026/05/28/post-title  → 记录+1并返回
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

  const key = `views:${slug}`;
  let count = parseInt(await env.blog_count.get(key) || '0', 10);

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
}

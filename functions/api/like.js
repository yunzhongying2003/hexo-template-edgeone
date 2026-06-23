// EdgeOne Pages Function — 文章点赞/反应
// KV binding: blog_count
// POST /api/like?slug=2026/05/28/post-title&reaction=heart
// GET  /api/like?slug=2026/05/28/post-title  → 返回所有反应计数

const VALID_REACTIONS = ['heart', 'star', 'fire', 'clap', 'like'];

export async function onRequest({ request, env }) {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');

  if (!slug) {
    return new Response(JSON.stringify({ error: 'Missing slug' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // POST: 记录一个反应
  if (request.method === 'POST') {
    const reaction = url.searchParams.get('reaction') || 'heart';
    if (!VALID_REACTIONS.includes(reaction)) {
      return new Response(JSON.stringify({ error: `Invalid reaction: ${reaction}` }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const key = `like:${slug}:${reaction}`;
    let count = parseInt(await env.blog_count.get(key) || '0', 10);
    count += 1;
    await env.blog_count.put(key, String(count));

    return new Response(JSON.stringify({ slug, reaction, count }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      }
    });
  }

  // GET: 返回所有反应计数
  const reactions = {};
  for (const r of VALID_REACTIONS) {
    const key = `like:${slug}:${r}`;
    const val = await env.blog_count.get(key);
    reactions[r] = val ? parseInt(val, 10) : 0;
  }

  return new Response(JSON.stringify({ slug, reactions }), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store'
    }
  });
}
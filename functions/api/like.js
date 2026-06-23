// EdgeOne Pages Function — 文章点赞/反应
// KV binding: blog_count
// KV key 限制：仅支持数字、字母及下划线 → key 用 _ 替代非法字符
//
// POST /api/like?slug=2026_05_28_post-title&reaction=heart
// GET  /api/like?slug=2026_05_28_post-title  → 返回所有反应计数

const VALID_REACTIONS = ['heart', 'star', 'fire', 'clap', 'like'];

export async function onRequest({ request }) {
  const url = new URL(request.url);
  const slug = url.searchParams.get('slug');

  if (!slug) {
    return new Response(JSON.stringify({ error: 'Missing slug' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    // POST: 记录一个反应
    if (request.method === 'POST') {
      const reaction = url.searchParams.get('reaction') || 'heart';
      if (!VALID_REACTIONS.includes(reaction)) {
        return new Response(JSON.stringify({ error: `Invalid reaction: ${reaction}` }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // KV key 仅支持数字、字母及下划线
      const key = `like_${slug}_${reaction}`;
      const raw = await blog_count.get(key);
      let count = parseInt(raw || '0', 10);
      count += 1;
      await blog_count.put(key, String(count));

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
      const key = `like_${slug}_${r}`;
      const val = await blog_count.get(key);
      reactions[r] = val ? parseInt(val, 10) : 0;
    }

    return new Response(JSON.stringify({ slug, reactions }), {
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
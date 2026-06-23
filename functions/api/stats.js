// EdgeOne Pages Function — 全站统计
// KV binding: blog_count
// GET /api/stats → { total_views, total_heart, total_star, ... }

export async function onRequest() {
  try {
    const totalRaw = await blog_count.get('total_views');
    const total = parseInt(totalRaw || '0', 10);

    return new Response(JSON.stringify({ total_views: total }), {
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
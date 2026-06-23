// EdgeOne Pages Function — 列出待审 FAQ
// KV binding: blog_count
// GET /api/faq-pending?limit=20
// 鉴权方式：Header X-FAQ-Key 或 URL 参数 ?key=<FAQ_API_KEY>

export async function onRequest(context) {
  try {
    const request = context.request;
    if (request.method !== 'GET') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405, headers: { 'Content-Type': 'application/json' }
      });
    }

    const FAQ_KEY = (context.env && context.env.FAQ_API_KEY) || (typeof FAQ_API_KEY !== 'undefined' ? FAQ_API_KEY : '');

    const url = new URL(request.url);
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '20', 10) || 20, 50);
    // 支持 Header 和 URL 参数两种鉴权
    const apiKey = request.headers.get('X-FAQ-Key') || url.searchParams.get('key') || '';

    if (!apiKey || apiKey !== FAQ_KEY) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401, headers: { 'Content-Type': 'application/json' }
      });
    }

    const indexRaw = await blog_count.get('faq_pending_index');
    const ids = indexRaw ? JSON.parse(indexRaw) : [];
    const items = [];

    for (const id of ids) {
      const raw = await blog_count.get(`faq_pending_${id}`);
      if (raw) {
        try { items.push(JSON.parse(raw)); } catch {}
      }
    }

    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return new Response(JSON.stringify({ total: items.length, items: items.slice(0, limit) }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
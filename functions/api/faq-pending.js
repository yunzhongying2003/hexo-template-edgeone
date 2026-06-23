// EdgeOne Pages Function — 列出待审 FAQ
// KV binding: blog_count
// GET /api/faq-pending?limit=20
// Header: X-FAQ-Key: <FAQ_API_KEY>

export async function onRequest(context) {
  try {
    const request = context.request;
    if (request.method !== 'GET') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const FAQ_KEY = (context.env && context.env.FAQ_API_KEY) || (typeof FAQ_API_KEY !== 'undefined' ? FAQ_API_KEY : '');
    const apiKey = request.headers.get('X-FAQ-Key');
    if (!apiKey || apiKey !== FAQ_KEY) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const url = new URL(request.url);
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '20', 10) || 20, 50);

    const result = await blog_count.list('faq_pending_');
    const items = [];

    for (const key of result.keys) {
      const raw = await blog_count.get(key.name);
      if (raw) {
        try { items.push(JSON.parse(raw)); } catch {}
      }
    }

    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return new Response(JSON.stringify({ total: items.length, items: items.slice(0, limit) }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
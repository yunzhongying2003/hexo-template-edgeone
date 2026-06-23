// EdgeOne Pages Function — 审批 FAQ（批准/拒绝）
// KV binding: blog_count
// POST /api/faq/review
// Body: { id, action: 'approve' | 'reject' }
// Header: X-FAQ-Key: <FAQ_API_KEY>

export async function onRequest({ request }) {
  if (request.method !== 'POST') {
    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // 验证 API Key
  const apiKey = request.headers.get('X-FAQ-Key');
  const envKey = typeof FAQ_API_KEY !== 'undefined' ? FAQ_API_KEY : '';
  if (!apiKey || apiKey !== envKey) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const body = await request.json();
    const { id, action } = body;

    if (!id || !action || !['approve', 'reject'].includes(action)) {
      return new Response(JSON.stringify({
        error: 'Missing or invalid fields. Required: id, action (approve|reject)'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const fromKey = `faq_pending:${id}`;
    const raw = await blog_count.get(fromKey);

    if (!raw) {
      return new Response(JSON.stringify({ error: 'FAQ not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // 读取已有数据，加上审核时间
    let data;
    try { data = JSON.parse(raw); } catch { data = { id }; }
    data.reviewed_at = new Date().toISOString();

    const toKey = action === 'approve' ? `faq_approved:${id}` : `faq_rejected:${id}`;
    await blog_count.put(toKey, JSON.stringify(data));
    await blog_count.delete(fromKey);

    return new Response(JSON.stringify({ ok: true, action, id }), {
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
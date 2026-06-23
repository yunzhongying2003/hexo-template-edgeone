// EdgeOne Pages Function — 删除 FAQ（pending 或 approved 均可）
// KV binding: blog_count
// POST /api/faq-delete
// Body: { id }
// Header: X-FAQ-Key: <FAQ_API_KEY>

export async function onRequest(context) {
  try {
    const request = context.request;
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405, headers: { 'Content-Type': 'application/json' }
      });
    }

    const FAQ_KEY = (context.env && context.env.FAQ_API_KEY) || (typeof FAQ_API_KEY !== 'undefined' ? FAQ_API_KEY : '');
    const apiKey = request.headers.get('X-FAQ-Key');
    if (!apiKey || apiKey !== FAQ_KEY) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401, headers: { 'Content-Type': 'application/json' }
      });
    }

    const body = await request.json();
    const { id } = body;
    if (!id) {
      return new Response(JSON.stringify({ error: 'Missing id' }), {
        status: 400, headers: { 'Content-Type': 'application/json' }
      });
    }

    let deleted = false;

    // 尝试从 pending 删除
    const pendingKey = `faq_pending_${id}`;
    const pendingRaw = await blog_count.get(pendingKey);
    if (pendingRaw) {
      await blog_count.delete(pendingKey);
      // 从 pending 索引移除
      const indexRaw = await blog_count.get('faq_pending_index');
      if (indexRaw) {
        const index = JSON.parse(indexRaw);
        const idx = index.indexOf(id);
        if (idx !== -1) {
          index.splice(idx, 1);
          await blog_count.put('faq_pending_index', JSON.stringify(index));
        }
      }
      deleted = true;
    }

    // 尝试从 approved 删除
    if (!deleted) {
      const approvedKey = `faq_approved_${id}`;
      const approvedRaw = await blog_count.get(approvedKey);
      if (approvedRaw) {
        await blog_count.delete(approvedKey);
        // 从 approved 索引移除
        const idxRaw = await blog_count.get('faq_approved_index');
        if (idxRaw) {
          const idxList = JSON.parse(idxRaw);
          const idx = idxList.indexOf(id);
          if (idx !== -1) {
            idxList.splice(idx, 1);
            await blog_count.put('faq_approved_index', JSON.stringify(idxList));
          }
        }
        deleted = true;
      }
    }

    if (!deleted) {
      return new Response(JSON.stringify({ error: 'FAQ not found' }), {
        status: 404, headers: { 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ ok: true, deleted: id }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
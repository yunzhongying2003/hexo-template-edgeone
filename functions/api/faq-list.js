// EdgeOne Pages Function — 列出所有已发布 FAQ
// KV binding: blog_count
// GET /api/faq-list?limit=50
// 公开访问（只返回已批准的 FAQ，不需要鉴权）

export async function onRequest(context) {
  try {
    const url = new URL(context.request.url);
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '50', 10) || 50, 100);

    const indexRaw = await blog_count.get('faq_approved_index');
    const ids = indexRaw ? JSON.parse(indexRaw) : [];
    const items = [];

    for (const id of ids) {
      const raw = await blog_count.get(`faq_approved_${id}`);
      if (raw) {
        try {
          const faq = JSON.parse(raw);
          // 摘要：取 answer 前 120 字
          const summary = (faq.answer || '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 120) + ((faq.answer || '').length > 120 ? '…' : '');
          items.push({
            id: faq.id,
            question: faq.question,
            summary,
            article_title: faq.article_title || '(无关联文章)',
            article_url: faq.article_url || '',
            status: 'approved',
            created_at: faq.created_at
          });
        } catch {}
      }
    }

    // 按时间倒序
    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return new Response(JSON.stringify({ total: items.length, items: items.slice(0, limit) }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
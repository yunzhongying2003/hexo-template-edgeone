// EdgeOne Pages Function — 查询某篇文章的已发布 FAQ
// KV binding: blog_count
// GET /api/faq-by-article?path=/2026/06/19/hermes-cron-job-guide-2026/
// 公开可访问（无需鉴权）

export async function onRequest(context) {
  try {
    const request = context.request;
    const url = new URL(request.url);
    const articlePath = url.searchParams.get('path') || '';

    if (!articlePath) {
      return new Response(JSON.stringify({ total: 0, items: [] }), {
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=300' }
      });
    }

    const indexRaw = await blog_count.get('faq_approved_index');
    const ids = indexRaw ? JSON.parse(indexRaw) : [];
    const items = [];

    for (const id of ids) {
      const raw = await blog_count.get(`faq_approved_${id}`);
      if (raw) {
        try {
          const faq = JSON.parse(raw);
          // 匹配文章路径（支持包含 www 和不含两种）
          if (faq.article_url && faq.article_url.includes(articlePath)) {
            items.push(faq);
          }
        } catch {}
      }
    }

    // 按时间倒序
    items.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return new Response(JSON.stringify({ total: items.length, items }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=300' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500, headers: { 'Content-Type': 'application/json' }
    });
  }
}
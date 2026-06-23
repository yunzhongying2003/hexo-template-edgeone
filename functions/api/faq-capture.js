// EdgeOne Pages Function — 捕获 FAQ 待审
// KV binding: blog_count
// POST /api/faq-capture
// Body: { question, answer, article_url?, article_title? }
// Header: X-FAQ-Key: <FAQ_API_KEY>

export async function onRequest(context) {
  try {
    const request = context.request;
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // 环境变量：优先 context.env，降级全局
    const FAQ_KEY = (context.env && context.env.FAQ_API_KEY) || (typeof FAQ_API_KEY !== 'undefined' ? FAQ_API_KEY : '');
    if (!FAQ_KEY) {
      return new Response(JSON.stringify({ error: 'FAQ_API_KEY not configured' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const apiKey = request.headers.get('X-FAQ-Key');
    if (!apiKey || apiKey !== FAQ_KEY) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const body = await request.json();
    const id = Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
    const data = JSON.stringify({
      id,
      question: (body.question || '').slice(0, 2000),
      answer: (body.answer || '').slice(0, 5000),
      article_url: body.article_url || '',
      article_title: body.article_title || '',
      created_at: new Date().toISOString()
    });

    await blog_count.put(`faq_pending_${id}`, data);

    return new Response(JSON.stringify({ captured: true, id }), {
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: e.message || String(e) }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
// EdgeOne Pages Function — 捕获 FAQ 待审
// KV binding: blog_count
// POST /api/faq/capture
// Body: { question, answer, article_url?, article_title? }
// Header: X-FAQ-Key: <FAQ_API_KEY>

export async function onRequest({ request }) {
  // 只接受 POST
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
    const { question, answer, article_url, article_title } = body;

    if (!question || !answer) {
      return new Response(JSON.stringify({ error: 'Missing required fields: question, answer' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // 生成唯一 ID（边缘函数环境没有 crypto.randomUUID，用时间戳 + 随机数替代）
    const id = Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
    const key = `faq_pending_${id}`;
    const data = {
      id,
      question: question.slice(0, 2000),
      answer: answer.slice(0, 5000),
      article_url: article_url || '',
      article_title: article_title || '',
      created_at: new Date().toISOString()
    };

    await blog_count.put(key, JSON.stringify(data));

    return new Response(JSON.stringify({ captured: true, id }), {
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
// Blog 互动功能：阅读计数 + 点赞/反应
// 仅对文章页面生效（路径匹配 /YYYY/MM/DD/title/）

(function() {
  'use strict';

  const path = window.location.pathname;
  const isPost = /^\/(\d{4}\/\d{2}\/\d{2}\/)/.test(path);
  if (!isPost) return;

  const slug = path.replace(/^\//, '').replace(/\/$/, '').replace(/\//g, '_');

  // ========== 阅读计数 ==========
  async function loadViews() {
    try {
      const res = await fetch(`/api/views?slug=${encodeURIComponent(slug)}`);
      const data = await res.json();
      const el = document.getElementById('blog-views-count');
      if (el) el.textContent = data.count;
    } catch (e) { /* API unavailable */ }
  }

  // ========== 点赞/反应 ==========
  const REACTIONS = [
    { id: 'heart', icon: '\u2764\uFE0F', label: '\u7231\u5FC3' },
    { id: 'star', icon: '\u2B50', label: '\u6536\u85CF' },
    { id: 'fire', icon: '\uD83D\uDD25', label: '\u706B' },
    { id: 'clap', icon: '\uD83D\uDC4F', label: '\u9F13\u638C' },
    { id: 'like', icon: '\uD83D\uDC4D', label: '\u8D5E' }
  ];

  async function loadReactions() {
    try {
      const res = await fetch(`/api/like?slug=${encodeURIComponent(slug)}`);
      const data = await res.json();
      return data.reactions || {};
    } catch (e) { return {}; }
  }

  async function sendReaction(reaction) {
    try {
      const res = await fetch(`/api/like?slug=${encodeURIComponent(slug)}&reaction=${reaction}`, { method: 'POST' });
      const data = await res.json();
      return data.count;
    } catch (e) { return null; }
  }

  // ========== 注入 UI ==========
  function injectUI() {
    const footer = document.querySelector('.post-footer');
    if (!footer) return;

    const isDark = document.querySelector('html[data-user-color-scheme="dark"]')

    // 阅读计数行
    const viewsHTML = `
      <div class="blog-interaction-bar" style="margin-top:20px;padding-top:15px;border-top:1px solid var(--border-color,#eee);display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
        <span style="color:var(--text-color,#999);font-size:13px;">
          \uD83D\uDC41\uFE0F \u9605\u8BFB <span id="blog-views-count" style="font-weight:bold;">-</span> \u6B21
        </span>
      </div>
    `;
    footer.insertAdjacentHTML('beforebegin', viewsHTML);

    // 反应按钮行
    let reactionsHTML = '<div class="blog-reactions-bar" style="margin-top:12px;margin-bottom:24px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;">';
    REACTIONS.forEach(r => {
      reactionsHTML += `
        <button class="blog-reaction-btn" data-reaction="${r.id}"
          style="display:inline-flex;align-items:center;gap:4px;padding:6px 12px;border:1px solid ${isDark ? '#444' : '#e0e0e0'};border-radius:20px;background:transparent;cursor:pointer;font-size:14px;transition:all 0.15s;line-height:1;"
          title="${r.label}">
          <span>${r.icon}</span>
          <span class="reaction-count" data-reaction="${r.id}" style="font-size:12px;color:#999;min-width:16px;text-align:center;">-</span>
        </button>
      `;
    });
    reactionsHTML += '</div>';
    footer.insertAdjacentHTML('beforebegin', reactionsHTML);

    // 绑定点击
    document.querySelectorAll('.blog-reaction-btn').forEach(btn => {
      btn.addEventListener('click', async function() {
        const reaction = this.dataset.reaction;
        const countEl = this.querySelector('.reaction-count');
        this.style.transform = 'scale(0.85)';
        setTimeout(() => this.style.transform = 'scale(1)', 200);

        const newCount = await sendReaction(reaction);
        if (newCount !== null) {
          countEl.textContent = newCount;
        }
      });
    });
  }

  // ========== Markdown 渲染 ==========
  function renderMarkdown(text) {
    if (!text) return '';
    let h = text
      // 表格块：连续 | 开头的行，跳过分隔行 (---|---)
      .replace(/(^\|.+\n?)+/gm, function(block) {
        var rows = block.trim().split('\n').filter(function(r) {
          return r.trim() && !/^\|[\s:-]+\|/.test(r.trim());
        });
        if (rows.length === 0) return block;
        var tableRows = rows.map(function(r) {
          var cells = r.slice(1,-1).split('|').map(function(c){return c.trim()});
          return '<tr><td style="padding:4px 8px;border:1px solid #ddd;font-size:12px">' + cells.join('</td><td style="padding:4px 8px;border:1px solid #ddd;font-size:12px">') + '</td></tr>';
        });
        return '<table style="border-collapse:collapse;margin:8px 0;width:100%">' + tableRows.join('') + '</table>';
      })
      // 代码块 ``` ``` → <pre><code>
      .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
      // 行内代码
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      // 图片 ![alt](url)
      .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width:100%">')
      // 链接 [text](url)
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
      // 加粗 **text**
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      // 斜体 *text*
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      // 标题 ### text → h4
      .replace(/^### (.+)$/gm, '<h4 style="margin:8px 0 4px;font-size:14px">$1</h4>')
      .replace(/^## (.+)$/gm, '<h3 style="margin:10px 0 4px;font-size:15px">$1</h3>')
      // 无序列表 - item
      .replace(/^- (.+)$/gm, '<li style="margin:2px 0">$1</li>')
      .replace(/(<li[^>]*>.*<\/li>\n?)+/g, '<ul style="padding-left:16px;margin:4px 0">$&</ul>')
      // 换行
      .replace(/\n\n/g, '</p><p style="margin:6px 0">')
      .replace(/\n/g, '<br>');
    return '<p style="margin:6px 0">' + h + '</p>';
  }

  // ========== FAQ 展示 ==========
  async function loadFAQs() {
    try {
      const path = window.location.pathname.replace(/\/$/, '');
      const res = await fetch(`/api/faq-by-article?path=${encodeURIComponent(path)}`);
      const data = await res.json();
      if (!data.items || data.items.length === 0) return;

      const footer = document.querySelector('.post-footer');
      if (!footer) return;

      let html = '<div class="faq-section" style="margin-top:32px;padding-top:20px;border-top:1px solid var(--border-color,#eee);">';
      html += '<h3 style="font-size:16px;font-weight:600;margin:0 0 12px 0;color:var(--text-color,#333);">\u2753 \u5E38\u89C1\u95EE\u7B54</h3>';

      data.items.forEach((faq, i) => {
        html += '<div class="faq-item" style="margin-bottom:8px;border:1px solid var(--border-color,#eee);border-radius:8px;overflow:hidden;">';
        html += '<button class="faq-question" data-index="' + i + '" style="width:100%;display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border:none;background:var(--bg-color,#f9f9f9);cursor:pointer;font-size:14px;color:var(--text-color,#333);text-align:left;transition:background 0.15s;">';
        html += '<span>' + faq.question + '</span>';
        html += '<span class="faq-toggle" style="font-size:12px;transition:transform 0.2s;">\u25BC</span>';
        html += '</button>';
        html += '<div class="faq-answer" style="display:none;padding:10px 14px;font-size:13px;line-height:1.6;color:var(--text-color,#555);background:#fff;border-top:1px solid var(--border-color,#eee);">';
        html += renderMarkdown(faq.answer);
        html += '</div></div>';
      });

      html += '</div>';
      footer.insertAdjacentHTML('beforebegin', html);

      // 绑定点击展开/收起
      document.querySelectorAll('.faq-question').forEach(btn => {
        btn.addEventListener('click', function() {
          const answer = this.nextElementSibling;
          const toggle = this.querySelector('.faq-toggle');
          if (answer.style.display === 'none' || answer.style.display === '') {
            answer.style.display = 'block';
            toggle.style.transform = 'rotate(180deg)';
          } else {
            answer.style.display = 'none';
            toggle.style.transform = 'rotate(0deg)';
          }
        });
      });
    } catch (e) { /* FAQ API unavailable */ }
  }

  // ========== 初始化 ==========
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  async function init() {
    injectUI();
    loadViews();
    const reactions = await loadReactions();
    document.querySelectorAll('.reaction-count').forEach(el => {
      const r = el.dataset.reaction;
      el.textContent = reactions[r] || 0;
    });
    loadFAQs();
  }
})();
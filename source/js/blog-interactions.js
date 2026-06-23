// Blog 互动功能：阅读计数 + 点赞/反应
// 仅对文章页面生效（路径匹配 /YYYY/MM/DD/title/）

(function() {
  'use strict';

  const path = window.location.pathname;
  const isPost = /^\/(\d{4}\/\d{2}\/\d{2}\/)/.test(path);
  if (!isPost) return;

  const slug = path.replace(/^\//, '').replace(/\/$/, '');

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
  }
})();
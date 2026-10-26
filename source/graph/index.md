---
title: 文章关系图谱
layout: page-graph
permalink: /graph/
---

<script src="https://unpkg.com/vis-network@9.1.9/dist/vis-network.min.js"></script>

<div id="graph-canvas">
    <div id="loading" class="graph-loading">📊 加载图谱中...</div>
    <div id="network"></div>
</div>

<!-- 控制条 -->
<div id="graph-controls">
    <div class="gc-head">
        <span class="gc-title"><span class="gc-ico">🕸</span> 关系图谱</span>
        <button id="btn-focus" class="gc-btn-icon" title="聚焦中心文章 (1 度子图)">◎</button>
    </div>
    <div class="gc-row">
        <div class="gc-search">
            <span class="gc-search-ico">🔍</span>
            <input id="search-input" type="text" placeholder="搜索文章标题…" autocomplete="off" spellcheck="false">
            <span id="search-count"></span>
        </div>
        <div class="gc-search-list" id="search-list"></div>
    </div>
    <div class="gc-row">
        <div class="gc-depth">
            <div class="gc-depth-head">
                <span>查看深度</span>
                <span id="depth-val">全部</span>
            </div>
            <input id="depth-slider" type="range" min="0" max="3" step="1" value="0">
            <div class="gc-depth-hint" id="depth-hint">聚焦文章后调整</div>
        </div>
    </div>
    <div class="gc-sep"></div>
    <div class="gc-row">
        <div class="gc-legend-title">分类（点击筛选）</div>
        <div id="legend"></div>
    </div>
</div>

<!-- 图头信息 -->
<div id="graph-header">
    <div id="g-title">文章关系图谱</div>
    <div id="g-sub">点击节点聚焦 · ↑↓ 切换搜索结果 · Esc 重置</div>
</div>

<!-- 底部统计 -->
<div id="graph-footer"></div>

<!-- Info panel -->
<div class="graph-info-panel" id="info-panel">
    <button class="graph-close" onclick="closePanel()">✕</button>
    <h3 id="info-title"></h3>
    <div class="graph-meta" id="info-date"></div>
    <div class="graph-tags" id="info-tags"></div>
    <div class="graph-related-header" id="related-header" style="display:none">相关文章</div>
    <div class="graph-links" id="info-links"></div>
</div>

<!-- Custom tooltip -->
<div id="graph-tooltip" class="graph-tooltip"></div>

<style>
/* ============================================
   Layout — hide headband, full-height canvas
   ============================================ */
.headband { display: none !important; }
.post-content {
    padding: 0 !important;
    margin: 0 !important;
    background: none !important;
    box-shadow: none !important;
    border-radius: 0 !important;
}
.main-inner {
    padding: 0 !important;
    min-height: calc(100vh - 80px) !important;
}
#graph-canvas {
    width: 100%;
    height: calc(100vh - 80px);
    position: relative;
    display: flex;
    overflow: hidden;
}
#network { width: 100%; height: 100%; flex: 1; }

/* ============================================
   Theme variables — matches NexT Pisces
   ============================================ */
:root {
    --bg: #ffffff;
    --bg-alt: #f8fafc;
    --primary: #2563eb;
    --primary-light: rgba(37, 99, 235, 0.08);
    --text: #1a1a2e;
    --text-secondary: #64748b;
    --border: #e2e8f0;
    --card-bg: rgba(255, 255, 255, 0.88);
    --card-border: #e2e8f0;
    --shadow: 0 10px 34px rgba(15, 23, 42, 0.12);
    --shadow-sm: 0 4px 14px rgba(15, 23, 42, 0.09);
    --node-hermes: #2563eb;
    --node-ai: #16a34a;
    --node-dev: #d97706;
    --node-other: #64748b;
    --edge-color: rgba(100, 116, 139, 0.32);
    --edge-color-hover: rgba(37, 99, 235, 0.65);
    --canvas-bg-1: #ffffff;
    --canvas-bg-2: #eef1f7;
    --focus-glow: rgba(37, 99, 235, 0.5);
}
[data-theme="dark"] {
    --bg: #0f172a;
    --bg-alt: #1e293b;
    --primary: #60a5fa;
    --primary-light: rgba(96, 165, 250, 0.13);
    --text: #e2e8f0;
    --text-secondary: #94a3b8;
    --border: #334155;
    --card-bg: rgba(30, 41, 59, 0.9);
    --card-border: #334155;
    --shadow: 0 10px 34px rgba(0, 0, 0, 0.5);
    --shadow-sm: 0 4px 14px rgba(0, 0, 0, 0.4);
    --node-hermes: #60a5fa;
    --node-ai: #4ade80;
    --node-dev: #fbbf24;
    --node-other: #94a3b8;
    --edge-color: rgba(148, 163, 184, 0.28);
    --edge-color-hover: rgba(96, 165, 250, 0.6);
    --canvas-bg-1: #101a2e;
    --canvas-bg-2: #0a101f;
    --focus-glow: rgba(96, 165, 250, 0.55);
}

/* ============================================
   Loading
   ============================================ */
.graph-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: var(--primary);
    font-size: 0.95em;
    z-index: 200;
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    padding: 12px 22px;
    border-radius: 12px;
    box-shadow: var(--shadow-sm);
}
.graph-loading.hidden { display: none; }

/* ============================================
   Control panel
   ============================================ */
#graph-controls {
    position: absolute;
    top: 16px;
    left: 16px;
    width: 268px;
    max-height: calc(100% - 32px);
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    box-shadow: var(--shadow);
    padding: 13px 14px;
    z-index: 90;
}
#graph-controls::-webkit-scrollbar { width: 4px; }
#graph-controls::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.gc-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
.gc-title {
    font-size: 0.9em;
    font-weight: 700;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 7px;
}
.gc-ico { font-size: 1.05em; }
.gc-btn-icon {
    background: var(--primary-light);
    border: 1px solid transparent;
    color: var(--primary);
    width: 27px;
    height: 27px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    line-height: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color .18s, color .18s;
}
.gc-btn-icon:hover { border-color: var(--primary); }
.gc-btn-icon.off { opacity: 0.35; }
.gc-btn-icon .tip { display: none; }

.gc-row { margin-bottom: 10px; }
.gc-row:last-child { margin-bottom: 0; }
.gc-sep {
    height: 1px;
    background: var(--border);
    margin: 11px 0;
    opacity: 0.8;
}

.gc-search {
    position: relative;
    display: flex;
    align-items: center;
    background: var(--bg-alt);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 0 9px;
    transition: border-color .18s;
}
.gc-search:focus-within { border-color: var(--primary); }
.gc-search-ico {
    font-size: 11px;
    opacity: 0.55;
    margin-right: 6px;
}
.gc-search input {
    flex: 1;
    border: 0;
    background: transparent;
    outline: 0;
    color: var(--text);
    font-size: 0.82em;
    padding: 8px 0;
    min-width: 0;
    font-family: inherit;
}
.gc-search input::placeholder { color: var(--text-secondary); opacity: 0.8; }
#search-count {
    font-size: 0.68em;
    color: var(--primary);
    font-weight: 700;
    margin-left: 6px;
    white-space: nowrap;
}

.gc-search-list { margin-top: 6px; display: none; }
.gc-search-list.show { display: block; }
.gc-search-list .si {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 9px;
    font-size: 0.75em;
    color: var(--text);
    cursor: pointer;
    border-radius: 7px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.3;
}
.gc-search-list .si:hover { background: var(--primary-light); }
.gc-search-list .si.sel {
    background: var(--primary-light);
    color: var(--primary);
    font-weight: 600;
}
.gc-search-list .si i {
    font-style: normal;
    font-size: 0.88em;
    color: var(--text-secondary);
    flex-shrink: 0;
}

.gc-depth-head {
    display: flex;
    justify-content: space-between;
    font-size: 0.78em;
    color: var(--text-secondary);
    font-weight: 600;
    margin-bottom: 3px;
}
.gc-depth-head #depth-val {
    color: var(--primary);
    font-weight: 700;
}
#depth-slider {
    width: 100%;
    height: 4px;
    -webkit-appearance: none;
    appearance: none;
    background: var(--border);
    border-radius: 2px;
    outline: none;
    margin: 5px 0 4px;
}
#depth-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--primary);
    cursor: pointer;
    border: 2px solid #fff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.35);
}
#depth-slider::-moz-range-thumb {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: var(--primary);
    cursor: pointer;
    border: 2px solid #fff;
}
.gc-depth-hint {
    font-size: 0.7em;
    color: var(--text-secondary);
    opacity: 0.85;
}

.gc-legend-title {
    font-size: 0.7em;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 600;
    margin-bottom: 6px;
}
#legend .li {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 6px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 0.78em;
    color: var(--text);
    transition: background .15s, opacity .15s;
    user-select: none;
}
#legend .li:hover { background: var(--bg-alt); }
#legend .li.off { opacity: 0.35; }
#legend .li.off .dot { background: var(--text-secondary) !important; }
#legend .dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 6px rgba(0,0,0,0.2);
}
#legend .nm { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
#legend .ct { color: var(--text-secondary); font-size: 0.88em; }

/* ============================================
   Header info (top-right)
   ============================================ */
#graph-header {
    position: absolute;
    top: 16px;
    right: 16px;
    text-align: right;
    z-index: 90;
    pointer-events: none;
}
#g-title {
    font-size: 0.92em;
    font-weight: 700;
    color: var(--text);
    background: var(--card-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 7px 13px;
    box-shadow: var(--shadow-sm);
    display: inline-block;
    max-width: 440px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
#g-sub {
    font-size: 0.7em;
    color: var(--text-secondary);
    margin-top: 5px;
    background: var(--card-bg);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 4px 10px;
    display: inline-block;
}

/* ============================================
   Info Panel
   ============================================ */
.graph-info-panel {
    position: fixed;
    top: 80px;
    right: 24px;
    width: 330px;
    max-height: calc(100vh - 140px);
    overflow-y: auto;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 14px;
    padding: 20px;
    z-index: 100;
    display: none;
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: var(--shadow);
    transition: background .3s, border-color .3s;
}
.graph-info-panel.show { display: block; }
.graph-info-panel h3 {
    font-size: 0.97em;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
    line-height: 1.5;
    padding-right: 20px;
}
.graph-meta {
    font-size: 0.79em;
    color: var(--text-secondary);
    margin-bottom: 6px;
}
.graph-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 10px;
}
.graph-tags .tag {
    background: var(--primary-light);
    color: var(--primary);
    padding: 2px 9px;
    border-radius: 4px;
    font-size: 0.78em;
    font-weight: 500;
}
.graph-tags .cat {
    background: rgba(22, 163, 74, 0.1);
    color: var(--node-ai);
    padding: 2px 9px;
    border-radius: 4px;
    font-size: 0.78em;
    font-weight: 500;
}
.graph-close {
    position: absolute;
    top: 12px;
    right: 14px;
    background: none;
    border: none;
    color: var(--text-secondary);
    cursor: pointer;
    font-size: 1.1em;
    padding: 4px;
    border-radius: 4px;
    line-height: 1;
    transition: color .2s, background .2s;
}
.graph-close:hover {
    color: var(--text);
    background: var(--primary-light);
}
.graph-related-header {
    color: var(--text-secondary);
    font-size: 0.74em;
    font-weight: 600;
    margin-top: 14px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.graph-links a {
    display: block;
    color: var(--primary);
    font-size: 0.82em;
    text-decoration: none;
    padding: 6px 0;
    border-bottom: 1px solid var(--border);
    transition: color .2s;
}
.graph-links a:last-child { border-bottom: none; }
.graph-links a:hover {
    color: var(--primary);
    text-decoration: underline;
}
.graph-links a .weight {
    float: right;
    font-size: 0.75em;
    color: var(--text-secondary);
    font-weight: 400;
}
.graph-info-panel::-webkit-scrollbar { width: 4px; }
.graph-info-panel::-webkit-scrollbar-track { background: transparent; }
.graph-info-panel::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ============================================
   Tooltip
   ============================================ */
.graph-tooltip {
    position: fixed;
    display: none;
    z-index: 9999;
    background: var(--card-bg);
    color: var(--text);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 0.8em;
    font-weight: 600;
    max-width: 300px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    pointer-events: none;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: var(--shadow-sm);
}
.graph-tooltip .tt-sub {
    display: block;
    font-weight: 400;
    font-size: 0.84em;
    color: var(--text-secondary);
    margin-top: 1px;
    white-space: nowrap;
}

/* ============================================
   Footer
   ============================================ */
#graph-footer {
    position: absolute;
    bottom: 12px;
    right: 16px;
    font-size: 0.7em;
    color: var(--text-secondary);
    z-index: 80;
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid var(--card-border);
    border-radius: 8px;
    padding: 5px 11px;
}
#graph-footer b {
    color: var(--text);
    font-weight: 700;
    font-size: 1.06em;
}
#graph-footer .fk { color: var(--node-hermes); font-weight: 600; }
#graph-footer .fm { color: var(--node-dev); font-weight: 600; }
#graph-footer .fw { color: var(--text-secondary); }

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 900px) {
    #graph-controls { width: 226px; padding: 11px 12px; }
    #graph-header { display: none; }
}
@media (max-width: 640px) {
    #graph-controls {
        top: auto;
        bottom: 12px;
        left: 12px;
        right: 12px;
        width: auto;
        max-height: 46vh;
    }
    .graph-info-panel {
        top: auto;
        bottom: 50vh;
        right: 12px;
        left: 12px;
        width: auto;
        max-height: 42vh;
    }
}
</style>

<script>
    // ===================================================================
    // 1. Theme sync with NexT
    // ===================================================================
    (function() {
        var html = document.documentElement;
        var STORAGE_KEY = 'theme';

        function getInitialTheme() {
            var stored = localStorage.getItem(STORAGE_KEY);
            if (stored) return stored;
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) return 'dark';
            return 'light';
        }
        html.setAttribute('data-theme', getInitialTheme());
        window.addEventListener('storage', function(e) {
            if (e.key === STORAGE_KEY || e.key === null) {
                html.setAttribute('data-theme', getInitialTheme());
            }
        });
    })();

    // ===================================================================
    // 2. State
    // ===================================================================
    var BLOG_URL = window.location.origin;
    var network = null, dsNodes = null, dsEdges = null;
    var allNodes = [], allEdges = [], adj = {}, degree = {}, nodeTypes = {};

    var FOCUS_NODE = null;   // null | 'all' | <nodeId>
    var DEPTH = 0;           // 0 = 全部
    var disabledCats = {};
    var searchResults = [], selIdx = 0;

    var CONTAINER = null, TOOLTIP = null;
    var mx = 0, my = 0;

    // ===================================================================
    // 3. Helpers
    // ===================================================================
    function cssVar(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }
    function typeLabel(t) {
        return { hermes: 'Hermes 工程', ai: 'AI 技术', dev: '开发 · 工具', other: '其他' }[t] || '其他';
    }
    function catColorVar(type) { return cssVar('--node-' + type); }
    function esc(s) {
        return String(s == null ? '' : s).replace(/[&<>"]/g, function(c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
        });
    }
    function truncate(s, n) {
        s = String(s || '');
        return s.length > n ? s.slice(0, n - 1) + '…' : s;
    }
    function getNodeColor(node) {
        var cats = (node.categories || []).map(function(c) { return String(c).toLowerCase(); });
        if (cats.some(function(c) { return c.indexOf('hermes') !== -1; })) return 'hermes';
        if (cats.some(function(c) { return c.indexOf('ai') !== -1; })) return 'ai';
        if (cats.some(function(c) { return c.indexOf('开发') !== -1 || c.indexOf('工具') !== -1; })) return 'dev';
        return 'other';
    }
    function nodeById(id) {
        for (var i = 0; i < allNodes.length; i++) if (allNodes[i].id === id) return allNodes[i];
        return null;
    }
    function nodeSize(id) {
        var d = degree[id] || 0;
        if (d >= 25) return 18;
        if (d >= 18) return 15.5;
        if (d >= 12) return 13;
        if (d >= 6) return 11;
        return 9;
    }

    // ===================================================================
    // 4. Graph computation
    // ===================================================================
    function buildAdj() {
        allNodes.forEach(function(n) { adj[n.id] = []; });
        allEdges.forEach(function(e) {
            if (adj[e.from]) adj[e.from].push({ to: e.to, edge: e });
            if (adj[e.to]) adj[e.to].push({ to: e.from, edge: e });
        });
        Object.keys(adj).forEach(function(id) { degree[id] = adj[id].length; });
    }

    function subgraphFor(id, depth) {
        var s = new Set([id]);
        if (!depth) return s;
        var frontier = [id];
        for (var d = 0; d < depth; d++) {
            var next = [];
            frontier.forEach(function(u) {
                (adj[u] || []).forEach(function(x) {
                    if (!s.has(x.to)) { s.add(x.to); next.push(x.to); }
                });
            });
            frontier = next;
        }
        return s;
    }

    function computeVisibleIds() {
        var focusSet = FOCUS_NODE && FOCUS_NODE !== 'all' ? subgraphFor(FOCUS_NODE, DEPTH) : null;
        var q = (searchInput() ? searchInput().value : '') ;
        q = String(q || '').trim().toLowerCase();
        var searchSet = null;
        if (q) {
            searchSet = new Set();
            searchResults = [];
            allNodes.forEach(function(n) {
                if (String(n.title).toLowerCase().indexOf(q) !== -1) {
                    searchSet.add(n.id);
                    searchResults.push(n.id);
                }
            });
        } else if (searchInput) searchResults = [];

        var vis = new Set();
        allNodes.forEach(function(n) {
            if (disabledCats[nodeTypes[n.id]]) return;
            if (focusSet && !focusSet.has(n.id)) return;
            if (searchSet && !searchSet.has(n.id)) return;
            vis.add(n.id);
        });
        return vis;
    }

    // ===================================================================
    // 5. Render
    // ===================================================================
    function applyVisibility() {
        var vis = computeVisibleIds();
        dsNodes.forEach(function(n) { n.visible = vis.has(n.id); });
        dsEdges.forEach(function(e) { e.visible = vis.has(e.from) && vis.has(e.to); });
        return vis;
    }

    function applyLabels() {
        // 全图只标高连接度枢纽节点（degree>=25）；聚焦后显示聚焦节点 + 其邻居
        dsNodes.forEach(function(n) {
            var deg = degree[n.id] || 0;
            var focus = (FOCUS_NODE === n.id);
            var show;
            if (FOCUS_NODE === 'all') {
                show = deg >= 25;
            } else if (FOCUS_NODE) {
                show = focus || deg >= 5;
            } else {
                show = false;
            }
            n.label = show ? n.title : '';
            n.font = { size: focus ? 13 : 11.5, color: cssVar('--text'),
                       face: '-apple-system, sans-serif',
                       strokeWidth: 3, strokeColor: cssVar('--card-bg') };
            n.borderWidth = focus ? 4 : 2;
        });
    }

    function applyEdgeStyle() {
        dsEdges.forEach(function(e) {
            e.color = { color: cssVar('--edge-color'), hover: cssVar('--edge-color-hover'), opacity: 0.6 };
        });
    }

    function refresh(opts) {
        opts = opts || {};
        applyVisibility();
        applyLabels();
        applyEdgeStyle();
        dsNodes.update(dsNodes.get());
        dsEdges.update(dsEdges.get());
        paintSearchList();
        updateDepthUI();
        updateDepthHint();
        renderFooter();
        var vis = computeVisibleIds();
        gtitle(vis.size === allNodes.length && !searchInput().value.trim()
            ? '文章关系图谱'
            : (searchInput().value.trim() ? '搜索 "' + truncate(searchInput().value, 18) + '" · ' + searchResults.length + ' 项'
                : '聚焦 · ' + vis.size + ' / ' + allNodes.length + ' 篇'));
        if (opts.fit !== false) fitView(true);
    }

    function fitView(smooth) {
        try {
            network.fit({ animation: smooth ? { duration: 420, easingFunction: 'easeInOutQuad' } : false, scale: 0.95 });
        } catch (e) {}
    }

    // ===================================================================
    // 6. Network
    // ===================================================================
    function initNetwork() {
        CONTAINER = document.getElementById('network');
        TOOLTIP = document.getElementById('graph-tooltip');

        dsNodes = new vis.DataSet(allNodes.map(function(n) {
            var color = catColorVar(getNodeColor(n));
            return {
                id: n.id,
                title: n.title,
                size: nodeSize(n.id),
                mass: Math.max(1, 1 + (degree[n.id] || 0) * 0.12),
                physics: true,
                visible: true,
                label: '',
                color: { background: color, border: color,
                         shadow: { enabled: true, color: 'rgba(0,0,0,0.22)', size: 7, x: 0, y: 0 } },
                font: { size: 11.5, color: cssVar('--text'), face: '-apple-system, sans-serif',
                        strokeWidth: 3, strokeColor: cssVar('--card-bg') },
                borderWidth: 2,
                shape: 'dot'
            };
        }));

        dsEdges = new vis.DataSet(allEdges.map(function(e) {
            var w = e.weight || 0;
            return {
                from: e.from, to: e.to,
                weight: w,
                shared_tags: e.shared_tags || [],
                width: Math.min(Math.max(w * 0.42, 0.4), 2.6),
                color: { color: cssVar('--edge-color'), hover: cssVar('--edge-color-hover'), opacity: 0.6 },
                smooth: { enabled: true, type: 'continuous', roundness: 0.35 },
                hoverWidth: 1.6,
                visible: true
            };
        }));

        network = new vis.Network(CONTAINER, { nodes: dsNodes, edges: dsEdges }, {
            autoResize: true,
            interaction: {
                hover: true,
                tooltipDelay: 120,
                hoverConnectedEdges: false,
                zoomView: true,
                dragView: true,
                dragNodes: true,
                zoomSpeed: 0.55,
                multiselect: true,
                hideEdgesOnDrag: true,
                hideEdgesOnZoom: true
            },
            layout: { improvedLayout: true },
            physics: {
                enabled: true,
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -42,
                    centralGravity: 0.01,
                    springLength: 150,
                    springConstant: 0.042,
                    damping: 0.45,
                    avoidOverlap: 0.32
                },
                minVelocity: 0.25,
                timestep: 0.5,
                adaptiveTimestep: true,
                stabilization: { enabled: true, iterations: 320, updateInterval: 25 }
            }
        });

        // ---- events ----
        network.on('click', function(params) {
            if (params.nodes.length > 0) {
                clearSearch();
                focusNode(params.nodes[0]);
            } else {
                focusNode('all');
                clearSearch();
                closePanel();
            }
        });

        network.on('hoverNode', function(params) {
            CONTAINER.style.cursor = 'pointer';
            var nd = nodeById(params.node);
            if (!nd) return;
            var deg = degree[nd.id] || 0;
            TOOLTIPShow(nd.title, '关联 ' + deg + ' 篇 · 点击聚焦');
        });
        network.on('blurNode', function() {
            CONTAINER.style.cursor = 'default';
            TOOLTIP.style.display = 'none';
        });
        network.on('hoverEdge', function(params) {
            var ed = dsEdges.get(params.edge);
            if (ed && ed.shared_tags && ed.shared_tags.length) {
                TOOLTIPShow('关联度 ' + ed.weight, ed.shared_tags.join(' · '));
            }
        });
        network.on('blurEdge', function() { TOOLTIP.style.display = 'none'; });

        document.addEventListener('mousemove', function(e) { mx = e.clientX; my = e.clientY; moveTooltip(); });

        var observer = new MutationObserver(function() { reapplyTheme(); });
        observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    }

    function TOOLTIPShow(main, sub) {
        TOOLTIP.innerHTML = esc(main) + '<span class="tt-sub">' + esc(sub) + '</span>';
        TOOLTIP.style.display = 'block';
        moveTooltip();
    }
    function moveTooltip() {
        if (TOOLTIP.style.display !== 'block') return;
        var w = TOOLTIP.offsetWidth, h = TOOLTIP.offsetHeight;
        var x = mx + 16, y = my - 10;
        if (x + w > window.innerWidth - 6) x = mx - w - 14;
        if (y + h > window.innerHeight - 6) y = my - h - 12;
        if (y < 6) y = 6;
        TOOLTIP.style.left = x + 'px';
        TOOLTIP.style.top = y + 'px';
    }

    // ===================================================================
    // 7. Theme
    // ===================================================================
    function reapplyTheme() {
        var dark = document.documentElement.getAttribute('data-theme') === 'dark';
        document.body.classList.toggle('dark', dark);
        dsNodes.forEach(function(n) {
            n.color = { background: catColorVar(nodeTypes[n.id]), border: catColorVar(nodeTypes[n.id]),
                shadow: { enabled: true, color: dark ? 'rgba(0,0,0,0.6)' : 'rgba(0,0,0,0.22)', size: 7, x: 0, y: 0 } };
            n.font = { size: 11.5, color: cssVar('--text'), face: '-apple-system, sans-serif',
                       strokeWidth: 3, strokeColor: cssVar('--card-bg') };
            n.size = nodeSize(n.id);
        });
        applyLabels();
        applyEdgeStyle();
        dsNodes.update(dsNodes.get());
        dsEdges.update(dsEdges.get());
        buildLegend();
        fitView(false);
    }

    // ===================================================================
    // 8. Focus / search / depth / legend UI
    // ===================================================================
    function focusNode(id) {
        FOCUS_NODE = id;
        if (id === 'all') { DEPTH = 0; }
        else { DEPTH = 1; }   // 聚焦默认展开 1 度邻域
        var slider = document.getElementById('depth-slider');
        if (slider) slider.value = DEPTH;
        refresh();
        if (id && id !== 'all') {
            network.selectNodes([id]);
            showInfo(id);
        } else {
            try { network.deselectNodes(); } catch (e) {}
            closePanel();
        }
    }

    function gtitle(t) { document.getElementById('g-title').textContent = t; }
    function searchInput() { return document.getElementById('search-input'); }

    var debounceT = null;
    function bindSearch() {
        var input = searchInput();
        input.addEventListener('input', function() {
            clearTimeout(debounceT);
            debounceT = setTimeout(function() { selIdx = 0; refresh(); }, 130);
        });
        input.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (searchResults.length) { selIdx = Math.min(selIdx + 1, searchResults.length - 1); paintSearchList(); }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (searchResults.length) { selIdx = Math.max(selIdx - 1, 0); paintSearchList(); }
            } else if (e.key === 'Enter') {
                e.preventDefault();
                var id = searchResults[selIdx] || searchResults[0];
                if (id) { clearSearch(); focusNode(id); }
            } else if (e.key === 'Escape') {
                e.stopPropagation();
                clearSearch();
            }
        });
    }

    function clearSearch() {
        var el = searchInput();
        if (el) { el.value = ''; el.blur(); }
        selIdx = 0;
        searchResults = [];
        var box = document.getElementById('search-list');
        if (box) { box.classList.remove('show'); box.innerHTML = ''; }
        var cnt = document.getElementById('search-count');
        if (cnt) cnt.textContent = '';
    }

    function paintSearchList() {
        var box = document.getElementById('search-list');
        var cnt = document.getElementById('search-count');
        if (!box) return;
        cnt.textContent = searchResults.length ? searchResults.length + ' 项' : '';
        if (!searchResults.length) { box.classList.remove('show'); box.innerHTML = ''; return; }
        box.innerHTML = searchResults.map(function(id, i) {
            var n = nodeById(id);
            return '<div class="si' + (i === selIdx ? ' sel' : '') + '" data-id="' + esc(id) + '">' +
                   esc(truncate(n.title, 24)) + '<i>' + (degree[id] || 0) + '</i></div>';
        }).join('');
        box.classList.add('show');
        Array.prototype.forEach.call(box.children, function(el) {
            el.addEventListener('click', function() {
                var id = el.getAttribute('data-id');
                clearSearch();
                focusNode(id);
            });
        });
    }

    function updateDepthUI() {
        var btn = document.getElementById('btn-focus');
        var slider = document.getElementById('depth-slider');
        var dv = document.getElementById('depth-val');
        if (!btn) return;
        var off = (FOCUS_NODE === 'all');
        btn.classList.toggle('off', off);
        btn.title = off ? '需先点击一个节点' : ('切换深度（当前 ' + (DEPTH === 0 ? '全部' : DEPTH + ' 度') + '）');
        slider.disabled = off;
        dv.textContent = DEPTH === 0 ? '全部' : DEPTH + ' 度';
    }

    function updateDepthHint() {
        var h = document.getElementById('depth-hint');
        if (!h) return;
        if (FOCUS_NODE === 'all' || !FOCUS_NODE) { h.textContent = '点击节点 → 可限定 1~3 度子图'; return; }
        var n = nodeById(FOCUS_NODE);
        if (!n) return;
        var cnt = subgraphFor(FOCUS_NODE, DEPTH).size;
        h.textContent = (DEPTH === 0 ? '全部关联' : DEPTH + ' 度') + ' · ' + cnt + ' 篇';
    }

    function buildLegend() {
        var counts = {};
        Object.keys(nodeTypes).forEach(function(id) {
            var t = nodeTypes[id]; counts[t] = (counts[t] || 0) + 1;
        });
        var order = ['hermes', 'ai', 'dev', 'other'];
        var el = document.getElementById('legend');
        el.innerHTML = order.filter(function(t) { return counts[t]; }).map(function(t) {
            return '<div class="li' + (disabledCats[t] ? ' off' : '') + '" data-cat="' + t + '">' +
                   '<span class="dot" style="background:' + catColorVar(t) + '"></span>' +
                   '<span class="nm">' + typeLabel(t) + '</span>' +
                   '<span class="ct">' + counts[t] + '</span></div>';
        }).join('');
        Array.prototype.forEach.call(el.children, function(li) {
            li.addEventListener('click', function() {
                var t = li.getAttribute('data-cat');
                disabledCats[t] = !disabledCats[t];
                refresh();
                li.classList.toggle('off', !!disabledCats[t]);
            });
        });
    }

    function renderFooter() {
        var el = document.getElementById('graph-footer');
        if (!el) return;
        var vis = computeVisibleIds();
        var ve = allEdges.filter(function(e) { return vis.has(e.from) && vis.has(e.to); }).length;
        var strong = allEdges.filter(function(e){return e.weight>=8;}).length;
        var mid = allEdges.filter(function(e){return e.weight>=4 && e.weight<8;}).length;
        var weak = allEdges.length - strong - mid;
        el.innerHTML = '<b>' + vis.size + '</b> 篇 / <b>' + ve + '</b> 关联' +
            ' &nbsp;·&nbsp; <span class="fk">强</span> ' + strong +
            ' <span class="fm">中</span> ' + mid +
            ' <span class="fw">弱</span> ' + weak;
    }

    // ===================================================================
    // 9. Info panel
    // ===================================================================
    function showInfo(nodeId) {
        var node = nodeById(nodeId);
        if (!node) return;

        document.getElementById('info-title').innerHTML = '<a href="' + BLOG_URL + '/' +
            node.date.split(' ')[0].replace(/-/g, '/') + '/' + node.id + '/" target="_blank" ' +
            'style="color:inherit;text-decoration:none;">' + esc(node.title) + '</a>';
        document.getElementById('info-date').textContent = node.date
            ? new Date(node.date).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
            : '';

        var tagsEl = document.getElementById('info-tags');
        tagsEl.innerHTML = '';
        (node.tags || []).forEach(function(t) {
            var span = document.createElement('span');
            span.className = 'tag'; span.textContent = t;
            tagsEl.appendChild(span);
        });
        (node.categories || []).forEach(function(c) {
            var span = document.createElement('span');
            span.className = 'cat'; span.textContent = c;
            tagsEl.appendChild(span);
        });

        var related = allEdges
            .filter(function(e) { return e.from === nodeId || e.to === nodeId; })
            .sort(function(a, b) { return b.weight - a.weight; })
            .slice(0, 10);

        var linksEl = document.getElementById('info-links');
        var headerEl = document.getElementById('related-header');
        linksEl.innerHTML = '';

        if (related.length > 0) {
            headerEl.style.display = 'block';
            headerEl.textContent = '相关文章（' + related.length + '）';
            related.forEach(function(e) {
                var targetId = e.from === nodeId ? e.to : e.from;
                var target = nodeById(targetId);
                if (!target) return;
                var a = document.createElement('a');
                a.href = BLOG_URL + '/' + target.date.split(' ')[0].replace(/-/g, '/') + '/' + target.id + '/';
                a.innerHTML = esc(target.title) + ' <span class="weight">' + e.weight + '</span>';
                a.title = '关联度: ' + (e.shared_tags ? e.shared_tags.join(', ') : '');
                linksEl.appendChild(a);
            });
        } else {
            headerEl.style.display = 'none';
        }
        document.getElementById('info-panel').classList.add('show');
    }

    function closePanel() {
        document.getElementById('info-panel').classList.remove('show');
    }

    // ===================================================================
    // 10. Boot
    // ===================================================================
    function boot() {
        fetch('/graph/graph.json')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                allNodes = data.nodes;
                allEdges = data.edges;
                buildAdj();
                allNodes.forEach(function(n) { nodeTypes[n.id] = getNodeColor(n); });
                initNetwork();
                initControls();
                FOCUS_NODE = 'all';
                refresh({ fit: false });
                buildLegend();
                document.getElementById('loading').classList.add('hidden');
                setTimeout(function() { fitView(false); }, 120);
            })
            .catch(function(e) {
                var el = document.getElementById('loading');
                el.textContent = '⚠️ 图谱加载失败：' + e;
                el.style.color = '#f87171';
            });
    }

    function initControls() {
        // focus button — cycles depth
        document.getElementById('btn-focus').addEventListener('click', function() {
            if (!FOCUS_NODE || FOCUS_NODE === 'all') {
                updateDepthHint();
                return;
            }
            var d = (DEPTH >= 3) ? 0 : DEPTH + 1;
            DEPTH = d;
            document.getElementById('depth-slider').value = d;
            refresh();
        });

        // depth slider
        document.getElementById('depth-slider').addEventListener('input', function() {
            DEPTH = parseInt(this.value, 10);
            refresh();
        });

        // keyboard
        document.addEventListener('keydown', function(e) {
            var tag = document.activeElement && document.activeElement.tagName;
            if (tag === 'INPUT' || tag === 'TEXTAREA') return;
            if (e.key === 'Escape') { focusNode('all'); clearSearch(); closePanel(); }
            else if (e.code === 'Space') { e.preventDefault(); fitView(true); }
        });

        bindSearch();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
</script>

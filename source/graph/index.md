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

<!-- Filter controls -->
<div class="graph-controls">
    <button id="btn-all" class="active" onclick="filterCategory('all')">全部</button>
    <button id="btn-hermes" onclick="filterCategory('Hermes')">Hermes</button>
    <button id="btn-ai" onclick="filterCategory('AI')">AI</button>
    <button id="btn-dev" onclick="filterCategory('开发')">开发</button>
</div>

<!-- Info panel -->
<div class="graph-info-panel" id="info-panel">
    <button class="graph-close" onclick="closePanel()">✕</button>
    <h3 id="info-title"></h3>
    <div class="graph-meta" id="info-date"></div>
    <div class="graph-tags" id="info-tags"></div>
    <div class="graph-related-header" id="related-header" style="display:none">相关文章</div>
    <div class="graph-links" id="info-links"></div>
</div>

<!-- Legend -->
<div class="graph-legend">
    <div class="graph-legend-item"><div class="graph-dot" style="background:var(--node-hermes)"></div> Hermes</div>
    <div class="graph-legend-item"><div class="graph-dot" style="background:var(--node-ai)"></div> AI</div>
    <div class="graph-legend-item"><div class="graph-dot" style="background:var(--node-dev)"></div> 开发</div>
    <div class="graph-legend-item"><div class="graph-line" style="background:var(--edge-color)"></div> 关联强度</div>
</div>

<style>
/* ============================================
   Keep full header visible (brand + nav menu)
   ============================================ */
.headband {
    display: none !important;
}

/* Use list-page style: .post-content instead of .post-body */
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

/* Graph container fills the content area */
#graph-canvas {
    width: 100%;
    height: calc(100vh - 80px);
    position: relative;
}
#network {
    width: 100%;
    height: 100%;
}

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
    --card-bg: rgba(255, 255, 255, 0.95);
    --card-border: #e2e8f0;
    --shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
    --node-hermes: #2563eb;
    --node-ai: #16a34a;
    --node-dev: #d97706;
    --node-other: #64748b;
    --edge-color: rgba(100, 116, 139, 0.35);
    --edge-color-hover: rgba(37, 99, 235, 0.6);
}
[data-theme="dark"] {
    --bg: #0f172a;
    --bg-alt: #1e293b;
    --primary: #60a5fa;
    --primary-light: rgba(96, 165, 250, 0.1);
    --text: #e2e8f0;
    --text-secondary: #94a3b8;
    --border: #334155;
    --card-bg: rgba(15, 23, 42, 0.95);
    --card-border: #334155;
    --shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    --node-hermes: #60a5fa;
    --node-ai: #4ade80;
    --node-dev: #fbbf24;
    --node-other: #94a3b8;
    --edge-color: rgba(148, 163, 184, 0.25);
    --edge-color-hover: rgba(96, 165, 250, 0.5);
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
}
.graph-loading.hidden { display: none; }

/* ============================================
   Controls (top-left, after sidebar)
   ============================================ */
.graph-controls {
    position: fixed;
    top: 84px;
    left: 262px;
    display: flex;
    gap: 6px;
    z-index: 100;
    background: var(--card-bg);
    padding: 6px;
    border-radius: 10px;
    border: 1px solid var(--border);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    transition: background 0.3s, border-color 0.3s;
}
.graph-controls button {
    background: transparent;
    border: 1px solid transparent;
    color: var(--text-secondary);
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85em;
    font-weight: 500;
    transition: all 0.2s;
    font-family: inherit;
}
.graph-controls button:hover {
    color: var(--primary);
    background: var(--primary-light);
}
.graph-controls button.active {
    background: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
}

/* ============================================
   Info Panel
   ============================================ */
.graph-info-panel {
    position: fixed;
    top: 80px;
    right: 24px;
    width: 320px;
    max-height: calc(100vh - 140px);
    overflow-y: auto;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    z-index: 100;
    display: none;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    transition: background 0.3s, border-color 0.3s;
}
.graph-info-panel.show { display: block; }
.graph-info-panel h3 {
    font-size: 1em;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
    line-height: 1.5;
    padding-right: 20px;
}
.graph-meta {
    font-size: 0.8em;
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
    font-size: 0.8em;
    font-weight: 500;
}
.graph-tags .cat {
    background: rgba(22, 163, 74, 0.1);
    color: var(--node-ai);
    padding: 2px 9px;
    border-radius: 4px;
    font-size: 0.8em;
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
    transition: color 0.2s, background 0.2s;
}
.graph-close:hover {
    color: var(--text);
    background: var(--primary-light);
}
.graph-related-header {
    color: var(--text-secondary);
    font-size: 0.8em;
    font-weight: 600;
    margin-top: 14px;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.graph-links a {
    display: block;
    color: var(--primary);
    font-size: 0.85em;
    text-decoration: none;
    padding: 5px 0;
    border-bottom: 1px solid var(--border);
    transition: color 0.2s;
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
   Legend
   ============================================ */
.graph-legend {
    position: fixed;
    bottom: 80px;
    left: 262px;
    background: var(--card-bg);
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid var(--border);
    z-index: 100;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    transition: background 0.3s, border-color 0.3s;
}
.graph-legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
    font-size: 0.8em;
    color: var(--text-secondary);
}
.graph-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.graph-line {
    width: 20px;
    height: 2px;
    flex-shrink: 0;
    border-radius: 1px;
}

/* ============================================
   Responsive
   ============================================ */
@media (max-width: 640px) {
    .graph-info-panel {
        top: auto;
        bottom: 80px;
        right: 12px;
        left: 12px;
        width: auto;
        max-height: 50vh;
    }
    .graph-controls {
        gap: 4px;
        padding: 4px;
    }
    .graph-controls button {
        padding: 5px 10px;
        font-size: 0.8em;
    }
    .graph-legend { display: none; }
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
    // 2. Graph
    // ===================================================================
    var BLOG_URL = window.location.origin;
    var network = null;
    var allNodes = [];
    var allEdges = [];
    var currentFilter = 'all';

    function getNodeColor(node) {
        var cats = (node.categories || []).map(function(c) { return c.toLowerCase(); });
        if (cats.some(function(c) { return c.indexOf('hermes') !== -1; })) return 'hermes';
        if (cats.some(function(c) { return c.indexOf('ai') !== -1; })) return 'ai';
        if (cats.some(function(c) { return c.indexOf('开发') !== -1 || c.indexOf('工具') !== -1; })) return 'dev';
        return 'other';
    }

    function cssVar(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    }

    function initNetwork() {
        var nodes = new vis.DataSet(
            allNodes.map(function(n) {
                var type = getNodeColor(n);
                var colorMap = { hermes: '--node-hermes', ai: '--node-ai', dev: '--node-dev', other: '--node-other' };
                var nodeColor = cssVar(colorMap[type]);
                return {
                    id: n.id,
                    label: n.title.length > 15 ? n.title.substring(0, 15) + '…' : n.title,
                    title: n.title,
                    size: n.size || 12,
                    color: {
                        background: nodeColor,
                        border: nodeColor,
                        highlight: { background: cssVar('--primary'), border: cssVar('--primary') },
                        hover: { background: cssVar('--primary'), border: cssVar('--primary') }
                    },
                    font: { size: 12, color: cssVar('--text'), face: '-apple-system, sans-serif' },
                    borderWidth: 2,
                    borderWidthSelected: 3,
                    shadow: { enabled: true, color: 'rgba(0,0,0,0.15)', size: 8, x: 0, y: 0 },
                    shape: 'dot'
                };
            })
        );

        var edges = new vis.DataSet(
            allEdges.map(function(e) {
                return {
                    from: e.from,
                    to: e.to,
                    width: Math.max(e.weight * 0.6, 0.5),
                    color: { color: cssVar('--edge-color'), hover: cssVar('--edge-color-hover'), opacity: 0.7 },
                    smooth: { type: 'continuous' },
                    hoverWidth: 1.5,
                    selectionWidth: 2
                };
            })
        );

        var container = document.getElementById('network');
        var options = {
            physics: {
                enabled: true,
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {
                    gravitationalConstant: -40,
                    centralGravity: 0.008,
                    springLength: 160,
                    springConstant: 0.04,
                    damping: 0.4
                },
                stabilization: { iterations: 150 }
            },
            interaction: {
                hover: true,
                tooltipDelay: 200,
                zoomView: true,
                dragView: true,
                dragNodes: true,
                zoomSpeed: 0.5
            },
            layout: { improvedLayout: true },
            edges: { smooth: { type: 'continuous' } }
        };

        network = new vis.Network(container, { nodes: nodes, edges: edges }, options);

        // Click — show info panel
        network.on('click', function(params) {
            if (params.nodes.length > 0) {
                showInfo(params.nodes[0]);
            } else {
                closePanel();
            }
        });

        network.on('hoverNode', function() {
            network.body.container.style.cursor = 'pointer';
        });
        network.on('blurNode', function() {
            network.body.container.style.cursor = 'default';
        });

        // Re-color nodes when theme changes
        var observer = new MutationObserver(function() {
            nodes.forEach(function(n) {
                var nodeData = allNodes.find(function(x) { return x.id === n.id; });
                if (!nodeData) return;
                var type = getNodeColor(nodeData);
                var colorMap = { hermes: '--node-hermes', ai: '--node-ai', dev: '--node-dev', other: '--node-other' };
                var c = cssVar(colorMap[type]);
                nodes.update({ id: n.id, color: { background: c, border: c, highlight: { background: cssVar('--primary'), border: cssVar('--primary') }, hover: { background: cssVar('--primary'), border: cssVar('--primary') } } });
            });
            edges.forEach(function(e) {
                edges.update({ id: e.id, color: { color: cssVar('--edge-color'), hover: cssVar('--edge-color-hover'), opacity: 0.7 } });
            });
        });
        observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    }

    function showInfo(nodeId) {
        var node = allNodes.find(function(n) { return n.id === nodeId; });
        if (!node) return;

        document.getElementById('info-title').textContent = node.title;
        document.getElementById('info-date').textContent = node.date
            ? new Date(node.date).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
            : '';

        var tagsEl = document.getElementById('info-tags');
        tagsEl.innerHTML = '';
        (node.tags || []).forEach(function(t) {
            var span = document.createElement('span');
            span.className = 'tag';
            span.textContent = t;
            tagsEl.appendChild(span);
        });
        (node.categories || []).forEach(function(c) {
            var span = document.createElement('span');
            span.className = 'cat';
            span.textContent = c;
            tagsEl.appendChild(span);
        });

        var related = allEdges
            .filter(function(e) { return e.from === nodeId || e.to === nodeId; })
            .sort(function(a, b) { return b.weight - a.weight; })
            .slice(0, 8);

        var linksEl = document.getElementById('info-links');
        var headerEl = document.getElementById('related-header');
        linksEl.innerHTML = '';

        if (related.length > 0) {
            headerEl.style.display = 'block';
            related.forEach(function(e) {
                var targetId = e.from === nodeId ? e.to : e.from;
                var target = allNodes.find(function(n) { return n.id === targetId; });
                if (!target) return;
                var a = document.createElement('a');
                a.href = BLOG_URL + '/' + target.id + '/';
                a.innerHTML = target.title + ' <span class="weight">' + e.weight + '</span>';
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

    function filterCategory(cat) {
        currentFilter = cat;
        document.querySelectorAll('.graph-controls button').forEach(function(b) { b.classList.remove('active'); });
        var btn = document.getElementById('btn-' + (cat === 'all' ? 'all' : cat.toLowerCase()));
        if (btn) btn.classList.add('active');

        if (!network) return;

        if (cat === 'all') {
            network.body.data.nodes.forEach(function(n) { network.body.data.nodes.update({ id: n.id, hidden: false }); });
            network.body.data.edges.forEach(function(e) { network.body.data.edges.update({ id: e.id, hidden: false }); });
            return;
        }

        var catLower = cat.toLowerCase();
        var filteredIds = new Set();
        allNodes.forEach(function(n) {
            var cats = (n.categories || []).map(function(c) { return c.toLowerCase(); });
            var tags = (n.tags || []).map(function(t) { return t.toLowerCase(); });
            var match = cats.some(function(c) { return c.indexOf(catLower) !== -1; }) ||
                        tags.some(function(t) { return t.indexOf(catLower) !== -1; });
            if (match) filteredIds.add(n.id);
        });

        network.body.data.nodes.forEach(function(n) {
            network.body.data.nodes.update({ id: n.id, hidden: !filteredIds.has(n.id) });
        });
        network.body.data.edges.forEach(function(e) {
            network.body.data.edges.update({ id: e.id, hidden: !filteredIds.has(e.from) || !filteredIds.has(e.to) });
        });
    }

    var filterObserver = new MutationObserver(function() {
        if (network && currentFilter !== 'all') {
            filterCategory(currentFilter);
        }
    });
    filterObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    // ===================================================================
    // 3. Load data
    // ===================================================================
    fetch('/graph/graph.json')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            allNodes = data.nodes;
            allEdges = data.edges;
            initNetwork();
            document.getElementById('loading').classList.add('hidden');
        })
        .catch(function(err) {
            document.getElementById('loading').innerHTML =
                '<div style="text-align:center;color:var(--text-secondary)"><h2>❌ 加载失败</h2><p>' + err.message + '</p></div>';
        });

    // ===================================================================
    // 4. Keyboard shortcuts
    // ===================================================================
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closePanel();
    });
</script>
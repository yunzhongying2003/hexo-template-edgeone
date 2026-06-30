import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 中文字体
font_bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font_reg = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# ========== 图1：文章头图 ==========
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')

# 深色渐变背景
gradient = np.linspace(0, 1, 256).reshape(256, 1)
ax.imshow(gradient, aspect='auto', cmap='Blues', alpha=0.3, extent=[0, 16, 0, 9])
ax.set_facecolor('#0a0e27')

# 装饰网格线
for i in range(0, 17, 2):
    ax.axvline(x=i, color='#1a3a6a', linewidth=0.5, alpha=0.3)
for i in np.arange(0, 10, 1.5):
    ax.axhline(y=i, color='#1a3a6a', linewidth=0.5, alpha=0.3)

# 主标题
ax.text(8, 6.5, 'MCP 协议实战', fontproperties=font_bold, fontsize=42,
        color='#ffffff', ha='center', va='center',
        fontweight='bold')
ax.text(8, 5.5, '从零构建 AI 的"USB-C"接口', fontproperties=font_bold, fontsize=22,
        color='#7eb8ff', ha='center', va='center')

# 分隔线
ax.plot([3, 13], [4.8, 4.8], color='#4a9eff', linewidth=2, alpha=0.8)

# 副标题
ax.text(8, 4.2, 'Model Context Protocol · 协议解析 · 工具链构建 · 实战部署',
        fontproperties=font_reg, fontsize=14, color='#a0c4ff', ha='center', va='center')

# 底部装饰元素 - 三个节点
nodes = [(3, 2.5, 'Host', '#4a9eff'), (8, 2.5, 'Client', '#6ee7b7'), (13, 2.5, 'Server', '#f97316')]
for nx, ny, label, color in nodes:
    circle = plt.Circle((nx, ny), 0.8, color=color, alpha=0.15)
    ax.add_patch(circle)
    circle_border = plt.Circle((nx, ny), 0.8, color=color, fill=False, linewidth=2)
    ax.add_patch(circle_border)
    ax.text(nx, ny, label, fontproperties=font_bold, fontsize=14, color=color,
            ha='center', va='center')

# 箭头连接
for sx, ex in [(3.8, 7.2), (8.8, 12.2)]:
    ax.annotate('', xy=(ex, 2.5), xytext=(sx, 2.5),
                arrowprops=dict(arrowstyle='->', color='#7eb8ff', lw=2.5))

# 底部标签
ax.text(8, 0.8, 'golook.cf  ·  AI 技术笔记 · 效率工具 · 深度分析',
        fontproperties=font_reg, fontsize=11, color='#5a7ab0', ha='center', va='center')

plt.tight_layout(pad=0)
plt.savefig('/root/hexo-template-edgeone/source/images/mcp-header.png',
            dpi=100, bbox_inches='tight', facecolor='#0a0e27')
plt.close()
print("Header image saved.")

# ========== 图2：MCP 架构示意图 ==========
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#0a0e27')

# 背景网格
for i in range(0, 17, 2):
    ax.axvline(x=i, color='#1a3a6a', linewidth=0.5, alpha=0.3)
for i in np.arange(0, 10, 1.5):
    ax.axhline(y=i, color='#1a3a6a', linewidth=0.5, alpha=0.3)

# 标题
ax.text(8, 8.3, 'MCP 三层架构', fontproperties=font_bold, fontsize=28,
        color='#ffffff', ha='center', va='center')
ax.plot([4, 12], [7.8, 7.8], color='#4a9eff', linewidth=1.5, alpha=0.6)

# Host 层
host_box = FancyBboxPatch((0.5, 5.5), 5, 1.8, boxstyle="round,pad=0.1",
                           facecolor='#1a3a6a', edgecolor='#4a9eff', linewidth=2)
ax.add_patch(host_box)
ax.text(3, 6.6, 'MCP Host', fontproperties=font_bold, fontsize=16,
        color='#7eb8ff', ha='center', va='center')
ax.text(3, 6.0, 'Claude Desktop / Cursor / Cline', fontproperties=font_reg, fontsize=11,
        color='#a0c4ff', ha='center', va='center')
ax.text(3, 5.6, '管控 context 聚合', fontproperties=font_reg, fontsize=10,
        color='#7a9ac0', ha='center', va='center')

# Client 层
client_box = FancyBboxPatch((6, 5.5), 4, 1.8, boxstyle="round,pad=0.1",
                             facecolor='#1a3a6a', edgecolor='#6ee7b7', linewidth=2)
ax.add_patch(client_box)
ax.text(8, 6.6, 'MCP Client', fontproperties=font_bold, fontsize=16,
        color='#6ee7b7', ha='center', va='center')
ax.text(8, 6.0, 'JSON-RPC Session', fontproperties=font_reg, fontsize=11,
        color='#a0c4ff', ha='center', va='center')
ax.text(8, 5.6, '协商能力 / 路由消息', fontproperties=font_reg, fontsize=10,
        color='#7a9ac0', ha='center', va='center')

# Server 层
server_box = FancyBboxPatch((11.5, 5.5), 4, 1.8, boxstyle="round,pad=0.1",
                             facecolor='#1a3a6a', edgecolor='#f97316', linewidth=2)
ax.add_patch(server_box)
ax.text(13.5, 6.6, 'MCP Server', fontproperties=font_bold, fontsize=16,
        color='#f97316', ha='center', va='center')
ax.text(13.5, 6.0, 'Web Search / Database', fontproperties=font_reg, fontsize=11,
        color='#a0c4ff', ha='center', va='center')
ax.text(13.5, 5.6, '公开 Tools / Resources', fontproperties=font_reg, fontsize=10,
        color='#7a9ac0', ha='center', va='center')

# 箭头
ax.annotate('', xy=(6, 6.4), xytext=(5.5, 6.4),
            arrowprops=dict(arrowstyle='->', color='#7eb8ff', lw=2.5))
ax.annotate('', xy=(11.5, 6.4), xytext=(10, 6.4),
            arrowprops=dict(arrowstyle='->', color='#7eb8ff', lw=2.5))

# Server 能力
abilities = [('Tools', '#f97316', 2.5), ('Resources', '#6ee7b7', 4.5), ('Prompts', '#a78bfa', 6.5)]
for label, color, x in abilities:
    box = FancyBboxPatch((x-0.8, 3.2), 1.6, 0.8, boxstyle="round,pad=0.05",
                         facecolor=color, edgecolor=color, linewidth=1.5, alpha=0.2)
    ax.add_patch(box)
    ax.text(x, 3.6, label, fontproperties=font_bold, fontsize=13,
            color=color, ha='center', va='center')

# 连接线
ax.plot([13.5, 13.5], [5.5, 4.0], color='#f97316', linewidth=1.5, alpha=0.5)
ax.plot([2.5, 6.5], [4.0, 4.0], color='#7eb8ff', linewidth=1.5, alpha=0.5)

# 传输层
ax.text(8, 2.2, '传输层', fontproperties=font_bold, fontsize=14,
        color='#7eb8ff', ha='center', va='center')
ax.text(8, 1.6, 'stdio（本地）  ·  SSE（云端）  ·  WebSocket',
        fontproperties=font_reg, fontsize=12, color='#a0c4ff', ha='center', va='center')

# 底部
ax.text(8, 0.6, '基于 JSON-RPC 2.0  ·  灵感来自 LSP (Language Server Protocol)',
        fontproperties=font_reg, fontsize=10, color='#5a7ab0', ha='center', va='center')

plt.tight_layout(pad=0)
plt.savefig('/root/hexo-template-edgeone/source/images/mcp-architecture.png',
            dpi=100, bbox_inches='tight', facecolor='#0a0e27')
plt.close()
print("Architecture image saved.")

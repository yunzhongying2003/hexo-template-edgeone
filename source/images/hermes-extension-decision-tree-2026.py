#!/usr/bin/env python3
"""Hermes Agent 扩展机制选型决策树"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FONT_BOLD = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_REG  = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

BG      = '#0f1226'
NODE_Q  = '#2a2f5e'   # 问题节点
NODE_A  = '#4c3d8a'   # 结论 A (Skill)
NODE_B  = '#2c5f7f'   # 结论 B (Plugin)
NODE_C  = '#4a3070'   # 结论 C (MCP)
NODE_D  = '#3d4c28'   # 结论 D (Agent Plugins)
ARROW   = '#7c9cff'
ARROW_Y = '#fbbf24'
TEXT    = '#ffffff'
SUBT    = '#a8aede'

fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 160)
ax.set_ylim(0, 90)
ax.axis('off')

def block(x, y, w, h, color, title, subtitle=None, title_size=12):
    """绘制圆角矩形块，标题在上，副标题在下（都在色块内部）"""
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle="round,pad=0.02,rounding_size=0.6",
                          linewidth=0, facecolor=color)
    ax.add_patch(rect)
    if subtitle:
        ax.text(x, y + h*0.22, title, fontproperties=FONT_BOLD, fontsize=title_size,
                color='white', ha='center', va='center')
        ax.text(x, y - h*0.18, subtitle, fontproperties=FONT_REG, fontsize=9,
                color='#e6e6ff', ha='center', va='center')
    else:
        ax.text(x, y, title, fontproperties=FONT_BOLD, fontsize=title_size,
                color='white', ha='center', va='center')

def arrow(x1, y1, x2, y2, label='', color=ARROW, label_pos=0.5, label_dy=1.5):
    """画箭头 + 可选中间标签"""
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle='-|>', mutation_scale=14,
                          linewidth=1.5, color=color, alpha=0.85)
    ax.add_patch(arr)
    if label:
        mx = x1 + (x2-x1)*label_pos
        my = y1 + (y2-y1)*label_pos
        ax.text(mx, my + label_dy, label, fontproperties=FONT_BOLD, fontsize=8,
                color=color, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=BG, edgecolor='none'))

# 标题
ax.text(80, 85, 'Hermes Agent 扩展机制：选型决策树',
        fontproperties=FONT_BOLD, fontsize=22, color=TEXT, ha='center', va='center')
ax.text(80, 80.5, '从需求出发，四步定位到最适合的扩展方式',
        fontproperties=FONT_REG, fontsize=12, color=SUBT, ha='center', va='center')

# 第 1 层：起点
block(80, 74, 42, 6.5, '#4a4f8a', '起点：我需要扩展 Hermes Agent', None, title_size=13)

# 第 2 层：第一个问题
arrow(80, 70.5, 80, 66)
block(80, 63, 50, 6.5, NODE_Q, 'Q1: 需要新增能力，还是仅教 Agent 用现有工具？', None, title_size=11.5)

# 分支：左 → Skill
arrow(55, 59.5, 22, 51.5, label='仅教 Agent 怎么做', color=ARROW_Y, label_pos=0.45, label_dy=1.8)
# 分支：右 → 继续问
arrow(105, 59.5, 100, 51.5, label='需要新工具/服务', color=ARROW, label_pos=0.45, label_dy=1.8)

# 结论 A：Skill
block(15, 46, 22, 9, NODE_A, '→ 用 SKILL', 'Markdown 文件\n~/.hermes/skills/xxx/SKILL.md', title_size=12)
block(15, 33, 22, 8, '#3d3070', '典型：写作模板\n团队最佳实践\n个人工作流', None, title_size=9)

# 第 3 层（右）：第二个问题
block(100, 47, 54, 6.5, NODE_Q, 'Q2: 扩展来源是自己写代码，还是接入外部服务？', None, title_size=11.5)
arrow(78, 43.5, 60, 36, label='自己写 Python', color=ARROW, label_pos=0.5, label_dy=1.6)
arrow(122, 43.5, 142, 36, label='接入外部服务', color=ARROW, label_pos=0.5, label_dy=1.6)

# 结论 B：Plugin
block(45, 32, 22, 9, NODE_B, '→ 用 PLUGIN', 'Python + plugin.yaml\n~/.hermes/plugins/xxx/', title_size=12)
block(45, 20, 22, 8, '#244a62', '典型：企业集成\n新增 CLI 子命令\n自定义钩子', None, title_size=9)

# 结论 C：MCP
block(142, 32, 22, 9, NODE_C, '→ 用 MCP', '独立进程 + JSON-RPC\nmcp_servers: 配置', title_size=12)
block(142, 20, 22, 8, '#3a2a5c', '典型：GitHub / Postgres\nFigma / Stripe\n跨 Agent 复用', None, title_size=9)

# 第 4 层：是否需要分发
arrow(45, 16, 65, 12, label='', color=ARROW)
arrow(142, 16, 122, 12, label='', color=ARROW)
block(93, 9.5, 68, 6.5, NODE_D, 'Q3: 想发布给社区复用？→ 用 AGENT PLUGINS v1.0.0 打包', None, title_size=11)
arrow(93, 6.5, 93, 3.5)
block(93, 2.5, 46, 3.5, '#4a6228', 'plugin.json + skills/ + mcp.json', None, title_size=9.5)

# 底部图例
ax.text(8, 12, '图例：', fontproperties=FONT_BOLD, fontsize=10, color=SUBT, ha='left', va='center')
legends = [
    ('#4a4f8a', '起点'),
    (NODE_Q, '决策节点'),
    (NODE_A, 'Skill'),
    (NODE_B, 'Plugin'),
    (NODE_C, 'MCP'),
    (NODE_D, 'Agent Plugins'),
]
lx = 20
for color, name in legends:
    rect = FancyBboxPatch((lx, 10.8), 3, 2.4, boxstyle="round,pad=0.02,rounding_size=0.2",
                          linewidth=0, facecolor=color)
    ax.add_patch(rect)
    ax.text(lx + 4, 12, name, fontproperties=FONT_REG, fontsize=8.5, color=TEXT, ha='left', va='center')
    lx += 8.5

plt.tight_layout()
plt.savefig('/root/hexo-template-edgeone/source/images/hermes-extension-decision-tree-2026.png',
            facecolor=BG, bbox_inches='tight', pad_inches=0.3)
print('✅ 图 2 完成：hermes-extension-decision-tree-2026.png')

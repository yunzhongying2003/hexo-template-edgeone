#!/usr/bin/env python3
"""Hermes Agent 扩展机制全景图 — 四种机制 × 六个维度对比表"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch

# 中文字体
FONT_BOLD = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_REG  = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# 主题色（深色背景 + 蓝紫）
BG      = '#0f1226'
PANEL   = '#181c38'
HEADER  = '#2a2f5e'
CELL    = '#1e2348'
CELL_A  = '#2a2f5e'   # hover/强调
GRID    = '#3a3f70'
TITLE_C = '#ffffff'
SUB_C   = '#a8aede'
ACCENT  = '#7c9cff'   # 蓝
ACCENT2 = '#b58cff'   # 紫
GREEN   = '#4ade80'
YELLOW  = '#fbbf24'
RED     = '#f87171'
GREY    = '#6b7280'

fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.set_xlim(0, 160)
ax.set_ylim(0, 90)
ax.axis('off')

# 标题
ax.text(80, 85, 'Hermes Agent 扩展机制全景（2026）',
        fontproperties=FONT_BOLD, fontsize=22, color=TITLE_C, ha='center', va='center')
ax.text(80, 80.5, '四种机制 · 六个维度 · 一张表看明白选型',
        fontproperties=FONT_REG, fontsize=12, color=SUB_C, ha='center', va='center')

# 表格布局：1 列维度 + 4 列机制
col_x = [10, 38, 62, 86, 110, 134]   # 6 列中心 x
col_w = 22
row_h = 5.4
row_top = 76

# 表头行
header_y = row_top - 1.5
for i, x in enumerate(col_x):
    # 交替色块
    if i == 0:
        color = '#3a3f70'
        label = '维度 ↓  机制 →'
    elif i == 1:
        color = '#4c3d8a'  # skill 紫
        label = 'SKILL\n(Markdown)'
    elif i == 2:
        color = '#2c5f7f'  # plugin 青
        label = 'PLUGIN\n(Python ctx)'
    elif i == 3:
        color = '#4a3070'  # MCP 深紫
        label = 'MCP\n(独立进程)'
    else:
        color = '#3d4c28'  # Agent Plugins 绿
        label = 'AGENT\nPLUGINS v1.0'
    rect = FancyBboxPatch((x - col_w/2, header_y - 3.4), col_w, 6.8,
                          boxstyle="round,pad=0.02,rounding_size=0.5",
                          linewidth=0, facecolor=color)
    ax.add_patch(rect)
    # 表头文字：分两行时垂直居中，一行时居中
    if '\n' in label:
        ax.text(x, header_y + 0.5, label.split('\n')[0],
                fontproperties=FONT_BOLD, fontsize=11, color='white', ha='center', va='center')
        ax.text(x, header_y - 1.5, label.split('\n')[1],
                fontproperties=FONT_REG, fontsize=8, color='#e6e6ff', ha='center', va='center')
    else:
        ax.text(x, header_y, label,
                fontproperties=FONT_BOLD, fontsize=10, color='white', ha='center', va='center')

# 数据行：6 个维度
rows = [
    # (维度, skill, plugin, mcp, agent_plugins)
    ('触发方式', '自然语言匹配\n自动加载', '启动时注册\n模型主动调用', '启动时连接\n模型主动调用', '启动时安装\n客户端发现'),
    ('能力上限', '教 Agent 怎么做\n不新增工具', '新增工具/钩子/CLI\n最灵活', '外部服务工具\n可跨 Agent 复用', '打包 Skill+MCP\n跨 Agent 分发'),
    ('代码改动', '无代码\nMarkdown 文件', 'Python 代码\nplugin.yaml', '独立服务进程\nJSON-RPC', '目录打包\nplugin.json'),
    ('热重载', '√ 立即生效', '√ 重启即生效', '× 需服务运行', '× 客户端支持'),
    ('适用场景', '个人工作流\n团队最佳实践', '深度定制\n企业集成', '通用工具复用\n第三方生态', '发布到市场\n一次打包多用'),
    ('生态规模', '82 内置\n117 可选\n169 社区', 'pip 分发\n项目自定义', '数千服务器\n官方 + 社区', '新标准\n2026-08 发布'),
]

def cell_color(row_idx, col_idx, value):
    """给关键单元格上色"""
    v = value.replace('\n', '')
    if '无代码' in v or '✅ 立即' in v or '⚠' in v:
        if '⚠' in v:
            return '#4a2f2f'
        return '#2c4a2f'
    return CELL

row_y_start = row_top - 5.5
for i, (dim, a, b, c, d) in enumerate(rows):
    y = row_y_start - i * row_h
    # 维度列
    rect = FancyBboxPatch((col_x[0] - col_w/2, y - row_h + 1), col_w, row_h - 1,
                          boxstyle="round,pad=0.02,rounding_size=0.4",
                          linewidth=0, facecolor=HEADER)
    ax.add_patch(rect)
    ax.text(col_x[0], y - 0.2, dim, fontproperties=FONT_BOLD, fontsize=10,
            color=ACCENT, ha='center', va='center')

    for j, val in enumerate([a, b, c, d]):
        x = col_x[j+1]
        rect = FancyBboxPatch((x - col_w/2, y - row_h + 1), col_w, row_h - 1,
                              boxstyle="round,pad=0.02,rounding_size=0.4",
                              linewidth=0, facecolor=CELL)
        ax.add_patch(rect)
        # 多行文本
        lines = val.split('\n')
        if len(lines) == 1:
            # 单独行也检查颜色关键字
            if val.startswith('√'):
                color = GREEN
            elif val.startswith('×'):
                color = RED
            else:
                color = TITLE_C
            ax.text(x, y - 0.2, val, fontproperties=FONT_REG, fontsize=9,
                    color=color, ha='center', va='center')
        else:
            for k, line in enumerate(lines):
                yy = y - 0.2 - (len(lines)-1)*0.9/2 + k*0.9
                # √ × 单独着色（表头行/热重载行使用）
                if line.startswith('√'):
                    color = GREEN
                elif line.startswith('×'):
                    color = RED
                else:
                    color = TITLE_C
                ax.text(x, yy, line, fontproperties=FONT_REG, fontsize=9,
                        color=color, ha='center', va='center')

# 底部注解
ax.text(80, 4, '数据来源：Hermes Agent 官方文档 (v0.20.6) · awesome-hermes-skills · Agent Plugins 1.0.0 Spec (2026-08-06)',
        fontproperties=FONT_REG, fontsize=8, color=GREY, ha='center', va='center')
ax.text(80, 1.5, '© Golook · 2026',
        fontproperties=FONT_REG, fontsize=7, color=GREY, ha='center', va='center')

plt.tight_layout()
plt.savefig('/root/hexo-template-edgeone/source/images/hermes-extension-mechanisms-overview-2026.png',
            facecolor=BG, bbox_inches='tight', pad_inches=0.3)
print('✅ 图 1 完成：hermes-extension-mechanisms-overview-2026.png')

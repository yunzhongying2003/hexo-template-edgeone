#!/usr/bin/env python3
"""Hermes Agent 扩展机制全景图 — 四种机制 × 六个维度对比表

修复记录（2026-10-26）：
  1. 原 col_x 有 6 个 x 坐标，表头循环画了 6 个盒子，但数据只有 4 个机制 →
     最右列永远空白。现改为 NCOLS=5（1 维度列 + 4 机制列），表头与数据同长度。
  2. 原多行文字行距 0.9 单位 = 9px，而 fontsize=9 @ dpi=100 = 13.75px →
     行距小于字号，文字互相压叠。现按 LINE_SP 单位（>= fontsize/dpi 折算）计算行距，
     并按每格最大行数动态抬高该行高度。
"""
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
HEADER  = '#2a2f5e'
CELL    = '#1e2348'
TITLE_C = '#ffffff'
SUB_C   = '#a8aede'
ACCENT  = '#7c9cff'   # 蓝
GREEN   = '#4ade80'
RED     = '#f87171'
GREY    = '#6b7280'

FIG_W_IN, FIG_H_IN, DPI = 16, 9, 100
X_MAX, Y_MAX = 160, 90

# --- 版式几何（单位：数据坐标；1 单位 y = FIG_H_IN/Y_MAX*DPI px）---
PX_PER_UNIT_Y = FIG_H_IN / Y_MAX * DPI          # 1 单位 y 对应的像素数
FS_CELL = 9                                     # 正文字号
FS_HEAD = 11.5
FS_HEAD_SUB = 8.5
FS_DIM = 10.5
LINE_SP = (FS_CELL * 1.55) / PX_PER_UNIT_Y      # 行距单位：保证 > 一行字高
PAD_V = 1.0                                     # 单元格上下内边距（单位 y）

NMECH = 4                                        # 机制列数
NCOLS = NMECH + 1                                # 总列数（含维度列）
GAP = 2.6                                        # 列间隙
COLOFF = 14                                     # 左侧留白
COL_W = 26.6
col_x = [COLOFF + GAP / 2 + i * (COL_W + GAP) for i in range(NCOLS)]

# --- 表头（1 维度列 + 4 机制列，长度与数据严格一致）---
HEADERS = [
    ('维度 ↓  机制 →', '#3a3f70', None),
    ('SKILL', '#4c3d8a', 'Markdown'),
    ('PLUGIN', '#2c5f7f', 'Python ctx'),
    ('MCP', '#4a3070', '独立进程'),
    ('AGENT PLUGINS', '#3d4c28', 'v1.0'),
]
HEAD_H = 7.4

# --- 数据行：6 个维度 × 4 机制 ---
ROWS = [
    ('触发方式', '自然语言匹配\n自动加载', '启动时注册\n模型主动调用', '启动时连接\n模型主动调用', '启动时安装\n客户端发现'),
    ('能力上限', '教 Agent 怎么做\n不新增工具', '新增工具/钩子/CLI\n最灵活', '外部服务工具\n可跨 Agent 复用', '打包 Skill+MCP\n跨 Agent 分发'),
    ('代码改动', '无代码\nMarkdown 文件', 'Python 代码\nplugin.yaml', '独立服务进程\nJSON-RPC', '目录打包\nplugin.json'),
    ('热重载',   '√ 立即生效', '√ 重启即生效', '× 需服务运行', '× 客户端支持'),
    ('适用场景', '个人工作流\n团队最佳实践', '深度定制\n企业集成', '通用工具复用\n第三方生态', '发布到市场\n一次打包多用'),
    ('生态规模', '82 内置\n117 可选\n169 社区', 'pip 分发\n项目自定义', '数千服务器\n官方 + 社区', '新标准\n2026-08 发布'),
]


def nlines(val):
    return len(val.split('\n'))


def cell_h(vals):
    """按该行最大行数算出所需行高，保证不压叠、不溢出。"""
    need = max(nlines(v) for v in vals) * LINE_SP + PAD_V * 2
    return max(need, 5.6)


def draw_cell(ax, x, y_top, w, h, color):
    ax.add_patch(FancyBboxPatch(
        (x - w / 2, y_top - h), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.5",
        linewidth=0, facecolor=color, zorder=1))


def cell_text_color(val):
    """热重载行按 √/× 着色，其余白色。"""
    if val.startswith('√'):
        return GREEN
    if val.startswith('×'):
        return RED
    return TITLE_C


fig, ax = plt.subplots(figsize=(FIG_W_IN, FIG_H_IN), dpi=DPI)
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.set_xlim(0, X_MAX)
ax.set_ylim(0, Y_MAX)
ax.axis('off')

# 标题
ax.text(80, Y_MAX - 5, 'Hermes Agent 扩展机制全景（2026）',
        fontproperties=FONT_BOLD, fontsize=22, color=TITLE_C, ha='center', va='center', zorder=2)
ax.text(80, Y_MAX - 10, '四种机制 · 六个维度 · 一张表看明白选型',
        fontproperties=FONT_REG, fontsize=12, color=SUB_C, ha='center', va='center', zorder=2)

# 表头行
head_top = Y_MAX - 13.5
draw_cell(ax, col_x[0], head_top, COL_W, HEAD_H, '#3a3f70')
ax.text(col_x[0], head_top - HEAD_H / 2, '维度 ↓  机制 →',
        fontproperties=FONT_BOLD, fontsize=FS_HEAD_SUB, color='white',
        ha='center', va='center', zorder=2)

for j in range(1, NCOLS):
    name, color, sub = HEADERS[j]
    draw_cell(ax, col_x[j], head_top, COL_W, HEAD_H, color)
    cy = head_top - HEAD_H / 2
    if sub:
        ax.text(col_x[j], cy + 1.5, name, fontproperties=FONT_BOLD, fontsize=FS_HEAD,
                color='white', ha='center', va='center', zorder=2)
        ax.text(col_x[j], cy - 1.7, sub, fontproperties=FONT_REG, fontsize=FS_HEAD_SUB,
                color='#e6e6ff', ha='center', va='center', zorder=2)
    else:
        ax.text(col_x[j], cy, name, fontproperties=FONT_BOLD, fontsize=FS_HEAD,
                color='white', ha='center', va='center', zorder=2)

# 数据行（行高按内容动态计算，逐行下推）
y_cursor = head_top - HEAD_H - 2.2
for dim, *vals in ROWS:
    h = cell_h(vals)
    # 维度列
    draw_cell(ax, col_x[0], y_cursor, COL_W, h, HEADER)
    ax.text(col_x[0], y_cursor - h / 2, dim, fontproperties=FONT_BOLD, fontsize=FS_DIM,
            color=ACCENT, ha='center', va='center', zorder=2)
    # 机制列
    for j, val in enumerate(vals):
        draw_cell(ax, col_x[j + 1], y_cursor, COL_W, h, CELL)
        lines = val.split('\n')
        color = cell_text_color(val)
        if len(lines) == 1:
            ax.text(col_x[j + 1], y_cursor - h / 2, lines[0], fontproperties=FONT_REG,
                    fontsize=FS_CELL, color=color, ha='center', va='center', zorder=2)
        else:
            block_h = (len(lines) - 1) * LINE_SP
            first_y = y_cursor - h / 2 + block_h / 2
            for k, line in enumerate(lines):
                ax.text(col_x[j + 1], first_y - k * LINE_SP, line,
                        fontproperties=FONT_REG, fontsize=FS_CELL, color=color,
                        ha='center', va='center', zorder=2)
    y_cursor -= h + 2.0

# 底部注解
ax.text(80, 5, '数据来源：Hermes Agent 官方文档 (v0.20.6) · awesome-hermes-skills · Agent Plugins 1.0.0 Spec (2026-08-06)',
        fontproperties=FONT_REG, fontsize=8, color=GREY, ha='center', va='center', zorder=2)
ax.text(80, 2, '© Golook · 2026',
        fontproperties=FONT_REG, fontsize=7, color=GREY, ha='center', va='center', zorder=2)

plt.tight_layout(pad=0.6)
plt.savefig('/root/hexo-template-edgeone/source/images/hermes-extension-mechanisms-overview-2026.png',
            facecolor=BG, bbox_inches='tight', pad_inches=0.35)
print('✅ 图 1 完成：hermes-extension-mechanisms-overview-2026.png')
print(f'   列数={NCOLS} 行距={LINE_SP:.2f}单位({LINE_SP*PX_PER_UNIT_Y:.1f}px) '
      f'字高={FS_CELL/PX_PER_UNIT_Y:.2f}单位 行数比={LINE_SP/(FS_CELL/PX_PER_UNIT_Y):.2f}')

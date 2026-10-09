#!/usr/bin/env python3
"""AI 浏览器自动化工具对比图 — Golook 博客配图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

FONT_BOLD = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_REG  = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

BG = '#0d1117'
FG = '#e6edf3'
GRID = '#30363d'

# 工具颜色（5 种）
C = {
    'BU':  '#a78bfa',   # Browser Use - 紫
    'SH':  '#34d399',   # Stagehand   - 绿
    'PM':  '#60a5fa',   # Playwright MCP - 蓝
    'AB':  '#f59e0b',   # agent-browser - 橙
    'SK':  '#f472b6',   # Skyvern     - 粉
}

fig = plt.figure(figsize=(16, 9), facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
ax.set_xlim(0, 160)
ax.set_ylim(0, 90)
ax.axis('off')

# ================= 标题区 =================
ax.text(80, 84, 'AI Agent 浏览器自动化生态图谱', ha='center', va='center',
        fontproperties=FONT_BOLD, fontsize=24, color=FG)
ax.text(80, 78.5, 'Browser Use · Stagehand · Playwright MCP · agent-browser · Skyvern',
        ha='center', va='center', fontproperties=FONT_REG, fontsize=12, color='#8b949e')

# ================= 5 个工具卡（水平排列）=================
cards = [
    # (标签, 中文名, GitHub ⭐, 语言, 授权, 定位, x)
    ('BU', 'Browser Use',      '117.3k ★', 'Python',       'MIT',     '全自主 Agent 循环',     15),
    ('SH', 'Stagehand',        '25.4k ★',  'TS/Py/Go',     'MIT',     '代码持有 SDK，AI 原语', 40),
    ('PM', 'Playwright MCP',   '37.8k ★',  'TS (MCP)',     'Apache-2', 'MCP 工具服务器',       65),
    ('AB', 'agent-browser',    '43.5k ★',  'Rust CLI',     'Apache-2', 'CLI 快照+Ref，省 93% token', 90),
    ('SK', 'Skyvern',          '12k+ ★',   'Python',       'AGPL-3.0','视觉驱动工作流平台',   115),
]
for code, en, stars, lang, lic, role, cx in cards:
    color = C[code]
    w, h = 30, 18
    x0, y0 = cx - w/2, 55
    box = FancyBboxPatch((x0, y0), w, h,
                        boxstyle='round,pad=0.3,rounding_size=1.5',
                        linewidth=1.5, edgecolor=color, facecolor=BG)
    ax.add_patch(box)
    # 顶部色带
    ax.add_patch(plt.Rectangle((x0, y0+h-2.2), w, 2.2,
                               facecolor=color, edgecolor='none'))
    ax.text(cx, y0+h-1.1, code, ha='center', va='center',
            fontproperties=FONT_BOLD, fontsize=11, color='white')
    # 英文名
    ax.text(cx, y0+h-5, en, ha='center', va='center',
            fontproperties=FONT_BOLD, fontsize=13, color=color)
    # GitHub stars
    ax.text(cx, y0+h-8.5, stars, ha='center', va='center',
            fontproperties=FONT_BOLD, fontsize=11, color=FG)
    # 语言 + 授权
    ax.text(cx, y0+h-11.5, f'{lang} · {lic}', ha='center', va='center',
            fontproperties=FONT_REG, fontsize=9, color='#8b949e')
    # 定位
    ax.text(cx, y0+2.5, role, ha='center', va='center',
            fontproperties=FONT_REG, fontsize=9.5, color=FG)

# ================= 中间：分层图 =================
# 分层：上层 Agent 框架 / 中层 SDK/CLI / 底层 Playwright + CDP
def layer_box(x0, y0, w, h, title, subtitle, color):
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle='round,pad=0.2,rounding_size=1',
                                linewidth=1.2, edgecolor=color,
                                facecolor='#161b22'))
    ax.text(x0+w/2, y0+h-2.2, title, ha='center', va='center',
            fontproperties=FONT_BOLD, fontsize=12, color=color)
    ax.text(x0+w/2, y0+h-5, subtitle, ha='center', va='center',
            fontproperties=FONT_REG, fontsize=9, color=FG)

# 层 1：Agent 框架
layer_box(15, 34, 60, 12, '① Agent 框架（自主循环）',
          'Browser Use  ·  Claude Computer Use', C['BU'])
# 层 2：SDK / CLI
layer_box(80, 34, 65, 12, '② 代码 SDK & CLI（可控点）',
          'Stagehand  ·  Playwright MCP  ·  agent-browser', C['SH'])
# 层 3：平台/基础设施
layer_box(15, 14, 130, 14, '③ 浏览器基础设施 & 工作流平台',
          'Browserbase（托管会话）  ·  Steel  ·  Skyvern（工作流+APA）', C['SK'])

# 连接箭头（工具卡到所属层）
arrows = [
    (15,  55,  25, 46, C['BU']),  # BU -> Agent 框架
    (15,  55,  15, 34, C['BU']),  # BU -> 基础设施（长箭头，双身份）
    (40,  55,  55, 46, C['SH']),  # SH -> SDK/CLI
    (65,  55,  80, 46, C['PM']),  # PM -> SDK/CLI
    (90,  55, 100, 46, C['AB']),  # AB -> SDK/CLI
    (115, 55, 115, 46, C['SK']),  # SK -> 基础设施（下穿到 layer3）
]
for x1, y1, x2, y2, color in arrows:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle='-|>', mutation_scale=12,
                                 linewidth=1.2, color=color,
                                 shrinkA=3, shrinkB=3, alpha=0.7))

# 基础设施 -> 底层浏览器
ax.add_patch(FancyArrowPatch((80, 14), (80, 6),
                             arrowstyle='-|>', mutation_scale=14,
                             linewidth=1.6, color='#8b949e'))
# 底层浏览器层
ax.add_patch(FancyBboxPatch((40, 0.5), 80, 6,
                            boxstyle='round,pad=0.2,rounding_size=1',
                            linewidth=1.2, edgecolor='#8b949e',
                            facecolor='#161b22'))
ax.text(80, 3.5, 'Chromium / CDP（Chrome DevTools Protocol）', ha='center', va='center',
        fontproperties=FONT_BOLD, fontsize=11, color=FG)

# ================= 底部说明 =================
ax.text(80, -0.5, '数据来源：GitHub 官方仓库（2026-10） · MIT / Apache-2 / AGPL 混合生态',
        ha='center', va='center', fontproperties=FONT_REG, fontsize=8.5, color='#8b949e')

out = '/root/hexo-template-edgeone/source/images/browser-automation-landscape-2026.png'
plt.savefig(out, dpi=150, facecolor=BG, bbox_inches='tight', pad_inches=0.3)
print(f'saved: {out}')

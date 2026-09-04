#!/usr/bin/env python3
"""2026 Deep Research 工具对比概览图"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

font_bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font_regular = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.set_facecolor('#0f0f1a')
fig.patch.set_facecolor('#0f0f1a')
ax.axis('off')

# Title
ax.text(8, 8.55, '2026 Deep Research 六大工具全景对比', fontproperties=font_bold,
        fontsize=22, color='white', ha='center', va='center')
ax.text(8, 8.12, 'ChatGPT · Perplexity · Gemini · Claude · Grok · 选型指南（2026 年 9 月）',
        fontproperties=font_regular, fontsize=12, color='#8899bb', ha='center', va='center')

# Five product cards
products = [
    {'name': 'ChatGPT Deep Research', 'short': 'GPT Deep Research',
     'color': '#10a37f', 'price': '$20 起', 'quota': '10/月', 'hlm': '26.6%',
     'strength': '推理深度 · GAIA 王者'},
    {'name': 'Perplexity Deep Research', 'short': 'Perplexity',
     'color': '#3b82f6', 'price': '$20/月', 'quota': '20/天', 'hlm': '21.1%',
     'strength': '引用准确 · 高频首选'},
    {'name': 'Gemini Deep Research', 'short': 'Gemini',
     'color': '#8b5cf6', 'price': '$19.99/月', 'quota': '20/天', 'hlm': '—',
     'strength': 'Google 生态 · 1M 上下文'},
    {'name': 'Claude Deep Research', 'short': 'Claude',
     'color': '#d97757', 'price': '$20/月', 'quota': 'Pro 独占', 'hlm': '—',
     'strength': '报告写作 · 长文档'},
    {'name': 'Grok DeepSearch', 'short': 'Grok',
     'color': '#06b6d4', 'price': '$30/月', 'quota': '含 Pro', 'hlm': '—',
     'strength': 'X 实时数据 · 大上下文'},
]

# Bar data for comparison (bottom half)
bar_labels = ['Pro 月费\n(美元)', '月配额\n(相对)', 'GAIA 精度\n(相对)']
bar_data = {
    'ChatGPT': [20, 10, 26.6],
    'Perplexity': [20, 600, 21.1],
    'Gemini': [19.99, 600, 15],
    'Claude': [20, 25, 18],
    'Grok': [30, 20, 20],
}
bar_colors = ['#10a37f', '#3b82f6', '#8b5cf6', '#d97757', '#06b6d4']

# Row 1: five product cards
card_w = 2.85
card_h = 1.9
gap = 0.15
start_x = 0.2
y_top = 7.7
y_bot = 5.75

for i, p in enumerate(products):
    x = start_x + i * (card_w + gap)
    # Card rect
    rect = plt.Rectangle((x, y_bot), card_w, card_h,
                          linewidth=1.5, edgecolor=p['color'], facecolor=p['color'],
                          alpha=0.15)
    ax.add_patch(rect)
    # Bottom border accent
    accent = plt.Rectangle((x, y_bot), card_w, 0.05,
                            facecolor=p['color'], alpha=0.9, edgecolor='none')
    ax.add_patch(accent)

    # 标题（y_bot + h*0.72）
    ax.text(x + card_w/2, y_bot + card_h*0.78, p['short'],
            fontproperties=font_bold, fontsize=11, color='white',
            ha='center', va='center')
    # 英文名
    ax.text(x + card_w/2, y_bot + card_h*0.58, p['strength'],
            fontproperties=font_regular, fontsize=8.5, color='#c8d8f8',
            ha='center', va='center')
    # 价格 + 配额
    ax.text(x + card_w/2, y_bot + card_h*0.25, f'{p["price"]} · {p["quota"]}',
            fontproperties=font_bold, fontsize=9, color='white',
            ha='center', va='center')

# Row 2: metrics bar chart area
ax.text(8, 5.35, '核心指标对比（Pro 计划）', fontproperties=font_bold,
        fontsize=13, color='white', ha='center', va='center')

# Build bars for 3 metrics x 5 products
metrics = [
    ('月费（$）', '越低越好', [20, 20, 19.99, 20, 30], '#3b82f6'),
    ('月配额（次）', '越高越好', [10, 600, 600, 25, 20], '#10a37f'),
    ('HLE/GAIA 相对精度（%）', '越高越好', [26.6, 21.1, 15, 18, 20], '#f59e0b'),
]

bar_start_x = 0.2
bar_area_w = 15.6
bar_area_h = 2.5
bar_y_top = 5.0
bar_y_bot = 2.5

metric_row_h = bar_area_h / 3
for mi, (label, desc, vals, color) in enumerate(metrics):
    row_y = bar_y_bot + metric_row_h * (2 - mi)
    # Label
    ax.text(0.2, row_y + metric_row_h/2, f'{label}  {desc}',
            fontproperties=font_regular, fontsize=8.5, color='#a0b4d0',
            ha='left', va='center')
    # Bars
    bar_x = 2.2
    bar_total_w = 13.5
    bar_w = bar_total_w / 5 * 0.8
    bar_gap = bar_total_w / 5 * 0.2
    max_val = max(vals)
    for j, (v, bcolor) in enumerate(zip(vals, bar_colors)):
        ratio = v / max_val
        bx = bar_x + j * (bar_w + bar_gap)
        by = row_y + 0.15
        bh = metric_row_h - 0.35
        bheight = bh * ratio
        rect = plt.Rectangle((bx, by), bar_w, bheight,
                              facecolor=bcolor, alpha=0.75, edgecolor='white', linewidth=0.4)
        ax.add_patch(rect)
        # Value label above bar
        ax.text(bx + bar_w/2, by + bheight + 0.05, f'{v}',
                fontproperties=font_bold, fontsize=7.5, color='white',
                ha='center', va='bottom')

# Legend
legend_y = 2.05
legend_items = ['ChatGPT', 'Perplexity', 'Gemini', 'Claude', 'Grok']
for j, (name, bcolor) in enumerate(zip(legend_items, bar_colors)):
    lx = 1.0 + j * 2.8
    rect = plt.Rectangle((lx, legend_y - 0.08), 0.35, 0.16,
                          facecolor=bcolor, alpha=0.85, edgecolor='none')
    ax.add_patch(rect)
    ax.text(lx + 0.42, legend_y, name, fontproperties=font_regular,
            fontsize=9, color='white', ha='left', va='center')

# Key insights box
insight_x = 0.2
insight_y = 0.15
insight_w = 15.6
insight_h = 1.4
insight_rect = plt.Rectangle((insight_x, insight_y), insight_w, insight_h,
                               facecolor='#1a1a2e', edgecolor='#334466',
                               linewidth=1, alpha=0.9)
ax.add_patch(insight_rect)
ax.text(insight_x + insight_w/2, insight_y + insight_h*0.78,
        '核心结论', fontproperties=font_bold, fontsize=11,
        color='white', ha='center', va='center')
ax.text(insight_x + insight_w/2, insight_y + insight_h*0.45,
        '高频研究选 Perplexity（月配额 600 次）  ·  重推理深度选 ChatGPT（GAIA 72.6%）  ·  生态整合选 Gemini  ·  实时资讯选 Grok  ·  报告写作选 Claude',
        fontproperties=font_regular, fontsize=8.5, color='#c8d8f8',
        ha='center', va='center')
ax.text(insight_x + insight_w/2, insight_y + insight_h*0.18,
        '数据源（2026-09）：OpenAI / Anthropic / Google / xAI / Perplexity 官方定价页、HLE 与 GAIA 基准',
        fontproperties=font_regular, fontsize=7, color='#8899bb',
        ha='center', va='center')

plt.tight_layout(pad=0.3)
plt.savefig('/root/hexo-template-edgeone/source/images/deep-research-tools-overview-2026.png',
            facecolor=fig.get_facecolor(), bbox_inches='tight')
print('Done.')

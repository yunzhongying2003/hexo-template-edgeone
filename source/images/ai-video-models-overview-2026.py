#!/usr/bin/env python3
"""
2026 AI 视频生成模型对比图 — Golook 博客配图
规则：Matplotlib + Noto Sans CJK，深色科技风，16:9
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

# 字体
FONT_BOLD = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
FONT_REG = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# 画布 16:9
fig, ax = plt.subplots(figsize=(16, 9), dpi=100)
fig.patch.set_facecolor('#0b1020')
ax.set_facecolor('#0b1020')
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 标题
ax.text(8, 8.55, '2026 AI 视频生成模型全景对比',
        fontproperties=FONT_BOLD, fontsize=22, color='white',
        ha='center', va='center')
ax.text(8, 8.05, 'Gemini Omni Flash · Veo 3.1 · Kling 3.0 · Runway Gen-4.5 · MiniMax H3 · Luma Ray3.2 · Seedance 2.0',
        fontproperties=FONT_REG, fontsize=11, color='#a0aec0',
        ha='center', va='center')

# 主区：Elo 得分条形（Artificial Analysis Text-to-Video with Audio, Sep 2026）
# 数据：Elo 分（Artificial Analysis Video Arena, 2026-09-26）
elo_data = [
    ('Gemini Omni Flash', 'Google',      1233, '#fbbf24'),
    ('Wan 3.0',           'Alibaba',     1229, '#f97316'),
    ('MiniMax H3 Max',    'MiniMax/fal', 1227, '#22d3ee'),
    ('MiniMax H3',        'MiniMax',     1218, '#22d3ee'),
    ('Seedance 2.0',      'ByteDance',   1205, '#ef4444'),
    ('Veo 3.1',           'Google',      1198, '#fbbf24'),
    ('Kling 3.0',         'Kuaishou',    1185, '#34d399'),
    ('Runway Gen-4.5',    'Runway',      1180, '#f472b6'),
    ('Luma Ray3.2',       'Luma',        1172, '#818cf8'),
]
# Sora 2 已下线，单列显示
sora_label = ('Sora 2 (OpenAI)', '已下线 · 2026-09-24 API 停止')

# 布局：左 60% 是 Elo 条，右 40% 是功能矩阵
bar_x0 = 4.6
bar_y_top = 7.35
bar_row_h = 0.42
bar_max_x = 3.6  # 最长条的图长度
elo_min = 1160
elo_max = 1240

# 左侧标签栏
ax.text(0.25, 7.62, '模型（Elo 分）', fontproperties=FONT_BOLD, fontsize=11, color='#e2e8f0', va='center')
ax.text(4.4, 7.62, '得分', fontproperties=FONT_BOLD, fontsize=11, color='#e2e8f0', va='center', ha='right')
ax.text(4.6, 7.62, '', fontproperties=FONT_REG, fontsize=1)

for i, (name, vendor, elo, color) in enumerate(elo_data):
    y = bar_y_top - i * bar_row_h - 0.28
    # 名字
    ax.text(0.25, y, name, fontproperties=FONT_BOLD, fontsize=9.5, color='white', va='center')
    ax.text(0.25 + len(name) * 0.115, y, f'  ·  {vendor}',
            fontproperties=FONT_REG, fontsize=7.5, color='#94a3b8', va='center')
    # 条
    bar_len = (elo - elo_min) / (elo_max - elo_min) * bar_max_x
    ax.add_patch(FancyBboxPatch((bar_x0, y - 0.13), bar_len, 0.26,
                                boxstyle="round,pad=0,rounding_size=0.03",
                                linewidth=0, facecolor=color))
    # Elo 数字放条右侧
    ax.text(bar_x0 + bar_len + 0.12, y, str(elo),
            fontproperties=FONT_BOLD, fontsize=9.5, color='white', va='center')

# 底部：Sora 2 特殊标注（灰色）
sora_y = bar_y_top - 8 * bar_row_h - 0.28
ax.text(0.25, sora_y, 'Sora 2', fontproperties=FONT_BOLD, fontsize=9.5, color='#94a3b8', va='center')
ax.text(1.35, sora_y, '  ·  OpenAI',
        fontproperties=FONT_REG, fontsize=7.5, color='#64748b', va='center')
ax.add_patch(Rectangle((bar_x0, sora_y - 0.11), bar_max_x, 0.22,
                       facecolor='#1e293b', edgecolor='#475569', linewidth=1,
                       linestyle='--'))
ax.text(bar_x0 + bar_max_x/2, sora_y, '已下线 · API 2026-09-24 停止',
        fontproperties=FONT_REG, fontsize=8.5, color='#94a3b8',
        va='center', ha='center')

# 数据来源脚注
ax.text(0.25, 0.35, '数据来源：Artificial Analysis Video Arena Text-to-Video with Audio 榜单 · 2026-09-26',
        fontproperties=FONT_REG, fontsize=7.5, color='#64748b', va='center')

# ===== 右侧：功能/成本矩阵 =====
right_x = 8.55
ax.text(right_x, 7.62, '核心能力与成本', fontproperties=FONT_BOLD, fontsize=11, color='#e2e8f0', va='center')

# 表格列
col_x = [right_x, right_x + 1.6, right_x + 3.2, right_x + 4.6]
headers = ['能力', 'Veo 3.1', 'Kling 3.0', 'Gen-4.5']
for i, h in enumerate(headers):
    color = '#22d3ee' if h == '能力' else '#f1f5f9'
    fw = FONT_BOLD if h != '能力' else FONT_BOLD
    ax.text(col_x[i] + 0.02, 7.28, h, fontproperties=fw, fontsize=9, color=color, va='center')

# 底部分隔线
ax.plot([right_x - 0.1, col_x[3] + 1.4], [7.14, 7.14], color='#334155', linewidth=0.8)

# 数据行
rows = [
    ('最大时长', '8s', '10s', '16s'),
    ('原生 4K', '是', '是', '否 · 4K 上采样'),
    ('原生音频', '有', '无 · 加购', '有'),
    ('API 单价', '$0.40/s', '$15-20/min', '12 credits/s'),
    ('免费额度', '无', '166 credits/日', '125 一次性'),
    ('授权友好', '商业', '商业', '商业'),
    ('生态', 'Google Cloud', '快手', '创意套件'),
]
row_h = 0.42
for i, (label, v1, v2, v3) in enumerate(rows):
    y = 6.72 - i * row_h
    # 斑马纹
    if i % 2 == 0:
        ax.add_patch(Rectangle((right_x - 0.15, y - 0.16), 6.3, 0.32,
                               facecolor='#111827', edgecolor='none'))
    ax.text(col_x[0] + 0.02, y, label,
            fontproperties=FONT_REG, fontsize=8.8, color='#94a3b8', va='center')
    ax.text(col_x[1] + 0.02, y, v1,
            fontproperties=FONT_BOLD, fontsize=9, color='#e2e8f0', va='center')
    ax.text(col_x[2] + 0.02, y, v2,
            fontproperties=FONT_BOLD, fontsize=9, color='#e2e8f0', va='center')
    ax.text(col_x[3] + 0.02, y, v3,
            fontproperties=FONT_BOLD, fontsize=9, color='#e2e8f0', va='center')

# 底部：决策卡（三条建议）
advice_y = 2.9
advice_w = 1.85
gap = 0.15
advice_x0 = right_x
cards = [
    ('预算优先', 'Kling 3.0\n$6.99/月 · 免费 166/日', '#34d399'),
    ('质量优先', 'Veo 3.1 Standard\n原生 4K + 原生音频', '#fbbf24'),
    ('导演控制', 'Runway Gen-4.5\nMotion Brush + Director', '#f472b6'),
]
for i, (title, desc, color) in enumerate(cards):
    x = advice_x0 + i * (advice_w + gap)
    # 卡片背景
    ax.add_patch(FancyBboxPatch((x, advice_y - 0.7), advice_w, 1.25,
                                boxstyle="round,pad=0.02,rounding_size=0.08",
                                facecolor=color, edgecolor='none'))
    # 标题（卡片上方）
    ax.text(x + advice_w/2, advice_y + 0.72, title,
            fontproperties=FONT_BOLD, fontsize=10.5, color='white',
            va='center', ha='center')
    # 描述两行
    lines = desc.split('\n')
    ax.text(x + advice_w/2, advice_y + 0.28, lines[0],
            fontproperties=FONT_BOLD, fontsize=9.5, color='white',
            va='center', ha='center')
    if len(lines) > 1:
        ax.text(x + advice_w/2, advice_y - 0.08, lines[1],
                fontproperties=FONT_REG, fontsize=8.2, color='#ffffff',
                va='center', ha='center', alpha=0.95)

# 关键洞察框（底部左侧，跨越全宽）
insight_y = 1.35
ax.add_patch(FancyBboxPatch((0.25, insight_y - 0.5), 15.5, 0.85,
                            boxstyle="round,pad=0.02,rounding_size=0.06",
                            facecolor='#1e1b4b', edgecolor='#6366f1', linewidth=1.2))
ax.text(0.55, insight_y + 0.12, '【2026 关键信号】',
        fontproperties=FONT_BOLD, fontsize=11, color='#a5b4fc', va='center')
ax.text(0.55, insight_y - 0.18,
        'Sora 2 完全下线（App 4-26 / API 9-24） · Gemini Omni Flash 登顶 · 中国模型进入前三 · 价格与质量彻底脱钩（H3 Max $2.4/min vs Veo 3.1 $24/min）',
        fontproperties=FONT_REG, fontsize=9.5, color='#e2e8f0', va='center')

# 保存
out_path = os.path.join(os.path.dirname(__file__), 'ai-video-models-overview-2026.png')
plt.tight_layout(pad=0.3)
plt.savefig(out_path, dpi=120, facecolor=fig.get_facecolor(), bbox_inches='tight', pad_inches=0.3)
plt.close()
print(f'Saved: {out_path}')
print(f'Size: {os.path.getsize(out_path)} bytes')

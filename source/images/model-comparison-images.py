import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 中文字体
font_bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font_reg = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# 配色方案：深色背景蓝紫
BG = '#0d0d1a'
GRID = '#1e1e3a'
C_LAVENDER = '#8b7cf6'  # purple for Claude
C_TEAL = '#4fd1c5'      # teal for OpenAI
C_CYAN = '#38bdf8'      # cyan for Gemini
TEXT = '#e2e8f0'
TEXT_DIM = '#8892b0'

fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG)
ax.set_facecolor(BG)

# --- 数据 ---
models = ['Claude\nFable 5', 'GPT-5.2', 'Gemini\n3.5 Pro']
# GPQA Diamond
gpqa = [91.3, 93.2, 93.8]
# AIME 2025
aime = [82.0, 100.0, 96.7]
# SWE-bench Verified
swe = [74.9, 70.0, 76.2]
# Context (100K)
ctx = [10, 4, 20]  # in units of 100K tokens
# Input price ($/MTok)
price = [10.0, 1.75, 2.5]

x = np.arange(len(models))
w = 0.25

bars1 = ax.bar(x - w, gpqa, w, label='GPQA Diamond (%)', color=C_LAVENDER, alpha=0.9, zorder=3)
bars2 = ax.bar(x,     aime, w, label='AIME 2025 (%)', color=C_TEAL, alpha=0.9, zorder=3)
bars3 = ax.bar(x + w, swe, w, label='SWE-bench Verified (%)', color=C_CYAN, alpha=0.9, zorder=3)

# 数值标注
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f}', xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 4), textcoords='offset points',
                    ha='center', fontsize=9, color=TEXT, fontproperties=font_reg)

ax.set_xticks(x)
ax.set_xticklabels(models, fontproperties=font_bold, color=TEXT, fontsize=12)
ax.set_ylabel('分数 (%)', fontproperties=font_bold, color=TEXT, fontsize=12)
ax.set_ylim(0, 115)
ax.tick_params(colors=TEXT_DIM, labelsize=10)
ax.grid(axis='y', color=GRID, linewidth=0.8, zorder=0)
ax.spines[:].set_color(GRID)

# 第二个 Y 轴：上下文窗口
ax2 = ax.twinx()
ax2.set_facecolor(BG)
ctx_vals = [10, 4, 20]
ctx_colors = [C_LAVENDER, C_TEAL, C_CYAN]
for i, (v, c) in enumerate(zip(ctx_vals, ctx_colors)):
    ax2.scatter(x[i], v, s=300, color=c, edgecolors=BG, linewidths=2, zorder=5, marker='D')
    ax2.annotate(f'{v}×100K', (x[i], v), xytext=(0, 16), textcoords='offset points',
                 ha='center', fontsize=9, color=c, fontproperties=font_reg)
ax2.set_ylabel('上下文窗口', fontproperties=font_bold, color=TEXT_DIM, fontsize=11)
ax2.set_ylim(0, 25)
ax2.tick_params(colors=TEXT_DIM, labelsize=9)
ax2.spines[:].set_color(GRID)

# 标题
ax.set_title('2026 旗舰推理模型：性能 × 上下文 × 价格全维度对比',
             fontproperties=font_bold, color=TEXT, fontsize=18, pad=20)

# 图例
ax.legend(loc='upper right', framealpha=0.15, facecolor=BG,
          labelcolor=TEXT, prop=font_reg, fontsize=10)

# 底部价格注释
ax.text(0.5, -0.12,
        '输入价格 ($/M Tokens)：Claude Fable 5 $10 ｜ GPT-5.2 $1.75 ｜ Gemini 3.5 Pro ~$2.5  |  数据截至 2026-07',
        transform=ax.transAxes, ha='center', fontsize=9,
        color=TEXT_DIM, fontproperties=font_reg)

plt.tight_layout()
fig.savefig('/root/hexo-template-edgeone/source/images/model-comparison-header-2026.png',
            dpi=150, facecolor=BG, bbox_inches='tight')
print('Saved!')

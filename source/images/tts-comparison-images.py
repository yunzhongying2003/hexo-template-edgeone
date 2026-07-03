import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np

# Fonts
font_bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font_reg = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# Color palette
bg_color = '#0f172a'
card_bg = '#1e293b'
accent_blue = '#3b82f6'
accent_purple = '#8b5cf6'
accent_cyan = '#06b6d4'
accent_green = '#10b981'
accent_orange = '#f59e0b'
accent_red = '#ef4444'
text_primary = '#f1f5f9'
text_secondary = '#94a3b8'
text_muted = '#64748b'
grid_color = '#334155'

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.patch.set_facecolor(bg_color)

# ---- Chart 1: Commercial TTS Pricing (per 1K chars) ----
ax1 = axes[0, 0]
ax1.set_facecolor(card_bg)
tools = ['OpenAI TTS', 'ElevenLabs\nFlash', 'ElevenLabs\nMultilingual', 'Google\nCloud', 'Azure\nNeural']
prices = [0.015, 0.05, 0.10, 0.016, 0.016]  # per 1K chars
colors = [accent_blue, accent_green, accent_purple, accent_cyan, accent_orange]
bars = ax1.bar(range(len(tools)), prices, color=colors, width=0.6, edgecolor='none')
ax1.set_xticks(range(len(tools)))
ax1.set_xticklabels(tools, fontproperties=font_reg, fontsize=9, color=text_primary)
ax1.set_ylabel('价格 ($/1K 字符)', fontproperties=font_bold, fontsize=11, color=text_primary)
ax1.set_title('商业 TTS API 价格对比', fontproperties=font_bold, fontsize=13, color=text_primary, pad=12)
ax1.set_facecolor(card_bg)
ax1.tick_params(colors=text_muted)
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.yaxis.grid(True, color=grid_color, alpha=0.3)
ax1.set_axisbelow(True)
# Add value labels
for bar, price in zip(bars, prices):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
             f'${price}', ha='center', va='bottom', fontproperties=font_bold, fontsize=10, color=text_primary)

# ---- Chart 2: Open-source TTS GitHub Stars ----
ax2 = axes[0, 1]
ax2.set_facecolor(card_bg)
oss_tools = ['ChatTTS', 'Fish Speech', 'MeloTTS', 'Kokoro', 'XTTS v2']
stars = [39500, 31100, 10000, 8000, 15000]  # approximate
colors2 = [accent_purple, accent_blue, accent_cyan, accent_green, accent_orange]
bars2 = ax2.barh(range(len(oss_tools)), stars, color=colors2, height=0.6, edgecolor='none')
ax2.set_yticks(range(len(oss_tools)))
ax2.set_yticklabels(oss_tools, fontproperties=font_reg, fontsize=10, color=text_primary)
ax2.set_xlabel('GitHub Stars', fontproperties=font_bold, fontsize=11, color=text_primary)
ax2.set_title('开源 TTS 项目 GitHub 热度', fontproperties=font_bold, fontsize=13, color=text_primary, pad=12)
ax2.set_facecolor(card_bg)
ax2.tick_params(colors=text_muted)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.xaxis.grid(True, color=grid_color, alpha=0.3)
ax2.set_axisbelow(True)
for bar, star in zip(bars2, stars):
    ax2.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
             f'{star:,}', ha='left', va='center', fontproperties=font_bold, fontsize=10, color=text_primary)

# ---- Chart 3: Real-time TTS Arena Ranking (May 2026) ----
ax3 = axes[1, 0]
ax3.set_facecolor(card_bg)
arena_tools = ['Inworld\nRealtime TTS', 'StepAudio\n2.5 TTS', 'ElevenLabs\nEleven v3', 'Cartesia\nSonic 3', 'Deepgram\nAura-2']
elo_scores = [1208, 1187, 1178, 1150, 1130]  # approximate Elo
colors3 = [accent_green, accent_blue, accent_purple, accent_cyan, accent_orange]
bars3 = ax3.bar(range(len(arena_tools)), elo_scores, color=colors3, width=0.6, edgecolor='none')
ax3.set_xticks(range(len(arena_tools)))
ax3.set_xticklabels(arena_tools, fontproperties=font_reg, fontsize=9, color=text_primary)
ax3.set_ylabel('ELO 评分', fontproperties=font_bold, fontsize=11, color=text_primary)
ax3.set_title('实时 TTS Arena 排名 (2026年5月)', fontproperties=font_bold, fontsize=13, color=text_primary, pad=12)
ax3.set_facecolor(card_bg)
ax3.tick_params(colors=text_muted)
ax3.set_ylim(1100, 1230)
for spine in ax3.spines.values():
    spine.set_visible(False)
ax3.yaxis.grid(True, color=grid_color, alpha=0.3)
ax3.set_axisbelow(True)
for bar, score in zip(bars3, elo_scores):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             str(score), ha='center', va='bottom', fontproperties=font_bold, fontsize=10, color=text_primary)

# ---- Chart 4: TTS Selection Decision Tree ----
ax4 = axes[1, 1]
ax4.set_facecolor(card_bg)
ax4.set_xlim(0, 10)
ax4.set_ylim(0, 10)
ax4.axis('off')
ax4.set_title('TTS 选型决策树', fontproperties=font_bold, fontsize=13, color=text_primary, pad=12)

# Draw decision tree
def draw_box(ax, x, y, w, h, text, color, fontsize=9):
    rect = plt.Rectangle((x - w/2, y - h/2), w, h, facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontproperties=font_bold, fontsize=fontsize, color=text_primary, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color=text_muted):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# Root
draw_box(ax4, 5, 9, 3.5, 0.8, '需要 TTS？', accent_blue, 11)
# Branch 1: Commercial
draw_arrow(ax4, 5, 8.6, 2.5, 7.5)
draw_box(ax4, 2.5, 7, 3, 0.7, '商业 API', accent_green, 10)
draw_arrow(ax4, 2.5, 6.65, 1.2, 5.5)
draw_arrow(ax4, 2.5, 6.65, 3.8, 5.5)
draw_box(ax4, 1.2, 5.1, 2.2, 0.7, '追求极致质量\nElevenLabs', accent_purple, 8)
draw_box(ax4, 3.8, 5.1, 2.2, 0.7, '性价比优先\nOpenAI TTS', accent_cyan, 8)
# Branch 2: Open-source
draw_arrow(ax4, 5, 8.6, 7.5, 7.5)
draw_box(ax4, 7.5, 7, 3, 0.7, '开源方案', accent_orange, 10)
draw_arrow(ax4, 7.5, 6.65, 6.2, 5.5)
draw_arrow(ax4, 7.5, 6.65, 8.8, 5.5)
draw_box(ax4, 6.2, 5.1, 2.2, 0.7, '轻量快速\nKokoro / MeloTTS', accent_green, 8)
draw_box(ax4, 8.8, 5.1, 2.2, 0.7, '高质量克隆\nFish Speech', accent_purple, 8)
# Bottom row
draw_arrow(ax4, 1.2, 4.75, 1.2, 3.5)
draw_arrow(ax4, 3.8, 4.75, 3.8, 3.5)
draw_arrow(ax4, 6.2, 4.75, 6.2, 3.5)
draw_arrow(ax4, 8.8, 4.75, 8.8, 3.5)
draw_box(ax4, 1.2, 3.1, 2.2, 0.6, '视频配音/有声书', accent_blue, 7)
draw_box(ax4, 3.8, 3.1, 2.2, 0.6, '实时语音助手', accent_cyan, 7)
draw_box(ax4, 6.2, 3.1, 2.2, 0.6, '本地部署/隐私', accent_green, 7)
draw_box(ax4, 8.8, 3.1, 2.2, 0.6, '声音克隆/多语言', accent_purple, 7)

plt.tight_layout(pad=2)
plt.savefig('/root/hexo-template-edgeone/source/images/tts-comparison-overview-2026.png',
            dpi=150, facecolor=bg_color, edgecolor='none', bbox_inches='tight')
plt.close()
print("Image 1 saved: tts-comparison-overview-2026.png")

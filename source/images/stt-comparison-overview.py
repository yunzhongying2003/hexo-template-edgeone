#!/usr/bin/env python3
"""Generate STT tools comparison chart for blog article."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties
import numpy as np

font_bold = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
font_reg = FontProperties(fname='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')

# ============================================================
# Chart 1: STT Provider Comparison — WER vs. Price
# ============================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.patch.set_facecolor('#1a1a2e')

providers_short = ['Whisper\nL-V3', 'Canary\nQwen', 'Deepgram\nNova-3', 'AssemblyAI\nU-3 Pro',
                   'ElevenLabs\nScribe', 'GPT-4o\ntranscribe', 'MS\nMAI-T-1', 'NVIDIA\nParakeet']
wer_values = [7.4, 5.63, 5.26, 5.6, 6.2, 4.5, 3.8, 8.0]
price_values = [0.36, 0.30, 0.46, 0.45, 0.70, 1.02, 0.50, 0.15]

x = np.arange(len(providers_short))
w = 0.35

# Chart 1: WER bar chart
colors_wer = ['#e74c3c' if w > 7 else '#f39c12' if w > 6 else '#2ecc71' for w in wer_values]
ax1_bar1 = ax1.bar(x - w/2, wer_values, w, color=colors_wer, edgecolor='white', linewidth=0.5, alpha=0.9)
ax1.set_xticks(x)
ax1.set_xticklabels(providers_short, fontproperties=font_reg, fontsize=9, color='#cccccc')
ax1.set_ylabel('Word Error Rate (%)', fontproperties=font_bold, fontsize=12, color='#e0e0e0')
ax1.set_title('STT Model Accuracy (Lower WER = Better)', fontproperties=font_bold, fontsize=14, color='#ffffff', pad=15)
ax1.set_facecolor('#16213e')
ax1.tick_params(colors='#888888')
ax1.set_ylim(0, 11)
ax1.grid(axis='y', alpha=0.15, color='#555555')

for bar, val in zip(ax1_bar1, wer_values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{val}%', ha='center', va='bottom', fontproperties=font_bold,
             fontsize=9, color='#e0e0e0')

# Mark best
best_wer_idx = wer_values.index(min(wer_values))
ax1.text(best_wer_idx - w/2, min(wer_values) + 1.0,
         'BEST', ha='center', fontproperties=font_bold, fontsize=10, color='#f1c40f')

# Chart 2: Price per hour
price_colors = ['#3498db' if p < 0.4 else '#e67e22' if p < 0.6 else '#e74c3c' for p in price_values]
ax2_bar = ax2.bar(x, price_values, w*0.8, color=price_colors,
                  edgecolor='white', linewidth=0.5, alpha=0.9)
ax2.set_xticks(x)
ax2.set_xticklabels(providers_short, fontproperties=font_reg, fontsize=9, color='#cccccc')
ax2.set_ylabel('Price ($/hour)', fontproperties=font_bold, fontsize=12, color='#e0e0e0')
ax2.set_title('STT API Pricing (Lower = Better)', fontproperties=font_bold, fontsize=14, color='#ffffff', pad=15)
ax2.set_facecolor('#16213e')
ax2.tick_params(colors='#888888')
ax2.set_ylim(0, max(price_values) * 1.35)
ax2.grid(axis='y', alpha=0.15, color='#555555')

for bar, val in zip(ax2_bar, price_values):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'${val:.2f}', ha='center', va='bottom', fontproperties=font_bold,
             fontsize=9, color='#e0e0e0')

cheapest_idx = price_values.index(min(price_values))
ax2.text(cheapest_idx, min(price_values) + 0.08,
         'CHEAPEST', ha='center', fontproperties=font_bold, fontsize=10, color='#f1c40f')

plt.tight_layout(pad=3)
plt.savefig('/root/hexo-template-edgeone/source/images/stt-comparison-overview.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print("Chart 1 saved: stt-comparison-overview.png")

# ============================================================
# Chart 2: Selection Guide / Decision Tree
# ============================================================
fig2, ax3 = plt.subplots(figsize=(14, 8))
fig2.patch.set_facecolor('#1a1a2e')
ax3.set_facecolor('#16213e')
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 10)
ax3.axis('off')

ax3.text(5, 9.5, 'STT Selection Guide', fontproperties=font_bold, fontsize=18,
         ha='center', color='#ffffff')

# Top decision box
ax3.add_patch(mpatches.FancyBboxPatch((3.5, 7.8), 3.0, 1.2,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#0f3460', edgecolor='#e94560', linewidth=2))
ax3.text(5.0, 8.4, 'Your Use Case?', fontproperties=font_bold, fontsize=13,
         ha='center', color='#ffffff')

# Branch 1: Self-hosted
ax3.add_patch(mpatches.FancyBboxPatch((0.3, 5.8), 2.8, 1.2,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#1a3a5c', edgecolor='#3498db', linewidth=1.5))
ax3.text(1.7, 6.4, 'Self-Hosted / Open-Source', fontproperties=font_bold, fontsize=10,
         ha='center', color='#a8d8ea')
ax3.annotate('', xy=(5.0, 7.8), xytext=(1.7, 7.0),
             arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))

# Branch 2: Commercial API
ax3.add_patch(mpatches.FancyBboxPatch((3.3, 5.8), 3.0, 1.2,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#1a3a5c', edgecolor='#2ecc71', linewidth=1.5))
ax3.text(4.8, 6.4, 'Commercial API', fontproperties=font_bold, fontsize=10,
         ha='center', color='#a8d8ea')
ax3.annotate('', xy=(5.0, 7.8), xytext=(4.8, 7.0),
             arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))

# Branch 3: Real-time agent
ax3.add_patch(mpatches.FancyBboxPatch((6.8, 5.8), 2.8, 1.2,
                                       boxstyle="round,pad=0.1",
                                       facecolor='#1a3a5c', edgecolor='#f39c12', linewidth=1.5))
ax3.text(8.2, 6.4, 'Real-Time Voice Agent', fontproperties=font_bold, fontsize=10,
         ha='center', color='#a8d8ea')
ax3.annotate('', xy=(6.5, 8.4), xytext=(8.2, 7.0),
             arrowprops=dict(arrowstyle='->', color='#555555', lw=1.5))

# Self-hosted recommendations
ax3.add_patch(mpatches.FancyBboxPatch((0.1, 3.5), 3.0, 1.6,
                                       boxstyle="round,pad=0.2",
                                       facecolor='#0a1628', edgecolor='#3498db', linewidth=1))
ax3.text(0.2, 4.8, 'Top Picks:', fontproperties=font_bold, fontsize=10, color='#3498db')
ax3.text(0.2, 4.3, '  Canary Qwen 2.5B', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(0.2, 4.0, '  - Best accuracy (5.63% WER)', fontproperties=font_reg, fontsize=8, color='#888888')
ax3.text(0.2, 3.7, '  Whisper L-V3 Turbo', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(0.2, 3.4, '  - 99 languages, 216x RTF', fontproperties=font_reg, fontsize=8, color='#888888')

# Commercial recommendations
ax3.add_patch(mpatches.FancyBboxPatch((3.5, 3.5), 3.0, 1.6,
                                       boxstyle="round,pad=0.2",
                                       facecolor='#0a1628', edgecolor='#2ecc71', linewidth=1))
ax3.text(3.6, 4.8, 'Top Picks:', fontproperties=font_bold, fontsize=10, color='#2ecc71')
ax3.text(3.6, 4.3, '  Deepgram Nova-3', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(3.6, 4.0, '  - 5.26% WER, 300ms latency', fontproperties=font_reg, fontsize=8, color='#888888')
ax3.text(3.6, 3.7, '  GPT-4o-transcribe', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(3.6, 3.4, '  - Best overall (4.5% WER)', fontproperties=font_reg, fontsize=8, color='#888888')

# Real-time recommendations
ax3.add_patch(mpatches.FancyBboxPatch((6.8, 3.5), 3.0, 1.6,
                                       boxstyle="round,pad=0.2",
                                       facecolor='#0a1628', edgecolor='#f39c12', linewidth=1))
ax3.text(6.9, 4.8, 'Top Picks:', fontproperties=font_bold, fontsize=10, color='#f39c12')
ax3.text(6.9, 4.3, '  Deepgram Flux', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(6.9, 4.0, '  - Built-in EOT (<300ms)', fontproperties=font_reg, fontsize=8, color='#888888')
ax3.text(6.9, 3.7, '  ElevenLabs Scribe v2', fontproperties=font_reg, fontsize=9, color='#cccccc')
ax3.text(6.9, 3.4, '  - Sub-150ms predictive', fontproperties=font_reg, fontsize=8, color='#888888')

# Arrows from branches to recommendations
ax3.annotate('', xy=(1.7, 5.8), xytext=(1.7, 5.1), arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
ax3.annotate('', xy=(4.8, 5.8), xytext=(4.8, 5.1), arrowprops=dict(arrowstyle='->', color='#555555', lw=1))
ax3.annotate('', xy=(8.2, 5.8), xytext=(8.2, 5.1), arrowprops=dict(arrowstyle='->', color='#555555', lw=1))

# Footer
ax3.text(5, 1.2, 'Key Metrics: WER, RTF (Real-Time Factor), Latency (ms), Language Count, Price',
         fontproperties=font_reg, fontsize=9, ha='center', color='#888888')
ax3.text(5, 0.6, 'Data: Coval.ai (Jun 2026), HuggingFace Open ASR, Vendor Publications',
         fontproperties=font_reg, fontsize=8, ha='center', color='#666666')

plt.tight_layout(pad=2)
plt.savefig('/root/hexo-template-edgeone/source/images/stt-selection-guide.png',
            dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print("Chart 2 saved: stt-selection-guide.png")

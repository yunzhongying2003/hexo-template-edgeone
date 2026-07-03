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
text_primary = '#f1f5f9'
text_secondary = '#94a3b8'
text_muted = '#64748b'
grid_color = '#334155'

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(card_bg)

# Table data
headers = ['工具', '类型', '价格', '语言数', '声音克隆', '延迟', '最佳场景']
rows = [
    ['ElevenLabs', '商业 API', '$0.05-0.10/1K字', '32+', '支持(即时+专业)', '~200ms', '视频配音/有声书'],
    ['OpenAI TTS', '商业 API', '$0.015-0.03/1K字', '多语言', '不支持', '~300ms', '性价比首选'],
    ['Google Cloud TTS', '商业 API', '$0.016/1K字', '100+', '不支持', '~250ms', '企业集成'],
    ['Azure Speech', '商业 API', '$0.016/1K字', '100+', '支持(定制神经)', '~200ms', '企业/合规场景'],
    ['Inworld Realtime TTS', '商业 API', '$15/M字符', '多语言', '不支持', '<250ms P90', '实时语音助手'],
    ['Cartesia Sonic 3', '商业 API', '按量计费', '多语言', '支持', '<100ms TTFB', '超低延迟场景'],
    ['Fish Speech S2', '开源', '免费', '50+', '支持(短片段克隆)', '中等', '高质量克隆/多语言'],
    ['Kokoro-82M', '开源', '免费', '10+', '不支持', '极快', '轻量本地部署'],
    ['MeloTTS', '开源', '免费', '6+', '不支持', '极快(CPU)', '实时应用/嵌入式'],
    ['ChatTTS', '开源', '免费', '中英', '不支持', '中等', '对话式AI助手'],
    ['XTTS v2', '开源', '免费', '17', '支持(3秒克隆)', '较慢', '声音克隆实验'],
]

# Create table
table_data = [headers] + rows
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.13, 0.08, 0.15, 0.08, 0.13, 0.12, 0.15])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.2)

# Header style
for j in range(len(headers)):
    cell = table[(0, j)]
    cell.set_facecolor(accent_blue)
    cell.set_text_props(color=text_primary, fontproperties=font_bold, fontsize=11)
    cell.set_edgecolor('#1e3a5f')

# Row styles - alternate colors for commercial vs open-source
commercial_colors = ['#1e293b', '#253348']
oss_colors = ['#1a2332', '#223044']

for i in range(1, len(table_data)):
    for j in range(len(headers)):
        cell = table[(i, j)]
        if i <= 6:  # Commercial
            cell.set_facecolor(commercial_colors[(i-1) % 2])
        else:  # Open-source
            cell.set_facecolor(oss_colors[(i-7) % 2])
        cell.set_text_props(color=text_primary, fontproperties=font_reg, fontsize=9.5)
        cell.set_edgecolor('#2d3a4f')

# Highlight key cells
# Price column for OpenAI (best value)
table[(2, 2)].set_text_props(color=accent_green, fontproperties=font_bold, fontsize=9.5)
# Latency column for Cartesia (fastest)
table[(6, 5)].set_text_props(color=accent_cyan, fontproperties=font_bold, fontsize=9.5)
# Stars for ChatTTS
table[(9, 0)].set_text_props(color=accent_purple, fontproperties=font_bold, fontsize=9.5)

ax.set_title('2026 TTS 工具全景对比表', fontproperties=font_bold, fontsize=16, color=text_primary, pad=20)
ax.axis('off')

# Add legend
legend_y = 0.08
ax.text(0.02, legend_y, '[商业 API]', fontproperties=font_bold, fontsize=11, color=accent_blue, transform=ax.transAxes)
ax.text(0.25, legend_y, '[开源方案]', fontproperties=font_bold, fontsize=11, color=accent_green, transform=ax.transAxes)
ax.text(0.5, legend_y, '数据截至 2026年7月', fontproperties=font_reg, fontsize=9, color=text_muted, transform=ax.transAxes)

plt.tight_layout(pad=1)
plt.savefig('/root/hexo-template-edgeone/source/images/tts-full-comparison-table-2026.png',
            dpi=150, facecolor=bg_color, edgecolor='none', bbox_inches='tight')
plt.close()
print("Image 2 saved: tts-full-comparison-table-2026.png")

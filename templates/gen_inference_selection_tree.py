"""
生成文章配图 2：推理引擎选型决策流程图
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

FONT_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_bold = FontProperties(fname=FONT_BOLD_PATH, size=13)
font_reg = FontProperties(fname=FONT_REG_PATH, size=11)
font_small = FontProperties(fname=FONT_REG_PATH, size=10)
font_tiny = FontProperties(fname=FONT_REG_PATH, size=9)

fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')

# 标题
ax.text(8, 8.55, 'LLM 推理引擎选型决策树',
        fontproperties=font_bold, fontsize=17, color='#ffffff', ha='center', va='center')
ax.text(8, 8.10, '按核心诉求、模型规模、团队能力三维快速定位',
        fontproperties=font_reg, fontsize=11, color='#8b949e', ha='center', va='center')

def draw_node(x, y, w, h, text, sub, color, text_color='white'):
    r = mpatches.FancyBboxPatch((x, y), w, h,
                                 boxstyle='round,pad=0.06',
                                 linewidth=1.5, edgecolor=color,
                                 facecolor=color + '25')
    ax.add_patch(r)
    ax.text(x + w/2, y + h*0.72, text,
            fontproperties=font_bold, fontsize=12, color=text_color, ha='center', va='center')
    ax.text(x + w/2, y + h*0.28, sub,
            fontproperties=font_small, fontsize=9, color='#8b949e', ha='center', va='center')

def draw_arrow(x1, y1, x2, y2, label='', color='#58a6ff'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx + 0.05, my + 0.10, label,
                fontproperties=font_tiny, fontsize=8, color=color, ha='left', va='bottom')

# 入口节点
draw_node(6.2, 7.0, 3.6, 0.8, '我要部署 LLM 推理服务', 'Start · 明确核心诉求', '#c0c0c0')

# 第一层分叉：性能诉求
draw_node(1.0, 5.5, 4.5, 0.8, '追求极致吞吐 / 高并发', 'Throughput Priority', '#58a6ff')
draw_node(6.0, 5.5, 4.5, 0.8, '追求低延迟 / 长上下文', 'Latency Priority', '#3fb950')
draw_node(10.5, 5.5, 4.5, 0.8, '快速验证 / 简化部署', 'Ease of Deploy', '#d29922')

# 箭头 + 标签
ax.annotate('', xy=(3.2, 5.9), xytext=(6.5, 7.0),
            arrowprops=dict(arrowstyle='->', color='#58a6ff', lw=1.5))
ax.text(4.35, 6.65, '吞吐优先', fontproperties=font_tiny, fontsize=8, color='#58a6ff')

ax.annotate('', xy=(8.2, 5.9), xytext=(8.0, 7.0),
            arrowprops=dict(arrowstyle='->', color='#3fb950', lw=1.5))
ax.text(8.05, 6.65, '延迟优先', fontproperties=font_tiny, fontsize=8, color='#3fb950')

ax.annotate('', xy=(12.7, 5.9), xytext=(9.5, 7.0),
            arrowprops=dict(arrowstyle='->', color='#d29922', lw=1.5))
ax.text(11.15, 6.65, '易部署', fontproperties=font_tiny, fontsize=8, color='#d29922')

# 第二层（吞吐 → vLLM 或 TRT-LLM）
draw_node(0.5, 3.8, 5.5, 0.8, 'vLLM ★ 推荐 · 生产默认',
          '88.9k★  ·  PagedAttention  ·  模型支持最广', '#58a6ff')
draw_node(0.5, 2.6, 5.5, 0.8, 'TensorRT-LLM  极致性能但难调',
          '14.4k★  ·  需 NVIDIA GPU  ·  冷启动 28 分钟', '#f97583')

ax.annotate('', xy=(3.2, 4.2), xytext=(3.2, 5.5),
            arrowprops=dict(arrowstyle='->', color='#58a6ff', lw=1.5))
ax.text(3.28, 5.05, '默认路径', fontproperties=font_tiny, fontsize=8, color='#58a6ff')
ax.annotate('', xy=(3.2, 3.0), xytext=(3.2, 3.8),
            arrowprops=dict(arrowstyle='->', color='#f97583', lw=1.0, linestyle='dashed'))
ax.text(3.28, 3.45, '进阶 (1-2周调优)', fontproperties=font_tiny, fontsize=8, color='#f97583')

# 第二层（延迟 → SGLang）
draw_node(5.8, 3.8, 5.5, 0.8, 'SGLang ★ 推荐 · 低延迟王者',
          '31.5k★  ·  RadixAttention  ·  TTFT 80ms', '#3fb950')
draw_node(5.8, 2.6, 5.5, 0.8, 'vLLM (Chunked Prefill 开启)',
          '通用备选  ·  共享前缀增益不如 Radix', '#8b949e')

ax.annotate('', xy=(8.5, 4.2), xytext=(8.2, 5.5),
            arrowprops=dict(arrowstyle='->', color='#3fb950', lw=1.5))
ax.text(8.55, 5.05, '多轮对话/RAG', fontproperties=font_tiny, fontsize=8, color='#3fb950')
ax.annotate('', xy=(8.5, 3.0), xytext=(8.5, 3.8),
            arrowprops=dict(arrowstyle='->', color='#8b949e', lw=1.0, linestyle='dashed'))
ax.text(8.55, 3.45, '单一请求少共享', fontproperties=font_tiny, fontsize=8, color='#8b949e')

# 第二层（易部署 → TGI / llama-cpp-rs）
draw_node(10.3, 3.8, 5.5, 0.8, 'llama-cpp-rs ★ 推荐 · TGI 后继',
          'HF TGI 2026-03 归档  ·  Rust 原生', '#d29922')
draw_node(10.3, 2.6, 5.5, 0.8, 'TGI (archived) · 历史项目可用',
          '10.9k★  ·  IBM fork 仍在维护', '#8b949e')

ax.annotate('', xy=(13.0, 4.2), xytext=(12.7, 5.5),
            arrowprops=dict(arrowstyle='->', color='#d29922', lw=1.5))
ax.text(13.05, 5.05, '新项目', fontproperties=font_tiny, fontsize=8, color='#d29922')
ax.annotate('', xy=(13.0, 3.0), xytext=(13.0, 3.8),
            arrowprops=dict(arrowstyle='->', color='#8b949e', lw=1.0, linestyle='dashed'))
ax.text(13.05, 3.45, '存量旧项目', fontproperties=font_tiny, fontsize=8, color='#8b949e')

# 底部总结带
ax.axhline(y=1.6, xmin=0.03, xmax=0.97, color='#30363d', linewidth=1)
ax.text(8, 1.35, '关键判断维度', fontproperties=font_bold, fontsize=11, color='#58a6ff', ha='center', va='center')
ax.text(8, 0.95, '① 请求模式：批量吞吐 vs 实时交互  ② 前缀共享率：高共享选 SGLang，低共享选 vLLM  ③ 硬件：纯 NVIDIA 可选 TRT-LLM，异构环境用 vLLM',
        fontproperties=font_reg, fontsize=10, color='white', ha='center', va='center')
ax.text(8, 0.55, '④ 团队能力：快速上线选 vLLM / llama-cpp-rs，极限性能且有时间调优选 TensorRT-LLM',
        fontproperties=font_reg, fontsize=10, color='white', ha='center', va='center')

plt.tight_layout(pad=0.5)
out = '/root/hexo-template-edgeone/source/images/llm-inference-selection-tree-2026.png'
fig.savefig(out, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f'Saved: {out}')

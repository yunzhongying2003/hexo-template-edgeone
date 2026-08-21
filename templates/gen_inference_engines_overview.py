"""
生成文章配图 1：四大推理引擎技术架构总览（含中文标签）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.patches as mpatches

FONT_BOLD_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_bold = FontProperties(fname=FONT_BOLD_PATH, size=14)
font_reg = FontProperties(fname=FONT_REG_PATH, size=11)
font_small = FontProperties(fname=FONT_REG_PATH, size=9)

fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('#0d1117')
fig.patch.set_facecolor('#0d1117')

# 标题
ax.text(8, 8.55, '2026 LLM 推理服务引擎 · 技术内核对比总览',
        fontproperties=font_bold, fontsize=17, color='#ffffff', ha='center', va='center')
ax.text(8, 8.05, 'vLLM / SGLang / TGI / TensorRT-LLM  四引擎核心机制与适用场景',
        fontproperties=font_reg, fontsize=10, color='#8b949e', ha='center', va='center')

# 分隔线
ax.axhline(y=7.8, xmin=0.03, xmax=0.97, color='#30363d', linewidth=1)

# 四个引擎卡片
engines = [
    {
        'x': 0.3, 'w': 3.5,
        'name_cn': 'vLLM', 'name_en': 'vllm-project/vllm',
        'stars': '88.9k ★',
        'core_cn': 'PagedAttention 虚拟内存 KV Cache',
        'highlight_cn': '生产默认选择',
        'highlight_en': 'Production Default',
        'features_cn': [
            'Model Runner v2 GPU 原生内核',
            'PagedAttention 内存碎片 < 4%',
            'Tensor/Pipeline Parallelism 完善',
            'Speculative Decoding 动态投机',
            '89k ★ · 社区生态最活跃',
        ],
        'color': '#58a6ff',
    },
    {
        'x': 4.1, 'w': 3.5,
        'name_cn': 'SGLang', 'name_en': 'sgl-project/sglang',
        'stars': '31.5k ★',
        'core_cn': 'RadixAttention 前缀共享 KV Cache',
        'highlight_cn': '低延迟 · 长上下文王者',
        'highlight_en': 'Low-latency King',
        'features_cn': [
            'Radix Tree 缓存 前缀计算可复用',
            '共享上下文吞吐比 vLLM 高 29%',
            'TTFT p50 80-120ms 行业最快',
            'XGrammar 后端原生 JSON 输出',
            '40万+ GPU 部署 · LMSYS 主办',
        ],
        'color': '#3fb950',
    },
    {
        'x': 7.9, 'w': 3.5,
        'name_cn': 'TGI', 'name_en': 'huggingface/tgi',
        'stars': '10.9k ★',
        'core_cn': 'Rust 后端 · HF 生态集成',
        'highlight_cn': '易部署 · 已归档',
        'highlight_en': 'Easy Deploy · Archived',
        'features_cn': [
            'Rust + CUDA 后端 · 部署最简单',
            'HuggingFace Hub 原生对接',
            '自动 Tensor Parallel 开箱即用',
            '2026-03 已归档 · 转向 llama-cpp-rs',
            '10.9k ★ · IBM fork 仍在维护',
        ],
        'color': '#d29922',
    },
    {
        'x': 11.7, 'w': 3.5,
        'name_cn': 'TensorRT-LLM', 'name_en': 'NVIDIA/TensorRT-LLM',
        'stars': '14.4k ★',
        'core_cn': '编译优化 · CUDA Kernel 定制',
        'highlight_cn': '极致性能 · 需 NVIDIA',
        'highlight_en': 'Max Performance · NVIDIA',
        'features_cn': [
            '模型编译为 TRT Engine 一次优化',
            'Quantization / FP8 / NVFP4 全支持',
            '冷启动 ~28 分钟 · 启动最慢',
            'Q3 2026 路线图：KVCache V2 + 视频',
            '14.4k ★ · 需 1-2 周调优',
        ],
        'color': '#f97583',
    },
]

y_top = 7.5
y_bot = 2.0
card_h = y_top - y_bot

for eng in engines:
    x, w = eng['x'], eng['w']
    # 卡片背景
    rect = mpatches.FancyBboxPatch(
        (x, y_bot), w, card_h,
        boxstyle='round,pad=0.08',
        linewidth=2, edgecolor=eng['color'],
        facecolor=eng['color'] + '18'  # 半透明色
    )
    ax.add_patch(rect)

    # 顶部色带
    band_h = 0.55
    band = mpatches.FancyBboxPatch(
        (x + 0.04, y_top - band_h - 0.04), w - 0.08, band_h,
        boxstyle='round,pad=0.04',
        linewidth=0, facecolor=eng['color']
    )
    ax.add_patch(band)

    # 三层文字：名称（色带上）/ 核心机制（副标题）/ 特性列表
    # 名称
    ax.text(x + w/2, y_top - 0.30, eng['name_cn'],
            fontproperties=font_bold, fontsize=15, color='white', ha='center', va='center')
    # GitHub 地址
    ax.text(x + w/2, y_top - 0.60, eng['name_en'],
            fontproperties=font_small, fontsize=8, color='#8b949e', ha='center', va='center')

    # 核心机制标签
    core_y = y_bot + card_h * 0.58
    ax.text(x + w/2, core_y, eng['core_cn'],
            fontproperties=font_bold, fontsize=11, color=eng['color'], ha='center', va='center')

    # Star 数
    star_y = y_bot + card_h * 0.44
    ax.text(x + w/2, star_y, eng['stars'],
            fontproperties=font_reg, fontsize=10, color='#f2cc60', ha='center', va='center')

    # Highlight
    hi_y = y_bot + card_h * 0.30
    ax.text(x + w/2, hi_y, eng['highlight_cn'],
            fontproperties=font_bold, fontsize=11, color='white', ha='center', va='center')
    ax.text(x + w/2, hi_y - 0.18, eng['highlight_en'],
            fontproperties=font_small, fontsize=8, color='#8b949e', ha='center', va='center')

    # 底部分隔
    ax.axhline(y=y_bot + card_h * 0.18, xmin=(x)/16, xmax=(x + w)/16,
               color=eng['color'] + '80', linewidth=0.8)

    # 特性列表（描述层）
    feat_y_start = y_bot + card_h * 0.12
    for i, feat in enumerate(eng['features_cn']):
        fy = feat_y_start - (i + 1) * 0.18
        if fy < y_bot + 0.12:
            break
        ax.text(x + 0.25, fy, '· ' + feat,
                fontproperties=font_small, fontsize=8, color='#c9d1d9', ha='left', va='center')

# 底部结论区
ax.axhline(y=1.4, xmin=0.03, xmax=0.97, color='#30363d', linewidth=1)
ax.text(8, 1.10, '选型口诀', fontproperties=font_bold, fontsize=12, color='#58a6ff', ha='center', va='center')
ax.text(8, 0.72, '吞吐优先选 vLLM  ·  延迟优先选 SGLang  ·  易部署选 TGI(归档前)  ·  极致性能选 TensorRT-LLM',
        fontproperties=font_bold, fontsize=11, color='white', ha='center', va='center')
ax.text(8, 0.35, '数据源：vllm-project/vllm (88.9k★) · sgl-project/sglang (31.5k★) · huggingface/tgi (10.9k★) · NVIDIA/TensorRT-LLM (14.4k★)  2026-08',
        fontproperties=font_small, fontsize=7.5, color='#8b949e', ha='center', va='center')

plt.tight_layout(pad=0.5)
out = '/root/hexo-template-edgeone/source/images/llm-inference-engines-overview-2026.png'
fig.savefig(out, dpi=150, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print(f'Saved: {out}')

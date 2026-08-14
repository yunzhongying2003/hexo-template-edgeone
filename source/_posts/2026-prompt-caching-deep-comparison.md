---
title: Prompt Caching 实战全解：Anthropic vs OpenAI vs Gemini 缓存机制深度对比（2026）
date: 2026-08-14 11:01:45
tags: [prompt-caching, claude, openai, gemini, 成本优化, llm, cost-optimization]
categories: 深度分析
---

> **分析日期**：2026-08-14
> **涉及产品**：Anthropic Claude、OpenAI GPT 系列、Google Gemini 2.5+
> **核心问题**：如何让同样的 prompt 重复调用时少付 90% 的输入 token 费？

## 一、为什么要认真看待 Prompt Caching？

LLM API 计费的核心公式很简单：**输入 token 价格 × 输入 token 数 + 输出 token 价格 × 输出 token 数**。当你的 system prompt 有 3000 token、RAG 上下文有 5 万 token、工具定义又占 2000 token，每次请求都在为这些"几乎不变的内容"重复付费。

Prompt Caching 的本质：**把每次请求的"共享前缀"缓存起来，重复调用时只对新增部分做完整前向传播（prefill）**。三家大厂 2026 年都已落地，但机制、计费、最低门槛差别很大。

![三家大厂的 Prompt Caching 机制对比](/images/prompt-caching-three-providers-arch.png)

## 二、三大厂商缓存机制逐一拆解

### 2.1 Anthropic Claude：显式标记，精细可控

Claude 的缓存需要开发者**显式声明**。在 API 请求的某个 content block 上加 `cache_control` 标记：

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "以下是你需要的参考资料……",
      "cache_control": {"type": "ephemeral", "ttl": "1h"}
    },
    {"type": "text", "text": "用户的真实问题……"}
  ]
}
```

**关键规则**：

- **断点位置决定缓存范围**：缓存引用从 prompt 开头到 `cache_control` 断点之间的所有内容
- **最低 token 数**：Sonnet 4.6 / Opus 4.8 需要 ≥1024 token；旧版 Opus 4.7/4.5、Haiku 4.5 需要 ≥4096 token
- **最多 4 个断点**：单次请求最多打 4 个 cache 标记
- **窗口**：API 会向前扫描断点前的最多 20 个 content block 来找合适的缓存点

**计费模型**：

| 缓存时长 | 写入价格 | 读取价格 | 有效折扣 |
|---------|---------|---------|---------|
| 5 分钟 | 1.25× 标准输入 | 0.10× 标准输入 | 命中后 90% 折扣 |
| 1 小时 | 2.0× 标准输入 | 0.10× 标准输入 | 命中后 90% 折扣 |

每次缓存命中都会**重置 TTL**——只要 5 分钟内有人复用，缓存就一直活着。1 小时版本适合低频率但大文档的场景（比如每天固定查询一个 500 页 PDF）。

### 2.2 OpenAI GPT：零配置自动生效

OpenAI 的做法完全不同：**不需要加任何标记，也不需要代码改动**。只要你的请求 prompt 超过 1024 token，并且前缀与之前请求共享，就会自动触发缓存。

**计费按代际分化**：

| 模型 | 缓存输入价格 | 相对标准折扣 |
|------|------------|------------|
| GPT-4o / GPT-4.1 | 0.50× 标准输入 | 50% 折扣 |
| GPT-5.4 / GPT-5.5 | 0.50/M vs 5/M 标准 | 90% 折扣 |
| gpt-realtime-2.1 | $0.40/M vs $32/M 标准 | 98.75% 折扣 |

**2026 年 7 月的重大变化**：GPT-5.6 开始引入显式缓存模式和 1.25× 写入费，与 Anthropic 靠拢。自动模式下仍保留，但显式模式通过 `prompt_cache_breakpoint` 标记 + `prompt_cache_options.mode = "explicit"` 实现，最低 TTL 30 分钟。

**注意点**：OpenAI 的缓存 token 仍然**计入 TPM（tokens per minute）配额**——缓存命中虽然便宜，但速率限制照样算。

### 2.3 Google Gemini：隐式 + 显式双模式

Gemini 提供了两种缓存机制，且**支持多模态内容**（文本、PDF、图片、音视频）：

**隐式缓存（Implicit）**：
- 默认开启，零代码改动
- Gemini 2.5 Flash 最低 2048 token；Gemini 2.5 Pro 最低 2048 token
- 命中即享受折扣，通过 `usage.total_cached_tokens` 查看
- 没有额外存储费用

**显式缓存（Explicit）**：
- 需要主动创建缓存对象（`CachedContent`）并在后续请求中引用
- 最低 **32768 token**——门槛最高
- **存储费用**：$1 / M token / hour
- 支持 TTL 管理、可手动删除

**关键差异**：Gemini 是**唯一支持缓存音视频/多模态内容**的厂商。如果你在做长视频分析、大型 PDF 多轮问答，Gemini 的显式缓存是唯一选择。

## 三、成本对比实战：1M token 场景账单

以一个常见场景建模：标准输入 $3/M、100 万 token 的共享上下文、一天内被复用 10 次。

![1M token 缓存成本对比](/images/prompt-caching-cost-comparison.png)

**不缓存的基线**：11 次请求 × 1M × $3/M = **$33/天**

**各方案对比**：

- **Claude 5 分钟**：写 $3.75 + 10×读 $0.30 = **$6.75/天**（节省 79%）
- **Claude 1 小时**：写 $6.00 + 10×读 $0.30 = **$9.00/天**（节省 73%）
- **OpenAI GPT-5.x**：写 $3.00 + 10×读 $0.30 = **$6.00/天**（节省 82%）
- **OpenAI GPT-4.1**：写 $3.00 + 10×读 $1.50 = **$18.00/天**（节省 45%）
- **Gemini 2.5+（隐式）**：10×读 $0.30（无写费） = **$3.00/天**（节省 91%）

Gemini 隐式缓存"零写费"的架构优势在高频复用场景下极为突出。但实际选择要综合看模型能力、输出质量、生态等因素。

## 四、Prompt 结构设计：让缓存真正生效

无论哪一家，**缓存 key 通常基于 prompt 前缀的 hash**。所以 prompt 结构直接决定缓存命中率：

**错误示范**（前缀不固定，缓存失效）：

```python
prompt = f"""
今天日期：{date.today()}
用户问题：{question}
参考资料：{reference_doc}  # 大段内容在后面
"""
```

**正确示范**（静态内容前置，动态内容后置）：

```python
# Anthropic 方式：明确断点
prompt = [
    {"type": "text", "text": SYSTEM_PROMPT},
    {"type": "text", "text": TOOL_DEFINITIONS,
     "cache_control": {"type": "ephemeral", "ttl": "5m"}},
    {"type": "text", "text": RAG_CONTEXT,
     "cache_control": {"type": "ephemeral", "ttl": "1h"}},
    {"type": "text", "text": f"用户问题：{question}"}  # 动态尾部
]
```

```python
# OpenAI 方式：只需保证前缀稳定 + >1024 token
prompt = (SYSTEM_PROMPT + TOOL_DEFINITIONS + RAG_CONTEXT +
          f"\n用户问题：{question}")
```

**三个实战技巧**：

1. **日期 / 版本号 / 随机 seed 永远不要放在前缀里**——即使一个字符不同，缓存就断了
2. **工具定义放 system prompt 中**——所有请求共享，命中率最高
3. **RAG 上下文分块标记**——把高频段落（如知识库总纲）用独立 cache_control 包住

## 五、缓存监控：如何确认真的省到钱？

三家 API 都在 `usage` 字段中暴露缓存统计：

| 厂商 | 字段名 |
|------|-------|
| Anthropic | `cache_creation_input_tokens`、`cache_read_input_tokens` |
| OpenAI | `cached_tokens`（在 `usage` 中） |
| Gemini | `usage.total_cached_tokens` |

**估算缓存命中率**：`cache_read_tokens / (cache_read_tokens + cache_creation_tokens)`

命中率突然下降时，通常意味着：工具集改了、system prompt 版本号变了、或者前缀结构被重构。

## 六、选型决策指南

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 长 system prompt + 稳定工具集 | Claude 5min | 1.25× 写费极低，写一次读十次回本 |
| 高频短会话（每分钟多次） | Claude 5min 或 OpenAI 自动 | 5 分钟窗口自然覆盖 |
| 每天复用同一份大文档（<1 次/小时） | Claude 1h | 2× 写费 vs 10× 读节省 |
| 多用户共享同一 prompt 模板 | OpenAI 自动 | 零门槛，部署即可省钱 |
| 需要缓存 PDF / 视频 / 音频 | Gemini 显式 | 唯一支持多模态缓存 |
| 需要显式 TTL 控制 + 可删除 | Gemini 显式 | 最细粒度的缓存生命周期管理 |
| 已有 OpenAI 生态，不想改代码 | OpenAI 自动 | 直接生效 |

## 七、总结

Prompt Caching 已经不是"要不要用"的问题，而是"如何用对"的问题。三家厂商在 2026 年都达到了 90% 左右的读取折扣，差异主要在：

- **操作门槛**：OpenAI < Gemini 隐式 < Gemini 显式 < Claude
- **多模态支持**：Gemini > OpenAI ≈ Claude
- **生命周期可控性**：Gemini 显式 > Claude > OpenAI
- **写入成本**：OpenAI/Gemini 隐式 < Claude 5min < Claude 1h

对大多数团队来说，**第一步永远是确认 prompt 前缀是否稳定**。把动态变量挪到尾部，静态系统提示和工具定义固定在前，这一步做完通常就能白拿 30-50% 的折扣。之后再根据场景精细化到 TTL、断点、多模态缓存的层面。

---

*本文基于 2026-08 各家 API 文档及行业分析综合整理，价格为参考值，实际以各厂商官网最新公布为准。*

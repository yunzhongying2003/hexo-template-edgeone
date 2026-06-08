---
title: Hermes Agent 上下文压缩插件开发全记录
date: 2026-06-08 23:00:00
tags: [Hermes, context-compression, plugin, devlog, token-savings]
categories: 技术实践
---

![上下文压缩插件架构概览](/images/context-compressor-arch.png)

> 从零到一开发一款 Hermes Agent 插件，实现自动化的 context 压缩 + CCR 可逆存储。

## 一、背景：为什么需要上下文压缩

在使用 Hermes Agent 的过程中，一个反复出现的问题是——**工具返回的大 JSON 烧了太多 token**。

典型的场景：

- `web_search` 返回 50-100 条结果 → 几千甚至上万字符
- `search_files` 一次 grep 匹配上百条 → 大量重复文本
- `skills_list` 返回所有 skill 详情 → 信息密度极低

按 1 token ≈ 4 chars 估算，一次大输出就能吃掉 1500-3000 tokens。对话几轮下来，上下文窗口里充斥着冗余数据，钱花了、信息没多。

### V1：手动压缩

最初的方案是写一个 `compress_output.py` 脚本 + shell alias `co`，每次看到大输出就手动：

```
echo '{大JSON}' | python3 compress_output.py
```

效果不错，但**太依赖主动性**——经常忘了压缩，或者到下一轮 dialog 才意识到。

### V2 构想：Headroom Proxy

接下来调研了 [Headroom](https://github.com/michaelnyu/headroom)（一个输入压缩中间件）。Headroom 能做成透明 HTTP 代理，架在 API 调用路径上自动压缩，还带 KV Cache 对齐（Conformer）。

想法很美好，但引入一个新 HTTP 层意味着：
- 多一层网络依赖
- 和高可用 gateway 串联 debug 复杂度高
- 模型 provider 路径多一层代理

最终决定：**不用 Headroom，直接在 Hermes Agent 的插件机制上实现**。

## 二、架构设计

Hermes Agent 支持用 `transform_tool_result` hook 拦截工具输出，在结果进入 LLM 之前做处理。这是天然的压缩切入面。

### 整体结构

```
工具返回大 JSON
    ↓
transform_tool_result hook 触发
    ↓
context-compressor 插件拦截
    ├── 不符合条件? → 原样透传 (fail-open)
    └── 符合条件? → 调用 compress_output.py
                        ├── 保存原始到 CCR (~/.hermes/ccr/)
                        └── 返回压缩结果
    ↓
LLM 收到精简版 + CCR 可逆标记
```

### 三层防御

1. **`_should_compress()`**：判断是否值得压缩
   - 跳过指定工具（vision、browser_vision、TTS 等）
   - 输入 < 1500 chars → 不压缩
   - 不是 JSON 大数组（<= 20 条）→ 不压缩
2. **`_has_already_compressed()`**：检查是否已被压缩过，避免重复压缩
3. **`_compress_result()`**：实际压缩 + 5% 最低收益门槛
   - 子进程调用 `compress_output.py`
   - 30 秒超时保护
   - 压缩后节省 < 5% → 放弃，原样透传

### Fail-Open 原则

**这是设计上最重要的决策**：插件任何环节出问题都不会影响 Hermes 运行。

| 异常场景 | 行为 |
|----------|------|
| Python 运行时异常 | 写一行 debug log → 原数据透传 |
| subprocess 超时 (30s) | 原数据透传 |
| 压缩脚本不存在 | 原数据透传 |
| 非 JSON 输入 | 原数据透传 |
| 数据太小 | 原数据透传 |
| 已被压缩过 | 跳过，不重复压缩 |

## 三、CCR 可逆压缩机制

CCR（Content Compression with Retrieval）是本方案的关键创新：

- **压缩前**，`compress_output.py` 自动将原始数据保存到 `~/.hermes/ccr/<uuid>.json`
- **压缩后**，LLM 收到的结果末尾追加 `_ccr_note` 字段：`@retrieve <uuid>`
- **需要还原时**，LLM 说 `@retrieve <uuid>` 即可取回完整数据
- **自动清理**：超过 7 天的 CCR 缓存自动清除

这个机制解决了压缩的最大痛点——**信息无损**。LLM 可以安全地丢弃冗余数据，但需要时能随时恢复。

## 四、压缩算法

`compress_output.py` 的压缩策略是多重准则的组合：

1. **错误优先** — 包含 error/exception/failed/critical/fatal 等关键字的条目 **100% 保留**
2. **异常值检测** — 数值字段超过 2σ 的条目保留（IQR 方法）
3. **头部代表性** — 前 30% 的条目保留（展示数据 schema）
4. **尾部时效性** — 后 15% 的条目保留（展示最新/最近结果）
5. **多样性择优** — 剩余预算按字段长度、信息量排序择优

默认压缩上限 20 条，既能保留足够信息，又能大幅减负。

## 五、实际效果

插件启用后的对话中，触发了 **2 次压缩尝试**，真实数据如下：

| 工具 | 原始 | 压缩后 | 节省 | 压缩率 | 结果 |
|------|------|--------|------|--------|------|
| `search_files` (29条) | 5,038 chars (~1,259 tokens) | 4,504 chars (~1,126 tokens) | **534 chars (~133 tokens)** | **11%** | ✅ 成功 |
| `skills_list` (22个skill) | 3,961 chars (~990 tokens) | — | <5% | — | ⚠️ 原样透传 |

**净节省：~133 tokens（1 次有效压缩）**

### 为什么看起来少？

- **插件启用时间短**：当天才装上，只跑了几轮对话
- **对话类型决定**：日常聊天中大部分工具输出小于阈值
- **阈值设计偏保守**：1500 chars + >20 数组 + >5% 压缩率三者同满足才生效

**但真实场景的收益远不止这些**：

| 场景 | 预期节省 |
|------|----------|
| 大量 web_search（50-100条） | 60-80% |
| 大文件 grep 结果 | 50-70% |
| cron 任务批量输出 | 40-60% |
| 多 agent 编排中间结果 | 30-50% |

日常对话只是开胃菜，真正的价值在数据密集型场景。

## 六、安装与配置

> ⚠️ **注意**：此插件为自定义开发，未发布到任何插件仓库。以下安装方法供参考，实际部署需手动创建文件。

```bash
# 1. 创建插件目录结构
mkdir -p ~/.hermes/plugins/context-compressor/

# 2. 写入插件文件（__init__.py、plugin.yaml）
# 见 https://github.com/yunzhongying2003/hermes-webui 或 Wiki 知识库获取文件内容

# 3. 启用插件
hermes plugins enable context-compressor

# 4. 创建压缩脚本
mkdir -p ~/.hermes/scripts/
# 把 compress_output.py、ccr-retrieve.py 放到 ~/.hermes/scripts/

# 5. 创建 CCR 缓存目录
mkdir -p ~/.hermes/ccr/

# 6. 重启网关
hermes gateway restart
```

## 七、未来方向

- **调试模式**：在插件日志中加入压缩前/后 Token 计数，便于评估 ROI
- **自适应阈值**：根据近期对话 Token 消耗自动调整压缩门槛
- **插件配置化**：支持通过 plugin.yaml 配置压缩阈值、保留条数等参数
- **多模型适配**：针对不同模型（DeepSeek、Claude、GPT）做差异化的压缩策略

## 八、总结

- 从 V1 手动压缩 → V2 Headroom 调研 → 最终插件方案，**走了三条路才找到最优解**
- 核心设计原则：**fail-open** 确保零风险；**CCR 可逆** 确保信息无损
- 插件基于 Hermes 的 `transform_tool_result` hook，零侵入、热插拔
- 日常收益不大，**数据密集型场景才是真正战场**
- 纯 Python 标准库实现，零外部依赖
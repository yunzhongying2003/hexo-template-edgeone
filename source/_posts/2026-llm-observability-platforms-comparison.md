---
title: LLM 可观测性平台全面对比：2026 年该选哪一个？
date: 2026-07-31 11:00:00
tags: [LLM, AI工程, 可观测性, 工具对比, DevOps]
categories: AI 工具对比评测
---

随着 LLM Agent 从实验走向生产，"我的 Agent 到底干了什么、哪一步出错、Token 花了多少"这三个问题，正在成为团队每天都在问的刚需。LLM 可观测性（Observability）平台就是为回答这些问题而生。

2026 年的 LLM 可观测性赛道已经高度成熟。本文对比四款主流平台：**Langfuse**、**LangSmith**、**Arize Phoenix**、**W&B Weave**，从架构、功能、定价、适用场景四个维度给出选购建议。

![LLM 可观测性平台全面对比 2026](/images/llm-observability-platforms-overview-2026.png)

## 四款平台速览

### 1. Langfuse — 开源可观测性第一选择

**GitHub**: [langfuse/langfuse](https://github.com/langfuse/langfuse) | ⭐ 32.2k | **MIT 许可证**
**社区**: 5,000+ Discord 成员，周更发布

Langfuse 是 2026 年社区最活跃的 LLM 可观测性平台。核心亮点：

- **真正开源**：完整功能 MIT 许可证，自托管免费，所有功能可用
- **自托管零成本**：Docker Compose、Kubernetes Helm、AWS/GCP/Azure Terraform 模板全支持，数据存储于 ClickHouse + Postgres + Redis
- **框架无关**：通过 OpenTelemetry 接入任意 LLM SDK（OpenAI、Anthropic、LangChain、LiteLLM 等）
- **Prompt 管理**：版本化 Prompt 模板，支持回滚和 A/B 测试
- **数据集与实验**：离线评估 Prompt/模型变更，支持 CI（GitHub Actions）集成
- **被 ClickHouse 收购**：2026 年 1 月 ClickHouse 收购 Langfuse，团队并入、资源增强，但开源承诺和自托管路径不变

Python SDK（v4，2026 年 3 月发布，重大重写）：
```bash
pip install langfuse
```

JS/TS SDK（v5，2026 年 3 月发布）也已重写。其他语言通过 OpenTelemetry endpoint 接入。

**定价（云版，2026 年 7 月）**：
- Hobby：免费，50k units/月，30 天保留，2 用户
- Core：$29/月，100k units，90 天保留，**不限用户**
- Pro：$199/月，无限数据
- Enterprise：$2,499/月起，自定义

**关键成本优势**：按 "units（数据深度）" 计费而非按 trace 数量。超出后每 100k units $8，100 万 events/月约 **$101/月**（Core 套餐）。

### 2. LangSmith — LangChain 原生生态

**官网**: [smith.langchain.com](https://smith.langchain.com) | **闭源**
**GitHub**: LangSmith 本身不开源

LangSmith 由 LangChain 团队开发，是 LangChain 生态的原生可观测性方案。核心亮点：

- **LangChain/LangGraph 深度集成**：零配置自动 tracing，`langchain.tracer` 一行接入
- **LangGraph Studio**：专门为 LangGraph Agent 设计的调试 IDE，可视化 agent 执行步骤
- **Prompt Hub**：集中管理、版本化、测试 Prompt
- **标注队列（Annotation Queues）**：团队协作标注，构建人工反馈数据
- **Playground**：直接测试模型和 Prompt 组合

**三种部署模式**：
1. **Cloud**：LangChain 托管（GCP us-central-1 或 EU 区域）
2. **Hybrid**：SaaS 控制平面 + 自托管数据平面
3. **Self-hosted**：完全自托管，**仅限 Enterprise 合约**（无开源选项）

**定价（2026 年 7 月）**：
- Developer：免费，5k base traces/月，14 天保留，1 用户
- Plus：$39/座/月，10k base traces/月，14 天保留（可升级至 400 天，$5/千 traces）
- Enterprise：定制报价

**成本陷阱**：按 seat + 按 trace 双重计费。base traces $2.50/千（14 天），extended traces（400 天）$5.00/千。100 万 traces/月约 **$2,514/月**（Plus 套餐）。seat 费用在大团队中叠加显著。

### 3. Arize Phoenix — OpenTelemetry 原生 + 深度评估

**GitHub**: [arize-ai/phoenix](https://github.com/arize-ai/phoenix) | ⭐ 10.8k | **ELv2 许可证（Source-Available）**

Phoenix 由 Arize（ML 监控老牌）孵化，是目前 OpenTelemetry 原生程度最高的 LLM 可观测性方案。核心亮点：

- **Docker 本地运行**：`pip install arize-phoenix && phoenix launch-server`，零外部依赖，Jupyter notebook 友好
- **OpenTelemetry + OpenInference 标准**：遵循社区标准，不被任何厂商锁定
- **深度评估（Eval）**：内置 drift 检测、评分、回归测试，评估能力在竞品中最深
- **Agent 工作流可视化**：原生支持 LlamaIndex、OpenAI Agents SDK 的 trace 回放
- **企业版 Arize AX**：分布式、企业级生产可观测性（商业定价）

**部署模式**：
- Phoenix OSS：Docker 本地运行，免费
- Phoenix Cloud：2 个免费实例，无需基础设施
- Arize AX：企业版，定制定价

**适用场景**：已在使用 Arize 做 ML 监控的团队，或需要最严苛评估标准的受监管行业（金融、医疗）。

### 4. W&B Weave — ML 团队的统一方案

**GitHub**: [wandb/weave](https://github.com/wandb/weave) | ⭐ 1.1k | **Apache-2.0**
**官网**: [docs.wandb.ai/weave](https://docs.wandb.ai/weave)

W&B Weave 由 Weights & Biases 推出，定位为 ML 实验跟踪平台的 LLM 扩展。核心亮点：

- **极简接入**：`weave.op` 装饰器一行接入，Python + JS/TS 双语言
- **与 W&B 实验追踪联动**：LLM 开发与 ML 实验在同一个平台，适合多模型团队
- **LLM Judge & 评估管道**：内置评估框架，支持数据集管理
- **Trace 可视化**：在 W&B 项目中查看 LLM inputs/outputs/code

**典型接入代码**：
```python
import weave
weave.init("my-project")

@weave.op
def my_llm_call(prompt: str) -> str:
    # 自动记录 inputs/outputs/code
    return openai_client.chat(prompt)
```

**适用场景**：已经在用 W&B 做实验跟踪的团队，希望 LLM 与 ML 实验统一平台。对于纯 LLM 团队，Weave 的功能深度不如前三者。

## 价格成本对比

![100 万请求/月 月度成本对比](/images/llm-observability-pricing-comparison-2026.png)

**同等规模下，开源/自托管方案成本优势极为显著**。100 万 events/月：

| 平台 | 模式 | 月成本 |
|------|------|--------|
| LangSmith Plus | 闭源云 | ~$2,514 |
| W&B Weave | 按用量 | ~$150 |
| Langfuse Core | 云 | ~$101 |
| Arize Phoenix | 自托管 | ~$25（仅基础设施） |
| Langfuse | 自托管 | ~$30（仅基础设施） |

**成本差异根因**：
1. LangSmith 的 seat 收费（$39/人）是主要成本来源，团队扩张时叠加显著
2. Langfuse 按 units（数据深度）计费，不限用户，Core 套餐 $29 起
3. 自托管方案只需承担 ClickHouse 基础设施成本（ClickHouse Cloud 约 $66/月起）

## 架构与标准对比

| 维度 | Langfuse | LangSmith | Arize Phoenix | W&B Weave |
|------|----------|-----------|---------------|-----------|
| **开源** | MIT（全功能） | 闭源 | ELv2（Source-Available） | Apache-2.0（SDK 开源） |
| **自托管** | 免费（全套） | Enterprise 仅 | 免费（Docker） | 无 |
| **OTel 支持** | ✅ 原生 | ⚠️ 有限 | ✅ 原生 + OpenInference | ✅ |
| **框架依赖** | 无 | LangChain 绑定 | 无（LlamaIndex 集成好） | 无 |
| **核心存储** | ClickHouse | 闭源 | 闭源 | W&B 云 |
| **SDK 语言** | Python, JS/TS | Python | Python, JS/TS | Python, JS/TS |
| **评估深度** | LLM-as-judge | Prompt-based | 最深（drift/回归） | LLM Judge |
| **Prompt 管理** | ✅ 版本化 | ✅ Prompt Hub | ❌ 有限 | ❌ |
| **Agent 专用** | 通用 | ✅ LangGraph Studio | ✅ 工作流回放 | 通用 |

## 选型决策树

![LLM 可观测性平台选型决策树](/images/llm-observability-decision-tree-2026.png)

实际选型时，可以按以下路径判断：

1. **你的 Agent 跑在 LangChain/LangGraph 上吗？** → 是，直接选 **LangSmith**，零摩擦集成
2. **你需要开源自托管（数据主权/成本）吗？** → 是，选 **Langfuse**（MIT，全功能免费自托管）
3. **你的团队强调 OpenTelemetry 标准和深度评估吗？** → 是，选 **Arize Phoenix**（OpenInference 原生）
4. **团队已经在用 W&B 做 ML 实验吗？** → 是，选 **W&B Weave**，平台统一收益最大

## 实际使用中的三个坑

### 1. LangSmith 的 trace 成本曲线

LangSmith 免费 5k traces 看起来很友好，但到了生产规模就急剧上升。base traces 只有 14 天保留，要 400 天需要升级到 extended traces（$5/千）。**注意**：包含用户反馈的 trace 会自动升级为 extended，费用翻倍。

### 2. Langfuse Python SDK v4 迁移

2026 年 3 月 Langfuse Python SDK 重写为 v4（基于 OpenTelemetry），从 v2/v3 迁移需要阅读迁移指南。部分用户反馈第三方自动 instrumentation 的回归问题。

### 3. Phoenix 的 ELv2 许可证

Phoenix 使用 Elastic License 2.0（非 OSI 批准的标准开源）。可以免费自托管，但不能作为托管服务提供。如果你计划把可观测性作为内部平台对外提供，需注意许可证限制。

## 总结

2026 年的 LLM 可观测性市场呈现清晰的分工：

- **LangSmith**：LangChain 生态首选，集成最深但最贵
- **Langfuse**：开源 + 自托管首选，性价比最高，社区最活跃
- **Arize Phoenix**：OTel 原生 + 深度评估，适合严谨团队
- **W&B Weave**：ML 团队统一方案，适合已有 W&B 基础设施的团队

对于大多数团队，**Langfuse** 是最稳妥的起点——MIT 开源、云免费 50k units、自托管零费用，且 ClickHouse 收购后长期稳定性有保障。如果深度绑定 LangChain，则 LangSmith 的生态价值不可替代。

---

> 数据来源：各平台官网及 GitHub（2026 年 7 月）
>
> - [Langfuse GitHub](https://github.com/langfuse/langfuse) · [Langfuse 官网](https://langfuse.com)
> - [LangSmith](https://smith.langchain.com)
> - [Arize Phoenix GitHub](https://github.com/arize-ai/phoenix) · [Arize 官网](https://arize.com/phoenix)
> - [W&B Weave GitHub](https://github.com/wandb/weave) · [W&B Docs](https://docs.wandb.ai/weave)

---
title: AI Agent 浏览器自动化工具全景对比 2026：Browser Use vs Stagehand vs Playwright MCP vs agent-browser vs Skyvern
date: 2026-10-09 11:05:00
summary: "2026 landscape comparison of five AI browser automation tools — Browser Use, Stagehand, Playwright MCP, agent-browser, Skyvern — with GitHub stars, architectures, use cases, pricing, and decision matrix."
tags: [browser-use, stagehand, playwright-mcp, agent-browser, skyvern, ai-agent, browser-automation, mcp, 2026-comparison]
categories: AI 工具对比评测
---

![AI Agent 浏览器自动化生态图谱](/images/browser-automation-landscape-2026.png)

---

## TL;DR

- **What this is**: A 2026 head-to-head comparison of the five most-adopted AI browser automation tools (Browser Use, Stagehand, Playwright MCP, agent-browser, Skyvern), covering architecture, GitHub traction, licensing, pricing, and production fit.
- **This is for**: Engineers and technical leads building AI agents that need to interact with web UIs, decide whether to build their own agent loop or plug into an existing MCP server, and pick the right tool for the right job.
- **We chose**: Rather than crown a "winner", we classify each tool by *what it owns* on the autonomy-to-determinism spectrum and give a concrete decision matrix so you can pick based on your actual task.

---

## 为什么这个话题在 2026 年突然变得重要

过去一年 AI agent 的能力边界从"聊天 → 写代码 → 操作电脑"扩展到"操作浏览器"。2026 年是这一年发生爆炸性变化的一年：

- **Browser Use** 从 2024 年 3 月上线时的 5k stars，飙到 2026 年 10 月的 **117.3k stars**，成为 GitHub 上"AI 浏览器 agent"这个赛道的绝对头部（数据：[github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)）。
- **Firecrawl** 也突破 130k+ stars，与 Browser Use 一起进入 GitHub Top 100 仓库（[Firecrawl Blog, 2026](https://www.firecrawl.dev/blog/best-browser-agents)）。
- **Vercel Labs 的 agent-browser** 用 Rust CLI 架构，用 8 个月冲到 43.5k stars，把"给 agent 提供浏览器"这个工作简化成命令行调用（[github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)）。
- **市场端**：AI 浏览器市场规模预计从 2024 年的 45 亿美元增长到 2034 年的 **768 亿美元**（CAGR 32.8%），79% 的公司已经采用某种形式的 AI agent 技术。

问题也随规模浮现：不同团队对"浏览器自动化"的定义差异巨大。是自主 agent 自己决定每一步？还是工程师写脚本、只在几个模糊步骤调用 AI？还是给已有 agent 一个浏览器工具？**这些不是"哪个更好"，是"哪个更合适"。**

---

## 一图看清五个工具

![AI Agent 浏览器自动化生态图谱](/images/browser-automation-landscape-2026.png)

（配图说明：横向色卡展示 5 个工具的核心定位，纵向三层展示 Agent 框架 / SDK/CLI / 基础设施的分层关系。所有数据来自 GitHub 官方仓库页面，2026-10 抓取。）

---

## 五个工具的详细拆解

### 1. Browser Use — 全自主 Agent 框架

**GitHub**: [github.com/browser-use/browser-use](https://github.com/browser-use/browser-use)  
**⭐ Stars**: 117.3k（GitHub 上 AI 浏览器赛道最高）  
**语言**: Python | **授权**: MIT | **月下载**: 8.1M（[browser-use.com](https://browser-use.com)）

Browser Use 是这个赛道的定义者。它把"给 LLM 一个浏览器"包装成一个完整的 agent 循环：你给它一个自然语言任务，它自己规划、自己导航、自己观察、自己点击。

**核心 API**：
```python
from browser_use import Agent, Browser, ChatOpenAI

llm = ChatOpenAI(model='gpt-5.6-luna')
agent = Agent(
    task="Find the number of stars of the browser-use repo",
    llm=llm,
    browser=Browser(use_cloud=True),  # 可选：使用托管云浏览器
)
history = await agent.run()
```

**架构层次**：`LLM Agent → Browser-Use → Playwright → Chromium`

**优势**：
- 完全端到端，不需要你写 Playwright 脚本
- 内置视觉理解（配合 vision LLM）
- UI 变化时可自愈（selector 变化不会立刻崩）
- 支持 LangChain 生态、OpenAI、Anthropic、Gemini 等多个 LLM 后端
- 提供 managed cloud browser，无需自己运维浏览器集群

**代价**：
- 每次决策都消耗 LLM token，延迟和成本不可预测
- 每一步都可能走出不同的路径，行为不稳定
- 官方 API 迭代快，模型对象和 LangChain 模型对象不通用

**商业化**：$0 Pay-As-You-Go 起步；Starter 计划 $100/月（$83/月年付），Business $500/月（$400/月年付），浏览器时间 $0.03-0.06/小时，代理流量 $4-10/GB。

**适合**：Python 团队、希望快速搭建自主浏览 agent 的原型、非浏览器领域的团队第一次做 agent。

---

### 2. Stagehand — 代码持有的 SDK，AI 是可选工具

**GitHub**: [github.com/browserbase/stagehand](https://github.com/browserbase/stagehand)  
**⭐ Stars**: 25.4k | **语言**: TypeScript / Python / Go（一等公民）  
**授权**: MIT | **背景**: Browserbase 官方产品

Stagehand 是**代码所有权**流派。它的哲学很清晰：你的应用持有控制流，AI 是几个可控的原语。

**三大原语**（[Stagehand v4 文档](https://docs.stagehand.dev/v4/first-steps/introduction)）：
```typescript
// Act: 用自然语言执行动作
await stagehand.act("click the login button");

// Extract: 用 Zod schema 提取结构化数据
const { data } = await stagehand.extract(
    "extract the price",
    z.object({ price: z.number() })
);

// Observe: 发现页面上可操作的动作
const observations = await stagehand.observe("Find the first link");
```

**⚠️ 关键变化：v4 移除了内置 `agent()`**

Stagehand v3 有一个 `agent()` 内置循环，让模型规划整段浏览流程。**v4 官方迁移指南明确移除了这个循环**（[migration guide](https://github.com/browserbase/stagehand/blob/main/packages/docs/v4/migrations/v3.mdx)）：应用脚本或外部模型/工具循环持有控制权，`act`、`extract`、`observe` 保留。

v3 到 v4 的性能数据（Stagehand 官方发布）：
- **速度提升 44%**（相比 v2，a11y-tree 替代 DOM）
- **Token 消耗显著降低**（首次执行后缓存）
- **Universal CDP**：可运行在任意浏览器（不局限于 Playwright）
- **OTel traces**：一等公民的 observability

**优势**：
- 完全掌控工作流，AI 只是"帮忙理解页面"的工具
- 类型安全的 extraction（Zod schema 验证）
- 三种语言一等支持
- 与 Browserbase 托管运行时天然集成
- 抽象层比裸 Playwright 少 60-70% 样板代码（[Digital Applied, 2026](https://www.digitalapplied.com/blog/browser-automation-ai-agents-playwright-stagehand-2026)）

**代价**：
- v4 移除 `agent()` 后，需要自己写循环或接入外部 MCP 客户端
- 不提供业务层面的编排和审批系统
- 当前浏览器引擎以 Chromium 为主

**适合**：TypeScript/JavaScript 团队、有 Playwright 基础设施、想"AI 在需要的地方介入"而不是"把整个流程交给 LLM"的产品和平台团队。

---

### 3. Playwright MCP — 给已有 Agent 装浏览器工具

**GitHub**: [github.com/microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)  
**⭐ Stars**: 37.8k | **背景**: Microsoft 官方  
**授权**: Apache-2.0

Playwright MCP 不是 agent，是 **MCP Server**（Model Context Protocol）。它暴露 Playwright 的浏览器操作能力给任何 MCP 客户端。

**架构**：
```
[你的 MCP Client / LLM Agent]  ← MCP protocol →  [Playwright MCP Server]  →  [Chromium]
```

**核心特点**：
- 用 **accessibility snapshot** 作为页面表示，结构化返回可交互元素
- 核心工作流不要求 vision 模型（截图可选）
- Client 端决定调用哪些工具、什么时机完成任务
- 支持 stdio 和远程（WebSocket）两种 transport
- 持久化 profile 和 storage-state 支持认证

**典型 MCP 配置**：
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Docker 部署**（官方推荐）：
```bash
docker run -d -i --rm --init --pull=always \
  --entrypoint node --name playwright \
  -p 8931:8931 mcr.microsoft.com/playwright/mcp \
  /app/cli.js --headless --browser chromium \
  --no-sandbox --port 8931 --host 0.0.0.0
```

**优势**：
- 客户端无关，任何 MCP client（Claude、Cursor、Copilot、Cline、Continue）都能接
- 微软维护，标准实现，生态背书最强
- 测试自动化级别的可靠性
- Apache-2.0，商用无风险

**代价**：
- 它只提供工具，不提供业务 agent
- 复杂任务需要 client 端自己编排
- 需要客户端支持 MCP 协议

**适合**：已经有 MCP client（Claude Code、Cursor 等）的团队，不想引入新 SDK、只想"让现有 agent 能用浏览器"。

---

### 4. agent-browser — Rust CLI，93% Token 节省

**GitHub**: [github.com/vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)  
**⭐ Stars**: 43.5k | **背景**: Vercel Labs  
**授权**: Apache-2.0

Vercel Labs 的 agent-browser 是一个 **CLI 工具**，为 AI agent 优化到极致：

**三层架构**：
1. **Rust CLI** — 命令解析，高性能，跨平台
2. **Rust Daemon** — 直连 CDP，无需 Node.js
3. **Fallback** — Node.js 执行（原生二进制不可用时）

**核心工作流**（三步曲）：
```bash
agent-browser open https://example.com    # 1. 导航
agent-browser snapshot -i                  # 2. 快照（返回 @e1, @e2 元素引用）
agent-browser click @e1                    # 3. 按引用交互
agent-browser fill @e2 "test@example.com"
agent-browser screenshot
```

**93% Token 节省**（[Apiyi, 2026](https://help.apiyi.com/en/agent-browser-ai-browser-automation-cli-guide-en.html)）：
- 使用 accessibility tree snapshot + 元素引用（`@e1`、`@e2`）
- 相比 Playwright MCP 的完整 DOM 传递，token 消耗减少 93%
- 直接省成本、防上下文溢出

**独特优势**：
- **不需要 MCP**：任何能执行 shell 命令的 agent（Cursor、Claude Code、Codex、Continue、Windsurf）都能直接调用
- 零配置：`npm install` 就能用
- 内置 auth vault、session 持久化、video recording
- 官方 skills 支持 Electron、Slack、exploratory testing
- 可连接 AgentCore 云浏览器或 Browserbase 会话

**代价**：
- 相对较新（2026 年 1 月发布）
- 生态比 Playwright MCP 小
- Skills 主要面向特定场景

**适合**：想要最快上手 CLI 优先 agent 的团队、已经在用 Claude Code/Cursor/Codex 但缺一个浏览器工具的开发者、对 token 成本敏感的场景。

---

### 5. Skyvern — 视觉驱动的 Agentic Process Automation 平台

**GitHub**: [github.com/Skyvern-AI/skyvern](https://github.com/Skyvern-AI/skyvern)  
**⭐ Stars**: 12k+ | **语言**: Python + TypeScript SDK  
**授权**: AGPL-3.0 | **部署**: 云托管 + 自托管 Docker

Skyvern 定位在"**Agentic Process Automation**"——它是浏览器自动化的上层平台，处理的是"发票下载、表单提交、合规门户"这类多步骤业务流程。

**工作机制**：
- 每个 AI 步骤捕获页面，把 DOM 降到可交互元素
- 把视觉布局和元素数据**同时**给 LLM
- LLM 决定下一步动作，Playwright 在 Chromium 执行
- 执行完检查目标是否完成，未完成继续

**产品化特性**：
- **视觉工作流编辑器**：非代码用户也能配置工作流
- **确定性 + AI 混合**：稳定步骤走 Playwright，动态步骤走 AI
- **自托管部署**：AGPL-3.0 源码，支持 Docker/Kubernetes
- **LLM 可替换**：Vertex AI、Azure OpenAI 等，数据不出私网
- **2026 年 6 月新增 Skyvern MCP Server**：Claude/Cursor/Windsurf 可直接调用

**AGPL 授权警告**：AGPL-3.0 是 copyleft 授权，商业化闭源集成前需要法务评估（[Skyvern Blog](https://www.skyvern.com/blog/browser-use-alternatives)）。

**适合**：需要处理"页面经常变、多步骤业务流"的场景（发票、报表下载、合规门户）、有非技术运营人员参与的团队、需要自托管+数据主权的合规场景。

---

## 关键维度对比表

| 维度 | Browser Use | Stagehand | Playwright MCP | agent-browser | Skyvern |
|-----|-------------|-----------|----------------|--------------|---------|
| **GitHub ⭐** | 117.3k | 25.4k | 37.8k | 43.5k | 12k+ |
| **主语言** | Python | TS/Py/Go | TS | Rust | Py/TS |
| **授权** | MIT | MIT | Apache-2 | Apache-2 | AGPL-3.0 |
| **架构角色** | Agent 框架 | 代码 SDK | MCP Server | CLI 工具 | 工作流平台 |
| **AI 循环所有权** | 内置 | 外部（v4） | 客户端持有 | 客户端持有 | 内置 |
| **AI 抽象** | 完整 agent 循环 | act/extract/observe | Playwright 工具 | snapshot + ref | 视觉 + 决策 |
| **页面表示** | a11y + screenshot | a11y-tree | a11y snapshot | a11y + ref | screenshot + DOM |
| **视觉模型必需** | 可选 | 可选 | 可选 | 否 | 是 |
| **多语言 SDK** | Py only | TS/Py/Go | TS only | CLI | Py/TS |
| **自托管** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **托管云** | Browser Use Cloud | Browserbase | Docker | AgentCore/Browserbase | Skyvern Cloud |
| **主要成本** | LLM + 浏览器时间 | LLM + 浏览器 | LLM + 浏览器 | LLM + 浏览器 | LLM + 平台 |
| **适合谁** | Python agent 团队 | TS/Go 平台团队 | 已有 MCP client | CLI 优先 agent | 业务流程团队 |

*数据来源：GitHub 官方仓库页面（2026-10-09 抓取），各项目官方文档。*

---

## 三个关键架构问题

### Q1：AI 循环谁持有？

这是最重要的架构分歧：

- **Browser Use 内置循环**：给它任务，它自己决定步骤。适合"我不知道路径怎么走"的场景。
- **Stagehand v4 外部循环**：v4 移除了内置 agent，需要你自己写循环或用外部 MCP client。这是**故意的**——让工程师更清楚自己控制什么。
- **Playwright MCP / agent-browser 客户端持有**：只提供工具，规划在客户端。
- **Skyvern 内置循环**：类似 Browser Use，但更结构化（有工作流编辑器和验证步骤）。

### Q2：页面表示用什么？

- **Accessibility tree**（a11y snapshot）：结构化，token 效率高，但 canvas-only 页面拿不到信息
- **Screenshot**：视觉证据，vision 模型必需，token 高
- **agent-browser 的 hybrid**：a11y + 元素引用（`@e1`），号称省 93% token

**选择建议**：
- 标准 Web 应用 → a11y 优先（Playwright MCP、Stagehand、agent-browser）
- Canvas-only 图表/游戏 → 需要 screenshot（Browser Use、Skyvern）
- 成本敏感 → agent-browser 的 ref 系统

### Q3：认证和会话怎么管？

所有五个工具都支持会话持久化，但方式不同：

| 工具 | 认证机制 |
|-----|---------|
| Browser Use | `storage_state` / 浏览器 profile |
| Stagehand | Playwright 兼容的 `storageState` |
| Playwright MCP | `--storage-state` flag + persistent profile |
| agent-browser | 内置 auth vault |
| Skyvern | Workflow 级别凭据管理 |

**生产环境建议**：
- 敏感系统：每次任务独立 session，最小权限凭证
- 长任务：明确处理重定向、新标签页、多 tab 关系
- 写操作（提交表单）：**先确认成功再重试**，否则可能重复提交

---

## 实际选择决策矩阵

| 你的场景 | 首选 | 备选 | 说明 |
|---------|-----|-----|------|
| Python 团队快速搭 agent | Browser Use | Skyvern | 端到端最省事 |
| TypeScript/Go 平台工程 | Stagehand | Playwright MCP | 代码所有权清晰 |
| 已有 Claude Code/Cursor | Playwright MCP 或 agent-browser | — | 直接接进现有栈 |
| 成本敏感（大量重复任务） | agent-browser | Stagehand (缓存) | 93% token 节省 + 缓存 |
| 非技术运营团队配置 | Skyvern | — | 视觉工作流编辑器 |
| 数据主权/合规要求 | Skyvern（自托管） | Stagehand（自托管） | AGPL 需法务评估 |
| 已有 Playwright 测试套件 | Stagehand | Playwright MCP | 增量扩展，不重构 |
| 需要浏览器基础设施 | Browserbase（+ Stagehand） | Steel | 只管浏览器，不管逻辑 |
| 需要视觉理解复杂页面 | Skyvern | Browser Use | DOM 不稳定时的兜底 |

---

## 生产部署的常见坑

### 坑 1：把 selector 缓存当作"页面没变"的证据

- Stagehand 支持 action 缓存，但**缓存只证明之前能跑，不证明现在能跑**
- 每次缓存命中后要校验 extraction 是否符合 schema
- 缓存失效后 fallback 到 AI 步骤，成本会突然上升

### 坑 2：写操作重试导致重复提交

- 表单提交超时时，模型可能不知道后端是否已接受
- 盲目重试 = 重复下单、重复支付
- 写操作用应用侧的 idempotency key，浏览器层只做 read

### 坑 3：MCP 客户端版本漂移

- 同一个 Playwright MCP，不同 client（Claude vs Cursor vs Cline）表现可能不同
- Client 决定工具调用顺序、上下文保留、失败处理
- 生产环境要 pin 版本，不能只 pin server

### 坑 4：多标签页和重定向

- 下载、认证跳转、详情页都可能开新标签
- 提取数据前要**明确当前 active page**
- 不要用"multitab supported"作为检查框，要测具体场景

### 坑 5：AGPL 授权陷阱

- Skyvern 是 AGPL-3.0
- 如果你在企业内闭源使用 Skyvern，需要看法务意见
- Stagehand、Playwright MCP、Browser Use、agent-browser 都是宽松授权

---

## 与 Hermes Agent 的集成方式

如果你用 Hermes Agent（也就是本文作者所在的环境），五个工具的接入方式：

| 工具 | Hermes 接入 |
|-----|------------|
| Playwright MCP | 直接作为 MCP server 添加到 Hermes 配置 |
| agent-browser | 作为 CLI toolset，用 terminal 工具调用 |
| Stagehand | 通过 Node.js subprocess 或 npm 集成 |
| Browser Use | Python subprocess，或 Cloud API |
| Skyvern | 通过其 MCP server（2026-06 发布）接入 |

对 Hermes 用户来说，Playwright MCP 和 agent-browser 是最自然的集成——它们是"agent 的工具"，不是"另一个 agent"。

---

## 2026 下半年趋势观察

1. **Agent 框架简化**：Browser Use v2 从"框架"退回"harness"，把控制权交回应用层。行业共识正在向 Stagehand v4 的方向靠拢。
2. **CLI 优先回归**：agent-browser 的爆发说明"agent 只需要 shell 命令"是真实需求。MCP 提供工具，CLI 提供工具，两者不互斥。
3. **基础设施与逻辑分离**：Browserbase 只做浏览器，Stagehand 只做 SDK，agent-browser 只做 CLI。这个"分层解耦"是生产可用的关键。
4. **Token 效率成核心指标**：93% token 节省（agent-browser）、a11y-tree 替代 DOM（Stagehand v3）都是明确的成本优化方向。
5. **视觉模型不再是必需品**：a11y snapshot 已经能覆盖大部分 Web UI，视觉模型只在 canvas-heavy 页面才必需。

---

## 结语：没有万能工具，只有合适的工具

AI 浏览器自动化在 2026 年已经不是"哪个工具最好"的问题。五个头部工具覆盖不同的层、不同的哲学、不同的团队画像。

**最实用的判断流程**：
1. **你的团队是什么语言？** → Python 走 Browser Use / Skyvern，TS 走 Stagehand / Playwright MCP
2. **你想让 AI 做多还是少？** → 多 → Browser Use，少 → Stagehand / Playwright MCP
3. **你的成本敏感吗？** → 敏感 → agent-browser（省 93% token）
4. **你需要非技术参与吗？** → 是 → Skyvern（可视化工作流）
5. **你的数据能出私网吗？** → 不能 → 全部支持自托管，但要注意 Skyvern 的 AGPL

用**同一个任务、同样的输入、同样的验收标准**测试每个候选工具，而不是看 star 数排名。星数是热度指标，不是生产力指标。

---

## ❓ 常见问题（FAQ）

**Q: 为什么 Stagehand v4 移除内置 agent() 是好事？**

移除不是回退，是哲学声明。Stagehand v3 的 agent() 让工程师以为自己在用"SDK"，实际是"agent 框架"。v4 之后每个决策都是显式的——你要用 AI 就在特定步骤调 act()，不要就在代码里写 Playwright 调用。这对生产环境更可预测，也让 token 成本可控。代价是需要你或外部 MCP client 写控制循环。

**Q: Playwright MCP 和 agent-browser 都是 MCP，为什么不用一个？**

Playwright MCP 是标准的 MCP server，需要 MCP 客户端才能用。agent-browser 是 CLI 工具，任何能执行 shell 命令的 agent 都能直接调用，不需要装 MCP。agent-browser 官方数据说比 Playwright MCP 省 93% token（因为用 element refs 而不是完整 snapshot）。选择看你的 client 支不支持 MCP——支持就用 Playwright MCP（微软维护，标准实现），不支持就用 agent-browser。

**Q: Browser Use 是不是过时了？**

不过时，但角色变了。2025 年 Browser Use 是"agent 框架"，2026 年它更偏"harness"（框架外壳）。核心 agent 循环依然在，只是文档和示例开始鼓励你把控制流外置。它仍然是 Python 生态最流行的选择（117k stars 领先第二名 3 倍）。如果你只是"快速搭一个能跑的原型"，它依然是最省事的。

**Q: Skyvern 的 AGPL 授权会阻止企业使用吗？**

不阻止，但需要法务审查。AGPL-3.0 要求任何通过网络提供服务的修改版本必须开源。如果你的团队内部使用 Skyvern 而不修改源码，或者你愿意开源你的集成层，就没问题。很多金融、医疗场景因为数据主权要求反而选择 Skyvern 的自托管部署。相比之下 Browser Use、Stagehand、Playwright MCP、agent-browser 都是宽松授权（MIT/Apache-2）。

**Q: 我应该同时用两个工具吗？**

完全可以。生产环境里很常见的组合：
- **Stagehand + Playwright MCP**：Stagehand 做核心 SDK，Playwright MCP 给已有 agent 工具
- **agent-browser + Browserbase**：CLI 交互 + 托管浏览器基础设施
- **Skyvern + Playwright MCP**：Skyvern 处理业务流，Playwright MCP 让 agent 直接触发

关键原则：**不要启动第二个自主循环只为换个工具**。每一层新增都要有明确的职责边界。

---

## 🔗 相关文章

- [MCP 协议深度指南 2026](/2026/06/30/mcp-protocol-guide-2026/) — Playwright MCP 和 agent-browser 的协议基础
- [AI Agent 框架深度对比 2026](/2026/09/25/2026-ai-agent-frameworks-deep-comparison/) — 上层的 agent 编排，浏览器是它们的一个工具
- [Deep Research 工具对比 2026](/2026/09/04/deep-research-tools-comparison-2026/) — 另一种"AI 使用浏览器"的场景：面向搜索而非操作
- [MCP Servers 精选 2026](/2026/08/28/mcp-servers-essentials-2026/) — MCP 生态全景，Playwright MCP 在其中
- [AI 编码工具深度对比 2026](/2026/07/28/2026-ai-coding-tools-deep-comparison/) — Claude Code/Cursor 等工具如何调用浏览器自动化

---

*数据来源与更新：本文所有 GitHub ⭐ 数据、版本号、定价均来自 2026-10-09 抓取的官方仓库页面和文档。工具生态迭代快速，建议每季度重新评估。*

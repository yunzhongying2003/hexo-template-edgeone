---
title: agentic-stack：一个 .agent/ 文件夹打通 8 种编程 Agent
date: 2026-06-04 22:50:00
tags: [AI-Agent, agentic-stack, memory, cross-platform, open-source]
categories: AI Agent
---

> **原文作者：** Shubham Saboo（Google AI PM）
> **来源：** LinkedIn / X @Saboo_Shubham_

有没有这样的体验：今天用 Claude Code 写了一个项目，记录了一大堆偏好设置，明天切换到 Cursor 或者 Codex，一切从头开始。每次工具变动，你的 Agent 就失忆一次。

现在这个问题被解决了。一个叫做 **agentic-stack** 的开源项目，让 8 种不同的编程 Agent 共享同一套记忆和技能系统。

<!-- more -->

## 一、核心问题

> "Every coding agent has its own memory format. Claude Code remembers one way. OpenClaw another. Hermes another. Switch tools and your agent starts from zero."

每个编程 Agent 都有自己独特的记忆格式：

| Agent | 记忆存储方式 |
|-------|-------------|
| **Claude Code** | `.claude/` 目录 + CLAUDE.md |
| **Cursor** | `.cursor/` + 规则文件 |
| **OpenClaw** | 专有格式 |
| **Hermes Agent** | `~/.hermes/skills/` + MEMORY.md |
| **Codex** | 项目级配置 |

换一个工具 → 所有偏好、教训、约定全部丢失 → 从头开始。

## 二、解决方案：.agent/

> "Just drop `.agent/` into your project, pick your harness, and it wires up automatically. Same brain. Different tool."

**agentic-stack** 的核心是一个名为 `.agent/` 的目录。把它放在你的项目根目录下，然后选择你想要的 Agent 驱动（harness），它就能自动连接。

### 支持 8 种 Harness

- Claude Code
- Cursor
- Windsurf
- OpenCode
- OpenClaw
- **Hermes Agent**
- Pi Coding Agent
- 自建的 Python 循环

### .agent/ 目录里有什么？

```
.agent/
├── MEMORY.md          # 工作记忆 — 当前会话相关信息
├── episodes/          # 情景记忆 — 每次交互的存档
├── semantic/          # 语义记忆 — 向量化的长期知识
├── user/              # 个人化记忆 — 用户偏好和风格
├── skills/            # 渐进式技能 — 按需加载的工作流
├── schemas/           # 类型化的工具定义
└── permissions/       # 权限策略
```

**四个记忆层 + 各自的保留策略**：
- **工作记忆** — 当前任务上下文，临时
- **情景记忆** — 每次操作的日志
- **语义记忆** — 聚类后的长期知识
- **个人化记忆** — 用户行为模型

## 三、复合循环

> "Every action logs to episodic memory. A nightly process clusters recurring patterns into candidate lessons. You review them with one command. Graduated lessons load automatically in future sessions."

流程是：

```
每次操作 → 记录到情景记忆
     ↓
夜间进程 → 聚类重复模式 → 提炼为候选经验
     ↓
你一键审查 → 批准/拒绝
     ↓
通过的经验 → 自动加载到未来会话
     ↓
    ↻
```

> "Your agent's git history becomes its autobiography."

## 四、这在解决什么问题？

### 4.1 供应商锁定（Vendor Lock-in）

使用某一家 Agent 工具时，你的所有配置、经验、记忆都锁在该工具的生态里。agentic-stack 用标准化的 `.agent/` 格式打破了这一点。你选择的是"大脑"，而不是"工具"。

> "You don't pick an agent anymore. You pick a brain and let your agent plug into it."

### 4.2 多 Agent 协作中的信息孤岛

LinkedIn 讨论中 Kane Dixon 的真实处境很有代表性：他用 Claude 做服务端、ChatGPT 做讨论、Antigravity 做前端、OpenClaw 做本地模型任务、Paperclip 做自组织 Agent、Hermes 做自进化 Agent。

> "A veritable slew of silos with no shared knowledge or context."

6 个工具，6 套记忆。agentic-stack 让它们在同一个 `.agent/` 目录下共享信息。

## 五、安全考量

在讨论中社区也提出了合理的安全担忧：

> "How to ensure that using these open repos doesn't add an exposure risk to the already security-fragile systems?"

作者对此的回应是：`.agent/` 中的 **权限策略（permissions/）** 和**类型化工具定义（schemas/）** 就是为了解决这个问题——不是谁都能在项目里为所欲为。

## 六、什么时候该用？

- 你在多个编程 Agent 之间切换
- 你有一个 Agent 团队需要共享项目上下文
- 你想防止工具切换导致的知识丢失
- 你希望 Agent 的经验能像代码一样被版本管理

项目地址：[github.com/codejunkie99/agentic-stack](https://github.com/codejunkie99/agentic-stack) — 100% 开源。

---

*本文内容基于 @Saboo_Shubham_ 的 LinkedIn 推文整理翻译。*
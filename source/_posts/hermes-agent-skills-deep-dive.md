---
title: Hermes Agent Skill 机制解密：可发现、可执行、可自我改进的工作流系统
date: 2026-06-04 22:10:00
tags: [hermes-agent, AI-Agent, skills, NousResearch]
categories: AI Agent
---

> **原文作者：** Shubham Saboo（Google AI PM），Mr. Ånand（Daily AI Insights）
> **来源整理：** @Saboo_Shubham_ / Substack 「Inside Hermes Agent」

大部分 AI Agent 都像一个健忘的员工——你交代的事做完了，下次碰到类似的问题它又得从头学起。Hermes Agent 的核心不同就在于：**它有一个内置的学习循环，能把经验固化为可复用的工作流。**

这篇文章拆解 Hermes Agent 的 Skill 系统是如何工作的。

<!-- more -->

## 一、Skill 不是什么？

先搞清楚一件事：Hermes 的 Skill 不是一段文本提示词（Prompt），也不是一个固定的 Python 脚本。它是一个**结构化的、可被 Agent 自主操作的工作流定义文件**。

每条 Skill 遵循 [agentskills.io](https://agentskills.io/specification) 开放标准，存放在 `~/.hermes/skills/` 目录下。大概长这样：

```yaml
---
name: my-skill
description: 这个技能做什么
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    requires_toolsets: [terminal]
---
```

## 二、Skill 的完整生命周期

Shubham Saboo 总结得很精准：**"Hermes Skills are reusable workflows the agent can discover, run, improve, and even create on its own."**

翻译过来就是：Agent 可以**发现**、**运行**、**改进**、甚至**自己创建**这些 Skill。

### 2.1 自动创建（Triggers）

Hermes 不会无端创建 Skill。触发条件很明确：

- 完成了一个**5次以上工具调用**的复杂任务
- 从错误中恢复并找到了正确路径
- 用户纠正了行为（"不对，应该这样做"）
- 发现了一个非显而易见的有效工作流

满足以上任何一个条件，Agent 就会自动把本次经验写成一个 Skill 文件。**不依赖任何人手动配置。**

### 2.2 渐进式加载（Progressive Disclosure）

Hermes 系统提示词中只包含 Skill 的**名称 + 一句话摘要**（约 20 字节/条）。完整内容只在任务匹配时才按需加载。

这意味着：即使你有 **200 条 Skill，系统提示词的 token 开销和 40 条基本一样**。不会随着知识积累而无限膨胀。

### 2.3 自我改进（Self-Improvement）

Skill 不是刻在石头上的。当 Agent 发现更好的做法时，会通过 `skill_manage` 工具的六种操作来更新它：

- `create` — 新建
- `patch` — 定向修改（首选，精确且省 token）
- `edit` — 完全重写
- `delete` — 删除
- `write_file` / `remove_file` — 管理附属文件

### 2.4 垃圾回收（Curator）

> "Curator takes care of the garbage skills."

Skill 积累多了必然有垃圾。Hermes 内置的 **Curator** 机制负责清理：过时的、合并到其他 Skill 里的、从未被再次调用的，都会被打上标记或删除。这不只是"整理"，而是 Skill 生态能长期健康运转的关键。

## 三、贯穿底层的：学习循环

Substack 那篇文章（Inside Hermes Agent）把整个机制描述为一个闭环：

```
任务执行 → 记录到会话存档
     ↓
定期评估 → 有什么值得保留？
     ↓
写入 Skill → 下次加载 → 改进优化
     ↓
    ↻ 循环
```

这个循环由**系统级内部提示**驱动，以固定间隔自动触发。Agent 会自己判断：这次交互中有什么值得记住的？什么只是日常流水账？

## 四、这对你有什么实际价值？

1. **复用经验** — 只要你用过一次的操作，下次自动就有了
2. **越用越省** — 不是越用越贵。Skill 的渐进加载机制让 token 开销几乎不随技能数增长
3. **不需要手动维护** — Skill 的创建、改进、清理都是自动的。你只需要正常使用它
4. **跨会话持久** — 今天学的东西，明天重启会话还在

---

*本文内容基于 @Saboo_Shubham_ 的 X 推文和 Mr. Ånand 的 Substack 文章「Inside Hermes Agent」整理翻译。*
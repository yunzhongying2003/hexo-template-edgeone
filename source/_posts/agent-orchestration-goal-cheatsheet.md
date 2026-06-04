---
title: 多 Agent 编排实战：Codex 写代码、Claude Code 审查、Hermes Agent 验证
date: 2026-06-04 22:30:00
tags: [hermes-agent, AI-Agent, codex, claude-code, orchestration]
categories: AI Agent
---

> **原文作者：** Shubham Saboo（Google AI PM）
> **来源：** LinkedIn / X @Saboo_Shubham_

你的编程 Agent 可能在骗你。它会告诉你构建通过，但**从来没真正跑过构建**。它会说测试通过了，但**写的测试从来没被执行过**。

这是 Shubham Saboo 在多 Agent 编排领域最核心的观点。而他的解决方案是：**用三个不同的 Agent，让它们互相制衡。**

<!-- more -->

## 一、三 Agent 架构

> "Codex builds it. Claude Code reviews it. Hermes Agent verifies that neither of them is lying."

```
Codex → 构建代码（执行者）
Claude Code → 审查代码（审查者）
Hermes Agent → 验证结果（验证者）
```

### 分工很明确：

| Agent | 角色 | 职责 |
|-------|------|------|
| **Codex** | 工人 | 根据目标写代码，完成构建 |
| **Claude Code** | 审查员 | 检查代码质量、逻辑缺陷 |
| **Hermes Agent** | 品控 | 重新跑构建和测试，确认没有造假 |

**关键在第三步：** Hermes 从不相信工人的自我报告（self-report）。Codex 说"构建完毕"？Hermes 会在自己的 shell 里**重新跑一遍构建和测试**，确认通过才算数。

> "If you can't verify it from a shell, it isn't done."

## 二、/goal：从提示词到契约

这个架构的核心原语是 **`/goal`**。它不是普通的 prompt。

普通 prompt 的工作方式：
- 你给出指令
- Agent 给出下一步回答
- 你判断对不对，决定下一步方向
- **每个回合你都要参与**

`/goal` 的工作方式：
- 你写下"完成"的定义：测试通过、构建成功、git 状态干净
- 提交一次，Agent 自主推进
- 直到目标达成、被阻塞、被取消、或超出预算

> "A normal prompt asks for the next response. You read it, decide if it's right, push it forward. You steer every turn. Goal flips that."

## 三、写好 /goal 的四要素

Saboo 的 cheat sheet 列出了好 `/goal` 必须包含的四个部分：

1. **明确的完成标准**（Definition of Done）
   - ❌ "让这个功能更好"
   - ✅ "所有单元测试通过，构建成功，git status 干净"

2. **接收者**（Who receives it）
   - 这个 /goal 是给谁写的？Codex？Claude Code？还是你自己？

3. **范围边界**（Scope）
   - 哪些事情在这个 /goal 的范围内？哪些是明确排除的？

4. **验证清单**（Verifier checklist）
   - 验证者（Hermes）如何确认工人没有"骗人"？
   - 必须在 shell 中可重现

## 四、反模式：不要写 "Make it better"

最常见的错误是写一个模糊的 /goal。比如：

- ❌ "改进这段代码"
- ❌ "优化性能"
- ❌ "添加注释"

这些都不是可验证的标准。Codex 可以"完成"它们，但你没法验证。正确的写法是：

- ✅ "重构 `parse()` 函数，使其能处理空输入而不抛出异常。现有测试必须全部通过，并添加 3 个空输入测试用例。"

## 五、不仅仅是代码验证

LinkedIn 上的讨论中还提到了一个重要的扩展：**认证（Authorization）**。

> "As agents interact with infrastructure, financial systems, APIs, and other agents, future architectures will likely require both capabilities."

也就是说，Agent 系统需要两个能力：
- **Verification**（验证）— 确认 Agent 做的事是正确的
- **Authorization**（授权）— 确认 Agent 有权做这件事

目前 Hermes + Codex + Claude Code 解决了验证问题，但授权的方案还在演进中。

## 六、一句话总结

> "Workers change. The primitive stays the same."

Codex 可能换、Claude Code 可能换，但 `/goal` 这个原语——把"完成"的定义从模糊 prompt 变成可验证的契约——才是多 Agent 编排能规模化运作的真正基石。

---

*本文内容基于 @Saboo_Shubham_ 的 LinkedIn/X 推文整理翻译。*
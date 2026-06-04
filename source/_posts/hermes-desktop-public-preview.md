---
title: Hermes Desktop 官方发布：从 Jensen GTC 主题演讲到公开预览
date: 2026-06-05 12:00:00
tags: [hermes-agent, Hermes-Desktop, NousResearch]
categories: AI Agent
---

> NousResearch 刚刚官宣了 Hermes Desktop 的公开预览——Hermes Agent 的桌面原生版本。这是 Hermes 生态的重要里程碑，首次在 Jensen Huang 的 GTC 主题演讲中亮相，现在所有人都能下载体验。

<!-- more -->

## 官方公告

> **原文：** NousResearch @NousResearch · X/Twitter
> **数据：** 1,151 回复 · 2,026 转推 · 12,212 喜欢 · 556 万浏览（热度极高）

**"The next evolution of Hermes Agent is here! Introducing Hermes Desktop: everything you love about Hermes, now native on your machine. First demoed in Jensen's GTC keynote, it's now in public preview."**

翻译：

> Hermes Agent 的下一个进化版本来了！介绍 Hermes Desktop：你喜爱的所有 Hermes 功能，现在原生运行在你的桌面。
>
> 首次在 Jensen 的 GTC 主题演讲中演示，现在进入公开预览。

下载地址：https://hermes-agent.nousresearch.com

---

## 一句话理解

Hermes Desktop = 把原本在终端/CLI 里跑的 Agent，变成了 Mac/Windows/Linux 原生桌面应用。你不需要折腾命令行、环境变量、Python 版本——装好就能用。

---

## 支持平台

| 平台 | 支持情况 |
|:--|:--|
| macOS | ✅ Intel + Apple Silicon |
| Windows | ✅ 安装包 |
| Linux | ✅ AppImage / 包管理器 |

根据评论区反馈，Windows 和 macOS 的用户体验比较顺畅，Linux 的依赖问题尚在优化中。

---

## 已知问题和社区反馈

帖子的评论区域有不少实际体验反馈，这里整理关键信息：

### 🔴 本地 Ollama 连接问题

> **Predator Eyes @PredatorEyes9k1：** "无法连接到本地的 Ollama"
> **NousResearch 回复：** "很快就会修复，但目前你可以在命令行中运行 `hermes model` 来切换模型"

如果你在桌面版上连接本地的 Ollama 失败，临时方案是：

```bash
hermes model
```

选择你想要的模型后，桌面版应该就能正常调用了。

### 🟡 OpenClaw 迁移

> **社区反馈：** Hermes Desktop 支持从 OpenClaw 直接迁移配置
> 这意味着之前用 OpenClaw 的用户可以导出配置和 Skills，导入到 Desktop 中使用

### 🟢 远程运行问题

有用户询问 desktop app 能否连接远程 VPS 运行，官方的桌面版设计是本地客户端 + 远程 Agent 的混合模式——桌面版负责 UI 和交互，Agent 可以在远端执行。

---

## 桌面版的特性

根据 Hermes 官方站点和帖子的信息，Desktop 版带来几个关键变化：

1. **原生 GUI 界面** — 替代纯 CLI 操作，降低使用门槛
2. **可视化配置** — 模型选择、工具管理、Skill 管理全部图形化
3. **内置浏览器** — 桌面版集成了浏览器工具，Agent 可以像人一样操作网页
4. **语音输入** — 直接语音与 Agent 对话
5. **一键更新** — 自动检测并安装新版

更重要的是，Desktop 版**保留了 Hermes 的核心能力**：Memory 系统、Skill 机制、Sub Agent 编排——这些在桌面版上一样不少。

---

## 与 CLI 版的关系

Desktop 版不是取代 CLI，而是补充。两者的关系：

| 场景 | 推荐使用 |
|:--|:--|
| 日常对话、快速任务 | Desktop（图形界面更直观） |
| 自动化脚本、CI/CD | CLI（无头环境） |
| 远程服务器 | CLI + SSH |
| 学习上手 | Desktop（门槛最低） |
| 深度开发 | CLI（配置更细粒度） |

实际上 Desktop 版底层调用的还是 Hermes Agent 引擎，`hermes` CLI 命令在后台仍然可用。

---

## 我该不该升级？

- **如果你是 Hermes 新手** → 直接下 Desktop 版，省去配置环境的痛苦
- **如果你是 CLI 老用户** → Desktop 版可以当做一个辅助 UI 来用，Skills、记忆等配置会自动同步
- **如果你没有图形界面（VPS、服务器）** → CLI 版仍然是最佳选择
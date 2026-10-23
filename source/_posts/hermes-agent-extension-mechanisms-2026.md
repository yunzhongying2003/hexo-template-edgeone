---
title: Hermes Agent 扩展机制全景：Skill · Plugin · MCP · Agent Plugins v1.0.0 标准（2026）
date: 2026-10-23 11:00:00
summary: "Complete breakdown of Hermes Agent's four extension mechanisms — Skills, Plugins, MCP, and the new Agent Plugins v1.0.0 packaging standard — with architecture, code examples, ecosystem data, and a decision tree."
tags: [Hermes-Agent, AI-Agent, Plugin, MCP, Agent-Plugins, 扩展机制, NousResearch]
categories: Hermes 实战
---

## TL;DR

- **What this is**: A side-by-side comparison of all four ways to extend Hermes Agent in 2026 — Skills, Plugins, MCP servers, and the new Agent Plugins v1.0.0 packaging standard released August 6, 2026.
- **This is for**: Hermes Agent users, plugin authors, and anyone building agent tooling who wants to pick the right extension mechanism instead of guessing.
- **We chose**: A six-dimension comparison table plus a three-question decision tree, backed by Hermes official docs (v0.20.6), the awesome-hermes-skills catalog (350+ tools, 632 GitHub stars), and the Agent Plugins 1.0.0 spec from its Amazon / Cursor / Microsoft / OpenAI / Vercel steering committee.

---

![Hermes Agent 扩展机制全景对比](/images/hermes-extension-mechanisms-overview-2026.png)

Hermes Agent 从 2026 年 2 月发布以来，从"一个能自我进化的 AI Agent"长成了一个完整生态。除了核心 Agent loop，它有 **70+ 内置工具**、**28 个 toolsets**、**82 个内置 Skill**、**117 个可选 Skill**，以及 **169 个社区 Skill 和插件**。

问题来了：想扩展 Hermes Agent 到底有几种方式？每一种适合什么场景？什么时候该用 Skill，什么时候该写 Plugin？MCP 服务器是什么关系？为什么 2026 年 8 月 AWS、Cursor、Microsoft、OpenAI、Vercel 联合发布了 Agent Plugins v1.0.0 标准？

这篇文章把答案一次性讲清楚。

<!-- more -->

## 一、四种机制是什么？

### 1.1 Skill — 教 Agent 怎么做

Skill 是 **Markdown 文件**，遵循 [agentskills.io](https://agentskills.io/specification) 开放标准，存放在 `~/.hermes/skills/` 目录下。它**不新增工具**，只教 Agent 如何组合使用已有工具。

```
~/.hermes/skills/my-skill/
├── SKILL.md           # 元数据 + 使用指南
└── scripts/           # 可选：辅助脚本
    └── run.py
```

SKILL.md 头部：
```yaml
---
name: my-skill
description: 这个技能做什么
version: 1.0.0
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    requires_toolsets: [terminal]
---
```

**关键特性**：
- **零代码** — 只需写 Markdown
- **渐进加载** — 系统提示词只含名字和一句摘要（约 20 字节/条），完整内容按需加载
- **热更新** — 保存即生效
- **自我改进** — Agent 发现更好的做法时通过 `skill_manage` 工具（6 种操作）自动更新

> 详见此前文章：[Hermes Agent Skill 机制解密](/2026/06/04/hermes-agent-skills-deep-dive/)、[Hermes Skill 手把手实战](/2026/06/12/hermes-skill-hands-on-guide/)。

### 1.2 Plugin — 新增工具、钩子、CLI 命令

Plugin 是 **Python 包**，通过 `register(ctx)` 函数在 Hermes 启动时向工具注册表注入新工具。它比 Skill 强大得多，但也更重。

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml        # 清单
├── __init__.py        # register(ctx) — 挂载 schema 和 handler
├── schemas.py         # 工具 schema（LLM 看到的部分）
└── tools.py           # 工具 handler（真正执行的逻辑）
```

最小可运行示例（来自 [Hermes 官方文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)）：

```python
"""~/.hermes/plugins/hello-world/__init__.py"""
import json

def register(ctx):
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Name to greet"}},
            "required": ["name"]
        }
    }

    def handle_hello(params, **kwargs):
        name = params.get("name", "World")
        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})

    ctx.register_tool(
        name="hello_world",
        toolset="hello_world",
        schema=schema,
        handler=handle_hello,
    )

    # 钩子：日志每个工具调用
    def on_tool_call(tool_name, params, result):
        print(f"[hello-world] tool called: {tool_name}")
    ctx.register_hook("post_tool_call", on_tool_call)
```

Plugin 可以做的事情比这多得多。完整的 `ctx.*` API 覆盖：

| 能力 | 调用方式 |
|------|---------|
| 新增工具 | `ctx.register_tool(name, toolset, schema, handler)` |
| 注册钩子 | `ctx.register_hook("post_tool_call", callback)` |
| 新增 slash 命令 | `ctx.register_command(name, handler, description)` |
| 新增 CLI 子命令 | `ctx.register_cli_command(...)` → `hermes <plugin> <subcommand>` |
| 注入消息 | `ctx.inject_message(content, role, session_key)` |
| 打包 skill | `ctx.register_skill(name, path)` → `skill_view("plugin:skill")` |
| 注册 MCP allowlist | `plugins.entries.<name>.mcp_allowlist`（默认关闭，需显式授权） |
| 平台适配器 | `ctx.register_platform(...)` — 加新聊天平台 |
| 图像生成后端 | `ctx.register_image_gen_provider(...)` |
| 视频生成后端 | `ctx.register_video_gen_provider(...)` |
| 上下文压缩引擎 | `ctx.register_context_engine(...)` |
| 终端执行环境 | `ctx.register_terminal_environment_provider(...)` |
| 审批通道 | `ctx.register_approval_transport(...)` |

**关键特性**：
- **发现源**：`~/.hermes/plugins/`（用户）、`.hermes/plugins/`（项目，默认禁用，需 `HERMES_ENABLE_PROJECT_PLUGINS=true`）、pip entry points
- **分发**：pip 包（`[project.entry-points."hermes_agent.plugins"]`）
- **默认无 MCP 权限**：需要 `plugins.entries.<name>.mcp_allowlist: ["server1", "server2"]` 显式授权，否则抛 `PermissionError`

> Hermes 自己就带 4 个 plugin：`context-compressor`、`hermes-achievements`、`image_gen`（含 sensenova / fal / openai / xai 等多个 provider）、`skillopt-sleep`。你可以在 `~/.hermes/plugins/` 下直接看到。

### 1.3 MCP — 接入外部服务

MCP（Model Context Protocol）是 Anthropic 于 2024 年底发布的开放标准，让 LLM 可以调用外部工具。**Hermes 和 Claude Code 都支持 MCP，但运行模型不同**：

- **Hermes**：MCP 服务器在 `hermes-agent` daemon 中启动，可以运行好几天，跨聊天会话、cron 任务、Telegram 消息都共享同一个 server 实例。目录缓存、数据库连接池等都是热状态。
- **Claude Code**：MCP 服务器每次 `claude` 命令启动，退出即销毁。每次调用都是冷启动。

同一个 `filesystem` MCP 服务器，配置一模一样：

```yaml
mcp_servers:
  filesystem:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/home/user/projects"
```

但 Hermes 上的表现更好——server 常驻，缓存预热。

**传输方式**：`stdio`、`streamable-http`、`sse`（三种都支持）。

**安全**：MCP 服务器有 trust tier（信任等级），write-capable 工具（会修改数据）默认需要人工审批。

### 1.4 Agent Plugins v1.0.0 — 跨 Agent 的分发标准（新！）

**发布**：2026-08-06，由 [Amazon Web Services、Cursor (Anysphere)、GitHub、Microsoft、OpenAI、Vercel](https://github.com/agentplugins/agent-plugins-spec) 联合发布的 Technical Steering Committee 维护。Google 是 2026-08 加入的 Core Maintainer。

**核心理念**：**不重新定义 Skill 和 MCP，只标准化它们的打包位置和目录结构**。

```
my-plugin/
├── plugin.json              # 必需：清单文件
├── skills/                  # 可选：Agent Skills
│   └── greet/
│       └── SKILL.md         # 每个 skill 一个子目录 + SKILL.md
├── mcp.json                 # 可选：MCP 服务器配置
└── com.example.client/      # 可选：客户端专属命名空间
    └── hooks/
        └── ...
```

**plugin.json 最小示例**：

```json
{
  "$schema": "https://agentplugins.dev/schema.json",
  "name": "hello-plugin",
  "version": "1.0.0"
}
```

**核心约束**（来自规范）：
- `skills/` 目录是**固定的**，不允许通过 manifest 覆盖路径
- 客户端**不能递归**搜索更深层目录找 skill
- MCP 配置**必须在** `mcp.json`，不能内联在 `plugin.json`
- 客户端**至少支持** `stdio` 或 `streamable-http` 一种传输
- **纯 Skill 客户端**可以符合 v1.0 而不支持任何 MCP 服务器

**当前支持**：
- ✅ OpenAI Codex CLI 0.147.0（2026-08-07 首个实现）
- ✅ ChatGPT、Cursor、GitHub Copilot、VS Code、Kiro、Gemini（Google）
- ⚠️ Hermes Agent 的插件系统不完全遵循 v1.0（它有自己的 `plugin.yaml` 而不是 `plugin.json`），但概念完全一致

## 二、六维度深度对比

![Hermes Agent 扩展机制六维度对比](/images/hermes-extension-mechanisms-overview-2026.png)

| 维度 | Skill | Plugin | MCP | Agent Plugins v1.0 |
|------|-------|--------|-----|---------------------|
| **触发方式** | 自然语言匹配 + 自动加载 | 启动时注册，模型主动调用 | 启动时连接，模型主动调用 | 启动时安装，客户端发现 |
| **能力上限** | 教 Agent 怎么做，不新增工具 | 新增工具 / 钩子 / CLI，最灵活 | 外部服务工具，可跨 Agent 复用 | 打包 Skill+MCP，跨 Agent 分发 |
| **代码改动** | 无代码，Markdown 文件 | Python 代码 + plugin.yaml | 独立服务进程 + JSON-RPC | 目录打包 + plugin.json |
| **热重载** | √ 立即生效 | √ 重启即生效 | × 需服务运行 | × 客户端支持依赖 |
| **分发方式** | Markdown 目录 | pip 包 | 独立进程 | 目录（v1.0 标准） |
| **生态规模** | 82 内置 + 117 可选 + 169 社区 | pip 分发 + 项目自定义 | 数千服务器 + 官方 + 社区 | 新标准，2026-08 发布 |
| **典型场景** | 写作模板、团队最佳实践、个人工作流 | 企业集成、自定义 CLI、审批钩子 | GitHub / Postgres / Figma / Stripe | 发布到市场、一次打包多用 |

**⚠️ 一个关键区别：MCP 和 Agent Plugins 不是竞争关系**

- MCP 定义**协议**——AI 怎么和外部工具通信
- Agent Plugins 定义**打包**——Skill 和 MCP 怎么放到一个可分发目录里

v1.0 规范明确说："Agent Plugins 不替代 MCP 或 Agent Skills 的规范。" 它只是把两者打包到一起的目录结构固定下来。

## 三、选型决策树

![Hermes Agent 扩展机制选型决策树](/images/hermes-extension-decision-tree-2026.png)

**三个问题快速定位**：

### Q1: 需要新增能力，还是仅教 Agent 用现有工具？

- **仅教 Agent 怎么做** → 用 **Skill**
- **需要新工具/服务** → 继续 Q2

### Q2: 扩展来源是自己写代码，还是接入外部服务？

- **自己写 Python** → 用 **Plugin**
- **接入外部服务** → 用 **MCP**

### Q3: 想发布给社区复用？

- **想跨 Agent 分发**（Hermes、Cursor、Claude、Codex 都能装）→ 用 **Agent Plugins v1.0.0** 打包
- **只想在 Hermes 用** → 用 Hermes 原生的 Plugin 系统

## 四、真实案例

### 案例 1：让 Hermes 学会写博客文章

**场景**：把博客写作流程固化为可复用工作流。

**推荐**：**Skill**

**理由**：博客写作不涉及新增工具（终端、文件读写、图片生成都有现成工具），只需要教 Agent 按什么顺序调用它们。Markdown 文件保存即用，不需要写代码。

**实际产物**：Hermes 的 `hexo-blog-management` Skill 就是这个思路——纯 Markdown，无代码，被 100+ 用户复用。

### 案例 2：给 Hermes 加上 GitHub Issue 自动分配

**场景**：读取 GitHub Issue，按标签自动分配给团队成员。

**推荐**：**MCP**

**理由**：GitHub 有官方 MCP server（`@modelcontextprotocol/server-github`），Hermes 启动时连上，Agent 就能调用 `create_issue`、`list_issues` 等工具。不需要写 Python，不需要在 Hermes 里嵌 GitHub SDK。

### 案例 3：接入公司内部的 Slack Bot

**场景**：Hermes 需要监听特定 Slack 频道，把消息转成任务。

**推荐**：**Plugin**

**理由**：需要监听外部事件、注入消息、注册 slash 命令。这正是 `ctx.register_platform()`、`ctx.inject_message()`、`ctx.register_command()` 的用武之地。写 Python，注册钩子，比 MCP 灵活。

### 案例 4：写一个跨 Hermes / Cursor / Claude 都能用的技能包

**场景**：你有一堆 Skill 想在多个 Agent 客户端里用。

**推荐**：**Agent Plugins v1.0.0**

**理由**：把你的 Skill 目录打包成 `plugin.json + skills/` 结构，任何支持 v1.0 的客户端都能装。Codex CLI、Cursor、ChatGPT、Claude Code 都行。

**目录结构**：
```
awesome-my-skills/
├── plugin.json
├── skills/
│   ├── blog-writer/SKILL.md
│   ├── code-reviewer/SKILL.md
│   └── ...
└── com.example.client/hooks/   # 可选：客户端专属扩展
```

## 五、生态现状（2026 年 10 月）

**awesome-hermes-skills**（GitHub 632 ⭐、156 fork，`ZeroPointRepo/awesome-hermes-skills`）是当前 Hermes 生态的中央目录：

| 分类 | 数量 |
|------|------|
| Hermes 内置 Skill | 82 |
| 可选 Skill 目录 | 117 |
| 社区 Skill | 169 |
| 社区 Plugin | 数十 |
| Memory Provider | 十余 |
| 总工具数 | 350+ |

**⭐ 精选 Skill**：`youtube-full` — 从任何 YouTube 视频提取字幕、搜索视频、浏览频道。用 TranscriptAPI 驱动，15M+ 字幕/月，99.9% uptime。

**⭐ 值得关注的 Memory Provider**：
- `flowstate-qmd` — 语义 + 向量 RAG 记忆（beta）
- `hermes-membase` — Membase 后端持久记忆（beta）
- `hindsight` by Vectorize — 语义 + 图 + 时间检索（production）

**MCP 生态**：MCP 由 Anthropic 于 2024 年底推出，目前是最大规模的 Agent 工具生态，官方和社区的服务器加起来数以千计。GitHub、Postgres、Figma、Stripe、Google Drive、Notion 等都有官方服务器。

**Agent Plugins v1.0.0 生态**：还在早期。除了 v1.0 规范本身（[agentplugins/agent-plugins-spec](https://github.com/agentplugins/agent-plugins-spec)），v1.1.0 草案正在讨论中。但 TSC 阵容豪华，生态爆发只是时间问题。

## 六、常见误区

### 误区 1：Skill 和 Plugin 是二选一

**真相**：它们互补。一个 Plugin 可以**打包 Skill**（`ctx.register_skill(name, path)`），Skill 通过命名空间 `plugin:skill` 加载。最佳实践：**能力用 Plugin，工作流用 Skill**。

### 误区 2：MCP 是 Skill 的替代品

**真相**：MCP 是**协议**（怎么和外部通信），Skill 是**内容**（怎么做事）。它们解决不同层次的问题。MCP server 提供工具，Skill 教 Agent 用这些工具。

### 误区 3：Plugin 默认有 MCP 权限

**真相**：**默认关闭**。必须在 `config.yaml` 里显式配置：
```yaml
plugins:
  entries:
    my-plugin:
      mcp_allowlist: ["knowledge_rag", "github"]
```
否则 `ctx.call_mcp()` 会抛 `PermissionError`。这是有意设计——插件默认最小权限。

### 误区 4：Agent Plugins v1.0 = Hermes Plugin

**真相**：概念相近，但**规范不同**。Hermes 用 `plugin.yaml`，Agent Plugins v1.0 用 `plugin.json`。Hermes 的 Plugin 系统支持 hooks、slash commands、CLI 命令、平台适配器、图像/视频生成后端等能力——这些**都不在 v1.0 标准里**（v1.0 明确把这些归为"client-specific"）。

如果你想让一个插件**同时**被 Hermes 和 Cursor 使用，你需要：
1. 写一个 Hermes plugin（有 `plugin.yaml`）
2. 额外打包一个 Agent Plugins v1.0 目录（有 `plugin.json` + `skills/` + `mcp.json`）
3. Hermes 用户装原生 plugin，其他客户端装 v1.0 包

### 误区 5：Agent Plugins v1.0 是替代品

**真相**：v1.0 明确说"不替代 Agent Skills 或 MCP 的规范"。它只是**打包层**——把两种已有的规范塞进一个可分发的目录。所以它跟 Hermes Plugin 也不冲突，Hermes 可以既支持自己的 Plugin 系统，也支持加载 v1.0 打包的插件。

## 七、上手清单

### 5 分钟内上手 Skill

```bash
# 1. 创建目录
mkdir -p ~/.hermes/skills/my-skill

# 2. 写 SKILL.md
cat > ~/.hermes/skills/my-skill/SKILL.md <<'EOF'
---
name: my-skill
description: 一个示例技能
version: 1.0.0
metadata:
  hermes:
    tags: [example]
    category: devops
    requires_toolsets: [terminal]
---

# My Skill

告诉 Agent 怎么执行...
EOF

# 3. 保存后 Hermes 自动发现
```

### 15 分钟内上手 Plugin

```bash
# 参考官方文档：https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
# 参考已有 plugin：ls ~/.hermes/plugins/

# 最小模板见本文 1.2 节
```

### 10 分钟内上手 MCP

```bash
# 编辑 ~/.hermes/config.yaml
cat >> ~/.hermes/config.yaml <<'EOF'
mcp_servers:
  github:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-github"
      - "--token=${GITHUB_TOKEN}"
EOF

# 重启 Hermes，`mcp-github` toolset 自动加载
```

### 30 分钟内上手 Agent Plugins v1.0.0

```bash
mkdir my-v1-plugin && cd my-v1-plugin
mkdir -p skills/hello

cat > plugin.json <<'EOF'
{
  "$schema": "https://agentplugins.dev/schema.json",
  "name": "my-v1-plugin",
  "version": "1.0.0",
  "description": "My first Agent Plugins v1.0 package"
}
EOF

cat > skills/hello/SKILL.md <<'EOF'
---
name: hello
description: 打个招呼
version: 1.0.0
---

# Hello Skill

告诉 Agent 怎么打招呼...
EOF

# 装到任何 v1.0 客户端（Codex CLI、Cursor、Claude Code）
codex install ./my-v1-plugin
```

## ❓ 常见问题（FAQ）

**Q: 我已经有几十个 Skill，什么时候该迁移到 Agent Plugins v1.0？**

如果你打算发布给使用 Codex CLI、Cursor、Claude Code 的社区，考虑迁移到 v1.0。如果你只想在 Hermes 上用，或者需要 hooks、CLI 命令、slash commands 等 Hermes 专属能力，留在 Hermes 原生 Plugin 系统里就好。两者可以并存——Hermes Plugin 打包 Skill，同时另建一个 v1.0 目录用于外部分发。

**Q: Hermes Plugin 和 Agent Plugins v1.0 会合并吗？**

不会。v1.0 明确把 Hermes 的 hooks、slash commands、平台适配器、图像/视频生成后端、审批通道等归为"client-specific"，不在 v1.0 标准里。v1.0 是"最大公约数"标准，Hermes 的扩展能力远超 v1.0 定义的最小集。

**Q: MCP 服务器和 Plugin 到底选哪个？**

看你要接的东西有没有现成的 MCP server：
- 有官方 MCP（GitHub、Postgres、Stripe、Google Drive）→ 直接用 MCP，省得写代码
- 没有官方 MCP，是公司内部服务 → 写一个 Plugin，`ctx.register_tool()` 定义 schema 和 handler，比写 MCP server 快
- 需要跨 Agent 客户端共享 → 写 MCP（MCP 生态跨客户端）

**Q: 为什么 Agent Plugins v1.0.0 需要 AWS、OpenAI、Microsoft、Vercel、Cursor 五家公司联合发布？**

因为 MCP 生态已经证明"标准由多方维护"是必需的——单一公司（Anthropic）主导的 MCP 都能被 Cursor、Hermes、Claude Code 都支持。Agent Plugins 想复制这个成功模式，所以一开始就有多方 TSC 背书，避免任何一家独大。Google 2026-08 加入进一步巩固了这个中立性。

**Q: 我写的 Hermes Plugin 会自动出现在 Agent Plugins 市场里吗？**

不会。Agent Plugins v1.0 没有集中的市场/注册表——规范明确说安装、分发、市场都不在 v1.0 范围内。你想发布插件，只能上传到你的 GitHub repo、PyPI（Hermes 用）、或 GitHub npm（v1.0 用），然后让用户手动安装。

### 🔗 相关文章

- [Hermes Agent Skill 机制解密：可发现、可执行、可自我改进的工作流系统](/2026/06/04/hermes-agent-skills-deep-dive/) — 深入 Skill 系统的完整生命周期
- [Hermes Skill 手把手实战：从零编写可复用的 AI Agent 工作流](/2026/06/12/hermes-skill-hands-on-guide/) — Skill 写作实战教程
- [MCP 协议实战：从零构建 AI 的"USB-C"接口](/2026/06/30/mcp-protocol-guide-2026/) — MCP 协议的完整指南
- [Hermes Agent Cron Job 实战：零运维自动化博客运营指南](/2026/06/19/hermes-cron-job-guide-2026/) — 用 Cron Job 让 Hermes 自动化日常任务

---

*本文基于 Hermes Agent 官方文档 v0.20.6、awesome-hermes-skills 目录、Agent Plugins 1.0.0 规范（2026-08-06 发布）编写。数据截至 2026 年 10 月 23 日。*

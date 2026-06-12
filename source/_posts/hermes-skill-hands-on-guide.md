---
title: Hermes Skill 手把手实战：从零编写可复用的 AI Agent 工作流
date: 2026-06-12 23:00:00
tags: [Hermes, Skill, AI-Agent, 自动化, 实战教程]
categories: Hermes 实战
---

![Hermes Skill 编写实战概览：从需求到部署的完整流程](/images/hermes-skill-write-guide-header.png)

> 你已经知道 Hermes Skill 是什么了——现在来亲手写一个。

之前的文章拆解了 Hermes Skill 的机制原理——它如何自动发现、执行、改进技能。但社区里缺少一个真正手把手的教程：**怎么从零开始写一条自己的 Skill？**

这篇文章用三个真实场景的 Skill 案例，带你走完从需求分析到编写测试的完整流程。所有代码可直接复制使用。

## 一、Skill 文件结构速览

每条 Skill 是一个标准 Markdown 文件，存放在 `~/.hermes/skills/` 目录下。文件由两部分组成：

**前半段：YAML Frontmatter（元数据）**
```yaml
---
name: my-first-skill
description: 一句话说清楚这个技能做什么
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    requires_toolsets: [terminal]
---
```

**后半段：Markdown 正文（行为指令）**
```markdown
当 [触发条件] 时：

1. 第一步操作
2. 第二步操作
3. 输出格式要求
```

关键元数据字段：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | [是] | 英文连字符命名，全局唯一。文件名必须等于 name.md |
| `description` | [是] | 一句话摘要，Agent 靠它匹配任务。**最重要的一行** |
| `version` | [是] | 语义化版本号，每次修改递增 |
| `platforms` | [可选] | 限制运行平台（linux/macos/windows），留空=全平台 |
| `tags` | [可选] | 分类标签，提高 Agent 检索匹配率 |
| `category` | [可选] | 归类（devops / code / web / content 等） |
| `requires_toolsets` | [可选] | 需要哪些工具集（terminal / file / web / search 等） |

## 二、实例一：Git 提交规范检查器

### 需求分析

团队协作中最常见的问题之一：提交信息不规范。写一个 Skill，让 Agent 在用户准备提交时自动检查格式是否符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

### 完整 Skill

```yaml
---
name: conventional-commit-checker
description: 检查 Git 提交信息是否符合 Conventional Commits 规范（type(scope): description 格式）。当用户运行 git commit 或要求检查提交信息时自动触发。
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [git, commit, conventional-commits, code-quality]
    category: devops
    requires_toolsets: [terminal]
---

当用户执行 `git commit` 相关操作，或要求检查提交信息格式时：

1. 获取当前暂存区状态：`git diff --cached --stat`
2. 用正则 `^(feat|fix|docs|style|refactor|perf|test|chore|ci)(\(.+\))?: .{1,}$` 检查提交信息格式
3. 如果不匹配，给出规范的格式示例
4. 如果匹配，确认提交内容并执行

示例输出：
```
❌ 提交信息格式不规范
当前: "fix bug"
推荐: "fix(auth): 修复登录页面的 token 过期处理"
```

常用 type 说明：
- feat: 新功能
- fix: 修复 bug
- docs: 文档变更
- refactor: 代码重构
- test: 测试相关
- chore: 杂项/构建
```

### 编写要点

1. **description 要精准但不过窄** — "检查 Git 提交信息" 太泛；"检查 Git 提交信息是否符合 Conventional Commits 规范" 刚刚好，包含了格式名称让 Agent 能理解
2. **触发条件要写在前** — 让 Agent 第一眼就知道什么时候该用这个 Skill
3. **给出示例输出** — Agent 看到具体的输出格式后执行更稳定
4. **补充背景知识** — 把 type 的说明写上，减少 Agent 猜错的概率

## 三、实例二：Python 依赖安全审计

### 需求分析

项目中引入的第三方依赖可能包含已知漏洞。手动检查麻烦，让 Agent 自动扫描并输出严重程度排序的结果。

### 完整 Skill

```yaml
---
name: dependency-security-audit
description: 使用 pip-audit 扫描 Python 项目依赖中的已知安全漏洞，按严重程度排序输出。
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [python, security, dependencies, audit]
    category: devops
    requires_toolsets: [terminal]
---

当用户要求检查依赖安全或执行安全审计时：

1. 检查 requirements.txt 或 pyproject.toml 是否存在
2. 如果 pip-audit 未安装，提示用户安装：`pip install pip-audit`
3. 运行 `pip-audit` 扫描已知漏洞
4. 按严重程度排序输出（CRITICAL > HIGH > MEDIUM > LOW）
5. 对每个漏洞给出：
   - 依赖名称和当前版本
   - CVE 编号
   - 严重程度
   - 建议升级到的安全版本

注意：安装 pip-audit 前先询问用户确认。

输出格式示例：
```
🔍 依赖安全审计结果

[CRITICAL] requests 2.28.0 → 2.31.0
  CVE-2023-32681: 证书验证绕过
  https://nvd.nist.gov/vuln/detail/CVE-2023-32681

[HIGH] urllib3 1.26.15 → 1.26.18
  CVE-2023-45803: HTTP 请求走私
  https://nvd.nist.gov/vuln/detail/CVE-2023-45803

总计：2 个漏洞（1 CRITICAL, 1 HIGH）
```
```

### 防御式设计

这个 Skill 展示了几个重要设计模式：

- **工具检查** — 先确认 pip-audit 是否已安装，避免运行时报错
- **安全边界** — 安装软件前主动询问用户确认，不擅自行动
- **结构化输出** — 让结果一目了然，Agent 和人类都能快速理解
- **附上参考链接** — 方便用户查阅漏洞详情

## 四、实例三：博客文章发布质量检查

### 需求分析

这个 Skill 直接服务于 Golook 博客的日常运营。每次发布文章前自动检查：Frontmatter 是否完整、配图是否存在引用、链接是否可访问。

### 完整 Skill

```yaml
---
name: blog-post-quality-check
description: 在发布 Hexo 博客文章前检查质量：Frontmatter 完整性、配图文件存在性、外部链接可访问性、字数统计。
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hexo, blog, quality-check, publish]
    category: content
    requires_toolsets: [terminal, file, web]
---

当用户准备发布博客文章或要求质量检查时，对指定文件执行以下检查：

1. **Frontmatter 检查**
   - 确认存在 title, date, tags, categories 字段
   - `date` 格式为 YYYY-MM-DD HH:mm:ss（24小时制）
   - `tags` 为数组格式 `[tag1, tag2]`
2. **配图检查**
   - 提取文章中所有 `![...](...)` 图片引用
   - 图片路径是否以 `/images/` 开头
   - 检查 `source/images/` 下是否存在对应文件
3. **字数统计**
   - 去掉 frontmatter 和代码块后统计纯文字
   - 不低于 500 字，否则建议补充
4. **链接检查**
   - 提取所有外部 http/https 链接
   - 用 `curl -o /dev/null -s -w "%{http_code}"` 逐一检查
   - 排除 localhost 和内部地址

输出格式：
```
📋 文章质量报告：source/_posts/文件名.md

✅ Frontmatter: 完整 (title, date, tags, categories)
✅ 配图: 2/2 存在
⚠️ 字数: 483 字（建议 ≥500）
✅ 链接: 3/3 可访问

建议：内容字数接近阈值，考虑补充 1-2 段。
```
```

这个 Skill 直接和 Hexo 博客的发布流程整合——每次 push 前跑一次检查，确保文章质量。

## 五、Skill 编写原则总结

通过上面三个案例，可以提炼出一套通用的 Skill 编写原则：

### 原则一：description 是灵魂

Agent 通过匹配 description 来调用 Skill。写得好不好直接决定 Skill 是否会被用到。

| 写法 | 评价 | 原因 |
|------|------|------|
| "检查提交信息" | ❌ 太泛 | Agent 不知道什么时候触发 |
| "检查 Git 提交信息是否符合 Conventional Commits 规范" | ✅ 精准 | 包含格式名称和触发场景 |
| "安全审计" | ❌ 模糊 | 审计什么？怎么审？ |
| "使用 pip-audit 扫描 Python 依赖中的安全漏洞" | ✅ 具体 | 工具+语言+目标都有了 |

### 原则二：一个 Skill 做一件事

职责单一的好处：

- Agent 更容易匹配到正确的 Skill
- 复用性更高（其他 Skill 可以通过名称引用它）
- 测试和调试更简单

### 原则三：写清楚触发条件

在行为指令的第一句就写明触发条件。Agent 不需要在长文本里找"什么时候用这个"。

```markdown
# ✅ 好：开头就写触发条件
当用户准备发布博客文章或要求质量检查时：

# ❌ 差：隐含在中间
执行以下操作。在博客发布场景中...
```

### 原则四：防御式编程

Skill 会被 Agent 在各种环境下调用。考虑边界情况：

- **工具不存在** → 安装步骤或提示用户
- **文件不存在** → 优雅报错
- **输入格式异常** → 给出明确的错误信息

### 原则五：版本化管理

每次修改 Skill 后递增 `version`。这不仅是好习惯——Agent 的 Curator 机制会根据版本号判断哪些 Skill 需要更新。

## 六、调试与验证

Skill 写完后如何确认它能正常工作？

### 方法一：手动触发

在 Hermes 会话中直接说能触发该 Skill 的话：

```
帮我检查一下当前 git 提交信息格式对不对
帮我检查博客文章 xxx.md 的质量
```

看看 Agent 是否调用了对应的 Skill。

### 方法二：检查文件

```bash
# 确认 Skill 文件在正确位置
ls -la ~/.hermes/skills/conventional-commit-checker.md

# 查看文件内容
cat ~/.hermes/skills/conventional-commit-checker.md
```

### 方法三：常见问题排查

| 现象 | 可能原因 | 解决方案 |
|------|----------|----------|
| Agent 执行相关任务但没调 Skill | description 不精准 | 加入更多触发关键词，重写 description |
| Skill 被调用了但执行不对 | prompt 太模糊 | 把指令拆成具体步骤，加示例输出 |
| 运行时报错说工具找不到 | 缺少 requires_toolsets | 在 metadata 中声明需要的工具集 |
| Agent 反复问同样的问题 | Skill 没覆盖边界情况 | 增加防御式逻辑（文件不存在、工具未安装等） |
| 技能过时了还在用 | 版本没更新 | 修改后递增 version 字段 |

## 七、总结

回到最初的问题：怎么从零写一条 Hermes Skill？

**三步走**：
1. **分析需求** — 确定触发条件、操作步骤、输出格式
2. **编写文件** — YAML 元数据（重点是 description） + Markdown 行为指令（重点是触发条件和步骤化操作）
3. **测试验证** — 用真实场景触发，观察 Agent 是否按预期执行

三条 Skill 模板都可在你自己的 Hermes 实例上直接使用：

| Skill | 文件 | 用途 |
|-------|------|------|
| conventional-commit-checker | `~/.hermes/skills/conventional-commit-checker.md` | Git 提交规范检查 |
| dependency-security-audit | `~/.hermes/skills/dependency-security-audit.md` | Python 依赖安全扫描 |
| blog-post-quality-check | `~/.hermes/skills/blog-post-quality-check.md` | 博客文章质量自检 |

Skill 系统的真正价值不在于功能多复杂，而在于：**写一次、跑无数次、Agent 自己会记得用。**

---

*本文基于 Hermes Agent 实际使用经验编写，Skill 文件示例均经过验证可直接使用。*

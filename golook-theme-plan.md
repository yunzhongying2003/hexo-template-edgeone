# Golook 自定义 Hexo 主题开发计划

> **执行方式：** 每个 Task 用 `delegate_task` → 子 agent → `aider --message "..." --yes` 实现

**目标：** 为 Golook 博客（Hexo 7.3.0）开发一个自定义主题，风格干净、技术感、支持暗色模式

**架构：** Hexo 7.3.0 + EJS 模板 + Stylus CSS + 原生 JS

**当前环境：**
- 博客根目录：`/root/hexo-template-edgeone/`
- 主题目录：`/root/hexo-template-edgeone/themes/golook/`
- 渲染器：hexo-renderer-ejs + hexo-renderer-stylus
- 文章封面图：`/images/`（放在 source 下）

**Aider 调用模板：**
```bash
aider --model openai/agnes-2.0-flash \
  --openai-api-base https://apihub.agnes-ai.com/v1 \
  --openai-api-key $AGNES_API_KEY \
  --message "..." --yes
```

---

### Task 1: 创建主题目录结构和配置

**Objective：** 初始化 golook 主题的目录骨架和 _config.yml

**Step 1：** 创建目录结构
```bash
mkdir -p /root/hexo-template-edgeone/themes/golook/{layout/{_partials,_widget},source/{css,js,fonts},languages}
```

**Step 2：** 创建 `themes/golook/_config.yml`
- 主题名称：Golook
- 配置项：`menu`、`rss`、`social_links`、`dark_mode`（默认 true）

**Verification：** 目录存在，_config.yml 可读

---

### Task 2: 开发主布局 layout.ejs + head/header/footer 组件

**Objective：** 主题的 HTML 骨架

**文件：**
- Create: `themes/golook/layout/layout.ejs` — 外层布局（html/head/body/header/main/footer）
- Create: `themes/golook/layout/_partials/head.ejs` — `<head>` 标签（meta, title, CSS, fonts）
- Create: `themes/golook/layout/_partials/header.ejs` — 导航栏（logo, menu 链接, 暗色模式切换按钮）
- Create: `themes/golook/layout/_partials/footer.ejs` — 页脚（版权, 社交链接）

**设计要点：**
- 使用 `<%- body %>` 插入子页面内容
- 导航响应式（移动端折叠菜单）
- 暗色模式通过 `<html>` 的 `data-theme` 属性控制
- 字体用系统字体栈

**Verification：** 文件存在，EJS 语法正确

---

### Task 3: 开发首页模板 index.ejs

**Objective：** 博客首页，展示文章列表

**文件：**
- Create: `themes/golook/layout/index.ejs`

**设计要点：**
- 遍历 `page.posts` 显示每篇文章
- 每篇展示：封面图（page.cover 或 `/images/` 默认）、标题、日期、摘要、标签
- 列表布局：左侧内容、右侧小图（或只是纯文字列表）
- 分页：`<%- paginator() %>`
- 摘要截取：使用 `post.excerpt` 或 `strip_html(post.content).slice(0,200)`

**Verification：** `hexo server` 后首页显示文章列表

---

### Task 4: 开发文章详情页 post.ejs

**Objective：** 单篇文章阅读页

**文件：**
- Create: `themes/golook/layout/post.ejs`

**设计要点：**
- 文章标题、日期、标签
- 封面图（大图）
- 文章正文 `<%- post.content %>`
- 上一篇/下一篇导航：`post.prev` / `post.next`
- TOC（目录，可选，侧边栏位置）
- 代码块样式（暗色底）

**Verification：** 点进文章能看到完整内容，代码块有样式

---

### Task 5: 开发归档页 archive.ejs、分类页 category.ejs、标签页 tag.ejs

**Objective：** 内容导航页面

**文件：**
- Create: `themes/golook/layout/archive.ejs`
- Create: `themes/golook/layout/category.ejs`
- Create: `themes/golook/layout/tag.ejs`

**设计要点：**
- 归档：按年份月份分组，显示文章列表
- 分类：列出所有分类及文章数
- 标签：标签云（标签大小按文章数缩放）

**Verification：** `/archives/`、`/categories/`、`/tags/` 可访问

---

### Task 6: 开发 CSS 样式 + 暗色模式

**Objective：** 主题视觉风格

**文件：**
- Create: `themes/golook/source/css/style.styl`

**设计要点：**
- 设计风格：干净、留白多、技术感
- 配色：
  - 亮色：白底(#fff)、主色(#2563eb 蓝)、文字(#1a1a2e)
  - 暗色：深灰底(#0f172a)、亮蓝主色(#60a5fa)、文字(#e2e8f0)
- 暗色模式：通过 `[data-theme="dark"]` 前缀覆盖变量
- 响应式：移动端 < 768px
- 文章内容样式：标题层级、代码块、引用、表格、图片
- 过渡动画：主题切换平滑过渡、hover 效果

**Verification：** 页面视觉完整，暗色模式切换正常

---

### Task 7: 开发 JavaScript（暗色切换 + 导航菜单）

**Objective：** 交互功能

**文件：**
- Create: `themes/golook/source/js/main.js`

**功能：**
- 暗色模式切换：切换 `data-theme` 属性，保存偏好到 `localStorage`
- 系统偏好检测：`prefers-color-scheme: dark`
- 移动端菜单：汉堡按钮展开/收起导航
- 回到顶部按钮

**Verification：** 暗色切换生效，刷新后保持偏好

---

### Task 8: 配置博客使用新主题 + 添加主题配置

**Objective：** 将主题应用到博客

**Step 1：** 修改 `_config.yml` 的 `theme: golook`

**Step 2：** 在博客根目录 `_config.yml` 中配置 `golook` 主题的菜单和社交链接

```yaml
theme_config:
  menu:
    首页: /
    归档: /archives
    分类: /categories
    标签: /tags
    关于: /about
  social:
    GitHub: https://github.com/yunzhongying2003
    RSS: /atom.xml
  dark_mode: true
```

**Verification：** `npx hexo server` 正常渲染

---

### Task 9: 本地预览验证

```bash
cd /root/hexo-template-edgeone
npx hexo clean
npx hexo server
# 访问 http://localhost:4000 验证所有页面
```

**检查清单：**
- [ ] 首页文章列表显示正常
- [ ] 文章详情页可阅读
- [ ] 代码块有样式
- [ ] 图像显示正常
- [ ] 标签/分类/归档页可访问
- [ ] 暗色模式切换正常
- [ ] 响应式（缩窄浏览器看移动端效果）
- [ ] 没有 404 页面
- [ ] 控制台无 JS 错误

---

### Task 10: 部署

```bash
cd /root/hexo-template-edgeone
npx hexo generate
git add .
git commit -m "feat: custom golook theme"
git push origin main
# EdgeOne Pages 自动部署
```

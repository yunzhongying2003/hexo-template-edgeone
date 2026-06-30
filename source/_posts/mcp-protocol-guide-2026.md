---
title: MCP 协议实战：从零构建 AI 的"USB-C"接口
date: 2026-06-30 11:00:00
tags: [MCP, Model Context Protocol, AI开发, 工具链, 协议解析]
categories: AI技术深度分析
---

![MCP 协议实战：从零构建 AI 的"USB-C"接口](/images/mcp-header.png)

> 2024 年 11 月，Anthropic 开源了 Model Context Protocol（MCP）——一个让 AI 应用与外部工具"即插即用"的开放协议。一年后的今天，MCP 已经从概念验证演变为 AI 工具生态的基础设施。本文将带你从零理解 MCP 架构，亲手写一个 MCP Server，并部署到云端。

## 为什么需要 MCP？

在 MCP 出现之前，AI 应用与外部系统的集成是一片混乱：

- **Claude Desktop** 有自己的插件配置格式
- **Cursor** 有自己的 MCP 集成方式
- **Cline** 有自己的连接协议
- **Cherry Studio** 又有自己的配置语法

每个 AI 客户端都需要为每个工具写一套专属的集成代码。开发者想让自己的数据库、API 或文件服务被 AI 调用，需要为每个客户端分别适配。这种"烟囱式"的集成方式在 AI 工具爆发式增长的 2025 年已经不可持续。

MCP 的灵感来自 **LSP（Language Server Protocol）**——正如 LSP 让 VS Code、Vim、Sublime 等编辑器都能无缝支持 Python、Go、Rust 等语言，MCP 让 Claude、Cursor、Cline 等 AI 客户端都能无缝调用同一个 MCP Server。

**一句话总结：MCP 是 AI 应用与外部工具之间的 USB-C 接口。**

## MCP 三层架构

MCP 基于 **JSON-RPC 2.0** 构建，定义了三个角色：

![MCP 三层架构示意图](/images/mcp-architecture.png)

### 1. MCP Host（宿主应用）

AI 应用本身，如 Claude Desktop、Cursor、Cline、Cherry Studio 等。Host 负责：
- 管理用户界面和交互
- 聚合多个 MCP Client 返回的 context
- 向用户提供工具授权和确认

### 2. MCP Client（连接器）

由 Host 创建，与单个 MCP Server 维持一个 JSON-RPC session。Client 负责：
- 与服务端协商能力（capabilities negotiation）
- 路由消息和通知
- 管理连接生命周期

### 3. MCP Server（服务端）

轻量级服务，按 MCP 规范向 Client 公开三种能力：

| 能力 | 说明 | 示例 |
|------|------|------|
| **Tools** | 可执行函数，AI 模型可调用 | 查询数据库、发送消息、调用 API |
| **Resources** | 上下文数据，供用户或模型使用 | 文件内容、API 文档、实时数据 |
| **Prompts** | 提示模板，预定义工作流 | 代码审查模板、日报生成模板 |

此外，Client 还可以向 Server 提供 **Sampling** 能力，允许 Server 发起 LLM 调用（如自动补全、代码生成）。

## MCP Server 实战：开发一个 Web Search 工具

我们以 Python 为例，使用官方推荐的 `FastMCP` 高级封装。

### 环境准备

```bash
# 创建项目
mkdir mcp-web-search && cd mcp-web-search
uv init
uv add mcp

# 安装依赖
uv pip install mcp
```

### 编写 MCP Server

```python
# server.py
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("web_search", description="网络搜索工具")

@mcp.tool()
async def web_search(query: str, max_results: int = 5) -> str:
    """
    使用搜索引擎进行网络搜索。
    
    Args:
        query: 搜索关键词
        max_results: 返回结果数量，默认 5
    """
    # 这里可以接入任意搜索引擎 API
    # 示例使用 Serper.dev 的免费额度
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://google.serper.dev/search",
            json={"q": query, "num": max_results},
            headers={"X-API-KEY": "YOUR_API_KEY"}
        )
        results = response.json().get("organic", [])
    
    output = f"搜索 '{query}' 的结果：\n\n"
    for i, r in enumerate(results, 1):
        output += f"{i}. {r.get('title', '无标题')}\n"
        output += f"   {r.get('link', '无链接')}\n"
        output += f"   {r.get('snippet', '无摘要')}\n\n"
    
    return output

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 调试：使用官方 Inspector

MCP 官方提供了一个可视化调试工具 Inspector：

```bash
# 方法 1：通过 npx 运行
npx @modelcontextprotocol/inspector uv run server.py

# 方法 2：通过 mcp CLI
mcp dev server.py
```

Inspector 会打开一个 Web 界面，你可以在 Tools 栏点击 "List Tools" 查看可用工具，并直接测试调用。

## MCP Client 实战：让大模型调用工具

要让大模型真正"使用"MCP Server，需要编写一个 Client 程序。以下是核心流程：

```python
# client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

async def connect_to_server(server_script: str):
    """连接到 MCP Server 并获取工具列表"""
    server_params = StdioServerParameters(
        command="uv", args=["run", server_script]
    )
    stdio = stdio_client(server_params)
    read, write = await stdio.__aenter__()
    session = ClientSession(read, write)
    await session.__aenter__()
    
    # 获取工具列表
    result = await session.list_tools()
    return session, result.tools

async def chat_with_tools(session, tools, query: str):
    """带工具调用的大模型对话"""
    client = AsyncOpenAI()
    
    # 将 MCP 工具转换为 OpenAI 格式
    openai_tools = []
    for tool in tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        })
    
    messages = [{"role": "user", "content": query}]
    
    # 第一轮：让模型决定是否调用工具
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=openai_tools
    )
    
    msg = response.choices[0].message
    
    if msg.tool_calls:
        # 模型决定调用工具
        for tc in msg.tool_calls:
            func_name = tc.function.name
            args = json.loads(tc.function.arguments)
            
            # 通过 MCP session 调用工具
            result = await session.call_tool(func_name, args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result)
            })
        
        # 第二轮：模型根据工具结果生成回答
        response2 = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response2.choices[0].message.content
    
    return msg.content

# 使用
async def main():
    session, tools = await connect_to_server("server.py")
    result = await chat_with_tools(session, tools, "搜索最新的 MCP 协议更新")
    print(result)
    await session.__aexit__(None, None, None)

asyncio.run(main())
```

**核心要点**：
1. 通过 `StdioServerParameters` 启动 MCP Server（子进程）
2. 建立 `ClientSession` 并获取工具列表
3. 将 MCP 工具格式转换为 OpenAI 函数调用格式
4. 模型返回 `tool_calls` 时，通过 `session.call_tool()` 执行
5. 将工具结果作为 `tool` 角色消息返回给模型

## 部署场景

### 场景 1：本地 Claude Desktop

在 Claude Desktop 中使用自定义 MCP Server 只需编辑配置文件：

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "web_search": {
      "command": "uv",
      "args": ["run", "/path/to/server.py"]
    }
  }
}
```

重启 Claude Desktop 后，右下角会出现工具图标，即可在对话中使用。

### 场景 2：云端 SSE 部署

要让 MCP Server 通过 HTTP 远程访问，使用 **SSE（Server-Sent Events）** 传输：

```python
# server_sse.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("web_search", description="网络搜索工具")

# ... 工具定义同上 ...

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8080,
        sse_path="/sse"
    )
```

部署到 **阿里云函数计算 FC 3.0**：

1. 创建 Web 函数，环境 Python 10
2. 添加官方公共层 `mcp`（包含全部依赖）
3. 设置启动命令和监听端口
4. 部署后获得 URL，在任意客户端通过 SSE 配置使用

### 场景 3：LangChain 集成

通过 `langchain-mcp-adapters` 开源项目，可以轻松将 MCP Server 集成到 LangChain 链中：

```python
from langchain_mcp_adapters.client import MultiServerClient

async with MultiServerClient({
    "web_search": {"command": "uv", "args": ["run", "server.py"]}
}) as client:
    tools = client.get_tools()
    # 直接用于 LangChain Agent
    agent = create_agent(model, tools=tools)
```

## 生态系统

MCP 生态已经相当活跃，以下是关键资源：

| 资源 | 用途 |
|------|------|
| [MCP 官方文档](https://modelcontextprotocol.io/) | 完整规范、快速入门、最佳实践 |
| [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | 官方可视化工具，调试 Server |
| [Glama.ai MCP Directory](https://glama.ai/mcp) | 按类别分类的 MCP 工具目录 |
| [Smithery.ai](https://smithery.ai/) | MCP 中介平台，可在线体验 |
| [Cursor MCP Directory](https://cursor.directory/) | Cursor 官方精选 MCP 工具 |
| [langchain-mcp-adapters](https://github.com/langchain-ai/langchain-mcp-adapters) | LangChain 集成适配器 |

## 安全注意事项

MCP 协议本身不提供角色访问控制（RBAC），安全性依赖实现者：

1. **用户授权**：Host 必须在调用任何工具前获得用户明确同意
2. **工具描述不可信**：工具描述（annotations）来自 Server，未经认证不应直接信任
3. **数据隐私**：Host 不得在未获用户同意的情况下将资源数据发送给 Server
4. **Sampling 控制**：用户必须明确批准任何 LLM 采样请求，控制 prompt 内容和结果可见性

社区工具 **MCPSafetyScanner**（[GitHub](https://github.com/johnhalloran321/mcpSafetyScanner)）可以模拟攻击者行为，对 MCP 工具清单进行安全扫描。

## 总结

MCP 协议在短短一年内从概念验证成长为 AI 工具生态的事实标准。它的价值在于：

- **对开发者**：一次编写，所有 AI 客户端可用——像写 LSP 服务器一样简单
- **对用户**：在 Claude、Cursor、Cline 等不同客户端间无缝切换，工具配置不丢失
- **对生态**：打破"烟囱式"集成，让 AI 工具真正可组合

MCP 不是终点，而是 AI 应用从"聊天机器人"走向"操作系统"的关键一步。当每个工具都可以通过标准协议被 AI 调用时，AI 将不再只是一个对话框，而是一个能真正操作你数字世界的智能代理。

---

**参考链接**：
- [MCP 官方规范](https://modelcontextprotocol.io/specification/2025-03-26)
- [Anthropic 发布博客](https://www.anthropic.com/news/model-context-protocol)
- [MCP 中文入门指南](https://github.com/liaokongVFX/MCP-Chinese-Getting-Started-Guide)
- [MCP Inspector 调试工具](https://github.com/modelcontextprotocol/inspector)

# iOS LLM Agent SDK (MALLMKit) Skills 使用文档

[⬆️ 返回首页](../README_zh.md)

## 产品介绍

**高德 iOS LLM Agent SDK Skills**（MALLMKit）是一套专为 AI IDE 设计的 AI 编程技能包。它将高德 MALLMKit SDK（iOS 版）的官方文档、最佳实践和代码模板整合为结构化的技能文件，使 Cursor、Claude、Cline 等 AI Coding 工具能够：

- **精准理解**如何将智能地图服务集成到 iOS 应用中
- **自动生成** Agent 初始化、查询、导航控制和 IPC 通信代码
- **主动避免**常见的授权失败和连接管理等集成问题
- **提供**经过验证的 Agent SDK 和 Link SDK 功能代码示例

## 产品特点

### 智能地图服务

支持自然语言查询路线规划、POI 搜索、导航控制等功能。用户可以使用自然语言与地图交互，如"去西藏"、"附近的肯德基"。

### 双 SDK 架构

包含 Agent SDK（AI Agent驱动的地图交互）和 Link SDK（与高德 APP 进行通信），提供全面的集成能力。

### 完整的导航控制

完整的导航生命周期管理，包括开始/停止导航、路线切换、播报模式控制和实时导航数据监听。

### IPC 通信

与高德 APP 的健壮 IPC 通信框架，支持授权认证、连接管理、数据传输和导航命令。

## 能力介绍

### Agent SDK

| **能力** | **说明** |
| --- | --- |
| 智能查询 | 自然语言查询路线、POI、导航 |
| 查询结果处理 | 处理 AI 返回的结构化数据 |
| 导航控制 | 开始/停止导航、切换路线、播报模式 |
| 导航数据监听 | 实时导航数据回调 |
| 出行方式 | 导航环境与路线偏好配置 |
| 生命周期管理 | 场景管理、状态重置、内存管理 |

### Link SDK

| **能力** | **说明** |
| --- | --- |
| 认证管理 | 通过 AMapAuthorizationManager 完成授权流程与回调处理 |
| 连接管理 | 通过 AMapLinkManager 建立连接、状态监听、自动重连 |
| 数据传输 | 发送数据、导航命令（途经点/目的地/播报/开始导航） |
| 导航命令 | 途经点/目的地设置、播报控制、导航启动 |

### 参考资料

| **能力** | **说明** |
| --- | --- |
| Agent 核心类 | Agent SDK 公共类与枚举速查 |
| Link 核心类 | Link SDK 公共类速查 |
| Link 错误码 | Link SDK 错误码速查 |
| 语音指令 | 支持的自然语言指令示例 |
| 问题排查 | 错误码与常见问题解决 |

## 快速接入

### 第一步：在 Cursor 中配置 Skill

```bash
# 将 iOS LLM Agent Skill 链接到您的项目
ln -s /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/ios-llm-agent-sdk
```

### 第二步：验证配置

打开 Cursor AI Chat，输入：

**Agent SDK 测试：**
```text
帮我将 MALLMKit SDK 集成到 iOS 应用中，实现一个自然语言地图查询
```

**Link SDK 测试：**
```text
帮我使用 Link SDK 建立与高德 APP 的 IPC 通信，包括授权和连接管理
```

如果 AI 能够正确引用 Skill 文件并生成完整的集成代码，说明 Skill 已成功加载。

### 第三步：选择集成路径

- **Agent SDK**：AI 驱动的地图交互 → 从 [快速开始](api/quick-start.md) 或 [接入 Agent](api/integrate-agent.md) 开始
- **Link SDK**：与高德 APP 的 IPC 通信 → 从 [Link 快速开始](api/link-quick-start.md) 开始

## 使用示例

### 示例 1：Agent 初始化

```text
在 iOS 应用中初始化 MALLMKit Agent SDK，注册导航命令并设置查询回调
```

### 示例 2：自然语言查询

```text
发送自然语言查询"找到最近的加油站并导航过去"，并处理路径规划结果
```

### 示例 3：导航控制

```text
实现导航控制功能，包括开始/停止、路线切换和实时导航数据展示
```

### 示例 4：Link SDK 集成

```text
配置 Link SDK 与高德 APP 通信，实现授权流程、建立连接并发送导航命令
```

## 目录结构

```text
ios-llm-agent-sdk/
├── SKILL.md                        # 技能主文件（AI 入口）
├── api/                            # API 使用指南
│   ├── quick-start.md              # Agent SDK 快速开始
│   ├── integrate-agent.md          # 完整 Agent 集成流程
│   ├── agent-query.md              # 自然语言查询
│   ├── query-result.md             # 查询结果处理
│   ├── navi-control.md             # 导航控制
│   ├── navi-data-listener.md       # 导航数据监听
│   ├── transport-mode.md           # 出行方式配置
│   ├── link-quick-start.md         # Link SDK 快速开始
│   ├── link-client.md              # LinkClient 管理
│   ├── authorization.md            # 认证管理
│   ├── connection.md               # 连接管理
│   ├── data-transfer.md            # 数据传输与命令
│   ├── logger.md                   # 日志配置
│   └── lifecycle.md                # 生命周期管理
└── references/                     # 参考资料
    ├── core-classes.md             # Agent SDK 核心类
    ├── link-core-classes.md        # Link SDK 核心类
    ├── link-error-codes.md         # Link SDK 错误码
    ├── troubleshooting.md          # 问题排查指南
    └── voice-commands.md           # 语音指令示例
```

## 常见问题

### Q：Agent 查询无返回结果

**A：** 请检查：
1. Agent SDK 是否使用正确的 API Key 初始化
2. 网络连接是否正常
3. 查询格式是否符合支持的模式（参见 [语音指令](references/voice-commands.md)）

### Q：Link SDK 授权失败

**A：** 请确保：
1. 设备上已安装高德 APP
2. 授权配置正确
3. 查看 [Link 错误码](references/link-error-codes.md) 中的错误码说明

### Q：导航数据监听未收到回调

**A：** 请验证：
1. 导航是否已正确启动
2. 数据监听是否在导航启动前注册
3. 定位权限是否已授予

### Q：与高德 APP 的连接频繁断开

**A：** 请检查：
1. AMapLinkManager 是否启用了自动重连
2. 两个应用是否在前台或启用了后台模式
3. 检查连接状态监听的实现

## 相关链接

- [高德开放平台控制台](https://console.amap.com/)
- [Cursor 官方文档](https://docs.cursor.com/)
- [⬆️ 返回首页](../README_zh.md)

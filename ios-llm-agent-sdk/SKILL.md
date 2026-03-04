# MALLMKit SDK Skill

高德地图 MALLMKit SDK 集成技能，支持自然语言查询、路线规划、POI搜索、导航控制等智能地图服务，以及与高德地图 APP 的 IPC 通信（授权认证、建联、收发数据）。

## 适用场景

- 集成高德智能语音助手到 iOS 应用
- 实现自然语言驱动的地图交互（如"去西藏"、"附近的肯德基"）
- 导航控制与数据监听
- 合作方 APP 与高德地图 APP 建立 IPC 通信链路，收发数据

## 触发词

| 触发词 | 文档 | 说明 |
|--------|------|------|
| **接入LLM Agent SDK** | [接入 Agent](api/integrate-agent.md) | Agent 初始化、命令注册、查询调用完整流程 |
| **链接高德app** | [链接高德 APP](api/link-quick-start.md) | Link 页面创建、授权认证、建联、导航命令收发完整流程 |

> 💡 别名：说"接入agent"或"接入agent sdk"也会匹配到"接入LLM Agent SDK"触发词。
> 💡 别名：说"连接高德app"、"接入linkKit"、"IPC通信"、"与高德APP通信"也会匹配到"链接高德app"触发词。

## 快速开始

- Agent SDK 首次接入请阅读：[快速集成指南](api/quick-start.md)
- Link SDK 首次接入请阅读：[Link 快速集成指南](api/link-quick-start.md)

## API 文档 — Agent SDK（按需查阅）

| 文档 | 说明 |
|------|------|
| [智能查询](api/agent-query.md) | 发起自然语言查询、多轮对话 |
| [查询结果处理](api/query-result.md) | 处理路线、POI、导航等查询结果 |
| [导航控制](api/navi-control.md) | 开始/停止导航、切换路线、播报模式 |
| [导航数据监听](api/navi-data-listener.md) | 实时监听导航数据回调 |
| [出行方式配置](api/transport-mode.md) | 导航环境、路线偏好、家/公司位置 |
| [IPC链路管理](api/link-client.md) | APP链路模式的建联与授权 |
| [生命周期管理](api/lifecycle.md) | 场景管理、状态重置、内存管理 |
| [日志管理](api/logger.md) | SDK 内部日志监听 |

## API 文档 — Link SDK（按需查阅）

| 文档 | 说明 |
|------|------|
| [认证管理](api/authorization.md) | 通过 AMapAuthorizationManager 完成授权流程与回调处理 |
| [连接管理](api/connection.md) | 通过 AMapLinkManager 建立连接、状态监听、自动重连、断开连接 |
| [数据传输与命令](api/data-transfer.md) | 发送数据、导航命令（途经点/目的地/播报/开始导航）、数据监听 |

## 参考文档（深入查阅）

| 文档 | 说明 |
|------|------|
| [Agent 核心类参考](references/core-classes.md) | Agent SDK 公共类与枚举速查 |
| [常见问题排查](references/troubleshooting.md) | 错误码与常见问题解决 |
| [语音指令参考](references/voice-commands.md) | 支持的自然语言指令示例 |
| [Link 核心类参考](references/link-core-classes.md) | Link SDK 公共类速查 |
| [Link 错误码参考](references/link-error-codes.md) | Link SDK 错误码速查 |

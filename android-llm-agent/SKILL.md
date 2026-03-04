# AMap LLM Agent SDK Skills

AMap LLM Agent SDK 是高德地图 AI 智能助手 SDK，支持自然语言交互的地图导航服务。

## 触发词

- "接入LLM Agent SDK"、"集成AI助手"、"接入Agent"
- "连接高德APP"、"配置LinkClient"

## 目录结构

```
amap-llm-agent/
├── SKILL.md                    # 本文件 - 入口索引
├── api/                        # API 使用指南
│   ├── quick-start.md          # 快速接入（3步完成）
│   ├── agent-query.md          # 发送 AI 查询
│   ├── query-result.md         # 处理查询结果
│   ├── link-client.md          # LinkClient 与高德APP通信
│   ├── transport-mode.md       # 切换导航模式
│   ├── logger.md               # 日志配置
│   └── lifecycle.md            # 生命周期管理
└── references/                 # 参考资料
    ├── voice-commands.md       # 支持的语音指令
    ├── troubleshooting.md      # 常见问题诊断
    └── core-classes.md         # 核心类说明
```

## 快速导航

| 需求 | 参考文档 |
|-----|---------|
| 首次接入 SDK | [api/quick-start.md](api/quick-start.md) |
| 发送语音/文字查询 | [api/agent-query.md](api/agent-query.md) |
| 处理 AI 返回结果 | [api/query-result.md](api/query-result.md) |
| 与高德 APP 联动 | [api/link-client.md](api/link-client.md) |
| 切换驾车/骑行/步行 | [api/transport-mode.md](api/transport-mode.md) |
| 查看支持的语音指令 | [references/voice-commands.md](references/voice-commands.md) |
| 排查问题 | [references/troubleshooting.md](references/troubleshooting.md) |

## 依赖版本

```gradle
// LLM Agent SDK
implementation 'com.amap.lbs.client:amap-agent:1.1.41'

// 导航 SDK（必须）
implementation 'com.amap.api:navi-3dmap:latest.integration'

// 定位 SDK（必须，用于实时位置更新）
implementation 'com.amap.api:location:latest.integration'
```

> ⚠️ **注意**：如果 Agent SDK 或导航 SDK 依赖有问题（如无法下载、版本冲突等），请联系高德相关同学获取依赖包。

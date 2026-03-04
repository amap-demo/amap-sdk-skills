# Android LLM Agent SDK Skills 使用文档

[⬆️ 返回首页](../README_zh.md)

## 产品介绍

**高德 Android LLM Agent SDK Skills** 是一套专为 AI IDE 设计的 AI 编程技能包。它将高德 LLM Agent SDK（Android 版）的官方文档、最佳实践和代码模板整合为结构化的技能文件，使 Cursor、Claude、Cline 等 AI Coding 工具能够：

- **精准理解**如何将 AI 智能导航助手集成到 Android 应用中
- **自动生成** SDK 初始化、查询和导航控制代码
- **主动避免**常见的依赖冲突和生命周期管理等集成问题
- **提供**经过验证的自然语言地图交互代码示例

## 产品特点

### AI 智能导航

支持自然语言交互的地图导航服务，用户可以通过语音或文字指令控制地图，如"导航到最近的加油站"。

### 无缝高德 APP 联动

内置 LinkClient 支持，可与高德 APP 通信，实现跨应用导航和数据共享。

### 多出行方式

支持驾车、步行、骑行模式切换，配合 AI 驱动的路径规划。

### 完整的生命周期管理

全面的生命周期管理指南，覆盖初始化、场景管理、状态重置和内存清理。

## 能力介绍

### 核心功能

| **能力** | **说明** |
| --- | --- |
| 自然语言查询 | 发送语音/文字查询进行智能地图交互 |
| 查询结果处理 | 处理 AI 返回的路线、POI 和导航数据 |
| 导航控制 | 开始/停止导航、切换路线 |
| LinkClient | 与高德 APP 通信实现跨应用功能 |

### 配置

| **能力** | **说明** |
| --- | --- |
| 出行方式 | 驾车、步行、骑行 |
| 日志配置 | SDK 内部日志配置 |
| 生命周期 | 场景管理、状态重置、内存清理 |

### 参考资料

| **能力** | **说明** |
| --- | --- |
| 语音指令 | 支持的自然语言指令示例 |
| 核心类 | 公共类与枚举速查 |
| 问题排查 | 错误码与常见问题解决 |

## 快速接入

### 第一步：在 Cursor 中配置 Skill

```bash
# 将 Android LLM Agent Skill 链接到您的项目
ln -s /path/to/open_sdk_skills/android-llm-agent .cursor/skills/android-llm-agent
```

### 第二步：添加依赖

```gradle
// LLM Agent SDK
implementation 'com.amap.lbs.client:amap-agent:1.1.41'

// 导航 SDK（必须）
implementation 'com.amap.api:navi-3dmap:latest.integration'

// 定位 SDK（必须，用于实时位置更新）
implementation 'com.amap.api:location:latest.integration'
```

### 第三步：验证配置

打开 Cursor AI Chat，输入：

```text
帮我将高德 LLM Agent SDK 集成到 Android 应用中，发送一个自然语言查询搜索附近的餐厅
```

如果 AI 能够正确引用 Skill 文件并生成完整的集成代码，说明 Skill 已成功加载。

## 使用示例

### 示例 1：SDK 初始化

```text
在 Android Application 类中初始化高德 LLM Agent SDK，并做好生命周期管理
```

### 示例 2：自然语言查询

```text
发送自然语言查询"导航到北京首都机场"，并处理路径规划结果
```

### 示例 3：LinkClient 集成

```text
配置 LinkClient 与高德 APP 通信，实现跨应用导航
```

### 示例 4：出行方式切换

```text
实现一个出行方式选择器，允许用户在驾车、步行、骑行之间切换
```

## 目录结构

```text
android-llm-agent/
├── SKILL.md                    # 技能主文件（AI 入口）
├── api/                        # API 使用指南
│   ├── quick-start.md          # 快速接入指南
│   ├── agent-query.md          # 发送 AI 查询
│   ├── query-result.md         # 处理查询结果
│   ├── link-client.md          # LinkClient 通信
│   ├── transport-mode.md       # 出行方式切换
│   ├── logger.md               # 日志配置
│   └── lifecycle.md            # 生命周期管理
└── references/                 # 参考资料
    ├── core-classes.md         # 核心类参考
    ├── troubleshooting.md      # 问题排查指南
    └── voice-commands.md       # 语音指令示例
```

## 常见问题

### Q：Agent SDK 依赖无法下载

**A：** 如果 Agent SDK 或导航 SDK 依赖有问题（如无法下载、版本冲突等），请联系高德相关同学获取依赖包。

### Q：自然语言查询无返回结果

**A：** 请检查：
1. SDK 是否正确初始化
2. 网络连接是否正常
3. API Key 是否正确配置

### Q：LinkClient 连接失败

**A：** 请确保：
1. 设备上已安装高德 APP
2. LinkClient 配置正确
3. 已授予所需权限

## 相关链接

- [高德开放平台控制台](https://console.amap.com/)
- [Cursor 官方文档](https://docs.cursor.com/)
- [⬆️ 返回首页](../README_zh.md)

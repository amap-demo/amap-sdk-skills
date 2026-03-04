# AMap SDK Skills 使用文档

## 产品介绍

**AMap SDK Skills** 是一套专为 AI IDE 设计的 AI 编程技能包合集。它将多个高德地图 SDK 的官方文档、最佳实践和代码模板整合为结构化的技能文件，使 Cursor、Claude、Cline 等 AI Coding 工具能够：

- **精准理解**高德地图各平台 SDK 的使用方法
- **自动生成**符合官方规范的 SDK 集成代码
- **主动避免**常见的开发陷阱和兼容性问题
- **提供**经过验证的完整代码示例和最佳实践

无论您是在 RTOS 设备上集成地图能力，还是在 Android/iOS 上构建 AI 驱动的导航助手，这套 Skills 都能显著提升您的开发效率。

## 包含的 Skills

本仓库包含三个独立的 Skill 技能包，分别对应不同的高德地图功能 SDK：

| Skill | 平台 | 说明 | 文档 |
| --- | --- | --- | --- |
| **RTOS 地图 SDK** | RTOS | 面向智能眼镜、智能手表等 RTOS 设备的轻量级地图 SDK，支持栅格/矢量地图渲染与轨迹导航 | [📖 详情](./RTOS/README_zh.md) |
| **Android LLM Agent SDK** | Android | AI 智能导航助手 Android版SDK，支持自然语言交互的地图导航服务 | [📖 详情](./android-llm-agent/README_zh.md) |
| **iOS LLM Agent SDK** | iOS | AI 智能导航助手 iOS版SDK，支持自然语言交互的地图导航服务 | [📖 详情](./ios-llm-agent-sdk/README_zh.md) |

## 产品特点

### 多平台覆盖

覆盖 RTOS 嵌入式设备、Android 和 iOS 平台，为高德地图 SDK 在主流平台的集成提供全面的 AI 编程辅助。

### 模块化设计

每个 Skill 按功能模块组织文档（初始化、地图操作、导航、覆盖物等），AI 可按需引用，精准回答您的问题。

### 安全与最佳实践

内置安全配置指南和最佳实践，帮助开发者避免常见的鉴权问题、内存泄漏和线程安全等陷阱。

### 代码可验证

所有代码示例均经过实际 SDK API 验证，AI 会自我校验生成代码的可用性，确保输出可以正确编译和运行。

## 能力介绍

### RTOS 地图 SDK

| **能力** | **说明** |
| --- | --- |
| 地图渲染 | 栅格/矢量地图显示、缩放、旋转 |
| 覆盖物 | 点/线/面标注 |
| 轨迹导航 | 实时导航数据展示 |
| 离线地图 | 离线数据下载与使用 |
| 平台适配器 | 内存、文件、网络、渲染、线程适配器 |

### Android LLM Agent SDK

| **能力** | **说明** |
| --- | --- |
| 自然语言查询 | 语音/文字智能地图交互 |
| 路径规划 | AI 驱动的多出行方式路径规划 |
| 导航控制 | 开始/停止导航、路线切换 |
| LinkClient | 与高德 APP 通信 |
| 出行方式 | 驾车、步行、骑行 |

### iOS LLM Agent SDK (MALLMKit)

| **能力** | **说明** |
| --- | --- |
| 自然语言查询 | 语音/文字智能地图交互 |
| 路径规划 | AI 驱动的多出行方式路径规划 |
| 导航控制 | 开始/停止导航、路线切换 |
| IPCLink | 与高德 APP 通信 |
| 出行方式 | 驾车、步行、骑行 |

## 快速接入

### 第一步：获取 Skills 文件

#### 方式一：Git Clone（推荐）

```bash
# 克隆仓库到本地
git clone <repository-url>

# 进入目录
cd open_sdk_skills
```

#### 方式二：直接下载

从 Releases 页面下载最新版本的压缩包并解压。

### 第二步：在 Cursor 中配置 Skill

Cursor 支持通过 `.cursor/skills/` 目录加载自定义技能。

#### 2.1 创建 Skills 目录

在您的项目根目录下创建 `.cursor/skills/` 文件夹：

```bash
mkdir -p .cursor/skills
```

#### 2.2 链接或复制 Skill 文件

**方式一：软链接（推荐，方便更新）**

```bash
# macOS / Linux - 链接您需要的 Skill
ln -s /path/to/open_sdk_skills/RTOS .cursor/skills/RTOS
ln -s /path/to/open_sdk_skills/android-llm-agent .cursor/skills/android-llm-agent
ln -s /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/ios-llm-agent-sdk

# Windows（以管理员身份运行 CMD）
mklink /D .cursor\skills\RTOS C:\path\to\open_sdk_skills\RTOS
mklink /D .cursor\skills\android-llm-agent C:\path\to\open_sdk_skills\android-llm-agent
mklink /D .cursor\skills\ios-llm-agent-sdk C:\path\to\open_sdk_skills\ios-llm-agent-sdk
```

**方式二：直接复制**

```bash
# 复制您需要的 Skill
cp -r /path/to/open_sdk_skills/RTOS .cursor/skills/
cp -r /path/to/open_sdk_skills/android-llm-agent .cursor/skills/
cp -r /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/
```

#### 2.3 项目目录结构

配置完成后，您的项目目录结构应该类似：

```text
your-project/
├── .cursor/
│   └── skills/
│       ├── RTOS/                       # RTOS 地图 SDK Skill
│       │   ├── SKILL.md
│       │   ├── api/
│       │   └── references/
│       ├── android-llm-agent/          # Android LLM Agent Skill
│       │   ├── SKILL.md
│       │   ├── api/
│       │   └── references/
│       └── ios-llm-agent-sdk/          # iOS LLM Agent Skill
│           ├── SKILL.md
│           ├── api/
│           └── references/
├── src/
└── ...
```

### 第三步：验证配置

1. 打开 Cursor IDE
2. 打开您的项目
3. 按 `Cmd/Ctrl + L` 打开 AI Chat
4. 根据您配置的 Skill 输入测试问题：

**RTOS 测试：**
```text
帮我初始化 WatchSDK 并在 RTOS 设备上创建一个地图视图
```

**Android LLM Agent 测试：**
```text
帮我集成高德 LLM Agent SDK，发送一个自然语言导航查询
```

**iOS LLM Agent 测试：**
```text
帮我集成 LLM Agent SDK，发送一个自然语言导航查询
```

如果 AI 在思考过程中能够正确引用 Skill 文件并生成完整的、符合规范的代码，说明 Skill 已成功加载。

## 目录结构

```text
open_sdk_skills/
├── RTOS/                               # RTOS 地图 SDK Skill
│   ├── SKILL.md                        # 技能主文件（AI 入口）
│   ├── api/                            # API 使用指南
│   │   ├── quick-start.md              # 快速开始
│   │   ├── ios-integration.md          # iOS 集成指南
│   │   ├── ios-demo-guide.md           # iOS Demo 指南
│   │   ├── lifecycle.md                # 生命周期管理
│   │   ├── adapters.md                 # 适配器实现
│   │   ├── map-operations.md           # 地图操作
│   │   ├── overlays.md                 # 覆盖物管理
│   │   └── navigation.md              # 导航
│   └── references/                     # 参考资料
│       ├── adapter-requirements.md     # 适配器必需函数
│       ├── core-types.md               # 核心类型定义
│       ├── error-codes.md              # 错误码
│       └── troubleshooting.md          # 常见问题
├── android-llm-agent/                  # Android LLM Agent SDK Skill
│   ├── SKILL.md                        # 技能主文件（AI 入口）
│   ├── api/                            # API 使用指南
│   │   ├── quick-start.md              # 快速开始
│   │   ├── agent-query.md              # AI 查询
│   │   ├── query-result.md             # 查询结果处理
│   │   ├── link-client.md              # LinkClient 通信
│   │   ├── transport-mode.md           # 出行方式
│   │   ├── logger.md                   # 日志配置
│   │   └── lifecycle.md                # 生命周期管理
│   └── references/                     # 参考资料
│       ├── core-classes.md             # 核心类
│       ├── troubleshooting.md          # 常见问题
│       └── voice-commands.md           # 语音指令
└── ios-llm-agent-sdk/                  # iOS LLM Agent SDK Skill
    ├── SKILL.md                        # 技能主文件（AI 入口）
    ├── api/                            # API 使用指南
    │   ├── quick-start.md              # 快速开始
    │   ├── integrate-agent.md          # Agent 集成
    │   ├── agent-query.md              # AI 查询
    │   ├── query-result.md             # 查询结果处理
    │   ├── navi-control.md             # 导航控制
    │   ├── navi-data-listener.md       # 导航数据监听
    │   ├── link-client.md              # LinkClient 通信
    │   ├── link-quick-start.md         # Link 快速开始
    │   ├── authorization.md            # 认证管理
    │   ├── connection.md               # 连接管理
    │   ├── data-transfer.md            # 数据传输
    │   ├── transport-mode.md           # 出行方式
    │   ├── logger.md                   # 日志配置
    │   └── lifecycle.md                # 生命周期管理
    └── references/                     # 参考资料
        ├── core-classes.md             # 核心类
        ├── link-core-classes.md        # Link 核心类
        ├── link-error-codes.md         # Link 错误码
        ├── troubleshooting.md          # 常见问题
        └── voice-commands.md           # 语音指令
```

## 常见问题

### Q：我应该使用哪个 Skill？

**A：** 根据您的目标平台选择：
- **RTOS 设备**（智能眼镜、智能手表）：使用 `RTOS` Skill
- **Android 应用** AI 导航：使用 `android-llm-agent` Skill
- **iOS 应用** AI 导航：使用 `ios-llm-agent-sdk` Skill

### Q：可以同时使用多个 Skill 吗？

**A：** 可以！您可以同时将多个 Skill 目录链接到 `.cursor/skills/` 中。Cursor AI 会根据您的问题自动引用相关的 Skill。

### Q：Cursor AI 没有使用 Skill 中的知识

**A：** 请确保：
1. Skill 文件放置在 `.cursor/skills/` 目录下
2. `SKILL.md` 文件存在且格式正确
3. 尝试在提问时明确提及 SDK 名称（如"WatchSDK"、"LLM Agent"、"MALLMKit"）

### Q：如何更新 Skill？

**A：** 如果使用软链接方式，只需拉取仓库的最新更改即可。如果使用复制方式，需要重新复制最新文件。

## 相关链接

- [高德开放平台控制台](https://console.amap.com/)
- [Cursor 官方文档](https://docs.cursor.com/)

**让 AI 成为您的高德 SDK 开发助手，从今天开始！**

# AMap SDK Skills User Guide

[🇨🇳 中文文档](./README_zh.md)

## Product Introduction

**AMap SDK Skills** is a collection of AI programming skill packages designed for AI IDEs. It integrates the official documentation, best practices, and code templates of multiple AMap SDKs into structured skill files, enabling AI coding tools like Cursor, Claude, and Cline to:

- **Accurately understand** how to use AMap SDKs across different platforms
- **Automatically generate** SDK integration code that complies with official specifications
- **Proactively avoid** common development pitfalls and compatibility issues
- **Provide** verified complete code examples and best practices

Whether you're integrating map capabilities into RTOS devices, or building AI-powered navigation assistants on Android/iOS, these Skills can significantly improve your development efficiency.

## Included Skills

This repository contains three independent Skill packages for different AMap functional SDKs:

| Skill | Platform | Description | Documentation |
| --- | --- | --- | --- |
| **RTOS Map SDK** | RTOS | Lightweight map SDK for smart glasses, smart watches and other RTOS devices, supporting raster/vector map rendering and track navigation | [📖 Details](./RTOS/README.md) |
| **Android LLM Agent SDK** | Android | AI-powered navigation assistant SDK for Android, supporting natural language interaction for map and navigation services | [📖 Details](./android-llm-agent/README.md) |
| **iOS LLM Agent SDK** | iOS | AI-powered navigation assistant SDK for iOS, supporting natural language interaction for map and navigation services | [📖 Details](./ios-llm-agent-sdk/README.md) |

## Product Features

### Multi-Platform Coverage

Covers RTOS embedded devices, Android, and iOS platforms, providing comprehensive AI programming assistance for AMap SDK integration across major platforms.

### Modular Design

Each Skill is organized by functional modules (initialization, map operations, navigation, overlays, etc.), allowing AI to reference as needed and accurately answer your questions.

### Security & Best Practices

Built-in security configuration guides and best practices to help developers avoid common pitfalls such as authentication issues, memory leaks, and thread safety problems.

### Verifiable Code

All code examples have been verified against actual SDK APIs. AI will self-validate the usability of generated code to ensure the output compiles and runs correctly.

## Capabilities Overview

### RTOS Map SDK

| **Capability** | **Description** |
| --- | --- |
| Map Rendering | Raster/vector map display, zoom, rotation |
| Overlays | Point, polyline, polygon annotations |
| Track Navigation | Real-time navigation data display |
| Offline Maps | Offline data download and usage |
| Platform Adapters | Memory, file, network, render, thread adapters |

### Android LLM Agent SDK

| **Capability** | **Description** |
| --- | --- |
| Natural Language Query | Voice/text-based intelligent map interaction |
| Route Planning | AI-driven route planning with multi-transport modes |
| Navigation Control | Start/stop navigation, route switching |
| LinkClient | Communication with AMap APP |
| Transport Mode | Switch between driving, walking, cycling |

### iOS LLM Agent SDK (MALLMKit)

| **Capability** | **Description** |
| --- | --- |
| Natural Language Query | Voice/text-based intelligent map interaction |
| Route Planning | AI-driven route planning with multi-transport modes |
| Navigation Control | Start/stop navigation, route switching |
| IPCLink | Communication with AMap APP |
| Transport Mode | Switch between driving, walking, cycling |

## Quick Start

### Step 1: Get Skills Files

#### Option 1: Git Clone (Recommended)

```bash
# Clone the repository locally
git clone <repository-url>

# Enter the directory
cd open_sdk_skills
```

#### Option 2: Direct Download

Download the latest version archive from the Releases page and extract it.

### Step 2: Configure Skill in Cursor

Cursor supports loading custom skills through the `.cursor/skills/` directory.

#### 2.1 Create Skills Directory

Create the `.cursor/skills/` folder in your project root directory:

```bash
mkdir -p .cursor/skills
```

#### 2.2 Link or Copy Skill Files

**Option 1: Symbolic Link (Recommended for easy updates)**

```bash
# macOS / Linux - Link the specific skill you need
ln -s /path/to/open_sdk_skills/RTOS .cursor/skills/RTOS
ln -s /path/to/open_sdk_skills/android-llm-agent .cursor/skills/android-llm-agent
ln -s /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/ios-llm-agent-sdk

# Windows (Run CMD as Administrator)
mklink /D .cursor\skills\RTOS C:\path\to\open_sdk_skills\RTOS
mklink /D .cursor\skills\android-llm-agent C:\path\to\open_sdk_skills\android-llm-agent
mklink /D .cursor\skills\ios-llm-agent-sdk C:\path\to\open_sdk_skills\ios-llm-agent-sdk
```

**Option 2: Direct Copy**

```bash
# Copy the specific skill you need
cp -r /path/to/open_sdk_skills/RTOS .cursor/skills/
cp -r /path/to/open_sdk_skills/android-llm-agent .cursor/skills/
cp -r /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/
```

#### 2.3 Project Directory Structure

After configuration, your project directory structure should look like:

```text
your-project/
├── .cursor/
│   └── skills/
│       ├── RTOS/                       # RTOS Map SDK Skill
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

### Step 3: Verify Configuration

1. Open Cursor IDE
2. Open your project
3. Press `Cmd/Ctrl + L` to open AI Chat
4. Enter a test question based on the Skill you configured:

**For RTOS:**
```text
Help me initialize the WatchSDK and create a map view on an RTOS device
```

**For Android LLM Agent:**
```text
Help me integrate the AMap LLM Agent SDK and send a natural language navigation query
```

**For iOS LLM Agent:**
```text
Help me integrate the LLM Agent SDK and send a natural language navigation query
```

If AI correctly references the Skill files during the thinking process and generates complete, specification-compliant code, the Skill has been successfully loaded.

## Directory Structure

```text
open_sdk_skills/
├── RTOS/                               # RTOS Map SDK Skill
│   ├── SKILL.md                        # Main skill file (AI entry point)
│   ├── api/                            # API guides
│   │   ├── quick-start.md              # Quick start guide
│   │   ├── ios-integration.md          # iOS integration guide
│   │   ├── ios-demo-guide.md           # iOS demo guide
│   │   ├── lifecycle.md                # Lifecycle management
│   │   ├── adapters.md                 # Adapter implementation
│   │   ├── map-operations.md           # Map operations
│   │   ├── overlays.md                 # Overlay management
│   │   └── navigation.md              # Navigation
│   └── references/                     # Reference documentation
│       ├── adapter-requirements.md     # Adapter requirements
│       ├── core-types.md               # Core type definitions
│       ├── error-codes.md              # Error codes
│       └── troubleshooting.md          # Troubleshooting
├── android-llm-agent/                  # Android LLM Agent SDK Skill
│   ├── SKILL.md                        # Main skill file (AI entry point)
│   ├── api/                            # API guides
│   │   ├── quick-start.md              # Quick start guide
│   │   ├── agent-query.md              # AI query
│   │   ├── query-result.md             # Query result handling
│   │   ├── link-client.md              # LinkClient communication
│   │   ├── transport-mode.md           # Transport mode
│   │   ├── logger.md                   # Logger configuration
│   │   └── lifecycle.md                # Lifecycle management
│   └── references/                     # Reference documentation
│       ├── core-classes.md             # Core classes
│       ├── troubleshooting.md          # Troubleshooting
│       └── voice-commands.md           # Voice commands
└── ios-llm-agent-sdk/                  # iOS LLM Agent SDK Skill
    ├── SKILL.md                        # Main skill file (AI entry point)
    ├── api/                            # API guides
    │   ├── quick-start.md              # Quick start guide
    │   ├── integrate-agent.md          # Agent integration
    │   ├── agent-query.md              # AI query
    │   ├── query-result.md             # Query result handling
    │   ├── navi-control.md             # Navigation control
    │   ├── navi-data-listener.md       # Navigation data listener
    │   ├── link-client.md              # LinkClient communication
    │   ├── link-quick-start.md         # Link quick start
    │   ├── authorization.md            # Authorization
    │   ├── connection.md               # Connection management
    │   ├── data-transfer.md            # Data transfer
    │   ├── transport-mode.md           # Transport mode
    │   ├── logger.md                   # Logger configuration
    │   └── lifecycle.md                # Lifecycle management
    └── references/                     # Reference documentation
        ├── core-classes.md             # Core classes
        ├── link-core-classes.md        # Link core classes
        ├── link-error-codes.md         # Link error codes
        ├── troubleshooting.md          # Troubleshooting
        └── voice-commands.md           # Voice commands
```

## FAQ

### Q: Which Skill should I use?

**A:** Choose based on your target platform:
- **RTOS devices** (smart glasses, smart watches): Use the `RTOS` Skill
- **Android apps** with AI navigation: Use the `android-llm-agent` Skill
- **iOS apps** with AI navigation: Use the `ios-llm-agent-sdk` Skill

### Q: Can I use multiple Skills at the same time?

**A:** Yes! You can link multiple Skill directories into `.cursor/skills/` simultaneously. Cursor AI will automatically reference the relevant Skill based on your questions.

### Q: Cursor AI doesn't use knowledge from Skill

**A:** Please ensure:
1. Skill files are placed in the `.cursor/skills/` directory
2. `SKILL.md` file exists and is correctly formatted
3. Try explicitly mentioning the SDK name in your questions (e.g., "WatchSDK", "LLM Agent", "MALLMKit")

### Q: How to update Skills?

**A:** If using symbolic links, simply pull the latest changes from the repository. If using the copy method, re-copy the latest files.

## Related Links

- [AMap Open Platform Console](https://console.amap.com/)
- [Cursor Official Documentation](https://docs.cursor.com/)

**Let AI become your AMap SDK development assistant, starting today!**





# Android LLM Agent SDK Skills User Guide

[🇨🇳 中文文档](./README_zh.md) | [⬆️ Back to Home](../README.md)

## Product Introduction

**AMap Android LLM Agent SDK Skills** is an AI programming skill package designed for AI IDEs. It integrates the official documentation, best practices, and code templates of the AMap LLM Agent SDK for Android into structured skill files, enabling AI coding tools like Cursor, Claude, and Cline to:

- **Accurately understand** how to integrate the AI-powered navigation assistant into Android apps
- **Automatically generate** SDK initialization, query, and navigation control code
- **Proactively avoid** common integration issues such as dependency conflicts and lifecycle management
- **Provide** verified code examples for natural language map interactions

## Product Features

### AI-Powered Navigation

Enables natural language interaction for map and navigation services, allowing users to control maps through voice or text commands like "Navigate to the nearest gas station".

### Seamless AMap APP Integration

Built-in LinkClient support for communication with the AMap APP, enabling cross-app navigation and data sharing.

### Multi-Transport Mode

Supports switching between driving, walking, and cycling modes with AI-driven route planning.

### Complete Lifecycle Management

Comprehensive lifecycle management guide covering initialization, scene management, state reset, and memory cleanup.

## Capabilities

### Core Features

| **Capability** | **Description** |
| --- | --- |
| Natural Language Query | Send voice/text queries for intelligent map interaction |
| Query Result Handling | Process AI responses including routes, POIs, and navigation data |
| Navigation Control | Start/stop navigation, switch routes |
| LinkClient | Communicate with AMap APP for cross-app features |

### Configuration

| **Capability** | **Description** |
| --- | --- |
| Transport Mode | Switch between driving, walking, cycling |
| Logger | Configure SDK internal logging |
| Lifecycle | Scene management, state reset, memory cleanup |

### Reference

| **Capability** | **Description** |
| --- | --- |
| Voice Commands | Supported natural language command examples |
| Core Classes | Public classes and enum reference |
| Troubleshooting | Error codes and common issue resolution |

## Quick Start

### Step 1: Configure Skill in Cursor

```bash
# Link the Android LLM Agent skill to your project
ln -s /path/to/open_sdk_skills/android-llm-agent .cursor/skills/android-llm-agent
```

### Step 2: Add Dependencies

```gradle
// LLM Agent SDK
implementation 'com.amap.lbs.client:amap-agent:1.1.41'

// Navigation SDK (Required)
implementation 'com.amap.api:navi-3dmap:latest.integration'

// Location SDK (Required)
implementation 'com.amap.api:location:latest.integration'
```

### Step 3: Verify Configuration

Open Cursor AI Chat and enter:

```text
Help me integrate the AMap LLM Agent SDK into my Android app and send a natural language query to search for nearby restaurants
```

If AI correctly references the Skill files and generates complete integration code, the Skill has been successfully loaded.

## Usage Examples

### Example 1: SDK Initialization

```text
Initialize the AMap LLM Agent SDK in my Android Application class with proper lifecycle management
```

### Example 2: Natural Language Query

```text
Send a natural language query "Navigate to Beijing Capital Airport" and handle the route planning result
```

### Example 3: LinkClient Integration

```text
Set up LinkClient to communicate with the AMap APP for cross-app navigation
```

### Example 4: Transport Mode Switch

```text
Implement a transport mode selector that allows users to switch between driving, walking, and cycling
```

## Directory Structure

```text
android-llm-agent/
├── SKILL.md                    # Main skill file (AI entry point)
├── api/                        # API guides
│   ├── quick-start.md          # Quick integration guide
│   ├── agent-query.md          # Send AI queries
│   ├── query-result.md         # Handle query results
│   ├── link-client.md          # LinkClient communication
│   ├── transport-mode.md       # Transport mode switching
│   ├── logger.md               # Logger configuration
│   └── lifecycle.md            # Lifecycle management
└── references/                 # Reference documentation
    ├── core-classes.md         # Core classes reference
    ├── troubleshooting.md      # Troubleshooting guide
    └── voice-commands.md       # Voice command examples
```

## FAQ

### Q: Agent SDK dependency cannot be downloaded

**A:** If the Agent SDK or Navigation SDK dependency has issues (download failure, version conflicts, etc.), please contact the AMap team for the dependency package.

### Q: Natural language query returns no result

**A:** Check that:
1. SDK is properly initialized
2. Network connection is available
3. API key is correctly configured

### Q: LinkClient connection fails

**A:** Ensure:
1. AMap APP is installed on the device
2. LinkClient is properly configured
3. Required permissions are granted

## Related Links

- [AMap Open Platform Console](https://console.amap.com/)
- [Cursor Official Documentation](https://docs.cursor.com/)
- [⬆️ Back to Home](../README.md)

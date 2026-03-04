# iOS LLM Agent SDK (MALLMKit) Skills User Guide

[🇨🇳 中文文档](./README_zh.md) | [⬆️ Back to Home](../README.md)

## Product Introduction

**AMap iOS LLM Agent SDK Skills** (MALLMKit) is an AI programming skill package designed for AI IDEs. It integrates the official documentation, best practices, and code templates of the AMap MALLMKit SDK for iOS into structured skill files, enabling AI coding tools like Cursor, Claude, and Cline to:

- **Accurately understand** how to integrate intelligent map services into iOS applications
- **Automatically generate** Agent initialization, query, navigation control, and IPC communication code
- **Proactively avoid** common integration issues such as authorization failures and connection management
- **Provide** verified code examples for both Agent SDK and Link SDK features

## Product Features

### Intelligent Map Services

Supports natural language queries for route planning, POI search, navigation control, and more. Users can interact with maps using natural language like "Go to Tibet" or "Find nearby KFC".

### Dual SDK Architecture

Includes both Agent SDK (for AI Agent-powered map interactions) and Link SDK (for communication with AMap APP), providing comprehensive integration capabilities.

### Complete Navigation Control

Full navigation lifecycle management including start/stop navigation, route switching, broadcast mode control, and real-time navigation data monitoring.

### IPC Communication

Robust IPC communication framework with AMap APP, supporting authorization, connection management, data transfer, and navigation commands.

## Capabilities

### Agent SDK

| **Capability** | **Description** |
| --- | --- |
| Intelligent Query | Natural language queries for routes, POI, navigation |
| Query Result Handling | Process AI responses with structured data |
| Navigation Control | Start/stop navigation, switch routes, broadcast mode |
| Navigation Data Listener | Real-time navigation data callbacks |
| Transport Mode | Navigation environment and route preference configuration |
| Lifecycle Management | Scene management, state reset, memory cleanup |

### Link SDK

| **Capability** | **Description** |
| --- | --- |
| Authorization | AMapAuthorizationManager for auth flow and callbacks |
| Connection Management | AMapLinkManager for connection, status monitoring, auto-reconnect |
| Data Transfer | Send data, navigation commands (waypoints, destination, broadcast, start navigation) |
| Navigation Commands | Waypoint/destination setting, broadcast control, navigation start |

### Reference

| **Capability** | **Description** |
| --- | --- |
| Agent Core Classes | Agent SDK public classes and enum reference |
| Link Core Classes | Link SDK public classes reference |
| Link Error Codes | Link SDK error code reference |
| Voice Commands | Supported natural language command examples |
| Troubleshooting | Error codes and common issue resolution |

## Quick Start

### Step 1: Configure Skill in Cursor

```bash
# Link the iOS LLM Agent skill to your project
ln -s /path/to/open_sdk_skills/ios-llm-agent-sdk .cursor/skills/ios-llm-agent-sdk
```

### Step 2: Verify Configuration

Open Cursor AI Chat and enter:

**For Agent SDK:**
```text
Help me integrate MALLMKit SDK into my iOS app and implement a natural language map query
```

**For Link SDK:**
```text
Help me set up IPC communication with AMap APP using the Link SDK, including authorization and connection management
```

If AI correctly references the Skill files and generates complete integration code, the Skill has been successfully loaded.

### Step 3: Choose Your Integration Path

- **Agent SDK**: For AI-powered map interactions → Start with [Quick Start](api/quick-start.md) or [Integrate Agent](api/integrate-agent.md)
- **Link SDK**: For IPC communication with AMap APP → Start with [Link Quick Start](api/link-quick-start.md)

## Usage Examples

### Example 1: Agent Initialization

```text
Initialize MALLMKit Agent SDK in my iOS app, register navigation commands, and set up query callbacks
```

### Example 2: Natural Language Query

```text
Send a natural language query "Find the nearest gas station and navigate there" and handle the route planning result
```

### Example 3: Navigation Control

```text
Implement navigation control with start/stop, route switching, and real-time navigation data display
```

### Example 4: Link SDK Integration

```text
Set up Link SDK to communicate with AMap APP, implement authorization flow, establish connection, and send navigation commands
```

## Directory Structure

```text
ios-llm-agent-sdk/
├── SKILL.md                        # Main skill file (AI entry point)
├── api/                            # API guides
│   ├── quick-start.md              # Agent SDK quick start
│   ├── integrate-agent.md          # Complete Agent integration flow
│   ├── agent-query.md              # Natural language queries
│   ├── query-result.md             # Query result handling
│   ├── navi-control.md             # Navigation control
│   ├── navi-data-listener.md       # Navigation data listener
│   ├── transport-mode.md           # Transport mode configuration
│   ├── link-quick-start.md         # Link SDK quick start
│   ├── link-client.md              # LinkClient management
│   ├── authorization.md            # Authorization management
│   ├── connection.md               # Connection management
│   ├── data-transfer.md            # Data transfer and commands
│   ├── logger.md                   # Logger configuration
│   └── lifecycle.md                # Lifecycle management
└── references/                     # Reference documentation
    ├── core-classes.md             # Agent SDK core classes
    ├── link-core-classes.md        # Link SDK core classes
    ├── link-error-codes.md         # Link SDK error codes
    ├── troubleshooting.md          # Troubleshooting guide
    └── voice-commands.md           # Voice command examples
```

## FAQ

### Q: Agent query returns no result

**A:** Check that:
1. Agent SDK is properly initialized with correct API key
2. Network connection is available
3. Query format follows the supported patterns (see [Voice Commands](references/voice-commands.md))

### Q: Link SDK authorization fails

**A:** Ensure:
1. AMap APP is installed on the device
2. Authorization configuration is correct
3. Check error codes in [Link Error Codes](references/link-error-codes.md)

### Q: Navigation data listener not receiving callbacks

**A:** Verify:
1. Navigation is properly started
2. Data listener is registered before navigation starts
3. Location permissions are granted

### Q: Connection with AMap APP drops frequently

**A:** Check:
1. Auto-reconnect is enabled in AMapLinkManager
2. Both apps are in the foreground or have background mode enabled
3. Review connection status monitoring implementation

## Related Links

- [AMap Open Platform Console](https://console.amap.com/)
- [Cursor Official Documentation](https://docs.cursor.com/)
- [⬆️ Back to Home](../README.md)

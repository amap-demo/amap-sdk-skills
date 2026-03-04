# RTOS Map SDK Skills User Guide

[🇨🇳 中文文档](./README_zh.md) | [⬆️ Back to Home](../README.md)

## Product Introduction

**AMap RTOS Map SDK Skills** (WatchSDK) is an AI programming skill package designed for AI IDEs. It integrates the official documentation, best practices, and code templates of the AMap RTOS Map SDK into structured skill files, enabling AI coding tools like Cursor, Claude, and Cline to:

- **Accurately understand** how to integrate and use the WatchSDK on RTOS devices
- **Automatically generate** adapter implementations and map integration code
- **Proactively avoid** common pitfalls such as incorrect enum names, missing struct fields, and thread safety issues
- **Provide** verified code examples with strict type checking against SDK header files

## Product Features

### Lightweight Map SDK

Designed specifically for smart glasses, smart watches and other RTOS devices, providing raster and vector map rendering with minimal resource footprint.

### Strict Type Safety

Built-in code implementation guidelines that enforce reading SDK header files before writing code, preventing common compilation errors from incorrect enum values or struct field names.

### Complete Adapter Guide

Comprehensive adapter implementation documentation covering memory, file, network, render, system, and thread adapters with platform-specific examples.

### iOS Integration Support

Detailed iOS integration guide including SwiftUI views, gesture handling, and complete demo project references.

## Capabilities

### Map Rendering

| **Capability** | **Description** |
| --- | --- |
| Map Initialization | SDK init, device activation, map creation |
| Raster/Vector Maps | Standard grid and satellite tile styles |
| View Control | Zoom, rotation, center point adjustment |
| Lifecycle Management | Init, activate, create, render, destroy flow |

### Overlays

| **Capability** | **Description** |
| --- | --- |
| Point Overlay | Point annotations on map |
| Polyline Overlay | Line annotations for routes and tracks |
| Polygon Overlay | Area annotations |
| Overlay Management | Add, remove, update overlays |

### Navigation

| **Capability** | **Description** |
| --- | --- |
| Track Navigation | Real-time navigation data display |
| Navigation Callbacks | Turn-by-turn data, distance, ETA |
| Turn Icons | Navigation turn direction icons |

### Platform Adapters

| **Capability** | **Description** |
| --- | --- |
| Memory Adapter | malloc/free/realloc implementations |
| File Adapter | File I/O operations |
| Network Adapter | HTTP request handling |
| Render Adapter | Map rendering to screen (most critical) |
| System Adapter | System time, device info |
| Thread Adapter | Thread creation and synchronization |

## Quick Start

### Step 1: Configure Skill in Cursor

```bash
# Link the RTOS skill to your project
ln -s /path/to/open_sdk_skills/RTOS .cursor/skills/RTOS
```

### Step 2: Verify Configuration

Open Cursor AI Chat and enter:

```text
Help me initialize the WatchSDK and create a map view, implementing all required adapters for iOS platform
```

If AI correctly references the RTOS Skill files and generates code with proper header file type checking, the Skill has been successfully loaded.

### Step 3: Key Integration Points

1. **Initialize SDK** with `awk_init()` - see [Quick Start](api/quick-start.md)
2. **Implement Adapters** - see [Adapters Guide](api/adapters.md)
3. **Activate Device** with `awk_activate_device()` - see [Lifecycle](api/lifecycle.md)
4. **Create Map** with `awk_map_create_view()` - see [Map Operations](api/map-operations.md)

## Usage Examples

### Example 1: SDK Initialization

```text
Initialize WatchSDK with all required adapters for iOS, including memory, file, network, render, system, and thread adapters
```

### Example 2: Map Creation

```text
Create a map view centered on Beijing with zoom level 12, using standard grid tile style
```

### Example 3: Add Overlays

```text
Add a polyline overlay on the map showing a navigation route from point A to point B
```

### Example 4: Navigation Integration

```text
Initialize navigation module and set up callbacks to receive real-time navigation data including turn directions and remaining distance
```

## Directory Structure

```text
RTOS/
├── SKILL.md                        # Main skill file (AI entry point)
├── api/                            # API guides
│   ├── quick-start.md              # Quick SDK integration
│   ├── ios-integration.md          # iOS platform integration
│   ├── ios-demo-guide.md           # iOS demo project guide
│   ├── lifecycle.md                # Init, activate, destroy flow
│   ├── adapters.md                 # Adapter implementation guide
│   ├── map-operations.md           # Map creation and control
│   ├── overlays.md                 # Overlay management
│   └── navigation.md              # Navigation setup
└── references/                     # Reference documentation
    ├── adapter-requirements.md     # Required adapter functions
    ├── core-types.md               # Key data structure definitions
    ├── error-codes.md              # Error codes and troubleshooting
    └── troubleshooting.md          # FAQ and problem diagnosis
```

## Key Constraints

1. **Single-Thread Model**: All SDK methods must be called on the same main thread
2. **Coordinate System**: Uses GCJ02 coordinate system exclusively
3. **Activation Required**: First-time use requires network activation
4. **Header File First**: Always read SDK header files before writing integration code

## FAQ

### Q: Map shows blank/nothing renders

**A:** Check that the render adapter is fully implemented. The three critical functions are `begin_drawing`, `commit_drawing`, and `draw_bitmap`. Empty implementations will result in no map display.

### Q: Compilation errors with enum values

**A:** SDK enum naming is inconsistent. Always read the header file to confirm exact enum names. For example, use `AWK_MAP_TILE_LOAD_ONLINE` not `AWK_MAP_TILE_LOAD_MODE_ONLINE`.

### Q: Compilation errors with struct fields

**A:** Some struct fields have unusual naming (e.g., `fill_ttyle` instead of `fill_style`). Always verify field names against the header file definitions.

## Related Links

- [AMap Open Platform Console](https://console.amap.com/)
- [Cursor Official Documentation](https://docs.cursor.com/)
- [⬆️ Back to Home](../README.md)

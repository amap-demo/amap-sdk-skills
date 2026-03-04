# WatchSDK Agent Skill

> RTOS 地图 SDK 接入助手 - 支持栅格/矢量地图渲染与轨迹导航

## 触发词

当用户询问以下内容时，应触发此 Skill：

### SDK 相关
- WatchSDK、RTOS地图SDK、手表地图SDK、智能硬件地图
- awk_init、awk_uninit、SDK初始化、SDK接入

### 地图相关
- awk_map、地图渲染、创建地图、销毁地图
- 瓦片、tile、栅格地图、矢量地图
- 地图缩放、地图旋转、地图中心点
- awk_map_create_view、awk_map_do_render

### 覆盖物相关
- overlay、覆盖物、点标注、线标注、面标注
- awk_map_add_overlay、awk_map_remove_overlay
- point_overlay、polyline_overlay、polygon_overlay

### 导航相关
- awk_navi、导航、轨迹导航、实时导航
- 导航回调、导航数据、转向图标
- awk_init_navi、awk_navi_data

### 适配器相关
- adapter、适配器、适配器函数、必需函数
- memory_adapter、内存适配器
- file_adapter、文件适配器
- render_adapter、渲染适配器
- network_adapter、网络适配器
- system_adapter、系统适配器
- thread_adapter、线程适配器
- tile_file_adapter、瓦片文件适配器
- AWK_CHECK_ADAPTER_FUNC、适配器检查

### iOS 相关
- iOS 集成、iOS 接入、iOS 适配器
- Objective-C、Swift 集成
- CADisplayLink、GCD、主线程
- .a 静态库、静态库引入
- Header Search Paths、Library Search Paths

### 设备与激活
- 设备激活、awk_activate_device、license
- device_id、开放平台key

### SwiftUI 与 WatchOS 相关
- SwiftUI 地图视图、GDMapView、AMapMyLocationView
- 手势处理、拖拽、单点、双击、表冠旋转
- NavigationLink、视图导航
- 视图生命周期、onAppear、onDisappear

### Demo 与示例
- WatchSDKDemo、我的地图、导航组件
- GDWatchEngine、GDMapViewModel
- 地图场景、MapScene、GDSceneParam
- 渲染回调、AMapRenderDelegate

### 坐标相关
- GCJ02、坐标系、坐标转换
- 经纬度转屏幕坐标、屏幕坐标转经纬度
- awk_map_lonlat_to_xy、awk_map_xy_to_lonlat

### 错误与问题
- 错误码、初始化失败、激活失败
- 地图不显示、渲染异常、线程问题
- 适配器错误、-200、-300、-400、-500、-600、-701、-800
- 缺失函数、未实现函数

---

## 核心能力

WatchSDK 是一个面向 RTOS 设备的轻量级地图 SDK，提供：
- **地图渲染**：栅格/矢量地图显示、缩放、旋转
- **覆盖物**：点/线/面标注
- **轨迹导航**：实时导航数据展示
- **离线地图**：离线数据下载与使用

## 快速导航

### 接入指南
| 文档 | 说明 |
|------|------|
| [快速开始](api/quick-start.md) | 5分钟完成 SDK 接入 |
| [iOS 集成](api/ios-integration.md) | iOS 平台完整接入指南 |
| [iOS Demo 指南](api/ios-demo-guide.md) | 基于 WatchSDKDemo 的功能实现参考 |
| [生命周期](api/lifecycle.md) | 初始化、激活、销毁流程 |
| [适配器](api/adapters.md) | 内存/文件/网络/渲染适配器实现 |

### API 文档
| 文档 | 说明 |
|------|------|
| [地图操作](api/map-operations.md) | 创建、控制、渲染地图 |
| [覆盖物](api/overlays.md) | 点/线/面覆盖物管理 |
| [导航](api/navigation.md) | 导航初始化与数据回调 |

### 参考资料
| 文档 | 说明 |
|------|------|
| [适配器必需函数](references/adapter-requirements.md) | 必须实现的适配器函数与错误码 |
| [核心类型](references/core-types.md) | 关键数据结构定义 |
| [错误码](references/error-codes.md) | 错误码说明与排查 |
| [常见问题](references/troubleshooting.md) | FAQ 与问题排查 |

## 关键约束

1. **单线程模型**：所有 SDK 方法必须在同一主流程线程调用
2. **坐标系**：统一使用 GCJ02 坐标系
3. **激活要求**：首次使用需联网激活设备

## 头文件引用

```c
#include "awk.h"           // 核心初始化
#include "awk_adapter.h"   // 适配器定义
#include "map/awk_map.h"   // 地图操作
#include "navi/awk_navi.h" // 导航功能
```

---

## 🔧 代码实现规范

### 核心原则：以 SDK 头文件为唯一真理来源

在实现任何 SDK 相关代码时，**必须**遵循以下流程：

### 1. 实现前必读头文件

**在编写任何使用 SDK 类型、函数、枚举的代码前，必须先使用 `read_file` 工具读取相关头文件，确认：**

- ✅ 结构体的完整定义和所有字段名称
- ✅ 枚举值的完整名称（包括前缀、下划线等）
- ✅ 函数签名的完整参数列表和类型
- ✅ 回调函数的签名和参数顺序

**禁止行为：**
- ❌ 根据经验或猜测假设字段名称
- ❌ 使用简写或不完整的枚举值名称
- ❌ 假设结构体包含某些"常见"字段
- ❌ 复制其他项目的代码而不验证类型定义

### 2. 关键头文件清单

实现代码时必须查阅的头文件：

| 头文件 | 用途 | 何时查阅 |
|--------|------|----------|
| `awk_defines.h` | 基础类型定义（点、矩形、位图等） | 使用 `awk_point_t`、`awk_bitmap_t`、`awk_rect_area_t` 等类型时 |
| `awk_adapter.h` | 适配器接口定义 | 实现任何适配器函数时 |
| `map/awk_map_defines.h` | 地图相关类型定义 | 使用地图参数、覆盖物、瓦片样式等时 |
| `map/awk_map.h` | 地图操作 API | 调用地图创建、渲染等函数时 |
| `navi/awk_navi_defines.h` | 导航相关类型 | 使用导航数据结构时 |
| `navi/awk_navi.h` | 导航操作 API | 调用导航相关函数时 |

### 3. 类型使用检查清单

在使用任何 SDK 类型前，必须确认：

#### 结构体字段
```
□ 已读取头文件确认结构体定义
□ 字段名称与头文件完全一致（包括大小写、下划线）
□ 字段类型正确（指针、枚举、嵌套结构体等）
□ 理解字段的语义和使用方式
```

#### 枚举值
```
□ 已读取头文件确认枚举定义
□ 使用完整的枚举值名称（不使用简写）
□ 枚举值前缀正确（如 AWK_MAP_TILE_STYLE_）
□ 注意下划线的位置（如 RGBA_8888 不是 RGBA8888）
□ 严禁根据命名规律猜测枚举值名称
```

**⚠️ 枚举值命名陷阱警告：**

SDK 中的枚举值命名**不遵循统一规则**，必须逐个查阅头文件确认。以下是常见的命名陷阱：

| 错误示例 | 正确名称 | 头文件位置 |
|---------|---------|-----------|
| ❌ `AWK_MAP_TILE_LOAD_MODE_ONLINE` | ✅ `AWK_MAP_TILE_LOAD_ONLINE` | `map/awk_map_defines.h` |
| ❌ `AWK_MAP_TILE_LOAD_MODE_OFFLINE` | ✅ `AWK_MAP_TILE_LOAD_OFFLINE` | `map/awk_map_defines.h` |
| ❌ `AWK_MAP_TILE_STYLE_NORMAL` | ✅ `AWK_MAP_TILE_STYLE_STANDARD_GRID` | `map/awk_map_defines.h` |
| ❌ `AWK_PIXEL_MODE_RGBA8888` | ✅ `AWK_PIXEL_MODE_RGBA_8888` | `awk_defines.h` |

**关键规则：**
1. **绝对禁止**根据其他枚举的命名规律推测新枚举的名称
2. **绝对禁止**使用"常见"或"标准"的命名假设
3. **必须**使用 `read_file` 工具读取对应头文件确认枚举定义
4. **必须**复制粘贴头文件中的完整枚举值名称，不要手动输入

#### 函数调用
```
□ 已读取头文件确认函数签名
□ 参数数量正确
□ 参数类型匹配
□ 参数顺序正确
□ 理解返回值的含义
```

### 4. 实现流程示例

**正确的实现流程：**

```
步骤 1: 确定需要使用的类型/函数
  ↓
步骤 2: 使用 read_file 读取相关头文件
  ↓
步骤 3: 仔细阅读类型定义和注释
  ↓
步骤 4: 按照头文件定义编写代码
  ↓
步骤 5: 再次对照头文件检查代码
```

**示例 1：实现网络适配器（结构体字段）**

```objc
// ❌ 错误做法：直接编写代码
static uint64_t aw_network_send(awk_http_request_t *request, ...) {
    // 假设 request->body 是 char*
    urlRequest.HTTPBody = [NSData dataWithBytes:request->body 
                                         length:request->body_size];
}

// ✅ 正确做法：先读取 awk_adapter.h 确认结构体定义
// 1. read_file("awk_adapter.h") 查看 awk_http_request_t 定义
// 2. 发现 body 是 awk_http_buffer_t* 类型
// 3. 再查看 awk_http_buffer_t 定义
// 4. 按照实际定义编写代码

static uint64_t aw_network_send(awk_http_request_t *request, ...) {
    // 正确：使用 request->body->buffer 和 request->body->length
    if (request->body && request->body->buffer && request->body->length > 0) {
        urlRequest.HTTPBody = [NSData dataWithBytes:request->body->buffer 
                                             length:request->body->length];
    }
}
```

**示例 2：使用枚举值（最常见错误）**

```objc
// ❌ 错误做法：根据命名规律猜测
awk_context_t context;
context.tile_load_mode = AWK_MAP_TILE_LOAD_MODE_ONLINE;  // 编译错误！
context.tile_style = AWK_MAP_TILE_STYLE_NORMAL;          // 编译错误！

// ✅ 正确做法：先读取 map/awk_map_defines.h 确认枚举定义
// 1. read_file("map/awk_map_defines.h")
// 2. 搜索 "awk_map_tile_load_mode_t" 找到枚举定义：
//    typedef enum {
//        AWK_MAP_TILE_LOAD_OFFLINE = 0x01,
//        AWK_MAP_TILE_LOAD_ONLINE = 0x02    // ← 注意：不是 MODE_ONLINE
//    } awk_map_tile_load_mode_t;
// 3. 搜索 "awk_map_tile_style_t" 找到枚举定义：
//    typedef enum {
//        AWK_MAP_TILE_STYLE_STANDARD_GRID = 0,  // ← 注意：不是 NORMAL
//        AWK_MAP_TILE_SATELLITE = 1,
//        ...
//    } awk_map_tile_style_t;
// 4. 复制粘贴正确的枚举值

awk_context_t context;
context.tile_load_mode = AWK_MAP_TILE_LOAD_ONLINE;        // ✅ 正确
context.tile_style = AWK_MAP_TILE_STYLE_STANDARD_GRID;    // ✅ 正确
```

### 5. 常见错误模式及预防

| 错误模式 | 预防方法 | 实际案例 |
|---------|---------|---------|
| 字段名称错误（如 `data` vs `buffer`） | 读取头文件确认字段名 | `request->body` 实际是 `awk_http_buffer_t*` 类型 |
| **枚举值名称错误** | **必须读取头文件确认完整枚举值** | **`AWK_MAP_TILE_LOAD_MODE_ONLINE` ❌ 应为 `AWK_MAP_TILE_LOAD_ONLINE` ✅** |
| 枚举值前缀不一致 | 不要根据命名规律猜测 | `AWK_MAP_TILE_STYLE_NORMAL` ❌ 应为 `AWK_MAP_TILE_STYLE_STANDARD_GRID` ✅ |
| 结构体字段不存在（如 `center`、`zoom`） | 读取头文件确认结构体定义 | `awk_context_t` 中没有 `center` 字段 |
| 回调函数签名错误 | 读取头文件确认函数指针定义 | 回调参数顺序和类型必须完全匹配 |
| 类型嵌套错误（如 `body` 是指针） | 读取头文件理解类型层次 | `request->body->buffer` 而非 `request->body` |
| **字段名拼写错误** | **必须读取头文件确认字段名** | **`fill_style` ❌ 应为 `fill_ttyle` ✅（头文件拼写错误）** |

**🚨 枚举值错误是最常见的编译错误，必须严格遵守以下流程：**

```
步骤 1: 确定需要使用的枚举类型（如 tile_load_mode）
  ↓
步骤 2: 使用 read_file 读取对应头文件（如 map/awk_map_defines.h）
  ↓
步骤 3: 搜索枚举类型定义（如 awk_map_tile_load_mode_t）
  ↓
步骤 4: 复制粘贴完整的枚举值名称（如 AWK_MAP_TILE_LOAD_ONLINE）
  ↓
步骤 5: 绝不手动输入或根据规律猜测
```

---

## 🎨 渲染适配器实现指南

渲染适配器是 WatchSDK 中**最关键**的适配器，负责将地图内容绘制到屏幕上。如果渲染适配器实现为空或不正确，地图将无法显示。

### 1. 渲染适配器核心职责

渲染适配器需要实现 9 个回调函数：

| 函数 | 职责 | 是否必需 |
|------|------|---------|
| `begin_drawing` | 开始绘制，创建图形上下文 | ✅ 必需 |
| `commit_drawing` | 结束绘制，提交渲染结果 | ✅ 必需 |
| `draw_bitmap` | 绘制位图（地图瓦片） | ✅ 必需 |
| `draw_point` | 绘制点（覆盖物） | 可选 |
| `draw_polyline` | 绘制线（覆盖物） | 可选 |
| `draw_polygon` | 绘制面（覆盖物） | 可选 |
| `draw_text` | 绘制文字（标注） | 可选 |
| `draw_color` | 绘制纯色背景 | 可选 |
| `measure_text` | 测量文字尺寸 | ✅ 必需 |

### 2. 实现前必读的头文件

```c
#include "awk_adapter.h"  // 渲染适配器接口定义
#include "awk_defines.h"  // 基础类型定义
```

**关键类型定义：**

```c
// 渲染上下文（注意：没有 scale 字段）
typedef struct _awk_render_context_t {
    int32_t width;                      // 画布宽度
    int32_t height;                     // 画布高度
    awk_rect_area_t map_view_rect;     // 地图view的rect区域
} awk_render_context_t;

// 绘制样式（注意：字段名是 fill_ttyle，不是 fill_style）
typedef struct _awk_paint_style_t {
    uint32_t width;                 // 画笔宽度
    uint32_t color;                 // 画笔颜色 ARGB
    float angle;                    // 旋转角度
    awk_text_style_t text_style;    // 文字样式
    awk_fill_style_t fill_ttyle;    // ⚠️ 注意拼写：fill_ttyle
    awk_dash_style_t dash_style;    // 虚线样式
} awk_paint_style_t;

// 填充样式枚举
typedef enum {
   AWK_FILL_STYLE_DRAWING_ONLY,          // 仅填充
   AWK_FILL_STYLE_DRAWING_AND_STROKE,    // 填充+描边
   AWK_FILL_STYLE_STROKE_ONLY            // 仅描边
} awk_fill_style_t;
```

### 3. iOS 平台实现要点

#### 3.1 全局状态管理

```objc
// 全局渲染上下文存储
static NSMutableDictionary<NSNumber*, NSValue*> *g_renderContexts = nil;
static NSMutableDictionary<NSNumber*, UIImage*> *g_renderedImages = nil;

typedef struct {
    int32_t width;
    int32_t height;
} RenderContext;
```

#### 3.2 begin_drawing 实现

**关键点：**
- 创建 UIKit 图形上下文
- 保存渲染上下文信息
- ⚠️ 注意：`awk_render_context_t` 中**没有 scale 字段**

```objc
static void aw_begin_drawing(uint32_t map_id, awk_render_context_t context) {
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        g_renderContexts = [NSMutableDictionary dictionary];
        g_renderedImages = [NSMutableDictionary dictionary];
    });
    
    // 保存渲染上下文
    RenderContext renderCtx;
    renderCtx.width = context.width;
    renderCtx.height = context.height;
    
    NSValue *value = [NSValue valueWithBytes:&renderCtx objCType:@encode(RenderContext)];
    g_renderContexts[@(map_id)] = value;
    
    // 创建图形上下文（scale 使用固定值 1.0）
    CGSize size = CGSizeMake(context.width, context.height);
    UIGraphicsBeginImageContextWithOptions(size, NO, 1.0);
    
    NSLog(@"[Render] Begin drawing for map %d, size: %dx%d", map_id, context.width, context.height);
}
```

#### 3.3 commit_drawing 实现

**关键点：**
- 从图形上下文获取渲染的 UIImage
- 通过 NSNotification 通知主线程更新 UI
- 结束图形上下文

```objc
static void aw_commit_drawing(uint32_t map_id) {
    // 获取渲染的图像
    UIImage *image = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    
    if (image) {
        g_renderedImages[@(map_id)] = image;
        NSLog(@"[Render] Commit drawing for map %d, image size: %.0fx%.0f", 
              map_id, image.size.width, image.size.height);
        
        // 通知主线程更新 UI
        dispatch_async(dispatch_get_main_queue(), ^{
            [[NSNotificationCenter defaultCenter] postNotificationName:@"WatchSDKMapRendered" 
                                                                object:nil 
                                                              userInfo:@{@"mapId": @(map_id), @"image": image}];
        });
    }
}
```

#### 3.4 draw_bitmap 实现（最关键）

**关键点：**
- 创建 CGBitmapContext 处理位图数据
- **坐标系转换**：SDK 使用标准坐标系（原点在左下），iOS 使用左上坐标系
- 支持旋转角度
- 正确释放内存

```objc
static void aw_draw_bitmap(uint32_t map_id, awk_rect_area_t area, awk_bitmap_t bitmap, const awk_paint_style_t *style) {
    if (!bitmap.buffer || bitmap.width == 0 || bitmap.height == 0) return;
    
    CGContextRef context = UIGraphicsGetCurrentContext();
    if (!context) return;
    
    // 获取渲染上下文
    NSValue *value = g_renderContexts[@(map_id)];
    if (!value) return;
    
    RenderContext renderCtx;
    [value getValue:&renderCtx];
    
    // 创建位图上下文
    CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
    size_t bitsPerComponent = 8;
    uint32_t alphaInfo = bitmap.pre_multiplied ? kCGImageAlphaPremultipliedLast : kCGImageAlphaLast;
    
    CGContextRef bitmapContext = CGBitmapContextCreate(
        (void*)bitmap.buffer,
        bitmap.width,
        bitmap.height,
        bitsPerComponent,
        bitmap.width * 4,  // bytesPerRow (RGBA = 4 bytes)
        colorSpace,
        alphaInfo
    );
    
    if (!bitmapContext) {
        CGColorSpaceRelease(colorSpace);
        return;
    }
    
    CGImageRef imageRef = CGBitmapContextCreateImage(bitmapContext);
    
    // 🔑 关键：坐标系转换
    // SDK 使用标准坐标系（原点在左下），iOS 使用左上坐标系
    CGContextSaveGState(context);
    CGContextTranslateCTM(context, 0, renderCtx.height);
    CGContextScaleCTM(context, 1.0, -1.0);
    
    CGRect targetRect = CGRectMake(area.x, renderCtx.height - area.y - area.height, area.width, area.height);
    
    // 处理旋转
    if (style && style->angle != 0) {
        CGFloat centerX = targetRect.origin.x + area.width / 2.0;
        CGFloat centerY = targetRect.origin.y + area.height / 2.0;
        CGContextTranslateCTM(context, centerX, centerY);
        CGContextRotateCTM(context, style->angle * M_PI / 180.0);
        CGContextDrawImage(context, CGRectMake(-area.width / 2.0, -area.height / 2.0, area.width, area.height), imageRef);
        CGContextRotateCTM(context, -style->angle * M_PI / 180.0);
        CGContextTranslateCTM(context, -centerX, -centerY);
    } else {
        CGContextDrawImage(context, targetRect, imageRef);
    }
    
    CGContextRestoreGState(context);
    
    // 释放内存
    CGImageRelease(imageRef);
    CGContextRelease(bitmapContext);
    CGColorSpaceRelease(colorSpace);
}
```

#### 3.5 辅助函数

```objc
// ARGB 颜色转 UIColor
static UIColor* UIColorFromARGB(uint32_t argb) {
    CGFloat alpha = ((argb >> 24) & 0xFF) / 255.0;
    CGFloat red = ((argb >> 16) & 0xFF) / 255.0;
    CGFloat green = ((argb >> 8) & 0xFF) / 255.0;
    CGFloat blue = (argb & 0xFF) / 255.0;
    return [UIColor colorWithRed:red green:green blue:blue alpha:alpha];
}
```

#### 3.6 draw_point 实现

**⚠️ 注意：字段名是 `fill_ttyle`，不是 `fill_style`**

```objc
static void aw_draw_point(uint32_t map_id, awk_point_t *points, uint32_t point_size, const awk_paint_style_t *style) {
    if (!points || point_size == 0 || !style) return;
    
    CGContextRef context = UIGraphicsGetCurrentContext();
    if (!context) return;
    
    UIColor *color = UIColorFromARGB(style->color);
    [color set];
    
    for (uint32_t i = 0; i < point_size; i++) {
        awk_point_t point = points[i];
        CGFloat radius = style->width / 2.0;
        
        // ⚠️ 使用 fill_ttyle，不是 fill_style
        if (style->fill_ttyle == AWK_FILL_STYLE_DRAWING_ONLY || 
            style->fill_ttyle == AWK_FILL_STYLE_DRAWING_AND_STROKE) {
            CGContextAddArc(context, point.x, point.y, radius, 0, 2 * M_PI, 0);
            CGContextFillPath(context);
        }
        
        if (style->fill_ttyle == AWK_FILL_STYLE_STROKE_ONLY || 
            style->fill_ttyle == AWK_FILL_STYLE_DRAWING_AND_STROKE) {
            CGContextSetLineWidth(context, 2.0);
            CGContextAddArc(context, point.x, point.y, radius + 1, 0, 2 * M_PI, 0);
            CGContextStrokePath(context);
        }
    }
}
```

#### 3.7 draw_polyline 实现

**⚠️ 注意：`awk_paint_style_t` 中没有 `cap_style` 字段**

```objc
static void aw_draw_polyline(uint32_t map_id, awk_point_t *points, uint32_t point_size, const awk_paint_style_t *style) {
    if (!points || point_size < 2 || !style) return;
    
    CGContextRef context = UIGraphicsGetCurrentContext();
    if (!context) return;
    
    UIColor *color = UIColorFromARGB(style->color);
    [color set];
    
    CGContextSetLineWidth(context, style->width);
    CGContextSetLineCap(context, kCGLineCapRound);  // 固定使用圆角
    
    // 设置虚线样式
    if (style->dash_style.painted_length > 0 || style->dash_style.unpainted_length > 0) {
        CGFloat lengths[] = {style->dash_style.painted_length, style->dash_style.unpainted_length};
        CGContextSetLineDash(context, style->dash_style.offset, lengths, 2);
    }
    
    CGContextBeginPath(context);
    CGContextMoveToPoint(context, points[0].x, points[0].y);
    for (uint32_t i = 1; i < point_size; i++) {
        CGContextAddLineToPoint(context, points[i].x, points[i].y);
    }
    CGContextStrokePath(context);
    
    // 重置虚线样式
    CGContextSetLineDash(context, 0, NULL, 0);
}
```

### 4. UI 层集成

在 ViewController 中接收渲染结果：

```objc
@interface MapViewController ()
@property (nonatomic, strong) UIImageView *mapImageView;
@end

@implementation MapViewController

- (void)setupUI {
    // 创建地图图像视图
    self.mapImageView = [[UIImageView alloc] initWithFrame:self.view.bounds];
    self.mapImageView.contentMode = UIViewContentModeScaleAspectFit;
    [self.view addSubview:self.mapImageView];
    
    // 监听地图渲染完成通知
    [[NSNotificationCenter defaultCenter] addObserver:self 
                                             selector:@selector(onMapRendered:) 
                                                 name:@"WatchSDKMapRendered" 
                                               object:nil];
}

- (void)onMapRendered:(NSNotification *)notification {
    NSDictionary *userInfo = notification.userInfo;
    NSNumber *mapId = userInfo[@"mapId"];
    UIImage *image = userInfo[@"image"];
    
    if (mapId.intValue == self.mapId && image) {
        self.mapImageView.image = image;
        NSLog(@"[MapViewController] Map rendered and displayed");
    }
}

- (void)dealloc {
    [[NSNotificationCenter defaultCenter] removeObserver:self];
}

@end
```

### 5. 常见渲染问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 地图不显示 | 渲染适配器未实现或实现为空 | 实现完整的 `begin_drawing`、`commit_drawing`、`draw_bitmap` |
| 编译错误：`fill_style` 不存在 | 字段名拼写错误 | 使用 `fill_ttyle`（头文件中的拼写） |
| 编译错误：`scale` 不存在 | `awk_render_context_t` 中没有此字段 | 使用固定值 1.0 或从其他地方获取 |
| 编译错误：`cap_style` 不存在 | `awk_paint_style_t` 中没有此字段 | 使用固定值 `kCGLineCapRound` |
| 地图倒置 | 坐标系未转换 | 使用 `CGContextTranslateCTM` 和 `CGContextScaleCTM` 转换 |
| 内存泄漏 | 未释放 CGContext 和 CGImage | 调用 `CGContextRelease` 和 `CGImageRelease` |

### 6. 渲染适配器实现检查清单

```
□ 已读取 awk_adapter.h 确认所有回调函数签名
□ 已读取 awk_defines.h 确认基础类型定义
□ 实现了 begin_drawing（创建图形上下文）
□ 实现了 commit_drawing（提交渲染结果）
□ 实现了 draw_bitmap（绘制地图瓦片）
□ 实现了 measure_text（测量文字尺寸）
□ 正确处理了坐标系转换
□ 使用了正确的字段名（fill_ttyle 而非 fill_style）
□ 没有使用不存在的字段（scale、cap_style）
□ 正确释放了所有 CGContext 和 CGImage
□ 通过通知机制将渲染结果传递给 UI 层
```

---

## 📚 参考资料

### 完整示例代码

完整的渲染适配器实现可参考以下关键文件结构：

**iOS 平台适配器实现：**
```
项目根目录/
├── SDK/
│   ├── WatchSDKAdapters.h      // 适配器头文件
│   ├── WatchSDKAdapters.m      // 适配器实现（包含渲染适配器）
│   └── WatchSDKManager.h/m     // SDK 管理器
└── ViewControllers/
    └── MapViewController.m      // UI 层集成示例
```

**关键实现文件说明：**
- **适配器实现文件**：包含所有 6 个适配器的完整实现（内存、文件、系统、网络、渲染、线程）
- **SDK 管理器**：封装 SDK 初始化、激活、地图创建等操作
- **UI 集成文件**：展示如何接收渲染结果并显示地图

### 相关文档

- [适配器必需函数](references/adapter-requirements.md)
- [iOS 集成指南](api/ios-integration.md)
- [常见问题排查](references/troubleshooting.md）
// ❌ 错误做法：根据命名规律猜测
awk_context_t context;
context.tile_load_mode = AWK_MAP_TILE_LOAD_MODE_ONLINE;  // 编译错误！
context.tile_style = AWK_MAP_TILE_STYLE_NORMAL;          // 编译错误！

// ✅ 正确做法：先读取 map/awk_map_defines.h 确认枚举定义
// 1. read_file("map/awk_map_defines.h")
// 2. 搜索 "awk_map_tile_load_mode_t" 找到枚举定义：
//    typedef enum {
//        AWK_MAP_TILE_LOAD_OFFLINE = 0x01,
//        AWK_MAP_TILE_LOAD_ONLINE = 0x02    // ← 注意：不是 MODE_ONLINE
//    } awk_map_tile_load_mode_t;
// 3. 搜索 "awk_map_tile_style_t" 找到枚举定义：
//    typedef enum {
//        AWK_MAP_TILE_STYLE_STANDARD_GRID = 0,  // ← 注意：不是 NORMAL
//        AWK_MAP_TILE_SATELLITE = 1,
//        ...
//    } awk_map_tile_style_t;
// 4. 复制粘贴正确的枚举值

awk_context_t context;
context.tile_load_mode = AWK_MAP_TILE_LOAD_ONLINE;        // ✅ 正确
context.tile_style = AWK_MAP_TILE_STYLE_STANDARD_GRID;    // ✅ 正确
```

### 5. 常见错误模式及预防

| 错误模式 | 预防方法 | 实际案例 |
|---------|---------|---------|
| 字段名称错误（如 `data` vs `buffer`） | 读取头文件确认字段名 | `request->body` 实际是 `awk_http_buffer_t*` 类型 |
| **枚举值名称错误** | **必须读取头文件确认完整枚举值** | **`AWK_MAP_TILE_LOAD_MODE_ONLINE` ❌ 应为 `AWK_MAP_TILE_LOAD_ONLINE` ✅** |
| 枚举值前缀不一致 | 不要根据命名规律猜测 | `AWK_MAP_TILE_STYLE_NORMAL` ❌ 应为 `AWK_MAP_TILE_STYLE_STANDARD_GRID` ✅ |
| 结构体字段不存在（如 `center`、`zoom`） | 读取头文件确认结构体定义 | `awk_context_t` 中没有 `center` 字段 |
| 回调函数签名错误 | 读取头文件确认函数指针定义 | 回调参数顺序和类型必须完全匹配 |
| 类型嵌套错误（如 `body` 是指针） | 读取头文件理解类型层次 | `request->body->buffer` 而非 `request->body` |

**🚨 枚举值错误是最常见的编译错误，必须严格遵守以下流程：**

```
步骤 1: 确定需要使用的枚举类型（如 tile_load_mode）
  ↓
步骤 2: 使用 read_file 读取对应头文件（如 map/awk_map_defines.h）
  ↓
步骤 3: 搜索枚举类型定义（如 awk_map_tile_load_mode_t）
  ↓
步骤 4: 复制粘贴完整的枚举值名称（如 AWK_MAP_TILE_LOAD_ONLINE）
  ↓
步骤 5: 绝不手动输入或根据规律猜测
```

### 6. 架构兼容性检查

在 iOS 项目中集成静态库时，必须检查架构兼容性：

```bash
# 检查静态库支持的架构
lipo -info libWatchSDK.a

# 如果库是 x86_64，需要在项目配置中排除 arm64
# Build Settings → Excluded Architectures → arm64
```

### 7. 编译前自检

在提交代码或编译前，进行以下检查：

```
□ 所有使用的类型都已查阅头文件
□ 所有字段名称与头文件一致
□ 所有枚举值使用完整名称
□ 所有函数调用参数正确
□ 静态库架构与编译目标匹配
□ 没有假设或猜测的代码
```

---

## 📝 实现检查表

在完成 SDK 集成代码后，使用此检查表验证：

### 适配器实现
- [ ] 已读取 `awk_adapter.h` 确认所有适配器函数签名
- [ ] 所有回调函数的参数类型和顺序正确
- [ ] 结构体字段访问使用正确的字段名
- [ ] 枚举值使用完整名称

### 地图操作
- [ ] 已读取 `map/awk_map_defines.h` 确认参数结构体定义
- [ ] `awk_map_view_param_t` 只使用存在的字段
- [ ] 瓦片样式枚举值完整正确
- [ ] 像素模式枚举值包含下划线

### 类型使用
- [ ] 已读取 `awk_defines.h` 确认基础类型定义
- [ ] `awk_bitmap_t` 使用 `buffer` 字段而非 `data`
- [ ] `awk_paint_style_t` 使用 `color` 字段而非 `fill_color`
- [ ] 所有指针类型正确解引用

### 编译配置
- [ ] 已检查静态库架构（`lipo -info`）
- [ ] 项目配置排除不支持的架构
- [ ] Header Search Paths 正确配置
- [ ] Library Search Paths 正确配置

---

## 🎯 总结

**核心原则：永远以 SDK 头文件为准，不要假设任何类型定义。**

在实现任何 SDK 相关代码时：
1. **先读头文件** - 使用 `read_file` 工具
2. **确认定义** - 仔细阅读类型定义和注释
3. **按定义编写** - 严格按照头文件定义编写代码
4. **再次检查** - 对照头文件检查代码正确性

这样可以从根本上避免类型不匹配、字段不存在等编译错误。

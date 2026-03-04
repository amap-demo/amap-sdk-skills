# 适配器必需函数与错误码

> 基于 `awk.c` 中 `AWK_CHECK_ADAPTER_FUNC` 的完整适配器要求

## 概述

SDK 初始化时会通过 `awk_check_context` 函数检查所有必需的适配器函数是否已实现。如果缺少任何必需函数，初始化将失败并返回对应的错误码。

## 初始化参数检查

在检查适配器函数之前，SDK 会先检查基本参数：

| 参数 | 错误码 | 说明 |
|------|--------|------|
| `context` | -100 | 上下文对象为空 |
| `context->key` | -101 | 高德开放平台 key 未设置 |
| `context->device_id` | -102 | 设备 ID 未设置 |
| `context->root_dir` | -103 | SDK 数据根目录未设置 |

## 渲染适配器 (render_adapter)

### 必需函数

| 函数 | 错误码 | 说明 | 必需条件 |
|------|--------|------|----------|
| `begin_drawing` | -200 | 开始绘制回调 | **始终必需** |
| `commit_drawing` | -201 | 结束绘制回调 | **始终必需** |
| `draw_point` | -202 | 绘制点回调 | **始终必需** |
| `draw_polyline` | -203 | 绘制线回调 | **始终必需** |
| `draw_polygon` | -204 | 绘制面回调 | **始终必需** |
| `draw_bitmap` | -205 | 绘制位图回调 | **始终必需** |
| `draw_color` | -206 | 绘制颜色回调 | **始终必需** |
| `draw_text` | -207 | 绘制文字回调 | **条件必需*** |
| `measure_text` | -208 | 测量文字尺寸回调 | **条件必需*** |

**条件必需说明**：
- 当 `tile_style` 为 `AWK_MAP_TILE_STYLE_GRID_AND_POI` 或 `AWK_MAP_TILE_STYLE_ROAD_AND_POI` 时，`draw_text` 和 `measure_text` 为必需函数

### 函数签名

```c
typedef struct _awk_render_adapter_t {
    void (*begin_drawing)(uint32_t map_id, awk_render_context_t context);
    void (*commit_drawing)(uint32_t map_id);
    void (*draw_point)(uint32_t map_id, awk_point_t *point, uint32_t point_size, const awk_paint_style_t *style);
    void (*draw_polyline)(uint32_t map_id, awk_point_t *points, uint32_t point_size, const awk_paint_style_t *style);
    void (*draw_polygon)(uint32_t map_id, awk_point_t *points, uint32_t point_size, const awk_paint_style_t *style);
    void (*draw_bitmap)(uint32_t map_id, awk_rect_area_t area, awk_bitmap_t bitmap, const awk_paint_style_t *style);
    void (*draw_text)(uint32_t map_id, awk_point_t center, const char *text, const awk_paint_style_t *style);
    void (*draw_color)(uint32_t map_id, awk_rect_area_t area, const awk_paint_style_t *style);
    bool (*measure_text)(uint32_t map_id, const char *text, const awk_paint_style_t *style, 
                         int32_t *width, int32_t *ascender, int32_t *descender);
} awk_render_adapter_t;
```

## 文件适配器 (file_adapter)

### 必需函数

| 函数 | 错误码 | 说明 |
|------|--------|------|
| `file_open` | -300 | 打开文件 |
| `file_close` | -301 | 关闭文件 |
| `file_read` | -302 | 读取文件 |
| `file_write` | -303 | 写入文件 |
| `file_exists` | -304 | 检查文件是否存在 |
| `file_remove` | -305 | 删除文件 |
| `file_dir_exists` | -306 | 检查目录是否存在 |
| `file_mkdir` | -307 | 创建目录 |
| `file_rmdir` | -308 | 删除目录 |
| `file_opendir` | -309 | 打开目录 |
| `file_closedir` | -310 | 关闭目录 |
| `file_readdir` | -311 | 读取目录内容 |
| `file_get_size` | -312 | 获取文件大小 |
| `file_get_last_access` | -313 | 获取文件最后访问时间 |
| `file_rename` | -314 | 重命名文件 |
| `file_seek` | -315 | 文件定位 |
| `file_flush` | -316 | 刷新文件缓冲区 |

### 函数签名

```c
typedef struct _awk_file_adapter_t {
    void*  (*file_open)(const char *filename, const char *mode);
    int    (*file_close)(void* handler);
    size_t (*file_read)(void *ptr, size_t size, void* handler);
    size_t (*file_write)(void *ptr, size_t size, void* handler);
    long   (*file_tell)(void *handler);
    int    (*file_seek)(void *handler, long offset, int where);
    int    (*file_flush)(void *handler);
    bool   (*file_exists)(const char *path);
    int    (*file_remove)(const char *path);
    bool   (*file_dir_exists)(const char *path);
    int    (*file_mkdir)(const char *path, uint16_t model);
    int    (*file_rmdir)(const char *path);
    void*  (*file_opendir)(const char *path);
    int    (*file_closedir)(void *dir);
    bool   (*file_readdir)(void *dir, awk_readdir_result *result);
    size_t (*file_get_size)(const char *path);
    long   (*file_get_last_access)(const char *path);
    int    (*file_rename)(const char *old_name, const char *new_name);
    bool   (*file_unzip)(const char *zip_file, const char *out_dir);
} awk_file_adapter_t;
```

## 内存适配器 (memory_adapter)

### 必需函数

| 函数 | 错误码 | 说明 |
|------|--------|------|
| `mem_malloc` | -400 | 分配内存 |
| `mem_free` | -401 | 释放内存 |
| `mem_calloc` | -402 | 分配并清零内存 |
| `mem_realloc` | -403 | 重新分配内存 |

### 函数签名

```c
typedef struct _awk_memory_adapter_t {
    void  (*mem_free)(void* ptr);
    void* (*mem_malloc)(size_t size);
    void* (*mem_calloc)(size_t count, size_t size);
    void* (*mem_realloc)(void* ptr, size_t size);
} awk_memory_adapter_t;
```

## 系统适配器 (system_adapter)

### 必需函数

| 函数 | 错误码 | 说明 |
|------|--------|------|
| `get_system_time` | -500 | 获取系统时间（毫秒） |
| `log_printf` | -501 | 日志输出 |

### 函数签名

```c
typedef struct _awk_system_adapter_t {
    uint64_t (*get_system_time)(void);
    int (*log_printf)(const char* __fmt, ...);
} awk_system_adapter_t;
```

## 网络适配器 (network_adapter)

### 必需函数

| 函数 | 错误码 | 说明 |
|------|--------|------|
| `send` | -600 | 发送 HTTP 请求 |
| `cancel` | -601 | 取消 HTTP 请求 |

### 函数签名

```c
typedef struct _awk_network_adapter_t {
    uint64_t (*send)(awk_http_request_t *request, awk_http_response_callback_t *callback);
    void (*cancel)(uint64_t request_id);
} awk_network_adapter_t;
```

**重要说明**：
- 网络请求可以在异步线程中处理
- 但回调 SDK 时**必须切回主线程**

## 线程适配器 (thread_adapter)

### 必需函数

| 函数 | 错误码 | 说明 |
|------|--------|------|
| `get_thread_id` | -701 | 获取当前线程 ID |

### 函数签名

```c
typedef struct _awk_thread_adapter_t {
    uint64_t (*get_thread_id)(void);
} awk_thread_adapter_t;
```

## 瓦片文件适配器 (tile_file_adapter)

### 必需函数

| 函数 | 错误码 | 说明 | 必需条件 |
|------|--------|------|----------|
| `on_tile_file` | -800 | 加载瓦片文件回调 | **条件必需*** |

**条件必需说明**：
- 当 `tile_style` 为 `AWK_MAP_TILE_STYLE_GRID_AND_POI` 或 `AWK_MAP_TILE_STYLE_ROAD_AND_POI` 时为必需函数

### 函数签名

```c
typedef struct _awk_map_tile_file_adapter_t {
    bool (*on_tile_file)(const char* tile_file_key, char *file_path, size_t *file_offset, size_t *file_size);
} awk_map_tile_file_adapter_t;
```

## 完整错误码列表

### 基本参数错误 (-100 ~ -103)

| 错误码 | 说明 |
|--------|------|
| -100 | 上下文对象为空 |
| -101 | 高德开放平台 key 未设置 |
| -102 | 设备 ID 未设置 |
| -103 | SDK 数据根目录未设置 |

### 渲染适配器错误 (-200 ~ -208)

| 错误码 | 缺失函数 |
|--------|----------|
| -200 | `render_adapter.begin_drawing` |
| -201 | `render_adapter.commit_drawing` |
| -202 | `render_adapter.draw_point` |
| -203 | `render_adapter.draw_polyline` |
| -204 | `render_adapter.draw_polygon` |
| -205 | `render_adapter.draw_bitmap` |
| -206 | `render_adapter.draw_color` |
| -207 | `render_adapter.draw_text` (条件必需) |
| -208 | `render_adapter.measure_text` (条件必需) |

### 文件适配器错误 (-300 ~ -316)

| 错误码 | 缺失函数 |
|--------|----------|
| -300 | `file_adapter.file_open` |
| -301 | `file_adapter.file_close` |
| -302 | `file_adapter.file_read` |
| -303 | `file_adapter.file_write` |
| -304 | `file_adapter.file_exists` |
| -305 | `file_adapter.file_remove` |
| -306 | `file_adapter.file_dir_exists` |
| -307 | `file_adapter.file_mkdir` |
| -308 | `file_adapter.file_rmdir` |
| -309 | `file_adapter.file_opendir` |
| -310 | `file_adapter.file_closedir` |
| -311 | `file_adapter.file_readdir` |
| -312 | `file_adapter.file_get_size` |
| -313 | `file_adapter.file_get_last_access` |
| -314 | `file_adapter.file_rename` |
| -315 | `file_adapter.file_seek` |
| -316 | `file_adapter.file_flush` |

### 内存适配器错误 (-400 ~ -403)

| 错误码 | 缺失函数 |
|--------|----------|
| -400 | `memory_adapter.mem_malloc` |
| -401 | `memory_adapter.mem_free` |
| -402 | `memory_adapter.mem_calloc` |
| -403 | `memory_adapter.mem_realloc` |

### 系统适配器错误 (-500 ~ -501)

| 错误码 | 缺失函数 |
|--------|----------|
| -500 | `system_adapter.get_system_time` |
| -501 | `system_adapter.log_printf` |

### 网络适配器错误 (-600 ~ -601)

| 错误码 | 缺失函数 |
|--------|----------|
| -600 | `network_adapter.send` |
| -601 | `network_adapter.cancel` |

### 线程适配器错误 (-701)

| 错误码 | 缺失函数 |
|--------|----------|
| -701 | `thread_adapter.get_thread_id` |

### 瓦片文件适配器错误 (-800)

| 错误码 | 缺失函数 |
|--------|----------|
| -800 | `tile_file_adapter.on_tile_file` (条件必需) |

## 检查流程

SDK 初始化时的检查流程如下：

```c
int32_t awk_init(awk_context_t *context) {
    // 1. 检查是否已初始化
    if (s_inited) {
        return -1;
    }

    // 2. 检查上下文和适配器
    int32_t re = awk_check_context(context);
    if (re != 0) {
        return re;  // 返回具体的错误码
    }

    // 3. 继续初始化流程
    // ...
}
```

## 最佳实践

### 1. 初始化前检查

```c
awk_context_t context = {0};

// 设置基本参数
context.key = "your_amap_key";
context.device_id = "your_device_id";
context.root_dir = "/path/to/sdk/data";

// 设置所有必需的适配器函数
context.render_adapter.begin_drawing = my_begin_drawing;
context.render_adapter.commit_drawing = my_commit_drawing;
// ... 设置其他所有必需函数

// 初始化
int32_t ret = awk_init(&context);
if (ret != 0) {
    // 根据错误码定位问题
    switch (ret) {
        case -100:
            printf("错误：上下文对象为空\n");
            break;
        case -101:
            printf("错误：未设置高德开放平台 key\n");
            break;
        case -200:
            printf("错误：未实现 render_adapter.begin_drawing\n");
            break;
        // ... 处理其他错误码
        default:
            printf("初始化失败，错误码：%d\n", ret);
    }
}
```

### 2. 条件必需函数处理

```c
// 如果使用带 POI 的瓦片样式
if (context.tile_style == AWK_MAP_TILE_STYLE_GRID_AND_POI ||
    context.tile_style == AWK_MAP_TILE_STYLE_ROAD_AND_POI) {
    // 必须实现文字相关函数
    context.render_adapter.draw_text = my_draw_text;
    context.render_adapter.measure_text = my_measure_text;
    
    // 必须实现瓦片文件加载函数
    context.tile_file_adapter.on_tile_file = my_on_tile_file;
}
```

### 3. 错误处理建议

```c
const char* get_error_message(int32_t error_code) {
    switch (error_code) {
        case -100: return "上下文对象为空";
        case -101: return "未设置高德开放平台 key";
        case -102: return "未设置设备 ID";
        case -103: return "未设置 SDK 数据根目录";
        case -200: return "未实现 render_adapter.begin_drawing";
        case -201: return "未实现 render_adapter.commit_drawing";
        // ... 添加所有错误码的描述
        default: return "未知错误";
    }
}
```

## 注意事项

1. **所有必需函数都必须实现**，否则初始化会失败
2. **条件必需函数**根据 `tile_style` 决定是否必需
3. **线程安全**：所有 SDK 方法必须在主线程调用
4. **网络回调**：网络请求可异步处理，但回调 SDK 时必须切回主线程
5. **错误码范围**：
   - -100 ~ -103：基本参数错误
   - -200 ~ -299：渲染适配器错误
   - -300 ~ -399：文件适配器错误
   - -400 ~ -499：内存适配器错误
   - -500 ~ -599：系统适配器错误
   - -600 ~ -699：网络适配器错误
   - -700 ~ -799：线程适配器错误
   - -800 ~ -899：瓦片文件适配器错误

## 相关文档

- [适配器实现](../api/adapters.md) - 适配器实现示例
- [iOS 集成指南](../api/ios-integration.md) - iOS 平台适配器实现
- [错误码](error-codes.md) - 完整错误码说明

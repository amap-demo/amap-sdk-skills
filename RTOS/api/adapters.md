# 适配器实现

> SDK 通过适配器模式与平台解耦，需实现以下适配器

## 适配器概览

| 适配器 | 作用 | 必需 |
|--------|------|------|
| `memory_adapter` | 内存管理 | ✓ |
| `file_adapter` | 文件 I/O | ✓ |
| `system_adapter` | 系统服务 | ✓ |
| `network_adapter` | HTTP 请求 | ✓ |
| `render_adapter` | 地图绘制 | ✓ |
| `thread_adapter` | 线程管理 | ✓ |

---

## 内存适配器

```c
typedef struct {
    void* (*mem_malloc)(size_t size);
    void  (*mem_free)(void* ptr);
    void* (*mem_calloc)(size_t count, size_t size);
    void* (*mem_realloc)(void* ptr, size_t size);
} awk_memory_adapter_t;
```

### POSIX 实现示例

```c
static void* awk_mem_malloc_adapter(size_t size) {
    return malloc(size);
}

static void awk_mem_free_adapter(void* ptr) {
    free(ptr);
}

static void* awk_mem_calloc_adapter(size_t count, size_t size) {
    return calloc(count, size);
}

static void* awk_mem_realloc_adapter(void* ptr, size_t size) {
    return realloc(ptr, size);
}
```

---

## 文件适配器

```c
typedef struct {
    void*  (*file_open)(const char *filename, const char *mode);
    int    (*file_close)(void* handler);
    size_t (*file_read)(void *ptr, size_t size, void* handler);
    size_t (*file_write)(void *ptr, size_t size, void* handler);
    int    (*file_seek)(void *handler, long offset, int where);
    int    (*file_flush)(void *handler);
    bool   (*file_exists)(const char *path);
    bool   (*file_dir_exists)(const char *path);
    int    (*file_mkdir)(const char *path, uint16_t mode);
    int    (*file_remove)(const char *path);
    int    (*file_rmdir)(const char *path);
    void*  (*file_opendir)(const char *path);
    int    (*file_closedir)(void *dir);
    void   (*file_readdir)(void *dir, awk_file_dir_foreach foreach, void *user_data);
    size_t (*file_get_size)(const char *path);
    long   (*file_get_last_access)(const char *path);
    int    (*file_rename)(const char *old_name, const char *new_name);
    int    (*file_unzip)(const char *zip_path, const char *dest_path);
} awk_file_adapter_t;
```

### POSIX 实现示例

```c
static void* awk_file_open_adapter(const char *filename, const char *mode) {
    return (void*)fopen(filename, mode);
}

static int awk_file_close_adapter(void* handler) {
    return fclose((FILE*)handler);
}

static size_t awk_file_read_adapter(void *ptr, size_t size, void* handler) {
    return fread(ptr, size, 1, (FILE*)handler);
}

static size_t awk_file_write_adapter(void *ptr, size_t size, void* handler) {
    return fwrite(ptr, size, 1, (FILE*)handler);
}

static int awk_file_seek_adapter(void *handler, long offset, int where) {
    return fseek((FILE*)handler, offset, where);
}

static bool awk_file_exists_adapter(const char *path) {
    return access(path, 0) == 0;
}

static bool awk_file_dir_exists_adapter(const char *path) {
    struct stat st;
    return (stat(path, &st) == 0) && S_ISDIR(st.st_mode);
}

static int awk_file_mkdir_adapter(const char *path, uint16_t mode) {
    return mkdir(path, mode);
}

static void awk_file_readdir_adapter(void *dir, awk_file_dir_foreach foreach, void *user_data) {
    struct dirent *entry;
    while ((entry = readdir((DIR*)dir)) != NULL) {
        awk_file_dir_entry dir_entry = {.file_name = entry->d_name};
        foreach(dir_entry, user_data);
    }
}
```

---

## 系统适配器

```c
typedef struct {
    uint64_t (*get_system_time)(void);  // 返回毫秒级时间戳
    void (*log_printf)(const char *format, ...);
} awk_system_adapter_t;
```

### 实现示例

```c
static uint64_t awk_get_system_time_adapter(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (uint64_t)tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

static void awk_printf_adapter(const char *format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}
```

---

## 网络适配器

```c
typedef struct {
    void (*send)(awk_network_request_t *request, awk_network_callback callback);
    void (*cancel)(int32_t request_id);
} awk_network_adapter_t;
```

**注意**：网络回调可在异步线程处理，但回调 SDK 时必须切回主线程。

---

## 渲染适配器

```c
typedef struct {
    void (*begin_drawing)(uint32_t map_id, awk_render_context_t context);
    void (*commit_drawing)(uint32_t map_id);
    void (*draw_point)(uint32_t map_id, awk_point_t *point, uint32_t size, const awk_paint_style_t *style);
    void (*draw_polyline)(uint32_t map_id, awk_point_t *points, uint32_t size, const awk_paint_style_t *style);
    void (*draw_polygon)(uint32_t map_id, awk_point_t *points, uint32_t size, const awk_paint_style_t *style);
    void (*draw_bitmap)(uint32_t map_id, awk_rect_area_t area, awk_bitmap_t bitmap, const awk_paint_style_t *style);
    void (*draw_text)(uint32_t map_id, awk_point_t center, const char *text, const awk_paint_style_t *style);
    void (*draw_color)(uint32_t map_id, awk_rect_area_t area, const awk_paint_style_t *style);
    bool (*measure_text)(uint32_t map_id, const char *text, const awk_paint_style_t *style, 
                         int32_t *width, int32_t *ascender, int32_t *descender);
} awk_render_adapter_t;
```

### 绘制流程

```
begin_drawing → draw_xxx (多次) → commit_drawing
```

### 绘制样式

```c
typedef struct {
    uint32_t width;              // 画笔宽度（像素）
    uint32_t color;              // ARGB 颜色
    float angle;                 // 旋转角度 [0-360)
    awk_text_style_t text_style; // 文字样式
    awk_fill_style_t fill_style; // 填充样式
    awk_dash_style_t dash_style; // 虚线样式
} awk_paint_style_t;
```

---

## 线程适配器

```c
typedef struct {
    uint64_t (*get_thread_id)(void);
} awk_thread_adapter_t;
```

---

## 完整配置示例

```c
awk_context_t context = {0};

// 内存适配器
context.memory_adapter.mem_malloc = awk_mem_malloc_adapter;
context.memory_adapter.mem_free = awk_mem_free_adapter;
context.memory_adapter.mem_calloc = awk_mem_calloc_adapter;
context.memory_adapter.mem_realloc = awk_mem_realloc_adapter;

// 文件适配器
context.file_adapter.file_open = awk_file_open_adapter;
context.file_adapter.file_close = awk_file_close_adapter;
context.file_adapter.file_read = awk_file_read_adapter;
context.file_adapter.file_write = awk_file_write_adapter;
// ... 其他文件操作

// 系统适配器
context.system_adapter.get_system_time = awk_get_system_time_adapter;
context.system_adapter.log_printf = awk_printf_adapter;

// 网络适配器
context.network_adapter.send = awk_network_send_adapter;
context.network_adapter.cancel = awk_network_cancel_adapter;

// 渲染适配器
context.render_adapter.begin_drawing = awk_render_begin_drawing_adapter;
context.render_adapter.commit_drawing = awk_render_commit_drawing_adapter;
context.render_adapter.draw_bitmap = awk_render_bitmap_adapter;
// ... 其他渲染操作

// 线程适配器
context.thread_adapter.get_thread_id = awk_get_thread_id_adapter;

awk_init(&context);
```

## 下一步

- [地图操作](map-operations.md) - 创建和控制地图
- [核心类型](../references/core-types.md) - 了解数据结构定义

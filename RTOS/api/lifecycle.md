# 生命周期管理

> SDK 初始化、激活、销毁的完整流程

## 生命周期流程

```
┌─────────────┐
│   awk_init  │ ← 环境初始化
└──────┬──────┘
       ▼
┌─────────────────────┐
│ awk_activate_device │ ← 设备激活（首次）
└──────┬──────────────┘
       ▼
┌─────────────────────┐
│ awk_map_create_view │ ← 创建地图
└──────┬──────────────┘
       ▼
┌─────────────────────┐
│  awk_map_do_render  │ ← 渲染循环
└──────┬──────────────┘
       ▼
┌──────────────────────┐
│ awk_map_destroy_view │ ← 销毁地图
└──────┬───────────────┘
       ▼
┌─────────────┐
│  awk_uninit │ ← 反初始化
└─────────────┘
```

## 初始化

### awk_init

```c
int32_t awk_init(awk_context_t *context);
```

**参数 `awk_context_t`：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `device_id` | char* | ✓ | 设备唯一标识 |
| `key` | char* | ✓ | 高德开放平台智能硬件 key |
| `root_dir` | char* | ✓ | SDK 内部文件夹根路径 |
| `tile_mem_cache_max_size` | uint32_t | | 瓦片内存缓存，单位：KB |
| `tile_disk_cache_max_size` | uint32_t | | 瓦片磁盘缓存，单位：MB |
| `tile_load_mode` | int32_t | | 加载模式：离线/在线/混合 |
| `tile_pixel_mode` | awk_pixel_mode_t | | 像素格式 |
| `memory_adapter` | awk_memory_adapter_t | ✓ | 内存适配器 |
| `file_adapter` | awk_file_adapter_t | ✓ | 文件适配器 |
| `network_adapter` | awk_network_adapter_t | ✓ | 网络适配器 |
| `render_adapter` | awk_render_adapter_t | ✓ | 渲染适配器 |
| `system_adapter` | awk_system_adapter_t | ✓ | 系统适配器 |

**返回值：**

| 值 | 说明 |
|----|------|
| 0 | 成功 |
| -1 | 已初始化，不能重复初始化 |
| -100 | context 为空 |
| -101 | key 为空 |
| -102 | device_id 为空 |
| -103 | root_dir 为空 |
| -2xx | render_adapter 函数指针为空 |
| -3xx | file_adapter 函数指针为空 |
| -4xx | memory_adapter 函数指针为空 |
| -5xx | system_adapter 函数指针为空 |
| -6xx | network_adapter 函数指针为空 |

### awk_uninit

```c
int32_t awk_uninit(void);
```

**返回值：**

| 值 | 说明 |
|----|------|
| 0 | 成功 |
| -1 | 未初始化 |
| -3 | 调用线程与初始化线程不一致 |

## 设备激活

### awk_activate_device

首次使用需联网激活，未激活 SDK 不可用。

```c
void awk_activate_device(
    awk_device_activate_param_t *param,
    awk_device_active_callback callback
);
```

**参数 `awk_device_activate_param_t`：**

| 字段 | 说明 |
|------|------|
| `area` | 区域：`mainland`=国内，`overseas`=海外 |
| `country` | 地图主张：`cn` |
| `type` | 0=新激活，1=恢复出厂，2=续约 |
| `data_type` | `raster`=栅格，`vector`=矢量 |

**回调：**

```c
typedef struct {
    void (*awk_device_active_on_success)(const char* license_id);
    void (*awk_device_active_on_fail)(int code, const char* msg);
} awk_device_active_callback;
```

**错误码：**

| 码 | 说明 |
|----|------|
| 30046 | license 数量超限 |
| 30047 | license 已存在 |
| 30048 | license 已禁用 |
| 30049 | license 超过有效期 |

### awk_check_device_activated

检查设备是否已激活：

```c
bool awk_check_device_activated(
    awk_device_activate_param_t *param,
    awk_context_t *context
);
```

## 缓存管理

### 清除磁盘缓存

```c
int32_t awk_clear_disk_cache(void);
```

### 清除内存缓存

```c
int32_t awk_clear_memory_cache(awk_memory_cache_type_t type);
```

**缓存类型：**

| 值 | 说明 |
|----|------|
| `AWK_MEMORY_CACHE_TYPE_TILE` | 瓦片缓存 |
| `AWK_MEMORY_CACHE_TYPE_POI` | POI 缓存 |

## 线程模型

⚠️ **重要约束**：

1. SDK 为**单线程模型**
2. 所有方法必须在**同一主流程线程**调用
3. 网络回调可在异步线程处理，但回调 SDK 时必须切回主线程
4. 并发调用可能导致异常

## 下一步

- [适配器实现](adapters.md) - 实现平台适配器
- [地图操作](map-operations.md) - 创建和控制地图

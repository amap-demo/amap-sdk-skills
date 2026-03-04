# 快速开始

> 5 分钟完成 WatchSDK 接入

## 最简接入流程

```
初始化 SDK → 激活设备 → 创建地图 → 渲染循环
```

## 1. 初始化 SDK

```c
#include "awk.h"

awk_context_t context;
memset(&context, 0, sizeof(awk_context_t));

// 必填参数
context.device_id = "your_device_id";
context.key = "your_amap_key";           // 高德开放平台智能硬件 key
context.root_dir = "/path/to/sdk/data";  // SDK 内部文件夹根路径

// 缓存配置
context.tile_mem_cache_max_size = 6;     // 内存缓存，单位：KB
context.tile_disk_cache_max_size = 200;  // 磁盘缓存，单位：MB

// 设置适配器（必需）
context.memory_adapter = your_memory_adapter;
context.file_adapter = your_file_adapter;
context.system_adapter = your_system_adapter;
context.network_adapter = your_network_adapter;
context.render_adapter = your_render_adapter;
context.thread_adapter = your_thread_adapter;

int32_t result = awk_init(&context);
// result: 0=成功, 负数=错误码
```

**→ 适配器实现详见 [适配器文档](adapters.md)**

## 2. 激活设备

首次使用需联网激活：

```c
awk_device_activate_param_t param = {
    .area = "mainland",      // mainland=国内, overseas=海外
    .country = "cn",
    .type = 0,               // 0=新激活, 1=恢复出厂, 2=续约
    .data_type = "raster"    // raster=栅格, vector=矢量
};

awk_device_active_callback callback = {
    .awk_device_active_on_success = on_activate_success,
    .awk_device_active_on_fail = on_activate_fail
};

awk_activate_device(&param, callback);
```

## 3. 创建地图

```c
awk_map_view_param_t param;
param.port.width = 375;   // 地图宽度（像素）
param.port.height = 667;  // 地图高度（像素）

int32_t map_id = awk_map_create_view(param);
// map_id > 0 表示成功
```

## 4. 渲染循环

```c
// 在主循环中定时调用
while (running) {
    awk_map_do_render();
    // ... 其他逻辑
}
```

## 5. 清理资源

```c
awk_map_destroy_view(map_id);
awk_uninit();
```

## 完整示例

```c
#include "awk.h"
#include "map/awk_map.h"

int main() {
    // 1. 初始化
    awk_context_t ctx = {0};
    ctx.device_id = "device_001";
    ctx.key = "your_key";
    ctx.root_dir = "./sdk_data";
    // ... 设置适配器
    awk_init(&ctx);
    
    // 2. 激活（首次）
    awk_device_activate_param_t act = {
        .area = "mainland", .country = "cn",
        .type = 0, .data_type = "raster"
    };
    awk_activate_device(&act, callback);
    
    // 3. 创建地图
    awk_map_view_param_t vp = {.port = {375, 667}};
    uint32_t map_id = awk_map_create_view(vp);
    
    // 4. 渲染循环
    while (1) {
        awk_map_do_render();
    }
    
    // 5. 清理
    awk_map_destroy_view(map_id);
    awk_uninit();
    return 0;
}
```

## 下一步

- [生命周期详解](lifecycle.md) - 了解完整的初始化流程
- [适配器实现](adapters.md) - 实现平台适配器
- [地图操作](map-operations.md) - 控制地图显示

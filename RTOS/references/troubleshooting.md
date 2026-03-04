# 常见问题

> FAQ 与问题排查指南

## 初始化问题

### Q: 初始化返回 -1xx 错误

**原因**：必填参数缺失

**解决**：
```c
awk_context_t context;
memset(&context, 0, sizeof(awk_context_t));  // 务必先 memset

context.device_id = "xxx";  // 必填
context.key = "xxx";        // 必填
context.root_dir = "xxx";   // 必填
```

### Q: 初始化返回 -2xx/-3xx/-4xx 错误

**原因**：适配器函数指针未设置

**解决**：确保所有必需适配器的函数指针都已设置：
- `-2xx`：检查 `render_adapter`
- `-3xx`：检查 `file_adapter`
- `-4xx`：检查 `memory_adapter`
- `-5xx`：检查 `system_adapter`
- `-6xx`：检查 `network_adapter`

---

## 激活问题

### Q: 激活失败，返回 30046

**原因**：license 数量超限

**解决**：联系商务扩容或清理无用设备

### Q: 激活失败，返回 30049

**原因**：license 过期

**解决**：
1. 检查设备时间是否正确
2. 联系商务续约

### Q: 离线环境无法激活

**原因**：激活需要联网

**解决**：
1. 首次激活必须联网
2. 激活成功后可离线使用
3. 可使用 `awk_check_device_activated()` 检查激活状态

---

## 渲染问题

### Q: 地图不显示

**排查步骤**：
1. 检查 `awk_map_create_view()` 返回值是否 > 0
2. 确认 `awk_map_do_render()` 在主循环中定时调用
3. 检查 `render_adapter` 实现是否正确
4. 确认设备已激活

### Q: 地图显示异常/闪烁

**原因**：多线程调用

**解决**：确保所有 SDK 方法在同一主线程调用

### Q: 瓦片加载失败

**排查步骤**：
1. 检查网络连接（在线模式）
2. 检查离线地图路径（离线模式）
3. 检查 `network_adapter` 实现
4. 查看 `on_tile_end_download` 回调状态

---

## 覆盖物问题

### Q: 覆盖物不显示

**排查步骤**：
1. 检查 `awk_map_add_overlay()` 返回值
2. 确认坐标在当前地图可视范围内
3. 检查 `visible` 属性是否为 `true`
4. 检查 `z_index` 层级

### Q: 添加覆盖物返回 -2

**原因**：guid 重复

**解决**：确保每个覆盖物的 guid 唯一

### Q: 线/面覆盖物内存泄漏

**原因**：未释放坐标点数组

**解决**：
```c
// 添加后释放
awk_map_add_overlay(bindmap_id, bindoverlay);
free(bindoverlay->points);  // 释放坐标数组
```

---

## 导航问题

### Q: 导航数据回调不触发

**排查步骤**：
1. 确认已调用 `awk_navi_add_data_callback()`
2. 检查 `awk_navi_data()` 返回值
3. 确认 PB 数据格式正确

### Q: awk_navi_data 返回负数

| 返回值 | 处理 |
|--------|------|
| -2, -7, -20 | 重传数据 |
| -10000 | 检查数据格式 |
| -10001 | 重新初始化导航 |

### Q: 导航地图操作无效

**原因**：导航模式下内部控制地图

**解决**：导航中不要外部操作地图（缩放、旋转等）

---

## 性能问题

### Q: 内存占用过高

**解决**：
1. 减小 `tile_mem_cache_max_size`
2. 定期调用 `awk_clear_memory_cache()`
3. 减少覆盖物数量

### Q: 渲染卡顿

**解决**：
1. 降低渲染频率
2. 减少覆盖物数量
3. 使用较低的瓦片精细度 `poi_tile_density`

---

## 调试技巧

### 启用日志

```c
context.system_adapter.log_printf = my_log_function;
```

### 检查激活状态

```c
if (!awk_check_device_activated(&param, &context)) {
    // 需要激活
    awk_activate_device(&param, callback);
}
```

### 监控瓦片下载

```c
awk_map_render_callback_t cb = {
    .on_tile_end_download = on_tile_download_complete
};

void on_tile_download_complete(int32_t type, uint32_t x, uint32_t y, 
                                uint32_t zoom, awk_map_tile_response_status_t status) {
    if (status != AWK_MAP_TILE_RESPONSE_SUCCESS) {
        printf("瓦片下载失败: %d/%d/%d, status=%d\n", zoom, x, y, status);
    }
}
```

## 获取帮助

如问题仍未解决，请提供：
1. SDK 版本
2. 设备信息
3. 错误码/日志
4. 复现步骤

# 错误码说明

> SDK 返回值与错误码参考

## 通用错误码

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| -1 | 未初始化 | 先调用 `awk_init()` |
| -2 | 资源不存在 | 检查 ID 是否正确 |
| -3 | 线程不一致 | 确保在主线程调用 |
| -4 | 参数错误 | 检查参数有效性 |

---

## 初始化错误码

### awk_init 返回值

| 错误码 | 说明 |
|--------|------|
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
| -7xx | thread_adapter 函数指针为空 |
| -8xx | tile_file_adapter 函数指针为空 |

---

## 设备激活错误码

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| 30046 | license 数量超限 | 联系商务扩容 |
| 30047 | license 已存在 | 无需重复激活 |
| 30048 | license 已禁用 | 联系商务处理 |
| 30049 | license 超过有效期 | 续约 license |

---

## 地图操作错误码

### awk_map_create_view

| 返回值 | 说明 |
|--------|------|
| >0 | 成功，返回地图 ID |
| -1 | 未初始化 |
| -2 | license 校验失败 |
| -3 | 线程不一致 |

### awk_map_add_overlay

| 返回值 | 说明 |
|--------|------|
| 0 | 成功 |
| -1 | 未初始化 |
| -2 | guid 已存在 |
| -3 | overlay 为空或类型错误 |
| -4 | 线程不一致 |

### awk_map_set_level

| 返回值 | 说明 |
|--------|------|
| 0 | 成功 |
| -1 | 未初始化 |
| -3 | 线程不一致 |
| -4 | level 不合法（超出 3-20 范围）|

---

## 导航错误码

### awk_navi_data

| 返回值 | 说明 | 处理建议 |
|--------|------|----------|
| 0 | 成功 | - |
| -2 | 数据解析失败 | 重传数据 |
| -7 | 数据不完整 | 重传数据 |
| -20 | 数据校验失败 | 重传数据 |
| -10000 | 外层数据结构异常 | 检查数据格式 |
| -10001 | 反初始化后调用 | 重新初始化 |

---

## 瓦片下载状态

```c
typedef enum {
    AWK_MAP_TILE_RESPONSE_SUCCESS,      // 成功
    AWK_MAP_TILE_RESPONSE_NETWORK_ERROR, // 网络错误
    AWK_MAP_TILE_RESPONSE_NOT_FOUND,    // 瓦片不存在
    AWK_MAP_TILE_RESPONSE_TIMEOUT,      // 超时
    AWK_MAP_TILE_RESPONSE_CANCELLED,    // 已取消
} awk_map_tile_response_status_t;
```

---

## 错误处理示例

```c
int32_t result = awk_init(&context);
switch (result) {
    case 0:
        printf("初始化成功\n");
        break;
    case -1:
        printf("错误：已初始化，不能重复初始化\n");
        break;
    case -100:
        printf("错误：context 为空\n");
        break;
    case -101:
        printf("错误：key 为空\n");
        break;
    default:
        if (result <= -200 && result > -300) {
            printf("错误：render_adapter 不完整\n");
        } else if (result <= -300 && result > -400) {
            printf("错误：file_adapter 不完整\n");
        }
        break;
}
```

## 下一步

- [常见问题](troubleshooting.md) - FAQ 与问题排查

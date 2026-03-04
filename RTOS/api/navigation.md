# 导航功能

> 实时导航数据展示与控制

## 导航流程

```
awk_init_navi → awk_init_navi_view → awk_navi_data → 回调处理 → awk_uninit_navi
```

---

## 初始化

### 初始化导航

```c
int32_t awk_init_navi(awk_navi_config_t *config);
```

**配置参数：**

```c
typedef struct {
    awk_map_point_overlay_t car_overlay;  // 车标覆盖物
    // ... 其他配置
} awk_navi_config_t;
```

### 初始化导航视图

```c
int32_t awk_init_navi_view(uint32_t map_id, awk_navi_view_config_t *view_config);
```

⚠️ **注意**：导航中外部不可操作地图（旋转、缩放等），否则会与内部操作冲突。

### 反初始化

```c
int32_t awk_uninit_navi(void);
int32_t awk_uninit_navi_view(void);
```

---

## 数据回调

### 设置回调

```c
int32_t awk_navi_add_data_callback(awk_navi_data_callback_t *callback);
int32_t awk_navi_remove_data_callback(awk_navi_data_callback_t *callback);
```

### 回调结构

```c
typedef struct {
    // 路线更新
    void (*update_navi_route_group)(awk_navi_data_callback_t *cb, 
                                     awk_navi_route_group_t route_group,
                                     awk_navi_data_info_t data_info);
    
    // 导航信息更新
    void (*update_navi_info)(awk_navi_data_callback_t *cb,
                             awk_navi_info_t navi_info,
                             awk_navi_data_info_t data_info);
    
    // 自车位置更新
    void (*update_navi_location)(awk_navi_data_callback_t *cb,
                                  awk_navi_location_t location,
                                  awk_navi_data_info_t data_info);
    
    // 转向图标更新
    void (*update_turn_info)(awk_navi_data_callback_t *cb,
                             awk_navi_icon_type turn_icon_type,
                             awk_navi_data_info_t data_info);
    
    // 下一路口转向
    void (*update_next_turn_info)(awk_navi_data_callback_t *cb,
                                   awk_navi_icon_type turn_icon_type,
                                   awk_navi_data_info_t data_info);
    
    // 后方来车提醒
    void (*show_rear_appr_vehicle)(awk_navi_data_callback_t *cb,
                                    awk_navi_rear_vehicle_info_t info,
                                    awk_navi_data_info_t data_info);
    void (*hide_rear_appr_vehicle)(awk_navi_data_callback_t *cb,
                                    awk_navi_data_info_t data_info);
    
    // 红绿灯倒计时
    void (*show_traffic_signal)(awk_navi_data_callback_t *cb,
                                 awk_navi_traffic_signal_info_t info,
                                 awk_navi_data_info_t data_info);
    void (*hide_traffic_signal)(awk_navi_data_callback_t *cb,
                                 awk_navi_data_info_t data_info);
    
    // 车道线信息
    void (*show_lane_info)(awk_navi_data_callback_t *cb,
                           awk_navi_lane_info_t lane_info,
                           awk_navi_data_info_t data_info);
    void (*hide_lane_info)(awk_navi_data_callback_t *cb,
                           awk_navi_data_info_t data_info);
} awk_navi_data_callback_t;
```

---

## 事件回调

```c
int32_t awk_navi_add_event_callback(awk_navi_event_callback_t *callback);
int32_t awk_navi_remove_event_callback(awk_navi_event_callback_t *callback);
```

```c
typedef struct {
    void (*on_arrived_destination)(awk_navi_event_callback_t *cb);
    void (*on_reset)(awk_navi_event_callback_t *cb);
} awk_navi_event_callback_t;
```

---

## 导航数据输入

```c
int32_t awk_navi_data(const uint8_t *data, size_t len);
```

传入导航 PB 数据，内部解析。

**返回值：**

| 值 | 说明 |
|----|------|
| 0 | 成功 |
| -10000 | 数据结构异常 |
| -10001 | 反初始化后调用 |
| -2, -7, -20 | 需重传数据 |

---

## 显示控制

### 跟随模式

```c
int32_t awk_navi_set_tracking_mode(awk_navi_tracking_mode_type mode);
```

| 模式 | 说明 |
|------|------|
| 北朝上 | 地图始终北朝上 |
| 车头朝上 | 地图随车头方向旋转 |

### 显示模式

```c
int32_t awk_navi_set_show_mode(awk_navi_show_mode_type mode);
```

| 模式 | 说明 |
|------|------|
| 锁车状态 | 跟随车辆 |
| 全览状态 | 显示完整路线 |
| 普通状态 | 自由浏览 |

### UI 元素显示

```c
int32_t awk_navi_show_ui_elements(bool show);
```

控制除底图和路线外的所有 UI 元素。

---

## 车标控制

### 自动旋转

```c
int32_t awk_navi_should_autorotate_car(bool should_autorotate);
```

### 手动设置角度

```c
int32_t awk_navi_set_car_angle(float angle);
```

- 需先设置 `awk_navi_should_autorotate_car(false)`
- 角度：0=北，90=东，180=南，270=西

---

## 状态查询

### 是否导航中

```c
bool awk_navi_is_navigating(void);
```

### 获取地图 ID

```c
int32_t awk_navi_get_map_id(void);
```

---

## 完整示例

```c
// 1. 初始化导航
awk_navi_config_t config = {0};
awk_init_navi(&config);

// 2. 设置回调
awk_navi_data_callback_t data_cb = {
    .update_navi_info = on_navi_info_update,
    .update_navi_location = on_location_update,
    .update_turn_info = on_turn_info_update
};
awk_navi_add_data_callback(&data_cb);

// 3. 初始化导航视图
awk_navi_view_config_t view_config = {0};
awk_init_navi_view(map_id, &view_config);

// 4. 接收导航数据
awk_navi_data(pb_data, pb_len);

// 5. 清理
awk_uninit_navi_view();
awk_uninit_navi();
```

## 下一步

- [核心类型](../references/core-types.md) - 导航相关数据结构
- [错误码](../references/error-codes.md) - 错误处理

# 地图操作

> 创建、控制、渲染地图

## 创建与销毁

### 创建地图

```c
int32_t awk_map_create_view(awk_map_view_param_t param);
```

**参数：**

```c
typedef struct {
    awk_map_view_port_t port;  // 视口大小
} awk_map_view_param_t;

typedef struct {
    int32_t width;   // 宽度（像素）
    int32_t height;  // 高度（像素）
} awk_map_view_port_t;
```

**返回值：**

| 值 | 说明 |
|----|------|
| >0 | 地图实例 ID |
| -1 | 未初始化 |
| -2 | license 校验失败 |
| -3 | 线程不一致 |

**示例：**

```c
awk_map_view_param_t param;
param.port.width = 375;
param.port.height = 667;

int32_t map_id = awk_map_create_view(param);
if (map_id > 0) {
    // 创建成功
}
```

### 销毁地图

```c
int32_t awk_map_destroy_view(uint32_t map_id);
```

---

## 渲染控制

### 执行渲染

```c
int32_t awk_map_do_render(void);
```

需在主循环中定时调用。

### 暂停/恢复渲染

```c
int32_t awk_map_pause_render(uint32_t map_id);
int32_t awk_map_resume_render(uint32_t map_id);
```

---

## 地图状态控制

### 设置中心点

```c
int32_t awk_map_set_center(uint32_t map_id, awk_map_coord2d_t center);
```

```c
awk_map_coord2d_t center = {
    .lon = 116.397428,  // 经度
    .lat = 39.90923     // 纬度
};
awk_map_set_center(map_id, center);
```

### 设置缩放级别

```c
int32_t awk_map_set_level(uint32_t map_id, float level);
```

- 范围：3-20
- 可通过 `limit_min_zoom` / `limit_max_zoom` 限制

### 设置旋转角度

```c
int32_t awk_map_set_roll_angle(uint32_t map_id, float angle);
```

- 范围：0-360
- 0 度为正北

### 获取地图状态

```c
int32_t awk_map_get_posture(uint32_t map_id, awk_map_posture_t *posture);
```

```c
typedef struct {
    awk_map_coord2d_t center;  // 中心点
    float level;               // 缩放级别
    float roll_angle;          // 旋转角度
} awk_map_posture_t;
```

---

## 手势操作

```c
// 手势开始
int32_t awk_map_touch_begin(uint32_t map_id, int32_t x, int32_t y);

// 手势移动
int32_t awk_map_touch_update(uint32_t map_id, int32_t x, int32_t y);

// 手势结束
int32_t awk_map_touch_end(uint32_t map_id, int32_t x, int32_t y);
```

---

## 坐标转换

### 经纬度 → 屏幕坐标

```c
int32_t awk_map_lonlat_to_xy(uint32_t map_id, awk_map_coord2d_t lonlat, int32_t *x, int32_t *y);
```

### 屏幕坐标 → 经纬度

```c
int32_t awk_map_xy_to_lonlat(uint32_t map_id, int32_t x, int32_t y, awk_map_coord2d_t *lonlat);
```

### 计算两点距离

```c
double awk_map_calc_points_distance(double lon1, double lat1, double lon2, double lat2);
```

返回距离，单位：米。

---

## 渲染回调

```c
typedef struct {
    // 覆盖物绘制回调
    bool (*on_point_begin_draw)(uint32_t map_id, int32_t guid);
    void (*on_point_end_draw)(uint32_t map_id, int32_t guid, int32_t status);
    bool (*on_line_begin_draw)(uint32_t map_id, int32_t guid);
    void (*on_line_end_draw)(uint32_t map_id, int32_t guid, int32_t status);
    bool (*on_polygon_begin_draw)(uint32_t map_id, int32_t guid);
    void (*on_polygon_end_draw)(uint32_t map_id, int32_t guid, int32_t status);
    
    // 瓦片绘制回调
    bool (*on_tile_begin_draw)(uint32_t map_id, uint32_t tile_x, uint32_t tile_y, uint32_t zoom);
    void (*on_tile_end_draw)(uint32_t map_id, uint32_t tile_x, uint32_t tile_y, uint32_t zoom, int32_t status);
    
    // 瓦片下载回调
    bool (*on_tile_begin_download)(int32_t type, uint32_t tile_x, uint32_t tile_y, uint32_t zoom);
    void (*on_tile_end_download)(int32_t type, uint32_t tile_x, uint32_t tile_y, uint32_t zoom, awk_map_tile_response_status_t status);
} awk_map_render_callback_t;
```

## 下一步

- [覆盖物](overlays.md) - 添加点/线/面标注
- [导航](navigation.md) - 导航功能接入

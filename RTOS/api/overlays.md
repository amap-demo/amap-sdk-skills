# 覆盖物

> 点/线/面覆盖物的创建与管理

## 覆盖物类型

| 类型 | 结构体 | 用途 |
|------|--------|------|
| 点 | `awk_map_point_overlay_t` | 标记位置、POI |
| 线 | `awk_map_polyline_overlay_t` | 路径、轨迹 |
| 面 | `awk_map_polygon_overlay_t` | 区域、范围 |

---

## 点覆盖物

### 创建

```c
// 1. 初始化
awk_map_point_overlay_t point;
awk_map_init_point_overlay(&point);

// 2. 设置位置
point.position.lon = 116.397428;
point.position.lat = 39.90923;

// 3. 设置图标（可选）
point.normal_marker.icon_texture.texture_id = texture_id;
point.normal_marker.icon_texture.scale = 0.8f;

// 4. 添加到地图
awk_map_add_overlay(map_id, (awk_map_base_overlay_t *)&point);
```

### 纹理管理

```c
// 添加纹理
awk_map_texture_data_t texture = {
    .pixel_mode = AWK_PIXEL_MODE_ARGB_8888,
    .buffer = image_data,
    .buffer_size = data_size,
    .width = 32,
    .height = 32
};
int32_t texture_id = awk_map_add_texture(&texture);

// 更新纹理
awk_map_update_texture(texture_id, &new_texture);

// 移除纹理
awk_map_remove_texture(texture_id);
```

---

## 线覆盖物

### 创建

```c
// 1. 初始化
awk_map_polyline_overlay_t line;
awk_map_init_line_overlay(&line);

// 2. 设置坐标点
line.point_size = 3;
line.points = malloc(sizeof(awk_map_coord2d_t) * 3);
line.points[0] = (awk_map_coord2d_t){116.397428, 39.90923};
line.points[1] = (awk_map_coord2d_t){116.407428, 39.91923};
line.points[2] = (awk_map_coord2d_t){116.417428, 39.92923};

// 3. 设置样式
line.normal_marker.line_width = 4;           // 线宽（像素）
line.normal_marker.line_color = 0xFFFF0000;  // ARGB: 红色
line.normal_marker.border_width = 2;         // 边框宽度
line.normal_marker.border_color = 0xFFFFFFFF; // ARGB: 白色

// 4. 添加到地图
awk_map_bindadd_overlay(map_id, (awk_map_base_overlay_t *)&line);

// 5. 释放内存
free(line.points);
```

### 虚线样式

```c
line.normal_marker.dash_style.painted_length = 10;   // 绘制长度
line.normal_marker.dash_style.unpainted_length = 5;  // 空白长度
line.normal_marker.dash_style.offset = 0;            // 起始偏移
```

---

## 面覆盖物

### 创建

```c
// 1. 初始化
awk_map_polygon_overlay_t polygon;
awk_map_init_polygon_overlay(&polygon);

// 2. 设置坐标点（至少3个点）
polygon.point_size = 4;
polygon.points = malloc(sizeof(awk_map_coord2d_t) * 4);
polygon.points[0] = (awk_map_coord2d_t){116.397428, 39.90923};
polygon.points[1] = (awk_map_coord2d_t){116.407428, 39.90923};
polygon.points[2] = (awk_map_coord2d_t){116.407428, 39.91923};
polygon.points[3] = (awk_map_coord2d_t){116.397428, 39.91923};

// 3. 设置填充颜色
polygon.color = 0x80FF0000;  // ARGB: 半透明红色

// 4. 添加到地图
awk_map_bindadd_overlay(map_id, (awk_map_base_overlay_t *)&polygon);

// 5. 释放内存
free(polygon.points);
```

---

## 覆盖物管理

### 添加

```c
int32_t awk_map_add_overlay(uint32_t map_id, awk_map_base_overlay_t *overlay);
```

**返回值：**

| 值 | 说明 |
|----|------|
| 0 | 成功 |
| -1 | 未初始化 |
| -2 | guid 已存在 |
| -3 | overlay 为空或类型错误 |
| -4 | 线程不一致 |

### 移除

```c
int32_t awk_map_remove_overlay(uint32_t map_id, int32_t overlay_id);
```

### 查找

```c
const awk_map_base_overlay_t* awk_map_find_overlay(uint32_t map_id, int32_t overlay_id);
```

### 获取数量

```c
uint32_t awk_map_get_overlay_count(uint32_t map_id);
```

### 按索引获取

```c
const awk_map_base_overlay_t* awk_map_get_overlay(uint32_t map_id, uint32_t index);
```

---

## 颜色格式

所有颜色使用 **ARGB** 格式（32位）：

```
0xAARRGGBB
  │ │ │ └─ 蓝色 (0-255)
  │ │ └─── 绿色 (0-255)
  │ └───── 红色 (0-255)
  └─────── 透明度 (0=透明, 255=不透明)
```

**示例：**

| 颜色 | 值 |
|------|-----|
| 不透明红色 | `0xFFFF0000` |
| 半透明蓝色 | `0x800000FF` |
| 不透明白色 | `0xFFFFFFFF` |
| 不透明黑色 | `0xFF000000` |

## 下一步

- [导航](navigation.md) - 导航功能接入
- [核心类型](../references/core-types.md) - 数据结构定义

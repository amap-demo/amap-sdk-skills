# 核心类型定义

> 关键数据结构参考

## 基础类型

### 坐标点

```c
// 经纬度坐标（GCJ02）
typedef struct {
    double lon;  // 经度
    double lat;  // 纬度
} awk_map_coord2d_t;

// 屏幕坐标（左上角为原点）
typedef struct {
    float x;
    float y;
} awk_point_t;
```

### 矩形区域

```c
typedef struct {
    float x;       // 左上角 x
    float y;       // 左上角 y
    float width;   // 宽度（像素）
    float height;  // 高度（像素）
} awk_rect_area_t;
```

### 位图

```c
typedef struct {
    awk_pixel_mode_t pixel_mode;  // 像素格式
    uint8_t *buffer;              // 数据缓冲区
    uint32_t buffer_size;         // 缓冲区大小
    uint32_t width;               // 宽度（像素）
    uint32_t height;              // 高度（像素）
    uint32_t stride;              // 每像素字节数
    bool pre_multiplied;          // 是否预乘 alpha
} awk_bitmap_t;
```

---

## 像素格式

```c
typedef enum {
    AWK_PIXEL_MODE_GREY,       // 8位灰度
    AWK_PIXEL_MODE_RGB_332,    // 8位 RGB
    AWK_PIXEL_MODE_RGB_565,    // 16位 RGB
    AWK_PIXEL_MODE_RGB_888,    // 24位 RGB
    AWK_PIXEL_MODE_ARGB_8888,  // 32位 ARGB
    AWK_PIXEL_MODE_RGBA_8888,  // 32位 RGBA
    AWK_PIXEL_MODE_BGR_233,    // 8位 BGR
    AWK_PIXEL_MODE_BGR_565,    // 16位 BGR
    AWK_PIXEL_MODE_BGR_888,    // 24位 BGR
    AWK_PIXEL_MODE_BGRA_8888,  // 32位 BGRA
    AWK_PIXEL_MODE_ABGR_8888,  // 32位 ABGR
} awk_pixel_mode_t;
```

**字节顺序说明：**

| 格式 | 字节数 | 字节顺序 |
|------|--------|----------|
| RGB_565 | 2 | 字节0: G[2:0]+B[4:0], 字节1: R[4:0]+G[5:3] |
| RGB_888 | 3 | R, G, B |
| ARGB_8888 | 4 | A, R, G, B |
| RGBA_8888 | 4 | R, G, B, A |

---

## 地图相关

### 地图视口

```c
typedef struct {
    int32_t width;
    int32_t height;
} awk_map_view_port_t;

typedef struct {
    awk_map_view_port_t port;
} awk_map_view_param_t;
```

### 地图姿态

```c
typedef struct {
    awk_map_coord2d_t center;  // 中心点
    float level;               // 缩放级别 (3-20)
    float roll_angle;          // 旋转角度 (0-360)
} awk_map_posture_t;
```

### 瓦片加载模式

```c
typedef enum {
    AWK_MAP_TILE_LOAD_MODE_OFFLINE,  // 离线
    AWK_MAP_TILE_LOAD_MODE_ONLINE,   // 在线
    AWK_MAP_TILE_LOAD_MODE_MIXED,    // 混合
} awk_map_tile_load_mode_t;
```

### 瓦片样式

```c
typedef enum {
    AWK_MAP_TILE_STYLE_NORMAL,  // 标准
    AWK_MAP_TILE_STYLE_DARK,    // 暗色
} awk_map_tile_style_t;
```

---

## 覆盖物相关

### 基础覆盖物

```c
typedef struct {
    int32_t guid;                    // 唯一标识
    awk_map_geometry_type_t type;    // 几何类型
    int32_t z_index;                 // 层级
    bool visible;                    // 是否可见
} awk_map_base_overlay_t;
```

### 点覆盖物

```c
typedef struct {
    awk_map_base_overlay_t base;
    awk_map_coord2d_t position;           // 位置
    awk_map_point_marker_t normal_marker; // 普通状态样式
    awk_map_point_marker_t selected_marker; // 选中状态样式
} awk_map_point_overlay_t;
```

### 线覆盖物

```c
typedef struct {
    awk_map_base_overlay_t base;
    awk_map_coord2d_t *points;        // 坐标点数组
    uint32_t point_size;              // 点数量
    awk_map_line_marker_t normal_marker;
} awk_map_polyline_overlay_t;
```

### 面覆盖物

```c
typedef struct {
    awk_map_base_overlay_t base;
    awk_map_coord2d_t *points;  // 坐标点数组
    uint32_t point_size;        // 点数量
    uint32_t color;             // 填充颜色 (ARGB)
} awk_map_polygon_overlay_t;
```

---

## 绘制样式

### 画笔样式

```c
typedef struct {
    uint32_t width;              // 画笔宽度（像素）
    uint32_t color;              // 颜色 (ARGB)
    float angle;                 // 旋转角度 [0-360)
    awk_text_style_t text_style;
    awk_fill_style_t fill_style;
    awk_dash_style_t dash_style;
} awk_paint_style_t;
```

### 文字样式

```c
typedef struct {
    awk_align_style_t align;     // 对齐方式
    uint32_t font_size;          // 字号
    awk_font_weight_t font_weight; // 字重
} awk_text_style_t;

typedef enum {
    AWK_ALIGN_STYLE_NONE,
    AWK_ALIGN_STYLE_CENTER,
    AWK_ALIGN_STYLE_LEFT,
    AWK_ALIGN_STYLE_RIGHT
} awk_align_style_t;

typedef enum {
    AWK_FONT_WEIGHT_NORMAL,
    AWK_FONT_WEIGHT_THIN,
    AWK_FONT_WEIGHT_BOLD
} awk_font_weight_t;
```

### 虚线样式

```c
typedef struct {
    int32_t painted_length;    // 绘制长度（像素）
    int32_t unpainted_length;  // 空白长度（像素）
    int32_t offset;            // 起始偏移
} awk_dash_style_t;
```

### 填充样式

```c
typedef enum {
    AWK_FILL_STYLE_DRAWING_ONLY,        // 仅填充
    AWK_FILL_STYLE_DRAWING_AND_STROKE,  // 填充+描边
    AWK_FILL_STYLE_STROKE_ONLY          // 仅描边
} awk_fill_style_t;
```

---

## 导航相关

### 导航信息

```c
typedef struct {
    awk_navi_mode_t navi_mode;     // 导航模式
    uint32_t remain_distance;      // 剩余距离（米）
    uint32_t remain_time;          // 剩余时间（秒）
    // ...
} awk_navi_info_t;
```

### 导航位置

```c
typedef struct {
    awk_map_coord2d_t position;  // 当前位置
    float speed;                 // 速度
    float direction;             // 方向
} awk_navi_location_t;
```

### 转向图标类型

```c
typedef enum {
    AWK_NAVI_ICON_STRAIGHT,      // 直行
    AWK_NAVI_ICON_TURN_LEFT,     // 左转
    AWK_NAVI_ICON_TURN_RIGHT,    // 右转
    AWK_NAVI_ICON_UTURN,         // 掉头
    // ...
} awk_navi_icon_type;
```

## 下一步

- [错误码](error-codes.md) - 错误码说明
- [常见问题](troubleshooting.md) - FAQ

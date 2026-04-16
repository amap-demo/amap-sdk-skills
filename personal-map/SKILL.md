---
name: personal-map
description: 高德地图个人专属地图生成工具。封装了高德开放平台的Web服务API，提供地理编码、POI搜索、路径规划、周边搜索、天气查询等能力，最终生成可在高德地图App中打开的个人地图小程序二维码。当用户提到以下任意场景时，都应主动使用本技能：查找附近的餐厅/景点/商场等POI、规划从A到B的路线（步行/驾车/公交/骑行）、生成旅游行程/出行计划/打卡地图、在地图上标记多个地点、分享地图给他人、查询某地天气、将地址转换为坐标或反向解析、制作个人专属地图、行程规划、路线规划、地图分享。即使用户没有明确说"生成地图"，只要涉及地理位置、出行、导航、打卡、行程等话题，都应考虑使用本技能。
---

# 高德个人地图 Skill

## 概述

本 Skill 封装了高德开放平台的 Web 服务 API，提供地理编码、POI 搜索、路径规划等核心能力，根据用户描述生成个人专属地图，并支持在高德地图 App 中扫码打开。

**重要**：所有调用此技能的会话，最终都应调用 `maps_schema_personal_map` 生成个人地图二维码，并通过以下方式展示给用户：
1. **下载二维码图片到本地**（推荐保存到工作目录）
2. **使用 `present` 工具展示图片**
3. **在回复中直接嵌入 Markdown 图片**（双重保障）
4. **提供备用 URL 链接**（防止图片展示失败）

这样可以确保用户能够可靠地看到并保存二维码。

## 接口说明

### 1. 地理编码

- **`maps_geo`**：地址 → 经纬度坐标
  - 参数：`address`（详细地址）、`city`（城市，可选）
  - 返回：经纬度坐标、格式化地址

- **`maps_regeocode`**：经纬度坐标 → 结构化地址
  - 参数：`longitude`（经度）、`latitude`（纬度）
  - 返回：国家、省份、城市、区县等完整地址信息

### 2. POI 搜索

- **`maps_text_search`**：关键词搜索兴趣点
  - 参数：`keywords`（搜索关键词）、`city`（城市，可选）、`offset`（每页记录数，默认 20）
  - 返回：POI 列表（名称、坐标、地址、电话）

- **`maps_around_search`**：周边兴趣点搜索
  - 参数：`keywords`、`location`（中心点"经度,纬度"）、`radius`（搜索半径，单位米，默认 1000）、`types`（POI 类型，可选）、`offset`（默认 20）、`page`（默认 1）
  - 返回：周边 POI 列表（含距离信息）

### 3. 路径规划

- **`maps_direction_walking`**：步行路线规划
  - 参数：`origin`（起点"经度,纬度"）、`destination`（终点"经度,纬度"）

- **`maps_direction_driving`**：驾车路线规划
  - 参数：`origin`、`destination`

- **`maps_direction_transit_integrated`**：公共交通路线规划
  - 参数：`origin`、`destination`、`city`（城市，默认"北京"）

### 4. 位置服务

- **`maps_ip_location`**：IP 地址 → 地理位置
  - 参数：`ip`（IP 地址）
  - 返回：省份、城市、行政区、ISP 等信息

### 5. 地图生成（核心）

- **`maps_schema_personal_map`**：生成个人地图小程序二维码
  - 参数：
    - `orgName`（地图名称）
    - `lineList`（行程列表，每条路线最多 16 个点）
    - `sceneType`（场景类型，可选，默认 `1`）：
      - `1` — 创建资源点且创建路线（默认，通用场景）
      - `2` — 仅创建资源点（搜索类数据，多个点之间无关联关系）
      - `3` — 仅创建路线（路径规划类数据，多个点有关联关系，如起终点、换乘点）
  - 返回：`qr_code_url`（二维码图片链接）、`lineList`（行程数据）

  **sceneType 选择指引：**
  - 用户做的是**搜索**（找餐厅、找景点、找周边 POI 等）→ 用 `sceneType=2`
  - 用户做的是**路径规划**（从 A 到 B、导航、换乘等）→ 用 `sceneType=3`
  - 两者都有，或不确定 → 用默认 `sceneType=1`

## 使用前提

1. 申请高德地图开发者账号并获取 API Key（https://lbs.amap.com/）
2. 配置环境变量：`export AMAP_API_KEY='your_api_key_here'`
3. 确保网络连接正常

## 异常处理

所有接口在出错时均返回结构化错误信息，不会抛出异常：

```python
{"error": "错误类型", "message": "具体原因"}
```

常见错误类型：`API Key 缺失`、`请求失败`、`搜索失败`、`路径规划失败`、`生成地图行程失败`。

检查返回值的推荐方式：
```python
result = client.maps_text_search("餐厅", "北京")
if isinstance(result, list) and result and "error" in result[0]:
    print(f"错误: {result[0]['message']}")
```

## 使用示例

### 初始化客户端

```python
from scripts.amap_personal_map_client import AMapPersonalMapClient

client = AMapPersonalMapClient()  # 读取环境变量 AMAP_API_KEY
# 或直接传入：client = AMapPersonalMapClient(api_key='your_api_key_here')
```

### 地理编码

```python
# 地址转坐标
result = client.maps_geo("北京市朝阳区三里屯", "北京")
print(f"经度: {result['longitude']}, 纬度: {result['latitude']}")

# 坐标转地址
result = client.maps_regeocode(116.447716, 39.906736)
print(f"完整地址: {result['formatted_address']}")
```

### POI 搜索

```python
# 关键词搜索
pois = client.maps_text_search("烤鸭", "北京", offset=20)
for poi in pois:
    print(f"{poi['name']} - {poi['address']}")

# 周边搜索
pois = client.maps_around_search(keywords="餐厅", location="116.397451,39.909221", radius=1000)
for poi in pois:
    print(f"{poi['name']}, 距离: {poi.get('distance', '未知')}米")
```

### 路径规划

```python
# 步行
result = client.maps_direction_walking("116.397451,39.909221", "116.397029,39.917839")

# 驾车
result = client.maps_direction_driving("116.397451,39.909221", "116.397029,39.917839")

# 公共交通
result = client.maps_direction_transit_integrated("116.397451,39.909221", "116.397029,39.917839", city="北京")
```

### 生成个人地图（最终步骤）

```python
import urllib.request
from scripts.amap_personal_map_client import AMapPersonalMapClient

client = AMapPersonalMapClient()

line_list = [{
    "title": "北京市中心一日游",
    "pointInfoList": [
        {"name": "天安门广场", "lon": 116.397451, "lat": 39.909221, "poiId": "B000A8URXB"},
        {"name": "故宫博物院",  "lon": 116.397029, "lat": 39.917839, "poiId": "B000A8URXC"}
    ]
}]

# 搜索类数据 → sceneType=2（仅创建资源点）
result = client.maps_schema_personal_map("北京热门景点", line_list, sceneType=2)

# 路径规划类数据 → sceneType=3（仅创建路线）
result = client.maps_schema_personal_map("北京一日游路线", line_list, sceneType=3)

# 通用场景（默认）
result = client.maps_schema_personal_map("北京市中心一日游", line_list)

# 下载并保存二维码图片到本地
qr_url = result['qr_code_url']
output_path = '/path/to/output/个人地图二维码.png'
urllib.request.urlretrieve(qr_url, output_path)

# 使用 present 工具展示图片（实际使用时通过工具调用）
# present(artifacts=[output_path])

# 在回复中嵌入 Markdown 图片（双重保障）
print(f"![个人地图二维码](file://{output_path})")

# 提供备用 URL 链接
print(f"备用链接: {qr_url}")
```

### 会话管理

AMAP_API_KEY 配置正常的前提下，每次会话结束请调用 `maps_schema_personal_map` 生成个人地图二维码，并**按以下步骤展示**：

1. **下载二维码图片**：使用 `urllib.request.urlretrieve()` 将二维码保存到本地工作目录
2. **调用 `present` 工具**：将保存的图片路径传入 `present` 工具展示
3. **Markdown 嵌入**：在回复中使用 `![描述](file://路径)` 格式嵌入图片
4. **提供备用链接**：同时输出二维码的原始 URL，以防图片展示失败

用户可以通过高德地图 App 扫描二维码打开个人地图小程序页。

**最佳实践示例：**
```python
import urllib.request
from scripts.amap_personal_map_client import AMapPersonalMapClient

client = AMapPersonalMapClient()

# ... 搜索/规划逻辑 ...

result = client.maps_schema_personal_map("我的地图", line_list, sceneType=2)

# 1. 保存二维码到本地
qr_path = '/workspace/我的地图二维码.png'
urllib.request.urlretrieve(result['qr_code_url'], qr_path)

# 2. 调用 present 工具展示
# present(artifacts=[qr_path])

# 3. 在回复中嵌入图片和备用链接
print(f"![个人地图](file://{qr_path})")
print(f"备用链接: {result['qr_code_url']}")
```

## logo
![](https://img.alicdn.com/imgextra/i4/O1CN01OIfavw1VGuqFZdQnc_!!6000000002636-2-tps-256-256.png)

## 使用场景
1. 旅游路线规划与地图分享
2. 周边 POI 搜索与标记
3. 通勤/出行路径规划
4. 商业选址与市场分析
5. 物流配送路径优化

## changelog

### v1.2.0
- `maps_schema_personal_map` 新增 `sceneType` 参数，支持按场景控制创建资源点/路线

### v1.1.0
- 新增骑行路线规划功能
- 新增 URI 生成功能（导航页面唤起、打车页面唤起）
- 完善会话管理机制，提升用户体验
- 优化错误处理和异常情况应对

### v1.0.0
- 初始版本发布
- 支持地理编码、POI 搜索、路径规划等核心功能
- 支持生成个人地图小程序二维码
- 支持会话管理与二维码自动生成

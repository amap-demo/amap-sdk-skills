# 导航控制 API

通过 `AMapNaviClientManager` 控制导航行为，SDK 和 APP 链路统一接口。

## 停止导航

```objc
[[AMapNaviClientManager shareInstance] stopNavi];
```

## 切换路线

```objc
// routeID 来自查询结果中的路线字典 key
[[AMapNaviClientManager shareInstance] switchRoute:routeID];
```

## 强制刷新路线

重新请求路线数据，刷新后会重新回调路线数据：

```objc
[[AMapNaviClientManager shareInstance] forceRefreshRoute];
```

## 播报模式

```objc
// mode 值：
// 0 — 静音
// 1 — 简洁播报
// 2 — 详细播报
// 6 — 极简播报
// 7 — 智能播报
[[AMapNaviClientManager shareInstance] switchBroadcastMode:2];
```

> **注意**：导航过程中设置播报模式，需在下次算路后生效（如偏航重算、手动刷新）。SDK 链路下，仅驾车支持全部播报模式，骑步行仅支持静音(0)和播报(1)。

## 设置导航视图

用于获取导航跟随模式回调数据：

```objc
// view 可以是 AMapNaviDriveView / AMapNaviRideView / AMapNaviWalkView
[[AMapNaviClientManager shareInstance] setAmapNaviView:driveView];
```

> 切换导航类型后需重新设置。不设置则跟随模式变更不会回调，但导航数据仍可通过 `addNaviDataListener` 获取。

## 获取精简路线信息

获取当前高亮路线从自车位置开始的精简路线 PB 数据：

```objc
// limitPointSize: 限制坐标点数量
AMapNaviPbData *partialRoute = [[AMapNaviClientManager shareInstance] getPartialRouteGroupWithLimitPointSize:100];
```

## 位置更新

持续向 SDK 提供定位数据：

```objc
// 在 CLLocationManager 回调中调用
[[AMapNaviClientManager shareInstance] updateMyLocation:location];

// 可配置最小发送间隔（秒），默认 0 不限制
[AMapNaviClientManager shareInstance].locationUpdateInterval = 1.0;
```

## 相关文档

- [导航数据监听](navi-data-listener.md) — 监听导航过程中的数据回调
- [出行方式配置](transport-mode.md) — 配置导航类型和路线偏好

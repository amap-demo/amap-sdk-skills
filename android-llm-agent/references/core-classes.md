# 核心类说明

SDK 主要类和接口说明。

## 入口类

| 类名 | 说明 |
|-----|------|
| `AMapApi` | SDK 入口类，提供各客户端访问 |
| `AMapContext` | 上下文配置，包含导航环境和日志 |

## 配置类

| 类名 | 说明 |
|-----|------|
| `AMapNaviEnv` | 导航环境配置，包含位置、偏好等 |
| `Poi` | POI 点位信息 |
| `LatLng` | 经纬度坐标 |
| `AMapCarInfo` | 车辆信息 |

## 客户端

| 类名 | 说明 |
|-----|------|
| `AgentClient` | AI 助手客户端，处理自然语言查询 |
| `NaviClient` | 导航客户端，管理导航功能 |
| `LinkClient` | 链路客户端，与高德 APP 通信 |

## 查询相关

| 类名 | 说明 |
|-----|------|
| `AMapAgentQueryParam` | 查询参数 |
| `AMapAgentQueryResult` | 查询结果 |
| `AMapAgentQueryResult.ActionType` | 操作类型枚举 |

## 回调接口

| 接口 | 说明 |
|-----|------|
| `AMapAgentCallback` | Agent 查询结果回调 |
| `AMapNaviInfoCallback` | 导航信息回调 |
| `AMapLinkStateCallback` | 链接状态回调 |
| `AMapTaxiInfoCallback` | 打车信息回调 |
| `ILogger` | 日志回调接口 |

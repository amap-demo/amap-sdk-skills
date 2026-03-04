# 生命周期管理

管理 Agent 场景状态、会话重置和单例销毁。

## 场景管理

通过 `resetAgentScene:` 切换 Agent 当前所处的业务场景：

```objc
// 场景值说明：
// "home"   — 行前场景（主图）
// "route"  — 行前场景（路线规划）
// "navi"   — 行中场景（导航中）
// "search" — 搜索场景
[[AMapAgentClientManager shareInstance] resetAgentScene:@"home"];
```

> 切换场景会影响 Agent 对自然语言的理解上下文。例如在 `"navi"` 场景下，"加个途经点" 才会被正确识别。

## 会话状态重置

清除当前多轮对话上下文，开始新的会话：

```objc
[[AMapAgentClientManager shareInstance] resetAgentStatus];
```

## 单例销毁

在不再需要 SDK 时（如退出地图模块），按顺序销毁：

```objc
// 1. 移除所有监听器
[[AMapNaviClientManager shareInstance] removeNaviDataListener:self.naviDataCallback];

// 2. 销毁单例（按依赖顺序）
[AMapAgentClientManager destroy];
[AMapNaviClientManager destroy];
[AMapLinkManager destroy];  // 仅 APP 链路模式需要
```

> `destroy` 返回 `NO` 表示单例仍被外部强引用，请检查是否有未释放的引用。

## 导航 Manager 销毁通知

当外部控制销毁导航 Manager 时，需通知 Agent 清理内部数据：

```objc
[[AMapNaviClientManager shareInstance] onNaviManagerDestroyed:AMapNaviTypeDrive];
```

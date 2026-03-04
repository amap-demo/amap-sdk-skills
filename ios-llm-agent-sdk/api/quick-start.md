# 快速集成指南

## 系统要求

- iOS 11.0+
- 需集成高德地图 SDK 相关组件（AMapNaviKit、AMapSearchKit）

## 1. 添加依赖

在项目中添加 `MALLMKit.a` 静态库依赖。

## 2. 导入头文件

MALLMKit 以静态库（`.a`）形式提供，头文件通过 Header Search Paths 引入：

```objc
#import "AMapAgentClientManager.h"
#import "AMapNaviClientManager.h"
#import "AMapAgentQueryParam.h"
#import "AMapAgentQueryResult.h"
#import "AMapNaviEnv.h"
#import "AMapLinkManager.h"
#import "AMapAuthorizationManager.h"
```

## 3. 初始化（最小可用配置）

```objc
// 1) 设置链路模式：SDK链路（应用内集成）或 APP链路（依赖高德APP）
[AMapAgentClientManager shareInstance].commandDestination = AMapAgentCommandDestinationSDK;

// 2) 设置查询结果回调
[[AMapAgentClientManager shareInstance] setQueryResultCallback:^(AMapAgentQueryResult *queryResult) {
    // 处理查询结果，详见 query-result.md
}];

// 3) 配置导航环境
AMapNaviEnv *env = [AMapNaviEnv new];
env.amapNaviType = AMapNaviTypeDrive;
env.multipleRoute = YES;
[AMapNaviClientManager shareInstance].amapNaviEnv = env;

// 4) 重置场景到主图
[[AMapAgentClientManager shareInstance] resetAgentScene:@"home"];
```

## 4. 发起第一次查询

```objc
AMapAgentQueryParam *param = [AMapAgentQueryParam new];
param.queryText = @"附近的加油站";
NSString *sessionId = [[AMapAgentClientManager shareInstance] query:param];
```

## 初始化顺序要求

> **重要**：`AMapAgentClientManager` 和 `AMapNaviClientManager` 必须在 `AMapLinkManager` 之前初始化。

## 两种链路模式

| 模式 | 枚举值 | 特点 |
|------|--------|------|
| **SDK链路** | `AMapAgentCommandDestinationSDK` | 应用内独立运行，不依赖高德APP |
| **APP链路** | `AMapAgentCommandDestinationAPP` | 与高德APP深度集成，需额外建联和授权 |

SDK链路适合大多数场景。如需 APP链路，请参阅 [IPC链路管理](link-client.md)。

## 下一步

- [智能查询 API](agent-query.md) — 了解查询参数与多轮对话
- [查询结果处理](query-result.md) — 处理路线、POI 等返回结果

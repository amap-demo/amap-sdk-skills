# 查询结果处理

`AMapAgentQueryResult` 是所有查询的统一返回结构，通过 `setQueryResultCallback:` 回调获取。

## AMapAgentQueryResult 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `actionType` | `AMapAgentQueryResultActionType` | 操作类型（路线/POI/退出导航等） |
| `stateType` | `AMapAgentQueryResultStateType` | 状态（进行中/追加/结束） |
| `resultType` | `AMapAgentQueryResultType` | 结果类型（命令/总结） |
| `summary` | `NSString` | 查询总结文本 |
| `resultObj` | `id` | 结果数据对象（类型取决于 actionType） |
| `errorInfo` | `NSError` | 错误信息（无错误时为 nil） |
| `sessionId` | `NSString` | 查询会话 ID |
| `endPoiName` | `NSString` | 终点名称 |
| `viaPoiItem` | `AMapPOI` | 途经点信息 |

## actionType 与 resultObj 对应关系

| actionType | 含义 | resultObj 类型 |
|------------|------|----------------|
| `RequestRoute` | 行前请求路线 | `NSDictionary<NSNumber*, AMapNaviRoute*>` |
| `RequestRouteInNavi` | 行中请求路线 | `NSDictionary<NSNumber*, AMapNaviRoute*>` |
| `SearchPoi` | POI 搜索 | `AMapPOIResult` |
| `SelectPoiWorkFlow` | 行前 POI 选点 | `AMapPOIResult` |
| `SelectPoiWorkFlowSingle` | 单点选点 | `AMapPOIResult` |
| `RouteSearch` | 行中顺路搜 | `NSArray<AMapRoutePOI*>` |
| `ExitNavi` | 退出导航 | 无 |
| `BreakSession` | 中断会话 | 无 |
| `Refuse` | 拒绝命令 | 无 |
| `ChangeOrViaPoi` | 行中变更POI | 无 |
| `SetAutoListen` | 闲聊指令 | 无 |
| `RequestGuideInfo` | 行中引导 | 无 |

## stateType 状态流转

| 状态 | 说明 |
|------|------|
| `Working` | 查询进行中，可能有中间结果 |
| `Append` | 追加结果（如流式返回） |
| `End` | 查询结束，结果完整 |

## 典型处理模式

```objc
[[AMapAgentClientManager shareInstance] setQueryResultCallback:^(AMapAgentQueryResult *result) {
    // 1. 先检查错误
    if (result.errorInfo) {
        NSLog(@"查询错误: %@", result.errorInfo);
        return;
    }
    
    // 2. 按 actionType 分发处理
    switch (result.actionType) {
        case AMapAgentQueryResultActionTypeRequestRoute: {
            NSDictionary *routes = result.resultObj;
            // 处理路线数据，开始导航
            break;
        }
        case AMapAgentQueryResultActionTypeSearchPoi: {
            AMapPOIResult *poiResult = result.resultObj;
            NSArray<AMapPOI *> *pois = poiResult.poiItemArray;
            // 展示 POI 列表
            break;
        }
        case AMapAgentQueryResultActionTypeExitNavi:
            // 退出导航
            break;
        default:
            break;
    }
}];
```

## 相关文档

- [智能查询 API](agent-query.md) — 发起查询
- [常见问题排查](../references/troubleshooting.md) — 错误码说明

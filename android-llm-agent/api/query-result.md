# 处理 AI 查询结果

根据 ActionType 处理不同场景的返回结果。

## 导入依赖

```java
import com.amap.llm.agent.api.AMapAgentQueryResult;
import com.amap.llm.agent.api.PoiResultWrapper;
import com.amap.api.services.routepoisearch.RoutePOIItem;

import java.util.List;
```

## 回调处理

```java
private void handleQueryResult(AMapAgentQueryResult result) {
    // 1. 检查错误
    if (result.errorCode != 0) {
        Log.e(TAG, "Query error: " + result.errorCode + " - " + result.errorMessage);
        return;
    }
    
    // 2. 获取总结文本（注意：没有 ttsText 字段，使用 summary）
    if (result.summary != null && !result.summary.isEmpty()) {
        Log.d(TAG, "Summary: " + result.summary);
    }
    
    // 3. 根据 ActionType 处理（需要从 resultObj 进行类型转换）
    switch (result.actionType) {
        case REQUEST_ROUTE:
        case REQUEST_ROUTE_NAVI:
            Log.d(TAG, "路线规划完成");
            // resultObj 类型: Map<Integer, AMapNaviPath>
            break;
            
        case SEARCH_POI:
        case SELECT_POI_WORK_FLOW:
        case SELECT_POI_WORK_FLOW_SINGLE:
            if (result.resultObj instanceof PoiResultWrapper) {
                PoiResultWrapper poiResult = (PoiResultWrapper) result.resultObj;
                showPoiList(poiResult);
            }
            break;
            
        case ROUTE_SEARCH:
            if (result.resultObj instanceof List) {
                @SuppressWarnings("unchecked")
                List<RoutePOIItem> routePoiList = (List<RoutePOIItem>) result.resultObj;
                showRoutePoiList(routePoiList);
            }
            break;
            
        case COMMAND_EXIT_NAVI:
            Log.d(TAG, "退出导航");
            break;
            
        case REQUEST_GUIDE_INFO:
            Log.d(TAG, "请求引导信息");
            break;
            
        default:
            break;
    }
    
    // 4. 保存状态用于多轮对话
    mCurrentActionType = result.actionType;
}
```

## ActionType 说明

| ActionType | 说明 | resultObj 类型 |
|------------|------|---------------|
| `NONE` | 无操作 | - |
| `REQUEST_ROUTE` | 请求路线 | `Map<Integer, AMapNaviPath>` |
| `REQUEST_ROUTE_NAVI` | 行中请求路线 | `Map<Integer, AMapNaviPath>` |
| `SEARCH_POI` | POI 搜索结果 | `PoiResultWrapper` |
| `SELECT_POI_WORK_FLOW` | POI 选点工作流 | `PoiResultWrapper` |
| `SELECT_POI_WORK_FLOW_SINGLE` | 单 POI 确认 | `PoiResultWrapper` |
| `ROUTE_SEARCH` | 沿途搜索结果 | `List<RoutePOIItem>` |
| `CHANGE_OR_VIA_POI` | 行中变更 POI | - |
| `COMMAND_EXIT_NAVI` | 退出导航 | - |
| `BREAK_SESSION` | 中断会话 | - |
| `REFUSE` | 拒绝取消 | - |
| `SET_AUTO_LISTEN` | 闲聊追问 | - |
| `REQUEST_GUIDE_INFO` | 请求引导信息 | - |

## 关键字段说明

| 字段 | 类型 | 说明 |
|-----|------|------|
| `errorCode` | int | 错误码，0 表示成功 |
| `errorMessage` | String | 错误信息 |
| `sessionId` | String | 会话 ID |
| `taskId` | String | 任务 ID |
| `actionType` | ActionType | 操作类型 |
| `stateType` | StateType | 状态类型（WORKING/APPEND/END） |
| `resultType` | ResultType | 结果类型（COMMAND/SUMMARY） |
| `summary` | String | 总结文本 |
| `resultObj` | Object | 结果对象，需根据 actionType 进行类型转换 |
| `endPoiName` | String | 终点名称 |
| `viaPoiItem` | PoiItem | 途径点信息 |

## 相关文档

- [发送 AI 查询](agent-query.md)
- [常见问题诊断](../references/troubleshooting.md)

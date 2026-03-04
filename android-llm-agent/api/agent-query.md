# 发送 AI 查询

通过 AgentClient 发送自然语言查询。

## 导入依赖

```java
import com.amap.llm.agent.api.AMapAgentQueryParam;
import com.amap.llm.agent.api.AMapAgentQueryResult;
import com.amap.llm.agent.api.AMapApi;
import com.amap.llm.agent.api.AMapConstants;
import com.amap.api.services.route.RoutePOIItem;

import java.util.List;
```

## 基础查询

```java
private void sendQuery(String queryText) {
    if (mAMapApi == null || queryText == null || queryText.isEmpty()) {
        return;
    }
    AMapAgentQueryParam param = new AMapAgentQueryParam();
    param.queryText = queryText;
    
    String sessionId = mAMapApi.getAgentClient().query(param);
    Log.d(TAG, "Query sent, sessionId: " + sessionId);
}

// 使用示例
sendQuery("去颐和园");
sendQuery("帮我搜一下麦当劳");
sendQuery("开车去奥森公园需要多久");
sendQuery("离终点还有多远");
sendQuery("顺路搜下加油站");
```

## 多轮对话（带上下文）

```java
private AMapAgentQueryResult.ActionType mCurrentActionType;
private Object mCurrentPoiResult;
private List<RoutePOIItem> mRoutePOIItemList;

private void sendQueryWithContext(String queryText) {
    AMapAgentQueryParam param = new AMapAgentQueryParam();
    param.queryText = queryText;
    
    // 如果是选择场景，需要填充上下文
    if (mCurrentActionType == AMapAgentQueryResult.ActionType.SEARCH_POI) {
        param.selectedObject = mCurrentPoiResult;
        param.lastActionType = AMapAgentQueryResult.ActionType.SEARCH_POI;
        // 泛搜支持打断
        mAMapApi.getAgentClient().resetAgentStatus();
    } else if (mCurrentActionType == AMapAgentQueryResult.ActionType.ROUTE_SEARCH) {
        param.selectedObject = mRoutePOIItemList;
        param.lastActionType = AMapAgentQueryResult.ActionType.ROUTE_SEARCH;
    }
    
    String sessionId = mAMapApi.getAgentClient().query(param);
}
```

## 多轮对话示例

```java
// 第一轮：搜索
sendQuery("帮我搜一下肯德基");

// 第二轮：选择结果
sendQueryWithContext("第二个");

// 第三轮：开始导航
sendQueryWithContext("导航去那里");
```

## 重置状态

```java
// 重置 Agent 状态（打断当前对话）
mAMapApi.getAgentClient().resetAgentStatus();

// 重置到指定场景
mAMapApi.getAgentClient().resetAgentScene(AMapConstants.SceneType.HOME);
```

## 相关文档

- [处理查询结果](query-result.md)

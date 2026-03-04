# 智能查询 API

通过 `AMapAgentClientManager` 发起自然语言查询，SDK 会自动解析意图并返回结构化结果。

## 核心类

- **AMapAgentClientManager** — 查询入口（单例）
- **AMapAgentQueryParam** — 查询参数

## 基础查询

```objc
AMapAgentQueryParam *param = [AMapAgentQueryParam new];
param.queryText = @"去西藏";
NSString *sessionId = [[AMapAgentClientManager shareInstance] query:param];
```

`query:` 返回 `sessionId`，用于追踪本次查询会话。结果通过 `setQueryResultCallback:` 异步回调。

## 多轮对话

在上一次查询结果基础上继续对话（如选择搜索结果中的某一个）：

```objc
AMapAgentQueryParam *param = [AMapAgentQueryParam new];
param.queryText = @"第一个";
param.selectedObject = previousResult.resultObj;    // 上次结果对象
param.lastActionType = previousResult.actionType;   // 上次操作类型
NSString *sessionId = [[AMapAgentClientManager shareInstance] query:param];
```

## AMapAgentQueryParam 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `queryText` | `NSString` | 自然语言查询文本 |
| `lastActionType` | `AMapAgentQueryResultActionType` | 上一次查询的操作类型（多轮对话时设置） |
| `selectedObject` | `id` | 上一次查询的结果对象（多轮对话时设置） |

## 自定义 Agent 服务地址

```objc
// 必须在使用 Agent 前调用
[AMapAgentClientManager configureAgentURL:@"https://your-custom-url.com"];

// 获取当前 URL
NSString *currentURL = [AMapAgentClientManager currentAgentURL];
```

## 相关文档

- [查询结果处理](query-result.md) — 如何处理回调中的 `AMapAgentQueryResult`
- [语音指令参考](../references/voice-commands.md) — 支持的自然语言指令示例

# 常见问题排查

## 错误码速查

### AMapAgentQueryResultErrorCode

| 错误码 | 值 | 含义 | 解决方案 |
|--------|-----|------|----------|
| `CmdNotSupport` | -20001 | 当前命令不支持 | 检查查询文本是否在支持范围内 |
| `QueryTimeout` | -20002 | 查询超时 | 检查网络连接，重试查询 |
| `HomeNotSet` | -20003 | 家位置未设置 | 通过 `AMapNaviEnv.homeLocation` 设置 |
| `CompanyNotSet` | -20004 | 公司位置未设置 | 通过 `AMapNaviEnv.workLocation` 设置 |
| `CmdTimeout` | -20005 | 命令执行超时 | 检查导航 SDK 状态，重试 |
| `ViaNotFound` | -20006 | 未找到途经点 | 检查途经点查询文本 |
| `DoAction` | -20007 | doAction 参数错误 | 检查传入参数 |
| `RequestRoute` | -20008 | requestRoute 参数错误 | 检查路线请求参数 |

## 常见问题

### Q: 收不到 addNaviDataListener 回调

**原因**：
1. `AMapNaviClientManager` 未正确设置 `naviType`
2. 监听器在算路之后才设置

**解决**：
```objc
// 确保在算路前设置
[AMapNaviClientManager shareInstance].naviType = AMapNaviTypeDrive;
[[AMapNaviClientManager shareInstance] addNaviDataListener:callback];
// 然后再发起算路
```

### Q: setAmapNaviView 是否必须调用

**不必须**。`setAmapNaviView` 仅用于获取导航跟随模式回调数据。导航数据通过 `addNaviDataListener` 回调，不依赖 NaviView 设置。切换导航类型后需重新设置。

### Q: SDK 链路 vs APP 链路如何选择

| 维度 | SDK 链路 | APP 链路 |
|------|----------|----------|
| 依赖 | 不依赖高德 APP | 需安装高德 APP |
| 功能 | 独立运行 | 可享受高德 APP 完整功能 |
| 集成复杂度 | 低 | 需额外建联和授权 |

### Q: 初始化顺序错误导致崩溃

**正确顺序**：
1. `AMapAgentClientManager` — 最先初始化
2. `AMapNaviClientManager` — 其次
3. `AMapLinkManager` — 最后（仅 APP 链路）

### Q: destroy 返回 NO

单例仍被外部强引用。检查是否有 property 或变量持有了单例引用，释放后重试。

### Q: 导航视图切换注意事项

1. 移除旧导航视图
2. 创建新导航视图并设置 delegate
3. 调用 `setAmapNaviView:` 重新绑定
4. 更新 `naviType` 和 `amapNaviEnv.amapNaviType`
5. 添加新的 DataRepresentative

### Q: UI 更新崩溃

查询结果回调可能在子线程，UI 更新需切回主线程：

```objc
dispatch_async(dispatch_get_main_queue(), ^{
    [self updateUIWithResult:queryResult];
});
```

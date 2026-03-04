# 错误码参考

MALLMKit IPC Link 相关的错误码参考。

## 授权错误

`AMapAuthorizationManager` 的 `startAuthenticationWithCallback:` 回调中的 `NSError`：

| 场景 | 说明 | 解决方案 |
|------|------|----------|
| 高德 APP 未安装 | 无法跳转授权 | 提示用户安装高德地图 APP |
| 授权被拒绝 | 用户在高德 APP 中拒绝授权 | 引导用户重新授权 |
| URL 回调解析失败 | `handleURL:` 返回 NO | 检查 URL Scheme 配置是否正确 |

## 连接错误

`AMapLinkManager` 连接过程中可能出现的问题：

| 场景 | 说明 | 解决方案 |
|------|------|----------|
| 未授权就建联 | `isAuthored` 为 NO 时调用 `connect` | 先完成授权流程 |
| 重复连接 | 已连接状态下再次调用 `connect` | 通过 `isConnected` 检查状态 |
| 连接断开 | 高德 APP 退出或网络异常 | 配置 `autoReconnect = YES` 自动重连 |
| 重连达到上限 | 超过 `maxReconnectAttempts` 次数 | 提示用户检查高德 APP 状态，按需重新建联 |

## 数据发送错误

| 场景 | 说明 | 解决方案 |
|------|------|----------|
| 未连接时发送 | 连接未建立就调用 `sendDataToClient:` | 先确保 `isConnected == YES` |
| JSON 序列化失败 | 数据不是合法 JSON 对象 | 通过 `isValidJSONObject:` 校验 |

## 错误处理最佳实践

```objc
// 建联前检查授权和连接状态
- (void)createConnect {
    if (!self.isAuthored) {
        // 需先完成授权
        [self openAmap];
        return;
    }

    if ([[AMapLinkManager sharedInstance] isConnected]) {
        return;
    }

    AMapLinkConnectConfig *config = [AMapLinkConnectConfig new];
    config.autoReconnect = YES;
    config.maxReconnectAttempts = 50;
    config.reconnectDelay = 2;

    [[AMapLinkManager sharedInstance] initWithConnectConfig:config];
    [[AMapLinkManager sharedInstance] connect];
}
```

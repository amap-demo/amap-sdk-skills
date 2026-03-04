# IPC 链路管理

APP 链路模式下，通过 `AMapLinkManager` 与高德 APP 建立 IPC 连接，通过 `AMapAuthorizationManager` 完成授权。

> 仅当 `commandDestination = AMapAgentCommandDestinationAPP` 时需要使用。SDK 链路模式可跳过本文档。

## 建联配置

```objc
AMapLinkConnectConfig *config = [AMapLinkConnectConfig defaultConfig];
config.autoReconnect = YES;          // 是否自动重连，默认 NO
config.maxReconnectAttempts = 5;     // 最大重连次数，默认 5
config.reconnectDelay = 2.0;         // 重连间隔（秒），默认 2

[[AMapLinkManager sharedInstance] initWithConnectConfig:config];
[[AMapLinkManager sharedInstance] connect];
```

## 连接状态监听

```objc
NSString *observerID = [[AMapLinkManager sharedInstance] addReachablityChanged:^(BOOL isReachable) {
    NSLog(@"连接状态: %@", isReachable ? @"已连接" : @"已断开");
}];

// 移除监听
[[AMapLinkManager sharedInstance] removeReachablityObserver:observerID];
```

## 错误监听

```objc
NSString *errorObserverID = [[AMapLinkManager sharedInstance] addErrorOccurred:^(NSError *error) {
    NSLog(@"连接错误: %@", error.localizedDescription);
}];

[[AMapLinkManager sharedInstance] removeErrorObserver:errorObserverID];
```

## Server 探测

```objc
[[AMapLinkManager sharedInstance] startServerProbing];  // 手动开始探测
[[AMapLinkManager sharedInstance] stopServerProbing];   // 停止探测
BOOL isProbing = [[AMapLinkManager sharedInstance] isServerProbing];
```

## APP 授权

```objc
// 1. 检查高德 APP 是否安装
if (![[AMapAuthorizationManager sharedInstance] isInstallAMapApp]) {
    [[AMapAuthorizationManager sharedInstance] turnToAppStore];
    return;
}

// 2. 发起授权
[[AMapAuthorizationManager sharedInstance] startAuthenticationWithCallback:^(BOOL success, NSError *error) {
    if (success) {
        NSLog(@"授权成功");
    }
}];

// 3. 在 AppDelegate 中处理回调
- (BOOL)application:(UIApplication *)app openURL:(NSURL *)url options:(NSDictionary *)options {
    return [[AMapAuthorizationManager sharedInstance] handleURL:url];
}
```

## Info.plist 配置

APP 链路需要在 `Info.plist` 中声明：

```xml
<key>LSApplicationQueriesSchemes</key>
<array>
    <string>amapuri</string>
</array>
```

## 授权错误码

| 错误码 | 含义 |
|--------|------|
| `AppAuthSuccess` | 授权成功 |
| `InvalidAPIKey` | 无效的 apiKey |
| `MissingAPIKey` | 缺少 apiKey |
| `NetworkFailed` | 校验网络异常 |
| `AppNotInstalled` | 高德 APP 未安装 |
| `AppOpenFailed` | 跳转 APP 失败 |
| `AppAuthFailed` | 授权失败 |

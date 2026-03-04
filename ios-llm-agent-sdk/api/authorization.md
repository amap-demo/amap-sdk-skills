# 认证管理

通过 `AMapAuthorizationManager` 跳转高德地图 APP 完成鉴权授权。

## 前置条件

1. 已在 Info.plist 中配置 URL Scheme 和 `LSApplicationQueriesSchemes`（详见 [quick-start.md](quick-start.md)）
2. 已导入头文件：
```objc
#import <MALLMKit/AMapAuthorizationManager.h>
```

## 发起鉴权

通过 `AMapAuthorizationManager` 的 `startAuthenticationWithCallback:` 方法发起授权，SDK 会自动跳转高德地图 APP：

```objc
- (void)openAmap {
    __weak typeof(self) weakSelf = self;
    [[AMapAuthorizationManager sharedInstance] startAuthenticationWithCallback:^(BOOL success, NSError * _Nonnull error) {
        NSLog(@"授权结果: %d, error: %@", success, error);
    }];
}
```

### 回调参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `success` | BOOL | 授权是否成功 |
| `error` | NSError | 授权失败时的错误信息 |

## 处理授权回调 URL

授权完成后高德 APP 会通过 URL Scheme 回调，需在 App/SceneDelegate 中将 URL 传递给 `AMapAuthorizationManager` 处理：

### AppDelegate 方式

```objc
- (BOOL)application:(UIApplication *)app openURL:(NSURL *)url options:(NSDictionary *)options {
    [self.viewController handleUrl:url];
    return YES;
}
```

### SceneDelegate 方式（iOS 13+）

```objc
- (void)scene:(UIScene *)scene openURLContexts:(NSSet<UIOpenURLContext *> *)URLContexts {
    UIOpenURLContext *context = URLContexts.allObjects.firstObject;
    if (context) {
        [self.viewController handleUrl:context.URL];
    }
}
```

### 业务页面处理 URL

在业务 ViewController 中调用 `AMapAuthorizationManager.handleURL:` 解析授权结果，并在授权成功后持久化状态、发起建联：

```objc
#define kAMapAIPCAuthStatus @"kAMapAIPCAuthStatus"

- (BOOL)handleUrl:(NSURL *)url {
    BOOL authResult = [[AMapAuthorizationManager sharedInstance] handleURL:url];
    self.isAuthored = authResult;
    if (authResult) {
        [[NSUserDefaults standardUserDefaults] setBool:authResult forKey:kAMapAIPCAuthStatus];
        [self createConnect];
    }
    return YES;
}
```

## 授权状态持久化

授权成功后通过 `NSUserDefaults` 持久化授权状态，APP 下次启动时可直接尝试建联，无需重复授权：

```objc
// 读取授权状态
self.isAuthored = [[NSUserDefaults standardUserDefaults] boolForKey:kAMapAIPCAuthStatus];

// 已授权则直接建联
if (self.isAuthored) {
    [self createConnect];
}
```

## 注意事项

- 授权通过 `AMapAuthorizationManager` 统一管理，无需手动构造 URL
- `handleURL:` 返回 `YES` 表示授权成功，返回 `NO` 表示授权失败
- 建议通过 `NSUserDefaults` 持久化授权状态，避免每次启动都需要重新授权
- 授权成功后应立即调用 `createConnect` 建立 IPC 连接

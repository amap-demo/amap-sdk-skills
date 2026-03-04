# 连接管理

通过 `AMapLinkManager` 管理与高德 APP 的 IPC 连接。

## 导入头文件

```objc
#import <MALLMKit/AMapLinkManager.h>
#import <MALLMKit/AMapLinkConnectConfig.h>
```

## 初始化与建联

授权成功后，通过 `AMapLinkManager` 单例创建连接：

```objc
- (void)createConnect {
    if (!self.isAuthored) {
        return;
    }

    // 防重复连接
    if ([[AMapLinkManager sharedInstance] isConnected]) {
        return;
    }

    // 1. 创建连接配置
    AMapLinkConnectConfig *config = [AMapLinkConnectConfig new];
    config.autoReconnect = YES;
    config.maxReconnectAttempts = 50;
    config.reconnectDelay = 2;
    self.connectConfig = config;

    // 2. 初始化并连接
    [[AMapLinkManager sharedInstance] initWithConnectConfig:config];
    [[AMapLinkManager sharedInstance] connect];
}
```

### AMapLinkConnectConfig 配置参数

| 属性 | 类型 | 说明 |
|------|------|------|
| `autoReconnect` | BOOL | 是否自动重连 |
| `maxReconnectAttempts` | NSUInteger | 最大重连次数 |
| `reconnectDelay` | NSTimeInterval | 重连间隔（秒） |

## 检查连接状态

```objc
BOOL isConnected = [[AMapLinkManager sharedInstance] isConnected];
```

## 监听数据回调

通过 `AMapLinkClientObserverManager` 注册观察者接收高德 APP 回传的消息：

```objc
__weak typeof(self) weakSelf = self;
[[AMapLinkClientObserverManager sharedInstance] addObserver:^(NSString * _Nonnull msg) {
    [weakSelf handleReceivedMessage:msg];
}];
```

## 断开连接

```objc
[[AMapLinkManager sharedInstance] disconnect];
```

## 注意事项

- `AMapLinkManager` 是全局单例，通过 `sharedInstance` 获取
- 建联前必须先完成授权（`isAuthored == YES`）
- 建联前应通过 `isConnected` 检查状态，避免重复连接
- 数据回调通过观察者模式接收，UI 更新需切换到主线程

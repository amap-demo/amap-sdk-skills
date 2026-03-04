# 日志管理

通过 `AMapAgentLog` 监听 SDK 内部日志，用于调试和问题排查。

## 设置日志代理

```objc
// 实现 AMapAgentLogProtocol 协议
@interface YourClass () <AMapAgentLogProtocol>
@end

@implementation YourClass

- (void)setupLogging {
    [[AMapAgentLog shareInstance] setLogDelegate:self];
}

#pragma mark - AMapAgentLogProtocol

- (void)onLog:(AMapAgentLogLevel)logLevel logContent:(NSString *)logContent {
    NSLog(@"[Agent %ld] %@", (long)logLevel, logContent);
}

@end
```

## AMapAgentLogLevel 日志级别

| 级别 | 值 | 说明 |
|------|-----|------|
| `Debug` | 0 | 调试信息 |
| `Info` | 1 | 一般信息 |
| `Warning` | 2 | 警告 |
| `Error` | 3 | 错误 |
| `Fatal` | 4 | 致命错误 |
| `Track` | 5 | 性能排查 |

> 重复调用 `setLogDelegate:` 会覆盖之前的代理。

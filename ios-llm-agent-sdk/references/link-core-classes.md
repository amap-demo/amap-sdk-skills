# 核心类参考

MALLMKit 中 IPC Link 相关的公共类速查表。基于 `AMapLinkClientViewController` 实际使用的 API。

## 核心管理类

### AMapLinkManager

**头文件**：`<MALLMKit/AMapLinkManager.h>` | IPC 连接管理器（单例）

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `+ sharedInstance` | 类方法 | 获取单例实例 |
| `- isConnected` | BOOL | 查询当前连接状态 |
| `- initWithConnectConfig:` | 实例方法 | 使用配置初始化连接 |
| `- connect` | 实例方法 | 发起连接 |
| `- disconnect` | 实例方法 | 断开连接 |
| `- sendDataToClient:` | 实例方法 | 发送 JSON 字符串数据 |

### AMapAuthorizationManager

**头文件**：`<MALLMKit/AMapAuthorizationManager.h>` | 授权管理器（单例）

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `+ sharedInstance` | 类方法 | 获取单例实例 |
| `- startAuthenticationWithCallback:` | 实例方法 | 发起授权，跳转高德 APP，回调返回 (BOOL success, NSError *error) |
| `- handleURL:` | 实例方法 | 处理授权回调 URL，返回 BOOL 表示授权结果 |

### AMapLinkConnectConfig

**头文件**：`<MALLMKit/AMapLinkConnectConfig.h>` | 连接配置

| 属性 | 类型 | 说明 |
|------|------|------|
| `autoReconnect` | `BOOL` | 是否自动重连 |
| `maxReconnectAttempts` | `NSUInteger` | 最大重连次数 |
| `reconnectDelay` | `NSTimeInterval` | 重连间隔（秒） |

## 工具类

### AMapLinkClientObserverManager

**头文件**：`AMapLinkClientObserverManager.h` | 数据接收观察者管理（单例）

| 方法 | 说明 |
|------|------|
| `+ sharedInstance` | 获取单例实例 |
| `- addObserver:` | 添加观察者，回调类型为 `void (^)(NSString *msg)` |

用于接收高德 APP 回传的消息数据。

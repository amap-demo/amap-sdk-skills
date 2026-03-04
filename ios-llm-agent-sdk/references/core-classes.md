# 核心类参考

MALLMKit 对外暴露的公共类（PublicHeaders）与枚举速查表。所有属性和方法均基于源码头文件定义。

## 管理器类（单例）

### AMapAgentClientManager

**头文件**：`AMapAgentClientManager.h` | **获取方式**：`[AMapAgentClientManager shareInstance]`

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `commandDestination` | `AMapAgentCommandDestination` | 链路模式（SDK / APP） |
| `+ configureAgentURL:` | 类方法 | 配置 Agent 服务器 URL |
| `+ currentAgentURL` | 类方法 | 获取当前 Agent URL |
| `- setQueryResultCallback:` | 实例方法 | 设置查询结果回调 |
| `- query:` | 实例方法 | 发起查询，参数为 `AMapAgentQueryParam`，返回 sessionId |
| `- resetAgentScene:` | 实例方法 | 重置场景（home/route/navi/search） |
| `- resetAgentStatus` | 实例方法 | 重置会话状态 |
| `- version` | 实例方法 | 获取版本号 |
| `+ destroy` | 类方法 | 销毁单例 |

### AMapNaviClientManager

**头文件**：`AMapNaviClientManager.h` | **获取方式**：`[AMapNaviClientManager shareInstance]`

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `defaultNaviEnv` | `AMapNaviEnv` | 全局默认导航配置 |
| `amapNaviEnv` | `AMapNaviEnv` | 当前导航配置（优先级更高） |
| `naviType` | `AMapNaviType` | 当前导航类型 |
| `locationUpdateInterval` | `NSTimeInterval` | 定位数据发送最小间隔（秒） |
| `- addNaviDataListener:` | 实例方法 | 添加导航 PB 数据监听 |
| `- removeNaviDataListener:` | 实例方法 | 移除导航 PB 数据监听 |
| `- addNaviTypeDataListener:` | 实例方法 | 添加类型化数据监听（APP 链路） |
| `- removeNaviTypeDataListener:` | 实例方法 | 移除类型化数据监听 |
| `- stopNavi` | 实例方法 | 停止导航 |
| `- switchRoute:` | 实例方法 | 切换路线 |
| `- switchBroadcastMode:` | 实例方法 | 设置播报模式（1简洁/2详细/0静音/6极简/7智能） |
| `- setAmapNaviView:` | 实例方法 | 设置导航视图（用于跟随模式回调） |
| `- updateMyLocation:` | 实例方法 | 更新定位信息 |
| `- forceRefreshRoute` | 实例方法 | 强制重刷路线 |
| `- getPartialRouteGroupWithLimitPointSize:` | 实例方法 | 获取精简路线 PB 数据 |
| `- onNaviManagerDestroyed:` | 实例方法 | 通知导航 Manager 销毁 |
| `+ destroy` | 类方法 | 销毁单例 |

### AMapLinkManager

**头文件**：`AMapLinkManager.h` | **获取方式**：`[AMapLinkManager sharedInstance]` | APP 链路 IPC 建联管理

### AMapAuthorizationManager

**头文件**：`AMapAuthorizationManager.h` | **获取方式**：`[AMapAuthorizationManager sharedInstance]` | APP 链路授权管理

### AMapAgentLog

**头文件**：`AMapAgentLog.h` | **获取方式**：`[AMapAgentLog shareInstance]`

| 方法 | 说明 |
|------|------|
| `- setLogDelegate:` | 设置日志代理（`id<AMapAgentLogProtocol>`） |

**AMapAgentLogProtocol 协议方法**：`- (void)onLog:(AMapAgentLogLevel)logLevel logContent:(NSString *)logContent;`

## 数据模型类

### AMapAgentQueryParam

**头文件**：`AMapAgentQueryParam.h`

| 属性 | 类型 | 说明 |
|------|------|------|
| `queryText` | `NSString` | 查询文本 |
| `lastActionType` | `AMapAgentQueryResultActionType` | 上一次查询的 actionType（多轮对话） |
| `selectedObject` | `id` | 上一次查询的结果对象（多轮对话） |

### AMapAgentQueryResult

**头文件**：`AMapAgentQueryResult.h`

| 属性 | 类型 | 说明 |
|------|------|------|
| `errorInfo` | `NSError *` | 错误信息（nil 表示成功） |
| `sessionId` | `NSString` | 会话 ID |
| `taskId` | `NSString` | 任务 ID |
| `tppTrace` | `NSString` | 服务 tppTrace ID |
| `sequence` | `NSInteger` | 任务序列号 |
| `actionType` | `AMapAgentQueryResultActionType` | 操作类型 |
| `stateType` | `AMapAgentQueryResultStateType` | 流式状态（Working/Append/End） |
| `resultType` | `AMapAgentQueryResultType` | 结果类型（Command/Summary） |
| `summary` | `NSString` | 总结文本 |
| `resultObj` | `id` | 结果对象（类型取决于 actionType） |
| `endPoiName` | `NSString` | 终点名称 |
| `viaPoiItem` | `AMapPOI *` | 途经点信息 |

**resultObj 类型对照**：
- `RequestRoute` → `NSDictionary<NSNumber *, AMapNaviRoute *>`
- `SearchPoi` / `SelectPoiWorkFlow` → `AMapPOIResult`
- `RouteSearch` → `NSArray<AMapRoutePOI *>`

### AMapNaviEnv

**头文件**：`AMapNaviEnv.h`

| 属性 | 类型 | 说明 |
|------|------|------|
| `homeLocation` | `AMapAgentPOI` | 家位置 |
| `workLocation` | `AMapAgentPOI` | 公司位置 |
| `amapNaviType` | `AMapNaviType` | 导航类型 |
| `amapVehicleInfo` | `AMapNaviVehicleInfo` | 车辆信息 |
| `multipleRoute` | `BOOL` | 是否多路径 |
| `avoidCongestion` | `BOOL` | 是否躲避拥堵 |
| `avoidHighway` | `BOOL` | 是否躲避高速 |
| `avoidCost` | `BOOL` | 是否躲避收费 |
| `prioritiseHighway` | `BOOL` | 是否优先高速 |

### 其他数据模型

| 类名 | 头文件 | 说明 |
|------|--------|------|
| `AMapAgentPOI` | `AMapAgentPOI.h` | POI 数据 |
| `AMapPOIResult` | `AMapPOIResult.h` | POI 搜索结果（poiItemArray） |
| `AMapNaviPbData` | `AMapNaviPbData.h` | 导航 PB 数据（data、type、source） |
| `AMapNaviTypeData` | `AMapNaviTypeData.h` | 类型化导航数据（resultObj、type、source） |
| `AMapLinkConnectConfig` | `AMapLinkConnectConfig.h` | 建联配置 |
| `AMapTaxiInfo` | `AMapTaxiInfo.h` | 打车信息 |

## Category

| 类名 | 头文件 | 说明 |
|------|--------|------|
| `AMapPOIExtension+AgentExtension` | `AMapPOIExtension+AgentExtension.h` | POI 扩展属性 |

## 关键枚举

### AMapAgentCommandDestination — 链路模式

| 值 | 说明 |
|----|------|
| `SDK` | 应用内 SDK 链路 |
| `APP` | 高德 APP 链路 |

### AMapAgentQueryResultActionType — 查询操作类型

| 值 | 说明 |
|----|------|
| `RequestRoute` | 行前请求路线 |
| `RequestRouteInNavi` | 行中请求路线 |
| `SearchPoi` | POI 搜索 |
| `SelectPoiWorkFlow` | 行前 POI 选点 |
| `SelectPoiWorkFlowSingle` | 单点选点 |
| `RouteSearch` | 行中顺路搜 |
| `ChangeOrViaPoi` | 行中变更 POI |
| `ExitNavi` | 退出导航 |
| `BreakSession` | 中断会话 |
| `Refuse` | 拒绝命令 |
| `SetAutoListen` | 闲聊指令 |
| `RequestGuideInfo` | 行中引导 |

### AMapAgentQueryResultStateType — 查询状态

| 值 | 说明 |
|----|------|
| `Working` | 进行中 |
| `Append` | 追加结果 |
| `End` | 结束 |

### AMapNaviDataType — 导航数据类型

| 值 | 编号 | 说明 |
|----|------|------|
| `CalcSuccess` | 1 | 算路成功 |
| `UpdateRouteGroup` | 2 | 路线数据更新 |
| `CalcFailed` | 3 | 算路失败 |
| `UpdateNaviInfo` | 4 | 导航信息更新 |
| `StartNavi` | 7 | 开始导航 |
| `PlayNaviSound` | 8 | 播报信息 |
| `ArrivedWayPoint` | 9 | 到达途经点 |
| `HighLightChanged` | 20 | 高亮路线变更 |
| `StopNavi` | 100 | 结束导航 |
| `ArrivedDestination` | 200 | 到达目的地 |

### AMapAgentLogLevel — 日志级别

| 值 | 编号 | 说明 |
|----|------|------|
| `Debug` | 0 | 调试 |
| `Info` | 1 | 信息 |
| `Warning` | 2 | 警告 |
| `Error` | 3 | 错误 |
| `Fatal` | 4 | 致命 |
| `Track` | 5 | 性能排查 |

### AMapAuthorizationErrorCode — 授权错误码

| 值 | 说明 |
|----|------|
| `AppAuthSuccess` | 授权成功 |
| `InvalidAPIKey` | 无效 apiKey |
| `MissingAPIKey` | 缺少 apiKey |
| `NetworkFailed` | 网络异常 |
| `AppNotInstalled` | APP 未安装 |
| `AppOpenFailed` | 跳转失败 |
| `AppAuthFailed` | 授权失败 |

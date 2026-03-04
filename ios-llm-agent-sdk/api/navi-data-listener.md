# 导航数据监听

通过 `addNaviDataListener` 实时监听导航过程中的各种数据更新。

## PB 数据监听

```objc
// 添加监听
NaviDataCallback callback = ^(AMapNaviPbData *naviData) {
    NSLog(@"类型: %ld, 来源: %ld", (long)naviData.type, (long)naviData.source);
};
[[AMapNaviClientManager shareInstance] addNaviDataListener:callback];

// 移除监听（需持有 callback 引用）
[[AMapNaviClientManager shareInstance] removeNaviDataListener:callback];
```

## AMapNaviPbData 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `data` | `NSData` | 导航 PB 二进制数据 |
| `type` | `AMapNaviDataType` | 数据类型枚举 |
| `source` | `AMapNaviDataSource` | 数据来源 |

## AMapNaviDataType 关键枚举值

| 枚举值 | 值 | 说明 |
|--------|-----|------|
| `CalcSuccess` | 1 | 算路成功 |
| `UpdateRouteGroup` | 2 | 路线数据更新（路线真正应用） |
| `CalcFailed` | 3 | 算路失败 |
| `UpdateNaviInfo` | 4 | 行中导航信息更新 |
| `StartNavi` | 7 | 开始导航 |
| `PlayNaviSound` | 8 | 播报导航信息 |
| `ArrivedWayPoint` | 9 | 到达途经点 |
| `ShowLaneInfo` | 14 | 车道线数据 |
| `HideLaneInfo` | 15 | 车道线隐藏 |
| `UpdateNaviLocation` | 16 | 定位信息更新 |
| `TrackingModeInfo` | 18 | 跟随模式 |
| `HighLightChanged` | 20 | 高亮路线变更 |
| `StopNavi` | 100 | 结束导航 |
| `ArrivedDestination` | 200 | 到达目的地 |

## AMapNaviDataSource 数据来源

| 枚举值 | 值 | 说明 |
|--------|-----|------|
| `Open` | 0 | 开平 SDK 内集成导航 |
| `OpenAgent` | 1 | 开平 Agent SDK |
| `AMap` | 2 | 高德 APP |

## 类型化数据监听

除 PB 原始数据外，还可监听类型化数据（APP 链路）：

```objc
[[AMapNaviClientManager shareInstance] addNaviTypeDataListener:^(AMapNaviTypeData *naviTypeData) {
    switch (naviTypeData.type) {
        case AMapNaviDataTypeUpdateRouteGroup:
            NSLog(@"路线数据更新，resultObj: %@", naviTypeData.resultObj);
            break;
        case AMapNaviDataTypeCalcSuccess:
            NSLog(@"算路成功");
            break;
        case AMapNaviDataTypeStartNavi:
            NSLog(@"开始导航");
            break;
        default:
            break;
    }
}];
```

## AMapNaviTypeData 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `resultObj` | `id` | 类型化结果对象，具体类型取决于 `type` |
| `type` | `AMapNaviDataType` | 数据类型枚举 |
| `source` | `AMapNaviDataSource` | 数据来源 |

## 重要注意事项

1. **必须在算路之前设置监听器**，否则可能收不到回调
2. `AMapNaviClientManager` 须正确设置 `naviType` 才能注册对应导航数据监听
3. 导航数据回调可能在子线程，UI 更新需切回主线程

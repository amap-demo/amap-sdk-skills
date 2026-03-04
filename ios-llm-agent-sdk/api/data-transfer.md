# 数据传输与命令

通过 IPC 连接向高德 APP 发送 JSON 命令，实现导航控制、途经点管理、播报设置等功能。

## 发送数据

通过 `AMapLinkManager` 的 `sendDataToClient:` 方法发送 JSON 字符串：

```objc
- (void)sendData:(NSDictionary *)data {
    if (!data || ![NSJSONSerialization isValidJSONObject:data]) {
        return;
    }

    NSError *error;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:data
                                                       options:NSJSONWritingSortedKeys
                                                         error:&error];
    NSString *jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];

    if (jsonString) {
        [[AMapLinkManager sharedInstance] sendDataToClient:jsonString];
    }
}
```

## 接收数据

通过 `AMapLinkClientObserverManager` 注册观察者接收高德 APP 回传的消息：

```objc
__weak typeof(self) weakSelf = self;
[[AMapLinkClientObserverManager sharedInstance] addObserver:^(NSString * _Nonnull msg) {
    dispatch_async(dispatch_get_main_queue(), ^{
        // 处理接收到的消息
        NSLog(@"收到消息: %@", msg);
    });
}];
```

## 导航命令参考

所有命令通过 JSON 格式发送，核心字段：
- **`cmd`**：命令类型编号
- **`data`**：命令参数（部分命令无需此字段）
- **`requestId`**：请求标识符

### 添加途经点（cmd: 3）

```objc
NSDictionary *command = @{
    @"cmd": @(3),
    @"data": @{
        @"lon": @116.397455,
        @"lat": @39.909187,
        @"name": @"天安门",
        @"poiid": @"B000A60DA1",
        @"entranceList": @[
            @{ @"lon": @116.397604, @"lat": @39.907697 }
        ]
    },
    @"requestId": @2222223
};
[self sendData:command];
```

### 更改目的地（cmd: 4）

```objc
NSDictionary *command = @{
    @"cmd": @(4),
    @"data": @{
        @"lon": @116.397455,
        @"lat": @39.909187,
        @"name": @"天安门",
        @"poiid": @"B000A60DA1",
        @"entranceList": @[
            @{ @"lon": @116.397604, @"lat": @39.907697 }
        ]
    },
    @"requestId": @2222224
};
[self sendData:command];
```

### 获取导航结构化数据（cmd: 5）

```objc
NSDictionary *command = @{
    @"cmd": @(5),
    @"requestId": @2222225
};
[self sendData:command];
```

### 更改播报设置（cmd: 6）

```objc
// 骑行播报模式：@"0"-关闭, @"1"-开启
- (void)changeRideBroadcast {
    NSArray *rideValues = @[@"0", @"1"];
    NSUInteger randomIndex = arc4random_uniform((uint32_t)rideValues.count);
    NSString *randomValue = rideValues[randomIndex];
    [self sendData:@{
        @"cmd": @(6),
        @"data": @{
            @"value": randomValue,
        },
        @"requestId": @2222226
    }];
}

// 驾车播报模式：0-静音, 1-简洁, 2-详细, 6-极简, 7-智能
- (void)changeCarBroadcast {
    NSArray *carValues = @[@(0), @(1), @(2), @(6), @(7)];
    NSUInteger randomIndex = arc4random_uniform((uint32_t)carValues.count);
    NSNumber *randomValue = carValues[randomIndex];
    [self sendData:@{
        @"cmd": @(6),
        @"data": @{
            @"value": randomValue,
        },
        @"requestId": @2222227
    }];
}
```

## 命令速查表

| cmd | 功能 | data 字段 |
|-----|------|-----------|
| 3 | 添加途经点 | lon, lat, name, poiid, entranceList |
| 4 | 更改目的地 | lon, lat, name, poiid, entranceList |
| 5 | 获取导航结构化数据 | 无 |
| 6 | 更改播报设置 | value（驾车: 0/1/2/6/7，骑行: "0"/"1"） |

## POI 数据结构

途经点和目的地命令中的 `data` 字段结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| `lon` | NSNumber | 经度 |
| `lat` | NSNumber | 纬度 |
| `name` | NSString | POI 名称 |
| `poiid` | NSString | POI ID |
| `entranceList` | NSArray | 入口坐标列表，每项含 lon/lat |

## 注意事项

- 发送数据前需确保连接已建立（`[[AMapLinkManager sharedInstance] isConnected] == YES`）
- JSON 数据必须通过 `isValidJSONObject:` 校验
- 驾车和骑行的播报 value 类型不同（NSNumber vs NSString）
- 观察者回调可能在子线程，UI 更新需切换到主线程

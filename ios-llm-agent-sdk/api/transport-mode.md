# 出行方式配置

通过 `AMapNaviEnv` 配置导航环境，包括出行方式、路线偏好和常用地点。

## 导航环境配置

`AMapNaviClientManager` 提供两级配置：

| 属性 | 说明 |
|------|------|
| `defaultNaviEnv` | 全局默认配置 |
| `amapNaviEnv` | 当前导航配置（优先级更高） |

```objc
AMapNaviEnv *env = [AMapNaviEnv new];

// 出行方式
env.amapNaviType = AMapNaviTypeDrive;  // AMapNaviTypeDrive / AMapNaviTypeRide / AMapNaviTypeWalk

// 路线偏好
env.multipleRoute = YES;       // 是否返回多条路线
env.avoidCongestion = NO;      // 躲避拥堵
env.avoidHighway = NO;         // 躲避高速
env.avoidCost = NO;            // 躲避收费
env.prioritiseHighway = NO;    // 优先高速

[AMapNaviClientManager shareInstance].amapNaviEnv = env;
```

## 设置家和公司位置

```objc
AMapAgentPOI *home = [AMapAgentPOI new];
home.name = @"我的家";
home.coordinate = CLLocationCoordinate2DMake(39.908823, 116.397470);
home.uid = @"HOME_POI_ID";
env.homeLocation = home;

AMapAgentPOI *work = [AMapAgentPOI new];
work.name = @"我的公司";
work.coordinate = CLLocationCoordinate2DMake(39.918823, 116.407470);
work.uid = @"WORK_POI_ID";
env.workLocation = work;
```

> 未设置家/公司位置时，用户说"回家"/"去公司"会返回 `HomeNotSet` / `CompanyNotSet` 错误。

## 导航类型同步

设置导航类型时需同步更新 `AMapNaviClientManager.naviType`：

```objc
[AMapNaviClientManager shareInstance].naviType = AMapNaviTypeDrive;
[AMapNaviClientManager shareInstance].amapNaviEnv.amapNaviType = AMapNaviTypeDrive;
```

## AMapAgentPOI 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `name` | `NSString` | POI 名称 |
| `coordinate` | `CLLocationCoordinate2D` | 经纬度坐标 |
| `uid` | `NSString` | POI 唯一标识 |

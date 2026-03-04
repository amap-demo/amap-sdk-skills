# 接入 Agent

触发词：**接入agent**

本文档说明如何新建一个 UIViewController 并通过 MALLMKit 接入 Agent SDK（SDK 直连模式）。生成的类名为 `AMapAgentDemoViewController`。

## 整体流程

```
1. 导入头文件 → 2. ViewController 声明 → 3. 初始化 Agent + 导航环境 → 4. 创建导航视图与 UI → 5. 初始化定位 → 6. 发起查询与多轮对话 → 7. 浮动快捷操作 → 8. 日志监听 → 9. 生命周期管理
```

## 1. 导入头文件

```objc
#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>
#import "AMapAgentDemoViewController.h"
#import <MALLMKit/AMapAgentClientManager.h>
#import <MALLMKit/AMapAgentQueryParam.h>
#import <MALLMKit/AMapAgentQueryResult.h>
#import <MALLMKit/AMapNaviClientManager.h>
#import <MALLMKit/AMapNaviPbData.h>
#import <MALLMKit/AMapAgentLog.h>
#import <MALLMKit/AMapPOIResult.h>
#import <MALLMKit/AMapNaviEnv.h>
#import <MALLMKit/AMapAgentPOI.h>
#import <MALLMKit/AMapNaviTypeData.h>
#import <AMapNaviKit/AMapNaviDriveDataRepresentable.h>
#import <AMapNaviKit/AMapNaviDriveManager.h>
#import <AMapNaviKit/AMapNaviRoute.h>
#import "UIView+Layout.h"
```

> 如果使用 APP 链路模式，还需导入：
> ```objc
> #import <MALLMKit/AMapLinkManager.h>
> #import <MALLMKit/AMapAuthorizationManager.h>
> #import <MALLMKit/AMapLinkConnectConfig.h>
> ```

## 2. ViewController 声明

### 头文件（.h）

```objc
#import <UIKit/UIKit.h>
#import <AMapNaviKit/AMapNaviKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface AMapAgentDemoViewController : UIViewController
@property (nonatomic, strong) MAMapView *mapView;
@property (nonatomic, strong) id mAMapNaviView;
@end

NS_ASSUME_NONNULL_END
```

### 实现文件（.m）

```objc
static const CGFloat AGENT_BTN_H = 30;
static const CGFloat AGENT_BTN_M = 6;
static const CGFloat AGENT_BTN_PADDING_H = 12;
static const CGFloat AGENT_BTN_PADDING_V = 4;
static const CGFloat AGENT_BTN_RADIUS = 15;
static const CGFloat AGENT_LOG_VIEW_H = 160;
typedef void (^AgentNaviDataCallback)(AMapNaviPbData *navidata);

@interface AMapAgentDemoViewController () <CLLocationManagerDelegate, AMapNaviDriveManagerDelegate, AMapNaviDriveDataRepresentable, AMapNaviDriveViewDelegate, MAMapViewDelegate, AMapAgentLogProtocol>
@property (nonatomic, strong) CLLocationManager *locationManager;
@property (nonatomic, copy) AgentNaviDataCallback naviDataCallback;
@property (nonatomic, strong) AMapPOIResult *currentPoiResult;
@property (nonatomic, copy) NSArray<AMapRoutePOI *> *routePois;
@property (nonatomic, strong) AMapAgentQueryResult *lastQueryResult;

@property (nonatomic, strong) UIButton *mStopNaviButton;
@property (nonatomic, strong) UIButton *mNextActionButton;
@property (nonatomic, strong) UIButton *mYesActionButton;
@property (nonatomic, strong) UITextField *queryTextField;
@property (nonatomic, strong) UIView *inputContainerView;
@property (nonatomic, strong) UITextView *logTextView;
@property (nonatomic, strong) UIView *logContainerView;
@end
```

## 3. 初始化流程（在 init 中调用 initAgent + initNavi）

初始化在 `init` 中完成，确保 Agent 和导航环境在 `viewDidLoad` 之前就绑定好：

```objc
- (instancetype)init {
    if (self = [super init]) {
        [self initAgent];
        [self initNavi];
    }
    return self;
}
```

### 3.1 initAgent — 设置链路模式、日志、查询回调、重置场景

```objc
- (void)initAgent {
    // 设置链路模式为 SDK 直连
    [AMapAgentClientManager shareInstance].commandDestination = AMapAgentCommandDestinationSDK;
    // 设置日志监听
    [[AMapAgentLog shareInstance] setLogDelegate:self];
    // 设置查询结果回调
    __weak typeof(self) weakSelf = self;
    [[AMapAgentClientManager shareInstance] setQueryResultCallback:^(AMapAgentQueryResult * _Nonnull queryResult) {
        __strong typeof(weakSelf) strongSelf = weakSelf;
        NSString *logMsg = [NSString stringWithFormat:@"summary: %@, actionType: %ld, stateType: %ld, seq: %ld",
                             queryResult.summary, (long)queryResult.actionType,
                             (long)queryResult.stateType, (long)queryResult.sequence];
        NSLog(@"onQueryResult %@, sessionID: %@", logMsg, queryResult.sessionId);
        [strongSelf appendLogMessage:logMsg];

        if (queryResult.resultObj) {
            if (queryResult.actionType == AMapAgentQueryResultActionTypeSearchPoi) {
                // POI 搜索结果
                strongSelf.currentPoiResult = queryResult.resultObj;
            } else if (queryResult.actionType == AMapAgentQueryResultActionTypeRouteSearch) {
                // 顺路搜结果
                strongSelf.routePois = queryResult.resultObj;
            } else if (queryResult.actionType == AMapAgentQueryResultActionTypeRequestRoute) {
                // 路线规划完成，自动开始驾车模拟导航
                [[AMapNaviDriveManager sharedInstance] setIsUseInternalTTS:YES];
                [[AMapNaviDriveManager sharedInstance] selectNaviRouteWithRouteID:0];
                [[AMapNaviDriveManager sharedInstance] setEmulatorNaviSpeed:120];
                [[AMapNaviDriveManager sharedInstance] startEmulatorNavi];
            }
        }
        strongSelf.lastQueryResult = queryResult;
    }];
    // 重置场景到主图
    [[AMapAgentClientManager shareInstance] resetAgentScene:@"home"];
}
```

### 3.2 initNavi — 配置导航环境、家/公司位置、车辆信息、导航数据监听

```objc
- (void)initNavi {
    AMapNaviEnv *env = [AMapNaviEnv new];
    AMapAgentPOI *homeLocation = [AMapAgentPOI new];
    env.homeLocation = homeLocation;
    AMapAgentPOI *workLocation = [AMapAgentPOI new];
    env.workLocation = workLocation;
    env.homeLocation.name = @"望京西园一区";
    env.homeLocation.coordinate = CLLocationCoordinate2DMake(40.004585, 116.476334);
    env.homeLocation.uid = @"B000A7QPDF";
    env.workLocation.name = @"阿里中心·望京B座";
    env.workLocation.coordinate = CLLocationCoordinate2DMake(40.002577, 116.489854);
    env.workLocation.uid = @"B0FFHU7UFS";
    AMapNaviVehicleInfo *carInfo = [AMapNaviVehicleInfo new];
    env.amapVehicleInfo = carInfo;
    env.amapVehicleInfo.vehicleId = @"京DFZ588";
    env.amapNaviType = AMapNaviTypeDrive;
    env.multipleRoute = YES;
    env.avoidCongestion = NO;
    env.avoidHighway = NO;
    env.avoidCost = NO;
    env.prioritiseHighway = NO;
    [AMapNaviClientManager shareInstance].amapNaviEnv = env;
    [AMapNaviClientManager shareInstance].locationUpdateInterval = 1.0;
    // 导航数据监听
    self.naviDataCallback = ^(AMapNaviPbData * _Nonnull navidata) {
    };
    [[AMapNaviClientManager shareInstance] addNaviDataListener:self.naviDataCallback];
}
```

> **初始化顺序要求**：`AMapAgentClientManager` 和 `AMapNaviClientManager` 必须在 `AMapLinkManager` 之前初始化。

## 4. 创建导航视图与 UI（在 viewDidLoad 中）

`viewDidLoad` 中依次创建：导航视图 → 底部输入区域 → 日志面板 → 浮动操作按钮 → 初始化定位。

```objc
- (void)viewDidLoad {
    [super viewDidLoad];

    // 1. 创建导航视图（全屏）
    self.mAMapNaviView = [[AMapNaviDriveView alloc] initWithFrame:CGRectMake(0, 0, self.view.bounds.size.width, self.view.bounds.size.height)];
    [[AMapNaviClientManager shareInstance] setAmapNaviView:self.mAMapNaviView];
    [(AMapNaviDriveView *)self.mAMapNaviView setDelegate:self];
    [self.view addSubview:self.mAMapNaviView];
    [[AMapNaviDriveManager sharedInstance] addDataRepresentative:self.mAMapNaviView];

    // 2. 底部输入区域（输入框 + 发送查询 / 重置对话按钮）
    CGFloat inputAreaHeight = 110;
    CGFloat inputAreaY = self.view.height - inputAreaHeight;
    self.inputContainerView = [[UIView alloc] initWithFrame:CGRectMake(0, inputAreaY, self.view.width, inputAreaHeight)];
    self.inputContainerView.backgroundColor = [UIColor whiteColor];
    self.inputContainerView.layer.shadowColor = [UIColor blackColor].CGColor;
    self.inputContainerView.layer.shadowOffset = CGSizeMake(0, -2);
    self.inputContainerView.layer.shadowOpacity = 0.15;
    self.inputContainerView.layer.shadowRadius = 4;
    [self.view addSubview:self.inputContainerView];

    CGFloat horizontalPadding = 16;
    // 输入框（橙色边框）
    self.queryTextField = [[UITextField alloc] initWithFrame:CGRectMake(horizontalPadding, 10, self.view.width - horizontalPadding * 2, 44)];
    self.queryTextField.placeholder = @"输入查询词，如：导航去天安门。";
    self.queryTextField.font = [UIFont systemFontOfSize:16];
    self.queryTextField.borderStyle = UITextBorderStyleNone;
    self.queryTextField.layer.borderColor = [UIColor orangeColor].CGColor;
    self.queryTextField.layer.borderWidth = 2.0;
    self.queryTextField.layer.cornerRadius = 4;
    self.queryTextField.leftView = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 12, 44)];
    self.queryTextField.leftViewMode = UITextFieldViewModeAlways;
    self.queryTextField.rightView = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 12, 44)];
    self.queryTextField.rightViewMode = UITextFieldViewModeAlways;
    self.queryTextField.returnKeyType = UIReturnKeySend;
    [self.queryTextField addTarget:self action:@selector(sendQueryAction) forControlEvents:UIControlEventEditingDidEndOnExit];
    [self.inputContainerView addSubview:self.queryTextField];

    // "发送查询" 和 "重置对话" 按钮
    CGFloat btnWidth = (self.view.width - horizontalPadding * 2 - 12) / 2.0;
    CGFloat btnHeight = 44;
    CGFloat btnY = 10 + 44 + 8;

    UIButton *sendButton = [UIButton buttonWithType:UIButtonTypeSystem];
    sendButton.frame = CGRectMake(horizontalPadding, btnY, btnWidth, btnHeight);
    [sendButton setTitle:@"发送查询" forState:UIControlStateNormal];
    sendButton.titleLabel.font = [UIFont boldSystemFontOfSize:16];
    sendButton.backgroundColor = [UIColor whiteColor];
    [sendButton setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
    sendButton.layer.borderColor = [UIColor lightGrayColor].CGColor;
    sendButton.layer.borderWidth = 1.0;
    sendButton.layer.cornerRadius = 4;
    [sendButton addTarget:self action:@selector(sendQueryAction) forControlEvents:UIControlEventTouchUpInside];
    [self.inputContainerView addSubview:sendButton];

    UIButton *resetButton = [UIButton buttonWithType:UIButtonTypeSystem];
    resetButton.frame = CGRectMake(horizontalPadding + btnWidth + 12, btnY, btnWidth, btnHeight);
    [resetButton setTitle:@"重置对话" forState:UIControlStateNormal];
    resetButton.titleLabel.font = [UIFont boldSystemFontOfSize:16];
    resetButton.backgroundColor = [UIColor whiteColor];
    [resetButton setTitleColor:[UIColor blackColor] forState:UIControlStateNormal];
    resetButton.layer.borderColor = [UIColor lightGrayColor].CGColor;
    resetButton.layer.borderWidth = 1.0;
    resetButton.layer.cornerRadius = 4;
    [resetButton addTarget:self action:@selector(resetConversationAction) forControlEvents:UIControlEventTouchUpInside];
    [self.inputContainerView addSubview:resetButton];

    // 3. Agent 回调日志面板（在输入区域上方）
    CGFloat logPanelHeight = AGENT_LOG_VIEW_H;
    CGFloat logTop = inputAreaY - logPanelHeight;
    self.logContainerView = [[UIView alloc] initWithFrame:CGRectMake(0, logTop, self.view.width, logPanelHeight)];
    self.logContainerView.backgroundColor = [[UIColor blackColor] colorWithAlphaComponent:0.7];
    [self.view addSubview:self.logContainerView];

    UILabel *logTitleLabel = [[UILabel alloc] initWithFrame:CGRectMake(12, 4, 200, 20)];
    logTitleLabel.text = @"📋 Agent 回调日志";
    logTitleLabel.textColor = [[UIColor whiteColor] colorWithAlphaComponent:0.8];
    logTitleLabel.font = [UIFont boldSystemFontOfSize:12];
    [self.logContainerView addSubview:logTitleLabel];

    self.logTextView = [[UITextView alloc] initWithFrame:CGRectMake(8, 24, self.view.width - 16, logPanelHeight - 28)];
    self.logTextView.backgroundColor = [UIColor clearColor];
    self.logTextView.textColor = [UIColor greenColor];
    self.logTextView.font = [UIFont fontWithName:@"Menlo" size:11];
    self.logTextView.editable = NO;
    self.logTextView.scrollEnabled = YES;
    self.logTextView.showsVerticalScrollIndicator = YES;
    self.logTextView.textContainer.lineBreakMode = NSLineBreakByWordWrapping;
    self.logTextView.textContainer.maximumNumberOfLines = 0;
    self.logTextView.textContainerInset = UIEdgeInsetsMake(4, 0, 4, 0);
    self.logTextView.text = @"等待 Agent 回调...\n";
    [self.logContainerView addSubview:self.logTextView];

    // 4. 浮动操作按钮（日志面板上方：去第一个、是的、停止导航）
    CGFloat floatingY = self.logContainerView.top - AGENT_BTN_H - 12;
    CGFloat floatingX = self.view.width - AGENT_BTN_M;

    self.mStopNaviButton = [self createOutlineButton:@"⏹ 停止导航" action:@selector(testStopNavi) color:[UIColor systemRedColor]];
    [self.mStopNaviButton sizeToFit];
    self.mStopNaviButton.frame = CGRectMake(floatingX - self.mStopNaviButton.width, floatingY, self.mStopNaviButton.width, AGENT_BTN_H);
    [self.view addSubview:self.mStopNaviButton];
    floatingX = self.mStopNaviButton.left - AGENT_BTN_M;

    self.mYesActionButton = [self createOutlineButton:@"✅ 是的" action:@selector(testSelectYes) color:[UIColor systemGreenColor]];
    [self.mYesActionButton sizeToFit];
    self.mYesActionButton.frame = CGRectMake(floatingX - self.mYesActionButton.width, floatingY, self.mYesActionButton.width, AGENT_BTN_H);
    [self.view addSubview:self.mYesActionButton];
    floatingX = self.mYesActionButton.left - AGENT_BTN_M;

    self.mNextActionButton = [self createOutlineButton:@"👉 去第一个" action:@selector(testSelectFirst) color:[UIColor systemPurpleColor]];
    [self.mNextActionButton sizeToFit];
    self.mNextActionButton.frame = CGRectMake(floatingX - self.mNextActionButton.width, floatingY, self.mNextActionButton.width, AGENT_BTN_H);
    [self.view addSubview:self.mNextActionButton];

    // 5. 初始化定位
    [self initLocation];
}
```

### UI 辅助方法

```objc
- (UIButton *)createOutlineButton:(NSString *)title action:(SEL)action color:(UIColor *)color {
    UIButton *button = [UIButton buttonWithType:UIButtonTypeCustom];
    [button setTitle:title forState:UIControlStateNormal];
    [button setTitleColor:color forState:UIControlStateNormal];
    button.titleLabel.font = [UIFont systemFontOfSize:13 weight:UIFontWeightSemibold];
    button.backgroundColor = [[UIColor whiteColor] colorWithAlphaComponent:0.9];
    button.layer.cornerRadius = AGENT_BTN_RADIUS;
    button.layer.masksToBounds = YES;
    button.layer.borderWidth = 1.5;
    button.layer.borderColor = color.CGColor;
    button.contentEdgeInsets = UIEdgeInsetsMake(AGENT_BTN_PADDING_V, AGENT_BTN_PADDING_H, AGENT_BTN_PADDING_V, AGENT_BTN_PADDING_H);
    [button addTarget:self action:action forControlEvents:UIControlEventTouchUpInside];
    return button;
}

- (void)appendLogMessage:(NSString *)message {
    dispatch_async(dispatch_get_main_queue(), ^{
        NSString *timestamp = [NSDateFormatter localizedStringFromDate:[NSDate date]
                                                            dateStyle:NSDateFormatterNoStyle
                                                            timeStyle:NSDateFormatterMediumStyle];
        NSString *logLine = [NSString stringWithFormat:@"[%@] %@\n", timestamp, message];
        self.logTextView.text = [self.logTextView.text stringByAppendingString:logLine];
        NSRange bottom = NSMakeRange(self.logTextView.text.length - 1, 1);
        [self.logTextView scrollRangeToVisible:bottom];
    });
}
```

## 5. 定位管理

```objc
- (void)initLocation {
    self.locationManager = [[CLLocationManager alloc] init];
    self.locationManager.delegate = self;
    self.locationManager.desiredAccuracy = kCLLocationAccuracyBest;
    [self startLocationServices];
}

- (void)startLocationServices {
    [self.locationManager startUpdatingLocation];
}

- (void)locationManagerDidChangeAuthorization:(CLLocationManager *)manager {
    CLAuthorizationStatus status = [CLLocationManager authorizationStatus];
    if (status == kCLAuthorizationStatusNotDetermined) {
        [manager requestWhenInUseAuthorization];
    } else if (status == kCLAuthorizationStatusAuthorizedWhenInUse ||
               status == kCLAuthorizationStatusAuthorizedAlways) {
        [manager startUpdatingLocation];
    } else {
        NSLog(@"定位权限未授予");
    }
}

- (void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray<CLLocation *> *)locations {
    CLLocation *location = [locations lastObject];
    [[AMapNaviClientManager shareInstance] updateMyLocation:location];
}

- (void)locationManager:(CLLocationManager *)manager didFailWithError:(NSError *)error {
    NSLog(@"定位失败: %@", error.localizedDescription);
}
```

## 6. 发起查询与多轮对话

### 基础查询方法

```objc
- (NSString *)query:(AMapAgentQueryParam *)param {
    NSString *sessionId = [[AMapAgentClientManager shareInstance] query:param];
    return sessionId;
}
```

### 输入框发送查询（自动携带多轮上下文）

用户在输入框中输入自然语言查询词，点击"发送查询"或按回车键发送。自动携带上一次的搜索结果上下文，实现多轮对话：

```objc
- (void)sendQueryAction {
    NSString *queryText = self.queryTextField.text;
    if (queryText.length == 0) {
        return;
    }
    AMapAgentQueryParam *param = [AMapAgentQueryParam new];
    param.queryText = queryText;
    // 多轮对话：自动携带上一次的搜索结果上下文
    if (self.currentPoiResult) {
        param.selectedObject = self.currentPoiResult;
        param.lastActionType = AMapAgentQueryResultActionTypeSearchPoi;
    } else if (self.routePois) {
        param.selectedObject = self.routePois;
        param.lastActionType = AMapAgentQueryResultActionTypeRouteSearch;
    }
    [self query:param];
    self.queryTextField.text = @"";
    [self.queryTextField resignFirstResponder];
}
```

### 重置对话

清除所有多轮上下文，重置场景到主图：

```objc
- (void)resetConversationAction {
    self.currentPoiResult = nil;
    self.routePois = nil;
    self.lastQueryResult = nil;
    self.logTextView.text = @"";
    self.queryTextField.text = @"";
    [[AMapAgentClientManager shareInstance] resetAgentScene:@"home"];
    [self appendLogMessage:@"对话已重置，场景切换到主图"];
}
```

## 7. 浮动快捷操作

三个浮动按钮用于常见的多轮交互快捷操作：

```objc
// 选择搜索结果中的第一个
- (void)testSelectFirst {
    AMapAgentQueryParam *param = [AMapAgentQueryParam new];
    param.queryText = @"第一个";
    if (self.currentPoiResult) {
        param.selectedObject = self.currentPoiResult;
        param.lastActionType = AMapAgentQueryResultActionTypeSearchPoi;
    } else if (self.routePois) {
        param.selectedObject = self.routePois;
        param.lastActionType = AMapAgentQueryResultActionTypeRouteSearch;
    }
    [self query:param];
}

// 确认选择
- (void)testSelectYes {
    AMapAgentQueryParam *param = [AMapAgentQueryParam new];
    param.queryText = @"是的，确认";
    if (self.currentPoiResult) {
        param.selectedObject = self.currentPoiResult;
        param.lastActionType = AMapAgentQueryResultActionTypeSearchPoi;
    }
    [self query:param];
}

// 停止导航
- (void)testStopNavi {
    AMapAgentQueryParam *param = [AMapAgentQueryParam new];
    param.queryText = @"结束导航";
    [self query:param];
}
```

## 8. 场景管理

查询前需确保场景正确，影响 Agent 对意图的理解：

```objc
// 行前主图场景
[[AMapAgentClientManager shareInstance] resetAgentScene:@"home"];

// 路线规划场景（算路成功后切换）
[[AMapAgentClientManager shareInstance] resetAgentScene:@"route"];

// 行中导航场景（开始导航后切换）
[[AMapAgentClientManager shareInstance] resetAgentScene:@"navi"];

// 搜索场景
[[AMapAgentClientManager shareInstance] resetAgentScene:@"search"];
```

## 9. 日志监听（AMapAgentLogProtocol）

```objc
- (void)onLog:(AMapAgentLogLevel)logLevel logContent:(NSString *)logContent {
    NSLog(@"logLevel: %lu, message: %@", logLevel, logContent);
}
```

## 10. 生命周期管理

```objc
- (void)viewDidDisappear:(BOOL)animated {
    [AMapAgentClientManager destroy];
    [AMapNaviClientManager destroy];
    [self.locationManager stopUpdatingLocation];
}
```

> **注意**：`AMapAgentClientManager` 和 `AMapNaviClientManager` 是全局单例，通常不需要在页面销毁时调用 `destroy`。仅在确定不再使用 SDK 时才调用。

## 11. 错误码参考

| 错误码 | 常量 | 说明 |
|--------|------|------|
| -20001 | `AMapAgentQueryResultErrorCodeCmdNotSupport` | 当前命令不支持 |
| -20002 | `AMapAgentQueryResultErrorCodeQueryTimeout` | query 超时 |
| -20003 | `AMapAgentQueryResultErrorCodeHomeNotSet` | 家位置未设置 |
| -20004 | `AMapAgentQueryResultErrorCodeCompanyNotSet` | 公司位置未设置 |
| -20005 | `AMapAgentQueryResultErrorCodeCmdTimeout` | 命令执行超时 |
| -20006 | `AMapAgentQueryResultErrorCodeViaNotFound` | 未找到途经点 |
| -20007 | `AMapAgentQueryResultErrorCodeDoAction` | doaction 参数错误 |
| -20008 | `AMapAgentQueryResultErrorCodeRequestRoute` | requestRoute 参数错误 |

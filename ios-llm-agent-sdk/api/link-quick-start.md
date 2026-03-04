# 链接高德 APP

触发词：**链接高德app**

本文档说明如何新建一个 UIViewController 并通过 MALLMKit 接入 Link SDK，实现与高德地图 APP 的 IPC 通信（授权认证、建联、收发数据）。生成的类名为 `AMapLinkDemoViewController`，同时生成配套的 `AMapLinkDemoNavBarView`（导航栏，高德蓝渐变背景 + 返回按钮）和 `AMapLinkDemoEventActionView`（操作按钮面板，分组配色 + 卡片式布局）。

## 整体流程

```
1. 创建 AMapLinkDemoNavBarView → 2. 创建 AMapLinkDemoEventActionView → 3. 创建 AMapLinkDemoViewController → 4. 配置 Info.plist → 5. 处理授权回调 URL
```

## 1. 创建 AMapLinkDemoNavBarView（导航栏视图）

### 头文件（AMapLinkDemoNavBarView.h）

```objc
#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface AMapLinkDemoNavBarView : UIView

@property (nonatomic, strong) UILabel *titleLabel;
@property (nonatomic, strong) UIButton *backButton;
@property (nonatomic, copy, nullable) void (^onBackTapped)(void);

- (instancetype)initWithFrame:(CGRect)frame;
- (void)setTitle:(NSString *)title;

@end

NS_ASSUME_NONNULL_END
```

### 实现文件（AMapLinkDemoNavBarView.m）

```objc
#import "AMapLinkDemoNavBarView.h"

@implementation AMapLinkDemoNavBarView

- (instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        // 高德蓝渐变背景
        CAGradientLayer *gradient = [CAGradientLayer layer];
        gradient.frame = CGRectMake(0, 0, frame.size.width, frame.size.height);
        gradient.colors = @[
            (__bridge id)[UIColor colorWithRed:0.0 green:0.48 blue:1.0 alpha:1.0].CGColor,
            (__bridge id)[UIColor colorWithRed:0.0 green:0.36 blue:0.85 alpha:1.0].CGColor
        ];
        gradient.startPoint = CGPointMake(0, 0);
        gradient.endPoint = CGPointMake(1, 1);
        [self.layer insertSublayer:gradient atIndex:0];

        // 返回按钮
        _backButton = [UIButton buttonWithType:UIButtonTypeSystem];
        [_backButton setTitle:@"‹ 返回" forState:UIControlStateNormal];
        [_backButton setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
        _backButton.titleLabel.font = [UIFont systemFontOfSize:16.0 weight:UIFontWeightMedium];
        [_backButton addTarget:self action:@selector(backButtonTapped) forControlEvents:UIControlEventTouchUpInside];
        [self addSubview:_backButton];

        // 标题
        _titleLabel = [[UILabel alloc] init];
        _titleLabel.textAlignment = NSTextAlignmentCenter;
        _titleLabel.font = [UIFont boldSystemFontOfSize:18.0];
        _titleLabel.textColor = [UIColor whiteColor];
        [self addSubview:_titleLabel];

        // 底部阴影线
        self.layer.shadowColor = [UIColor blackColor].CGColor;
        self.layer.shadowOffset = CGSizeMake(0, 2);
        self.layer.shadowOpacity = 0.1;
        self.layer.shadowRadius = 4;
    }
    return self;
}

- (void)layoutSubviews {
    [super layoutSubviews];
    CGFloat statusBarHeight = 20;
    if (@available(iOS 11.0, *)) {
        UIWindow *window = UIApplication.sharedApplication.windows.firstObject;
        statusBarHeight = window.safeAreaInsets.top;
    }
    CGFloat titleHeight = 44;
    CGFloat titleWidth = self.bounds.size.width - 160;
    _titleLabel.frame = CGRectMake((self.bounds.size.width - titleWidth) / 2, statusBarHeight, titleWidth, titleHeight);
    _backButton.frame = CGRectMake(8, statusBarHeight, 70, titleHeight);

    // 更新渐变 layer 尺寸
    CAGradientLayer *gradient = (CAGradientLayer *)self.layer.sublayers.firstObject;
    if ([gradient isKindOfClass:[CAGradientLayer class]]) {
        gradient.frame = self.bounds;
    }
}

- (void)backButtonTapped {
    if (self.onBackTapped) {
        self.onBackTapped();
    }
}

- (void)setTitle:(NSString *)title {
    self.titleLabel.text = title;
}

@end
```

## 2. 创建 AMapLinkDemoEventActionView（操作按钮面板）

### 头文件（AMapLinkDemoEventActionView.h）

```objc
#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@protocol AMapLinkDemoEventActionViewDelegate <NSObject>

- (void)openAmap;
- (void)createConnect;
- (void)disconnect;
- (void)sendData;
- (void)startNavi;
- (void)changeRideBroadcast;
- (void)changeCarBroadcast;
- (void)changeDestination;
- (void)addViaPoint;
- (void)copyLog;
- (void)clearLog;

@end

@interface AMapLinkDemoEventActionView : UIView

@property (nonatomic, weak) id<AMapLinkDemoEventActionViewDelegate> delegate;

- (instancetype)initWithOriginX:(CGFloat)x originY:(CGFloat)y width:(CGFloat)width;
- (void)updateInfo:(NSDictionary *)dict;

@end

NS_ASSUME_NONNULL_END
```

### 实现文件（AMapLinkDemoEventActionView.m）

```objc
#import "AMapLinkDemoEventActionView.h"

@interface AMapLinkDemoEventActionView ()

@property (nonatomic, strong) NSArray *btnDataList;
@property (nonatomic, strong) NSMutableArray *btnViewList;

@end

typedef NS_ENUM(NSUInteger, AMapLinkDemoBtnType) {
    AMapLinkDemoBtnType_openAmap = 1,
    AMapLinkDemoBtnType_createConnect,
    AMapLinkDemoBtnType_sendData,
    AMapLinkDemoBtnType_disconnect,
    AMapLinkDemoBtnType_startNavi,
    AMapLinkDemoBtnType_changeRideBroadcast,
    AMapLinkDemoBtnType_changeCarBroadcast,
    AMapLinkDemoBtnType_changeDestination,
    AMapLinkDemoBtnType_addViaPoint,
    AMapLinkDemoBtnType_copyLog,
    AMapLinkDemoBtnType_clearLog
};

@implementation AMapLinkDemoEventActionView

- (instancetype)initWithOriginX:(CGFloat)x originY:(CGFloat)y width:(CGFloat)width {
    CGFloat height = [self calculateRequiredHeight:width];
    CGRect frame = CGRectMake(x, y, width, height);
    return [self initWithFrame:frame];
}

- (instancetype)initWithFrame:(CGRect)frame {
    self = [super initWithFrame:frame];
    if (self) {
        _btnViewList = [NSMutableArray array];
        [self initUI];
        [self updateInfo:@{}];
    }
    return self;
}

- (void)updateInfo:(NSDictionary *)dict {
    BOOL isConnected = [[dict valueForKey:@"isConnected"] boolValue];
    BOOL isAuthored = [[dict valueForKey:@"isAuthored"] integerValue];

    UIColor *amapBlue = [UIColor colorWithRed:0.0 green:0.48 blue:1.0 alpha:1.0];
    UIColor *successGreen = [UIColor colorWithRed:0.2 green:0.78 blue:0.35 alpha:1.0];

    for (UIButton *button in self.btnViewList) {
        NSInteger index = button.tag;
        NSDictionary *btnInfo = self.btnDataList[index];
        AMapLinkDemoBtnType btnType = [btnInfo[@"btnType"] integerValue];

        if (btnType == AMapLinkDemoBtnType_openAmap) {
            if (isAuthored) {
                [button setEnabled:NO];
                [button setTitle:@"✓ 已鉴权" forState:UIControlStateDisabled];
                button.backgroundColor = [successGreen colorWithAlphaComponent:0.15];
                [button setTitleColor:successGreen forState:UIControlStateDisabled];
                button.layer.borderColor = successGreen.CGColor;
            } else {
                [button setEnabled:YES];
                [button setTitle:@"鉴权验证" forState:UIControlStateNormal];
                button.backgroundColor = amapBlue;
                [button setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
                button.layer.borderColor = amapBlue.CGColor;
            }
        } else if (btnType == AMapLinkDemoBtnType_createConnect) {
            if (isConnected && isAuthored) {
                [button setEnabled:NO];
                [button setTitle:@"✓ 已连接" forState:UIControlStateDisabled];
                button.backgroundColor = [successGreen colorWithAlphaComponent:0.15];
                [button setTitleColor:successGreen forState:UIControlStateDisabled];
                button.layer.borderColor = successGreen.CGColor;
            } else {
                [button setTitle:@"创建连接" forState:UIControlStateNormal];
                [button setEnabled:isAuthored ? YES : NO];
                if (isAuthored) {
                    button.backgroundColor = amapBlue;
                    [button setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
                    button.layer.borderColor = amapBlue.CGColor;
                } else {
                    button.backgroundColor = [UIColor colorWithRed:0.95 green:0.95 blue:0.95 alpha:1.0];
                    [button setTitleColor:[UIColor colorWithRed:0.7 green:0.7 blue:0.7 alpha:1.0] forState:UIControlStateDisabled];
                    button.layer.borderColor = [UIColor colorWithRed:0.88 green:0.88 blue:0.88 alpha:1.0].CGColor;
                }
            }
        } else if (btnType == AMapLinkDemoBtnType_copyLog || btnType == AMapLinkDemoBtnType_clearLog) {
            // 日志操作按钮始终可用
            [button setEnabled:YES];
            button.backgroundColor = [UIColor colorWithRed:0.96 green:0.96 blue:0.97 alpha:1.0];
            [button setTitleColor:[UIColor colorWithRed:0.4 green:0.4 blue:0.45 alpha:1.0] forState:UIControlStateNormal];
            button.layer.borderColor = [UIColor colorWithRed:0.88 green:0.88 blue:0.88 alpha:1.0].CGColor;
        } else {
            if (isConnected && isAuthored) {
                [button setEnabled:YES];
                button.backgroundColor = [UIColor whiteColor];
                [button setTitleColor:[UIColor colorWithRed:0.2 green:0.2 blue:0.25 alpha:1.0] forState:UIControlStateNormal];
                button.layer.borderColor = [UIColor colorWithRed:0.82 green:0.82 blue:0.85 alpha:1.0].CGColor;
            } else {
                [button setEnabled:NO];
                button.backgroundColor = [UIColor colorWithRed:0.95 green:0.95 blue:0.95 alpha:1.0];
                [button setTitleColor:[UIColor colorWithRed:0.7 green:0.7 blue:0.7 alpha:1.0] forState:UIControlStateDisabled];
                button.layer.borderColor = [UIColor colorWithRed:0.88 green:0.88 blue:0.88 alpha:1.0].CGColor;
            }
        }
    }
}

- (void)handleButtonClick:(UIButton *)sender {
    NSInteger index = sender.tag;
    if (index >= 0 && index < self.btnDataList.count) {
        NSDictionary *btnInfo = self.btnDataList[index];
        SEL action = NSSelectorFromString(btnInfo[@"action"]);
        if (action && [self.delegate respondsToSelector:action]) {
            [self.delegate performSelector:action];
        }
    }
}

- (NSArray *)btnDataList {
    return @[
        @{ @"title": @"鉴权验证",           @"action": @"openAmap",            @"btnType": @(AMapLinkDemoBtnType_openAmap) },
        @{ @"title": @"创建连接",           @"action": @"createConnect",        @"btnType": @(AMapLinkDemoBtnType_createConnect) },
        @{ @"title": @"测试联通性",          @"action": @"sendData",            @"btnType": @(AMapLinkDemoBtnType_sendData) },
        @{ @"title": @"断开链接",           @"action": @"disconnect",           @"btnType": @(AMapLinkDemoBtnType_disconnect) },
        @{ @"title": @"获取导航结构化数据",   @"action": @"startNavi",           @"btnType": @(AMapLinkDemoBtnType_startNavi) },
        @{ @"title": @"播报-ride",          @"action": @"changeRideBroadcast",  @"btnType": @(AMapLinkDemoBtnType_changeRideBroadcast) },
        @{ @"title": @"播报-car",           @"action": @"changeCarBroadcast",   @"btnType": @(AMapLinkDemoBtnType_changeCarBroadcast) },
        @{ @"title": @"更改目的地",          @"action": @"changeDestination",    @"btnType": @(AMapLinkDemoBtnType_changeDestination) },
        @{ @"title": @"添加途经点",          @"action": @"addViaPoint",          @"btnType": @(AMapLinkDemoBtnType_addViaPoint) },
        @{ @"title": @"复制",              @"action": @"copyLog",              @"btnType": @(AMapLinkDemoBtnType_copyLog) },
        @{ @"title": @"清空日志",           @"action": @"clearLog",             @"btnType": @(AMapLinkDemoBtnType_clearLog) }
    ];
}

- (CGFloat)calculateRequiredHeight:(CGFloat)width {
    CGFloat buttonWidth = 100.0;
    CGFloat buttonHeight = 32.0;
    CGFloat horizontalMargin = 10.0;
    CGFloat verticalMargin = 8.0;
    int buttonsPerRow = floor((width + horizontalMargin) / (buttonWidth + horizontalMargin));
    if (buttonsPerRow < 1) buttonsPerRow = 1;
    int numRows = ceil((float)self.btnDataList.count / buttonsPerRow);
    return verticalMargin + numRows * (buttonHeight + verticalMargin) + verticalMargin;
}

- (void)initUI {
    CGFloat containerHeight = self.frame.size.height;
    UIView *buttonContainer = [[UIView alloc] initWithFrame:CGRectMake(0, 0, self.frame.size.width, containerHeight)];
    buttonContainer.backgroundColor = [UIColor clearColor];
    [self addSubview:buttonContainer];

    NSMutableArray *buttons = [NSMutableArray array];
    for (int i = 0; i < self.btnDataList.count; i++) {
        NSDictionary *btnInfo = self.btnDataList[i];
        UIButton *button = [UIButton buttonWithType:UIButtonTypeSystem];
        [button setTitle:btnInfo[@"title"] forState:UIControlStateNormal];
        button.tag = i;
        [button addTarget:self action:@selector(handleButtonClick:) forControlEvents:UIControlEventTouchUpInside];

        // 统一字体和多行支持
        button.titleLabel.font = [UIFont systemFontOfSize:13.0 weight:UIFontWeightMedium];
        button.titleLabel.numberOfLines = 2;
        button.titleLabel.textAlignment = NSTextAlignmentCenter;
        button.titleLabel.adjustsFontSizeToFitWidth = YES;
        button.titleLabel.minimumScaleFactor = 0.8;

        // 现代化圆角 + 边框 + 阴影
        button.backgroundColor = [UIColor whiteColor];
        button.layer.cornerRadius = 8.0;
        button.layer.borderWidth = 1.0;
        button.layer.borderColor = [UIColor colorWithRed:0.88 green:0.88 blue:0.88 alpha:1.0].CGColor;
        button.layer.shadowColor = [UIColor blackColor].CGColor;
        button.layer.shadowOffset = CGSizeMake(0, 1);
        button.layer.shadowOpacity = 0.06;
        button.layer.shadowRadius = 3;
        button.clipsToBounds = NO;

        [button setTitleColor:[UIColor colorWithRed:0.2 green:0.2 blue:0.25 alpha:1.0] forState:UIControlStateNormal];
        [buttons addObject:button];
        [buttonContainer addSubview:button];
        [self.btnViewList addObject:button];
    }
    [self layoutButtonsInContainer:buttonContainer withButtons:buttons];
}

- (void)layoutButtonsInContainer:(UIView *)container withButtons:(NSArray *)buttons {
    if (buttons.count == 0) return;
    CGFloat buttonWidth = 100.0;
    CGFloat buttonHeight = 32.0;
    CGFloat horizontalMargin = 10.0;
    CGFloat verticalMargin = 8.0;
    CGFloat containerWidth = container.frame.size.width;
    int buttonsPerRow = floor((containerWidth + horizontalMargin) / (buttonWidth + horizontalMargin));
    if (buttonsPerRow < 1) buttonsPerRow = 1;
    int numRows = ceil((float)buttons.count / buttonsPerRow);
    CGFloat requiredHeight = verticalMargin + numRows * (buttonHeight + verticalMargin);
    CGRect containerFrame = container.frame;
    containerFrame.size.height = requiredHeight;
    container.frame = containerFrame;
    CGRect selfFrame = self.frame;
    selfFrame.size.height = container.frame.origin.y + requiredHeight;
    self.frame = selfFrame;
    CGFloat availableWidth = containerWidth - (buttonsPerRow * buttonWidth);
    CGFloat adjustedHorizontalMargin = availableWidth / (buttonsPerRow + 1);
    for (int i = 0; i < buttons.count; i++) {
        UIButton *button = buttons[i];
        int row = i / buttonsPerRow;
        int col = i % buttonsPerRow;
        CGFloat x = adjustedHorizontalMargin + col * (buttonWidth + adjustedHorizontalMargin);
        CGFloat y = verticalMargin + row * (buttonHeight + verticalMargin);
        button.frame = CGRectMake(x, y, buttonWidth, buttonHeight);
    }
}

@end
```

## 3. 创建 AMapLinkDemoViewController

### 头文件（AMapLinkDemoViewController.h）

```objc
#import <UIKit/UIKit.h>

NS_ASSUME_NONNULL_BEGIN

@interface AMapLinkDemoViewController : UIViewController

- (BOOL)handleUrl:(NSURL *)url;

@end

NS_ASSUME_NONNULL_END
```

### 实现文件（AMapLinkDemoViewController.m）

```objc
#import "AMapLinkDemoViewController.h"
#import "AMapLinkDemoNavBarView.h"
#import "AMapLinkDemoEventActionView.h"
#import <MALLMKit/AMapLinkManager.h>
#import <MALLMKit/AMapAuthorizationManager.h>
#import <MALLMKit/AMapLinkConnectConfig.h>
#import "AMapLinkClientObserverManager.h"

#define kAMapAIPCAuthStatus @"kAMapAIPCAuthStatus"

@interface AMapLinkDemoViewController () <AMapLinkDemoEventActionViewDelegate>

@property (nonatomic, assign) BOOL isAuthored;
@property (nonatomic, strong) UITextView *receivedTextView;
@property (nonatomic, strong) AMapLinkDemoNavBarView *navBarView;
@property (nonatomic, strong) AMapLinkDemoEventActionView *eventActionView;
@property (nonatomic, strong) AMapLinkConnectConfig *connectConfig;

@end

@implementation AMapLinkDemoViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [self.view setBackgroundColor:[UIColor whiteColor]];
    self.isAuthored = [[NSUserDefaults standardUserDefaults] boolForKey:kAMapAIPCAuthStatus];
    [self initUI];
    [self tryLink];

    __weak typeof(self) weakSelf = self;
    [[AMapLinkClientObserverManager sharedInstance] addObserver:^(NSString * _Nonnull msg) {
        [weakSelf appendMessage:msg];
        [weakSelf updateInfo];
    }];
}

#pragma mark - Link Management

- (void)tryLink {
    if (self.isAuthored) {
        [self createConnect];
    }
}

- (void)openAmap {
    __weak typeof(self) weakSelf = self;
    [[AMapAuthorizationManager sharedInstance] startAuthenticationWithCallback:^(BOOL success, NSError * _Nonnull error) {
        [weakSelf appendMessage:[NSString stringWithFormat:@"%d  %@", success, error]];
        [weakSelf updateInfo];
    }];
}

- (BOOL)handleUrl:(NSURL *)url {
    BOOL authResult = [[AMapAuthorizationManager sharedInstance] handleURL:url];
    self.isAuthored = authResult;
    if (authResult) {
        [[NSUserDefaults standardUserDefaults] setBool:authResult forKey:kAMapAIPCAuthStatus];
        [self createConnect];
    }
    return YES;
}

- (void)createConnect {
    if (!self.isAuthored) {
        return;
    }
    if ([[AMapLinkManager sharedInstance] isConnected]) {
        return;
    }
    AMapLinkConnectConfig *config = [AMapLinkConnectConfig new];
    config.autoReconnect = YES;
    config.maxReconnectAttempts = 50;
    config.reconnectDelay = 2;
    self.connectConfig = config;
    [[AMapLinkManager sharedInstance] initWithConnectConfig:config];
    [[AMapLinkManager sharedInstance] connect];
}

- (void)disconnect {
    [[AMapLinkManager sharedInstance] disconnect];
}

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
        [self appendMessage:[NSString stringWithFormat:@"writeData: %@", jsonString]];
        [[AMapLinkManager sharedInstance] sendDataToClient:jsonString];
    }
}

#pragma mark - AMapLinkDemoEventActionViewDelegate

- (void)sendData {
    [self sendData:@{ @"text": @"你好呀" }];
}

- (void)startNavi {
    [self sendData:@{ @"cmd": @(5), @"requestId": @2222225 }];
}

- (void)changeRideBroadcast {
    NSArray *rideValues = @[@"0", @"1"];
    NSUInteger randomIndex = arc4random_uniform((uint32_t)rideValues.count);
    [self sendData:@{
        @"cmd": @(6),
        @"data": @{ @"value": rideValues[randomIndex] },
        @"requestId": @2222226
    }];
}

- (void)changeCarBroadcast {
    NSArray *carValues = @[@(0), @(1), @(2), @(6), @(7)];
    NSUInteger randomIndex = arc4random_uniform((uint32_t)carValues.count);
    [self sendData:@{
        @"cmd": @(6),
        @"data": @{ @"value": carValues[randomIndex] },
        @"requestId": @2222227
    }];
}

- (void)changeDestination {
    [self sendData:@{
        @"cmd": @(4),
        @"data": @{
            @"lon": @116.397455, @"lat": @39.909187,
            @"name": @"天安门", @"poiid": @"B000A60DA1",
            @"entranceList": @[ @{ @"lon": @116.397604, @"lat": @39.907697 } ]
        },
        @"requestId": @2222224
    }];
}

- (void)addViaPoint {
    [self sendData:@{
        @"cmd": @(3),
        @"data": @{
            @"lon": @116.397455, @"lat": @39.909187,
            @"name": @"天安门", @"poiid": @"B000A60DA1",
            @"entranceList": @[ @{ @"lon": @116.397604, @"lat": @39.907697 } ]
        },
        @"requestId": @2222223
    }];
}

- (void)clearLog {
    self.receivedTextView.text = @"日志已清除";
}

- (void)copyLog {
    UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"复制日志"
                                                                             message:@"确认要复制日志内容到剪贴板吗？"
                                                                      preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *cancelAction = [UIAlertAction actionWithTitle:@"取消"
                                                           style:UIAlertActionStyleCancel
                                                         handler:nil];
    UIAlertAction *confirmAction = [UIAlertAction actionWithTitle:@"确认"
                                                            style:UIAlertActionStyleDefault
                                                          handler:^(UIAlertAction * _Nonnull action) {
        [UIPasteboard generalPasteboard].string = self.receivedTextView.text;
        [self appendMessage:@"日志内容已复制到剪贴板"];
    }];
    [alertController addAction:cancelAction];
    [alertController addAction:confirmAction];
    [self presentViewController:alertController animated:YES completion:nil];
}

#pragma mark - UI

- (void)appendMessage:(id)message {
    if ([message isKindOfClass:[NSObject class]]) {
        dispatch_async(dispatch_get_main_queue(), ^{
            self.receivedTextView.text = [NSString stringWithFormat:@"%@\n----------------------------\n%@",
                                          self.receivedTextView.text, message];
        });
    }
}

- (void)updateInfo {
    dispatch_async(dispatch_get_main_queue(), ^{
        BOOL isConnected = [[AMapLinkManager sharedInstance] isConnected];
        BOOL isAuthed = self.isAuthored || [[NSUserDefaults standardUserDefaults] boolForKey:kAMapAIPCAuthStatus];
        [self.eventActionView updateInfo:@{
            @"isConnected": @(isConnected),
            @"isAuthored": @(isAuthed)
        }];
    });
}

- (void)initUI {
    NSInteger screenWidth = self.view.bounds.size.width;
    NSInteger screenHeight = self.view.bounds.size.height;

    // 页面背景色
    self.view.backgroundColor = [UIColor colorWithRed:0.96 green:0.96 blue:0.97 alpha:1.0];

    // 1. 导航栏
    CGFloat statusBarHeight = 20;
    if (@available(iOS 11.0, *)) {
        UIWindow *window = UIApplication.sharedApplication.windows.firstObject;
        statusBarHeight = window.safeAreaInsets.top;
    }
    CGFloat navBarHeight = statusBarHeight + 44;
    AMapLinkDemoNavBarView *navBarView = [[AMapLinkDemoNavBarView alloc] initWithFrame:CGRectMake(0, 0, screenWidth, navBarHeight)];
    [navBarView setTitle:@"AMap IPC Link Demo"];
    __weak typeof(self) weakSelf = self;
    navBarView.onBackTapped = ^{
        [weakSelf.navigationController popViewControllerAnimated:YES];
    };
    [self.view addSubview:navBarView];
    self.navBarView = navBarView;

    // 2. 操作按钮面板（带卡片容器）
    CGFloat panelTop = navBarView.bounds.size.height + 12;
    UIView *panelCard = [[UIView alloc] init];
    panelCard.backgroundColor = [UIColor whiteColor];
    panelCard.layer.cornerRadius = 12;
    panelCard.layer.shadowColor = [UIColor blackColor].CGColor;
    panelCard.layer.shadowOffset = CGSizeMake(0, 2);
    panelCard.layer.shadowOpacity = 0.06;
    panelCard.layer.shadowRadius = 8;

    AMapLinkDemoEventActionView *eventActionView = [[AMapLinkDemoEventActionView alloc] initWithOriginX:0
                                                                                        originY:0
                                                                                          width:screenWidth - 32];
    eventActionView.delegate = self;

    panelCard.frame = CGRectMake(16, panelTop, screenWidth - 32, eventActionView.bounds.size.height + 16);
    eventActionView.frame = CGRectMake(0, 8, screenWidth - 32, eventActionView.bounds.size.height);
    [panelCard addSubview:eventActionView];
    [self.view addSubview:panelCard];
    self.eventActionView = eventActionView;

    // 3. 日志标题
    CGFloat logSectionTop = CGRectGetMaxY(panelCard.frame) + 16;
    UILabel *logTitleLabel = [[UILabel alloc] initWithFrame:CGRectMake(24, logSectionTop, screenWidth - 48, 22)];
    logTitleLabel.text = @"📋 通信日志";
    logTitleLabel.font = [UIFont systemFontOfSize:15 weight:UIFontWeightSemibold];
    logTitleLabel.textColor = [UIColor colorWithRed:0.3 green:0.3 blue:0.35 alpha:1.0];
    [self.view addSubview:logTitleLabel];

    // 4. 日志回显区域（卡片样式）
    CGFloat logTop = logSectionTop + 30;
    CGFloat bottomSafeArea = 34;
    if (@available(iOS 11.0, *)) {
        UIWindow *window = UIApplication.sharedApplication.windows.firstObject;
        bottomSafeArea = window.safeAreaInsets.bottom;
    }
    UITextView *receivedTextView = [[UITextView alloc] initWithFrame:CGRectMake(16, logTop,
                                                                                screenWidth - 32,
                                                                                screenHeight - logTop - bottomSafeArea - 16)];
    receivedTextView.text = @"等待通信日志...";
    receivedTextView.textColor = [UIColor colorWithRed:0.35 green:0.35 blue:0.4 alpha:1.0];
    receivedTextView.font = [UIFont fontWithName:@"Menlo" size:12.5];
    receivedTextView.backgroundColor = [UIColor whiteColor];
    receivedTextView.textAlignment = NSTextAlignmentLeft;
    receivedTextView.editable = NO;
    receivedTextView.scrollEnabled = YES;
    receivedTextView.textContainerInset = UIEdgeInsetsMake(12, 10, 12, 10);
    receivedTextView.layer.cornerRadius = 12;
    receivedTextView.layer.shadowColor = [UIColor blackColor].CGColor;
    receivedTextView.layer.shadowOffset = CGSizeMake(0, 2);
    receivedTextView.layer.shadowOpacity = 0.06;
    receivedTextView.layer.shadowRadius = 8;
    receivedTextView.clipsToBounds = NO;
    [self.view addSubview:receivedTextView];
    self.receivedTextView = receivedTextView;
}

@end
```

## 4. Info.plist 配置

### 配置 URL Scheme

在 Info.plist 中添加 URL Types，用于接收高德 APP 的授权回调：

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>你的URLScheme</string>
        </array>
    </dict>
</array>
```

### 配置 LSApplicationQueriesSchemes

添加高德地图 APP 的 Scheme，允许跳转：

```xml
<key>LSApplicationQueriesSchemes</key>
<array>
    <string>iosamap</string>
</array>
```

## 5. 处理授权回调 URL

在 AppDelegate 或 SceneDelegate 中将 URL 传递给 `AMapLinkDemoViewController` 处理：

### AppDelegate 方式

```objc
- (BOOL)application:(UIApplication *)app openURL:(NSURL *)url options:(NSDictionary *)options {
    [self.linkDemoViewController handleUrl:url];
    return YES;
}
```

### SceneDelegate 方式（iOS 13+）

```objc
- (void)scene:(UIScene *)scene openURLContexts:(NSSet<UIOpenURLContext *> *)URLContexts {
    UIOpenURLContext *context = URLContexts.allObjects.firstObject;
    if (context) {
        [self.linkDemoViewController handleUrl:context.URL];
    }
}
```

## 下一步

- [认证管理](authorization.md) — 授权流程详细说明
- [连接管理](connection.md) — 连接配置与状态管理
- [数据传输与命令](data-transfer.md) — 导航命令与数据收发

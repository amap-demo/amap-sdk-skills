# iOS 平台接入指南

> 在 iOS 项目中集成 WatchSDK 的完整指南

## 概述

WatchSDK 是一个面向 RTOS 的 C 语言 SDK，在 iOS 中需要通过适配器模式桥接 iOS 的 Foundation 框架。

## 项目结构

```
YourProject/
├── libWatchSDK.a              # 静态库
├── include/                   # SDK 头文件
│   ├── awk.h
│   ├── awk_adapter.h
│   ├── awk_defines.h
│   ├── map/
│   │   ├── awk_map.h
│   │   └── awk_map_defines.h
│   └── navi/
│       ├── awk_navi.h
│       └── awk_navi_defines.h
└── RTOSPlayground/
    ├── WatchSDKManager.h      # SDK 管理器
    ├── WatchSDKManager.m
    ├── WatchSDKAdapters.h     # 适配器实现
    └── WatchSDKAdapters.m
```

## 接入步骤

### 1. 添加静态库和头文件

**方法一：直接拖拽**
- 将 `libWatchSDK.a` 拖入 Xcode 项目
- 将 `include/` 文件夹拖入 Xcode 项目
- 勾选 `Copy items if needed`
- 确保 `Add to targets` 选中你的 App target

**方法二：配置 Build Settings**
1. 选择项目 target
2. `Build Settings` → `Library Search Paths`
   - 添加: `$(PROJECT_DIR)/Vendor/WatchSDK`
3. `Build Settings` → `Header Search Paths`
   - 添加: `$(PROJECT_DIR)/Vendor/WatchSDK/include`

### 2. 创建适配器

#### WatchSDKAdapters.h

```objc
#import <Foundation/Foundation.h>
#import "awk_adapter.h"

@interface WatchSDKAdapters : NSObject

+ (awk_memory_adapter_t)memoryAdapter;
+ (awk_file_adapter_t)fileAdapter;
+ (awk_system_adapter_t)systemAdapter;
+ (awk_network_adapter_t)networkAdapter;
+ (awk_render_adapter_t)renderAdapter;
+ (awk_thread_adapter_t)threadAdapter;

@end
```

#### WatchSDKAdapters.m

**内存适配器实现：**

```objc
+ (awk_memory_adapter_t)memoryAdapter {
    static awk_memory_adapter_t adapter = {
        .mem_malloc = aw_mem_malloc,
        .mem_free = aw_mem_free,
        .mem_calloc = aw_mem_calloc,
        .mem_realloc = aw_mem_realloc
    };
    return adapter;
}

static void* aw_mem_malloc(size_t size) {
    return malloc(size);
}

static void aw_mem_free(void* ptr) {
    if (ptr) free(ptr);
}

static void* aw_mem_calloc(size_t count, size_t size) {
    return calloc(count, size);
}

static void* aw_mem_realloc(void* ptr, size_t size) {
    return realloc(ptr, size);
}
```

**系统适配器实现：**

```objc
+ (awk_system_adapter_t)systemAdapter {
    static awk_system_adapter_t adapter = {
        .get_system_time = aw_get_system_time,
        .log_printf = aw_log_printf
    };
    return adapter;
}

static uint64_t aw_get_system_time(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (uint64_t)tv.tv_sec * 1000 + tv.tv_usec / 1000;
}

static int aw_log_printf(const char *format, ...) {
    va_list args;
    va_start(args, format);
    NSString *message = [[NSString alloc] initWithFormat:[NSString stringWithUTF8String:format] 
                                              arguments:args];
    va_end(args);
    NSLog(@"[WatchSDK] %@", message);
    return 0;
}
```

**线程适配器实现：**

```objc
+ (awk_thread_adapter_t)threadAdapter {
    static awk_thread_adapter_t adapter = {
        .get_thread_id = aw_get_thread_id
    };
    return adapter;
}

static uint64_t aw_get_thread_id(void) {
    pthread_t pid = pthread_self();
    return (uint64_t)pid;
}
```

### 3. 创建 SDK 管理器

#### WatchSDKManager.h

```objc
#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

typedef void (^WatchSDKActivateSuccessCallback)(void);
typedef void (^WatchSDKActivateFailCallback)(int32_t errorCode, NSString *errorMessage);

@interface WatchSDKManager : NSObject

+ (instancetype)sharedManager;

/**
 * 初始化 SDK
 * @param deviceId 设备 ID
 * @param amapKey 高德开放平台 key
 * @param rootDir SDK 数据根目录
 * @return 0=成功，负数=错误码
 */
- (int32_t)initializeWithDeviceId:(NSString *)deviceId
                          amapKey:(NSString *)amapKey
                         rootDir:(NSString *)rootDir;

/**
 * 激活设备（首次使用需联网激活）
 */
- (void)activateDeviceWithSuccess:(WatchSDKActivateSuccessCallback)successCallback
                          failure:(WatchSDKActivateFailCallback)failCallback;

/**
 * 创建地图视图
 */
- (int32_t)createMapViewWithWidth:(int32_t)width height:(int32_t)height;

/**
 * 销毁地图视图
 */
- (void)destroyMapView:(int32_t)mapId;

/**
 * 执行地图渲染（需要在主循环中定时调用）
 */
- (void)doRender;

/**
 * 反初始化 SDK
 */
- (void)uninitialize;

@end

NS_ASSUME_NONNULL_END
```

#### WatchSDKManager.m

```objc
#import "WatchSDKManager.h"
#import "WatchSDKAdapters.h"
#import "awk.h"

// 全局回调存储
static WatchSDKActivateSuccessCallback g_successCallback = nil;
static WatchSDKActivateFailCallback g_failCallback = nil;

static void on_activate_success(const char* license_id) {
    if (g_successCallback) {
        dispatch_async(dispatch_get_main_queue(), ^{
            g_successCallback();
            g_successCallback = nil;
            g_failCallback = nil;
        });
    }
}

static void on_activate_fail(int32_t error_code, const char* error_message) {
    if (g_failCallback) {
        NSString *msg = error_message ? [NSString stringWithUTF8String:error_message] : @"Unknown error";
        dispatch_async(dispatch_get_main_queue(), ^{
            g_failCallback(error_code, msg);
            g_successCallback = nil;
            g_failCallback = nil;
        });
    }
}

@implementation WatchSDKManager

+ (instancetype)sharedManager {
    static WatchSDKManager *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[WatchSDKManager alloc] init];
    });
    return instance;
}

- (int32_t)initializeWithDeviceId:(NSString *)deviceId
                          amapKey:(NSString *)amapKey
                         rootDir:(NSString *)rootDir {
    if (!deviceId || !amapKey || !rootDir) {
        return -2;
    }
    
    // 创建根目录
    NSFileManager *fileManager = [NSFileManager defaultManager];
    if (![fileManager fileExistsAtPath:rootDir]) {
        NSError *error = nil;
        [fileManager createDirectoryAtPath:rootDir
               withIntermediateDirectories:YES
                                attributes:nil
                                     error:&error];
        if (error) {
            return -3;
        }
    }
    
    // 构建初始化上下文
    awk_context_t context;
    memset(&context, 0, sizeof(awk_context_t));
    
    context.device_id = [deviceId UTF8String];
    context.key = [amapKey UTF8String];
    context.root_dir = [rootDir UTF8String];
    context.tile_mem_cache_max_size = 6;   // KB
    context.tile_disk_cache_max_size = 200; // MB
    
    // 设置适配器
    context.memory_adapter = [WatchSDKAdapters memoryAdapter];
    context.file_adapter = [WatchSDKAdapters fileAdapter];
    context.system_adapter = [WatchSDKAdapters systemAdapter];
    context.network_adapter = [WatchSDKAdapters networkAdapter];
    context.render_adapter = [WatchSDKAdapters renderAdapter];
    context.thread_adapter.get_thread_id = aw_get_thread_id;
    
    // 调用 SDK 初始化
    int32_t result = awk_init(&context);
    
    return result;
}

- (void)activateDeviceWithSuccess:(WatchSDKActivateSuccessCallback)successCallback
                          failure:(WatchSDKActivateFailCallback)failCallback {
    g_successCallback = [successCallback copy];
    g_failCallback = [failCallback copy];
    
    awk_device_activate_param_t param = {
        .area = "mainland",
        .country = "cn",
        .type = 0,
        .data_type = "raster"
    };
    
    awk_device_active_callback callback = {
        .awk_device_active_on_success = on_activate_success,
        .awk_device_active_on_fail = on_activate_fail
    };
    
    awk_activate_device(&param, callback);
}

- (int32_t)createMapViewWithWidth:(int32_t)width height:(int32_t)height {
    awk_map_view_param_t param = {
        .port = {width, height}
    };
    return awk_map_create_view(param);
}

- (void)destroyMapView:(int32_t)mapId {
    awk_map_destroy_view(mapId);
}

- (void)doRender {
    awk_map_do_render();
}

- (void)uninitialize {
    awk_uninit();
}

@end
```

### 4. 在 ViewController 中使用

```objc
#import "MapViewController.h"
#import "WatchSDKManager.h"

@interface MapViewController ()
@property (nonatomic, strong) CADisplayLink *renderTimer;
@property (nonatomic, assign) int32_t mapId;
@end

@implementation MapViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    // 1. 初始化 SDK
    NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
    NSString *rootDir = [paths.firstObject stringByAppendingPathComponent:@"WatchSDKData"];
    
    NSString *deviceId = [[UIDevice currentDevice] identifierForVendor].UUIDString;
    NSString *amapKey = @"your_amap_key";
    
    WatchSDKManager *manager = [WatchSDKManager sharedManager];
    int32_t result = [manager initializeWithDeviceId:deviceId amapKey:amapKey rootDir:rootDir];
    
    if (result == 0) {
        NSLog(@"SDK 初始化成功");
        [self activateDevice];
    }
}

- (void)activateDevice {
    [[WatchSDKManager sharedManager] activateDeviceWithSuccess:^{
        NSLog(@"设备激活成功");
        [self createMap];
    } failure:^(int32_t errorCode, NSString *errorMessage) {
        NSLog(@"激活失败: %@", errorMessage);
    }];
}

- (void)createMap {
    CGSize screenSize = [UIScreen mainScreen].bounds.size;
    CGFloat scale = [UIScreen mainScreen].scale;
    
    self.mapId = [[WatchSDKManager sharedManager] createMapViewWithWidth:(int32_t)(screenSize.width * scale)
                                                                   height:(int32_t)(screenSize.height * scale)];
    
    if (self.mapId > 0) {
        [self startRenderTimer];
    }
}

- (void)startRenderTimer {
    self.renderTimer = [CADisplayLink displayLinkWithTarget:self 
                                                  selector:@selector(render)];
    [self.renderTimer addToRunLoop:[NSRunLoop mainRunLoop] 
                          forMode:NSRunLoopCommonModes];
}

- (void)render {
    [[WatchSDKManager sharedManager] doRender];
}

- (void)dealloc {
    if (self.renderTimer) {
        [self.renderTimer invalidate];
    }
    if (self.mapId > 0) {
        [[WatchSDKManager sharedManager] destroyMapView:self.mapId];
    }
}

@end
```

## 关键注意事项

### 1. 线程模型

⚠️ SDK 为单线程模型，所有 SDK 方法必须在主线程调用：

```objc
// ✅ 正确：在主线程调用
dispatch_async(dispatch_get_main_queue(), ^{
    awk_map_do_render();
});

// ❌ 错误：在后台线程调用
dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
    awk_map_do_render(); // 可能导致异常
});
```

### 2. 回调处理

SDK 的回调函数需要在主线程执行，使用 GCD 切换：

```objc
static void on_activate_success(const char* license_id) {
    dispatch_async(dispatch_get_main_queue(), ^{
        // 处理成功回调
    });
}
```

### 3. 渲染循环

使用 CADisplayLink 在主线程定时调用渲染：

```objc
self.renderTimer = [CADisplayLink displayLinkWithTarget:self selector:@selector(render)];
[self.renderTimer addToRunLoop:[NSRunLoop mainRunLoop] forMode:NSRunLoopCommonModes];
```

### 4. 内存管理

适配器的内存操作直接使用系统函数：

```objc
static void* aw_mem_malloc(size_t size) {
    return malloc(size);
}

static void aw_mem_free(void* ptr) {
    if (ptr) free(ptr);
}
```

## 常见问题

### Q: 编译错误 "Undefined symbols for architecture arm64"

**原因**：静态库未正确链接

**解决**：
1. 检查 `Library Search Paths` 是否正确
2. 确认静态库架构与项目架构一致
3. 使用 `lipo -info libWatchSDK.a` 查看静态库支持的架构

### Q: 头文件找不到

**原因**：`Header Search Paths` 配置错误

**解决**：
```
Build Settings → Header Search Paths
添加: $(PROJECT_DIR)/Vendor/WatchSDK/include
勾选: Recursive
```

### Q: 地图不显示

**排查步骤**：
1. 确认设备已激活
2. 检查渲染定时器是否启动
3. 确认 `render_adapter` 实现正确
4. 检查地图尺寸是否有效

## 下一步

- [适配器实现](adapters.md) - 查看完整适配器实现
- [快速开始](quick-start.md) - 了解基础接入流程
- [地图操作](map-operations.md) - 学习地图控制 API

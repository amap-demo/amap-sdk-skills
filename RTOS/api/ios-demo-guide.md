# iOS Demo 功能实现指南

> 基于 WatchSDKDemo 工程的完整功能实现参考

## 概述

本文档基于 WatchSDKDemo 工程中的实际实现，详细说明如何使用 WatchSDK 实现常见的地图功能。

## 核心架构

### 架构图

```
AMapMainView (主界面)
    ↓ NavigationLink
AMapMyLocationView (我的地图)
    ↓
GDMapView (地图视图)
    ↓
GDMapViewModel (地图业务逻辑)
    ↓
GDWatchEngine (SDK 引擎封装)
    ↓
WatchSDK (C SDK)
```

### 关键类说明

| 类名 | 职责 |
|------|------|
| `GDWatchEngine` | SDK 引擎单例封装，提供所有 SDK 功能的统一入口 |
| `GDMapView` | SwiftUI 地图视图组件，处理手势和 UI 交互 |
| `GDMapViewModel` | 地图业务逻辑，管理地图状态和渲染回调 |
| `AMapMyLocationView` | 我的地图页面，整合地图和导航组件 |
| `AMapMyLocationViewModel` | 定位业务逻辑，管理当前位置 |

## "我的地图"功能实现

### 1. 主入口 - AMapMainView

用户点击"我的地图"按钮后，通过 `NavigationLink` 导航到地图页面：

```swift
NavigationLink {
    GDDeferView {
        AMapMyLocationView()
    }
} label: {
    HStack {
        Image("ic-location-o")
            .resizable()
            .frame(width: GDSize.match(21), height: GDSize.match(21))
            .foregroundColor(.blue)
        Text("我的地图")
            .font(Font.system(size: GDSize.match(18)))
    }
    .frame(height: GDSize.match(48))
}
.buttonStyle(.plain)
```

**关键点：**
- 使用 `GDDeferView` 延迟初始化，确保视图按需加载
- 按钮使用 `plain` 样式，保持界面简洁

### 2. 地图页面 - AMapMyLocationView

```swift
struct AMapMyLocationView: View {
    var viewModel = AMapMyLocationViewModel()

    var body: some View {
        ZStack() {
            // 地图视图
            GDMapView(MapScene(mode: .location(mapCenter: viewModel.myLocation.coordinate),
                             tileStyle: GDTileStyleGridAndPoi))
                .baseHandle { mapViewHandler in
                    viewModel.mapHandler = mapViewHandler
                }
            
            // UI 层
            VStack(alignment: .leading) {
                // 顶部返回按钮
                HStack {
                    Image("ic-list-o 2")
                        .renderingMode(.template)
                        .foregroundColor(.white)
                    Spacer()
                }
                .decorateHandleBack {
                    viewModel.mapHandler?.destroy()
                }
                
                // 导航组件
                AMapNaviView()
                Spacer()
                
                // 底部定位按钮
                HStack {
                    Button {
                        viewModel.mapCenterMoveToMyLocation()
                    } label: {
                        Image("ic-location-o")
                            .renderingMode(.template)
                            .foregroundColor(.white)
                            .frame(width: GDSize.match(40), height: GDSize.match(40))
                            .background(Color(uiColor: UIColor.ltmColor(withHexString: "#222223")))
                            .cornerRadius(GDSize.match(12))
                    }
                    .buttonStyle(.plain)
                    Spacer()
                }
            }
        }
        .onDisappear {
            viewModel.mapHandler?.destroy()
        }
    }
}
```

**关键点：**
- 使用 `ZStack` 叠加地图和 UI 层
- 通过 `baseHandle` 回调获取地图操作句柄
- 在 `onDisappear` 时销毁地图资源

### 3. 地图视图 - GDMapView

#### MapScene 配置

```swift
struct MapScene {
    var mode: MapMode
    var size = WKInterfaceDevice.current().screenBounds.size
    var isUserInteractionEnabled = true
    var zoom = 18.0
    var eventDelegate: GDSceneEventProtocol? = nil
    var tileStyle: GDTileStyle = GDTileStyleGridAndPoi
    
    var sceneType: GDSceneType {
        switch mode {
        case .image(_):
            return GDSceneTypePOI
        case .location(_):
            return GDSceneTypeMainMap
        }
    }
    
    var pageType: GDPageType {
        switch mode {
        case .image(_):
            return GDPageTypeDetail
        case .location(_):
            return GDPageTypeMainMap
        }
    }
    
    func configMap(_ engine: GDWatchEngine, mapid: Int) {
        engine.setViewport(size, mapId: mapid)
        engine.setZoom(zoom, mapId: mapid)
        switch mode {
        case .image(let mapCenter), .location(let mapCenter):
            if CLLocationCoordinate2DIsValid(mapCenter) {
                engine.setMapCenterWithLocation(mapCenter, mapId: mapid)
            }
        }
    }
}
```

#### 地图视图实现

```swift
struct GDMapView: View {
    private var mapScene: MapScene
    @ObservedObject private var mapData: GDMapViewModel
    
    init(_ initScene: MapScene, handler: GDMapViewProtocol? = nil) {
        mapScene = initScene
        mapData = GDMapViewModel(mapScene)
    }
    
    var body: some View {
        ZStack() {
            if mapData.mapImage != nil {
                Image(uiImage: mapData.mapImage!)
                    .resizable()
                    .gesture(drag)
                    .onTapGesture(count: 2) {
                        mapData.crownDidRotate(crownThresholdValue)
                    }
                    .onTapGesture { location in
                        mapData.onSingleTap(location)
                    }
            } else {
                ProgressView()
            }
            
            // 控制按钮
            VStack(spacing: 5) {
                Spacer()
                // 缩放按钮
                VStack(spacing: 0) {
                    Image(systemName: "plus")
                        .onTapGesture { mapData.zoomChange(1.0) }
                    Spacer().frame(height: 0.5)
                    Image(systemName: "minus")
                        .onTapGesture { mapData.zoomChange(-1.0) }
                }
                .cornerRadius(28)
                Spacer()
            }
        }
        .focusable(mapScene.isUserInteractionEnabled)
        .digitalCrownRotation($crownValue, from: 0.1, through: 10.0, sensitivity: .low)
        .onAppear { mapData.willActivate() }
        .onDisappear { mapData.didDeactivate() }
    }
    
    var drag: some Gesture {
        DragGesture(minimumDistance: 1, coordinateSpace: .local)
            .onChanged { value in
                if !isGesturing {
                    isGesturing = true
                    mapData.onPanBegin(value.startLocation)
                }
                mapData.onPanMoved(start: value.startLocation, 
                                  location: value.location, 
                                  velocity: CGPoint(x: 0, y: 0))
            }
            .onEnded { value in
                isGesturing = false
                mapData.onPanEnd(value.location)
            }
    }
}
```

**关键点：**
- 使用 `@ObservedObject` 监听地图状态变化
- 实现 `DragGesture` 处理地图拖拽
- 使用 `digitalCrownRotation` 支持表冠缩放
- 通过 `Image(uiImage:)` 显示 SDK 渲染的地图图片

### 4. 地图业务逻辑 - GDMapViewModel

```swift
class GDMapViewModel: NSObject, ObservableObject {
    @Published var show = true
    var scene: MapScene
    var mapid = -1
    @Published var mapImage: UIImage?
    
    let engine = GDWatchEngine.sharedInstance()
    
    init(_ inputScene: MapScene) {
        engine.initEngine()
        scene = inputScene
        super.init()
        
        let param = GDSceneParam()
        param.sceneType = scene.sceneType
        param.pageType = scene.pageType
        param.size = WKInterfaceDevice.current().screenBounds.size
        param.tileStyle = scene.tileStyle
        
        mapid = Int(engine.createMapView(param, renderDelegate: self))
        scene.configMap(engine, mapid: mapid)
        engine.initNavi()
    }
    
    deinit {
        print("GDMapViewModel deinit")
    }
    
    func willActivate() {
        self.showMap()
    }
    
    func didDeactivate() {
        self.hideMap()
    }
    
    // 手势处理
    func onPanBegin(_ start: CGPoint) {
        engine.onPanBegin(start, mapId: mapid)
    }
    
    func onPanMoved(start: CGPoint, location: CGPoint, velocity: CGPoint) {
        engine.onPanMoved(location, velocity: velocity, mapId: mapid)
    }
    
    func onPanEnd(_ end: CGPoint) {
        engine.onPanEnd(end, mapId: mapid)
    }
    
    func onSingleTap(_ point: CGPoint) {
        engine.onSingleTap(point, mapId: mapid)
    }
    
    func crownDidRotate(_ rotationalDelta: Double) {
        let zoom = engine.zoom(forMapId: mapid)
        if rotationalDelta > 0 && zoom < 20 {
            engine.setZoom(zoom + 1.0, mapId: mapid)
        } else if rotationalDelta < 0 && zoom > 1 {
            engine.setZoom(zoom - 1.0, mapId: mapid)
        }
    }
    
    func zoomChange(_ value: Double) {
        let zoom = engine.zoom(forMapId: mapid)
        if value > 0 && zoom < 20 {
            engine.setZoom(zoom + value, mapId: mapid)
        }
        if value < 0 && zoom > 0 {
            engine.setZoom(zoom + value, mapId: mapid)
        }
    }
}

extension GDMapViewModel: AMapRenderDelegate {
    func onRenderImage(_ image: UIImage) {
        self.mapImage = image
    }
    
    func onShowMap(_ show: Bool) {
        if show {
            self.showMap()
        } else {
            self.hideMap()
        }
    }
    
    func setNeedsRender() {
        // 触发重新渲染
    }
}

extension GDMapViewModel: GDMapBaseHandlerProtocol {
    func setMapCenter(_ location: CLLocationCoordinate2D) {
        engine.setMapCenterWithLocation(location, mapId: mapid)
    }
    
    func setZoom(_ value: Double) {
        if value > 0 && value < 20 {
            engine.setZoom(value, mapId: mapid)
        }
    }
    
    func destroy() {
        if mapid == -1 {
            return
        }
        engine.destroyMapView(UInt32(mapid))
        mapid = -1
    }
    
    func showMap() {
        show = true
    }
    
    func hideMap() {
        show = false
    }
}
```

**关键点：**
- 实现 `AMapRenderDelegate` 接收 SDK 渲染回调
- 实现 `GDMapBaseHandlerProtocol` 提供地图操作接口
- 使用 `@Published` 属性驱动 SwiftUI 视图更新
- 在 `deinit` 时销毁地图资源

### 5. 定位逻辑 - AMapMyLocationViewModel

```swift
class AMapMyLocationViewModel: NSObject, ObservableObject {
    var myLocation: CLLocation = CLLocation(latitude: 40.0039877, longitude: 116.488981)
    private var hasShowRealLocation = false
    var mapHandler: GDMapBaseHandlerProtocol?
    
    override init() {
        super.init()
        // 获取真实定位
        if let location = GDLocationManager.sharedInstance().engineLocation {
            myLocation = location
            hasShowRealLocation = true
        } else {
            GDLocationManager.sharedInstance().addObserver(self)
        }
        self.mapCenterMoveToMyLocation()
    }
    
    deinit {
        GDLocationManager.sharedInstance().removeObserver(self)
    }
    
    func mapCenterMoveToMyLocation() {
        mapHandler?.setMapCenter(myLocation.coordinate)
    }
}

extension AMapMyLocationViewModel: GDLocationManagerDelegate {
    func gdLocationManagerlocationDidUpdate(_ location: CLLocation) {
        myLocation = location
        if !hasShowRealLocation {
            hasShowRealLocation = true
            self.mapCenterMoveToMyLocation()
        }
    }
}
```

**关键点：**
- 优先使用真实定位，失败时使用默认坐标
- 实现定位回调，实时更新当前位置
- 首次获取到真实定位时自动移动地图中心

## GDWatchEngine 核心接口

### 初始化与生命周期

```objc
// 单例获取
+ (instancetype)sharedInstance;

// 初始化引擎
- (void)initEngine;

// 反初始化引擎
- (void)uninitEngine;

// 初始化导航
- (void)initNavi;
```

### 地图创建与销毁

```objc
// 创建地图视图
- (uint32_t)createMapView:(GDSceneParam *)sceneConfig 
          renderDelegate:(id<AMapRenderDelegate>)renderDelegate;

// 销毁地图视图
- (void)destroyMapView:(uint32_t)mapId;

// 恢复地图绘制
- (void)onRender_resume:(NSInteger)mapId;

// 暂停地图绘制
- (void)onRender_pause:(NSInteger)mapId;
```

### 地图控制

```objc
// 设置视口大小
- (void)setViewport:(CGSize)size mapId:(NSInteger)mapId;

// 获取缩放级别
- (CGFloat)zoomForMapId:(NSInteger)mapId;

// 设置缩放级别
- (void)setZoom:(CGFloat)zoom mapId:(NSInteger)mapId;

// 设置地图中心点
- (void)setMapCenterWithLocation:(CLLocationCoordinate2D)location 
                           mapId:(NSInteger)mapId;

// 设置显示模式（锁车、全览、普通）
- (void)setShowMode:(awk_navi_show_mode_type)show_mode_type;

// 设置跟随模式（车头向上、北向上）
- (void)setTrackingMode:(awk_navi_tracking_mode_type)tracking_mode_type;

// 设置导航类型（驾车、骑行、步行）
- (void)set_navi_type:(awk_navi_type)navi_type;
```

### 手势处理

```objc
// 拖拽开始
- (void)onPanBegin:(CGPoint)startPoint mapId:(NSInteger)mapId;

// 拖拽移动
- (void)onPanMoved:(CGPoint)toPoint 
          velocity:(CGPoint)velocity 
             mapId:(NSInteger)mapId;

// 拖拽结束
- (void)onPanEnd:(CGPoint)endPoint mapId:(NSInteger)mapId;

// 单击
- (void)onSingleTap:(CGPoint)point mapId:(NSInteger)mapId;
```

### 覆盖物管理

```objc
// 添加基础覆盖物
- (void)addBaseOverlay:(NSInteger)mapId;

// 添加点覆盖物
- (void)addPointOverlay:(NSInteger)mapId;

// 添加线覆盖物
- (void)addLineOverlay:(NSInteger)mapId;

// 添加面覆盖物
- (void)addPolygonOverlay:(NSInteger)mapId;

// 添加轨迹导航覆盖物
- (void)addTrackNaviOverlay:(NSInteger)mapId;
```

### 离线地图

```objc
// 下载离线地图
- (void)downloadMap:(id<AMapDownloadDelegate>)downloadDelegate;
```

## AMapRenderDelegate 渲染回调

```objc
@protocol AMapRenderDelegate <NSObject>

// 渲染完成回调
- (void)onRenderImage:(UIImage *)image;

// 地图显示状态回调
- (void)onShowMap:(BOOL)show;

@end
```

## 导航组件 - AMapNaviView

导航组件展示实时导航信息，包括：
- 剩余距离
- 剩余时间
- 交通光柱
- 转向信息
- 速度信息
- 途经点
- 转向图标

导航数据通过 `GDNaviViewDelegate` 回调更新：

```objc
@protocol GDNaviViewDelegate <NSObject>

- (void)updateRemainDistance:(awk_navi_remain_distance_component)remain_distance;
- (void)updateRemainTime:(awk_navi_remain_time_component)remain_time;
- (void)updateTrafficBar:(awk_navi_traffic_bar_component)traffic_bar;
- (void)updateTurnInfoCard:(awk_navi_info_card_component)turn_info_card;
- (void)updateSpeedInfo:(awk_navi_speed_component)speed_info;
- (void)updateNorthUp:(awk_navi_north_up_component)north_up;
- (void)updateTrafficLightInfo:(awk_navi_traffic_signal_info_component)traffic_light;
- (void)updateRearVehicleInfo:(awk_navi_rear_vehicle_component)rear_vehicle;
- (void)updateLaneInfo:(awk_navi_lane_component)lane_info andImage:(UIImage *)image;
- (void)updateTrafficLightNum:(awk_navi_traffic_num_component)traffic_light_num;

@end
```

## 常见使用场景

### 场景 1：创建基础地图

```swift
// 创建地图场景
let scene = MapScene(
    mode: .location(mapCenter: CLLocationCoordinate2D(latitude: 39.9, longitude: 116.4)),
    tileStyle: GDTileStyleGridAndPoi
)

// 创建地图视图
let mapView = GDMapView(scene)
```

### 场景 2：移动地图中心

```swift
func setMapCenter(_ location: CLLocationCoordinate2D) {
    mapHandler?.setMapCenter(location)
}
```

### 场景 3：缩放地图

```swift
// 放大
mapData.zoomChange(1.0)

// 缩小
mapData.zoomChange(-1.0)

// 设置指定缩放级别
mapData.setZoom(15.0)
```

### 场景 4：切换显示模式

```swift
// 锁车模式
engine.setShowMode(AWK_NAVI_SHOW_MODE_CAR_POSITION_LOCKED)

// 全览模式
engine.setShowMode(AWK_NAVI_SHOW_MODE_OVERVIEW)
```

### 场景 5：切换跟随模式

```swift
// 车头向上
engine.setTrackingMode(AWK_NAVI_TRACKING_MODE_CAR_NORTH)

// 北向上
engine.setTrackingMode(AWK_NAVI_TRACKING_MODE_MAP_NORTH)
```

### 场景 6：切换导航类型

```swift
// 驾车
engine.set_navi_type(AWK_NAVI_TYPE_DRIVE)

// 骑行
engine.set_navi_type(AWK_NAVI_TYPE_RIDE)

// 步行
engine.set_navi_type(AWK_NAVI_TYPE_WALK)
```

## 注意事项

### 1. 线程安全

- 所有 SDK 方法必须在**主线程**调用
- UI 更新必须在主线程执行
- 回调数据可能来自后台线程，需要切换到主线程处理

### 2. 资源管理

- 必须在 `onDisappear` 或 `deinit` 时调用 `destroyMapView`
- 避免重复创建或销毁地图
- 使用 `onRender_pause/onRender_resume` 控制渲染性能

### 3. 内存管理

- GDWatchEngine 使用单例模式，不需要手动释放
- GDMapViewModel 需要在视图销毁时释放
- 注意避免循环引用

### 4. 表冠旋转

- 表冠旋转值是连续的，需要处理边界情况
- 设置合理的缩放阈值，避免过度缩放

### 5. 手势冲突

- 拖拽手势可能与 SwiftUI 原生手势冲突
- 使用 `coordinateSpace: .local` 指定坐标系
- 设置合适的 `minimumDistance` 避免误触

## 相关文档

- [iOS 集成指南](ios-integration.md)
- [地图操作](map-operations.md)
- [导航](navigation.md)
- [适配器](adapters.md)

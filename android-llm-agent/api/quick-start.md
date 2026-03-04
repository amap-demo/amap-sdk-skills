# 快速接入 AMap LLM Agent SDK

完成 SDK 集成的完整步骤。

## 步骤 1：添加依赖

在 `build.gradle` 中添加：

```gradle
dependencies {
    // LLM Agent SDK
    implementation 'com.amap.lbs.client:amap-agent:1.1.41'
    
    // 导航 SDK（必须）
    implementation 'com.amap.api:navi-3dmap:latest.integration'
    
    // 定位 SDK（必须，用于实时位置更新）
    implementation 'com.amap.api:location:latest.integration'
}
```

> ⚠️ **注意**：如果 Agent SDK 或导航 SDK 依赖有问题（如无法下载、版本冲突等），请联系高德相关同学获取依赖包。

## 步骤 2：Application 初始化（可选）

Application 中可以进行全局配置，如 API Key、隐私政策等。如果这些配置已在其他地方完成，Application 可以保持空实现。

```java
public class MyApp extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        // 以下配置根据实际需要选择性添加
        
        // 设置 API Key（如果需要在 Application 中设置）
        // AMapApi.setApiKey(this, "your_amap_api_key");
        
        // 开启定位引擎云控控制能力（可选）
        // AMapNavi.setCustomPosControlEnable(true);
        
        // 设置隐私政策同意状态（必须在某处调用）
        // NaviSetting.updatePrivacyShow(this, true, true);
        // NaviSetting.updatePrivacyAgree(this, true);
    }
}
```

## 步骤 3：布局文件

在布局文件中添加 `AMapNaviView`：

```xml
<com.amap.api.navi.AMapNaviView
    android:id="@+id/navi_view"
    android:layout_width="match_parent"
    android:layout_height="match_parent" />
```

## 步骤 4：Activity 中初始化

```java
// Agent SDK 核心类
import com.amap.llm.agent.api.AMapAgentCallback;
import com.amap.llm.agent.api.AMapAgentQueryParam;
import com.amap.llm.agent.api.AMapAgentQueryResult;
import com.amap.llm.agent.api.AMapApi;
import com.amap.llm.agent.api.AMapContext;
import com.amap.llm.agent.api.AMapNaviEnv;
import com.amap.llm.agent.api.AgentClient;
import com.amap.llm.agent.api.ILogger;
import com.amap.api.maps.model.LatLng;
import com.amap.api.maps.model.Poi;
import com.amap.api.navi.AMapNavi;
import com.amap.api.navi.AMapNaviListener;
import com.amap.api.navi.AMapNaviView;
import com.amap.api.navi.AMapNaviViewListener;
import com.amap.api.navi.enums.TransportType;
// 定位 SDK
import com.amap.api.location.AMapLocation;
import com.amap.api.location.AMapLocationClient;
import com.amap.api.location.AMapLocationClientOption;
import com.amap.api.location.AMapLocationListener;

public class MainActivity extends Activity implements AMapNaviListener, AMapNaviViewListener {
    private AMapApi mAMapApi;
    private AMapContext mAMapContext;
    private AMapNaviEnv mAMapNaviEnv;
    private AMapNavi mAMapNavi;
    private AMapNaviView mAMapNaviView;
    
    // 定位相关
    private AMapLocationClient mAMapLocationClient;
    private AMapLocationClientOption mLocationOption;
    private AMapLocationListener mAMapLocationListener = new AMapLocationListener() {
        @Override
        public void onLocationChanged(AMapLocation aMapLocation) {
            if (mAMapApi != null) {
                // 将定位结果更新给 Agent SDK
                mAMapApi.getNaviClient().updateMyLocation(aMapLocation);
            }
            // 定位错误时打印详细信息
            if (aMapLocation != null && aMapLocation.getErrorCode() != 0) {
                Log.e(TAG, "定位错误: code=" + aMapLocation.getErrorCode() + 
                    ", detail=" + aMapLocation.getLocationDetail());
            }
        }
    };
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // 1. 初始化 AMapNaviView（必须在 setContentView 之后）
        mAMapNaviView = findViewById(R.id.navi_view);
        mAMapNaviView.onCreate(savedInstanceState);
        mAMapNaviView.setAMapNaviViewListener(this);
        
        // 2. 创建 API 实例
        mAMapApi = AMapApi.create();
        
        // 3. 创建上下文
        mAMapContext = new AMapContext(this);
        
        // 4. 设置日志回调（推荐）
        setupLogger();
        
        // 5. 初始化 AMapNavi
        initAMapNavi();
        
        // 6. 配置导航环境
        setupNavigationEnvironment();
        
        // 7. 初始化 SDK
        mAMapApi.init(mAMapContext);
        
        // 8. 配置 Agent 客户端
        setupAgentClient();
        
        // 9. 初始化定位 SDK（必须在 mAMapApi 初始化之后）
        initLocation();
    }
    
    private void initLocation() {
        try {
            mAMapLocationClient = new AMapLocationClient(getApplicationContext());
            mLocationOption = new AMapLocationClientOption();
            
            // 设置定位监听
            mAMapLocationClient.setLocationListener(mAMapLocationListener);
            
            // 设置定位间隔（毫秒）
            mLocationOption.setInterval(1000);
            mLocationOption.setOnceLocation(false);
            
            // 设置为高精度定位模式
            mLocationOption.setLocationMode(AMapLocationClientOption.AMapLocationMode.Hight_Accuracy);
            
            // 不需要逆地理信息
            mLocationOption.setNeedAddress(false);
            
            // 设置定位参数
            mAMapLocationClient.setLocationOption(mLocationOption);
            
            // 启动定位
            mAMapLocationClient.startLocation();
        } catch (Exception e) {
            Log.e(TAG, "初始化定位 SDK 失败", e);
        }
    }
    
    private void setupLogger() {
        mAMapContext.setLogger(new ILogger() {
            @Override
            public void onLog(int level, String msg) {
                switch (level) {
                    case ILogger.LOG_LEVEL_DEBUG:
                        Log.d(TAG, msg);
                        break;
                    case ILogger.LOG_LEVEL_INFO:
                        Log.i(TAG, msg);
                        break;
                    case ILogger.LOG_LEVEL_WARN:
                        Log.w(TAG, msg);
                        break;
                    case ILogger.LOG_LEVEL_ERROR:
                        Log.e(TAG, msg);
                        break;
                    case ILogger.LOG_LEVEL_FATAL:
                        Log.wtf(TAG, msg);
                        break;
                    case ILogger.LOG_LEVEL_TRACK:
                        Log.i(TAG, "[TRACK] " + msg);
                        break;
                }
                // 可选：将日志显示到 UI 上
                // appendLog("[" + level + "] " + msg);
            }
        });
    }
    
    private void initAMapNavi() {
        mAMapNavi = AMapNavi.getInstance(getApplicationContext());
        mAMapNavi.addAMapNaviListener(this);
        mAMapNavi.setUseInnerVoice(true);
    }
    
    private void setupNavigationEnvironment() {
        mAMapNaviEnv = new AMapNaviEnv();
        
        // 设置家和公司位置
        Poi homePoi = new Poi("我的家", new LatLng(39.904200, 116.407396), "HOME_POI_ID");
        mAMapNaviEnv.homeLocation = homePoi;
        
        Poi workPoi = new Poi("我的公司", new LatLng(40.002577, 116.489854), "WORK_POI_ID");
        mAMapNaviEnv.workLocation = workPoi;
        
        // 设置导航类型和路径偏好
        mAMapNaviEnv.transportType = TransportType.Drive;
        mAMapNaviEnv.avoidCongestion = true;
        mAMapNaviEnv.avoidHighway = false;
        mAMapNaviEnv.avoidCost = false;
        
        // 绑定导航实例（必须）
        mAMapNaviEnv.amapNavi = mAMapNavi;
        mAMapNaviEnv.amapNaviView = mAMapNaviView;
        
        mAMapContext.setAMapNaviEnv(mAMapNaviEnv);
    }
    
    private void setupAgentClient() {
        AgentClient agentClient = mAMapApi.getAgentClient();
        
        agentClient.setAgentCallback(new AMapAgentCallback() {
            @Override
            public void onQueryResult(AMapAgentQueryResult result) {
                handleQueryResult(result);
            }
        });
        
        // AMAP_SDK: 在当前应用执行 | AMAP_APP: 发送到高德APP执行
        agentClient.setAgentCommandDestination(AgentClient.AgentCommandDestination.AMAP_SDK);
    }
    
    // ==================== 生命周期管理 ====================
    
    @Override
    protected void onResume() {
        super.onResume();
        if (mAMapNaviView != null) {
            mAMapNaviView.onResume();
        }
    }
    
    @Override
    protected void onPause() {
        super.onPause();
        if (mAMapNaviView != null) {
            mAMapNaviView.onPause();
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 销毁定位
        if (mAMapLocationClient != null) {
            mAMapLocationClient.stopLocation();
            mAMapLocationClient.onDestroy();
            mAMapLocationClient = null;
        }
        if (mAMapNaviView != null) {
            mAMapNaviView.onDestroy();
        }
        if (mAMapNavi != null) {
            mAMapNavi.removeAMapNaviListener(this);
            mAMapNavi.destroy();
        }
        if (mAMapApi != null) {
            mAMapApi.destroy();
        }
    }
    
    // ==================== AMapNaviListener 关键回调 ====================
    
    @Override
    public void onCalculateRouteSuccess(int[] ints) {
        // 算路成功后自动开始导航
        if (mAMapNavi != null) {
            mAMapNavi.startNavi(NaviType.GPS);
        }
    }
    
    @Override
    public void onCalculateRouteFailure(int errorInfo) {
        Log.e(TAG, "路线计算失败: " + errorInfo);
    }
    
    // 其他 AMapNaviListener 和 AMapNaviViewListener 方法需要实现
    // 参考完整示例代码
}
```

## 初始化顺序说明

正确的初始化顺序非常重要：

1. **AMapNaviView.onCreate()** - 必须在 setContentView 之后立即调用
2. **AMapApi.create()** - 创建 API 实例
3. **AMapContext** - 创建上下文
4. **setLogger()** - 设置日志回调（推荐，便于调试）
5. **AMapNavi.getInstance()** - 初始化导航实例
6. **setupNavigationEnvironment()** - 配置导航环境，绑定 AMapNavi 和 AMapNaviView
7. **AMapApi.init()** - 初始化 SDK
8. **setupAgentClient()** - 配置 Agent 客户端
9. **initLocation()** - 初始化定位 SDK（必须在 mAMapApi 初始化之后，因为定位回调需要调用 mAMapApi）

## 定位 SDK 说明

定位 SDK 用于获取用户实时位置，并通过 `mAMapApi.getNaviClient().updateMyLocation(aMapLocation)` 将位置信息更新给 Agent SDK，这对于导航和位置相关的查询非常重要。

关键配置：
- **定位间隔**：默认 1000ms，可根据需求调整
- **定位模式**：使用高精度模式 `Hight_Accuracy`
- **逆地理信息**：默认关闭，如需地址信息可开启

## 下一步

- [发送 AI 查询](agent-query.md)
- [处理查询结果](query-result.md)
- [日志配置](logger.md)

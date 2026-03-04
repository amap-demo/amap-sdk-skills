# LinkClient 与高德 APP 通信

通过 LinkClient 实现与高德 APP 的数据同步和远程控制。

## 导入依赖

```java
import com.amap.llm.agent.api.AMapApi;
import com.amap.llm.agent.api.AMapLinkStateCallback;
import com.amap.llm.agent.api.AMapNaviInfoCallback;
import com.amap.llm.agent.api.AMapTaxiInfoCallback;
import com.amap.llm.agent.api.AgentClient;
import com.amap.llm.agent.api.LinkClient;
```

## 初始化配置

```java
private void connectToAmapApp() {
    LinkClient linkClient = mAMapApi.getLinkClient();
    
    // 1. 配置自动重连（启用重连，间隔100ms，最多2次）
    linkClient.setReconnectConfig(true, 100, 2);
    
    // 2. 设置链接状态回调
    linkClient.setLinkStateCallback(new AMapLinkStateCallback() {
        @Override
        public void onLinkState(AMapLinkStateCallback.LinkState state) {
            runOnUiThread(() -> {
                switch (state) {
                    case CONNECTED:
                        Log.i(TAG, "已连接到高德APP");
                        // 连接成功后切换命令目标为高德APP
                        mAMapApi.getAgentClient().setAgentCommandDestination(
                            AgentClient.AgentCommandDestination.AMAP_APP);
                        break;
                    case DISCONNECTED:
                        Log.w(TAG, "与高德APP断开连接");
                        // 断开后切回本地SDK执行
                        mAMapApi.getAgentClient().setAgentCommandDestination(
                            AgentClient.AgentCommandDestination.AMAP_SDK);
                        break;
                }
            });
        }
        
        @Override
        public void onLinkError(int errorCode, String errorMessage) {
            Log.e(TAG, "连接错误: " + errorCode + " - " + errorMessage);
        }
    });
    
    // 3. 设置导航信息回调
    linkClient.setNaviInfoCallback(new AMapNaviInfoCallback() {
        @Override
        public void onNaviInfo(NaviInfo info) {
            Log.i(TAG, "收到导航信息: 类型=" + info.type);
        }
    });
    
    // 4. 设置打车信息回调
    linkClient.setTaxiInfoCallback(new AMapTaxiInfoCallback() {
        @Override
        public void onTaxiReceived(TaxiInfo info) {
            Log.i(TAG, "打车信息: " + info.toString());
        }
    });
    
    // 5. 连接服务器
    linkClient.connectLinkServer();
}
```

> **注意**：状态回调在子线程中触发，如需更新 UI（如按钮文字、Toast 等），必须通过 `runOnUiThread` 切换到主线程。

## 常用操作

```java
// 连接/断开服务器
mAMapApi.getLinkClient().connectLinkServer();
mAMapApi.getLinkClient().disConnectLinkServer();

// 停止导航
mAMapApi.getLinkClient().stopNavi();

// 切换路线
mAMapApi.getLinkClient().switchRoute("pathID");

// 切换播报方式（驾车）
mAMapApi.getLinkClient().switchVoiceMode(0, 2);

// 强制刷新导航信息
mAMapApi.getLinkClient().sendKeyNaviInfo();

// 跳转到应用市场下载高德APP
mAMapApi.getLinkClient().goToDownloadAmapApp();

// 开始认证
mAMapApi.getLinkClient().startAuth();
```

## 相关文档

- [快速接入](quick-start.md)

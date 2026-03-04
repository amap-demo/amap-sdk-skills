# 切换导航模式

支持驾车、骑行、步行、电动车等导航模式切换。

## 导入依赖

```java
import com.amap.llm.agent.api.AMapApi;
import com.amap.llm.agent.api.AMapConstants;
import com.amap.llm.agent.api.AMapNaviEnv;
import com.amap.api.navi.enums.TransportType;
import com.amap.api.navi.AMapNavi;
import com.amap.api.navi.AMapNaviView;
import com.amap.api.navi.model.AMapTravelInfo;
```

## 切换方法

```java
private void switchTransportType(int transportType) {
    // 1. 停止当前导航
    mAMapNavi.stopNavi();
    mAMapNavi.destroy();
    
    // 2. 重新创建导航实例
    mAMapNavi = AMapNavi.getInstance(getApplicationContext());
    mAMapNavi.addAMapNaviListener(this);
    
    // 3. 根据类型设置导航视图模式
    if (transportType == TransportType.Ride || 
        transportType == TransportType.Walk || 
        transportType == TransportType.EleBike) {
        mAMapNavi.setIsNaviTravelView(true);
        mAMapNavi.setTravelInfo(new AMapTravelInfo(transportType));
    } else {
        mAMapNavi.setIsNaviTravelView(false);
    }
    
    // 4. 更新导航环境
    mAMapNaviEnv.transportType = transportType;
    mAMapNaviEnv.amapNavi = mAMapNavi;
    mAMapNaviEnv.amapNaviView = mAMapNaviView;
    mAMapApi.getNaviClient().configNaviEnv(mAMapNaviEnv);
    
    // 5. 重置 Agent 状态
    mAMapApi.getAgentClient().resetAgentScene(AMapConstants.SceneType.HOME);
}
```

## 使用示例

```java
switchTransportType(TransportType.Drive);    // 驾车
switchTransportType(TransportType.Ride);     // 骑行
switchTransportType(TransportType.Walk);     // 步行
switchTransportType(TransportType.EleBike);  // 电动车
```

## TransportType 说明

| 类型 | 说明 |
|-----|------|
| `TransportType.Drive` | 驾车导航 |
| `TransportType.Ride` | 骑行导航 |
| `TransportType.Walk` | 步行导航 |
| `TransportType.EleBike` | 电动车导航 |

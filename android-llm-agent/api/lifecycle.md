# 生命周期管理

正确管理 SDK 生命周期，避免内存泄漏。

## Activity 生命周期

```java
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
    
    // 1. 停止并销毁定位
    if (mAMapLocationClient != null) {
        mAMapLocationClient.stopLocation();
        mAMapLocationClient.onDestroy();
        mAMapLocationClient = null;
    }
    
    // 2. 销毁导航视图
    if (mAMapNaviView != null) {
        mAMapNaviView.onDestroy();
    }
    
    // 3. 移除监听并销毁导航
    if (mAMapNavi != null) {
        mAMapNavi.removeAMapNaviListener(this);
        mAMapNavi.destroy();
    }
    
    // 4. 销毁 SDK
    if (mAMapApi != null) {
        mAMapApi.destroy();
    }
}
```

## 注意事项

- `onResume`/`onPause` 必须调用 `mAMapNaviView` 对应方法，需加 null 检查
- `onDestroy` 中需按顺序释放资源：定位 → 导航视图 → 导航实例 → SDK
- 销毁导航前需先调用 `removeAMapNaviListener` 移除监听
- 定位销毁后需置 null 避免重复销毁

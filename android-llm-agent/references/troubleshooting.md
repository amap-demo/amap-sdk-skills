# 常见问题诊断

## SDK 初始化失败

```java
private boolean checkInitialization() {
    // 检查 API Key
    if (TextUtils.isEmpty(getApiKey())) {
        Log.e(TAG, "API Key not set");
        return false;
    }
    
    // 检查网络权限
    if (!hasNetworkPermission()) {
        Log.e(TAG, "Network permission not granted");
        return false;
    }
    
    return true;
}
```

**检查项：**
- API Key 是否正确设置
- 网络权限是否授予
- 高德地图 SDK 版本兼容性
- 查看日志中的具体错误信息

## 查询没有返回结果

```java
private void diagnoseQueryIssue(AMapAgentQueryResult result) {
    Log.d(TAG, "Error code: " + result.errorCode);
    Log.d(TAG, "Error message: " + result.errorMessage);
    Log.d(TAG, "Session ID: " + result.sessionId);
    Log.d(TAG, "Action type: " + result.actionType);
    
    switch (result.errorCode) {
        case AMapConstants.ERROR_CODE_ILLEGAL_STATUS_STR:
            mAMapApi.getAgentClient().resetAgentScene(AMapConstants.SceneType.HOME);
            break;
        case AMapConstants.ERROR_CODE_HOME_NOT_SET:
            Log.w(TAG, "请先设置家的位置");
            break;
    }
}
```

**检查项：**
- 查询文本格式是否正确
- 当前场景状态是否合适
- 网络连接是否正常

## 导航无法开始

**检查项：**
- 定位权限是否授予
- 定位服务是否正常
- 起终点坐标是否有效
- AMapNaviEnv 配置是否正确

## 性能问题

**优化建议：**
- 合理设置定位频率
- 及时释放大对象和回调
- 使用异步处理避免阻塞主线程
- 定期清理缓存数据

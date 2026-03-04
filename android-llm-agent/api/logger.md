# 日志配置

配置 SDK 日志输出和性能埋点。

## 配置方法

```java
mAMapContext.setLogger(new ILogger() {
    @Override
    public void onLog(int level, String msg) {
        switch (level) {
            case LOG_LEVEL_DEBUG:
                Log.d(TAG, msg);
                break;
            case LOG_LEVEL_INFO:
                Log.i(TAG, msg);
                break;
            case LOG_LEVEL_WARN:
                Log.w(TAG, msg);
                break;
            case LOG_LEVEL_ERROR:
                Log.e(TAG, msg);
                break;
            case LOG_LEVEL_FATAL:
                Log.wtf(TAG, msg);
                break;
            case LOG_LEVEL_TRACK:
                Log.i(TAG, "[TRACK] " + msg);
                break;
        }
    }
});

// 可选：启用多路径发送
mAMapContext.setSendMultiPath(true);
```

## 日志级别说明

| 级别 | 说明 |
|-----|------|
| `LOG_LEVEL_DEBUG` | 调试信息 |
| `LOG_LEVEL_INFO` | 一般信息 |
| `LOG_LEVEL_WARN` | 警告信息 |
| `LOG_LEVEL_ERROR` | 错误信息 |
| `LOG_LEVEL_FATAL` | 致命错误 |
| `LOG_LEVEL_TRACK` | 性能埋点 |

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高德地图REST API Skill使用示例
演示如何使用AMapPersonalMapClient实现各种地理信息服务
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from amap_personal_map_client import AMapPersonalMapClient
import json

def demo_basic_services():
    """演示基本服务功能"""
    print("=== 基本服务功能演示 ===")
    
    # 初始化客户端
    client = AMapPersonalMapClient(os.getenv("AMAP_API_KEY"))
    
    # 1. 地理编码服务
    print("1. 地理编码服务:")
    result = client.maps_geo("天安门广场", "北京")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 2. 逆地理编码服务
    print("\n2. 逆地理编码服务:")
    result = client.maps_regeocode(116.397451, 39.909221)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def demo_poi_services():
    """演示POI服务功能"""
    print("\n=== POI服务功能演示 ===")
    
    # 初始化客户端
    client = AMapPersonalMapClient(os.getenv("AMAP_API_KEY"))
    
    # 3. 关键词搜索POI
    print("3. 关键词搜索POI:")
    pois = client.maps_text_search("烤鸭", "北京", offset=3)
    print(json.dumps(pois, ensure_ascii=False, indent=2))
    
    # 4. 周边搜索POI
    print("\n4. 周边搜索POI:")
    pois = client.maps_around_search("餐厅", "116.397451,39.909221", radius=1000, offset=3)
    print(json.dumps(pois, ensure_ascii=False, indent=2))

def demo_routing_services():
    """演示路径规划服务功能"""
    print("\n=== 路径规划服务功能演示 ===")
    
    # 初始化客户端
    client = AMapPersonalMapClient(os.getenv("AMAP_API_KEY"))
    
    # 5. 步行路线规划
    print("5. 步行路线规划:")
    route = client.maps_direction_walking("116.397451,39.909221", "116.397029,39.917839")
    if "error" not in route:
        distance = route.get("route", {}).get("paths", [{}])[0].get("distance", "未知")
        duration = route.get("route", {}).get("paths", [{}])[0].get("duration", "未知")
        print("步行距离: {}米, 预计时间: {}秒".format(distance, duration))
    else:
        print(json.dumps(route, ensure_ascii=False, indent=2))
    
    # 6. 驾车路线规划
    print("\n6. 驾车路线规划:")
    route = client.maps_direction_driving("116.397451,39.909221", "116.397029,39.917839")
    if "error" not in route:
        distance = route.get("route", {}).get("paths", [{}])[0].get("distance", "未知")
        duration = route.get("route", {}).get("paths", [{}])[0].get("duration", "未知")
        print("驾车距离: {}米, 预计时间: {}秒".format(distance, duration))
    else:
        print(json.dumps(route, ensure_ascii=False, indent=2))
    
    # 7. 公共交通路线规划
    print("\n7. 公共交通路线规划:")
    route = client.maps_direction_transit_integrated("116.397451,39.909221", "116.397029,39.917839", "北京")
    if "error" not in route:
        distance = route.get("route", {}).get("transits", [{}])[0].get("distance", "未知")
        duration = route.get("route", {}).get("transits", [{}])[0].get("duration", "未知")
        print("公交距离: {}米, 预计时间: {}秒".format(distance, duration))
    else:
        print(json.dumps(route, ensure_ascii=False, indent=2))

def demo_other_services():
    """演示其他服务功能"""
    print("\n=== 其他服务功能演示 ===")
    
    # 初始化客户端
    client = AMapPersonalMapClient(os.getenv("AMAP_API_KEY"))
    
    # 9. IP定位服务
    print("9. IP定位服务:")
    result = client.maps_ip_location("114.114.114.114")
    print(json.dumps(result, ensure_ascii=False, indent=2))

def demo_map_services():
    """演示地图展示服务功能 - 包含二维码下载和展示最佳实践"""
    print("\n=== 地图展示服务功能演示 ===")
    
    # 初始化客户端
    client = AMapPersonalMapClient(os.getenv("AMAP_API_KEY"))
    
    # 12. 生成个人地图行程(WIA小程序版本)
    print("12. 生成个人地图行程(WIA小程序版本):")
    line_list = [
        {
            "title": "北京市中心一日游",
            "pointInfoList": [
                {
                    "name": "天安门广场",
                    "lon": 116.397451,
                    "lat": 39.909221,
                    "poiId": "B000A8URXB"
                },
                {
                    "name": "故宫博物院",
                    "lon": 116.397029,
                    "lat": 39.917839,
                    "poiId": "B000A8URXC"
                }
            ]
        }
    ]
    
    # sceneType 说明：
    #   1 - 创建资源点 且 创建路线（默认，通用场景）
    #   2 - 仅创建资源点（搜索类数据，多个点无关联关系）
    #   3 - 仅创建路线（路径规划类数据，多个点有关联关系，如起终点/换乘点）
    map_info = client.maps_schema_personal_map("北京经典景点游", line_list, sceneType=2)
    if "error" not in map_info:
        print("高德地图WIA小程序链接:", map_info.get("schema_url", ""))
        print("二维码图片链接:", map_info.get("qr_code_url", ""))
        
        # ========== 二维码展示最佳实践 ==========
        # 1. 下载二维码到本地
        import urllib.request
        import os
        
        # 设置输出路径（根据实际环境调整）
        output_dir = os.path.expanduser("~/.qoderwork/workspace")
        os.makedirs(output_dir, exist_ok=True)
        qr_path = os.path.join(output_dir, "北京经典景点游_二维码.png")
        
        try:
            urllib.request.urlretrieve(map_info["qr_code_url"], qr_path)
            print(f"\n✅ 二维码已保存到: {qr_path}")
            
            # 2. 在回复中嵌入 Markdown 图片（双重保障）
            print(f"\n![个人地图二维码](file://{qr_path})")
            
            # 3. 提供备用链接
            print(f"\n备用链接（如果图片无法显示）: {map_info['qr_code_url']}")
            
            # 4. 使用 present 工具展示（实际使用时调用）
            # from qoderwork.tools import present
            # present(artifacts=[qr_path])
            
        except Exception as e:
            print(f"\n⚠️  下载二维码失败: {e}")
            print(f"请直接访问二维码链接: {map_info['qr_code_url']}")
    else:
        print("生成失败:", map_info["message"])

def main():
    """主函数"""
    try:
        demo_basic_services()
        demo_poi_services()
        demo_routing_services()
        demo_other_services()
        demo_map_services()
        print("\n🎉 所有功能演示完成！")
    except Exception as e:
        print("❌ 演示过程中出现错误: {}".format(str(e)))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
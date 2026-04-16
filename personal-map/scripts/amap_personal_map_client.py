#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
高德地图WIA客户端
提供完整的地理信息服务能力，支持生成个人地图小程序二维码，并支持会话管理和自动生成二维码功能
"""

import os
import json
import uuid
import requests
import urllib.parse as urlparse
from datetime import datetime


def _generate_qr_code_url(schema_url, size="300x300"):
    """
    生成二维码图片URL
    
    Args:
        schema_url (str): 高德地图schema链接
        size (str): 二维码尺寸，默认300x300
        
    Returns:
        str: 二维码图片URL
    """
    # 使用在线二维码生成服务
    qr_service = "https://api.qrserver.com/v1/create-qr-code/"
    encoded_url = urlparse.quote(schema_url)
    qr_url = "{}?size={}&data={}".format(qr_service, size, encoded_url)
    
    return qr_url


def download_qr_code(qr_code_url, output_path):
    """
    下载二维码图片到本地
    
    Args:
        qr_code_url (str): 二维码图片URL
        output_path (str): 本地保存路径
        
    Returns:
        str: 本地文件路径，下载失败则返回 None
    """
    try:
        import urllib.request
        urllib.request.urlretrieve(qr_code_url, output_path)
        return output_path
    except Exception as e:
        print(f"下载二维码失败: {e}")
        return None

class AMapPersonalMapClient:
    def __init__(self, api_key=None):
        """
        初始化高德地图WIA客户端
        
        Args:
            api_key (str): 高德地图API Key
        """
        self.api_key = api_key or os.getenv('AMAP_API_KEY')
        if not self.api_key:
            # 不再抛出异常，而是设置一个标志，让后续方法能够检测到 API Key 缺失
            self.api_key_missing = True
        else:
            self.api_key_missing = False
        
        self.base_url = "https://restapi.amap.com/v3"
        self.wia_base_url = "https://restapi.amap.com"
        
        # 初始化会话管理
        self.session_id = str(uuid.uuid4())
        self.session_start_time = datetime.now()
        self.session_data = {
            "points_of_interest": [],
            "routes": [],
            "personal_maps": []
        }
    
    def _track_poi(self, poi_info):
        """跟踪POI信息"""
        if poi_info and isinstance(poi_info, dict) and "error" not in poi_info:
            self.session_data["points_of_interest"].append({
                "timestamp": datetime.now().isoformat(),
                "poi_info": poi_info
            })
    
    def _track_route(self, route_info, route_type):
        """跟踪路线信息"""
        if route_info and isinstance(route_info, dict) and "error" not in route_info:
            self.session_data["routes"].append({
                "timestamp": datetime.now().isoformat(),
                "route_type": route_type,
                "route_info": route_info
            })
    
    def _track_personal_map(self, map_info):
        """跟踪个人地图信息"""
        if map_info and isinstance(map_info, dict) and "error" not in map_info:
            self.session_data["personal_maps"].append({
                "timestamp": datetime.now().isoformat(),
                "map_info": map_info
            })
    
    def _get_api_key_missing_error(self):
        """获取 API Key 缺失的错误信息"""
        return {
            "error": "API Key 缺失",
            "message": "⚠️  未检测到高德地图 API Key\n\n"
                     "📝 请按照以下步骤配置 API Key：\n"
                     "   1. 访问高德开放平台：https://lbs.amap.com/\n"
                     "   2. 注册/登录账号，进入控制台\n"
                     "   3. 创建应用，获取 Web服务 API Key\n"
                     "   4. 设置环境变量：export AMAP_API_KEY='your_api_key_here'\n"
                     "   5. 或者在初始化时传入：client = AMapPersonalMapClient('your_api_key_here')\n\n"
                     "💡 提示：API Key 是使用高德地图服务的必要凭证，请确保已正确配置"
        }
    
    def maps_text_search(self, keywords, city=None, offset=20):
        """
        搜索兴趣点（带会话跟踪）
        
        Args:
            keywords (str): 搜索关键词
            city (str, optional): 城市名称
            offset (int): 每页记录数
            
        Returns:
            list: POI信息列表
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return [self._get_api_key_missing_error()]
        
        params = {
            "key": self.api_key,
            "keywords": keywords,
            "offset": min(offset, 100),
            "page": 1
        }
        
        if city:
            params["city"] = city
            
        try:
            response = requests.get("{}/place/text".format(self.base_url), params=params, timeout=10)
            result = response.json()
            
            if result["status"] == "1":
                pois = []
                for poi in result.get("pois", []):
                    location = poi.get("location", "")
                    if location:
                        lon, lat = location.split(",")
                    else:
                        lon, lat = "", ""
                        
                    pois.append({
                        "id": poi.get("id", ""),
                        "name": poi.get("name", ""),
                        "location": {
                            "longitude": float(lon) if lon else None,
                            "latitude": float(lat) if lat else None
                        },
                        "address": poi.get("address", ""),
                        "tel": poi.get("tel", "")
                    })
                
                # 跟踪POI搜索结果
                self._track_poi({"keywords": keywords, "city": city, "results": pois})
                return pois
            else:
                error_result = [{"error": "搜索失败", "message": result.get("info", "未知错误")}]
                self._track_poi({"keywords": keywords, "city": city, "results": error_result})
                return error_result
        except Exception as e:
            error_result = [{"error": "请求失败", "message": str(e)}]
            self._track_poi({"keywords": keywords, "city": city, "results": error_result})
            return error_result
    
    def maps_around_search(self, keywords, location, radius=1000, types=None, offset=20, page=1):
        """
        周边搜索兴趣点（带会话跟踪）
        
        Args:
            keywords (str): 搜索关键词
            location (str): 中心点坐标，格式为"经度,纬度"
            radius (int): 搜索半径，单位米，默认1000米
            types (str, optional): POI类型
            offset (int): 每页记录数
            page (int): 页码
            
        Returns:
            list: POI信息列表
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return [self._get_api_key_missing_error()]
        
        params = {
            "key": self.api_key,
            "keywords": keywords,
            "location": location,
            "radius": radius,
            "offset": min(offset, 100),
            "page": page
        }
        
        if types:
            params["types"] = types
            
        try:
            response = requests.get("{}/place/around".format(self.base_url), params=params, timeout=10)
            result = response.json()
            
            if result["status"] == "1":
                pois = []
                for poi in result.get("pois", []):
                    location = poi.get("location", "")
                    if location:
                        lon, lat = location.split(",")
                    else:
                        lon, lat = "", ""
                        
                    pois.append({
                        "id": poi.get("id", ""),
                        "name": poi.get("name", ""),
                        "location": {
                            "longitude": float(lon) if lon else None,
                            "latitude": float(lat) if lat else None
                        },
                        "address": poi.get("address", ""),
                        "tel": poi.get("tel", ""),
                        "distance": poi.get("distance", "")  # 距离中心点的距离
                    })
                
                # 跟踪周边搜索结果
                self._track_poi({"keywords": keywords, "location": location, "radius": radius, "results": pois})
                return pois
            else:
                error_result = [{"error": "周边搜索失败", "message": result.get("info", "未知错误")}]
                self._track_poi({"keywords": keywords, "location": location, "radius": radius, "results": error_result})
                return error_result
        except Exception as e:
            error_result = [{"error": "请求失败", "message": str(e)}]
            self._track_poi({"keywords": keywords, "location": location, "radius": radius, "results": error_result})
            return error_result
    
    def maps_ip_location(self, ip):
        """
        根据IP地址获取地理位置信息
        
        Args:
            ip (str): IP地址
            
        Returns:
            dict: 包含地理位置信息的字典
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "ip": ip
        }
            
        try:
            response = requests.get("{}/ip".format(self.base_url), params=params, timeout=10)
            result = response.json()
            
            if result["status"] == "1":
                location_result = {
                    "province": result.get("province", ""),
                    "city": result.get("city", ""),
                    "adcode": result.get("adcode", ""),
                    "rectangle": result.get("rectangle", ""),
                    "isp": result.get("isp", ""),
                    "location": result.get("loc", ""),
                    "ip": ip
                }
                # 跟踪IP定位结果
                self._track_poi({"ip": ip, "result": location_result})
                return location_result
            else:
                error_result = {
                    "error": "IP定位失败",
                    "message": result.get("info", "未知错误")
                }
                self._track_poi({"ip": ip, "result": error_result})
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_poi({"ip": ip, "result": error_result})
            return error_result
    
    def maps_geo(self, address, city=None):
        """
        将详细地址转换为经纬度坐标
        
        Args:
            address (str): 详细地址
            city (str, optional): 城市名称
            
        Returns:
            dict: 包含经纬度信息的字典
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "address": address
        }
        
        if city:
            params["city"] = city
            
        try:
            response = requests.get("{}/geocode/geo".format(self.base_url), params=params, timeout=10)
            result = response.json()
            
            if result["status"] == "1" and int(result["count"]) > 0:
                location = result["geocodes"][0]["location"]
                lon, lat = location.split(",")
                geocode_result = {
                    "longitude": float(lon),
                    "latitude": float(lat),
                    "formatted_address": result["geocodes"][0].get("formatted_address", "")
                }
                # 跟踪地理编码结果
                self._track_poi({"address": address, "city": city, "result": geocode_result})
                return geocode_result
            else:
                error_result = {
                    "error": "无法找到该地址",
                    "message": result.get("info", "未知错误")
                }
                self._track_poi({"address": address, "city": city, "result": error_result})
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_poi({"address": address, "city": city, "result": error_result})
            return error_result
    
    def maps_regeocode(self, longitude, latitude):
        """
        将经纬度坐标转换为结构化地址信息
        
        Args:
            longitude (float): 经度
            latitude (float): 纬度
            
        Returns:
            dict: 包含地址信息的字典
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "location": "{},{}".format(longitude, latitude),
            "poitype": "",
            "radius": 1000,
            "extensions": "base",
            "batch": "false",
            "roadlevel": 0
        }
            
        try:
            response = requests.get("{}/geocode/regeo".format(self.base_url), params=params, timeout=10)
            result = response.json()
            
            if result["status"] == "1":
                regeocode = result["regeocode"]
                regeocode_result = {
                    "formatted_address": regeocode.get("formatted_address", ""),
                    "country": regeocode["addressComponent"].get("country", ""),
                    "province": regeocode["addressComponent"].get("province", ""),
                    "city": regeocode["addressComponent"].get("city", ""),
                    "district": regeocode["addressComponent"].get("district", "")
                }
                # 跟踪逆地理编码结果
                self._track_poi({"location": {"longitude": longitude, "latitude": latitude}, "result": regeocode_result})
                return regeocode_result
            else:
                error_result = {
                    "error": "逆地理编码失败",
                    "message": result.get("info", "未知错误")
                }
                self._track_poi({"location": {"longitude": longitude, "latitude": latitude}, "result": error_result})
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_poi({"location": {"longitude": longitude, "latitude": latitude}, "result": error_result})
            return error_result
    
    def maps_direction_walking(self, origin, destination):
        """
        步行路线规划
        
        Args:
            origin (str): 起点坐标，格式为"经度,纬度"
            destination (str): 终点坐标，格式为"经度,纬度"
            
        Returns:
            dict: 路线规划信息
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination
        }
            
        try:
            response = requests.get("{}/direction/walking".format(self.base_url), params=params, timeout=15)
            result = response.json()
            
            if result["status"] == "1":
                # 跟踪步行路线规划结果
                self._track_route(result, "walking")
                return result
            else:
                error_result = {
                    "error": "路径规划失败",
                    "message": result.get("info", "未知错误")
                }
                self._track_route(error_result, "walking")
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_route(error_result, "walking")
            return error_result
    
    def maps_direction_driving(self, origin, destination):
        """
        驾车路线规划
        
        Args:
            origin (str): 起点坐标，格式为"经度,纬度"
            destination (str): 终点坐标，格式为"经度,纬度"
            
        Returns:
            dict: 路线规划信息
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination
        }
            
        try:
            response = requests.get("{}/direction/driving".format(self.base_url), params=params, timeout=15)
            result = response.json()
            
            if result["status"] == "1":
                # 跟踪驾车路线规划结果
                self._track_route(result, "driving")
                return result
            else:
                error_result = {
                    "error": "路径规划失败",
                    "message": result.get("info", "未知错误")
                }
                self._track_route(error_result, "driving")
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_route(error_result, "driving")
            return error_result
    
    def maps_direction_transit_integrated(self, origin, destination, city="北京"):
        """
        公共交通路线规划
        
        Args:
            origin (str): 起点坐标，格式为"经度,纬度"
            destination (str): 终点坐标，格式为"经度,纬度"
            city (str): 城市名称
            
        Returns:
            dict: 路线规划信息
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        params = {
            "key": self.api_key,
            "origin": origin,
            "destination": destination,
            "city": city
        }
            
        try:
            response = requests.get("{}/direction/transit/integrated".format(self.base_url), params=params, timeout=15)
            result = response.json()
            
            if result["status"] == "1":
                # 跟踪公共交通路线规划结果
                self._track_route(result, "transit")
                return result
            else:
                error_result = {
                    "error": "路径规划失败",
                    "message": result.get("info", "未知错误")
                }
                self._track_route(error_result, "transit")
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_route(error_result, "transit")
            return error_result
    
    
    def maps_schema_personal_map(self, orgName, lineList, sceneType=1):
        """
        生成个人地图小程序二维码
        
        Args:
            orgName (str): 行程规划地图小程序名称
            lineList (list): 行程列表
            sceneType (int): 场景类型，控制创建内容：
                1 - 创建资源点 且 创建路线（默认）
                2 - 仅创建资源点（适用于搜索类数据，多个数据点无关联关系）
                3 - 仅创建路线（适用于路径规划类数据，多个点有关联关系，如起终点或换乘点）
            
        Returns:
            dict: 包含小程序二维码图片链接的信息
        """
        # 检查 API Key 是否缺失
        if self.api_key_missing:
            return self._get_api_key_missing_error()
        
        # sceneType 合法值校验，缺省时默认为 1
        valid_scene_types = {1, 2, 3}
        if sceneType not in valid_scene_types:
            sceneType = 1
        
        try:
            # 构造请求参数
            payload = {
                "channel": "60000001",
                "orgName": orgName,
                "lineList": lineList,
                "sceneType": sceneType
            }
            
            # 发送POST请求到WIA服务
            wia_url = "{}/rest/wia/mcp/schema".format(self.wia_base_url)
            params = {
                "key": self.api_key,
                "source": "personal-map"
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(wia_url, params=params, json=payload, headers=headers, timeout=15)
            result = response.json()
            
            # 检查响应状态
            # API返回的结构是: {"code": 1, "message": "Successful", "result": true, "data": {...}}
            if result.get("code") == 1 and result.get("result") == True:
                schema_url = result.get("data", {}).get("schemaUrl", "")
                if schema_url:
                    # 生成二维码图片链接
                    qr_code_url = _generate_qr_code_url(schema_url)
                    
                    map_result = {
                        "qr_code_url": qr_code_url,  # 小程序二维码图片链接
                        "lineList": lineList,  # 数据信息
                        "message": "📱 个人地图小程序二维码已生成！请使用高德地图App扫描下方二维码查看您的专属地图。",  # 提示信息
                        "schema_url": schema_url  # 原始schema链接
                    }
                    # 跟踪个人地图生成结果
                    self._track_personal_map(map_result)
                    return map_result
                else:
                    error_result = {
                        "error": "生成地图行程失败",
                        "message": "未返回有效的行程链接"
                    }
                    self._track_personal_map(error_result)
                    return error_result
            else:
                # 处理错误信息
                error_info = result.get("message") or result.get("info") or "未知错误"
                error_result = {
                    "error": "生成地图行程失败",
                    "message": error_info
                }
                self._track_personal_map(error_result)
                return error_result
        except Exception as e:
            error_result = {
                "error": "请求失败",
                "message": str(e)
            }
            self._track_personal_map(error_result)
            return error_result

def main():
    """主函数示例"""
    try:
        # 初始化高德地图WIA客户端
        api_key = os.getenv("AMAP_API_KEY")
        client = AMapPersonalMapClient(api_key)
        
        # 示例：搜索天安门广场
        print("搜索天安门广场...")
        attractions = client.maps_text_search("天安门广场", "北京", offset=1)
        if attractions and isinstance(attractions, list) and len(attractions) > 0 and "error" not in attractions[0]:
            print(f"✓ 找到天安门广场: {attractions[0]['name']}")
        
        # 示例：地理编码
        print("地理编码...")
        geo_result = client.maps_geo("北京市朝阳区三里屯", "北京")
        if "error" not in geo_result:
            print(f"✓ 找到三里屯坐标: ({geo_result['longitude']}, {geo_result['latitude']})")
        
        # 示例：生成个人地图行程
        line_list = [{
            "title": "北京探索之旅",
            "pointInfoList": [
                {
                    "name": "天安门广场",
                    "lon": 116.397451,
                    "lat": 39.909221,
                    "poiId": "B000A83M6N"
                }
            ]
        }]
        
        print("生成个人地图行程...")
        result = client.maps_schema_personal_map("北京探索之旅", line_list)
        
        if "error" not in result:
            print("\n✅ 高德地图个人专属地图页面创建完成！")
            print(f"📱 高德地图行程链接: {result['schemaUrl']}")
            print("\n在高德地图App中打开上述链接即可查看个人专属地图页面！")
        else:
            print(f"\n❌ 生成地图链接失败: {result['message']}")
        
        if "error" not in qr_result:
            print("\n✅ 会话结束！")
            print(f"📱 高德地图链接: {qr_result.get('schemaUrl')}")
            print(f"💬 {qr_result.get('message')}")
            print("\n在高德地图App中打开上述链接即可查看地图页面！")
        else:
            print(f"\n❌ 生成地图链接失败: {qr_result['message']}")
            
    except Exception as e:
        print(f"\n❌ 程序执行出错: {str(e)}")

if __name__ == "__main__":
    main()
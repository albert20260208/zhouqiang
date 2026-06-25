#!/usr/bin/env python3
"""
测试从213实例找到的真实API Key
"""

import requests
import json

# 从213实例找到的API Key
API_KEY = "sk-d0c41d84342e451ca2546a37b1c47955"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

print("🔍 测试从213实例找到的API Key")
print("=" * 60)
print(f"API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
print(f"基础URL: {BASE_URL}")

# 测试模型列表端点
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

try:
    print("\n📡 测试API连接...")
    response = requests.get(f"{BASE_URL}/models", headers=headers, timeout=10)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        models = response.json()
        print(f"✅ API连接成功！")
        print(f"可用模型数量: {len(models.get('data', []))}")
        
        # 显示所有模型
        print("\n📋 可用模型列表:")
        for i, model in enumerate(models.get('data', [])[:20]):  # 只显示前20个
            model_id = model.get('id', 'N/A')
            if 'seedance' in model_id.lower():
                print(f"  {i+1:2d}. ✅ {model_id}")
            else:
                print(f"  {i+1:2d}.     {model_id}")
        
        # 查找Seedance模型
        seedance_models = [m for m in models.get('data', []) if 'seedance' in m.get('id', '').lower()]
        print(f"\n🎬 找到 {len(seedance_models)} 个Seedance模型:")
        for model in seedance_models:
            model_id = model.get('id')
            print(f"  - {model_id}")
            
            # 检查是否是1.5 Pro
            if '1-5-pro' in model_id:
                print(f"    ✅ 这是Seedance 1.5 Pro模型！")
                
    elif response.status_code == 401:
        print(f"❌ 认证失败: 401 Unauthorized")
        print(f"错误信息: {response.text[:500]}")
        
        # 尝试其他认证格式
        print("\n🔄 尝试其他认证格式...")
        auth_formats = [
            ("直接Key格式", API_KEY),
            ("X-API-Key格式", API_KEY),
        ]
        
        for format_name, auth_value in auth_formats:
            print(f"\n测试格式: {format_name}")
            test_headers = {"Content-Type": "application/json"}
            
            if "X-API-Key" in format_name:
                test_headers["X-API-Key"] = auth_value
            else:
                test_headers["Authorization"] = auth_value
            
            try:
                test_response = requests.get(f"{BASE_URL}/models", headers=test_headers, timeout=10)
                print(f"状态码: {test_response.status_code}")
                if test_response.status_code == 200:
                    print(f"✅ {format_name} 认证成功！")
                    break
                else:
                    print(f"❌ {format_name} 失败: {test_response.text[:200]}")
            except Exception as e:
                print(f"❌ 请求异常: {e}")
                
    else:
        print(f"❌ API连接失败: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        
except Exception as e:
    print(f"❌ API连接异常: {e}")

print("\n" + "=" * 60)
print("如果API Key有效，下一步：")
print("1. 确认正确的视频生成端点")
print("2. 发送李世民攻城视频生成请求")
print("3. 监控任务状态")
print("4. 下载生成的视频")
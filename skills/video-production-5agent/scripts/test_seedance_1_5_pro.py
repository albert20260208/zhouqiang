#!/usr/bin/env python3
"""
专门测试 Seedance 1.5 Pro 模型 (doubao-seedance-1-5-pro-251215)
"""

import base64
import json
import requests
import time
from pathlib import Path

# 配置
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL_ID = "doubao-seedance-1-5-pro-251215"

# 测试用的API Key（需要替换为实际可用的Key）
# 注意：根据之前的测试，当前Key格式可能不正确
TEST_API_KEYS = [
    "sk-4f3d4d8f5a8b4e8c9d7f6a5b4c3d2e1f",  # 当前使用的Key
    # 添加其他可能格式的Key
]

# 图片路径
IMAGE_PATH = "/root/.openclaw/workspace/lishimin_reference.jpg"

# 简化提示词（用于测试）
TEST_PROMPT = "生成一个3秒的视频，展现李世民指挥军队的场景。风格：史诗战争电影。"

def encode_image_to_base64(image_path):
    """将图片编码为base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_model_list(api_key):
    """测试获取模型列表（验证API Key和端点）"""
    print(f"\n测试API Key: {api_key[:20]}...")
    
    # 尝试不同的认证头格式
    auth_formats = [
        ("Bearer标准", {"Authorization": f"Bearer {api_key}"}),
        ("直接Key", {"Authorization": api_key}),
        ("X-API-Key", {"X-API-Key": api_key}),
    ]
    
    for format_name, headers in auth_formats:
        print(f"  认证格式: {format_name}")
        full_headers = {"Content-Type": "application/json", **headers}
        
        try:
            response = requests.get(f"{BASE_URL}/models", headers=full_headers, timeout=10)
            print(f"    状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                print(f"    ✓ 成功! 获取到 {len(models)} 个模型")
                
                # 检查是否有Seedance 1.5 Pro模型
                seedance_models = [m for m in models if 'seedance' in m.get('id', '').lower()]
                print(f"    Seedance模型: {[m['id'] for m in seedance_models]}")
                
                # 检查目标模型是否存在
                target_model = next((m for m in models if m['id'] == MODEL_ID), None)
                if target_model:
                    print(f"    ✓ 找到目标模型: {MODEL_ID}")
                    print(f"      模型信息: {json.dumps(target_model, indent=2, ensure_ascii=False)[:200]}...")
                    return True, api_key, format_name
                else:
                    print(f"    ✗ 未找到模型: {MODEL_ID}")
                    
            elif response.status_code == 401:
                error_data = response.json()
                print(f"    ✗ 认证失败: {error_data.get('error', {}).get('message', 'Unknown error')}")
            else:
                print(f"    ✗ 其他错误: {response.text[:100]}")
                
        except Exception as e:
            print(f"    ✗ 请求异常: {str(e)[:50]}")
    
    return False, None, None

def test_video_generation(api_key, auth_format):
    """测试视频生成"""
    print(f"\n测试视频生成 (使用 {auth_format} 格式)...")
    
    # 编码图片
    print("  编码图片...")
    image_base64 = encode_image_to_base64(IMAGE_PATH)
    print(f"  图片base64长度: {len(image_base64)} 字符")
    
    # 准备请求头
    if auth_format == "Bearer标准":
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    elif auth_format == "直接Key":
        headers = {"Authorization": api_key, "Content-Type": "application/json"}
    elif auth_format == "X-API-Key":
        headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    else:
        headers = {"Authorization": api_key, "Content-Type": "application/json"}
    
    # 尝试不同的请求体格式
    # 格式1: 简单格式（可能适用于Seedance）
    payload1 = {
        "model": MODEL_ID,
        "prompt": TEST_PROMPT,
        "image": image_base64,
        "duration": 3,  # 3秒
        "fps": 24,
        "resolution": "1024x576"  # 测试用较低分辨率
    }
    
    # 格式2: 内容数组格式
    payload2 = {
        "model": MODEL_ID,
        "content": [
            {"type": "text", "text": TEST_PROMPT},
            {"type": "image", "image": image_base64}
        ],
        "video_params": {
            "duration_seconds": 3,
            "fps": 24,
            "width": 1024,
            "height": 576
        }
    }
    
    # 格式3: 消息格式（OpenAI兼容）
    payload3 = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": TEST_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
    }
    
    # 测试不同的端点
    endpoints = [
        "/video/generate",
        "/generations",
        "/inference",
        "/tasks",
        "/completions"
    ]
    
    for endpoint in endpoints:
        print(f"\n  测试端点: {endpoint}")
        url = f"{BASE_URL}{endpoint}"
        
        for i, payload in enumerate([payload1, payload2, payload3], 1):
            print(f"    格式{i}...")
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=30)
                print(f"      状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"      ✓ 成功! 响应: {response.text[:200]}")
                    result = response.json()
                    
                    # 保存响应
                    filename = f"seedance_response_{endpoint.replace('/', '_')}_format{i}.json"
                    with open(filename, "w") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    print(f"      响应已保存到: {filename}")
                    
                    # 检查是否有视频URL或任务ID
                    if "video_url" in result:
                        print(f"      视频URL: {result['video_url']}")
                        return True, result
                    elif "task_id" in result:
                        print(f"      任务ID: {result['task_id']}")
                        return True, result
                    elif "data" in result and "video_url" in result.get("data", {}):
                        print(f"      视频URL: {result['data']['video_url']}")
                        return True, result
                    else:
                        print(f"      响应内容: {json.dumps(result, ensure_ascii=False)[:300]}")
                        
                elif response.status_code == 401:
                    error_data = response.json()
                    print(f"      ✗ 认证失败: {error_data.get('error', {}).get('message', 'Unknown error')}")
                elif response.status_code == 404:
                    print(f"      ✗ 端点不存在: {endpoint}")
                else:
                    print(f"      ✗ 其他错误: {response.text[:200]}")
                    
            except Exception as e:
                print(f"      ✗ 请求异常: {str(e)[:100]}")
    
    return False, None

def main():
    print("=" * 60)
    print("Seedance 1.5 Pro 视频生成测试")
    print(f"模型ID: {MODEL_ID}")
    print("=" * 60)
    
    # 检查图片文件
    if not Path(IMAGE_PATH).exists():
        print(f"错误: 图片文件不存在: {IMAGE_PATH}")
        return
    
    print(f"图片文件: {IMAGE_PATH} (存在)")
    
    # 测试每个API Key
    successful_auth = None
    for api_key in TEST_API_KEYS:
        success, working_key, auth_format = test_model_list(api_key)
        if success:
            successful_auth = (working_key, auth_format)
            break
    
    if not successful_auth:
        print("\n✗ 所有API Key都认证失败")
        print("\n关键问题: API Key格式不正确或无效")
        print("错误信息: 'The API key format is incorrect'")
        print("\n需要:")
        print("1. 有效的火山引擎API Key")
        print("2. 正确的认证头格式")
        print("3. API Key需要有视频生成权限")
        print("\n建议:")
        print("1. 登录火山引擎控制台 (https://console.volcengine.com)")
        print("2. 进入「火山方舟」→「API密钥管理」")
        print("3. 创建新的API Key或检查现有Key的状态")
        print("4. 确认Key有视频生成服务的权限")
        return
    
    working_key, auth_format = successful_auth
    print(f"\n✓ 使用有效的认证: {auth_format}")
    
    # 测试视频生成
    print("\n开始视频生成测试...")
    success, result = test_video_generation(working_key, auth_format)
    
    if success:
        print("\n" + "="*60)
        print("✓ 视频生成请求成功!")
        print("="*60)
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
        
        # 提供后续步骤
        print("\n后续操作:")
        print("1. 如果返回了task_id，可能需要轮询获取结果")
        print("2. 如果返回了video_url，可以直接下载视频")
        print("3. 检查保存的JSON文件获取详细信息")
    else:
        print("\n" + "="*60)
        print("✗ 视频生成测试失败")
        print("="*60)
        print("\n可能的原因:")
        print("1. API端点不正确（需要准确的视频生成端点）")
        print("2. 请求格式不符合API要求")
        print("3. 模型参数配置错误")
        print("4. 账户配额不足或服务未开通")
        
        print("\n建议:")
        print("1. 查看火山引擎官方文档获取准确API端点")
        print("2. 联系技术支持获取帮助")
        print("3. 检查火山引擎控制台的服务状态和配额")

if __name__ == "__main__":
    main()
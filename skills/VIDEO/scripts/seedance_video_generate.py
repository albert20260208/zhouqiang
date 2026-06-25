#!/usr/bin/env python3
"""
Seedance 2.0 视频生成脚本
基于官方文档：https://www.volcengine.com/docs/82379/1366799?lang=zh

需要：
1. API Key
2. 图片base64编码
3. 详细提示词
"""

import base64
import json
import requests
import time
from pathlib import Path

# 配置参数
API_KEY = "sk-4f3d4d8f5a8b4e8c9d7f6a5b4c3d2e1f"  # 替换为实际API Key
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
MODEL_ID = "doubao-seedance-1-5-pro-251215"  # Seedance 1.5 Pro 模型（支持API调用）

# 图片路径
IMAGE_PATH = "/root/.openclaw/workspace/lishimin_reference.jpg"

# 详细提示词（5秒视频，分段描述）
PROMPT = """生成一个5秒的史诗级战争视频，展现李世民指挥千军万马攻城的场景。

时间分段和镜头语言：
0-2秒：从李世民背后视角开始，他身穿明光铠，手持龙泉宝剑，站在高处指挥。镜头缓慢环绕，展现他坚毅的侧脸和身后飘扬的军旗，士兵们列阵待发。
2-4秒：镜头快速拉升，转为无人机高空视角，展现整个战场全景。千军万马如潮水般涌向城墙，投石车发射，箭雨如蝗，火光冲天，烟尘弥漫。
4-5秒：镜头俯冲而下，特写士兵拼杀细节。刀剑碰撞，盾牌格挡，战马嘶鸣，展现战争的残酷与壮烈。最后定格在李世民坚定的眼神特写上。

风格要求：
- 电影级史诗感，恢弘气势
- 类似《指环王》的战争场面
- 写实动漫风格，细节丰富
- 动态镜头流畅，景别变化自然
- 色彩饱和度高，对比强烈
- 光影效果出色，有电影质感

技术要求：
- 视频时长：5秒
- 帧率：24fps
- 分辨率：1920×1080
- 画面稳定，无抖动
- 动作连贯，无卡顿"""

def encode_image_to_base64(image_path):
    """将图片编码为base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_api_endpoints():
    """测试API端点"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    endpoints_to_test = [
        "/models",  # 模型列表
        "/chat/completions",  # OpenAI兼容格式
        "/completions",  # 补全格式
        "/generations",  # 生成格式
        "/inference",  # 推理格式
        "/tasks",  # 任务格式
        "/video/generate",  # 视频生成
        "/videos",  # 视频相关
        "/seedance/generate",  # Seedance专用
        "/ark/video/generate",  # ARK视频生成
    ]
    
    print("测试API端点...")
    for endpoint in endpoints_to_test:
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"{endpoint}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"{endpoint}: 错误 - {str(e)[:100]}")

def generate_video_direct():
    """直接调用视频生成API"""
    # 编码图片
    print("编码图片为base64...")
    image_base64 = encode_image_to_base64(IMAGE_PATH)
    print(f"图片base64长度: {len(image_base64)} 字符")
    
    # 准备请求数据
    # 尝试多种可能的API格式
    
    # 格式1: OpenAI兼容格式
    payload1 = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": PROMPT
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }
    
    # 格式2: 简单生成格式
    payload2 = {
        "model": MODEL_ID,
        "input": PROMPT,
        "image": image_base64,
        "parameters": {
            "duration": 5,
            "fps": 24,
            "resolution": "1920x1080"
        }
    }
    
    # 格式3: 内容数组格式
    payload3 = {
        "model": MODEL_ID,
        "content": [
            {
                "type": "text",
                "text": PROMPT
            },
            {
                "type": "image",
                "image": image_base64
            }
        ],
        "video_params": {
            "duration_seconds": 5,
            "fps": 24,
            "width": 1920,
            "height": 1080
        }
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 测试不同的端点
    endpoints = [
        "/chat/completions",
        "/completions", 
        "/generations",
        "/inference",
        "/video/generate",
        "/videos",
        "/seedance/generate"
    ]
    
    for endpoint in endpoints:
        print(f"\n尝试端点: {endpoint}")
        url = f"{BASE_URL}{endpoint}"
        
        # 尝试每种payload格式
        for i, payload in enumerate([payload1, payload2, payload3], 1):
            print(f"  格式{i}...")
            try:
                response = requests.post(
                    url, 
                    headers=headers, 
                    json=payload,
                    timeout=30
                )
                print(f"    状态码: {response.status_code}")
                if response.status_code == 200:
                    print(f"    成功! 响应: {response.text[:200]}")
                    # 保存响应
                    with open(f"response_{endpoint.replace('/', '_')}_format{i}.json", "w") as f:
                        json.dump(response.json(), f, indent=2)
                    return response.json()
                else:
                    print(f"    错误: {response.text[:200]}")
            except Exception as e:
                print(f"    异常: {str(e)[:100]}")
    
    return None

def main():
    print("=" * 60)
    print("Seedance 2.0 视频生成脚本")
    print("=" * 60)
    
    # 检查图片文件
    if not Path(IMAGE_PATH).exists():
        print(f"错误: 图片文件不存在: {IMAGE_PATH}")
        return
    
    print(f"图片文件: {IMAGE_PATH} (存在)")
    
    # 测试API端点
    print("\n1. 测试API端点...")
    test_api_endpoints()
    
    # 尝试生成视频
    print("\n2. 尝试生成视频...")
    result = generate_video_direct()
    
    if result:
        print("\n✓ 视频生成请求成功!")
        print(f"响应: {json.dumps(result, indent=2)[:500]}...")
        
        # 检查是否有视频URL或任务ID
        if "video_url" in result:
            print(f"视频URL: {result['video_url']}")
        elif "task_id" in result:
            print(f"任务ID: {result['task_id']}")
        elif "data" in result and "video_url" in result.get("data", {}):
            print(f"视频URL: {result['data']['video_url']}")
    else:
        print("\n✗ 所有尝试都失败了")
        print("可能的原因:")
        print("1. API端点不正确")
        print("2. API Key权限不足")
        print("3. 模型ID不正确")
        print("4. 请求格式不符合API要求")
        print("\n建议:")
        print("1. 查看火山引擎控制台获取准确API文档")
        print("2. 检查API Key是否包含视频生成权限")
        print("3. 联系技术支持获取帮助")

if __name__ == "__main__":
    main()
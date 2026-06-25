#!/usr/bin/env python3
"""
手动查询任务状态
"""

import requests
import json
import time

API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
TASK_ID = "cgt-20260227001305-cg4lf"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print(f"🔍 查询任务状态: {TASK_ID}")
print("=" * 60)

# 尝试不同的查询端点
endpoints = [
    f"{BASE_URL}/content_generation/tasks/{TASK_ID}",
    f"{BASE_URL}/tasks/{TASK_ID}",
    f"{BASE_URL}/generations/{TASK_ID}",
]

for endpoint in endpoints:
    print(f"\n尝试端点: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 查询成功!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 提取状态
            status = result.get('status') or result.get('state') or result.get('task_status')
            print(f"\n📊 任务状态: {status}")
            
            # 检查是否完成
            if status in ["succeeded", "completed", "finished"]:
                # 提取视频URL
                video_url = None
                if 'video_url' in result:
                    video_url = result['video_url']
                elif 'url' in result:
                    video_url = result['url']
                elif 'content' in result and 'video_url' in result['content']:
                    video_url = result['content']['video_url']
                elif 'data' in result and 'video_url' in result['data']:
                    video_url = result['data']['video_url']
                
                if video_url:
                    print(f"🎥 视频URL: {video_url}")
                    
                    # 尝试下载视频
                    print(f"\n⬇️  尝试下载视频...")
                    try:
                        video_response = requests.get(video_url, timeout=30)
                        if video_response.status_code == 200:
                            video_filename = f"/root/.openclaw/workspace/lishimin_battle_{TASK_ID}.mp4"
                            with open(video_filename, "wb") as f:
                                f.write(video_response.content)
                            print(f"✅ 视频下载成功: {video_filename}")
                            print(f"📏 文件大小: {len(video_response.content) / 1024 / 1024:.2f} MB")
                        else:
                            print(f"❌ 视频下载失败: {video_response.status_code}")
                    except Exception as e:
                        print(f"❌ 视频下载异常: {e}")
            
            break
            
        elif response.status_code == 404:
            print(f"❌ 端点不存在")
        else:
            print(f"❌ 查询失败: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
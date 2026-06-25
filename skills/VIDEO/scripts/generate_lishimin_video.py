#!/usr/bin/env python3
"""
使用231实例的配置生成李世民攻城视频
"""

import os
import time
import json
import base64
from pathlib import Path
from volcenginesdkarkruntime import Ark

# ============ 配置 ============

# 使用231实例的有效API Key
ARK_API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"

# 模型ID (Seedance 1.0 Pro - 231实例已验证可用)
MODEL_ID = "doubao-seedance-1-0-pro-250528"

# 图片文件路径
IMAGE_PATH = "/root/.openclaw/workspace/lishimin_reference.jpg"

# ============ 初始化客户端 ============

print("=" * 60)
print("🎬 李世民攻城视频生成")
print("=" * 60)

try:
    client = Ark(api_key=ARK_API_KEY)
    print(f"✅ 客户端初始化成功")
except Exception as e:
    print(f"❌ 客户端初始化失败: {e}")
    exit(1)

# ============ 图片处理 ============

def image_to_base64(image_path):
    """将图片转换为base64字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# 检查图片文件
if not Path(IMAGE_PATH).exists():
    print(f"❌ 图片文件不存在: {IMAGE_PATH}")
    exit(1)

print(f"📷 读取图片: {IMAGE_PATH}")
image_base64 = image_to_base64(IMAGE_PATH)
print(f"✅ 图片已编码: {len(image_base64)} 字符")

# ============ 视频生成参数 ============

# 详细提示词（5秒时间分段）
prompt = """0-2秒：李世民背面→侧面环绕，指挥千军万马，明光铠反射阳光，龙泉宝剑指向城墙
2-4秒：镜头拉升，无人机战场全景，千军万马冲锋，投石车发射，城墙火光
4-5秒：俯冲特写，士兵拼杀细节，刀剑碰撞火花，尘土飞扬，战旗飘扬
风格：恢弘气势，电影史诗感，4K画质，电影级运镜，动态光影"""

print(f"\n📝 提示词: {prompt}")
print(f"🎬 模型: {MODEL_ID}")
print(f"⏱️ 时长: 5秒")
print(f"📐 比例: 16:9")

# ============ 发送生成请求 ============

def generate_video():
    """发送视频生成请求"""
    print("\n🚀 发送视频生成请求...")
    
    try:
        # 构建请求内容
        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}"
                }
            },
            {
                "type": "text",
                "text": prompt
            }
        ]
        
        # 创建视频生成任务
        task = client.content_generation.tasks.create(
            model=MODEL_ID,
            content=content,
            extra_body={
                "duration": 5,
                "ratio": "16:9"
            }
        )
        
        print(f"✅ 任务创建成功!")
        print(f"   任务 ID: {task.id}")
        print(f"   状态: {task.status}")
        print(f"   创建时间: {task.created_at}")
        
        return {"task_id": task.id, "status": task.status, "created_at": task.created_at}
        
    except Exception as e:
        print(f"❌ 创建任务失败: {e}")
        return {"error": str(e)}

# ============ 任务状态查询 ============

def check_task_status(task_id):
    """查询任务状态"""
    try:
        task = client.content_generation.tasks.retrieve(task_id)
        
        result = {
            "task_id": task.id,
            "status": task.status,
            "created_at": task.created_at,
        }
        
        # 如果完成，获取视频 URL
        if task.status == "succeeded" and hasattr(task, 'content'):
            if hasattr(task.content, 'video_url'):
                result["video_url"] = task.content.video_url
                print(f"🎥 视频URL: {task.content.video_url}")
        
        return result
        
    except Exception as e:
        return {"error": str(e)}

# ============ 等待视频生成 ============

def wait_for_video(task_id, max_wait=300, interval=10):
    """
    等待视频生成完成
    
    Args:
        task_id: 任务 ID
        max_wait: 最大等待时间（秒）
        interval: 轮询间隔（秒）
    """
    print(f"\n⏳ 等待视频生成...")
    print(f"   任务ID: {task_id}")
    print(f"   最大等待: {max_wait}秒")
    print(f"   轮询间隔: {interval}秒")
    
    start_time = time.time()
    last_status = ""
    
    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)
        
        if "error" in result:
            print(f"❌ 查询状态失败: {result['error']}")
            return result
        
        status = result.get("status", "")
        
        # 只在新状态时打印
        if status != last_status:
            print(f"   [{time.strftime('%H:%M:%S')}] 状态: {status}")
            last_status = status
        
        if status == "succeeded":
            print(f"✅ 视频生成完成!")
            print(f"🎉 成功生成李世民攻城视频!")
            return result
        elif status == "failed":
            print(f"❌ 视频生成失败")
            return {"error": "Video generation failed", "details": result}
        
        time.sleep(interval)
    
    return {"error": f"Timeout after {max_wait} seconds"}

# ============ 主函数 ============

def main():
    # 发送生成请求
    result = generate_video()
    
    if "error" in result:
        print(f"\n❌ 无法创建任务: {result['error']}")
        return
    
    if "task_id" not in result:
        print(f"\n❌ 未获取到任务ID")
        return
    
    task_id = result["task_id"]
    
    # 保存任务ID
    with open("/root/.openclaw/workspace/task_id.txt", "w") as f:
        f.write(task_id)
    print(f"📝 任务ID已保存到: /root/.openclaw/workspace/task_id.txt")
    
    # 等待视频生成
    final_result = wait_for_video(task_id, max_wait=600, interval=15)  # 10分钟超时
    
    print(f"\n📦 最终结果:")
    print(json.dumps(final_result, indent=2, ensure_ascii=False))
    
    if "video_url" in final_result:
        print(f"\n🎥 视频下载链接: {final_result['video_url']}")
        
        # 保存视频URL
        with open("/root/.openclaw/workspace/video_url.txt", "w") as f:
            f.write(final_result['video_url'])
        print(f"📝 视频URL已保存到: /root/.openclaw/workspace/video_url.txt")
        
        print(f"\n🎉 李世民攻城视频生成成功！")
        print(f"   请使用上面的URL下载视频文件")
    else:
        print(f"\n❌ 视频生成失败或超时")
        print(f"   错误信息: {final_result.get('error', '未知错误')}")

if __name__ == "__main__":
    main()
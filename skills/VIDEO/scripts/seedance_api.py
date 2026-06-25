#!/usr/bin/env python3
"""
Seedance 视频生成 API 调用脚本
使用火山引擎官方 SDK
"""

import os
import time
import json
from volcenginesdkarkruntime import Ark

# ============ 配置 ============

# API Key (从火山引擎控制台获取)
ARK_API_KEY = "d380aed6-916e-4542-bd67-a20bbd1b377c"  # 海哥提供的 API Key

# 模型 ID (Seedance 视频生成模型)
MODEL_ID = "doubao-seedance-1-5-pro-251215"  # 回退到 Seedance 1.5 (2.0需要激活)

# ============ 初始化客户端 ============

client = Ark(api_key=ARK_API_KEY)


def generate_video_text2video(prompt: str, 
                               duration: int = 5,
                               ratio: str = "16:9") -> dict:
    """
    文生视频 - 根据文字描述生成视频
    
    Args:
        prompt: 视频描述提示词
        duration: 视频时长（秒），支持 5 或 10
        ratio: 画面比例，支持 "16:9", "9:16", "1:1"
    
    Returns:
        任务信息
    """
    try:
        # 创建视频生成任务
        task = client.content_generation.tasks.create(
            model=MODEL_ID,
            content=[
                {
                    "type": "text",
                    "text": prompt
                }
            ],
            # 视频参数
            extra_body={
                "duration": duration,
                "ratio": ratio
            }
        )
        
        print(f"✅ 任务创建成功!")
        print(f"   任务 ID: {task.id}")
        
        # 打印完整任务信息用于调试
        print(f"   完整任务信息:")
        for attr in dir(task):
            if not attr.startswith('_'):
                try:
                    value = getattr(task, attr)
                    if not callable(value):
                        print(f"     - {attr}: {value}")
                except:
                    pass
        
        return {"task_id": task.id, "task_object": task}
        
    except Exception as e:
        print(f"❌ 创建任务失败: {e}")
        return {"error": str(e)}


def generate_video_image2video(image_url: str,
                                prompt: str = "",
                                duration: int = 5) -> dict:
    """
    图生视频 - 根据图片生成视频
    
    Args:
        image_url: 图片 URL
        prompt: 可选的文字描述
        duration: 视频时长（秒）
    
    Returns:
        任务信息
    """
    try:
        content = [
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ]
        
        if prompt:
            content.append({
                "type": "text", 
                "text": prompt
            })
        
        task = client.content_generation.tasks.create(
            model=MODEL_ID,
            content=content,
            extra_body={
                "duration": duration
            }
        )
        
        print(f"✅ 图生视频任务创建成功!")
        print(f"   任务 ID: {task.id}")
        
        return {"task_id": task.id, "status": task.status}
        
    except Exception as e:
        print(f"❌ 创建任务失败: {e}")
        return {"error": str(e)}


def check_task_status(task_id: str) -> dict:
    """查询视频生成任务状态"""
    try:
        task = client.content_generation.tasks.get(task_id=task_id)
        
        result = {
            "task_id": task.id,
            "status": task.status,  # "pending", "processing", "succeeded", "failed"
            "created_at": task.created_at,
        }
        
        # 如果完成，获取视频 URL
        if task.status == "succeeded" and hasattr(task, 'content'):
            result["video_url"] = task.content.video_url
            
        return result
        
    except Exception as e:
        return {"error": str(e)}


def wait_for_video(task_id: str, max_wait: int = 300, interval: int = 10) -> dict:
    """
    等待视频生成完成
    
    Args:
        task_id: 任务 ID
        max_wait: 最大等待时间（秒）
        interval: 轮询间隔（秒）
    
    Returns:
        最终结果
    """
    print(f"\n⏳ 等待视频生成...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        result = check_task_status(task_id)
        
        if "error" in result:
            return result
        
        status = result.get("status", "")
        print(f"   状态: {status}")
        
        if status == "succeeded":
            print(f"✅ 视频生成完成!")
            return result
        elif status == "failed":
            print(f"❌ 视频生成失败")
            return {"error": "Video generation failed", "details": result}
        
        time.sleep(interval)
    
    return {"error": "Timeout waiting for video generation"}


# ============ 使用示例 ============

if __name__ == "__main__":
    print("=" * 50)
    print("Seedance 视频生成测试")
    print("=" * 50)
    
    # 测试提示词
    test_prompt = """
    一只可爱的橘猫在阳光下的窗台上打盹，
    镜头缓慢推进，
    温暖的午后光线，
    电影质感，4K画质
    """
    
    print(f"\n📝 提示词: {test_prompt.strip()}")
    print(f"🎬 模型: {MODEL_ID}")
    print()
    
    # 创建任务
    result = generate_video_text2video(
        prompt=test_prompt,
        duration=5,
        ratio="16:9"
    )
    
    if "task_id" in result:
        # 等待完成
        final_result = wait_for_video(result["task_id"])
        print(f"\n📦 最终结果:")
        print(json.dumps(final_result, indent=2, ensure_ascii=False))
        
        if "video_url" in final_result:
            print(f"\n🎥 视频下载链接: {final_result['video_url']}")
    else:
        print(f"\n❌ 错误: {result}")

#!/usr/bin/env python3
"""
生成房间两个不同视角的静态图像（通过短视频实现）
确保场景一致性和物品位置逻辑正确
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seedance_api import generate_video_text2video, check_task_status

def generate_room_view(view_name, prompt, duration=2):
    """生成一个房间视角"""
    print(f"\n🎨 生成 {view_name}...")
    print(f"📝 提示词: {prompt[:100]}...")
    
    result = generate_video_text2video(prompt, duration=duration)
    
    if result and "task_id" in result:
        task_id = result["task_id"]
        print(f"✅ 任务创建成功: {task_id}")
        
        # 监控任务状态
        print("⏳ 监控任务状态...")
        for i in range(30):  # 最多等待5分钟
            status_result = check_task_status(task_id)
            status = status_result.get('status', 'unknown')
            print(f"  检查 {i+1}/30: 状态={status}")
            
            if status == 'succeeded':
                video_url = status_result.get('video_url')
                print(f"✅ 生成完成!")
                return {"task_id": task_id, "video_url": video_url, "success": True}
            elif status == 'failed':
                print(f"❌ 生成失败")
                return {"task_id": task_id, "success": False, "error": "生成失败"}
                
            time.sleep(10)
        else:
            print("⏰ 超时")
            return {"task_id": task_id, "success": False, "error": "超时"}
    else:
        print("❌ 创建任务失败")
        return {"success": False, "error": "未获取到任务ID"}

def download_video(task_id, video_url, filename):
    """下载视频到本地"""
    import requests
    
    download_dir = '/root/.openclaw/workspace/downloads/videos'
    os.makedirs(download_dir, exist_ok=True)
    filepath = os.path.join(download_dir, filename)
    
    print(f"📥 下载视频到: {filepath}")
    
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                downloaded += len(chunk)
                f.write(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    if int(percent) % 20 == 0:
                        print(f"  下载进度: {percent:.1f}%")
        
        file_size = os.path.getsize(filepath) / (1024*1024)
        print(f"✅ 下载完成: {file_size:.2f} MB")
        return {"success": True, "filepath": filepath, "size_mb": file_size}
    
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return {"success": False, "error": str(e)}

def main():
    print("=" * 60)
    print("房间多视角一致性测试")
    print("生成两个不同视角的静态房间图像")
    print("=" * 60)
    
    # 视角1: 从东往西看
    view1_prompt = """Static view from the east side of a room looking west. 
    Camera fixed, no movement, static image style. 
    On the left (south wall): a wooden desk with books and a lamp. 
    Directly ahead (west wall): a comfortable bed with blue bedsheets. 
    On the right (north wall): a glass coffee table with a vase. 
    Behind the camera (east wall): a wooden door. 
    Photorealistic, interior design, detailed textures, natural lighting, 
    static shot, no motion, 8K quality, architectural visualization."""
    
    # 视角2: 从西往东看（对面视角）
    view2_prompt = """Static view from the west side of the same room looking east. 
    Camera fixed, no movement, static image style. 
    On the left (north wall): a glass coffee table with a vase. 
    Directly ahead (east wall): a wooden door. 
    On the right (south wall): a wooden desk with books and a lamp. 
    Behind the camera (west wall): a comfortable bed with blue bedsheets. 
    Consistent room layout with previous view, same furniture and decor. 
    Photorealistic, interior design, detailed textures, natural lighting, 
    static shot, no motion, 8K quality, architectural visualization."""
    
    # 生成第一个视角
    view1_result = generate_room_view("视角1: 从东往西看", view1_prompt, duration=5)
    
    if not view1_result.get("success"):
        print("❌ 视角1生成失败")
        sys.exit(1)
    
    # 生成第二个视角
    view2_result = generate_room_view("视角2: 从西往东看", view2_prompt, duration=5)
    
    if not view2_result.get("success"):
        print("❌ 视角2生成失败")
        sys.exit(1)
    
    # 下载两个视频
    print("\n" + "=" * 60)
    print("开始下载生成的视频...")
    print("=" * 60)
    
    download1 = download_video(
        view1_result["task_id"], 
        view1_result["video_url"],
        f"房间视角1_从东往西看_{view1_result['task_id']}.mp4"
    )
    
    download2 = download_video(
        view2_result["task_id"], 
        view2_result["video_url"],
        f"房间视角2_从西往东看_{view2_result['task_id']}.mp4"
    )
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("生成结果汇总:")
    print("=" * 60)
    
    results = []
    if download1.get("success"):
        results.append({
            "name": "房间视角1 - 从东往西看",
            "filepath": download1["filepath"],
            "size_mb": download1["size_mb"],
            "task_id": view1_result["task_id"]
        })
    
    if download2.get("success"):
        results.append({
            "name": "房间视角2 - 从西往东看", 
            "filepath": download2["filepath"],
            "size_mb": download2["size_mb"],
            "task_id": view2_result["task_id"]
        })
    
    # 保存结果到文件供后续使用
    results_file = "/tmp/room_views_results.txt"
    with open(results_file, "w") as f:
        for r in results:
            f.write(f"{r['name']}\n")
            f.write(f"  task_id: {r['task_id']}\n")
            f.write(f"  filepath: {r['filepath']}\n")
            f.write(f"  size: {r['size_mb']:.2f} MB\n")
            f.write("\n")
    
    print(f"✅ 所有任务完成! 结果保存到: {results_file}")
    
    # 打印结果供用户查看
    for r in results:
        print(f"\n📋 {r['name']}:")
        print(f"  任务ID: {r['task_id']}")
        print(f"  文件路径: {r['filepath']}")
        print(f"  文件大小: {r['size_mb']:.2f} MB")

if __name__ == "__main__":
    main()
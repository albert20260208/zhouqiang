#!/usr/bin/env python3
"""Seedream 5.0 图像生成 - 直接HTTP调用"""

import requests
import json
import sys
import os

API_KEY = "c62ca369-c8cc-4a21-b97e-b0dcc6776e69"
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

def generate_image(prompt, size="1920x1920", model="doubao-seedream-5-0-260128"):
    """生成图片"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "url",
        "watermark": False
    }
    
    print(f"🎨 正在生成图片...")
    print(f"   模型: {model}")
    print(f"   尺寸: {size}")
    print(f"   提示词: {prompt[:80]}...")
    print()
    
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        print(f"   HTTP状态: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            if "data" in data and len(data["data"]) > 0:
                url = data["data"][0].get("url", "")
                print(f"✅ 生成成功!")
                print(f"🖼️ 图片URL: {url}")
                return url
            else:
                print(f"❌ 返回数据异常: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 请求失败: {resp.text}")
            
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    return None

if __name__ == "__main__":
    prompt = """一位唐朝少女站在古城墙之上，俯瞰远方。

【人物】
年轻女子，约18岁，鹅蛋脸，柳叶眉，杏眼含情，肤若凝脂。
乌黑长发高挽成飞仙髻，点缀金步摇和鲜花发簪。
身穿石榴红交领齐胸襦裙，披帛如彩云般随风飘扬，
腰系鹅黄色丝质腰带，佩戴白玉璎珞。

【场景】
唐代古城城墙之上，青砖城垛，远处是飞檐翘角的城楼。
城下是繁华的长安街市，隐约可见坊市屋顶。
天空金霞满布，夕阳西下，暮色将至。

【镜头】
中近景（Medium Close-Up），胸部以上。
肩高机位（Shoulder Level），微仰5度，
赋予人物端庄高贵感。
人物置于画面右侧三分构图位，
微侧身回眸望向镜头左侧远方。
浅景深（f/2.0），前景清晰，
背景城楼和夕阳柔和虚化。
85mm人像镜头质感。

【色彩与光线】
黄金时刻（Golden Hour）侧逆光，
发丝和披帛边缘泛金色轮廓光，
面部以自然反射光柔和补光。
整体暖橙色调，高光偏金，暗部偏赭。

【质感】
电影级画质，4K超清，
胶片颗粒感，色彩浓郁饱满，
2.35:1宽银幕构图感。"""

    # 9:16竖屏人像
    url = generate_image(prompt, size="1600x2848")
    
    if url:
        # 下载图片
        print(f"\n📥 正在下载图片...")
        img_resp = requests.get(url, timeout=60)
        if img_resp.status_code == 200:
            save_path = "/root/.openclaw/workspace/tang_girl.jpg"
            with open(save_path, "wb") as f:
                f.write(img_resp.content)
            print(f"✅ 已保存到: {save_path}")
            print(f"   文件大小: {len(img_resp.content) / 1024:.1f} KB")

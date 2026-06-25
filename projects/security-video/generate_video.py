#!/usr/bin/env python3
"""
上海银行安防数智化宣传片 - 自动生成脚本
读取Excel脚本 → 生成带字幕/旁白/背景的MP4视频
"""

import openpyxl
import asyncio
import os
import sys
import subprocess
from pathlib import Path
from moviepy import (
    VideoClip, AudioFileClip, TextClip, ColorClip,
    CompositeVideoClip, concatenate_videoclips, ImageClip,
    vfx, afx
)
import numpy as np

# ====== 配置 ======
EXCEL_PATH = "/root/.openclaw/media/qqbot/downloads/20260616上海银行安防数字化探索实践短片脚本-V1_1781602866070_644fd5.xlsx"
OUTPUT_DIR = Path("/root/.openclaw/workspace/projects/security-video/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 视频参数
VIDEO_SIZE = (1920, 1080)  # 16:9 1080p
FPS = 24

# 文字样式
FONT_COLOR = "#1a1a1a"
FONT_SIZE_TITLE = 52
FONT_SIZE_BODY = 36
FONT_NAME = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"  # 文泉驿微米黑

# 背景色
BG_COLOR = (245, 245, 248)  # 浅灰白
BG_COLOR_ALT = (250, 250, 253)  # 备用白

# TTS 配置
TTS_VOICE = "zh-CN-XiaoxiaoNeural"  # 晓晓 - 女声
TTS_RATE = "+5%"  # 稍微加速


def parse_excel(excel_path: str) -> list[dict]:
    """解析Excel脚本，提取所有场景"""
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['上篇']

    scenes = []
    current_chapter = ""

    for row in ws.iter_rows(values_only=True):
        vals = [str(c).strip() if c else '' for c in row]
        line = '|'.join(vals)

        # 跳过空行
        if all(v == '' for v in vals[:4]):
            continue

        # 检测章节标题
        if '章节' in vals[0] or '板块' in vals[0]:
            current_chapter = vals[0]
            continue

        # 解析镜号行
        first = vals[0]
        if first.isdigit():
            # 解析时间
            time_str = vals[1] if len(vals) > 1 else ''
            start_sec, end_sec = parse_time(time_str)

            scenes.append({
                'num': int(first),
                'time': time_str,
                'start_sec': start_sec,
                'end_sec': end_sec,
                'duration': end_sec - start_sec,
                'visual': vals[2] if len(vals) > 2 else '',
                'subtitle': vals[3] if len(vals) > 3 else '',
                'narration': vals[4] if len(vals) > 4 else '',
                'materials': vals[5] if len(vals) > 5 else '',
                'chapter': current_chapter
            })
            print(f"✓ 镜号{first} | {time_str} | {vals[3][:40] if len(vals) > 3 else ''}")

    return scenes


def parse_time(time_str: str) -> tuple[float, float]:
    """解析 mm:ss 时间格式为秒"""
    if not time_str or '-' not in time_str:
        return 0, 10

    parts = time_str.split('-')
    def _to_sec(t):
        t = t.strip()
        if ':' in t:
            m, s = t.split(':')
            return int(m) * 60 + int(s)
        return float(t)

    return _to_sec(parts[0]), _to_sec(parts[1])


def create_placeholder_bg(color: tuple, size: tuple) -> np.ndarray:
    """创建纯色占位背景 - 带渐变效果"""
    w, h = size
    img = np.zeros((h, w, 3), dtype=np.uint8)
    # 从上到下渐变
    for y in range(h):
        ratio = y / h
        r = int(color[0] + (color[0] * 0.5) * ratio)
        g = int(color[1] + (color[1] * 0.6) * ratio)
        b = int(color[2] + (color[2] * 0.4) * ratio)
        img[y, :] = [min(r, 255), min(g, 255), min(b, 255)]
    return img


def create_scene_clip(scene: dict, idx: int, total: int) -> VideoClip:
    """为单个场景创建视频片段"""
    duration = max(scene['duration'], 3)  # 最少3秒
    w, h = VIDEO_SIZE

    # 1. 创建背景
    if idx % 2 == 0:
        bg_color = BG_COLOR
    else:
        bg_color = BG_COLOR_ALT

    def make_frame(t):
        """动态背景 - 带缓慢光效动画"""
        frame = create_placeholder_bg(bg_color, VIDEO_SIZE)
        # 添加缓慢移动的光点
        cx = int(w * 0.3 + np.sin(t * 0.5) * w * 0.3)
        cy = int(h * 0.4 + np.cos(t * 0.6) * h * 0.3)
        for dx in range(-150, 150, 5):
            for dy in range(-150, 150, 5):
                px, py = cx + dx, cy + dy
                if 0 <= px < w and 0 <= py < h:
                    dist = np.sqrt(dx*dx + dy*dy)
                    alpha = max(0, 1 - dist / 150)
                    brightness = int(alpha * 40)
                    frame[py, px] = np.clip(
                        frame[py, px].astype(int) + brightness, 0, 255
                    ).astype(np.uint8)
        return frame

    bg_clip = VideoClip(make_frame, duration=duration)

    # 2. 创建字幕
    subtitle = scene['subtitle']
    clips = [bg_clip]

    if subtitle and subtitle != '/' and subtitle.strip():
        # 清理字幕文本
        clean_text = subtitle.replace('【下阶段】', '\n【下阶段】')
        clean_text = clean_text.replace('【动画】', '').replace('【照片轮播】', '').replace('【视频轮播】', '')
        # 分割多行
        lines = clean_text.split('\n')
        display_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 跳过纯素材标记行
            if line.startswith('1、') or line.startswith('2、') or line.startswith('3、'):
                display_lines.append(line)
                continue
            # 如果一行超过40字，进一步拆分
            if len(line) > 40:
                # 按标点拆分
                import re
                sub_lines = re.split(r'[；;，,]', line)
                # 合并短的
                merged = []
                current = ''
                for sl in sub_lines:
                    sl = sl.strip()
                    if not sl:
                        continue
                    if len(current + sl) < 45:
                        current += ('；' if current else '') + sl
                    else:
                        if current:
                            merged.append(current)
                        current = sl
                if current:
                    merged.append(current)
                display_lines.extend(merged if merged else [line])
            else:
                display_lines.append(line)

        # 计算字体大小
        n_lines = len(display_lines)
        max_len = max(len(l) for l in display_lines) if display_lines else 0
        if max_len < 15:
            body_size = FONT_SIZE_TITLE
        else:
            body_size = FONT_SIZE_BODY

        # 行距
        line_height = body_size * 1.6
        total_height = line_height * n_lines

        # 逐行创建文字clip，带依次淡入效果
        for i, line in enumerate(display_lines):
            txt_clip = TextClip(
                text=line,
                font=FONT_NAME,
                font_size=body_size,
                color=FONT_COLOR,
                stroke_color=(255, 255, 255),
                stroke_width=0,
                size=(w - 200, None),
                method='caption',
                horizontal_align='center',
            )

            # 计算每行Y位置（居中排列）
            y_start = int((h - total_height) / 2) + int(i * line_height)

            txt_clip = txt_clip.with_position(('center', y_start))

            # 渐入动画：每个字幕行延迟出现
            stagger = i * 0.3  # 每行间隔0.3秒
            txt_clip = txt_clip.with_duration(duration - stagger)
            txt_clip = txt_clip.with_start(stagger)

            # 淡入淡出 (需要先设置duration再应用效果)
            fade_in = min(0.8, (duration - stagger) * 0.2)
            fade_out = min(0.8, (duration - stagger) * 0.2)
            if fade_in > 0:
                txt_clip = txt_clip.with_effects([vfx.FadeIn(fade_in)])
            if fade_out > 0:
                txt_clip = txt_clip.with_effects([vfx.FadeOut(fade_out)])

            clips.append(txt_clip)

    # 3. 场景编号水印（右上角小字）


    # 4. 合成
    composite = CompositeVideoClip(clips, size=VIDEO_SIZE)
    composite = composite.with_duration(duration)
    return composite


async def generate_tts(text: str, output_path: str, voice: str = TTS_VOICE):
    """使用Edge TTS生成旁白音频"""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=TTS_RATE)
    await communicate.save(output_path)
    return output_path


async def main():
    # 1. 解析Excel
    print("=" * 60)
    print("📋 解析Excel脚本...")
    print("=" * 60)
    scenes = parse_excel(EXCEL_PATH)
    print(f"\n共 {len(scenes)} 个场景\n")

    # 2. 生成旁白音频
    print("=" * 60)
    print("🔊 生成旁白音频 (Edge TTS)...")
    print("=" * 60)
    tts_tasks = []
    for scene in scenes:
        narration = scene['narration']
        if narration and narration.strip() and narration != '/':
            audio_path = str(TEMP_DIR / f"narration_{scene['num']:02d}.mp3")
            tts_tasks.append((scene['num'], narration, audio_path))
            print(f"  TTS 镜号{scene['num']}: {narration[:50]}...")

    tts_results = {}
    for num, text, path in tts_tasks:
        try:
            await generate_tts(text, path)
            tts_results[num] = path
            print(f"  ✓ 镜号{num} 旁白生成完成")
        except Exception as e:
            print(f"  ⚠ 镜号{num} TTS失败: {e}")

    # 3. 生成视频片段
    print(f"\n{'='*60}")
    print("🎬 生成视频片段...")
    print("=" * 60)

    scene_clips = []
    for i, scene in enumerate(scenes):
        print(f"  镜号{scene['num']}: {scene['duration']:.0f}秒")

        clip = create_scene_clip(scene, i, len(scenes))

        # 添加旁白音频
        if scene['num'] in tts_results:
            try:
                audio = AudioFileClip(tts_results[scene['num']])
                # 如果音频比视频长，裁剪；如果短，不处理
                if audio.duration > clip.duration:
                    audio = audio.with_duration(clip.duration)
                clip = clip.with_audio(audio)
            except Exception as e:
                print(f"  ⚠ 音频合成失败 镜号{scene['num']}: {e}")

        # 转场效果（淡入淡出）- clip已有duration，直接加效果
        if i > 0:
            clip = clip.with_effects([vfx.FadeIn(0.5)])
        # 拼接时用crossfade更好，这里先不加FadeOut

        scene_clips.append(clip)

    # 4. 拼接所有片段
    print(f"\n{'='*60}")
    print("🔗 拼接视频...")
    print("=" * 60)

    final_video = concatenate_videoclips(scene_clips)

    # 5. 导出
    output_path = str(OUTPUT_DIR / "上海银行安防宣传片_v2_白底黑字.mp4")
    print(f"\n📤 导出: {output_path}")
    print(f"   分辨率: {VIDEO_SIZE[0]}x{VIDEO_SIZE[1]}")
    print(f"   总时长: {final_video.duration:.0f}秒")

    final_video.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='3000k',
        audio_bitrate='192k',
        preset='medium',
        ffmpeg_params=['-pix_fmt', 'yuv420p'],
    )

    # 清理
    final_video.close()
    for clip in scene_clips:
        clip.close()

    print(f"\n✅ 完成! 视频: {output_path}")
    return output_path


if __name__ == '__main__':
    asyncio.run(main())

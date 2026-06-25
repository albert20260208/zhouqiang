#!/usr/bin/env python3
"""
上海银行安防宣传片 V5 — MoviePy 视频合成
品牌色：藏蓝#003D7C + 金#C9A96E + 深底#080C14
每页右下留数字人占位 · TTS旁白 · 文字逐行动画
"""

import openpyxl, asyncio, os, re, json
from pathlib import Path
from moviepy import (
    VideoClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, vfx
)
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass

# ====== 配置 ======
EXCEL_PATH = "/root/.openclaw/media/qqbot/downloads/20260616上海银行安防数字化探索实践短片脚本-V1_1781602866070_644fd5.xlsx"
OUTPUT_DIR = Path("/root/.openclaw/workspace/projects/security-video/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_v5"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

VIDEO_SIZE = (1920, 1080)
FPS = 24
FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

# ====== 品牌色 ======
NAVY   = (0, 61, 124)     # 藏蓝 #003D7C
GOLD   = (201, 169, 110)  # 金色 #C9A96E
BG_D   = (8, 12, 20)      # 深底 #080C14
BG_L   = (13, 21, 37)     # 浮层 #0D1525
WHITE  = (255, 255, 255)
LIGHT  = (208, 212, 220)  # 正文浅灰
GRAY   = (138, 146, 162)  # 辅助灰
DIM    = (85, 93, 110)    # 暗灰

# 数字人区域
AVATAR_BOX = (1550, 800, 1860, 1020)  # (x1, y1, x2, y2) 右下
CONTENT_MAX_X = 1520  # 文字内容最大X（避开数字人）

# ====== 字体加载 ======
def load_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def parse_excel(excel_path: str) -> list[dict]:
    wb = openpyxl.load_workbook(excel_path)
    ws = wb['上篇']
    scenes, chap, sec = [], "", ""
    for row in ws.iter_rows(values_only=True):
        vals = [str(c).strip() if c else '' for c in row[:6]]
        f = vals[0]
        if all(v == '' for v in vals[:4]): continue
        if '章节' in f: chap = f; continue
        if '板块' in f: sec = f; continue
        if '部分' in f or '镜号' in f or '此篇' in f: continue
        if f.isdigit():
            scenes.append(dict(
                num=int(f), time=vals[1],
                visual=vals[2], subtitle=vals[3], narration=vals[4],
                materials=vals[5] if len(vals)>5 else '',
                chapter=chap, section=sec))
    return scenes


def split_lines(text, font, max_width):
    """中文自动换行"""
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_gradient_bg(size, top_color, bottom_color):
    """垂直渐变背景"""
    w, h = size
    img = Image.new('RGB', size)
    for y in range(h):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * y / h)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * y / h)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * y / h)
        for x in range(w):
            img.putpixel((x, y), (r, g, b))
    return img


def make_frame_bg():
    """生成纯深底背景帧"""
    return draw_gradient_bg(VIDEO_SIZE, BG_D, (5, 9, 15))


def draw_text_with_fade(draw, img, lines_data, alpha_mult=1.0):
    """在PIL draw上绘制多行文字，支持透明度"""
    for line in lines_data:
        text = line['text']
        font = line['font']
        color = line['color']
        x, y = line['x'], line['y']
        alpha = line.get('alpha', 1.0) * alpha_mult

        if alpha <= 0:
            continue

        c = tuple(int(v * alpha + (1-alpha) * bg_v) for v, bg_v in zip(color, BG_D))
        draw.text((x, y), text, font=font, fill=c)


# ====== 场景渲染函数 ======

def make_cover_frame():
    """封面帧"""
    img = draw_gradient_bg(VIDEO_SIZE, BG_D, (4, 8, 14))
    draw = ImageDraw.Draw(img)

    # 左侧金线
    for y in range(1080):
        img.putpixel((6, y), GOLD)

    # LOGO
    font_logo = load_font(32, True)
    font_name = load_font(56, True)
    font_main = load_font(64, True)
    font_sub = load_font(28)
    font_bottom = load_font(22)
    font_small = load_font(18)

    draw.text((960, 180), "SHANGHAI BANK", font=font_logo, fill=GOLD, anchor="mt")
    draw.text((960, 220), "上海银行", font=font_name, fill=WHITE, anchor="mt")

    # 金线
    draw.line([(640, 320), (1280, 320)], fill=GOLD, width=3)

    draw.text((960, 430), "安防数智化应用展示", font=font_main, fill=WHITE, anchor="mt")
    draw.text((960, 560), "统筹发展与安全 · 筑牢金融安全防线", font=font_sub, fill=GOLD, anchor="mt")

    # 底栏
    draw.rectangle([(0, 940), (1920, 1080)], fill=BG_L)
    draw.text((960, 960), "上篇 · 安防数智化探索实践", font=font_bottom, fill=GRAY, anchor="mt")
    draw.text((960, 1000), "安全保卫部", font=font_small, fill=DIM, anchor="mt")

    return np.array(img)


def make_scene_frame(sc: dict, scene_idx: int, total: int, progress: float, chapter_label: str):
    """通用场景帧 — 标题 + 内容 + 数字人占位"""
    img = draw_gradient_bg(VIDEO_SIZE, BG_D, (4, 8, 14))
    draw = ImageDraw.Draw(img)

    # 顶栏金线
    draw.line([(0, 4), (1920, 4)], fill=GOLD, width=3)

    # 页码
    font_sm = load_font(16)
    draw.text((60, 18), f"{scene_idx:02d} / {total:02d}", font=font_sm, fill=DIM)

    # 章节标签（右上）
    if chapter_label:
        draw.text((1860, 18), chapter_label, font=font_sm, fill=GOLD, anchor="ra")

    # 数字人占位（右下）
    ax1, ay1, ax2, ay2 = AVATAR_BOX
    draw.rectangle([(ax1, ay1), (ax2, ay2)], outline=GOLD, width=2)
    # 虚线效果：隔段画
    for y in range(ay1+10, ay2, 20):
        draw.line([(ax1+5, y), (ax1+30, y)], fill=GOLD, width=1)
    font_avat = load_font(18)
    draw.text(((ax1+ax2)//2, (ay1+ay2)//2), "数字人", font=font_avat, fill=DIM, anchor="mm")

    # ====== 标题 ======
    subtitle = sc.get('subtitle', '')
    lines = subtitle.replace('<br>', '\n').split('\n') if subtitle and subtitle != '/' else []
    main_title = ""
    for l in lines:
        l = l.strip().replace('【下阶段】', '')
        if l:
            main_title = l
            break
    if not main_title:
        nar = sc.get('narration', '')
        main_title = nar.split('。')[0][:40] if nar else ""

    font_title = load_font(42, True)
    # 限制标题宽度
    title_lines = split_lines(main_title, font_title, 1300)
    for i, tl_text in enumerate(title_lines):
        draw.text((60, 80 + i*55), tl_text, font=font_title, fill=WHITE)

    # 金线
    title_end_y = 80 + len(title_lines)*55
    draw.line([(60, title_end_y+15), (300, title_end_y+15)], fill=GOLD, width=2)

    # ====== 内容要点 ======
    font_body = load_font(26)
    font_body_sm = load_font(22)

    # 从 subtitle 提取要点
    body_items = []
    if subtitle and subtitle != '/':
        for line in subtitle.replace('<br>', '\n').split('\n'):
            line = line.strip()
            if not line or '下阶段' in line: continue
            m = re.match(r'^\d+[、.]?\s*(.+)', line)
            if m: line = m.group(1)
            if len(line) > 3:
                body_items.append(line)

    if not body_items:
        # 从 narration 提取
        nar = sc.get('narration', '')
        body_items = re.split(r'[。；]', nar)
        body_items = [b.strip() for b in body_items if len(b.strip()) > 5]

    # 根据 progress 决定显示多少行
    total_items = len(body_items[:5])
    y_offset = title_end_y + 45
    item_height = 45

    for i, item in enumerate(body_items[:5]):
        item_progress = max(0, min(1, (progress - 0.1 - i*0.15) / 0.15))
        alpha = item_progress

        txt = f"▸ {item}"
        body_lines = split_lines(txt, font_body_sm, 1300)
        for j, bl in enumerate(body_lines):
            c = tuple(int(v * alpha + (1-alpha) * bg_v) for v, bg_v in zip(LIGHT, BG_D))
            if alpha > 0.01:
                draw.text((70, y_offset + i*item_height + j*28), bl, font=font_body_sm, fill=c)

    # ====== 底部旁白 ======
    if progress > 0.6:
        nar = sc.get('narration', '')
        if nar and nar != '/':
            short = nar.split('。')[0].strip()
            if len(short) > 80: short = short[:80] + "..."
            nar_alpha = min(1, (progress - 0.6) / 0.2)
            c = tuple(int(v * nar_alpha + (1-nar_alpha) * bg_v) for v, bg_v in zip(GRAY, BG_D))
            draw.text((60, 980), f"「 {short} 」", font=font_body_sm, fill=c)

    return np.array(img)


def make_chapter_frame(chapter_num: int, title: str, subtitle: str):
    """章节过渡帧"""
    img = draw_gradient_bg(VIDEO_SIZE, BG_D, (4, 8, 14))
    draw = ImageDraw.Draw(img)
    for y in range(1080):
        img.putpixel((6, y), GOLD)

    font_ch = load_font(28, True)
    font_title = load_font(56, True)
    font_sub = load_font(32)
    font_bottom = load_font(20)

    draw.text((100, 60), f"CHAPTER {chapter_num:02d}", font=font_ch, fill=GOLD)
    draw.rectangle([(0, 940), (1920, 1080)], fill=BG_L)
    draw.text((100, 380), title, font=font_title, fill=WHITE)
    if subtitle:
        draw.line([(100, 480), (500, 480)], fill=GOLD, width=2)
        draw.text((100, 510), subtitle, font=font_sub, fill=GOLD)

    return np.array(img)


def make_ending_frame():
    """结尾帧"""
    img = draw_gradient_bg(VIDEO_SIZE, BG_D, (4, 8, 14))
    draw = ImageDraw.Draw(img)
    for y in range(1080):
        img.putpixel((6, y), GOLD)

    font_main = load_font(56, True)
    font_sub = load_font(32)
    font_sm = load_font(20)

    lines = ["持续数智创新", "筑牢金融安全屏障"]
    for i, l in enumerate(lines):
        draw.text((960, 300+i*70), l, font=font_main, fill=WHITE, anchor="mt")

    draw.line([(640, 520), (1280, 520)], fill=GOLD, width=3)
    draw.text((960, 580), "金融让生活更美好", font=font_sub, fill=GOLD, anchor="mt")

    # LOGO
    draw.rectangle([(760, 680), (1160, 820)], fill=BG_L)
    font_lg = load_font(24, True)
    font_nm = load_font(40, True)
    draw.text((960, 710), "SHANGHAI BANK", font=font_lg, fill=GOLD, anchor="mt")
    draw.text((960, 750), "上海银行", font=font_nm, fill=WHITE, anchor="mt")

    draw.text((960, 920), "安全保卫部", font=font_sm, fill=DIM, anchor="mt")

    return np.array(img)


async def generate_tts(text: str, output_path: str):
    """TTS 生成旁白音频"""
    output_path = str(output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        return output_path

    import edge_tts
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+5%")
    await communicate.save(output_path)
    return output_path


def get_scene_duration(sc: dict) -> float:
    """根据时间字段计算场景时长"""
    t = sc.get('time', '')
    m = re.findall(r'(\d+):(\d+)-(\d+):(\d+)', t)
    if m:
        m1, s1, m2, s2 = map(int, m[0])
        return (m2*60+s2) - (m1*60+s1)
    return 8.0  # 默认8秒


def get_chapter_label(sc: dict) -> str:
    sec = sc.get('section', '') or ''
    ch = sc.get('chapter', '') or ''
    if '看得到' in sec: return '板块一 · 看得到'
    if '防得住' in sec: return '板块二 · 防得住'
    if '用得优' in sec: return '板块三 · 用得优'
    if '第一章' in ch or '开篇' in ch: return '开篇'
    if '第二' in ch or '规划' in ch: return '整体规划'
    if '第三' in ch or '实践' in ch: return '核心实践'
    if '第四' in ch or '总结' in ch: return '总结展望'
    return ''

# ====== 主流程 ======
async def main():
    scenes = parse_excel(f"{EXCEL_PATH}")
    print(f"📋 {len(scenes)} 个场景")

    total_scene_count = len(scenes) + 4  # scenes + 封面 + 3章节 + 结尾
    clips = []
    scene_idx = 0

    # ---- 封面 3s ----
    print("🎬 封面")
    cover_arr = make_cover_frame()
    cover_clip = VideoClip(lambda t: cover_arr, duration=3).with_fps(FPS)
    clips.append(cover_clip)
    scene_idx += 1

    def make_scene_clip(sc, label="", duration=None):
        """创建场景clip"""
        nonlocal scene_idx
        if duration is None:
            duration = get_scene_duration(sc)
        # 逐帧渲染（带进度控制文字淡入）
        def frame_fn(t):
            progress = min(1.0, t / max(duration * 0.7, 1.0))
            return make_scene_frame(sc, scene_idx, total_scene_count, progress, label)
        clip = VideoClip(frame_fn, duration=duration).with_fps(FPS)
        scene_idx += 1
        return clip

    # ---- 章节1 + 镜1-4 ----
    print("📖 Chapter 1")
    ch1_arr = make_chapter_frame(1, "开篇 · 背景与发展概况", "模拟 → 数字 → 智能 → 数智化")
    clips.append(VideoClip(lambda t: ch1_arr, duration=3).with_fps(FPS))
    scene_idx += 1

    for sc in scenes:
        if sc['num'] == 1:
            clips.append(make_scene_clip(sc, "开篇"))
        elif sc['num'] == 2:
            clips.append(make_scene_clip(sc, "开篇"))
        elif sc['num'] == 3:
            clips.append(make_scene_clip(sc, "开篇"))
        elif sc['num'] == 4:
            clips.append(make_scene_clip(sc, "开篇"))

    # ---- 章节2 + 镜5 ----
    print("📖 Chapter 2")
    ch2_arr = make_chapter_frame(2, "整体规划框架", "三大方向 ·「看得到 管得牢 用得优」")
    clips.append(VideoClip(lambda t: ch2_arr, duration=3).with_fps(FPS))
    scene_idx += 1

    for sc in scenes:
        if sc['num'] == 5:
            clips.append(make_scene_clip(sc, "整体规划"))

    # ---- 章节3 + 镜6-13 ----
    print("📖 Chapter 3")
    ch3_arr = make_chapter_frame(3, "核心实践成果", "三大板块 · 全面落地")
    clips.append(VideoClip(lambda t: ch3_arr, duration=3).with_fps(FPS))
    scene_idx += 1

    for sc in scenes:
        if 6 <= sc['num'] <= 13:
            label = get_chapter_label(sc)
            clips.append(make_scene_clip(sc, label))

    # ---- 章节4 + 镜15 ----
    print("📖 Chapter 4")
    ch4_arr = make_chapter_frame(4, "上篇 · 总结展望", "立足安防 · 拥抱AI · 服务全行")
    clips.append(VideoClip(lambda t: ch4_arr, duration=3).with_fps(FPS))
    scene_idx += 1

    for sc in scenes:
        if sc['num'] == 15:
            clips.append(make_scene_clip(sc, "总结展望"))

    # ---- 结尾 3s ----
    print("🎬 结尾")
    end_arr = make_ending_frame()
    clips.append(VideoClip(lambda t: end_arr, duration=3).with_fps(FPS))

    # ====== 生成TTS旁白 ======
    print("🔊 生成旁白...")
    tts_audio = None

    all_narration = ""
    for sc in scenes:
        nar = sc.get('narration', '')
        if nar and nar != '/':
            all_narration += nar + " "

    if all_narration.strip():
        tts_path = str(TEMP_DIR / "narration_full.mp3")
        await generate_tts(all_narration.strip(), tts_path)
        tts_audio = AudioFileClip(tts_path)

    # ====== 合成 ======
    print(f"🎞️ 合成 {len(clips)} 个片段...")

    # 添加交叉淡化
    final_clips = []
    for i, clip in enumerate(clips):
        if i == 0:
            final_clips.append(clip.with_effects([vfx.FadeIn(0.5)]))
        elif i == len(clips) - 1:
            final_clips.append(clip.with_effects([vfx.FadeOut(0.5)]))
        else:
            final_clips.append(clip.with_effects([vfx.CrossFadeIn(0.3), vfx.CrossFadeOut(0.3)]))

    video = concatenate_videoclips(final_clips, method="compose")

    # 叠加旁白音频（如果是整体配音）
    if tts_audio:
        video_duration = video.duration
        if tts_audio.duration > video_duration:
            tts_audio = tts_audio.subclipped(0, video_duration)
        video = video.with_audio(tts_audio)

    # ====== 输出 ======
    out_path = str(OUTPUT_DIR / "上海银行安防宣传片_v5.mp4")
    print(f"💾 渲染到 {out_path}...")
    video.write_videofile(
        out_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        bitrate='4000k',
        preset='medium',
        threads=4
    )

    print(f"\n✅ {out_path}")
    print(f"   {os.path.getsize(out_path)/1024/1024:.0f} MB  |  {video.duration:.0f}秒")


if __name__ == '__main__':
    asyncio.run(main())

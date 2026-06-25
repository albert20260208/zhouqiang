#!/usr/bin/env python3
"""
上海银行安防宣传片 V5 — MoviePy 视频合成 (高效版)
numpy梯度背景 · 预渲染画面 · 逐场景配旁白
"""

import openpyxl, asyncio, os, re, glob, subprocess
from pathlib import Path
from moviepy import (
    VideoClip, AudioFileClip, CompositeVideoClip, ImageClip,
    concatenate_videoclips, vfx
)
import numpy as np
from PIL import Image, ImageDraw, ImageFont

EXCEL_PATH = "/root/.openclaw/media/qqbot/downloads/20260616上海银行安防数字化探索实践短片脚本-V1_1781602866070_644fd5.xlsx"
OUTPUT_DIR = Path("/root/.openclaw/workspace/projects/security-video/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR = OUTPUT_DIR / "temp_v5"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
FRAME_DIR = TEMP_DIR / "frames"
FRAME_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1920, 1080
FPS = 24

# 品牌色
NAVY   = np.array([0, 61, 124])
GOLD   = np.array([201, 169, 110])
BG_D   = np.array([8, 12, 20])
BG_L   = np.array([13, 21, 37])
WHITE  = np.array([255, 255, 255])
LIGHT  = np.array([208, 212, 220])
GRAY   = np.array([138, 146, 162])
DIM    = np.array([85, 93, 110])

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

def load_font(size, bold=False):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def np_gradient(h, w, top, bottom):
    """numpy 渐变背景 — 向量化，快"""
    t = np.linspace(0, 1, h).reshape(h, 1, 1)
    top_a = np.array(top).reshape(1, 1, 3)
    bottom_a = np.array(bottom).reshape(1, 1, 3)
    stripe = ((1 - t) * top_a + t * bottom_a).astype(np.uint8)
    return np.tile(stripe, (1, w, 1))


def make_base_bg():
    """基础背景 — 深底 + 顶边金线"""
    bg = np_gradient(H, W, BG_D, np.array([5, 9, 15]))
    bg[2:5, :, :] = GOLD  # 顶边金线
    return bg


def draw_text_np(img, text, x, y, font, color):
    """PIL 绘制文字到 numpy 数组"""
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)
    draw.text((x, y), text, font=font, fill=tuple(int(c) for c in color))
    return np.array(pil)


def draw_line_np(img, x1, y1, x2, y2, color, width=2):
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)
    draw.line([(x1, y1), (x2, y2)], fill=tuple(int(c) for c in color), width=width)
    return np.array(pil)


def draw_rect_np(img, x1, y1, x2, y2, color, width=2):
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)
    draw.rectangle([(x1, y1), (x2, y2)], outline=tuple(int(c) for c in color), width=width)
    return np.array(pil)


def draw_filled_rect(img, x1, y1, x2, y2, color):
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)
    draw.rectangle([(x1, y1), (x2, y2)], fill=tuple(int(c) for c in color))
    return np.array(pil)


def draw_multitext(img, items):
    """一次绘制多行文字"""
    pil = Image.fromarray(img)
    draw = ImageDraw.Draw(pil)
    for text, x, y, font, color in items:
        draw.text((x, y), text, font=font, fill=tuple(int(c) for c in color))
    return np.array(pil)


# ====== 解析 ======
def parse_excel():
    wb = openpyxl.load_workbook(EXCEL_PATH)
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


def pts(text, n=5):
    if not text or text == '/': return []
    out, seen = [], set()
    for line in text.replace('<br>','\n').split('\n'):
        line = line.strip()
        if not line or '下阶段' in line: continue
        m = re.match(r'^\d+[、.]?\s*(.+)', line)
        if m: line = m.group(1)
        if len(line) > 3 and line not in seen:
            seen.add(line); out.append(line)
    return out[:n]


def split_lines(text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        test = cur + ch
        if font.getbbox(test)[2] - font.getbbox(test)[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = ch
    if cur: lines.append(cur)
    return lines


# ====== 场景帧渲染 ======
def render_cover():
    """封面 — 存为PNG"""
    bg = np_gradient(H, W, BG_D, np.array([4, 8, 14]))
    bg[:, :6, :] = GOLD  # 左侧金线
    bg[940:1080, :, :] = BG_L  # 底栏

    items = [
        ("SHANGHAI BANK", 960, 140, load_font(32, True), GOLD),
        ("上海银行", 960, 185, load_font(56, True), WHITE),
    ]
    bg = draw_multitext(bg, items)
    bg = draw_line_np(bg, 640, 280, 1280, 280, GOLD, 3)

    items2 = [
        ("安防数智化应用展示", 960, 380, load_font(64, True), WHITE),
        ("统筹发展与安全 · 筑牢金融安全防线", 960, 510, load_font(28), GOLD),
        ("上篇 · 安防数智化探索实践", 960, 960, load_font(22), GRAY),
        ("安全保卫部", 960, 1000, load_font(18), DIM),
    ]
    bg = draw_multitext(bg, items2)
    return bg


def render_chapter(num, title, subtitle):
    """章节过渡页"""
    bg = np_gradient(H, W, BG_D, np.array([4, 8, 14]))
    bg[:, :6, :] = GOLD
    bg[940:1080, :, :] = BG_L

    items = [
        (f"CHAPTER {num:02d}", 100, 60, load_font(28, True), GOLD),
        (title, 100, 380, load_font(56, True), WHITE),
    ]
    bg = draw_multitext(bg, items)
    if subtitle:
        bg = draw_line_np(bg, 100, 480, 500, 480, GOLD, 2)
        bg = draw_text_np(bg, subtitle, 100, 510, load_font(32), GOLD)
    return bg


def render_ending():
    """结尾页"""
    bg = np_gradient(H, W, BG_D, np.array([4, 8, 14]))
    bg[:, :6, :] = GOLD

    items = [
        ("持续数智创新", 960, 260, load_font(56, True), WHITE),
        ("筑牢金融安全屏障", 960, 330, load_font(56, True), WHITE),
        ("金融让生活更美好", 960, 540, load_font(32), GOLD),
    ]
    bg = draw_multitext(bg, items)
    bg = draw_line_np(bg, 640, 480, 1280, 480, GOLD, 3)

    # LOGO框
    bg = draw_filled_rect(bg, 760, 640, 1160, 780, BG_L)
    items2 = [
        ("SHANGHAI BANK", 960, 660, load_font(24, True), GOLD),
        ("上海银行", 960, 700, load_font(40, True), WHITE),
        ("安全保卫部", 960, 900, load_font(20), DIM),
    ]
    bg = draw_multitext(bg, items2)
    return bg


def render_scene_full(sc, label=""):
    """预渲染场景完整背景（不含文字动画）— 基础层"""
    bg = np_gradient(H, W, BG_D, np.array([4, 8, 14]))
    bg[2:5, :, :] = GOLD  # 顶边金线

    # 数字人占位框（右下）
    bg = draw_rect_np(bg, 1550, 800, 1860, 1020, GOLD, 2)
    bg = draw_text_np(bg, "数字人", 1705, 895, load_font(18), DIM)

    return bg


def render_scene_with_text(sc, label=""):
    """渲染场景帧（含文字）"""
    bg = render_scene_full(sc, label)

    # 章节标签（右上）
    if label:
        bg = draw_text_np(bg, label, 1850, 18, load_font(16), GOLD)

    # 标题
    subtitle = sc.get('subtitle', '')
    lines = subtitle.replace('<br>','\n').split('\n') if subtitle and subtitle != '/' else []
    main_title = ""
    for l in lines:
        l = l.strip().replace('【下阶段】','')
        if l:
            main_title = l
            break
    if not main_title:
        nar = sc.get('narration', '')
        main_title = nar.split('。')[0][:40] if nar else ""

    font_title = load_font(42, True)
    title_lines = split_lines(main_title, font_title, 1400)
    titles = [(tl, 60, 80+i*55, font_title, WHITE) for i, tl in enumerate(title_lines)]
    bg = draw_multitext(bg, titles)

    title_end = 80 + len(title_lines)*55
    bg = draw_line_np(bg, 60, title_end+15, 300, title_end+15, GOLD, 2)

    # 要点
    body_items = pts(subtitle, 5)
    if not body_items:
        nar = sc.get('narration', '')
        parts = re.split(r'[。；]', nar)
        body_items = [b.strip() for b in parts if len(b.strip()) > 5]

    font_body = load_font(24)
    y0 = title_end + 50
    text_items = []
    for i, item in enumerate(body_items[:5]):
        txt = f"▸ {item}"
        bls = split_lines(txt, font_body, 1400)
        for j, bl in enumerate(bls):
            text_items.append((bl, 70, y0 + i*55 + j*30, font_body, LIGHT))
    bg = draw_multitext(bg, text_items)

    return bg


# ====== TTS ======
async def gen_tts(text, path):
    path = str(path)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    import edge_tts
    comm = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+5%")
    await comm.save(path)
    return path


def get_duration(sc):
    t = sc.get('time', '')
    m = re.findall(r'(\d+):(\d+)-(\d+):(\d+)', t)
    if m:
        m1, s1, m2, s2 = map(int, m[0])
        return max(3, (m2*60+s2) - (m1*60+s1))
    return 8.0


def get_label(sc):
    sec = sc.get('section', '') or ''
    ch = sc.get('chapter', '') or ''
    if '看得到' in sec: return '板块一 · 看得到'
    if '防得住' in sec: return '板块二 · 防得住'
    if '用得优' in sec: return '板块三 · 用得优'
    if '第一' in ch or '开篇' in ch: return '开篇'
    if '第二' in ch or '规划' in ch: return '整体规划'
    if '第三' in ch or '实践' in ch: return '核心实践'
    if '第四' in ch or '总结' in ch: return '总结展望'
    return ''


async def main():
    scenes = parse_excel()
    print(f"📋 {len(scenes)} 个场景")

    # ====== 预渲染所有帧到PNG ======
    print("🎨 预渲染帧...")

    # 封面
    cover = render_cover()
    Image.fromarray(cover).save(str(FRAME_DIR / "00_cover.png"))

    # 章节页
    chapter_pages = [
        (1, "开篇 · 背景与发展概况", "模拟 → 数字 → 智能 → 数智化"),
        (2, "整体规划框架", "三大方向 ·「看得到 管得牢 用得优」"),
        (3, "核心实践成果", "三大板块 · 全面落地"),
        (4, "上篇 · 总结展望", "立足安防 · 拥抱AI · 服务全行"),
    ]
    for i, (num, title, sub) in enumerate(chapter_pages):
        img = render_chapter(num, title, sub)
        Image.fromarray(img).save(str(FRAME_DIR / f"ch{i+1}_chapter{num}.png"))

    # 结尾
    ending = render_ending()
    Image.fromarray(ending).save(str(FRAME_DIR / "99_ending.png"))

    # 场景页
    for sc in scenes:
        label = get_label(sc)
        img = render_scene_with_text(sc, label)
        Image.fromarray(img).save(str(FRAME_DIR / f"scene_{sc['num']:02d}.png"))
        print(f"  ✓ 镜号{sc['num']}")

    # ====== 生成TTS旁白 ======
    print("🔊 生成旁白...")
    scene_narrations = {}
    for sc in scenes:
        nar = sc.get('narration', '')
        if nar and nar != '/':
            scene_narrations[sc['num']] = nar

    # 整体旁白
    all_narration = " ".join(scene_narrations.values())
    tts_path = str(TEMP_DIR / "narration_v5.mp3")
    if all_narration.strip():
        await gen_tts(all_narration.strip(), tts_path)

    # ====== 构建视频 ======
    print("🎞️ 合成视频...")
    clips = []

    def add_img(name, dur, fade_in=0.3, fade_out=0.3):
        path = str(FRAME_DIR / name)
        clip = ImageClip(path, duration=dur)
        if fade_in > 0: clip = clip.with_effects([vfx.FadeIn(fade_in)])
        if fade_out > 0: clip = clip.with_effects([vfx.FadeOut(fade_out)])
        return clip

    # 封面 3s
    clips.append(add_img("00_cover.png", 3.0, 0.5, 0.3))

    # Ch1 + 镜1-4
    clips.append(add_img("ch1_chapter1.png", 2.5))
    for sc in scenes:
        if sc['num'] in [1,2,3,4]:
            dur = get_duration(sc)
            clips.append(add_img(f"scene_{sc['num']:02d}.png", dur))

    # Ch2 + 镜5
    clips.append(add_img("ch2_chapter2.png", 2.5))
    for sc in scenes:
        if sc['num'] == 5:
            clips.append(add_img(f"scene_05.png", get_duration(sc)))

    # Ch3 + 镜6-13
    clips.append(add_img("ch3_chapter3.png", 2.5))
    for sc in scenes:
        if 6 <= sc['num'] <= 13:
            clips.append(add_img(f"scene_{sc['num']:02d}.png", get_duration(sc)))

    # Ch4 + 镜15
    clips.append(add_img("ch4_chapter4.png", 2.5))
    for sc in scenes:
        if sc['num'] == 15:
            clips.append(add_img(f"scene_15.png", get_duration(sc)))

    # 结尾 3s
    clips.append(add_img("99_ending.png", 3.0, 0.3, 0.5))

    # 拼接
    video = concatenate_videoclips(clips, method="compose")

    # 叠加旁白
    if os.path.exists(tts_path):
        audio = AudioFileClip(tts_path)
        if audio.duration < video.duration:
            # 循环填充
            pass
        elif audio.duration > video.duration:
            audio = audio.subclipped(0, video.duration)
        video = video.with_audio(audio)

    # 输出
    out = str(OUTPUT_DIR / "上海银行安防宣传片_v5.mp4")
    print(f"💾 渲染 {out} ({video.duration:.0f}s)...")
    video.write_videofile(
        out, fps=FPS, codec='libx264', audio_codec='aac',
        bitrate='4000k', preset='fast', threads=4
    )

    size_mb = os.path.getsize(out)/1024/1024
    print(f"\n✅ {out}  |  {size_mb:.0f} MB  |  {video.duration:.0f}s")


if __name__ == '__main__':
    asyncio.run(main())

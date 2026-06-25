#!/usr/bin/env python3
"""
上海银行安防宣传片 V5 — PIL预渲染 + ffmpeg合成 (内存高效)
"""
import openpyxl, asyncio, os, re, subprocess, json
from pathlib import Path
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
NAVY   = np.array([0, 61, 124], dtype=np.uint8)
GOLD   = np.array([201, 169, 110], dtype=np.uint8)
WHITE  = np.array([255, 255, 255], dtype=np.uint8)
LIGHT  = np.array([208, 212, 220], dtype=np.uint8)
GRAY   = np.array([138, 146, 162], dtype=np.uint8)
DIM    = np.array([85, 93, 110], dtype=np.uint8)

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"

def load_font(size):
    try: return ImageFont.truetype(FONT_PATH, size)
    except: return ImageFont.load_default()

def np_gradient(h, w, top, bottom):
    t = np.linspace(0, 1, h).reshape(h, 1, 1)
    top_a = np.array(top).reshape(1, 1, 3)
    bottom_a = np.array(bottom).reshape(1, 1, 3)
    return np.tile(((1 - t) * top_a + t * bottom_a).astype(np.uint8), (1, w, 1))

def draw(pil, text, x, y, font, color, anchor=None):
    """在PIL Image上绘制文字"""
    draw = ImageDraw.Draw(pil)
    draw.text((x, y), text, font=font, fill=tuple(int(c) for c in color), anchor=anchor)

def draw_line(pil, x1, y1, x2, y2, color, width=3):
    ImageDraw.Draw(pil).line([(x1, y1), (x2, y2)], fill=tuple(int(c) for c in color), width=width)

def draw_rect(pil, x1, y1, x2, y2, color, width=2):
    ImageDraw.Draw(pil).rectangle([(x1, y1), (x2, y2)], outline=tuple(int(c) for c in color), width=width)

def get_bg():
    """基础深底背景"""
    return np_gradient(H, W, np.array([8,12,20]), np.array([5,9,15]))

# ====== 页面渲染函数 ======

def render_cover():
    bg = get_bg()
    bg[:, :6, :] = GOLD  # 左侧金线
    bg[H-140:H, :, :] = np.array([16, 24, 40], dtype=np.uint8)  # 底栏

    pil = Image.fromarray(bg)
    f_large = load_font(56)
    f_med = load_font(32)
    f_small = load_font(22)
    f_tiny = load_font(18)

    draw(pil, "SHANGHAI BANK", W//2, 140, f_med, GOLD, "ma")
    draw(pil, "上海银行", W//2, 195, f_large, WHITE, "ma")
    draw_line(pil, W//2-320, 280, W//2+320, 280, GOLD, 2)

    draw(pil, "安防数智化应用展示", W//2, 390, load_font(64), WHITE, "ma")
    draw(pil, "统筹发展与安全 · 筑牢金融安全防线", W//2, 520, load_font(28), GOLD, "ma")
    draw(pil, "上篇 · 安防数智化探索实践", W//2, H-80, f_small, GRAY, "ma")
    draw(pil, "安全保卫部", W//2, H-45, f_tiny, DIM, "ma")

    return np.array(pil)


def render_chapter(num, title, subtitle):
    bg = get_bg()
    bg[:, :6, :] = GOLD
    bg[H-140:H, :, :] = np.array([16, 24, 40], dtype=np.uint8)

    pil = Image.fromarray(bg)
    draw(pil, f"CHAPTER {num:02d}", 100, 60, load_font(28), GOLD)
    draw(pil, title, 100, 380, load_font(56), WHITE)
    if subtitle:
        draw_line(pil, 100, 480, 500, 480, GOLD, 2)
        draw(pil, subtitle, 100, 510, load_font(32), GOLD)
    return np.array(pil)


def render_ending():
    bg = get_bg()
    bg[:, :6, :] = GOLD

    pil = Image.fromarray(bg)
    draw(pil, "持续数智创新", W//2, 260, load_font(56), WHITE, "ma")
    draw(pil, "筑牢金融安全屏障", W//2, 330, load_font(56), WHITE, "ma")
    draw_line(pil, W//2-320, 480, W//2+320, 480, GOLD, 2)
    draw(pil, "金融让生活更美好", W//2, 540, load_font(32), GOLD, "ma")

    # LOGO框
    ImageDraw.Draw(pil).rectangle([(760, 640), (1160, 780)], fill=(16, 24, 40))
    draw(pil, "SHANGHAI BANK", W//2, 670, load_font(24), GOLD, "ma")
    draw(pil, "上海银行", W//2, 710, load_font(40), WHITE, "ma")
    draw(pil, "安全保卫部", W//2, 900, load_font(20), DIM, "ma")

    return np.array(pil)


def render_scene(sc, label=""):
    bg = get_bg()
    bg[2:5, :, :] = GOLD  # 顶边金线

    pil = Image.fromarray(bg)

    # 数字人占位框（右下）
    draw_rect(pil, 1550, 800, 1860, 1020, GOLD, 2)
    draw(pil, "数字人", 1705, 895, load_font(18), DIM, "ma")

    # 章节标签
    if label:
        draw(pil, label, 1900, 20, load_font(16), GOLD, "ra")

    # 标题
    subtitle = str(sc.get('subtitle', '')).replace('<br>','\n')
    lines = subtitle.split('\n')
    main_title = ""
    for l in lines:
        l = l.strip().replace('【下阶段】','')
        if l:
            main_title = l
            break
    if not main_title:
        nar = str(sc.get('narration', ''))
        main_title = nar.split('。')[0][:40] if nar else ""

    font_title = load_font(42)
    # 简单分行
    title_lines = []
    cur = ""
    for ch in main_title:
        if load_font(42).getbbox(cur + ch)[2] <= 1400:
            cur += ch
        else:
            title_lines.append(cur); cur = ch
    if cur: title_lines.append(cur)

    y = 80
    for tl in title_lines:
        draw(pil, tl, 60, y, font_title, WHITE)
        y += 55

    draw_line(pil, 60, y+10, 300, y+10, GOLD, 2)
    y += 45

    # 要点
    body_items = []
    if subtitle and subtitle != '/':
        import re as re_m
        pts = re_m.split(r'[\n；;]', subtitle)
        for p in pts:
            p = p.strip()
            m = re_m.match(r'^\d+[、.]?\s*(.+)', p)
            if m: p = m.group(1)
            if len(p) > 3 and '下阶段' not in p:
                body_items.append(p)

    font_body = load_font(24)
    for item in body_items[:4]:
        txt = f"▸ {item}"
        bl = []
        cur = ""
        for ch in txt:
            if font_body.getbbox(cur + ch)[2] <= 1400:
                cur += ch
            else:
                bl.append(cur); cur = ch
        if cur: bl.append(cur)
        for bj in bl:
            draw(pil, bj, 70, y, font_body, LIGHT)
            y += 32

    return np.array(pil)


# ====== 解析Excel ======
def parse_excel():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb['上篇']
    scenes, chap = [], ""
    for row in ws.iter_rows(values_only=True):
        vals = [str(c).strip() if c else '' for c in row[:6]]
        f = vals[0]
        if all(v == '' for v in vals[:4]): continue
        if '章节' in f: chap = f; continue
        if '板块' in f: continue
        if '部分' in f or '镜号' in f or '此篇' in f: continue
        if f.isdigit():
            scenes.append(dict(
                num=int(f), time=vals[1],
                visual=vals[2], subtitle=vals[3], narration=vals[4],
                materials=vals[5] if len(vals)>5 else '',
                chapter=chap))
    return scenes


def get_label(sc):
    sub = str(sc.get('subtitle', ''))
    if '看得到' in sub: return '板块一 · 看得到'
    if '防得住' in sub: return '板块二 · 防得住'
    if '用得优' in sub: return '板块三 · 用得优'
    ch = str(sc.get('chapter', ''))
    if '第一' in ch or '开篇' in ch: return '开篇'
    if '第二' in ch: return '整体规划'
    if '第三' in ch or '实践' in ch: return '核心实践'
    if '第四' in ch or '总结' in ch: return '总结展望'
    return ''


def get_duration(sc):
    t = str(sc.get('time', ''))
    m = re.findall(r'(\d+):(\d+)-(\d+):(\d+)', t)
    if m:
        m1, s1, m2, s2 = map(int, m[0])
        d = max(3, (m2*60+s2) - (m1*60+s1))
        return d
    return 8.0


# ====== TTS ======
async def gen_tts(text, path):
    path = str(path)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    import edge_tts
    comm = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural", rate="+5%")
    await comm.save(path)
    return path


def make_silence(path, dur):
    """生成静音WAV"""
    import struct, wave
    sr = 44100
    nsamples = int(sr * dur)
    with wave.open(path, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b'\x00' * nsamples * 4)


# ====== ffmpeg 合成 ======
def build_video_ffmpeg(segments, audio_path, out_path):
    """
    segments: list of (png_path, duration) tuples
    用 ffmpeg 合成 — 每帧转短视频clip再concat
    """
    # 方案：每个image转成带fade in/out的短clip，然后用concat demuxer拼接
    clip_files = []

    for i, (png, dur) in enumerate(segments):
        clip_out = str(TEMP_DIR / f"clip_{i:03d}.mp4")
        # 每个clip: fade in 0.5s, fade out 0.3s
        fade_frames_in = int(0.5 * FPS)
        fade_frames_out = int(0.3 * FPS)
        total_frames = int(dur * FPS)
        cmd = [
            'ffmpeg', '-y', '-loop', '1', '-i', png,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            '-t', f'{total_frames / FPS:.3f}',
            '-r', str(FPS),
            '-vf', f'fade=t=in:st=0:d=0.5,fade=t=out:st={dur-0.3:.2f}:d=0.3,fps={FPS},setpts=N/FRAME_RATE/TB',
            '-preset', 'ultrafast',
            clip_out
        ]
        subprocess.run(cmd, capture_output=True)
        clip_files.append(clip_out)

    # 生成concat list
    concat_list = str(TEMP_DIR / "concat.txt")
    with open(concat_list, 'w') as f:
        for cf in clip_files:
            f.write(f"file '{cf}'\n")

    # concat + 叠加音频
    concat_out = str(TEMP_DIR / "concat_nosound.mp4")
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_list, '-c', 'copy', concat_out
    ], capture_output=True)

    # 叠加音频
    subprocess.run([
        'ffmpeg', '-y',
        '-i', concat_out,
        '-i', audio_path,
        '-c:v', 'copy', '-c:a', 'aac',
        '-shortest', '-map', '0:v:0', '-map', '1:a:0',
        out_path
    ], capture_output=True)

    # 清理临时clip
    for cf in clip_files:
        try: os.unlink(cf)
        except: pass


async def main():
    scenes = parse_excel()
    print(f"📋 {len(scenes)} 个场景")

    # ====== 1. 渲染所有帧PNG (仅GIF关键帧) ======
    print("🎨 渲染帧 PNG...")
    segments = []  # (png_path, duration) 

    # 封面
    cover_path = str(FRAME_DIR / "00_cover.png")
    Image.fromarray(render_cover()).save(cover_path)
    segments.append((cover_path, 3.0))
    print("  ✓ 封面")

    # 章节1
    ch1_path = str(FRAME_DIR / "ch1.png")
    Image.fromarray(render_chapter(1, "开篇 · 背景与发展概况", "模拟 → 数字 → 智能 → 数智化")).save(ch1_path)
    segments.append((ch1_path, 2.5))

    # 镜1-4
    for sc in scenes:
        if sc['num'] in [1,2,3,4]:
            p = str(FRAME_DIR / f"s{sc['num']:02d}.png")
            Image.fromarray(render_scene(sc, get_label(sc))).save(p)
            segments.append((p, get_duration(sc)))

    # 章节2
    ch2_path = str(FRAME_DIR / "ch2.png")
    Image.fromarray(render_chapter(2, "整体规划框架", "三大方向 ·「看得到 管得牢 用得优」")).save(ch2_path)
    segments.append((ch2_path, 2.5))

    for sc in scenes:
        if sc['num'] == 5:
            p = str(FRAME_DIR / f"s{sc['num']:02d}.png")
            Image.fromarray(render_scene(sc, get_label(sc))).save(p)
            segments.append((p, get_duration(sc)))

    # 章节3
    ch3_path = str(FRAME_DIR / "ch3.png")
    Image.fromarray(render_chapter(3, "核心实践成果", "三大板块 · 全面落地")).save(ch3_path)
    segments.append((ch3_path, 2.5))

    for sc in scenes:
        if 6 <= sc['num'] <= 13:
            p = str(FRAME_DIR / f"s{sc['num']:02d}.png")
            Image.fromarray(render_scene(sc, get_label(sc))).save(p)
            segments.append((p, get_duration(sc)))

    # 章节4
    ch4_path = str(FRAME_DIR / "ch4.png")
    Image.fromarray(render_chapter(4, "上篇 · 总结展望", "立足安防 · 拥抱AI · 服务全行")).save(ch4_path)
    segments.append((ch4_path, 2.5))

    for sc in scenes:
        if sc['num'] == 15:
            p = str(FRAME_DIR / f"s{sc['num']:02d}.png")
            Image.fromarray(render_scene(sc, get_label(sc))).save(p)
            segments.append((p, get_duration(sc)))

    # 结尾
    end_path = str(FRAME_DIR / "99_end.png")
    Image.fromarray(render_ending()).save(end_path)
    segments.append((end_path, 3.0))
    print("  ✓ 结尾")

    total_dur = sum(s[1] for s in segments)
    print(f"  总时长: {total_dur:.0f}s  |  {len(segments)} 个片段")

    # ====== 2. TTS 旁白 ======
    print("🔊 生成旁白...")
    all_narration = ""
    for sc in scenes:
        nar = str(sc.get('narration', ''))
        if nar and nar != '/':
            all_narration += nar + " "

    tts_path = str(TEMP_DIR / "narration_v5.mp3")
    if all_narration.strip():
        await gen_tts(all_narration.strip(), tts_path)

    # ====== 3. ffmpeg 合成 ======
    print("🎞️ ffmpeg 合成视频...")
    out_path = str(OUTPUT_DIR / "上海银行安防宣传片_v5.mp4")

    # 直接使用 ffmpeg concat + xfade 方案
    # 方法: 每个image用 image2 demuxer 生成短clip，一次性concat
    build_video_ffmpeg(segments, tts_path, out_path)

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"\n✅ {out_path}  |  {size_mb:.0f} MB  |  {total_dur:.0f}s")


if __name__ == '__main__':
    asyncio.run(main())

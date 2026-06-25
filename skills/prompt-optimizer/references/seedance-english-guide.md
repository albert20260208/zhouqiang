# Seedance 英文提示词指南

## @ 引用系统 (英文版)

### 文件引用格式
```
@Image1    @Image2    @Image3   ...  (最多9张图片)
@Video1    @Video2    @Video3       (最多3个视频)
@Audio1    @Audio2    @Audio3       (最多3个音频)
总计: ≤12个文件
```

### 角色分配表 (英文)

| 用途 | 语法示例 | 中文对应 |
|------|----------|----------|
| First frame | `@Image1 as the first frame` | @Image1 作为首帧 |
| Last frame | `@Image2 as the last frame` | @Image2 作为尾帧 |
| Character | `@Image1's character as the subject` | @Image1 的人物作为主体 |
| Scene | `scene references @Image3` | 场景参考 @Image3 |
| Camera movement | `reference @Video1's camera movement` | 参考 @Video1 的运镜 |
| Action choreography | `reference @Video1's action choreography` | 参考 @Video1 的动作编排 |
| Visual effects | `completely reference @Video1's effects` | 完全参考 @Video1 的特效 |
| BGM | `BGM references @Audio1` | BGM 参考 @Audio1 |
| Clothing | `wearing @Image2's clothing` | 穿着 @Image2 的服装 |

### 组合引用示例
```
@Image1's character as the subject, 
reference @Video1's camera movement and action choreography,
BGM references @Audio1, 
scene references @Image2
```

## 10个场景模板 (英文)

### 1. Character Consistency - 人物一致性
```
@Image1's character, [action description], [scene description].
Camera [camera movement]. [Emotion/expression change].
```

### 2. Camera Movement Replication - 运镜复刻
```
Reference @Image1's character. Completely reference @Video1's camera movement.
[Scene description]. [Action description].
```

### 3. Creative Template - 特效复刻
```
Replace @Video1's character with @Image1. @Image1 as the first frame.
Completely reference @Video1's transition effects and visual style.
[Scene switching description]
```

### 4. Video Extension - 视频延长
```
Extend @Video1 by [X] seconds.
1-5 seconds: [Continuation description]
6-10 seconds: [Development description]
```

### 5. Video Editing - 视频编辑
```
Subvert @Video1's plot — [new plot direction]
```

### 6. Music Beat-Matching - 音乐卡点
```
@Image1 @Image2 @Image3...
Reference @Video1's visual rhythm and music beats for beat-matching editing.
Character movements more dynamic, overall style more dreamy.
```

### 7. Dialogue and Voice Acting - 对白配音
```
[Character description] facing the camera, [expression/action].
Dialogue: "[line content]"
Background: [scene description]
```

### 8. One-Take - 一镜到底
```
One-take follow shot, from [starting point] through [path],
finally reaching [end point]. No cuts throughout.
```

### 9. E-commerce - 电商展示
```
Static shot. [Product] floating and rotating.
[Product disassembly/assembly action description]
Maintain the ultimate beauty of [product characteristics].
```

### 10. Educational - 科普教育
```
[X]-second health science short video.
0-5 seconds: [Visualization description 1]
5-10 seconds: [Visualization description 2]
10-15 seconds: [Comparison/summary]
Overall tone [description].
```

## 英文提示词结构

### 基本公式
```
[Subject/Character] + [Scene/Environment] + [Action/Movement] + 
[Camera Movement] + [Time Segmentation] + [Transition/Effects] + 
[Audio/Sound] + [Style/Atmosphere]
```

### 结构化模板
```
【Scene】Environment description
【Character】Role + action
【Camera】Camera movement method
【Style】Director style reference
【Color & Lighting】Tone + lighting effects
【Texture】Rendering method
```

### 时间分段 (10秒以上推荐)
```
0-3 seconds: [Opening description, camera, action]
3-6 seconds: [Mid-section development]
6-10 seconds: [Climax or key action]
10-15 seconds: [Ending, brand reveal]
```

## 参数格式 (英文)

### 基础参数
```
--resolution 1080p    # Resolution
--duration 5          # Duration (seconds)
--camerafixed false   # Whether camera is fixed
--watermark true      # Watermark
```

### 高级参数
```
--style cinematic     # Visual style
--lighting golden_hour # Lighting condition
--color_palette warm  # Color palette
--framerate 24        # Frame rate
```

## 风格关键词 (英文)

### 视觉风格
- `cinematic quality, film grain, shallow depth of field`
- `2.35:1 widescreen, 24fps`
- `ink painting style` / `anime style` / `realistic style`
- `high saturation neon colors, warm-cool contrast`
- `4K quality` / `8K ultra HD` / `HD high definition`
- `cyberpunk` / `sci-fi` / `fantasy`

### 光线效果
- `natural lighting` / `Natural lighting`
- `golden hour` / `Golden hour`
- `neon lights` / `Neon lights`
- `backlit` / `Backlit`
- `Rembrandt lighting`
- `ray tracing` / `volumetric lighting`

### 氛围关键词
- `tense suspense` / `warm healing` / `epic grandeur`
- `comedy exaggerated expressions`
- `documentary style, restrained narration`
- `Wong Kar-wai style: step-printing jumps, neon colors`

## 导演风格提示词 (英文)

### Hitchcock Style
```
Hitchcock style:
- Subjective POV shots
- Slow push-in creating oppression
- Strong shadow and light contrast
- Close-ups of character expressions conveying fear
```

### Kubrick Style
```
Kubrick style:
- Perfect symmetrical composition
- One-point perspective converging to center
- Wide-angle lens emphasizing space
- Cool tones, geometric lines
```

### Wong Kar-wai Style
```
Wong Kar-wai style:
- Step-printing jumpiness, discontinuous motion
- Neon colors, strong warm-cool contrast
- Slow motion close-ups
- Urban night scenes, glass reflections
```

### Nolan Style
```
Nolan style:
- Grand scenes, IMAX aspect ratio
- Practical effects, real explosions
- Visualized time folding
- Low bass vibration, tense soundtrack
```

## 常见错误避免 (英文)

### ❌ 避免的问题

1. **Vague references** - Don't just say "reference @Video1", specify what to reference
   - ❌ "reference @Video1"
   - ✅ "reference @Video1's camera movement and action choreography"

2. **Conflicting instructions** - Don't request contradictory effects simultaneously
   - ❌ "static shot" + "orbiting shot"
   - ❌ "camera fixed" + "push-in close-up"

3. **Content overload** - Don't cram too many scenes into short videos
   - ❌ 5-second video contains 5 scene transitions
   - ✅ 5-second video focuses on 1-2 scenes

4. **Ignoring audio** - Sound effects greatly enhance the effect
   - ✅ Include BGM description, sound effect description

5. **Real human faces** - The system will intercept real face materials
   - ❌ Upload real person photos
   - ✅ Use illustrations/3D characters

6. **Ignoring proportions** - Not paying attention to height in multi-person scenes
   - ❌ Don't write character proportions, protagonist may become giant
   - ✅ "protagonist's height proportional to surrounding characters"

## 优秀示例 (英文)

### Example 1: Jarvis Appearance
```
【Scene】
Future cyberpunk city night scene, neon skyscrapers stand tall
Exactly the same as the reference image

【Character】
Jarvis, 25-year-old Asian male, dark blue tech jacket
Height proportional to surrounding pedestrians

【Camera】
Opening: Ground-level aerial shot of street
Camera quickly tilts upward and bursts upward like a rocket
Sweeping past building sides, neon signs flashing
Rising faster and faster, rushing toward rooftop
Finally slowing to定格: Back view overlooking city

【Wong Kar-wai Style】
Step-printing jumpiness, neon color flow
High contrast光影, film grain texture

--duration 5 --camerafixed false --watermark false
```

### Example 2: Orange Cat
```
A cute orange cat napping on a sunny windowsill,
camera slowly pushes in,
warm afternoon light,
cinematic quality, 4K quality
```

### Example 3: AI Birth
```
In the digital world, countless light points converge into a glowing AI consciousness,
code flying like meteors,
neural network nodes闪烁连接,
an intelligent assistant正在诞生,
sci-fi style, blue neon光芒, movie质感
```

## 使用建议

### 1. 保持一致性
- 在同一项目中使用相同的术语风格
- 保持参数格式统一
- 使用相同的导演风格关键词

### 2. 逐步优化
- 从简单提示词开始
- 根据生成结果逐步添加细节
- 保留有效的关键词组合

### 3. 文化适应
- 注意中英文表达差异
- 确保文化概念正确传达
- 必要时添加文化背景说明

---

_来源: prompt-knowledge-merged-20260328.md Seedance英文提示词指南部分_
_整合时间: 2026-03-30_
_状态: ✅ 新增内容_
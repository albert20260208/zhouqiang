# Seedance 2.0 官方提示词指南 — 全网资料聚合

> 来源：官方指南 + GitHub结构化提示词库 + imagine.art 70个实战模板 + 社区经验
> 整理时间：2026-04-24 22:00

---

## 一、核心公式（6步结构）

```
【主体】+【动作】+【环境】+【运镜】+【风格】+【约束】
```

| 步骤 | 要素 | 要求 | 示例 |
|------|------|------|------|
| 1.主体 | 谁/什么 | 具体视觉特征优先 | "一个穿白裙的年轻女子" |
| 2.动作 | 做什么 | 使用具体动词，量化强度 | "缓慢转身，风吹动裙摆" |
| 3.环境 | 在哪里 | 包含光线和氛围 | "在海边黄昏，金色光芒" |
| 4.运镜 | 怎么拍 | 只用1个主要运镜指令 | "镜头缓慢推近" |
| 5.风格 | 什么感觉 | 具体视觉参考 | "电影级质感，35mm胶片" |
| 6.约束 | 避免什么 | 排除常见问题 | "避免抖动和肢体扭曲" |

**完整示例（好的）：**
```
A skateboarder lands a clean trick in an empty dawn parking lot,
camera low tracking shot then subtle rise, modern cinematic contrast,
6 seconds, 16:9, avoid jitter and bent limbs.
```

**不好的：**
```
cool skateboard video, cinematic, fast, amazing tricks, lots of movement, epic style
```
→ 全是模糊形容词，没有具体指令

---

## 二、8种运镜方式（最高杠杆技巧）

| 运镜 | 英文术语 | 效果 | 最佳用途 |
|------|---------|------|---------|
| 推近 | push-in / dolly in | 镜头缓慢移向主体 | 特写强调，情感聚焦 |
| 拉远 | pull-out / dolly out | 镜头拉远展示全景 | 环境揭示，空间语境 |
| 平移 | lateral motion / pan | 镜头水平移动 | 追踪主体，扫描场景 |
| 跟拍 | tracking shot / follow | 镜头跟随主体运动 | 动作场景，行走角色 |
| 环绕 | orbit / arc | 镜头绕主体旋转 | 产品展示，角色肖像 |
| 航拍 | aerial / drone shot | 高空或鸟瞰视角 | 景观，城市，宏大场面 |
| 手持 | handheld | 模拟自然轻微晃动 | 纪录片风格，真实感 |
| 固定 | fixed / locked-off | 镜头完全静止 | 聚焦主体动作 |

### 运镜核心规则

**规则1：只用1个主要运镜指令**
- ✅ `camera slow push-in`
- ❌ `push-in, then pan left, zoom out, orbit around`
- 多个矛盾指令会导致抖动或脱帧

**规则2：用节奏描述，不用技术参数**
- ✅ `slow, smooth, stable, gradual, gentle`
- ❌ `24fps, f/2.8, ISO 800, 85mm focal length`

**规则3：分离主体运动和镜头运动**
- ✅ `The dancer spins slowly. Camera holds fixed framing.`
- ❌ `spinning camera around a dancing person`
- 混在一起是最常见错误，导致画面失控

### 速度关键词表

| 速度 | 关键词 | 效果 |
|------|--------|------|
| 极慢 | imperceptible, barely | 几乎注意不到的运动 |
| 慢 | slow, gentle, gradual | 平稳顺滑运动 |
| 中 | smooth, controlled | 自然运动节奏 |
| 快 | dynamic, swift | 高冲击（慎用） |

**⚠️ 重要警告**："Fast"是最容易降低视频质量的关键词。快速运镜+快速剪辑+复杂场景几乎必然导致抖动伪影。使用时只选一个要素设为Fast。

---

## 三、风格关键词与光线（最高杠杆）

### 风格关键词

| 类别 | 关键词 | 效果 |
|------|--------|------|
| 电影感 | cinematic, film tone, 35mm | 经典电影质感 |
| 画质 | 4K, high detail, sharp | 高清细节 |
| 胶片 | film grain, analog, vintage | 复古纹理 |
| 色调 | warm tone, cool palette, desaturated | 色彩倾向 |
| 氛围 | moody, dreamy, ethereal | 情绪氛围 |
| 写实 | realistic, natural, documentary | 真实风格 |

### 光线：提示词中最高杠杆元素

官方强调：在提示词中加一行光线描述，比加十个形容词都有效。

| 光线 | 效果 | 示例用法 |
|------|------|---------|
| golden hour | 暖金色时刻光线 | "soft golden hour lighting" |
| rim light | 勾勒主体边缘 | "dramatic rim light against dark bg" |
| natural light | 自然光照 | "soft natural window light" |
| neon | 霓虹光芒 | "neon-lit rainy street" |
| backlit | 背光 | "backlit silhouette at sunset" |
| overcast | 柔和漫射光 | "even overcast diffused light" |

**💡 秘诀**：只能加一个要素的话，选光线。「一个人走路」和「一个人走在柔和金色黄昏中」差距巨大。

---

## 四、负面提示词（禁忌词清单）

### 4.1 推荐写在约束段的负面词

| 负面提示 | 排除什么 | 使用场景 |
|---------|---------|---------|
| avoid jitter | 画面抖动 | 所有视频 |
| avoid bent limbs | 肢体扭曲 | 角色视频 |
| avoid temporal flicker | 时间闪烁 | 长时长视频 |
| avoid identity drift | 主体特征漂移 | 角色一致性 |
| avoid chaotic composition | 杂乱构图 | 复杂场景 |

### 4.2 降低质量的危险关键词

| 危险词 | 为什么危险 | 替代方案 |
|--------|-----------|---------|
| fast (不加限定) | 导致全面混乱 | 只选1个要素设fast |
| cinematic (单独用) | 太模糊，缺指导 | "cinematic film tone, 35mm, warm" |
| epic | 模型不知道什么意思 | 描述具体视觉效果 |
| amazing/beautiful | 形容词缺乏实际指导 | 用具体光线和构图 |
| lots of movement | 太多运动导致抖动 | 描述具体的单一动作 |

### 4.3 中文常见问题替换

| ❌ 不要这样写 | ✅ 改成这样 |
|-------------|------------|
| 快速运动/快速切换 | 描述单一具体动作+速度词 |
| 电影感/大片质感 | 35mm胶片色调+光线描述 |
| 好看/漂亮/惊艳 | 暖色调+逆光+高分辨率 |
| 激烈的打斗 | 中景+固定镜头+武器碰撞特写 |
| 很多特效 | 具体描述特效链（聚能→释放→残留） |

---

## 五、三种生成模式的提示词差异

### 文生视频（T2V）
- 用6步公式完整描述视频内容
- 需详细描述主体外貌和场景

```
A lone astronaut walks across an amber desert under
twin moons, camera slow lateral tracking, cinematic
sci-fi tone, 8 seconds, 16:9, avoid temporal flicker.
```

### 图生视频（I2V）
- 已有参考图，提示词只需描述运动和变化
- **必须包含** "preserve composition and colors"

```
Animate the provided image, preserve composition and
colors, add gentle wind motion to the leaves, camera
slowly pushes in, keep consistent lighting, 6 seconds.
```

| 要素 | 文生视频 | 图生视频 |
|------|---------|---------|
| 主体描述 | 必须详细 | 已由图提供，可省略 |
| 运动描述 | 完整描述 | 聚焦动态变化 |
| 构图保留 | 不适用 | 必须强调"preserve" |
| 运镜 | 灵活 | 须与图像构图对齐 |

### 视频生视频（V2V）
- 用参考视频，提示词描述风格转换

```
Transform source clip to anime watercolor style,
preserve core motion and timing, adjust color palette
to pastel, keep identity consistent, avoid identity drift.
```

---

## 六、GitHub结构化提示词系统（中文社区精华）

### 6.1 系统核心理念

**Seedance 2.0 的智能前提：**
- ✅ 有智能 — 具备导演思维，自动编排分镜
- ✅ 有知识 — 自带世界知识，无需百科全书式描述
- ✅ 全能参考 — 支持图片≤9张、视频≤3个、音频≤3个同时参考

### 6.2 一句话生成原则

满足以下条件时，一句话即可：
- ✅ 有世界知识（餐饮品牌/健身动作/历史时期等）
- ✅ 不需要特定角色一致性
- ✅ 不需要特殊运镜风格

示例：
- "生产一个精美高级的兰州拉面广告，注意分镜编排"
- "帮我生成一个讲述无印良品这个品牌的宣传片"

### 6.3 标准结构化公式

```
【风格】_____风格，_____秒，_____比例，_____氛围

【时间轴】
0-X秒：[镜头] + [画面] + [动作] + [特效]
X-Y秒：[镜头] + [画面] + [动作] + [特效]
...

【声音】_____配乐 + _____音效 + _____对白

【参考】@图片1 _____，@视频1 _____
```

### 6.4 @引用系统

```
@图片1 作为首帧
@图片2 作为尾帧
@图片3 作为角色形象参考
@图片4-6 作为场景参考
@视频1 参考运镜方式
@视频2 参考动作节奏
@音频1 用于配乐
@音频2 用于对白参考
```

### 6.5 中文平台实测限制

| 项目 | 限制 |
|------|------|
| 真人脸部素材 | ❌ 不支持（写实真人脸会拦截）|
| 文件总数 | 最多12个（图片≤9+视频≤3+音频≤3）|
| 视频总时长 | ≤15秒 |
| 音频格式 | 仅支持MP3 |
| 生成分辨率 | 目前720P为主 |

---

## 七、关键词避坑（中文特供版）

### 7.1 模型自带世界知识，不要过度描述

✅ 推荐：生成一个精美高级的兰州拉面广告，注意分镜编排
❌ 不推荐：描述如何揉面、拉面、浇汤的每个步骤细节

### 7.2 知名角色处理（避免被拒）

- ❌ 不要直接写角色名字（孙悟空、路飞等）
- ✅ 使用 "Figure 1"、"Figure 2" 替代
- ✅ 描述外观特征（"穿橙色衣服戴草帽的少年"）

### 7.3 打斗场景核心提示

```
角色1与角色2在[场景]中进行对战
使用@视频1中的动作节奏
使用@视频1中的镜头运动
```

---

## 八、迭代测试方法论（官方推荐）

### 一次只改一个变量

多次生成，每次只改一个维度：
1. 第一版：调光线
2. 第二版：调运镜
3. 第三版：调风格

秘诀：同时改三个东西，你永远不知道是哪个变量产生了差异。

### 三级模板管理

| 层级 | 用途 | 特征 |
|------|------|------|
| Starter | 快速验证方向 | 短而精确 |
| Production | 正式交付 | 严格的运镜和一致性约束 |
| Fallback | 不稳定时降级 | 极度简化，回归基础 |

### 输出前六连问

- [ ] 通读全文，以非作者视角看
- [ ] 去掉冗余形容词
- [ ] 确认只有1个主要运镜指令
- [ ] 确保约束条件在后期可执行
- [ ] 检查风格和动态指令是否冲突
- [ ] 是否可用一句话表达核心？有世界知识就别啰嗦

---

## 九、推荐学习资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 即梦官网 | https://jimeng.jianying.com | 全量上线 |
| 小云雀 | https://xyq.jianying.com | App下载，开放所有用户 |
| GitHub结构化提示词库 | https://github.com/liangdabiao/make-prompt-seedance2 | 16+模板，中文完整版 |
| Seedance2Prompt社区库 | https://www.seedance2prompt.com | 815个实战提示词 |
| imagine.art 70个模板 | https://www.imagine.art/blogs/seedance-2-0-prompt-guide | 分14类，英 |
| 官方提示词深度解读（英） | https://help.apiyi.com/en/seedance-2-0-prompt-guide... | 6步公式+8运镜+避坑 |
| 即梦Seedance 2.0使用手册 | https://seed.bytedance.com/zh/seedance2_0 | 含参考视频和完整指南 |
| B站30集保姆级教程 | https://www.bilibili.com/video/BV1gEfcBKEYR/ | 从入门到多主体一致性 |

---

## 十、与胡导风格（Vidu）的关键差异

| 维度 | Seedance 2.0 | Vidu（胡导风格） |
|------|-------------|-----------------|
| 运镜 | 支持推拉摇移跟环绕（但避免摇镜） | 全部固定镜头 |
| 时长 | 4-15秒，支持长镜头 | 15秒，快节奏切镜 |
| 画幅 | 16:9/9:16/2.35:1 | 16:9为主 |
| @引用 | 支持图片≤9+视频≤3+音频≤3 | 参考图即可 |
| 运动镜头 | 能跑，但fast容易崩 | 不写运动镜头 |
| 约束段 | 可加avoid jitter等 | 不加负面提示词（郑有朋偏好）|
| 分镜写作 | 时间轴分段（0-X秒） | 镜头N（X-Y秒）结构 |
| 对话处理 | 直接用自然语言描述 | 台词标注在内容中 |

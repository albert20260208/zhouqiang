# 场景质感增强技能

> **创建日期**：2026-06-26
> **来源**：全网搜索（Seedance官方/即梦实战/Midjourney/阿里云/通义万相/Reddit）+ 摄影/建筑可视化领域知识整合
> **用途**：为 Seedance 视频提示词提供系统化的场景（建筑/自然/室内/光影/天气/地面）质感、真实性、美观性增强方案
> **与现有体系关系**：本技能与 `人物服装增强技能` 互补——后者管人物，本技能管场景。场景描述写入提示词【场景】段或分镜内容中

---

## 一、概述

### 问题诊断

AI 生成的场景常见问题：
| 问题 | 根因 | 解决方向 |
|------|------|---------|
| 场景像游戏贴图 | 材质表面太光滑，无纹理细节 | 加材质纹理/磨损/凹凸/ambient occlusion |
| 光影扁平无层次 | 默认均匀光照，无体积感 | 加体积光/god rays/阴影层次/环境光遮蔽 |
| 远景糊成一片 | 无大气透视和景深 | 加 atmospheric haze/DOF/远景色彩衰减 |
| 自然元素重复规律化 | 模型偏好在规则图案 | 加"随机分布/不规则排列/自然形态" |
| 室内像样板间 | 完美无使用痕迹 | 加生活痕迹/自然落灰/使用磨损 |
| 天空/水/云假 | 色块化、边缘硬 | 加云层体积/水面反射折射/天空渐变 |

### 核心原则

**场景的真实感 = 材质纹理 × 光影层次 × 细节不完美。** 三个维度缺一个就一眼假。

---

## 二、场景类型增强模块

### 🏛️ 模块一：建筑/Architecture

#### 古建筑/中式建筑
```
汉白玉石基表面微颗粒纹理，石材自然风化微裂纹，石阶边缘自然磨损圆滑，
红色漆柱表面微细龟裂纹理，漆面哑光非镜面反光，柱身岁月包浆微泛哑光，
琉璃瓦逐片独立反光而非均匀一片，瓦片间缝隙阴影可见，
斗拱木构榫卯接缝清晰，木材表面纵向纹理和节疤可见，
檐下阴影区 ambient occlusion 加深形成纵深层次。
```
- 追加关键词：`weathered stone surface`, `aged wood grain`, `roof tile individual specular highlights`, `mortise and tenon joint detail`, `architectural patina`

#### 现代建筑/金属玻璃
```
玻璃幕墙反射天空云层而非纯镜面，玻璃非均匀微扭曲反射，
金属框架哑光喷砂质感，焊点/铆钉独立微反光，
混凝土表面细微气孔纹理，模板木纹印痕隐约可见，
不锈钢扶手表面拉丝纹理单向反光，边缘圆角倒边非锐利。
```
- 追加关键词：`brushed metal directional grain`, `glass non-uniform reflection`, `concrete micro-porosity`, `architectural material contrast`

#### 废墟/古堡
```
石砖风化边缘不规则剥落，砖缝青苔自然分布非均匀，
拱门石材承重沉降微裂缝，铁质构件锈蚀氧化橘红斑点，
灰尘在光束中自然悬浮，cobweb in dark corners with dust,
断裂石材断面粗糙纹理，fresh break vs weathered surface 对比。
```
- 追加关键词：`stone erosion weathering`, `natural moss distribution on brick`, `iron rust oxidation patina`, `dust motes in light beams`

#### 雕塑/雕像
```
石雕表面凿痕纹理走向可见，不同打磨程度区域光泽对比，
金属雕像铜绿自然氧化斑，接缝铸造线隐约可见，
大理石雕像次表面散射微透光，表面蜡质柔和反光，
基座石材与雕像材质纹理对比分明。
```

#### 建筑材料通用增强词库

| 材质 | 中文增强 | 英文关键词 |
|------|---------|-----------|
| 石材 | 表面微颗粒纹理，自然风化，接缝阴影 | `stone grain texture`, `natural weathering`, `mortar joint shadow` |
| 木材 | 纵向纹理，节疤，哑光漆面 | `wood grain direction`, `knot detail`, `matte varnish` |
| 金属 | 拉丝纹理，铆钉反光，氧化 | `brushed metal grain`, `rivet highlight`, `oxidation patina` |
| 玻璃 | 非均匀反射，微扭曲，边缘绿边 | `non-uniform glass reflection`, `edge refraction` |
| 混凝土 | 气孔纹理，模板印痕，色差 | `concrete porosity`, `formwork imprint`, `color variation` |
| 砖/瓦 | 表面粗糙微凹凸，砖缝砂浆纹理 | `brick surface roughness`, `mortar joint texture` |
| 琉璃/釉面 | 局部高光非均匀，釉面微气泡 | `glaze specular hotspot`, `micro bubble in glaze` |

---

### 🌿 模块二：自然/Nature

#### 树木/植物
```
树干表皮粗糙纵向裂纹纹理，树皮分层剥落细节，
树叶非均匀分布，不同朝向叶片受光/背光色差，
林间光束 Tyndall effect 穿过枝叶缝隙形成可见光柱，
前景叶片微模糊景深虚化，中景叶片锐利纹理可见，
枝干分叉处节疤纹理，苔藓在树干北面自然附生。
```
- 追加关键词：`bark texture with deep crevices`, `leaves light direction color variation`, `Tyndall effect forest beams`, `branching natural asymmetry`

#### 草地/植被
```
草叶非均匀高度和朝向，不同草种颜色微差，
草叶边缘逆光微透亮半透明绿色，叶脉纹理可见，
地面枯黄草叶混合绿色形成自然色差，
踩踏处草地自然倒伏形成路径痕迹，
草地表面昆虫微距可见而非光秃一片。
```
- 追加关键词：`grass blade height variation`, `backlit grass edge translucency`, `natural color mix green and dry`, `vegetation irregular distribution`

#### 花卉
```
花瓣表面微绒纹理/蜡质光泽按花种区分，
花瓣边缘自然微卷非完美几何形状，
花蕊花粉颗粒可见，不同开放度花苞并存，
花茎绒毛/刺节纹理可见，叶片虫咬洞自然不规则。
```
- 追加关键词：`petal surface micro-texture`, `stamen pollen granules visible`, `natural petal edge irregularity`, `leaf insect damage marks`

#### 水
```
水面微波形成非均匀反射，波谷反射天空波峰反射环境，
水质微浑浊悬浮颗粒而非纯净透明，
溪流/瀑布 white water 泡沫细节而非均匀白块，
水下岩石折射扭曲变形，水面边缘与岸石交界处湿润变深色，
清澈水面下可见水底鹅卵石折射偏移，水深色渐变由浅绿到深墨绿。
```
- 追加关键词：`water surface micro-ripple non-uniform reflection`, `suspended particles in water`, `white water foam detail`, `underwater refraction distortion`, `wet edge color darkening`

#### 天空/云
```
云层体积感三维立体而非平面贴图，云边缘柔软羽状渐变，
不同高度云层（低积云/高卷云）共存形成深度，
蓝天色彩从头顶深蓝到地平线浅白渐变，
雷电云内部闪电照亮云体而非边缘发光，
日落云层底部暖橙色到顶部冷紫色渐变自然。
```
- 追加关键词：`volumetric cloud 3D structure`, `cloud edge soft feather gradient`, `atmospheric sky color gradient zenith to horizon`, `multi-layer cloud depth`

#### 山脉/地形
```
远山 atmospheric haze 随距离递增色彩衰减变为蓝灰，
岩石层理走向可见，不同岩层颜色差异，
山体植被覆盖线自然过渡（从山脚密林到山顶裸露岩石），
悬崖断面碎石堆积锥形自然角度，崩塌面新鲜与风化面对比，
雪线自然不规则，非完美均匀覆盖。
```
- 追加关键词：`atmospheric haze distance gradient`, `rock strata visible layers`, `vegetation line natural transition`, `talus slope natural angle`

---

### 🏠 模块三：室内/Interior

#### 墙面/地面
```
墙面微凹凸纹理非平滑平面，涂料滚筒刷痕/墙纸接缝可见，
踢脚线与墙面/地面交界处自然阴影缝隙，
木地板每块颜色微差，木纹纹理走向各有不同，
地板自然磨损区域（走道/椅子拖拽痕迹）光泽差异，
地毯纤维粗细可见，踩踏区域压痕。
```
- 追加关键词：`wall micro-texture brush marks`, `baseboard gap shadow`, `floorboard individual grain variation`, `floor wear pattern`

#### 家具
```
木质家具表面天然木纹，不同角度反光差异，
布艺沙发面料编织纹理可见，坐垫使用凹陷自然形态，
皮质家具表面毛孔纹理，折痕处自然磨损光泽，
金属五金件拉丝或镜面按类型区分，螺丝孔位可见。
```
- 追加关键词：`furniture wood open grain`, `fabric weave on upholstery`, `leather pore texture`, `natural use patina`

#### 道具/摆件
```
瓷器釉面微气泡/开片龟裂纹，非完美工厂新品，
书籍封皮微磨损边角，书页自然泛黄渐变，
金属器皿表面使用划痕微反光，底部接触面磨损，
植物叶片自然朝向光源非均匀生长，
玻璃器皿边缘绿色折射，表面轻微指纹或灰尘。
```
- 追加关键词：`ceramic glaze crackle pattern`, `book edge natural wear`, `prop surface aging`, `glass rim green tint refraction`

#### 织物/窗帘
```
窗帘面料编织经纬纹理可见，褶皱自然重力垂坠，
窗帘边缘自然不规则微卷，透光区域薄纱半透渐变，
地毯穗边自然散开不规则，织物表面起毛球使用痕迹，
不同面料（棉/麻/丝/绒）光泽和纹理区分明显。
```
- 追加关键词：`curtain fabric weave visible`, `natural drape gravity fold`, `sheer fabric light transmission gradient`, `textile material contrast`

---

### 💡 模块四：光影与大气/Lighting & Atmosphere

#### 体积光/God Rays
```
体积光穿过窗口/枝叶/建筑缝隙形成可见光柱，
光柱中悬浮微尘粒子自然分布非均匀，
光束边缘柔软渐变非硬边界，
体积光强度在路径上逐渐衰减符合物理平方反比定律。
```
- 追加关键词：`volumetric light beams`, `dust particles in light shaft`, `god ray soft edge gradient`, `light falloff over distance`

#### 环境光遮蔽/Ambient Occlusion
```
物体接触面阴影加深（墙角/家具底部/缝隙），
AO 阴影不是死黑而是环境色微染，
折叠处/凹角/叠合处自然阴影渐变而非硬线，
远景大气散射使阴影变为偏蓝灰色。
```
- 追加关键词：`ambient occlusion contact shadows`, `crevice shadow depth gradient`, `shadow tinted by environment color`

#### 大气透视/Haze
```
远景色彩饱和度随距离递减，远景对比度降低，
山间薄雾分层非均匀飘动，雾层底部密度大顶部稀薄，
城市远景 haze 偏暖灰，自然远景 haze 偏蓝灰，
黄昏时段 haze 被夕阳染成暖金色。
```
- 追加关键词：`atmospheric perspective color desaturation`, `haze density vertical gradient`, `distance haze warm/cool shift`, `golden hour haze tint`

#### 特殊光影
```
烛光/火光：暖橙色非均匀跳动光照，光源周围热浪微扭曲空气，
闪电：瞬间冷白高光，阴影锐利，后续环境残影余晖，
月光：冷蓝银白漫射，高对比阴影，场景偏蓝调，
霓虹灯：彩色光在潮湿地面形成倒影，光晕扩散柔和，
逆光：主体轮廓 rim light 金边，前景略暗保留细节。
```
- 追加关键词：`candlelight flicker warm orange`, `lightning harsh shadow sharp`, `moonlight cool blue silver diffusion`, `neon light ground reflection`, `rim light golden edge`

#### 电影级光影增强通用尾缀
```
真实物理光照衰减，非均匀自然光源，
体积光穿过场景介质可见，环境光遮蔽加深物体接触面，
阴影区域保留细节非死黑，高光区域保留纹理非过曝，
光影随镜头内时间自然变化符合物理规律，
cinematic lighting, natural light falloff, physically based light behavior,
shadow detail preserved, highlight rolloff smooth
```
- 追加关键词：`physically based lighting`, `light falloff inverse square`, `shadow detail not crushed`, `highlight texture not clipped`

---

### 🌧️ 模块五：天气与粒子/Weather & Particles

#### 雨
```
雨丝不同远近形成深度层次而非均匀线条，
雨滴打在地面积水形成涟漪扩散，
路面湿润镜面反射街道灯光和环境，
屋檐滴水形成连续水帘非断开，
雨幕中远景 atmospheric attenuation 形成灰白雾感。
```
- 追加关键词：`rain streaks depth layers`, `raindrop ripple on puddle`, `wet ground specular reflection`, `rain atmospheric attenuation`

#### 雪
```
雪花大小不一非均匀飘落，近景大远景小形成深度感，
积雪表面微晶反光 sparkle，风吹雪面形成波纹纹理，
雪地踏痕边缘自然不规则，房檐冰柱自然形成下垂尖端水滴状，
建筑/树木积雪厚度按面朝风向分布不均。
```
- 追加关键词：`snowflake size depth variation`, `snow surface sparkle micro-reflection`, `wind-blown snow ripple texture`, `icicle natural drip formation`

#### 雾
```
雾层非均匀密度分布，低处密度大高处稀薄，
雾中物体轮廓边缘模糊程度随距离递增，
雾中光源形成可见散射球非均匀，
前景清晰→中景半隐→远景消失的渐进景深。
```
- 追加关键词：`fog density vertical gradient`, `fog object edge softness distance`, `light scattering in fog`, `fog depth layering`

#### 风/地面粒子
```
风吹地面扬起细尘/沙粒/落叶，粒子非均匀线性运动含随机微位移，
落叶在地面滚动/翻转/打转非匀速直线，
沙尘暴远景扬尘天际线模糊，近景沙粒高速运动模糊，
布料/旗帜/树枝在风中非匀速摆动含自然间歇。
```
- 追加关键词：`wind-blown particles random motion`, `dust devil ground swirl`, `fabric natural wind flutter`, `particle motion blur`

#### 火焰/烟
```
火焰非均匀橙-黄-蓝层级，焰尖飘动不可预测路径，
烟气非均匀密度上升，边缘湍流涡旋可见，
余烬火星随热气流螺旋上升，木柴爆裂弹出火星粒子，
烟火粒子轨迹弧线下落渐变衰减，灰烬落地堆积。
```
- 追加关键词：`flame color temperature gradient`, `smoke turbulent vortex edge`, `embers spiral upward on thermal`, `ash particle trajectory`


### 🌍 模块六：地面与路径/Terrain & Ground

#### 泥土/沙地
```
泥土表面自然颗粒纹理非平滑，湿度差异形成深浅色块，
沙地风吹波纹纹理，沙粒反光微闪烁，
脚印边缘崩落不规则而非整齐压痕，
泥土干裂龟裂网格自然随机非规则六边形。
```
- 追加关键词：`soil granular surface texture`, `sand wind ripple pattern`, `footprint edge crumbling`, `mud crackle random pattern`

#### 石头/岩石
```
岩石表面粗糙颗粒纹理，不同矿物成分的色泽差异，
岩壁表面裂缝/节理/层理可见，青苔在阴面自然生长，
溪流中鹅卵石表面圆滑水磨纹理，湿润状态反光，
散落碎石大小随机分布符合自然分选。
```
- 追加关键词：`rock surface mineral variety`, `cliff face fracture and joint`, `river stone water-polished texture`, `rubble size natural distribution`

#### 道路/铺装
```
沥青路面表面骨料颗粒纹理可见，裂缝非直线自然曲折，
路面积水处反光形成水洼倒影，路面标线褪色磨损，
石板路每块石板微高差非完美齐平，石缝间小草/青苔自然生长，
砂石路面车轮辙痕纹理，雨后车辙积水。
```
- 追加关键词：`asphalt aggregate surface visible`, `road crack natural meander`, `cobblestone uneven height variation`, `wheel rut water reflection`

---

## 三、景别适配指南

不同景别能看到的场景细节不同——写多了模型无视，写少了画面空。

| 景别 | 可见场景细节 | 增强重点 | 不可见（别写） |
|------|------------|---------|---------------|
| 大特写 ECU | 材料表面纹理、磨损、水珠、锈蚀 | 微观材质纹理 | 整体建筑形态 |
| 特写 CU | 面材纹理、接缝、光影局部 | 材质对比、局部AO | 场景全貌 |
| 近景 MCU | 单面墙/地面、道具、环境局部 | 材质+光影层次 | 远方环境 |
| 中景 MS | 房间一角、建筑局部、植被群 | 材质+空间关系+中景大气 | 极远景 |
| 全景 FS | 完整建筑、整个房间、大片植被 | 大气透视+整体光影+宏观材质 | 微纹理 |
| 远景 LS | 城际线、山脉、天际 | 大气雾+天空云+整体色调 | 任何表面细节 |
| 超远景 EWS | 地貌轮廓、云层 | 光色+云层+大气渐变 | 任何近景 |


## 四、场景类型快速适配

按场景类型一键选择增强模块组合：

| 场景类型 | 必加模块 | 选加模块 |
|---------|---------|---------|
| 中式古建筑 | 建筑·古建 + 光影·体积光 | 天气·雾 + 地面·石板路 |
| 仙侠场景 | 自然·山脉/云 + 光影·体积光 + 天气·雾 | 自然·水/树木 |
| 现代都市 | 建筑·现代 + 光影·AO + 地面·道路 | 天气·雨 + 光影·霓虹 |
| 室内古风 | 室内·墙面/家具 + 光影·烛光 | 室内·织物 + 光影·体积光 |
| 室内现代 | 室内·全模块 + 光影·AO | 光影·特殊·霓虹 |
| 森林/野外 | 自然·树木/草地 + 光影·God Rays | 天气·风 + 自然·水 |
| 雨夜街景 | 天气·雨 + 地面·道路 + 光影·霓虹 | 建筑·现代 |
| 雪景 | 天气·雪 + 光影·逆光 | 自然·山脉 + 地面·雪地 |
| 废墟/战场 | 建筑·废墟 + 天气·烟/火 | 光影·体积光 + 地面·泥土 |
| 沙漠/戈壁 | 地面·沙地 + 天气·风 + 自然·天空 | 建筑·废墟 + 光影·haze |

---

## 五、使用方式

### 方式一：嵌入提示词【场景】段（推荐）

将增强描述直接写入场景描述中，和人物描述并列：

```
【场景】
中式庭院，汉白玉石基表面微颗粒纹理，石材自然风化微裂纹，
红色漆柱表面微细龟裂纹理，琉璃瓦逐片独立反光，
檐下阴影区 ambient occlusion 加深形成纵深层次，
阳光穿过桂花树叶间隙形成可见体积光束，
光柱中悬浮微尘粒子自然分布，电影级光影渲染。
```

### 方式二：分镜内容中局部增强

在具体镜头内容中追加场景质感词：
```
（0-3秒）低角度仰拍，汉白玉石阶边缘自然磨损特写，
雨后石面湿润反光形成水洼倒影，石缝间青苔自然附生。
```

### 方式三：作为场景质感尾缀

在提示词末尾追加全局场景质感：
```
8K电影级渲染，场景材质纹理每处不同非平铺重复，
真实物理光照衰减，环境光遮蔽加深接触面，
大气透视远景色彩衰减，体积光穿过场景介质可见，
所有表面保留微纹理和自然磨损痕迹，非CG完美光滑。
```

---

## 六、场景质感通用尾缀（一行完整版）

**适用于任何场景类型，追加在提示词末尾：**

```
场景材质纹理真实，每处表面保留微纹理和自然磨损痕迹，
非CG完美光滑，非平铺重复纹理，ambient occlusion 加深接触面，
真实物理光照衰减，体积光穿过场景介质可见悬浮微尘粒子，
atmospheric haze 远景色彩饱和度随距离衰减，阴影保留细节非死黑，
高光区域纹理可见非过曝，电影级场景渲染，8K细节。
```

**配套 avoid 约束行：**
```
避免场景像游戏贴图，避免材质纹理平铺重复，
避免光影扁平无层次，避免远景糊成一片，
避免自然元素规则排列违反自然随机分布。
```

---

## 七、避坑指南

| 问题 | 错误写法 | 正确写法 |
|------|---------|---------|
| 场景太空洞 | "中式庭院" | "中式庭院，汉白玉石基表面微颗粒纹理，红色漆柱表面微细龟裂纹理..." |
| 材质重复感 | 不写纹理描述，模型默认平铺 | 每种材质单独描述纹理特征 |
| 光影扁平 | "阳光照射" | "阳光穿过树叶间隙形成体积光束，光柱中悬浮微尘，地面形成斑驳光斑" |
| 远景假 | "远处有山" | "远山被大气薄雾笼罩，色彩随距离衰减为蓝灰色，山体轮廓边缘模糊渐变" |
| 自然元素规整 | "一排树" / "整齐的花" | "树木非均匀分布形成自然林缘线" / "花卉不同开放度花苞并存" |
| 水假 | "清澈的水" | "水质微浑浊悬浮颗粒，水面微波形成非均匀反射，水底鹅卵石折射偏移" |
| 室内样板间 | "干净明亮的房间" | "房间墙面微凹凸纹理，木地板走道区域自然磨损光泽，窗帘自然褶皱重力垂坠" |
| 天空假 | "蓝天白云" | "蓝天色彩从头顶深蓝到地平线浅白渐变，云层体积感三维立体，云边缘柔软羽状渐变" |

---

## 八、快速决策流

```
1. 判断场景类型 → 查「四、场景类型快速适配」选模块
2. 判断景别 → 查「三、景别适配指南」定细节层级
3. 选模块 → 从对应模块中摘取关键词写入场景描述
4. 追加光影 → 从「模块四」选匹配的光影增强
5. 追加天气 → 有天气元素时从「模块五」选
6. 末尾 → 追加「六、场景质感通用尾缀」+ avoid约束
```

---

## 九、版本维护

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-26 | 初始版本，六大模块（建筑/自然/室内/光影/天气/地面）+ 景别适配 + 场景快速适配 + 避坑指南 + 快速决策流 |

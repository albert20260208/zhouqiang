---
name: VIDEO
description: |
  综合视频制作知识库，整合了所有视频相关技能的知识点。
  包含：Seedance/Seedream模型使用指南、5Agent工作流、短剧制作、导演技巧、编剧指南、镜头语言等。
  适用于：商业视频广告、电影/短剧片段、教学演示视频、视频素材创作。
---

# VIDEO - 综合视频制作知识库

## 📚 目录结构

### 1. 核心模型指南
- [Seedance指南](references/seedance-guide.md) - Seedance视频生成完全指南（@引用系统、提示词结构、镜头语言）
- [Seedream 5.0指南](references/seedream-5.0.md) - Seedream 5.0图像生成指南（联网检索、组图生成、一致性增强）
- [火山引擎API指南](references/volcano-api-guide.md) - API调用与配置（认证、参数、错误处理）

### 2. 工作流与流程
- [5Agent工作流](references/5agent-workflow.md) - 5Agent分工协作流程（场记、编剧、建模师、导演、摄影师）
- [工作流索引](references/workflow-index.md) - 视频制作工作流索引
- [短剧制作工作流](workflows/short-drama-workflow.md) - 短剧制作专业流程（剧本、分镜、角色、场景、后期）

### 3. 创作与制作
- [编剧指南](references/screenwriting.md) - 剧本创作与剧情分析（故事结构、人物弧光、对白设计）
- [导演指南](references/directing.md) - 导演技巧与运镜设计（镜头调度、节奏控制、情感表达）
- [导演风格参考](references/director-styles.md) - 不同导演风格模板（王家卫、诺兰、斯皮尔伯格等）
- [胡导风格指南](已移除（过时，5层新标准替代）) - 胡导风格标准格式（固定镜头、15秒规则、@引用系统）
- [镜头语言指南](references/shots-guide.md) - 镜头语言与拍摄技巧（景别、角度、运动、构图）
- [武侠动作指导](references/wuxia-action-guide.md) - 武侠动作设计与特效表现（招式设计、兵器特性、轻功表现）
- [制作技巧](已移除（过时）) - 视频制作实用技巧（场景一致性、物理常识、画质增强）

### 4. 子技能（2026-06 新增）
- [违禁词审查技能](违禁词审查技能/SKILL.md) - 出稿前全文扫描11大类违禁词并替换
- [人物服装增强技能](人物服装增强技能/SKILL.md) - 皮肤/眼睛/头发/服装四维质感增强
- [场景质感增强技能](场景质感增强技能/SKILL.md) - 建筑/自然/室内/光影/天气六模块增强
- [场景一致性保持技能](场景一致性保持技能/SKILL.md) - 四面墙法+八维准则+多镜头一致性
- [打斗设计技能](打斗设计技能/SKILL.md) - 运镜/节奏/打击反馈/技术参数全栈
- [传奇打斗动作模版一](传奇打斗动作模版一/SKILL.md) - 写实格斗·冲击波四层·6镜循环
- [传奇打斗动作模版二](传奇打斗动作模版二/SKILL.md) - 赛博奇幻·太极×机甲·9镜标准版

### 5. 基础知识
- [视频制作知识库](references/knowledge.md) - 视频制作基础知识（术语、流程、工具）
- [短剧结构指南](references/short-drama-structure.md) - 短剧剧本结构（三幕式、钩子设计、情绪曲线）
- [竖屏镜头指南](references/vertical-shots-guide.md) - 竖屏视频拍摄指南（9:16构图、手机端优化）
- [角色提示词库](references/character-prompts.md) - 角色设计与提示词（外貌、服装、表情、姿态）
- [多人打斗站位指南](references/multi-character-fight-positioning.md) - 3+人空间布局与轴线管理

### 6. 模板与工具
- [项目整体说明模板](templates/project-overview-template.md) - 项目启动文档模板（需求确认、规格定义）
- [短剧剧本模板](templates/short-drama-script-template.md) - 完整短剧剧本模板（人物、场景、对白、情绪）
- [剧本分析模板](templates/script-analysis-template.md) - 剧本分析模板（结构、人物、情绪曲线）
- [分镜设计模板](templates/storyboard-template.md) - 分镜设计模板（镜头、运镜、音频）
- [API调用脚本](scripts/) - 视频生成相关脚本（Seedance、Seedream、任务监控）

## 📊 整合统计

| 分类 | 数量 | 最后更新 |
|------|------|---------|
| 主入口 SKILL.md | 1 | 2026-06-29 |
| 子技能 | 7 | 2026-06-28 |
| 参考文档 references/ | 18 | 2026-06-27 |
| 工作流 workflows/ | 2 | 2026-03-30 |
| 模板 templates/ | 4 | 2026-03-30 |
| 脚本 scripts/ | 8 | 2026-03-30 |
| **合计** | **38** | — |

## 🎯 核心能力

### 1. Seedance视频生成
- **@引用系统**：图片、视频、音频引用
- **提示词结构**：结构化模板与时间分段
- **镜头语言**：基础运动与高级技巧
- **多幕一致性**：人物、服装、场景一致性保持
- **画质增强**：4K直出与智能增强技巧

### 2. Seedream图像生成
- **联网检索**：实时搜索最新素材
- **生成模式**：文生图、图生图、组图生成
- **一致性增强**：跨图像角色特征保持
- **尺寸选项**：2K/3K分辨率与自定义尺寸

### 3. 5Agent协作流程
- **场记(Video Scribe)**：需求确认与项目管理
- **编剧(Video Writer)**：剧情分析与提示词创作
- **建模师(Video Modeler)**：参考图片素材生成
- **导演(Video Director)**：运镜脚本与分镜设计
- **摄影师(Video Cameraman)**：API调用与视频生成

### 4. 短剧制作专业
- **快节奏叙事**：强情绪、高冲突、竖屏优化
- **剧本分析**：三幕结构、人物弧光、情感曲线
- **分镜设计**：竖屏镜头语言、情绪节奏控制
- **场景一致性**：人物、服装、场景、色调统一

## 🔧 技术栈

### API与模型
- **视频生成**：Seedance 2.0/1.5 Pro
- **图像生成**：Seedream 5.0/4.5/4.0
- **API端点**：`https://ark.cn-beijing.volces.com/api/v3`
- **认证方式**：API Key鉴权

### 编程语言
- **主要语言**：Python 3.12+
- **SDK**：volcenginesdkarkruntime
- **脚本库**：scripts/目录下的各种工具脚本

### 输出规格
- **视频分辨率**：480p-720p（可增强至4K）
- **视频时长**：4-15秒
- **图像分辨率**：2K/3K（2048x2048-4096x2304）
- **宽高比**：支持1:1、4:3、16:9、9:16等

## 📋 使用流程

### 标准视频制作流程
1. **项目启动**：确认需求，创建项目说明文档
2. **内容创作**：生成剧情分析与提示词
3. **素材准备**：生成参考图片与运镜脚本
4. **视频生成**：按镜头顺序生成视频片段
5. **质检交付**：检查一致性，整合交付

### 短剧制作流程
1. **剧本创作**：三幕结构，强情绪冲突
2. **分镜设计**：竖屏优化，情绪节奏控制
3. **角色设计**：人物特征一致性保持
4. **场景生成**：连续镜头场景一致性
5. **后期整合**：音乐、音效、字幕整合

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install volcenginesdkarkruntime
```

### 2. 配置API Key
获取火山引擎API Key：https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey

### 3. 运行示例脚本
```python
from scripts.seedance_api import generate_video

# 生成简单视频
task_id = generate_video(
    prompt="一只可爱的橘猫在阳光下打盹，电影质感，4K画质",
    duration=5
)
```

### 4. 查看详细指南
- 阅读[Seedance指南](references/seedance-guide.md)了解提示词撰写
- 阅读[5Agent工作流](references/5agent-workflow.md)了解协作流程
- 阅读[短剧制作指南](workflows/short-drama-workflow.md)了解短剧制作

## 📁 文件来源

本知识库整合了以下来源的知识点：
- `skills/video/` - 原始视频知识库
- `skills/video-production-5agent/references/` - 5Agent参考资料
- `skills/short-drama-production/` - 短剧制作知识
- `skills/video-production/` - 视频制作流程

所有知识点已重新组织，避免分散，便于查找和使用。

---

_整合版本: v2.0_
_更新时间: 2026-06-29_
_状态: ✅ 持续维护（2026-06-29 完成违禁词去重合并+索引更新）_
_维护者: AI助手3号_

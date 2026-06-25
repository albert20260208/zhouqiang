---
name: video-production-5agent
description: |
  专业的视频制作能力，基于火山引擎Seedance和Seedream模型，使用5Agent分工协作流程。
  适用于：(1) 创建商业视频广告 (2) 生成电影/短剧片段 (3) 制作教学演示视频 (4) 视频素材创作。
  包含：5Agent角色分工、火山引擎API调用、视频生成工作流、场景一致性处理、专业提示词撰写。
---

# Video Production 5Agent - 视频制作专业Skill

## 快速开始

### 核心工作流
1. **场记(Video Scribe)** - 确认项目需求，创建《项目整体说明》
2. **编剧(Video Writer)** - 生成剧情分析和提示词
3. **建模师(Video Modeler)** - 生成参考图片素材
4. **导演(Video Director)** - 制作运镜脚本
5. **摄影师(Video Cameraman)** - 调用API生成视频

### 关键模型
- **文生图**: `doubao-seedream-5-0-260128`
- **文生视频**: `doubao-seedance-1-5-pro-251215`
- **API端点**: `https://ark.cn-beijing.volces.com/api/v3`

## 5Agent角色配置

| Agent ID | 名称 | 模型 | 职责 |
|----------|------|------|------|
| video-scribe | 场记 | MiniMax-M2.5 | 需求确认、记录、项目管理 |
| video-writer | 编剧 | deepseek-reasoner | 剧情、提示词、内容创作 |
| video-modeler | 建模师 | deepseek-reasoner | 生成参考图片素材 |
| video-director | 导演 | deepseek-reasoner | 运镜脚本、分镜设计 |
| video-cameraman | 摄影师 | deepseek-reasoner | API调用、视频生成 |

## 详细流程

### 阶段0：项目启动（场记）
- 确认故事背景、剧情主线、视频规格
- 创建《项目整体说明》模板
- 必须得到用户确认后才能进入下一阶段

### 阶段1：需求归档（场记）
- 整理《项目需求基准文档》
- 同步给所有Agent

### 阶段2：内容创作（编剧）
- 生成剧情分镜文案
- 输出提示词供后续使用
- 必须用户确认

### 阶段3：素材与脚本生成（建模师+导演并行）
- 建模师：生成参考图片（使用Seedream）
- 导演：制作运镜脚本
- 用户同时确认

### 阶段4：视频生成（摄影师）
- 使用Seedance API生成视频
- 每个片段必须用户确认
- 连续镜头使用上一视频首帧作为参考

### 阶段5：质检与交付（场记）
- 检查物理常识、人文习俗、生活常识
- 场景一致性验证
- 知识沉淀

## 关键参考资料

### 必读
- [5agent-workflow.md](references/5agent-workflow.md) - 完整5Agent分工流程
- [volcano-api-guide.md](references/volcano-api-guide.md) - 火山引擎API调用指南

### 专业技术
- [seedance-guide.md](references/seedance-guide.md) - Seedance使用指南
- [seedream-5.0.md](references/seedream-5.0.md) - Seedream 5.0文生图指南
- [screenwriting.md](references/screenwriting.md) - 编剧指南
- [directing.md](references/directing.md) - 导演指南

### 进阶参考
- [shots-guide.md](references/shots-guide.md) - 镜头语言指南
- [director-styles.md](references/director-styles.md) - 导演风格参考
- [production-tips.md](references/production-tips.md) - 制作技巧
- [knowledge.md](references/knowledge.md) - 视频制作基础知识

## 可用脚本

### 视频生成脚本
- `scripts/seedance_video_generate.py` - Seedance视频生成主脚本
- `scripts/generate_lishimin_video.py` - 李世民视频生成示例
- `scripts/check_task_status.py` - 任务状态轮询

### 测试与调试脚本
- `scripts/test_seedance_1_5_pro.py` - Seedance 1.5 Pro测试
- `scripts/test_real_api_key.py` - API Key有效性测试

## 场景一致性处理

### 多段视频衔接规则
1. 每个视频的第一帧必须使用上一视频最后一帧
2. 保持场景内所有物品布局不变
3. 人物、服装、场景、色调必须完全一致
4. 禁止出现"幻觉"（物品突变、场景跳变）

### 物理/人文/常识约束
- 严格遵循物理常识（重力、运动规律）
- 符合人文习俗（服装、礼仪、建筑风格）
- 符合生活常识（日常行为逻辑）

## 常见问题

### API调用问题
- 认证失败：检查API Key格式和权限
- 参数错误：确认模型ID和请求格式
- 生成失败：优化提示词后重试（最多3次）

### 质量问题
- 场景不一致：确保使用首帧参考图
- 风格不统一：在提示词中明确风格要求
- 动作不自然：详细描述动作细节和时序

## 模板文件

- [项目整体说明模板.md](assets/项目整体说明模板.md) - 项目启动文档模板

# 小说转剧本 AI 研究（2026-08-06）

## 核心论文/框架

### 1. DSR (Dual-Stage Refinement) - 阿里/北大
论文：Beyond Direct Generation: A Decomposed Approach to Well-Crafted Screenwriting with LLMs

核心思路：
- **两阶段分离**：Stage 1（大纲→小说文体）专注于创意叙事生成，Stage 2（小说→剧本）专注于格式转换
- 解决了"任务耦合困境"：强迫单一模型同时做创意生成+格式遵守=效果差
- 中间表示是"小说文体"而非传统文学小说——专为大屏幕视觉叙事设计，只描述可观察的动作和可听的对话
- 例子：不说"他充满悔恨"→说"他盯着破裂的照片，下颌紧绷，然后慢慢闭上眼睛"

关键洞察：
- 小说的信息密度高，剧本的信息密度低且有严格格式约束
- 小说→剧本 = 信息压缩+格式转换

### 2. R2 Framework - ICLR 2025
论文：R2: A LLM Based Novel-to-Screenplay Generation Framework with Causal Plot Graphs

核心思路：
- 使用因果情节图+角色档案保证一致性
- 处理LLM幻觉问题
- 自适应重写（HAR）迭代细化

## 工具

### ScriptBreak
GitHub: wassermanproductions/scriptbreak
功能：
- 导入剧本（Fountain/Final Draft/PDF/TXT）
- 自动拆解场景、角色、地点、道具
- 生成shot lists、timeline
- 导出AI prompt packs（支持Veo/Runway/Kling/Seedance等）
- 纯本地运行，无需API key

### Awesome LLM Story Generation
GitHub: Picrew/awesome-llm-story-generation
汇总了LLM故事/小说/剧本生成的最新论文和开源项目

## 关键设计原则

1. **两阶段优于单阶段**：叙事生成和格式转换分开训练
2. **中间小说文体**：为剧本服务的描述性文本，非传统文学小说
3. **Chain-of-Thought**：在Stage 1加入思维链推理，提高质量
4. **角色档案锚定**：保证跨场景角色一致性
5. **可观察动作 > 抽象情感**：描述performable moment

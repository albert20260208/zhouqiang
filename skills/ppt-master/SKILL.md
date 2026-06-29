---
name: ppt-master
description: AI驱动的多角色协作PPT生成系统，产出原生可编辑PPTX。当用户说"做PPT""生成PPT""制作演示文稿"时使用。
---

# PPT Master — PPT生成技能

> 开源项目：`hugohe3/ppt-master` v2.11.0 | MIT License
> 本地路径：`ppt-master/`

## 触发条件

用户说「做PPT」「生成PPT」「制作演示文稿」「做个PPT」等。

## 工作流

```
源文档 → 创建项目 → Strategist(8确认·⛔阻塞) → Executor(手写SVG·逐页) → 质检 → 后处理 → 导出PPTX
```

- **⛔ 阻塞点**：Strategist 的 8 项确认必须等用户逐一回复，不准替用户决定
- **串行执行**：前一步输出是下一步输入，不跳过
- **SVG 必须手写**：不准脚本批量生成，不准子代理代写，逐页生成

## 命令

| 阶段 | 命令 |
|------|------|
| 安装依赖 | `pip install -r ppt-master/requirements.txt` |
| 创建项目 | `python ppt-master/project_manager.py create <项目名>` |
| 读取技能 | 先读 `ppt-master/skills/ppt-master/SKILL.md` 完整工作流 |
| 导出PPTX | 由 Executor 生成的 SVG → python-pptx 打包 |

## 关键经验（来自实战）

1. **`<g opacity>` 不认**：必须逐元素设 `opacity`/`stroke-opacity`/`fill-opacity`
2. **`<animate>` 禁止**：SMIL 动画元素不能出现在 SVG 中
3. **字体问题**：SVG 用 Microsoft YaHei，Linux 服务器渲染 PNG 时需替换为 WenQuanYi Micro Hei
4. **项目路径**：新建项目在 `ppt-master/projects/<项目名>/`
5. **spec_lock.md**：每页 SVG 生成前必读，颜色/字体/图标/图片全从中取

## 完整文档

项目自带完整技能文件：`ppt-master/skills/ppt-master/SKILL.md`

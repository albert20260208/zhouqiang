---
name: skill-manager
description: 技能库梳理、去重、整合 — 批量审计 SKILL.md 文件的冗余、冲突、过时内容，给出合并建议和清理方案
---

# 🧩 Skill Manager — 技能梳理·去重·整合

> **仅供手动触发** — 不自动执行任何操作。主人说"执行 skill-manager" 才启动工作流。

---

## 一、能力总览

| 模块 | 功能 | 产出物 |
|------|------|--------|
| **梳理** | 扫描全部 skills 目录，分类、统计、生成/更新 INDEX | 📋 技能清单 + 技能地图 |
| **去重** | 检测同主题重复 SKILL.md、重叠描述、双索引 | 🗑️ 去重报告 + 合并建议 |
| **整合** | 合并相关技能、归档废弃技能、统一命名/结构 | 🔗 整合方案 + 执行脚本 |

---

## 二、扫描范围

执行时会扫描以下三层技能目录：

```
# 层1: 系统内置 skills（只读，仅记录）
/usr/local/lib/node_modules/openclaw/skills/*/
/usr/local/lib/node_modules/openclaw/dist/extensions/*/skills/*/

# 层2: 用户全局 skills
~/.openclaw/skills/*/

# 层3: 工作区 skills（可读写）
~/.openclaw/workspace/skills/*/
```

---

## 三、工作流（手动执行）

### Phase 1: 梳理 — `技能清单`

**步骤**:
1. 遍历三层 skills 目录，收集所有 `SKILL.md`
2. 解析每个 SKILL.md 的 frontmatter（name / description / tags）
3. 按主题分类：
 - 股票金融 / 视频制作 / 进化迭代 / 平台集成 / 运维审计 / 知识管理 / 工具辅助 / 其他
4. 统计每类技能数量、总文件数、总大小
5. 生成/更新 `skills/INDEX.md` — 确保与真实目录一致

**输出**: `skills/INDEX.md`（更新版）

### Phase 2: 去重 — `检测清单`

**检测项**:

| # | 检测项 | 方法 |
|---|--------|------|
| 1 | **同名 SKILL.md** | 不同目录下是否存在相同 `name:` 但内容有差异的技能 |
| 2 | **功能重叠** | 对比 description + tags，识别相似主题（如 file organizer 有多个版本） |
| 3 | **双索引** | 同一类内容是否被 INDEX.md 和另一个索引文件同时记录 |
| 4 | **引用死链** | SKILL.md 中引用的路径/脚本/文件是否实际存在 |
| 5 | **冗余代码脚本** | `.py` / `.sh` 是否在多个技能中被重复复制 |
| 6 | **过时技能** | 描述的功能已被其他技能覆盖，或不再使用的旧版技能 |

**扫描命令**:
```bash
# 同名校验
find ~/.openclaw/skills /usr/local/lib/node_modules/openclaw/skills -name "SKILL.md" -exec grep -l "^name:" {} \; | sort

# 功能重叠初步：提取所有 name + description
for f in $(find ~/.openclaw/workspace/skills ~/.openclaw/skills -name "SKILL.md" 2>/dev/null); do
 echo "=== $f ==="
 head -10 "$f" | grep -E "^name:|^description:"
done
```

**输出**: `去重报告`（列出重复项 + 严重程度 + 建议操作）

### Phase 3: 整合 — `合并方案`

**合并类型**:

| 类型 | 说明 | 操作 |
|------|------|------|
| 🟢 轻量合并 | 两个技能功能一致但分布在 skills/root 和 workspace | 保留 workspace 版，删除另一版，INDEX 记录为止 |
| 🟡 内容合并 | 多个技能覆盖同一主题但各有侧重 | 新建综合版 SKILL.md，旧版标记 DEPRECATED |
| 🔴 架构合并 | 同一个扩展技能分散在多处（如 capability-evolver） | 统一目录结构 + 更新所有引用路径 |

**命名规范**（整合后统一）:
```
skills/{category}/{skill-name}/
 ├── SKILL.md # 主技能文件
 ├── README.md # 说明（可选）
 └── scripts/ # 绑定脚本（可选）
```

**输出**: `整合方案.md`（合并计划 + 回滚方案）

### Phase 4: 报告输出

```
📋 [日期] Skill Manager 报告

🔍 梳理结果
- 总计: N 个技能 | M 个文件 | X MB
- 新增: N 个 / 过时: M 个 / 变动: X 个

🗑️ 去重发现
- 🔴 严重：N 个（必须处理）
- 🟡 建议：M 个（建议处理）
- 🟢 信息：X 个（仅记录）

🔗 整合建议
- 建议合并：N 组
- 建议归档：M 个
- 建议保留：X 个

📌 手动操作指令
./scripts/merge_skills.sh [合并ID] # 执行合并
./scripts/archive_skill.sh [名称] # 归档技能
```

---

## 四、辅助脚本

技能目录下可附带以下辅助脚本（创建但不自动运行）：

| 脚本 | 用途 | 安全措施 |
|------|------|---------|
| `scripts/skill_index.sh` | 扫描所有技能生成 INDEX | 只读，不修改文件 |
| `scripts/dedup_check.sh` | 去重检测，输出报告 | 只读，不删除文件 |
| `scripts/merge_skills.sh` | 按方案执行合并（需手动调用） | 操作前备份原文件 |

---

## 五、安全约束

- **只读扫描**：梳理和去重阶段不修改任何文件
- **整合需确认**：合并方案展示后，必须主人说"执行"才执行
- **自动备份**：任何合并/删除前，自动备份到 `memory/skill-manager-backups/` 带时间戳
- **回滚路径**：每个操作记录 exact undo 指令

---

## 六、触发方式

主人说以下任一指令时启动：

> "整理技能" / "技能去重" / "技能梳理" / "跑一下 skill-manager"

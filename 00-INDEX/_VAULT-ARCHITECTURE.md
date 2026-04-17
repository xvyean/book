---
type: meta
description: 本库的架构设计说明，面向 AI（Claude）和人类作者
created: 2026-04-02
updated: 2026-04-13
---

# Vault 架构设计：AI 友好型西幻小说设定库

## 设计哲学

本库的目录结构、文件命名、frontmatter 规范，均以 **Claude 通过 MCP 检索** 的效率为第一优先级。

### Claude 的检索特征

| 特征 | 设计对策 |
|------|----------|
| Claude 通过**文件名/路径搜索**定位文件 | 文件名使用 `类型前缀-名称` 格式，如 `char-艾伦.md` |
| Claude **逐文件读取**，无法一次看到全库 | 每个文件头部有 `summary` 字段，3 句话说清这是什么 |
| Claude 依赖 **frontmatter 属性**做结构化查询 | 统一模板，关键关系写入属性而非散落在正文 |
| Claude 通过 **wikilinks** 追踪关联 | 所有交叉引用使用 `[[]]` 语法，属性中也用 wikilinks |
| Claude 的上下文窗口有限 | 长文件拆分，单文件控制在 500 行以内 |
| Claude 不知道库里有什么 | `_MASTER-INDEX.md` 作为全库地图，首次检索入口 |

---

## 目录结构

```
new book/
├── 00-INDEX/                  # 导航层：Claude 的起点
│   ├── _MASTER-INDEX.md       # 全库地图（Claude 首读文件）
│   ├── _VAULT-ARCHITECTURE.md # 本文件：架构说明
│   └── _STYLE-GUIDE.md        # 写作风格与命名规范
│
├── 01-WORLD/                  # 世界观设定
│   ├── _index.md              # 世界观总览 hub
│   ├── magic/                 # 魔法体系子域
│   │   ├── _index.md          # 魔法域导航
│   │   └── magic-*.md         # 7 个魔法体系文件
│   ├── religion/              # 宗教体系子域
│   │   ├── _index.md          # 宗教域导航
│   │   ├── religion-*.md      # 6 个体系规则文件
│   │   └── religion-神明-*.md # 17 个神明个档
│   ├── geography/             # 地理子域（基础框架已建立）
│   │   ├── _index.md          # 地理域导航
│   │   ├── geo-世界总览.md     # 六层世界骨架与族群空间总览
│   │   ├── geo-中央内海.md     # 文明交通核心
│   │   ├── geo-主舞台板块.md   # 六种文明空间总览
│   │   ├── geo-精灵林地.md     # 林地文明圈（区域）
│   │   ├── geo-沿海城邦带.md   # 混居城邦带（区域）
│   │   └── geo-巡游学院.md     # 流动知识中心（区域）
│   ├── history/               # 历史子域（待建设）
│   │   └── _index.md
│   ├── culture/               # 文化子域（待建设）
│   │   └── _index.md
│   └── politics/              # 政治子域（待建设）
│       └── _index.md
│
├── 02-CHARACTERS/             # 角色设定
│   ├── _index.md
│   └── char-*.md
│
├── 03-FACTIONS/               # 势力与组织
│   ├── _index.md
│   └── fac-*.md
│
├── 04-ITEMS/                  # 重要物品、神器、材料
│   ├── _index.md
│   └── item-*.md
│
├── 05-PLOT/                   # 剧情结构
│   ├── _index.md
│   ├── arc-*.md               # 故事弧
│   ├── timeline-*.md          # 时间线
│   └── subplot-*.md           # 支线
│
├── 06-CHAPTERS/               # 正文章节
│   ├── _index.md
│   └── ch-*.md
│
├── 07-REFERENCES/             # 参考资料
│   ├── naming-规则.md
│   ├── glossary-术语表.md
│   └── inspirations.md
│
└── _TEMPLATES/                # Obsidian 模板
    ├── tpl-character.md
    ├── tpl-location.md
    ├── tpl-faction.md
    ├── tpl-item.md
    ├── tpl-arc.md
    ├── tpl-chapter.md
    ├── tpl-world.md
    ├── tpl-deity.md           # 神明个档专用模板
    └── tpl-region.md          # 区域/文明圈专用模板
```

---

## 文件命名规范

### 前缀系统

| 前缀 | 类型 | 示例 |
|------|------|------|
| `char-` | 角色 | `char-艾伦.md` |
| `geo-` | 地理/地点 | `geo-灰港.md` |
| `hist-` | 历史事件 | `hist-黎明之战.md` |
| `magic-` | 魔法相关 | `magic-魔导卡体系总览.md` |
| `culture-` | 文化/民族 | `culture-北境部族.md` |
| `religion-` | 宗教/信仰 | `religion-神明-卡尔涅斯.md` |
| `politics-` | 政治/制度 | `politics-联邦议会制.md` |
| `fac-` | 势力/组织 | `fac-暗影公会.md` |
| `item-` | 物品/神器 | `item-碎星剑.md` |
| `arc-` | 故事弧 | `arc-第一卷-觉醒.md` |
| `ch-` | 章节 | `ch-001.md` |
| `timeline-` | 时间线 | `timeline-主线.md` |
| `subplot-` | 支线 | `subplot-复仇线.md` |
| `tpl-` | 模板 | `tpl-character.md` |
| `_` | 索引/元文件 | `_index.md`, `_MASTER-INDEX.md` |

### 子文件夹与前缀的配合

`01-WORLD/` 下的内容按领域分入子文件夹（magic/、religion/ 等）。Obsidian 的 wikilink 基于**文件名**而非路径，因此文件移入子文件夹不会破坏已有链接。前缀仍然保留，因为它在搜索和文件列表中提供额外的类型信号。

---

## Frontmatter 规范

### 通用字段（所有文件必须包含）

```yaml
---
type: character | location | faction | item | history | magic | culture | religion | politics | arc | chapter | meta
summary: "一句话概括本文件内容（给 Claude 的速读摘要）"
tags: [标签1, 标签2]
related: ["[[相关文件1]]", "[[相关文件2]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 角色专用字段

```yaml
---
type: character
role: protagonist | antagonist | supporting | minor
full_name: "全名"
aliases: ["别名1", "外号"]
age: 数字或描述
gender: "..."
species: "人类 | 精灵 | ..."
faction: "[[fac-所属势力]]"
location: "[[geo-当前所在地]]"
origin: "[[geo-出生地]]"
allies: ["[[char-盟友1]]"]
enemies: ["[[char-敌人1]]"]
status: alive | dead | unknown | missing
arc: ["[[arc-参与的故事弧]]"]
---
```

### 地点专用字段

```yaml
---
type: location
category: continent | region | kingdom | city | town | dungeon | landmark | wilderness
parent_location: "[[geo-上级地点]]"
sub_locations: ["[[geo-子地点1]]"]
ruler: "[[char-统治者]]"
faction: "[[fac-控制势力]]"
population: "..."
climate: "..."
---
```

### 势力专用字段

```yaml
---
type: faction
category: kingdom | guild | order | cult | tribe | alliance
leader: "[[char-领袖]]"
headquarters: "[[geo-总部]]"
members: ["[[char-成员1]]"]
allies: ["[[fac-盟友势力]]"]
enemies: ["[[fac-敌对势力]]"]
goals: "核心目标"
status: active | disbanded | secret
---
```

### 神明专用字段

```yaml
---
type: world
category: religion
alignment: 正神 | 邪神 | 中立神
god_tier: 一阶 | 二阶 | 三阶 | 四阶
deity_title: "职能之神"
deity_name: "专有名字"
law_domains: [法则领域]
divine_realm: "神国名称"
symbols: [象征物列表]
worship_groups: [典型信众群体]
allied_deities: ["[[religion-神明-盟友]]"]
hostile_deities: ["[[religion-神明-敌对]]"]
truth_card_affinity: "强关联 | 中等关联 | 冲突型关联 | 弱关联"
---
```

---

## Hub 文件（_index.md）的作用

每个主文件夹和子域文件夹下的 `_index.md` 是该领域的**导航枢纽**。Claude 在探索某个领域时，先读 `_index.md` 获取全貌，再深入具体文件。

### 三层导航路径

```
_MASTER-INDEX.md → 01-WORLD/_index.md → religion/_index.md → religion-神明-卡尔涅斯.md
```

### _index.md 的标准结构

```markdown
---
type: meta
summary: "XX领域的总览与导航"
---

# XX 总览

## 概述
（2-3 段文字介绍这个领域的核心设定）

## 文件清单
| 文件 | 摘要 |
|------|------|
| [[具体文件1]] | 一句话描述 |

## 关键关系
（这个领域内部的核心关系图谱）

## 待完善
- [ ] 尚未创建的设定
```

---

## _MASTER-INDEX.md 的核心地位

这是 **Claude 的第一读取目标**。当 Claude 需要在库中查找任何信息时，应首先读取此文件。它提供：

1. 全库的文件夹说明（含子域入口）
2. 每个领域的一句话概括
3. 关键文件的直接链接
4. 当前创作进度

---

## 写作规则（面向 AI 可读性）

1. **摘要前置**：每个文件在 frontmatter 的 `summary` 和正文第一段都要用最精炼的语言说明"这是什么"
2. **关系显式化**：人物关系、势力关系不要只写在叙述文字里，必须写入 frontmatter 属性
3. **避免歧义引用**：正文中提到其他设定元素时，始终使用 `[[wikilink]]`，不要用纯文本
4. **单一职责**：一个文件只描述一个实体。不要在"某王国"的文件里详细展开国王的生平（应链接到国王的角色文件）
5. **控制文件长度**：单文件不超过 500 行。过长则拆分
6. **使用标准 Markdown**：避免 Obsidian 专属渲染语法，正文部分保持纯 Markdown

---

## 与 Claude 协作的最佳实践

### 让 Claude 查找信息
> "请先读取 `00-INDEX/_MASTER-INDEX.md`，然后根据需要查找相关设定"

### 让 Claude 创建新设定
> "请使用 `_TEMPLATES/tpl-character.md` 的模板格式，为我创建一个新角色"

### 让 Claude 检查一致性
> "请读取所有 `char-` 开头的文件的 frontmatter，检查角色关系是否有矛盾"

### 让 Claude 写章节
> "请先读取 `arc-第一卷.md` 了解剧情结构，再读取涉及角色的设定文件，然后撰写 ch-003"

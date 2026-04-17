# 小说设定库 - Codex 协作指南

## 项目概述
这是一部西幻小说的 Obsidian 设定库，架构专为 AI 检索优化。

## Codex 的工作流程

### 查找信息时
1. 先读 `00-INDEX/_MASTER-INDEX.md` 获取全局视图
2. 根据需要读对应子域的 `_index.md` 深入某个领域（如 `01-WORLD/magic/_index.md`、`01-WORLD/religion/_index.md`）
3. 再读具体的设定文件

### 创建新内容时
1. 使用 `_TEMPLATES/` 下的对应模板
2. 文件名使用前缀系统（char-、geo-、fac-、item- 等）
3. 完整填写 frontmatter，特别是 summary、related、关系字段
4. 更新对应的 `_index.md` 文件
5. 更新关联文件的双向引用

### 写作正文时
1. 先读 `arc-` 文件了解剧情结构
2. 再读涉及角色的 `char-` 文件
3. 读取相关地点的 `geo-` 文件
4. 确保正文与设定一致

## 文件命名前缀
- char-（角色）、geo-（地理）、hist-（历史）、magic-（魔法）
- culture-（文化）、religion-（宗教）、politics-（政治）
- fac-（势力）、item-（物品）、arc-（故事弧）
- ch-（章节）、timeline-（时间线）、subplot-（支线）

## 规范
- 所有交叉引用使用 [[wikilink]] 语法
- 修改关系时双向更新
- 单文件不超过 500 行
- 设定文件用客观百科风格，正文用小说叙事风格

---
name: style-compass
description: 根据项目上下文、仓库结构、页面截图和用户偏好推荐 3 种合适的 UI 设计风格，并展示风格说明卡、官方预览链接、适配理由和风险提醒。内置可浏览的“风格总览（Style Gallery）”，适合用户先横向看方向，再进入推荐和 UI 改造方案。也支持已有项目 UI 改造场景：基于仓库线索和当前页面截图输出改造方向、改造收益/难度/风险，以及可交接给实现 skill 的 UI-REFACTOR.md 草稿。用户提到“帮我挑风格”“像苹果/耐克/Stripe 那样”“根据这个项目推荐 UI 风格”“给我几个可选视觉方向”“看看这个项目适合什么设计风格”“给已有项目改版 UI”时必须使用。
---

# Beta 风格罗盘

## 概述

把“挑风格”从随口猜测变成可解释的设计路由。先读项目线索，再给 3 张风格卡，让用户知道为什么推荐、这些风格通常长什么样、哪里适合、哪里可能翻车。

现在支持双模式：

- `greenfield`：新项目 / 新页面 / 新品牌方向。输出 3 张风格卡，确认后生成 `DESIGN.md` 草稿。
- `refactor`：已有项目 UI 改造。输出带“改造收益 / 难度 / 风险”的风格卡，确认后生成 `UI-REFACTOR.md` 草稿。

## 首次使用先看这里

- 总览页入口：`风格总览（Style Gallery）.html`
- 总览文件夹入口：`风格总览（Style Gallery）/`
- 实际构建页：`assets/gallery/style-gallery.html`
- 开源入口页：`README.md`
- 开源许可证：`MIT`
- License 文件：`LICENSE`
- 原项目地址：`https://getdesign.md`
- 上游仓库：`https://github.com/VoltAgent/awesome-design-md`
- 适合谁先看：还没定方向、想先横向刷热门、或者不知道该从哪个品牌风格开始的人。
- 推荐首次使用顺序：
  1. 先打开“风格总览（Style Gallery）”
  2. 再收敛出 1 到 3 个候选风格
  3. 再运行推荐、输出 `DESIGN.md` 或 `UI-REFACTOR.md`

## 风格总览（Style Gallery）

这是这个 skill 的首个入口，而不是附带页面。它的作用是让用户先浏览，再决策，而不是一上来就读脚本说明。

风格来源需要明确说明：本地总览和推荐流程基于原项目 `getdesign.md / awesome-design-md` 的公开风格资料构建；对外展示或介绍这个 skill 时，默认应保留原项目地址说明。

开源仓库首页默认使用双语 README 发布页风格，而不是内部脚本说明书风格；如果用户要更新 GitHub 首页介绍，优先修改 `README.md` 的发布页结构，不要把 SKILL 文档原样搬上去。

本地总览现已支持：

- 中文默认浏览
- 一键切换 English
- 页面顶部热门总榜
- 各分类热门榜
- 完整风格卡筛选与预览

首次探索阶段建议优先提醒用户打开总览页，尤其当用户还在说“先看看有哪些风格”“给我几个方向”“我还没想好是 Apple 还是 Linear”时，不要直接跳进脚本细节。

## 何时使用

- 用户还没有定风格，需要先看 2 到 3 个视觉方向。
- 用户点名了一个风格，但希望知道是否还有更合适或更稳的备选。
- 用户给了仓库、页面截图、PRD、页面草图，希望先做设计定位，再进入实现。
- 用户已有项目，需要在尽量保留结构与交互的前提下升级 UI。
- 用户在“苹果风 / 耐克风 / Vercel 风 / Stripe 风 / Linear 风”之间犹豫。
- 用户已经看完推荐，想把选中的风格转成可落地的 `DESIGN.md` 或 `UI-REFACTOR.md` 初稿。

## 工作流

1. 提取输入信号，并判断 `project_mode` 是 `greenfield` 还是 `refactor`。
2. 归一化为项目画像。
3. 若是 `refactor`，先做现状诊断，补齐 `current_ui_findings / existing_pages / component_inventory / refactor_scope`。
4. 运行推荐脚本产出 3 个候选。
5. 渲染风格卡并附预览链接；`refactor` 模式额外展示“改造收益 / 难度 / 风险”。
6. 若用户确认风格，输出 `DESIGN.md` 或 `UI-REFACTOR.md` 草稿。
7. 给出下一步建议，而不是直接写代码。

## 输入优先级

始终按这个顺序决策：

1. 用户显式约束
2. 页面截图信号
3. 仓库结构信号
4. 现有 UI 问题诊断
5. 通用默认

### 用户显式约束

- 明确点名某个风格时，不要跳过推荐。
- 将该风格强制纳入结果集，再补 2 个相邻但不完全重复的备选。
- 输出时说明“为什么保留用户指定风格，以及另外两种风格分别解决什么问题”。

### 截图信号

优先观察：

- 视觉密度：低 / 中 / 高
- 亮暗倾向：浅色 / 深色 / 混合
- 排版张力：克制 / 编辑感 / 夸张 / 广告感
- 图片权重：低 / 中 / 高
- 产品气质：工具型 / 品牌型 / 内容型 / 电商型

若用户给了本地图片路径，可直接读取图片；若是对话里附图，也优先依据图像判断，而不是只看文字描述。先按 `references/screenshot-checklist.md` 提取信号，再写入 `screenshot_signals`。

### 仓库结构信号

优先提取：

- 技术栈与页面类型
- 组件密度与交互复杂度
- 是否偏 SaaS 控制台、编辑器、营销站、电商、媒体、作品集
- 是否已有深色工具界面、侧边栏、数据面板、卡片网格、摄影大图

推荐先读取 `references/analysis-rubric.md`，再将信号写成 JSON 供脚本使用。

### 现状诊断信号

当任务是已有项目改造时，额外沉淀：

- `current_ui_findings`：当前 UI 的主要问题，如层级混乱、密度失衡、组件语言不统一、品牌感不足。
- `existing_pages`：现有页面职责，如 `dashboard / editor / settings / marketing`。
- `component_inventory`：现有主要组件，如 `sidebar / topbar / data table / card / form / modal`。
- `refactor_scope`：改造边界，如“仅视觉层”“允许布局调整”“允许组件重组但不改信息架构”。

## 产出规则

每次固定输出 3 张风格卡，顺序为：

1. 最推荐
2. 次推荐
3. 对照项

每张卡至少包含：

- 风格名
- 一句话白话印象
- 为什么适合当前项目
- 这类风格通常长什么样
- 主要风险或不适配点
- 官方预览链接
- 本地说明卡字段

本地说明卡字段固定为：

- 主色倾向
- 排版气质
- 版式密度
- 典型适用页面
- 情绪关键词

若 `project_mode=refactor`，每张卡还必须包含：

- 改造收益
- 改造难度
- 兼容风险

## 输出硬规则

- 无论用户是否明确点名某个风格，最终都必须完整输出 **3 张风格卡**，不能只讲用户点名的那一张。
- 当用户指定某个风格时，该风格必须保留在结果里，同时再补 2 个相邻但不完全重复的备选。
- 当用户仍处于“先看看有哪些风格”“先帮我挑方向”的阶段，优先提醒可打开 `风格总览（Style Gallery）.html`，不要一上来就把注意力带到脚本和参数。
- 运行了 `scripts/render_style_cards.py` 后，默认应将其生成的 Markdown **原样用于最终回复**，不要再压缩成一句话摘要，否则容易把第 2、3 张卡吞掉。
- 如果要在 Codex 中显示本地 SVG 预览卡，必须保留 `![alt](/absolute/path/to/file.svg)` 这种 Markdown 图片语法。
- 不要把本地图片 Markdown 放进代码块、行内代码或纯文本说明里，否则 Codex 不会渲染图片。
- 如果某张卡没有本地缩略图，也要正常输出该卡的文字信息，不能因此减少候选数量。
- 若本次输出要直接发给用户，推荐先把 Markdown 写到临时文件，再运行 `scripts/verify_rendered_cards.py` 做一轮结果自检；校验没过时，不要直接交付。

## 脚本

### 1. 刷新风格目录

当需要同步上游仓库时，运行：

```bash
python3 scripts/build_style_catalog.py
```

这会从 `awesome-design-md` 的 README 生成：

- `references/style-catalog.json`
- `references/style-catalog.md`

### 2. 生成输入骨架

先准备一个输入 JSON，再运行推荐脚本：

```bash
python3 scripts/recommend_styles.py --input /tmp/style-input.json
```

输入 JSON 结构示例：

```json
{
  "user_request": "帮我给 AI 画布工具挑风格",
  "project_mode": "greenfield",
  "explicit_styles": ["Apple"],
  "repo_signals": {
    "page_types": ["editor", "dashboard"],
    "ui_density": "high",
    "surfaces": "dark",
    "tone": ["tooling", "professional"],
    "keywords": ["canvas", "workflow", "sidebar"]
  },
  "screenshot_signals": {
    "brightness": "dark",
    "ui_density": "high",
    "image_weight": "low",
    "mood": ["minimal", "precise"],
    "keywords": ["panel", "editor", "canvas"]
  }
}
```

也可以先用脚本生成一个输入骨架：

```bash
python3 scripts/bootstrap_profile.py \
  --request "帮我给 AI 画布工具挑风格" \
  --style Apple \
  --page-type editor \
  --page-type dashboard \
  --density high \
  --surface dark \
  --repo-keyword canvas \
  --repo-keyword sidebar
```

如果是已有项目改造，额外补上：

```bash
python3 scripts/bootstrap_profile.py \
  --request "给已有编辑器项目升级 UI，尽量保留结构" \
  --project-mode refactor \
  --page-type editor \
  --page-type dashboard \
  --existing-page editor \
  --existing-page dashboard \
  --component sidebar \
  --component modal \
  --component "data table" \
  --refactor-scope "允许布局调整和组件重组，但不改核心信息架构"
```

### 2.5 诊断已有项目 UI

当 `project_mode=refactor` 时，先运行：

```bash
python3 scripts/diagnose_refactor.py --input /tmp/style-input.json
```

这会补齐：

- `current_ui_findings`
- `existing_pages`
- `component_inventory`
- `refactor_scope`

### 3. 渲染风格卡

```bash
python3 scripts/render_style_cards.py --input /tmp/style-recommendations.json
```

若命中高频风格，输出会自动附带本地缩略图卡路径。`refactor` 模式会额外展示“改造收益 / 难度 / 风险”。

默认内建校验：

- 候选必须正好 3 张
- 若用户指定过风格，最终结果里必须保留至少 1 张指定风格
- 对于存在本地 SVG 的卡，输出里必须真的包含可渲染的图片 Markdown

如需显式跳过，仅在调试时使用：

```bash
python3 scripts/render_style_cards.py --input /tmp/style-recommendations.json --skip-validation
```

### 3.2 校验渲染结果

推荐把渲染结果先写入临时 Markdown，再检查一次：

```bash
python3 scripts/render_style_cards.py \
  --input /tmp/style-recommendations.json \
  --output /tmp/style-cards.md

python3 scripts/verify_rendered_cards.py \
  --input /tmp/style-recommendations.json \
  --markdown /tmp/style-cards.md
```

通过时输出 `PASS`，失败时输出 `FAIL` 和缺失项。

### 3.3 一键渲染并校验

如果你不想手动串两步，直接用：

```bash
python3 scripts/render_and_verify_cards.py \
  --input /tmp/style-recommendations.json \
  --output /tmp/style-cards.md
```

这个脚本会：

- 先渲染最终 Markdown
- 再立即检查 3 张卡、指定风格保留情况、SVG 图片 Markdown
- 校验通过后输出 `PASS`
- 校验失败后输出 `FAIL` 并阻断交付

### 3.5 生成本地风格缩略图

```bash
python3 scripts/generate_thumbnail_cards.py
```

默认会为当前 catalog 中的全部风格生成本地 SVG 缩略图。

### 3.6 审查缩略图是否匹配官方预览

```bash
python3 scripts/audit_thumbnails.py
```

该脚本会：

- 抓取官方预览页并生成官方风格指纹基线
- 抽取本地 SVG 缩略图指纹
- 输出一致性审查报告
- 对未通过项尝试按审查配置重生成一轮
- 将 `audit_status / audit_score / audit_version` 写回缩略图 manifest

生成产物：

- `references/style-audit-baseline.json`
- `references/style-audit-report.json`
- `references/style-audit-report.md`

注意：

- gallery 小卡主图默认回到本地 SVG 路线
- 官方缩略图保留为幕后校准与人工复核资源，不再占主视觉

### 3.7 生成官方缩略图

```bash
python3 scripts/generate_official_thumbnails.py
```

该脚本会：

- 针对全部风格抓取官方预览首屏
- 统一裁成 gallery 使用的缩略图比例
- 输出到 `assets/official-thumbnails/`
- 将 `official_thumb_path` 写回缩略图 manifest，供审查和人工复核使用

注意：

- gallery 小卡主图默认仍使用本地 SVG
- 官方缩略图只作为幕后校准依据，不再占小卡主视觉
- 官方缩略图不代表本地 SVG 已通过真实性审查；真实性仍以审查状态为准

### 3.8 生成本地风格总览页

```bash
python3 scripts/build_style_gallery.py
```

默认生成：

- `风格总览（Style Gallery）.html`
- `风格总览（Style Gallery）/`
- `assets/gallery/style-gallery.html`

注意：

- 这里记录的是“如何重新生成总览页”，不是新用户的首次入口说明。
- 首次使用时，应优先把用户引导到前面的“风格总览（Style Gallery）”章节。

该页面支持：

- 中文 / English 切换
- 页面顶部热门总榜
- 各分类热门榜
- 按名称搜索
- 按分类筛选
- 按布局筛选
- 直接查看本地 SVG 缩略图
- 跳转官方预览页

### 3.9 生成 README / GitHub 预览图

```bash
python3 scripts/build_github_preview.py
```

该脚本现在会：

- 先重建当前总览页，确保截图来源是最新版本
- 再从当前总览页实时截取“热门总榜”和“分类热门”
- 最后生成 `assets/gallery/previews/style-gallery-github-preview.png`

注意：

- GitHub 预览图不再依赖旧的静态 PNG 作为真源
- 第一印象必须以当前总览页实际卡片为准，而不是示意性拼图
- 若 README 展示图与当前总览页不一致，优先重跑这个脚本而不是手工替换图片

推荐固定顺序：

```bash
python3 scripts/build_style_catalog.py
python3 scripts/generate_thumbnail_cards.py
python3 scripts/audit_thumbnails.py
python3 scripts/generate_official_thumbnails.py
python3 scripts/build_style_gallery.py
```

### 3.9 批量补齐 prompt blocks

当你已经引入结构化提示词层，并希望为 catalog 中的全部风格补齐 prompt block 时，运行：

```bash
python3 scripts/generate_prompt_blocks.py
```

默认行为：

- 读取 `references/style-catalog.json`
- 自动为缺失风格生成 `references/prompt-blocks/<style-slug>.json`
- 保留已经人工优化过的高频风格 block，不覆盖现有文件

如需从 catalog 重新生成全部 block，仅在确认已有人工修改已备份时使用：

```bash
python3 scripts/generate_prompt_blocks.py --force
```

### 4. 生成 DESIGN.md 草稿

用户确定风格后，再运行：

```bash
python3 scripts/draft_design_md.py \
  --input /tmp/style-recommendations.json \
  --style Apple
```

若不传 `--style`，默认取第一名推荐。

### 4.2 生成结构化提示词

当你已经选定风格，想给下游实现 skill 一个更稳定的 handoff 时，运行：

```bash
python3 scripts/build_style_prompt.py \
  --input /tmp/style-recommendations.json \
  --style Apple \
  --format design-markdown
```

若当前任务是已有项目 UI 改造，可改成：

```bash
python3 scripts/build_style_prompt.py \
  --input /tmp/style-recommendations.json \
  --style Linear \
  --format refactor-markdown
```

该脚本会：

- 从 `references/prompt-blocks/` 读取高频风格的结构化提示词 block
- 对未覆盖的风格按推荐结果和项目画像自动兜底
- 生成可嵌入 `DESIGN.md` 或 `UI-REFACTOR.md` 的提示词段落

### 4.5 生成 UI-REFACTOR.md 草稿

当任务是已有项目改造时，用户确定风格后运行：

```bash
python3 scripts/draft_ui_refactor_md.py \
  --input /tmp/style-recommendations.json \
  --style Linear
```

若不传 `--style`，默认取第一名推荐。

### 4.8 开源前红队测试

若你准备在开源前验证这个 skill 是否真的好用，而不是只看脚本能跑，使用：

```bash
python3 scripts/scaffold_red_team_workspace.py --iteration iteration-1
```

相关资产：

- 用例集：`evals/evals.json`
- 评审清单：`evals/red-team-checklist.md`
- 默认工作区：`../style-compass-workspace/iteration-1`

## 结果后的下一步

- 用户已经选定风格：将该风格交给 `前端界面设计（Frontend Design）` 或对应单风格 skill 继续实现。
- 用户已经选定风格，且是已有项目改造：先生成 `UI-REFACTOR.md`，再把页面级 / 组件级任务单交给 `前端界面设计（Frontend Design）`。
- 用户仍在犹豫：重点比较前两名的气质与风险，不要立刻跳到代码实现。
- 用户要直接落成 `DESIGN.md`：先用本 skill 定方向，再调用 `scripts/draft_design_md.py` 生成初稿，不要在方向未定时直接写规范。

## 边界

- 本 skill 负责推荐、解释和改造方案，不直接修改项目代码。
- `refactor` 模式会输出半落地方案，但仍不直接改项目代码。
- 默认不生成真实截图缩略图，只提供本地说明卡和官方预览链接。
- 高频风格可使用本地 SVG 缩略图卡，作为更直观的近似预览。
- 项目信号不足时仍给 3 个推荐，但必须明确说明置信度较低。
- `DESIGN.md` 和 `UI-REFACTOR.md` 都是起点，不替代最终设计规范；复杂项目仍要人工补充组件状态、响应式策略和禁用项。

## 参考文件

- 分析规则：`references/analysis-rubric.md`
- 截图抽取清单：`references/screenshot-checklist.md`
- 风格目录：`references/style-catalog.md`
- 提示词结构：`references/prompt-schema.md`
- DESIGN 模板：`references/design-draft-template.md`
- UI 改造模板：`references/ui-refactor-draft-template.md`
- 说明卡模板：`assets/cards/style-card-template.md`
- 本地总览页入口：`风格总览（Style Gallery）.html`
- 本地总览文件夹：`风格总览（Style Gallery）/`
- 实际构建页：`assets/gallery/style-gallery.html`
- GitHub 预览图生成脚本：`scripts/build_github_preview.py`
- 开源入口页：`README.md`
- 红队用例：`evals/evals.json`
- 红队清单：`evals/red-team-checklist.md`

# 风格提示词结构

给风格罗盘（style-compass）补提示词层时，优先写成结构化 block，再由脚本拼装成 `DESIGN.md` 与 `UI-REFACTOR.md` 中的交接内容。

## 目标

- 不把 `SKILL.md` 变成大段提示词仓库。
- 把“风格方向”转成可交给实现 skill 的稳定输入。
- 允许只覆盖高频风格，其他风格走脚本兜底。

## 存放位置

- 路径：`references/prompt-blocks/<style-slug>.json`
- 例如：`references/prompt-blocks/apple.json`
- 全量补齐时，优先运行 `scripts/generate_prompt_blocks.py` 批量生成缺失 block，再按需要人工微调高频风格。

## JSON 字段

```json
{
  "name": "Apple",
  "style_keywords": ["克制", "高级感", "精密排版"],
  "negative_constraints": [
    "不要滥用彩色渐变",
    "不要让每个模块都抢主视觉"
  ],
  "layout_bias": [
    "主视觉区保持大留白和强聚焦",
    "内容区按稳定模块节奏展开"
  ],
  "component_tone": {
    "button": "主按钮克制但精致",
    "card": "卡片像产品展台，不像后台灰盒",
    "input": "输入区尽量安静，不抢内容层级",
    "navigation": "导航语气克制，层级明确",
    "panel": "面板优先干净边界和均匀留白"
  },
  "image_direction": "优先产品主体、材质和留白，不做碎装饰拼贴。",
  "best_for_pages": ["landing-page", "product-site", "creative-tool"],
  "avoid_for_pages": ["dense-dashboard"],
  "page_prompt_examples": {
    "landing-page": "按 Apple 风格实现产品落地页，主视觉保持克制留白和高质量产品主体。",
    "product-site": "按 Apple 风格实现产品官网，控制文案、图片和模块节奏。"
  },
  "component_prompt_examples": {
    "button": "按钮要精致克制，不要做成营销海报式 CTA。",
    "panel": "面板像精密容器，不要堆砌阴影和描边。"
  },
  "handoff_template": "按 Apple 风格落地页面，优先精密层级、留白和主内容聚焦。"
}
```

## 字段说明

- `style_keywords`
  这组词会进入 `Agent Prompt Guide`，用于描述风格气质。
- `negative_constraints`
  这组词用于约束实现，避免只学到表层配色。
- `layout_bias`
  描述页面骨架、模块节奏与留白方式。
- `component_tone`
  约束高频组件语气，建议至少覆盖 `button / card / input / navigation / panel`。
- `image_direction`
  描述插图、摄影、产品图或背景图的使用原则。
- `best_for_pages`
  说明该风格天然适配的页面类型。
- `avoid_for_pages`
  说明需要慎用的页面类型。
- `page_prompt_examples`
  页面级 prompt 示例，优先覆盖 `landing-page / dashboard / editor / docs / product-site`。
- `component_prompt_examples`
  组件级 prompt 示例，优先覆盖 `button / card / panel / navigation / form`。
- `handoff_template`
  当该风格需要更稳定的交接语气时，用它覆盖默认 handoff 开头。

## 实施原则

- 先覆盖高频风格：`Apple / Linear / Stripe / Vercel / Nike / Figma / Supabase`
- block 不求长，求稳定、可拼装。
- 缺字段时允许脚本兜底，但不要把空对象提交成长期状态。
- 新增 block 后，优先用 `scripts/build_style_prompt.py` 自检输出，再看是否需要补细节。
- 批量生成时默认保留已有人工优化文件，只补缺失项；确需重建时再使用覆盖模式。

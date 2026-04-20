# 截图抽取清单

当用户给你截图时，不要直接凭“感觉”下结论。先按这个清单把图像信号压缩成 `screenshot_signals`。

## 1. 先判断页面类型

- 是否像官网 Hero / 品牌页
- 是否像控制台 / 仪表盘
- 是否像编辑器 / 画布工具
- 是否像文档 / 教程页
- 是否像电商 / 商品详情页

若页面同时具备两类特征，保留 2 个 `page_types`。

## 2. 再判断视觉密度

- `low`：大留白、控件少、叙事主导
- `medium`：信息与展示平衡
- `high`：面板多、操作频繁、数据密

## 3. 再判断明暗与图片权重

- `brightness`：`light` / `dark` / `mixed`
- `image_weight`：`low` / `medium` / `high`

提示：

- 如果画面主要由按钮、输入框、表格、面板组成，通常 `image_weight=low`
- 如果摄影图、海报图、产品图主导第一屏，通常 `image_weight=high`

## 4. 提取排版与气质关键词

优先从这些词里选：

- `minimal`
- `precise`
- `editorial`
- `bold`
- `friendly`
- `cinematic`
- `luxury`
- `tooling`
- `playful`

## 5. 写入 JSON

建议结构：

```json
{
  "brightness": "dark",
  "image_weight": "low",
  "page_types": ["editor", "dashboard"],
  "mood": ["minimal", "precise", "tooling"],
  "keywords": ["panel", "canvas", "sidebar"]
}
```

## 6. 红旗

- 不要只因为“好看”就判断为 Apple。
- 不要只因为“黑色背景”就判断为 Linear。
- 不要把“有大图”自动等同于 Nike。
- 先看页面承担的任务，再看视觉风格。

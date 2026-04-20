#!/usr/bin/env python3
"""Draft a DESIGN.md file from style-compass recommendations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_style_prompt import build_prompt_bundle, render_design_prompt_guide

LABELS = {
    "low": "低",
    "medium": "中",
    "high": "高",
    "light": "浅色",
    "dark": "深色",
    "mixed": "混合",
    "landing-page": "营销落地页",
    "product-site": "产品官网",
    "creative-tool": "创意工具",
    "dashboard": "控制台 / 仪表盘",
    "editor": "编辑器 / 画布工具",
    "saas": "SaaS 产品页",
    "docs": "文档页",
    "brand-site": "品牌官网",
    "commerce": "电商页",
    "campaign": "活动专题页",
    "minimal": "极简",
    "premium": "高级",
    "cinematic": "电影感",
    "tooling": "工具感",
    "precise": "精准",
}


def humanize(items: list[str] | str) -> str:
    if isinstance(items, str):
        return LABELS.get(items, items)
    return "、".join(LABELS.get(item, item) for item in items)


def choose_entry(payload: dict, style: str | None, rank: int | None) -> dict:
    entries = payload["recommendations"]
    if style:
        for entry in entries:
            if entry["name"].lower() == style.lower():
                return entry
        raise SystemExit(f"Style not found in recommendations: {style}")
    if rank is not None:
        idx = max(1, rank) - 1
        if idx >= len(entries):
            raise SystemExit(f"Rank out of range: {rank}")
        return entries[idx]
    return entries[0]


def design_markdown(entry: dict, payload: dict) -> str:
    best_for = humanize(entry["best_for"][:3])
    moods = humanize(entry["mood_keywords"][:4])
    brightness = humanize(payload["profile"]["brightness"])
    density = humanize(payload["profile"]["ui_density"])
    request = payload["profile"]["user_request"]
    prompt_bundle = build_prompt_bundle(payload, entry)

    return f"""# DESIGN.md

## 1. Visual Theme & Atmosphere
- 整体气质：以 {entry['name']} 风格为主轴，保留 {entry['plain_impression']}
- 页面密度：当前项目建议采用 {density} 密度，避免脱离真实使用场景
- 设计哲学：优先服务于 {request} 的产品目标，不做无意义的纯装饰化模仿

## 2. Color Palette & Roles
- 主色：{entry['color_tendency']}
- 背景色：建议根据项目保持 {brightness} 倾向，并围绕主色做层级拆分
- 文本色：确保标题、正文、辅助信息形成清晰对比
- 强调色：仅在主 CTA、选中态、关键状态中使用
- 风险提示：{entry['risk_note']}

## 3. Typography Rules
- 标题字体气质：{entry['typography_tone']}
- 正文字体气质：保持清晰、稳定、可读，避免为了模仿而牺牲信息效率
- 字重与层级：Hero、区块标题、正文、辅助说明至少形成 4 级层级

## 4. Component Stylings
- Button：主按钮突出品牌方向，次按钮降一级，不要所有按钮都像主操作
- Card：围绕 {entry['name']} 的表面气质组织边框、圆角、阴影和留白
- Input：保持可读与可扫视优先，尤其是高密度工具页面
- Navigation：导航与内容区要有明确层级，不要只靠颜色硬分割
- Panel：适合当前风格的面板语气要统一，不混入无关视觉语言

## 5. Layout Principles
- 页面骨架：优先支持 {best_for}
- 间距系统：使用统一 spacing scale，避免局部随意写值
- 留白策略：结合 {entry['name']} 的风格倾向控制留白，而不是盲目放大或压缩

## 6. Depth & Elevation
- 表面层级：至少区分 base / raised / active 三层
- 边框与阴影：以当前风格的克制程度为准，不额外叠加无关发光和装饰

## 7. Do's and Don'ts
- Do：保留 {moods} 这些气质关键词，并让组件、排版、图像权重一致
- Do：在复杂功能页面里优先保证操作效率和信息结构
- Don't：只复制表层颜色或大图，不复制布局逻辑与节奏
- Don't：把推荐风格硬套到所有页面，忽略页面职责差异

## 8. Responsive Behavior
- Desktop：完整保留主骨架与层级关系
- Mobile：优先折叠次要装饰，保留核心操作路径和关键信息

{render_design_prompt_guide(prompt_bundle).rstrip()}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--style", help="Chosen style name")
    parser.add_argument("--rank", type=int, help="Chosen rank (1-based)")
    parser.add_argument("--output", help="Optional output path, defaults to stdout")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    entry = choose_entry(payload, args.style, args.rank)
    output = design_markdown(entry, payload)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

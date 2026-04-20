#!/usr/bin/env python3
"""Draft a UI-REFACTOR.md document from refactor recommendations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_style_prompt import build_prompt_bundle, render_refactor_prompt_guide

PAGE_LABELS = {
    "dashboard": "控制台 / 仪表盘",
    "editor": "编辑器 / 画布工具",
    "creative-tool": "创意工具",
    "docs": "文档页",
    "landing-page": "营销落地页",
    "brand-site": "品牌官网",
    "commerce": "电商页",
    "marketing": "营销页",
}

VISUAL_ONLY = {"landing-page", "brand-site", "marketing", "campaign", "product-site"}
DENSITY_TUNE = {"dashboard", "docs", "settings", "analytics", "commerce"}
REORDER = {"editor", "creative-tool", "workbench"}


def humanize(items: list[str] | str) -> str:
    if isinstance(items, str):
        return PAGE_LABELS.get(items, items)
    return "、".join(PAGE_LABELS.get(item, item) for item in items)


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


def classify_pages(existing_pages: list[str]) -> dict[str, list[str]]:
    mapping = {
        "visual_only": [],
        "density_and_hierarchy": [],
        "reorder_modules": [],
        "hold": [],
    }
    for page in existing_pages:
        if page in VISUAL_ONLY:
            mapping["visual_only"].append(page)
        elif page in DENSITY_TUNE:
            mapping["density_and_hierarchy"].append(page)
        elif page in REORDER:
            mapping["reorder_modules"].append(page)
        else:
            mapping["hold"].append(page)
    return mapping


def classify_components(components: list[str], entry: dict) -> dict[str, list[str]]:
    mood_keywords = set(entry.get("mood_keywords", []))
    keep = [item for item in components if item in {"sidebar", "topbar", "canvas", "toolbar", "data table", "form", "modal"}]
    redraw = [item for item in components if item in {"card", "panel", "hero", "feature card", "cta section", "pricing", "drawer", "grid"}]
    unify = [item for item in components if item in {"panel", "modal", "filter bar", "data table", "form", "tabs", "search", "dropdown"}]
    deprecated = []

    if mood_keywords & {"precise", "minimal", "tooling"}:
        deprecated.extend(["多套阴影和描边并存", "装饰性渐变滥用", "无规则圆角"])
    if mood_keywords & {"premium", "cinematic", "editorial", "bold"}:
        deprecated.extend(["默认后台灰卡片语气", "所有模块同权重排版", "弱化品牌区块"])

    return {
        "keep": dedupe(keep),
        "redraw": dedupe(redraw),
        "unify": dedupe(unify),
        "deprecated": dedupe(deprecated),
    }


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        value = str(item).strip()
        if not value:
            continue
        marker = value.lower()
        if marker in seen:
            continue
        seen.add(marker)
        ordered.append(value)
    return ordered


def render_bullets(items: list[str], fallback: str) -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def build_markdown(payload: dict, entry: dict) -> str:
    profile = payload["profile"]
    findings = profile.get("current_ui_findings", [])
    existing_pages = profile.get("existing_pages", []) or profile.get("page_types", [])
    components = profile.get("component_inventory", [])
    scope = profile.get("refactor_scope") or "优先视觉层和组件规范统一"
    page_mapping = classify_pages(existing_pages)
    component_mapping = classify_components(components, entry)
    assessment = entry.get("refactor_assessment", {})
    prompt_bundle = build_prompt_bundle(payload, entry)

    return f"""# UI-REFACTOR.md

## 1. 当前 UI 问题摘要
{render_bullets(findings[:6], "当前诊断信号不足，建议先补页面截图和组件清单。")}

- 改造范围：{scope}
- 目标风格：{entry['name']}，{entry['plain_impression']}
- 为什么选它：{entry['why_it_fits']}

## 2. 改造收益 / 难度 / 风险
- 改造收益：{assessment.get('benefit', {}).get('label', '中')}｜{assessment.get('benefit', {}).get('reason', '主要收益在于统一视觉语言和页面气质。')}
- 改造难度：{assessment.get('difficulty', {}).get('label', '中')}｜{assessment.get('difficulty', {}).get('reason', '主要工作集中在组件样式与页面节奏收敛。')}
- 兼容风险：{assessment.get('risk', {}).get('label', '中')}｜{assessment.get('risk', {}).get('reason', '风险主要来自局部页面与风格语气不完全一致。')}

## 3. 页面级改造映射
### 只换视觉语气
{render_bullets([humanize(item) for item in page_mapping['visual_only']], "营销或品牌页面可优先做视觉层升级。")}

### 允许调整密度和层级
{render_bullets([humanize(item) for item in page_mapping['density_and_hierarchy']], "优先在高频功能页统一层级、间距和状态语法。")}

### 允许重组模块顺序
{render_bullets([humanize(item) for item in page_mapping['reorder_modules']], "编辑器与复杂工作台可按操作优先级重排模块。")}

### 暂不建议先动
{render_bullets([humanize(item) for item in page_mapping['hold']], "权限、计费、低频后台页先跟随基础组件升级，不单独重做。")}

## 4. 组件级改造映射
### 保留结构，只重设视觉语言
{render_bullets(component_mapping['keep'], "保留导航、表单和核心工作流组件的结构，避免重写交互逻辑。")}

### 需要重画样式的组件
{render_bullets(component_mapping['redraw'], "按钮、卡片、面板和 CTA 区块优先重画样式。")}

### 需要统一规范的组件
{render_bullets(component_mapping['unify'], "统一输入、表格、弹层和筛选组件的边框、状态和间距规则。")}

### 不建议沿用的旧视觉模式
{render_bullets(component_mapping['deprecated'], "避免继续叠加零散装饰和多套视觉语法。")}

## 5. 视觉语言约束
- 主色倾向：{entry['color_tendency']}
- 排版气质：{entry['typography_tone']}
- 页面密度：保留 {profile.get('ui_density', 'medium')} 场景的使用效率，再按 {entry.get('layout_density', 'medium')} 的风格节奏收敛界面。
- 明暗规则：当前项目以 {profile.get('brightness', 'mixed')} 为底，逐步收敛到与 {entry['name']} 一致的容器层级和强调色使用方式。
- 边界：不把风格模仿扩成无必要的交互重构，先统一表面语言、层级、状态和模块秩序。

## 6. 实施优先级
1. 先统一设计 token：颜色、圆角、描边、阴影、间距、标题层级。
2. 再改高频组件：按钮、输入、卡片、表格、面板、导航。
3. 然后处理核心页面：{humanize(existing_pages[:3]) if existing_pages else '优先用户最高频的页面'}。
4. 最后再补品牌区块、空状态、插图或营销表达。

## 7. 交接给实现 skill 的任务单
- 以 {entry['name']} 风格为目标，先建立一套可复用 token，不直接逐页手涂。
- 页面级任务：优先处理 {humanize(existing_pages[:3]) if existing_pages else '高频核心页面'}，按“结构不乱、层级更清、品牌更稳”的顺序推进。
- 组件级任务：优先统一 {', '.join(component_mapping['unify'][:5]) if component_mapping['unify'] else '表单、表格、面板和弹层'}。
- 验收标准：同类组件不再出现多套圆角 / 阴影 / 状态色；关键页面首屏主次清晰；移动端不因装饰增加操作负担。

{render_refactor_prompt_guide(prompt_bundle).rstrip()}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--style", help="Chosen style name")
    parser.add_argument("--rank", type=int, help="Chosen rank (1-based)")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    entry = choose_entry(payload, args.style, args.rank)
    output = build_markdown(payload, entry)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

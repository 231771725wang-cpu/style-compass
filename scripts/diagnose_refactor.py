#!/usr/bin/env python3
"""Infer refactor-oriented diagnostics from project and screenshot signals."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

PAGE_COMPONENT_MAP = {
    "dashboard": ["sidebar", "topbar", "filter bar", "data table", "status card", "modal"],
    "editor": ["canvas", "toolbar", "sidebar", "properties panel", "layer panel", "modal"],
    "creative-tool": ["canvas", "toolbar", "sidebar", "panel", "asset tray"],
    "docs": ["docs sidebar", "toc", "code block", "tab switcher", "search"],
    "commerce": ["product grid", "product card", "filter bar", "price block", "cart drawer"],
    "landing-page": ["hero", "feature card", "cta section", "logo wall", "pricing"],
    "brand-site": ["hero", "story section", "media block", "cta section"],
    "marketing": ["hero", "feature card", "cta section", "testimonial"],
}

KEYWORD_COMPONENT_MAP = {
    "sidebar": "sidebar",
    "toolbar": "toolbar",
    "topbar": "topbar",
    "panel": "panel",
    "canvas": "canvas",
    "table": "data table",
    "grid": "grid",
    "filter": "filter bar",
    "chart": "chart",
    "modal": "modal",
    "drawer": "drawer",
    "form": "form",
    "hero": "hero",
    "pricing": "pricing",
    "card": "card",
}

PAGE_LABELS = {
    "dashboard": "dashboard",
    "editor": "editor",
    "creative-tool": "creative-tool",
    "docs": "docs",
    "commerce": "commerce",
    "landing-page": "landing-page",
    "brand-site": "brand-site",
    "marketing": "marketing",
}


def uniq(items: list[str]) -> list[str]:
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


def infer_existing_pages(payload: dict) -> list[str]:
    explicit = payload.get("existing_pages", [])
    repo = payload.get("repo_signals", {})
    shot = payload.get("screenshot_signals", {})
    pages: list[str] = []
    pages.extend(str(item) for item in explicit)
    pages.extend(str(item) for item in repo.get("page_types", []))
    pages.extend(str(item) for item in shot.get("page_types", []))
    return uniq([PAGE_LABELS.get(item, item) for item in pages])


def infer_components(payload: dict, existing_pages: list[str]) -> list[str]:
    explicit = payload.get("component_inventory", [])
    repo = payload.get("repo_signals", {})
    shot = payload.get("screenshot_signals", {})
    components: list[str] = [str(item) for item in explicit]
    for page in existing_pages:
        components.extend(PAGE_COMPONENT_MAP.get(page, []))
    keywords = list(repo.get("keywords", [])) + list(shot.get("keywords", []))
    for keyword in keywords:
        lowered = str(keyword).strip().lower()
        for token, component in KEYWORD_COMPONENT_MAP.items():
            if token in lowered:
                components.append(component)
    return uniq(components)


def default_refactor_scope(payload: dict, existing_pages: list[str]) -> str:
    explicit = str(payload.get("refactor_scope", "")).strip()
    if explicit:
        return explicit
    if "editor" in existing_pages or "dashboard" in existing_pages:
        return "允许布局调整和组件重组，但不改核心信息架构"
    return "优先视觉层和组件规范统一，必要时微调模块层级"


def infer_findings(payload: dict, existing_pages: list[str], components: list[str], scope: str) -> list[str]:
    repo = payload.get("repo_signals", {})
    shot = payload.get("screenshot_signals", {})
    findings: list[str] = [str(item) for item in payload.get("current_ui_findings", [])]

    brightness = str(shot.get("brightness") or repo.get("surfaces") or "").lower()
    density = str(shot.get("ui_density") or repo.get("ui_density") or "").lower()
    image_weight = str(shot.get("image_weight") or "").lower()

    if "dashboard" in existing_pages or "editor" in existing_pages:
        findings.append("功能界面占比高，改造优先级应放在层级、状态和连续操作效率，而不是表层装饰。")
    if density == "high":
        findings.append("当前信息密度偏高，需先统一 spacing、分组节奏和主次强调，避免面板互相抢注意力。")
    elif density == "low" and ("dashboard" in existing_pages or "docs" in existing_pages):
        findings.append("页面密度偏低，复杂信息承载可能显得松散，建议补强层级和扫描路径。")

    if brightness == "mixed":
        findings.append("浅深表面并置风险较高，需先收敛背景层级和容器语法，避免视觉噪音。")
    elif brightness == "dark" and ("landing-page" in existing_pages or "brand-site" in existing_pages):
        findings.append("深色基底能强化氛围，但需要额外约束品牌信息层级，否则首屏容易只剩情绪没有信息。")

    if image_weight == "low" and any(page in existing_pages for page in ("landing-page", "brand-site", "marketing")):
        findings.append("品牌表达可能偏弱，若目标包含升级感知，需要通过排版张力和重点视觉模块补足记忆点。")
    if image_weight == "high" and any(page in existing_pages for page in ("dashboard", "editor", "docs")):
        findings.append("视觉素材权重偏高，可能压缩工具效率，建议把主视觉限制在入口区和空状态。")

    if len(components) >= 6:
        findings.append("组件族较多，边框、圆角、阴影、状态色和交互反馈容易出现多套语言并存。")

    if not payload.get("screenshot_signals"):
        findings.append("缺少截图信号，当前问题判断主要依据仓库结构，视觉结论需要人工复核。")
    elif not any(shot.get(key) for key in ("brightness", "ui_density", "image_weight", "mood", "keywords", "page_types")):
        findings.append("截图信号不足，当前结论更偏结构推断，落地前应再补一轮视觉核对。")
    if not repo:
        findings.append("缺少仓库结构信号，页面与组件盘点可能不完整，不应假装理解实现细节。")

    if "不改核心信息架构" in scope:
        findings.append("这次改造应以视觉系统和模块秩序为主，不把任务扩大成信息架构重构。")

    return uniq(findings)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input profile JSON")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    existing_pages = infer_existing_pages(payload)
    components = infer_components(payload, existing_pages)
    scope = default_refactor_scope(payload, existing_pages)
    findings = infer_findings(payload, existing_pages, components, scope)

    payload["project_mode"] = payload.get("project_mode") or "refactor"
    payload["existing_pages"] = existing_pages
    payload["component_inventory"] = components
    payload["refactor_scope"] = scope
    payload["current_ui_findings"] = findings

    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

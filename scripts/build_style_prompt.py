#!/usr/bin/env python3
"""Build structured style handoff prompts from style-compass recommendations."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOCK_DIR = ROOT / "references" / "prompt-blocks"

DEFAULT_COMPONENT_TONE = {
    "button": "按钮需要明确主次，不靠堆装饰制造存在感。",
    "card": "卡片应服务信息层级，不要把所有卡片做成同权重视觉块。",
    "input": "输入控件优先可读、可扫视和状态清楚。",
    "navigation": "导航负责稳住结构秩序，不承担多余表演。",
    "panel": "面板要统一表面语言、边界和留白。",
}

SUPPORTED_PROMPT_PAGE_TYPES = {
    "landing-page",
    "brand-site",
    "product-site",
    "marketing",
    "commerce",
    "campaign",
    "dashboard",
    "docs",
    "settings",
    "analytics",
    "developer-tool",
    "editor",
    "creative-tool",
}

PAGE_TYPE_ALIASES = {
    "saas": "product-site",
    "ai-platform": "product-site",
    "editorial": "landing-page",
    "workbench": "editor",
    "launch-page": "landing-page",
    "pricing": "product-site",
    "showcase": "brand-site",
    "collaboration": "product-site",
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


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


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


def load_prompt_block(style_name: str) -> dict:
    path = BLOCK_DIR / f"{slugify(style_name)}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_page_list(items: list[str]) -> list[str]:
    normalized: list[str] = []
    for item in items:
        value = PAGE_TYPE_ALIASES.get(item, item)
        if value in SUPPORTED_PROMPT_PAGE_TYPES:
            normalized.append(value)
    return dedupe(normalized)


def fallback_negative_constraints(entry: dict, profile: dict) -> list[str]:
    page_types = set(profile.get("page_types", [])) | set(profile.get("existing_pages", []))
    moods = set(entry.get("mood_keywords", []))
    negatives = [
        "不要只复制表层颜色、圆角或大图，忽略布局逻辑与模块节奏。",
        "不要让所有模块同权重，必须保留明确主次。",
    ]
    if profile.get("project_mode") == "refactor":
        negatives.append("不要把这次视觉升级扩成无必要的产品重构。")
    if page_types & {"dashboard", "editor", "docs", "developer-tool"}:
        negatives.append("不要为了品牌表达牺牲扫描效率和高频操作路径。")
    if entry.get("brightness") == "dark":
        negatives.append("不要把深色层级压成同一块黑面，必须保留表面差异。")
    if moods & {"premium", "cinematic", "bold", "editorial"}:
        negatives.append("不要把品牌张力做成浮夸海报，仍需服务真实页面职责。")
    return dedupe(negatives)


def fallback_layout_bias(entry: dict, profile: dict) -> list[str]:
    page_types = set(profile.get("page_types", [])) | set(profile.get("existing_pages", []))
    layout = []
    if page_types & {"landing-page", "brand-site", "product-site", "campaign", "marketing", "commerce"}:
        layout.extend(
            [
                "首屏需要明确主视觉和价值主张，不要一开始就掉进零散模块堆叠。",
                "区块之间要有节奏断点，让叙事和转化路径都清楚。",
            ]
        )
    if page_types & {"dashboard", "editor", "docs", "settings", "analytics", "developer-tool"}:
        layout.extend(
            [
                "优先稳定骨架与高频操作路径，模块秩序比装饰更重要。",
                "用间距、边界和对齐建立层级，不要靠堆特效解决结构问题。",
            ]
        )
    density = profile.get("ui_density", "medium")
    if density == "high":
        layout.append("高密度页面要保留扫描效率，不盲目为了风格而拉大留白。")
    elif density == "low":
        layout.append("低密度页面要避免信息过散，留白服务聚焦而不是放空。")
    if not layout:
        layout.append(f"围绕 {entry['name']} 风格的模块节奏组织页面，先稳住骨架，再叠加气质。")
    return dedupe(layout)


def fallback_component_tone(entry: dict) -> dict:
    tone = dict(DEFAULT_COMPONENT_TONE)
    style_name = entry["name"]
    tone["button"] = f"按钮要体现 {style_name} 的气质，但主次必须清楚。"
    tone["card"] = f"卡片围绕 {style_name} 的表面语气组织边界、留白和状态。"
    tone["panel"] = f"面板需要有 {style_name} 的容器感，但不能破坏信息秩序。"
    return tone


def fallback_page_prompt_examples(entry: dict, profile: dict) -> dict[str, str]:
    raw_pages = dedupe(list(profile.get("page_types", [])) + list(profile.get("existing_pages", [])) + list(entry.get("best_for", [])))
    pages: list[str] = []
    for page in raw_pages:
        normalized = PAGE_TYPE_ALIASES.get(page, page)
        if normalized in SUPPORTED_PROMPT_PAGE_TYPES:
            pages.append(normalized)
    pages = dedupe(pages)
    examples: dict[str, str] = {}
    for page in pages[:4]:
        if page in {"landing-page", "brand-site", "product-site", "marketing", "commerce", "campaign"}:
            examples[page] = (
                f"按 {entry['name']} 风格实现 {page} 页面，先稳住主视觉、标题层级和转化路径，"
                "再引入品牌气质，不要让所有区块同权重。"
            )
        elif page in {"dashboard", "docs", "settings", "analytics", "developer-tool"}:
            examples[page] = (
                f"按 {entry['name']} 风格实现 {page} 页面，优先保证扫描效率、状态清晰和模块秩序，"
                "风格表达放在表面语言与层级里。"
            )
        elif page in {"editor", "creative-tool"}:
            examples[page] = (
                f"按 {entry['name']} 风格实现 {page} 页面，保留工作流效率，"
                "重点统一侧栏、工具栏、面板和主工作区的表面语气。"
            )
        else:
            examples[page] = f"按 {entry['name']} 风格实现 {page} 页面，先统一骨架、层级和组件语气。"
    return examples


def fallback_component_prompt_examples(entry: dict) -> dict[str, str]:
    return {
        "button": f"把按钮做成 {entry['name']} 风格，但保留明确主次、状态反馈和点击目标。",
        "card": f"把卡片做成 {entry['name']} 风格，重点控制边界、留白和信息层级。",
        "panel": f"把面板做成 {entry['name']} 风格，强调容器秩序，不要无规则叠阴影。",
        "navigation": f"把导航做成 {entry['name']} 风格，让结构稳定清楚，不要抢走主内容注意力。",
        "form": f"把表单做成 {entry['name']} 风格，优先可读性、状态反馈和输入效率。",
    }


def select_prompt_examples(examples: dict[str, str], profile: dict, fallback_limit: int = 3) -> dict[str, str]:
    preferred = dedupe(list(profile.get("page_types", [])) + list(profile.get("existing_pages", [])))
    ordered: list[tuple[str, str]] = []
    seen: set[str] = set()
    for key in preferred:
        if key in examples:
            ordered.append((key, examples[key]))
            seen.add(key)
    for key, value in examples.items():
        if key in seen:
            continue
        ordered.append((key, value))
    return dict(ordered[:fallback_limit])


def build_prompt_bundle(payload: dict, entry: dict) -> dict:
    profile = payload["profile"]
    block = load_prompt_block(entry["name"])
    extra_keywords = entry.get("mood_keywords_zh") or entry.get("mood_keywords", [])
    style_keywords = dedupe(list(block.get("style_keywords", [])) + list(extra_keywords))
    negative_constraints = dedupe(list(block.get("negative_constraints", [])) or fallback_negative_constraints(entry, profile))
    layout_bias = dedupe(list(block.get("layout_bias", [])) or fallback_layout_bias(entry, profile))

    component_tone = fallback_component_tone(entry)
    component_tone.update(block.get("component_tone", {}))

    page_examples = fallback_page_prompt_examples(entry, profile)
    page_examples.update(block.get("page_prompt_examples", {}))
    page_examples = select_prompt_examples(page_examples, profile)

    component_examples = fallback_component_prompt_examples(entry)
    component_examples.update(block.get("component_prompt_examples", {}))

    best_for = normalize_page_list(list(block.get("best_for_pages", [])) + list(entry.get("best_for", [])))
    avoid_for = normalize_page_list(list(block.get("avoid_for_pages", [])))

    one_liner = (
        f"按 {entry['name']} 风格实现页面，但优先服务当前项目的真实信息结构、操作效率和主次层级。"
    )
    handoff_prefix = block.get("handoff_template") or f"按 {entry['name']} 风格落地页面。"
    page_focus = dedupe(list(profile.get("page_types", [])) + list(profile.get("existing_pages", [])))
    page_focus_text = "、".join(page_focus[:3]) if page_focus else "当前核心页面"
    handoff_prompt = (
        f"{handoff_prefix} 优先处理 {page_focus_text}，先统一颜色、圆角、描边、阴影和标题层级，"
        "再处理按钮、输入、卡片、面板和导航的视觉语言。"
    )
    if profile.get("project_mode") == "refactor":
        handoff_prompt += " 保留主要信息架构和核心交互逻辑，不要把这次改造扩大成产品重构。"
    else:
        handoff_prompt += " 先稳住页面骨架和模块节奏，再补品牌表达和情绪细节。"

    return {
        "style": entry["name"],
        "one_liner": one_liner,
        "style_keywords": style_keywords,
        "negative_constraints": negative_constraints,
        "layout_bias": layout_bias,
        "component_tone": component_tone,
        "image_direction": block.get("image_direction", "图像与背景只服务主叙事，不抢走信息结构。"),
        "best_for_pages": best_for,
        "avoid_for_pages": avoid_for,
        "page_prompt_examples": page_examples,
        "component_prompt_examples": component_examples,
        "handoff_prompt": handoff_prompt,
    }


def render_design_prompt_guide(bundle: dict) -> str:
    component_lines = "\n".join(f"- {key}：{value}" for key, value in bundle["component_tone"].items())
    page_lines = "\n".join(f"- `{key}`：{value}" for key, value in bundle["page_prompt_examples"].items())
    avoid_text = "、".join(bundle["avoid_for_pages"]) if bundle["avoid_for_pages"] else "无硬性禁用页面，但需要按页面职责判断。"
    return f"""## 9. Agent Prompt Guide
- 一句话指令：{bundle['one_liner']}
- 风格关键词：{'、'.join(bundle['style_keywords'])}
- 禁止项：{'；'.join(bundle['negative_constraints'][:4])}

### 页面骨架偏好
{chr(10).join(f"- {item}" for item in bundle['layout_bias'])}

### 组件语气
{component_lines}

### 图像与背景方向
- {bundle['image_direction']}

### 最适合页面
- {'、'.join(bundle['best_for_pages'][:5])}

### 慎用页面
- {avoid_text}

### 页面示例提示词
{page_lines}

### 组件示例提示词
{chr(10).join(f"- `{key}`：{value}" for key, value in bundle['component_prompt_examples'].items())}

### 总体 Handoff
- {bundle['handoff_prompt']}
"""


def render_refactor_prompt_guide(bundle: dict) -> str:
    page_lines = "\n".join(f"- `{key}`：{value}" for key, value in bundle["page_prompt_examples"].items())
    component_lines = "\n".join(f"- `{key}`：{value}" for key, value in bundle["component_prompt_examples"].items())
    return f"""## 8. 实现提示词
- 总体 handoff：{bundle['handoff_prompt']}
- 风格关键词：{'、'.join(bundle['style_keywords'])}
- 禁止项：{'；'.join(bundle['negative_constraints'][:4])}

### 页面骨架偏好
{chr(10).join(f"- {item}" for item in bundle['layout_bias'])}

### 组件语气
{chr(10).join(f"- {key}：{value}" for key, value in bundle['component_tone'].items())}

### 页面级 prompt 示例
{page_lines}

### 组件级 prompt 示例
{component_lines}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--style", help="Chosen style name")
    parser.add_argument("--rank", type=int, help="Chosen rank (1-based)")
    parser.add_argument(
        "--format",
        choices=["json", "design-markdown", "refactor-markdown"],
        default="json",
        help="Output format",
    )
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    entry = choose_entry(payload, args.style, args.rank)
    bundle = build_prompt_bundle(payload, entry)

    if args.format == "json":
        output = json.dumps(bundle, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "design-markdown":
        output = render_design_prompt_guide(bundle) + "\n"
    else:
        output = render_refactor_prompt_guide(bundle) + "\n"

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate prompt blocks for style-compass from the local style catalog."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "references" / "style-catalog.json"
OUTPUT_DIR = ROOT / "references" / "prompt-blocks"

PAGE_TYPE_ALIASES = {
    "saas": "product-site",
    "ai-platform": "product-site",
    "editorial": "landing-page",
    "launch-page": "landing-page",
    "pricing": "product-site",
    "showcase": "brand-site",
    "collaboration": "product-site",
    "workbench": "editor",
}

SUPPORTED_PAGES = {
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

MOOD_ZH_MAP = {
    "developer": "开发者气质",
    "editorial": "编辑感",
    "future-facing": "未来感",
    "technical": "技术感",
    "gradient": "渐变品牌感",
    "cinematic": "电影感",
    "premium": "高级感",
    "minimal": "极简",
    "precise": "精准",
    "tooling": "工具感",
    "bold": "强标题张力",
    "luxury": "奢华感",
    "friendly": "亲和",
    "financial": "金融秩序感",
    "trust-driven": "信任感",
    "creative": "创作感",
    "expressive": "表现力",
    "heroic": "主视觉驱动",
    "product-led": "产品导向",
    "monumental": "纪念碑式构图",
    "precision": "精密感",
}

CATEGORY_KEYWORDS = {
    "AI & LLM Platforms": ["AI 产品感", "技术品牌感"],
    "Automotive": ["高冲击摄影", "品牌气场"],
    "Backend, Database & DevOps": ["系统秩序", "控制台气质"],
    "Design & Creative Tools": ["创作工具感", "模块清晰"],
    "Developer Tools & IDEs": ["开发者气质", "高频操作效率"],
    "E-commerce & Retail": ["转化导向", "商品聚焦"],
    "Fintech & Crypto": ["信任感", "秩序精准"],
    "Media & Consumer Tech": ["品牌叙事", "产品主视觉"],
    "Productivity & SaaS": ["产品化", "模块稳定"],
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


def normalize_page(page: str) -> str | None:
    normalized = PAGE_TYPE_ALIASES.get(page, page)
    if normalized in SUPPORTED_PAGES:
        return normalized
    return None


def generate_style_keywords(entry: dict) -> list[str]:
    keywords = [entry.get("color_tendency", ""), entry.get("typography_tone", "")]
    keywords.extend(entry.get("mood_keywords_zh") or [MOOD_ZH_MAP.get(item, item) for item in entry.get("mood_keywords", [])])
    keywords.extend(CATEGORY_KEYWORDS.get(entry.get("category", ""), []))
    return dedupe(keywords)


def generate_negative_constraints(entry: dict, pages: list[str]) -> list[str]:
    notes = [
        "不要只复制表层颜色、圆角或大图，忽略布局逻辑与模块节奏。",
        "不要让所有模块同权重，必须保留明确主次。",
        entry.get("risk_note", ""),
    ]
    brightness = entry.get("brightness")
    if brightness == "dark":
        notes.append("不要把深色层级压成一整块黑面，必须保留容器层次和状态差异。")
    if entry.get("layout_density") == "high":
        notes.append("不要因为追求风格把高密度页面做得难以扫描。")
    if pages and any(page in {"dashboard", "editor", "docs", "developer-tool"} for page in pages):
        notes.append("不要为了品牌表达牺牲高频操作效率和信息扫描速度。")
    if entry.get("category") in {"Automotive", "Media & Consumer Tech", "E-commerce & Retail"}:
        notes.append("不要把品牌张力做成无节制海报，仍要服务页面路径和信息转化。")
    return dedupe(notes)


def generate_layout_bias(entry: dict, pages: list[str]) -> list[str]:
    category = entry.get("category", "")
    density = entry.get("layout_density", "medium")
    lines: list[str] = []
    if any(page in {"landing-page", "brand-site", "product-site", "campaign", "commerce", "marketing"} for page in pages):
        lines.extend(
            [
                "首屏需要明确主视觉和价值主张，不要一开始就掉进零散模块堆叠。",
                "区块之间保留节奏断点，让叙事、信息和转化路径都清楚。",
            ]
        )
    if any(page in {"dashboard", "editor", "docs", "developer-tool", "creative-tool"} for page in pages):
        lines.extend(
            [
                "优先稳定骨架与高频操作路径，模块秩序比装饰更重要。",
                "用对齐、间距、边界和容器层级建立结构，不靠堆特效解决问题。",
            ]
        )
    if category in {"Automotive", "Media & Consumer Tech"}:
        lines.append("允许更强的主视觉和品牌画面，但不能冲散页面主次关系。")
    if category in {"Backend, Database & DevOps", "Developer Tools & IDEs", "Productivity & SaaS"}:
        lines.append("优先面板结构和稳定分区，让用户快速定位状态、操作和内容。")
    if density == "high":
        lines.append("高密度页面要保留扫描效率，不盲目为了风格而拉大留白。")
    elif density == "low":
        lines.append("低密度页面要让留白服务聚焦，而不是把信息摊得过散。")
    else:
        lines.append("中密度页面优先平衡品牌气质与信息效率，不要偏向单一极端。")
    return dedupe(lines)


def generate_component_tone(entry: dict) -> dict[str, str]:
    category = entry.get("category", "")
    style_name = entry["name"]
    button = f"按钮要体现 {style_name} 的语气，但主次必须清楚。"
    card = f"卡片围绕 {style_name} 的表面气质组织边界、留白和信息层级。"
    navigation = "导航负责稳住结构秩序，不承担多余表演。"
    panel = f"面板需要有 {style_name} 的容器感，但不能破坏信息秩序。"
    input_ = "输入控件优先可读、可扫视和状态清楚。"

    if category in {"Developer Tools & IDEs", "Backend, Database & DevOps", "Productivity & SaaS"}:
        button = "按钮应直接清楚，强调动作反馈，不要像营销贴片。"
        navigation = "导航像工具骨架，稳定、安静、连续。"
        panel = "面板强调秩序、层级和状态一致性，不做浮夸装饰。"
    elif category in {"Design & Creative Tools"}:
        button = "按钮要友好清楚，带一点创作工具语气，但不失去效率。"
        card = "卡片允许更轻量的表现力，但必须可扫视、可归类。"
        navigation = "导航像创作工作台框架，清楚但不死板。"
    elif category in {"Automotive", "Media & Consumer Tech", "E-commerce & Retail"}:
        button = "按钮要承接品牌或转化语气，但仍然保持路径清晰。"
        card = "卡片更像品牌模块或商品信息单元，不要退回普通后台灰盒。"
        navigation = "导航要稳住节奏，给强主视觉和大图区块兜底。"
    elif category in {"Fintech & Crypto"}:
        button = "按钮要可信、果断，避免廉价促销感。"
        panel = "面板以秩序、信任和状态清楚为先，不做噪音式装饰。"

    return {
        "button": button,
        "card": card,
        "input": input_,
        "navigation": navigation,
        "panel": panel,
    }


def generate_image_direction(entry: dict) -> str:
    category = entry.get("category", "")
    if category == "Automotive":
        return "优先高冲击产品摄影和大场景画面，让图像承担品牌气场。"
    if category in {"Media & Consumer Tech", "E-commerce & Retail"}:
        return "优先产品主体、主视觉画面或商品图，不做碎装饰拼贴。"
    if category in {"Developer Tools & IDEs", "Backend, Database & DevOps", "Productivity & SaaS"}:
        return "图像从简，优先界面截图、代码片段或抽象技术图形，不靠大插画取胜。"
    if category == "Design & Creative Tools":
        return "适合轻量色块、界面截图和创作素材，图像用于增强创作氛围。"
    if category == "Fintech & Crypto":
        return "图像和图形服务于秩序、数据感和信任感，不做廉价炫技流光。"
    return "图像与背景只服务主叙事，不抢走信息结构。"


def infer_avoid_pages(entry: dict, pages: list[str]) -> list[str]:
    category = entry.get("category", "")
    avoids: list[str] = []
    if category in {"Automotive", "Media & Consumer Tech", "E-commerce & Retail"}:
        avoids.append("dashboard")
    if category in {"Developer Tools & IDEs", "Backend, Database & DevOps"}:
        avoids.append("brand-site")
    if category == "Fintech & Crypto":
        avoids.append("campaign")
    if category == "Design & Creative Tools":
        avoids.append("commerce")
    if entry.get("layout_density") == "high" and "landing-page" in pages:
        avoids.append("campaign")
    return dedupe([page for page in avoids if page not in pages])


def page_prompt(style_name: str, page: str) -> str:
    if page in {"landing-page", "brand-site", "product-site", "marketing", "commerce", "campaign"}:
        return (
            f"按 {style_name} 风格实现 {page} 页面，先稳住主视觉、标题层级和转化路径，"
            "再引入品牌气质，不要让所有区块同权重。"
        )
    if page in {"dashboard", "docs", "settings", "analytics", "developer-tool"}:
        return (
            f"按 {style_name} 风格实现 {page} 页面，优先保证扫描效率、状态清晰和模块秩序，"
            "风格表达放在表面语言与层级里。"
        )
    if page in {"editor", "creative-tool"}:
        return (
            f"按 {style_name} 风格实现 {page} 页面，保留工作流效率，"
            "重点统一侧栏、工具栏、面板和主工作区的表面语气。"
        )
    return f"按 {style_name} 风格实现 {page} 页面，先统一骨架、层级和组件语气。"


def generate_page_examples(entry: dict, pages: list[str]) -> dict[str, str]:
    ordered = pages[:3] if pages else ["product-site", "dashboard"]
    return {page: page_prompt(entry["name"], page) for page in ordered}


def generate_component_examples(entry: dict) -> dict[str, str]:
    style_name = entry["name"]
    return {
        "button": f"把按钮做成 {style_name} 风格，保留明确主次、状态反馈和点击目标。",
        "card": f"把卡片做成 {style_name} 风格，重点控制边界、留白和信息层级。",
        "panel": f"把面板做成 {style_name} 风格，强调容器秩序，不要无规则叠阴影。",
        "navigation": f"把导航做成 {style_name} 风格，让结构稳定清楚，不要抢走主内容注意力。",
        "form": f"把表单做成 {style_name} 风格，优先可读性、状态反馈和输入效率。",
    }


def generate_handoff_template(entry: dict, pages: list[str]) -> str:
    category = entry.get("category", "")
    style_name = entry["name"]
    if category in {"Developer Tools & IDEs", "Backend, Database & DevOps", "Productivity & SaaS"}:
        return f"按 {style_name} 风格重构界面，优先保证工具效率、层级秩序和模块一致性。"
    if category in {"Automotive", "Media & Consumer Tech", "E-commerce & Retail"}:
        return f"按 {style_name} 风格落地页面，用主视觉和品牌张力拉开气场，但保持路径清晰。"
    if category == "Fintech & Crypto":
        return f"按 {style_name} 风格实现界面，优先建立信任感、秩序感和关键状态清晰度。"
    if category == "Design & Creative Tools":
        return f"按 {style_name} 风格落地界面，兼顾创作氛围、色彩识别和工具效率。"
    target = "页面" if any(page in {"landing-page", "brand-site", "product-site", "commerce"} for page in pages) else "界面"
    return f"按 {style_name} 风格落地{target}，先稳住骨架和层级，再补品牌表达。"


def generate_block(entry: dict) -> dict:
    pages = dedupe([normalized for item in entry.get("best_for", []) if (normalized := normalize_page(item))])
    return {
        "name": entry["name"],
        "style_keywords": generate_style_keywords(entry),
        "negative_constraints": generate_negative_constraints(entry, pages),
        "layout_bias": generate_layout_bias(entry, pages),
        "component_tone": generate_component_tone(entry),
        "image_direction": generate_image_direction(entry),
        "best_for_pages": pages,
        "avoid_for_pages": infer_avoid_pages(entry, pages),
        "page_prompt_examples": generate_page_examples(entry, pages),
        "component_prompt_examples": generate_component_examples(entry),
        "handoff_template": generate_handoff_template(entry, pages),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default=str(CATALOG_PATH), help="Path to style catalog JSON")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Prompt block output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing prompt blocks")
    args = parser.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    for entry in catalog:
        output_path = output_dir / f"{slugify(entry['name'])}.json"
        if output_path.exists() and not args.force:
            skipped += 1
            continue
        block = generate_block(entry)
        output_path.write_text(json.dumps(block, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1

    print(json.dumps({"created": created, "skipped": skipped, "total_catalog": len(catalog)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

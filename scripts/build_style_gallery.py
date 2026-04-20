#!/usr/bin/env python3
"""Build a bilingual local gallery page for style thumbnails and rankings."""

from __future__ import annotations

import json
from pathlib import Path

CATEGORY_ORDER = [
    "AI & LLM Platforms",
    "Developer Tools & IDEs",
    "Backend, Database & DevOps",
    "Productivity & SaaS",
    "Design & Creative Tools",
    "Fintech & Crypto",
    "E-commerce & Retail",
    "Media & Consumer Tech",
    "Automotive",
]

LAYOUT_LABELS = {
    "hero-light": {"zh": "主视觉", "en": "Hero"},
    "dashboard": {"zh": "控制台", "en": "Dashboard"},
    "poster": {"zh": "海报", "en": "Poster"},
    "creative": {"zh": "创意", "en": "Creative"},
    "editorial": {"zh": "编辑式", "en": "Editorial"},
    "docs-grid": {"zh": "文档", "en": "Docs"},
    "commerce-split": {"zh": "商业", "en": "Commerce"},
    "luxury-banner": {"zh": "奢华", "en": "Luxury"},
    "ai-capsule": {"zh": "AI 胶囊", "en": "AI Capsule"},
    "product-stack": {"zh": "产品层叠", "en": "Product"},
    "editor-workbench": {"zh": "工作台", "en": "Workbench"},
}

HIGH_FREQUENCY_NAMES = {
    "Apple",
    "Nike",
    "Stripe",
    "Vercel",
    "Linear",
    "Supabase",
    "Figma",
    "Cursor",
    "Claude",
    "Airbnb",
    "BMW",
    "WIRED",
}

UI_STRINGS = {
    "zh": {
        "page_title": "风格总览 / Style Gallery",
        "eyebrow": "STYLE GALLERY",
        "hero_title": "风格总览 / Style Gallery",
        "hero_description": "先看总览，再做 UI 风格决策。这里不是附带页面，而是风格罗盘（style-compass）给新用户准备的第一个入口。",
        "hero_stats": [
            "{count} 个风格",
            "双语切换",
            "总榜 + 分类热门",
        ],
        "guide_title": "第一次来先看这里",
        "guide_copy": "如果你还没定方向、只想先横向比较，或者不知道该从 Apple、Stripe、Linear 还是别的路线开始，先逛这个总览页。",
        "guide_path_label": "总览页路径",
        "guide_path_value": "assets/gallery/style-gallery.html",
        "guide_steps": [
            "先看热门总榜，快速建立参照物",
            "再刷分类热门，缩小到同类风格",
            "最后用搜索和筛选收敛 1 到 3 个候选"
        ],
        "guide_readme": "查看 README",
        "guide_skill": "查看 SKILL.md",
        "language_zh": "中文",
        "language_en": "English",
        "filters_title": "筛选",
        "search_label": "搜索名称",
        "search_placeholder": "比如 Apple / Stripe / Linear",
        "category_label": "按分类筛选",
        "category_all": "全部分类",
        "layout_label": "按布局筛选",
        "layout_all": "全部布局",
        "global_hot_overline": "HOT LIST",
        "global_hot_title": "热门总榜",
        "global_hot_copy": "先看最常被拿来做参考的风格，再决定要深入哪一组。",
        "category_hot_overline": "BY CATEGORY",
        "category_hot_title": "分类热门",
        "category_hot_copy": "每个分类各挑 3 个代表项，方便在同类里横向比较。",
        "all_styles_title": "完整风格卡",
        "result_count": "显示 {visible} / {total}",
        "result_note": "完整卡片区支持搜索、分类筛选和布局筛选",
        "results_mode_title": "筛选结果",
        "results_mode_copy": "筛选激活后自动进入结果模式，排行内容折叠为摘要。",
        "results_toolbar_title": "看结果",
        "results_count_label": "结果数",
        "results_nav_title": "灵感导航",
        "results_nav_copy": "热门和分类还在，但压缩成更轻的导航条。",
        "results_hot_line": "热门总榜",
        "results_category_line": "分类热门",
        "sticky_search_label": "搜索",
        "sticky_category_label": "分类",
        "sticky_layout_label": "布局",
        "active_filters_label": "当前筛选",
        "no_active_filters": "无",
        "clear_filters": "清空筛选",
        "return_browse": "返回浏览",
        "browse_reset_hint": "回到逛灵感",
        "summary_title": "灵感摘要",
        "summary_copy": "筛选时已折叠完整排行，需要时再展开查看。",
        "summary_global": "热门总榜摘要",
        "summary_category": "分类热门摘要",
        "collapsed_note": "筛选激活，完整热门区已折叠。",
        "no_results_title": "没有匹配结果",
        "no_results_copy": "换个关键词，或者清空筛选回到逛灵感。",
        "rank_reason_label": "为什么热门",
        "best_for_label": "适用",
        "mood_label": "关键词",
        "preview_entry": "风格预览",
        "preview_only": "仅预览页",
        "rank_badge": "第 {rank} 名",
        "category_top_label": "分类 Top 3",
    },
    "en": {
        "page_title": "Style Gallery",
        "eyebrow": "STYLE GALLERY",
        "hero_title": "Style Gallery",
        "hero_description": "Browse the gallery first, then make a UI style decision. This is the first-time entry for Style Compass, not just an extra page.",
        "hero_stats": [
            "{count} styles",
            "Bilingual toggle",
            "Global + category hot lists",
        ],
        "guide_title": "Start Here",
        "guide_copy": "If you are still exploring, comparing directions, or do not know whether to begin with Apple, Stripe, Linear, or something else, start with this gallery.",
        "guide_path_label": "Gallery path",
        "guide_path_value": "assets/gallery/style-gallery.html",
        "guide_steps": [
            "Start with the global hot list to build a baseline",
            "Use category hot lists to compare within the same cluster",
            "Finish with search and filters to narrow down to 1-3 candidates"
        ],
        "guide_readme": "Open README",
        "guide_skill": "Open SKILL.md",
        "language_zh": "中文",
        "language_en": "English",
        "filters_title": "Filters",
        "search_label": "Search by name",
        "search_placeholder": "Try Apple / Stripe / Linear",
        "category_label": "Filter by category",
        "category_all": "All categories",
        "layout_label": "Filter by layout",
        "layout_all": "All layouts",
        "global_hot_overline": "HOT LIST",
        "global_hot_title": "Global Favorites",
        "global_hot_copy": "Start from the most reusable references before diving deeper into one cluster.",
        "category_hot_overline": "BY CATEGORY",
        "category_hot_title": "Category Favorites",
        "category_hot_copy": "Three high-signal picks per category so comparisons stay local and useful.",
        "all_styles_title": "Full Style Cards",
        "result_count": "Showing {visible} / {total}",
        "result_note": "The full grid supports search, category filters, and layout filters",
        "results_mode_title": "Results",
        "results_mode_copy": "Once filters are active, the page shifts into result mode and collapses the long ranking blocks.",
        "results_toolbar_title": "Results mode",
        "results_count_label": "Result count",
        "results_nav_title": "Highlights rail",
        "results_nav_copy": "Hot picks and category favorites stay visible as a compact guide.",
        "results_hot_line": "Global favorites",
        "results_category_line": "Category favorites",
        "sticky_search_label": "Search",
        "sticky_category_label": "Category",
        "sticky_layout_label": "Layout",
        "active_filters_label": "Active filters",
        "no_active_filters": "None",
        "clear_filters": "Clear filters",
        "return_browse": "Back to browse",
        "browse_reset_hint": "Return to inspiration mode",
        "summary_title": "Highlights summary",
        "summary_copy": "The long ranking sections are collapsed while filters are active.",
        "summary_global": "Global favorites summary",
        "summary_category": "Category favorites summary",
        "collapsed_note": "Filtered mode is active. Full highlight sections are collapsed.",
        "no_results_title": "No matching results",
        "no_results_copy": "Try another keyword, or clear filters to return to browsing.",
        "rank_reason_label": "Why it ranks",
        "best_for_label": "Best for",
        "mood_label": "Keywords",
        "preview_entry": "Style preview",
        "preview_only": "Preview only",
        "rank_badge": "No. {rank}",
        "category_top_label": "Category Top 3",
    },
}


def relative_thumb_path(gallery_dir: Path, absolute_thumb: str | None) -> str | None:
    if not absolute_thumb:
        return None
    return Path(absolute_thumb).relative_to(gallery_dir.parent).as_posix()


def hot_sort_key(item: dict) -> tuple[float, int, str]:
    return (-float(item["hot_score"]), 0 if item["is_high_frequency"] else 1, item["name"].lower())


def build_payload(manifest: list[dict], catalog_by_slug: dict[str, dict], gallery_dir: Path) -> dict:
    items: list[dict] = []
    manifest_by_slug = {entry["slug"]: entry for entry in manifest}

    for slug, detail in catalog_by_slug.items():
        manifest_item = manifest_by_slug.get(slug, {})
        layout_key = manifest_item.get("layout", "hero-light")
        labels = LAYOUT_LABELS.get(layout_key, {"zh": layout_key, "en": layout_key.title()})
        audit_status = manifest_item.get("audit_status", "needs_audit")
        svg_thumb_path = relative_thumb_path(gallery_dir, manifest_item.get("path"))
        official_thumb_path = relative_thumb_path(gallery_dir, manifest_item.get("official_thumb_path"))
        thumb_source = manifest_item.get("thumb_source")
        display_thumb_path = None

        if svg_thumb_path:
            thumb_source = "svg"
            display_thumb_path = svg_thumb_path
        elif thumb_source == "official" and official_thumb_path:
            display_thumb_path = official_thumb_path
        elif official_thumb_path:
            thumb_source = "official"
            display_thumb_path = official_thumb_path
        else:
            thumb_source = "none"
        items.append(
            {
                "name": detail["name"],
                "name_zh": detail.get("name_zh") or detail["name"],
                "slug": detail["slug"],
                "category_key": detail["category"],
                "category_zh": detail["category_zh"],
                "category_en": detail["category_en"],
                "layout_key": layout_key,
                "layout_label_zh": labels["zh"],
                "layout_label_en": labels["en"],
                "thumb_path": display_thumb_path,
                "svg_thumb_path": svg_thumb_path,
                "official_thumb_path": official_thumb_path,
                "thumb_source": thumb_source,
                "design_url": detail["design_url"],
                "preview_url": manifest_item.get("preview_url", detail["preview_url"]),
                "plain_impression_zh": detail.get("plain_impression_zh", detail["plain_impression"]),
                "plain_impression_en": detail.get("plain_impression_en", detail["summary"]),
                "best_for_zh": detail.get("best_for_zh", detail["best_for"]),
                "best_for_en": detail.get("best_for_en", detail["best_for"]),
                "mood_keywords_zh": detail.get("mood_keywords_zh", detail["mood_keywords"]),
                "mood_keywords_en": detail.get("mood_keywords_en", detail["mood_keywords"]),
                "hot_score": detail.get("hot_score", 0),
                "hot_reason_zh": detail.get("hot_reason_zh", ""),
                "hot_reason_en": detail.get("hot_reason_en", ""),
                "is_high_frequency": detail["name"] in HIGH_FREQUENCY_NAMES,
                "audit_status": audit_status,
                "audit_score": manifest_item.get("audit_score", 0.0),
            }
        )

    items.sort(key=lambda item: item["name"].lower())
    global_hot = sorted(items, key=hot_sort_key)[:12]

    category_hot: list[dict] = []
    for category_key in CATEGORY_ORDER:
        bucket = [item for item in items if item["category_key"] == category_key]
        if not bucket:
            continue
        category_hot.append(
            {
                "category_key": category_key,
                "category_zh": bucket[0]["category_zh"],
                "category_en": bucket[0]["category_en"],
                "items": [item["slug"] for item in sorted(bucket, key=hot_sort_key)[:3]],
            }
        )

    categories = [
        {
            "key": category_key,
            "zh": next(item["category_zh"] for item in items if item["category_key"] == category_key),
            "en": next(item["category_en"] for item in items if item["category_key"] == category_key),
        }
        for category_key in CATEGORY_ORDER
        if any(item["category_key"] == category_key for item in items)
    ]

    layout_order = [key for key in LAYOUT_LABELS if any(item["layout_key"] == key for item in items)]
    layouts = [{"key": key, "zh": LAYOUT_LABELS[key]["zh"], "en": LAYOUT_LABELS[key]["en"]} for key in layout_order]

    return {
        "items": items,
        "global_hot": [item["slug"] for item in global_hot],
        "category_hot": category_hot,
        "categories": categories,
        "layouts": layouts,
        "ui": UI_STRINGS,
    }


def json_blob(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


def build_html(payload: dict) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{UI_STRINGS["zh"]["page_title"]}</title>
    <style>
      :root {{
        --bg: #040404;
        --panel: #0b0b0b;
        --panel-soft: #101010;
        --panel-muted: #151515;
        --field: #111111;
        --line: rgba(255, 255, 255, 0.12);
        --line-strong: rgba(255, 255, 255, 0.24);
        --text: #f7f7f2;
        --muted: #a6a6a0;
        --muted-soft: #7d7d77;
        --accent: #ffffff;
        --chip: rgba(255, 255, 255, 0.05);
        --shadow: none;
        --radius-xl: 14px;
        --radius-lg: 12px;
        --radius-md: 10px;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        min-height: 100vh;
        font-family: "Helvetica Neue", Arial, sans-serif;
        color: var(--text);
        background: linear-gradient(180deg, #030303 0%, #080808 52%, #050505 100%);
      }}
      .shell {{
        width: min(1520px, calc(100vw - 24px));
        margin: 14px auto 36px;
        display: grid;
        gap: 18px;
      }}
      .section-card {{
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: var(--radius-xl);
        box-shadow: var(--shadow);
      }}
      .masthead {{
        padding: 24px 26px;
        display: grid;
        gap: 20px;
      }}
      .masthead-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
      }}
      .eyebrow {{
        display: inline-flex;
        padding: 8px 11px;
        border-radius: 999px;
        background: var(--chip);
        color: #f3f3ee;
        font-size: 12px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 800;
      }}
      .lang-toggle {{
        display: inline-flex;
        gap: 6px;
        padding: 4px;
        border-radius: 999px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.01);
      }}
      .lang-toggle button {{
        border: 0;
        background: transparent;
        color: var(--muted);
        padding: 9px 13px;
        border-radius: 999px;
        cursor: pointer;
        font-size: 13px;
        font-weight: 700;
      }}
      .lang-toggle button.active {{
        background: #f5f5ef;
        color: #050505;
      }}
      .masthead-content {{
        display: grid;
        grid-template-columns: minmax(0, 1.2fr) minmax(320px, 520px);
        gap: 22px;
        align-items: start;
      }}
      .hero-copy-wrap {{
        display: grid;
        gap: 12px;
      }}
      h1 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: clamp(40px, 6.2vw, 76px);
        line-height: 0.92;
        letter-spacing: -0.05em;
        font-weight: 900;
        max-width: 10ch;
      }}
      .hero-copy {{
        margin: 0;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.55;
        max-width: 460px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }}
      .hero-meta {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }}
      .hero-meta span {{
        padding: 9px 12px;
        border-radius: var(--radius-md);
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #d6d6cf;
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      .hero-guide {{
        display: grid;
        gap: 10px;
        padding: 16px 18px;
        border-radius: var(--radius-lg);
        border: 1px solid var(--line);
        background: var(--panel-soft);
        max-width: 560px;
      }}
      .hero-guide h2 {{
        margin: 0;
        font-size: 16px;
        color: var(--text);
        letter-spacing: -0.02em;
      }}
      .hero-guide p {{
        margin: 0;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.6;
      }}
      .hero-guide code {{
        display: inline-block;
        padding: 6px 9px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #ecece5;
        font-size: 12px;
      }}
      .hero-guide-label {{
        display: block;
        color: var(--muted-soft);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
      }}
      .hero-guide ol {{
        margin: 0;
        padding-left: 18px;
        color: #e7e7e1;
        font-size: 13px;
        line-height: 1.6;
      }}
      .hero-guide li + li {{
        margin-top: 4px;
      }}
      .hero-guide-links {{
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }}
      .hero-guide-links a {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 38px;
        padding: 0 14px;
        border-radius: 999px;
        border: 1px solid var(--line);
        background: rgba(255, 255, 255, 0.02);
        color: var(--text);
        text-decoration: none;
        font-size: 12px;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 700;
      }}
      .hero-guide-links a:hover {{
        border-color: var(--line-strong);
      }}
      .filters {{
        display: grid;
        gap: 12px;
        padding: 16px;
        border-radius: var(--radius-lg);
        border: 1px solid var(--line);
        background: var(--panel-soft);
      }}
      .filters-head {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: flex-start;
        flex-wrap: wrap;
      }}
      .filters-hint {{
        color: var(--muted-soft);
        font-size: 12px;
        max-width: 320px;
        text-align: right;
      }}
      .filters h2,
      .section-eyebrow {{
        margin: 0;
        font-size: 12px;
        color: #f2f2ed;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 800;
      }}
      .toolbar-grid {{
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
      }}
      .toolbar-grid .field:first-child {{
        grid-column: 1 / -1;
      }}
      .field {{
        display: grid;
        gap: 7px;
      }}
      .field label {{
        font-size: 12px;
        color: #d6d6cf;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .field input,
      .field select {{
        width: 100%;
        border: 1px solid var(--line);
        background: var(--field);
        color: var(--text);
        border-radius: 8px;
        padding: 12px 13px;
        outline: none;
      }}
      .field input:focus,
      .field select:focus {{
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: none;
      }}
      .hidden {{
        display: none !important;
      }}
      .section-card {{
        padding: 22px 24px;
        scroll-margin-top: 88px;
      }}
      .results-toolbar-shell {{
        position: sticky;
        top: 12px;
        z-index: 30;
        border: 1px solid var(--line-strong);
        border-radius: 12px;
        background: rgba(7, 7, 7, 0.96);
        backdrop-filter: blur(10px);
        padding: 12px 14px;
      }}
      .results-toolbar-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
      }}
      .results-toolbar-head h2 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: -0.03em;
      }}
      .results-toolbar-copy {{
        margin: 0;
        color: var(--muted-soft);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .results-toolbar-grid {{
        display: grid;
        grid-template-columns: minmax(0, 1.3fr) repeat(2, minmax(180px, 0.8fr)) auto;
        gap: 10px;
        align-items: end;
      }}
      .results-toolbar-grid .field:first-child {{
        grid-column: 1 / 3;
      }}
      .results-toolbar-grid .toolbar-actions {{
        justify-self: end;
      }}
      .toolbar-actions {{
        display: flex;
        gap: 8px;
        align-items: end;
      }}
      .toolbar-actions button {{
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: transparent;
        color: var(--text);
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        cursor: pointer;
        white-space: nowrap;
      }}
      .toolbar-actions button.primary {{
        background: #f5f5ef;
        border-color: #f5f5ef;
        color: #050505;
      }}
      .results-nav-shell {{
        padding: 14px 16px;
        display: grid;
        gap: 12px;
      }}
      .results-nav-head {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: end;
      }}
      .results-nav-head h2 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 18px;
        text-transform: uppercase;
      }}
      .results-nav-copy {{
        margin: 0;
        color: var(--muted-soft);
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .results-nav-lines {{
        display: grid;
        gap: 10px;
      }}
      .results-nav-line {{
        display: grid;
        grid-template-columns: 96px minmax(0, 1fr);
        gap: 12px;
        align-items: start;
      }}
      .results-nav-label {{
        padding-top: 8px;
        font-size: 11px;
        color: #f0f0ea;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 800;
      }}
      .compact-chip-list {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }}
      .compact-chip {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        min-height: 42px;
        padding: 6px 10px 6px 6px;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(255, 255, 255, 0.03);
        color: #e8e8e2;
        text-decoration: none;
      }}
      .compact-chip:hover {{
        border-color: rgba(255, 255, 255, 0.18);
        background: rgba(255, 255, 255, 0.05);
      }}
      .compact-chip img {{
        width: 32px;
        height: 32px;
        border-radius: 999px;
        background: #0c0c0c;
        padding: 4px;
        object-fit: contain;
        flex: 0 0 auto;
      }}
      .compact-chip-icon {{
        width: 32px;
        height: 32px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.08);
        color: #f7f7f2;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        flex: 0 0 auto;
      }}
      .thumb-media {{
        position: relative;
      }}
      .compact-chip-text {{
        display: grid;
        gap: 2px;
        min-width: 0;
      }}
      .compact-chip-title {{
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #f7f7f2;
        white-space: nowrap;
      }}
      .compact-chip-subtitle {{
        font-size: 10px;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
      }}
      .section-head {{
        display: flex;
        justify-content: space-between;
        gap: 14px;
        align-items: start;
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      }}
      .section-head h2 {{
        margin: 4px 0 4px;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: clamp(24px, 3vw, 38px);
        letter-spacing: -0.04em;
        line-height: 0.96;
        font-weight: 900;
        text-transform: uppercase;
      }}
      .section-copy {{
        margin: 0;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.5;
        max-width: 460px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }}
      .rank-strip {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
      }}
      .rank-card {{
        border: 1px solid var(--line);
        border-radius: var(--radius-lg);
        background: var(--panel-soft);
        overflow: hidden;
        display: grid;
        grid-template-rows: auto 1fr;
        min-height: 100%;
      }}
      .rank-card img {{
        display: block;
        width: 100%;
        aspect-ratio: 16 / 10;
        object-fit: contain;
        padding: 12px;
        background: #0a0a0a;
        filter: saturate(0.92) contrast(1.02);
      }}
      .thumb-fallback {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        aspect-ratio: 16 / 10;
        border-radius: 8px;
        background: #0a0a0a;
        border: 1px dashed rgba(255, 255, 255, 0.12);
        color: #d9d9d3;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 12px;
        text-align: center;
      }}
      .rank-body {{
        padding: 14px;
        display: grid;
        grid-template-rows: auto auto auto 1fr auto;
        gap: 10px;
      }}
      .rank-top {{
        display: flex;
        justify-content: space-between;
        gap: 8px;
        align-items: center;
      }}
      .rank-badge,
      .layout-pill,
      .mini-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 6px 9px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 700;
        background: rgba(255, 255, 255, 0.06);
        color: #efefe8;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      .rank-card h3,
      .mini-card h4,
      .full-card h3 {{
        margin: 0;
        letter-spacing: -0.02em;
      }}
      .rank-card h3 {{
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 26px;
        line-height: 0.98;
        text-transform: uppercase;
      }}
      .rank-card p,
      .mini-card p,
      .full-card p,
      .meta dd {{
        margin: 0;
        color: var(--muted);
      }}
      .rank-category {{
        font-size: 12px;
        color: #f0f0ea;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .clamp-2,
      .clamp-3 {{
        display: -webkit-box;
        overflow: hidden;
        -webkit-box-orient: vertical;
      }}
      .clamp-2 {{
        -webkit-line-clamp: 2;
      }}
      .clamp-3 {{
        -webkit-line-clamp: 3;
      }}
      .rank-actions,
      .card-actions {{
        display: flex;
        gap: 10px;
      }}
      .rank-actions a,
      .card-actions a {{
        flex: 1;
        text-align: center;
        text-decoration: none;
        padding: 11px 12px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: var(--text);
        background: transparent;
        font-size: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}
      .rank-actions a.primary,
      .card-actions a.primary {{
        background: #f5f5ef;
        color: #050505;
        border-color: #f5f5ef;
      }}
      .category-hot-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 16px;
      }}
      .category-panel {{
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: var(--radius-lg);
        background: #090909;
        padding: 14px;
        display: grid;
        gap: 12px;
      }}
      .category-panel-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
      }}
      .category-panel-head h3 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 20px;
        text-transform: uppercase;
      }}
      .mini-list {{
        display: grid;
        gap: 10px;
      }}
      .mini-card {{
        display: grid;
        grid-template-columns: 132px 1fr;
        gap: 12px;
        padding: 12px;
        border-radius: 10px;
        background: var(--panel-muted);
        border: 1px solid rgba(255, 255, 255, 0.04);
      }}
      .mini-card img {{
        width: 132px;
        height: 94px;
        object-fit: contain;
        padding: 8px;
        border-radius: 8px;
        background: #0c0c0c;
      }}
      .mini-thumb-fallback {{
        width: 132px;
        height: 94px;
      }}
      .mini-card-body {{
        display: grid;
        gap: 6px;
      }}
      .mini-card-body h4 {{
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 18px;
        text-transform: uppercase;
      }}
      .catalog-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
      }}
      .catalog-head h2 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: clamp(24px, 3vw, 38px);
        text-transform: uppercase;
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
      }}
      .results-meta {{
        display: grid;
        gap: 10px;
        margin-bottom: 14px;
      }}
      .results-meta-top {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        align-items: center;
        color: var(--muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .results-chip-list {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }}
      .results-chip {{
        display: inline-flex;
        align-items: center;
        padding: 8px 10px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 11px;
        color: #ecece6;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .empty-state {{
        border: 1px dashed rgba(255, 255, 255, 0.14);
        border-radius: 12px;
        padding: 28px 24px;
        text-align: center;
        display: grid;
        gap: 12px;
        background: rgba(255, 255, 255, 0.02);
      }}
      .empty-state h3 {{
        margin: 0;
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 26px;
        text-transform: uppercase;
      }}
      .empty-state p {{
        margin: 0;
        color: var(--muted);
        font-size: 13px;
      }}
      .empty-state-actions {{
        display: flex;
        justify-content: center;
        gap: 10px;
      }}
      .empty-state-actions button {{
        border: 1px solid rgba(255, 255, 255, 0.12);
        background: transparent;
        color: var(--text);
        border-radius: 8px;
        padding: 12px 14px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        cursor: pointer;
      }}
      .empty-state-actions button.primary {{
        background: #f5f5ef;
        border-color: #f5f5ef;
        color: #050505;
      }}
      .full-card {{
        background: var(--panel-soft);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 14px;
        display: grid;
        grid-template-rows: auto 1fr;
        gap: 14px;
        min-height: 500px;
      }}
      .thumb-wrap {{
        padding: 0;
      }}
      .thumb-wrap img {{
        display: block;
        width: 100%;
        aspect-ratio: 16 / 10;
        object-fit: contain;
        padding: 12px;
        border-radius: 8px;
        background: #0a0a0a;
      }}
      .thumb-wrap .thumb-fallback {{
        padding: 16px;
      }}
      .card-body {{
        display: grid;
        grid-template-rows: auto auto auto auto 1fr auto;
        gap: 10px;
      }}
      .card-top {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }}
      .card-top h3 {{
        font-family: "Arial Black", "Helvetica Neue", Arial, sans-serif;
        font-size: 28px;
        line-height: 0.98;
        text-transform: uppercase;
      }}
      .category-line {{
        font-size: 12px;
        color: #f0f0ea;
        text-transform: uppercase;
        letter-spacing: 0.06em;
      }}
      .summary {{
        font-size: 12px;
        line-height: 1.5;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }}
      .meta {{
        display: grid;
        gap: 8px;
        margin: 0;
      }}
      .meta div {{
        display: grid;
        grid-template-columns: 40px 1fr;
        gap: 10px;
        font-size: 11px;
      }}
      .meta dt {{
        color: #efefe8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }}
      .meta dd {{
        display: -webkit-box;
        overflow: hidden;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
      }}
      .card-actions {{
        margin-top: auto;
      }}
      @media (max-width: 1180px) {{
        .masthead-content {{
          grid-template-columns: 1fr;
        }}
        .filters {{
          width: 100%;
        }}
      }}
      @media (max-width: 980px) {{
        .rank-strip,
        .category-hot-grid,
        .grid {{
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
        .results-toolbar-grid {{
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
        .results-toolbar-grid .field:first-child {{
          grid-column: 1 / -1;
        }}
        .results-toolbar-grid .toolbar-actions {{
          grid-column: 1 / -1;
          justify-self: stretch;
        }}
        .section-head,
        .catalog-head,
        .results-meta-top,
        .results-nav-head,
        .masthead-top {{
          align-items: start;
          flex-direction: column;
        }}
        .results-nav-line {{
          grid-template-columns: 1fr;
        }}
        .results-nav-label {{
          padding-top: 0;
        }}
        .toolbar-grid {{
          grid-template-columns: 1fr;
        }}
        .toolbar-grid .field:first-child {{
          grid-column: auto;
        }}
        .toolbar-actions {{
          width: 100%;
        }}
        .toolbar-actions button {{
          flex: 1;
        }}
      }}
      @media (max-width: 640px) {{
        .shell {{
          width: min(100vw - 14px, 1520px);
          margin: 8px auto 28px;
        }}
        .masthead,
        .section-card {{
          border-radius: 22px;
        }}
        .masthead-content,
        .rank-strip,
        .category-hot-grid,
        .grid {{
          grid-template-columns: 1fr;
        }}
        .mini-card {{
          grid-template-columns: 116px 1fr;
        }}
        .mini-card img {{
          width: 116px;
          height: 82px;
        }}
        .results-toolbar-shell {{
          top: 8px;
        }}
        .results-toolbar-grid {{
          grid-template-columns: 1fr;
        }}
        .results-toolbar-grid .field:first-child,
        .results-toolbar-grid .toolbar-actions {{
          grid-column: auto;
        }}
        .toolbar-actions {{
          flex-direction: column;
          width: 100%;
        }}
        .filters-hint {{
          max-width: 100%;
          text-align: left;
        }}
        .compact-chip {{
          width: 100%;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <section class="section-card masthead">
        <div class="masthead-top">
          <span class="eyebrow" id="hero-eyebrow"></span>
          <div class="lang-toggle" aria-label="Language toggle">
            <button type="button" data-lang="zh" class="active" id="lang-zh"></button>
            <button type="button" data-lang="en" id="lang-en"></button>
          </div>
        </div>
        <div class="masthead-content">
          <div class="hero-copy-wrap">
            <h1 id="hero-title"></h1>
            <p class="hero-copy" id="hero-description"></p>
            <div class="hero-meta" id="hero-meta"></div>
            <div class="hero-guide">
              <h2 id="guide-title"></h2>
              <p id="guide-copy"></p>
              <div>
                <span class="hero-guide-label" id="guide-path-label"></span>
                <code id="guide-path-value"></code>
              </div>
              <ol id="guide-steps"></ol>
              <div class="hero-guide-links">
                <a href="../README.md" id="guide-readme-link"></a>
                <a href="../SKILL.md" id="guide-skill-link"></a>
              </div>
            </div>
          </div>
          <aside class="filters">
            <div class="filters-head">
              <h2 id="filters-title"></h2>
              <span class="filters-hint" id="filters-note"></span>
            </div>
            <div class="toolbar-grid">
              <div class="field">
                <label for="search-input" id="search-label"></label>
                <input id="search-input" type="search" />
              </div>
              <div class="field">
                <label for="category-select" id="category-label"></label>
                <select id="category-select"></select>
              </div>
              <div class="field">
                <label for="layout-select" id="layout-label"></label>
                <select id="layout-select"></select>
              </div>
            </div>
          </aside>
        </div>
      </section>

      <section class="results-toolbar-shell hidden" id="results-toolbar-shell">
        <div class="results-toolbar-head">
          <div>
            <h2 id="results-toolbar-title"></h2>
            <p class="results-toolbar-copy" id="results-toolbar-copy"></p>
          </div>
        </div>
        <div class="results-toolbar-grid">
          <div class="field">
            <label for="results-search-input" id="results-search-label"></label>
            <input id="results-search-input" type="search" />
          </div>
          <div class="field">
            <label for="results-category-select" id="results-category-label"></label>
            <select id="results-category-select"></select>
          </div>
          <div class="field">
            <label for="results-layout-select" id="results-layout-label"></label>
            <select id="results-layout-select"></select>
          </div>
          <div class="field">
            <label id="results-count-label"></label>
            <div class="results-chip-list" id="results-count-chip"></div>
          </div>
          <div class="toolbar-actions">
            <button type="button" id="clear-filters-btn"></button>
            <button type="button" class="primary" id="return-browse-btn"></button>
          </div>
        </div>
      </section>

      <section class="section-card results-nav-shell hidden" id="results-nav-shell">
        <div class="results-nav-head">
          <div>
            <h2 id="results-nav-title"></h2>
            <p class="results-nav-copy" id="results-nav-copy"></p>
          </div>
        </div>
        <div class="results-nav-lines">
          <div class="results-nav-line">
            <span class="results-nav-label" id="results-hot-line-label"></span>
            <div class="compact-chip-list" id="results-hot-line"></div>
          </div>
          <div class="results-nav-line">
            <span class="results-nav-label" id="results-category-line-label"></span>
            <div class="compact-chip-list" id="results-category-line"></div>
          </div>
        </div>
      </section>

      <section class="section-card" id="global-hot-section">
        <div class="section-head">
          <div>
            <p class="section-eyebrow" id="global-hot-overline"></p>
            <h2 id="global-hot-title"></h2>
            <p class="section-copy" id="global-hot-copy"></p>
          </div>
          <span id="global-result-count"></span>
        </div>
        <div class="rank-strip" id="global-hot-list"></div>
      </section>

      <section class="section-card" id="category-hot-section">
        <div class="section-head">
          <div>
            <p class="section-eyebrow" id="category-hot-overline"></p>
            <h2 id="category-hot-title"></h2>
            <p class="section-copy" id="category-hot-copy"></p>
          </div>
        </div>
        <div class="category-hot-grid" id="category-hot-list"></div>
      </section>

      <section class="section-card" id="catalog-section">
        <div class="catalog-head">
          <h2 id="catalog-title"></h2>
        </div>
        <div class="results-meta" id="results-meta">
          <div class="results-meta-top">
            <span id="catalog-result-count"></span>
            <span id="catalog-result-note"></span>
          </div>
          <div class="results-chip-list" id="active-filter-chips"></div>
        </div>
        <div class="empty-state hidden" id="empty-state">
          <h3 id="empty-state-title"></h3>
          <p id="empty-state-copy"></p>
          <div class="empty-state-actions">
            <button type="button" id="empty-clear-btn"></button>
            <button type="button" class="primary" id="empty-browse-btn"></button>
          </div>
        </div>
        <div class="grid" id="all-cards"></div>
      </section>
    </div>

    <script id="gallery-data" type="application/json">{json_blob(payload)}</script>
    <script>
      const payload = JSON.parse(document.getElementById('gallery-data').textContent);
      const itemsBySlug = new Map(payload.items.map((item) => [item.slug, item]));
      const state = {{
        lang: 'zh',
        search: '',
        category: 'all',
        layout: 'all',
        mode: 'browse',
      }};

      const dom = {{
        masthead: document.querySelector('.masthead'),
        heroEyebrow: document.getElementById('hero-eyebrow'),
        heroTitle: document.getElementById('hero-title'),
        heroDescription: document.getElementById('hero-description'),
        heroMeta: document.getElementById('hero-meta'),
        guideTitle: document.getElementById('guide-title'),
        guideCopy: document.getElementById('guide-copy'),
        guidePathLabel: document.getElementById('guide-path-label'),
        guidePathValue: document.getElementById('guide-path-value'),
        guideSteps: document.getElementById('guide-steps'),
        guideReadmeLink: document.getElementById('guide-readme-link'),
        guideSkillLink: document.getElementById('guide-skill-link'),
        langZh: document.getElementById('lang-zh'),
        langEn: document.getElementById('lang-en'),
        filtersTitle: document.getElementById('filters-title'),
        filtersNote: document.getElementById('filters-note'),
        searchLabel: document.getElementById('search-label'),
        searchInput: document.getElementById('search-input'),
        categoryLabel: document.getElementById('category-label'),
        categorySelect: document.getElementById('category-select'),
        layoutLabel: document.getElementById('layout-label'),
        layoutSelect: document.getElementById('layout-select'),
        resultsToolbarShell: document.getElementById('results-toolbar-shell'),
        resultsToolbarTitle: document.getElementById('results-toolbar-title'),
        resultsToolbarCopy: document.getElementById('results-toolbar-copy'),
        resultsSearchLabel: document.getElementById('results-search-label'),
        resultsSearchInput: document.getElementById('results-search-input'),
        resultsCategoryLabel: document.getElementById('results-category-label'),
        resultsCategorySelect: document.getElementById('results-category-select'),
        resultsLayoutLabel: document.getElementById('results-layout-label'),
        resultsLayoutSelect: document.getElementById('results-layout-select'),
        resultsCountLabel: document.getElementById('results-count-label'),
        resultsCountChip: document.getElementById('results-count-chip'),
        clearFiltersBtn: document.getElementById('clear-filters-btn'),
        returnBrowseBtn: document.getElementById('return-browse-btn'),
        resultsNavShell: document.getElementById('results-nav-shell'),
        resultsNavTitle: document.getElementById('results-nav-title'),
        resultsNavCopy: document.getElementById('results-nav-copy'),
        resultsHotLineLabel: document.getElementById('results-hot-line-label'),
        resultsHotLine: document.getElementById('results-hot-line'),
        resultsCategoryLineLabel: document.getElementById('results-category-line-label'),
        resultsCategoryLine: document.getElementById('results-category-line'),
        globalHotSection: document.getElementById('global-hot-section'),
        globalHotOverline: document.getElementById('global-hot-overline'),
        globalHotTitle: document.getElementById('global-hot-title'),
        globalHotCopy: document.getElementById('global-hot-copy'),
        globalResultCount: document.getElementById('global-result-count'),
        globalHotList: document.getElementById('global-hot-list'),
        categoryHotSection: document.getElementById('category-hot-section'),
        categoryHotOverline: document.getElementById('category-hot-overline'),
        categoryHotTitle: document.getElementById('category-hot-title'),
        categoryHotCopy: document.getElementById('category-hot-copy'),
        categoryHotList: document.getElementById('category-hot-list'),
        catalogSection: document.getElementById('catalog-section'),
        catalogTitle: document.getElementById('catalog-title'),
        resultsMeta: document.getElementById('results-meta'),
        catalogResultCount: document.getElementById('catalog-result-count'),
        catalogResultNote: document.getElementById('catalog-result-note'),
        activeFilterChips: document.getElementById('active-filter-chips'),
        emptyState: document.getElementById('empty-state'),
        emptyStateTitle: document.getElementById('empty-state-title'),
        emptyStateCopy: document.getElementById('empty-state-copy'),
        emptyClearBtn: document.getElementById('empty-clear-btn'),
        emptyBrowseBtn: document.getElementById('empty-browse-btn'),
        allCards: document.getElementById('all-cards'),
      }};

      function strings() {{
        return payload.ui[state.lang];
      }}

      function renderTemplate(template, values) {{
        return template.replace(/\\{{(\\w+)\\}}/g, (_, key) => values[key] ?? '');
      }}

      function thumbMarkup(item, variant = '') {{
        if (item.thumb_path) {{
          return `<div class="thumb-media"><img src="../${{item.thumb_path}}" alt="${{displayName(item)}} thumbnail" loading="lazy" /></div>`;
        }}
        return `<div class="thumb-media"><div class="thumb-fallback ${{variant}}">${{strings().preview_only}}</div></div>`;
      }}

      function joinList(list) {{
        return state.lang === 'zh' ? list.join('、') : list.join(' / ');
      }}

      function hasActiveFilters() {{
        return Boolean(state.search.trim()) || state.category !== 'all' || state.layout !== 'all';
      }}

      function syncModeFromFilters() {{
        state.mode = hasActiveFilters() ? 'results' : 'browse';
      }}

      function displayName(item) {{
        return state.lang === 'zh' ? (item.name_zh || item.name) : item.name;
      }}

      function displayCategory(item) {{
        return state.lang === 'zh' ? item.category_zh : item.category_en;
      }}

      function displayLayout(item) {{
        return state.lang === 'zh' ? item.layout_label_zh : item.layout_label_en;
      }}

      function displayImpression(item) {{
        return state.lang === 'zh' ? item.plain_impression_zh : item.plain_impression_en;
      }}

      function displayBestFor(item) {{
        return state.lang === 'zh' ? item.best_for_zh : item.best_for_en;
      }}

      function displayMood(item) {{
        return state.lang === 'zh' ? item.mood_keywords_zh : item.mood_keywords_en;
      }}

      function displayHotReason(item) {{
        return state.lang === 'zh' ? item.hot_reason_zh : item.hot_reason_en;
      }}

      function searchHaystack(item) {{
        return [
          item.name,
          item.name_zh,
          item.category_en,
          item.category_zh,
          item.layout_label_en,
          item.layout_label_zh,
          item.plain_impression_en,
          item.plain_impression_zh,
          ...(item.best_for_en || []),
          ...(item.best_for_zh || []),
          ...(item.mood_keywords_en || []),
          ...(item.mood_keywords_zh || []),
        ].join(' ').toLowerCase();
      }}

      function categoryLabelByKey(key) {{
        const match = payload.categories.find((category) => category.key === key);
        if (!match) return '';
        return state.lang === 'zh' ? match.zh : match.en;
      }}

      function layoutLabelByKey(key) {{
        const match = payload.layouts.find((layout) => layout.key === key);
        if (!match) return '';
        return state.lang === 'zh' ? match.zh : match.en;
      }}

      function activeFilterItems() {{
        const chips = [];
        if (state.search.trim()) {{
          chips.push(`"${{state.search.trim()}}"`);
        }}
        if (state.category !== 'all') {{
          chips.push(categoryLabelByKey(state.category));
        }}
        if (state.layout !== 'all') {{
          chips.push(layoutLabelByKey(state.layout));
        }}
        return chips;
      }}

      function renderSelectOptions(select, list, allLabel, currentValue) {{
        select.innerHTML = [
          `<option value="all">${{allLabel}}</option>`,
          ...list.map((item) => {{
            const label = state.lang === 'zh' ? item.zh : item.en;
            return `<option value="${{item.key}}">${{label}}</option>`;
          }}),
        ].join('');
        select.value = currentValue;
      }}

      function focusResultsSearch() {{
        requestAnimationFrame(() => {{
          dom.resultsSearchInput.focus();
          const length = dom.resultsSearchInput.value.length;
          dom.resultsSearchInput.setSelectionRange(length, length);
        }});
      }}

      function scrollToResults(keepTyping = false) {{
        requestAnimationFrame(() => {{
          const target = state.mode === 'results' && !dom.resultsNavShell.classList.contains('hidden')
            ? dom.resultsNavShell
            : dom.catalogSection;
          target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          if (keepTyping) {{
            focusResultsSearch();
          }}
        }});
      }}

      function scrollToBrowse() {{
        requestAnimationFrame(() => {{
          dom.masthead.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }});
      }}

      function filteredItems() {{
        const query = state.search.trim().toLowerCase();
        return payload.items.filter((item) => {{
          if (state.category !== 'all' && item.category_key !== state.category) return false;
          if (state.layout !== 'all' && item.layout_key !== state.layout) return false;
          if (!query) return true;
          return searchHaystack(item).includes(query);
        }});
      }}

      function renderHero() {{
        const ui = strings();
        document.title = ui.page_title;
        dom.heroEyebrow.textContent = ui.eyebrow;
        dom.heroTitle.textContent = ui.hero_title;
        dom.heroDescription.textContent = ui.hero_description;
        dom.heroMeta.innerHTML = ui.hero_stats
          .map((chip) => `<span>${{renderTemplate(chip, {{ count: payload.items.length }})}}</span>`)
          .join('');
        dom.guideTitle.textContent = ui.guide_title;
        dom.guideCopy.textContent = ui.guide_copy;
        dom.guidePathLabel.textContent = ui.guide_path_label;
        dom.guidePathValue.textContent = ui.guide_path_value;
        dom.guideSteps.innerHTML = ui.guide_steps.map((step) => `<li>${{step}}</li>`).join('');
        dom.guideReadmeLink.textContent = ui.guide_readme;
        dom.guideSkillLink.textContent = ui.guide_skill;
        dom.langZh.textContent = ui.language_zh;
        dom.langEn.textContent = ui.language_en;
        dom.langZh.classList.toggle('active', state.lang === 'zh');
        dom.langEn.classList.toggle('active', state.lang === 'en');
      }}

      function renderFilters() {{
        const ui = strings();
        dom.filtersTitle.textContent = ui.filters_title;
        dom.filtersNote.textContent = ui.result_note;
        dom.searchLabel.textContent = ui.search_label;
        dom.searchInput.placeholder = ui.search_placeholder;
        dom.categoryLabel.textContent = ui.category_label;
        dom.layoutLabel.textContent = ui.layout_label;
        dom.searchInput.value = state.search;
        renderSelectOptions(dom.categorySelect, payload.categories, ui.category_all, state.category);
        renderSelectOptions(dom.layoutSelect, payload.layouts, ui.layout_all, state.layout);
      }}

      function renderResultsToolbar(items) {{
        const ui = strings();
        const visible = state.mode === 'results';
        dom.resultsToolbarShell.classList.toggle('hidden', !visible);
        if (!visible) {{
          return;
        }}
        dom.resultsToolbarTitle.textContent = ui.results_toolbar_title;
        dom.resultsToolbarCopy.textContent = ui.results_mode_copy;
        dom.resultsSearchLabel.textContent = ui.sticky_search_label;
        dom.resultsCategoryLabel.textContent = ui.sticky_category_label;
        dom.resultsLayoutLabel.textContent = ui.sticky_layout_label;
        dom.resultsSearchInput.placeholder = ui.search_placeholder;
        dom.resultsSearchInput.value = state.search;
        renderSelectOptions(dom.resultsCategorySelect, payload.categories, ui.category_all, state.category);
        renderSelectOptions(dom.resultsLayoutSelect, payload.layouts, ui.layout_all, state.layout);
        dom.resultsCountLabel.textContent = ui.results_count_label;
        dom.resultsCountChip.innerHTML = `<span class="results-chip">${{renderTemplate(ui.result_count, {{ visible: items.length, total: payload.items.length }})}}</span>`;
        dom.clearFiltersBtn.textContent = ui.clear_filters;
        dom.returnBrowseBtn.textContent = ui.return_browse;
      }}

      function compactHotItems() {{
        return payload.global_hot
          .slice(0, 5)
          .map((slug, index) => {{
            const item = itemsBySlug.get(slug);
            return {{
              href: item.preview_url,
              thumb: item.thumb_path ? `../${{item.thumb_path}}` : null,
              title: displayName(item),
              subtitle: renderTemplate(strings().rank_badge, {{ rank: index + 1 }}),
            }};
          }});
      }}

      function compactCategoryItems() {{
        return payload.category_hot
          .slice(0, 6)
          .map((bucket) => {{
            const lead = itemsBySlug.get(bucket.items[0]);
            const label = state.lang === 'zh' ? bucket.category_zh : bucket.category_en;
            return {{
              href: lead.preview_url,
              thumb: lead.thumb_path ? `../${{lead.thumb_path}}` : null,
              title: label,
              subtitle: displayName(lead),
            }};
          }});
      }}

      function renderCompactChips(target, items) {{
        target.innerHTML = items
          .map((item) => `
            <a class="compact-chip" href="${{item.href}}" target="_blank" rel="noreferrer">
              ${{item.thumb ? `<img src="${{item.thumb}}" alt="${{item.title}} thumbnail" loading="lazy" />` : `<span class="compact-chip-icon">${{strings().preview_only}}</span>`}}
              <span class="compact-chip-text">
                <span class="compact-chip-title">${{item.title}}</span>
                <span class="compact-chip-subtitle">${{item.subtitle}}</span>
              </span>
            </a>
          `)
          .join('');
      }}

      function renderResultsNav() {{
        const ui = strings();
        const visible = state.mode === 'results';
        dom.resultsNavShell.classList.toggle('hidden', !visible);
        dom.globalHotSection.classList.toggle('hidden', visible);
        dom.categoryHotSection.classList.toggle('hidden', visible);
        if (!visible) {{
          return;
        }}
        dom.resultsNavTitle.textContent = ui.results_nav_title;
        dom.resultsNavCopy.textContent = ui.results_nav_copy;
        dom.resultsHotLineLabel.textContent = ui.results_hot_line;
        dom.resultsCategoryLineLabel.textContent = ui.results_category_line;
        renderCompactChips(dom.resultsHotLine, compactHotItems());
        renderCompactChips(dom.resultsCategoryLine, compactCategoryItems());
      }}

      function renderGlobalHot() {{
        const ui = strings();
        dom.globalHotOverline.textContent = ui.global_hot_overline;
        dom.globalHotTitle.textContent = ui.global_hot_title;
        dom.globalHotCopy.textContent = ui.global_hot_copy;
        dom.globalResultCount.textContent = renderTemplate(ui.result_count, {{
          visible: payload.items.length,
          total: payload.items.length,
        }});
        dom.globalHotList.innerHTML = payload.global_hot
          .map((slug, index) => {{
            const item = itemsBySlug.get(slug);
            return `
              <article class="rank-card">
                ${{thumbMarkup(item)}}
                <div class="rank-body">
                  <div class="rank-top">
                    <span class="rank-badge">${{renderTemplate(ui.rank_badge, {{ rank: index + 1 }})}}</span>
                    <span class="layout-pill">${{displayLayout(item)}}</span>
                  </div>
                  <h3>${{displayName(item)}}</h3>
                  <p class="rank-category">${{displayCategory(item)}}</p>
                  <p class="clamp-3">${{displayHotReason(item)}}</p>
                  <div class="rank-actions">
                    <a class="primary" href="${{item.preview_url}}" target="_blank" rel="noreferrer">${{ui.preview_entry}}</a>
                  </div>
                </div>
              </article>
            `;
          }})
          .join('');
      }}

      function renderCategoryHot() {{
        const ui = strings();
        dom.categoryHotOverline.textContent = ui.category_hot_overline;
        dom.categoryHotTitle.textContent = ui.category_hot_title;
        dom.categoryHotCopy.textContent = ui.category_hot_copy;
        dom.categoryHotList.innerHTML = payload.category_hot
          .map((bucket) => {{
            const categoryLabel = state.lang === 'zh' ? bucket.category_zh : bucket.category_en;
            const cards = bucket.items
              .map((slug, index) => {{
                const item = itemsBySlug.get(slug);
                return `
                  <article class="mini-card">
                    ${{thumbMarkup(item, 'mini-thumb-fallback')}}
                    <div class="mini-card-body">
                      <div class="rank-top">
                        <span class="mini-pill">${{renderTemplate(ui.rank_badge, {{ rank: index + 1 }})}}</span>
                        <span class="layout-pill">${{displayLayout(item)}}</span>
                      </div>
                      <h4>${{displayName(item)}}</h4>
                      <p class="clamp-2">${{displayHotReason(item)}}</p>
                      <div class="rank-actions">
                        <a class="primary" href="${{item.preview_url}}" target="_blank" rel="noreferrer">${{ui.preview_entry}}</a>
                      </div>
                    </div>
                  </article>
                `;
              }})
              .join('');
            return `
              <section class="category-panel">
                <div class="category-panel-head">
                  <h3>${{categoryLabel}}</h3>
                  <span class="mini-pill">${{ui.category_top_label}}</span>
                </div>
                <div class="mini-list">${{cards}}</div>
              </section>
            `;
          }})
          .join('');
      }}

      function renderAllCards() {{
        const ui = strings();
        const items = filteredItems();
        dom.catalogTitle.textContent = state.mode === 'results' ? ui.results_mode_title : ui.all_styles_title;
        dom.catalogResultCount.textContent = renderTemplate(ui.result_count, {{
          visible: items.length,
          total: payload.items.length,
        }});
        dom.catalogResultNote.textContent = state.mode === 'results' ? ui.browse_reset_hint : ui.result_note;
        dom.resultsMeta.classList.toggle('hidden', state.mode !== 'results');

        const filterChips = activeFilterItems();
        dom.activeFilterChips.innerHTML = filterChips.length
          ? filterChips.map((chip) => `<span class="results-chip">${{chip}}</span>`).join('')
          : `<span class="results-chip">${{ui.active_filters_label}} · ${{ui.no_active_filters}}</span>`;

        dom.emptyStateTitle.textContent = ui.no_results_title;
        dom.emptyStateCopy.textContent = ui.no_results_copy;
        dom.emptyClearBtn.textContent = ui.clear_filters;
        dom.emptyBrowseBtn.textContent = ui.return_browse;

        const hasItems = items.length > 0;
        dom.emptyState.classList.toggle('hidden', hasItems);
        dom.allCards.classList.toggle('hidden', !hasItems);
        if (!hasItems) {{
          dom.allCards.innerHTML = '';
          return items;
        }}

        dom.allCards.innerHTML = items
          .map((item) => `
            <article class="full-card" data-name="${{item.name.toLowerCase()}}">
              <div class="thumb-wrap">
                ${{thumbMarkup(item)}}
              </div>
              <div class="card-body">
                <div class="card-top">
                  <h3>${{displayName(item)}}</h3>
                  <span class="layout-pill">${{displayLayout(item)}}</span>
                </div>
                <p class="category-line">${{displayCategory(item)}}</p>
                <p class="summary clamp-2">${{displayImpression(item)}}</p>
                <dl class="meta">
                  <div><dt>${{ui.best_for_label}}</dt><dd>${{joinList(displayBestFor(item))}}</dd></div>
                  <div><dt>${{ui.mood_label}}</dt><dd>${{joinList(displayMood(item))}}</dd></div>
                </dl>
                <div class="card-actions">
                  <a class="primary" href="${{item.preview_url}}" target="_blank" rel="noreferrer">${{ui.preview_entry}}</a>
                </div>
              </div>
            </article>
          `)
          .join('');
        return items;
      }}

      function applyFilterChange(key, value, options = {{}}) {{
        const previousMode = state.mode;
        state[key] = value;
        syncModeFromFilters();
        const items = render();
        if (state.mode === 'results' && (previousMode !== 'results' || options.scroll)) {{
          scrollToResults(Boolean(options.keepTyping));
        }}
        return items;
      }}

      function clearFilters(options = {{}}) {{
        state.search = '';
        state.category = 'all';
        state.layout = 'all';
        syncModeFromFilters();
        render();
        if (options.scrollTop) {{
          scrollToBrowse();
        }}
      }}

      function render() {{
        syncModeFromFilters();
        renderHero();
        renderFilters();
        const items = filteredItems();
        renderResultsToolbar(items);
        renderResultsNav();
        renderGlobalHot();
        renderCategoryHot();
        renderAllCards();
        return items;
      }}

      dom.langZh.addEventListener('click', () => {{
        state.lang = 'zh';
        render();
      }});
      dom.langEn.addEventListener('click', () => {{
        state.lang = 'en';
        render();
      }});
      dom.searchInput.addEventListener('input', (event) => {{
        applyFilterChange('search', event.target.value, {{ scroll: true, keepTyping: true }});
      }});
      dom.categorySelect.addEventListener('change', (event) => {{
        applyFilterChange('category', event.target.value, {{ scroll: true }});
      }});
      dom.layoutSelect.addEventListener('change', (event) => {{
        applyFilterChange('layout', event.target.value, {{ scroll: true }});
      }});
      dom.resultsSearchInput.addEventListener('input', (event) => {{
        applyFilterChange('search', event.target.value);
      }});
      dom.resultsCategorySelect.addEventListener('change', (event) => {{
        applyFilterChange('category', event.target.value);
      }});
      dom.resultsLayoutSelect.addEventListener('change', (event) => {{
        applyFilterChange('layout', event.target.value);
      }});
      dom.clearFiltersBtn.addEventListener('click', () => {{
        clearFilters();
      }});
      dom.returnBrowseBtn.addEventListener('click', () => {{
        clearFilters({{ scrollTop: true }});
      }});
      dom.emptyClearBtn.addEventListener('click', () => {{
        clearFilters();
      }});
      dom.emptyBrowseBtn.addEventListener('click', () => {{
        clearFilters({{ scrollTop: true }});
      }});

      render();
    </script>
  </body>
</html>
"""


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    references_dir = skill_dir / "references"
    manifest_path = skill_dir / "assets" / "thumbnails" / "manifest.json"
    gallery_dir = skill_dir / "assets" / "gallery"
    gallery_dir.mkdir(parents=True, exist_ok=True)

    catalog = json.loads((references_dir / "style-catalog.json").read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    catalog_by_slug = {entry["slug"]: entry for entry in catalog}

    payload = build_payload(manifest, catalog_by_slug, gallery_dir)
    output_path = gallery_dir / "style-gallery.html"
    output_path.write_text(build_html(payload), encoding="utf-8")
    print(f"Wrote gallery to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

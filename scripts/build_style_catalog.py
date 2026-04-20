#!/usr/bin/env python3
"""Build a bilingual local style catalog from the awesome-design-md README."""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

README_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/README.md"
OFFICIAL_FINGERPRINT_VERSION = "2026-04-v1"

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

CATEGORY_DEFAULTS = {
    "AI & LLM Platforms": {
        "best_for": ["developer-tool", "product-site", "ai-platform"],
        "mood_keywords": ["technical", "future-facing", "developer"],
        "risk_note": "容易偏技术宣传，若产品更生活化会显得冷。",
    },
    "Developer Tools & IDEs": {
        "best_for": ["dashboard", "editor", "docs"],
        "mood_keywords": ["precise", "tooling", "developer"],
        "risk_note": "工具效率很强，但若做品牌营销页会显得克制。",
    },
    "Backend, Database & DevOps": {
        "best_for": ["dashboard", "docs", "developer-tool"],
        "mood_keywords": ["technical", "structured", "dense"],
        "risk_note": "常偏文档或控制台语气，品牌情绪不一定够强。",
    },
    "Productivity & SaaS": {
        "best_for": ["saas", "dashboard", "landing-page"],
        "mood_keywords": ["efficient", "friendly", "product"],
        "risk_note": "通用 SaaS 感较强，需要避免做成普通企业站。",
    },
    "Design & Creative Tools": {
        "best_for": ["editor", "creative-tool", "showcase"],
        "mood_keywords": ["creative", "expressive", "tooling"],
        "risk_note": "创意表达会拉高实现要求，信息秩序要额外控制。",
    },
    "Fintech & Crypto": {
        "best_for": ["dashboard", "pricing", "product-site"],
        "mood_keywords": ["trust", "precision", "finance"],
        "risk_note": "金融语气容易显得冷或压迫，泛消费产品未必适合。",
    },
    "E-commerce & Retail": {
        "best_for": ["landing-page", "commerce", "brand-site"],
        "mood_keywords": ["heroic", "product", "conversion"],
        "risk_note": "图片与品牌素材权重高，素材弱时容易撑不住版面。",
    },
    "Media & Consumer Tech": {
        "best_for": ["landing-page", "editorial", "brand-site"],
        "mood_keywords": ["editorial", "brand", "narrative"],
        "risk_note": "叙事与视觉张力更强，复杂工具流可能不够稳。",
    },
    "Automotive": {
        "best_for": ["brand-site", "launch-page", "showcase"],
        "mood_keywords": ["luxury", "cinematic", "monumental"],
        "risk_note": "气场很重，容易压过产品功能本身。",
    },
}

CATEGORY_LABELS = {
    "AI & LLM Platforms": {"zh": "AI 与大模型平台", "en": "AI & LLM Platforms"},
    "Developer Tools & IDEs": {"zh": "开发者工具与 IDE", "en": "Developer Tools & IDEs"},
    "Backend, Database & DevOps": {"zh": "后端、数据库与 DevOps", "en": "Backend, Database & DevOps"},
    "Productivity & SaaS": {"zh": "效率工具与 SaaS", "en": "Productivity & SaaS"},
    "Design & Creative Tools": {"zh": "设计与创意工具", "en": "Design & Creative Tools"},
    "Fintech & Crypto": {"zh": "金融科技与加密", "en": "Fintech & Crypto"},
    "E-commerce & Retail": {"zh": "电商与零售", "en": "E-commerce & Retail"},
    "Media & Consumer Tech": {"zh": "媒体与消费科技", "en": "Media & Consumer Tech"},
    "Automotive": {"zh": "汽车品牌", "en": "Automotive"},
}

BEST_FOR_LABELS = {
    "dashboard": {"zh": "数据后台", "en": "Dashboards"},
    "editor": {"zh": "编辑器界面", "en": "Editors"},
    "landing-page": {"zh": "落地页", "en": "Landing pages"},
    "docs": {"zh": "文档站", "en": "Documentation"},
    "commerce": {"zh": "电商页面", "en": "Commerce"},
    "editorial": {"zh": "内容专题页", "en": "Editorial pages"},
    "developer-tool": {"zh": "开发者产品页", "en": "Developer tools"},
    "product-site": {"zh": "产品官网", "en": "Product sites"},
    "ai-platform": {"zh": "AI 平台页", "en": "AI platforms"},
    "saas": {"zh": "SaaS 首页", "en": "SaaS homepages"},
    "creative-tool": {"zh": "创作工具页", "en": "Creative tools"},
    "showcase": {"zh": "作品展示页", "en": "Showcases"},
    "brand-site": {"zh": "品牌官网", "en": "Brand sites"},
    "launch-page": {"zh": "发布页", "en": "Launch pages"},
    "pricing": {"zh": "价格页", "en": "Pricing pages"},
    "collaboration": {"zh": "协作场景页", "en": "Collaboration views"},
    "campaign": {"zh": "营销活动页", "en": "Campaign pages"},
}

MOOD_LABELS = {
    "technical": {"zh": "技术感", "en": "Technical"},
    "future-facing": {"zh": "未来感", "en": "Future-facing"},
    "developer": {"zh": "开发者气质", "en": "Developer"},
    "precise": {"zh": "精准克制", "en": "Precise"},
    "precision": {"zh": "秩序精准", "en": "Precision"},
    "tooling": {"zh": "工具导向", "en": "Tooling"},
    "minimal": {"zh": "极简", "en": "Minimal"},
    "cinematic": {"zh": "电影感", "en": "Cinematic"},
    "premium": {"zh": "高级感", "en": "Premium"},
    "creative": {"zh": "创意表达", "en": "Creative"},
    "expressive": {"zh": "表现力强", "en": "Expressive"},
    "friendly": {"zh": "亲和", "en": "Friendly"},
    "product": {"zh": "产品导向", "en": "Product-led"},
    "trust": {"zh": "信任感", "en": "Trust-driven"},
    "finance": {"zh": "金融秩序感", "en": "Financial"},
    "heroic": {"zh": "主视觉强势", "en": "Heroic"},
    "conversion": {"zh": "转化导向", "en": "Conversion-focused"},
    "brand": {"zh": "品牌感", "en": "Brand-led"},
    "narrative": {"zh": "叙事感", "en": "Narrative"},
    "editorial": {"zh": "编辑感", "en": "Editorial"},
    "luxury": {"zh": "奢华气场", "en": "Luxury"},
    "monumental": {"zh": "纪念碑式构图", "en": "Monumental"},
    "bold": {"zh": "大胆张扬", "en": "Bold"},
    "playful": {"zh": "轻松活泼", "en": "Playful"},
    "structured": {"zh": "结构化", "en": "Structured"},
    "dense": {"zh": "信息密度高", "en": "Dense"},
    "elegant": {"zh": "优雅", "en": "Elegant"},
    "gradient": {"zh": "渐变品牌感", "en": "Gradient"},
    "developer-brand": {"zh": "开发者品牌感", "en": "Developer brand"},
    "code-first": {"zh": "代码优先", "en": "Code-first"},
    "emerald": {"zh": "翠绿强调", "en": "Emerald"},
    "efficient": {"zh": "效率优先", "en": "Efficient"},
    "ai-native": {"zh": "AI 原生", "en": "AI-native"},
}

COLOR_HINTS = [
    ("monochrome", "黑白单色"),
    ("black and white", "黑白单色"),
    ("emerald", "黑绿与祖母绿点缀"),
    ("green", "绿色点缀"),
    ("purple", "紫色或紫色渐变"),
    ("blue", "蓝色点缀"),
    ("yellow", "黄色高对比点缀"),
    ("red", "红色点缀"),
    ("orange", "橙色暖调点缀"),
    ("terracotta", "陶土暖色点缀"),
]

TYPOGRAPHY_HINTS = [
    ("editorial", "编辑感、层级明显"),
    ("monospace", "代码感、等宽点缀"),
    ("minimal", "克制、精密"),
    ("premium", "高级、克制"),
    ("bold", "大胆、强标题"),
    ("friendly", "亲和、清晰"),
    ("cinematic", "电影感、画面驱动"),
]

BEST_FOR_KEYWORDS = {
    "dashboard": ["dashboard", "analytics", "monitoring", "data-dense"],
    "editor": ["editor", "canvas", "builder", "command", "ide", "workflow"],
    "landing-page": ["marketing", "brand", "platform", "site", "hero"],
    "docs": ["documentation", "docs", "reading", "developer documentation"],
    "commerce": ["retail", "shopping", "exchange", "payments", "product"],
    "editorial": ["editorial", "media", "magazine", "story"],
}

HOT_SCORE_BASE = {
    "AI & LLM Platforms": 76.0,
    "Developer Tools & IDEs": 80.0,
    "Backend, Database & DevOps": 74.0,
    "Productivity & SaaS": 77.0,
    "Design & Creative Tools": 79.0,
    "Fintech & Crypto": 75.0,
    "E-commerce & Retail": 78.0,
    "Media & Consumer Tech": 77.0,
    "Automotive": 74.0,
}

HOT_SCORE_OVERRIDES = {
    "Apple": 99.0,
    "Stripe": 98.0,
    "Linear": 97.0,
    "Vercel": 96.0,
    "Supabase": 95.0,
    "Cursor": 94.0,
    "Figma": 93.0,
    "Nike": 92.0,
    "Claude": 91.0,
    "Airbnb": 90.0,
    "Notion": 89.0,
    "BMW": 88.0,
    "Framer": 87.0,
    "Shopify": 86.0,
    "WIRED": 86.0,
    "Tesla": 85.0,
    "Raycast": 84.0,
    "Sentry": 84.0,
    "Spotify": 83.0,
    "Warp": 83.0,
    "MongoDB": 82.0,
    "Miro": 82.0,
    "RunwayML": 81.0,
    "Figma": 93.0,
}

HOT_REASON_OVERRIDES = {
    "Apple": {
        "zh": "几乎是“高级科技产品页”的通用参考，辨识度和适配面都很高。",
        "en": "A reliable north star for premium product pages with broad appeal.",
    },
    "Stripe": {
        "zh": "开发者品牌感和商业转化感兼得，做首页和价格页都很稳。",
        "en": "Balances developer-brand polish with strong conversion energy.",
    },
    "Linear": {
        "zh": "工具型产品里最稳的一档，适合高密度但仍想保持秩序的界面。",
        "en": "A top-tier reference for dense but highly ordered product interfaces.",
    },
    "Vercel": {
        "zh": "黑白极简的品牌官网参考，适合想做得克制又专业的项目。",
        "en": "A clean black-and-white benchmark for restrained developer branding.",
    },
    "Supabase": {
        "zh": "深色开发者工具气质强，做现代 SaaS 与后台都很容易出效果。",
        "en": "Strong dark SaaS energy that lands quickly for product and console UI.",
    },
    "Cursor": {
        "zh": "编辑器与 AI 工具方向都能接住，适合偏工作台式产品。",
        "en": "A sharp fit for AI editors and workbench-style interfaces.",
    },
    "Figma": {
        "zh": "创作工具和协作工具都能借鉴，视觉活力和专业感比较平衡。",
        "en": "A balanced pick when you want creative energy without losing rigor.",
    },
    "Nike": {
        "zh": "想要冲击力和品牌态度时，它通常是最直观的参考项。",
        "en": "A fast way to benchmark high-impact brand storytelling and motion energy.",
    },
    "Claude": {
        "zh": "编辑感和 AI 气质结合得很顺，适合内容型或研究型 AI 产品。",
        "en": "Blends editorial calm with AI-native tone for content-rich product surfaces.",
    },
    "Airbnb": {
        "zh": "商业友好、产品感强，适合需要温度和转化力同时在线的页面。",
        "en": "A warm, conversion-ready reference for product-led brand experiences.",
    },
    "BMW": {
        "zh": "奢华、克制、画面感强，适合想要高级品牌气场的展示页。",
        "en": "A strong luxury benchmark for cinematic, high-prestige presentations.",
    },
    "WIRED": {
        "zh": "内容调性非常强，适合做专题感、媒体感或杂志感页面参考。",
        "en": "A high-signal editorial reference for magazine-like layouts and stories.",
    },
}

OVERRIDES = {
    "Apple": {
        "plain_impression_zh": "苹果官网那种克制高级感，留白、精密排版和产品大片一起发力。",
        "plain_impression_en": "Apple-style polish with restrained white space, precise typography, and cinematic product framing.",
        "color_tendency": "黑白灰为主，少量蓝色 CTA 点缀",
        "typography_tone": "克制、精密、电影感",
        "layout_density": "low",
        "brightness": "mixed",
        "best_for": ["landing-page", "product-site", "creative-tool"],
        "mood_keywords": ["minimal", "premium", "cinematic"],
        "risk_note": "很吃留白和素材，复杂后台直接套会显得太薄。",
    },
    "Nike": {
        "plain_impression_zh": "黑白硬朗、超大标题、全幅图片，像运动品牌广告页。",
        "plain_impression_en": "Hard-edged monochrome, massive type, and full-bleed imagery like a sports campaign page.",
        "color_tendency": "黑白基底，颜色交给商品图或少量强调色",
        "typography_tone": "激进、广告化、力量感",
        "layout_density": "medium",
        "brightness": "mixed",
        "best_for": ["brand-site", "commerce", "campaign"],
        "mood_keywords": ["bold", "heroic", "kinetic"],
        "risk_note": "品牌气势很强，但做工具界面会压缩操作效率。",
    },
    "Linear": {
        "plain_impression_zh": "极简精密的工程感工具界面，紫色点缀，密度高但不乱。",
        "plain_impression_en": "An ultra-precise product UI with deep tooling discipline and a cool purple accent.",
        "color_tendency": "深色底加冷紫点缀",
        "typography_tone": "精准、冷静、工程化",
        "layout_density": "high",
        "brightness": "dark",
        "best_for": ["dashboard", "editor", "saas"],
        "mood_keywords": ["precise", "tooling", "minimal"],
        "risk_note": "很稳，但如果你想要强品牌记忆点，可能不够戏剧化。",
    },
    "Stripe": {
        "plain_impression_zh": "紫色渐变和轻盈排版一起营造出高级开发者品牌感。",
        "plain_impression_en": "Soft gradients and elegant typography create a premium developer-brand feel.",
        "color_tendency": "浅底或深底都能配合紫色渐变",
        "typography_tone": "轻、优雅、科技品牌感",
        "layout_density": "medium",
        "brightness": "mixed",
        "best_for": ["landing-page", "pricing", "developer-tool"],
        "mood_keywords": ["elegant", "gradient", "developer-brand"],
        "risk_note": "若组件过密，轻盈感会被挤掉，容易只剩渐变表面功夫。",
    },
    "Vercel": {
        "plain_impression_zh": "黑白极简、字距精准，属于开发者世界里最稳的品牌官网语言。",
        "plain_impression_en": "A black-and-white developer brand language that feels exact, calm, and highly controlled.",
        "color_tendency": "黑白为主，少量中性灰",
        "typography_tone": "精准、简洁、克制",
        "layout_density": "medium",
        "brightness": "mixed",
        "best_for": ["landing-page", "docs", "developer-tool"],
        "mood_keywords": ["minimal", "precise", "developer"],
        "risk_note": "很稳，但如果产品需要亲和力或趣味，会偏冷。",
    },
    "Supabase": {
        "plain_impression_zh": "深色开发者工具质感，带一点绿色生命力，适合现代 SaaS。",
        "plain_impression_en": "A dark code-first aesthetic with green vitality, well suited to modern SaaS and tools.",
        "color_tendency": "深色底加绿色强调",
        "typography_tone": "开发者友好、稳、直接",
        "layout_density": "high",
        "brightness": "dark",
        "best_for": ["dashboard", "docs", "developer-tool"],
        "mood_keywords": ["code-first", "tooling", "emerald"],
        "risk_note": "工具风很强，若做消费级品牌页可能不够情绪化。",
    },
    "Figma": {
        "plain_impression_zh": "多彩但专业，既像创作工具，也像协作平台。",
        "plain_impression_en": "Colorful yet disciplined, sitting neatly between a creative tool and a collaboration platform.",
        "color_tendency": "多彩点缀搭配清晰中性色",
        "typography_tone": "灵活、现代、创意协作感",
        "layout_density": "medium",
        "brightness": "mixed",
        "best_for": ["editor", "creative-tool", "collaboration"],
        "mood_keywords": ["creative", "playful", "tooling"],
        "risk_note": "多彩元素一多就容易乱，信息层级必须压得住。",
    },
    "Cursor": {
        "plain_impression_zh": "深色编辑器气质很强，带一点蓝色梯度，适合工作台式 AI 产品。",
        "plain_impression_en": "A sleek dark editor style with cool blue accents and obvious workbench energy.",
        "hot_score": 94.0,
    },
    "Claude": {
        "plain_impression_zh": "暖陶土色加干净编辑式布局，很适合研究感或内容感更强的 AI 产品。",
        "plain_impression_en": "Warm terracotta tones and an editorial layout give it a calm, research-friendly AI feel.",
        "hot_score": 91.0,
    },
    "Airbnb": {
        "plain_impression_zh": "温暖、商业友好、产品感强，适合需要亲和力和转化力并存的页面。",
        "plain_impression_en": "Warm, commercial, and product-led, with strong hospitality and conversion energy.",
        "hot_score": 90.0,
    },
    "BMW": {
        "plain_impression_zh": "深色奢华表面配合硬朗构图，适合想做高级品牌展示的页面。",
        "plain_impression_en": "Dark premium surfaces and controlled drama make it a strong luxury showcase reference.",
        "hot_score": 88.0,
    },
    "WIRED": {
        "plain_impression_zh": "纸媒密度和科技杂志气质很强，适合内容专题和媒体感页面。",
        "plain_impression_en": "Dense, magazine-like, and highly editorial, with a strong tech publication voice.",
        "hot_score": 86.0,
    },
}


@dataclass
class StyleEntry:
    name: str
    name_zh: str
    slug: str
    category: str
    category_zh: str
    category_en: str
    design_url: str
    preview_url: str
    official_fingerprint_version: str
    summary: str
    plain_impression: str
    plain_impression_zh: str
    plain_impression_en: str
    color_tendency: str
    typography_tone: str
    layout_density: str
    brightness: str
    best_for: list[str]
    best_for_zh: list[str]
    best_for_en: list[str]
    mood_keywords: list[str]
    mood_keywords_zh: list[str]
    mood_keywords_en: list[str]
    risk_note: str
    suitable_for: list[str]
    hot_score: float
    hot_reason_zh: str
    hot_reason_en: str
    source: str


def fetch_readme(url: str) -> str:
    req = Request(url, headers={"User-Agent": "style-compass/1.0"})
    try:
        with urlopen(req) as response:
            return response.read().decode("utf-8")
    except (ssl.SSLCertVerificationError, URLError) as exc:
        reason = getattr(exc, "reason", exc)
        if not isinstance(reason, ssl.SSLCertVerificationError) and "CERTIFICATE_VERIFY_FAILED" not in str(reason):
            raise
        insecure = ssl._create_unverified_context()
        with urlopen(req, context=insecure) as response:
            print("[WARN] SSL certificate verification failed; retried with insecure context.", file=sys.stderr)
            return response.read().decode("utf-8")


def slug_from_design_url(design_url: str) -> str:
    match = re.match(r"https://getdesign\.md/([^/]+)/design-md/?$", design_url)
    if not match:
        raise ValueError(f"Unexpected design URL: {design_url}")
    return match.group(1)


def preview_from_slug(slug: str) -> str:
    return f"https://getdesign.md/design-md/{slug}/preview.html"


def infer_color(summary: str) -> str:
    lower = summary.lower()
    for needle, label in COLOR_HINTS:
        if needle in lower:
            return label
    if "dark" in lower:
        return "深色基底"
    if "white" in lower or "light" in lower or "cream" in lower:
        return "浅色基底"
    return "中性色基底"


def infer_typography(summary: str) -> str:
    lower = summary.lower()
    for needle, label in TYPOGRAPHY_HINTS:
        if needle in lower:
            return label
    if "precise" in lower or "clean" in lower:
        return "精准、清爽"
    return "现代、清晰"


def infer_density(summary: str, category: str) -> str:
    lower = summary.lower()
    if "data-dense" in lower or "technical" in lower:
        return "high"
    if "minimal" in lower or "white space" in lower or "clean white canvas" in lower:
        return "low"
    if category in {"Developer Tools & IDEs", "Backend, Database & DevOps"}:
        return "high"
    return "medium"


def infer_brightness(summary: str) -> str:
    lower = summary.lower()
    if "dark" in lower or "black" in lower:
        return "dark"
    if "white" in lower or "light" in lower or "cream" in lower:
        return "light"
    return "mixed"


def dedupe_preserve(items: list[str]) -> list[str]:
    seen: list[str] = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def infer_best_for(summary: str, category: str) -> list[str]:
    lower = summary.lower()
    best_for: list[str] = []
    for label, needles in BEST_FOR_KEYWORDS.items():
        if any(needle in lower for needle in needles):
            best_for.append(label)
    best_for.extend(CATEGORY_DEFAULTS[category]["best_for"])
    return dedupe_preserve(best_for)


def infer_mood_keywords(summary: str, category: str) -> list[str]:
    words = set(CATEGORY_DEFAULTS[category]["mood_keywords"])
    lower = summary.lower()
    for token in (
        "minimal",
        "cinematic",
        "friendly",
        "bold",
        "precise",
        "playful",
        "luxury",
        "technical",
        "editorial",
        "narrative",
        "gradient",
        "trust",
        "conversion",
        "future-facing",
        "heroic",
        "elegant",
        "efficient",
    ):
        if token in lower:
            words.add(token)
    return sorted(words)


def translate_list(items: list[str], mapping: dict[str, dict[str, str]], lang: str) -> list[str]:
    return [mapping.get(item, {}).get(lang, item.replace("-", " ").title()) for item in items]


def chinese_join(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return "、".join(items)


def infer_name_zh(name: str) -> str:
    return name


def infer_plain_impression_zh(
    name: str,
    category: str,
    color_tendency: str,
    typography_tone: str,
    best_for: list[str],
    mood_keywords: list[str],
) -> str:
    best_for_zh = translate_list(best_for[:2], BEST_FOR_LABELS, "zh")
    mood_zh = translate_list(mood_keywords[:2], MOOD_LABELS, "zh")
    category_zh = CATEGORY_LABELS[category]["zh"]
    pieces = [f"{name} 偏{category_zh}路线", color_tendency, typography_tone]
    if mood_zh:
        pieces.append(f"整体更偏{chinese_join(mood_zh)}")
    tail = f"适合{chinese_join(best_for_zh)}这类页面。" if best_for_zh else "适合做风格参考。"
    return "，".join(pieces) + "，" + tail


def infer_hot_score(name: str, category: str, best_for: list[str], mood_keywords: list[str]) -> float:
    if name in HOT_SCORE_OVERRIDES:
        return HOT_SCORE_OVERRIDES[name]

    score = HOT_SCORE_BASE[category]
    if "landing-page" in best_for:
        score += 1.5
    if "dashboard" in best_for:
        score += 1.0
    if "brand-site" in best_for:
        score += 1.0
    if "editorial" in best_for:
        score += 0.8
    if "minimal" in mood_keywords:
        score += 0.4
    if "bold" in mood_keywords or "luxury" in mood_keywords:
        score += 0.6
    if name in HIGH_FREQUENCY_NAMES:
        score += 2.0
    return round(score, 1)


def infer_hot_reason_zh(name: str, category: str, best_for: list[str], mood_keywords: list[str]) -> str:
    if name in HOT_REASON_OVERRIDES:
        return HOT_REASON_OVERRIDES[name]["zh"]

    best_for_zh = translate_list(best_for[:1], BEST_FOR_LABELS, "zh")
    mood_zh = translate_list(mood_keywords[:1], MOOD_LABELS, "zh")
    category_zh = CATEGORY_LABELS[category]["zh"]
    focus = best_for_zh[0] if best_for_zh else "风格比较"
    tone = mood_zh[0] if mood_zh else "辨识度"
    return f"在{category_zh}里属于{tone}比较强的一档，拿来做{focus}参考很顺手。"


def infer_hot_reason_en(name: str, category: str, best_for: list[str], mood_keywords: list[str]) -> str:
    if name in HOT_REASON_OVERRIDES:
        return HOT_REASON_OVERRIDES[name]["en"]

    best_for_en = translate_list(best_for[:1], BEST_FOR_LABELS, "en")
    mood_en = translate_list(mood_keywords[:1], MOOD_LABELS, "en")
    focus = best_for_en[0].lower() if best_for_en else "style exploration"
    tone = mood_en[0].lower() if mood_en else "high-signal"
    return f"Strong {tone} energy for {focus} in this style cluster."


def enrich_entry(category: str, name: str, design_url: str, summary: str) -> StyleEntry:
    slug = slug_from_design_url(design_url)
    base = CATEGORY_DEFAULTS[category]

    payload = {
        "name": name,
        "slug": slug,
        "category": category,
        "category_zh": CATEGORY_LABELS[category]["zh"],
        "category_en": CATEGORY_LABELS[category]["en"],
        "design_url": design_url,
        "preview_url": preview_from_slug(slug),
        "official_fingerprint_version": OFFICIAL_FINGERPRINT_VERSION,
        "summary": summary,
        "color_tendency": infer_color(summary),
        "typography_tone": infer_typography(summary),
        "layout_density": infer_density(summary, category),
        "brightness": infer_brightness(summary),
        "best_for": infer_best_for(summary, category),
        "mood_keywords": infer_mood_keywords(summary, category),
        "risk_note": base["risk_note"],
        "suitable_for": base["best_for"],
        "source": README_URL,
    }

    payload.update(OVERRIDES.get(name, {}))

    payload["name_zh"] = payload.get("name_zh") or infer_name_zh(name)
    payload["best_for_zh"] = payload.get("best_for_zh") or translate_list(payload["best_for"], BEST_FOR_LABELS, "zh")
    payload["best_for_en"] = payload.get("best_for_en") or translate_list(payload["best_for"], BEST_FOR_LABELS, "en")
    payload["mood_keywords_zh"] = payload.get("mood_keywords_zh") or translate_list(payload["mood_keywords"], MOOD_LABELS, "zh")
    payload["mood_keywords_en"] = payload.get("mood_keywords_en") or translate_list(payload["mood_keywords"], MOOD_LABELS, "en")
    payload["plain_impression_zh"] = payload.get("plain_impression_zh") or infer_plain_impression_zh(
        name=name,
        category=category,
        color_tendency=payload["color_tendency"],
        typography_tone=payload["typography_tone"],
        best_for=payload["best_for"],
        mood_keywords=payload["mood_keywords"],
    )
    payload["plain_impression_en"] = payload.get("plain_impression_en") or summary.rstrip(".")
    payload["plain_impression"] = payload["plain_impression_zh"]
    payload["hot_score"] = payload.get("hot_score") or infer_hot_score(name, category, payload["best_for"], payload["mood_keywords"])
    payload["hot_reason_zh"] = payload.get("hot_reason_zh") or infer_hot_reason_zh(
        name, category, payload["best_for"], payload["mood_keywords"]
    )
    payload["hot_reason_en"] = payload.get("hot_reason_en") or infer_hot_reason_en(
        name, category, payload["best_for"], payload["mood_keywords"]
    )

    return StyleEntry(**payload)


def parse_collection(readme: str) -> list[StyleEntry]:
    section_pattern = re.compile(r"^### (.+)$", re.MULTILINE)
    item_pattern = re.compile(r"^- \[\*\*(.+?)\*\*\]\((https://getdesign\.md/[^)]+/design-md)\) - (.+)$")
    lines = readme.splitlines()
    current_category = None
    entries: list[StyleEntry] = []
    categories = set(CATEGORY_DEFAULTS)

    for line in lines:
        category_match = section_pattern.match(line)
        if category_match:
            name = category_match.group(1).strip()
            current_category = name if name in categories else current_category
            continue
        item_match = item_pattern.match(line)
        if item_match and current_category:
            style_name, design_url, summary = item_match.groups()
            entries.append(enrich_entry(current_category, style_name, design_url, summary.strip()))
    return entries


def markdown_for(entries: list[StyleEntry]) -> str:
    grouped: dict[str, list[StyleEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.category, []).append(entry)

    lines = [
        "# 风格目录",
        "",
        f"上游来源：`{README_URL}`",
        "",
        f"当前快照共 {len(entries)} 个风格，供 `style-compass` 推荐脚本与本地 gallery 使用。",
        "",
    ]

    for category in CATEGORY_DEFAULTS:
        bucket = grouped.get(category, [])
        if not bucket:
            continue
        lines.append(f"## {CATEGORY_LABELS[category]['zh']} / {category}")
        lines.append("")
        for entry in bucket:
            lines.extend(
                [
                    f"### {entry.name}",
                    f"- 设计入口：{entry.design_url}",
                    f"- 规范预览：{entry.preview_url}",
                    f"- 中文印象：{entry.plain_impression_zh}",
                    f"- English impression: {entry.plain_impression_en}",
                    f"- 热门分：{entry.hot_score}",
                    f"- 热门理由：{entry.hot_reason_zh}",
                    f"- 主色倾向：{entry.color_tendency}",
                    f"- 排版气质：{entry.typography_tone}",
                    f"- 版式密度：{entry.layout_density}",
                    f"- 典型适用页面：{chinese_join(entry.best_for_zh[:3])}",
                    f"- 情绪关键词：{chinese_join(entry.mood_keywords_zh[:3])}",
                    f"- 风险：{entry.risk_note}",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=README_URL, help="README source URL")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1] / "references"),
        help="Directory for generated catalog files",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        readme = fetch_readme(args.url)
    except Exception as exc:  # pragma: no cover - network
        print(f"[ERROR] Failed to fetch README: {exc}", file=sys.stderr)
        return 1

    entries = parse_collection(readme)
    if not entries:
        print("[ERROR] No style entries parsed from README.", file=sys.stderr)
        return 1

    json_path = output_dir / "style-catalog.json"
    md_path = output_dir / "style-catalog.md"

    json_path.write_text(
        json.dumps([asdict(entry) for entry in entries], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(markdown_for(entries), encoding="utf-8")

    print(f"Wrote {len(entries)} entries to {json_path}")
    print(f"Wrote catalog markdown to {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate local SVG thumbnail cards for the full style catalog."""

from __future__ import annotations

import json
from pathlib import Path

AUDIT_VERSION = "2026-04-v1"

HIGH_FREQUENCY_OVERRIDES = {
    "Apple": {
        "bg": "#f5f5f7",
        "panel": "#ffffff",
        "text": "#111111",
        "muted": "#6e6e73",
        "accent": "#0071e3",
        "kicker": "PREMIUM MINIMAL",
        "headline": "Apple",
        "subhead": "留白、精密排版、产品感",
        "layout": "hero-light",
    },
    "Nike": {
        "bg": "#0b0b0b",
        "panel": "#151515",
        "text": "#ffffff",
        "muted": "#b7b7b7",
        "accent": "#ffffff",
        "kicker": "MOVE FAST",
        "headline": "NIKE",
        "subhead": "超大标题 + 满版视觉冲击",
        "layout": "poster",
    },
    "Linear": {
        "bg": "#ffffff",
        "panel": "#f6f5fb",
        "text": "#111111",
        "muted": "#6b7280",
        "accent": "#5e6ad2",
        "kicker": "WORKFLOW UI",
        "headline": "Linear",
        "subhead": "极简精密、工程气质、秩序很强",
        "layout": "hero-light",
    },
    "Stripe": {
        "bg": "#f7f4ff",
        "panel": "#ffffff",
        "text": "#1f1235",
        "muted": "#6a5a8c",
        "accent": "#635bff",
        "kicker": "DEVELOPER BRAND",
        "headline": "Stripe",
        "subhead": "轻盈渐变、品牌感、技术优雅",
        "layout": "hero-light",
    },
    "Vercel": {
        "bg": "#ffffff",
        "panel": "#fafafa",
        "text": "#111111",
        "muted": "#6b7280",
        "accent": "#111111",
        "kicker": "PRECISE B/W",
        "headline": "Vercel",
        "subhead": "黑白极简、开发者官网质感",
        "layout": "hero-light",
    },
    "Supabase": {
        "bg": "#0f1720",
        "panel": "#111827",
        "text": "#eefaf4",
        "muted": "#86a89c",
        "accent": "#3ecf8e",
        "kicker": "CODE-FIRST SAAS",
        "headline": "Supabase",
        "subhead": "深色工具感 + 绿色生命力",
        "layout": "dashboard",
    },
    "Figma": {
        "bg": "#f4f1ff",
        "panel": "#ffffff",
        "text": "#13111c",
        "muted": "#6f6785",
        "accent": "#7b61ff",
        "kicker": "CREATIVE TOOL",
        "headline": "Figma",
        "subhead": "多彩、专业、协作与创作并存",
        "layout": "creative",
    },
    "Cursor": {
        "bg": "#0d1018",
        "panel": "#141826",
        "text": "#eff2ff",
        "muted": "#8f97b1",
        "accent": "#5a7cff",
        "kicker": "AI EDITOR",
        "headline": "Cursor",
        "subhead": "深色编辑器、梯度点缀、强工具感",
        "layout": "dashboard",
    },
    "Sentry": {
        "bg": "#ffffff",
        "panel": "#f1eef9",
        "text": "#1f1633",
        "muted": "#746a8f",
        "accent": "#6c5ce7",
        "kicker": "ERROR STACK",
        "headline": "Sentry",
        "subhead": "紫色工程感、监控堆栈、结构清楚",
        "layout": "sentry-docs",
        "button_radius": "soft",
    },
    "xAI": {
        "bg": "#f8f8f8",
        "panel": "#ffffff",
        "text": "#1f2228",
        "muted": "#6f737b",
        "accent": "#1f2228",
        "kicker": "TRY GROK",
        "headline": "xAI",
        "subhead": "极简未来感、等宽字、黑白精密",
        "layout": "xai-mono",
        "button_radius": "soft",
    },
    "Zapier": {
        "bg": "#fffdf9",
        "panel": "#fffefb",
        "text": "#2a1917",
        "muted": "#8b7d75",
        "accent": "#ff5a1f",
        "kicker": "START FREE",
        "headline": "Zapier",
        "subhead": "暖白产品页、橙色点火、友好转化",
        "layout": "zapier-launchpad",
        "button_radius": "pill",
    },
    "Sanity": {
        "bg": "#090909",
        "panel": "#141414",
        "text": "#f5f5f5",
        "muted": "#8d8d93",
        "accent": "#f36458",
        "kicker": "CONTENT CLOUD",
        "headline": "Sanity",
        "subhead": "深色内容中台、结构清楚、红色点火",
        "layout": "dashboard-slab",
        "button_radius": "pill",
    },
    "Kraken": {
        "bg": "#ffffff",
        "panel": "#f6f3ff",
        "text": "#171717",
        "muted": "#6b7280",
        "accent": "#7132f5",
        "kicker": "FINTECH SYSTEM",
        "headline": "Kraken",
        "subhead": "白底紫色、金融精度、信任感强",
        "layout": "hero-light",
        "button_radius": "pill",
    },
    "Ollama": {
        "bg": "#ffffff",
        "panel": "#f5f5f5",
        "text": "#111111",
        "muted": "#707070",
        "accent": "#111111",
        "kicker": "LOCAL LLM",
        "headline": "Ollama",
        "subhead": "极简本地模型感、黑白单色、很克制",
        "layout": "hero-light",
        "button_radius": "soft",
    },
    "The Verge": {
        "bg": "#ffffff",
        "panel": "#ffffff",
        "text": "#101010",
        "muted": "#5b6470",
        "accent": "#3cffd0",
        "kicker": "EDITORIAL HAZARD",
        "headline": "The Verge",
        "subhead": "白底大标题、新闻锋利感、霓虹点缀",
        "layout": "editorial",
        "button_radius": "pill",
    },
    "Together AI": {
        "bg": "#faf6ff",
        "panel": "#ffffff",
        "text": "#101124",
        "muted": "#6b7280",
        "accent": "#ef2cc1",
        "kicker": "DEVELOPER SYSTEM",
        "headline": "Together AI",
        "subhead": "轻盈渐变、粉橙品牌感、开发者入口",
        "layout": "hero-light",
        "button_radius": "pill",
    },
    "Framer": {
        "bg": "#050505",
        "panel": "#111111",
        "text": "#ffffff",
        "muted": "#97a0aa",
        "accent": "#0099ff",
        "kicker": "MOTION SYSTEM",
        "headline": "Framer",
        "subhead": "黑底蓝光、动效优先、锋利创意感",
        "layout": "hero-light",
        "button_radius": "pill",
    },
    "Cal.com": {
        "bg": "#ffffff",
        "panel": "#f5f5f5",
        "text": "#111111",
        "muted": "#707070",
        "accent": "#111111",
        "kicker": "SCHEDULING CORE",
        "headline": "Cal.com",
        "subhead": "白底黑字、效率优先、极简日历产品",
        "layout": "hero-light",
        "button_radius": "soft",
    },
    "MongoDB": {
        "bg": "#022b38",
        "panel": "#0a3543",
        "text": "#f3f7f8",
        "muted": "#9ab0b7",
        "accent": "#00ed64",
        "kicker": "INFRA SYSTEM",
        "headline": "MongoDB",
        "subhead": "深绿蓝底、开发者文档感、品牌很强",
        "layout": "hero-light",
        "button_radius": "pill",
    },
    "Replicate": {
        "bg": "#f5426f",
        "panel": "#ff7b52",
        "text": "#ffffff",
        "muted": "#ffe3ea",
        "accent": "#1f1f1f",
        "kicker": "MODEL PLATFORM",
        "headline": "Replicate",
        "subhead": "高饱和红粉渐变、模型平台、很醒目",
        "layout": "poster",
        "button_radius": "pill",
    },
    "RunwayML": {
        "bg": "#040404",
        "panel": "#0e1016",
        "text": "#f4f4f6",
        "muted": "#8f96a2",
        "accent": "#8b8cff",
        "kicker": "GEN-VIDEO",
        "headline": "RunwayML",
        "subhead": "电影感黑场、偏影像、很像片头封面",
        "layout": "hero-light",
        "button_radius": "soft",
    },
}

LAYOUT_LABELS = {
    "hero-light": "Hero",
    "dashboard": "Dashboard",
    "poster": "Poster",
    "creative": "Creative",
    "editorial": "Editorial",
    "docs-grid": "Docs",
    "commerce-split": "Commerce",
    "luxury-banner": "Luxury",
    "ai-capsule": "AI Capsule",
    "product-stack": "Product",
    "editor-workbench": "Workbench",
    "sentry-docs": "Docs",
    "xai-mono": "Docs",
    "zapier-launchpad": "Docs",
    "token-catalog-light": "Docs",
    "token-catalog-dark": "Docs",
    "token-catalog-warm": "Docs",
    "editorial-cascade": "Editorial",
    "dashboard-slab": "Dashboard",
}

ACCENT_MAP = [
    ("黑白灰", "#0071e3"),
    ("黑白基底", "#ffffff"),
    ("黑白单色", "#f5f5f5"),
    ("蓝色", "#3b82f6"),
    ("绿色", "#3ecf8e"),
    ("黑绿", "#3ecf8e"),
    ("紫色", "#7c6cff"),
    ("黄色", "#facc15"),
    ("红色", "#ef4444"),
    ("橙色", "#f97316"),
    ("陶土", "#c9735b"),
    ("中性色", "#6b7280"),
    ("多彩", "#7b61ff"),
]

MOOD_KICKERS = {
    "minimal": "PRECISE MINIMAL",
    "premium": "PREMIUM SYSTEM",
    "cinematic": "CINEMATIC BRAND",
    "tooling": "TOOLING UI",
    "developer": "DEVELOPER SYSTEM",
    "creative": "CREATIVE TOOL",
    "playful": "PLAYFUL SYSTEM",
    "luxury": "LUXURY SURFACE",
    "editorial": "EDITORIAL MODE",
    "conversion": "CONVERSION FIRST",
}


def derive_accent(color_tendency: str) -> str:
    for needle, value in ACCENT_MAP:
        if needle in color_tendency:
            return value
    return "#7c6cff"


def lighten(hex_color: str, factor: float) -> str:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def darken(hex_color: str, factor: float) -> str:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def choose_layout(entry: dict) -> str:
    moods = set(entry.get("mood_keywords", []))
    best_for = set(entry.get("best_for", []))
    category = entry["category"]

    if category == "Automotive" or {"luxury", "monumental"} & moods:
        return "luxury-banner"
    if {"commerce", "campaign"} & best_for or {"conversion", "heroic", "kinetic"} & moods:
        return "commerce-split"
    if "editorial" in best_for or {"editorial", "narrative"} & moods:
        return "editorial"
    if "ai-platform" in best_for or {"future-facing", "ai-native"} & moods:
        return "ai-capsule"
    if "docs" in best_for and entry.get("layout_density") != "high":
        return "docs-grid"
    if "editor" in best_for and entry.get("brightness") == "dark":
        return "editor-workbench"
    if "creative" in moods or "playful" in moods or "creative-tool" in best_for or category == "Design & Creative Tools":
        return "creative"
    if "dashboard" in best_for or entry.get("layout_density") == "high" or {"dense", "structured", "tooling"} & moods:
        return "dashboard"
    if "product-site" in best_for or {"product", "friendly", "trust"} & moods:
        return "product-stack"
    if category in {"E-commerce & Retail", "Automotive"} or "cinematic" in moods or "luxury" in moods:
        return "poster"
    return "hero-light"


def choose_palette(entry: dict) -> dict[str, str]:
    accent = derive_accent(entry["color_tendency"])
    brightness = entry["brightness"]
    density = entry["layout_density"]

    if brightness == "dark":
        bg = "#0d1117"
        panel = lighten(bg, 0.06)
        text = "#f5f7fb"
        muted = "#94a3b8"
    elif brightness == "light":
        bg = "#f8fafc"
        panel = "#ffffff"
        text = "#111827"
        muted = "#64748b"
    else:
        if density == "low":
            bg = lighten(accent, 0.92)
            panel = "#ffffff"
            text = "#111827"
            muted = "#6b7280"
        else:
            bg = "#f5f7fb"
            panel = "#ffffff"
            text = "#0f172a"
            muted = "#64748b"

    if entry["name"] in {"xAI", "Ollama", "SpaceX", "Ferrari", "Bugatti"}:
        bg = "#0b0b0c"
        panel = "#141518"
        text = "#f5f5f5"
        muted = "#9ca3af"
    return {"bg": bg, "panel": panel, "text": text, "muted": muted, "accent": accent}


def choose_kicker(entry: dict) -> str:
    for mood in entry.get("mood_keywords", []):
        if mood in MOOD_KICKERS:
            return MOOD_KICKERS[mood]
    category_tokens = {
        "AI & LLM Platforms": "AI PLATFORM",
        "Developer Tools & IDEs": "DEV TOOL",
        "Backend, Database & DevOps": "INFRA SYSTEM",
        "Productivity & SaaS": "PRODUCT SYSTEM",
        "Design & Creative Tools": "CREATIVE TOOL",
        "Fintech & Crypto": "FINTECH SYSTEM",
        "E-commerce & Retail": "BRAND COMMERCE",
        "Media & Consumer Tech": "CONSUMER TECH",
        "Automotive": "LUXURY MOTION",
    }
    return category_tokens.get(entry["category"], "STYLE SYSTEM")


def subhead_for(entry: dict) -> str:
    plain = entry.get("plain_impression", "").strip()
    if "，" in plain:
        plain = plain.split("，", 1)[1].strip()
    if "：" in plain:
        plain = plain.split("：", 1)[-1].strip()
    if len(plain) > 20:
        plain = plain[:20] + "…"
    return plain or entry["summary"][:20]


def generic_style(entry: dict) -> dict:
    palette = choose_palette(entry)
    return {
        **palette,
        "kicker": choose_kicker(entry),
        "headline": entry["name"],
        "subhead": subhead_for(entry),
        "layout": choose_layout(entry),
        "mood_keywords": list(entry.get("mood_keywords", [])),
        "best_for": list(entry.get("best_for", [])),
    }


def style_for_entry(entry: dict) -> dict:
    style = dict(generic_style(entry))
    style.update(HIGH_FREQUENCY_OVERRIDES.get(entry["name"], {}))
    return style


def svg_for(style: dict) -> str:
    bg = style["bg"]
    panel = style["panel"]
    text = style["text"]
    muted = style["muted"]
    accent = style["accent"]
    kicker = style["kicker"]
    headline = style["headline"]
    subhead = style["subhead"]
    layout = style["layout"]
    button_radius = style.get("button_radius", "pill")

    soft = lighten(accent, 0.55)
    soft2 = lighten(accent, 0.28)
    dark = darken(accent, 0.18)
    button_rx = {"pill": 20, "soft": 14, "sharp": 8}.get(button_radius, 20)
    small_button_rx = max(8, button_rx - 2)

    if layout == "poster":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="24" y="24" width="720" height="384" rx="30" fill="{panel}"/>
  <rect x="40" y="40" width="688" height="352" rx="24" fill="{soft}" fill-opacity="0.08"/>
  <path d="M82 330C190 236 286 180 460 140C566 116 646 98 706 70V362H82V330Z" fill="{accent}" fill-opacity="0.16"/>
  <rect x="64" y="60" width="96" height="12" rx="6" fill="#ffffff" fill-opacity="0.16"/>
  <text x="64" y="286" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="84" font-weight="900" letter-spacing="-2">{headline}</text>
  <text x="64" y="324" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="600">{subhead}</text>
  <rect x="64" y="346" width="138" height="36" rx="{small_button_rx}" fill="#ffffff" fill-opacity="0.08"/>
  <text x="92" y="369" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700">Campaign</text>
  <text x="548" y="86" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="2">{kicker}</text>
</svg>
"""
    if layout == "sentry-docs":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="32" width="704" height="368" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.12"/>
  <rect x="56" y="56" width="656" height="54" rx="18" fill="#ffffff" fill-opacity="0.96"/>
  <text x="84" y="90" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800" letter-spacing="2">{kicker}</text>
  <rect x="594" y="68" width="88" height="28" rx="14" fill="{accent}" fill-opacity="0.12"/>
  <text x="616" y="87" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="700">TRACES</text>
  <text x="80" y="180" fill="{text}" fill-opacity="0.18" font-family="Helvetica, Arial, sans-serif" font-size="72" font-weight="900" letter-spacing="-2">{headline}</text>
  <rect x="82" y="206" width="180" height="12" rx="6" fill="{muted}" fill-opacity="0.18"/>
  <rect x="82" y="230" width="148" height="12" rx="6" fill="{muted}" fill-opacity="0.12"/>
  <rect x="82" y="280" width="154" height="40" rx="14" fill="{accent}" fill-opacity="0.10"/>
  <text x="114" y="306" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="17" font-weight="700">Resolve</text>
  <rect x="82" y="338" width="134" height="26" rx="13" fill="{accent}" fill-opacity="0.08"/>
  <text x="108" y="356" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="800">Issue Feed</text>
  <rect x="404" y="146" width="276" height="216" rx="24" fill="#ffffff" fill-opacity="0.98"/>
  <rect x="426" y="170" width="232" height="26" rx="13" fill="{accent}" fill-opacity="0.08"/>
  <rect x="426" y="212" width="102" height="108" rx="18" fill="{accent}" fill-opacity="0.16"/>
  <rect x="540" y="212" width="118" height="48" rx="18" fill="{text}" fill-opacity="0.08"/>
  <rect x="540" y="272" width="118" height="48" rx="18" fill="{text}" fill-opacity="0.05"/>
  <rect x="426" y="332" width="82" height="12" rx="6" fill="{muted}" fill-opacity="0.22"/>
  <rect x="520" y="332" width="64" height="12" rx="6" fill="{accent}" fill-opacity="0.24"/>
  <rect x="596" y="332" width="62" height="12" rx="6" fill="{muted}" fill-opacity="0.14"/>
</svg>
"""
    if layout == "xai-mono":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="32" width="704" height="368" rx="28" fill="{panel}" stroke="#1f2228" stroke-opacity="0.12"/>
  <rect x="32" y="116" width="704" height="1" fill="#1f2228" fill-opacity="0.10"/>
  <text x="78" y="84" fill="{text}" font-family="Menlo, SFMono-Regular, Consolas, monospace" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <rect x="590" y="56" width="122" height="40" rx="12" fill="{text}"/>
  <text x="624" y="81" fill="#ffffff" font-family="Menlo, SFMono-Regular, Consolas, monospace" font-size="14" font-weight="700">START</text>
  <text x="78" y="186" fill="{text}" font-family="Menlo, SFMono-Regular, Consolas, monospace" font-size="86" font-weight="700" letter-spacing="-3">{headline}</text>
  <text x="80" y="224" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="80" y="260" width="156" height="40" rx="12" fill="{text}"/>
  <text x="114" y="286" fill="#ffffff" font-family="Menlo, SFMono-Regular, Consolas, monospace" font-size="15" font-weight="700">GET STARTED</text>
  <rect x="252" y="260" width="214" height="40" rx="12" fill="#ffffff" stroke="{text}" stroke-opacity="0.14"/>
  <text x="286" y="286" fill="{text}" font-family="Menlo, SFMono-Regular, Consolas, monospace" font-size="15" font-weight="700">VIEW DOCS</text>
  <rect x="80" y="332" width="104" height="22" rx="11" fill="{text}" fill-opacity="0.08"/>
  <rect x="196" y="332" width="104" height="22" rx="11" fill="{text}" fill-opacity="0.12"/>
  <rect x="486" y="156" width="192" height="176" rx="24" fill="#fcfcfc" stroke="{text}" stroke-opacity="0.08"/>
  <rect x="514" y="186" width="136" height="14" rx="7" fill="{text}" fill-opacity="0.10"/>
  <rect x="514" y="214" width="98" height="92" rx="18" fill="{text}" fill-opacity="0.12"/>
  <rect x="624" y="214" width="26" height="92" rx="13" fill="{text}" fill-opacity="0.06"/>
</svg>
"""
    if layout == "zapier-launchpad":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="32" width="704" height="368" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.10"/>
  <rect x="620" y="48" width="92" height="34" rx="17" fill="{accent}"/>
  <text x="646" y="70" fill="#ffffff" font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="800">{kicker}</text>
  <text x="384" y="138" text-anchor="middle" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="74" font-weight="900" letter-spacing="-3">{headline}</text>
  <text x="384" y="178" text-anchor="middle" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="226" y="212" width="126" height="40" rx="20" fill="#2a1917"/>
  <text x="258" y="238" fill="#ffffff" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">Get Started</text>
  <rect x="366" y="212" width="176" height="40" rx="20" fill="#ffffff" stroke="#2a1917" stroke-opacity="0.16"/>
  <text x="400" y="238" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">View Docs</text>
  <rect x="92" y="298" width="170" height="86" rx="22" fill="#2a1917"/>
  <rect x="286" y="298" width="170" height="86" rx="22" fill="#fff7ef" stroke="{accent}" stroke-opacity="0.20"/>
  <rect x="480" y="298" width="196" height="86" rx="22" fill="#fffaf4" stroke="#2a1917" stroke-opacity="0.08"/>
  <rect x="114" y="318" width="92" height="12" rx="6" fill="#ffffff" fill-opacity="0.16"/>
  <rect x="114" y="340" width="64" height="28" rx="14" fill="{accent}" fill-opacity="0.94"/>
  <rect x="308" y="320" width="108" height="12" rx="6" fill="{text}" fill-opacity="0.14"/>
  <rect x="308" y="344" width="80" height="12" rx="6" fill="{accent}" fill-opacity="0.24"/>
  <rect x="506" y="320" width="118" height="12" rx="6" fill="{text}" fill-opacity="0.12"/>
  <rect x="506" y="344" width="86" height="12" rx="6" fill="{muted}" fill-opacity="0.20"/>
</svg>
"""
    if layout in {"token-catalog-light", "token-catalog-dark", "token-catalog-warm"}:
        hero_bg = panel if layout != "token-catalog-dark" else lighten(bg, 0.04)
        canvas_bg = bg if layout != "token-catalog-dark" else "#111317"
        title_fill = text if layout != "token-catalog-dark" else "#f2f4f8"
        cta_fill = accent if layout != "token-catalog-dark" else lighten(accent, 0.08)
        secondary_bg = "#ffffff" if layout != "token-catalog-dark" else "#16181d"
        secondary_stroke = darken(text, 0.12) if layout != "token-catalog-dark" else "#2b2e36"
        primary_tile = accent if layout != "token-catalog-dark" else lighten(accent, 0.06)
        tile_2 = "#fffdf9" if layout == "token-catalog-warm" else "#ffffff"
        tile_3 = lighten(accent, 0.84) if layout != "token-catalog-dark" else "#1e2129"
        tile_4 = lighten(accent, 0.74) if layout != "token-catalog-dark" else "#2a2e39"
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{canvas_bg}"/>
  <rect x="28" y="28" width="712" height="376" rx="30" fill="{hero_bg}" stroke="{accent}" stroke-opacity="0.10"/>
  <rect x="48" y="48" width="108" height="24" rx="8" fill="#ffffff" fill-opacity="0.88"/>
  <text x="70" y="64" fill="{darken(text, 0.15) if layout != 'token-catalog-dark' else '#111111'}" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="800">Design Tokens</text>
  <rect x="166" y="48" width="126" height="24" rx="8" fill="#ffffff" fill-opacity="0.88"/>
  <text x="189" y="64" fill="{darken(text, 0.15) if layout != 'token-catalog-dark' else '#111111'}" font-family="Helvetica, Arial, sans-serif" font-size="12" font-weight="800">preview</text>
  <rect x="604" y="42" width="108" height="34" rx="12" fill="{cta_fill}"/>
  <text x="630" y="64" fill="#ffffff" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="800">{kicker}</text>
  <text x="384" y="154" text-anchor="middle" fill="{title_fill}" font-family="Helvetica, Arial, sans-serif" font-size="76" font-weight="900" letter-spacing="-3">{headline}</text>
  <text x="384" y="194" text-anchor="middle" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="224" y="220" width="138" height="42" rx="{button_rx}" fill="{cta_fill}"/>
  <text x="260" y="247" fill="#ffffff" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">Get Started</text>
  <rect x="376" y="220" width="176" height="42" rx="{button_rx}" fill="{secondary_bg}" stroke="{secondary_stroke}" stroke-opacity="0.16"/>
  <text x="414" y="247" fill="{title_fill}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">View Docs</text>
  <text x="80" y="312" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="700" letter-spacing="1">01 / COLORS</text>
  <text x="80" y="352" fill="{title_fill}" font-family="Helvetica, Arial, sans-serif" font-size="34" font-weight="800">Palette</text>
  <rect x="80" y="372" width="148" height="12" rx="6" fill="{muted}" fill-opacity="0.20"/>
  <rect x="80" y="388" width="144" height="0" fill="transparent"/>
  <rect x="314" y="298" width="114" height="86" rx="18" fill="{primary_tile}"/>
  <rect x="438" y="298" width="114" height="86" rx="18" fill="{tile_2}" stroke="{secondary_stroke}" stroke-opacity="0.10"/>
  <rect x="562" y="298" width="114" height="86" rx="18" fill="{tile_3}" stroke="{secondary_stroke}" stroke-opacity="0.10"/>
  <rect x="686" y="298" width="0" height="0" fill="transparent"/>
</svg>
"""
    if layout == "editorial-cascade":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="32" width="704" height="368" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.10"/>
  <rect x="54" y="54" width="202" height="324" rx="24" fill="{lighten(accent, 0.82)}" fill-opacity="0.20"/>
  <rect x="74" y="74" width="88" height="10" rx="5" fill="{accent}" fill-opacity="0.30"/>
  <rect x="74" y="98" width="66" height="10" rx="5" fill="{muted}" fill-opacity="0.20"/>
  <text x="286" y="94" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800" letter-spacing="2">{kicker}</text>
  <text x="286" y="176" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="68" font-weight="900" letter-spacing="-2">{headline}</text>
  <text x="286" y="216" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="286" y="254" width="184" height="14" rx="7" fill="{muted}" fill-opacity="0.16"/>
  <rect x="286" y="280" width="172" height="14" rx="7" fill="{muted}" fill-opacity="0.12"/>
  <rect x="286" y="320" width="154" height="42" rx="{button_rx}" fill="{accent}" fill-opacity="0.14"/>
  <text x="324" y="347" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">Explore</text>
  <rect x="544" y="66" width="154" height="112" rx="22" fill="#ffffff" fill-opacity="0.10"/>
  <rect x="544" y="194" width="154" height="168" rx="22" fill="#ffffff" fill-opacity="0.06"/>
</svg>
"""
    if layout == "dashboard-slab":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="28" y="28" width="712" height="376" rx="30" fill="{panel}" stroke="{accent}" stroke-opacity="0.10"/>
  <rect x="48" y="48" width="672" height="44" rx="16" fill="{accent}" fill-opacity="0.08"/>
  <text x="70" y="76" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800" letter-spacing="2">{kicker}</text>
  <text x="64" y="162" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="64" font-weight="900" letter-spacing="-2">{headline}</text>
  <text x="64" y="204" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="64" y="244" width="178" height="40" rx="{button_rx}" fill="{accent}" fill-opacity="0.18"/>
  <text x="104" y="270" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="800">Open Panel</text>
  <rect x="384" y="136" width="304" height="208" rx="24" fill="#ffffff" fill-opacity="0.06"/>
  <rect x="404" y="156" width="118" height="72" rx="18" fill="{accent}" fill-opacity="0.14"/>
  <rect x="536" y="156" width="132" height="28" rx="14" fill="#ffffff" fill-opacity="0.08"/>
  <rect x="536" y="196" width="132" height="32" rx="14" fill="#ffffff" fill-opacity="0.05"/>
  <rect x="404" y="244" width="264" height="80" rx="18" fill="#ffffff" fill-opacity="0.04"/>
</svg>
"""
    if layout == "luxury-banner":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="36" width="704" height="360" rx="28" fill="{panel}"/>
  <path d="M92 270C198 208 332 154 470 124C568 104 636 92 694 78V334H92V270Z" fill="{accent}" fill-opacity="0.14"/>
  <rect x="86" y="74" width="84" height="10" rx="5" fill="#ffffff" fill-opacity="0.12"/>
  <rect x="86" y="94" width="66" height="8" rx="4" fill="{muted}" fill-opacity="0.18"/>
  <text x="84" y="318" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="72" font-weight="800" letter-spacing="-1">{headline}</text>
  <text x="84" y="352" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="20" font-weight="600">{subhead}</text>
  <text x="534" y="82" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="2">{kicker}</text>
</svg>
"""
    if layout == "commerce-split":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="32" y="32" width="704" height="368" rx="28" fill="{bg}" stroke="{accent}" stroke-opacity="0.08"/>
  <rect x="52" y="52" width="356" height="328" rx="24" fill="{panel}"/>
  <path d="M72 322C150 248 220 198 388 138V360H72V322Z" fill="{accent}" fill-opacity="0.16"/>
  <rect x="432" y="70" width="264" height="18" rx="9" fill="{accent}" fill-opacity="0.12"/>
  <text x="432" y="160" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="62" font-weight="800" letter-spacing="-2">{headline}</text>
  <text x="432" y="202" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="432" y="238" width="180" height="14" rx="7" fill="{muted}" fill-opacity="0.18"/>
  <rect x="432" y="264" width="204" height="14" rx="7" fill="{muted}" fill-opacity="0.13"/>
  <rect x="432" y="314" width="122" height="40" rx="{button_rx}" fill="{accent}" fill-opacity="0.18"/>
  <text x="464" y="340" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700">Explore</text>
  <text x="432" y="114" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
</svg>
"""
    if layout == "editorial":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="34" y="34" width="700" height="364" rx="28" fill="{panel}"/>
  <rect x="58" y="58" width="192" height="316" rx="22" fill="{soft}" fill-opacity="0.16"/>
  <rect x="280" y="64" width="28" height="286" rx="14" fill="{accent}" fill-opacity="0.08"/>
  <text x="334" y="94" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="334" y="176" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="70" font-weight="800" letter-spacing="-2">{headline}</text>
  <rect x="336" y="204" width="256" height="12" rx="6" fill="{muted}" fill-opacity="0.22"/>
  <rect x="336" y="226" width="238" height="12" rx="6" fill="{muted}" fill-opacity="0.18"/>
  <rect x="336" y="256" width="144" height="42" rx="{button_rx}" fill="#ffffff" fill-opacity="0.06"/>
  <text x="366" y="283" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="17" font-weight="700">Read More</text>
  <text x="334" y="332" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
</svg>
"""
    if layout == "ai-capsule":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <circle cx="154" cy="112" r="112" fill="{accent}" fill-opacity="0.08"/>
  <circle cx="644" cy="344" r="98" fill="{soft2}" fill-opacity="0.10"/>
  <rect x="72" y="62" width="624" height="308" rx="34" fill="{panel}" stroke="{accent}" stroke-opacity="0.16"/>
  <text x="104" y="104" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="104" y="178" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="68" font-weight="800" letter-spacing="-2">{headline}</text>
  <text x="104" y="220" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="104" y="274" width="244" height="52" rx="26" fill="{accent}" fill-opacity="0.12"/>
  <circle cx="468" cy="206" r="62" fill="{accent}" fill-opacity="0.24"/>
  <rect x="546" y="154" width="108" height="14" rx="7" fill="{text}" fill-opacity="0.16"/>
  <rect x="546" y="182" width="92" height="14" rx="7" fill="{muted}" fill-opacity="0.20"/>
  <rect x="546" y="210" width="84" height="14" rx="7" fill="{muted}" fill-opacity="0.16"/>
</svg>
"""
    if layout == "editor-workbench":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="28" y="28" width="712" height="376" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.16"/>
  <rect x="48" y="48" width="88" height="336" rx="20" fill="#ffffff" fill-opacity="0.04"/>
  <rect x="152" y="48" width="366" height="336" rx="20" fill="{bg}" fill-opacity="0.42"/>
  <rect x="170" y="70" width="330" height="20" rx="10" fill="#ffffff" fill-opacity="0.05"/>
  <rect x="170" y="114" width="214" height="14" rx="7" fill="{accent}" fill-opacity="0.20"/>
  <rect x="170" y="142" width="188" height="10" rx="5" fill="{muted}" fill-opacity="0.20"/>
  <rect x="170" y="162" width="164" height="10" rx="5" fill="{muted}" fill-opacity="0.16"/>
  <rect x="540" y="48" width="180" height="148" rx="20" fill="#ffffff" fill-opacity="0.05"/>
  <text x="540" y="238" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="540" y="298" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="48" font-weight="800" letter-spacing="-1">{headline}</text>
  <text x="540" y="328" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="500">{subhead}</text>
</svg>
"""
    if layout == "docs-grid":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="34" y="34" width="700" height="364" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.10"/>
  <text x="62" y="90" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="62" y="150" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="56" font-weight="800" letter-spacing="-1">{headline}</text>
  <rect x="62" y="184" width="198" height="12" rx="6" fill="{muted}" fill-opacity="0.22"/>
  <rect x="62" y="226" width="174" height="136" rx="20" fill="#ffffff" fill-opacity="0.88"/>
  <rect x="248" y="226" width="174" height="136" rx="20" fill="{soft}" fill-opacity="0.28"/>
  <rect x="434" y="226" width="114" height="136" rx="20" fill="#ffffff" fill-opacity="0.70"/>
  <rect x="560" y="226" width="114" height="136" rx="20" fill="#ffffff" fill-opacity="0.48"/>
</svg>
"""
    if layout == "creative":
        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="34" y="34" width="700" height="364" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.18"/>
  <circle cx="188" cy="148" r="76" fill="{accent}" fill-opacity="0.92"/>
  <circle cx="258" cy="148" r="58" fill="{soft2}"/>
  <circle cx="160" cy="228" r="44" fill="{dark}"/>
  <circle cx="236" cy="236" r="54" fill="{soft}"/>
  <text x="410" y="102" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="410" y="176" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="62" font-weight="800" letter-spacing="-2">{headline}</text>
  <text x="410" y="216" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="500">{subhead}</text>
  <rect x="410" y="260" width="180" height="14" rx="7" fill="{muted}" fill-opacity="0.18"/>
  <rect x="410" y="286" width="144" height="14" rx="7" fill="{accent}" fill-opacity="0.16"/>
</svg>
"""
    art = []
    if layout == "hero-light":
        art.extend(
            [
                f'<rect x="452" y="28" width="288" height="196" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.15"/>',
                f'<rect x="476" y="54" width="240" height="110" rx="22" fill="{accent}" fill-opacity="0.10"/>',
                f'<rect x="492" y="72" width="98" height="14" rx="7" fill="{soft}" fill-opacity="0.42"/>',
                f'<rect x="476" y="178" width="122" height="12" rx="6" fill="{muted}" fill-opacity="0.28"/>',
                f'<rect x="608" y="178" width="72" height="12" rx="6" fill="{accent}" fill-opacity="0.28"/>',
            ]
        )
    elif layout == "product-stack":
        art.extend(
            [
                f'<rect x="444" y="34" width="294" height="186" rx="30" fill="{panel}" stroke="{accent}" stroke-opacity="0.18"/>',
                f'<rect x="468" y="56" width="112" height="142" rx="24" fill="{accent}" fill-opacity="0.14"/>',
                f'<rect x="596" y="56" width="118" height="52" rx="18" fill="{soft}" fill-opacity="0.28"/>',
                f'<rect x="596" y="122" width="118" height="32" rx="16" fill="{muted}" fill-opacity="0.18"/>',
                f'<rect x="596" y="166" width="82" height="32" rx="16" fill="{accent}" fill-opacity="0.18"/>',
                f'<rect x="686" y="166" width="28" height="32" rx="14" fill="#ffffff" fill-opacity="0.08"/>',
            ]
        )
    elif layout == "poster":
        art.extend(
            [
                f'<rect x="452" y="28" width="288" height="196" rx="28" fill="{panel}"/>',
                f'<rect x="476" y="52" width="240" height="86" rx="18" fill="{soft}" fill-opacity="0.12"/>',
                f'<rect x="476" y="150" width="160" height="46" rx="16" fill="#ffffff" fill-opacity="0.05"/>',
                f'<rect x="650" y="150" width="66" height="46" rx="16" fill="{accent}" fill-opacity="0.12"/>',
            ]
        )
    elif layout == "dashboard":
        art.extend(
            [
                f'<rect x="452" y="28" width="288" height="196" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.24"/>',
                f'<rect x="470" y="48" width="74" height="156" rx="18" fill="{accent}" fill-opacity="0.10"/>',
                f'<rect x="558" y="48" width="164" height="48" rx="16" fill="{accent}" fill-opacity="0.14"/>',
                f'<rect x="558" y="106" width="164" height="48" rx="16" fill="#ffffff" fill-opacity="0.06"/>',
                f'<rect x="558" y="164" width="76" height="40" rx="14" fill="#ffffff" fill-opacity="0.05"/>',
                f'<rect x="646" y="164" width="76" height="40" rx="14" fill="{accent}" fill-opacity="0.18"/>',
            ]
        )
    elif layout == "editor-workbench":
        art.extend(
            [
                f'<rect x="444" y="28" width="296" height="198" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.2"/>',
                f'<rect x="462" y="46" width="262" height="22" rx="11" fill="#ffffff" fill-opacity="0.05"/>',
                f'<rect x="462" y="82" width="78" height="126" rx="18" fill="#ffffff" fill-opacity="0.04"/>',
                f'<rect x="552" y="82" width="154" height="18" rx="9" fill="{accent}" fill-opacity="0.18"/>',
                f'<rect x="552" y="112" width="136" height="10" rx="5" fill="{muted}" fill-opacity="0.22"/>',
                f'<rect x="552" y="132" width="124" height="10" rx="5" fill="{muted}" fill-opacity="0.18"/>',
                f'<rect x="552" y="162" width="154" height="46" rx="16" fill="#ffffff" fill-opacity="0.06"/>',
            ]
        )
    elif layout == "docs-grid":
        art.extend(
            [
                f'<rect x="446" y="30" width="292" height="194" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.12"/>',
                f'<rect x="466" y="52" width="252" height="28" rx="14" fill="{accent}" fill-opacity="0.10"/>',
                f'<rect x="466" y="94" width="76" height="112" rx="18" fill="#ffffff" fill-opacity="0.85"/>',
                f'<rect x="554" y="94" width="76" height="112" rx="18" fill="{soft}" fill-opacity="0.28"/>',
                f'<rect x="642" y="94" width="76" height="112" rx="18" fill="#ffffff" fill-opacity="0.65"/>',
            ]
        )
    elif layout == "creative":
        art.extend(
            [
                f'<rect x="452" y="28" width="288" height="196" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.22"/>',
                f'<circle cx="520" cy="82" r="28" fill="{accent}"/>',
                f'<circle cx="570" cy="82" r="28" fill="{lighten(accent, 0.18)}"/>',
                f'<circle cx="520" cy="132" r="28" fill="{darken(accent, 0.08)}"/>',
                f'<circle cx="570" cy="132" r="28" fill="{lighten(accent, 0.34)}"/>',
                f'<circle cx="545" cy="182" r="28" fill="{lighten(accent, 0.48)}"/>',
                f'<rect x="622" y="60" width="86" height="18" rx="9" fill="{muted}" fill-opacity="0.35"/>',
                f'<rect x="622" y="92" width="72" height="12" rx="6" fill="{accent}" fill-opacity="0.28"/>',
                f'<rect x="622" y="122" width="88" height="12" rx="6" fill="{muted}" fill-opacity="0.25"/>',
                f'<rect x="622" y="152" width="66" height="12" rx="6" fill="{muted}" fill-opacity="0.25"/>',
            ]
        )
    elif layout == "editorial":
        art.extend(
            [
                f'<rect x="450" y="26" width="290" height="200" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.14"/>',
                f'<rect x="470" y="46" width="130" height="160" rx="22" fill="{soft}" fill-opacity="0.18"/>',
                f'<rect x="616" y="48" width="104" height="12" rx="6" fill="{accent}" fill-opacity="0.34"/>',
                f'<rect x="616" y="72" width="92" height="12" rx="6" fill="{text}" fill-opacity="0.24"/>',
                f'<rect x="616" y="102" width="94" height="10" rx="5" fill="{muted}" fill-opacity="0.22"/>',
                f'<rect x="616" y="122" width="80" height="10" rx="5" fill="{muted}" fill-opacity="0.18"/>',
                f'<rect x="616" y="154" width="94" height="36" rx="18" fill="#ffffff" fill-opacity="0.06"/>',
            ]
        )
    elif layout == "commerce-split":
        art.extend(
            [
                f'<rect x="446" y="28" width="292" height="196" rx="28" fill="{panel}"/>',
                f'<path d="M466 188C510 132 556 86 716 48V188H466Z" fill="{accent}" fill-opacity="0.16"/>',
                f'<rect x="468" y="48" width="168" height="120" rx="24" fill="#ffffff" fill-opacity="0.06"/>',
                f'<rect x="650" y="58" width="66" height="66" rx="20" fill="{soft}" fill-opacity="0.30"/>',
                f'<rect x="650" y="138" width="66" height="54" rx="18" fill="#ffffff" fill-opacity="0.08"/>',
            ]
        )
    elif layout == "luxury-banner":
        art.extend(
            [
                f'<rect x="446" y="28" width="292" height="196" rx="28" fill="{panel}"/>',
                f'<rect x="462" y="46" width="260" height="160" rx="24" fill="{soft}" fill-opacity="0.08"/>',
                f'<path d="M482 170C540 114 616 76 710 64V192H482Z" fill="{accent}" fill-opacity="0.14"/>',
                f'<rect x="482" y="64" width="88" height="12" rx="6" fill="#ffffff" fill-opacity="0.14"/>',
                f'<rect x="482" y="88" width="66" height="10" rx="5" fill="{muted}" fill-opacity="0.18"/>',
            ]
        )
    elif layout == "ai-capsule":
        art.extend(
            [
                f'<rect x="446" y="28" width="292" height="196" rx="28" fill="{panel}" stroke="{accent}" stroke-opacity="0.2"/>',
                f'<rect x="468" y="50" width="248" height="36" rx="18" fill="{accent}" fill-opacity="0.10"/>',
                f'<rect x="468" y="100" width="248" height="92" rx="28" fill="{soft}" fill-opacity="0.18"/>',
                f'<circle cx="518" cy="146" r="24" fill="{accent}" fill-opacity="0.32"/>',
                f'<rect x="556" y="124" width="116" height="12" rx="6" fill="{text}" fill-opacity="0.18"/>',
                f'<rect x="556" y="148" width="92" height="12" rx="6" fill="{muted}" fill-opacity="0.24"/>',
            ]
        )

    shapes = "\n  ".join(art)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="768" height="432" viewBox="0 0 768 432" fill="none">
  <rect width="768" height="432" rx="36" fill="{bg}"/>
  <rect x="28" y="28" width="712" height="376" rx="30" fill="{bg}" stroke="{accent}" stroke-opacity="0.08"/>
  <text x="52" y="74" fill="{accent}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="2">{kicker}</text>
  <text x="52" y="156" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="64" font-weight="800">{headline}</text>
  <text x="52" y="204" fill="{muted}" font-family="Helvetica, Arial, sans-serif" font-size="24" font-weight="500">{subhead}</text>
  <rect x="52" y="248" width="188" height="18" rx="9" fill="{muted}" fill-opacity="0.20"/>
  <rect x="52" y="282" width="236" height="18" rx="9" fill="{muted}" fill-opacity="0.16"/>
  <rect x="52" y="330" width="124" height="40" rx="{button_rx}" fill="{accent}" fill-opacity="0.18"/>
  <text x="84" y="356" fill="{text}" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700">Preview</text>
  {shapes}
</svg>
"""


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    catalog = json.loads((skill_dir / "references" / "style-catalog.json").read_text(encoding="utf-8"))
    out_dir = skill_dir / "assets" / "thumbnails"
    out_dir.mkdir(parents=True, exist_ok=True)

    manifest = []
    for entry in catalog:
        style = style_for_entry(entry)
        output_path = out_dir / f"{entry['slug']}.svg"
        output_path.write_text(svg_for(style), encoding="utf-8")
        manifest.append(
            {
                "name": entry["name"],
                "slug": entry["slug"],
                "path": str(output_path),
                "preview_url": entry["preview_url"],
                "layout": style["layout"],
                "layout_label": LAYOUT_LABELS.get(style["layout"], style["layout"].title()),
                "style": style,
                "audit_status": "needs_audit",
                "audit_score": 0.0,
                "audit_version": AUDIT_VERSION,
                "official_fingerprint_version": entry.get("official_fingerprint_version", AUDIT_VERSION),
                "audit_failures": [],
            }
        )

    manifest.sort(key=lambda item: item["name"].lower())
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(manifest)} thumbnail cards in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

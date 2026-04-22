#!/usr/bin/env python3
"""Audit local SVG thumbnails against official preview fingerprints."""

from __future__ import annotations

import json
import re
import ssl
import sys
from copy import deepcopy
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

import generate_thumbnail_cards as generator

AUDIT_VERSION = "2026-04-v2"
OFFICIAL_FINGERPRINT_VERSION = "2026-04-v1"
MAX_REPAIR_PASSES = 3
FINGERPRINT_FORCE_REFRESH = {"BMW", "Claude", "Figma"}

HIGH_FREQUENCY_PROFILES = {
    "Apple": {
        "expected_layout": "hero-light",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "blue",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"minimal", "premium", "product"},
        "forbidden_layouts": {"dashboard", "docs-grid", "editor-workbench"},
        "colors": {"background": "#F5F5F7", "panel": "#FFFFFF", "text": "#1D1D1F", "accent": "#0071E3"},
    },
    "Nike": {
        "expected_layout": "poster",
        "brightness": "dark",
        "monochrome": True,
        "accent_family": "neutral",
        "force_uppercase": True,
        "button_radius": "soft",
        "moods": {"bold", "heroic", "conversion"},
        "forbidden_layouts": {"dashboard", "docs-grid", "editor-workbench"},
    },
    "Linear": {
        "expected_layout": "dashboard",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "purple",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"precise", "tooling", "developer"},
        "forbidden_layouts": {"poster", "commerce-split", "luxury-banner"},
    },
    "Stripe": {
        "expected_layout": "hero-light",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "purple",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"gradient", "developer-brand", "elegant"},
        "forbidden_layouts": {"dashboard", "editor-workbench"},
    },
    "Vercel": {
        "expected_layout": "hero-light",
        "brightness": "light",
        "monochrome": True,
        "accent_family": "neutral",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"minimal", "precise", "developer"},
        "forbidden_layouts": {"poster", "commerce-split"},
    },
    "Supabase": {
        "expected_layout": "dashboard",
        "brightness": "dark",
        "monochrome": False,
        "accent_family": "green",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"tooling", "developer", "code-first"},
        "forbidden_layouts": {"poster", "luxury-banner"},
    },
    "Figma": {
        "expected_layout": "creative",
        "brightness": "dark",
        "monochrome": False,
        "accent_family": "green",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"creative", "expressive", "product"},
        "forbidden_layouts": {"docs-grid", "luxury-banner"},
    },
    "Cursor": {
        "expected_layout": "dashboard",
        "brightness": "dark",
        "monochrome": False,
        "accent_family": "blue",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"tooling", "developer", "future-facing"},
        "forbidden_layouts": {"poster", "luxury-banner"},
    },
    "Claude": {
        "expected_layout": "editorial",
        "brightness": "dark",
        "monochrome": False,
        "accent_family": "orange",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"editorial", "friendly", "future-facing"},
        "forbidden_layouts": {"dashboard", "poster"},
    },
    "Airbnb": {
        "expected_layout": "commerce-split",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "red",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"friendly", "conversion", "product"},
        "forbidden_layouts": {"dashboard", "docs-grid"},
    },
    "BMW": {
        "expected_layout": "luxury-banner",
        "brightness": "light",
        "monochrome": True,
        "accent_family": "neutral",
        "force_uppercase": True,
        "button_radius": "soft",
        "moods": {"luxury", "cinematic", "monumental"},
        "forbidden_layouts": {"dashboard", "docs-grid", "editor-workbench"},
    },
    "WIRED": {
        "expected_layout": "editorial",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "red",
        "force_uppercase": True,
        "button_radius": "sharp",
        "moods": {"editorial", "brand", "narrative"},
        "forbidden_layouts": {"dashboard", "luxury-banner"},
        "colors": {"background": "#F7F7F2", "panel": "#FFFFFF", "text": "#111111", "accent": "#FF3B30"},
    },
    "Sentry": {
        "expected_layout": "sentry-docs",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "purple",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"brand", "dense", "developer", "structured", "technical"},
        "forbidden_layouts": {"poster", "commerce-split", "luxury-banner"},
        "colors": {"background": "#FFFFFF", "panel": "#F1EEF9", "text": "#1F1633", "accent": "#6C5CE7"},
    },
    "xAI": {
        "expected_layout": "xai-mono",
        "brightness": "light",
        "monochrome": True,
        "accent_family": "neutral",
        "force_uppercase": False,
        "button_radius": "soft",
        "moods": {"developer", "future-facing", "minimal", "technical"},
        "forbidden_layouts": {"dashboard", "poster", "luxury-banner"},
        "colors": {"background": "#F8F8F8", "panel": "#FFFFFF", "text": "#1F2228", "accent": "#1F2228"},
    },
    "Zapier": {
        "expected_layout": "zapier-launchpad",
        "brightness": "light",
        "monochrome": False,
        "accent_family": "orange",
        "force_uppercase": False,
        "button_radius": "pill",
        "moods": {"brand", "efficient", "friendly", "product"},
        "forbidden_layouts": {"dashboard", "editor-workbench", "luxury-banner"},
        "colors": {"background": "#FFFDF9", "panel": "#FFFEFB", "text": "#2A1917", "accent": "#FF5A1F"},
    },
}

COLOR_BY_FAMILY = {
    "neutral": "#111111",
    "blue": "#3b82f6",
    "green": "#22c55e",
    "purple": "#7c6cff",
    "red": "#ef4444",
    "orange": "#c9735b",
    "yellow": "#facc15",
}

TOOLING_LAYOUTS = {
    "dashboard",
    "docs-grid",
    "editor-workbench",
    "sentry-docs",
    "xai-mono",
    "zapier-launchpad",
    "token-catalog-light",
    "token-catalog-dark",
    "token-catalog-warm",
    "dashboard-slab",
}
SHOWCASE_LAYOUTS = {"poster", "commerce-split", "luxury-banner", "hero-light"}
EDITORIAL_LAYOUTS = {"editorial", "creative", "ai-capsule", "product-stack", "editorial-cascade"}
LAYOUT_EQUIVALENTS = {
    "docs-grid": {"docs-grid", "sentry-docs", "xai-mono", "zapier-launchpad", "token-catalog-light", "token-catalog-dark", "token-catalog-warm"},
    "dashboard": {"dashboard", "dashboard-slab", "editor-workbench"},
    "editorial": {"editorial", "editorial-cascade"},
}
NEUTRAL_FAMILIES = {"neutral", "unknown"}


def fetch_url(url: str) -> str:
    req = Request(url, headers={"User-Agent": "style-compass-audit/1.0"})
    try:
        with urlopen(req, timeout=25) as response:
            return response.read().decode("utf-8", errors="ignore")
    except (ssl.SSLCertVerificationError, URLError) as exc:
        reason = getattr(exc, "reason", exc)
        if not isinstance(reason, ssl.SSLCertVerificationError) and "CERTIFICATE_VERIFY_FAILED" not in str(reason):
            raise
        insecure = ssl._create_unverified_context()
        with urlopen(req, timeout=25, context=insecure) as response:
            print("[WARN] SSL verification failed; retried preview fetch with insecure context.", file=sys.stderr)
            return response.read().decode("utf-8", errors="ignore")


def strip_html(html: str) -> str:
    cleaned = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.IGNORECASE)
    cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", "\n", cleaned)
    cleaned = unescape(cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    return cleaned


def extract_hexes(source: str) -> list[str]:
    colors = []
    for match in re.findall(r"#[0-9a-fA-F]{6}", source):
        upper = match.upper()
        if upper not in colors:
            colors.append(upper)
    return colors


def is_neutral(hex_color: str) -> bool:
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return False
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    return max(abs(r - g), abs(g - b), abs(r - b)) <= 16


def brightness_from_hex(hex_color: str) -> str:
    value = hex_color.lstrip("#")
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    if luminance >= 0.8:
        return "light"
    if luminance <= 0.28:
        return "dark"
    return "mixed"


def color_family(hex_color: str) -> str:
    value = hex_color.lstrip("#")
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    if is_neutral(hex_color):
        return "neutral"
    if r >= g and r >= b:
        if g > 145 and b < 120:
            return "yellow"
        if g > 80:
            return "orange"
        return "red"
    if g >= r and g >= b:
        return "green"
    if b >= r and b >= g:
        if r > 80 and b > 140:
            return "purple"
        return "blue"
    return "unknown"


def accent_mode(accent_color: str) -> str:
    return "monochrome" if color_family(accent_color) in NEUTRAL_FAMILIES else "color"


def button_radius_label(radius: int) -> str:
    if radius >= 18:
        return "pill"
    if radius >= 10:
        return "soft"
    return "sharp"


def classify_layout(layout: str) -> str:
    if layout in TOOLING_LAYOUTS:
        return "tooling"
    if layout in SHOWCASE_LAYOUTS:
        return "showcase"
    if layout in EDITORIAL_LAYOUTS:
        return "editorial"
    return layout


def infer_layout_from_text(text: str, entry: dict) -> str:
    lower = text.lower()
    if any(token in lower for token in ("poster", "campaign", "product hero", "hero image", "impactful hero")):
        return "poster"
    if any(token in lower for token in ("dashboard", "data-dense", "console", "developer ui")):
        return "dashboard"
    if any(token in lower for token in ("editorial", "magazine", "story", "content-led")):
        return "editorial"
    if any(token in lower for token in ("docs", "documentation", "reading layout")):
        return "docs-grid"
    if any(token in lower for token in ("commerce", "conversion", "shopping", "retail")):
        return "commerce-split"
    if any(token in lower for token in ("luxury", "automotive", "cinematic", "monumental")):
        return "luxury-banner"
    if any(token in lower for token in ("ai platform", "future-facing", "intelligence", "ml platform")):
        return "ai-capsule"
    if any(token in lower for token in ("creative tool", "playful", "expressive")):
        return "creative"
    if any(token in lower for token in ("workbench", "editor", "workspace")):
        return "editor-workbench"
    if entry.get("layout_density") == "high":
        return "dashboard"
    return generator.choose_layout(entry)


def infer_moods_from_text(text: str, entry: dict) -> list[str]:
    lower = text.lower()
    moods = set(entry.get("mood_keywords", []))
    text_map = {
        "minimal": ("minimal", "restrained", "clean white", "clean white canvas"),
        "premium": ("premium", "luxury", "refined"),
        "cinematic": ("cinematic", "movie", "campaign"),
        "tooling": ("tooling", "dashboard", "developer ui", "console"),
        "developer": ("developer", "engineering", "technical"),
        "creative": ("creative", "playful", "expressive"),
        "editorial": ("editorial", "magazine", "story"),
        "conversion": ("conversion", "retail", "commerce"),
        "brand": ("brand", "campaign", "marketing"),
        "friendly": ("friendly", "warm", "hospitality"),
    }
    for mood, needles in text_map.items():
        if any(needle in lower for needle in needles):
            moods.add(mood)
    return sorted(moods)


def parse_button_radius_from_text(text: str) -> str:
    lower = text.lower()
    if any(token in lower for token in ("pill", "full rounded", "capsule")):
        return "pill"
    if any(token in lower for token in ("sharp corners", "square")):
        return "sharp"
    return "soft"


def extract_official_colors(text: str, html: str, fallback: dict[str, str]) -> dict[str, str]:
    context_pairs = {
        "background": r"(?:Background|Canvas|Page Background|Base Background)[^#\n]*(#[0-9a-fA-F]{6})",
        "panel": r"(?:Surface|Card Background|Panel Background)[^#\n]*(#[0-9a-fA-F]{6})",
        "text": r"(?:Primary Text|Text Color|Text)[^#\n]*(#[0-9a-fA-F]{6})",
        "accent": r"(?:Accent|Primary CTA|Primary Action|Button Color|Link Color)[^#\n]*(#[0-9a-fA-F]{6})",
    }
    resolved = {}
    for key, pattern in context_pairs.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            resolved[key] = match.group(1).upper()
    colors = extract_hexes(html)
    neutrals = [color for color in colors if is_neutral(color)]
    chromas = [color for color in colors if not is_neutral(color)]
    resolved.setdefault("background", neutrals[0] if neutrals else fallback["bg"].upper())
    resolved.setdefault("panel", neutrals[1] if len(neutrals) > 1 else fallback["panel"].upper())
    resolved.setdefault("text", neutrals[-1] if neutrals else fallback["text"].upper())
    resolved.setdefault("accent", chromas[0] if chromas else fallback["accent"].upper())
    return resolved


def official_fingerprint(entry: dict) -> dict[str, Any]:
    fallback_style = generator.style_for_entry(entry)
    profile = HIGH_FREQUENCY_PROFILES.get(entry["name"], {})
    try:
        html = fetch_url(entry["preview_url"])
        text = strip_html(html)
    except Exception as exc:  # pragma: no cover - network fallback
        html = ""
        text = entry["summary"]
        print(f"[WARN] Failed to fetch preview for {entry['name']}: {exc}", file=sys.stderr)

    colors = extract_official_colors(text, html, fallback_style)
    colors.update({key: value.upper() for key, value in profile.get("colors", {}).items()})
    lower = text.lower()
    uppercase = entry["name"].isupper()
    mono_flag = ("monochrome" in lower or "black and white" in lower or "black-white" in lower or "single-color" in lower)
    accent_family_name = color_family(colors["accent"])
    if profile.get("monochrome") is True:
        mono_flag = True
    elif profile.get("monochrome") is False:
        mono_flag = False
    if mono_flag:
        accent_family_name = "neutral"
    return {
        "version": OFFICIAL_FINGERPRINT_VERSION,
        "name": entry["name"],
        "preview_url": entry["preview_url"],
        "colors": colors,
        "brightness": profile.get("brightness") or brightness_from_hex(colors["background"]),
        "accent_family": profile.get("accent_family") or accent_family_name,
        "accent_mode": "monochrome" if mono_flag or accent_family_name == "neutral" else "color",
        "layout_hint": profile.get("expected_layout") or infer_layout_from_text(text, entry),
        "button_radius": profile.get("button_radius") or parse_button_radius_from_text(text),
        "uppercase_title": profile.get("force_uppercase", uppercase),
        "moods": sorted(profile.get("moods", set()) or infer_moods_from_text(text, entry)),
        "excerpt": text[:520].strip(),
    }


def load_cached_fingerprints(references_dir: Path) -> dict[str, dict[str, Any]]:
    baseline_path = references_dir / "style-audit-baseline.json"
    if not baseline_path.exists():
        return {}
    try:
        rows = json.loads(baseline_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    cached: dict[str, dict[str, Any]] = {}
    for row in rows:
        fingerprint = row.get("fingerprint") or {}
        if fingerprint.get("version") != OFFICIAL_FINGERPRINT_VERSION:
            continue
        slug = row.get("slug")
        if not slug:
            continue
        cached[slug] = row
    return cached


def official_fingerprint_with_cache(entry: dict, cached_rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if entry["name"] in FINGERPRINT_FORCE_REFRESH:
        return official_fingerprint(entry)
    cached = cached_rows.get(entry["slug"])
    if cached:
        fingerprint = deepcopy(cached.get("fingerprint") or {})
        if fingerprint:
            fingerprint["name"] = entry["name"]
            fingerprint["preview_url"] = entry["preview_url"]
            fingerprint["version"] = OFFICIAL_FINGERPRINT_VERSION
            return fingerprint
    return official_fingerprint(entry)


def svg_fingerprint(manifest_item: dict) -> dict[str, Any]:
    style = manifest_item.get("style", {})
    svg_text = Path(manifest_item["path"]).read_text(encoding="utf-8")
    fills = extract_hexes(svg_text)
    colors = {
        "background": style.get("bg", fills[0] if fills else "#111111").upper(),
        "panel": style.get("panel", fills[1] if len(fills) > 1 else "#1A1A1A").upper(),
        "text": style.get("text", style.get("accent", "#F5F5F5")).upper(),
        "accent": style.get("accent", next((color for color in fills if not is_neutral(color)), fills[0] if fills else "#FFFFFF")).upper(),
    }
    headline = str(style.get("headline") or manifest_item["name"]).strip()
    button_radius = str(style.get("button_radius") or "soft")
    moods = set(style.get("mood_keywords", []))
    style_text = " ".join(str(style.get(key, "")) for key in ("kicker", "subhead", "layout"))
    lower = style_text.lower()
    for token in ("minimal", "premium", "cinematic", "tooling", "developer", "creative", "editorial", "conversion", "brand"):
        if token in lower:
            moods.add(token)
    return {
        "layout": manifest_item["layout"],
        "layout_group": classify_layout(manifest_item["layout"]),
        "colors": colors,
        "brightness": brightness_from_hex(colors["background"]),
        "accent_family": color_family(colors["accent"]),
        "accent_mode": accent_mode(colors["accent"]),
        "headline": headline,
        "uppercase_title": headline.isupper(),
        "headline_size": 0,
        "button_radius": button_radius,
        "moods": sorted(moods),
    }


def overlap_score(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def layout_matches(expected_layout: str, actual_layout: str) -> bool:
    if actual_layout == expected_layout:
        return True
    return actual_layout in LAYOUT_EQUIVALENTS.get(expected_layout, set())


def fallback_layout(expected_layout: str, official: dict[str, Any], entry: dict) -> str:
    accent_family = official["accent_family"]
    brightness = official["brightness"]
    if expected_layout == "docs-grid":
        if accent_family == "orange":
            return "token-catalog-warm"
        if brightness == "dark":
            return "token-catalog-dark"
        return "token-catalog-light"
    if expected_layout == "editorial":
        return "editorial-cascade"
    if expected_layout == "dashboard" and brightness == "light":
        return "dashboard-slab"
    if expected_layout == "dashboard" and "developer-tool" in entry.get("best_for", []):
        return "dashboard-slab"
    return expected_layout


def repair_style(entry: dict, manifest_item: dict, official: dict[str, Any], pass_index: int) -> dict[str, Any]:
    style = deepcopy(manifest_item.get("style") or generator.style_for_entry(entry))
    profile = HIGH_FREQUENCY_PROFILES.get(entry["name"], {})
    expected_layout = profile.get("expected_layout") or official["layout_hint"]
    style["layout"] = expected_layout if pass_index == 1 else fallback_layout(expected_layout, official, entry)

    colors = dict(official["colors"])
    colors.update({key: value.upper() for key, value in profile.get("colors", {}).items()})
    style["bg"] = colors["background"]
    style["panel"] = colors["panel"]
    style["text"] = colors["text"]

    if official["accent_mode"] == "monochrome":
        style["accent"] = "#111111" if official["brightness"] != "dark" else "#F5F5F5"
    else:
        family = profile.get("accent_family") or official["accent_family"]
        style["accent"] = colors["accent"] if family == official["accent_family"] else COLOR_BY_FAMILY.get(family, colors["accent"])

    if profile.get("force_uppercase"):
        style["headline"] = entry["name"].upper()
    else:
        style["headline"] = entry["name"]
    style["button_radius"] = profile.get("button_radius") or official["button_radius"]

    subhead = style.get("subhead") or generator.subhead_for(entry)
    if len(subhead) > 26:
        subhead = subhead[:26] + "…"
    style["subhead"] = subhead
    style["kicker"] = style.get("kicker") or generator.choose_kicker(entry)
    style["mood_keywords"] = list(dict.fromkeys(profile.get("moods", set()) or entry.get("mood_keywords", [])))
    style["best_for"] = list(entry.get("best_for", []))
    if pass_index >= 2 and official["accent_mode"] == "monochrome":
        style["muted"] = "#6f737b" if official["brightness"] == "light" else "#9ca3af"
    if pass_index >= 2 and official["accent_family"] == "orange":
        style["accent"] = "#FF5A1F"
        style["text"] = colors["text"]
    if pass_index >= 3 and expected_layout == "dashboard":
        style["layout"] = "dashboard-slab"
    return style


def compare_fingerprints(entry: dict, official: dict[str, Any], svg: dict[str, Any]) -> dict[str, Any]:
    profile = HIGH_FREQUENCY_PROFILES.get(entry["name"], {})
    failures: list[str] = []
    breakdown: dict[str, float] = {}

    expected_layout = profile.get("expected_layout") or official["layout_hint"]
    if layout_matches(expected_layout, svg["layout"]):
        breakdown["layout"] = 30
    elif classify_layout(svg["layout"]) == classify_layout(expected_layout):
        breakdown["layout"] = 18
    else:
        breakdown["layout"] = 0
        failures.append(f"布局不匹配：官方偏 {expected_layout}，本地是 {svg['layout']}")

    if svg["brightness"] == (profile.get("brightness") or official["brightness"]):
        breakdown["brightness"] = 15
    else:
        breakdown["brightness"] = 4
        failures.append(f"明暗倾向不匹配：官方偏 {profile.get('brightness') or official['brightness']}，本地是 {svg['brightness']}")

    expected_accent_family = profile.get("accent_family") or official["accent_family"]
    expected_accent_mode = "monochrome" if profile.get("monochrome") else official["accent_mode"]
    if svg["accent_mode"] == expected_accent_mode:
        breakdown["accent_mode"] = 15
    else:
        breakdown["accent_mode"] = 0
        failures.append(f"强调色模式不匹配：官方偏 {expected_accent_mode}，本地是 {svg['accent_mode']}")

    official_accent = official["colors"]["accent"].upper()
    svg_accent = svg["colors"]["accent"].upper()
    if official_accent == svg_accent:
        breakdown["accent_family"] = 10
    elif expected_accent_family == svg["accent_family"] or (expected_accent_family == "neutral" and svg["accent_family"] in NEUTRAL_FAMILIES):
        breakdown["accent_family"] = 10
    elif expected_accent_mode == "monochrome" and svg["accent_family"] in NEUTRAL_FAMILIES:
        breakdown["accent_family"] = 10
    else:
        breakdown["accent_family"] = 2
        failures.append(f"强调色家族不匹配：官方偏 {expected_accent_family}，本地是 {svg['accent_family']}")

    expected_uppercase = profile.get("force_uppercase", official["uppercase_title"])
    if bool(svg["uppercase_title"]) == bool(expected_uppercase):
        breakdown["typography_case"] = 5
    else:
        breakdown["typography_case"] = 1
        failures.append("标题大小写语气不匹配")

    expected_radius = profile.get("button_radius") or official["button_radius"]
    if svg["button_radius"] == expected_radius:
        breakdown["button_radius"] = 10
    elif {svg["button_radius"], expected_radius} <= {"soft", "pill"}:
        breakdown["button_radius"] = 6
    else:
        breakdown["button_radius"] = 1
        failures.append(f"按钮圆角不匹配：官方偏 {expected_radius}，本地是 {svg['button_radius']}")

    expected_moods = set(profile.get("moods", [])) or set(official["moods"])
    breakdown["mood"] = round(15 * overlap_score(expected_moods, set(svg["moods"])), 1)
    if breakdown["mood"] < 4:
        failures.append("情绪关键词重合度过低")

    hard_fail = False
    if expected_accent_mode == "monochrome" and svg["accent_family"] not in NEUTRAL_FAMILIES:
        hard_fail = True
        failures.append("官方是黑白/单色体系，但本地用了明显彩色强调")
    if expected_layout in {"poster", "luxury-banner"} and svg["layout"] in TOOLING_LAYOUTS:
        hard_fail = True
        failures.append("官方是品牌展示/海报型，但本地缩略图做成了工具控制台")
    if (profile.get("brightness") or official["brightness"]) == "dark" and expected_layout in TOOLING_LAYOUTS and svg["layout"] == "hero-light":
        hard_fail = True
        failures.append("官方是深色工具风，但本地缩略图做成了浅色 hero")
    if svg["layout"] in profile.get("forbidden_layouts", set()):
        hard_fail = True
        failures.append(f"{entry['name']} 命中了禁止版式：{svg['layout']}")

    score = round(sum(breakdown.values()), 1)
    if hard_fail:
        status = "needs_override"
    elif score >= 90:
        status = "pass"
    elif score >= 78:
        status = "needs_override"
    else:
        status = "fail"

    return {
        "status": status,
        "score": score,
        "breakdown": breakdown,
        "failures": failures,
        "hard_fail": hard_fail,
    }


def report_markdown(entries: list[dict[str, Any]]) -> str:
    lines = [
        "# SVG 缩略图风格审查报告",
        "",
        f"- 审查版本：`{AUDIT_VERSION}`",
        f"- 官方指纹版本：`{OFFICIAL_FINGERPRINT_VERSION}`",
        f"- 总数：{len(entries)}",
        "",
    ]
    for row in entries:
        lines.extend(
            [
                f"## {row['name']} / {row['status'].upper()} / {row['score']}",
                "",
                f"- 官方预览：{row['preview_url']}",
                f"- 本地缩略图：{row['path']}",
                f"- 官方布局：{row['official']['layout_hint']}",
                f"- 本地布局：{row['svg']['layout']}",
                f"- 官方明暗：{row['official']['brightness']}",
                f"- 本地明暗：{row['svg']['brightness']}",
                f"- 官方强调：{row['official']['accent_family']} / {row['official']['accent_mode']}",
                f"- 本地强调：{row['svg']['accent_family']} / {row['svg']['accent_mode']}",
                f"- 失败原因：{'；'.join(row['failures']) if row['failures'] else '无'}",
                f"- 修复动作：{row['repair_note']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    references_dir = skill_dir / "references"
    thumbnails_dir = skill_dir / "assets" / "thumbnails"
    cached_fingerprints = load_cached_fingerprints(references_dir)

    catalog = json.loads((references_dir / "style-catalog.json").read_text(encoding="utf-8"))
    manifest = json.loads((thumbnails_dir / "manifest.json").read_text(encoding="utf-8"))
    catalog_by_slug = {entry["slug"]: entry for entry in catalog}
    manifest_by_slug = {entry["slug"]: entry for entry in manifest}

    baseline_rows = []
    report_rows = []
    updated_manifest = []

    for entry in catalog:
        manifest_item = deepcopy(manifest_by_slug[entry["slug"]])
        official = official_fingerprint_with_cache(entry, cached_fingerprints)
        svg = svg_fingerprint(manifest_item)
        audit = compare_fingerprints(entry, official, svg)
        repair_attempts = 0
        repair_note = "无需修复" if audit["status"] == "pass" else "待返工"

        while audit["status"] != "pass" and repair_attempts < MAX_REPAIR_PASSES:
            repair_attempts += 1
            repaired_style = repair_style(entry, manifest_item, official, repair_attempts)
            Path(manifest_item["path"]).write_text(generator.svg_for(repaired_style), encoding="utf-8")
            manifest_item["style"] = repaired_style
            manifest_item["layout"] = repaired_style["layout"]
            svg = svg_fingerprint(manifest_item)
            audit = compare_fingerprints(entry, official, svg)
            repair_note = f"已自动重生成 {repair_attempts} 轮"
        if audit["status"] == "pass" and repair_attempts:
            repair_note = f"第 {repair_attempts} 轮后通过"
        elif audit["status"] != "pass" and repair_attempts:
            repair_note = f"自动重生成 {repair_attempts} 轮后仍未通过"

        manifest_item["layout"] = manifest_item["style"]["layout"]
        manifest_item["layout_label"] = generator.LAYOUT_LABELS.get(manifest_item["layout"], manifest_item["layout"].title())
        manifest_item["audit_status"] = audit["status"]
        manifest_item["audit_score"] = audit["score"]
        manifest_item["audit_version"] = AUDIT_VERSION
        manifest_item["official_fingerprint_version"] = OFFICIAL_FINGERPRINT_VERSION
        manifest_item["audit_failures"] = [] if audit["status"] == "pass" else audit["failures"]
        updated_manifest.append(manifest_item)

        baseline_rows.append(
            {
                "name": entry["name"],
                "slug": entry["slug"],
                "official_fingerprint_version": OFFICIAL_FINGERPRINT_VERSION,
                "preview_url": entry["preview_url"],
                "fingerprint": official,
            }
        )
        report_rows.append(
            {
                "name": entry["name"],
                "slug": entry["slug"],
                "path": manifest_item["path"],
                "preview_url": entry["preview_url"],
                "status": audit["status"],
                "score": audit["score"],
                "breakdown": audit["breakdown"],
                "failures": [] if audit["status"] == "pass" else audit["failures"],
                "repair_note": repair_note,
                "official": official,
                "svg": svg,
            }
        )

    updated_manifest.sort(key=lambda item: item["name"].lower())
    report_rows.sort(key=lambda item: item["name"].lower())
    baseline_rows.sort(key=lambda item: item["name"].lower())

    (references_dir / "style-audit-baseline.json").write_text(
        json.dumps(baseline_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (references_dir / "style-audit-report.json").write_text(
        json.dumps(report_rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (references_dir / "style-audit-report.md").write_text(report_markdown(report_rows), encoding="utf-8")
    (thumbnails_dir / "manifest.json").write_text(
        json.dumps(updated_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    passed = sum(1 for row in report_rows if row["status"] == "pass")
    needs_override = sum(1 for row in report_rows if row["status"] == "needs_override")
    failed = sum(1 for row in report_rows if row["status"] == "fail")
    print(f"Audited {len(report_rows)} thumbnails: {passed} pass / {needs_override} needs_override / {failed} fail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

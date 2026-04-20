#!/usr/bin/env python3
"""Recommend three styles from a local style catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CANONICAL_STYLE_MAP = {
    "apple": "Apple",
    "nike": "Nike",
    "linear": "Linear",
    "stripe": "Stripe",
    "vercel": "Vercel",
    "supabase": "Supabase",
    "figma": "Figma",
}

CATEGORY_HINTS = {
    "editor": ["Design & Creative Tools", "Developer Tools & IDEs", "Productivity & SaaS"],
    "dashboard": ["Developer Tools & IDEs", "Backend, Database & DevOps", "Productivity & SaaS"],
    "docs": ["Developer Tools & IDEs", "Backend, Database & DevOps", "Productivity & SaaS"],
    "landing-page": ["Media & Consumer Tech", "E-commerce & Retail", "Fintech & Crypto"],
    "commerce": ["E-commerce & Retail", "Fintech & Crypto"],
    "brand-site": ["Media & Consumer Tech", "Automotive", "E-commerce & Retail"],
    "creative-tool": ["Design & Creative Tools", "Media & Consumer Tech"],
}

DENSITY_SCALE = {"low": 1, "medium": 2, "high": 3}
TOOLISH_PAGES = {"editor", "dashboard", "docs", "creative-tool"}
BRANDISH_PAGES = {"landing-page", "brand-site", "commerce", "campaign", "marketing"}
TOOLISH_MOODS = {"developer", "precise", "tooling", "technical", "minimal"}
EXPRESSIVE_MOODS = {"premium", "cinematic", "editorial", "bold", "luxury", "future-facing"}
REFACTOR_HINTS = (
    "已有项目",
    "改版",
    "重做 ui",
    "重做界面",
    "升级界面",
    "保留结构",
    "换视觉",
    "不要从零设计",
    "改造 ui",
    "改造界面",
)


def load_catalog(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonicalize_style(name: str) -> str:
    key = name.strip().lower()
    if key in CANONICAL_STYLE_MAP:
        return CANONICAL_STYLE_MAP[key]
    for value in CANONICAL_STYLE_MAP.values():
        if value.lower() == key:
            return value
    return name.strip()


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


def detect_project_mode(payload: dict) -> str:
    explicit = str(payload.get("project_mode", "")).strip().lower()
    if explicit in {"greenfield", "refactor"}:
        return explicit
    if payload.get("current_ui_findings") or payload.get("existing_pages") or payload.get("component_inventory"):
        return "refactor"
    lowered = str(payload.get("user_request", "")).lower()
    return "refactor" if any(token in lowered for token in REFACTOR_HINTS) else "greenfield"


def density_gap(current: str, target: str) -> int:
    if current not in DENSITY_SCALE or target not in DENSITY_SCALE:
        return 0
    return abs(DENSITY_SCALE[current] - DENSITY_SCALE[target])


def level_from_points(points: int) -> str:
    if points >= 5:
        return "高"
    if points >= 3:
        return "中"
    return "低"


def join_reason(parts: list[str], fallback: str) -> str:
    cleaned = [part.rstrip("。.;； ") for part in parts if part]
    if not cleaned:
        return fallback
    return "；".join(cleaned[:2]) + "。"


def assess_refactor(entry: dict, profile: dict) -> dict:
    page_types = set(profile["page_types"]) | set(profile["existing_pages"])
    entry_pages = set(entry.get("best_for", []))
    entry_moods = set(entry.get("mood_keywords", []))
    findings_text = " ".join(profile["current_ui_findings"]).lower()
    scope = str(profile["refactor_scope"]).lower()

    benefit_points = 0
    benefit_reasons: list[str] = []
    difficulty_points = 1
    difficulty_reasons: list[str] = []
    risk_points = 1
    risk_reasons: list[str] = []

    page_matches = page_types & entry_pages
    if page_matches:
        benefit_points += min(3, len(page_matches))
        benefit_reasons.append(f"命中现有页面类型：{', '.join(sorted(page_matches))}")
    elif page_types:
        risk_points += 2
        risk_reasons.append("与当前页面职责的直接匹配较弱")

    if entry.get("brightness") == profile["brightness"]:
        benefit_points += 1
        benefit_reasons.append("明暗基调延续现有界面，改造阻力较小")
    elif profile["brightness"] != "mixed":
        difficulty_points += 1
        risk_points += 1
        difficulty_reasons.append("需要重新收敛明暗层级")

    gap = density_gap(profile["ui_density"], entry.get("layout_density", "medium"))
    if gap == 0:
        benefit_points += 1
        benefit_reasons.append("版式密度与当前使用场景一致")
    elif gap == 1:
        difficulty_points += 1
        difficulty_reasons.append("需要适度调整信息密度和留白")
    elif gap >= 2:
        difficulty_points += 2
        risk_points += 1
        difficulty_reasons.append("页面密度跨度较大，可能触发布局级调整")

    if page_types & TOOLISH_PAGES:
        if entry_moods & TOOLISH_MOODS:
            benefit_points += 2
            benefit_reasons.append("风格自带工具效率和精准感，适合保留现有工作流")
        else:
            risk_points += 1
            risk_reasons.append("品牌表达可能压过工具效率")

    if page_types & BRANDISH_PAGES:
        if entry_moods & EXPRESSIVE_MOODS:
            benefit_points += 2
            benefit_reasons.append("能补足品牌张力和记忆点")
        else:
            risk_points += 1
            risk_reasons.append("可能过稳，品牌升级感不够明显")

    if "层级" in findings_text or "spacing" in findings_text or "面板" in findings_text:
        if entry_moods & {"precise", "minimal", "tooling"}:
            benefit_points += 1
            benefit_reasons.append("对层级和模块秩序的修复收益更直接")
    if "品牌" in findings_text or "记忆点" in findings_text:
        if entry_moods & {"premium", "cinematic", "editorial", "bold"}:
            benefit_points += 1
            benefit_reasons.append("更容易拉开品牌感知")

    if "不改核心信息架构" in scope and gap >= 2:
        risk_points += 1
        risk_reasons.append("当前范围不适合大幅重排信息结构")

    if entry["name"] in profile["explicit_styles"] and benefit_points <= 2:
        risk_points += 1
        risk_reasons.append("这是用户指定风格，但需要更严格地控制落地范围")

    return {
        "benefit": {
            "label": level_from_points(benefit_points),
            "reason": join_reason(benefit_reasons, "能改善当前项目的视觉一致性和页面气质。"),
        },
        "difficulty": {
            "label": level_from_points(difficulty_points),
            "reason": join_reason(
                difficulty_reasons,
                "主要是样式层和组件规范收敛，改造复杂度可控。",
            ),
        },
        "risk": {
            "label": level_from_points(risk_points),
            "reason": join_reason(risk_reasons, "主要风险来自局部页面与该风格的适配边界。"),
        },
        "compatibility_note": join_reason(
            benefit_reasons + risk_reasons,
            "适配度总体可控，但仍需按页面职责分层落地。",
        ),
    }


def collect_profile(payload: dict) -> dict:
    explicit_styles = [canonicalize_style(item) for item in payload.get("explicit_styles", [])]
    repo_signals = payload.get("repo_signals", {})
    screenshot_signals = payload.get("screenshot_signals", {})

    page_types = set(repo_signals.get("page_types", []))
    page_types.update(screenshot_signals.get("page_types", []))

    moods = set(repo_signals.get("tone", []))
    moods.update(screenshot_signals.get("mood", []))
    moods.update(repo_signals.get("keywords", []))
    moods.update(screenshot_signals.get("keywords", []))

    brightness = screenshot_signals.get("brightness") or repo_signals.get("surfaces") or "mixed"
    ui_density = repo_signals.get("ui_density") or screenshot_signals.get("ui_density") or "medium"
    existing_pages = uniq(payload.get("existing_pages", []))
    component_inventory = uniq(payload.get("component_inventory", []))
    current_ui_findings = uniq(payload.get("current_ui_findings", []))
    project_mode = detect_project_mode(payload)
    refactor_scope = str(payload.get("refactor_scope", "")).strip()

    confidence_inputs = 0
    confidence_inputs += 1 if explicit_styles else 0
    confidence_inputs += 1 if repo_signals else 0
    confidence_inputs += 1 if screenshot_signals else 0
    confidence_inputs += 1 if current_ui_findings or existing_pages or component_inventory else 0

    return {
        "user_request": payload.get("user_request", ""),
        "project_mode": project_mode,
        "explicit_styles": explicit_styles,
        "page_types": sorted(page_types),
        "moods": sorted(moods),
        "brightness": str(brightness).lower(),
        "ui_density": str(ui_density).lower(),
        "existing_pages": existing_pages,
        "component_inventory": component_inventory,
        "current_ui_findings": current_ui_findings,
        "refactor_scope": refactor_scope,
        "confidence": "high" if confidence_inputs >= 3 else "medium" if confidence_inputs == 2 else "low",
    }


def score_entry(entry: dict, profile: dict) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    if entry["name"] in profile["explicit_styles"]:
        score += 120
        reasons.append("用户已明确点名该风格，必须纳入候选。")

    matches = set(entry.get("best_for", [])) & set(profile["page_types"])
    if matches:
        delta = 22 * len(matches)
        score += delta
        reasons.append(f"页面类型匹配：{', '.join(sorted(matches))}。")

    if entry.get("brightness") == profile["brightness"]:
        score += 12
        reasons.append(f"亮暗倾向匹配：{profile['brightness']}。")

    if entry.get("layout_density") == profile["ui_density"]:
        score += 12
        reasons.append(f"界面密度匹配：{profile['ui_density']}。")

    mood_matches = set(entry.get("mood_keywords", [])) & set(profile["moods"])
    if mood_matches:
        delta = 6 * len(mood_matches)
        score += delta
        reasons.append(f"气质关键词匹配：{', '.join(sorted(mood_matches))}。")

    request_lower = profile["user_request"].lower()
    for token in (entry["name"], entry["slug"], entry["category"]):
        if token.lower() in request_lower:
            score += 8
            reasons.append(f"用户描述中出现了 {token} 相关线索。")
            break

    category_bonus = 0
    for page_type in profile["page_types"]:
        if entry["category"] in CATEGORY_HINTS.get(page_type, []):
            category_bonus += 7
    if category_bonus:
        score += category_bonus
        reasons.append("所属品类与当前项目形态相符。")

    if not reasons:
        reasons.append("作为对照项，它提供了不同于主推荐路线的审美方向。")
    return score, reasons


def diversify(sorted_entries: list[dict], profile: dict) -> list[dict]:
    explicit = set(profile["explicit_styles"])
    chosen: list[dict] = []
    for entry in sorted_entries:
        if entry["name"] in explicit and entry not in chosen:
            chosen.append(entry)
            break

    for entry in sorted_entries:
        if entry in chosen:
            continue
        penalty = 0
        for picked in chosen:
            if entry["category"] == picked["category"]:
                penalty += 18
            overlap = len(set(entry.get("best_for", [])) & set(picked.get("best_for", [])))
            penalty += overlap * 4
            if entry.get("brightness") == picked.get("brightness"):
                penalty += 2
        adjusted = entry["score"] - penalty
        entry["_adjusted_score"] = adjusted

    remaining = [e for e in sorted_entries if e not in chosen]
    remaining.sort(key=lambda item: item.get("_adjusted_score", item["score"]), reverse=True)
    for entry in remaining:
        if len(chosen) >= 3:
            break
        chosen.append(entry)
    chosen = chosen[:3]

    rank_labels = ["最推荐", "次推荐", "对照项"]
    for idx, entry in enumerate(chosen):
        entry["rank_label"] = rank_labels[idx]
    return chosen


def build_output(catalog: list[dict], payload: dict) -> dict:
    profile = collect_profile(payload)
    ranked: list[dict] = []
    for raw_entry in catalog:
        score, reasons = score_entry(raw_entry, profile)
        entry = dict(raw_entry)
        entry["score"] = score
        entry["reasons"] = reasons
        ranked.append(entry)

    ranked.sort(key=lambda item: item["score"], reverse=True)
    top_three = diversify(ranked, profile)

    for entry in top_three:
        if entry["name"] in profile["explicit_styles"] and len(entry["reasons"]) > 1:
            reason_line = "；".join(item.rstrip("。.；; ") for item in entry["reasons"][:2]) + "。"
        else:
            reason_line = entry["reasons"][0]
        entry["why_it_fits"] = reason_line
        entry["how_it_looks"] = entry.get("summary", "")
        entry["official_preview"] = entry["preview_url"]
        entry["override_note"] = (
            "这是你指定的风格之一，我额外保留了两个相邻但不完全重复的备选。"
            if entry["name"] in profile["explicit_styles"]
            else ""
        )
        if profile["project_mode"] == "refactor":
            entry["refactor_assessment"] = assess_refactor(entry, profile)

    return {
        "profile": profile,
        "recommendations": top_three,
        "next_step": (
            "若你已经偏向第一名，先生成 UI-REFACTOR.md 草稿，再把页面级与组件级任务单交给前端界面设计（Frontend Design）继续落地；"
            "若还在犹豫，先重点比较前两名的改造收益、难度和兼容风险。"
            if profile["project_mode"] == "refactor"
            else "若你已经偏向第一名，把它交给前端界面设计（Frontend Design）继续落页面；"
            "若还在犹豫，先重点比较前两名的风险差异。"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the project profile JSON")
    parser.add_argument(
        "--catalog",
        default=str(Path(__file__).resolve().parents[1] / "references" / "style-catalog.json"),
        help="Path to style catalog JSON",
    )
    parser.add_argument("--output", help="Optional path for JSON output")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    catalog = load_catalog(Path(args.catalog))
    result = build_output(catalog, payload)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render markdown style cards from recommendation JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

LABELS = {
    "low": "低",
    "medium": "中",
    "high": "高",
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
    "developer": "开发者感",
    "precise": "精准",
    "tooling": "工具感",
    "minimal": "极简",
    "premium": "高级",
    "cinematic": "电影感",
}


def validate_recommendations(payload: dict) -> None:
    recommendations = payload.get("recommendations", [])
    if len(recommendations) != 3:
        raise SystemExit(f"Expected exactly 3 recommendations, got {len(recommendations)}")

    explicit_styles = {
        str(item).strip().lower()
        for item in payload.get("profile", {}).get("explicit_styles", [])
        if str(item).strip()
    }
    if explicit_styles:
        selected = {str(item.get("name", "")).strip().lower() for item in recommendations}
        if not selected & explicit_styles:
            raise SystemExit("Expected at least one explicit style to be preserved in recommendations")


def validate_rendered_markdown(markdown: str, payload: dict) -> None:
    recommendations = payload.get("recommendations", [])
    header_count = sum(1 for line in markdown.splitlines() if line.startswith("## "))
    expected_headers = len(recommendations) + 1
    if header_count < expected_headers:
        raise SystemExit(
            f"Rendered markdown is missing card sections: expected at least {expected_headers} H2 headers, got {header_count}"
        )

    for idx, entry in enumerate(recommendations, start=1):
        header = f"## {idx}. {entry['name']}｜"
        if header not in markdown:
            raise SystemExit(f"Rendered markdown is missing the card header for {entry['name']}")

        thumbnail_path = thumbnail_path_for(entry)
        if thumbnail_path:
            image_markdown = f"![{entry['name']} 预览]({thumbnail_path})"
            if image_markdown not in markdown:
                raise SystemExit(f"Rendered markdown is missing the SVG preview markdown for {entry['name']}")


def humanize(items: list[str] | str) -> str:
    if isinstance(items, str):
        return LABELS.get(items, items)
    return " / ".join(LABELS.get(item, item) for item in items)


def thumbnail_path_for(entry: dict) -> Path | None:
    skill_dir = Path(__file__).resolve().parents[1]
    candidate = skill_dir / "assets" / "thumbnails" / f"{entry['slug']}.svg"
    if candidate.exists():
        return candidate
    return None


def card_markdown(rank: int, entry: dict) -> str:
    lines = [
        f"## {rank}. {entry['name']}｜{entry.get('rank_label', '')}",
        "",
        f"白话印象：{entry['plain_impression']}",
        "",
        f"为什么适合：{entry['why_it_fits']}",
    ]
    if entry.get("override_note"):
        lines.extend(["", f"补充说明：{entry['override_note']}"])
    thumbnail_path = thumbnail_path_for(entry)
    if thumbnail_path:
        lines.extend(
            [
                "",
                f"本地缩略图：![{entry['name']} 预览]({thumbnail_path})",
                f"缩略图路径：`{thumbnail_path}`",
            ]
        )
    lines.extend(
        [
            "",
            f"这类风格通常长什么样：{entry['how_it_looks']}",
            "",
            f"主要风险：{entry['risk_note']}",
            "",
            f"官方预览：[{entry['official_preview']}]({entry['official_preview']})",
            "",
            "本地说明卡：",
            f"- 主色倾向：{entry['color_tendency']}",
            f"- 排版气质：{entry['typography_tone']}",
            f"- 版式密度：{humanize(entry['layout_density'])}",
            f"- 典型适用页面：{humanize(entry['best_for'][:3])}",
            f"- 情绪关键词：{humanize(entry['mood_keywords'][:4])}",
        ]
    )
    assessment = entry.get("refactor_assessment")
    if assessment:
        lines.extend(
            [
                "",
                "改造判断：",
                f"- 改造收益：{assessment['benefit']['label']}｜{assessment['benefit']['reason']}",
                f"- 改造难度：{assessment['difficulty']['label']}｜{assessment['difficulty']['reason']}",
                f"- 兼容风险：{assessment['risk']['label']}｜{assessment['risk']['reason']}",
            ]
        )
    return "\n".join(lines)


def render_markdown(payload: dict, *, skip_validation: bool = False) -> str:
    if not skip_validation:
        validate_recommendations(payload)
    cards = [card_markdown(idx, entry) for idx, entry in enumerate(payload["recommendations"], start=1)]
    intro = [
        "# 风格推荐结果",
        "",
        f"项目模式：{payload['profile'].get('project_mode', 'greenfield')}",
        "",
        f"判断置信度：{payload['profile']['confidence']}",
        "",
    ]
    if payload["profile"].get("project_mode") == "refactor":
        intro.extend(
            [
                "当前 UI 诊断：",
                *[f"- {item}" for item in payload["profile"].get("current_ui_findings", [])[:5]],
                "",
            ]
        )
    intro.extend(
        [
        *cards,
        "",
        "## 建议下一步",
        "",
        payload["next_step"],
        "",
        ]
    )
    markdown = "\n".join(intro)
    if not skip_validation:
        validate_rendered_markdown(markdown, payload)
    return markdown


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--output", help="Optional markdown output path")
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip the built-in output validation checks",
    )
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    markdown = render_markdown(payload, skip_validation=args.skip_validation)
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

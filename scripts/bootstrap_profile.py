#!/usr/bin/env python3
"""Bootstrap a style-compass input profile JSON from simple CLI flags."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


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


def detect_project_mode(request: str, explicit_mode: str | None) -> str:
    if explicit_mode:
        return explicit_mode
    lowered = request.lower()
    return "refactor" if any(token in lowered for token in REFACTOR_HINTS) else "greenfield"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True, help="User request text")
    parser.add_argument(
        "--project-mode",
        choices=["greenfield", "refactor"],
        help="Project mode. Defaults to auto-detect from the request.",
    )
    parser.add_argument("--style", action="append", default=[], help="Explicit style preference")
    parser.add_argument("--page-type", action="append", default=[], help="Repo page type signal")
    parser.add_argument("--density", default="medium", help="UI density")
    parser.add_argument("--surface", default="mixed", help="Surface brightness or repo surface tone")
    parser.add_argument("--tone", action="append", default=[], help="Repo tone keywords")
    parser.add_argument("--repo-keyword", action="append", default=[], help="Repo keywords")
    parser.add_argument(
        "--existing-page",
        action="append",
        default=[],
        help="Known existing page or surface to preserve/refactor",
    )
    parser.add_argument(
        "--component",
        action="append",
        default=[],
        help="Known component inventory item",
    )
    parser.add_argument(
        "--current-finding",
        action="append",
        default=[],
        help="Known current UI issue or finding",
    )
    parser.add_argument(
        "--refactor-scope",
        default="",
        help="Refactor scope, such as 仅视觉层 or 允许布局调整",
    )
    parser.add_argument("--screenshot-page-type", action="append", default=[], help="Screenshot page types")
    parser.add_argument("--screenshot-brightness", help="Screenshot brightness")
    parser.add_argument("--screenshot-density", help="Screenshot density override")
    parser.add_argument("--image-weight", help="Screenshot image weight")
    parser.add_argument("--mood", action="append", default=[], help="Screenshot mood keywords")
    parser.add_argument("--shot-keyword", action="append", default=[], help="Screenshot keywords")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    payload = {
        "user_request": args.request,
        "project_mode": detect_project_mode(args.request, args.project_mode),
        "explicit_styles": args.style,
        "repo_signals": {
            "page_types": args.page_type,
            "ui_density": args.density,
            "surfaces": args.surface,
            "tone": args.tone,
            "keywords": args.repo_keyword,
        },
        "screenshot_signals": {
            "page_types": args.screenshot_page_type,
            "brightness": args.screenshot_brightness,
            "ui_density": args.screenshot_density,
            "image_weight": args.image_weight,
            "mood": args.mood,
            "keywords": args.shot_keyword,
        },
        "existing_pages": args.existing_page,
        "component_inventory": args.component,
        "current_ui_findings": args.current_finding,
        "refactor_scope": args.refactor_scope,
    }

    output = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

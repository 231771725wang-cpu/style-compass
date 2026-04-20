#!/usr/bin/env python3
"""Render style cards and verify the final markdown in one step."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_style_cards import render_markdown
from verify_rendered_cards import verify


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--output", required=True, help="Output markdown path")
    parser.add_argument(
        "--skip-render-validation",
        action="store_true",
        help="Skip render_style_cards.py built-in validation checks",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only write the markdown file and suppress PASS logs",
    )
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    markdown = render_markdown(payload, skip_validation=args.skip_render_validation)
    output_path = Path(args.output)
    output_path.write_text(markdown, encoding="utf-8")

    issues = verify(payload, markdown)
    if issues:
        print("FAIL")
        for item in issues:
            print(f"- {item}")
        return 1

    if not args.quiet:
        print("PASS")
        print(f"- 已输出 Markdown：{output_path}")
        print("- 已确认输出包含 3 张风格卡。")
        if payload.get("profile", {}).get("explicit_styles"):
            print("- 已确认保留至少一张用户指定风格。")
        print("- 已确认可用的本地 SVG 预览 Markdown 已写进输出。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

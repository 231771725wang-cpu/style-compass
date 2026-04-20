#!/usr/bin/env python3
"""Verify that rendered style cards are complete and image-ready for Codex."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def thumbnail_path_for(entry: dict) -> Path | None:
    skill_dir = Path(__file__).resolve().parents[1]
    candidate = skill_dir / "assets" / "thumbnails" / f"{entry['slug']}.svg"
    if candidate.exists():
        return candidate
    return None


def verify(payload: dict, markdown: str) -> list[str]:
    issues: list[str] = []
    recommendations = payload.get("recommendations", [])
    if len(recommendations) != 3:
        issues.append(f"候选数量不对：期望 3 张卡，实际 {len(recommendations)} 张。")

    explicit_styles = {
        str(item).strip().lower()
        for item in payload.get("profile", {}).get("explicit_styles", [])
        if str(item).strip()
    }
    selected = {str(item.get("name", "")).strip().lower() for item in recommendations}
    if explicit_styles and not (selected & explicit_styles):
        issues.append("用户指定风格没有出现在最终 3 张卡里。")

    for idx, entry in enumerate(recommendations, start=1):
        header = f"## {idx}. {entry['name']}｜"
        if header not in markdown:
            issues.append(f"缺少第 {idx} 张卡的标题：{entry['name']}。")

        thumbnail_path = thumbnail_path_for(entry)
        if thumbnail_path:
            image_markdown = f"![{entry['name']} 预览]({thumbnail_path})"
            if image_markdown not in markdown:
                issues.append(f"{entry['name']} 的 SVG 预览 Markdown 没有写进输出。")
        elif "本地缩略图：" in markdown and entry["name"] in markdown:
            issues.append(f"{entry['name']} 没有本地 SVG，但输出里看起来像是引用了缩略图占位。")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Recommendation JSON path")
    parser.add_argument("--markdown", required=True, help="Rendered markdown path")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    markdown = Path(args.markdown).read_text(encoding="utf-8")
    issues = verify(payload, markdown)
    if issues:
        print("FAIL")
        for item in issues:
            print(f"- {item}")
        return 1

    print("PASS")
    print("- 已确认输出包含 3 张风格卡。")
    if payload.get("profile", {}).get("explicit_styles"):
        print("- 已确认保留至少一张用户指定风格。")
    print("- 已确认可用的本地 SVG 预览 Markdown 已写进输出。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

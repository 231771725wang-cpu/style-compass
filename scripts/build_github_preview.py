#!/usr/bin/env python3
"""Build a shareable GitHub preview image from local gallery screenshots."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_DIR = ROOT / "assets" / "gallery" / "previews"
OUTPUT_PATH = PREVIEW_DIR / "style-gallery-github-preview.png"

SOURCES = [
    ("总览入口", PREVIEW_DIR / "style-gallery-hero.png"),
    ("卡片密度", PREVIEW_DIR / "style-gallery-preview-fixed.png"),
    ("组织结构", PREVIEW_DIR / "style-gallery-structured.png"),
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def rounded_card(image: Image.Image, size: tuple[int, int], radius: int) -> Image.Image:
    target = image.resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    card = Image.new("RGBA", size, (0, 0, 0, 0))
    card.paste(target, (0, 0), mask)
    return card


def build() -> None:
    canvas = Image.new("RGB", (1600, 980), "#06070b")
    draw = ImageDraw.Draw(canvas)

    for y, color in [(0, "#0b1020"), (320, "#09090d"), (980, "#050506")]:
        draw.rectangle((0, y, 1600, y + 420), fill=color)

    draw.ellipse((-180, -120, 520, 420), fill="#121a34")
    draw.ellipse((1100, -160, 1780, 360), fill="#151328")
    draw.ellipse((1220, 640, 1820, 1200), fill="#121827")

    title_font = load_font(76, bold=True)
    body_font = load_font(28)
    chip_font = load_font(20, bold=True)
    label_font = load_font(22, bold=True)

    draw.rounded_rectangle((86, 78, 302, 124), radius=23, fill="#12151e", outline="#23283a", width=2)
    draw.text((108, 91), "STYLE GALLERY", fill="#f4f5f7", font=chip_font)

    draw.text((86, 164), "风格总览 / Style Gallery", fill="#f6f6f2", font=title_font)
    draw.text(
        (86, 254),
        "先看总览，再做 UI 风格决策。把“帮我挑风格”变成一个可浏览、可比较、可交接的入口。",
        fill="#d4d7dd",
        font=body_font,
    )

    chips = ["68 个风格", "热门总榜", "分类热门", "双语切换", "官方预览跳转"]
    x = 88
    for chip in chips:
        width = draw.textbbox((0, 0), chip, font=chip_font)[2] + 36
        draw.rounded_rectangle((x, 322, x + width, 366), radius=22, fill="#10131b", outline="#262c3d", width=2)
        draw.text((x + 18, 334), chip, fill="#f0f1f4", font=chip_font)
        x += width + 12

    positions = [
        (86, 430, 448, 274),
        (498, 430, 448, 274),
        (910, 430, 604, 360),
    ]

    for (label, source), (x0, y0, w, h) in zip(SOURCES, positions):
        image = Image.open(source).convert("RGB")
        card = rounded_card(image, (w, h), radius=24)
        shadow = Image.new("RGBA", (w + 28, h + 28), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle((14, 18, w + 10, h + 14), radius=28, fill=(0, 0, 0, 110))
        canvas.paste(shadow, (x0 - 10, y0 - 8), shadow)
        canvas.paste(card, (x0, y0), card)

        label_width = draw.textbbox((0, 0), label, font=label_font)[2] + 28
        draw.rounded_rectangle((x0 + 18, y0 + 16, x0 + 18 + label_width, y0 + 52), radius=18, fill="#10141d")
        draw.text((x0 + 32, y0 + 24), label, fill="#f4f5f7", font=label_font)

    footer = "适合 GitHub README 首屏、仓库介绍和后续分享物料"
    draw.text((88, 860), footer, fill="#aeb4c0", font=body_font)
    draw.text((88, 900), "assets/gallery/style-gallery.html", fill="#eff1f5", font=label_font)

    canvas.save(OUTPUT_PATH, quality=95)


def main() -> int:
    build()
    print(f"Wrote GitHub preview to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

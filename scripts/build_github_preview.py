#!/usr/bin/env python3
"""Build a shareable GitHub preview image from live gallery screenshots."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
PREVIEW_DIR = ROOT / "assets" / "gallery" / "previews"
GALLERY_PATH = ROOT / "assets" / "gallery" / "style-gallery.html"
OUTPUT_PATH = PREVIEW_DIR / "style-gallery-github-preview.png"
HOT_OUTPUT_PATH = PREVIEW_DIR / "style-gallery-live-hot.png"
CATEGORY_OUTPUT_PATH = PREVIEW_DIR / "style-gallery-live-category.png"
UPSTREAM_SITE = "https://getdesign.md"
UPSTREAM_REPO = "https://github.com/VoltAgent/awesome-design-md"
VIEWPORT = {"width": 1680, "height": 1900}
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]
LIVE_SOURCES = [
    ("热门总榜实时截图", HOT_OUTPUT_PATH, (86, 430, 844, 430)),
    ("分类热门实时截图", CATEGORY_OUTPUT_PATH, (954, 430, 560, 430)),
]


def choose_browser_executable() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("No supported browser executable found for gallery preview capture.")


def load_font_from_candidates(
    candidates: list[str], size: int
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def load_zh_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        ]
    )
    return load_font_from_candidates(candidates, size)


def load_zh_display_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    return load_font_from_candidates(candidates, size)


def load_en_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = (
        [
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/HelveticaNeue.ttc",
            "/System/Library/Fonts/SFNS.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
    )
    return load_font_from_candidates(candidates, size)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_card(image: Image.Image, size: tuple[int, int], radius: int) -> Image.Image:
    target = image.resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    card = Image.new("RGBA", size, (0, 0, 0, 0))
    card.paste(target, (0, 0), mask)
    return card


def ensure_gallery_is_current() -> None:
    subprocess.run([sys.executable, str(SCRIPT_DIR / "build_style_gallery.py")], check=True)


def wait_for_section_images(page, selector: str) -> None:
    page.wait_for_function(
        """
        (sectionSelector) => {
          const section = document.querySelector(sectionSelector);
          if (!section) return false;
          const images = Array.from(section.querySelectorAll('img'));
          return images.length > 0 && images.every((img) => img.complete && img.naturalWidth > 0);
        }
        """,
        arg=selector,
        timeout=15000,
    )


def capture_live_gallery_sections() -> None:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    executable_path = choose_browser_executable()
    gallery_url = GALLERY_PATH.resolve().as_uri()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=executable_path)
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)

        try:
            page.goto(gallery_url, wait_until="networkidle", timeout=45000)
        except PlaywrightTimeoutError:
            page.goto(gallery_url, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(2200)

        page.add_style_tag(
            content="""
            * { animation: none !important; transition: none !important; }
            html, body { scroll-behavior: auto !important; }
            """
        )
        page.wait_for_selector("#global-hot-list .rank-card", timeout=20000)
        page.wait_for_selector("#category-hot-list .category-panel", timeout=20000)
        page.wait_for_function(
            "() => document.querySelectorAll('#global-hot-list .rank-card').length >= 4",
            timeout=20000,
        )
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)

        page.locator("#lang-zh").click()
        page.wait_for_timeout(400)

        hot_locator = page.locator("#global-hot-section")
        hot_locator.scroll_into_view_if_needed()
        wait_for_section_images(page, "#global-hot-section")
        hot_locator.screenshot(path=str(HOT_OUTPUT_PATH))

        category_locator = page.locator("#category-hot-section")
        category_locator.scroll_into_view_if_needed()
        wait_for_section_images(page, "#category-hot-section")
        category_locator.screenshot(path=str(CATEGORY_OUTPUT_PATH))

        browser.close()


def build() -> None:
    ensure_gallery_is_current()
    capture_live_gallery_sections()

    canvas = Image.new("RGB", (1600, 980), "#080808")
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((0, 0, 1600, 980), fill="#080808")
    draw.rounded_rectangle((34, 30, 1566, 950), radius=38, outline="#1a1a1a", width=2)
    draw.rounded_rectangle((52, 48, 1548, 932), radius=30, outline="#121212", width=1)
    draw.line((82, 338, 1518, 338), fill="#191919", width=2)
    draw.line((1090, 384, 1090, 882), fill="#161616", width=2)

    eyebrow_font = load_en_font(16, bold=True)
    title_zh_font = load_zh_display_font(78)
    title_en_font = load_en_font(32, bold=False)
    body_font = load_zh_font(24, bold=False)
    chip_font = load_zh_font(18, bold=False)
    label_font = load_zh_font(20, bold=False)
    footer_font = load_zh_font(17, bold=False)
    meta_font = load_en_font(16, bold=False)

    draw.rounded_rectangle((84, 72, 284, 118), radius=23, fill="#101010", outline="#2a2a2a", width=2)
    draw.text((108, 87), "STYLE COMPASS", fill="#f2efe8", font=eyebrow_font)

    draw.text((84, 144), "风格总览", fill="#f4f1ea", font=title_zh_font)
    draw.text((90, 238), "Style Gallery", fill="#b4b1aa", font=title_en_font)

    description = "README 封面直接取自当前总览页实时截图，让第一印象来自真实卡片，而不是示意图。"
    draw.text((84, 292), description, fill="#c8c4bc", font=body_font)

    chips = ["实时截图", "热门总榜", "分类热门"]
    x = 84
    for chip in chips:
        width = draw.textbbox((0, 0), chip, font=chip_font)[2] + 30
        draw.rounded_rectangle((x, 356, x + width, 396), radius=20, fill="#101010", outline="#252525", width=2)
        draw.text((x + 15, 367), chip, fill="#ece8df", font=chip_font)
        x += width + 10

    for label, source, (x0, y0, w, h) in [
        ("热门总榜", HOT_OUTPUT_PATH, (84, 390, 980, 458)),
        ("分类热门", CATEGORY_OUTPUT_PATH, (1122, 430, 394, 418)),
    ]:
        image = Image.open(source).convert("RGB")
        card = rounded_card(image, (w, h), radius=24)
        shadow = Image.new("RGBA", (w + 28, h + 28), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shadow_draw.rounded_rectangle((14, 18, w + 10, h + 14), radius=28, fill=(0, 0, 0, 145))
        canvas.paste(shadow, (x0 - 10, y0 - 8), shadow)
        canvas.paste(card, (x0, y0), card)

        label_width = draw.textbbox((0, 0), label, font=label_font)[2] + 24
        draw.rounded_rectangle((x0 + 18, y0 + 16, x0 + 18 + label_width, y0 + 48), radius=16, fill="#0e0e0e")
        draw.text((x0 + 30, y0 + 22), label, fill="#f2eee7", font=label_font)

    footer_title = "适合 README 首屏，也能直接说明这个 skill 的真实视觉质感。"
    draw.text((84, 872), footer_title, fill="#ddd8cf", font=body_font)
    draw.text((84, 910), "本地入口  风格总览（Style Gallery）.html", fill="#f1eee7", font=label_font)

    source_lines = wrap_text(
        draw,
        f"原项目地址  {UPSTREAM_SITE}  ·  {UPSTREAM_REPO}",
        footer_font,
        620,
    )
    y = 906
    for line in source_lines:
        draw.text((892, y), line, fill="#959089", font=footer_font)
        y += 24

    draw.text((1122, 882), "Live screenshots from current local gallery", fill="#7e7a73", font=meta_font)
    canvas.save(OUTPUT_PATH, quality=95)


def main() -> int:
    build()
    print(f"Wrote GitHub preview to {OUTPUT_PATH}")
    print(f"Wrote live gallery previews to {HOT_OUTPUT_PATH} and {CATEGORY_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

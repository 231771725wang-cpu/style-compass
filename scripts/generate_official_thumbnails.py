#!/usr/bin/env python3
"""Generate official preview thumbnails for style calibration."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from PIL import Image, ImageOps
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
MANIFEST_PATH = SKILL_DIR / "assets" / "thumbnails" / "manifest.json"
OUTPUT_DIR = SKILL_DIR / "assets" / "official-thumbnails"

VIEWPORT = {"width": 1440, "height": 960}
TARGET_SIZE = (1280, 800)
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def choose_browser_executable() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("No supported browser executable found for official thumbnail capture.")


def crop_thumbnail(source_path: Path, target_path: Path) -> None:
    with Image.open(source_path) as image:
        fitted = ImageOps.fit(
            image.convert("RGB"),
            TARGET_SIZE,
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.08),
        )
        fitted.save(target_path, format="PNG", optimize=True)


def load_manifest() -> list[dict]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(entries: list[dict]) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def capture_preview(page, url: str, output_path: Path) -> None:
    try:
        page.goto(url, wait_until="networkidle", timeout=45000)
    except PlaywrightTimeoutError:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2000)

    page.evaluate("window.scrollTo(0, 0)")
    page.add_style_tag(
        content="""
        * { animation: none !important; transition: none !important; }
        html, body { scroll-behavior: auto !important; }
        """
    )
    page.wait_for_timeout(1200)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        temp_path = Path(handle.name)

    try:
        page.screenshot(path=str(temp_path), full_page=False)
        crop_thumbnail(temp_path, output_path)
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    manifest = load_manifest()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    executable_path = choose_browser_executable()

    captured = 0
    missing = 0

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=executable_path)
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)

        for entry in manifest:
            output_path = OUTPUT_DIR / f"{entry['slug']}.png"

            preview_url = entry.get("preview_url")
            if not preview_url:
                entry["official_thumb_path"] = None
                entry["thumb_source"] = "svg" if entry.get("path") else "none"
                missing += 1
                continue

            try:
                capture_preview(page, preview_url, output_path)
            except Exception as exc:  # noqa: BLE001
                print(f"[WARN] Failed to capture official thumbnail for {entry['name']}: {exc}")
                entry["official_thumb_path"] = None
                entry["thumb_source"] = "svg" if entry.get("path") else "none"
                missing += 1
                continue

            entry["official_thumb_path"] = str(output_path)
            entry["thumb_source"] = "svg" if entry.get("path") else "official"
            captured += 1

        browser.close()

    save_manifest(manifest)
    print(f"Official thumbnails generated: {captured}; missing: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

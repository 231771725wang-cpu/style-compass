# English · [中文](README.md)

<div align="center">
  <h1>Style Compass</h1>
  <p><em>"Browse directions first. Decide with confidence. Hand off a style recommendation that can actually be built."</em></p>
  <p>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5b5b5b"></a>
    <img alt="Install: Local Git" src="https://img.shields.io/badge/Install-Local_Git-111111">
    <img alt="Entry: Style Gallery" src="https://img.shields.io/badge/Entry-Style_Gallery-1f6feb">
    <img alt="Chinese-first" src="https://img.shields.io/badge/Language-Chinese_first-0f766e">
    <a href="https://github.com/VoltAgent/awesome-design-md"><img alt="Built on awesome-design-md" src="https://img.shields.io/badge/Built_on-awesome--design--md-7a3cff"></a>
  </p>
</div>

> "Do not start redesigning blind. Build the reference frame first, then narrow the field to the one to three directions worth pursuing."

**Style Compass** turns “help me choose a UI style” into a workflow you can browse, compare, filter, and hand off. Instead of forcing an immediate choice between Apple, Stripe, Linear, Nike, Vercel, and similar directions, it starts with a gallery so you can see the landscape first and only then ask the skill for a buildable recommendation.

This repository builds on the public style references from [getdesign.md](https://getdesign.md) and [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), then adds a Chinese-first entry, a local style gallery, thumbnail audit corrections, and a recommendation plus handoff workflow for Codex. It is not just a card collection; it is a release-grade front door for direction-finding.

If you are still wavering between Apple, Stripe, Linear, Nike, Vercel, and adjacent routes, open the gallery before you touch your current UI.

**Open the gallery first:** [Style Gallery](风格总览（Style Gallery）.html)  
**Install into Codex:** `git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass`  
**Upstream sources:** [getdesign.md](https://getdesign.md) / [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## Preview

![Style Gallery GitHub Preview](assets/gallery/previews/style-gallery-github-preview.png)

## Install

```bash
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

If you already installed an earlier version:

```bash
git -C ~/.codex/skills/style-compass pull
```

After installation, start here:

- [Style Gallery](风格总览（Style Gallery）.html)

## What You Get

- 68 styles to browse side by side
- Global hot list and category hot lists
- Chinese-first browsing with an English toggle
- Search, category, and layout filters
- Direct links to official preview pages
- Follow-up drafts for `DESIGN.md` or `UI-REFACTOR.md`

## Hot List

![Live Hot List](assets/gallery/previews/style-gallery-live-hot.png)

This screenshot comes directly from the current hot-list area of the gallery and helps you inspect the most-referenced directions first.

## Category Favorites

![Live Category Favorites](assets/gallery/previews/style-gallery-live-category.png)

The gallery is not just one ranking. It also lets you compare adjacent styles inside the same cluster instead of forcing a choice across unrelated visual languages.

## Suggested Flow

1. Open the Style Gallery and skim the hot list plus category favorites.
2. Narrow the field to one to three candidate directions.
3. Ask Style Compass for a structured recommendation with fit, risk, and handoff output.
4. Continue into `DESIGN.md` or `UI-REFACTOR.md`, then pass that to an implementation-focused skill.

## Who It Helps

- Anyone who wants to inspect direction before picking a style
- Teams wavering between Apple / Stripe / Linear / Nike / Vercel references
- Existing projects that need a UI upgrade without jumping straight into implementation
- People who want to establish a reference frame before handing work to frontend execution

## Repo Entrypoints

- Gallery entry: [`风格总览（Style Gallery）.html`](风格总览（Style Gallery）.html)
- Gallery folder: [`风格总览（Style Gallery）/`](风格总览（Style Gallery）/)
- Built gallery page: [`assets/gallery/style-gallery.html`](assets/gallery/style-gallery.html)
- Chinese homepage: [`README.md`](README.md)
- Skill spec: [`SKILL.md`](SKILL.md)
- Gallery build script: [`scripts/build_style_gallery.py`](scripts/build_style_gallery.py)
- GitHub preview builder: [`scripts/build_github_preview.py`](scripts/build_github_preview.py)

## Disclaimer

This repository is built on public style references for direction-finding, recommendation, and handoff. It does not imply official affiliation with the referenced brands or websites.

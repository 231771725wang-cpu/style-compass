# [English](#english) · [中文](#chinese)

<a id="english"></a>

<div align="center">
  <h1>Style Compass</h1>
  <p><em>"Browse first. Choose with conviction. Hand off a direction that can actually be built."</em></p>
  <p>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5b5b5b"></a>
    <img alt="Install: Local Git" src="https://img.shields.io/badge/Install-Local_Git-2f2f2f">
    <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111111">
    <img alt="Bilingual README" src="https://img.shields.io/badge/README-Bilingual-1f6feb">
    <a href="https://github.com/VoltAgent/awesome-design-md"><img alt="Built on awesome-design-md" src="https://img.shields.io/badge/Built_on-awesome--design--md-7a3cff"></a>
  </p>
</div>

> **Style Compass** turns "help me pick a UI style" into a usable workflow: browse references, narrow to 1-3 directions, then hand off a recommendation that can be implemented.

Built on the public style references from [getdesign.md](https://getdesign.md) and [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), this repo adds a local gallery, Chinese-first entrypoints, thumbnail audits, and a recommendation workflow for Codex.

If you are still deciding between Apple, Stripe, Linear, Nike, Vercel, or other directions, this is the entrypoint before you start redesigning screens or writing handoff docs.

## Preview

![Style Compass GitHub Preview](assets/gallery/previews/style-gallery-github-preview.png)

## Install

Clone this repository directly into your Codex global skills directory:

```bash
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

Update an existing local copy:

```bash
git -C ~/.codex/skills/style-compass pull --ff-only
```

If the directory already exists and you want a clean reinstall:

```bash
mv ~/.codex/skills/style-compass ~/.codex/skills/style-compass.bak
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

Use it from the Codex global skill library at `~/.codex/skills`.

## What You Get

- A browsable local style gallery with `68` references
- Global favorites and category-specific hot lists
- Chinese-first browsing with English toggle
- Search, category filters, and layout filters
- Direct links to official preview pages
- Style recommendation output that can continue into `DESIGN.md` or `UI-REFACTOR.md`

## How It Works

1. Start from the local gallery instead of guessing blindly.
2. Build a baseline from the hot list, then compare within a category.
3. Narrow down to `1-3` candidates using search and layout/category filters.
4. Run Style Compass against your project context, screenshots, or repo clues.
5. Turn the selected direction into a handoff draft that an implementation skill can use.

## Sections

[Preview](#preview) · [Install](#install) · [What You Get](#what-you-get) · [How It Works](#how-it-works) · [Gallery Files](#gallery-files) · [Upstream Credit](#upstream-credit)

## Gallery Files

- Main entry: [`风格总览（Style Gallery）.html`](风格总览（Style%20Gallery）.html)
- Folder entry: [`风格总览（Style Gallery）/`](风格总览（Style%20Gallery）/)
- Built gallery page: [`assets/gallery/style-gallery.html`](assets/gallery/style-gallery.html)
- Skill spec: [`SKILL.md`](SKILL.md)

## Additional Preview

### Live Hot List

![Style Gallery Live Hot List](assets/gallery/previews/style-gallery-live-hot.png)

The top row should match the real gallery experience, including Apple, Stripe, Linear, and Vercel.

### Live Category Favorites

![Style Gallery Live Category Favorites](assets/gallery/previews/style-gallery-live-category.png)

This is where the gallery shifts from a single ranking into cluster-based comparison.

## Upstream Credit

- Original project site: [getdesign.md](https://getdesign.md)
- Upstream repository: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- This repository adds:
  - local gallery entrypoints
  - Chinese-first navigation
  - thumbnail audit and correction workflow
  - recommendation and handoff flow for Codex

---

<a id="chinese"></a>

<div align="center">
  <h1>风格罗盘</h1>
  <p><em>“先看方向，再做决定，再交付一份真的能落地的风格建议。”</em></p>
  <p>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5b5b5b"></a>
    <img alt="安装方式：本地 Git" src="https://img.shields.io/badge/安装方式-Local_Git-2f2f2f">
    <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111111">
    <img alt="双语 README" src="https://img.shields.io/badge/README-双语-1f6feb">
    <a href="https://github.com/VoltAgent/awesome-design-md"><img alt="基于 awesome-design-md" src="https://img.shields.io/badge/基于-awesome--design--md-7a3cff"></a>
  </p>
</div>

> **风格罗盘（style-compass）** 不是单纯给你一堆风格卡，而是把“帮我挑 UI 风格”这件事做成一个可浏览、可比较、可交接的工作流。

这个仓库基于 [getdesign.md](https://getdesign.md) 与 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的公开风格资料，补上了本地总览页、中文入口、缩略图审计，以及适合 Codex 使用的推荐与 handoff 流程。

如果你还在 Apple、Stripe、Linear、Nike、Vercel 这些路线之间摇摆，正确顺序不是直接开改，而是先用它建立参照，再收敛方向。

## 效果

![风格罗盘 GitHub 预览](assets/gallery/previews/style-gallery-github-preview.png)

## 安装

直接把仓库 clone 到 Codex 全局技能目录：

```bash
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

已有本地副本时，更新方式：

```bash
git -C ~/.codex/skills/style-compass pull --ff-only
```

如果目录已存在、想重新装一份干净版本：

```bash
mv ~/.codex/skills/style-compass ~/.codex/skills/style-compass.bak
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

默认使用场景是 Codex 全局技能库：`~/.codex/skills`

## 你会得到什么

- 一个可浏览的本地风格总览，当前含 `68` 个风格参考
- 热门总榜 + 分类热门，两种进入方式
- 中文优先浏览，并可切换英文
- 名称搜索、分类筛选、布局筛选
- 每张卡都能直达官方预览页
- 收敛完方向后，可继续产出 `DESIGN.md` 或 `UI-REFACTOR.md`

## 核心工作方式

1. 先从总览页建立参照物，而不是盲猜。
2. 先看热门总榜，再进入同类分类横向比较。
3. 用搜索、分类和布局筛选，把候选收敛到 `1-3` 个。
4. 再结合项目上下文、页面截图或仓库线索运行风格推荐。
5. 最后把选中的方向变成可交接给实现技能的 handoff 草稿。

## 快速导航

[效果](#效果) · [安装](#安装) · [你会得到什么](#你会得到什么) · [核心工作方式](#核心工作方式) · [总览入口](#总览入口) · [上游来源](#上游来源)

## 总览入口

- 主入口：[`风格总览（Style Gallery）.html`](风格总览（Style%20Gallery）.html)
- 文件夹入口：[`风格总览（Style Gallery）/`](风格总览（Style%20Gallery）/)
- 实际构建页：[`assets/gallery/style-gallery.html`](assets/gallery/style-gallery.html)
- 技能规范：[`SKILL.md`](SKILL.md)

## 补充预览

### 热门总榜实时截图

![风格总览热门总榜](assets/gallery/previews/style-gallery-live-hot.png)

这里看到的第一排卡片，应该和你本地打开总览时看到的 Apple、Stripe、Linear、Vercel 保持一致。

### 分类热门实时截图

![风格总览分类热门](assets/gallery/previews/style-gallery-live-category.png)

这一段负责把“总榜参照”变成“同类比较”，适合继续缩小风格范围。

## 上游来源

- 原项目站点：[getdesign.md](https://getdesign.md)
- 上游仓库：[VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- 当前仓库额外补上的部分：
  - 本地风格总览入口
  - 中文优先导航
  - 缩略图真实性审计与修正
  - 面向 Codex 的推荐与交接流程

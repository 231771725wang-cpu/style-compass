# [English](README.en.md) · 中文

<div align="center">
  <h1>风格罗盘</h1>
  <p><em>“先看方向，再做决定，再交付一份真的能落地的风格建议。”</em></p>
  <p>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5b5b5b"></a>
    <img alt="安装方式：Local Git" src="https://img.shields.io/badge/Install-Local_Git-111111">
    <img alt="入口：风格总览" src="https://img.shields.io/badge/Entry-Style_Gallery-1f6feb">
    <img alt="中文优先" src="https://img.shields.io/badge/Language-中文优先-0f766e">
    <a href="https://github.com/VoltAgent/awesome-design-md"><img alt="基于 awesome-design-md" src="https://img.shields.io/badge/Built_on-awesome--design--md-7a3cff"></a>
  </p>
</div>

> “不要直接开改。先把参照系看清，再把方向收窄到值得做的那 1 到 3 个。”

**风格罗盘（style-compass）** 把“帮我挑 UI 风格”从一句模糊需求，变成一套可以浏览、比较、筛选、再继续交接实现的工作流。你不是先被迫选 Apple、Stripe、Linear、Nike、Vercel 里的某一个，而是先进入总览，把方向看懂，再让 skill 给出真正能落地的推荐。

这个仓库基于 [getdesign.md](https://getdesign.md) 与 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的公开风格资料，补上了中文优先入口、本地风格总览、缩略图校准审计，以及适合 Codex 使用的推荐与 handoff 流程。它不是单纯的风格卡收藏夹，而是一个“先逛方向，再收敛决策”的发布级入口。

如果你正在苹果、Stripe、Linear、Nike、Vercel 这些路线之间摇摆，先打开总览页，而不是先动手改现有界面。

**稳定网页版预览：** [https://231771725wang-cpu.github.io/style-compass/](https://231771725wang-cpu.github.io/style-compass/)  
**安装到 Codex：** `git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass`  
**上游项目：** [getdesign.md](https://getdesign.md) / [awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## 预览

![风格总览（Style Gallery）GitHub 预览](assets/gallery/previews/style-gallery-github-preview.png)

## 安装

```bash
git clone https://github.com/231771725wang-cpu/style-compass.git ~/.codex/skills/style-compass
```

如果已经装过旧版本：

```bash
git -C ~/.codex/skills/style-compass pull
```

安装后优先从这个入口开始：

- [风格总览（Style Gallery）.html](风格总览（Style%20Gallery）.html)

## 你会得到什么

- 68 个可横向浏览的风格方向
- 热门总榜与分类热门榜
- 中文优先浏览，可切换英文
- 搜索、分类和布局筛选
- 每张卡默认打开本地预览，官方预览链接只作为备用入口
- 风格收敛后继续输出 `DESIGN.md` 或 `UI-REFACTOR.md`

## 热门总览

![热门总榜实时截图](assets/gallery/previews/style-gallery-live-hot.png)

这张图直接来自当前总览页的热门总榜区域，用来帮助你先看最常被拿来做参照的方向，再决定要深入哪一组。

## 分类热门

![分类热门实时截图](assets/gallery/previews/style-gallery-live-category.png)

总览页不是只有一个总榜。你也可以按赛道继续横向看相近风格，而不是在完全不同的视觉路线里硬选。

## 推荐使用顺序

1. 先打开“风格总览（Style Gallery）”，快速逛热门总榜和分类热门。
2. 从总览里收敛出 1 到 3 个候选方向。
3. 再让风格罗盘（style-compass）正式推荐，并输出理由、风险和 handoff 草稿。
4. 选定方向后，继续生成 `DESIGN.md` 或 `UI-REFACTOR.md`，再交给实现型 skill 落地。

## 适合谁

- 还没定 UI 风格，想先看方向再决定的人
- 在 Apple / Stripe / Linear / Nike / Vercel 等路线之间犹豫的人
- 已有项目想升级 UI，但不想直接跳进实现的人
- 希望先建立参照，再交接给前端实现的人

## 仓库入口

> GitHub 会把 `.html` 文件当源码展示，不会直接渲染成交互网页。请使用上面的 GitHub Pages 预览，或先 clone / 下载仓库后在本地浏览器打开入口文件。卡片默认使用本地预览，不依赖 `getdesign.md`；官方预览链接只作为备用入口保留。

- 稳定网页版：[`https://231771725wang-cpu.github.io/style-compass/`](https://231771725wang-cpu.github.io/style-compass/)
- 总览页入口：[`风格总览（Style Gallery）.html`](风格总览（Style%20Gallery）.html)
- 总览文件夹：[`风格总览（Style Gallery）/`](风格总览（Style%20Gallery）/)
- 实际构建页：[`assets/gallery/style-gallery.html`](assets/gallery/style-gallery.html)
- 英文说明：[`README.en.md`](README.en.md)
- Skill 规范：[`SKILL.md`](SKILL.md)
- 总览页构建脚本：[`scripts/build_style_gallery.py`](scripts/build_style_gallery.py)
- GitHub 预览图生成脚本：[`scripts/build_github_preview.py`](scripts/build_github_preview.py)

## 免责声明

本仓库基于公开风格资料构建，用于建立视觉参照、推荐方向与交接文档，不代表这些品牌或网站与本项目存在官方合作关系。

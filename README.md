# [English](README.en.md) · 中文

<div align="center">
  <h1>风格罗盘</h1>
  <p><em>“先浏览一下。坚定地选择。交出一个真正能建造的方向。”</em></p>
  <p>
    <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-5b5b5b"></a>
    <img alt="安装方式：本地 Git" src="https://img.shields.io/badge/安装方式-Local_Git-2f2f2f">
    <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111111">
    <img alt="README 双语" src="https://img.shields.io/badge/README-双语-1f6feb">
    <a href="https://github.com/VoltAgent/awesome-design-md"><img alt="基于 awesome-design-md" src="https://img.shields.io/badge/基于-awesome--design--md-7a3cff"></a>
  </p>
</div>

> **风格罗盘（style-compass）** 不是单纯给你一堆风格卡，而是把“帮我挑 UI 风格”这件事做成一个可浏览、可比较、可交接的工作流。

这个仓库基于 [getdesign.md](https://getdesign.md) 与 [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 的公开风格资料，补上了本地总览页、中文入口、缩略图审计，以及适合 Codex 使用的推荐与 handoff 流程。

如果你还在 Apple、Stripe、Linear、Nike、Vercel 这些路线之间摇摆，正确顺序不是直接开改，而是先用它建立参照，再收敛方向。

![风格总览（Style Gallery）GitHub 预览](assets/gallery/previews/style-gallery-github-preview.png)

**先打开总览：** [风格总览（Style Gallery）](风格总览（Style Gallery）.html)  
**再看 skill 说明：** [SKILL.md](SKILL.md)

**原项目地址：** [getdesign.md](https://getdesign.md)  
**上游仓库：** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

## 先看总览

如果你是第一次接触这个 skill，或者你现在只知道“想要更高级一点 / 更像 Apple 一点 / 更像 Linear 一点”，先打开总览页最省时间。

- 本地打开：优先打开 `风格总览（Style Gallery）.html`
- 文件夹入口：也可以直接进入 `风格总览（Style Gallery）/`
- 在线发布：将 `assets/gallery/style-gallery.html` 托管到 GitHub Pages、Vercel 或任意静态托管，即可得到在线入口
- GitHub 内预览：先看上面的 hero 截图，再决定要不要本地打开完整交互页

## 你会得到什么

- 68 个风格可横向浏览
- 热门总榜与分类热门榜
- 中文默认浏览，并可一键切换 English
- 搜索、分类、布局筛选
- 每张卡可直达官方预览页
- 风格选定后可继续生成 `DESIGN.md` 或 `UI-REFACTOR.md`

## 展示

### 1. GitHub 首屏预览

![GitHub Hero Preview](assets/gallery/previews/style-gallery-github-preview.png)

这张图适合放 README 首屏、仓库介绍页和后续社交分享物料。  
图内主视觉已经切到“当前总览页实时截图”，不再使用旧版示意素材，并继续保留原项目地址说明。

### 2. 热门总榜实时截图

![Style Gallery Live Hot List](assets/gallery/previews/style-gallery-live-hot.png)

这张图直接来自当前总览页的热门总榜区域，第一排卡片应与本地实际浏览时看到的 Apple / Stripe / Linear / Vercel 保持一致。

### 3. 分类热门实时截图

![Style Gallery Live Category Favorites](assets/gallery/previews/style-gallery-live-category.png)

这张图来自当前总览页的分类热门区域，用来说明总览页不只是单一排行榜，而是可继续在同类风格里横向比较。

## 在线预览方式

- 本地体验：直接打开 `风格总览（Style Gallery）.html`
- GitHub Pages：把 `assets/gallery/style-gallery.html` 作为静态页发布
- Vercel：把 `assets/gallery/` 目录当静态站点托管

如果你后面补上真实在线链接，建议把它直接放到 README 顶部 CTA 下方。

## 推荐的新手路径

1. 先打开“风格总览（Style Gallery）”，快速逛热门总榜和分类热门。
2. 从总览里收敛出 1 到 3 个候选风格，再让风格罗盘（style-compass）正式推荐。
3. 选定风格后，继续生成 `DESIGN.md` 或 `UI-REFACTOR.md`，再交给实现型 skill 落地。

## 适合谁先用

- 还没定 UI 风格，想先横向看方向的人
- 在 Apple / Stripe / Linear / Nike / Vercel 等风格之间犹豫的人
- 已有项目想升级 UI，但不想直接跳进实现的人
- 希望先定方向，再把结果交接给前端实现的人

## 核心输出

- 3 张风格卡：最推荐、次推荐、对照项
- 风格适配理由、风险提示、官方预览链接
- `DESIGN.md` 初稿
- `UI-REFACTOR.md` 初稿
- 结构化 handoff prompt

## 仓库入口

- 总览页入口：[`风格总览（Style Gallery）.html`](风格总览（Style Gallery）.html)
- 总览文件夹：[`风格总览（Style Gallery）/`](风格总览（Style Gallery）/)
- 实际构建页：[`assets/gallery/style-gallery.html`](assets/gallery/style-gallery.html)
- Skill 规范：[`SKILL.md`](SKILL.md)
- GitHub 首页英文说明：[`README.en.md`](README.en.md)
- 总览页构建脚本：[`scripts/build_style_gallery.py`](scripts/build_style_gallery.py)
- GitHub 预览图生成脚本：[`scripts/build_github_preview.py`](scripts/build_github_preview.py)（会先从当前总览页实时截图，再生成封面图）

## 开源前红队测试

开源前的极限红队测试资产已经放进仓库：

- 用例集：[`evals/evals.json`](evals/evals.json)
- 评审清单：[`evals/red-team-checklist.md`](evals/red-team-checklist.md)
- 工作区脚手架：[`scripts/scaffold_red_team_workspace.py`](scripts/scaffold_red_team_workspace.py)

生成第一轮工作区：

```bash
python3 scripts/scaffold_red_team_workspace.py --iteration iteration-1
```

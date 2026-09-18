# W1 修复报告：3 页移动端横向溢出

> 实测环境：真实浏览器（Chromium headless），375px 视口，`document.documentElement.scrollWidth - clientWidth` 计算溢出。
> 修复手法沿用 W2 已验证配方（grid `minmax(0,1fr)` / flex `flex-wrap:wrap` / 横向滚动容器 `overflow-x:auto`）。

## 1. modular-scale-calculator

| 项 | 值 |
|:--|:--|
| 修复前溢出 | **+360px**（元凶 DIV 宽 719px） |
| 修复后实测 | **0px** |
| 根因 | `.main-grid` 网格轨道 `1fr`（= `minmax(auto,1fr)`）的 auto 最小值被内部 `.scale-text`（`white-space:nowrap` 长文本）的 min-content（719px）撑开，wrapper div 被拉到 719px |
| 改动 CSS | ① `.main-grid` 加 `grid-template-columns:minmax(0,1fr)`（配方2）；② `.scale-text` 加 `min-width:0`（配方3） |

自证：
```bash
node -e "const s=require('fs').readFileSync('modular-scale-calculator/index.html','utf8'); console.log('含grid minmax(0,1fr):', s.includes('grid-template-columns:minmax(0,1fr)'))"
# 含grid minmax(0,1fr): true
```

## 2. drum-beat-maker

| 项 | 值 |
|:--|:--|
| 修复前溢出 | **+246px**（音序器网格超视口） |
| 修复后实测 | **0px**（网格内部可横向滚动，clientWidth=301 / scrollWidth=516，页面 scrollWidth=375） |
| 根因 | `.sequencer-grid` 的 `repeat(16,1fr)` 轨道 auto 最小值被 `.seq-cell`（`min-height:28px` + `aspect-ratio:1`）撑到 28px/列，网格 min-content ≈ 579px |
| 改动 CSS | `.sequencer-grid` 改为 `repeat(16,minmax(24px,1fr))` + `overflow-x:auto;-webkit-overflow-scrolling:touch`（配方2+6），移动端横向滚动、桌面端正常铺满 |

自证：
```bash
node -e "const s=require('fs').readFileSync('drum-beat-maker/index.html','utf8'); console.log('含overflow-x:auto:', s.includes('overflow-x:auto'))"
# 含overflow-x:auto: true
```

## 3. eq-presets

| 项 | 值 |
|:--|:--|
| 修复前溢出 | **+161px**（元凶 DIV 宽 520px） |
| 修复后实测 | **0px** |
| 根因 | `.slider-group` flex 行 10 列 × `min-width:40px`（≈436px min-content）经 `.grid-2`、`.main-grid` 两级 `1fr` 轨道 auto 最小值逐级撑开至 520px |
| 改动 CSS | `.slider-group` 加 `flex-wrap:wrap`（配方3），min-content 降为单列 40px，滑块自动换行，全部可见 |

自证：
```bash
node -e "const s=require('fs').readFileSync('eq-presets/index.html','utf8'); console.log('含flex-wrap:wrap:', s.includes('flex-wrap:wrap'))"
# 含flex-wrap:wrap: true
```

## 合规确认
- 未改 URL、未动 GA `G-QVBQNJ3L5E` / Adsterra `pl31040516` / Bing `msvalidate.01`
- 未改可执行 JS 逻辑（仅改 CSS）
- 未删页面、未加 noindex、未 `git push`
- 未使用 `!important`
- 每页修复后立即单独 `git commit`（3 个独立提交）
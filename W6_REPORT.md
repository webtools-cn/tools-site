# W6 修复报告

> 实测环境：Chromium 无头浏览器，375×667 视口（控件高度项另测 1280×800 桌面视口）。
> 全部修复均为纯 CSS/class 改动，未改任何可执行 JS 逻辑，未动四 ID / URL / sitemap。

## A. 横向溢出（375px 视口）

| 页面 | 修复前 | 修复后 | 手法 |
|:--|--:|--:|:--|
| rgb-to-cmyk | +46px | 0px | `table.data` 加 `table-layout:fixed`；结果网格 `grid-template-columns:repeat(4,minmax(0,1fr))` |
| en/test-data-generator | +45px | 0px | `.add-field-row` 加 `flex-wrap:wrap` |
| scientific-notation-converter | +42px | 0px | `.faq-item table` 加 `table-layout:fixed` |
| full-screen-clock | +35px | 0px | 移动端 `.digital-time{font-size:3rem!important}` 覆盖 JS 内联字号 |
| mood-tracker | +17px | 0px | `#moodSelector{flex-wrap:wrap!important}` |

## B. 复选框尺寸（桌面端）

| 页面 | 修复前 | 修复后 |
|:--|:--|:--|
| file-checksum-calculator | 复选框 13/21/37/37px | 18/18/18/18px，label 热区 min-height:44px |

根因：`.form-group input` 的 `width:100%` 作用到复选框。修复：`#algoGroup input[type=checkbox]{width:18px;height:18px}` + `#algoGroup label{min-height:44px;display:flex;align-items:center;gap:8px}`。

## C. 控件高度（<36px → min-height:36px）

| 页面 | 修复前 | 修复后 | 涉及控件 |
|:--|:--|:--|:--|
| airport-code-lookup | 27 / 35px | 36px | `.copy-btn` / `.btn` |
| en/temperature-difference-calculator | 29 / 33px | 36px | `.copy-btn` / `.btn` / `.btn-preset` |
| ral-color-converter | 33px | 36px | `.chip` / `.copy-btn` |
| email-signature-generator | 33px | 36px | 输入框（`.form-group input` 等） |
| metronome-online | 29 / 35px | 36px | `.bpm-btn` / `select` |
| tax-bracket-calculator | 33px | 36px | `.copy-btn` |
| daily-journal | 34px | 36px | `.mood-btn` |
| random-word-generator | 27px | 36px | `.result-item .copy-btn` |

豁免项（未改）：纯图标小按钮（← → ✕）、range 滑块。

## 提交记录

```
fix(w6): rgb-to-cmyk 横向溢出 46px -> 0px
fix(w6): en/test-data-generator 横向溢出 45px -> 0px
fix(w6): scientific-notation-converter 横向溢出 42px -> 0px
fix(w6): full-screen-clock 横向溢出 35px -> 0px
fix(w6): mood-tracker 横向溢出 17px -> 0px
fix(w6): file-checksum-calculator 复选框 13/21/37/37px -> 18px
fix(w6): airport-code-lookup 控件高度 27/35px -> 36px
fix(w6): en/temperature-difference-calculator 控件高度 29/33px -> 36px
fix(w6): ral-color-converter 控件高度 33px -> 36px
fix(w6): email-signature-generator 输入框高度 33px -> 36px
fix(w6): metronome-online 控件高度 29/35px -> 36px
fix(w6): tax-bracket-calculator 控件高度 33px -> 36px
fix(w6): daily-journal 控件高度 34px -> 36px
fix(w6): random-word-generator 控件高度 27px -> 36px
```
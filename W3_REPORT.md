# W3 · P2 排版布局可用性修复报告

- 分支：`worker/w3`
- 日期：2026-09-18
- 范围：`_top40.txt` 中 40 个页面（CN + EN，共 79 个 HTML 文件）
- 方法：Node 静态检测 + Puppeteer/Chromium 真实浏览器实测（375px / 1440px）

## 验收结果

| 检查 | 结果 |
|:--|:--|
| `python3 scripts/validate_ids.py` | ✅ PASS 7551 页 |
| `grep -c '<loc>' sitemap.xml` | ✅ 7166（未变） |
| `git status --short \| wc -l` | ✅ 0（4 个 commit，未 push） |

## 修复方式

每页在 `<style>` 末尾追加统一 CSS 覆盖块（`/* W3 layout fixes */`），只改 CSS，未动任何 `<script>`、四 ID、canonical、title、h1、URL：

1. **触摸目标 ≥44px**：`button { min-height:44px; min-width:44px }`；文本类 `input/select/textarea { min-height:44px }`；`input[type=checkbox]/[type=radio] { width:44px; height:44px !important }`（覆盖页面更高优先级规则）。
2. **输入框字号 ≥16px**：`input, select, textarea { font-size:16px !important }`（防 iOS 自动缩放）。
3. **正文 ≥14px**：`label, p, li, .btn, .tab-btn, .preset-btn, .quick-btn, .copy-btn, .lang-switch, .nav-back, .badge, .footer*, .result-*, .hint, .toast, .stat-*, .sub, .value, .lbl, .cycle-count span` 等 → `14px !important`；内联 `font-size:.8rem/.75rem/.85rem` 的 div/span 一并覆盖。
4. **横向滚动修复**（4 页）：
   - `heat-index-calculator` EN：`.main-grid > * { min-width:0 }`
   - `graphing-calculator` CN：`.main-grid > * { min-width:0 }`
   - `paycheck-calculator` CN/EN：`.main-grid > * { min-width:0 }` + 结果网格移动端改 2 列
   - `cidr-calculator` EN：`.result-item .sub/.value { overflow-wrap:break-word }` + `.result-grid > * { min-width:0 }`
5. **首屏优化（尽力）**：移动端收紧 `.hero/.section/.header/.nav-back` 间距，使部分页面主按钮进入首屏。

## 40 页逐页结果

| # | 页面 | 发现的问题 | 修了什么 | 关键数值（前→后） |
|:--|:--|:--|:--|:--|
| 1 | business-days-calculator | 按钮/输入<44px；输入<16px；正文<14px；首屏按钮不可见 | 触摸/字号/输入字号 | tab-btn 37→44px；input 14.4→16px；lang 13.6→14px |
| 2 | sunrise-sunset-calculator | 输入<44px；输入<16px；label<14px | 触摸/字号 | input 38→44px；label 13.6→14px |
| 3 | tax-calculator | footer 13px | 字号 | footer 13→14px |
| 4 | business-day-calculator | 按钮/checkbox<44px；输入<16px；label<14px | 触摸/字号 | tab 36→44px；checkbox 13→44px |
| 5 | tax-refund-calculator | 输入/按钮<44px；输入<16px；btn<14px | 触摸/字号 | input 39→44px；btn 13.6→14px |
| 6 | bpm-tapper | 按钮<44px；输入<16px；正文<14px；首屏不可见 | 触摸/字号 | btn 38→44px |
| 7 | mouse-tester | 按钮<44px；key/log<14px；首屏不可见 | 触摸/字号 | btn 38→44px；key 12.8→14px |
| 8 | checksum-calculator | 复制按钮 23px；输入<16px；seo<14px；首屏不可见 | 触摸/字号 | 复制 23→44px |
| 9 | file-hash-checker | checkbox 16px；输入<16px；hint<14px；首屏不可见 | 触摸/字号 | checkbox 16→44px |
| 10 | battery-capacity-tester | tab/输入<44px；输入<16px；unit 12px；首屏不可见 | 触摸/字号 | tab 36→44px；unit 12→14px |
| 11 | reaction-test | 按钮<44px；stat-label<14px；首屏不可见 | 触摸/字号 | btn 37→44px |
| 12 | speed-test | 按钮 41px；result-unit 12.8px | 触摸/字号 | btn 41→44px |
| 13 | whats-my-ip | 按钮<44px；ip-label<14px；首屏不可见 | 触摸/字号 | retry 32→44px |
| 14 | pow-captcha | 按钮<44px；输入<16px；span 12px | 触摸/字号 | btn 38→44px |
| 15 | signature-generator | tab/checkbox<44px；输入<16px；label 12.8px；首屏不可见 | 触摸/字号 | checkbox 16→44px |
| 16 | heat-index-calculator | **横向滚动**；按钮 31px；输入<16px；结果<14px | 网格 min-width:0 + 触摸/字号 | sw 398→375px；btn 31→44px |
| 17 | mac-address-lookup | 按钮 34px；quick-chip 12.8px；首屏不可见 | 触摸/字号 | btn 34→44px |
| 18 | speaker-test | 按钮 39px；privacy-note 13.6px | 触摸/字号 | btn 39→44px |
| 19 | timesheet-calculator | 输入/按钮<44px；输入<16px；label 12px；首屏不可见 | 触摸/字号 | input 38→44px |
| 20 | midi-player | 按钮/select<44px；输入<16px；label<14px；首屏不可见 | 触摸/字号 | btn 38→44px |
| 21 | graphing-calculator | **横向滚动**；函数按钮 25px；输入<16px；coord 12.8px | 网格 min-width:0 + 触摸/字号 | sw 402→375px；函数按钮 25→44px |
| 22 | paycheck-calculator | **横向滚动**；tab/输入<44px；输入<16px；lbl 12.48px；首屏不可见 | 网格 min-width:0 + 结果网格2列 + 触摸/字号 | sw 566→375px |
| 23 | rhyme-finder | 按钮 43px/checkbox 16px；输入<16px；updated 12.8px | 触摸/字号 | checkbox 16→44px |
| 24 | online-compass | 按钮<44px；compass-mark 13px；首屏不可见 | 触摸/字号 | btn 38→44px |
| 25 | log-viewer | 按钮 37px；输入 13px；stats 13px | 触摸/字号 | btn 37→44px；input 13→16px |
| 26 | character-unicode-finder | footer 13px | 字号 | footer 13→14px |
| 27 | atbash-cipher | checkbox 13px/按钮 41px；输入<16px；faq 13.6px | 触摸/字号 | checkbox 13→44px |
| 28 | en/mouse-tester | 按钮 33px；key 12.8px；首屏不可见 | 触摸/字号 | btn 33→44px |
| 29 | time-duration-calc | footer 13px | 字号 | footer 13→14px |
| 30 | monte-carlo-simulator | 输入 39px；输入<16px；hint 12.8px；首屏不可见 | 触摸/字号 | input 39→44px |
| 31 | cursive-text-generator | 按钮<44px；输入<16px；font-name 12.8px；首屏不可见(EN) | 触摸/字号 | btn-copy 33→44px |
| 32 | unicode-decoder | mode-btn 37px；mode-btn 13px；首屏不可见 | 触摸/字号 | mode-btn 37→44px |
| 33 | binary-calculator | op-btn 38px；输入<16px；span 12px | 触摸/字号 | op-btn 38→44px |
| 34 | trig-calculator | checkbox 13px/按钮 41px；输入<16px；updated 12.8px | 触摸/字号 | checkbox 13→44px |
| 35 | electricity-cost-calculator | footer 13px | 字号 | footer 13→14px |
| 36 | sleep-calculator | select/按钮<44px；cycle span 13.6px；首屏不可见 | 触摸/字号 | select 41→44px |
| 37 | kpi-calculator | 输入 38px；输入<16px；footer 12.8px；首屏不可见 | 触摸/字号 | input 38→44px |
| 38 | gpu-benchmark | 按钮 43px；输入<16px；nav-back 13.6px | 触摸/字号 | btn 43→44px |
| 39 | cidr-calculator | **横向滚动(EN)**；按钮 42px；输入 15px；preset-tag 12px | 结果文本换行 + 触摸/字号 | sw 380→375px |
| 40 | emoji-combiner | tab 32px；label 12.8px；首屏不可见 | 触摸/字号 | tab 32→44px |

## 已知限制（未修，报告标注）

1. **首屏主按钮不可见（约 20 页）**：主按钮位于 600–1700px 处，因页面结构为「header → hero → tab → 输入区 → 按钮」，属结构性布局。已通过移动端收紧 hero/section 间距尽力优化，但未做 HTML 结构调整（避免破坏 CN/EN 一致性与脚本依赖）。涉及：business-days、bpm-tapper、mouse-tester、checksum、file-hash、battery、reaction、whats-my-ip、signature、mac-address、timesheet、midi-player、paycheck、online-compass、monte-carlo、unicode-decoder、sleep、kpi、emoji、cursive(EN)。
2. **`input[type=range]` 滑块**（heat-index、signature、emoji、midi-player、pow-captcha、mouse-tester）：轨道高度 6–34px，未强制 44px（滑块交互目标是 thumb，强制轨道 44px 会破坏滑块 UI）。已按例外处理。
3. **sitemap.xml**：pre-commit 钩子自动更新了 78 条 `lastmod`（仓库既有行为），`<loc>` 数量保持 7166 不变。

## 提交记录（未 push）

```
7dca14d625 style(w3): 修复前10页移动端排版可用性(触摸目标44px/字号≥14px/输入≥16px)
5b4140452e style(w3): 修复第11-20页移动端排版可用性(触摸目标44px/字号≥14px/输入≥16px)
445a740288 style(w3): 修复第21-29页移动端排版可用性(触摸目标44px/字号≥14px/输入≥16px)
ad60955aa1 style(w3): 修复第30-40页移动端排版可用性(触摸目标44px/字号≥14px/输入≥16px)
```
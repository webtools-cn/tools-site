# W1 报告：3 页移动端横向溢出修复

> 验证方式：`google-chrome-stable` headless + puppeteer，375px 视口实测（与任务真机口径一致）。
> 修复前 3 页均复现任务描述的溢出量与元凶宽度；修复后 375px 全部归零。

## 1. whois-domain-lookup（+124px → 0px）

- **元凶元素**：`SECTION.related-tools` 宽 483px（实测复现）。根因是页面 HTML 中 `main-grid` 的 `<div>` 未闭合，导致 `related-tools` 段落在 `grid-template-columns:1fr 300px` 的网格项内；网格项默认 `min-width:auto`，无法收缩到内容宽度以下，被撑到 483px。
- **改了什么**（纯 CSS，`index.html` 内联 `<style>`）：
  1. `.main-grid` 改为 `grid-template-columns:minmax(0,1fr) 300px`，移动端媒体查询改为 `minmax(0,1fr)` —— 网格项可收缩（配方 1）。
  2. `.related-tools{max-width:100%}` + `.related-tools a` 加 `overflow-wrap:break-word;word-break:break-word`（配方 4）。
  3. 修复后实测仍残留 +82px，进一步定位到 FAQ `<p>` 中 `.com、.net、.org、.info、.io、.co、.me、.cn、.cc、.tv、.biz` 这类「拉丁词 + 顿号 + 拉丁词」串在 Chrome 中不可断行（最小化用例已复现），故给 `.faq-item p` 加 `overflow-wrap:break-word;word-break:break-word`（配方 2 同款手法）。
- **预期溢出归零**：✅ 375px 实测 `scrollWidth=375`，溢出 0px。

## 2. vin-decoder（+82px → 0px）

- **元凶元素**：无 class 的 `DIV` 宽 441px（实测复现）。根因是 `.main-grid`（单列 grid）的网格项 `min-width:auto`，其内容最小宽度被结果表格撑到 441px：表格首列 `white-space:nowrap;width:140px` 的「WMI（世界制造商识别）」约 183px + 第二列 VIN「1HGCM82633A004352」约 174px = 357px，逐层加 padding 后网格项达 441px。
- **改了什么**（纯 CSS）：
  1. `.result-table` 加 `table-layout:fixed`（配方 2），表格不再被内容撑破。
  2. `.result-table td` 加 `overflow-wrap:break-word;word-break:break-word`（配方 2）。
  3. `@media(max-width:640px)` 内加 `.result-table td:first-child{white-space:normal}`，移动端允许首列标签换行。
  4. `.main-grid` 加 `grid-template-columns:minmax(0,1fr)`（配方 1），网格项可收缩。
- **预期溢出归零**：✅ 375px 实测 `scrollWidth=375`，溢出 0px。

## 3. regex-crossword（+75px → 0px）

- **元凶元素**：`DIV.section` 宽 434px（实测复现）。根因是 JS 生成的列头容器带内联 `margin-left:calc(48px * 3 + 14px + 8px)` = 166px（原 JS 对齐公式偏大，属既有缺陷），使列头最小宽度达 350px，逐层撑大游戏区 → 网格项 → 434px。
- **改了什么**（纯 CSS，未动 JS 逻辑）：
  1. `.main-grid` 加 `grid-template-columns:minmax(0,1fr)`（配方 1），网格项可收缩。
  2. 新增 `#colHeaders{overflow-x:auto;max-width:100%}`（配方 4，兜底防撑破）。
  3. 新增 `#colHeaders>div{margin-left:60px!important}`，把列头偏移从错误的 166px 修正为与行标签对齐的 60px（入门难度 3×3 实测行标签 52px + 间距 8px），既消除溢出又修正对齐。
- **预期溢出归零**：✅ 375px 实测 `scrollWidth=375`，溢出 0px；切换「中级」4×4 关卡同样 0px。

## 自测说明

- 无 puppeteer 依赖问题：本机有 `google-chrome-stable` + `node` + `puppeteer`，用 `_verify.js`（临时目录）在 375px 视口逐页测量 `document.documentElement.scrollWidth`。
- 未引入任何 ≥400px 的固定像素宽度（`grep -nE "width:[4-9][0-9]{2}px|min-width:[4-9][0-9]{2}px"` 仅命中既有 `max-width:900px`、`width:140px`、`width:36px` 等）。

## 红线核对

- ✅ 未改 URL、未动 GA `G-QVBQNJ3L5E` / Adsterra `pl31040516` / Bing `msvalidate.01`
- ✅ 未改可执行 JS 逻辑（regex-crossword 仅用 CSS `!important` 覆盖内联样式）
- ✅ 未删页面、未加 noindex
- ✅ 未 push（仅本地 commit，等待独立验收）
- ✅ 未改 `related-tools.json`

## 提交记录

```
4729ca60e2 fix(whois-domain-lookup): 修复移动端横向溢出(related-tools 483px)
a4f5d45879 fix(whois-domain-lookup): FAQ文本长串不换行导致残留溢出
736e4f8d25 fix(vin-decoder): 修复移动端横向溢出(无class DIV 441px)
e1c013ee20 fix(regex-crossword): 修复移动端横向溢出(div.section 434px)
```

## 附注（超出本次任务范围，未改动）

- `regex-crossword` 在 320px 视口仍有 +17px：游戏区 div 内联 `min-width:300px` 在 320px 下超出容器（375px 任务口径内无此问题）。
- `en/vin-decoder` 在 375px 有 +80px 溢出（英文版，不在本次 3 页清单内，未改动）。
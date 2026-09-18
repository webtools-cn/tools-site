# W7 功能正确性复核报告（12 页）

日期：2026-09-18
范围：12 个高展现工具页，逐页独立对拍「输入→输出」。
结论：**11 页无问题，1 页发现真 bug 并已修复提交**（commit `7a9d0165b4`）。

## 逐页结论

| # | 页面 | 结论 | 对拍样例 |
|---|------|------|----------|
| 1 | rgb-to-cmyk | PAGE 已验，无问题 | 255,0,0 → C0/M100/Y100/K0；0,0,0 → 0/0/0/100（含纯黑特判） |
| 2 | gray-code-converter | PAGE 已验，无问题 | 十进制5→格雷码111(=7)；4→110(=6)；1011↔1110 双向正确 |
| 3 | ascii-to-hex | PAGE 已验，无问题 | "Hi" → "48 69"；hex→ascii 偶数长度校验正确 |
| 4 | hex-calculator | **已修复**（见下） | 0xFF+0x01 → 256（十进制正确，非溢出） |
| 5 | vat-calculator | PAGE 已验，无问题 | 不含税100、13% → 含税113、税额13；反向 113→100/13 正确 |
| 6 | cgpa-calculator | PAGE 已验，无问题 | Σ(绩点×学分)÷Σ学分 加权平均正确；4.0/5.0/百分制换算表边界正确 |
| 7 | dpi-calculator | PAGE 已验，无问题 | 1920×1080@24" → PPI=91.79，工具取整显示 92（正确取整，非错误） |
| 8 | modular-scale-calculator | PAGE 已验，无问题 | 16×1.25³=31.25px，px 显示取整为 31（rem/em 保留3位小数） |
| 9 | scientific-notation-converter | PAGE 已验，无问题 | 0.00042 → 4.2×10⁻⁴；10 的整数幂无浮点误差（log10 边界干净） |
| 10 | tax-bracket-calculator | PAGE 已验，无问题 | 上一轮修复仍正确；7 档速算扣除数边界全部自洽（36000/144000/300000/420000/660000/960000 处两档衔接一致）；月薪20000→税1590 |
| 11 | bpm-delay-time-calculator | PAGE 已验，无问题 | 120BPM：四分500ms、八分250ms、附点八分375ms、八分三连音166.67ms |
| 12 | metronome-online | PAGE 已验，无问题 | 120BPM → 60/120=0.5s/拍 = 2次/秒；Web Audio 前瞻调度（25ms 轮询、0.1s 预排），非 setInterval 直接计时 |

## 修复项（1 处）

**hex-calculator（中文版）位运算 32 位有符号溢出**

- 现象：对 ≥0x80000000 的十六进制数做 `&`/`|`/`^` 时，JS 位运算按 32 位有符号处理，结果被显示为负数。
- 修复前 → 修复后：
  - `0xFFFFFFFF & 0xFFFFFFFF`：`-1` → `FFFFFFFF`
  - `0xFFFFFFFF | 0x0F`：`-1` → `FFFFFFFF`
  - `0xFFFFFFFF ^ 0x0F`：`-10` → `FFFFFFF0`
- 修复方式：三个位运算分支结果加 `>>> 0` 转无符号 32 位（`hex-calculator/index.html:204-206`）。
- 英文版 `en/hex-calculator` 已自带 `>>>0`，无需改动。
- 加减乘除不受影响（JS 双精度，0xFF+0x01=256 正确）。

## 说明

- 未触碰任何红线项（GA/Adsterra/Bing/验证文件、URL、sitemap、清单外页面）。
- 未新增/遗留任何测试脚本文件（对拍均用 node 临时命令）。
- 提交：`7a9d0165b4 fix(hex-calculator): 位运算结果转无符号32位`
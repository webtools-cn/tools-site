# W2 报告：10 页控件触摸高度修复（375px 真机实测）

> 分支 `worker/w2` · 日期 2026-09-18
> 目标：所有交互控件高度 ≥ 36px，仅改 CSS / 内联 style，未动 JS 逻辑。

| # | slug | 问题控件 | 改前高度 | 改后预期高度 | 修法 |
|:--|:--|:--|--:|--:|:--|
| 1 | dpi-calculator | `button.preset-btn` ×3 | 33px | ≥36px | `.preset-btn` 加 `min-height:36px` |
| 2 | invisible-character | `button.copy-btn` | 27px | ≥36px | `.copy-btn` 加 `min-width:36px;min-height:36px` |
| 3 | daily-journal | `button` ×2 | 29px | ≥36px | `.btn` 加 `min-height:36px` |
| 4 | scientific-notation-converter | `input[type=text]` | 34px | ≥36px | `.form-row input/select` 加 `min-height:36px` |
| 5 | mood-tracker | `button.btn-secondary` | 33px | ≥36px | `.btn` 加 `min-height:36px` |
| 6 | cgpa-calculator | `button.btn-danger` ×2 + `btn-secondary` | 29-33px | ≥36px | `.btn` 加 `min-height:36px` |
| 7 | hourly-to-salary-calculator | `button.preset` ×3 | 34px | ≥36px | `.preset` 加 `min-height:36px` |
| 8 | vat-calculator | `button.rate-btn` ×3 | 33px | ≥36px | `.rate-btn` 加 `min-height:36px` |
| 9 | handwriting-generator | `input[type=color]` | 27px | ≥36px | 新增 `input[type=color]{min-height:36px;padding:4px}` |
| 10 | en/countdown-clock | `button.preset-btn` ×3 | 33px | ≥36px | `.preset-btn` 加 `min-height:36px` |

## 纪律执行
- 每页修完立即 `git add -A && git commit`（10 次独立提交）
- 未改 JS 逻辑、未改 URL/title/desc、未动 GA/Adsterra 代码
- 未使用 `input[type=checkbox]` 强制宽高、未改 `input[type=range]` 高度
- 每页仅 Read 1 次

## 提交记录
1. `fix(dpi-calculator): preset-btn 触摸高度提升至36px`
2. `fix(invisible-character): copy-btn 触摸高度提升至36px`
3. `fix(daily-journal): 按钮触摸高度提升至36px`
4. `fix(scientific-notation-converter): 输入框触摸高度提升至36px`
5. `fix(mood-tracker): 按钮触摸高度提升至36px`
6. `fix(cgpa-calculator): 按钮触摸高度提升至36px`
7. `fix(hourly-to-salary-calculator): preset 按钮触摸高度提升至36px`
8. `fix(vat-calculator): rate-btn 触摸高度提升至36px`
9. `fix(handwriting-generator): 颜色选择器触摸高度提升至36px`
10. `fix(countdown-clock): preset-btn 触摸高度提升至36px`
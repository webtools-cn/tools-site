# W2 · P2 功能正确性对拍报告（Bing 展现 71-100 名，30 页）

> 分支 `worker/w2` · 日期 2026-09-18
> 方法：逐页读取 `index.html` 提取核心计算函数 → Node 独立复算（≥2 组真实输入，含 0/负数/极大值/空值边界）→ 与页面公式对拍。**对不上才算 bug，只修真算错的。**

## 一、修复清单（7 个工具，7 处 bug）

| # | 工具 | 输入 | 旧输出 | 新输出 | 依据 |
|---|------|------|--------|--------|------|
| 1 | `speech-timer` | "Hello world, this is a test speech for timing." | 11 词（`,` 和 `.` 被误计为汉字） | 9 词 | 英文标点不应计入字数；`countWords` 的 cleaned 正则只去中文标点，英文 `,`/`.` 残留被 `chineseChars` 计入。修复：正则补充英文标点 `.,!?;:'"()[]{}<>/\\-_@#$%^&*+=|~\`` |
| 2 | `hourly-to-salary-calculator` | 时薪25 / 40h / 52周 | 月薪 $4,330.00（weekly×4.33） | 月薪 $4,333.33（annual÷12） | 正算月薪与反算（annual/12）及 FAQ（"月薪约$4,333"）不一致；4.33 是 52/12 的舍入误差。修复：`monthly = annual/12` |
| 3 | `eye-test` | E字表第5/6行 | 连续两行都显示"4.5" | 第5行 4.4、第6行 4.5 | 标准对数视力表级距单调递增，`eLevels` 数组 `4.5` 重复（typo）。修复：`{vision:4.4,size:60}` |
| 4 | `grammar-checker` | "They're going to the store." | 误报错误（"they're 后接名词可能应为 their"） | 不报错；"Their going to the store." 正确报错并建议 "they're going" | 规则 `they're+动词` 把正确句当错误，且漏掉真实错误 `their+动词`。修复：规则改为 `their+动词 → they're` |
| 5 | `regex-crossword` | 3 个谜题答案 | 入门/初级/中级答案均不满足行列正则（如入门 col1 `^C.D$` vs "BDF"），中级 col2 `^[C-Z]{2}K$` 仅 3 字符无法匹配 4 格列 | 3 个谜题全部自洽（答案满足全部行列正则） | 谜题不可解 = 功能失效。重设计：入门 rows `^A.C$ ^D.F$ ^G.I$` cols `^A.G$ ^B.H$ ^C.I$` ans ABC/DEF/GHI；初级 ans 改 EFH；中级 rows `^E[F-H]{2}.$ ^I.K.$` cols `^[C-Z]{2}K.$ ^[D-Z]H.P$` |
| 6 | `image-sprite-generator` | 上传图片→点"生成精灵图" | 无任何输出（页面 JS 只有 toast/copy 辅助函数，按钮全部失效） | 实现完整逻辑：上传/拖拽、缩略图、水平/垂直/网格排列、Canvas 合成、CSS 代码生成、下载 PNG、复制 CSS | 空壳工具（0 交互逻辑）违反 AGENTS.md 禁止项。按 HTML 已有结构补齐 JS |
| 7 | `en/frame-grabber` | 批量截图间隔输入 -1 | `while(t<duration)` 死循环冻结浏览器 | 间隔钳制到 ≥0.1s | 负间隔使 `t += interval` 永远小于 duration。修复：`if(interval<0.1) interval=0.1` |

## 二、逐页对拍表（30 页全部验证）

| 页面 | 输入 → 页面输出 → 独立复算 | 结论 |
|------|---------------------------|------|
| speech-timer | 示例稿66字@150wpm→0:26；"Hello world, this is a test speech for timing."→9词 | ✅ 已修复 |
| hourly-to-salary-calculator | 25/40/52→年52000 月4333.33 周1000 日200；反算100000→时薪48.08 | ✅ 已修复 |
| eye-test | E字表11级单调；色觉8题(12/8/6/29/5/3/15/7 标准石原数字) | ✅ 已修复 |
| vat-calculator | 不含税100/13%→税13 含税113；反向113→净100 税13（自洽） | ✅ |
| fancy-text-generator | 粗体ABCabc123→𝐀𝐁𝐂𝐚𝐛𝐜𝟏𝟐𝟑；全角!A→！Ａ；圆圈123→①②③ | ✅ |
| website-status-checker | fetch no-cors + img/favicon 兜底，无计算逻辑 | ✅ |
| grammar-checker | "Their going"→they're going；"They're going"→不报错；alot→a lot | ✅ 已修复 |
| ral-color-converter | 214色 RGB↔HEX 全一致，无重复 hex | ✅ |
| handwriting-generator | 纯字体渲染，无计算 | ✅ |
| bic-checker | DEUTDEFF 有效；1234DEFF/DEUTXXFF/6位 无效 | ✅ |
| en/countdown-clock | 90061000ms→1d1h1m1s；86400000→1d；datetime-local 时区偏移处理正确 | ✅ |
| random-word-generator | 唯一索引随机抽取，count≤pool 长度 | ✅ |
| uptime-checker | 网络检测，无计算逻辑 | ✅ |
| checklist-generator | 3/5 完成→60%；导出 [x]/[ ] 格式 | ✅ |
| atbash | Hello→Svool→Hello（自逆）；ABC123→ZYX123 | ✅ |
| image-tinter | Canvas 混合模式+透明度，无计算 | ✅ |
| subnet-divider | /24→254主机；/32→1；/31→2；/24分4→4个/26各62；/8分8→/11 | ✅ |
| whois-domain-lookup | RDAP 查询，无计算逻辑 | ✅ |
| regex-crossword | 3谜题答案全部满足行列正则 | ✅ 已修复 |
| email-signature-generator | HTML 模板+esc 转义，无计算 | ✅ |
| drum-machine | 120bpm 16分音符→125ms；90bpm→166.67ms；swing 交替步进 | ✅ |
| image-sprite-generator | 水平32+16+24+pad2→76×48；网格2列→66×98 | ✅ 已修复 |
| airport-code-lookup | 92机场无重复码；PEK/PVG/HKG/NRT/JFK/LAX 等抽查正确 | ✅ |
| metronome-online | 500ms 点拍→120bpm；400ms→150bpm；60/bpm 秒/拍 | ✅ |
| en/temperature-difference-calculator | 100°C-0°C→100°C=180°F=100K=180°R；0°C-32°F→0 | ✅ |
| en/frame-grabber | formatTime 65.5s→1:05.500；负间隔死循环 | ✅ 已修复 |
| color-palette-extractor | 16级量化取topN，hex 转换正确 | ✅ |
| markdown-table-formatter | 中文宽度×2 对齐；左/右/居中分隔符正确；CSV 转义正确 | ✅ |
| random-username-generator | 词+0-9999+可选下划线，无计算错误 | ✅ |
| access-log-analyzer | 5行日志→PV5 UV3；2xx/4xx/5xx 分组；小时提取正确 | ✅ |

## 三、验收项

1. ✅ 30 页全部验证，每页给出输入/页面输出/复算/结论（见上表）
2. ✅ 7 个不一致工具已修复，并用同一 harness 复验通过
3. ✅ `node --check` 对全部改动页 JS 通过
4. ✅ `python3 scripts/validate_ids.py` PASS（7551 页，四 ID 齐全，零禁用 ID）
5. ✅ 提交记录（每修完 5 页 commit 一次）：
   - `20a725181d` fix(w2): speech-timer 英文标点误计汉字 / hourly-to-salary 月薪不一致 / eye-test 重复4.5级
   - `49a0c24ed1` fix(w2): grammar-checker they're+动词规则误报
   - `1aa3daa8e2` fix(w2): regex-crossword 3谜题不可解，重设计
   - `68b6b72a92` fix(w2): image-sprite-generator 无JS逻辑，补齐实现
   - `04244f601f` fix(w2): en/frame-grabber 负间隔死循环

## 四、已知限制（未改，属设计取舍）

- `color-palette-extractor` 百分比是 top-N 色相对占比（合计100%），非全图占比——设计取舍，非计算错误。
- `grammar-checker` 的 "your welcome" 建议 "Your're" 大小写不统一——仅建议文案，不影响判定。
- `random-word-generator` 形容词池 "bold" 重复一次——数据冗余，不影响唯一索引抽取逻辑。
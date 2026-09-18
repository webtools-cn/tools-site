# W4 第二轮：流量增长报告（Bing 展现 131-160 名，30 页）

> 分支：`worker/w4` ｜ 时间：2026-09-18 ｜ 范围：`_list.txt` 内 30 页（仅此 30 页）

## 一、改动总览

| 改动类型 | 数量 | 说明 |
|:--|:--|:--|
| title 优化 | 7 页 | 去除 CN 标题中的英文 `Free ToolBase` / 超宽标题（≤60 宽度） |
| meta description 重写 | 27 页 | 全部扩写至 120-155 字符，含核心词 + 行动理由 |
| related-tools.json 内链 | 30 页 | 替换/补齐真正相关内链（清除链接农场默认项） |
| 页面硬编码相关工具区 | 19 页 | 替换为真正相关的内链（原为无关链接农场） |
| GEO 内容（FAQ/定义/场景） | 5 页 | 补 3-5 条真实 FAQ、修正"什么是X"定义与使用场景 |
| EN 页检查 | 5 页 | 人工核对英文，无机翻痕迹，仅优化 title/description |

## 二、逐页改动明细

| 页面 | 改动 | 理由 | 影响 |
|:--|:--|:--|:--|
| resolution-calculator | description 扩写至 123 字符；内链替换为宽高比/PPI/分辨率模拟器/图片缩放 | 原 desc 仅 64 字符，缺行动理由；原内链为计时器/存款等无关项 | 提升 CTR 与相关性 |
| typing-test | description 扩写至 126 字符；内链替换为打字/键盘/竞速类 | 原 desc 60 字符过短；原内链无关 | 提升 CTR |
| metal-weight-calculator | title 去 `\| Free ToolBase`；desc 扩写至 121；补内链（重量/密度/混凝土/贵金属） | 标题含英文品牌噪音；原无内链条目 | 标题更聚焦，内链补全 |
| en/har-file-viewer | title 改为 "Analyze HTTP Waterfalls Online"；补 EN 内链（JSON/速度/API/URL） | 原标题缺行动词；原无内链条目 | 提升 EN 点击 |
| dice-roll-simulator | title 去 `Free ToolBase`；desc 扩写；修复"什么是"定义与使用场景；补 4 条 FAQ；内链替换 | 原定义是坏模板文本、场景写错（"生成密码"）；原内链为缩写词/水印等无关项 | 修复内容错误，GEO 可提取 |
| modular-scale-calculator | title 从 72 宽度压至 33；desc 扩写；补内链（字体比例/排版/黄金比例） | 原标题超宽且混英文；原无内链 | 标题合规，内链补全 |
| eq-presets | desc 扩写至 122；内链替换为均衡器/音频类 | 原 desc 62 字符过短；原内链为 DNS/音频压缩等弱相关 | 提升 CTR |
| online-timer | title 去 `Free ToolBase`；desc 扩写；FAQ 从 2 条模板换成 4 条真实；内链替换 | 原 FAQ 是通用模板套话；原内链为 Unicode/渐变等无关项 | 真实 FAQ 贴近搜索 |
| sort-visualization | desc 扩写至 123；内链替换为算法/排序类 | 原 desc 62 字符过短；原内链为 UA/SQL 等无关项 | 提升 CTR |
| random-address | title 从 65 宽度压至 33；desc 扩写；FAQ 补至 4 条；内链替换 | 原标题超宽混英文；原内链为 Unicode/渐变等无关项 | 标题合规，FAQ 补全 |
| en/meta-description-generator | desc 从 115 扩写至 154；内链替换为 SEO 类 | 原 desc 偏短；原内链为计时器/存款等无关项 | 提升 EN CTR |
| openapi-spec-viewer | desc 扩写至 128；内链替换为 OpenAPI/JSON/API 类 | 原 desc 77 字符过短；原内链为 UA/SQL 等无关项 | 提升 CTR |
| grid-paper-generator | title 去 `\| Free ToolBase`；desc 扩写；内链替换为点阵网格/分辨率类 | 标题含英文品牌噪音；原内链无关 | 标题更聚焦 |
| text-to-braille | desc 扩写至 121；内链替换为盲文/摩斯/NATO/ASCII 类 | 原 desc 64 字符过短；原内链为日期/工时等无关项 | 提升 CTR |
| hearing-test | desc 扩写至 120；内链替换为音频/视力类 | 原 desc 69 字符过短；原内链为反链/热量等无关项 | 提升 CTR |
| emoji-translator | desc 扩写至 123；内链替换为 Emoji 类 | 原 desc 69 字符过短；原内链为 Base32/Base45 等无关项 | 提升 CTR |
| tailwind-gradient | desc 扩写至 124；内链替换为渐变/Tailwind 类 | 原 desc 70 字符过短；原无内链 | 提升 CTR |
| covered-call-calculator | title 去 `\| Free ToolBase`；desc 扩写；内链替换为期权重/ROI 类 | 标题含英文品牌噪音；原内链为期权策略/Black-Scholes 弱相关 | 标题更聚焦 |
| en/ini-editor | 内链替换为 JSON/YAML/TOML 类 | 原内链为二维码/JSON 等弱相关 | 提升 EN 相关性 |
| calorie-density-calculator | desc 扩写至 121；修复"什么是"定义与使用场景；补 4 条 FAQ；内链替换 | 原定义是坏模板文本；原内链为反链/热量记录等无关项 | 修复内容错误，GEO 可提取 |
| emoji-to-text | desc 扩写至 126；补 4 条 FAQ；内链替换 | 原无 FAQ；原内链为缩写词/水印等无关项 | GEO 补全 |
| sql-explainer | desc 扩写至 121；内链替换为 SQL 类 | 原 desc 72 字符过短；原内链为 Unicode/渐变等无关项 | 提升 CTR |
| unicode-character-map | desc 扩写至 120；内链替换为 Unicode/符号类 | 原 desc 69 字符过短；原内链为 UA/SQL 等无关项 | 提升 CTR |
| character-count | desc 扩写至 122；内链替换为字数/音节/统计类 | 原 desc 62 字符过短；原内链为计时器/存款等无关项 | 提升 CTR |
| html-sanitizer | desc 扩写至 123；内链替换为 HTML 类 | 原 desc 68 字符过短；原内链为计时器/存款等无关项 | 提升 CTR |
| logic-gate-simulator | desc 扩写至 121；内链替换为真值表/二进制类 | 原 desc 68 字符过短；原内链为日期/工时等无关项 | 提升 CTR |
| yaml-diff | desc 扩写至 121；内链替换为 JSON/文本/代码对比类 | 原 desc 59 字符过短；原内链为二维码/JSON 等弱相关 | 提升 CTR |
| en/ssh-key-generator | desc 从 98 扩写至 153；内链替换为 RSA/Hash/JWT/密码类 | 原 desc 偏短；原内链为计时器/存款等无关项 | 提升 EN CTR |
| en/fullwidth-converter | 内链替换为大小写/删除线/Unicode 类 | 原内链为计时器/存款等无关项 | 提升 EN 相关性 |
| gzip-test | desc 扩写至 122；内链替换为压缩/网站速度类 | 原 desc 66 字符过短；原内链为 Bash/CIDR 等无关项 | 提升 CTR |

## 三、内链清单（源页 → 目标页 | 理由）

> 全部内链均遵循"用户下一步会想看什么"，无链接农场。

| 源页 | 目标页 | 理由 |
|:--|:--|:--|
| resolution-calculator | aspect-ratio-calculator / ppi-calculator / screen-resolution-simulator / image-resize | 算完分辨率后想算纵横比/PPI/对比屏幕/调整图片尺寸 |
| typing-test | typing-speed-test / keyboard-tester / typing-race / typing-speed-calculator | 测速后想换模式/测键盘/竞速/换算速度 |
| metal-weight-calculator | weight-converter / density-calculator / concrete-weight-calculator / precious-metal-calculator | 算完金属重量后想换算单位/算密度/其他材料重量 |
| en/har-file-viewer | json-formatter / website-speed-test / api-tester / url-validator | 分析 HAR 后想格式化 JSON/测速/测 API/验证 URL |
| dice-roll-simulator | random-number-generator / coin-flip / wheel-of-names / dice-roller | 掷骰后想生成随机数/抛硬币/转盘/其他骰子工具 |
| modular-scale-calculator | type-scale-generator / typography-scale-generator / golden-ratio-calculator / font-size-converter | 生成排版比例后想用字体比例尺/黄金比例/换算字号 |
| eq-presets | audio-equalizer / online-equalizer / audio-eq-presets / tone-generator | 用 EQ 预设后想调均衡器/其他预设/生成测试音 |
| online-timer | timer-stopwatch / pomodoro-timer / countdown-timer / stopwatch | 计时后想用秒表/番茄钟/倒计时 |
| sort-visualization | algorithm-visualizer / text-sort / list-sorter / json-sorter | 看排序动画后想用算法可视化/实际排序工具 |
| random-address | random-address-generator / random-name-generator / fake-data-generator / test-data-generator | 生成地址后想生成姓名/假数据/测试数据 |
| en/meta-description-generator | seo-title-generator / seo-meta-tag-generator / keyword-density-analyzer / word-counter | 写 meta 后想生成标题/标签/查关键词密度/数字数 |
| openapi-spec-viewer | openapi-viewer / openapi-generator / json-formatter / api-tester | 看 OpenAPI 后想用其他查看器/生成器/格式化 JSON/测 API |
| grid-paper-generator | dot-grid-generator / screen-resolution-simulator / image-resize | 生成网格纸后想用点阵网格/对比屏幕/调整图片 |
| text-to-braille | braille-translator / text-to-morse / nato-alphabet / text-to-ascii-art | 转盲文后想用其他翻译器/摩斯/NATO/ASCII 艺术 |
| hearing-test | online-tone-generator / tone-generator / vision-test / white-noise-generator | 测听力后想生成测试音/测视力/白噪音 |
| emoji-translator | emoji-to-text / emoji-picker / text-to-emoji / emoji-meaning-finder | 翻译 Emoji 后想查含义/选表情/转文字 |
| tailwind-gradient | css-gradient-generator / tailwind-shadow-generator / color-palette-generator / tailwind-generator | 生成渐变后想用 CSS 渐变/阴影/配色/Tailwind 代码 |
| covered-call-calculator | stock-options-calculator / put-call-ratio / roi-calculator / investment-calculator | 算期权后想算股票期权/看跌看涨比/ROI/投资收益 |
| en/ini-editor | json-formatter / yaml-formatter / toml-editor / yaml-to-json | 编辑 INI 后想格式化 JSON/YAML/编辑 TOML/转换 |
| calorie-density-calculator | calorie-calculator / bmi-calculator / weight-loss-calculator / calorie-deficit-calculator | 算热量密度后想算卡路里/BMI/减重/热量缺口 |
| emoji-to-text | emoji-translator / emoji-picker / emoji-meaning-finder / symbol-picker | 查 Emoji 含义后想翻译/选表情/查符号 |
| sql-explainer | sql-formatter / sql-query-builder / json-to-sql / sql-diff | 解释 SQL 后想格式化/构建/转换/对比 SQL |
| unicode-character-map | unicode-converter / unicode-table / html-entity-reference / symbol-picker | 查字符后想编解码/查表/查 HTML 实体/选符号 |
| character-count | word-counter / syllable-counter / text-statistics / text-sort | 数字数后想数字数/音节/文本统计/排序 |
| html-sanitizer | html-formatter / html-validator / html-to-text / html-entity-encoder | 净化 HTML 后想格式化/验证/转文本/编码实体 |
| logic-gate-simulator | truth-table-generator / binary-calculator / binary-operations / binary-to-hex | 玩逻辑门后想生成真值表/二进制计算/位运算/进制转换 |
| yaml-diff | json-diff / text-compare / code-compare / yaml-to-json | 对比 YAML 后想对比 JSON/文本/代码/转 JSON |
| en/ssh-key-generator | rsa-key-generator / hash-generator / jwt-generator / password-generator | 生成 SSH 密钥后想生成 RSA/Hash/JWT/密码 |
| en/fullwidth-converter | case-converter / text-case-converter / strikethrough-text / unicode-converter | 转全半角后想转大小写/删除线/Unicode |
| gzip-test | gzip-compressor / brotli-compressor / website-speed-test / website-status-checker | 测压缩后想压缩文本/测速度/查网站状态 |

## 四、related-tools.json 字节数（证明无格式噪音）

| 项目 | 字节数 |
|:--|:--|
| 改前 | 2,304,303 |
| 改后 | 2,310,524 |
| 增量 | +6,221（仅新增 17 个缺失条目 + 替换 13 个条目内链，2 空格缩进保持不变） |

- 格式校验：`python3 -c "import json; json.load(open('related-tools.json'))"` → 有效
- 缩进：2 空格（`\n  "en"` 存在），未改动其他条目

## 五、验证

- `python3 scripts/validate_ids.py` → **PASS**（7551 页全部 OK，GA/GAconfig/Adsterra/Bing 四 ID 齐全，零禁用 ID）
- JS 语法：28 个改动页全部 `node -c` 通过
- 提交：3 次 commit（每批 ~10 页），工作区干净
- EN 页：5 页人工核对，英文为自然写作，无机翻痕迹
# W4 · P3 流量增长报告

> 工作目录：`/home/chison/wt/w4`（分支 `worker/w4`）

> 目标：提升真实流量 —— 内链 + 相关推荐 + 内容深度（GEO）

## 一、内链清单（源页 → 目标页 + 理由）

### P3-B 工作日计算器家族（单点最大缺口）

| 源页 | 目标页 | 理由 |
|:-----|:-------|:-----|
| `business-days-calculator` | `workdays-calculator` | 同为工作日计算场景，用户算完两个日期间工作日会想查全年/每月工作日 |
| `business-days-calculator` | `business-day-calculator` | 同为工作日/营业日计算，功能互补（本页为完整版，该页为精简版） |
| `business-days-calculator` | `work-hours-calculator` | 同为工时/工作时间场景，算完工作日天数自然要算每日工时 |
| `business-days-calculator` | `time-duration-calc` | 同为日期时间计算族，算工作日天数后可能想算具体时间间隔 |
| `business-days-calculator` | `date-difference-calculator` | 同为日期差计算族，工作日与自然日天数可互相印证 |
| `business-day-calculator` | `business-days-calculator` | 同族主工具，精简版引导到完整版 |
| `business-day-calculator` | `workdays-calculator` | 同为工作日计算场景 |
| `business-day-calculator` | `work-hours-calculator` | 同为工时/工作时间场景 |
| `business-day-calculator` | `time-duration-calc` | 同为日期时间计算族 |
| `business-day-calculator` | `date-difference-calculator` | 同为日期差计算族 |
| `workdays-calculator` | `business-days-calculator` | 同族主工具 |
| `workdays-calculator` | `business-day-calculator` | 同为工作日计算场景 |
| `workdays-calculator` | `work-hours-calculator` | 同为工时/工作时间场景 |
| `workdays-calculator` | `time-duration-calc` | 同为日期时间计算族 |
| `workdays-calculator` | `date-difference-calculator` | 同为日期差计算族 |
| `work-hours-calculator` | `time-card-calculator` | 同为工时计算场景 |
| `work-hours-calculator` | `business-days-calculator` | 同为工作时间场景 |
| `work-hours-calculator` | `workdays-calculator` | 同为工作日/工时场景 |
| `work-hours-calculator` | `time-duration-calc` | 同为时间计算族 |
| `work-hours-calculator` | `timesheet-calculator` | 同为工时表/考勤场景 |

### P3-A 高展现页相关推荐修复（替换占位链接）

共修复 **72 页** 占位相关推荐（百分比/番茄钟/BMI、自然语言日期解析器/指南针、DNS记录对比器/音频压缩、Docker验证器/文件类型识别、缩写词/水印/交叉渐变、Unicode/CSS、反链/热量/食物、Base32/45/64、文本去重/音节/URL、小费/双周还款、SVG/批量二维码/取色、Bash/CIDR、质数/斐波那契/阶乘 等占位模式），全部替换为真实相关工具。

代表性示例：

| 源页 | 原占位链接 | 替换为 | 理由 |
|:-----|:-----------|:-------|:-----|
| `heat-index-calculator` | 百分比/番茄钟/BMI | 风寒/紫外线/湿球/温度换算/露点 | 同为体感温度/天气场景 |
| `timesheet-calculator` | 百分比/番茄钟/BMI | 工时/工时卡/时间间隔/加班/计费工时 | 同为工时考勤场景 |
| `graphing-calculator` | 百分比/番茄钟/BMI | 科学计算/三角函数/矩阵/二次方程/百分比 | 同为数学计算场景 |
| `cidr-calculator` | 百分比/番茄钟/BMI | 子网/子网掩码/IP计算/IP范围/IPv4-IPv6 | 同为网络子网场景 |
| `bpm-tapper` | DNS/音频压缩/回声 | 节拍器/在线节拍器/BPM延迟/变速/音频发生器 | 同为音乐节拍场景 |
| `checksum-calculator` | Docker/文件类型/Google索引 | 文件校验/文件哈希/MD5/SHA256 | 同为哈希校验场景 |
| `tax-refund-calculator` | 小费/双周还款 | 个税/税率表/专项扣除/实发工资/工资个税 | 同为个税场景 |
| `whats-my-ip` | Bash/CIDR转IP | IP查询/IP地理/MAC查询/Whois/子网 | 同为IP网络场景 |
| `rhyme-finder` | 文本去重/音节/URL | 音节/单词重组/词频/回文/字数 | 同为文本语言场景 |
| `unicode-decoder` | Unicode/CSS | Unicode查询/转换/分析/浏览/查找 | 同为Unicode场景 |
| `regex-101` | Unicode/CSS | 正则测试/生成/可视化/解释/速查表 | 同为正则场景 |
| `image-histogram` | SVG/批量二维码/取色 | 调色板/图片取色/颜色选择/颜色转换/着色 | 同为图像颜色场景 |
| `vision-test` | 反链/热量/食物 | 视力测试/视力表换算/颜色转换/取色/显示器 | 同为视力检测场景 |
| `daily-journal` | 反链/热量/食物 | 心情记录/感恩日记/习惯追踪/肯定语/待办 | 同为日记习惯场景 |
| `vin-decoder` | Base32/45/64 | VIN验证/车贷/折旧/车险/租赁 | 同为车辆场景 |
| `cursive-text-generator` | 缩写词/水印/交叉渐变 | 花体/手写体/文字转手写/小字/Zalgo | 同为文字样式场景 |
| `mouse-tester` | 自然语言日期/工时/指南针 | 键盘测试/点击计数/反应测试/显示器/分辨率 | 同为硬件测试场景 |
| `sleep-calculator` | 自然语言日期/工时/指南针 | 睡眠周期/睡眠债务/睡眠周期/世界时钟/计时器 | 同为睡眠场景 |
| `atbash` | Unicode/CSS | Atbash/ROT13/维吉尼亚/凯撒/摩斯 | 同为密码学场景 |
| `markdown-table-formatter` | Unicode/CSS | Markdown表格/转CSV/编辑器/转HTML/排序 | 同为Markdown场景 |

### P3-C EN 页内链强化

| 源页 | 目标页 | 理由 |
|:-----|:-------|:-----|
| `en/mouse-tester` | `en/mouse-click-counter` | 同为鼠标测试场景 |
| `en/mouse-tester` | `en/keyboard-tester` | 同为外设测试场景 |
| `en/mouse-tester` | `en/reaction-test` | 同为硬件/反应测试场景 |
| `en/mouse-tester` | `en/monitor-test` | 同为硬件测试场景 |
| `en/mouse-tester` | `en/screen-resolution` | 同为硬件/显示场景 |
| `en/temperature-difference-calculator` | `en/temperature-converter` | 同为温度计算场景 |
| `en/temperature-difference-calculator` | `en/wet-bulb-calculator` | 同为温度/湿度场景 |
| `en/temperature-difference-calculator` | `en/heat-index-calculator` | 同为体感温度场景 |
| `en/temperature-difference-calculator` | `en/wind-chill-calculator` | 同为体感温度场景 |
| `en/temperature-difference-calculator` | `en/dew-point-calculator` | 同为温度/湿度场景 |
| `en/countdown-clock` | `en/full-screen-clock` | 同为时钟场景 |
| `en/countdown-clock` | `en/online-clock` | 同为时钟场景 |
| `en/countdown-clock` | `en/world-clock` | 同为时钟场景 |
| `en/countdown-clock` | `en/online-stopwatch` | 同为计时场景 |
| `en/countdown-clock` | `en/online-timer` | 同为计时场景 |
| `en/work-hours-calculator` | `en/time-card-calculator` | 同为工时计算场景 |
| `en/work-hours-calculator` | `en/business-days-calculator` | 同为工作时间场景 |
| `en/work-hours-calculator` | `en/workdays-calculator` | 同为工作日/工时场景 |
| `en/work-hours-calculator` | `en/time-duration-calc` | 同为时间计算族 |
| `en/work-hours-calculator` | `en/timesheet-calculator` | 同为工时表场景 |

## 二、新增 FAQ / GEO 内容页清单

| 页面 | 新增内容 |
|:-----|:---------|
| `workdays-calculator` | 修复占位使用场景 → 真实场景（项目排期/合同履约/考勤/时效）+ 4条FAQ |
| `en/workdays-calculator` | 新增 FAQ（4条：计算方式/端点包含/节假日排除/工作日vs自然日） |
| `en/work-hours-calculator` | 修复占位使用场景 → 真实场景（考勤/加班/计费工时/效率）+ 4条FAQ |
| `sunrise-sunset-calculator` | 新增可见 GEO 内容（定义+4场景+4FAQ）+ 相关推荐区 |
| `en/sunrise-sunset-calculator` | 新增 Use Cases + FAQ（4条）+ 强化相关推荐 |
| `kpi-calculator` | 修复占位使用场景 → 真实场景（KPI完成率/同比环比/目标跟踪/绩效评分） |
| `file-checksum-calculator` | 修复占位使用场景 → 真实场景（文件完整性/篡改检测/备份校验/内容比对） |
| `paycheck-calculator` | 补充可见 FAQ（4条：实发工资/时薪年薪/五险一金/数据安全） |
| `sleep-calculator` | 补充可见 FAQ（4条：周期计算/周期时长/5周期建议/午休时长） |
| `character-unicode-finder` | 新增 FAQ（4条：查询范围/编码查询/Emoji生僻字/复制） |
| `invisible-character` | 新增 FAQ（4条：隐形字符/空白昵称/平台识别/安全） |
| `file-checksum-calculator` | 新增 FAQ（4条：算法/完整性验证/隐私/大文件） |
| `gray-code-converter` | 新增 FAQ（4条：格雷码定义/二进制转/反向转换/用途） |
| `daily-journal` | 新增 FAQ（4条：使用/数据丢失/导出/隐私） |
| `atbash` | 新增 FAQ（4条：Atbash定义/解密/中文数字/安全性） |

## 三、验证输出

### 1. 内链目标页存在性（脚本验证）

```
总内链数: 498
损坏链接: 0
```

### 2. 相关推荐区零占位

```
占位问题: 0（invisible-character 的'占位'为正文内容，非占位链接）
```

### 3. EN 页无中文残留

```
EN 中文残留: 0
```

### 4. 内容深度（≥600字符）

```
workdays-calculator: 1202 chars [OK]
en/workdays-calculator: 1717 chars [OK]
work-hours-calculator: 771 chars [OK]
en/work-hours-calculator: 1912 chars [OK]
sunrise-sunset-calculator: 1073 chars [OK]
en/sunrise-sunset-calculator: 2754 chars [OK]
kpi-calculator: 1079 chars [OK]
file-checksum-calculator: 1248 chars [OK]
paycheck-calculator: 971 chars [OK]
sleep-calculator: 1114 chars [OK]
character-unicode-finder: 1075 chars [OK]
invisible-character: 1188 chars [OK]
gray-code-converter: 1014 chars [OK]
daily-journal: 1113 chars [OK]
atbash: 1037 chars [OK]
```

### 5. JS 语法检查

```
修改的 94 页中 92 页通过 node -c
2 页失败为既有问题（非本次修改引入）：whats-my-ip、uptime-checker（async window.x 语法）
```

### 6. sitemap / git 状态

```
sitemap.xml URL 数: 7166（未变）
git status --short: 干净
```

## 四、Git 提交记录

```
0aeae82e3f feat(seo): W4 为 gpu-benchmark/frame-grabber 补充 related-tools.json 相关推荐
bde170d1d8 feat(seo): W4 为 8 个高展现页补充可见 FAQ 内容
97fd2c0b0b feat(seo): W4 为 8 个高展现页补充相关推荐区（speed-test/bpm-delay 等）
fff51e99bf feat(seo): W4 补充日出日落计算器 GEO 内容与相关推荐（CN+EN）
24ce1a5511 feat(seo): W4 修复 kpi/file-checksum 占位使用场景为真实场景
9052376ac8 feat(seo): W4 补充工作日/工时族 GEO 内容（定义+场景+FAQ，CN+EN）
a8f09ba0ed feat(seo): W4 强化 EN 页内链承接（mouse-tester/temperature-difference 等）+ 修复 related-tools.json 占位
c2c0af8c8e feat(seo): W4 修复 top100 页相关推荐占位，替换为真实相关工具（72页）
33b25eab45 feat(seo): W4 修复工作日计算器家族页相关推荐占位（CN+EN）
```

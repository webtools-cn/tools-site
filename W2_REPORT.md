# W2 · P1 功能正确性对拍报告

> 分支 `worker/w2` · 日期 2026-09-18
> 方法：逐页读取 `index.html` 提取真实公式 → Node 独立复算（≥3 组输入，含 0/负数/极大值/空值边界）→ 与页面 JS 输出对拍。

## 一、修复清单（6 个工具，7 处 bug，CN+EN 共 11 个文件）

| # | 工具 | 问题 | 修复 |
|---|------|------|------|
| 1 | `wind-chill-calculator` (CN+EN) | Siple 公式错误：`0.045*(5.2735+10.45-V)*(T-33)+33` 缺少 `10√V` 项，-15°C/40km/h 算出 +85°C | 改为标准 Siple-Passel：`33+(10.45+10√V-V)*(T-33)/22.04`，-15°C/40km/h → -40.4°C |
| 2 | `tax-bracket-calculator` (CN) | 月薪模式误用**年度**级距（36000/144000…），月薪 20000 只算 450 元税 | 新增月度级距（3000/12000/25000…），月薪 20000 → 1590 元 |
| 3 | `tax-bracket-calculator` (EN) | 月薪模式未年化，直接用年度级距算月收入，严重少税 | 月薪×12 年化后计税再 ÷12 |
| 4 | `graphing-calculator` (CN+EN) | 表达式编译：`ln(x)`→`Math.Math.log10(x)` 报错；`log2(x)` 被 `(\d)\(` 规则破坏成 `log2*(x)` | 调整 log/log2/ln 替换顺序 + `(\d)\(` 加负向后瞻 `(?<![a-zA-Z])` |
| 5 | `sunrise-sunset-calculator` (CN+EN) | 输出的是**太阳时**而非当地钟表时（缺经度/时区校正），北京差 ~14 分钟、纽约差 ~56 分钟 | 加 `lngCorr = round(lng/15) - lng/15` 校正；北京 6/21 日出 04:47 与实测一致 |
| 6 | `business-day-calculator` (CN) | `isWorkday` 用 `toISOString()`（UTC）比对节假日，UTC+8 下节假日错位一天 | 改用本地 `formatDate()` |
| 7 | `cbor-encoder` (CN+EN) | 示例 hex 字符串长度错误（"compact" 标 6 字节、"extensible" 标 9 字节），点击示例解码必失败 | 修正为正确 CBOR（`83 67 63 6f 6d 70 61 63 74 … 6a 65 78 74 65 6e 73 69 62 6c 65`） |

## 二、逐页对拍表（48 页，全部通过）

### 计算器类（top120 内 36 页全验）

| 页面 | 输入 → 页面输出 → 独立复算 | 结论 |
|------|---------------------------|------|
| business-days-calculator | 2026-01-01~01-31 → 22 工作日/30 天/8 周末 → 22 | ✅ |
| sunrise-sunset-calculator | 北京 2026-06-21 → 日出04:47 日落19:47 → 实测04:46/19:47 | ✅ 已修复 |
| tax-calculator | 月薪20000 → 税1590 到手18410 → 1590/18410 | ✅ |
| business-day-calculator | 2026-01-01起+10工作日(含1/1节假日) → 2026-01-15 → 01-15 | ✅ 已修复 |
| tax-refund-calculator | 年收200000 已缴20000 → 退8520 → 8520 | ✅ |
| checksum-calculator | crc32("abc") → 352441c2 → zlib一致 | ✅ |
| heat-index-calculator | 35°C/70% → 50.3°C → NOAA公式50.3 | ✅ |
| timesheet-calculator | 5天(1天10h) → 42h/加班2h → 42/2 | ✅ |
| paycheck-calculator | 时薪100×40h 月结 → 税1056.67 到手16276.67 → 一致 | ✅ |
| time-duration-calc | 09:00-17:30 → 8h30m；23:59-00:01 → 2m | ✅ |
| binary-calculator | 1010+0101=1111(15)；NOT 0000=-1；0001<<3=1000 | ✅ |
| trig-calculator | 30°→sin0.5 tan0.577；90°→tan∞ | ✅ |
| electricity-cost-calculator | 1500W×5h×0.6元 → 日4.5/月135/年1642.5 | ✅ |
| sleep-calculator | 7:00起+15min入睡 → 23:15(5周期) | ✅ |
| kpi-calculator | 目标100万 实际120万 → 120%/+33.3% | ✅ |
| cidr-calculator | 192.168.1.0/24 → 网段/广播/254可用；/32→1 | ✅ |
| bpm-delay-time-calculator | 120BPM四分音符 → 500ms；八分→250ms | ✅ |
| hex-calculator | FF+0A=0x109；FF&0A=0xA；FF/0A=0x19 | ✅ |
| currency-converter | 100USD→CNY 725；1000JPY→CNY 46.03 | ✅ |
| dpi-calculator | 1920×1080/5.5" → 401PPI 16:9；300PPI/24"→6275×3530 | ✅ |
| uv-index-calculator | 25°N 7/15正午 → UV12.1；夜间→0 | ✅ |
| wind-chill-calculator | NWS -15/40 → -27.4°C；Siple -15/40 → -40.4°C | ✅ 已修复 |
| file-checksum-calculator | Web Crypto 原生 MD5/SHA 系列 | ✅ |
| gray-code-converter | 1011→1110；42→111111；255→10000000 | ✅ |
| tax-bracket-calculator | 月薪20000 → 税1590 到手18410；年终奖200000→税23080 | ✅ 已修复 |
| scientific-notation-converter | 299792458→2.997925×10⁸；6.6743e-11→×10⁻¹¹ | ✅ |
| cgpa-calculator | 目标3.5 现3.2/60学分/4学期×15 → 需3.80 | ✅ |
| hourly-to-salary-calculator | 时薪20×40h → 年41600/月3464 | ✅ |
| vat-calculator | 不含税100/13% → 税13 含税113；反向113→100 | ✅ |
| ral-color-converter | 214色 RGB↔HEX 全一致，无重复码 | ✅ |
| inflation-calculator | 10000/3%/10年 → 购买力7440.94 损失25.59% | ✅ |
| paypal-fee-calculator | 100/2.9%/0.3 → 费3.2 到手96.8 | ✅ |
| payroll-tax-calculator | 北京15000 → 社保1530 公积金1800 税457 到手11213 | ✅ |
| graphing-calculator | sin(x)、2x+1、x²、ln(x)、log2(x)、log(x) 全部正确 | ✅ 已修复 |
| en/temperature-difference-calculator | 100°C-0°C → 100°C=180°F=100K=180°R | ✅ |
| en/binary-hex-converter | 255→11111111/377/FF；BigInt 大数正确 | ✅ |

### 其他高流量工具（12 页）

| 页面 | 输入 → 页面输出 → 独立复算 | 结论 |
|------|---------------------------|------|
| en/cbor-encoder | 示例hex解码 → {"name":"cbor",…} | ✅ 已修复 |
| bpm-tapper | 500ms间隔 → 120BPM；400ms → 150BPM | ✅ |
| battery-capacity-tester | 5000mAh@3.7V → 5Ah/18.5Wh；100Wh@5V→20Ah | ✅ |
| reaction-test | getRank 150/220/300/500 分级正确 | ✅ |
| ascii-to-hex | "ABC"→41 42 43；"48656C6C6F"→Hello | ✅ |
| base58-decoder | "Hello, Base58!"→TcgsE5e9XJSrakNTEQQ（与标准一致） | ✅ |
| atbash-cipher | "Hello"→Svool；"123"含数字→876 | ✅ |
| bic-checker | DEUTDEFF 有效；1234DEFF/DEUTXXFF 无效 | ✅ |
| reading-speed-test | WPM=词数/(秒/60) 公式正确 | ✅ |
| subnet-divider | /24分4→4个/26各62主机；/8分8→/11 | ✅ |
| vin-decoder | 1HGCM82633A004352 校验位=3（独立实现一致） | ✅ |
| karnaugh-map-solver | 2var{0,1}→A'；3var{0,2,4,6}→C'；4var{0,1,2,3}→A'B' | ✅ |

## 三、空壳工具清单

top120 内未发现 0 输入 0 交互的空壳工具。全部 120 页经 smoke test 加载无 JS 报错。

## 四、验收项

1. ✅ 抽检 48 页（≥30），每页给出输入/页面输出/复算/结论（见上表）
2. ✅ 6 个不一致工具已修复，并用同一 harness 复验通过
3. ✅ `node --check` 对全部改动页 JS 通过（排除 JSON-LD schema 块）
4. ✅ `git status --short` 干净，3 个提交：
   - `c92ccd3ed5` fix(calc): W2 修正3个计算器错误 - wind-chill Siple公式、tax-bracket月薪级距、graphing ln/log2表达式
   - `35b1751e75` fix(calc): W2 修正日出日落时区校正 + business-day节假日UTC偏移bug
   - `8db803db82` fix(calc): W2 修正 cbor-encoder 示例hex字符串长度错误

## 五、已知限制（未改，属设计取舍）

- `sunrise-sunset-calculator` 时区由经度估算 `round(lng/15)`，无 DST 地区（如中国）精确；实行夏令时地区夏季有 ±1h 误差。未加时区下拉框（避免大改）。
- `currency-converter` 使用内置 fallback 汇率（网络不可用时），标注"仅供参考"。
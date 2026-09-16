#!/usr/bin/env python3
"""标题/描述精准优化 2026-09-16

用户铁律: 不能搞坏生产, 不能搞丢流量, 要严格测试。
做法: 只同步替换 5 个 head 字段 -- title / description / og:title / og:description /
      keywords(仅当原关键词是模板垃圾时)。其余内容逐字节不变。

安全闸: mask(old) == mask(new)  -- 把上述字段抹成占位符后, 两份内容必须完全相同。
        + GA / 广告 / canonical / JSON-LD / H1 数量核对

用法: --dry            预演全部
      --one <slug>     只改 1 页(先验证)
      --apply          全量
      --verify         核对是否生效
"""
import re, sys

BASE = "/home/chison/tools-site/"

# slug -> {title, desc, kw(可选)}
OPT = {
"tax-calculator": dict(
 title="个人所得税计算器2026 - 个税计算/税率表/专项附加扣除 - Free ToolBase",
 desc="免费在线个人所得税计算器，按2026年最新个税税率表计算工资薪金个人所得税，自动扣除5000元起征点、五险一金和专项附加扣除，实时显示应纳税所得额、适用税率、速算扣除数和税后到手工资。适合上班族核对工资条、HR核算个税、企业财务测算用工成本。纯前端本地计算，数据不上传服务器，无需注册。"),
"sunrise-sunset-calculator": dict(
 title="日出日落时间计算器 - 在线查询任意地点日出日落时间 | Free ToolBase",
 desc="免费在线日出日落时间计算器，输入城市名或经纬度即可查询任意日期、任意地点的日出时间、日落时间、昼长和正午太阳高度，支持黄金时刻、蓝调时刻与晨昏蒙影时间查询。适合摄影爱好者规划拍摄时机、户外出行安排、农业光照管理和天文观测。纯前端本地计算，数据不上传服务器，完全免费无需注册。"),
"mouse-tester": dict(
 title="免费在线鼠标测试工具 - 按键/滚轮/双击/移动轨迹检测 | 无需注册",
 desc="免费在线鼠标测试工具，全面检测鼠标左键、中键和右键的单击与双击响应灵敏度，测试滚轮上下滚动是否正常，实时可视化显示光标移动轨迹和当前坐标位置，并支持双击速度测试评估反应时间。适合排查鼠标硬件故障、检验新鼠标各按键功能是否完好、游戏玩家调校鼠标。纯网页运行无需安装任何软件，数据不上传服务器，完全免费无需注册。",
 kw="鼠标测试,在线鼠标测试,鼠标按键检测,鼠标滚轮测试,双击速度测试,鼠标轨迹测试,鼠标双击检测,鼠标故障检测"),
"reaction-test": dict(
 title="免费在线反应速度测试 - 毫秒级精准测量反应时间 | 平均值与评级",
 desc="免费在线反应速度测试工具，精准测量你的视觉反应时间毫秒值。支持多次连续测试取平均值、历史记录对比和趋势图表可视化分析，自动评级反应速度等级。使用高精度 performance.now 计时API毫秒级测量，数据本地保存不上传服务器，完全免费无需注册。",
 kw="反应速度测试,反应时间测试,在线反应测试,反应力测试,手速测试,反应速度平均值,毫秒反应测试,视力反应测试"),
"business-days-calculator": dict(
 title="工作日计算器 - 两个日期之间工作日天数在线计算 | 排除周末节假日 - Free ToolBase",
 desc="免费在线工作日计算器，快速计算两个日期之间的工作日天数，自动排除周末和自定义法定节假日。支持添加或减去N个工作日推算目标日期、一键加载中国法定节假日。适合项目经理排期规划、合同截止日期计算、HR考勤统计和物流时效预估等场景。纯前端本地处理，数据不上传服务器，完全免费无需注册。"),
"business-day-calculator": dict(
 title="工作日计算器 - N个工作日后是几号 | 工作日加减日期推算 - Free ToolBase",
 desc="免费在线工作日推算器，输入起始日期和工作日天数，自动推算N个工作日后（或前）是哪一天，自动跳过周末和法定节假日，支持自定义假期列表和调休上班日设定。适合合同签署期限、项目交付排期、证照办理时限和物流时效推算等场景。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="工作日推算,工作日计算器,工作日加减,工作日天数计算,日期推算,几个工作日后是哪天,排期计算,考勤天数计算"),
"file-hash-checker": dict(
 title="免费在线文件哈希校验工具 - MD5/SHA1/SHA256/SHA512 文件校验 | 无需注册",
 desc="免费在线文件哈希校验工具，拖拽上传文件即可计算 MD5、SHA-1、SHA-256、SHA-512 等多种哈希值，用于校验下载文件完整性、验证文件是否被篡改。适合软件下载安全验证、镜像文件核对、数字取证和备份一致性检查。纯前端本地处理，文件不上传服务器，无需注册完全免费。",
 kw="文件哈希校验,MD5校验工具,文件MD5值查询,SHA256校验,文件完整性校验,哈希值计算,文件指纹校验,在线哈希工具"),
"checksum-calculator": dict(
 title="在线校验和计算器 - MD5/SHA1/SHA256/CRC32 文本哈希校验 | 无需注册",
 desc="免费在线校验和计算器，输入文本或字符串即可计算 MD5、SHA1、SHA256、SHA512、CRC32、SHA3 等多种哈希与校验和值，支持大小写切换和批量文本计算。适合开发者校验接口签名、比对字符串哈希、验证数据一致性。纯前端本地处理，数据不上传服务器，完全免费无需注册。"),
"en/tax-calculator": dict(
 title="Income Tax Calculator 2026 - Salary Tax, Brackets & Take-Home Pay | ToolBase",
 desc="Free online income tax calculator. Estimate salary tax, your marginal bracket, deductions and take-home pay in seconds. Built for employees checking a payslip, HR teams estimating payroll tax and freelancers planning quarterly payments. Runs entirely in your browser - nothing is uploaded, no signup required."),
"en/mouse-tester": dict(
 title="Free Online Mouse Tester - Buttons, Scroll, Double-Click & Trail Test | No Signup",
 desc="Free online mouse tester. Check left, middle and right click and double-click response, test whether your scroll wheel works, and see your cursor movement trail and live coordinates. Measures double-click speed to estimate reaction time. Great for diagnosing a faulty mouse, checking a new one, or tuning a gaming setup. Runs entirely in your browser - no install, no upload, no signup.",
 kw="mouse tester,mouse test,online mouse checker,mouse button test,scroll wheel test,double click test,mouse click test,mouse trail test"),
"en/reaction-test": dict(
 title="Free Online Reaction Time Test - Millisecond Precision, Average & Rating | ToolBase",
 desc="Free online reaction time test that measures your visual reaction time in milliseconds. Run repeated tests, take the average, compare your history on a trend chart and get an automatic speed rating. Uses the high-precision performance.now timer. Results stay in your browser - nothing is uploaded, no signup required.",
 kw="reaction time test,reaction speed test,online reflex test,reaction time tester,average reaction time,human benchmark reaction,millisecond reaction test,visual reaction test"),
"en/sunrise-sunset-calculator": dict(
 title="Sunrise Sunset Calculator - Sunrise, Sunset & Daylight Time for Any Location | ToolBase",
 desc="Free online sunrise sunset calculator: enter a city or coordinates and get sunrise time, sunset time, day length and solar noon for any date, plus golden hour, blue hour and twilight times. Ideal for planning photo shoots, outdoor trips, farm lighting and stargazing. Runs entirely in your browser - no signup, no upload.",
 kw="sunrise time,sunset time,sunrise sunset calculator,golden hour calculator,day length calculator,daylight hours,blue hour,solar noon calculator"),
}

F = {
 "title":   (re.compile(r"<title>.*?</title>", re.S),
             lambda v: "<title>" + v + "</title>"),
 "desc":    (re.compile(r'<meta\s+name="description"\s+content="[^"]*"\s*/?>', re.S | re.I),
             lambda v: '<meta name="description" content="' + v + '">'),
 "og:title":(re.compile(r'<meta\s+property="og:title"\s+content="[^"]*"\s*/?>', re.S | re.I),
             lambda v: '<meta property="og:title" content="' + v + '">'),
 "og:desc": (re.compile(r'<meta\s+property="og:description"\s+content="[^"]*"\s*/?>', re.S | re.I),
             lambda v: '<meta property="og:description" content="' + v + '">'),
 "keywords":(re.compile(r'<meta\s+name="keywords"\s+content="[^"]*"\s*/?>', re.S | re.I),
             lambda v: '<meta name="keywords" content="' + v + '">'),
}
GA_RX = re.compile(r'googletagmanager\.com/gtag/js\?id=[A-Za-z0-9\-]+')
AD_RX = re.compile(r'pl\d+\.profitableratecpmnetwork\.com')
SAFETY = [("GA加载器", GA_RX), ("广告脚本", AD_RX),
          ("canonical", re.compile(r'rel="canonical"')),
          ("JSON-LD", re.compile(r'application/ld\+json')),
          ("H1", re.compile(r'<h1')), ("script对", re.compile(r'<script'))]


def mask(h):
    for rx, _ in F.values():
        h = rx.sub("<X/>", h)
    return h


def build(slug):
    p = BASE + slug + "/index.html"
    old = open(p, encoding="utf-8", errors="ignore").read()
    o = OPT[slug]
    vals = {"title": o["title"], "desc": o["desc"],
            "og:title": o["title"], "og:desc": o["desc"]}
    if o.get("kw"):
        vals["keywords"] = o["kw"]
    new = old
    for k, v in vals.items():
        rx, mk = F[k]
        if '"' in v:
            return None, f"{k} 含双引号, 不安全"
        n = len(rx.findall(new))
        if n != 1:
            return None, f"{k} 匹配 {n} 处 (需恰好1处)"
        new = rx.sub(lambda m, s=mk(v): s, new, count=1)
    if new == old:
        return None, "无变化"
    if mask(old) != mask(new):
        return None, "铁闸失败: 非目标字段被改动"
    for name, rx in SAFETY:
        if len(rx.findall(old)) != len(rx.findall(new)):
            return None, f"要害元素 {name} 数量变化"
    return new, "ok"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"
    todo = list(OPT)
    if mode == "--one":
        todo = [sys.argv[2]]
    for s in todo:
        p = BASE + s + "/index.html"
        old = open(p, encoding="utf-8", errors="ignore").read()
        new, msg = build(s)
        if new is None:
            print(f"  [跳过] {s}: {msg}")
            if mode in ("--apply", "--one") and "铁闸" in msg or "要害" in msg:
                print("      ⚠️ 这属于危险信号, 已中止不改")
            continue
        if mode == "--apply" or mode == "--one":
            open(p, "w", encoding="utf-8").write(new)
            print(f"  [已改] {s}  {len(new)-len(old):+d} 字节")
        else:
            print(f"  [预演] {s}  {len(new)-len(old):+d} 字节  新标题: {OPT[s]['title']}")


if __name__ == "__main__":
    main()

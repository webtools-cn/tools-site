#!/usr/bin/env python3
"""税务/工资簇差异化 2026-09-16  (批次1: 消除自相残杀)  v2 格式无关

背景: 60 个税务/工资页里 26 个挤在 3 个簇里互相抢同一个词
      (中国个税7页 / 税后实发6页 / 时薪年薪换算13页), 全簇合计才 4,910 展现。
做法: 不改功能、不删页、不重定向 —— 只给每页锁定一个**独有的搜索意图**,
      同步替换 title / description / og:title / og:description / keywords。
      其余内容逐字节不变(铁闸证明)。

v2: 同时兼容 <meta name="x" content="y"> 与 <meta content="y" name="x"> 两种属性顺序。
    keywords 标签缺失时静默跳过(不新增标签, 避免改变页面结构)。

用法: --dry | --one <slug> | --apply
"""
import re, sys

BASE = "/home/chison/tools-site/"

OPT = {
# ── A 簇: 中国个税 (7页) ─────────────────────────────────────────
# tax-calculator 已升级为真个税页, 占主词「个人所得税计算器」, 此处不再动
"tax-bracket-calculator": dict(
 title="个人所得税税率表计算器 - 2026税率级距与速算扣除数 | Free ToolBase",
 desc="免费在线个人所得税税率表计算器，按2026年综合所得七级超额累进税率表计算，输入税前收入、社保公积金和专项附加扣除，自动判断适用税率级距和速算扣除数并算出应纳个税。内置完整月度/年度税率对照表，支持工资薪金与年终奖两种计税方式对比。适合核对税率级距、验算工资条个税。纯前端计算，数据不上传服务器，无需注册。",
 kw="个人所得税税率表,2026个税税率表,税率级距,速算扣除数,综合所得税率表,个税税率计算器,七级累进税率,个人所得税计算"),
"payroll-tax-calculator": dict(
 title="工资个税计算器 - 按城市社保基数核算工资税 | Free ToolBase",
 desc="免费工资个税计算器，覆盖北京、上海、广州、深圳、杭州、成都等城市的社保与公积金基数比例，输入税前月薪即可按当地标准扣除五险一金后计算应缴个人所得税和实发工资。可自定义社保基数、公积金缴纳比例和专项附加扣除。适合跨城市对比到手工资、HR核算各地用工成本。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="工资个税计算器,工资税计算器,各城市社保基数,社保缴纳基数,公积金比例计算,工资税测算,个税核算,到手工资计算"),
"income-tax-calculator": dict(
 title="专项附加扣除计算器 - 子女教育/赡养老人/住房租金 | Free ToolBase",
 desc="免费在线个税专项附加扣除计算器，逐项录入子女教育、3岁以下婴幼儿照护、赡养老人、住房贷款利息、住房租金、继续教育等扣除项目，自动汇总每月专项附加扣除合计额并计算个人所得税和税后收入。适合填报个税APP前试算扣除额、核对单位代扣是否正确。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="专项附加扣除计算器,子女教育扣除,赡养老人扣除,住房租金扣除,住房贷款利息扣除,继续教育扣除,婴幼儿照护扣除,个税扣除计算"),
"chinese-tax-calculator": dict(
 title="中国个税计算器 - 年终奖单独计税与并入综合所得对比 | Free ToolBase",
 desc="免费中国个税计算器，按月工资个税和年终奖个人所得税分别计算，并对比年终奖「单独计税」与「并入综合所得」两种方式的税负差异，自动推荐更省税的方案。支持五险一金和专项附加扣除录入，适用2026年个税政策。适合年底发奖金前做税务筹划。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="中国个税计算器,年终奖个税,年终奖单独计税,年终奖并入综合所得,个税筹划,个税对比计算,年终奖计算器,中国个人所得税"),
"tax-estimator": dict(
 title="个税估算器 - 30秒快速估算每月个人所得税 | Free ToolBase",
 desc="免费个税估算器，只需输入月收入，即可按2026年个税税率表快速估算每月应缴个人所得税和大致的到手金额，可选填社保公积金和专项附加扣除以提高精度。适合快速了解个税水平、面试谈薪时估算到手工资、对工资条做粗略核对。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="个税估算器,个税快速估算,个人所得税估算,月收入个税,个税试算,估算个税,到手工资估算,个税估算工具"),
"paye-calculator": dict(
 title="PAYE个税计算器 - 中国/英国个税在线计算 | Free ToolBase",
 desc="免费PAYE个税计算器，支持按地区选择中国个税或英国PAYE税制计算个人所得税，输入收入金额和周期后自动应用对应地区的税率表与免税额，并支持五险一金和专项附加扣除录入。适合需要对比中英两地税负的跨境工作者和留学生。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="PAYE计算器,PAYE个税,英国个税计算,中英个税对比,跨境个税,个税计算器,PAYE tax,英国税制计算"),

# ── B 簇: 税后实发工资 (6页, 全零展现) ────────────────────────────
"take-home-pay": dict(
 title="实发工资计算器 - 到手工资/个税/五险一金明细 | Free ToolBase",
 desc="免费在线实发工资计算器，输入税前月收入，逐项扣除个人承担的养老保险、医疗保险、失业保险、住房公积金和个人所得税，清晰展示每一项扣除金额和最终到手工资。支持自定义各项比例和起征点，适合核对工资条、比较不同offer的实际收入。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="实发工资计算器,到手工资计算,税后工资,五险一金计算,工资条核对,净收入计算,个税扣除计算,实际到手收入"),
"net-pay-calculator": dict(
 title="净收入计算器 - 税前税后收入换算与可支配收入 | Free ToolBase",
 desc="免费在线净收入计算器，输入总收入并选择收入周期（月/年/周/日），按个税税率、社保和公积金比例扣除后算出净收入，同时展示扣除明细和实际税率。支持多周期换算，适合自由职业者估算实际可支配收入、跨周期比较收入水平。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="净收入计算器,净收入计算,税后净收入,可支配收入,收入换算,税前税后换算,净工资计算,收入周期换算"),
"paycheck-deduction": dict(
 title="工资扣除计算器 - 五险一金与个税扣除明细 | Free ToolBase",
 desc="免费工资扣除计算器，输入税前月薪、公积金比例和社保比例，自动算出五险一金个人扣除额、个人所得税和实发工资，并逐项展示扣除构成。适合快速了解工资被扣了哪些项目、核对单位代扣金额是否准确。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="工资扣除计算器,五险一金扣除,社保扣除计算,公积金扣除,工资扣款明细,个税扣除,税前税后工资,扣除比例计算"),
"paycheck-deductions": dict(
 title="工资单扣除项计算器 - 社保/公积金/个税逐项核算 | Free ToolBase",
 desc="免费在线工资单扣除项计算器，按发薪频率录入每期总收入，支持联邦税、州税、社保税等各项税率设置，逐项列出扣款明细并算出每期实发金额和年度合计。适合在美国领取工资的雇员核对 pay stub 各项扣除是否准确。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="工资单扣除,pay stub计算,工资扣款明细,联邦税扣除,州税扣除,社保税,每期实发工资,工资扣除项"),
"tax-withholding-calculator": dict(
 title="代扣代缴个税计算器 - 单位预扣个人所得税核算 | Free ToolBase",
 desc="免费在线代扣代缴个人所得税计算器，输入税前月薪、社保基数和公积金比例，按累计预扣预缴法计算单位每月代扣的个人所得税额和税后工资，并展示累计已扣税额。适合HR核算代扣个税、财务核对申报数据、员工核对工资条。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="代扣代缴个税,预扣预缴,累计预扣法,单位代扣个税,个税代扣计算,工资代扣,个人所得税预扣,代扣个税核算"),

# ── C 簇: 时薪/年薪换算 (13页, 只 1 页有 39 展现) ──────────────────
"hourly-to-salary-calculator": dict(
 title="时薪转年薪计算器 - 时薪×每周工时换算年薪月薪 | Free ToolBase",
 desc="免费在线时薪转年薪计算器，输入时薪、每周工作小时数和每年工作周数，自动换算年薪、月薪、周薪和日薪，支持多币种与自定义每年工作周数、每周工作天数。适合兼职或小时工对比不同工作机会的年化收入、面试谈薪时换算薪资水平。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="时薪转年薪,时薪计算器,小时工资换算,时薪换算年薪,年薪计算,时薪月薪换算,工资换算器,hourly to salary"),
"hourly-to-salary": dict(
 title="时薪换算器 - 小时工资转日薪/周薪/月薪/年薪 | Free ToolBase",
 desc="免费在线时薪换算器，输入时薪即可一次性换算成日薪、周薪、月薪和年薪，自动按每周工作天数和工作小时数折算，结果实时更新。适合打零工、兼职和小时工快速了解自己的月收入和年收入水平。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="时薪换算,小时工资换算,时薪转日薪,时薪转月薪,日薪换算,周薪换算,时薪换算器,工资单位换算"),
"salary-to-hourly-calculator": dict(
 title="年薪转时薪计算器 - 按年工作日折算小时工资 | Free ToolBase",
 desc="免费在线年薪转时薪计算器，输入年薪、每周工作小时数和每年工作周数，按实际工作小时数折算时薪，并显示等效的月薪和周薪。适合把年薪offer折算成小时工资、对比全职与自由职业的实际时薪。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="年薪转时薪,时薪折算,年薪换算时薪,小时工资计算,年薪折算,工资折算器,salary to hourly,年薪时薪换算"),
"salary-to-hourly": dict(
 title="月薪折算时薪计算器 - 月薪/年薪反推小时工资 | Free ToolBase",
 desc="免费在线月薪折算时薪计算器，输入年薪或月薪，按每周工作天数和每天工作小时数反推出实际时薪，支持自定义每年工作周数和综合税率。适合比较不同薪资结构的工作、评估加班是否划算、了解时间成本。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="月薪折算时薪,月薪转时薪,时薪反推,薪资折算时薪,小时工资计算器,年薪折算时薪,工资折算,月薪时薪换算"),
"annual-income-calculator": dict(
 title="年薪计算器 - 时薪/月薪/周薪/年薪互相换算 | Free ToolBase",
 desc="免费在线年薪计算器，在时薪、月薪、周薪、年薪之间任意换算，输入其中任意一项即可自动算出其余各项，支持自定义每天工作小时数和每年工作周数。适合求职时换算薪资口径、HR统一不同岗位的薪资单位。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="年薪计算器,年薪换算,月薪换算年薪,时薪换算年薪,薪资单位换算,工资换算器,年薪月薪周薪,收入换算"),
"salary-calculator": dict(
 title="薪资计算器 - 日薪/周薪/月薪/年薪单位换算 | ToolBase",
 desc="免费在线薪资计算器，在日薪、周薪、月薪、年薪之间快速换算，按每日工作小时数和每月工作日折算，支持自定义工作制。适合比较不同发薪周期的薪资、把offer折算成统一口径、了解各项薪资指标。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="薪资计算器,薪资换算,日薪换算月薪,周薪换算年薪,工资单位换算,薪资计算器在线,薪资口径换算,发薪周期换算"),
"salary-converter": dict(
 title="薪资换算器 - 时薪/月薪/年薪多币种换算 | Free ToolBase",
 desc="免费在线薪资换算器，支持时薪、日薪、周薪、月薪、年薪之间的互相换算，可切换货币单位并自定义每周工作天数和工作小时数。适合跨境电商、远程工作者换算不同币种和发薪周期的薪资水平。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="薪资换算器,薪资单位换算,多币种薪资,时薪月薪年薪换算,工资换算,薪资转换器,salary converter,薪资周期换算"),
"hourly-wage-calculator": dict(
 title="时薪工资计算器 - 按月薪和工时反算小时工资 | Free ToolBase",
 desc="免费在线时薪工资计算器，选择薪资类型后输入月薪、每周工作天数和每天工作小时数，自动算出实际时薪和日薪。适合固定月薪的上班族了解自己的折合时薪、评估加班和兼职的性价比。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="时薪工资计算器,时薪计算,小时工资计算,月薪折算时薪,时薪反算,工资折算,时薪查询,小时工资标准"),
"monthly-salary-calculator": dict(
 title="月薪计算器 - 年薪折算月薪及社保公积金扣除 | Free ToolBase",
 desc="免费在线月薪计算器，输入税前年收入并设置社保公积金比例，自动算出月薪、每月五险一金扣除额和月均到手金额。适合把年薪offer拆算成月度现金流、了解每月实际收入水平、规划月度开支。纯前端本地计算，数据不上传服务器，完全免费无需注册。",
 kw="月薪计算器,年薪折算月薪,月薪换算,社保公积金扣除,月均收入,月收入计算,年薪月薪换算,月薪明细"),
"hourly-paycheck": dict(
 title="时薪工资单计算器 - 含加班费的小时工资核算 | ToolBase",
 desc="免费在线时薪工资单计算器，输入时薪、每周工作小时数和加班小时数，按加班费率倍数计算加班工资，再扣除可选税率后算出每周实发工资。适合美国小时工核算含加班费的工资单金额、预估每期到手收入。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="时薪工资单,加班费计算,小时工资单,weekly paycheck,加班工资计算,时薪加班计算,工资单计算器,小时工工资"),
"china-salary-calculator": dict(
 title="中国工资计算器 - 五险一金与公积金比例核算 | Free ToolBase",
 desc="免费中国工资计算器，按城市类型和社保缴纳基数计算个人承担的五险一金金额，可自定义公积金比例，并展示各项扣除后的税前税后工资对比。适合了解中国社保公积金缴纳标准、核对单位缴纳基数是否合规。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="中国工资计算器,五险一金计算,社保基数,公积金比例,社保计算器,工资扣款,中国社保,工资核算"),
"gross-net-salary-calculator": dict(
 title="税前税后工资计算器 - 五险一金逐项扣除换算 | ToolBase",
 desc="免费在线税前税后工资计算器，逐项录入养老、医疗、失业、住房公积金个人承担比例，自动扣除五险一金和个税后算出实发工资，清晰展示税前到税后的完整换算过程。适合入职前估算到手工资、核对工资条各项扣款。纯前端本地计算，数据不上传服务器，无需注册。",
 kw="税前税后工资计算器,税前税后换算,gross to net,五险一金逐项,税后工资计算,实发工资,工资换算,到手工资"),
}

META_RX = re.compile(r'<meta\b[^>]*>', re.I)
TITLE_RX = re.compile(r'<title>.*?</title>', re.S)
GA_RX = re.compile(r'googletagmanager\.com/gtag/js\?id=[A-Za-z0-9\-]+')
AD_RX = re.compile(r'pl\d+\.profitableratecpmnetwork\.com')
SAFETY = [("GA加载器", GA_RX), ("广告脚本", AD_RX),
          ("canonical", re.compile(r'rel="canonical"')),
          ("JSON-LD", re.compile(r'application/ld\+json')),
          ("H1", re.compile(r'<h1')), ("script对", re.compile(r'<script'))]

# 被替换的字段(用于 mask)
MASK_TARGETS = [("name", "description"), ("property", "og:title"),
                ("property", "og:description"), ("name", "keywords")]


def set_title(html, value):
    n = len(TITLE_RX.findall(html))
    if n != 1:
        return html, n
    return TITLE_RX.sub("<title>" + value + "</title>", html, count=1), 1


def set_meta(html, kind, key, value):
    """替换 <meta kind="key" content="...">, 兼容属性顺序颠倒。返回(html, 命中数)"""
    cnt = [0]

    def _sub(m):
        tag = m.group(0)
        if not re.search(r'\b' + kind + r'\s*=\s*"' + re.escape(key) + r'"', tag, re.I):
            return tag
        cnt[0] += 1
        if cnt[0] > 1:
            return tag
        if re.search(r'\bcontent\s*=\s*"[^"]*"', tag, re.I):
            return re.sub(r'\bcontent\s*=\s*"[^"]*"',
                          lambda _: 'content="' + value + '"', tag, count=1, flags=re.I)
        return tag[:-1].rstrip() + ' content="' + value + '"/>'

    return META_RX.sub(_sub, html), cnt[0]


def mask(h):
    h = TITLE_RX.sub("<X/>", h)
    for kind, key in MASK_TARGETS:
        def _sub(m, k=kind, ky=key):
            return "<X/>" if re.search(r'\b' + k + r'\s*=\s*"' + re.escape(ky) + r'"',
                                       m.group(0), re.I) else m.group(0)
        h = META_RX.sub(_sub, h)
    return h


def build(slug):
    p = BASE + slug + "/index.html"
    old = open(p, encoding="utf-8", errors="ignore").read()
    o = OPT[slug]
    for v in (o["title"], o["desc"]):
        if '"' in v:
            return None, "值含双引号, 不安全"
    new = old
    done = []
    new, n = set_title(new, o["title"])
    if n != 1:
        return None, f"title 匹配 {n} 处 (需恰好1处)"
    done.append("title")
    for kind, key, val, req in [("name", "description", o["desc"], True),
                                ("property", "og:title", o["title"], True),
                                ("property", "og:description", o["desc"], True),
                                ("name", "keywords", o.get("kw"), False)]:
        if val is None:
            continue
        new, n = set_meta(new, kind, key, val)
        if n == 0 and not req:
            continue
        if n != 1:
            return None, f"{key} 匹配 {n} 处 (需恰好1处)"
        done.append(key)
    if new == old:
        return None, "无变化(已是目标值)"
    if mask(old) != mask(new):
        return None, "🔴铁闸失败: 非目标字段被改动"
    for name, rx in SAFETY:
        if len(rx.findall(old)) != len(rx.findall(new)):
            return None, f"🔴要害元素 {name} 数量变化"
    return new, "ok 改了 " + ",".join(done)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"
    todo = [sys.argv[2]] if mode == "--one" else list(OPT)
    ok = skip = 0
    for s in todo:
        p = BASE + s + "/index.html"
        old = open(p, encoding="utf-8", errors="ignore").read()
        new, msg = build(s)
        if new is None:
            print(f"  [跳过] {s:34s} {msg}")
            skip += 1
            continue
        if mode in ("--apply", "--one"):
            open(p, "w", encoding="utf-8").write(new)
            print(f"  [已改] {s:34s} {len(new)-len(old):+5d} 字节  {msg}")
        else:
            print(f"  [预演] {s:34s} {len(new)-len(old):+5d} 字节  {OPT[s]['title'][:56]}")
        ok += 1
    print(f"\n合计: 成功 {ok} / 跳过 {skip} / 共 {len(todo)}")


if __name__ == "__main__":
    main()

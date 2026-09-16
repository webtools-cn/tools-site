#!/usr/bin/env python3
"""tax-calculator 内容纵深 2026-09-16  (批次2: 最高杠杆页)

背景: 该页 4,802 展现/排名 7.1, 是站内第 2 大流量页。
      但内容里残留模板伪内容(「使用场景:日常工作中需要快速计算…」「工具特点」
      「税费计算器准确吗」), 且缺 Bing 排名靠前竞品都有的硬内容:
      完整税率表 / 专项附加扣除标准表 / 计算示例 / 具体 FAQ。

做法: 只替换「使用场景 + 工具特点 + 3条泛泛FAQ」这一整块模板伪内容,
      换成 7 级税率表 + 专项附加扣除标准表 + 3 个计算示例 + 6 条具体 FAQ
      + 站内相关工具内链(消除孤岛)。
      并同步扩充 FAQPage 结构化数据, 保持可见内容与 schema 一致。

安全证明: 新内容 = 原文前缀 + 新块 + 原文后缀, 前缀后缀**逐字节相同**。
          GA/广告/canonical/hreflang/script 数量零变化; JSON-LD 解析通过。

用法: --dry | --apply
"""
import json, re, sys

P = "/home/chison/tools-site/tax-calculator/index.html"

START = "<h2>使用场景</h2>"
END = ("我的数据会被记录吗？</h3><p>不会。本工具没有任何后端服务器，"
       "您输入的所有数据仅存在于浏览器内存中。</p>")

TD = 'padding:10px;color:#cbd5e1;border-bottom:1px solid rgba(148,163,184,.08)'
TH = 'padding:10px;text-align:left;border-bottom:1px solid rgba(148,163,184,.2)'
TB = ('width:100%;border-collapse:collapse;font-size:14px;background:#0f172a;'
      'border-radius:8px;overflow:hidden')

YEARS = [(1, "不超过 36,000 元", "3%", "0"),
         (2, "超过 36,000 至 144,000 元", "10%", "2,520"),
         (3, "超过 144,000 至 300,000 元", "20%", "16,920"),
         (4, "超过 300,000 至 420,000 元", "25%", "31,920"),
         (5, "超过 420,000 至 660,000 元", "30%", "52,920"),
         (6, "超过 660,000 至 960,000 元", "35%", "85,920"),
         (7, "超过 960,000 元", "45%", "181,920")]
MONTHS = [(1, "不超过 3,000 元", "3%", "0"),
          (2, "超过 3,000 至 12,000 元", "10%", "210"),
          (3, "超过 12,000 至 25,000 元", "20%", "1,410"),
          (4, "超过 25,000 至 35,000 元", "25%", "2,660"),
          (5, "超过 35,000 至 55,000 元", "30%", "4,410"),
          (6, "超过 55,000 至 80,000 元", "35%", "7,160"),
          (7, "超过 80,000 元", "45%", "15,160")]
DEDUCT = [("子女教育", "2,000 元/月/每个子女", "父母可选择由一方全额扣除或双方各扣 50%"),
          ("3 岁以下婴幼儿照护", "2,000 元/月/每个婴幼儿", "与子女教育类似，可一方全额或双方各半"),
          ("继续教育", "400 元/月 或 3,600 元/年", "学历（学位）继续教育 400 元/月（最长 48 个月）；取得职业资格证书当年 3,600 元"),
          ("大病医疗", "自负超 1.5 万元部分，年限额 8 万元", "在年度汇算清缴时扣除，不能在月度预扣时扣"),
          ("住房贷款利息", "1,000 元/月", "首套住房贷款利息，最长扣除 240 个月"),
          ("住房租金", "1,500 / 1,100 / 800 元/月", "按城市规模分档：直辖市、省会等 1,500；市辖区人口超 100 万 1,100；不超 100 万 800"),
          ("赡养老人", "3,000 元/月", "独生子女 3,000 元/月；非独生子女与兄弟姐妹分摊，每人不超过 1,500 元/月")]


def table(head, rows, widths=None):
    h = '<div style="overflow-x:auto;margin:16px 0"><table style="' + TB + '">\n<thead><tr style="background:#1e293b;color:#e2e8f0">'
    for i, c in enumerate(head):
        h += '<th style="' + TH + '">' + c + "</th>"
    h += "</tr></thead>\n<tbody>\n"
    for r in rows:
        h += "<tr>"
        for i, c in enumerate(r):
            h += '<td style="' + TD + '">' + str(c) + "</td>"
        h += "</tr>\n"
    return h + "</tbody></table></div>\n"


def build_block():
    b = ""
    b += "<h2>2026 年个人所得税税率表（综合所得）</h2>\n"
    b += ("<p>工资薪金所得适用 7 级超额累进税率。判断落在哪一级，看的是「应纳税所得额」"
          "（税前收入减掉起征点、五险一金和专项附加扣除之后的余额），不是收入本身。"
          "单位按月预扣时用月度税率表，年度汇算清缴时用年度税率表。</p>\n")
    b += "<h3>年度综合所得税率表</h3>\n"
    b += table(["级数", "全年应纳税所得额", "税率", "速算扣除数"], YEARS)
    b += "<h3>月度换算税率表（单位按月预扣用）</h3>\n"
    b += table(["级数", "月度应纳税所得额", "税率", "速算扣除数"], MONTHS)
    b += ("<p>月度级距就是把年度级距除以 12，速算扣除数同样除以 12。"
          "例如年度第 2 级「3.6 万–14.4 万、税率 10%、速算扣除数 2,520」"
          "对应月度「3,000–12,000 元、税率 10%、速算扣除数 210」（2,520 ÷ 12 = 210）。</p>\n")

    b += "<h2>专项附加扣除项目与标准</h2>\n"
    b += ("<p>专项附加扣除是 2019 年新个税法引入的减税项目，共 7 项，"
          "需要在「个人所得税」App 中自行填报后由单位按月扣除（大病医疗只在年度汇算时扣）。"
          "下表为 2023 年提高标准后的现行额度：</p>\n")
    b += table(["扣除项目", "扣除标准", "说明"], DEDUCT)

    b += "<h2>个税计算示例</h2>\n"
    b += ("<h3>示例一：月薪 10,000 元</h3>\n<p>五险一金 2,000 元、专项附加扣除 2,000 元："
          "应纳税所得额 = 10,000 − 5,000 − 2,000 − 2,000 = <strong>1,000 元</strong>，"
          "落在月度第 1 级（3%），速算扣除数 0，"
          "应缴个税 = 1,000 × 3% = <strong>30 元</strong>，到手 7,970 元。</p>\n")
    b += ("<h3>示例二：月薪 20,000 元</h3>\n<p>五险一金 4,000 元、专项附加扣除 3,000 元："
          "应纳税所得额 = 20,000 − 5,000 − 4,000 − 3,000 = <strong>8,000 元</strong>，"
          "落在月度第 2 级（10%）需减速算扣除数 210，"
          "应缴个税 = 8,000 × 10% − 210 = <strong>590 元</strong>，到手 15,410 元。</p>\n")
    b += ("<h3>示例三：月薪 50,000 元</h3>\n<p>五险一金 10,000 元、专项附加扣除 3,000 元："
          "应纳税所得额 = 50,000 − 5,000 − 10,000 − 3,000 = <strong>32,000 元</strong>，"
          "落在月度第 4 级（25%）速算扣除数 2,660，"
          "应缴个税 = 32,000 × 25% − 2,660 = <strong>5,340 元</strong>，到手 34,660 元。</p>\n")
    b += ("<p>把上面三组数字直接填进页面顶部的计算器，就能看到一模一样的应税所得额、"
          "适用税率、速算扣除数和税后工资，可以用来核对本页的算法。</p>\n")

    b += "<h2>更多常见问题</h2>\n"
    for q, a in FAQS:
        b += "<h3>" + q + "</h3>\n<p>" + a + "</p>\n"

    b += ('<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#0f172a;'
          'border-radius:8px;"><h2 style="font-size:1.1rem;margin-bottom:0.5rem;color:#e2e8f0;">'
          '🔗 相关工具推荐</h2><div style="display:flex;flex-wrap:wrap;gap:4px;">')
    for href, name in [("/tax-bracket-calculator/", "📊 个人所得税税率表计算器"),
                       ("/income-tax-calculator/", "🧾 专项附加扣除计算器"),
                       ("/chinese-tax-calculator/", "🎁 年终奖个税对比计算器"),
                       ("/payroll-tax-calculator/", "🏙️ 工资个税计算器（按城市社保）"),
                       ("/tax-refund-calculator/", "💸 个税退税计算器"),
                       ("/take-home-pay/", "💰 实发工资计算器")]:
        b += ('<a href="' + href + '" style="display:inline-block;padding:6px 12px;margin:4px;'
              'background:#0f172a;border-radius:6px;text-decoration:none;color:#22d3ee;'
              'font-size:14px;">' + name + "</a>")
    b += "</div></section>\n"
    return b


FAQS = [
 ("个人所得税起征点是多少？",
  "现行减除费用标准为 5,000 元/月（60,000 元/年）。注意这是「减除费用」，"
  "不是免税额：月收入低于 5,000 元且没有其他应纳税所得的，不需要缴纳个税；"
  "超过 5,000 元的部分还要先扣掉五险一金和专项附加扣除，剩下的余额才计税。"),
 ("2026 年个税税率表有变化吗？",
  "综合所得仍适用 7 级超额累进税率，税率区间 3%–45%，级距与速算扣除数延续现行标准，"
  "7 级分别为 3%、10%、20%、25%、30%、35%、45%。"
  "专项附加扣除额度为 2023 年提高后的标准（子女教育、3 岁以下婴幼儿照护 2,000 元/月，赡养老人 3,000 元/月）。"),
 ("五险一金可以抵个税吗？",
  "可以。个人承担的基本养老保险、基本医疗保险、失业保险和住房公积金，"
  "在计算个税前全额扣除，所以五险一金缴得多，应纳税所得额就低，个税也相应减少。"
  "单位承担的部分不影响个人个税。"),
 ("专项附加扣除需要自己申报吗？",
  "需要。必须在「个人所得税」App 中填报扣除信息，并选择由扣缴义务人（单位）按月扣除，"
  "或者留到次年 3–6 月办理年度汇算清缴时一次性扣除。"
  "没有主动填报的项目不会自动享受，这也是很多人「忘记申报导致多缴税」的主要原因。"),
 ("月薪 1 万元要交多少个税？",
  "取决于五险一金和专项附加扣除。以五险一金 2,000 元、专项附加扣除 2,000 元为例，"
  "应纳税所得额 = 10,000 − 5,000 − 2,000 − 2,000 = 1,000 元，适用 3% 税率，"
  "个税 30 元，到手 7,970 元。如果没有任何专项附加扣除，则应纳税所得额 3,000 元，个税 90 元。"),
 ("个税是按月算还是按年算？",
  "工资薪金采用「累计预扣预缴」：单位每月按累计收入减累计扣除计算应预扣税额，"
  "随着全年收入累积，适用税率会逐月爬坡，所以同样月薪下后半年的个税往往比前半年的高。"
  "年度终了后办理汇算清缴，多退少补。"),
]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"
    h = open(P, encoding="utf-8").read()

    # ── 前置断言 ──
    assert h.count(START) == 1, "起点锚点不唯一"
    assert h.count(END) == 1, "终点锚点不唯一"
    assert "相关工具推荐" not in h, "该页已有相关工具区块, 不能重复添加"
    i = h.index(START)
    j = h.index(END) + len(END)
    junk = h[i:j]
    print(f"将删除的模板伪内容: {len(junk)} 字节")
    for kw in ["使用场景", "工具特点", "税费计算器准确吗", "不需要安装插件"]:
        print(f"   含「{kw}」: {'✅' if kw in junk else '❌'}")

    block = build_block()
    new = h[:i] + block + h[j:]

    # ── 安全证明 1: 前缀/后缀逐字节相同 ──
    assert new[:i] == h[:i], "🔴前缀被改动"
    assert new[i + len(block):] == h[j:], "🔴后缀被改动"
    print("✅ 前缀/后缀逐字节不变")

    # ── 安全证明 2: 要害元素数量 ──
    for name, rx in [("GA", r'G-QVBQNJ3L5E'), ("GA加载器", r'googletagmanager\.com/gtag/js\?id='),
                     ("广告", r'profitableratecpmnetwork'), ("canonical", r'rel="canonical"'),
                     ("hreflang", r'hreflang'), ("H1", r'<h1'), ("JSON-LD", r'application/ld\+json')]:
        a, b = len(re.findall(rx, h)), len(re.findall(rx, new))
        assert a == b, f"🔴要害元素 {name} 数量变化 {a}->{b}"
    print("✅ GA/广告/canonical/hreflang/H1/JSON-LD 数量零变化")

    # ── 安全证明 3: 扩充 FAQPage schema ──
    key = '"@type":"FAQPage","mainEntity":['
    assert new.count(key) == 1, "FAQPage 锚点不唯一"
    s = new.index(key)
    e = new.index("</script>", s)
    tail = new[s:e]
    k = tail.rindex("]}")
    add = "".join(',{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                  % (json.dumps(q, ensure_ascii=False), json.dumps(
                      re.sub(r"<[^>]+>", "", a), ensure_ascii=False)) for q, a in FAQS)
    new2 = new[:s + k] + add + new[s + k:]
    # 校验 JSON-LD 仍可解析
    ld = [m.group(1) for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new2, re.S)]
    for x in ld:
        json.loads(x)
    faq = json.loads([x for x in ld if "FAQPage" in x][0])
    nq = len(faq["mainEntity"])
    print(f"✅ FAQPage 可解析, 问题数 {nq}")
    assert nq == 4 + len(FAQS), "FAQ 数量不对"
    print("✅ 前缀/后缀二次校验:", new2[:s + k].startswith(new[:s + k]) and new2[s + k + len(add):] == new[s + k:])

    if mode == "--apply":
        open(P, "w", encoding="utf-8").write(new2)
        print(f"\n[已写] {len(h)} -> {len(new2)} 字节 ({len(new2)-len(h):+d})")
    else:
        print(f"\n[预演] {len(h)} -> {len(new2)} 字节 ({len(new2)-len(h):+d})")


if __name__ == "__main__":
    main()

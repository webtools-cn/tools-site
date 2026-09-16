#!/usr/bin/env python3
"""把 tax-calculator 升级为真正的个人所得税计算器 (2026-09-16)

背景: Bing 把「个人所得税计算器」(2,927展现)「个税计算器2026」(1,580展现) 等
      99.9% 的个税词都排给了 tax-calculator, 但该页实际只做增值税含税/不含税换算,
      标题与功能不符 -> 点进来就跳出。
做法: 新增"工资薪金个税计算"主功能(2026年7级超额累进税率表), 原增值税换算保留为
      次要功能; 同步 h1/副标题/正文/FAQ/JSON-LD。
安全: 逐条断言每处替换恰好命中1次; GA/广告/canonical/hreflang/style 一个字节都不碰。
"""
import re, sys

P = "/home/chison/tools-site/tax-calculator/index.html"
h = open(P, encoding="utf-8").read()
orig = h
log = []


def rep(old, new, must=1, tag=""):
    global h
    n = h.count(old)
    assert n == must, f"[{tag}] 命中 {n} 次 (需 {must} 次)"
    h = h.replace(old, new, must)
    log.append(tag)


# ---------- 1. H1 + 副标题 ----------
rep("<h1>税费计算器</h1>", "<h1>个人所得税计算器</h1>", 1, "h1")
rep('<p class="subtitle">免费在线税费计算器，输入金额和税率自动计算含税/不含税金额。支持增值税、营业税等常见税种，适合财务人员和企业快速税务核算。...</p>',
    '<p class="subtitle">2026 年最新个人所得税计算器：输入税前月收入、五险一金和专项附加扣除，一键算出应纳税所得额、适用税率、速算扣除数、应缴个税和税后到手工资。下方另附增值税含税/不含税换算。</p>',
    1, "subtitle")

# ---------- 2. 主功能区: 个税在前, 增值税在后 ----------
OLD_MAIN = '''<div class="section">
<div class="form-group"><label>金额(元)</label><input type="number" id="v1" placeholder="如: 1000" step="any"></div>
<div class="form-group"><label>税率(%)</label><input type="number" id="v2" placeholder="如: 13" step="any"></div>
<button class="btn" onclick="calc()">🧮 计算</button>
</div>
<div class="result" id="result"><div class="val" id="rv">—</div></div>'''
NEW_MAIN = '''<div class="section">
<h2 style="font-size:1.15rem;margin-bottom:14px;color:#06b6d4">一、工资薪金个税计算</h2>
<div class="form-group"><label>税前月收入(元)</label><input type="number" id="t1" placeholder="如: 15000" step="any"></div>
<div class="form-group"><label>个人承担五险一金(元)</label><input type="number" id="t2" placeholder="如: 2500" step="any"></div>
<div class="form-group"><label>专项附加扣除合计(元)</label><input type="number" id="t3" placeholder="如: 2000" step="any"></div>
<button class="btn" onclick="calcTax()">💰 计算个税</button>
</div>
<div class="result" id="result"><div class="val" id="rv">—</div></div>
<div class="section">
<h2 style="font-size:1.15rem;margin-bottom:14px;color:#06b6d4">二、增值税含税 / 不含税换算</h2>
<div class="form-group"><label>金额(元)</label><input type="number" id="v1" placeholder="如: 1000" step="any"></div>
<div class="form-group"><label>税率(%)</label><input type="number" id="v2" placeholder="如: 13" step="any"></div>
<button class="btn" onclick="calc()">🧮 换算含税/不含税</button>
</div>
<div class="result" id="result-vat"><div class="val" id="rv-vat">—</div></div>'''
rep(OLD_MAIN, NEW_MAIN, 1, "主功能区")

# ---------- 3. JS: calc() 指向 vat, 新增 calcTax() ----------
rep("""document.getElementById('rv').innerHTML='不含税: ¥'+excl.toFixed(2)+'<br>含税: ¥'+incl.toFixed(2)+'<br>税额: ¥'+tax.toFixed(2);
document.getElementById('result').style.display='block';""",
    """document.getElementById('rv-vat').innerHTML='不含税: ¥'+excl.toFixed(2)+'<br>含税: ¥'+incl.toFixed(2)+'<br>税额: ¥'+tax.toFixed(2);
window.lastRes=document.getElementById('result-vat');
document.getElementById('result-vat').style.display='block';""",
    1, "calc()改指向")
# calc() 里旧的 rv/result 引用还在? 原文是 var 形式, 逐条确认
rep("""function calc(){""", """function calcTax(){
var inc=parseFloat(document.getElementById('t1').value);
var ins=parseFloat(document.getElementById('t2').value)||0;
var ded=parseFloat(document.getElementById('t3').value)||0;
if(isNaN(inc)||inc<0){show('请输入有效的税前月收入');return}
var base=inc-5000-ins-ded;
if(base<0)base=0;
var BR=[[3000,0.03,0],[12000,0.1,210],[25000,0.2,1410],[35000,0.25,2660],[55000,0.3,4410],[80000,0.35,7160],[Infinity,0.45,15160]];
var rate=0.03,qd=0;
for(var i=0;i<BR.length;i++){if(base<=BR[i][0]){rate=BR[i][1];qd=BR[i][2];break}}
var tax=base>0?base*rate-qd:0;
if(tax<0)tax=0;
var net=inc-ins-tax;
window.lastRes=document.getElementById('result');
document.getElementById('rv').innerHTML='应纳税所得额: ¥'+base.toFixed(2)+'<br>适用税率: '+(rate*100).toFixed(0)+'%　速算扣除数: ¥'+qd+'<br>应缴个税: ¥'+tax.toFixed(2)+'<br>税后到手: ¥'+net.toFixed(2);
document.getElementById('result').style.display='block';
}
function calc(){""", 1, "新增calcTax()")

# ---------- 4. 图表/复制 跟随最后计算的结果 ----------
rep("  var scope = document.getElementById('result') || document;",
    "  var scope = window.lastRes || document.getElementById('result') || document;", 1, "图表取lastRes")
rep("  var res=document.getElementById('result');",
    "  var res=window.lastRes||document.getElementById('result')||document.getElementById('result-vat');", 1, "复制取lastRes")

# ---------- 5. 正文/FAQ ----------
rep('<h2 style="font-size:1.3rem;margin-bottom:16px">关于 税费计算器</h2>',
    '<h2 style="font-size:1.3rem;margin-bottom:16px">关于 个人所得税计算器</h2>', 1, "关于标题")
rep('<p style="color:var(--text-secondary);line-height:1.7;margin-bottom:12px">算税费总让人头大——含税价、不含税价来回换算。只需输入金额和税率，一键算出含税/不含税金额和税额。</p>',
    '<p style="color:var(--text-secondary);line-height:1.7;margin-bottom:12px">工资条上的个税到底怎么来的？本工具按 2026 年最新个人所得税税率表计算：应纳税所得额 = 税前月收入 − 5,000 元起征点 − 五险一金 − 专项附加扣除；应缴个税 = 应纳税所得额 × 适用税率 − 速算扣除数。输入三项数据即可看到适用税率、速算扣除数、应缴个税和税后到手工资。</p>',
    1, "关于正文")
rep('<li>输入金额</li><li>输入税率百分比</li><li>点击计算查看含税价和税额</li>',
    '<li>输入税前月收入（工资、奖金等）</li><li>输入个人承担的五险一金金额</li><li>输入专项附加扣除合计（子女教育、房贷利息、赡养老人等）</li><li>点击计算，查看应纳税所得额、适用税率和税后到手工资</li><li>如需增值税换算，使用下方第二个计算区</li>',
    1, "如何使用")
rep('<h3>含税价怎么换算不含税价？</h3><p>不含税价=含税价/(1+税率)。如含税113元税率13%，不含税=113/1.13=100元。</p><h3>增值税一般税率多少？</h3><p>中国基本税率13%(货物)、9%(交通/建筑)、6%(服务业)，小规模纳税人3%。</p>',
    '<h3>个人所得税是怎么算的？</h3><p>应纳税所得额 = 税前月收入 − 5,000 元起征点 − 五险一金 − 专项附加扣除；应缴个税 = 应纳税所得额 × 适用税率 − 速算扣除数。例如税前 15,000 元、五险一金 2,500 元、专项附加扣除 2,000 元，应纳税所得额 = 5,500 元，适用 10% 税率、速算扣除数 210，个税 = 340 元，税后到手 12,160 元。</p><h3>专项附加扣除包括哪些项目？</h3><p>共 7 项：子女教育、3 岁以下婴幼儿照护、继续教育、大病医疗、住房贷款利息、住房租金、赡养老人，可在「个人所得税」App 中申报后由单位按月扣除。</p><h3>年终奖怎么计税更划算？</h3><p>年终奖可选择单独计税（奖金 ÷ 12 查月度税率表）或并入当年综合所得计税，两种方式税负可能不同，建议分别试算取较低者。</p><h3>含税价怎么换算不含税价？</h3><p>不含税价 = 含税价 ÷（1 + 税率）。如含税 113 元、税率 13%，不含税价 = 113 ÷ 1.13 = 100 元。本页下方提供增值税换算器。</p><h3>增值税一般税率是多少？</h3><p>中国现行基本税率 13%（货物）、9%（交通运输/建筑）、6%（服务业），小规模纳税人 3%。</p>',
    1, "FAQ")

rep('<h2>什么是税费计算器</h2><p>税费计算器是一款免费在线税费计算器，输入金额和税率自动计算含税/不含税金额。支持增值税、营业税等常见税种，适合财务人员和企业快速税务核算。...。无需安装或注册，输入金额、相关参数即可在浏览器中直接使用。金额、相关参数等输入仅在本地处理，不会上传到任何服务器。</p>',
    '<h2>什么是个人所得税计算器</h2><p>个人所得税计算器是一款免费在线个税计算工具，按 2026 年最新个税税率表（7 级超额累进）计算工资薪金所得应缴个税，支持扣除 5,000 元起征点、五险一金和专项附加扣除，自动给出应纳税所得额、适用税率、速算扣除数、应缴个税与税后到手工资。同时内置增值税含税/不含税换算，适合上班族核对工资条、HR 核算个税和企业财务测算用工成本。无需安装或注册，打开网页即可使用，所有输入仅在浏览器本地处理，不会上传到任何服务器。</p>',
    1, "什么是")

# ---------- 6. JSON-LD ----------
# 锚点刻意避开 @context 的 URL (读取工具会把 URL 屏蔽成 ***)
rep('"name":"税费计算器","applicationCategory":"UtilityApplication"',
    '"name":"个人所得税计算器","applicationCategory":"FinanceApplication"',
    1, "LD-SoftwareApplication")
rep('"position":2,"name":"税费计算器"',
    '"position":2,"name":"个人所得税计算器"', 1, "LD-Breadcrumb")
_new_faq = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
  '{"@type":"Question","name":"个人所得税是怎么算的？","acceptedAnswer":{"@type":"Answer","text":"应纳税所得额 = 税前月收入 − 5000 元起征点 − 五险一金 − 专项附加扣除；应缴个税 = 应纳税所得额 × 适用税率 − 速算扣除数。"}},'
  '{"@type":"Question","name":"专项附加扣除包括哪些项目？","acceptedAnswer":{"@type":"Answer","text":"共 7 项：子女教育、3 岁以下婴幼儿照护、继续教育、大病医疗、住房贷款利息、住房租金、赡养老人。"}},'
  '{"@type":"Question","name":"年终奖怎么计税更划算？","acceptedAnswer":{"@type":"Answer","text":"年终奖可单独计税（奖金÷12查月度税率表）或并入当年综合所得计税，两种方式税负可能不同，建议分别试算取低者。"}},'
  '{"@type":"Question","name":"含税价怎么换算不含税价？","acceptedAnswer":{"@type":"Answer","text":"不含税价 = 含税价 ÷（1 + 税率）。如含税 113 元、税率 13%，不含税价 = 100 元。"}}]}'
  '</script>')
_pat = re.compile(r'<script type="application/ld\+json">\{"@context":"[^"]*","@type":"FAQPage".*?\}</script>', re.S)
assert len(_pat.findall(h)) == 1, "FAQPage 块命中数 != 1"
h = _pat.sub(lambda m: _new_faq, h, count=1)
log.append("LD-FAQ")

# ---------- 安全核对 ----------
def cnt(s, rx): return len(re.findall(rx, s))
for name, rx in [("GA加载器", r'gtag/js\?id=G-QVBQNJ3L5E'), ("GA配置", r"gtag\('config','G-QVBQNJ3L5E'\)"),
                 ("广告", r'pl31040516\.profitableratecpmnetwork'), ("canonical", r'rel="canonical"'),
                 ("hreflang", r'rel="alternate" hreflang'), ("og:image", r'og:image'),
                 ("charset", r'charset="UTF-8"'), ("robots", r'name="robots"'), ("style块", r'<style>'),
                 ("</html>", r'</html>'), ("toast", r'id="toast"')]:
    a, b = cnt(orig, rx), cnt(h, rx)
    assert a == b, f"❌ {name} 数量变化 {a} -> {b}"
assert cnt(orig, r'<script') == cnt(h, r'<script'), "script 数量变化"
assert cnt(orig, r'</script>') == cnt(h, r'</script>'), "</script> 数量变化"

if len(sys.argv) > 1 and sys.argv[1] == "--apply":
    open(P, "w", encoding="utf-8").write(h)
    print("✅ 已写入")
else:
    print("✅ 预演通过 (未写入)")
print(f"   {len(orig)} → {len(h)} 字节 ({len(h)-len(orig):+d})")
print("   改动:", ", ".join(log))

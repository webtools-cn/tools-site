#!/usr/bin/env python3
"""GA/AdSense 安全修复 v3 (2026-09-15)

上一版教训: 有些页的 GA 加载器 script 标签没闭合, 业务代码被吞进去了;
           按"整块替换"处理会把业务代码删掉。本版改为**只做无损操作**。

本版只做三件事:
  A. 同长度字符串替换: 旧GA ID / 垃圾GA ID -> 正确GA ID (文件长度不变)
  B. 删除**纯加载器**的死 AdSense 块 (块内除加载器外无任何内容)
  C. 删除多余的第2+个**纯GA** script 块 (块内只有GA语句, 不含业务代码)
绝不删除任何含业务代码的块。绝不动 Adsterra / canonical / 标题 / 正文。

安全闸: 对每个改动文件, 用 mask() 抹掉全部GA/AdSense痕迹后比对,
        要求 mask(旧) == mask(新), 即**非GA内容一字未变**。

用法:
  python3 scripts/ga_fix_v3.py --test <file...>
  python3 scripts/ga_fix_v3.py --dry
  python3 scripts/ga_fix_v3.py --apply
"""
import os, re, sys, glob, collections

BASE = "/home/chison/tools-site/"
NEW_GA = "G-QVBQNJ3L5E"
OLD_GAS = ["G-9W1157EBQV", "G-XXXXXXXXXX", "G-4BZ8MD6QDM", "G-PZN7F2ESMS", "G-1RHEM5P4NK", "G-7WLERB1KHP"]
GA_SRC = "googletagmanager.com/gtag/js"

SCRIPT_RX = re.compile(r'<script\b[^>]*>.*?</script>', re.S)
GID_RX = re.compile(r'G-[A-Z0-9]{8,16}')

# 一条 GA 语句的各种写法 (分号可选, 允许换行/空格)
GA_TOKENS = [
    r'window\s*\.\s*dataLayer\s*=\s*window\s*\.\s*dataLayer\s*\|\|\s*\[\s*\]\s*;?',
    r'function\s+gtag\s*\(\s*\)\s*\{\s*dataLayer\s*\.\s*push\s*\(\s*arguments\s*\)\s*;?\s*\}\s*;?',
    r'gtag\s*\(\s*[\'"]js[\'"]\s*,\s*new\s+Date\s*\(\s*\)\s*\)\s*;?',
    r'gtag\s*\(\s*[\'"]config[\'"]\s*,[^)]*\)\s*;?',
    r'<!--[^>]*Google tag[^>]*-->',
]
TOKEN_RX = re.compile("|".join(GA_TOKENS), re.I | re.S)


def ADS_MARK(b):
    """是否是 AdSense 相关标签(两种URL形态)"""
    return ("adsbygoogle" in b) or ("googlesyndication.com/pagead/js" in b)


def inner_of(b):
    return b[b.find(">") + 1: b.rfind("</script>")]


def is_pure_ga(b):
    """块内除GA语句和空白/分号外, 什么都没有 -> 可安全删除"""
    if SCRIPT_RX.fullmatch(b) is None:
        return False
    i = inner_of(b)
    if GA_SRC in b:
        return i.strip() == ""
    if "gtag" not in b and "dataLayer" not in b:
        return re.fullmatch(r'[\s;]*', i) is not None and i.strip() != ""
    return re.fullmatch(r'[\s;]*', TOKEN_RX.sub("", i)) is not None


def mask(h):
    """抹掉全部GA/AdSense痕迹后的指纹; 用于证明非GA内容未变"""
    out, last = [], 0
    for m in SCRIPT_RX.finditer(h):
        out.append(h[last:m.start()])
        b = m.group(0)
        if ADS_MARK(b):
            i = inner_of(b)
            # 纯加载器块 -> 视同不存在(允许删除); 含内容的块 -> 保留内容受保护
            out.append("" if i.strip() == "" else "<ADSENSE-MIXED>" + i)
        elif is_pure_ga(b):
            out.append("")                                  # 纯GA块 -> 视为不存在
        else:
            t = TOKEN_RX.sub("", b)                          # 抹掉块内GA语句
            t = GID_RX.sub("<GID>", t)
            if GA_SRC in b:                                  # 标签本身也归一化
                t = re.sub(r'src="[^"]*gtag/js[^"]*"', 'src="<GASRC>"', t)
            out.append(t)
        last = m.end()
    out.append(h[last:])
    t = "".join(out)
    t = GID_RX.sub("<GID>", t)
    t = re.sub(r'ca-pub-\d+', '<PUB/>', t)
    t = re.sub(r'<script[^>]*googletagmanager[^>]*>', '<GATAG/>', t)
    t = re.sub(r'<script[^>]*adsbygoogle[^>]*>', '<ADSTAG/>', t)
    t = re.sub(r'<script[^>]*googlesyndication[^>]*>', '<ADSTAG/>', t)
    return re.sub(r'\n\s*\n', '\n', t)


def fix(h):
    if GA_SRC not in h and "gtag" not in h and "adsbygoogle" not in h and "googlesyndication" not in h:
        return h, {}
    original = h
    st = collections.Counter()
    # A. 同长度 ID 替换
    for old in OLD_GAS:
        if old in h:
            st["ID替换"] += original.count(old)
            h = h.replace(old, NEW_GA)
    # B. 清洗混在业务块里的裸 GA 片段 (该块含业务代码, 只摘掉GA语句)
    def _mixed(m):
        b = m.group(0)
        if GA_SRC in b or ADS_MARK(b) or is_pure_ga(b):
            return b
        if "dataLayer" not in b and "gtag" not in b:
            return b
        i = inner_of(b)
        if not TOKEN_RX.search(i):
            return b
        cleaned = TOKEN_RX.sub("", i)
        # 只合并空行, 且**保留下一行的缩进** (不碰任何业务代码字符)
        cleaned = re.sub(r'\n(?:[ \t]*\n)+([ \t]*)', r'\n\1', cleaned)
        st["清裸GA片段"] += 1
        return b[:b.find(">") + 1] + cleaned + "</script>"
    h = SCRIPT_RX.sub(_mixed, h)
    # B2. 删除纯加载器死 AdSense 块
    def _ads(m):
        b = m.group(0)
        if ADS_MARK(b) and inner_of(b).strip() == "":
            st["删死AdSense"] += 1
            return ""
        return b
    h = SCRIPT_RX.sub(_ads, h)
    # C. 删除多余的第2+个纯GA块 (只删可证明纯GA的)
    blocks = list(SCRIPT_RX.finditer(h))
    seen_loader = seen_cfg = 0
    edits = []
    for m in blocks:
        b = m.group(0)
        if GA_SRC in b:
            seen_loader += 1
            if seen_loader > 1 and is_pure_ga(b):
                edits.append((m.start(), m.end(), "")); st["删多余加载器"] += 1
        elif is_pure_ga(b) and ("gtag" in b or "dataLayer" in b):
            seen_cfg += 1
            if seen_cfg > 1:
                edits.append((m.start(), m.end(), "")); st["删多余配置块"] += 1
    for s, e, r in sorted(edits, key=lambda x: -x[0]):
        h = h[:s] + r + h[e:]
    if h == original:
        return original, {}
    return h, st


def all_files():
    return sorted(p for p in glob.glob(BASE + "**/*.html", recursive=True) if "/.git/" not in p)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return
    mode = args[0]
    if mode == "--test":
        for f in args[1:]:
            p = f if f.startswith("/") else BASE + f
            old = open(p, encoding="utf-8", errors="ignore").read()
            new, st = fix(old)
            same = mask(old) == mask(new)
            print(f"\n=== {f} ===")
            print(f"  操作: {dict(st) if st else '无(已合规)'}")
            print(f"  字节变化: {len(new)-len(old)}")
            print(f"  铁闸 mask(旧)==mask(新): {'✅ 通过' if same else '❌ 非GA内容被改动!'}")
            ids = GID_RX.findall(new); cfg = re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]([A-Z0-9\-]+)['\"]", new)
            print(f"  事后: config={len(cfg)} {sorted(set(cfg))} 广告保留={'profitableratecpmnetwork' in new}")
        return
    files = all_files()
    changed = 0; total = collections.Counter(); violated = []
    for p in files:
        old = open(p, encoding="utf-8", errors="ignore").read()
        new, st = fix(old)
        if new == old:
            continue
        if mask(old) != mask(new):
            violated.append(p.replace(BASE, "")); continue
        changed += 1; total.update(st)
        if mode == "--apply":
            open(p, "w", encoding="utf-8").write(new)
    print(f"{'改动文件' if mode=='--apply' else '将改动文件'} {changed}  统计: {dict(total)}")
    if violated:
        print(f"❌ 违反安全闸(已跳过) {len(violated)}: {violated[:5]}")
    else:
        print("✅ 安全闸通过: 所有改动均未触碰非GA内容")
    if mode == "--dry":
        print("(预演)")


if __name__ == "__main__":
    main()

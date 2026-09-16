#!/usr/bin/env python3
"""补齐缺失元素 v1 (2026-09-15)

只做两件事(均为纯插入, 不改动任何既有字符):
  A. 有GA加载器但缺 config 的页 -> 在加载器后插入规范 config 块
  B. 缺 Adsterra 广告脚本的页     -> 在 </head> 前插入全站统一脚本

安全闸: mask(旧)==mask(新), 其中 GA块/广告块均视为可增删, 其余内容必须一字不变。

用法: --test <file...> | --dry | --apply
"""
import re, sys, glob, collections

BASE = "/home/chison/tools-site/"
NEW_GA = "G-QVBQNJ3L5E"
LOADER = '<script async src="https://www.googletagmanager.com/gtag/js?id=' + NEW_GA + '"></script>'
CONFIG = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
          "gtag('js',new Date());gtag('config','" + NEW_GA + "');</script>")
AD = ('<script src="https://pl31040516.profitableratecpmnetwork.com/28/e9/94/'
      '28e99420b45a68504b62b54801dec958.js"></script>')

SCRIPT_RX = re.compile(r'<script\b[^>]*>.*?</script>', re.S)
GID_RX = re.compile(r'G-[A-Z0-9]{8,16}')
CFG_RX = re.compile(r"gtag\s*\(\s*['\"]config['\"]")
GA_TOKENS = [
    r'window\s*\.\s*dataLayer\s*=\s*window\s*\.\s*dataLayer\s*\|\|\s*\[\s*\]\s*;?',
    r'function\s+gtag\s*\(\s*\)\s*\{\s*dataLayer\s*\.\s*push\s*\(\s*arguments\s*\)\s*;?\s*\}\s*;?',
    r"gtag\s*\(\s*['\"]js['\"]\s*,\s*new\s+Date\s*\(\s*\)\s*\)\s*;?",
    r"gtag\s*\(\s*['\"]config['\"]\s*,[^)]*\)\s*;?",
    r'<!--[^>]*Google tag[^>]*-->',
]
TOKEN_RX = re.compile("|".join(GA_TOKENS), re.I | re.S)


def mask(h):
    """抹掉GA/广告痕迹后的指纹 (GA块与广告块视为可增删)"""
    out, last = [], 0
    for m in SCRIPT_RX.finditer(h):
        out.append(h[last:m.start()])
        b = m.group(0)
        if "profitableratecpmnetwork" in b:
            out.append("")                      # 广告块 -> 可增删
        elif "googletagmanager.com/gtag/js" in b:
            i = b[b.find(">") + 1: b.rfind("</script>")]
            out.append("" if i.strip() == "" else "<MIXED>" + i)
        elif "dataLayer" in b or CFG_RX.search(b):
            i = b[b.find(">") + 1: b.rfind("</script>")]
            rest = TOKEN_RX.sub("", i)
            out.append("" if re.fullmatch(r'[\s;]*', rest) else "<MIXED>" + i)
        else:
            t = GID_RX.sub("<GID>", b)
            t = re.sub(r'ca-pub-\d+', '<PUB/>', t)
            out.append(t)
        last = m.end()
    out.append(h[last:])
    t = "".join(out)
    t = GID_RX.sub("<GID>", t)
    t = re.sub(r'<script[^>]*googletagmanager[^>]*>', '<GATAG/>', t)
    t = re.sub(r'\n\s*\n', '\n', t)
    return t


def fix(h):
    original = h
    st = collections.Counter()
    # A. 缺 config -> 在加载器后插入
    if "googletagmanager.com/gtag/js" in h and not CFG_RX.search(h):
        mm = None
        for m in SCRIPT_RX.finditer(h):
            if "googletagmanager.com/gtag/js" in m.group(0):
                mm = m; break
        if mm:
            h = h[:mm.end()] + CONFIG + h[mm.end():]
            st["补config"] += 1
    # A2. 有 config 但缺加载器 -> 在 config 块前插入加载器
    if "googletagmanager.com/gtag/js" not in h and CFG_RX.search(h):
        mm = None
        for m in SCRIPT_RX.finditer(h):
            if CFG_RX.search(m.group(0)):
                mm = m; break
        if mm:
            h = h[:mm.start()] + LOADER + h[mm.start():]
            st["补加载器"] += 1
    # B. 缺广告 -> 在 </head> 前插入
    if "profitableratecpmnetwork" not in h and "</head>" in h:
        h = h.replace("</head>", AD + "\n</head>", 1)
        st["补广告"] += 1
    if h == original:
        return original, {}
    return h, st


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    if a[0] == "--test":
        for f in a[1:]:
            p = BASE + f
            o = open(p, encoding="utf-8", errors="ignore").read()
            n, st = fix(o)
            print(f"\n=== {f} ===\n  操作: {dict(st) or '无'}\n  字节: +{len(n)-len(o)}"
                  f"\n  铁闸: {'✅ 通过' if mask(o)==mask(n) else '❌ 失败'}")
        return
    files = sorted(p for p in glob.glob(BASE + "**/index.html", recursive=True) if "/.git/" not in p)
    ch = 0; tot = collections.Counter(); vio = []
    for p in files:
        o = open(p, encoding="utf-8", errors="ignore").read()
        n, st = fix(o)
        if n == o:
            continue
        if mask(o) != mask(n):
            vio.append(p.replace(BASE, "")); continue
        ch += 1; tot.update(st)
        if a[0] == "--apply":
            open(p, "w", encoding="utf-8").write(n)
    print(f"{'已补齐' if a[0]=='--apply' else '将补齐'} {ch} 个文件  统计: {dict(tot)}")
    print(f"❌ 违反安全闸 {len(vio)}: {vio[:5]}" if vio else "✅ 安全闸通过")


if __name__ == "__main__":
    main()

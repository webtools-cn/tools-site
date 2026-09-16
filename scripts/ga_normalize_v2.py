#!/usr/bin/env python3
"""GA 块规范化 v2 (安全版, 2026-09-15)

设计要点(吸取上一版把站改坏的教训):
  * 不用"整篇正则", 改为"逐 script 块解析", 能覆盖所有格式变体(单行/多行/引号差异)
  * 已合规页面 -> 返回 {} , 一个字节都不动
  * 顺序: 先摘完整GA块 -> 再清业务块里的裸片段 -> 最后原地重建唯一一份
  * 绝不触碰 Adsterra / AdSense / canonical / 业务逻辑 / 其它 script

用法:
  python3 scripts/ga_normalize_v2.py --test <file...>   # 沙箱测试, 不写盘
  python3 scripts/ga_normalize_v2.py --dry             # 全站预演
  python3 scripts/ga_normalize_v2.py --apply           # 全站执行
"""
import os, re, sys, glob, collections

BASE = "/home/chison/tools-site/"
NEW_GA = "G-QVBQNJ3L5E"
LOADER = ('<script async src="https://www.googletagmanager.com/gtag/js?id=' + NEW_GA + '"></script>')
CONFIG = ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
          "gtag('js',new Date());gtag('config','" + NEW_GA + "');</script>")

SCRIPT_RX = re.compile(r'<script\b[^>]*>.*?</script>', re.S)
GA_SRC_MARK = "googletagmanager.com/gtag/js"

# 一条 GA 语句的各种写法
GA_TOKENS = [
    r'window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\]\s*;',
    r'function\s+gtag\s*\(\s*\)\s*\{\s*dataLayer\.push\s*\(\s*arguments\s*\)\s*;?\s*\}',
    r'gtag\s*\(\s*[\'"]js[\'"]\s*,\s*new\s+Date\s*\(\s*\)\s*\)\s*;',
    r'gtag\s*\(\s*[\'"]config[\'"]\s*,\s*[\'"][^\'"]*[\'"]\s*\)\s*;',
    r'<!--\s*Google tag \(gtag\.js\)\s*-->',
]
TOKEN_RX = re.compile("|".join(GA_TOKENS), re.I)


def strip_ga_text(txt):
    """剥掉所有 GA 语句, 返回残留"""
    return TOKEN_RX.sub("", txt)


def is_ga_block(block, src_mark=False):
    if src_mark:
        return True
    if "dataLayer" not in block and "gtag" not in block:
        return False
    inner = block[block.find(">") + 1: block.rfind("</script>")]
    return strip_ga_text(inner).strip() == ""


def normalize(h):
    if "googletagmanager.com" not in h and "dataLayer" not in h:
        return h, {}                        # 与 GA 无关的页面, 不动
    original = h
    st = collections.Counter()
    edits = []          # (start, end, replacement)  原位替换, 保留格式
    loaders, configs, strays = [], [], []
    for m in SCRIPT_RX.finditer(h):
        b = m.group(0)
        if GA_SRC_MARK in b:
            loaders.append(m)
        elif is_ga_block(b):
            configs.append(m)
        elif "dataLayer" in b or "gtag(" in b:
            cleaned = strip_ga_text(b)
            if cleaned != b:
                strays.append((m, cleaned))
    if not loaders and not configs and not strays:
        return h, {}                                            # 已合规, 一字不动
    # 构造原位编辑(全部使用原文坐标, 从后往前应用)
    first_load_rep = LOADER
    first_cfg_rep = CONFIG
    if not loaders and not configs:
        # 两者都缺 -> 在 </head> 前插入整块
        anchor = h.find("</head>") if "</head>" in h else 0
        edits.append((anchor, anchor, LOADER + CONFIG))
        st["补整块"] += 1
    else:
        if not loaders:
            # 缺加载器 -> 让第一个配置块同时承担加载器
            first_cfg_rep = LOADER + CONFIG
            st["补加载器"] += 1
        if not configs:
            # 缺配置块 -> 让第一个加载器同时承担配置块
            first_load_rep = LOADER + CONFIG
            st["补配置块"] += 1
        for i, m in enumerate(loaders):
            edits.append((m.start(), m.end(), first_load_rep if i == 0 else ""))
            st["加载器"] += 1
        for i, m in enumerate(configs):
            edits.append((m.start(), m.end(), first_cfg_rep if i == 0 else ""))
            st["配置块"] += 1
    # 业务块里的裸 GA 片段 -> 原位清洗
    for m, cleaned in strays:
        edits.append((m.start(), m.end(), cleaned))
        st["清裸片段"] += 1
    for s, e, r in sorted(edits, key=lambda x: -x[0]):
        h = h[:s] + r + h[e:]
    if h == original:
        return original, {}                 # 内容完全等价 -> 不算改动, 不写盘
    return h, st


def verify(h):
    """检查是否恰好 1 加载器 + 1 配置 + 正确ID"""
    n_src = len(re.findall(r'googletagmanager\.com/gtag/js\?id=([A-Z0-9\-]+)', h))
    ids = re.findall(r'googletagmanager\.com/gtag/js\?id=([A-Z0-9\-]+)', h)
    cfg = re.findall(r"gtag\s*\(\s*['\"]config['\"]\s*,\s*['\"]([A-Z0-9\-]+)['\"]", h)
    stray = 0
    for m in SCRIPT_RX.finditer(h):
        b = m.group(0)
        if GA_SRC_MARK in b or is_ga_block(b):
            continue
        if strip_ga_text(b) != b:
            stray += 1
    return {"loader": len(ids), "loader_id": ids, "config": len(cfg), "config_id": cfg, "stray": stray}


def main():
    args = sys.argv[1:]
    if "--test" in args:
        for f in args[args.index("--test") + 1:]:
            p = f if os.path.isabs(f) else BASE + f
            h = open(p, encoding="utf-8", errors="ignore").read()
            new, st = normalize(h)
            print(f"\n=== {f} ===")
            print("  变更:", dict(st) or "无(已合规)")
            print("  变更字节:", len(new) - len(h))
            print("  事后校验:", verify(new))
            print("  广告脚本保留:", "profitableratecpmnetwork" in new)
            if new != h:
                open("/tmp/ga_test_out.html", "w", encoding="utf-8").write(new)
                print("  (新内容已存 /tmp/ga_test_out.html)")
        return
    if "--apply" in args or "--dry" in args:
        files = [p for p in glob.glob(BASE + "**/index.html", recursive=True)
                 if "/.git/" not in p and "/node_modules/" not in p]
        tot = collections.Counter(); n = 0
        for p in files:
            h = open(p, encoding="utf-8", errors="ignore").read()
            new, st = normalize(h)
            if not st:
                continue
            n += 1
            for k, v in st.items():
                tot[k] += v
            if "--apply" in args:
                open(p, "w", encoding="utf-8").write(new)
        print(f"改动文件 {n}  统计: {dict(tot)}")
        print("已写入" if "--apply" in args else "(预演)")
        return
    print(__doc__)


if __name__ == "__main__":
    main()

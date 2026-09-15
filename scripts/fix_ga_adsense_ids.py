#!/usr/bin/env python3
"""GA / AdSense ID 迁移: 旧废弃 ID -> 新版正确 ID (2026-09-15)

依据 STANDARD.md 第七节（项目自己的标准）:
  GA       G-9W1157EBQV            -> G-QVBQNJ3L5E
  AdSense  ca-pub-5527959372219623 -> ca-pub-5527959372219623
另外把 5 个垃圾占位 GA ID 也统一到正确 ID。

铁律: 绝不碰 Adsterra 广告脚本 / canonical / 任何其他内容。
       .md 文档不改（STANDARD.md 里旧 ID 是"已废弃"的说明，改了会毁掉文档）。

用法: python3 scripts/fix_ga_adsense_ids.py [--apply]
"""
import os, re, sys, glob, json, collections

BASE = "/home/chison/tools-site/"
OLD_GA, NEW_GA = "G-9W1157EBQV", "G-QVBQNJ3L5E"
OLD_ADS, NEW_ADS = "ca-pub-5527959372219623", "ca-pub-5527959372219623"
JUNK_GA = ["G-7WLERB1KHP", "G-XXXXXXXXXX", "G-4BZ8M6QDM", "G-PZN7F2ESMS", "G-1RHEM5P4NK"]
AD_MARK = "profitableratecpmnetwork.com"

LOADER = re.compile(r"(googletagmanager\.com/gtag/js\?id=)([A-Z0-9\-]+)")
CONFIG = re.compile(r"(gtag\(\s*['\"]config['\"]\s*,\s*['\"])([A-Z0-9\-]+)(['\"])")


def migrate_text(h):
    """返回 (新文本, 变更说明dict)"""
    st = collections.Counter()
    # 加载器 src
    def _l(m):
        if m.group(2) in (OLD_GA,) + tuple(JUNK_GA):
            st["loader"] += 1
            return m.group(1) + NEW_GA
        return m.group(0)
    h = LOADER.sub(_l, h)
    # config
    def _c(m):
        if m.group(2) in (OLD_GA,) + tuple(JUNK_GA):
            st["config"] += 1
            return m.group(1) + NEW_GA + m.group(3)
        return m.group(0)
    h = CONFIG.sub(_c, h)
    # AdSense
    n = h.count(OLD_ADS)
    if n:
        h = h.replace(OLD_ADS, NEW_ADS)
        st["adsense"] = n
    return h, st


def targets():
    # 全递归覆盖所有 index.html (含 <tool>/en/, <tool>/zh/, tools/xxx/ 等深层路径)
    html = glob.glob(BASE + "**/index.html", recursive=True)
    html = [p for p in html if "/.git/" not in p and "/node_modules/" not in p]
    scripts = []
    for ext in ("*.py", "*.sh"):
        scripts += glob.glob(BASE + ext) + glob.glob(BASE + "scripts/" + ext) \
                 + glob.glob(BASE + "_gen/" + ext)
    return sorted(set(html + scripts))


def main(apply=False):
    tot = collections.Counter()
    touched = []
    for p in targets():
        try:
            h = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        new, st = migrate_text(h)
        if not st:
            continue
        touched.append(p)
        for k, v in st.items():
            tot[k] += v
        if apply:
            open(p, "w", encoding="utf-8").write(new)
    print(f"涉及文件 {len(touched)}")
    print(f"  加载器 src 替换: {tot['loader']}")
    print(f"  config 替换:     {tot['config']}")
    print(f"  AdSense 替换:    {tot['adsense']}")
    if not apply:
        print("  (预演模式，未写入)")
    else:
        json.dump([x.replace(BASE, "") for x in touched],
                  open(BASE + ".temp/ga_migrated.json", "w"), indent=1)
        print("  已写入, 清单存 .temp/ga_migrated.json")


if __name__ == "__main__":
    main(apply="--apply" in sys.argv)

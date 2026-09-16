#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""回填 sitemap.xml 的 <lastmod> —— 让爬虫知道页面真的改过。

背景：页面改了但 sitemap 里的 <lastmod> 滞后，Google/Bing 靠 lastmod 决定
是否重抓，导致优化几周不被发现。

做法：
  1. 读 sitemap.xml，取每个 <url> 的 <loc> 与 <lastmod>
  2. 把 loc 映射回本地文件（/slug/ -> slug/index.html，/en/slug/ -> en/slug/index.html）
  3. 用一次 `git log --name-only --format=@@%cs` 建 文件 -> 最后提交日期 映射
  4. 若文件最后提交日期 **晚于** sitemap 现有 lastmod，则只替换那一处 lastmod 文本
  5. 绝不重建/重排 sitemap，绝不增删 <url> 或改 <loc>

用法:
  python3 scripts/sync_lastmod.py --dry-run   # 只打印将改动的条目
  python3 scripts/sync_lastmod.py             # 写盘
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
SP = os.path.join(ROOT, "sitemap.xml")
SITE = "https://free-toolbase.com"

BLOCK = re.compile(r"(<loc>([^<]+)</loc>\s*<lastmod>)([^<]*)(</lastmod>)")


def build_git_dates():
    """一次 git log 全量解析：文件(相对路径) -> 最后提交日期 YYYY-MM-DD。"""
    r = subprocess.run(["git", "log", "--name-only", "--format=@@%cs"],
                       cwd=ROOT, capture_output=True, text=True)
    dates = {}
    cur = None
    for line in r.stdout.splitlines():
        if line.startswith("@@"):
            cur = line[2:].strip()
        elif line.strip() and cur and line not in dates:
            dates[line] = cur
    return dates


def url_to_path(url):
    if not url.startswith(SITE):
        return None
    rel = url[len(SITE):].strip("/")
    if rel == "":
        return "index.html"
    return rel + "/index.html"


def main():
    dry = "--dry-run" in sys.argv
    raw = open(SP, encoding="utf-8").read()

    n_loc_before = raw.count("<loc>")
    n_lastmod_before = raw.count("<lastmod>")
    dates = build_git_dates()

    changes = []

    def repl(m):
        url = m.group(2).strip()
        old = m.group(3).strip()
        path = url_to_path(url)
        new = dates.get(path)
        if not new or not old:
            return m.group(0)
        if new > old:
            changes.append((url, old, new))
            return m.group(1) + new + m.group(4)
        return m.group(0)

    out = BLOCK.sub(repl, raw)

    n_loc_after = out.count("<loc>")
    n_lastmod_after = out.count("<lastmod>")
    if n_loc_after != n_loc_before or n_lastmod_after != n_lastmod_before:
        print("❌ 自检失败：<loc> 或 <lastmod> 数量变化，拒绝写盘")
        print("   loc %d->%d, lastmod %d->%d" % (n_loc_before, n_loc_after,
                                                n_lastmod_before, n_lastmod_after))
        return 1

    dist = {}
    for _, _, new in changes:
        dist[new] = dist.get(new, 0) + 1

    print("sitemap <url> 总数: %d（改动前后一致）" % n_loc_before)
    print("将更新 lastmod: %d 条" % len(changes))
    print("新日期分布:")
    for d in sorted(dist):
        print("   %s : %d" % (d, dist[d]))

    if dry:
        print("\n--dry-run 前 30 条: ")
        for url, old, new in changes[:30]:
            print("   %s  %s -> %s" % (url, old, new))
        if len(changes) > 30:
            print("   ... 另有 %d 条" % (len(changes) - 30))
        return 0

    if not changes:
        print("无需改动。")
        return 0

    open(SP, "w", encoding="utf-8").write(out)
    print("✅ 已写盘 sitemap.xml（%d 条 lastmod 更新）" % len(changes))
    return 0


if __name__ == "__main__":
    sys.exit(main())

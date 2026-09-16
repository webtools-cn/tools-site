#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git pre-commit hook —— 把本次提交改动页面的 sitemap <lastmod> 设为今天。

读取暂存区改动的 */index.html，映射成 URL，把 sitemap.xml 里对应条目的
<lastmod> 设为今天（只改文本，不重建）。若有变化则 git add sitemap.xml，
让本次提交带上。没有页面改动则原样放行。任何异常 exit 1 阻止提交。

安装: python3 scripts/install_git_hooks.py
"""
import datetime
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
os.chdir(ROOT)
SP = os.path.join(ROOT, "sitemap.xml")
SITE = "https://free-toolbase.com"

BLOCK = re.compile(r"(<loc>([^<]+)</loc>\s*<lastmod>)([^<]*)(</lastmod>)")


def page_to_url(path):
    if path == "index.html":
        return SITE + "/"
    if path.endswith("/index.html"):
        return SITE + "/" + path[: -len("index.html")]
    return None


def main():
    try:
        staged = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True).stdout.split()
    except Exception as e:
        print("❌ pre_commit_lastmod: 无法读取暂存区: %s" % e)
        return 1

    pages = [f for f in staged if f == "index.html" or f.endswith("/index.html")]
    if not pages:
        return 0

    url2page = {}
    for f in pages:
        u = page_to_url(f)
        if u:
            url2page[u] = f
    if not url2page:
        return 0

    today = datetime.date.today().isoformat()
    raw = open(SP, encoding="utf-8").read()
    changed = []

    def repl(m):
        url = m.group(2).strip()
        old = m.group(3).strip()
        if url in url2page and (not old or today > old):
            changed.append((url, old, today))
            return m.group(1) + today + m.group(4)
        return m.group(0)

    out = BLOCK.sub(repl, raw)

    if out.count("<loc>") != raw.count("<loc>") or out.count("<lastmod>") != raw.count("<lastmod>"):
        print("❌ pre_commit_lastmod: <loc>/<lastmod> 数量变化，拒绝写盘")
        return 1

    if not changed:
        print("ℹ️  pre_commit_lastmod: 本次 %d 个页面 lastmod 均为最新，无需改动" % len(url2page))
        return 0

    open(SP, "w", encoding="utf-8").write(out)
    r = subprocess.run(["git", "add", "sitemap.xml"], capture_output=True, text=True)
    if r.returncode != 0:
        print("❌ pre_commit_lastmod: git add sitemap.xml 失败")
        return 1
    print("✅ pre_commit_lastmod: %d 条 lastmod 设为 %s 并已 git add" % (len(changed), today))
    return 0


if __name__ == "__main__":
    sys.exit(main())

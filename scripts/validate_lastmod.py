#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lastmod 一致性闸门 —— 防止 sitemap 的 lastmod 落后于页面真实改动。

对 sitemap.xml 每个 URL：
  sitemap 的 lastmod 必须 >= 对应 index.html 的最后一次 git 提交日期。
不满足则打印前 30 条并 exit 1。

性能：用一次 `git log --name-only --format=@@%cs` 全量解析建映射，
绝不逐文件跑 git log（7,161 次调用会非常慢）。

用法:
  python3 scripts/validate_lastmod.py
接进 pre-commit: 见 scripts/install_git_hooks.py
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
SP = os.path.join(ROOT, "sitemap.xml")
SITE = "https://free-toolbase.com"

BLOCK = re.compile(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]*)</lastmod>", re.S)


def build_git_dates():
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
    if not os.path.exists(SP):
        print("❌ 找不到 sitemap.xml")
        return 2
    raw = open(SP, encoding="utf-8").read()
    dates = build_git_dates()

    bad = []
    checked = 0
    for m in BLOCK.finditer(raw):
        url, lm = m.group(1).strip(), m.group(2).strip()
        path = url_to_path(url)
        gd = dates.get(path) if path else None
        if not gd or not lm:
            continue
        checked += 1
        if lm < gd:
            bad.append((url, lm, gd))

    if bad:
        print("❌ lastmod 一致性闸门失败：%d/%d 条 lastmod 落后于文件提交日期" % (len(bad), checked))
        for url, lm, gd in bad[:30]:
            print("   %s  lastmod=%s < git=%s" % (url, lm, gd))
        if len(bad) > 30:
            print("   ... 共 %d 条（上面只列前 30）" % len(bad))
        print("\n修复: python3 scripts/sync_lastmod.py")
        return 1

    print("✅ lastmod 一致性闸门通过: %d 条全部 >= 对应文件最后提交日期" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git pre-commit hook —— sitemap.xml 提交闸门。

只要本次提交动了 sitemap.xml，就先跑严格校验；
发现问题先尝试自动修复（--fix），修不了就**阻止提交**。
安装: python3 scripts/install_git_hooks.py
"""
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
os.chdir(ROOT)

staged = subprocess.run(["git", "diff", "--cached", "--name-only"],
                        capture_output=True, text=True).stdout.split()

if "sitemap.xml" not in staged:
    sys.exit(0)

V = os.path.join(ROOT, "scripts", "validate_sitemap.py")
if not os.path.exists(V):
    print("⚠️  找不到 scripts/validate_sitemap.py，跳过 sitemap 校验")
    sys.exit(0)

r = subprocess.run([sys.executable, V], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout)
    print("🔧 尝试自动修复…")
    subprocess.run([sys.executable, V, "--fix"], capture_output=True, text=True)
    r2 = subprocess.run([sys.executable, V], capture_output=True, text=True)
    if r2.returncode != 0:
        print(r2.stdout)
        print("\n❌ sitemap.xml 未通过校验，禁止提交。")
        print("   修复后再 git add sitemap.xml && git commit")
        sys.exit(1)
    print("✅ 自动修复成功，重新 add sitemap.xml")
    subprocess.run(["git", "add", "sitemap.xml"])
else:
    print("✅ sitemap.xml 校验通过")

# 防止把 URL 块插到 <urlset> 外面的常见手误：提交前再确认一次
raw = open("sitemap.xml", encoding="utf-8").read()
i_set, i_url = raw.find("<urlset"), raw.find("<url>")
if i_set == -1 or (i_url != -1 and i_url < i_set):
    print("❌ 检测到 <url> 块位于 <urlset> 根元素之外，禁止提交。")
    sys.exit(1)
sys.exit(0)

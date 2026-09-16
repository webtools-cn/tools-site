#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git pre-commit hook —— 模板伪内容闸门。

只检查本次提交涉及的 index.html（快速、不影响无关页面）；
命中模板伪内容即**阻止提交并打印清单**，不做任何自动改写。

独立的全站扫描请直接运行:
    python3 scripts/validate_template_junk.py

安装: python3 scripts/install_git_hooks.py
"""
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
os.chdir(ROOT)

staged = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                        capture_output=True, text=True).stdout.split()
pages = [f for f in staged if f.endswith("index.html") and os.path.exists(f)]

if not pages:
    sys.exit(0)

V = os.path.join(ROOT, "scripts", "validate_template_junk.py")
if not os.path.exists(V):
    print("⚠️  找不到 scripts/validate_template_junk.py，跳过模板伪内容校验")
    sys.exit(0)

slugs = [f[:-len("/index.html")] for f in pages if f != "index.html"]
if "index.html" in pages:
    slugs.append(".")

r = subprocess.run([sys.executable, V] + slugs, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout)
    print("❌ 检测到模板伪内容，禁止提交。")
    print("   请人工重写这些页面的 meta description / 正文后再提交。")
    sys.exit(1)

print("✅ 模板伪内容闸门通过（本次提交 %d 个页面）" % len(pages))
sys.exit(0)

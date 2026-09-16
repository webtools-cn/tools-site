#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""post-commit 辅助脚本 —— 把本次提交改动的页面 URL 推给 IndexNow。

由 .git/hooks/post-commit 后台调用（绝不阻塞 git）。逻辑：
  1. 取本次提交改动的 index.html（CN + EN 都算）
  2. 映射成 URL，交给 scripts/indexnow_submit.py --stdin 提交
  3. 全部输出追加到 /tmp/indexnow_submit.log；任何失败只记日志

用法: python3 scripts/post_commit_indexnow.py
"""
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()
SITE = "https://free-toolbase.com"
INDEXNOW = os.path.join(ROOT, "scripts", "indexnow_submit.py")
LOG = "/tmp/indexnow_submit.log"


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg.rstrip() + "\n")


def changed_files():
    for cmd in (["git", "diff", "--name-only", "HEAD~1", "HEAD"],
                ["git", "show", "--name-only", "--format=", "HEAD"]):
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            return [x for x in r.stdout.splitlines() if x.strip()]
    return []


def file_to_url(f):
    if f == "index.html":
        return SITE + "/"
    m = re.match(r"^([^/]+)/index\.html$", f)
    if m:
        return "%s/%s/" % (SITE, m.group(1))
    m = re.match(r"^en/([^/]+)/index\.html$", f)
    if m:
        return "%s/en/%s/" % (SITE, m.group(1))
    return None


def main():
    if not os.path.exists(INDEXNOW):
        log("[indexnow] 找不到 %s，跳过" % INDEXNOW)
        return 0

    urls = []
    for f in changed_files():
        u = file_to_url(f)
        if u and u not in urls:
            urls.append(u)

    if not urls:
        log("[indexnow] 本次提交无页面改动，跳过")
        return 0

    log("[indexnow] 提交 %d 个 URL" % len(urls))
    try:
        r = subprocess.run([sys.executable, INDEXNOW, "--stdin"],
                           cwd=ROOT, input="\n".join(urls), capture_output=True,
                           text=True, timeout=20)
        log(r.stdout.strip())
        if r.stderr.strip():
            log(r.stderr.strip())
        log("[indexnow] exit=%d" % r.returncode)
    except subprocess.TimeoutExpired:
        log("[indexnow] 超时（>20s），已放弃（不影响 git）")
    except Exception as e:
        log("[indexnow] 异常: %s" % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())

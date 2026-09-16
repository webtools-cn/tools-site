#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三要素 + ID 守门尺 —— 每次改动页面后必须跑，退出码非 0 = 不合格。

用法:
  python3 scripts/validate_ids.py                 # 全站扫描
  python3 scripts/validate_ids.py <slug> [...]    # 只查指定页
  python3 scripts/validate_ids.py --diff          # 只查 git 本次改动的页

三要素（每页 <head> 内必须齐全，一个都不能丢、不能错）:
  1 GA 加载器   <script async src=".../gtag/js?id=G-QVBQNJ3L5E">
  2 GA config   gtag('config','G-QVBQNJ3L5E')
  3 Adsterra    <script src="https://pl31040516.profitableratecpmnetwork.com/...">

实现要点（血泪教训）:
  正则里**绝对不要写引号字符**（单/双引号经 shell + 文件多层转义后必然出错，
  会静默匹配失败 → 全站假阳性）。改为：先 str.find 定位标记，再对切片跑
  纯 ASCII 字符类正则取 ID。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GA = "G-QVBQNJ3L5E"
ADSTERRA_HOST = "pl31040516.profitableratecpmnetwork"
FORBIDDEN = ["G-9W1157EBQV", "G-4BZ8MD6QDM", "G-PZN7F2ESMS", "G-1RHEM5P4NK",
             "G-7WLERB1KHP", "G-XXXXXXXXXX", "ca-pub-5998441792679372"]
# 纯 ASCII，无引号 —— 取形如 G-XXXXXXXXXX 的 ID
RE_ID = re.compile(r"[A-Z]{1,2}-[A-Z0-9]{6,}")


def _id_after(text, marker, window=60):
    """在 text 中 marker 之后取第一个 GA 风格 ID。"""
    j = text.find(marker)
    if j < 0:
        return None
    m = RE_ID.search(text[j + len(marker): j + len(marker) + window])
    return m.group(0) if m else None


def check(path):
    h = open(path, encoding="utf-8", errors="ignore").read()
    i = h.find("</head>")
    head = h[:i] if i > 0 else h
    probs = []

    loader = _id_after(head, "gtag/js?id=")
    if loader is None:
        probs.append("1 缺 GA 加载器")
    elif loader != GA:
        probs.append("1 GA 加载器 ID 错误 -> %s" % loader)

    cfg = None
    for mk in ("gtag('config'", 'gtag("config"'):
        cfg = _id_after(head, mk)
        if cfg:
            break
    if cfg is None:
        probs.append("2 缺 GA config")
    elif cfg != GA:
        probs.append("2 GA config ID 错误 -> %s" % cfg)

    if ADSTERRA_HOST not in head:
        probs.append("3 缺 Adsterra 脚本")

    for b in FORBIDDEN:
        if b in head:
            probs.append("!! 残留废弃 ID -> %s" % b)
    return probs


def targets_from_args(arglist):
    out = []
    for a in arglist:
        p = os.path.join(ROOT, a.strip("/"), "index.html")
        if os.path.exists(p):
            out.append(p)
        else:
            print("warning: not found %s" % a)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--diff" in sys.argv:
        changed = subprocess.run(["git", "diff", "--name-only", "HEAD", "HEAD~1"],
                                 cwd=ROOT, capture_output=True, text=True).stdout.split()
        targets = [os.path.join(ROOT, f) for f in changed if f.endswith("index.html")]
    elif args:
        targets = targets_from_args(args)
    else:
        targets = []
        for r, d, fs in os.walk(ROOT):
            parts = r.split(os.sep)
            if ".git" in parts or "node_modules" in parts:
                continue
            if "index.html" in fs:
                targets.append(os.path.join(r, "index.html"))

    bad = []
    for p in targets:
        probs = check(p)
        if probs:
            bad.append((os.path.relpath(p, ROOT), probs))

    if not bad:
        print("PASS 三要素检查通过: %d 页全部 OK(1/2/3 齐全, ID 正确, 无废弃 ID)" % len(targets))
        return 0
    print("FAIL %d/%d 页不合格:" % (len(bad), len(targets)))
    for rel, probs in bad:
        print("   " + rel)
        for x in probs:
            print("      - " + x)
    return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🚫 模板伪内容闸门 —— 防止“机器拼接假句子”再次混入页面。

背景（AdSense 两次驳回的元凶）：
  站点曾用脚本把 title 原串塞进模板骨架，生成读起来像话、实则是机器拼凑的
  假描述。AdSense 判定为“模板伪内容（template junk）”并两次驳回。本闸门是
  **永久防线**：任何页面只要命中下列任一情况即判 FAIL，禁止提交。

判定规则（命中其一即 FAIL）:
  1. meta description 含任一模板特征串
  2. meta description 里 title 主干（`|` 前部分）重复出现 ≥2 次
  3. 可见正文含模板特征串
  4. meta description 长度 <40 或 >160（中文按字符）

用法:
  python3 scripts/validate_template_junk.py            # 全站扫描
  python3 scripts/validate_template_junk.py --list     # 只列命中清单（简洁）
  python3 scripts/validate_template_junk.py <slug> ...  # 只查指定页

退出码: 全部合格 = 0；有命中 = 1。
说明: 本脚本**不自动修改描述**（描述必须人写），只负责拦截。
安装为 git hook: python3 scripts/install_git_hooks.py
"""
import os
import re
import sys
import html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 已实测到的模板伪内容特征串（机器拼接产物，不是人写的句子）
MARKERS = [
    "快速高效地完成",
    "支持实时交互和即时结果显示",
    "适合日常办公和学习使用",
    "无需注册工具",
    "无需注册操作",
]

TAG = re.compile(r"<[^>]+>", re.S)


def strip_invisible(h: str) -> str:
    """去掉 script/style，再取纯可见文本。"""
    h = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S | re.I)
    return html.unescape(TAG.sub(" ", h))


def get_meta_content(h: str, name: str):
    """属性顺序无关地取 <meta name=... content=...> 的 content。"""
    for m in re.finditer(r"<meta\b[^>]*>", h, re.I):
        tag = m.group(0)
        nm = re.search(r"\bname\s*=\s*[\"']([^\"']*)[\"']", tag, re.I)
        if not nm or nm.group(1).strip().lower() != name:
            continue
        cm = re.search(r"\bcontent\s*=\s*(?:\"([^\"]*)\"|'([^']*)')", tag, re.S | re.I)
        if cm:
            return html.unescape(cm.group(1) if cm.group(1) is not None else cm.group(2))
    return None


def get_title(h: str) -> str:
    m = re.search(r"<title>(.*?)</title>", h, re.S | re.I)
    return html.unescape(m.group(1).strip()) if m else ""


def title_main(t: str) -> str:
    return re.sub(r"\s*-\s*Free ToolBase\s*$", "", t.split("|")[0].strip())


def check_page(path: str):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    desc = get_meta_content(raw, "description")
    desc = desc or ""
    problems = []

    hits = [k for k in MARKERS if k in desc]
    if hits:
        problems.append(("desc_marker", "描述含模板特征串: " + " / ".join(hits)))
    tm = title_main(get_title(raw))
    if len(tm) > 8 and desc.count(tm) >= 2:
        problems.append(("desc_title_dup", "描述里 title 主干重复 %d 次: %s" % (desc.count(tm), tm)))
    if len(desc) < 40:
        problems.append(("desc_short", "描述过短: %d 字符（<40）" % len(desc)))
    elif len(desc) > 160:
        problems.append(("desc_long", "描述过长: %d 字符（>160）" % len(desc)))

    visible = strip_invisible(raw)
    bhits = [k for k in MARKERS if k in visible]
    if bhits:
        problems.append(("body_marker", "正文含模板特征串: " + " / ".join(bhits)))

    return problems, desc


def collect_targets(args):
    if args:
        out = []
        for a in args:
            p = os.path.join(ROOT, a.strip("/"), "index.html")
            if os.path.exists(p):
                out.append(p)
            else:
                print("warning: not found %s" % a)
        return out
    out = []
    for r, d, fs in os.walk(ROOT):
        parts = r.split(os.sep)
        if ".git" in parts or "node_modules" in parts:
            continue
        if "index.html" in fs:
            out.append(os.path.join(r, "index.html"))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    brief = "--list" in sys.argv
    targets = collect_targets(args)

    bad = []
    for p in targets:
        problems, desc = check_page(p)
        if problems:
            bad.append((os.path.relpath(p, ROOT), problems, desc))

    if bad:
        print("FAIL 模板伪内容闸门：%d/%d 页命中:" % (len(bad), len(targets)))
        for rel, problems, desc in bad[:60]:
            print("   " + rel)
            for kind, msg in problems:
                print("      - [%s] %s" % (kind, msg))
            if not brief:
                print("      当前 desc: %s" % (desc[:160] if desc else "(空)"))
        if len(bad) > 60:
            print("   ... 共 %d 页命中（上面只列前 60）" % len(bad))
        return 1

    print("PASS 模板伪内容闸门通过: %d 页全部合格 (无特征串 / 无 title 重复 / 描述 40-160 字符)" % len(targets))
    return 0


if __name__ == "__main__":
    sys.exit(main())

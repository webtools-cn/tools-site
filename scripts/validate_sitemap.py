#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sitemap.xml 严格校验器 —— 防止"新工具脚本把 URL 块插到 <urlset> 外面"反复发作。

背景（复发事故）：
  新增工具脚本会把新 <url> 块插到 XML 声明之后、<urlset> 之前，
  导致这些块落在根元素之外 → XML 解析失败 → Google/Bing 读不了 sitemap。
  历史上多次发生，且肉眼很难发现（文件看起来"有 urlset 有 </urlset>"）。

本校验器是**唯一准入闸门**，任何改动 sitemap.xml 的流程（脚本/agent/手工）
都必须先跑它。退出码 0=通过，非 0=禁止提交。

用法:
  python3 scripts/validate_sitemap.py            # 校验
  python3 scripts/validate_sitemap.py --fix      # 尝试自动修复"块在根外"问题
安装为 git hook:
  ln -sf ../../scripts/validate_sitemap.py .git/hooks/pre-commit   (见 install_git_hooks.sh)
"""
import os, re, sys, glob
import xml.etree.ElementTree as ET

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SITE = "https://free-toolbase.com"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SP = os.path.join(ROOT, "sitemap.xml")

def is_noindex(head: str) -> bool:
    """属性顺序无关的 noindex 判定（content 可能在 name 之前）。"""
    for m in re.finditer(r"<meta\b[^>]*>", head, re.I):
        tag = m.group(0)
        if re.search(r"name\s*=\s*[\"']robots[\"']", tag, re.I) and "noindex" in tag.lower():
            return True
    return False


errors, warns = [], []


def fail(m):
    errors.append(m)


def warn(m):
    warns.append(m)


def structural_check(raw):
    """结构闸门：标签必须成套且 <urlset> 必须在第一个 <url> 之前。"""
    counts = {
        "<urlset": raw.count("<urlset"),
        "</urlset>": raw.count("</urlset>"),
        "<url>": raw.count("<url>"),
        "</url>": raw.count("</url>"),
        "<loc>": raw.count("<loc>"),
    }
    if counts["<urlset"] != 1:
        fail(f"<urlset> 开标签数量 = {counts['<urlset']}（必须恰好 1）")
    if counts["</urlset>"] != 1:
        fail(f"</urlset> 闭标签数量 = {counts['</urlset>']}（必须恰好 1）")
    if counts["<url>"] != counts["</url>"]:
        fail(f"<url>/</url> 不配对: {counts['<url>']} vs {counts['</url>']}")
    if counts["<loc>"] != counts["<url>"]:
        fail(f"<loc> 数量({counts['<loc>']}) != <url> 数量({counts['<url>']})")

    # ★ 核心闸门：第一个 <url> 必须在 <urlset> 之后
    i_set = raw.find("<urlset")
    i_url = raw.find("<url>")
    if i_set == -1:
        fail("找不到 <urlset> 根元素开标签")
    elif i_url != -1 and i_url < i_set:
        n = raw[:i_set].count("<url>")
        fail(f"🔴 有 {n} 个 <url> 块落在 <urlset> 根元素【外面】(位置 {i_url} < {i_set}) "
             f"→ 这正是历次 sitemap 损坏的根因")
    # XML 声明必须在最前
    first = raw.lstrip().split("\n", 1)[0].strip()
    if not first.startswith("<?xml"):
        fail(f"首行不是 XML 声明: {first[:60]!r}")


def auto_fix(raw):
    """把落在 <urlset> 之前的 <url> 块搬进根元素内部。"""
    i_set = raw.find("<urlset")
    i_url = raw.find("<url>")
    if i_set == -1 or i_url == -1 or i_url > i_set:
        return raw, False
    decl_end = raw.find("?>") + 2
    outside = raw[decl_end:i_set]
    line = raw[i_set:raw.find("\n", i_set)]
    rest = raw[i_set + len(line):]
    fixed = raw[:decl_end] + "\n" + line + "\n" + outside.strip("\n") + "\n" + rest.lstrip("\n")
    return fixed, True


def main():
    if not os.path.exists(SP):
        print(f"❌ 找不到 {SP}")
        return 2
    raw = open(SP, encoding="utf-8").read()

    structural_check(raw)

    if errors and "--fix" in sys.argv:
        fixed, did = auto_fix(raw)
        if did:
            open(SP, "w", encoding="utf-8").write(fixed)
            print("🔧 已自动修复（<url> 块搬回根元素内），重新校验…")
            raw = fixed
            errors.clear()
            structural_check(raw)

    if errors:
        print("❌ sitemap.xml 校验未通过：")
        for e in errors:
            print("   •", e)
        return 1

    # 解析
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        print(f"❌ XML 解析失败: {e}")
        print("   提示：多半是某个 <url> 块跑到了 <urlset> 外面 → 试 `--fix`")
        return 1
    if root.tag != f"{{{NS}}}urlset":
        print(f"❌ 根元素错误: {root.tag}（应为 {{{NS}}}urlset）")
        return 1

    urls = [c for c in root if c.tag == f"{{{NS}}}url"]
    if not urls:
        print("❌ 没有任何 <url> 条目")
        return 1

    # 每个 <url> 逐项检查
    seen, missing_files, noindex_hits, bad_lastmod, bad_order = set(), [], [], [], []
    ORDER = [f"{{{NS}}}{t}" for t in ("loc", "lastmod", "changefreq", "priority")]
    for u in urls:
        loc = u.find(f"{{{NS}}}loc")
        if loc is None or not (loc.text or "").strip():
            fail("存在没有 <loc> 的 <url>")
            continue
        url = loc.text.strip()
        if not url.startswith(SITE):
            fail(f"域名异常: {url}")
            continue
        if url in seen:
            fail(f"重复 URL: {url}")
            continue
        seen.add(url)

        tags = [c.tag for c in u]
        if tags != [t for t in ORDER if t in tags]:
            bad_order.append(url)
        lm = u.find(f"{{{NS}}}lastmod")
        if lm is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", (lm.text or "").strip()):
            bad_lastmod.append((url, lm.text))

        path = url[len(SITE):].strip("/")
        f = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
        if not os.path.exists(f):
            missing_files.append(url)
            continue
        head = open(f, encoding="utf-8", errors="ignore").read()
        if is_noindex(head):
            noindex_hits.append(url)

    if missing_files:
        fail(f"{len(missing_files)} 个 <loc> 指向不存在的文件（404 风险），例: {missing_files[:3]}")
    if noindex_hits:
        fail(f"{len(noindex_hits)} 个 URL 是 noindex 页面（不该进 sitemap），例: {noindex_hits[:3]}")
    if bad_lastmod:
        fail(f"{len(bad_lastmod)} 个 lastmod 格式非法（须 YYYY-MM-DD），例: {bad_lastmod[:2]}")
    if bad_order:
        warn(f"{len(bad_order)} 个 <url> 子标签顺序不符 XSD（应为 loc>lastmod>changefreq>priority）")

    # 完整性：可索引页面是否都在 sitemap
    seen_paths = {u[len(SITE):] for u in seen}
    for r, d, fs in os.walk(ROOT):
        if ".git" in r.split(os.sep) or "index.html" not in fs:
            continue
        p = os.path.join(r, "index.html")
        rel = "/" + os.path.relpath(p, ROOT).replace("/index.html", "").replace(os.sep, "/") + "/"
        rel = rel.replace("//", "/")
        if rel in seen_paths:
            continue
        head = open(p, encoding="utf-8", errors="ignore").read()
        if is_noindex(head):
            continue
        if "/en/" in rel[1:] and rel.count("/") > 2:   # 嵌套 en 重复路径，已知垃圾
            continue
        warn(f"可索引页面漏在 sitemap 外: {rel}")

    print(f"✅ sitemap.xml 通过校验：{len(urls)} 个 URL，唯一 {len(seen)}")
    if warns:
        print(f"⚠️  {len(warns)} 条提示：")
        for w in warns[:15]:
            print("   •", w)
        if len(warns) > 15:
            print(f"   … 另有 {len(warns)-15} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())

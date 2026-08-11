#!/usr/bin/env python3
"""Verify JS syntax (node --check) for the 8 repaired EN tool pages.

Extracts every non-JSON-LD <script> block per page and runs `node --check`.
Reports PASS/FAIL per page and totals.
"""
import os
import re
import subprocess
import sys

PAGES = [
    "en/emoji-generator/index.html",
    "en/html-to-xml/index.html",
    "en/html-validator/index.html",
    "en/image-rotator/index.html",
    "en/invoice-generator/index.html",
    "en/isometric-grid/index.html",
    "en/json-to-html-table/index.html",
    "en/json-viewer/index.html",
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = "/tmp/opencode/verify_js_syntax"


def check_page(rel):
    path = os.path.join(ROOT, rel)
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = re.findall(r"<script\b([^>]*)>([\s\S]*?)</script>", content, re.IGNORECASE)
    name = os.path.basename(os.path.dirname(rel))
    total = 0
    fails = []
    for i, (attrs, body) in enumerate(blocks):
        if "application/ld+json" in attrs.lower():
            continue
        total += 1
        fn = os.path.join(TMP, "%s_%d.js" % (name, i))
        with open(fn, "w", encoding="utf-8") as f:
            f.write(body)
        r = subprocess.run(["node", "--check", fn], capture_output=True, text=True)
        if r.returncode != 0:
            line = r.stderr.strip().splitlines()
            fails.append("  block%d: %s" % (i, line[1] if len(line) > 1 else r.stderr.strip()))
    return name, total, fails


def main():
    os.makedirs(TMP, exist_ok=True)
    results = []
    for rel in PAGES:
        name, total, fails = check_page(rel)
        results.append((name, total, fails))
    passed = 0
    failed = 0
    for name, total, fails in results:
        if fails:
            failed += 1
            print("FAIL  %s" % name)
            for f in fails:
                print(f)
        else:
            passed += 1
            print("PASS  %s (%d script block(s) OK)" % (name, total))
    print("----")
    print("PASS: %d  FAIL: %d  SKIP: 0  (total pages: %d)" % (passed, failed, len(results)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""创建目录"""
import os
TOOLS_DIR = "/home/chison/tools-site"
slugs = ["memory-game","speaker-test","latency-test","chinese-zodiac","zodiac-sign","rock-paper-scissors","would-you-rather","this-or-that","never-have-i-ever","yes-no-oracle"]
for s in slugs:
    os.makedirs(os.path.join(TOOLS_DIR, s), exist_ok=True)
    os.makedirs(os.path.join(TOOLS_DIR, "en", s), exist_ok=True)
    print(f"OK: {s}")
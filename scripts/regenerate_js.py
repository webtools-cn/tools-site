#!/usr/bin/env python3
"""批量重新生成33个彻底broken的工具 - 保留HTML结构，只替换JS"""
import subprocess, re, os, json

with open('quality-reports/acorn-errors.json') as f:
    report = json.load(f)

# 33个彻底坏了（Unexpected token，acorn解析不了）
regenerate = [
    ...[truncated]
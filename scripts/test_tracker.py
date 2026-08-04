#!/usr/bin/env python3
"""测试覆盖追踪系统 — 管理3409个工具的测试状态"""
import json, os, time, subprocess, random
from datetime import datetime

TRACK_FILE = '/home/chison/tools-site/quality/test_coverage.json'
TOOLS_DIR = '/home/chison/tools-site'

def load():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE) as f:
            return json.load(f)
    return {"last_updated": None, "tools": {}, "total_tools": 0}

def save(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(TRACK_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def scan_tools():
    """扫描所有工具目录"""
    tools = []
    for d in os.listdir(TOOLS_DIR):
        path = os.path.join(TOOLS_DIR, d, 'index.html')
        if os.path.isfile(path) and not d.startswith('.') and d not in ('css','js','scripts','quality','node_modules','en'):
            tools.append(d)
    return tools

def init():
    data = load()
    current_tools = set(scan_tools())
    
    # 去掉已删除的工具
    for t in list(data["tools"].keys()):
        if t not in current_tools:
            del data["tools"][t]
    
    # 添加新工具（未测试）
    for t in current_tools:
        if t not in data["tools"]:
            data["tools"][t] = {
                "last_test": None,
                "status": "untested",  # untested/passed/failed/fixed
                "issues_found": 0,
                "last_issue": None
            }
    
    data["total_tools"] = len(data["tools"])
    save(data)
    return data

def next_to_test():
    """选下一个要测试的工具：优先未测试的，其次最久没测的"""
    data = load()
    if not data["tools"]:
        init()
        data = load()
    
    # 优先未测试
    untested = [t for t, info in data["tools"].items() if info["status"] == "untested"]
    if untested:
        return random.choice(untested)
    
    # 最久没测的
    tested = [(t, info["last_test"] or "1970-01-01") 
              for t, info in data["tools"].items() 
              if info["status"] != "untested"]
    tested.sort(key=lambda x: x[1])
    if tested:
        return tested[0][0]
    
    return None

def mark_tested(tool, status, issues=0, issue_desc=None):
    """标记工具已测试"""
    data = load()
    if tool not in data["tools"]:
        data["tools"][tool] = {}
    
    data["tools"][tool].update({
        "last_test": datetime.now().isoformat(),
        "status": status,
        "issues_found": data["tools"][tool].get("issues_found", 0) + issues,
        "last_issue": issue_desc
    })
    save(data)

def get_stats():
    """获取覆盖统计"""
    data = load()
    total = len(data["tools"])
    untested = sum(1 for t in data["tools"].values() if t["status"] == "untested")
    passed = sum(1 for t in data["tools"].values() if t["status"] == "passed")
    failed = sum(1 for t in data["tools"].values() if t["status"] in ("failed", "fixed"))
    return {
        "total": total,
        "untested": untested,
        "tested": total - untested,
        "passed": passed,
        "failed": failed,
        "coverage": f"{(total-untested)/total*100:.1f}%" if total > 0 else "0%"
    }

if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    
    if cmd == "init":
        data = init()
        stats = get_stats()
        print(json.dumps(stats))
    elif cmd == "next":
        tool = next_to_test()
        print(tool if tool else "NONE")
    elif cmd == "mark":
        tool = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "passed"
        issues = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        desc = sys.argv[5] if len(sys.argv) > 5 else None
        mark_tested(tool, status, issues, desc)
        print(f"✅ {tool} → {status}")
    elif cmd == "stats":
        print(json.dumps(get_stats(), indent=2))

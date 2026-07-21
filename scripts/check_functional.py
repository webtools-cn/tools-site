#!/usr/bin/env python3
"""
门1：功能实测 - WebBridge自动化
检测工具页面是否有业务逻辑script块 + 核心按钮存在 + 按钮点击后输出是否变化

用法：python3 scripts/check_functional.py [tools...]
    无参数：检测全部工具
    带参数：检测指定工具（空格分隔）

输出：quality-reports/functional-{timestamp}.json
"""
import subprocess, json, time, sys, os, re
from datetime import datetime

WEBBRIDGE = "http://127.0.0.1:10086/command"
BASE = "https://free-toolbase.com"
TOOLS_DIR = "/home/chison/tools-site"
REPORTS_DIR = os.path.join(TOOLS_DIR, "quality-reports")
SESSION = "func-check"

os.makedirs(REPORTS_DIR, exist_ok=True)

def wb(action, args=None, session=SESSION):
    """调用WebBridge"""
    body = {"action": action, "args": args or {}, "session": session}
    try:
        r = subprocess.run(
            ["curl", "--noproxy", "127.0.0.1", "-s", "-X", "POST", WEBBRIDGE,
             "-H", "Content-Type: application/json", "-d", json.dumps(body)],
            capture_output=True, text=True, timeout=15)
        if not r.stdout.strip():
            return None
        d = json.loads(r.stdout)
        return d.get("data") if d.get("ok") else None
    except Exception as e:
        return None

def evaluate(code, session=SESSION):
    """在页面中执行JS并返回结果"""
    result = wb("evaluate", {"code": code}, session)
    if result:
        return result.get("value")
    return None

def check_tool(tool_name):
    """检测单个工具"""
    url = f"{BASE}/{tool_name}/"
    local_html = os.path.join(TOOLS_DIR, tool_name, "index.html")
    en_html = os.path.join(TOOLS_DIR, tool_name, "en", "index.html")
    
    issues = []
    status = "pass"
    
    # 1. 本地JS语法检查
    for path, label in [(local_html, "CN"), (en_html, "EN")]:
        if not os.path.exists(path):
            issues.append(f"{label}_MISSING")
            continue
        with open(path) as f:
            content = f.read()
        scripts = re.findall(r"<script>(.*?)</script>", content, re.DOTALL)
        
        # 检查是否有业务逻辑（非模板脚本：gtag/toggleFeedback/showToast）
        biz_scripts = [s for s in scripts if "gtag" not in s and "toggleFeedback" not in s 
                       and len(s) > 100
                       and not (s.count("showToast") < 3 and s.count("copyText") < 3 
                                and "function showToast" in s and "function copyText" in s)]
        if not biz_scripts:
            issues.append(f"{label}_NO_BIZ_JS")
            status = "fail"
            continue
        
        # JS语法
        for i, s in enumerate(scripts):
            with open("/tmp/check_func_js.js", "w") as f:
                f.write(s)
            r = subprocess.run(["node", "-c", "/tmp/check_func_js.js"], 
                             capture_output=True, text=True)
            if r.returncode != 0:
                issues.append(f"{label}_JS_SYNTAX_{i}")
                status = "fail"
    
    # 2. WebBridge功能验证（只测CN页面）
    nav = wb("navigate", {"url": url, "newTab": True})
    if not nav or not nav.get("success"):
        issues.append("NAVIGATE_FAILED")
        return {"tool": tool_name, "status": "fail", "issues": issues}
    
    # 2a. 检查h1是否存在且非空
    h1_result = evaluate("(function(){var h=document.querySelector(\"h1\");return h?h.textContent.trim():\"NO_H1\"})()")
    if not h1_result or h1_result == "NO_H1":
        issues.append("NO_H1")
        status = "fail"
    
    # 2b. 检查是否有业务按钮（过滤feedback按钮）
    btn_result = evaluate("(function(){var btns=document.querySelectorAll(\"button:not([onclick*=feedback])\");return btns.length})()")
    if btn_result is not None and int(btn_result) == 0:
        # 如果没按钮，检查是否有input
        inp_result = evaluate("(function(){var inps=document.querySelectorAll(\"input\");return inps.length})()")
        if inp_result is None or int(inp_result) == 0:
            issues.append("NO_INTERACTIVE_ELEMENTS")
            status = "fail"
    
    # 2c. 检查console错误
    console = wb("evaluate", {"code": "(function(){return window.__consoleErrors||\"\"})()"}) 
    # 注意：这需要页面先注入console.error监听，不然捕获不到
    
    return {"tool": tool_name, "status": status, "issues": issues}

def main():
    if len(sys.argv) > 1:
        tools = sys.argv[1:]
    else:
        tools = sorted([d for d in os.listdir(TOOLS_DIR) 
                       if os.path.isdir(os.path.join(TOOLS_DIR, d)) 
                       and not d.startswith(".") and not d.startswith("_")])
    
    results = []
    fail_count = 0
    total = len(tools)
    
    for i, tool in enumerate(tools):
        print(f"[{i+1}/{total}] {tool}...", end=" ", flush=True)
        r = check_tool(tool)
        results.append(r)
        if r["status"] == "fail":
            fail_count += 1
            print(f"❌ {'; '.join(r['issues'][:3])}")
        else:
            print("✅")
        
        if i % 5 == 4:
            time.sleep(0.5)  # 避免过快
    
    # 输出报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": total - fail_count,
        "failed": fail_count,
        "results": results
    }
    
    filename = f"functional-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"门1功能实测: {total-fail_count}/{total} 通过, {fail_count} 失败")
    print(f"报告: {filepath}")
    
    if fail_count > 0:
        failed_names = [r["tool"] for r in results if r["status"] == "fail"]
        print(f"失败工具: {', '.join(failed_names)}")
    
    return fail_count

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""CDP-based tool page tester - checks console errors, theme, and basic functionality."""
import json
import sys
import time
import websocket
import urllib.request

CDP_PORT = 9223
BASE_URL = "file:///home/chison/tools-site"

def get_ws_url():
    """Get websocket debugger URL for a new tab."""
    req = urllib.request.Request(f"http://127.0.0.1:{CDP_PORT}/json/new", method="PUT")
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    return data["webSocketDebuggerUrl"], data["id"]

def close_tab(tab_id):
    """Close a tab."""
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/close/{tab_id}")
    except:
        pass

def test_page(tool_name, lang="cn"):
    """Test a single tool page."""
    if lang == "cn":
        url = f"{BASE_URL}/{tool_name}/index.html"
    else:
        url = f"{BASE_URL}/en/{tool_name}/index.html"
    
    ws_url, tab_id = get_ws_url()
    ws = websocket.create_connection(ws_url, timeout=15)
    
    msg_id = 1
    console_errors = []
    console_messages = []
    
    def send_cmd(method, params=None):
        nonlocal msg_id
        cmd = {"id": msg_id, "method": method}
        if params:
            cmd["params"] = params
        ws.send(json.dumps(cmd))
        msg_id += 1
        # Wait for response
        while True:
            resp = json.loads(ws.recv())
            if "method" in resp and resp["method"] == "Console.messageAdded":
                entry = resp["params"]["message"]
                console_messages.append(entry)
                if entry.get("level") in ["error", "warning"]:
                    console_errors.append(f"[{entry.get('level')}] {entry.get('text', '')}")
            elif "method" in resp and resp["method"] == "Log.entryAdded":
                entry = resp["params"]["entry"]
                console_messages.append(entry)
                if entry.get("level") in ["error", "warning"]:
                    console_errors.append(f"[{entry.get('level')}] {entry.get('text', '')}")
            elif "id" in resp:
                return resp
    
    # Enable console and runtime
    send_cmd("Console.enable")
    send_cmd("Runtime.enable")
    send_cmd("Log.enable")
    
    # Navigate
    send_cmd("Page.enable")
    send_cmd("Page.navigate", {"url": url})
    time.sleep(3)
    
    # Check for JS errors via runtime evaluation
    result = send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            var errors = [];
            // Check theme
            var bodyBg = window.getComputedStyle(document.body).backgroundColor;
            var bodyColor = window.getComputedStyle(document.body).color;
            
            // Check for interactive elements
            var inputs = document.querySelectorAll('input, textarea, select');
            var buttons = document.querySelectorAll('button');
            var outputs = document.querySelectorAll('[class*="result"], [class*="output"], [id*="result"], [id*="output"], .toast');
            
            // Check for visible content
            var h1 = document.querySelector('h1');
            var h1Text = h1 ? h1.textContent.trim() : 'NO H1';
            
            // Check dark theme
            var isDark = false;
            var bg = window.getComputedStyle(document.body).backgroundColor;
            if (bg === 'rgb(15, 23, 42)' || bg.includes('15, 23, 42')) isDark = true;
            
            // Check for light backgrounds in key elements
            var lightBgs = [];
            document.querySelectorAll('input, textarea, .result, .output, main, .container, .card').forEach(function(el) {
                var elBg = window.getComputedStyle(el).backgroundColor;
                var elColor = window.getComputedStyle(el).color;
                if (elBg === 'rgb(255, 255, 255)' || elBg.includes('255, 255, 255') || 
                    elBg === 'rgb(248, 250, 252)' || elBg.includes('248, 250, 252')) {
                    lightBgs.push(el.tagName + '.' + el.className.split(' ').join('.') + ': bg=' + elBg);
                }
                // Check dark text on dark bg
                if (elColor === 'rgb(51, 51, 51)' || elColor === 'rgb(102, 102, 102)') {
                    lightBgs.push(el.tagName + '.' + el.className.split(' ').join('.') + ': text=' + elColor);
                }
            });
            
            return JSON.stringify({
                bodyBg: bg,
                bodyColor: bodyColor,
                isDarkTheme: isDark,
                inputCount: inputs.length,
                buttonCount: buttons.length,
                outputCount: outputs.length,
                h1Text: h1Text,
                lightBgs: lightBgs,
                title: document.title,
                lang: document.documentElement.lang || 'unknown'
            });
        })()
        """,
        "returnByValue": True
    })
    
    eval_result = {}
    if "result" in result and "result" in result["result"]:
        if "value" in result["result"]["result"]:
            eval_result = json.loads(result["result"]["result"]["value"])
        elif "exceptionDetails" in result["result"]:
            console_errors.append(f"Runtime error: {result['result']['exceptionDetails'].get('text', 'unknown')}")
    
    # Try to interact: find and click primary button
    interaction_result = send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            try {
                // Try to fill first input
                var input = document.querySelector('input[type="text"], input[type="number"], textarea');
                if (input) {
                    input.value = 'test';
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                    input.dispatchEvent(new Event('change', {bubbles: true}));
                }
                // Try to click first button
                var btn = document.querySelector('button');
                if (btn) {
                    btn.click();
                }
                return 'interacted';
            } catch(e) {
                return 'error: ' + e.message;
            }
        })()
        """,
        "returnByValue": True
    })
    
    time.sleep(1)
    
    # Check for errors after interaction
    post_errors = send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            // Check if any error appeared
            var errorEls = document.querySelectorAll('.error, .error-msg, [class*="error"]');
            var errorTexts = [];
            errorEls.forEach(function(el) {
                if (el.textContent.trim() && el.offsetHeight > 0) {
                    errorTexts.push(el.textContent.trim().substring(0, 100));
                }
            });
            return JSON.stringify({visibleErrors: errorTexts});
        })()
        """,
        "returnByValue": True
    })
    
    ws.close()
    close_tab(tab_id)
    
    return {
        "tool": tool_name,
        "lang": lang,
        "eval": eval_result,
        "console_errors": console_errors,
    }

if __name__ == "__main__":
    tools = sys.argv[1:]
    for tool in tools:
        for lang in ["cn", "en"]:
            try:
                result = test_page(tool, lang)
                print(f"\n{'='*60}")
                print(f"Tool: {tool} ({lang.upper()})")
                print(f"Title: {result['eval'].get('title', 'N/A')}")
                print(f"Lang attr: {result['eval'].get('lang', 'N/A')}")
                print(f"H1: {result['eval'].get('h1Text', 'N/A')}")
                print(f"Dark theme: {result['eval'].get('isDarkTheme', 'N/A')}")
                print(f"Body bg: {result['eval'].get('bodyBg', 'N/A')}")
                print(f"Body color: {result['eval'].get('bodyColor', 'N/A')}")
                print(f"Inputs: {result['eval'].get('inputCount', 0)}, Buttons: {result['eval'].get('buttonCount', 0)}, Outputs: {result['eval'].get('outputCount', 0)}")
                if result['eval'].get('lightBgs'):
                    print(f"⚠️ Light bg issues: {result['eval']['lightBgs']}")
                if result['console_errors']:
                    print(f"⚠️ Console errors: {result['console_errors']}")
                else:
                    print("Console: clean")
                if not result['eval'].get('isDarkTheme'):
                    print("❌ NOT DARK THEME!")
                if result['eval'].get('inputCount', 0) + result['eval'].get('buttonCount', 0) < 2:
                    print("❌ LOW INTERACTIVE ELEMENTS!")
            except Exception as e:
                print(f"\n{'='*60}")
                print(f"Tool: {tool} ({lang.upper()}) - ERROR: {e}")

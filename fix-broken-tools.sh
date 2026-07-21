#!/bin/bash
# 批量修复 broken tools 的 JS 语法错误
# 策略：提取 <script> 块中的 JS → 修复常见错误 → 语法检查 → 写回

set -e
REPORT_DIR=~/tools-site/quality-reports
ISSUES_FILE="$REPORT_DIR/current-issues.json"
FIXED_COUNT=0
FIXED_TOOLS=""
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "=== JS Syntax Fixer for Broken Tools ==="

# 提取 HTML 中所有 script 块里的 JS 内容
extract_all_js() {
    local html="$1"
    local out="$2"
    # 用 Python 提取所有 script 块（排除外部引用和 type!=text/javascript）
    python3 -c "
import sys, re
html = open('$html').read()
# 找所有 <script> 块，排除有 src 属性的
blocks = re.findall(r'<script(.*?)>(.*?)</script>', html, re.S)
for attrs, body in blocks:
    if 'src=' in attrs.lower():
        continue
    if 'application/ld+json' in attrs:
        continue
    # 合并输出
    print(body.strip())
" > "$out"
}

# 修复多行字符串中未转义的换行符
fix_newlines_in_strings() {
    local jsfile="$1"
    # 用 Python 精确修复：检测闭合引号之间的真实换行
    python3 -c "
import sys, re
js = open('$jsfile').read()

# 策略：找到每个引号包裹的字符串，如果内部有真实换行，加 \\n 转义
# 逐字符解析
result = []
i = 0
n = len(js)
while i < n:
    ch = js[i]
    if ch in '\"\\'':
        # 字符串开始
        quote = ch
        str_start = i
        result.append(ch)
        i += 1
        while i < n:
            c = js[i]
            if c == '\\\\':
                result.append(c)
                i += 1
                if i < n:
                    result.append(js[i])
                    i += 1
                continue
            if c == '\n':
                # 真实换行→转义
                result.append('\\\\n')
                i += 1
                continue
            if c == quote:
                result.append(c)
                i += 1
                break
            result.append(c)
            i += 1
    elif ch == '/' and i+1 < n and js[i+1] == '/':
        # 单行注释，跳过到行尾
        while i < n and js[i] != '\n':
            result.append(js[i])
            i += 1
        if i < n:
            result.append('\n')
            i += 1
    elif ch == '/' and i+1 < n and js[i+1] == '*':
        # 多行注释
        result.append('/*')
        i += 2
        while i+1 < n and not (js[i] == '*' and js[i+1] == '/'):
            result.append(js[i])
            i += 1
        if i+1 < n:
            result.append('*/')
            i += 2
    else:
        result.append(ch)
        i += 1

fixed = ''.join(result)
# 写入
open('$jsfile','w').write(fixed)
"
}

# 修复 unescaped newline（智能版 - 只修复真正的语法错误）
fix_js_syntax() {
    local jsfile="$1"
    local htmlfile="$2"
    
    # 先检查语法
    if node -c "$jsfile" 2>/dev/null; then
        echo "  [OK] Already valid"
        return 0
    fi
    
    # 多重修复策略
    # 1. 修复字面换行符在字符串中
    python3 -c "
import re
js = open('$jsfile').read()

# 修复：将字符串中的真实换行（不在模板字面量中）替换为 \\n
# 更安全的方法：找到所有 '...' 和 \"...\" 并修复内部换行
def fix_string_newlines(text):
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        # 检测字符串引号
        if c in '\"\\'':
            quote = c
            out.append(c)
            i += 1
            while i < n:
                c2 = text[i]
                if c2 == '\\\\':
                    out.append(c2)
                    i += 1
                    if i < n:
                        out.append(text[i])
                    i += 1
                    continue
                if c2 == quote:
                    out.append(c2)
                    i += 1
                    break
                if c2 == '\n' or c2 == '\r':
                    # 真实换行 → 转义
                    out.append('\\\\n')
                    i += 1
                    continue
                out.append(c2)
                i += 1
        # 跳过注释
        elif c == '/' and i+1 < n:
            if text[i+1] == '/':
                end = text.find('\n', i)
                if end == -1:
                    out.append(text[i:])
                    i = n
                else:
                    out.append(text[i:end+1])
                    i = end + 1
                continue
            elif text[i+1] == '*':
                end = text.find('*/', i+2)
                if end == -1:
                    out.append(text[i:])
                    i = n
                else:
                    out.append(text[i:end+2])
                    i = end + 2
                continue
            else:
                out.append(c)
                i += 1
        else:
            out.append(c)
            i += 1
    return ''.join(out)

fixed = fix_string_newlines(js)
open('$jsfile','w').write(fixed)
"
    
    # 再检查
    if node -c "$jsfile" 2>/dev/null; then
        echo "  [Fixed] newline-in-string"
        return 0
    fi
    
    # 2. 尝试修复 IIFE 不平衡
    ERROR_MSG=$(node -c "$jsfile" 2>&1 || true)
    if echo "$ERROR_MSG" | grep -qi "unexpected token.*')'\|unexpected token.*'}'"; then
        # 可能是多余的闭括号
        python3 -c "
js = open('$jsfile').read()
# 统计括号
opens = js.count('(') + js.count('{') + js.count('[')
closes = js.count(')') + js.count('}') + js.count(']')
# 如果 closes > opens，尝试去掉末尾多余闭括号
if closes > opens:
    diff = closes - opens
    fixed = js.rstrip()
    # 从末尾去掉 diff 个多余闭括号
    for _ in range(diff):
        fixed = re.sub(r'[)\}\]]\\s*$', '', fixed)
    open('$jsfile','w').write(fixed)
" 2>/dev/null || true
        
        if node -c "$jsfile" 2>/dev/null; then
            echo "  [Fixed] iife_balance"
            return 0
        fi
    fi
    
    # 3. 修复 missing ) after argument list
    if echo "$ERROR_MSG" | grep -qi "missing )"; then
        python3 -c "
import re
js = open('$jsfile').read()
# 在报错位置附近找函数调用缺闭括号
# 简单策略：补闭括号
fixed = re.sub(r'(setTimeout|setInterval|addEventListener|addEventListener)\\((.+?),\\s*(\\d+|function)', r'\1(\2, \3)', js)
open('$jsfile','w').write(fixed)
"
        if node -c "$jsfile" 2>/dev/null; then
            echo "  [Fixed] missing_paren"
            return 0
        fi
    fi

    # 4. 修复 extra_semicolon  
    if echo "$ERROR_MSG" | grep -qi "unexpected token.*';'"; then
        python3 -c "
import re
js = open('$jsfile').read()
# 修复多余分号：if 后、for 后、while 后的分号
fixed = re.sub(r'\)\\s*;\\s*;', ');', js)
open('$jsfile','w').write(fixed)
"
        if node -c "$jsfile" 2>/dev/null; then
            echo "  [Fixed] extra_semicolon"
            return 0
        fi
    fi

    # 5. 修复 missing_if_brace (unexpected else)
    if echo "$ERROR_MSG" | grep -qi "unexpected token.*'else'"; then
        python3 -c "
import re
js = open('$jsfile').read()
# 简单修复：在 else 前补 if 块
# 这个不好自动修，标记需要手动
open('$jsfile.failed','w').write('missing_if_brace')
"
        return 1
    fi

    return 1
}

# 将修复后的JS写回HTML
write_js_back() {
    local html="$1"
    local jsfile="$2"
    local out="$TMPDIR/output.html"
    
    python3 -c "
import re
html = open('$html').read()
js = open('$jsfile').read()

# 找到所有 <script> 块，按位置替换
def replace_script_blocks(html, new_js):
    # 找到所有内部 script 块
    pattern = re.compile(r'(<script(?![^>]*src=)([^>]*)>)(.*?)(</script>)', re.S)
    blocks = list(pattern.finditer(html))
    if not blocks:
        return html
    
    # 把所有JS块的内容拼接成一个
    js_parts = []
    for m in blocks:
        attrs = m.group(2)
        if 'application/ld+json' in attrs:
            js_parts.append(m.group(3))  # 保持原样
        else:
            js_parts.append(new_js)
    
    # 替换第一个非JSON script块，其余清空
    result = html
    js_idx = 0
    for m in blocks:
        attrs = m.group(2)
        body = m.group(3)
        if 'application/ld+json' in attrs:
            continue
        if js_idx == 0:
            result = result.replace(m.group(0), m.group(1) + new_js + m.group(4), 1)
        else:
            result = result.replace(m.group(0), m.group(1) + new_js + m.group(4), 1)
        js_idx += 1
    
    return result

result = replace_script_blocks(html, js)
open('$out','w').write(result)
"
    cp "$out" "$html"
}

# 主流程：逐个修复
while IFS= read -r tool; do
    HTML_FILE="$HOME/tools-site/$tool/index.html"
    if [ ! -f "$HTML_FILE" ]; then
        echo "[SKIP] $tool - no such file"
        continue
    fi
    
    echo "Processing: $tool"
    JS_FILE="$TMPDIR/$tool.js"
    extract_all_js "$HTML_FILE" "$JS_FILE"
    
    if fix_js_syntax "$JS_FILE" "$HTML_FILE"; then
        write_js_back "$HTML_FILE" "$JS_FILE"
        # 验证写入后的JS语法
        FINAL_JS="$TMPDIR/${tool}_final.js"
        extract_all_js "$HTML_FILE" "$FINAL_JS"
        if node -c "$FINAL_JS" 2>/dev/null; then
            echo "  [DONE] $tool fixed and verified"
            FIXED_TOOLS="$FIXED_TOOLS $tool"
            FIXED_COUNT=$((FIXED_COUNT + 1))
        else
            FINAL_ERR=$(node -c "$FINAL_JS" 2>&1 || true)
            echo "  [WARN] $tool: fix wrote back but still has errors: $(echo "$FINAL_ERR" | head -1)"
        fi
    else
        echo "  [FAIL] $tool - auto-fix unsuccessful"
        # 输出错误信息
        node -c "$JS_FILE" 2>&1 | head -5 || true
    fi
done < <(python3 -c "
import json
data = json.load(open('$ISSUES_FILE'))
for t in data['broken_tools_remaining']:
    print(t)
")

echo ""
echo "=== Summary ==="
echo "Fixed: $FIXED_COUNT tools"
echo "Fixed tools: $FIXED_TOOLS"

# 更新 current-issues.json
if [ "$FIXED_COUNT" -gt 0 ]; then
    python3 -c "
import json

data = json.load(open('$ISSUES_FILE'))
fixed_list = '$FIXED_TOOLS'.strip().split()
remaining = [t for t in data['broken_tools_remaining'] if t not in fixed_list]

# 重新验证剩余工具（逐个检查语法）
still_broken = []
for tool in remaining:
    import subprocess, os, re
    html = os.path.expanduser(f'~/tools-site/{tool}/index.html')
    if not os.path.exists(html):
        still_broken.append(tool)
        continue
    # 提取JS并检查
    with open(html) as f:
        content = f.read()
    js = ''
    for m in re.finditer(r'<script(.*?)>(.*?)</script>', content, re.S):
        if 'src=' in m.group(1).lower() or 'application/ld+json' in m.group(1):
            continue
        js += m.group(2).strip() + '\n'
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w', delete=False) as tmp:
        tmp.write(js)
        tmpname = tmp.name
    result = subprocess.run(['node', '-c', tmpname], capture_output=True, text=True)
    os.unlink(tmpname)
    if result.returncode != 0:
        still_broken.append(tool)

data['broken_tools_remaining'] = still_broken
data['summary']['gate0_js_syntax']['broken'] = len(still_broken)
data['summary']['gate0_js_syntax']['ok'] = data['summary']['gate0_js_syntax']['total'] - len(still_broken)
data['summary']['gate0_js_syntax']['fixed_this_run'] = data['summary']['gate0_js_syntax'].get('fixed_this_run', 0) + $FIXED_COUNT

if still_broken:
    data['urgent']['p0_blocking'] = True
    data['urgent']['reason'] = f'{len(still_broken)} tools still have JS syntax errors'
    data['urgent']['progress'] = f'{$FIXED_COUNT} fixed this run, {len(still_broken)} remaining'
else:
    data['urgent']['p0_blocking'] = False
    data['urgent']['reason'] = 'All JS syntax errors resolved'
    data['urgent']['progress'] = 'All fixed'

data['fixed_this_run'] = data.get('fixed_this_run', []) + fixed_list

open('$ISSUES_FILE','w').write(json.dumps(data, indent=2, ensure_ascii=False))
print(f'Updated {ISSUES_FILE}: {len(still_broken)} remaining, p0_blocking={data[\"urgent\"][\"p0_blocking\"]}')
" 2>&1
fi

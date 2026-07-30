#!/usr/bin/env python3
"""
修复"函数未定义"错误：从.bak文件中提取缺失的函数定义，注入到当前文件。
只处理有.bak备份的文件。
"""
import json
import os
import re
import sys

BASE = '/home/chison/tools-site'

def extract_functions_from_bak(bak_path):
    """从.bak文件提取所有function定义（仅顶层命名的function/async function）"""
    with open(bak_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取最后一个<script>块中的JS代码（通常在</body>之前）
    # 找到最后一个非schema的<script>标签
    script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    
    # 过滤掉schema（type="application/ld+json"）和短脚本
    real_scripts = []
    for s in script_blocks:
        if len(s.strip()) > 200 and 'application/ld+json' not in s and 'googletagmanager' not in s.lower():
            real_scripts.append(s)
    
    if not real_scripts:
        return None
    
    # 取最长的脚本（通常是核心工具JS）
    core_js = max(real_scripts, key=len)
    
    # 提取function定义（function name(...) 或 async function name(...)）
    func_pattern = re.findall(
        r'((?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*?(?:\{[^}]*\}[^}]*?)*\})',
        core_js
    )
    
    # 提取箭头函数赋值：var/let/const name = (...) => {...} 或 function(...){...}
    arrow_pattern = re.findall(
        r'(var|let|const)\s+(\w+)\s*=\s*(?:async\s+)?(?:function\s*\([^)]*\)\s*\{.*?\}|\([^)]*\)\s*=>\s*\{.*?\}(?:\([^)]*\))?)',
        core_js, re.DOTALL
    )
    
    # 也提取 var name = function(...){...} 模式
    var_func_pattern = re.findall(
        r'(var|let|const)\s+(\w+)\s*=\s*(?:async\s+)?function\s*\([^)]*\)\s*\{[^}]*\}',
        core_js
    )
    
    functions = set()
    for m in func_pattern:
        functions.add(m[1])  # function name
    for m in arrow_pattern:
        functions.add(m[1])
    for m in var_func_pattern:
        functions.add(m[1])
    
    return functions


def find_missing_functions(current_path, bak_path):
    """找出当前文件引用了但未定义的函数"""
    with open(current_path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(bak_path, 'r', encoding='utf-8') as f:
        bak_content = f.read()
    
    # 从当前HTML提取所有onclick/onchange等事件引用的函数
    event_funcs = set(re.findall(r'on\w+="(\w+)\s*\(', content))
    
    # 从.bak提取所有函数定义名
    bak_script_blocks = re.findall(r'<script>(.*?)</script>', bak_content, re.DOTALL)
    bak_all_js = '\n'.join([s for s in bak_script_blocks if len(s.strip()) > 200 and 'application/ld+json' not in s])
    
    # 找出.bak中定义的函数
    bak_funcs = set()
    for m in re.finditer(r'(?:async\s+)?function\s+(\w+)\s*\(', bak_all_js):
        bak_funcs.add(m.group(1))
    for m in re.finditer(r'(?:var|let|const)\s+(\w+)\s*=\s*(?:async\s+)?function', bak_all_js):
        bak_funcs.add(m.group(1))
    
    # 当前文件定义的函数
    cur_script_blocks = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    cur_all_js = '\n'.join([s for s in cur_script_blocks if len(s.strip()) > 200 and 'application/ld+json' not in s])
    cur_funcs = set()
    for m in re.finditer(r'(?:async\s+)?function\s+(\w+)\s*\(', cur_all_js):
        cur_funcs.add(m.group(1))
    for m in re.finditer(r'(?:var|let|const)\s+(\w+)\s*=\s*(?:async\s+)?function', cur_all_js):
        cur_funcs.add(m.group(1))
    
    # 缺失 = 事件引用但当前未定义，且bak中有定义
    missing = (event_funcs - cur_funcs) & bak_funcs
    
    # 排除通用函数（showToast, copyText等通常已存在）
    common = {'showToast', 'copyText', 'toggleFeedback', 'submitFeedback', 'gtag'}
    missing = missing - common
    
    return missing


def extract_function_code(bak_content, func_name):
    """从bak文件中提取指定函数的完整代码"""
    # 匹配 function funcName(...) { ... } 或 async function funcName(...) { ... }
    # 或 var/let/const funcName = function(...) { ... }
    # 或 var/let/const funcName = (...) => { ... }
    
    patterns = [
        # async function name(...) { ... }
        rf'(async\s+function\s+{func_name}\s*\([^)]*\)\s*\{{[^}}]*(?:\{{[^}}]*\}}[^}}]*)*\}})',
        # function name(...) { ... }  
        rf'(function\s+{func_name}\s*\([^)]*\)\s*\{{[^}}]*(?:\{{[^}}]*\}}[^}}]*)*\}})',
    ]
    
    for pattern in patterns:
        m = re.search(pattern, bak_content, re.DOTALL)
        if m:
            return m.group(1)
    
    # Try var/let/const assignment
    m = re.search(rf'(?:var|let|const)\s+{func_name}\s*=\s*(?:async\s+)?(?:function\s*\([^)]*\)\s*\{{[^}}]*\}}|\([^)]*\)\s*=>\s*\{{[^}}]*\}})', bak_content, re.DOTALL)
    if m:
        return m.group(0)
    
    return None


def fix_file(tool_name, dry_run=False):
    """修复单个文件的缺失函数"""
    current = os.path.join(BASE, tool_name, 'index.html')
    bak = os.path.join(BASE, tool_name, 'index.html.bak')
    
    if not os.path.exists(bak):
        return False, "no bak"
    
    missing = find_missing_functions(current, bak)
    if not missing:
        return False, "no missing funcs"
    
    with open(bak, 'r', encoding='utf-8') as f:
        bak_content = f.read()
    
    # 提取bak中所有script块的JS（非schema）
    bak_scripts = re.findall(r'<script>(.*?)</script>', bak_content, re.DOTALL)
    bak_all_js = '\n'.join([s for s in bak_scripts if len(s.strip()) > 200 and 'application/ld+json' not in s])
    
    # 收集缺失函数的代码
    func_codes = []
    for fn in sorted(missing):
        code = extract_function_code(bak_all_js, fn)
        if code:
            func_codes.append(code)
    
    if not func_codes:
        return False, "no func code extracted"
    
    if dry_run:
        return True, f"would add {len(func_codes)} funcs: {', '.join(missing)}"
    
    # 注入到当前文件：在最后一个 </script> 之前
    with open(current, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到最后一个script标签的结束位置
    last_script_end = content.rfind('</script>')
    if last_script_end == -1:
        return False, "no script tag"
    
    # 在</script>之前注入
    injection = '\n// === Auto-fixed: missing functions from backup ===\n' + '\n'.join(func_codes) + '\n'
    new_content = content[:last_script_end] + injection + content[last_script_end:]
    
    with open(current, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, f"added {len(func_codes)} funcs: {', '.join(sorted(missing))}"


def main():
    # Load failures
    with open(os.path.join(BASE, 'quality-reports/puppeteer-L0.json')) as f:
        data = json.load(f)
    
    # Get tools with 'not defined' errors
    nd_tools = [f['tool'] for f in data['failures'] if 'not defined' in f['reason']]
    
    print(f"Total 'not defined' tools: {len(nd_tools)}")
    
    fixed = []
    failed = []
    skipped = []
    
    for i, tool in enumerate(nd_tools[:20]):  # 第一批修20个
        success, msg = fix_file(tool, dry_run=False)
        if success:
            fixed.append((tool, msg))
            print(f"  ✅ {tool}: {msg}")
        elif 'no bak' in msg:
            skipped.append((tool, msg))
            print(f"  ⏭ {tool}: {msg}")
        else:
            failed.append((tool, msg))
            print(f"  ❌ {tool}: {msg}")
    
    print(f"\n=== Summary ===")
    print(f"Fixed: {len(fixed)}")
    print(f"Skipped: {len(skipped)}")
    print(f"Failed: {len(failed)}")
    
    # Write fix log
    with open(os.path.join(BASE, 'quality-reports/fix_missing_funcs.log'), 'w') as f:
        f.write(f"Fixed {len(fixed)} files:\n")
        for t, m in fixed:
            f.write(f"  {t}: {m}\n")
        f.write(f"\nSkipped {len(skipped)}:\n")
        for t, m in skipped:
            f.write(f"  {t}: {m}\n")
        f.write(f"\nFailed {len(failed)}:\n")
        for t, m in failed:
            f.write(f"  {t}: {m}\n")


if __name__ == '__main__':
    main()
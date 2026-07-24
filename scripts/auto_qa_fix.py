#!/usr/bin/env python3
"""
自动QA扫描+修复脚本 v2
- 自动修复：OG title含</h1>、h1嵌套错误、重复showToast/copyText函数
- 需手动：0交互空壳工具、invalid JSON-LD
- 跳过：分类目录页(about/contact/terms/privacy等)
"""
import os, re, sys, json
from datetime import datetime

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KANBAN_PATH = os.path.expanduser("~/.hermes/kanban/boards/tools-site-pipeline-tasks.json")

# 非工具目录
SKIP_DIRS = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git',
             'about','contact','terms','privacy'}

results = {"fixed": [], "needs_manual": [], "scanned": 0, "skipped": 0}

def get_tool_dirs():
    dirs = []
    for d in sorted(os.listdir(SITE_DIR)):
        if d in SKIP_DIRS or d.startswith('.'):
            continue
        path = os.path.join(SITE_DIR, d, 'index.html')
        if os.path.isfile(path):
            dirs.append(d)
    return dirs

def fix_og_title_h1(content):
    changed = False
    og = re.search(r'(og:title" content=")([^"]*?</h1>\s*)([^"]*?)(")', content)
    if og and og.group(3).strip():
        content = content[:og.start()] + og.group(1) + og.group(3).strip() + og.group(4) + content[og.end():]
        changed = True
    h1 = re.search(r'(<h1[^>]*>)(.*?)(</h1>\s*)(.*?)(</h1>)', content)
    if h1 and h1.group(4).strip():
        content = content[:h1.start()] + h1.group(1) + h1.group(4).strip() + h1.group(5) + content[h1.end():]
        changed = True
    return content, changed

def fix_duplicate_helpers(content):
    """删除重复的showToast/copyText函数（保留const版，删var版）"""
    changed = False
    for func_name in ['showToast', 'copyText']:
        # 找var版和const版
        var_pattern = rf'function\s+{func_name}\s*\([^)]*\)\s*\{{[^}}]*\}}'
        const_pattern = rf'(?:const|let|var)\s+{func_name}\s*=\s*(?:function|\([^)]*\)\s*=>)\s*(?:\{{[^}}]*\}}|\([^)]*\)\s*=>\s*\{{[^}}]*\}})'
        
        var_matches = list(re.finditer(var_pattern, content))
        const_matches = list(re.finditer(const_pattern, content))
        
        # 如果两种都有，删var版
        if var_matches and const_matches:
            # 从后往前删，避免偏移
            for m in reversed(var_matches):
                # 删除整行（包括前后空白和换行）
                start = content.rfind('\n', 0, m.start()) + 1
                end = content.find('\n', m.end())
                if end == -1:
                    end = m.end()
                content = content[:start] + content[end+1:]
                changed = True
    
    return content, changed

def is_empty_tool(content):
    """检查是否0交互空壳"""
    has_btn = bool(re.search(r'<button', content))
    has_submit = bool(re.search(r'type="submit"', content))
    has_onclick = bool(re.search(r'onclick', content))
    has_listener = bool(re.search(r'addEventListener', content))
    has_oninput = bool(re.search(r'oninput|onchange|onkeyup', content))
    return not any([has_btn, has_submit, has_onclick, has_listener, has_oninput])

def check_jsonld(content):
    """检查JSON-LD语法"""
    issues = []
    ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for ld in ld_matches:
        try:
            json.loads(ld.strip())
        except:
            issues.append("invalid JSON-LD")
            break
    return issues

def write_kanban_task(task):
    try:
        with open(KANBAN_PATH, 'r') as f:
            kanban = json.load(f)
        tasks = kanban.get('tasks', [])
        max_id = max([int(t['id'].replace('T','')) for t in tasks] + [0])
        task['id'] = f'T{max_id+1}'
        tasks.append(task)
        kanban['tasks'] = tasks
        col = task.get('column', 'backlog')
        if col not in kanban.get('columns', {}):
            kanban['columns'][col] = []
        if task['id'] not in kanban['columns'][col]:
            kanban['columns'][col].append(task['id'])
        with open(KANBAN_PATH, 'w') as f:
            json.dump(kanban, f, ensure_ascii=False, indent=2)
        return task['id']
    except Exception as e:
        return f"ERROR: {e}"

# === 主流程 ===
tools = get_tool_dirs()
results["scanned"] = len(tools)

for tool in tools:
    filepath = os.path.join(SITE_DIR, tool, 'index.html')
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 自动修复1: OG title + h1
    content, changed = fix_og_title_h1(content)
    if changed:
        fixes.append("og:title+h1")
    
    # 自动修复2: 重复helper函数
    content, changed = fix_duplicate_helpers(content)
    if changed:
        fixes.append("重复helper函数")
    
    # 检查: 空壳工具
    if is_empty_tool(content):
        results["needs_manual"].append({
            "tool": tool, "issue": "0交互空壳工具", "priority": "P1", "type": "fix"
        })
    
    # 检查: JSON-LD
    for issue in check_jsonld(content):
        results["needs_manual"].append({
            "tool": tool, "issue": issue, "priority": "P1", "type": "fix"
        })
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results["fixed"].append({"tool": tool, "fixes": fixes})

# 输出
print(f"扫描: {results['scanned']} 工具")
print(f"自动修复: {len(results['fixed'])} 个")
for f in results['fixed'][:10]:
    print(f"  ✅ {f['tool']}: {', '.join(f['fixes'])}")
if len(results['fixed']) > 10:
    print(f"  ... 还有 {len(results['fixed'])-10} 个")

print(f"\n需手动修复: {len(results['needs_manual'])} 个")
for m in results['needs_manual'][:20]:
    print(f"  ❌ {m['tool']}: {m['issue']} [{m['priority']}]")
if len(results['needs_manual']) > 20:
    print(f"  ... 还有 {len(results['needs_manual'])-20} 个")

# 写入看板
if results['needs_manual']:
    # 检查看板里是否已有该工具的任务，避免重复
    try:
        with open(KANBAN_PATH, 'r') as f:
            existing = json.load(f)
        existing_tools = set()
        for t in existing.get('tasks', []):
            tn = t.get('tool_name', '')
            if tn:
                existing_tools.add(tn)
    except:
        existing_tools = set()
    
    written = 0
    for m in results['needs_manual']:
        if m['tool'] in existing_tools:
            continue
        tid = write_kanban_task({
            "title": f"{m['priority']}: {m['tool']} - {m['issue']}",
            "type": m['type'], "priority": m['priority'], "column": "backlog",
            "tool_name": m['tool'], "assigned_to": "", "created_by": "auto-qa",
            "created_at": datetime.now().isoformat(),
            "checklist": {"dev": [f"修复 {m['tool']}: {m['issue']}"], "qa_test": [f"验证 {m['tool']}"]}
        })
        if not str(tid).startswith("ERROR"):
            written += 1
    print(f"\n新增看板任务: {written} 个（跳过已存在: {len(results['needs_manual'])-written}）")

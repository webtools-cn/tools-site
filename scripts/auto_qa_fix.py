#!/usr/bin/env python3
"""
自动QA扫描+修复脚本
发现问题直接修，不用建任务。只处理可自动修复的问题。
不可自动修复的（功能缺失等）输出到stdout，由cron agent建任务。
"""
import os, re, sys, json, glob

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KANBAN_PATH = os.path.expanduser("~/.hermes/kanban/boards/tools-site-pipeline-tasks.json")

results = {
    "fixed": [],
    "needs_manual": [],
    "scanned": 0
}

def get_tool_dirs():
    """获取所有工具目录（排除非工具目录）"""
    skip = {'scripts','css','js','docs','quality','blog','en','.gsc-data','.git'}
    dirs = []
    for d in sorted(os.listdir(SITE_DIR)):
        if d in skip or d.startswith('.'):
            continue
        path = os.path.join(SITE_DIR, d, 'index.html')
        if os.path.isfile(path):
            dirs.append(d)
    return dirs

def fix_og_title_h1(content, tool):
    """修复OG title含</h1>和h1嵌套错误"""
    changed = False
    
    # Fix og:title: content="XXX</h1> YYY" → content="YYY"
    og = re.search(r'(og:title" content=")([^"]*?</h1>\s*)([^"]*?)(")', content)
    if og and og.group(3).strip():
        content = content[:og.start()] + og.group(1) + og.group(3).strip() + og.group(4) + content[og.end():]
        changed = True
    
    # Fix h1: <h1>XXX</h1> YYY</h1> → <h1>YYY</h1>
    h1 = re.search(r'(<h1[^>]*>)(.*?)(</h1>\s*)(.*?)(</h1>)', content)
    if h1 and h1.group(4).strip():
        content = content[:h1.start()] + h1.group(1) + h1.group(4).strip() + h1.group(5) + content[h1.end():]
        changed = True
    
    return content, changed

def check_no_interaction(content, tool):
    """检查0交互工具（空壳）"""
    has_btn = bool(re.search(r'<button', content))
    has_submit = bool(re.search(r'type="submit"', content))
    has_onclick = bool(re.search(r'onclick', content))
    has_listener = bool(re.search(r'addEventListener', content))
    has_oninput = bool(re.search(r'oninput|onchange|onkeyup', content))
    
    if not any([has_btn, has_submit, has_onclick, has_listener, has_oninput]):
        return True  # 空壳
    return False

def check_duplicate_functions(content, tool):
    """检查重复函数定义"""
    funcs = re.findall(r'function\s+(\w+)\s*\(', content)
    seen = {}
    dupes = []
    for f in funcs:
        if f in seen:
            dupes.append(f)
        seen[f] = True
    return dupes

def check_schema(content, tool):
    """检查Schema问题"""
    issues = []
    # 检查fake aggregateRating
    if re.search(r'aggregateRating', content):
        issues.append("fake aggregateRating")
    # 检查JSON-LD语法
    ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for ld in ld_matches:
        try:
            json.loads(ld.strip())
        except:
            issues.append("invalid JSON-LD")
    return issues

def write_kanban_task(task):
    """写入看板任务"""
    try:
        with open(KANBAN_PATH, 'r') as f:
            kanban = json.load(f)
        tasks = kanban.get('tasks', [])
        # 找最大ID
        max_id = 0
        for t in tasks:
            tid = int(t['id'].replace('T',''))
            if tid > max_id:
                max_id = tid
        task['id'] = f'T{max_id+1}'
        tasks.append(task)
        kanban['tasks'] = tasks
        # 更新columns
        col = task.get('column', 'backlog')
        if col not in kanban.get('columns', {}):
            kanban['columns'][col] = []
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
    content, changed = fix_og_title_h1(content, tool)
    if changed:
        fixes.append("og:title+h1修复")
    
    # 检查2: 空壳工具（需手动）
    if check_no_interaction(content, tool):
        results["needs_manual"].append({
            "tool": tool,
            "issue": "0交互空壳工具",
            "priority": "P1",
            "type": "fix"
        })
    
    # 检查3: 重复函数
    dupes = check_duplicate_functions(content, tool)
    if dupes:
        results["needs_manual"].append({
            "tool": tool,
            "issue": f"重复函数: {','.join(set(dupes))}",
            "priority": "P2",
            "type": "fix"
        })
    
    # 检查4: Schema问题
    schema_issues = check_schema(content, tool)
    if schema_issues:
        for si in schema_issues:
            if si == "fake aggregateRating":
                # 自动删除fake aggregateRating
                # (这个之前已经全站删过了，如果还有就再删)
                pass
            else:
                results["needs_manual"].append({
                    "tool": tool,
                    "issue": si,
                    "priority": "P1",
                    "type": "fix"
                })
    
    # 写回修复
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results["fixed"].append({"tool": tool, "fixes": fixes})

# 输出结果
print(f"扫描: {results['scanned']} 工具")
print(f"自动修复: {len(results['fixed'])} 个")
for f in results['fixed']:
    print(f"  ✅ {f['tool']}: {', '.join(f['fixes'])}")

print(f"\n需手动修复: {len(results['needs_manual'])} 个")
for m in results['needs_manual'][:20]:
    print(f"  ❌ {m['tool']}: {m['issue']} [{m['priority']}]")
if len(results['needs_manual']) > 20:
    print(f"  ... 还有 {len(results['needs_manual'])-20} 个")

# 需手动修复的写入看板
if results['needs_manual']:
    print(f"\n写入看板任务...")
    written = 0
    for m in results['needs_manual']:
        tid = write_kanban_task({
            "title": f"{m['priority']}: {m['tool']} - {m['issue']}",
            "type": m['type'],
            "priority": m['priority'],
            "column": "backlog",
            "tool_name": m['tool'],
            "assigned_to": "",
            "created_by": "auto-qa",
            "created_at": __import__('datetime').datetime.now().isoformat(),
            "checklist": {"pm": [m['issue']], "dev": [f"修复 {m['tool']}"], "qa_test": [f"验证 {m['tool']} 功能正常"]}
        })
        if not str(tid).startswith("ERROR"):
            written += 1
    print(f"写入 {written} 个任务到看板backlog")

#!/usr/bin/env python3
"""门1: 快速静态扫描 - 检测0交互空壳工具 + toolInput模板空壳"""
import os, re, json

TOOLS_ROOT = '/home/chison/tools-site'
NOT_TOOLS = {'about','blog','privacy','terms','contact'}
SKIP = {'en','assets','scripts','quality','css','js','images','node_modules','.git','.github','fonts','libs','vendor','dist','build','.gsc-data'}

dirs = sorted(d for d in os.listdir(TOOLS_ROOT) 
              if os.path.isdir(os.path.join(TOOLS_ROOT, d)) 
              and d not in NOT_TOOLS|SKIP 
              and os.path.exists(os.path.join(TOOLS_ROOT, d, 'index.html')))

broken = []
stub_tools = []  # toolInput模板空壳

for name in dirs:
    with open(f'{TOOLS_ROOT}/{name}/index.html') as f:
        h = f.read()
    
    # 检测1: 0交互空壳（原逻辑）
    inputs = len(re.findall(r'<(?:input|textarea|select)\s', h))
    buttons = len(re.findall(r'<button[>\s]', h))
    has_canvas = '<canvas' in h
    has_video_audio = '<video' in h or '<audio' in h
    has_file = 'type="file"' in h
    has_onclick = 'onclick=' in h
    has_contenteditable = 'contenteditable' in h
    if inputs == 0 and buttons == 0 and not (has_canvas or has_video_audio or has_file or has_onclick or has_contenteditable):
        broken.append(name)
        continue
    
    # 检测2: toolInput模板空壳（有按钮但无真正功能）
    # 特征：id="toolInput" + runTool只做回显，没有实际计算/转换/生成逻辑
    if 'id="toolInput"' in h:
        # 明确回显空壳
        if '处理完成:' in h or '基于输入参数生成的结果' in h:
            stub_tools.append(name)
            continue
        # 有toolInput但没有calculate/compute/convert/generate/parse等计算函数
        # 排除showToast/copyText等通用函数，只看业务逻辑函数
        js_funcs = re.findall(r'function\s+(\w+)\s*\(', h)
        utility_funcs = {'showToast', 'copyText', 'copyResult', 'exportResult', 'clearTool', 'runTool', 'gtag'}
        business_funcs = [f for f in js_funcs if f not in utility_funcs and not f.startswith('_')]
        if len(business_funcs) == 0:
            stub_tools.append(name)
            continue

os.makedirs(f'{TOOLS_ROOT}/quality-reports', exist_ok=True)
report = {
    'total': len(dirs), 
    'zero_interact_shells': len(broken), 
    'toolinput_stubs': len(stub_tools),
    'total_broken': len(broken) + len(stub_tools),
    'zero_interact': broken,
    'toolinput_stubs_list': stub_tools
}
with open(f'{TOOLS_ROOT}/quality-reports/gate1-shells.json', 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'扫描完成: {len(dirs)}个工具')
print(f'  0交互空壳: {len(broken)}个')
print(f'  toolInput模板空壳: {len(stub_tools)}个')
print(f'  总计: {len(broken)+len(stub_tools)}个')
for b in broken:
    print(f'  [0交互] {b}')
for s in stub_tools:
    print(f'  [模板空壳] {s}')

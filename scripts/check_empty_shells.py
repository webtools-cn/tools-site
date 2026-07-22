#!/usr/bin/env python3
"""门1: 快速静态扫描 - 检测0交互空壳工具"""
import os, re, json

TOOLS_ROOT = '/home/chison/tools-site'
NOT_TOOLS = {'about','blog','privacy','terms','contact'}
SKIP = {'en','assets','scripts','quality','css','js','images','node_modules','.git','.github','fonts','libs','vendor','dist','build','.gsc-data'}

dirs = sorted(d for d in os.listdir(TOOLS_ROOT) 
              if os.path.isdir(os.path.join(TOOLS_ROOT, d)) 
              and d not in NOT_TOOLS|SKIP 
              and os.path.exists(os.path.join(TOOLS_ROOT, d, 'index.html')))

broken = []
for name in dirs:
    with open(f'{TOOLS_ROOT}/{name}/index.html') as f:
        h = f.read()
    inputs = len(re.findall(r'<(?:input|textarea|select)\s', h))
    buttons = len(re.findall(r'<button[>\s]', h))
    has_canvas = '<canvas' in h
    has_video_audio = '<video' in h or '<audio' in h
    has_file = 'type="file"' in h
    has_onclick = 'onclick=' in h
    has_contenteditable = 'contenteditable' in h
    if inputs == 0 and buttons == 0 and not (has_canvas or has_video_audio or has_file or has_onclick or has_contenteditable):
        broken.append(name)

os.makedirs(f'{TOOLS_ROOT}/quality-reports', exist_ok=True)
report = {'total': len(dirs), 'broken': len(broken), 'tools': broken}
with open(f'{TOOLS_ROOT}/quality-reports/gate1-shells.json', 'w') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f'扫描完成: {len(dirs)}个工具, {len(broken)}个空壳')
for b in broken:
    print(f'  {b}')
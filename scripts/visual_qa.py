#!/usr/bin/env python3
"""
真实用户验收脚本 v1.0
用Kimi WebBridge打开页面，截图，检查用户实际看到的问题
每次随机抽5个页面验收
"""
import json, random, time, os, sys

os.chdir('/home/chison/tools-site')

# 加载深度审计报告，从中抽有问题的页面
try:
    with open('quality/deep_audit_report.json', 'r') as f:
        report = json.load(f)
    problem_pages = list(report['pages'].keys())
except:
    # 没有报告就随机抽
    import glob
    problem_pages = [f.replace('/index.html','') for f in glob.glob('*/index.html') + glob.glob('en/*/index.html') if f != 'index.html']

# 随机抽5个
random.seed()
sample = random.sample(problem_pages, min(5, len(problem_pages)))

print(f'本次验收页面: {sample}')
print()

# 用Kimi WebBridge验收
import subprocess

def kimi_api(method, params=None):
    """调用Kimi WebBridge API"""
    url = 'http://127.0.0.1:10086'
    payload = {'method': method}
    if params:
        payload['params'] = params
    try:
        result = subprocess.run(
            ['curl', '-s', '-X', 'POST', url, '-H', 'Content-Type: application/json', 
             '-d', json.dumps(payload)],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(result.stdout) if result.stdout else None
    except Exception as e:
        return {'error': str(e)}

results = {}
for slug in sample:
    is_en = slug.startswith('en/')
    url = f'https://free-toolbase.com/{slug}/'
    
    print(f'验收: {slug}')
    
    # 1. 打开页面
    nav = kimi_api('navigate', {'url': url})
    if not nav or nav.get('error'):
        print(f'  ❌ 无法打开: {nav}')
        results[slug] = {'status': 'error', 'error': '无法打开'}
        continue
    
    time.sleep(2)
    
    # 2. 截图
    screenshot = kimi_api('screenshot', {'path': f'/tmp/qa_{slug.replace("/","_")}.png'})
    
    # 3. 获取页面快照
    snapshot = kimi_api('snapshot')
    
    # 4. 分析问题
    issues = []
    if snapshot and 'result' in snapshot:
        text = str(snapshot['result'])
        
        # 检查可见中文(EN页)
        if is_en:
            import re
            cn_char = re.compile(r'[\u4e00-\u9fff]')
            cn_matches = cn_char.findall(text)
            # 排除"中文"链接
            other_cn = [c for c in cn_matches if c != '中' and c != '文']
            if other_cn:
                issues.append(f'EN页面可见中文: {"".join(other_cn[:10])}')
        
        # 检查"未选择任何文件"
        if '未选择任何文件' in text:
            issues.append('EN页面文件按钮显示中文"未选择任何文件"')
        
        # 检查"intext"链接
        if 'intext' in text and is_en:
            issues.append('语言切换链接显示"intext"')
        
        # 检查空内容
        if len(text) < 100:
            issues.append('页面内容过少，可能加载失败')
    
    results[slug] = {
        'status': 'pass' if not issues else 'fail',
        'issues': issues,
        'url': url
    }
    
    icon = '✅' if not issues else '❌'
    print(f'  {icon} {len(issues)}个问题')
    for issue in issues:
        print(f'    - {issue}')
    
    # 关闭tab
    kimi_api('close_tab')
    time.sleep(1)

# 汇总
print()
print('=' * 50)
print('验收汇总:')
passed = sum(1 for r in results.values() if r['status'] == 'pass')
failed = sum(1 for r in results.values() if r['status'] == 'fail')
print(f'  通过: {passed}/{len(results)}')
print(f'  失败: {failed}/{len(results)}')

if failed > 0:
    print('\n失败页面:')
    for slug, r in results.items():
        if r['status'] == 'fail':
            print(f'  {slug}: {r["issues"]}')

# 保存结果
with open('quality/visual_qa_result.json', 'w') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f'\n结果已保存: quality/visual_qa_result.json')

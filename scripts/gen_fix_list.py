#!/usr/bin/env python3
"""Generate prioritized fix list for meta descriptions"""
import os, json
from html.parser import HTMLParser

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_desc = ''
        self.title = ''
        self.h1 = ''
        self.in_title = False
        self.in_h1 = False
        self.current_tag = ''
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta' and d.get('name','').lower() == 'description':
            self.meta_desc = d.get('content','')
        if tag == 'title':
            self.in_title = True
        if tag == 'h1':
            self.in_h1 = True
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
        if self.in_h1:
            self.h1 = data.strip()
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'h1':
            self.in_h1 = False

results = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('scripts','quality','node_modules','.gsc-data','css','js','assets','icons','images','public','tests','screenshots')]
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            try:
                with open(path) as fh:
                    parser = MetaParser()
                    parser.feed(fh.read())
                desc = parser.meta_desc
                if desc:
                    length = len(desc)
                    # Check for repetition
                    rep_count = desc.count('纯前端本地处理') + desc.count('数据不上传服务器') + desc.count('无需注册完全免费')
                    issues = []
                    if length < 100:
                        issues.append('TOO_SHORT')
                    elif length > 165:
                        issues.append('TOO_LONG')
                    if rep_count > 1:
                        issues.append('REPETITIVE')
                    if issues:
                        results.append({
                            'path': path,
                            'length': length,
                            'issues': issues,
                            'desc': desc,
                            'title': parser.title,
                            'h1': parser.h1,
                        })
            except Exception as e:
                pass

# Sort by severity
def sev_key(item):
    issues = item['issues']
    if 'TOO_SHORT' in issues: return 0
    if 'TOO_LONG' in issues and 'REPETITIVE' in issues: return 1
    if 'TOO_LONG' in issues: return 2
    if 'REPETITIVE' in issues: return 3
    return 4

results.sort(key=sev_key)

# Split into batches of 30
batches = []
for i in range(0, len(results), 30):
    batches.append(results[i:i+30])

print('Total pages needing fixes: %d' % len(results))
print('Batches: %d' % len(batches))
print()

# Show batch 1 summary
print('=== BATCH 1 (first %d pages) ===' % min(30, len(results)))
for item in results[:30]:
    issue_str = ','.join(item['issues'])
    print('[%s] %s (%dch)' % (issue_str, item['path'], item['length']))
    print('  Title: %s' % (item['h1'] or item['title'] or 'N/A'))
    print('  Current: %s' % item['desc'][:100])

# Save full data to JSON for later batches
with open('/tmp/meta_fix_list.json', 'w') as f:
    json.dump(results[:30], f, ensure_ascii=False, indent=2)
print('\nSaved first 30 to /tmp/meta_fix_list.json')

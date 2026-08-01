#!/usr/bin/env python3
"""Scan meta descriptions for SEO issues"""
import os, re
from html.parser import HTMLParser

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_desc = ''
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'meta' and d.get('name','').lower() == 'description':
            self.meta_desc = d.get('content','')

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
                    issues = []
                    if length < 100:
                        issues.append('TOO_SHORT')
                    if length > 165:
                        issues.append('TOO_LONG')
                    if length > 175:
                        issues.append('OVER_175')
                    cnt = desc.count('纯前端本地处理')
                    if cnt > 1:
                        issues.append('REPETITIVE')
                    if issues:
                        results.append((path, length, issues, desc[:150]))
            except:
                pass

def sev_key(item):
    issues = item[2]
    if 'TOO_SHORT' in issues: return 0
    if 'OVER_175' in issues: return 1
    if 'TOO_LONG' in issues: return 2
    return 3

results.sort(key=sev_key)

print('Total pages needing fixes: %d' % len(results))
print()
for path, length, issues, desc_preview in results[:50]:
    issue_str = ','.join(issues)
    print('[%s] %s (%dch)' % (issue_str, path, length))
    print('  %s...' % desc_preview)
    print()

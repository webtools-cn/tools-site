#!/usr/bin/env python3
"""Generate optimized meta descriptions for pages with short descriptions"""
import os, json, re
from html.parser import HTMLParser

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_desc = ''
        self.title = ''
        self.h1 = ''
        self.meta_line = -1
        self.line_count = 0
        self.in_title = False
        self.in_h1 = False
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

def generate_description(path, desc, title, h1):
    """Generate optimized meta description, maximizing to 140-160 chars"""
    # Clean the title/h1
    name = h1 or title or ''
    name = re.sub(r'^[^\w]*', '', name)  # strip emoji prefix
    name = re.sub(r'\s*[-–|].*', '', name).strip()  # strip after separator
    if not name:
        name = os.path.basename(os.path.dirname(path))
    
    # Extract key phrases from existing description
    clean_desc = desc
    # Remove boilerplate endings
    endings = [
        '纯前端本地处理，数据不上传服务器，无需注册完全免费。',
        '数据不上传服务器，无需注册完全免费。',
        '无需注册完全免费。',
        '纯前端计算，数据不上传。',
        '纯前端处理，数据安全。',
        '纯前端本地处理，数据不上传服务器，无需注册完全免费',
    ]
    for ending in endings:
        clean_desc = re.sub(re.escape(ending) + r'\.?\s*$', '', clean_desc)
    clean_desc = clean_desc.strip().rstrip('.')
    
    # If clean_desc is already decent length, just add proper ending
    if len(clean_desc) > 90:
        # Add concise ending to reach target length
        suffix = '纯浏览器端运行，安全免费。'
        new_desc = clean_desc + '。' + suffix
        if len(new_desc) > 160:
            # Trim slightly
            while len(new_desc) > 160 and '。' in new_desc[120:]:
                new_desc = new_desc[:new_desc.rindex('。', 120)] + '。' + suffix
        return new_desc
    
    # For very short ones, build a richer description
    # Try to extract more from the page title
    return new_desc

# Load first batch
with open('/tmp/meta_fix_list.json') as f:
    items = json.load(f)

for item in items[:15]:  # Focus on first 15
    path = item['path']
    desc = item['desc']
    h1 = item.get('h1', '')
    clean = desc 
    # Strip boilerplate
    endings = ['纯前端本地处理，数据不上传服务器，无需注册完全免费。', '数据不上传服务器，无需注册完全免费。', '无需注册完全免费。', '纯前端计算，数据不上传。', '纯前端处理，数据安全。', '纯前端本地处理，数据不上传服务器，无需注册完全免费']
    for ending in endings:
        clean = clean.replace(ending + '。', '').replace(ending, '')
    clean = clean.strip().rstrip('。').rstrip('，')
    
    print('Path: %s' % path)
    print('  H1: %s' % (h1 or 'N/A'))
    print('  Current: %s (%dch)' % (desc, len(desc)))
    print('  Clean:   %s (%dch)' % (clean, len(clean)))
    
    # Generate new description
    # Need to add ~20-60 more chars
    boilerplate = '纯浏览器本地处理，无需注册，完全免费。'
    needed = 145 - len(clean) - len(boilerplate) - 1  # -1 for 。
    if needed > 0:
        # Just add boilerplate
        new_desc = clean + '。' + boilerplate
    else:
        new_desc = clean[:160 - len(boilerplate) - 1] + '。' + boilerplate
    
    if len(new_desc) < 100:
        new_desc = clean + '。' + boilerplate
    
    print('  Proposed: %s (%dch)' % (new_desc, len(new_desc)))
    print()

#!/usr/bin/env python3
"""Fix remaining 4 SHORT CN pages."""
import os

fixes = {
    './syllable-counter/index.html': 
        "免费在线音节计数器，自动统计英文文本中每个单词的音节数，计算总音节、平均音节和Flesch可读性分数。支持实时统计、词频排序和CSV导出，浏览器本地处理保障隐私。适用于英文写作、SEO内容优化和语言学习场景。",
    './phone-link-generator/index.html':
        "免费在线手机链接生成器，一键生成tel协议HTML链接代码。点击后手机自动拨打电话，电脑打开Skype等通话软件。支持添加国家区号和分机号，实时预览效果复制即用。纯前端本地处理保障数据安全，无需注册完全免费。",
    './resignation-letter-generator/index.html':
        "免费在线辞职信生成器，填写姓名、职位、日期等基本信息即可生成专业辞职信。支持正式、友好、简短三种模板风格，一键复制到剪贴板或下载PDF文件。纯前端本地处理，数据不上传服务器，无需注册完全免费使用。",
    './time-duration-calculator/index.html':
        "免费在线时间时长计算器，轻松计算两个时间点之间的天数、小时、分钟和秒差。支持跨天计算夜班工时、日期差值对比和时间加减运算。结果以天时分秒等多种单位展示，纯前端本地处理，无需注册登录，打开即用。",
}

for filepath, new_desc in fixes.items():
    new_len = len(new_desc)
    if new_len < 100:
        print(f'WARN: {filepath} new_desc is {new_len} chars!')
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    found = False
    for i, line in enumerate(lines):
        if 'name="description"' in line:
            idx = line.find('content="')
            if idx < 0:
                continue
            start = idx + 9
            end = line.find('"', start)
            old_val = line[start:end]
            old_len = len(old_val)
            
            if old_val == new_desc:
                print(f'  SKIP: {filepath} (already matches)')
                found = True
                break
            
            lines[i] = line[:start] + new_desc + line[end:]
            found = True
            break
    
    if not found:
        print(f'  ERROR: no desc line in {filepath}')
        continue
    
    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f'✓ {filepath}: {old_len}→{new_len} chars')
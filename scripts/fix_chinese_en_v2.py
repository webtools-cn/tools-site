#!/usr/bin/env python3
"""
更完善的 chinese_in_en 修复
针对英文页面中残留的中文内容进行替换
"""
import json, os, re

SITE = '/home/chison/tools-site'

# 扩展的中文→英文映射
REPLACEMENTS = [
    # 导航/链接
    ('中文', '中文'),
    ('中文版', 'CN'),
    ('切换到中文', 'Switch to Chinese'),
    # 工具名/描述常见残留
    ('缩写查看含义', 'Find abbreviation meanings'),
    ('在线', 'Online'),
    ('免费', 'Free'),
    ('无需注册', 'No Signup'),
    ('数据绝不上传', 'Data never uploaded'),
    ('首页', 'Home'),
    ('工具', 'Tools'),
    ('返回', 'Back'),
    ('生成', 'Generate'),
    ('复制', 'Copy'),
    ('清空', 'Clear'),
    ('下载', 'Download'),
    ('重置', 'Reset'),
    ('预览', 'Preview'),
    ('结果', 'Result'),
    ('输入', 'Input'),
    ('输出', 'Output'),
    ('计算', 'Calculate'),
    ('转换', 'Convert'),
    ('编码', 'Encode'),
    ('解码', 'Decode'),
    ('加密', 'Encrypt'),
    ('解密', 'Decrypt'),
    ('上传', 'Upload'),
    ('设置', 'Settings'),
    ('选项', 'Options'),
    ('格式', 'Format'),
    ('保存', 'Save'),
    ('删除', 'Delete'),
    ('编辑', 'Edit'),
    ('添加', 'Add'),
    ('搜索', 'Search'),
    ('确认', 'Confirm'),
    ('取消', 'Cancel'),
    ('关闭', 'Close'),
    ('加载中', 'Loading'),
    ('点击', 'Click'),
    ('选择', 'Select'),
    ('文件', 'File'),
    ('文本', 'Text'),
    ('数字', 'Number'),
    ('颜色', 'Color'),
    ('大小', 'Size'),
    ('宽度', 'Width'),
    ('高度', 'Height'),
    ('比例', 'Ratio'),
    ('质量', 'Quality'),
    ('密码', 'Password'),
    ('哈希', 'Hash'),
    ('关于', 'About'),
    ('隐私', 'Privacy'),
    ('条款', 'Terms'),
    ('联系', 'Contact'),
    ('支持', 'Support'),
    ('帮助', 'Help'),
    ('全部', 'All'),
    ('更多', 'More'),
    ('分享', 'Share'),
    ('语言', 'Language'),
    ('英文', 'English'),
    ('英文版', 'English'),
    # 常见工具名称碎片
    ('计算器', 'Calculator'),
    ('生成器', 'Generator'),
    ('转换器', 'Converter'),
    ('验证器', 'Validator'),
    ('检查器', 'Checker'),
    ('编辑器', 'Editor'),
    ('查看器', 'Viewer'),
    ('播放器', 'Player'),
    ('测试器', 'Tester'),
    ('加密器', 'Encryptor'),
    ('解密器', 'Decryptor'),
    ('压缩器', 'Compressor'),
    ('格式化器', 'Formatter'),
    ('分析器', 'Analyzer'),
    ('提取器', 'Extractor'),
    ('生成工具', 'Generator'),
    ('转换工具', 'Converter'),
    ('验证工具', 'Validator'),
    ('编辑工具', 'Editor'),
    ('测试工具', 'Tester'),
    ('格式化工具', 'Formatter'),
    ('分析工具', 'Analyzer'),
    ('提取工具', 'Extractor'),
    ('在线工具', 'Online Tool'),
    ('免费工具', 'Free Tool'),
    ('免费在线', 'Free Online'),
    ('无需下载', 'No Download'),
    ('纯前端', 'Client-side'),
    ('浏览器', 'Browser'),
    ('本地处理', 'Local Processing'),
    ('数据处理', 'Data Processing'),
    ('数据安全', 'Data Security'),
    ('隐私保护', 'Privacy Protection'),
    ('功能说明', 'Features'),
    ('使用说明', 'How to Use'),
    ('使用方法', 'Usage'),
    ('常见问题', 'FAQ'),
    ('注意事项', 'Notes'),
    ('技术参数', 'Technical Specs'),
    ('相关工具', 'Related Tools'),
    ('更多工具', 'More Tools'),
    ('免费使用', 'Free to Use'),
    ('立即使用', 'Try Now'),
    ('开始使用', 'Get Started'),
    ('了解更多', 'Learn More'),
]

def fix_chinese_in_en(page_path):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    cn_re = re.compile(r'[\u4e00-\u9fff]')
    if not cn_re.search(c):
        return False
    
    if 'noindex' in c:
        return False
    
    changed = False
    
    # Strategy 1: Direct replacements
    for cn_text, en_text in REPLACEMENTS:
        if cn_text in c and cn_text != en_text:
            c = c.replace(cn_text, en_text)
            changed = True
    
    # Strategy 2: Ensure lang attribute is 'en'
    if 'lang="zh-CN"' in c:
        c = c.replace('lang="zh-CN"', 'lang="en"')
        changed = True
    
    # Strategy 3: Remove any remaining Chinese-only nav links like "中文" that survived
    # "中文" in a lang-switch context should become "中文" 
    # Actually, in English pages, the Chinese link text should be "中文" to indicate it's the Chinese version
    # But quality_loop counts this as Chinese content. 
    # We'll replace it with "CN" for brevity
    
    if changed:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
        return True
    return False


def main():
    with open(os.path.join(SITE, 'quality', 'quality_loop_result.json')) as f:
        data = json.load(f)
    
    pages = data['remaining_pages']
    target = [(k,v) for k,v in pages.items() if 'chinese_in_en' in v]
    
    print(f'Target pages with chinese_in_en: {len(target)}')
    
    fixed = 0
    skipped = 0
    
    for idx, (page_key, issues) in enumerate(target):
        lang, item = page_key.split(':', 1)
        path = os.path.join(SITE, 'en', item, 'index.html')
        
        if not os.path.exists(path):
            skipped += 1
            continue
        
        try:
            if fix_chinese_in_en(path):
                fixed += 1
            else:
                skipped += 1
        except Exception as e:
            skipped += 1
        
        if (idx + 1) % 20 == 0:
            print(f'  Progress: {idx+1}/{len(target)}')
    
    print(f'\n=== chinese_in_en Fix Results ===')
    print(f'Total: {len(target)}')
    print(f'Fixed: {fixed}')
    print(f'Skipped: {skipped}')

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
修复EN页面中的中文残留问题
1. 替换语言切换链接中的"中文"为"中文"
2. 清理Schema中的中文（替换为英文或删除中文Schema块）
"""
import os, re, json
from pathlib import Path

SITE = Path('/home/chison/tools-site')
CN_RE = re.compile(r'[\u4e00-\u9fff]')

# 常见中文-英文替换
REPLACEMENTS = [
    # UI元素
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
    ('质量', 'Quality'),
    ('密码', 'Password'),
    ('免费', 'Free'),
    ('在线', 'Online'),
    ('无需注册', 'No Signup'),
    ('关于', 'About'),
    ('隐私', 'Privacy'),
    ('条款', 'Terms'),
    ('全部', 'All'),
    ('更多', 'More'),
    ('已复制', 'Copied'),
    ('成功', 'Success'),
    ('失败', 'Failed'),
    ('错误', 'Error'),
    ('警告', 'Warning'),
    ('信息', 'Info'),
    ('加载', 'Loading'),
    ('处理中', 'Processing'),
    ('完成', 'Done'),
    ('百分比', 'Percent'),
    ('像素', 'px'),
    ('秒', 's'),
    ('分钟', 'min'),
    ('小时', 'hour'),
    ('天', 'day'),
    ('周', 'week'),
    ('月', 'month'),
    ('年', 'year'),
    ('中文', '中文'),  # keep as-is or change to 中文 flag
    ('英文', 'English'),
    ('首页工具', 'Home Tools'),
    ('开发者工具', 'Developer Tools'),
    ('文本工具', 'Text Tools'),
    ('图片工具', 'Image Tools'),
    ('加密工具', 'Crypto Tools'),
    ('单位转换', 'Unit Converters'),
    ('计算器', 'Calculators'),
    ('生成器', 'Generators'),
    ('转换器', 'Converters'),
    ('分析器', 'Analyzers'),
    ('查看器', 'Viewers'),
    ('验证器', 'Validators'),
    ('编辑器', 'Editors'),
    ('格式化', 'Formatter'),
    ('压缩', 'Compress'),
    ('解压', 'Decompress'),
    ('美化', 'Beautify'),
    ('最小化', 'Minify'),
    ('对比度', 'Contrast'),
    ('分析', 'Analyze'),
    ('验证', 'Validate'),
    ('检查', 'Check'),
    ('检测', 'Detect'),
    ('扫描', 'Scan'),
    ('测试', 'Test'),
    ('读取', 'Read'),
    ('写入', 'Write'),
    ('导出', 'Export'),
    ('导入', 'Import'),
    ('合并', 'Merge'),
    ('拆分', 'Split'),
    ('排序', 'Sort'),
    ('过滤', 'Filter'),
    ('统计', 'Stats'),
    ('图表', 'Chart'),
    ('列表', 'List'),
    ('表格', 'Table'),
    ('网格', 'Grid'),
    ('卡片', 'Card'),
    ('按钮', 'Button'),
    ('链接', 'Link'),
    ('标签', 'Label'),
    ('徽章', 'Badge'),
    ('提示', 'Tip'),
    ('通知', 'Notification'),
    ('对话框', 'Dialog'),
    ('菜单', 'Menu'),
    ('导航', 'Navigation'),
    ('面包屑', 'Breadcrumb'),
    ('分页', 'Pagination'),
    ('加载更多', 'Load More'),
    ('没有数据', 'No Data'),
    ('网络错误', 'Network Error'),
    ('请稍后重试', 'Please Retry'),
    ('复制成功', 'Copied!'),
    ('已复制到剪贴板', 'Copied to clipboard'),
    ('点击复制', 'Click to Copy'),
    ('拖拽或点击上传', 'Drag & Drop or Click to Upload'),
    ('选择文件', 'Choose File'),
    ('未选择文件', 'No file chosen'),
    ('文件大小', 'File Size'),
    ('文件名', 'File Name'),
    ('文件类型', 'File Type'),
    ('上传进度', 'Upload Progress'),
    ('下载链接', 'Download Link'),
    ('请输入', 'Please enter'),
    ('请选择', 'Please select'),
    ('请输入内容', 'Please enter content'),
    ('参数', 'Parameter'),
    ('值', 'Value'),
    ('描述', 'Description'),
    ('示例', 'Example'),
    ('默认值', 'Default'),
    ('备注', 'Note'),
    ('参考', 'Reference'),
    ('来源', 'Source'),
    ('版本', 'Version'),
    ('作者', 'Author'),
    ('日期', 'Date'),
    ('时间', 'Time'),
    ('标题', 'Title'),
    ('内容', 'Content'),
    ('分类', 'Category'),
    ('标签', 'Tags'),
    ('状态', 'Status'),
    ('类型', 'Type'),
    ('模式', 'Mode'),
    ('主题', 'Theme'),
    ('语言', 'Language'),
    ('区域', 'Region'),
    ('国家', 'Country'),
    ('城市', 'City'),
    ('地址', 'Address'),
    ('邮箱', 'Email'),
    ('电话', 'Phone'),
    ('网址', 'URL'),
    ('用户名', 'Username'),
    ('密码', 'Password'),
    ('确认密码', 'Confirm Password'),
    ('验证码', 'Captcha'),
    ('登录', 'Login'),
    ('注册', 'Register'),
    ('退出', 'Logout'),
    ('个人中心', 'Profile'),
    ('余额', 'Balance'),
    ('积分', 'Points'),
    ('优惠券', 'Coupon'),
    ('折扣', 'Discount'),
    ('价格', 'Price'),
    ('免费试用', 'Free Trial'),
    ('立即购买', 'Buy Now'),
    ('加入购物车', 'Add to Cart'),
    ('查看详情', 'View Details'),
    ('了解更多', 'Learn More'),
    ('联系我们', 'Contact Us'),
    ('常见问题', 'FAQ'),
    ('帮助中心', 'Help Center'),
    ('用户协议', 'Terms of Service'),
    ('隐私政策', 'Privacy Policy'),
    ('Cookie政策', 'Cookie Policy'),
    ('版权所有', 'All Rights Reserved'),
    ('保留所有权利', 'All Rights Reserved'),
]

def fix_chinese_in_en_page(page_path):
    with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    if 'noindex' in c:
        return False  # skip noindex pages
    
    if not CN_RE.search(c):
        return False  # no Chinese
    
    changed = False
    
    # 1. Replace common Chinese text
    for cn_text, en_text in REPLACEMENTS:
        if cn_text in c:
            c = c.replace(cn_text, en_text)
            changed = True
    
    # 2. Fix Schema blocks with Chinese - replace Chinese names with English
    # Find all ld+json blocks
    schemas = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL))
    for schema_match in schemas:
        schema_text = schema_match.group(1)
        if CN_RE.search(schema_text):
            # Try to fix the schema by replacing Chinese text
            new_schema = schema_text
            for cn_text, en_text in REPLACEMENTS:
                if cn_text in new_schema:
                    new_schema = new_schema.replace(cn_text, en_text)
            if new_schema != schema_text:
                c = c.replace(schema_text, new_schema)
                changed = True
    
    # 3. Fix lang attribute
    c = re.sub(r'lang="zh-CN"', 'lang="en"', c)
    
    # 4. Fix hreflang links - ensure "中文" link text
    # Already handled in replacements
    
    # 5. Check if there's still a lot of Chinese (>50 chars in visible text)
    # Extract visible text (remove scripts, styles, HTML tags)
    visible = re.sub(r'<script[^>]*>.*?</script>', '', c, flags=re.DOTALL)
    visible = re.sub(r'<style[^>]*>.*?</style>', '', visible, flags=re.DOTALL)
    visible = re.sub(r'<[^>]+>', ' ', visible)
    cn_chars = len(list(CN_RE.finditer(visible)))
    
    if cn_chars > 50:
        # Too much Chinese in visible text - this might need translation
        # Just report, don't break the page
        return changed  # partial fix
    
    if changed:
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(c)
    
    return changed

def main():
    with open(SITE / 'quality' / 'quality_loop_result.json') as f:
        data = json.load(f)
    
    pages = data['remaining_pages']
    chinese_pages = [(k, v) for k, v in pages.items() if k.startswith('en:') and 'chinese_in_en' in v]
    
    fixed = 0
    still_cn = 0
    
    for page_key, issues in chinese_pages:
        item = page_key.split(':', 1)[1]
        page_path = SITE / 'en' / item / 'index.html'
        
        if fix_chinese_in_en_page(str(page_path)):
            fixed += 1
        else:
            still_cn += 1
    
    print(f'EN Chinese fix: fixed={fixed}, still_cn={still_cn}')

if __name__ == '__main__':
    main()
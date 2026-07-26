#!/usr/bin/env python3
"""
chinese_in_en 批量修复 v4
处理所有en页面中的中文碎片
"""
import os, re, sys

SITE = '/home/chison/tools-site'
CN_RE = re.compile(r'[\u4e00-\u9fff]')

# 常见中文碎片→英文映射（按优先级）
FIXES = [
    # 批量脚本遗留的模板文案
    ('为所有区域添加复制按钮', ''),
    ('区域添加复制按钮', ''),
    ('区域', ''),
    ('按钮', ''),
    # lang-switch
    ('中文版', 'English'),
    ('中文', 'English'),
    # 标签碎片
    ('相关工具推荐', 'Related Tools'),
    ('工具列表', 'Tools'),
    ('免费在线工具', 'Free Online Tools'),
    ('免费在线', 'Free Online'),
    ('在线工具', 'Online Tool'),
    ('在线', 'Online'),
    ('首页', 'Home'),
    ('免费工具', 'Free Tool'),
    # 通用button/label
    ('复制', 'Copy'),
    ('已复制到剪贴板', 'Copied to clipboard!'),
    ('复制到剪贴板', 'Copy to clipboard'),
    ('到剪贴板', 'to clipboard'),
    ('已复制', 'Copied'),
    ('已', 'Done'),
    ('清除', 'Clear'),
    ('重置', 'Reset'),
    ('下载', 'Download'),
    ('上传', 'Upload'),
    ('生成', 'Generate'),
    ('计算', 'Calculate'),
    ('请输入', 'Please enter'),
    ('请', 'Please'),
    ('选择', 'Select'),
    ('输入', 'Enter'),
    ('输出', 'Output'),
    ('结果', 'Result'),
    ('错误', 'Error'),
    ('成功', 'Success'),
    ('警告', 'Warning'),
    ('提示', 'Tip'),
    ('确认', 'Confirm'),
    ('取消', 'Cancel'),
    ('保存', 'Save'),
    ('删除', 'Delete'),
    ('编辑', 'Edit'),
    ('搜索', 'Search'),
    ('关闭', 'Close'),
    ('打开', 'Open'),
    ('加载中', 'Loading...'),
    ('无数据', 'No data'),
    ('配置', 'Configuration'),
    ('样式', 'Style'),
    ('默认', 'Default'),
    ('自定义', 'Custom'),
    ('导出', 'Export'),
    ('导入', 'Import'),
    ('预览', 'Preview'),
    ('分享', 'Share'),
    ('评论', 'Comments'),
    ('点赞', 'Like'),
    ('收藏', 'Bookmark'),
    ('更多', 'More'),
    ('全部', 'All'),
    ('返回', 'Back'),
    ('下一步', 'Next'),
    ('上一步', 'Previous'),
    ('开始', 'Start'),
    ('结束', 'End'),
    ('暂停', 'Pause'),
    ('继续', 'Continue'),
    ('超时', 'Timeout'),
    ('无效', 'Invalid'),
    ('有效', 'Valid'),
    ('启用', 'Enable'),
    ('禁用', 'Disable'),
    ('显示', 'Show'),
    ('隐藏', 'Hide'),
    ('加载', 'Load'),
    ('提交', 'Submit'),
    ('发送', 'Send'),
    ('接收', 'Receive'),
    ('连接', 'Connect'),
    ('断开', 'Disconnect'),
    ('已连接', 'Connected'),
    ('未连接', 'Disconnected'),
    ('正在连接', 'Connecting...'),
    ('正在加载', 'Loading...'),
    ('处理中', 'Processing...'),
    ('完成', 'Complete'),
    ('失败', 'Failed'),
    ('成功', 'Success'),
    ('部分成功', 'Partial success'),
    ('请稍候', 'Please wait...'),
    ('暂无数据', 'No data available'),
    ('加载失败', 'Load failed'),
    ('网络错误', 'Network error'),
    ('请检查网络连接', 'Please check network connection'),
    ('请输入有效', 'Please enter valid'),
    ('请输入有效的', 'Please enter a valid'),
    ('不可为空', 'cannot be empty'),
    ('格式不正确', 'Invalid format'),
    ('超出范围', 'Out of range'),
    ('文件过大', 'File too large'),
    ('不支持的文件类型', 'Unsupported file type'),
    ('文件格式不支持', 'File format not supported'),
    ('上传成功', 'Upload successful'),
    ('上传失败', 'Upload failed'),
    ('下载成功', 'Download successful'),
    ('下载失败', 'Download failed'),
    ('操作成功', 'Operation successful'),
    ('操作失败', 'Operation failed'),
    ('未知错误', 'Unknown error'),
    ('请重试', 'Please try again'),
    ('重试', 'Retry'),
    ('返回首页', 'Back to Home'),
    ('了解更多', 'Learn more'),
    ('查看详情', 'View details'),
    ('立即体验', 'Try it now'),
    ('开始使用', 'Get Started'),
    ('免费使用', 'Free to use'),
    ('无需注册', 'No registration'),
    ('如何使用', 'How to use'),
    ('使用说明', 'Instructions'),
    ('常见问题', 'FAQ'),
    ('联系我们', 'Contact Us'),
    ('关于我们', 'About Us'),
    ('隐私政策', 'Privacy Policy'),
    ('服务条款', 'Terms of Service'),
    ('版权所有', 'All Rights Reserved'),
    ('保留所有权利', 'All Rights Reserved'),
    ('的详细步骤指南', ''),
    # 工具名碎片常见后缀
    ('器', ''),  # 生成器→generator, 转换器→converter, 计算器→calculator
    ('计算', ''),  # 面积计算→Area, 体积计算→Volume
    ('转换', ''),
    ('生成', ''),
    ('测试', ''),
    ('检测', ''),
    ('验证', ''),
    ('检查', ''),
    ('分析', ''),
    ('对比', ''),
    ('格式化', ''),
    ('加密', ''),
    ('解密', ''),
    ('压缩', ''),
    ('解压', ''),
    ('合并', ''),
    ('拆分', ''),
    ('提取', ''),
    ('转换器', ''),
    ('生成器', ''),
    ('计算器', ''),
    ('编辑器', ''),
    ('查看器', ''),
    ('阅读器', ''),
    ('分析器', ''),
    ('检测器', ''),
    ('验证器', ''),
    # 金融/数字相关
    ('元', '$'),
    ('折', 'off'),
    ('打折', 'discount'),
    ('立减', 'off'),
    ('后', 'after'),
    ('和', 'and'),
    ('是', 'is'),
    ('之间', 'between'),
    ('的', ''),
    ('到', 'to'),
    ('将', ''),
    ('在', 'at'),
    ('不', 'not'),
    ('否', 'no'),
    ('是', 'yes'),
    ('或', 'or'),
    ('与', 'and'),
    ('被', ''),
    ('由', 'by'),
    ('为', 'for'),
    ('以', 'with'),
    ('从', 'from'),
    ('对', 'to'),
    ('向', 'to'),
    ('于', 'at'),
    ('当', 'when'),
    ('此', 'this'),
    ('该', 'the'),
    ('其', 'its'),
    ('所', ''),
    ('均', 'all'),
    ('等', 'etc'),
    ('及', 'and'),
    ('即', 'i.e.'),
    ('如', 'e.g.'),
    ('若', 'if'),
    ('则', 'then'),
    ('但', 'but'),
    ('且', 'and'),
    ('因', 'because'),
    ('故', 'therefore'),
    ('无', 'no'),
    ('非', 'non'),
    ('未', 'not'),
    ('已', 'already'),
    ('曾', 'ever'),
    ('将', 'will'),
    ('要', 'to'),
    ('会', 'will'),
    ('可', 'can'),
    ('能', 'can'),
    ('应', 'should'),
    ('该', 'should'),
    ('需', 'need'),
    ('必须', 'must'),
    ('可能', 'may'),
    ('可以', 'can'),
    ('能够', 'able to'),
    ('应该', 'should'),
    ('需要', 'need'),
    ('必须', 'must'),
]


def has_chinese(text):
    """检查是否含有中文"""
    return bool(CN_RE.search(text))


def count_chinese(text):
    """统计中文字符数"""
    return len(CN_RE.findall(text))


def extract_text_without_tags(html):
    """去掉script/style标签，然后去掉HTML标签，返回纯文本"""
    # Remove script and style blocks
    clean = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    clean = re.sub(r'<style[^>]*>.*?</style>', '', clean, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', clean)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def fix_page(filepath):
    """修复单个页面，返回是否修改"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    
    if 'noindex' in original:
        return False
    
    text_only = extract_text_without_tags(original)
    cn_count = count_chinese(text_only)
    
    if cn_count <= 3:
        return False  # 不超过3个中文字符不算问题
    
    modified = original
    
    for cn, en in FIXES:
        if cn in modified:
            modified = modified.replace(cn, en)
    
    if modified != original:
        # 写回
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(modified)
        return True
    return False


def main():
    en_dir = os.path.join(SITE, 'en')
    fixed = 0
    skipped = 0
    still_has_cn = []
    
    for root, dirs, files in os.walk(en_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                rel = os.path.relpath(path, SITE)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                
                if 'noindex' in content:
                    continue
                
                text = extract_text_without_tags(content)
                cn_count = count_chinese(text)
                
                if cn_count <= 3:
                    continue
                
                if fix_page(path):
                    # 验证
                    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                        new_content = fh.read()
                    new_text = extract_text_without_tags(new_content)
                    new_cn = count_chinese(new_text)
                    
                    if new_cn <= 3 or new_cn < cn_count:
                        fixed += 1
                        print(f'✅ {rel}: {cn_count}→{new_cn} CN chars')
                    else:
                        # 修复效果不好，回滚
                        with open(path, 'w', encoding='utf-8') as fh:
                            fh.write(content)
                        still_has_cn.append((rel, cn_count, new_cn))
                else:
                    still_has_cn.append((rel, cn_count, cn_count))
    
    print(f'\n=== 汇总 ===')
    print(f'Fixed: {fixed}')
    print(f'Still have Chinese: {len(still_has_cn)}')
    for rel, before, after in still_has_cn[:30]:
        print(f'  ⚠️ {rel}: {before}→{after} CN chars')


if __name__ == '__main__':
    main()

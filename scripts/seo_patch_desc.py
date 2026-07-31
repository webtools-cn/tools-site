#!/usr/bin/env python3
"""修补不够140字符的meta description，在每个已更新描述基础上追加内容"""
import re

# 对每个需要修补的页面：old_suffix (唯一结尾) -> new_suffix (追加的内容)
PATCHES = {
    "2048-game": {
        "old_suffix": '纯前端实现无需安装打开即玩，无需注册完全免费。',
        "new_suffix": '适合碎片时间休闲娱乐和脑力训练。纯前端实现无需下载安装打开即玩，无需注册完全免费。'
    },
    "airbnb-income-calculator": {
        "old_suffix": '纯前端本地计算，数据不上传服务器，无需注册完全免费。',
        "new_suffix": '帮助房东科学评估短租房产收益潜力。纯前端本地计算，数据不上传服务器，无需注册完全免费。'
    },
    "api-key-generator": {
        "old_suffix": '纯前端浏览器本地运行，密钥绝不经过网络传输，无需注册完全免费。',
        "new_suffix": '适合开发者为API服务生成安全访问凭据。纯前端浏览器本地运行，密钥绝不经过网络传输，无需注册完全免费。'
    },
    "api-rate-limit-calculator": {
        "old_suffix": '帮助后端开发者设计合理API限流策略，纯前端无需注册。',
        "new_suffix": '适合微服务架构和高并发系统设计API限流策略。帮助后端开发者设计合理API限流策略，纯前端无需注册。'
    },
    "api-status-dashboard": {
        "old_suffix": '纯前端运行保护隐私数据，无需注册。',
        "new_suffix": '适合运维团队监控线上服务状态。纯前端运行保护隐私数据，无需注册。'
    },
    "apri-calculator": {
        "old_suffix": '纯前端本地计算无需注册。',
        "new_suffix": '为肝病患者提供便捷的无创肝纤维化风险初步筛查。纯前端本地计算无需注册。'
    },
    "area-chart-maker": {
        "old_suffix": '数据全程不上传服务器，无需注册完全免费。',
        "new_suffix": '适合数据分析和商业报告可视化。数据全程不上传服务器，无需注册完全免费。'
    },
    "area-converter": {
        "old_suffix": '纯前端无需注册。',
        "new_suffix": '适合不动产测量、土地规划和建筑工程计算。纯前端无需注册。'
    },
    "ascii-art": {
        "old_suffix": '一键复制分享无需注册。',
        "new_suffix": '适合程序员终端美化和创意设计。一键复制分享无需注册。'
    },
    "ascii-code-converter": {
        "old_suffix": '纯前端本地处理无需注册完全免费。',
        "new_suffix": '适合程序员调试和计算机专业学生编码学习。纯前端本地处理无需注册完全免费。'
    },
    "ascii-table": {
        "old_suffix": '纯前端零依赖无需注册。',
        "new_suffix": '适合程序员日常开发和计算机基础课程编码查询。纯前端零依赖无需注册。'
    },
    "ascvd-risk-calculator": {
        "old_suffix": '纯前端本地计算无需注册。',
        "new_suffix": '辅助医生和患者进行心血管疾病预防决策。纯前端本地计算无需注册。'
    },
    "asset-depreciation-calculator": {
        "old_suffix": '无需注册完全免费。',
        "new_suffix": '适合会计和财务人员进行固定资产管理与税务筹划。无需注册完全免费。'
    },
}

def patch_page(dirname, old_suffix, new_suffix):
    path = f"{dirname}/index.html"
    with open(path, 'r') as f:
        content = f.read()
    
    # Replace in meta description
    meta_re = r'<meta name="description" content="([^"]*' + re.escape(old_suffix) + r')"'
    m = re.search(meta_re, content)
    if not m:
        print(f"  ERROR {dirname}: meta not found with suffix")
        return False
    old_meta_desc = m.group(0)
    new_desc = m.group(1).replace(old_suffix, new_suffix)
    new_meta = f'<meta name="description" content="{new_desc}"'
    content = content.replace(old_meta_desc, new_meta)
    
    # Replace in og:description
    og_re = r'<meta property="og:description" content="([^"]*' + re.escape(old_suffix) + r')"'
    m_og = re.search(og_re, content)
    if m_og:
        old_og = m_og.group(0)
        new_og_desc = m_og.group(1).replace(old_suffix, new_suffix)
        new_og = f'<meta property="og:description" content="{new_og_desc}"'
        content = content.replace(old_og, new_og)
    
    # Replace in JSON-LD description
    schema_re = r'"description":\s*"([^"]*' + re.escape(old_suffix) + r')"'
    m_schema = re.search(schema_re, content)
    if m_schema:
        old_schema = m_schema.group(0)
        new_schema_desc = m_schema.group(1).replace(old_suffix, new_suffix)
        new_schema = f'"description": "{new_schema_desc}"'
        content = content.replace(old_schema, new_schema)
    
    with open(path, 'w') as f:
        f.write(content)
    return True

if __name__ == '__main__':
    count = 0
    for dirname, patch in PATCHES.items():
        ok = patch_page(dirname, patch['old_suffix'], patch['new_suffix'])
        if ok:
            # verify
            content = open(f'{dirname}/index.html').read()
            m = re.search(r'<meta name="description" content="([^"]+)"', content)
            if m:
                desc_len = len(m.group(1))
                in_range = 140 <= desc_len <= 160
                status = f"{desc_len} chars {'✓' if in_range else '⚠'}"
                count += 1
                print(f"  {dirname}: {status}")
    
    print(f"\nPatched {count} pages.")
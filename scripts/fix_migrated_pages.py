#!/usr/bin/env python3
"""修复已迁移页面的 noindex + meta description
- robots: index,follow → noindex,follow
- meta description: 占位符 → 精准描述
- Schema description: 同步更新
"""
import os, re, sys

def fix_page(path, tool_name, target_tool):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. Fix robots: index,follow → noindex,follow
    if 'content="index, follow"' in content and 'noindex' not in content:
        content = content.replace('content="index, follow"', 'content="noindex, follow"')
        changes.append('robots: index→noindex')
    
    # 2. Fix meta description  
    # 现有占位符类描述: 免费在线xxx工具。纯前端处理...
    desc_pattern = r'<meta name="description" content="([^"]*)"'
    m = re.search(desc_pattern, content)
    if m:
        old_desc = m.group(1)
        # Generate better description based on target tool
        new_desc = generate_desc(tool_name, target_tool)
        if new_desc and new_desc != old_desc:
            content = content.replace(
                f'<meta name="description" content="{old_desc}"',
                f'<meta name="description" content="{new_desc}"'
            )
            changes.append(f'desc: {len(old_desc)}→{len(new_desc)} chars')
    
    # 3. Fix Schema description
    schema_desc_pattern = r'"description":"([^"]*)"'
    m2 = re.search(schema_desc_pattern, content)
    if m2:
        old_schema_desc = m2.group(1)
        new_schema_desc = f'免费在线{tool_name}工具，已迁移至{target_tool}。纯前端处理，无需注册。'
        if new_schema_desc != old_schema_desc:
            content = content.replace(
                f'"description":"{old_schema_desc}"',
                f'"description":"{new_schema_desc}"'
            )
            changes.append('schema_desc')
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

def generate_desc(tool_name, target_tool):
    """为已迁移页面生成精准的meta description"""
    # 根据工具名生成中文描述
    tool_map = {
        'number-base': '此工具已迁移至新版在线进制转换器，支持二进制、八进制、十进制、十六进制之间任意转换，实时显示各进制对应结果。',
        'text-case': '此工具已迁移至新版英文大小写转换器，一键将文本转换为大写、小写、首字母大写、驼峰命名、蛇形命名等格式。',
        'http-status-codes': '此工具已迁移至HTTP状态码查询工具，涵盖1xx到5xx全部标准状态码的中文解释、常见原因和解决方案。',
        'text-to-html': '此工具已迁移至新版文本转HTML工具，将纯文本自动转换为标准HTML代码，自动处理段落标签、换行符和特殊字符转义。',
        'docker-compose-builder': '此工具已迁移至Docker Compose配置生成器，可视化编排多容器服务，支持端口映射、卷挂载、环境变量配置。',
        'http-status-code-reference': '此工具已迁移至HTTP状态码速查参考手册，完整收录1xx到5xx所有标准HTTP响应状态码及中文解析。',
        'password-strength-tester': '此工具已迁移至密码强度检测器，实时评估密码安全等级，检测常见弱密码模式和破解时间估算。',
        'css-specificity-analyzer': '此工具已迁移至CSS选择器优先级计算器，可视化分析CSS选择器特异性值，帮助解决样式覆盖问题。',
        'border-text': '此工具已迁移至在线文字描边生成器，为文字添加边框和描边效果，支持自定义字体、描边颜色和宽度。',
        'http-status-checker': '此工具已迁移至HTTP状态码检测工具，输入URL批量检测网页返回的状态码和重定向链。',
        'color-palette': '此工具已迁移至在线调色板生成器，智能生成协调配色方案，支持多种色彩规则，适合UI设计和品牌配色。',
        'base64-encoder': '此工具已迁移至Base64编解码工具，支持文本与Base64互转，适用于API开发、数据传输和文件嵌入场景。',
        'word-frequency-analyzer': '此工具已迁移至词频统计工具，分析文本中单词出现频率，支持中英文分词和停用词过滤。',
        'svg-to-react': '此工具已迁移至SVG转React组件工具，将SVG图标转换为React函数组件，支持TypeScript类型定义。',
        'morse-code': '此工具已迁移至摩斯密码转换器，支持文本与摩尔斯电码双向转换，可播放电码音频和闪光模拟。',
        'css-gradient-text': '此工具已迁移至CSS渐变文字生成器，为网页文字添加绚丽渐变色效果，支持线性和径向渐变模式。',
        'css-text-clamp': '此工具已迁移至CSS文本截断工具，多行文本溢出显示省略号，可视化配置行数和截断效果。',
        'svg-to-jsx': '此工具已迁移至SVG转JSX转换器，自动将SVG属性转换为React JSX格式，支持TypeScript。',
        'json-schema-faker': '此工具已迁移至JSON Schema Mock数据生成器，根据JSON Schema自动生成符合结构的模拟测试数据。',
        'html-entity-encode': '此工具已迁移至HTML实体编解码工具，支持HTML特殊字符的编码和解码，防止XSS攻击。',
        'sql-to-typescript': '此工具已迁移至SQL转TypeScript接口生成器，将SQL表结构自动转换为TypeScript类型定义。',
        'docker-compose-generator': '此工具已迁移至Docker Compose配置生成器，可视化编排多容器服务，一键生成docker-compose.yml。',
        'json-to-csv': '此工具已迁移至JSON转CSV转换器，将JSON数据一键转换为CSV表格格式，支持嵌套数据展平。',
        'semver-tester': '此工具已迁移至语义化版本验证器，验证SemVer格式、比较版本大小、检查npm版本范围。',
        'base64-decode': '此工具已迁移至Base64编解码工具，支持文本和文件的Base64编码与解码，纯前端数据安全保障。',
        'html-entity': '此工具已迁移至HTML实体编解码工具，将HTML特殊字符与实体名/实体编号之间相互转换。',
        'css-box-shadow': '此工具已迁移至CSS阴影生成器，可视化创建多层box-shadow效果，实时预览并一键复制CSS代码。',
        'semver-calculator': '此工具已迁移至语义化版本验证器，支持SemVer格式验证、版本比较和npm语义化范围检查。',
        'json-path-tester': '此工具已迁移至JSON Path提取工具，使用JSONPath表达式从复杂JSON中提取指定数据节点。',
        'json-to-rust': '此工具已迁移至JSON转Rust结构体生成器，自动从JSON数据生成Rust struct定义和serde注解。',
    }
    
    if tool_name in tool_map:
        return tool_map[tool_name]
    
    # 通用模板
    return f'此工具已迁移至新版{target_tool}，提供更完善的功能和更好的用户体验。纯前端本地处理，数据不上传服务器。'

def main():
    base_dir = '/home/chison/tools-site'
    count_fixed = 0
    
    for root, dirs, files in os.walk(base_dir):
        if '/en/' in root or 'node_modules' in root or '.git' in root:
            continue
        for f in files:
            if f == 'index.html' and root != base_dir and root != f'{base_dir}/en':
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                
                if '已迁移' not in content:
                    continue
                
                tool_name = root.replace(f'{base_dir}/', '')
                can_m = re.search(r'<link rel="canonical" href="https://free-toolbase\.com/([^/"]+)', content)
                target = can_m.group(1) if can_m else tool_name
                
                fixed, changes = fix_page(path, tool_name, target)
                if fixed:
                    count_fixed += 1
                    print(f'✓ {tool_name}: {", ".join(changes)}')
    
    print(f'\nTotal fixed: {count_fixed} pages')

if __name__ == '__main__':
    main()

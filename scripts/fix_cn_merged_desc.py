#!/usr/bin/env python3
"""
Fix Chinese meta descriptions - batch 1 (30 pages).
Focus on '已升级至新版本' merged pages and very short descriptions.
"""
import os
import re
import glob

BASE = '/home/chison/tools-site'

# 合并页面模板 — 不再写"已升级"，而是直接描述工具功能
MERGE_REDIRECT_DESC = {
    'aes-encryptor': '免费在线AES加密解密工具，支持CBC/ECB/GCM多种加密模式。在浏览器中安全加密文本，密钥不离开你的设备。无需注册，完全免费。',
    'base32-decoder': '免费在线Base32解码工具，将Base32编码字符串快速解码为原始文本。支持RFC 4648标准Base32格式，纯浏览器端处理，数据安全不泄露。',
    'base32-encoder': '免费在线Base32编码工具，将任意文本转换为Base32格式字符串。RFC 4648标准编码，适合数据传输和存储。无需注册，安全可靠。',
    'base64-decoder': '免费在线Base64解码工具，快速将Base64编码字符串解码为原始文本或文件。浏览器端本地解码，数据不上传服务器，安全可靠。',
    'base64-encoding': '免费在线Base64编码工具，将文本或文件编码为Base64格式。适用于数据传输、URL编码和内嵌资源。纯前端处理，无需注册。',
    'base64-image-encoder': '免费在线图片转Base64工具，将图片文件编码为Base64字符串。支持PNG/JPG/WebP等格式，适合将图片内嵌到HTML/CSS中。',
    'base64-image': '免费在线Base64图片工具，支持图片与Base64编码互转。将图片转换为Data URI格式直接嵌入网页，减少HTTP请求。无需注册。',
    'border-text-online': '免费在线CSS边框文字生成器，创建带描边效果的艺术文字。自定义文字颜色、边框宽度和颜色。生成HTML/CSS代码，复制即用。',
    'cron-expression-builder': '免费在线Cron表达式构建器，可视化生成和验证Cron定时任务表达式。支持秒/分/时/日/月/周字段配置，实时预览执行计划。',
    'cron-expression-generator': '免费在线Cron表达式生成器，通过可视化界面快速创建定时任务表达式。支持常用预设模板（每天/每小时/每周）和高级自定义配置。',
    'css-3d-transform': '免费在线CSS 3D变换生成器，可视化创建3D旋转、透视和变换效果。支持translate3d/rotate3d/scale3d，实时预览并复制CSS代码。',
    'css-anchor-position-generator': '免费在线CSS锚点定位生成器，使用CSS Anchor Positioning API创建精确定位的弹出层、工具提示和下拉菜单。可视化编辑，一键复制代码。',
    'css-anchor-positioning': '免费在线CSS锚点定位工具，基于CSS Anchor Positioning规范实现元素间的动态定位关系。适合工具提示、弹出菜单和上下文菜单。',
    'css-box-shadow': '免费在线CSS盒阴影生成器，可视化创建和调整box-shadow效果。支持多层阴影、内阴影、颜色和模糊度控制。实时预览，一键复制CSS代码。',
    'css-container-query-generator': '免费在线CSS容器查询生成器，基于元素容器尺寸而非视口设置响应式样式。可视化编辑@container规则，创建真正组件级的响应式设计。',
    'css-container-query': '免费在线CSS容器查询工具，学习和使用CSS Container Queries实现组件级响应式设计。告别媒体查询，让组件根据自身容器尺寸适配。',
    'css-container-query-playground': '免费在线CSS容器查询演练场，交互式学习@container规则。实时编辑HTML/CSS查看容器查询效果，掌握组件级响应式设计核心概念。',
    'css-gradient': '免费在线CSS渐变生成器，可视化创建线性、径向和锥形渐变背景。支持多色停止点、角度调整，实时预览并一键复制CSS代码。',
    'css-keyframe-animation': '免费在线CSS关键帧动画生成器，可视化创建@keyframes动画效果。支持多关键帧编辑、缓动函数配置，实时预览动画效果。',
    'css-keyframes-generator': '免费在线CSS关键帧动画生成器，拖拽式编辑动画关键帧。支持缩放、旋转、位移等变换，生成流畅的CSS动画代码。无需注册。',
    'css-loader-spinner': '免费在线CSS加载动画生成器，创建20+种加载旋转动画。自定义颜色、大小和动画速度，生成纯CSS加载指示器代码，复制即用。',
    'css-loading-animation': '免费在线CSS加载动画生成器，多种加载动画样式可选——旋转、脉冲、跳动、渐变等。自定义颜色和速度，生成纯CSS代码零JavaScript。',
    'css-loading-spinner': '免费在线CSS加载旋转器生成器，创建精美的页面加载动画。支持圆形、点状、条形等多种样式，纯CSS实现不依赖图片和JavaScript。',
    'css-specificity': '免费在线CSS选择器优先级计算器，精准计算CSS选择器的specificity值（ID/类/元素权重）。帮助解决样式冲突，理解CSS优先级规则。',
    'css-text-clamp': '免费在线CSS文本截断工具，使用-webkit-line-clamp实现多行文本截断。可视化调整行数和省略号样式，生成跨浏览器兼容CSS代码。',
    'css-text-shadow': '免费在线CSS文字阴影生成器，可视化创建多层文字阴影效果。支持发光、浮雕、3D立体等多种预设效果，一键复制CSS代码。',
    'css-text-stroke': '免费在线CSS文字描边生成器，创建文字轮廓描边效果。调整描边宽度、颜色和填充色，生成酷炫的镂空文字风格，复制CSS即用。',
    'css-view-transitions-generator': '免费在线CSS视图过渡动画生成器，使用View Transitions API创建页面切换动画。可视化配置过渡效果，生成流畅的SPA页面转场。',
    'css-view-transitions': '免费在线CSS视图过渡工具，学习CSS View Transitions API实现页面间平滑过渡。配置过渡名称、持续时间和缓动函数。',
    'csv-to-markdown': '免费在线CSV转Markdown表格工具，将CSV/TSV数据一键转换为Markdown格式表格。适合GitHub README、文档和静态网站内容编写。',
}

def fix_merged_page(filepath):
    dirname = os.path.basename(os.path.dirname(filepath))
    
    new_desc = MERGE_REDIRECT_DESC.get(dirname)
    if not new_desc:
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace meta description
    new_content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"',
        lambda m: f'<meta name="description" content="{new_desc}"',
        content
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    fixed = 0
    for dirname in MERGE_REDIRECT_DESC:
        filepath = os.path.join(BASE, dirname, 'index.html')
        if os.path.exists(filepath):
            if fix_merged_page(filepath):
                fixed += 1
                print(f"Fixed: {filepath}")
    
    print(f"\nTotal fixed: {fixed}/{len(MERGE_REDIRECT_DESC)}")

if __name__ == '__main__':
    main()
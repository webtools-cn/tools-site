#!/usr/bin/env python3
"""更新首页和sitemap"""
import re

BASE = '/home/chison/tools-site'
slugs = ['tint-image','terms-of-service-generator','recipe-analyzer','nutrition-analyzer','gradient-extractor','font-pair','audio-cutter','video-cutter','unit-converter-advanced','image-censor']

zh_cards = '''
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎨</span><span class="tool-name">图片调色</span><span class="tool-desc">上传图片调整色相、饱和度、亮度和透明度，实时预览</span><a href="tint-image/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">📜</span><span class="tool-name">服务条款生成器</span><span class="tool-desc">快速生成专业的网站/应用服务条款文档，支持多种业务类型</span><a href="terms-of-service-generator/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🍳</span><span class="tool-name">食谱营养分析</span><span class="tool-desc">添加食材自动计算总热量和蛋白质、脂肪、碳水等营养成分</span><a href="recipe-analyzer/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔍</span><span class="tool-name">食物营养查询</span><span class="tool-desc">查询20种常见食物的详细营养成分数据，支持搜索和快速选择</span><a href="nutrition-analyzer/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🌈</span><span class="tool-name">渐变色提取</span><span class="tool-desc">从图片中提取渐变色CSS代码，支持线性和径向渐变</span><a href="gradient-extractor/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔤</span><span class="tool-name">字体搭配方案</span><span class="tool-desc">浏览8套Google Fonts精选字体搭配，一键复制CSS引用代码</span><a href="font-pair/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎵</span><span class="tool-name">音频剪切</span><span class="tool-desc">在线剪切音频片段，支持WAV格式导出，本地处理不上传</span><a href="audio-cutter/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎬</span><span class="tool-name">视频剪切</span><span class="tool-desc">设置起止时间剪切视频片段，所有处理在浏览器本地完成</span><a href="video-cutter/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">📐</span><span class="tool-name">高级单位换算</span><span class="tool-desc">15大类单位换算：长度、重量、温度、面积、体积、速度等</span><a href="unit-converter-advanced/" class="btn">立即使用</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔲</span><span class="tool-name">图片打码</span><span class="tool-desc">在图片上拖动选区添加马赛克或模糊效果，保护隐私信息</span><a href="image-censor/" class="btn">立即使用</a></div>
'''

en_cards = '''
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎨</span><span class="tool-name">Tint Image - Adjust Hue Saturation Brightness | Free ToolBase</span><span class="tool-desc">Upload an image and adjust hue, saturation, lightness, and opacity in real-time</span><a href="./tint-image/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">📜</span><span class="tool-name">Terms of Service Generator - Website App SaaS | Free ToolBase</span><span class="tool-desc">Generate professional terms of service for websites, apps, and SaaS platforms</span><a href="./terms-of-service-generator/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🍳</span><span class="tool-name">Recipe Nutrition Analyzer - Calories & Macros | Free ToolBase</span><span class="tool-desc">Add ingredients and calculate total calories, protein, fat, and carbs</span><a href="./recipe-analyzer/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔍</span><span class="tool-name">Food Nutrition Lookup - 20 Common Foods | Free ToolBase</span><span class="tool-desc">Look up detailed nutrition data for 20 common foods with search</span><a href="./nutrition-analyzer/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🌈</span><span class="tool-name">Gradient Extractor - CSS Gradient from Image | Free ToolBase</span><span class="tool-desc">Extract gradient CSS code from images, supports linear and radial</span><a href="./gradient-extractor/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔤</span><span class="tool-name">Font Pairing Guide - Google Fonts Combinations | Free ToolBase</span><span class="tool-desc">Browse 8 curated Google Font pairings and copy CSS import code</span><a href="./font-pair/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎵</span><span class="tool-name">Audio Cutter - Trim Audio Clips Online | Free ToolBase</span><span class="tool-desc">Trim audio clips online and export as WAV, all processed locally</span><a href="./audio-cutter/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🎬</span><span class="tool-name">Video Cutter - Trim Video Clips Online | Free ToolBase</span><span class="tool-desc">Set start and end times to trim video clips in your browser</span><a href="./video-cutter/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">📐</span><span class="tool-name">Advanced Unit Converter - 15 Categories | Free ToolBase</span><span class="tool-desc">15 categories: length, weight, temperature, area, volume, speed and more</span><a href="./unit-converter-advanced/" class="btn">Use Now</a></div>
<div class="tool-card" data-cat="new-tools"><span class="tool-icon">🔲</span><span class="tool-name">Image Censor - Mosaic & Blur Tool | Free ToolBase</span><span class="tool-desc">Drag to select areas and apply mosaic or blur effects to images</span><a href="./image-censor/" class="btn">Use Now</a></div>
'''

# ZH index
with open(f'{BASE}/index.html') as f:
    c = f.read()
old = '<div class=\"tools-grid\" id=\"toolsGrid\">\n\n<div class=\"tool-card\"'
new = f'<div class="tools-grid" id="toolsGrid">\n{zh_cards}\n<div class="tool-card"'
c = c.replace(old, new)
with open(f'{BASE}/index.html', 'w') as f:
    f.write(c)
print('OK: index.html')

# EN index
with open(f'{BASE}/en/index.html') as f:
    c = f.read()
old_en = '<div class=\"tools-grid\">\n\n<div class=\"tool-card\" data-cat=\"image-tools\"><span class=\"tool-icon\">🖼️</span><span class=\"tool-name\">Add Watermark to Image'
new_en = f'<div class="tools-grid">\n{en_cards}\n<div class="tool-card" data-cat="image-tools"><span class="tool-icon">🖼️</span><span class="tool-name">Add Watermark to Image'
c = c.replace(old_en, new_en)
with open(f'{BASE}/en/index.html', 'w') as f:
    f.write(c)
print('OK: en/index.html')

# Sitemap
with open(f'{BASE}/sitemap.xml') as f:
    c = f.read()
new_sitemap = ''
for s in slugs:
    new_sitemap += f'  <url><loc>https://free-toolbase.com/{s}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
    new_sitemap += f'  <url><loc>https://free-toolbase.com/en/{s}/</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n'
c = c.replace('</urlset>', new_sitemap + '</urlset>')
with open(f'{BASE}/sitemap.xml', 'w') as f:
    f.write(c)
print(f'OK: sitemap.xml (+{len(slugs)*2} URLs)')

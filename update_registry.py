import json

with open('tools-registry.json', 'r') as f:
    d = json.load(f)

new_tools = [
    {
        "id": "serp-preview",
        "name": "SERP预览工具",
        "slug": "serp-preview",
        "status": "online",
        "version": "1.0.0",
        "created_at": "2026-07-11",
        "updated_at": "2026-07-11",
        "category": "SEO工具",
        "icon": "🔍",
        "description": "免费在线SERP搜索结果预览工具，模拟Google搜索结果展示效果。实时预览标题、URL、描述在搜索结果中的显示样式，支持桌面端和移动端视图，帮助优化Meta标签提升点击率。",
        "keywords": ["SERP预览","搜索结果预览","Meta描述预览","Google搜索结果模拟","标题标签预览","SEO预览工具","搜索片段预览","URL预览"]
    },
    {
        "id": "robots-txt-generator",
        "name": "Robots.txt生成器",
        "slug": "robots-txt-generator",
        "status": "online",
        "version": "1.0.0",
        "created_at": "2026-07-11",
        "updated_at": "2026-07-11",
        "category": "SEO工具",
        "icon": "🤖",
        "description": "免费在线Robots.txt生成器，可视化配置爬虫访问规则。支持设置User-agent、Allow/Disallow指令、网站地图URL、爬取延迟等。一键生成标准格式robots.txt文件。",
        "keywords": ["Robots.txt生成器","爬虫规则生成","SEO robots.txt","搜索引擎爬虫","Allow指令","Disallow指令","网站地图","robots.txt文件"]
    },
    {
        "id": "pdf-to-png",
        "name": "PDF转PNG转换器",
        "slug": "pdf-to-png",
        "status": "online",
        "version": "1.0.0",
        "created_at": "2026-07-11",
        "updated_at": "2026-07-11",
        "category": "PDF工具",
        "icon": "🖼️",
        "description": "免费在线PDF转PNG转换器，将PDF文件的每一页转换为高质量PNG图片。支持页面范围选择和自定义缩放比例，无损PNG格式保留透明度和细节。纯前端本地处理。",
        "keywords": ["PDF转PNG","PDF转图片","PDF页面转PNG","PDF提取图片","PDF转换","PNG转换器","PDF转PNG在线","PDF渲染"]
    },
    {
        "id": "pdf-crop",
        "name": "PDF裁剪工具",
        "slug": "pdf-crop",
        "status": "online",
        "version": "1.0.0",
        "created_at": "2026-07-11",
        "updated_at": "2026-07-11",
        "category": "PDF工具",
        "icon": "✂️",
        "description": "免费在线PDF裁剪工具，裁剪PDF页面多余白边和空白区域。可视化预览裁剪范围，支持分别设置上、下、左、右四个方向的裁剪值（pt单位）。所有页面统一裁剪，纯前端本地处理。",
        "keywords": ["PDF裁剪","裁剪PDF","PDF切边","PDF去白边","PDF边距调整","PDF页面裁剪","PDF裁剪工具","PDF裁边"]
    },
    {
        "id": "html-table-to-markdown",
        "name": "HTML表格转Markdown",
        "slug": "html-table-to-markdown",
        "status": "online",
        "version": "1.0.0",
        "created_at": "2026-07-11",
        "updated_at": "2026-07-11",
        "category": "开发者工具",
        "icon": "📋",
        "description": "免费在线HTML表格转Markdown工具，将HTML表格代码快速转换为GitHub Flavored Markdown格式表格。支持多表格批量转换、rowspan/colspan合并单元格、自定义对齐方式。",
        "keywords": ["HTML转Markdown","HTML表格转Markdown","表格转换","Markdown表格","HTML转MD","在线转换","HTML table to markdown","GFM表格"]
    }
]

d['tools'].extend(new_tools)
d['total_tools'] = len(d['tools'])

# Update all count fields
d['count'] = len(d['tools'])
d['last_updated'] = "2026-07-11"
d['updated_at'] = "2026-07-11"
d['updated'] = "2026-07-11"

with open('tools-registry.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Total tools now: {len(d['tools'])}")
print(f"Added: {[t['id'] for t in new_tools]}")

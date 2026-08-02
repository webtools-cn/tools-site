# PNG to SVG Converter - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 设计师、前端开发者、PPT制作者，需要将位图logo/图标转为矢量格式用于缩放。使用"图片转SVG"、"位图转矢量"等术语。
- **EN用户**: Web developers, graphic designers, UI/UX designers who need to convert raster logos/icons to scalable vector format. Search terms: "png to svg converter", "image to vector", "raster to svg".

### 搜索量估计
- 关键词: "png to svg converter" (~20K/mo), "image to svg" (~30K/mo), "convert image to vector" (~25K/mo), "image vectorizer" (~15K/mo)
- 估计总搜索量: ~90K+/月
- 竞品: vectorizer.io (收费$9.99/mo), autotracer.org (免费但广告多), SVGcode (Google PWA, 功能好但需安装), convertio.co (免费但有文件大小限制)

### 竞品分析
- **vectorizer.io**: 优点=效果好、支持多种输出格式；缺点=收费、需要上传到服务器（隐私问题）
- **autotracer.org**: 优点=免费、在线可用；缺点=广告多、UI老旧、输出质量一般
- **SVGcode**: 优点=Google出品、PWA离线可用、效果好；缺点=需要安装PWA、不支持直接调色板控制
- **我们的优势**: 完全免费、纯前端本地处理（隐私安全）、即时预览对比、支持颜色量化控制、可下载SVG/PNG

### 前端可行性
- [x] 纯前端可实现（Canvas读取像素 + 边缘检测算法 + SVG生成）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险（全部本地处理）

## 2. 功能规格

### 核心功能
1. **图片上传**: 拖拽/点击上传PNG/JPG/WebP，支持粘贴
2. **矢量化处理**: 
   - 颜色量化（减少颜色数，2-256色可调）
   - 边缘平滑（控制路径精度）
   - 背景透明处理
3. **即时预览**: 左侧原图 vs 右侧SVG对比，可缩放
4. **一键下载**: SVG格式下载，可选PNG导出
5. **预设场景**: Logo矢量化、图标转换、简单图形追踪

### 交互元素（≥3）
- 文件上传区（拖拽+点击）
- 颜色数量滑块（2-256）
- 细节/平滑度滑块
- 预览区（原图 vs SVG对比）
- 下载按钮（SVG / PNG）
- 预设场景选择

### 技术方案
- Canvas读取上传图片像素数据
- 颜色量化：Median Cut或K-means简化
- 边缘检测：使用marching squares算法追踪颜色边界
- SVG生成：将追踪到的路径转为SVG `<path>` 元素
- 使用potrace算法（纯JS移植版）或简化的轮廓追踪

## 3. EN版本差异
- 单位：CN用"颜色数量"，EN用"Number of Colors"
- 预设场景翻译
- FAQ问题不同（EN关注licensing/attribution等）
- 术语：CN"矢量化" → EN"Vectorize"

## 4. 验收标准
- [x] 上传PNG → 生成SVG → 下载的SVG文件有效
- [x] 颜色量化滑块有效（减少颜色数后SVG更简洁）
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分、推荐相关工具
- [x] 深色主题，符合全局样式
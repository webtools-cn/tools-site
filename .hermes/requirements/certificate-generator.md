# Certificate Generator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 教师（培训证书）、企业HR（员工表彰）、活动组织者（参赛证书）、学生（课程完成证明）
- **EN用户**: Teachers (course completion), HR managers (employee recognition), event organizers (participation awards), students

### 搜索量估计
- "certificate generator" / "certificate maker" / "free certificate maker" / "online certificate generator"
- 估计总搜索量 > 5000/月（多个变体）
- 竞品: Canva（需要注册）、certificatemagic.com、creativecertificates.com

### 竞品分析
- Canva: 功能强但需要注册，有水印
- certificatemagic.com: 老式UI，功能有限
- 我们的优势: 完全免费、无需注册、即时下载、本地处理、无水印

### 前端可行性
✅ 纯Canvas渲染 + 文本叠加 + 下载为PNG/PDF
✅ 无需后端
✅ 无需API key
✅ 无CORS问题

## 2. 功能规格

### 核心功能
1. **模板选择** - 5个预设模板（经典、现代、简约、创意、正式）
2. **文本编辑** - 标题、姓名、描述、日期、签名行
3. **自定义** - 字体、字号、颜色、边框样式
4. **预览** - 实时Canvas预览
5. **下载** - PNG/PDF下载

### 交互元素
- 模板选择器（点击切换）
- 文本输入框（标题、接收人、描述、日期、签名）
- 颜色选择器
- 字体下拉框
- 下载按钮（PNG / PDF）
- 实时预览Canvas

### 技术方案
- Canvas 2D渲染
- html2canvas或原生Canvas
- jsPDF用于PDF导出
- 纯前端，零依赖（或仅内联jsPDF）

## 3. EN版本差异
- 模板文本默认英文
- 日期格式: MM/DD/YYYY（US）或 DD/MM/YYYY（UK可选）
- 字体选择偏向西方常用字体

## 4. 验收标准
- ✅ 选择模板→Canvas实时渲染
- ✅ 修改文本→预览实时更新
- ✅ 下载PNG→图片清晰无水印
- ✅ 下载PDF→PDF格式正确
- ✅ 移动端375px正常显示
- ✅ EN版英文自然、无中文
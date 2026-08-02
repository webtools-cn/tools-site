# HTML表单生成器 - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 前端开发者、站长、产品经理，需要快速生成HTML表单代码。术语：「表单生成」「HTML表单」「输入框」「下拉菜单」「单选多选」
- **EN用户**: Web developers, designers, marketers who need quick form HTML without signup. Keywords: "html form generator", "online html form builder", "form code generator"

### 搜索量估计
- GSC实际数据: "html form generator" 16imp + "online html form builder" 11imp = 27imp
- 这两个关键词Google实际月搜索量估计更大（GSC仅反映已收录页面的曝光）
- 核心关键词: html form generator, html form builder, form code generator, online form maker
- 估计总月搜索量: 10,000-50,000

### 竞品分析
- **JotForm**: 功能强大但需注册，免费版限制多。重SaaS，页面加载慢。
- **Typeform**: 交互漂亮但需注册，不适合快速生成代码。
- **Formspree**: 后端托管，不是代码生成器。
- **W3Schools TryIt**: 只有代码编辑器，无可视化设计。
- **我们的优势**: 
  - 纯前端，零注册，秒开
  - 可视化设计+实时代码预览双栏模式
  - 一键复制HTML代码
  - 免费且无限制

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险（所有数据在浏览器）

## 2. 功能规格

### 核心功能
1. **字段类型选择器**: 文本输入、邮箱、密码、数字、电话、日期、文本域、下拉选择、单选、多选、文件上传、提交按钮
2. **可视化预览区**: 实时渲染表单预览，所见即所得
3. **HTML代码输出**: 自动生成干净的HTML表单代码，一键复制
4. **字段配置**: 标签文本、占位符、必填/可选、选项编辑（下拉/单选/多选）
5. **表单属性**: method(GET/POST)、action URL

### 交互元素（≥3）
- 字段类型选择按钮（12种类型可选）
- 添加/删除/排序字段
- 实时预览面板
- 复制代码按钮
- 字段配置表单（标签名、placeholder等）

### 技术方案
- 纯HTML+CSS+JS
- 左侧：字段类型库 + 已添加字段列表（可拖拽排序）
- 中间：实时预览面板（iframe或直接DOM渲染）
- 右侧：HTML代码输出（带语法高亮的code块）
- 移动端：垂直堆叠布局，面板切换

## 3. EN版本差异
- 字段类型名用英文
- 界面文案全英文
- 示例表单用英文标签
- 生成的代码用英文label

## 4. 验收标准
- [x] 添加字段 → 预览实时更新 → 代码实时生成
- [x] 布局正常、移动端375px不崩
- [x] EN版英文自然、无中文
- [x] 有Schema、无假评分、推荐相关
- [x] 深色主题强制
- [x] AdSense+GA代码在head
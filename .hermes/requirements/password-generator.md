# Password Generator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 需要为各种账户生成密码，重视安全性的用户。关键词："密码生成器"、"随机密码"、"强密码生成"
- **EN用户**: 全球用户，IT从业者、普通网民。"password generator", "strong password generator", "random password"

### 搜索量估计
- 关键词: "password generator" ~550K/月全球, "密码生成器" ~12K/月
- 估计总搜索量: ~600K+/月
- 竞品: LastPass、1Password、NordPass、Bitwarden等密码管理器自带

### 竞品分析
- 竞品1: LastPass Password Generator - 优点：简洁、信任度高；缺点：功能单一，仅长度+字符类型
- 竞品2: 1Password Generator - 优点：支持记忆词密码；缺点：也偏简单
- 竞品3: Avast Password Generator - 优点：免费；缺点：广告多、慢
- 我们的优势: 
  - 完全在浏览器端生成，不上传服务器（强调隐私）
  - 密码熵值可视化
  - 支持三种模式：随机密码、XKCD风格短语密码、PIN码
  - 一键复制
  - 密码强度可视化仪表盘
  - 无广告、无注册

### 前端可行性
- [x] 纯前端可实现（Crypto.getRandomValues）
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险（浏览器本地生成，绝不发送）

## 2. 功能规格

### 核心功能
1. 随机密码生成（默认模式）- 可调长度4-64，可选大写/小写/数字/符号
2. XKCD风格短语密码 - 4-6个随机单词组合，带分隔符
3. PIN码生成 - 4/6/8位数字密码
4. 密码强度实时评估（弱/中/强/极强）+ 熵值bits显示
5. 一键复制 + 重新生成

### 交互元素（≥3）
- 密码长度滑块 (range input)
- 字符类型复选框组（大写、小写、数字、符号）
- 生成/重新生成按钮
- 一键复制按钮
- 模式切换Tab（随机/短语/PIN）
- 密码强度指示条（progress bar）

### 技术方案
- `crypto.getRandomValues()` 用于安全随机数生成
- 密码熵计算：log2(字符集大小^长度)
- 短语密码：内置2000+常用英文单词表
- 密码绝不存储、绝不发送
- 纯CSS动画强度指示条

## 3. EN版本差异
- XKCD模式使用英文单词表（CN版也使用英文单词，这是国际惯例）
- 英文UI文案
- EN版添加"Generate Strong Password"等标题

## 4. 验收标准
- [ ] 输入数据→输出正确（密码符合设定的字符类型和长度）
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分、推荐相关工具
- [ ] 密码生成使用crypto.getRandomValues，非Math.random
- [ ] 强度评估公式正确（熵>=60为强，>=80为极强）

# Syllable Counter - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 英语学习者（背单词分音节）、诗歌创作者（俳句/古诗音节）、UI/UX写手（控制文案音节）、SEO内容创作者
- **EN用户**: Poets (haiku/sonnet), ESL teachers, songwriters, UX writers, students, speech writers
- 关键词: "syllable counter" / "音节计数器" / "syllable checker" / "haiku syllable checker"

### 搜索量估计
- "syllable counter": ~22K/月 (Google Keyword Planner 估计)
- "syllable checker": ~3K/月
- "haiku syllable counter": ~5K/月
- "how many syllables": ~15K/月
- 中文"音节计数器": ~1K/月
- **估计总搜索量: ~50K+/月**
- 竞品: howmanysyllables.com（字典型，非分析型）、syllablecounter.net（基础功能）、poetrysoup.com

### 竞品分析
- **howmanysyllables.com**: 优势=音节字典权威，劣势=只能查单个词，不能分析整段文本
- **syllablecounter.net**: 优势=简洁，劣势=UI老旧、功能单一、仅英文
- **poetrysoup.com**: 优势=诗歌社区，劣势=功能复杂、注册墙、广告多
- **我们的优势**:
  - 整段文本即时分析（非逐词查询）
  - 多语言支持：英文+中文拼音+日文假名
  - 可读性评分（Flesch-Kincaid Grade Level）
  - 俳句/Haiku模式检测（5-7-5音节验证）
  - 逐词音节分解可视化（彩色标注）
  - 完全本地处理，零延迟
  - 无广告、无注册、深色UI

### 前端可行性
- ✅ 纯前端可实现（JS音节分割算法）
- ✅ 无API依赖
- ✅ 无CORS问题
- ✅ 无数据隐私风险（本地计算）

## 2. 功能规格

### 核心功能
1. **文本输入框** - 支持粘贴/键入任意长度文本
2. **实时音节统计** - 总音节数、总词数、总句数、平均每词音节数
3. **逐词分解** - 每个单词的音节数用彩色badge标注
4. **可读性评分** - Flesch-Kincaid Reading Ease + Grade Level
5. **Haiku检测模式** - 自动检测5-7-5结构，三行高亮
6. **中文拼音音节** - 输入拼音自动计音节（如 "nǐ hǎo" → 2音节）
7. **TOP词频** - 显示按音节数排序的词频列表
8. **一键复制** + **清空**

### 交互元素（≥6）
- 文本输入区（textarea）
- 实时统计面板（音节/词/句/字符数）
- 逐词分解展示区（彩色标注）
- Haiku模式切换按钮
- 可读性评分仪表盘
- 复制/清空按钮

### 技术方案
- 英文音节算法：基于元音簇+规则（-ed/-es/silent e等）
- 中文拼音音节：正则匹配拼音音节模式
- Flesch-Kincaid公式：206.835 - 1.015*(总词数/总句数) - 84.6*(总音节数/总词数)
- Grade Level公式：0.39*(总词数/总句数) + 11.8*(总音节数/总词数) - 15.59
- 纯CSS+JS，零依赖

## 3. EN版本差异
- 英文UI文案
- 拼音部分用英文解释
- Haiku说明用英文诗歌传统
- Flesch-Kincaid评分默认英文语境

## 4. 验收标准
- [ ] 输入文本→实时显示音节统计
- [ ] 逐词分解颜色标注正确
- [ ] 可读性评分公式计算正确（用已知文本验证）
- [ ] Haiku模式正确检测5-7-5
- [ ] 中文拼音正确计数
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分、推荐相关工具
- [ ] 深色主题：--bg:#0f172a
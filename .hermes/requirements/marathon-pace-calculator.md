# Marathon Pace Calculator - 需求文档

## 1. 需求验证

### 用户是谁？
- **CN用户**: 跑步爱好者、马拉松跑者、跑步教练。使用"配速"、"马拉松配速"、"半马配速"等术语。场景：比赛前计算目标配速，训练中规划分段策略。
- **EN用户**: Runners training for 5K/10K/half-marathon/marathon. Terms: "pace", "splits", "negative splits", "race predictor".

### 搜索量估计
- 关键词: "marathon pace calculator", "half marathon pace", "running pace calculator", "race pace predictor", "马拉松配速计算器"
- 估计总搜索量: 50K+/月（EN为主，CN为辅）
- 竞品: runnersworld.com, coolrunning.com, omnicalculator.com, runpacers.com

### 竞品分析
- 竞品1: runnersworld.com/pace-calculator — 优点：权威品牌；缺点：广告多、加载慢、无中文
- 竞品2: omnicalculator.com — 优点：功能丰富；缺点：界面杂乱、无跑步专注页
- 竞品3: coolrunning pace calculator — 优点：经典；缺点：UI极老旧、无移动端适配
- 我们的优势: 纯前端秒开、中英文双语、移动端友好、无广告干扰、支持分段配速策略

### 前端可行性
- [x] 纯前端可实现
- [x] 无API依赖
- [x] 无CORS问题
- [x] 无数据隐私风险

## 2. 功能规格

### 核心功能
1. 距离+时间→计算配速（min/km 和 min/mile 双显示）
2. 配速+距离→计算完赛时间
3. 分段计时（每公里/每英里 split time）
4. 负分段策略建议（后半程比前半程快X秒）
5. 预设距离快捷选择（5K/10K/半马/全马）

### 交互元素（≥3）
- 距离输入（km/mile切换）
- 时间输入（HH:MM:SS）
- 配速显示（实时计算）
- 预设距离按钮组
- 分段表格

### 技术方案
- 纯HTML+CSS+JS
- 时间解析：字符串→秒
- 配速计算：总秒数/距离
- 分段生成：每公里时间数组
- 双向计算：改距离/时间→更新配速，改配速→更新总时间

## 3. EN版本差异
- 单位系统：EN默认mile，CN默认km
- 距离预设：EN用mile（3.1mi/6.2mi/13.1mi/26.2mi），CN用km（5km/10km/21.1km/42.2km）
- 术语差异：pace vs 配速，split vs 分段，negative split vs 负分段

## 4. 验收标准
- [ ] 输入距离和时间→正确显示配速
- [ ] 输入配速和距离→正确计算总时间
- [ ] 分段表正确显示每公里时间
- [ ] 布局正常、移动端375px不崩
- [ ] EN版英文自然、无中文
- [ ] 有Schema、无假评分、推荐相关
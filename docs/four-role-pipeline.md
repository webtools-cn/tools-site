# 四角色协作流水线 v2.0

> 核心原则：开发不推送，测试才推送。测试不通过，代码不发布。

## 一、角色与权限

| 角色 | 能做什么 | 不能做什么 |
|:-----|:---------|:-----------|
| PM | 选工具、定需求、定验收标准 | 不碰代码 |
| UX | 定布局规范、检查风格一致性 | 不碰代码 |
| DEV | 写代码、本地自检 | **禁止git commit/push** |
| QA | 验收、git commit、git push | 不改代码（打回给DEV） |

## 二、流程

```
PM: 选工具 + 定验收标准(Checklist)
  ↓
UX: 定布局方案 + 风格规范
  ↓
DEV: 开发CN+EN → 本地自检 → 代码留在工作区（不提交！）
  ↓
QA: 扫描工作区未提交文件 → 逐项验收
  ├── ✅ 全部通过 → git add + commit + push → 线上验证
  └── ❌ 不通过 → 打回DEV（说明问题）→ DEV修 → QA再测
```

## 三、QA验收标准（Checklist）

### 3.1 功能验收
- [ ] 所有按钮可点击，有响应
- [ ] 输入框可输入，有验证
- [ ] 输出结果正确（非空、非undefined、非NaN）
- [ ] 核心功能完整（至少3个交互元素）
- [ ] 复制/清空/重置等辅助功能正常
- [ ] 无JS报错（console无error）

### 3.2 布局与风格
- [ ] 整体布局与站内标准页一致（非左右分栏留空白）
- [ ] CSS变量使用统一（--primary/--bg/--text等）
- [ ] 按钮样式统一（圆角/颜色/大小）
- [ ] 输入框样式统一（边框/背景/圆角）
- [ ] 间距统一（padding/margin与标准页一致）
- [ ] 字体大小统一（h1/h2/body/code）
- [ ] 移动端375px不崩、不溢出

### 3.3 中英文
- [ ] CN版功能正常
- [ ] EN版功能正常
- [ ] lang-switch只有1个，链接正确
- [ ] 中英文内容对应，无遗漏
- [ ] EN版无中文残留

### 3.4 SEO与Schema
- [ ] title格式：工具名 - Free ToolBase
- [ ] meta description 50-160字符
- [ ] SoftwareApplication Schema完整
- [ ] FAQ Schema有真实内容（非空壳mainEntity:[]）
- [ ] HowTo Schema有真实步骤
- [ ] 无虚假aggregateRating
- [ ] canonical标签存在
- [ ] hreflang标签存在

### 3.5 站点同步
- [ ] sitemap.xml已更新
- [ ] llms.txt已更新
- [ ] CN首页卡片已添加
- [ ] EN首页卡片已添加

### 3.6 代码质量
- [ ] JS语法正确（node -c通过）
- [ ] 无innerHTML生成UI
- [ ] 无onclick内超过3行逻辑
- [ ] 无外部JS库引入
- [ ] 无alert/prompt/confirm
- [ ] 无unicode surrogate乱码

## 四、QA验收方法

1. **扫描工作区**：`git status --short` 找未提交文件
2. **本地启动**：`python3 -m http.server 8899`
3. **浏览器实测**：
   - 打开CN版，点所有按钮，输入数据，看输出
   - 打开EN版，同样操作
   - 缩放到375px看移动端
   - 检查console有无报错
4. **代码检查**：node -c验证JS语法
5. **对比检查**：与标准页面对比风格一致性
6. **通过→提交推送**：
   ```bash
   git add -A
   git commit -m "feat(tool): 新增XXX工具 - QA验收通过"
   git push
   ```
7. **线上验证**：push后打开线上页面确认

## 五、模型分配

| 角色 | 模型 | Provider |
|:-----|:-----|:---------|
| PM | deepseek-v4-flash | opencode-zen |
| UX | xopglm52 | xunfei-coding |
| DEV | xopglm52 | xunfei-coding |
| QA | xopdeepseekv4pro | xunfei-coding |

## 六、Cron调度

改造现有"工具站开发"cron（05,35 * * * *）：
- 每个周期执行1个完整流水线
- PM→UX→DEV→QA串行
- QA通过才push，不通过等下个周期重试

## 七、风格基线（标准参照页）

以下页面作为风格标准，新工具必须视觉一致：
- json-formatter（开发者工具代表）
- password-generator（安全工具代表）
- base64-encoder（文本工具代表）
- tax-calculator（计算器代表，横排布局）

## 八、立即生效

从此刻起：
1. DEV角色禁止git commit/push
2. 只有QA角色可以git commit/push
3. QA必须逐项验收通过才推送
4. 任何修改（包括批量修复）都必须走QA验收

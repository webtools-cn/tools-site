# AGENTS.md — free-toolbase.com 开发规范

> 最高行为准则。所有Agent（主+子）在开发/修改本项目时必须遵守。

## 一、技术栈强约束

| 项目 | 标准 | 禁止 |
|:-----|:-----|:-----|
| HTML | 原生HTML5，语义化标签 | `<div>`滥用，缺少doctype |
| CSS | 原生CSS3 + CSS变量 | Sass/Less/Tailwind构建版 |
| JS | Vanilla ES6+ | React/Vue/Angular/jQuery/npm |
| 图标 | SVG内联/emoji | 图标字体库 |
| 部署 | GitHub Pages，纯静态 | 后端/数据库/Node服务 |

## 二、目录结构

```
tools-site/
├── index.html              # 中文首页
├── en/index.html           # 英文首页
├── <tool-name>/            # 每个工具一个目录
│   └── index.html          # 中文工具页
├── en/<tool-name>/         # 英文版工具页
│   └── index.html
├── css/                    # 全局样式（极少用）
├── js/                     # 全局JS（极少用）
├── scripts/                # 质检/批量脚本
│   ├── check_js_syntax.py  # 门0: JS语法
│   ├── check_consistency.py # 门0.5: 页面一致性
│   ├── check_homepage.py   # 门8: 首页完整性
│   ├── check_tool_pages_llm.py # 门9: 大模型质检
│   └── check_functional.py # 门1: 功能验证
├── quality/                # 质检结果
├── .gsc-data/              # GSC数据
├── sitemap.xml
└── llms.txt
```

## 三、工具页面模板（v3.0）

### 必须包含
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>工具名 - Free ToolBase</title>
  <meta name="description" content="工具描述(50-160字符)">
  <!-- Open Graph -->
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <!-- Schema.org -->
  <script type="application/ld+json">{...SoftwareApplication...}</script>
  <!-- CSS变量 -->
  <style>:root { --primary: #4F46E5; --bg: #f8fafc; ... }</style>
</head>
<body>
  <header>...</header>
  <main>
    <h1>工具标题</h1>
    <!-- 交互区：输入+按钮+输出 -->
  </main>
  <footer>...</footer>
  <!-- toast通知组件 -->
  <!-- JS在底部 -->
  <script>...</script>
</body>
</html>
```

### 禁止
- `aggregateRating`（Google会因虚假评分降权）
- `innerHTML`生成UI（应静态HTML+JS事件绑定）
- 内联事件`onclick="..."`内超过3行的逻辑
- 空壳工具（0输入0交互）

## 四、新工具开发流程

1. **选型**：避免与已有2029个工具重复
2. **开发**：先写中文版（`<tool-name>/index.html`），再翻译英文版
3. **自检**：
   - `node -c` 验证JS语法
   - 交互元素 ≥ 3（输入+按钮+输出）
   - 浏览器实测功能正常
   - 移动端375px不崩
4. **提交**：`git add` → `git commit -m "feat(<name>): 新增XXX工具"` → `git push`
5. 更新sitemap和llms.txt

## 五、批量修改铁律

```
全站改动 → 先改1页验证 → 再全量 → 抽样3-5页验证 → git push → 线上验证1页
```

- 出问题用 `git revert` 回滚，不手动修
- 禁止多个批量脚本同一天执行
- 批量脚本不插入可见HTML组件（FAQ/HowTo/评分由模板统一管理）
- Schema和可见内容必须同步，不能重复

## 六、Git提交规范

```
feat(<tool>): 新增XXX工具
fix(<tool>): 修复XXX问题
style: 样式调整
refactor: 代码重构
chore: 批量脚本/质检更新
docs: 文档更新
```

## 七、禁止事项

1. 虚假评分（aggregateRating）
2. URL变更（SEO灾难）
3. 批量脚本同时跑多个
4. 未经验证就push
5. 新工具不写英文版
6. 在工具页加`alert()`（用toast组件）
7. 引入任何外部JS库（含CDN）

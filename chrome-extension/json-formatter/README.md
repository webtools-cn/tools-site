# JSON 格式化工具 - Chrome 扩展

> 基于 Manifest V3 的 Chrome 浏览器插件版 JSON 格式化工具。纯前端 HTML+CSS+JS，零依赖，数据完全本地处理，绝不上传服务器。复用 [webtools-cn.github.io](https://webtools-cn.github.io/json-formatter/) 工具站的核心逻辑。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **格式化** | 将压缩 JSON 展开为 2 空格缩进的多行格式，提升可读性 |
| **压缩** | 移除所有空白字符，生成最小体积 JSON |
| **验证** | 实时检测 JSON 语法错误，精确定位到行号和列号并高亮上下文 |
| **树状视图** | 可折叠/展开的交互式树形结构，便于浏览大型 JSON 层级关系 |
| **一键复制** | 一键复制格式化结果到剪贴板 |
| **一键粘贴** | 从剪贴板读取 JSON 直接填入输入框 |
| **统计信息** | 自动统计节点数、最大深度、对象/数组数量、字符长度 |
| **快捷键** | `Ctrl/Cmd + Enter` 快速格式化 |
| **深色主题** | 与工具站风格一致（`#0f172a` / `#1e293b`） |
| **完全离线** | 无需联网，所有解析在本地完成 |

## 📦 文件结构

```
json-formatter/
├── manifest.json        # Manifest V3 配置文件
├── popup.html           # 弹窗 UI 结构
├── popup.css            # 深色主题样式
├── popup.js             # 核心逻辑（格式化/压缩/验证/树状视图/统计）
├── icons/
│   ├── icon16.png       # 工具栏图标 16×16
│   ├── icon48.png       # 扩展管理页图标 48×48
│   └── icon128.png      # Chrome 商店图标 128×128
└── README.md            # 本说明文档
```

## 🚀 本地安装（开发者模式）

1. 打开 Chrome 浏览器，地址栏输入 `chrome://extensions/`
2. 右上角打开 **「开发者模式」** 开关
3. 点击 **「加载已解压的扩展程序」**
4. 选择本目录 `chrome-extension/json-formatter/`
5. 扩展即出现在工具栏，点击图标即可弹出 JSON 格式化工具窗口
6. 可将图标固定（📌）到工具栏方便随时使用

## 🎨 设计说明

- **Popup 尺寸**：400×500px，紧凑但功能完整
- **布局**：顶部标题栏 → 操作按钮 → 输入框 → 输出区（格式化文本/树状视图 Tab 切换）→ 消息提示 → 统计栏 → 底部操作栏（复制/清空 + 工具站链接）
- **配色**：深色主题，背景 `#0f172a`，卡片 `#1e293b`，主色青色 `#06b6d4`，错误红色 `#ef4444`，成功绿色 `#10b981`
- **字体**：系统字体 + JetBrains Mono 等宽字体（代码区）
- **隐私**：`manifest.json` 中 `permissions` 为空，`host_permissions` 为空，不申请任何敏感权限

## 🔒 隐私与权限

本扩展**不申请任何权限**（`permissions: []`，`host_permissions: []`），仅作为本地工具运行：

- ❌ 不读取、不修改任何网页内容
- ❌ 不发起任何网络请求
- ❌ 不存储任何用户数据
- ✅ 所有 JSON 解析、格式化、验证均在浏览器本地完成
- ✅ 支持 `offline_enabled: true`，完全离线可用

## 🌐 与在线版的关系

本插件复用了 [在线 JSON 格式化工具](https://webtools-cn.github.io/json-formatter/) 的核心算法（解析、错误定位、统计、树状视图），针对浏览器弹窗场景做了紧凑布局适配。在线版还提供 JSONPath 查询、转义/去转义、键排序、下载等进阶功能，欢迎访问体验。

底部 `🌐 webtools-cn.github.io` 链接点击后会在新标签页打开在线完整版工具站。

## 📋 Chrome Web Store 上架清单

发布到 Chrome Web Store 需要准备以下材料：

- [x] `manifest.json`（Manifest V3）
- [x] `popup.html` / `popup.css` / `popup.js`
- [x] 图标 `icon16.png` / `icon48.png` / `icon128.png`
- [x] 扩展名称：**JSON 格式化工具**
- [x] 简短描述（≤132 字符）：`纯前端本地处理的JSON格式化/压缩/验证/树状视图工具，数据不上传服务器。复用 webtools-cn.github.io 工具站逻辑。`
- [x] 分类：Developer Tools（开发者工具）
- [x] 语言：中文（简体）
- [x] 单文件隐私政策说明：本扩展不收集、不传输任何用户数据

### 上架步骤

1. 将本目录打包为 zip：`cd chrome-extension && zip -r json-formatter.zip json-formatter/`
2. 访问 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
3. 支付一次性 $5 开发者注册费（如未注册）
4. 点击「新建项目」上传 zip 包
5. 填写商店信息（截图、描述、分类、语言）
6. 填写隐私权声明（选择「不收集任何数据」）
7. 提交审核（通常 1-3 个工作日）

### 商店截图建议

- 截图 1：popup 主界面 + 示例 JSON 格式化结果
- 截图 2：错误定位高亮效果
- 截图 3：树状视图折叠展开效果
- 尺寸：1280×800 或 640×400

## 🛠️ 技术细节

- **Manifest V3**：使用 `action.default_popup`，无 background service worker
- **零依赖**：不引用任何外部 CDN 或库，纯原生 JS
- **复用算法**：`parseJSONWithPosition`、`computeStats`、`renderTreeView` 均与工具站逻辑一致
- **剪贴板兼容**：优先 `navigator.clipboard`，失败回退 `document.execCommand('copy')`
- **CSP 友好**：所有 JS/CSS 均为独立文件，无内联脚本，符合 MV3 默认 CSP

## 📝 版本历史

- **v1.0.0** (2026-07-02)：首个版本，支持格式化/压缩/验证/树状视图/复制/粘贴/统计

## 📮 反馈与联系

- 工具站：<https://webtools-cn.github.io>
- 问题反馈：REDACTED_EMAIL

---

💡 如果觉得好用，欢迎给工具站点个 ⭐ Star，也欢迎在 Chrome 商店留下评价！

# Hash 哈希生成器 - Chrome 扩展

> 基于 Manifest V3 的 Chrome 浏览器插件版 Hash 哈希生成器。纯前端 HTML+CSS+JS，零依赖，数据完全本地处理，绝不上传服务器。复用 [webtools-cn.github.io](https://webtools-cn.github.io/hash-generator/) 工具站的核心逻辑。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **文本哈希** | 输入任意文本，实时计算 MD5 / SHA-1 / SHA-256 / SHA-384 / SHA-512 |
| **文件哈希** | 拖拽或点击选择文件，本地计算文件哈希值，支持任意文件类型 |
| **HMAC** | 支持 HMAC-MD5 / HMAC-SHA1 / HMAC-SHA256 / HMAC-SHA384 / HMAC-SHA512 |
| **一键复制** | 每个哈希结果右侧独立复制按钮，支持一键复制全部结果 |
| **大写输出** | 可选大写/小写十六进制输出 |
| **实时计算** | 文本输入时自动延迟计算，无需手动点击 |
| **深色主题** | 与工具站风格一致（`#0f172a` / `#1e293b`） |
| **完全离线** | 无需联网，所有计算在浏览器本地完成 |

## 📦 文件结构

```
hash-generator/
├── manifest.json        # Manifest V3 配置文件
├── popup.html           # 弹窗 UI 结构
├── popup.css            # 深色主题样式
├── popup.js             # 核心逻辑（MD5/SHA-1/SHA-256/384/512、HMAC、文件哈希）
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
4. 选择本目录 `chrome-extension/hash-generator/`
5. 扩展即出现在工具栏，点击图标即可弹出 Hash 哈希生成器窗口
6. 可将图标固定（📌）到工具栏方便随时使用

## 🎨 设计说明

- **Popup 尺寸**：400×500px，紧凑但功能完整
- **布局**：顶部标题栏 → Tab 切换（文本/文件/HMAC）→ 输入区 → 结果列表 → 底部操作栏（复制全部 + 工具站链接）
- **配色**：深色主题，背景 `#0f172a`，卡片 `#1e293b`，主色青色 `#06b6d4`
- **字体**：系统字体 + JetBrains Mono 等宽字体（哈希值显示区）
- **隐私**：`manifest.json` 中 `permissions` 为空，`host_permissions` 为空，不申请任何敏感权限

## 🔒 隐私与权限

本扩展**不申请任何权限**（`permissions: []`，`host_permissions: []`），仅作为本地工具运行：

- ❌ 不读取、不修改任何网页内容
- ❌ 不发起任何网络请求
- ❌ 不存储任何用户数据
- ✅ 所有哈希计算均在浏览器本地完成
- ✅ 支持 `offline_enabled: true`，完全离线可用

## 🌐 与在线版的关系

本插件复用了 [在线 Hash 哈希生成器](https://webtools-cn.github.io/hash-generator/) 的核心算法（MD5/SHA-1 纯 JS 实现 + Web Crypto API），针对浏览器弹窗场景做了紧凑布局适配。在线版还提供哈希对比、算法知识说明等更多功能，欢迎访问体验。

底部 `🌐 webtools-cn.github.io` 链接点击后会在新标签页打开在线完整版工具站。

## 📋 Chrome Web Store 上架清单

发布到 Chrome Web Store 需要准备以下材料：

- [x] `manifest.json`（Manifest V3）
- [x] `popup.html` / `popup.css` / `popup.js`
- [x] 图标 `icon16.png` / `icon48.png` / `icon128.png`
- [x] 扩展名称：**Hash 哈希生成器**
- [x] 简短描述（≤132 字符）：`纯前端本地处理的Hash哈希生成器，支持MD5/SHA-1/SHA-256/SHA-384/SHA-512文本哈希、HMAC密钥消息认证、文件哈希拖拽计算，数据不上传服务器。复用 webtools-cn.github.io 工具站逻辑。`
- [x] 分类：Developer Tools（开发者工具）
- [x] 语言：中文（简体）
- [x] 单文件隐私政策说明：本扩展不收集、不传输任何用户数据

### 上架步骤

1. 将本目录打包为 zip：`cd chrome-extension && zip -r hash-generator.zip hash-generator/`
2. 访问 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
3. 支付一次性 $5 开发者注册费（如未注册）
4. 点击「新建项目」上传 zip 包
5. 填写商店信息（截图、描述、分类、语言）
6. 填写隐私权声明（选择「不收集任何数据」）
7. 提交审核（通常 1-3 个工作日）

### 商店截图建议

- 截图 1：文本哈希 Tab，展示多个哈希结果
- 截图 2：文件哈希 Tab，展示拖拽文件计算结果
- 截图 3：HMAC Tab，展示密钥输入与结果
- 尺寸：1280×800 或 640×400

## 🛠️ 技术细节

- **Manifest V3**：使用 `action.default_popup`，无 background service worker
- **零依赖**：不引用任何外部 CDN 或库，纯原生 JS
- **复用算法**：`md5()`、`sha1()`、`computeHMAC()` 均与工具站逻辑一致
- **哈希来源**：MD5 和 SHA-1 为纯 JavaScript 实现；SHA-256/384/512 使用浏览器原生 Web Crypto API
- **剪贴板兼容**：优先 `navigator.clipboard`，失败回退 `document.execCommand('copy')`
- **CSP 友好**：所有 JS/CSS 均为独立文件，无内联脚本，符合 MV3 默认 CSP

## 📝 版本历史

- **v1.0.0** (2026-07-02)：首个版本，支持文本哈希/文件哈希/HMAC/一键复制

## 📮 反馈与联系

- 工具站：<https://webtools-cn.github.io>
- 问题反馈：REDACTED_EMAIL

---

💡 如果觉得好用，欢迎给工具站点个 ⭐ Star，也欢迎在 Chrome 商店留下评价！

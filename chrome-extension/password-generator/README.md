# 密码生成器 - Chrome 扩展

> 基于 Manifest V3 的 Chrome 浏览器插件版密码生成工具。纯前端 HTML+CSS+JS，零依赖，数据完全本地处理，绝不上传服务器。复用 [webtools-cn.github.io](https://webtools-cn.github.io/password-generator/) 工具站的核心逻辑。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **密码生成** | 采用浏览器 Web Crypto API（`crypto.getRandomValues`）密码学安全随机数生成强密码 |
| **长度设置** | 支持 4~64 位密码长度，通过滑块或数字输入框实时调整 |
| **字符集选择** | 可自由开关大写字母、小写字母、数字、特殊符号四类字符 |
| **排除易混淆字符** | 一键排除 `l / 1 / I / 0 / O`，避免手动输入时出错 |
| **密码强度检测** | 实时计算熵值（bits），分级显示：弱 / 中等 / 强 / 极强 |
| **一键复制** | 点击「复制密码」或 `Ctrl+C` 快捷键，优先 `navigator.clipboard` 回退兜底 |
| **历史记录** | 自动保存最近生成的 10 条密码，支持单条复制和一键清空 |
| **快捷键** | `Space` / `Enter` 快速重新生成，`Ctrl+C` 复制当前密码 |
| **深色主题** | 与工具站风格一致（`#0f172a` / `#1e293b`），popup 尺寸 400×500px |
| **完全离线** | 无需联网，所有生成在本地完成 |

## 📦 文件结构

```
password-generator/
├── manifest.json        # Manifest V3 配置文件
├── popup.html           # 弹窗 UI 结构
├── popup.css            # 深色主题样式
├── popup.js             # 核心逻辑（生成/强度检测/复制/历史记录）
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
4. 选择本目录 `chrome-extension/password-generator/`
5. 扩展即出现在工具栏，点击图标即可弹出密码生成器窗口
6. 可将图标固定（📌）到工具栏方便随时使用

## 🎨 设计说明

- **Popup 尺寸**：400×500px，紧凑但功能完整
- **布局**：顶部标题栏 → 密码显示区（含强度条）→ 操作按钮 → 密码设置区（长度/字符集）→ 历史记录 → 底部工具站链接
- **配色**：深色主题，背景 `#0f172a`，卡片 `#1e293b`，主色青色 `#06b6d4`，错误红色 `#ef4444`，成功绿色 `#10b981`
- **字体**：系统字体 + JetBrains Mono 等宽字体（密码显示区）
- **隐私**：`manifest.json` 中 `permissions` 为空，`host_permissions` 为空，不申请任何敏感权限

## 🔒 隐私与权限

本扩展**不申请任何权限**（`permissions: []`，`host_permissions: []`），仅作为本地工具运行：

- ❌ 不读取、不修改任何网页内容
- ❌ 不发起任何网络请求
- ❌ 不存储任何用户数据（历史记录仅在 popup 打开期间保存在内存中）
- ✅ 所有密码生成、强度计算均在浏览器本地完成
- ✅ 支持 `offline_enabled: true`，完全离线可用

## 🌐 与在线版的关系

本插件复用了 [在线密码生成器](https://webtools-cn.github.io/password-generator/) 的核心算法（Web Crypto API 随机数、熵值计算、强度分级），针对浏览器弹窗场景做了紧凑布局适配。在线版还提供场景预设（WiFi/银行/API Key/可读密码）、批量生成、排除特定符号、SEO 知识科普等进阶功能，欢迎访问体验。

底部 `🌐 webtools-cn.github.io` 链接点击后会在新标签页打开在线完整版工具站。

## 📋 Chrome Web Store 上架清单

发布到 Chrome Web Store 需要准备以下材料：

- [x] `manifest.json`（Manifest V3）
- [x] `popup.html` / `popup.css` / `popup.js`
- [x] 图标 `icon16.png` / `icon48.png` / `icon128.png`
- [x] 扩展名称：**密码生成器**
- [x] 简短描述（≤132 字符）：`纯前端本地密码生成工具，采用Web Crypto API密码学安全随机数。支持自定义长度、字符集选择、密码强度检测、一键复制、历史记录。`
- [x] 分类：Productivity（生产力工具）
- [x] 语言：中文（简体）
- [x] 单文件隐私政策说明：本扩展不收集、不传输任何用户数据

### 上架步骤

1. 将本目录打包为 zip：`cd chrome-extension && zip -r password-generator.zip password-generator/`
2. 访问 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
3. 支付一次性 $5 开发者注册费（如未注册）
4. 点击「新建项目」上传 zip 包
5. 填写商店信息（截图、描述、分类、语言）
6. 填写隐私权声明（选择「不收集任何数据」）
7. 提交审核（通常 1-3 个工作日）

### 商店截图建议

- 截图 1：popup 主界面 + 已生成的密码 + 强度显示
- 截图 2：历史记录区展开效果
- 截图 3：调整长度和字符集后的生成效果
- 尺寸：1280×800 或 640×400

## 🛠️ 技术细节

- **Manifest V3**：使用 `action.default_popup`，无 background service worker
- **零依赖**：不引用任何外部 CDN 或库，纯原生 JS
- **复用算法**：`secureRandomInt`、`calculateEntropy`、`getStrengthLevel`、`generatePassword` 均与工具站逻辑一致
- **剪贴板兼容**：优先 `navigator.clipboard`，失败回退 `document.execCommand('copy')`
- **CSP 友好**：所有 JS/CSS 均为独立文件，无内联脚本，符合 MV3 默认 CSP

## 📝 版本历史

- **v1.0.0** (2026-07-02)：首个版本，支持密码生成/强度检测/字符集选择/一键复制/历史记录

## 📮 反馈与联系

- 工具站：<https://webtools-cn.github.io>
- 问题反馈：REDACTED_EMAIL

---

💡 如果觉得好用，欢迎给工具站点个 ⭐ Star，也欢迎在 Chrome 商店留下评价！

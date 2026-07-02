# 二维码生成器 - Chrome 扩展

> 基于 Manifest V3 的 Chrome 浏览器插件版二维码生成工具。纯前端 HTML+CSS+JS，零依赖，数据完全本地处理，绝不上传服务器。复用 [webtools-cn.github.io](https://webtools-cn.github.io/qr-generator/) 工具站核心逻辑。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **文本/URL 转二维码** | 输入任意文本、网址、WiFi 配置等内容，即时生成标准 QR 码 |
| **颜色自定义** | 可自由设置前景色和背景色，支持高对比度配色 |
| **尺寸调节** | 实时调节生成图片尺寸（160px - 320px），自动保持清晰度 |
| **纠错级别** | 支持 L/M/Q/H 四级纠错，默认 M 级（~15% 容错） |
| **PNG 下载** | 一键下载高分辨率 PNG 位图 |
| **SVG 下载** | 一键下载矢量 SVG 格式，无限放大不模糊 |
| **复制图片** | 一键复制二维码图片到剪贴板，方便直接粘贴使用 |
| **一键粘贴** | 从剪贴板读取内容直接填入输入框 |
| **深色主题** | 与工具站风格一致（`#0f172a` / `#1e293b`） |
| **完全离线** | 无需联网，所有编码计算在本地完成 |

## 📦 文件结构

```
qr-generator/
├── manifest.json        # Manifest V3 配置文件
├── popup.html           # 弹窗 UI 结构
├── popup.css            # 深色主题样式
├── popup.js             # 核心逻辑（QR 编码/渲染/下载/复制）
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
4. 选择本目录 `chrome-extension/qr-generator/`
5. 扩展即出现在工具栏，点击图标即可弹出二维码生成器窗口
6. 可将图标固定（📌）到工具栏方便随时使用

## 🎨 设计说明

- **Popup 尺寸**：400×500px，紧凑但功能完整
- **布局**：顶部标题栏 → 输入区 → 设置区（纠错/颜色/尺寸）→ 预览区 → 操作栏（PNG/SVG/下载/复制）→ 底部工具站链接
- **配色**：深色主题，背景 `#0f172a`，卡片 `#1e293b`，主色青色 `#06b6d4`，错误红色 `#ef4444`
- **字体**：系统字体栈
- **隐私**：`manifest.json` 中 `permissions` 为空，`host_permissions` 为空，不申请任何敏感权限

## 🔒 隐私与权限

本扩展**不申请任何权限**（`permissions: []`，`host_permissions: []`），仅作为本地工具运行：

- ❌ 不读取、不修改任何网页内容
- ❌ 不发起任何网络请求
- ❌ 不存储任何用户数据
- ✅ 所有 QR 编码、渲染、下载均在浏览器本地完成
- ✅ 支持 `offline_enabled: true`，完全离线可用

## 🌐 与在线版的关系

本插件复用了 [在线二维码生成器](https://webtools-cn.github.io/qr-generator/) 的核心 QR 编码算法（基于 Reed-Solomon 的纯 JavaScript 实现），针对浏览器弹窗场景做了紧凑布局适配。在线版还支持批量生成、Logo 嵌入、WiFi/名片预设模板、SVG 精细控制等进阶功能，欢迎访问体验。

底部 `🌐 webtools-cn.github.io` 链接点击后会在新标签页打开在线完整版工具站。

## 📋 Chrome Web Store 上架清单

发布到 Chrome Web Store 需要准备以下材料：

- [x] `manifest.json`（Manifest V3）
- [x] `popup.html` / `popup.css` / `popup.js`
- [x] 图标 `icon16.png` / `icon48.png` / `icon128.png`
- [x] 扩展名称：**二维码生成器**
- [x] 简短描述（≤132 字符）：`纯前端本地生成的二维码工具，支持文本/网址/WiFi等格式，自定义颜色尺寸，下载PNG/SVG，数据不上传服务器。`
- [x] 分类：Developer Tools（开发者工具）
- [x] 语言：中文（简体）
- [x] 单文件隐私政策说明：本扩展不收集、不传输任何用户数据

### 上架步骤

1. 将本目录打包为 zip：`cd chrome-extension && zip -r qr-generator.zip qr-generator/`
2. 访问 [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
3. 支付一次性 $5 开发者注册费（如未注册）
4. 点击「新建项目」上传 zip 包
5. 填写商店信息（截图、描述、分类、语言）
6. 填写隐私权声明（选择「不收集任何数据」）
7. 提交审核（通常 1-3 个工作日）

### 商店截图建议

- 截图 1：popup 主界面 + 默认网址二维码预览
- 截图 2：颜色自定义（非黑白配色）效果
- 截图 3：SVG 下载提示或复制成功提示
- 尺寸：1280×800 或 640×400

## 🛠️ 技术细节

- **Manifest V3**：使用 `action.default_popup`，无 background service worker
- **零依赖**：不引用任何外部 CDN 或库，纯原生 JS
- **复用算法**：`encodeQR`、`drawQR`、`generateSVG` 均与工具站逻辑一致
- **纯前端 QR 编码**：完整实现 QR Code Model 2 规范，包括数据分块、Reed-Solomon 纠错、掩码评估、格式/版本信息编码
- **剪贴板兼容**：优先 `navigator.clipboard`，失败回退 `document.execCommand('copy')`
- **CSP 友好**：所有 JS/CSS 均为独立文件，无内联脚本，符合 MV3 默认 CSP

## 📝 版本历史

- **v1.0.0** (2026-07-02)：首个版本，支持文本/URL 转二维码、颜色自定义、尺寸调节、PNG/SVG 下载、复制、四级纠错

## 📮 反馈与联系

- 工具站：<https://webtools-cn.github.io>
- 问题反馈：REDACTED_EMAIL

---

💡 如果觉得好用，欢迎给工具站点个 ⭐ Star，也欢迎在 Chrome 商店留下评价！

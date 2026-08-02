# WiFi二维码生成器 — 需求文档

## 1. 关键词分析
- `wifi qr code generator` / `wifi qr code` / `wifi二维码` / `wifi qr code maker`
- 估算月搜索量：20K-60K（多个变体合计）
- 竞品：qifi.org（极简）、qr-code-generator.com（要注册）、各种小站

## 2. 竞品分析
| 竞品 | 优势 | 劣势 |
|:-----|:-----|:-----|
| qifi.org | 极简、开源、速度快 | 功能太少、UI丑陋、无打印布局 |
| qr-code-generator.com | 功能多 | 要注册、有水印、广告多 |
| 各种小站 | 免费 | 广告满天飞、体验差 |

## 3. 差异化
- **深色主题**：`#0f172a` 背景，现代暗色界面（竞品几乎都是白色）
- **打印友好**：一键生成可打印的卡片布局（含SSID+密码明文+二维码）
- **多安全类型**：WPA/WPA2/WEP/nopass 全部支持
- **隐藏SSID选项**：支持隐藏网络的二维码
- **一键下载**：PNG下载 + 一键打印
- **数据完全本地**：WiFi密码不出浏览器
- **零广告干扰**

## 4. 用户场景
1. 咖啡馆/餐厅老板 → 生成WiFi二维码贴墙上
2. 家庭用户 → 客人来访扫码连WiFi
3. 办公室 → 访客WiFi二维码
4. Airbnb房东 → 入住指南里的WiFi信息
5. 活动组织者 → 活动现场WiFi分享

覆盖率: 100%

## 5. 功能清单
- ✅ SSID输入（网络名称）
- ✅ 密码输入（支持显示/隐藏切换）
- ✅ 加密类型选择（WPA/WPA2/WEP/nopass）
- ✅ 隐藏SSID选项
- ✅ 实时二维码预览（Canvas渲染）
- ✅ 打印友好卡片布局（含WiFi信息明文）
- ✅ 下载PNG
- ✅ 一键打印
- ✅ 响应式设计

## 6. 技术方案
- 纯HTML+CSS+JS，零依赖
- QR码编码：自实现QR编码算法或内联轻量库
- Canvas渲染二维码
- WiFi QR格式：`WIFI:T:<encryption>;S:<ssid>;P:<password>;H:<hidden>;;`
- 深色主题：`--bg:#0f172a --card-bg:#1e293b`

## 7. SEO标题
- CN: WiFi二维码生成器 - 在线WiFi密码二维码制作 | Free ToolBase
- EN: WiFi QR Code Generator - Free WiFi Password QR Maker | Free ToolBase
# DEV2 Batch Fix Report — 2026-07-25

## 完成内容：批量修复"0交互空壳工具" schema/title问题

### 修复的页面（7个）

| 任务ID | 工具 | 修复内容 |
|--------|------|----------|
| T137 | about | ✅ title分隔符·→\|, ✅ 修复og:title重复, ✅ SoftwareApplication→AboutPage, ✅ 移除HowTo/FAQPage |
| T230 | contact | ✅ title分隔符·→\|, ✅ 修复og:title/h1重复, ✅ SoftwareApplication→ContactPage, ✅ 移除HowTo, ✅ FAQPage改为contact相关 |
| T205 | calc | ✅ title分隔符·→\|, ✅ SoftwareApplication→CollectionPage, ✅ 移除HowTo |
| T231 | converter | ✅ title分隔符·→\|, ✅ SoftwareApplication→CollectionPage, ✅ 移除HowTo |
| T234 | creative | ✅ title分隔符·→\|, ✅ SoftwareApplication→CollectionPage, ✅ 移除HowTo |
| T317 | design | ✅ title分隔符·→\|, ✅ SoftwareApplication→CollectionPage, ✅ 移除HowTo |
| T319 | dev | ✅ title分隔符·→\|, ✅ SoftwareApplication→CollectionPage, ✅ 移除HowTo |

### 修复模式总结

对于"0交互空壳工具"（实为信息页/目录页），核心问题是：
1. **Schema类型错误**：信息页使用SoftwareApplication（应使用AboutPage/ContactPage），目录页使用SoftwareApplication（应使用CollectionPage）
2. **泛用HowToSchema**：关于/联系页面使用通用HowTo步骤（完全无关）
3. **泛用FAQPageSchema**：关于/联系页面使用工具FAQ模板（完全不相关）
4. **title分隔符**：·（中文符号）→ |（标准分隔符）
5. **og:title重复值**：部分页面og:title包含重复文字如"About About"/"Contact Contact"

### 状态
- Kanban已更新：7个任务从backlog→dev-in-progress（附qa_pass消息）
- 未commit/push（DEV2铁律）

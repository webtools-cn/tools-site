# Keyboard Shortcut Visualizer - 需求文档

## 1. 市场分析
- **关键词**: keyboard shortcut visualizer, visual keyboard shortcuts, keyboard shortcut guide, keyboard shortcut reference, shortcut key map
- **月搜索量（估算）**: 80,000+（含长尾：keyboard shortcuts 50K + shortcut guide 20K + visual keyboard 10K）
- **竞品**: 
  - keybr.com（打字练习，非快捷键参考）
  - shortcutworld.com（纯文本列表，无可视化）
  - defkey.com（文本列表，无交互键盘）
  - useyourkeyboard.com（基础教程）
- **差异化**: 
  - 交互式可视化键盘（Canvas绘制，按下高亮）
  - 按应用分类的快捷键数据库（VS Code / Chrome / Photoshop / Excel / Windows / Mac 等）
  - 搜索功能：按键找功能、功能找按键
  - Windows/Mac键盘布局切换
  - 实时按键检测+快捷键组合显示
  - 深色主题，现代UI
  - 完全免费，无需注册

## 2. 功能清单
### 核心功能
1. **Canvas键盘渲染**: 完整QWERTY键盘布局（含功能键、数字键、修饰键、导航键、数字小键盘）
2. **实时按键检测**: 用户按下键盘时，Canvas上对应按键高亮，同时显示按下的组合键
3. **快捷键数据库**: 内置常见应用快捷键（VS Code, Chrome, Windows, Mac, Excel, Photoshop, Terminal等），按应用分类
4. **搜索功能**: 
   - 搜索按键名→显示该键在各应用中的功能
   - 搜索功能描述→显示对应快捷键
5. **Windows/Mac切换**: 一键切换键盘布局（Ctrl↔Cmd, Alt↔Option, Win↔⌘）
6. **快捷键卡片**: 点击某个应用→显示该应用所有快捷键的卡片列表
7. **复制快捷键**: 点击快捷键卡片可复制
8. **颜色编码**: 不同修饰键组合用不同颜色高亮（Ctrl=蓝, Alt=橙, Shift=绿, Win/Cmd=紫）

### 交互元素（≥6）
- Canvas键盘（可点击）
- 应用选择下拉菜单
- 搜索输入框
- Windows/Mac切换按钮
- 快捷键卡片列表
- 实时按键显示面板
- 复制按钮

## 3. 技术方案
- 纯HTML+CSS+JS，零外部依赖
- Canvas 2D绘制键盘布局（约800x300px）
- keydown/keyup事件监听
- 快捷键数据库用JS对象存储
- CSS Grid布局（键盘区域+快捷键列表）
- 深色主题: --bg:#0f172a

## 4. 页面设计
- 顶部：标题 + Win/Mac切换 + 应用选择器 + 搜索框
- 中部：Canvas键盘可视化（可交互）
- 底部：快捷键卡片列表（按应用筛选）
- 响应式：移动端缩小键盘，单列布局

## 5. 快捷键数据库覆盖
至少包含以下应用的常用快捷键：
- **系统**: Windows通用, macOS通用
- **浏览器**: Chrome, Firefox, Edge
- **编辑器**: VS Code, Sublime Text, Vim基础
- **办公**: Excel, Word, PowerPoint, Google Sheets
- **设计**: Photoshop, Figma基础
- **终端**: Windows Terminal, macOS Terminal, Linux常用
- **其他**: Slack, Notion, GitHub

每个应用20-40个最常用快捷键，总计约300-400个快捷键条目。

## 6. 竞品对比
| 功能 | defkey.com | shortcutworld | keycombiner | 我们 |
|------|:---:|:---:|:---:|:---:|
| 可视化键盘 | ✗ | ✗ | ✗ | ✓ |
| 实时按键检测 | ✗ | ✗ | ✗ | ✓ |
| 多应用分类 | ✓ | ✓ | ✓ | ✓ |
| 搜索 | ✓ | ✗ | ✓ | ✓ |
| Win/Mac切换 | ✗ | ✗ | ✓ | ✓ |
| 免费 | ✓ | ✓ | 部分 | ✓ |
| 无需注册 | ✓ | ✓ | ✗ | ✓ |
| 深色主题 | ✗ | ✗ | ✓ | ✓ |

## 7. EN版本差异
- 快捷键数据库用英文（本来就是英文为主）
- 界面文案英文
- Mac/Win键盘布局用英文标注
- 应用名称保持英文

## 8. 验收标准
- ✅ Canvas键盘正确渲染，按键可识别
- ✅ 按下物理键盘→Canvas对应按键高亮
- ✅ 应用切换→快捷键列表更新
- ✅ 搜索功能正常（双向搜索）
- ✅ Win/Mac切换→键盘布局更新
- ✅ 快捷键卡片可复制
- ✅ 移动端375px不崩
- ✅ EN版英文自然、无中文
- ✅ Schema完整（SoftwareApplication+FAQ+Breadcrumb）
- ✅ 深色主题强制：--bg:#0f172a
- ✅ AdSense+GA代码在head
- ✅ node -c通过

## 决策：开始开发 ✅
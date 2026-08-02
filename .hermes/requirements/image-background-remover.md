# Image Background Remover - 需求文档

## 1. 关键词分析
- "remove background from image": ~50万月搜索量（全球）
- "background remover online": ~30万
- "free background remover": ~20万
- "image background remover": ~15万
- 总市场搜索量：100万+/月

## 2. 竞品分析

### 竞品1: remove.bg
- 功能：AI自动抠图，一键去除
- 优点：质量极高，速度快
- 缺点：付费（免费版低分辨率），需上传到服务器
- 月流量：5000万+

### 竞品2: Adobe Express Background Remover
- 功能：AI抠图
- 优点：品牌信任，质量好
- 缺点：需登录

### 竞品3: Pixelied Background Remover
- 功能：在线AI抠图+编辑
- 优点：免费，质量好
- 缺点：有水印

## 3. 差异化策略
我们的定位：**完全本地处理的免费背景工具套装**

- ✅ 所有处理在浏览器本地完成，数据不上传服务器（隐私卖点）
- ✅ 多种背景处理方式：颜色阈值去除 / 手动擦除 / 魔术棒 / 矩形选择
- ✅ 支持替换背景色/渐变/图片
- ✅ 完全免费，无水印，无分辨率限制
- ✅ 下载PNG（透明背景）

**核心差异**：隐私优先 + 无需上传 + 多工具合一

## 4. 用户场景
1. 电商卖家去除产品图背景 → 替换纯白背景
2. 设计师快速抠图 → 导出透明PNG
3. 社交媒体用户更换自拍背景
4. 开发者去除截图背景 → 用于文档

## 5. 功能清单
### MVP (本次)
- 上传图片（拖拽/点击）
- 颜色阈值去除（可调容差）
- 点击颜色拾取去除
- 手动橡皮擦
- 背景替换（纯色/渐变/另一张图片）
- 撤销/重做
- 下载PNG
- 缩放和拖拽画布

### 后续迭代
- 魔术棒工具
- 套索工具
- 矩形/椭圆选区
- 边缘羽化

## 6. 技术方案
- Canvas 2D API处理像素
- getImageData / putImageData 像素级操作
- 颜色空间转换（RGB→HSL用于颜色匹配）
- FileReader读取图片
- toBlob导出PNG

## 7. 搜索量验证
- 确认>1000月搜索量：✅（50万+）

## 8. URL规划
- CN: /image-background-remover/
- EN: /en/image-background-remover/

## 决策：开始开发

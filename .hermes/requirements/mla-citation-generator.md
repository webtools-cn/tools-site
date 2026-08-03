# MLA Citation Generator - 需求文档

## 1. 关键词搜索量
- "MLA citation generator": 月搜索量 ~90K-120K (全球)
- "MLA format citation": ~40K
- "MLA works cited": ~30K
- 远超1000的门槛

## 2. 竞品分析
| 竞品 | 功能 | 差异化机会 |
|------|------|-----------|
| EasyBib | 多格式、付费解锁高级功能 | 我们完全免费、无广告弹窗 |
| CitationMachine | 多格式、注册墙 | 我们无需注册 |
| BibMe | 多格式、有广告 | 我们纯前端、隐私安全 |
| MyBib | MLA/APA/Harvard | 我们深色主题、更快 |

## 3. 功能清单
- [x] 支持来源类型：Book, Website, Journal Article, Newspaper Article, Film/Video
- [x] MLA 9th Edition (2021) 格式
- [x] Works Cited 条目生成
- [x] In-text citation 生成
- [x] 多作者处理（1人/2人/3人+/企业作者/无作者）
- [x] 悬挂缩进显示
- [x] 历史记录（localStorage）
- [x] 一键复制
- [x] 导出为文本

## 4. 用户场景覆盖率
1. 学生写论文需要MLA格式引用 ✓
2. 研究人员引用网站文章 ✓
3. 引用书籍（含版次、多个作者）✓
4. 引用学术期刊（含卷号、期号、页码、DOI）✓
5. 引用新闻报道 ✓
6. 引用视频/电影 ✓
7. 无作者的情况 ✓
8. 企业作者 ✓

覆盖率 > 90%

## 5. 差异化
- 深色主题（与竞品全白背景区分）
- 纯前端，数据不上传
- MLA 9th最新版
- 悬挂缩进正确显示
- 实时预览
- 历史记录管理

## 6. MLA 9th Edition 格式规范

### Works Cited 格式
- **Book**: Author Last, First. *Title of Book*. Publisher, Year.
- **Website**: Author Last, First. "Title of Page." *Website Name*, Day Month Year, URL. Accessed Day Month Year.
- **Journal**: Author Last, First. "Article Title." *Journal Name*, vol. #, no. #, Year, pp. #–#.
- **Newspaper**: Author Last, First. "Article Title." *Newspaper Name*, Day Month Year, p. #.
- **Film/Video**: "Video Title." *Platform*, Day Month Year, URL.

### In-text Citation 格式
- 1 author: (Lastname page#)
- 2 authors: (Lastname and Lastname page#)
- 3+ authors: (Lastname et al. page#)
- No author: ("ShortTitle" page#)
- Corporate: (OrgName page#)

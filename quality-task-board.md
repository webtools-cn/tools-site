# 工具站质量梳理 — 任务看板

> 2026-08-07 启动。目标：系统性梳理修复 free-toolbase.com 质量问题。
> 由 cron「工具站质量梳理引擎」(every 2h) 持续处理，每2小时汇报。

## 问题底座（首次诊断 2026-08-07）

### Q1 · AdSense搜索广告被驳回（最高优先级）
- 根因：早期批量脚本往 1654 CN + 2081 EN 页硬塞"什么是/使用场景/工具特点"程序化内容段，按10种类型模板套话，被Google判"低价值内容"。
- 关键证据：EN域名页面被塞入大段**中文**（footer导航Contact显示"联系我们"、工具描述整个还是中文）→ Google审核员判=机器翻译/低质。
- 待办：回滚/重写雷同模板段，去程序化味。

### Q2 · 内容质量混乱（最近改动搞乱）
- **101个EN页footer中文残留** → ✅已修复(commit beefc68789)
- **31个EN页导航中文残留**(关于/如何使用→About/How to Use) → ✅已修复(commit 6773000d59)
- **20个EN页TOOL类残留**(工具名/描述/相关推荐链接中文) → ⏳待处理，需逐页翻译
  - power-calculator, potential-energy, force, work, torque, momentum, frequency, cpa, decibel, flow-converter, mass-converter, window-area, airflow, stud-wall, pipe-flow, breaker-size, beam, paint-coverage, number-converter, punycode
  - 特殊: paint-coverage含"TOOL_NAME_CN"占位符泄漏; window-area/airflow等整段广告描述还是中文

### Q3 · 存量问题（待系统梳理）
- 4个title/desc含{{占位符 / 异常: placeholder-image, placeholder-image-generator, dummy-text-generator, placeholder-text-generator
- 18个重复slug(首页重复展示同名卡片)

## 进度
| 批次 | 提交 | 内容 | 状态 |
|:--|:--|:--|:--|
| 英文首页404 | df592475a6 | 3个dict+4缺EN+5中文JSON | ✅ |
| footer中文 | beefc68789 | 101 EN页 | ✅ |
| 导航中文 | 6773000d59 | 31 EN页 | ✅ |
| TOOL类20页 | - | 逐页翻译 | ⏳cron |

## 铁律
- 批量用Python open+write(禁read_file回写)
- 每批改完git commit+push+抽样实测
- 不引入外部JS, 不加aggregateRating
- 记录看板防重复处理

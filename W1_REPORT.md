# W1 报告：四 ID + 广告 + 统计 全站覆盖核查与修复

日期：2026-09-18
分支：`worker/w1`

## 一、结论

**全站 ID 铁律 100% 通过。** 修复前 12 页残留禁用 AdSense ID，修复后零残留。

## 二、修复前后覆盖率对比

| 指标 | 修复前 | 修复后 |
|:-----|:------|:------|
| GA 加载器 `G-QVBQNJ3L5E` | 7551/7551 | 7551/7551 |
| GA config `G-QVBQNJ3L5E` | 7551/7551 | 7551/7551 |
| Adsterra `pl31040516` | 7551/7551 | 7551/7551 |
| Bing `19B854C82A618C376CC972901EF717E5` | 7551/7551 | 7551/7551 |
| 禁用 AdSense `ca-pub-*` | **12 页残留** | **0** |
| 禁用 GA（6 个废弃 ID） | 0 | 0 |
| 禁用 Bing（打错版） | 0 | 0 |
| Google 验证文件 | 存在且正确 | 存在且正确 |

## 三、发现的问题与修复

### 问题 1：12 页残留禁用 AdSense ID `ca-pub-5527959372219623`

- 10 页为 `<meta name="google-adsense-account" content="ca-pub-5527959372219623">`
- 2 页为 `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5527959372219623" ...></script>`

涉及页面：
```
macro-nutrient-calculator, data-transfer-rate-converter, tax-refund-calculator,
bac-calculator, file-checksum-calculator, test-score-calculator
+ 对应 en/ 6 页
```

修复：删除上述 AdSense meta/script 行（仅删 ID 相关行，未动业务逻辑）。

### 问题 2：闸门脚本 `scripts/validate_ids.py` 漏检

- 原 FORBIDDEN 列表只含单个 `ca-pub-5998441792679372`，漏掉其他 `ca-pub-*` → 改为正则 `ca-pub-[0-9]+` 全量拦截
- 原列表 `G-4BZ8MD6QDM` 与任务指定 `G-4BZ4DM6QDM` 不符 → 已更正

## 四、验收标准证据（真实命令输出）

### 1. `python3 scripts/validate_ids.py`
```
PASS ID 铁律通过: 7551 页全部 OK (GA=1 GAconfig=1 Adsterra=1 Bing=1, 零禁用ID)
PASS 根目录: googlefd1a7b2848e1c305.html 存在且内容正确, robots.txt 未屏蔽
```

### 2. `grep -rl "ca-pub-" --include=*.html . | wc -l`
```
0
```

### 3. `grep -c '<loc>' sitemap.xml`
```
7166
```

### 4. `git log --oneline` / `git status --short`
```
b53868a6e8 fix(ids): W1 清除全站残留 AdSense ca-pub ID + 修复闸门脚本漏检
093f5abcdc feat: add mead-calculator (CN+EN) - 蜂蜜酒配方计算器
...
git status --short: （空，干净）
```

## 五、补充核查

- sitemap 7166 条 URL 全部映射到存在的 `index.html`（缺失 0）
- 全站 HTML 无任何禁用 GA / 禁用 Bing ID
- 根目录 `googlefd1a7b2848e1c305.html` 内容 = `google-site-verification: googlefd1a7b2848e1c305.html`，robots.txt 未屏蔽

## 六、备注

仓库内存在历史遗留的临时/审计文件（`.temp/*.json`、`_tmp_check_js_*.js`）内含废弃 GA ID 字符串，但均非站点页面、不在 sitemap、不影响线上，未改动。
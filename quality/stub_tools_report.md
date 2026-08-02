# 空壳工具清单（2026-08-02质检发现）

62个工具的核心函数被替换成了stub（只输出"Generated at..."时间戳），需要逐个重写真实逻辑。

## 发现模式
```js
function generateXxx() {
  var out=document.getElementById('output')||document.getElementById('result')||document.getElementById('result-text');
  if(!out)return;
  out.textContent='Generated at '+new Date().toISOString();
  showToast('Generated!');
}
```

## 完整清单（62个）
./diff-patch-generator/index.html
./css-scroll-driven-animation-generator/index.html
./license-generator/index.html
./jwt-generator/index.html
./json-to-csharp-class/index.html
./color-shade-generator/index.html
./css-scroll-animation-builder/index.html
./color-palette-generator/index.html
./random-string-generator/index.html
./phone-link-generator/index.html
./og-meta-tag-generator/index.html
./domain-name-generator/index.html
./random-quote-generator/index.html
./directory-tree-generator/index.html
./json-mock-generator/index.html
./bip39-mnemonic/index.html
./gif-creator/index.html
./svg-blob-generator/index.html
./json-to-protobuf-schema/index.html
./http-to-curl/index.html
以及更多...

## 修复优先级
- 简单生成器（random-string, random-quote, domain-name等）→ 批量脚本修复
- 复杂工具（jwt, diff-patch, bip39等）→ 单独重写
- EN版本也需要同步检查

## 已修复
✅ uuid-generator/index.html (2026-08-02)
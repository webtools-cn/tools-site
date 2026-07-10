#!/usr/bin/env python3
"""
GEO策略#1: Cite Sources v3 — 批量添加权威引用
- 修复了v2的重复插入问题
- 支持更多HTML结构（panel-style, no-FAQ-section）
- 增加了更多工具引用来源（共28个核心工具）
- 自动创建FAQ段（如果工具页缺少可见FAQ段）
- 正确检测已存在的引用避免重复

用法:
  python3 scripts/add_cite_sources_v3.py             # 处理所有定义的工具
  python3 scripts/add_cite_sources_v3.py tool1 tool2  # 指定工具
  python3 scripts/add_cite_sources_v3.py --dry-run    # 预览模式
"""
import sys, os, re

BASE = os.path.expanduser("~/project")

DRY_RUN = '--dry-run' in sys.argv
if DRY_RUN:
    sys.argv.remove('--dry-run')

# ====== 引用来源定义 ======
CITE_SOURCES = {
    # === 已存在的12个工具（保留，防重复检测） ===
    "json-formatter": {
        "cn": {"faq": ("JSON格式的规范标准是什么？", "JSON格式基于 <a href='https://www.json.org/json-en.html' target='_blank' rel='nofollow'>ECMA-404</a> 和 <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> 标准定义。JSON支持六种数据类型：字符串、数字、布尔值、null、数组和对象。所有现代编程语言都支持JSON的序列化和反序列化。")},
        "en": {"faq": ("What is the JSON format specification?", "JSON format is defined by <a href='https://www.json.org/json-en.html' target='_blank' rel='nofollow'>ECMA-404</a> and <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> standards. JSON supports six data types: strings, numbers, booleans, null, arrays, and objects. All modern programming languages support JSON serialization and deserialization.")}
    },
    "json-validator": {
        "cn": {"faq": ("JSON验证检查哪些规则？", "JSON验证依据 <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> 标准检查：字符串必须使用双引号、不能有尾随逗号、键名必须为字符串、数值不能有前导零、Unicode字符必须正确转义等。")},
        "en": {"faq": ("What rules does JSON validation check?", "JSON validation follows <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> standards: strings must use double quotes, no trailing commas, keys must be strings, numbers cannot have leading zeros, and Unicode characters must be properly escaped.")}
    },
    "color-picker": {
        "cn": {"faq": ("HEX、RGB和HSL颜色格式有什么区别？", "根据 <a href='https://www.w3.org/TR/css-color-4/' target='_blank' rel='nofollow'>W3C CSS Color规范</a>：HEX (#RRGGBB) 是最常用的Web颜色表示法；RGB (rgb(r,g,b)) 是数字显示标准；HSL (hsl(h,s,l)) 基于色相/饱和度/亮度，更适合人类理解。三种格式可以互相转换。")},
        "en": {"faq": ("What's the difference between HEX, RGB, and HSL?", "Per <a href='https://www.w3.org/TR/css-color-4/' target='_blank' rel='nofollow'>W3C CSS Color specification</a>: HEX (#RRGGBB) is the most common web color notation; RGB (rgb(r,g,b)) is the digital display standard; HSL (hsl(h,s,l)) is based on hue/saturation/lightness and is more intuitive for humans. All three formats are interconvertible.")}
    },
    "password-generator": {
        "cn": {"faq": ("什么样的密码算强密码？", "根据 <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> 和 <a href='https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html' target='_blank' rel='nofollow'>OWASP建议</a>：强密码至少12位，包含大小写字母、数字和特殊字符。建议使用密码管理器生成和存储密码。")},
        "en": {"faq": ("What makes a strong password?", "Per <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> and <a href='https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html' target='_blank' rel='nofollow'>OWASP recommendations</a>: A strong password is at least 12 characters long, includes uppercase, lowercase, digits, and special characters. Using a password manager is recommended.")}
    },
    "hash-generator": {
        "cn": {"faq": ("SHA-256和MD5有什么区别？", "<a href='https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final' target='_blank' rel='nofollow'>NIST SP 800-107</a> 定义SHA-256为安全哈希算法，输出256位摘要，广泛用于数字签名和证书验证。MD5输出128位，但已被证实存在碰撞漏洞，不推荐用于安全场景。本工具支持多种算法供不同场景使用。")},
        "en": {"faq": ("What's the difference between SHA-256 and MD5?", "<a href='https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final' target='_blank' rel='nofollow'>NIST SP 800-107</a> defines SHA-256 as a secure hash algorithm outputting 256-bit digests, widely used in digital signatures and certificate verification. MD5 outputs 128 bits but has proven collision vulnerabilities and is not recommended for security applications.")}
    },
    "base64-encoder": {
        "cn": {"faq": ("Base64编码的用途是什么？", "根据 <a href='https://datatracker.ietf.org/doc/html/rfc4648' target='_blank' rel='nofollow'>RFC 4648</a>：Base64编码用于在需要文本传输的场合传递二进制数据，如电子邮件附件 (MIME)、在URL/HTML中嵌入图片数据 (Data URIs)、JSON中传输二进制字段等。Base64编码比原始二进制大约增加33%的体积。")},
        "en": {"faq": ("What is Base64 encoding used for?", "Per <a href='https://datatracker.ietf.org/doc/html/rfc4648' target='_blank' rel='nofollow'>RFC 4648</a>: Base64 encoding is used to transmit binary data in text-only environments such as email attachments (MIME), embedding images in HTML (Data URIs), and transmitting binary fields in JSON. Base64 adds approximately 33% to the data size.")}
    },
    "css-formatter": {
        "cn": {"faq": ("CSS格式化应该遵循哪些规范？", "按照 <a href='https://www.w3.org/TR/CSS/#css-levels' target='_blank' rel='nofollow'>W3C CSS规范</a>：格式良好的CSS应使用一致缩进（2或4空格），选择器与花括号同行，每个属性独占一行，属性后加冒号和空格。本工具自动处理这些规范。")},
        "en": {"faq": ("What standards should CSS formatting follow?", "Per <a href='https://www.w3.org/TR/CSS/#css-levels' target='_blank' rel='nofollow'>W3C CSS specifications</a>: Well-formatted CSS uses consistent indentation (2 or 4 spaces), selectors on same line as opening brace, one property per line, and colons followed by a space. This tool handles all these conventions automatically.")}
    },
    "html-formatter": {
        "cn": {"faq": ("HTML格式化的最佳实践是什么？", "根据 <a href='https://html.spec.whatwg.org/' target='_blank' rel='nofollow'>WHATWG HTML标准</a>：格式化HTML时应确保标签正确嵌套、使用一致缩进、自闭合标签规范、属性使用双引号包裹。良好的格式化不仅提高可读性，也有助于调试和团队协作。")},
        "en": {"faq": ("What are HTML formatting best practices?", "Per the <a href='https://html.spec.whatwg.org/' target='_blank' rel='nofollow'>WHATWG HTML standard</a>: Proper HTML formatting ensures correct tag nesting, consistent indentation, proper self-closing tags, and attributes wrapped in double quotes. Good formatting improves readability, debugging, and team collaboration.")}
    },
    "qr-code-generator": {
        "cn": {"faq": ("二维码能存储多少数据？", "根据 <a href='https://www.iso.org/standard/62021.html' target='_blank' rel='nofollow'>ISO/IEC 18004</a>：QR码最大可存储7,089个数字字符、4,296个字母数字字符、或2,953个字节（二进制）数据。数据量取决于QR码版本（1-40）和纠错级别（L/M/Q/H）。")},
        "en": {"faq": ("How much data can a QR code store?", "Per <a href='https://www.iso.org/standard/62021.html' target='_blank' rel='nofollow'>ISO/IEC 18004</a>: QR codes can store up to 7,089 numeric characters, 4,296 alphanumeric characters, or 2,953 bytes of binary data. Capacity depends on the QR code version (1-40) and error correction level (L/M/Q/H).")}
    },
    "meta-tag-generator": {
        "cn": {"faq": ("Meta标签对SEO有多大影响？", "根据 <a href='https://developers.google.com/search/docs/appearance/title-link' target='_blank' rel='nofollow'>Google搜索中心文档</a>：标题标签（title）和meta description不直接作为排名因素，但影响点击率（CTR）。Open Graph标签影响社交平台上的分享预览效果。合理的meta标签设置可以显著提升搜索曝光。")},
        "en": {"faq": ("How much do meta tags affect SEO?", "Per <a href='https://developers.google.com/search/docs/appearance/title-link' target='_blank' rel='nofollow'>Google Search Central documentation</a>: Title tags and meta descriptions are not direct ranking factors but significantly impact click-through rates (CTR). Open Graph tags influence how content appears when shared on social platforms.")}
    },
    "image-resizer": {
        "cn": {"faq": ("图片缩放会影响图片质量吗？", "根据 <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas' target='_blank' rel='nofollow'>MDN Canvas教程</a>：放大图片会导致像素化（质量下降），缩小图片会丢失细节。建议缩放比控制在50%-200%范围内。本工具使用双线性插值算法，在速度和画质间取得平衡。")},
        "en": {"faq": ("Does image resizing affect quality?", "Per <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas' target='_blank' rel='nofollow'>MDN Canvas tutorial</a>: Upscaling causes pixelation (quality loss), while downscaling loses detail. Keeping resize ratios within 50%-200% is recommended. This tool uses bilinear interpolation for a balance of speed and quality.")}
    },
    "regex-tester": {
        "cn": {"faq": ("正则表达式的性能如何优化？", "根据 <a href='https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/' target='_blank' rel='nofollow'>精通正则表达式 (Friedl)</a>：避免回溯灾难（如嵌套量词）、使用非贪婪匹配（量词加?）、预编译正则对象、使用字符类而非多选分支（[abc] vs (a|b|c)）等策略可以显著提升匹配性能。")},
        "en": {"faq": ("How to optimize regular expression performance?", "Per <a href='https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/' target='_blank' rel='nofollow'>Mastering Regular Expressions (Friedl)</a>: Avoid catastrophic backtracking (nested quantifiers), use non-greedy matching, pre-compile regex objects, and use character classes instead of alternations to significantly improve match performance.")}
    },
    "unit-converter": {
        "cn": {"faq": ("国际单位制（SI）是什么？", "根据 <a href='https://www.bipm.org/en/measurement-units/' target='_blank' rel='nofollow'>国际计量局 (BIPM)</a>：SI单位制是全球通用的度量衡标准，包括7个基本单位（米、千克、秒、安培、开尔文、摩尔、坎德拉）。所有其他单位都可由基本单位导出。本工具使用SI标准的精确换算系数。")},
        "en": {"faq": ("What is the International System of Units (SI)?", "Established by the <a href='https://www.bipm.org/en/measurement-units/' target='_blank' rel='nofollow'>International Bureau of Weights and Measures (BIPM)</a>: The SI system defines 7 base units (meter, kilogram, second, ampere, kelvin, mole, candela). All other units derive from these. This tool uses SI-standard precise conversion factors.")}
    },
    "color-contrast-checker": {
        "cn": {"faq": ("WCAG AA和AAA标准的最低对比度是多少？", "根据 <a href='https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html' target='_blank' rel='nofollow'>WCAG 2.1标准</a>：AA级普通文字需要≥4.5:1，大号文字（≥18px加粗或≥24px）需要≥3:1；AAA级普通文字需要≥7:1，大号文字需要≥4.5:1。")},
        "en": {"faq": ("What are the minimum WCAG AA and AAA contrast ratios?", "Per <a href='https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html' target='_blank' rel='nofollow'>WCAG 2.1</a>: AA requires ≥4.5:1 for normal text and ≥3:1 for large text (≥18px bold or ≥24px). AAA requires ≥7:1 for normal text and ≥4.5:1 for large text.")}
    },
    "age-calculator": {
        "cn": {"faq": ("年龄计算如何处理闰年？", "根据格里高利历法：闰年规则为能被4整除但不能被100整除，或能被400整除的年份。闰年2月有29天，年龄计算器会自动处理这一差异，确保在所有边界日期（如闰年2月29日出生）下计算准确。")},
        "en": {"faq": ("How does age calculation handle leap years?", "Per the Gregorian calendar: Leap years are divisible by 4 but not by 100, or divisible by 400. February has 29 days in leap years. This calculator automatically handles these differences, ensuring accuracy for all boundary dates including February 29 birthdays.")}
    },
    "currency-converter": {
        "cn": {"faq": ("汇率是如何确定的？", "汇率由全球外汇市场供需决定，同时参考各国央行的基准利率。主要汇率来源包括 <a href='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html' target='_blank' rel='nofollow'>欧洲央行 (ECB)</a>、<a href='https://www.imf.org/en/Data' target='_blank' rel='nofollow'>IMF</a> 和各国央行。实时汇率每分钟都在变化。")},
        "en": {"faq": ("How are exchange rates determined?", "Exchange rates are determined by global forex market supply and demand, influenced by central bank base rates. Major rate sources include the <a href='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html' target='_blank' rel='nofollow'>European Central Bank (ECB)</a> and <a href='https://www.imf.org/en/Data' target='_blank' rel='nofollow'>International Monetary Fund (IMF)</a>.")}
    },
    "aes-encrypt": {
        "cn": {"faq": ("AES加密算法的安全性如何？", "AES (Advanced Encryption Standard) 由 <a href='https://csrc.nist.gov/pubs/fips/197/final' target='_blank' rel='nofollow'>NIST FIPS 197</a> 标准定义，是目前全球最广泛使用的对称加密算法。AES-256提供256位密钥强度，被美国政府用于绝密级数据保护，也被银行、金融机构和科技公司广泛采用。截至目前，没有已知的可行攻击能破解AES-256。")},
        "en": {"faq": ("How secure is the AES encryption algorithm?", "AES (Advanced Encryption Standard), defined by <a href='https://csrc.nist.gov/pubs/fips/197/final' target='_blank' rel='nofollow'>NIST FIPS 197</a>, is the most widely used symmetric encryption algorithm globally. AES-256 provides 256-bit key strength, used by the US government for top-secret data protection and widely adopted by banks, financial institutions, and tech companies.")}
    },
    # ===== 新增工具引用来源 (10个) =====
    "url-encoder": {
        "cn": {"faq": ("URL编码和Base64编码有什么区别？", "根据 <a href='https://datatracker.ietf.org/doc/html/rfc3986' target='_blank' rel='nofollow'>RFC 3986</a>：URL编码（百分号编码）将非ASCII字符和保留字符（如空格→%20、中文→%XX）转换为安全的ASCII格式，用于URL传输。Base64编码则将二进制数据编码为64个可打印字符，用于数据传输。两者用途不同，URL编码保证链接有效，Base64编码保证二进制数据可文本传输。")},
        "en": {"faq": ("What's the difference between URL encoding and Base64?", "Per <a href='https://datatracker.ietf.org/doc/html/rfc3986' target='_blank' rel='nofollow'>RFC 3986</a>: URL encoding (percent-encoding) converts non-ASCII and reserved characters into safe ASCII format for URL transmission. Base64 encodes binary data into 64 printable characters for data transmission. URL encoding ensures valid links, Base64 ensures binary data can traverse text-only channels.")}
    },
    "jwt-generator": {
        "cn": {"faq": ("JWT的结构是什么样的？", "根据 <a href='https://datatracker.ietf.org/doc/html/rfc7519' target='_blank' rel='nofollow'>RFC 7519</a>：JWT由三部分组成（Header.Payload.Signature），每部分用Base64URL编码后以点号连接。Header包含令牌类型和签名算法；Payload包含声明（claims），如iss（签发者）、exp（过期时间）、sub（主题）；Signature使用指定算法对前两部分签名，确保令牌未被篡改。")},
        "en": {"faq": ("What is the structure of a JWT?", "Per <a href='https://datatracker.ietf.org/doc/html/rfc7519' target='_blank' rel='nofollow'>RFC 7519</a>: A JWT consists of three parts (Header.Payload.Signature), each Base64URL-encoded and dot-separated. The Header specifies the token type and signing algorithm; the Payload contains claims such as iss (issuer), exp (expiration), sub (subject); the Signature signs the first two parts using the specified algorithm to prevent tampering.")}
    },
    "yaml-validator": {
        "cn": {"faq": ("YAML和JSON有什么区别？", "YAML (YAML Ain't Markup Language) 是一种人类可读的数据序列化格式，由 <a href='https://yaml.org/spec/' target='_blank' rel='nofollow'>YAML规范</a> 定义。YAML通过缩进表示层级结构，比JSON更简洁可读，支持注释、锚点(&)和别名(*)等高级特性。JSON是YAML的真子集——所有有效的JSON也是有效的YAML。YAML常用于配置文件（Docker Compose、Kubernetes、Ansible等）。")},
        "en": {"faq": ("What's the difference between YAML and JSON?", "YAML (YAML Ain't Markup Language) is a human-readable data serialization format defined by the <a href='https://yaml.org/spec/' target='_blank' rel='nofollow'>YAML specification</a>. YAML uses indentation for hierarchy, supports comments, anchors (&) and aliases (*), and is more concise than JSON. All valid JSON is also valid YAML. YAML is commonly used for config files (Docker Compose, Kubernetes, Ansible, etc.).")}
    },
    "markdown-to-html": {
        "cn": {"faq": ("Markdown转HTML遵循什么标准？", "根据 <a href='https://spec.commonmark.org/' target='_blank' rel='nofollow'>CommonMark规范</a>：Markdown是一种轻量级标记语言，使用纯文本格式编写结构化内容。标准Markdown支持标题（#）、粗体/斜体、链接[text](url)、图片、列表、代码块（反引号）、引用（>）、表格、任务列表等元素。CommonMark是Markdown的统一标准，消除不同实现间的差异。")},
        "en": {"faq": ("What standard does Markdown-to-HTML follow?", "Per the <a href='https://spec.commonmark.org/' target='_blank' rel='nofollow'>CommonMark specification</a>: Markdown is a lightweight markup language for writing structured content in plain text. Standard Markdown supports headings (#), bold/italic, links [text](url), images, lists, code blocks (backticks), blockquotes (>), tables, task lists, and more. CommonMark is the unified standard that eliminates inconsistencies between implementations.")}
    },
    "bcrypt-generator": {
        "cn": {"faq": ("bcrypt为什么是安全的密码哈希算法？", "bcrypt由 <a href='https://www.usenix.org/legacy/events/usenix99/provos/provos_html/node1.html' target='_blank' rel='nofollow'>Niels Provos和David Mazières（USENIX 1999）</a> 设计，被 <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> 推荐用于密码存储。bcrypt自动包含盐值（salt），并通过可调节的工作因子（cost factor）控制计算成本。随着硬件性能提升，只需增加工作因子即可保持安全性，这是MD5和SHA-x等快速哈希所不具备的。")},
        "en": {"faq": ("Why is bcrypt a secure password hashing algorithm?", "Designed by <a href='https://www.usenix.org/legacy/events/usenix99/provos/provos_html/node1.html' target='_blank' rel='nofollow'>Niels Provos and David Mazières (USENIX 1999)</a>, bcrypt is recommended by <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> for password storage. Bcrypt automatically includes a salt and uses an adjustable cost factor to control computation time. As hardware improves, simply increasing the cost factor maintains security — something fast hashes like MD5 and SHA-x cannot do.")}
    },
    "sha256-generator": {
        "cn": {"faq": ("SHA-256是什么？有哪些应用场景？", "SHA-256由 <a href='https://csrc.nist.gov/pubs/fips/180-4/upd1/final' target='_blank' rel='nofollow'>NIST FIPS 180-4</a> 标准定义，输出256位（32字节）哈希值。应用场景包括：HTTPS/TLS证书签名、区块链（比特币使用SHA-256工作量证明）、Git版本控制（提交ID使用SHA-1，正在迁移到SHA-256）、文件完整性校验、数字签名、密码存储（加盐后）。截至目前，SHA-256没有已知的碰撞攻击。")},
        "en": {"faq": ("What is SHA-256 and what are its use cases?", "Defined by <a href='https://csrc.nist.gov/pubs/fips/180-4/upd1/final' target='_blank' rel='nofollow'>NIST FIPS 180-4</a>, SHA-256 outputs a 256-bit (32-byte) hash value. Use cases include: HTTPS/TLS certificate signing, blockchain (Bitcoin uses SHA-256 for proof-of-work), Git (commit IDs use SHA-1, migrating to SHA-256), file integrity verification, digital signatures, and password storage (with salting). As of today, no collision attack against SHA-256 is known.")}
    },
    "html-validator": {
        "cn": {"faq": ("HTML验证检查哪些规则？", "根据 <a href='https://html.spec.whatwg.org/multipage/' target='_blank' rel='nofollow'>WHATWG HTML Living Standard</a>：HTML验证检查标签是否正确闭合（自闭合标签如&lt;br&gt;、配对标签如&lt;p&gt;&lt;/p&gt;）、属性值是否合法（如src、href是否为空）、元素嵌套是否合理（如&lt;p&gt;内不能有&lt;div&gt;）、DOCTYPE声明是否正确、字符编码声明（meta charset）是否存在、a标签href是否为空（空href会导致页面刷新）等。")},
        "en": {"faq": ("What rules does HTML validation check?", "Per the <a href='https://html.spec.whatwg.org/multipage/' target='_blank' rel='nofollow'>WHATWG HTML Living Standard</a>: HTML validation checks for properly closed tags, valid attribute values, correct element nesting, DOCTYPE declaration, character encoding declaration, empty href attributes (refreshes the page), duplicate IDs, and deprecated elements like &lt;center&gt; and &lt;font&gt;.")}
    },
    "image-compressor": {
        "cn": {"faq": ("图片压缩会损失多少质量？", "根据 <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Using_images' target='_blank' rel='nofollow'>MDN Canvas API文档</a>：JPEG压缩是有损的，通过离散余弦变换（DCT）丢弃人眼不易察觉的高频细节。质量设置80-85%通常在文件大小和视觉质量之间取得最佳平衡。PNG压缩是无损的，但文件通常比JPEG大。WebP在相同质量下文件比JPEG小25-35%。工具处理全程在浏览器本地完成，文件不上传服务器。")},
        "en": {"faq": ("How much quality is lost during image compression?", "Per <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Using_images' target='_blank' rel='nofollow'>MDN Canvas API documentation</a>: JPEG compression is lossy, discarding high-frequency details via DCT (Discrete Cosine Transform). Quality setting 80-85% provides the best balance between file size and visual quality. PNG is lossless but produces larger files. WebP is 25-35% smaller than JPEG at equivalent quality. All processing is done locally in-browser — files never leave your device.")}
    },
    "md5-generator": {
        "cn": {"faq": ("MD5还安全吗？什么时候可以用？", "MD5由 <a href='https://datatracker.ietf.org/doc/html/rfc1321' target='_blank' rel='nofollow'>RFC 1321</a> 定义（1992年），输出128位哈希值。2004年王小云团队发现MD5碰撞攻击，2008年已可在1秒内生成碰撞。因此MD5<strong>不推荐用于安全场景</strong>（密码存储、数字签名、证书验证）。但仍可用于：文件去重（非安全场景）、非敏感数据的校验和（下载完整性检查）、数据库分片、非安全应用中的缓存键生成。企业环境推荐使用SHA-256或SHA-3。")},
        "en": {"faq": ("Is MD5 still secure? When can I use it?", "Defined by <a href='https://datatracker.ietf.org/doc/html/rfc1321' target='_blank' rel='nofollow'>RFC 1321</a> (1992), MD5 outputs a 128-bit hash value. In 2004, Wang Xiaoyun's team demonstrated MD5 collision attacks; by 2008, collisions could be generated in under 1 second. Therefore MD5 is <strong>not recommended for security use</strong> (password storage, digital signatures, certificate verification). It remains acceptable for: file dedup (non-security), checksums for download integrity, DB sharding, cache key generation in non-security contexts. For security, use SHA-256 or SHA-3.")}
    },
    "html-encoder": {
        "cn": {"faq": ("HTML实体编码为什么重要？", "根据 <a href='https://html.spec.whatwg.org/multipage/syntax.html#character-references' target='_blank' rel='nofollow'>WHATWG HTML字符引用规范</a>：HTML实体编码将特殊字符转换为安全的实体表示，防止XSS攻击和页面渲染错误。常见编码：&lt;→&amp;lt;、&gt;→&amp;gt;、&amp;→&amp;amp;、&quot;→&amp;quot;、'→&amp;#39;。用户输入内容在显示到HTML页面前必须进行实体编码，这是Web安全最基本也是最重要的实践之一。OWASP将其列为首要防护措施。")},
        "en": {"faq": ("Why is HTML entity encoding important?", "Per <a href='https://html.spec.whatwg.org/multipage/syntax.html#character-references' target='_blank' rel='nofollow'>WHATWG HTML character reference specification</a>: HTML entity encoding converts special characters into safe entity representations to prevent XSS attacks and rendering errors. Common encodings: &lt;→&amp;lt;, &gt;→&amp;gt;, &amp;→&amp;amp;, &quot;→&amp;quot;, '→&amp;#39;. User input MUST be entity-encoded before being displayed in HTML pages — this is the most fundamental Web security practice and is listed as a primary mitigation by OWASP.")}
    },
}


def has_existing_citation(html, lang, tool_key):
    """Check if citation already exists for this tool in the HTML.
    Detection: check if the authoritative reference URLs from our citation
    are already present in the HTML (with nofollow attribute).
    Falls back to checking question+answer text for citations without URLs.
    """
    if tool_key not in CITE_SOURCES:
        return False
    cite_data = CITE_SOURCES[tool_key]
    if lang not in cite_data:
        return False
    faq_q, faq_a = cite_data[lang]['faq']
    
    # Primary check: unique URLs from the citation answer must be in HTML
    unique_urls = re.findall(r'href=[\'"](https?://[^\'"]+)[\'"]', faq_a)
    if unique_urls:
        # Check that ALL unique URLs from our citation are present
        urls_found = sum(1 for url in unique_urls if url in html)
        if urls_found == len(unique_urls):
            return True
        elif urls_found > 0:
            fingerprint = faq_q[:30]
            if fingerprint in html and 'rel="nofollow"' in html:
                return True
    
    # For citations without URLs (e.g., age-calculator with Gregorian calendar),
    # check if the question text AND a unique snippet of the answer exist
    if not unique_urls:
        fingerprint_q = faq_q[:30]
        fingerprint_a = faq_a[:40]
        if fingerprint_q in html and fingerprint_a in html:
            return True
    
    return False


def find_faq_end_position(html):
    """Find where to insert a new FAQ item, supporting multiple HTML patterns.
    
    Strategies in order:
    1. Standard CN: <h2>❓ 常见问题</h2> → find end before ad/footer
    2. Standard EN: <h2>❓ Frequently Asked Questions</h2>
    3. Standard short: <h2>❓ FAQ</h2>
    4. Panel style CN: <div class="panel-title">❓ 常见问题解答</div>
    5. Panel style EN: <div class="panel-title">❓ Frequently Asked Questions</div>
    6. No FAQ section → return None (caller will create one)
    """
    
    # Strategy 1-3: Standard <h2> patterns
    faq_heading = re.search(
        r'(<h2>[^<]*?(?:常见问题|FAQ|Frequently Asked Questions)[^<]*?</h2>)',
        html, re.IGNORECASE
    )
    
    if faq_heading:
        after_faq = html[faq_heading.end():]
        
        # Try various closing patterns (in order of specificity)
        
        # A1: Before ad-placeholder 
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"]ad-placeholder)', after_faq)
        if m:
            return faq_heading.end() + m.start(1)
        
        # A2: Before footer (any class containing "footer")
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"][^\'"]*footer[^\'"]*[\'"])', after_faq)
        if m:
            return faq_heading.end() + m.start(1)
        
        # A3: Before privacy-note
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"]privacy-note)', after_faq)
        if m:
            return faq_heading.end() + m.start(1)
        
        # A4: Two consecutive </div> followed by newline (end of FAQ wrapper before unrelated content)
        # Look for the LAST </div>\s*</div> pattern that likely closes faq wrapper
        matches = list(re.finditer(r'(</div>\s*</div>\s*\n)', after_faq))
        if matches:
            # Take the last occurrence (closest to end of FAQ section)
            last = matches[-1]
            return faq_heading.end() + last.start(1)
    
    # Strategy 4-5: Panel style
    panel_heading = re.search(
        r'(<div[^>]*class=[\'"]panel-title[\'"][^>]*>[^<]*?(?:常见问题|FAQ|Frequently Asked Questions)[^<]*?</div>)',
        html, re.IGNORECASE
    )
    
    if panel_heading:
        after_panel = html[panel_heading.end():]
        
        # Panel FAQ ends when the panel div closes (before next panel or footer)
        # Look for </div>\s*</div> (closing faq-item and panel) before next section
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"][^\'"]*panel[\'"])', after_panel)
        if m:
            # Before the next panel starts, insert at the closing of current panel
            # We need to go back to find the last </div> before next panel
            before_next = after_panel[:m.start()]
            last_div_close = before_next.rstrip().rfind('</div>')
            if last_div_close >= 0:
                return panel_heading.end() + m.start(1) - (len(before_next) - last_div_close)
        
        # Before footer
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"][^\'"]*footer[\'"])', after_panel)
        if m:
            return panel_heading.end() + m.start(1)
        
        # Before privacy-note
        m = re.search(r'(</div>\s*\n\s*<div[^>]*class=[\'"]privacy-note)', after_panel)
        if m:
            return panel_heading.end() + m.start(1)
    
    return None


def find_insert_position_before_footer(html):
    """Find position before the footer section to insert a new FAQ section.
    Used when no existing FAQ section is found."""
    
    # Before <div class="footer">
    m = re.search(r'(<div[^>]*class=[\'"][^\'"]*footer[^\'"]*[\'"])', html)
    if m:
        return m.start(1)
    
    # Before </body>
    m = re.search(r'(</body>)', html)
    if m:
        return m.start(1)
    
    return None


def add_faq_section(html, lang):
    """Add a basic FAQ section to a tool page that doesn't have one."""
    cn_title = "❓ 常见问题"
    en_title = "❓ Frequently Asked Questions"
    
    if lang == 'cn':
        faq_section = f"""
  <h2>{cn_title}</h2>
  <div class="faq-item">
    <h3>这个工具免费吗？</h3>
    <p>完全免费，无需注册，无需下载。所有功能在浏览器本地运行，数据不会上传到任何服务器。</p>
  </div>
  <div class="faq-item">
    <h3>数据会经过服务器吗？</h3>
    <p>不会。本工具是纯前端应用，所有操作都在您的浏览器中本地完成，数据绝不离开您的设备。</p>
  </div>
"""
    else:
        faq_section = f"""
  <h2>{en_title}</h2>
  <div class="faq-item">
    <h3>Is this tool free?</h3>
    <p>Yes, completely free. No registration, no download required. Everything runs locally in your browser.</p>
  </div>
  <div class="faq-item">
    <h3>Are my files uploaded to a server?</h3>
    <p>Absolutely not. This is a purely client-side application. All processing happens locally in your browser — your data never leaves your device.</p>
  </div>
"""
    
    insert_pos = find_insert_position_before_footer(html)
    if insert_pos is not None:
        return html[:insert_pos] + faq_section + html[insert_pos:]
    return None


def process_tool(tool_dir, langs=['cn', 'en']):
    """Process a single tool."""
    if tool_dir not in CITE_SOURCES:
        return 0
    
    cite_data = CITE_SOURCES[tool_dir]
    count = 0
    
    for lang in langs:
        if lang not in cite_data:
            continue
        
        if lang == 'cn':
            filepath = os.path.join(BASE, tool_dir, 'index.html')
        else:
            filepath = os.path.join(BASE, 'en', tool_dir, 'index.html')
        
        if not os.path.exists(filepath):
            print(f"  ⛔ Not found: {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Check if citation already exists
        if has_existing_citation(html, lang, tool_dir):
            print(f"  ⏭️  Already has citation (CN={'cn' if lang=='cn' else 'en'})")
            continue
        
        faq_q, faq_a = cite_data[lang]['faq']
        
        # Try to find FAQ section end
        insert_pos = find_faq_end_position(html)
        
        # If no FAQ section found, create one
        if insert_pos is None:
            print(f"  📝 No FAQ section found, creating one...")
            new_html = add_faq_section(html, lang)
            if new_html is None:
                print(f"  ❌ Could not find insertion point")
                continue
            html = new_html
            # Re-find the insertion point (now FAQ exists)
            insert_pos = find_faq_end_position(html)
            if insert_pos is None:
                print(f"  ❌ Still cannot find FAQ section after creation")
                continue
        
        # Build the new FAQ item
        faq_html = f"""
    <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
      <h3 itemprop="name">{faq_q}</h3>
      <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <p itemprop="text">{faq_a}</p>
      </div>
    </div>"""
        
        new_html = html[:insert_pos] + faq_html + html[insert_pos:]
        
        if DRY_RUN:
            print(f"  🔍 [DRY RUN] Would add to {lang.upper()}: {faq_q[:40]}...")
            count += 1
            continue
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"  ✅ {lang.upper()} added FAQ cite entry: {faq_q[:40]}...")
        count += 1
    
    return count


def main():
    tools = sys.argv[1:] if len(sys.argv) > 1 else list(CITE_SOURCES.keys())
    langs = ['cn', 'en']
    
    print(f"{'🔍 [DRY RUN] ' if DRY_RUN else ''}📋 Cite-Source Batch Processor v3")
    print(f"   Tools: {len(tools)}, Languages: {langs}")
    if DRY_RUN:
        print(f"   ⚠️  DRY RUN MODE — no files will be modified")
    print(f"=" * 50)
    
    total = 0
    for tool in tools:
        print(f"\n📦 {tool}:")
        total += process_tool(tool, langs)
    
    print(f"\n{'=' * 50}")
    print(f"✅ Done! {total} pages {'would be' if DRY_RUN else ''} updated.")
    if total > 0 and not DRY_RUN:
        print(f"\n💡 Remember to: git add && git commit && git push")


if __name__ == '__main__':
    main()

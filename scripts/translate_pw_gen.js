#!/usr/bin/env node
// Translate password-generator from CN → EN
const fs = require('fs');

let cn = fs.readFileSync('password-generator/index.html', 'utf8');

// Key content area translations (targeted to specific elements)
const contentReplacements = [
  // Hero area
  ['<p>免费在线密码生成器，支持<strong>常规随机密码</strong>、<strong>易记口令短语</strong>和<strong>PIN码</strong>三种模式。自定义字符集、排除相似字符、批量生成、多格式导出、📱扫描二维码传输到手机。所有密码使用', '<p>Free online password generator with <strong>random passwords</strong>, <strong>memorable passphrases</strong>, and <strong>PIN codes</strong>. Custom charsets, exclude similar chars, batch generation, multi-format export, 📱 QR code sharing to phone. All passwords use'],
  ['真随机生成，纯本地处理，绝不上传。</p>', 'true random generation, processed locally, never uploaded.</p>'],
  ['⚡ 实时生成 · 🔒 零泄露 · 📦 批量导出 · 💬 口令短语 · 📱 二维码分享 · 🧠 记忆评分', '⚡ Real-time · 🔒 Zero-leak · 📦 Batch Export · 💬 Passphrase · 📱 QR Share · 🧠 Memorability'],
  // Mode tabs
  ['🔀 随机密码', '🔀 Random'],
  ['💬 口令短语', '💬 Passphrase'],
  ['📱 PIN码', '📱 PIN'],
  // Settings headers
  ['⚙️ 随机密码选项', '⚙️ Random Password Options'],
  ['💬 口令短语选项', '💬 Passphrase Options'],
  ['📱 PIN码选项', '📱 PIN Options'],
  // Labels
  ['密码长度', 'Password Length'],
  ['生成数量', 'Count'],
  ['包含字符类型', 'Character Types'],
  ['大写字母 (A-Z)', 'Uppercase (A-Z)'],
  ['小写字母 (a-z)', 'Lowercase (a-z)'],
  ['数字 (0-9)', 'Numbers (0-9)'],
  ['特殊符号 (!@#$%^&*)', 'Symbols (!@#$%^&*)'],
  ['排除相似字符 (0 O 1 l I)', 'Exclude Similar (0 O 1 l I)'],
  ['自定义字符集', 'Custom Charset'],
  ['覆盖上方选择', 'overrides above'],
  ['留空使用上方字符类型，如：0123456789abcdef', 'Leave empty to use above, e.g.: 0123456789abcdef'],
  ['单词数量', 'Word Count'],
  ['分隔符', 'Separator'],
  ['- 连字符', '- Hyphen'],
  ['空格', 'Space'],
  ['. 点', '. Dot'],
  ['_ 下划线', '_ Underscore'],
  ['无分隔', 'No Sep'],
  ['首字母大写', 'Capitalize'],
  ['末尾添加数字', 'Add Number'],
  ['PIN长度', 'PIN Length'],
  ['PIN格式', 'PIN Format'],
  ['无格式', 'Plain'],
  ['每4位空格', '4-digit Space'],
  ['每4位连字符', '4-digit Dash'],
  // Buttons
  ['🔄 重新生成', '🔄 Regenerate'],
  ['📋 复制全部', '📋 Copy All'],
  ['💾 导出', '💾 Export'],
  ['导出格式：', 'Export Format: '],
  ['🗑️ 清除历史', '🗑️ Clear History'],
  // Results area
  ['📋 生成的密码', '📋 Generated Passwords'],
  ['自动复制', 'Auto Copy'],
  ['每次生成后自动复制第一个密码到剪贴板', 'Auto-copy first password on generation'],
  ['🕒 复制历史', '🕒 Copy History'],
  ['保存在本地浏览器中（localStorage），最多10条。数据不会上传到服务器。', 'Stored in local browser (localStorage), max 10 entries. Data is never uploaded.'],
  // Tutorial
  ['📖 使用教程', '📖 How to Use'],
  ['模式一：随机密码', 'Mode 1: Random Password'],
  ['模式二：口令短语', 'Mode 2: Passphrase'],
  ['模式三：PIN码', 'Mode 3: PIN Code'],
  ['一键导出', 'One-click Export'],
  ['键盘快捷键', 'Keyboard Shortcuts'],
  ['🔍 密码泄露检测', '🔍 Leak Detection'],
  ['📋 自动复制模式', '📋 Auto Copy Mode'],
  // Use Cases
  ['🎯 应用场景', '🎯 Use Cases'],
  ['💡 安全密码建议', '💡 Password Security Tips'],
  // FAQ
  ['❓ 常见问题', '❓ FAQ'],
  ['🔒 密码强度说明', '🔒 Password Strength Guide'],
  ['弱', 'Weak'],
  ['强', 'Strong'],
  ['非常强', 'Very Strong'],
  ['⚡ 快捷预设', '⚡ Quick Presets'],
  ['⌨️ 快捷键', '⌨️ Shortcuts'],
  ['🆕 新功能', '🆕 New Features'],
  ['🧠 记忆难度评估', '🧠 Memorability Assessment'],
  ['🔗 相关工具推荐', '🔗 Related Tools'],
];

// Apply content replacements
for (const [from, to] of contentReplacements) {
  cn = cn.split(from).join(to);
}

// Global replacements for common terms appearing in many places  
const globalReplacements = [
  ['在线密码生成器 · 纯前端本地生成 · 密码绝不上传服务器', 'Online Password Generator · Pure Frontend · Passwords Never Uploaded'],
  ['问题反馈: dexshuang@google.com', 'Feedback: dexshuang@google.com'],
  ['选择密码长度（4-128位）和字符类型，勾选"排除相似字符"可去掉0/O/1/l/I。滑块拖动时', 'Choose length (4-128) and character types. Check "Exclude Similar" to remove 0/O/1/l/I. Sliders update '],
  ['实时生成', 'in real-time'],
  ['，你也可以使用', '. You can also use '],
  ['（如Hex字符集：0123456789abcdef）来生成满足特定要求的密码。', ' (e.g., Hex: 0123456789abcdef) for specific requirements.'],
  ['由3-10个随机英文单词组成，如', '3-10 random English words, e.g. '],
  ['。可选分隔符（连字符/空格/点/下划线）、首字母大写、末尾添加数字。口令短语比随机字符串更易记忆，同时具有极高安全性。', '. Optional separator, capitalization, trailing number. Passphrases are easier to remember while maintaining high security.'],
  ['纯数字PIN码，4-16位。支持无格式、四位空格分组、四位连字符分组三种格式。适合银行PIN、安全码、验证码等场景。', 'Numeric PIN, 4-16 digits. Plain, 4-digit space, or 4-digit dash formats. Ideal for bank PINs, security codes, verification codes.'],
  ['点击导出按钮，支持TXT、CSV、JSON三种格式下载。适合批量保存或导入密码管理器。', 'Click export for TXT, CSV, JSON download. Great for batch saving or importing to password managers.'],
  ['重新生成', 'Regenerate'],
  ['复制第一个密码', 'Copy First'],
  ['点击第一个密码旁的🔍按钮，即可通过Have I Been Pwned的k-anonymity API检查该密码是否出现在已知数据泄露中。完整密码不会被发送——仅哈希前5位用于查询，绝对安全。', 'Click the 🔍 button next to the first password to check via Have I Been Pwned k-anonymity API. Only the first 5 chars of the SHA-1 hash are sent — completely safe.'],
  ['勾选"自动复制"复选框后，每次生成密码时第一个密码会自动复制到剪贴板，省去手动点击步骤。', 'Check "Auto Copy" to automatically copy the first password on each generation.'],
  // 404 footer
  ['首页', 'Home'],
  ['工具', 'Tools'],
  ['全部工具', 'All Tools'],
  ['联系我们', 'Contact'],
  ['隐私政策', 'Privacy'],
  ['服务条款', 'Terms'],
  ['关于我们', 'About'],
  // Nav back
  ['首页</a>', 'Home</a>'],
  // Toast messages
  ['已复制密码', 'Password copied'],
  ['已复制', 'Copied'],
  ['已复制全部', 'Copied all'],
  ['已复制全部短语', 'Copied all phrases'],
  ['已复制全部PIN码', 'Copied all PINs'],
  ['请先生成密码', 'Generate passwords first'],
  ['请先生成口令短语', 'Generate passphrases first'],
  ['请先生成PIN码', 'Generate PINs first'],
  ['复制失败', 'Copy failed'],
  ['已清除历史记录', 'History cleared'],
  ['🔒 已自动复制密码到剪贴板', '🔒 Auto-copied to clipboard'],
  ['📱 扫描二维码复制到手机', '📱 Scan QR to copy to phone'],
  ['用手机相机扫描二维码，密码将自动复制', 'Scan with phone camera to transfer password'],
  ['关闭', 'Close'],
  ['⚠️ 此密码曾出现在泄露数据库中，建议更换！', '⚠️ This password appeared in known data breaches — change it!'],
  ['✅ 未在已知泄露中发现此密码', '✅ Password not found in known breaches'],
  ['泄露检测失败，请检查网络后重试', 'Leak check failed, check network and retry'],
  ['预估破解时间', 'Est. crack time'],
  ['检测泄露', 'Check Leak'],
  ['生成二维码 - 手机扫描复制', 'Generate QR - scan with phone'],
  ['已复制第一个密码', 'Copied first password'],
  ['重新复制', 'Re-copy'],
  ['复制', 'Copy'],
  ['请选择字符类型并生成密码', 'Select character types and generate'],
  ['请至少选择一种字符类型', 'Please select at least one character type'],
  ['自定义字符集至少需要2个字符', 'Custom charset needs at least 2 characters'],
  ['没有可导出的密码', 'No passwords to export'],
  ['已导出', 'Exported'],
  ['个密码', ' passwords'],
  ['平均熵', 'Avg entropy'],
  ['位', ' bits'],
  ['最弱密码破解', 'Weakest crack'],
  ['个易记', ' easy'],
  ['个中等', ' medium'],
  ['难记', 'Hard'],
  ['易记', 'Easy'],
  ['中等', 'Medium'],
  ['评分', ''],
  ['每个密码附带', 'Each password rated: '],
  ['综合考虑长度、字符类型、模式', 'Considers length, char types, and pattern'],
  ['📱 二维码分享 (手机扫描复制)', '📱 QR Share (phone scan)'],
  ['🧠 记忆难度评分', '🧠 Memorability Score'],
  ['🔍 密码泄露检测 (HIBP)', '🔍 Leak Check (HIBP)'],
  ['⏱ 破解时间估算', '⏱ Crack Time Estimate'],
  ['📋 自动复制模式', '📋 Auto Copy Mode'],
  ['💾 历史跨会话保存', '💾 Cross-session History'],
  ['📚 500+口令词库', '📚 500+ Word Library'],
  ['🔐 Hash生成器', '🔐 Hash Generator'],
  ['📝 Base64编解码', '📝 Base64 Encoder'],
  ['🔐 AES加密', '🔐 AES Encrypt'],
  ['🆔 UUID生成器', '🆔 UUID Generator'],
  ['64位十六进制密钥', '64-char hex key'],
  ['32字符Base32编码', '32-char Base32'],
  ['16位无符号', '16-char no symbols'],
  ['6-16位数字串', '6-16 digit string'],
  ['瞬间', 'Instant'],
  ['秒', 's'],
  ['分钟', 'min'],
  ['小时', 'hrs'],
  ['天', 'days'],
  ['年', 'years'],
  ['世纪', 'centuries'],
  ['万年', '10k years'],
  ['亿年', '100M years'],
  ['未在已知泄露中发现此密码', 'Not found in known breaches'],
  ['此密码曾在数据泄露中出现过！建议更换', 'Found in data breaches! Change recommended'],
  ['请选择字符类型并生成密码', 'Select character types and generate'],
  ['生成', 'Generate'],
];

for (const [from, to] of globalReplacements) {
  cn = cn.split(from).join(to);
}

// Fix lang attribute
cn = cn.replace('lang="zh-CN"', 'lang="en"');
cn = cn.replace(/hreflang="zh"/g, 'hreflang="en"');

// Fix title
cn = cn.replace(/<title>.*?<\/title>/, '<title>Free Password Generator - Strong Random Passwords | Passphrase | PIN | Real-time</title>');

// Fix OG URLs
cn = cn.replace(/content="https:\/\/free-toolbase\.com\/password-generator\/"/g, 'content="https://free-toolbase.com/en/password-generator/"');
cn = cn.replace(/content="https:\/\/free-toolbase\.com\/"/g, 'content="https://free-toolbase.com/en/"');
cn = cn.replace(/canonical" href="https:\/\/free-toolbase\.com\/password-generator\/"/, 'canonical" href="https://free-toolbase.com/en/password-generator/"');

// Fix OG image
cn = cn.replace(/content="https:\/\/free-toolbase\.com\/og-image\.svg"/g, 'content="https://free-toolbase.com/og-image.svg"');
cn = cn.replace(/og-image\.svg/g, '../../og-image.svg');

// Fix language switch
cn = cn.replace(
  '<a href="index.html" class="active">中文</a><a href="../en/password-generator/">EN</a>',
  '<a href="../../password-generator/">中文</a><a href="index.html" class="active">EN</a>'
);

// Fix nav links
cn = cn.replace(/href="\.\.\/index\.html"/g, 'href="../index.html"');
cn = cn.replace(/href="\.\.\/privacy\/"/g, 'href="../../privacy/"');
cn = cn.replace(/href="\.\.\/terms\/"/g, 'href="../../terms/"');
cn = cn.replace(/href="\.\.\/about\/"/g, 'href="../../about/"');

// Fix tool links to en versions
cn = cn.replace(/href="\/hash-generator\//g, 'href="/en/hash-generator/"');
cn = cn.replace(/href="\/base64\//g, 'href="/en/base64/"');
cn = cn.replace(/href="\/aes-encrypt\//g, 'href="/en/aes-encrypt/"');
cn = cn.replace(/href="\/uuid-generator\//g, 'href="/en/uuid-generator/"');

// Fix footer link back to EN homepage  
cn = cn.replace(/href="\.\.\/index\.html"/g, 'href="../index.html"');
cn = cn.replace(/href="\.\.\/\.\.\/index\.html"/g, 'href="../index.html"');
cn = cn.replace(/href="\.\.\/\.\.\/privacy\//g, 'href="../../privacy/"');
cn = cn.replace(/href="\.\.\/\.\.\/terms\//g, 'href="../../terms/"');
cn = cn.replace(/href="\.\.\/\.\.\/about\//g, 'href="../../about/"');

// Fix Schema description
cn = cn.replace(/"description":"免费在线密码生成器[^"]*"/, '"description":"Free online password generator with crypto.getRandomValues true random algorithm. Random passwords, passphrases, PIN codes, custom charset, exclude similar chars, batch export TXT/CSV/JSON, QR code sharing, memorability scoring, leak detection. Pure frontend, zero upload."');
cn = cn.replace(/"name":"在线密码生成器"/g, '"name":"Password Generator"');

// Fix remaining "位" in context like "240 位"
cn = cn.replace(/([\d.]+) 位/g, '$1 bits');
cn = cn.replace(/([\d.]+)位/g, '$1 bits');

// Fix the Japanese text remnants - "个密码" 
cn = cn.replace(/个/g, '');

// Fix footer link to EN in footer (already has ../../en/... from CN copy)
cn = cn.replace(/href="\.\.\/en\/password-generator\/"/g, 'href="../password-generator/"');

fs.writeFileSync('en/password-generator/index.html', cn);
console.log('English version created. Lines:', cn.split('\n').length);

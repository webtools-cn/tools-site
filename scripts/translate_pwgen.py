#!/usr/bin/env python3
"""Translate password-generator CN -> EN"""
import re

with open('password-generator/index.html') as f:
    cn = f.read()

trans_map = {
    '密码生成器 - Free ToolBase': 'Password Generator - Free ToolBase',
    '免费在线密码生成器，使用crypto.getRandomValues生成真正随机的密码。支持随机密码、口令短语、PIN码三种模式。': 'Free online password generator using crypto.getRandomValues for truly random passwords. Random, passphrase & PIN code modes.',
    '密码生成器,随机密码,强密码,口令短语,PIN码,批量导出,在线工具,免费,安全密码': 'password generator, random password, strong password, passphrase, PIN code, batch export, online tool, free, secure password',
    '密码生成器': 'Password Generator',
    '生成真正随机的强密码，纯前端处理，密码不会离开你的浏览器': 'Generate truly random strong passwords. Pure frontend — passwords never leave your browser.',
    '随机密码': 'Random Password',
    '口令短语': 'Passphrase',
    'PIN码': 'PIN Code',
    '密码长度': 'Password Length',
    '生成数量': 'Count',
    '字符类型': 'Character Types',
    '大写字母': 'Uppercase',
    '小写字母': 'Lowercase',
    '数字': 'Numbers',
    '符号': 'Symbols',
    '排除相似字符': 'Exclude Similar',
    '自定义字符集': 'Custom Charset',
    '自定义': 'Custom',
    '快捷预设': 'Quick Presets',
    '重新生成': 'Regenerate',
    '复制全部': 'Copy All',
    '导出': 'Export',
    '生成的密码': 'Generated Passwords',
    '自动复制': 'Auto Copy',
    '清除历史': 'Clear History',
    '复制历史': 'Copy History',
    '保存在本地浏览器中': 'Stored in your browser',
    '数据不会上传到服务器': 'Data never leaves your device',
    '使用教程': 'How to Use',
    '模式一：': 'Mode 1: ',
    '模式二：': 'Mode 2: ',
    '模式三：': 'Mode 3: ',
    '选择密码长度': 'Select password length',
    '和字符类型': 'and character types',
    '勾选"排除相似字符"可去掉0/O/1/l/I': 'Check "Exclude Similar" to remove 0/O/1/l/I',
    '滑块拖动时': 'Drag the slider to ',
    '实时生成': 'generate in real-time',
    '你也可以使用': 'You can also use the',
    '来生成满足特定要求的密码': 'for specific requirements',
    '由3-10个随机英文单词组成': '3-10 random English words',
    '可选分隔符': 'Optional separator',
    '连字符': 'hyphen',
    '空格': 'space',
    '点': 'dot',
    '下划线': 'underscore',
    '无分隔': 'no separator',
    '首字母大写': 'Capitalize',
    '末尾添加数字': 'Add number',
    '口令短语比随机字符串更易记忆，同时具有极高安全性': 'Passphrases are easier to remember than random strings while remaining highly secure.',
    '纯数字PIN码': 'Pure numeric PIN codes',
    '支持无格式、四位空格分组、四位连字符分组三种格式': 'Plain, space-grouped, and dash-grouped formats.',
    '适合银行PIN、安全码、验证码等场景': 'Ideal for bank PINs, security codes, and verification codes.',
    '一键导出': 'One-click Export',
    '点击导出按钮，支持TXT、CSV、JSON三种格式下载。适合批量保存或导入密码管理器。': 'Export to TXT, CSV, or JSON. Great for batch saving or importing to password managers.',
    '键盘快捷键': 'Keyboard Shortcuts',
    '复制第一个密码': 'Copy First',
    '密码泄露检测': 'Leak Detection',
    '点击第一个密码旁的': 'Click ',
    '按钮，即可通过Have I Been Pwned的k-anonymity API检查该密码是否出现在已知数据泄露中。完整密码不会被发送——仅哈希前5位用于查询，绝对安全。': ' to check via Have I Been Pwned k-anonymity API. Only the first 5 chars of the hash are sent — your full password stays private.',
    '自动复制模式': 'Auto Copy Mode',
    '勾选"自动复制"复选框后，每次生成密码时第一个密码会自动复制到剪贴板，省去手动点击步骤。': 'When enabled, the first password is automatically copied to your clipboard on each generation.',
    '应用场景': 'Use Cases',
    '账号注册：': 'Account Registration: ',
    '为各大网站和应用生成高强度唯一密码': 'Generate strong unique passwords for websites and apps',
    '密码管理：': 'Password Management: ',
    '配合密码管理器使用，定期更换重要账号密码': 'Use with password managers, rotate important credentials regularly',
    'WiFi密码：': 'WiFi Passwords: ',
    '生成复杂度高的无线网络密码防止蹭网': 'Generate complex WiFi passwords to prevent piggybacking',
    'API密钥：': 'API Keys: ',
    '为开发项目生成Hex/Bas32格式的安全密钥': 'Generate secure Hex/Base32 keys for development projects',
    '银行PIN：': 'Bank PINs: ',
    '生成安全的4-6位数字PIN码': 'Generate secure 4-6 digit PIN codes',
    '易记密码：': 'Memorable Passwords: ',
    '使用口令短语模式创建既安全又好记的密码': 'Create secure yet memorable passwords with passphrase mode',
    '安全密码建议': 'Password Security Tips',
    '长度优先：': 'Length First: ',
    '密码长度比复杂度更重要。建议使用至少12位以上的密码，16位为佳。': 'Password length matters more than complexity. Use at least 12 characters, 16 is better.',
    '口令短语：': 'Passphrase: ',
    '5个随机单词的口令短语比12位随机字符密码更安全且更容易记忆。熵值可达100+位。': 'A 5-word passphrase is more secure and easier to remember than a 12-char random password. 100+ bits of entropy.',
    '混合字符：': 'Mix Characters: ',
    '包含大写字母、小写字母、数字和特殊符号的组合，大幅增加暴力破解难度。': 'Combine uppercase, lowercase, numbers, and symbols to dramatically increase brute-force resistance.',
    '避免规律：': 'Avoid Patterns: ',
    '不要使用有意义的单词、生日、电话号码等容易被猜测的信息。': 'Don\'t use dictionary words, birthdays, phone numbers, or other guessable information.',
    '唯一性：': 'Uniqueness: ',
    '不同网站使用不同密码，避免一个密码泄露导致所有账号被盗。': 'Use different passwords for each site — one breach shouldn\'t compromise everything.',
    '定期更换：': 'Rotate Regularly: ',
    '重要账号每3-6个月更换一次密码，并启用双因素认证(2FA)。': 'Rotate important passwords every 3-6 months and enable two-factor authentication (2FA).',
    '常见问题': 'FAQ',
    '生成的密码真的安全吗？': 'Are the generated passwords really secure?',
    '是的。本工具使用浏览器的 crypto.getRandomValues() 方法生成真正的随机密码，所有计算在您本地设备的浏览器中完成，生成的密码不会通过网络传输或存储在服务器上。': 'Yes. This tool uses the browser\'s crypto.getRandomValues() for true randomness. All computation happens locally — passwords are never transmitted or stored on any server.',
    '密码泄露检测是什么？': 'What is password leak detection?',
    '点击密码旁的': 'Click ',
    '按钮，工具会将密码的SHA-1哈希前5位发送到Have I Been Pwned的k-anonymity API，检查该密码是否出现在已知的数据泄露中。整个过程您的完整密码不会被传输到任何服务器，只有哈希的前5位被用于查询。': ' to check against Have I Been Pwned via k-anonymity API. Only the first 5 SHA-1 hash characters are sent for querying — your full password never leaves your browser.',
    '破解时间是如何计算的？': 'How is crack time calculated?',
    '基于密码熵值（信息熵）和现代GPU集群每秒1000亿次猜测的能力进行估算。熵值越高，破解所需时间越长。16位含大小写字母+数字+符号的密码，熵值约100位，需要数十亿年才能暴力破解。': 'Based on password entropy and modern GPU clusters capable of 100 billion guesses per second. A 16-char password with all character types has ~100 bits of entropy — billions of years to brute-force.',
    '口令短语 vs 随机密码，哪个更好？': 'Passphrase vs random password — which is better?',
    '两者各有优势。口令短语（如 correct-horse-battery-staple）更易记忆，5个随机单词的熵值可达100+位，安全性极高。随机密码更紧凑但不易记忆。建议对需要手动输入的场景使用口令短语，对密码管理器自动填充的场景使用随机密码。': 'Both have advantages. Passphrases (e.g. correct-horse-battery-staple) are easier to remember — 5 random words = 100+ bits entropy. Random passwords are more compact but harder to remember. Use passphrases for manual entry, random passwords for password managers.',
    '密码强度条代表什么？': 'What does the password strength bar mean?',
    '密码强度基于熵值（信息熵）计算。弱（红色，&lt;30位）→ 中等（橙色，30-50位）→ 强（黄色，50-70位）→ 非常强（绿色，&gt;70位）。16位含所有字符类型的密码通常为"非常强"。': 'Based on entropy. Weak (red, <30 bits) → Medium (orange, 30-50) → Strong (yellow, 50-70) → Very Strong (green, >70). A 16-char password with all types is usually "Very Strong".',
    '排除相似字符有什么作用？': 'Why exclude similar characters?',
    '字符 0/O、1/l/I 在 Sans-serif 字体下难以区分。排除这些字符可避免手动输入时的混淆，提高密码的可读性和输入准确性。': 'Characters 0/O, 1/l/I are hard to distinguish in sans-serif fonts. Excluding them prevents manual entry errors.',
    '导出的密码文件安全吗？': 'Are exported password files secure?',
    '所有导出操作在浏览器本地完成，文件直接下载到您的设备，不会经过任何服务器。建议将导出的文件加密存储或导入密码管理器后删除原文件。': 'All exports happen locally in your browser. Files download directly to your device and never touch any server. We recommend encrypting exported files or importing them into a password manager, then deleting the originals.',
    '二维码分享如何工作？': 'How does QR code sharing work?',
    '点击密码旁的📱按钮，会生成包含该密码的二维码。用手机相机扫描即可获取密码，方便从电脑传输到手机。二维码完全在浏览器本地生成，密码不会上传到任何服务器。': 'Click 📱 to generate a QR code containing the password. Scan with your phone camera to transfer from desktop to mobile. QR codes are generated entirely in your browser — passwords are never uploaded.',
    '记忆难度评分是什么？': 'What is the memorability score?',
    '每个密码旁显示记忆难度：': 'Each password shows a memorability rating: ',
    '易记': 'Easy',
    '中等': 'Medium',
    '难记': 'Hard',
    '（如口令短语、纯数字PIN）': '(passphrases, numeric PINs)',
    '（字母+数字组合）': '(letters+numbers)',
    '（含特殊符号的随机字符串）。帮助您在安全性和可记忆性之间找到平衡。': '(random strings with symbols). Helps you balance security and memorability.',
    '密码强度说明': 'Strength Guide',
    '弱': 'Weak',
    '强': 'Strong',
    '非常强': 'Very Strong',
    '位熵': ' bits entropy',
    '新功能': 'New Features',
    '密码卡片打印': 'Password Card Print',
    '记忆难度': 'Memorability',
    '格式': 'Format',
    '无格式': 'Plain',
    '每4位空格': '4-digit Space',
    '每4位连字符': '4-digit Dash',
    '词库分类': 'Word Category',
    '通用': 'General',
    '科技': 'Tech',
    '自然': 'Nature',
    '食物': 'Food',
    '动物': 'Animals',
    '太空': 'Space',
    '安全评分': 'Security Score',
    '平均熵': 'Avg Entropy',
    '最短破解时间': 'Min Crack Time',
    '字符池大小': 'Char Pool Size',
    '密码已复制到剪贴板': 'Password copied to clipboard',
    '已复制全部': 'All copied',
    '已导出': 'Exported',
    '文件': 'file',
    '在线密码生成器 · 纯前端处理 · 密码不会上传到任何服务器': 'Online Password Generator · Pure Frontend · Passwords Never Uploaded',
    '反馈': 'Feedback',
    '无历史记录': 'No history yet',
    '密码': 'Password',
    '免费密码生成器 - 强随机密码 | 口令短语 | PIN码 | 实时生成': 'Free Password Generator - Strong Random Passwords | Passphrase | PIN | Real-time',
    '个)': ')',
    '最多10条': 'max 10 entries',
    '🔍': '🔍',
}

# Apply translations
en = cn
for cn_text, en_text in trans_map.items():
    en = en.replace(cn_text, en_text)

# Fix HTML lang
en = en.replace('<html lang="zh-CN">', '<html lang="en">')

# Fix canonical
en = en.replace(
    'href="https://free-toolbase.com/password-generator/"',
    'href="https://free-toolbase.com/en/password-generator/"'
)

# Fix hreflang
en = en.replace('hreflang="zh-CN"', 'hreflang="en"')

# Fix og:locale
en = en.replace('zh_CN', 'en_US')

# Fix alternates
en = re.sub(
    r'<link rel="alternate" hreflang="zh-CN" href="[^"]*"',
    '<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/password-generator/"',
    en
)

cn_pattern = re.compile(r'[\u4e00-\u9fff]')
remaining_cn = len(cn_pattern.findall(en))
orig_cn = len(cn_pattern.findall(cn))
print(f'Original CN chars: {orig_cn}')
print(f'Remaining CN chars: {remaining_cn}')

# Show remaining CN if any
if remaining_cn > 0:
    for i, line in enumerate(en.split('\n'), 1):
        matches = cn_pattern.findall(line)
        if matches:
            # Skip script/style blocks
            print(f'  Line {i}: {line.strip()[:100]}')

with open('en/password-generator/index.html', 'w') as f:
    f.write(en)
print('Written en/password-generator/index.html')
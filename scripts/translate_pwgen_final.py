#!/usr/bin/env python3
"""Translate password-generator CN -> EN - Final phase"""
import re

with open('en/password-generator/index.html') as f:
    en = f.read()

# Fix description meta (L10)
old_desc = '<meta name="description" content="免费在线随机Password Generator，一键生成高Strong度的安全Password。支持CustomPassword Length(8-128位)、大Lowercase、Numbers和特殊Symbols组合，实时评估PasswordStrong度。纯前端，无注册，免费使用。"'
new_desc = '<meta name="description" content="Free online password generator with crypto.getRandomValues for truly random passwords. Supports custom length (8-128 chars), uppercase, lowercase, numbers, symbols. Real-time strength assessment. Pure frontend, no signup, free."'
en = en.replace(old_desc, new_desc)

# Fix keywords meta (L11)
old_kw = '<meta name="keywords" content="Password Generator,Random Password,StrongPassword,Passphrase,passphrase,PIN Code,批量Export,在线Tools,免费,安全Password">'
new_kw = '<meta name="keywords" content="password generator,random password,strong password,passphrase,PIN code,batch export,online tool,free,secure password">'
en = en.replace(old_kw, new_kw)

# Fix OG description (L15) 
old_og = '<meta property="og:description" content="免费Online Password Generator，使用crypto.getRandomValues真随机算法生成高Strong度安全Password。支持Random Password、Passphrase、PIN Code三种Mode，Custom Charset、Exclude Similar、批量Export。纯前端，零上传。"'
new_og = '<meta property="og:description" content="Free online password generator using crypto.getRandomValues for truly random passwords. Random, passphrase & PIN code modes, custom charset, exclude similar, batch export. Pure frontend, zero upload."'
en = en.replace(old_og, new_og)

# Fix FAQPage schema
old_faq = '"name":"Generated Passwords安全吗？","acceptedAnswer":{"@type":"Answer","text":"是的。本Tools使用浏览器的 crypto.getRandomValues() 方法生成真正的随机Password，所有Calculate在您本地设备的浏览器中完成，Generated Passwords不会通过网络传输或存储在服务器上。"}'
new_faq = '"name":"Are generated passwords secure?","acceptedAnswer":{"@type":"Answer","text":"Yes. This tool uses the browser\'s crypto.getRandomValues() for true randomness. All computation happens locally — passwords are never transmitted or stored on any server."}'
en = en.replace(old_faq, new_faq)

old_faq2 = '"name":"Password泄露检测是什么？","acceptedAnswer":{"@type":"Answer","text":"Click next to the password🔍按钮，Tools会将Password的SHA-1哈希前5位发送到Have I Been Pwned的k-anonymity API，检查该Password是否出现在已知的数据泄露中。整个过程您的完整Password不会被传输到任何服务器，只有哈希的前5位被用于查询。"}'
new_faq2 = '"name":"What is password leak detection?","acceptedAnswer":{"@type":"Answer","text":"Click 🔍 next to any password to check it against Have I Been Pwned via k-anonymity API. Only the first 5 characters of the SHA-1 hash are sent — your full password never leaves your browser."}'
en = en.replace(old_faq2, new_faq2)

old_faq3 = '"name":"Time是such as何Calculate的？","acceptedAnswer":{"@type":"Answer","text":"Based on password entropy（Information entropy）and modern GPU cluster per second"}'
new_faq3 = '"name":"How is crack time calculated?","acceptedAnswer":{"@type":"Answer","text":"Based on password entropy and modern GPU clusters at 100 billion guesses per second"}'
en = en.replace(old_faq3, new_faq3)

old_faq4 = '"name":"Passphrase vs Random Password，哪更好？","acceptedAnswer":{"@type":"Answer","text":"Both have advantages。Passphrase（such as correct-horse-battery-staple）更Easy忆，5Entropy of random words can reach100+ bits，Extremely high security。Random passwords are more compact butEasy忆。For manual entry scenarios, use passphrases，For password manager auto-fill, use random passwords。"}'
new_faq4 = '"name":"Passphrase vs random password — which is better?","acceptedAnswer":{"@type":"Answer","text":"Both have advantages. Passphrases (e.g., correct-horse-battery-staple) are easier to remember — 5 random words = 100+ bits entropy. Random passwords are more compact but harder to remember. Use passphrases for manual entry, random passwords for password managers."}'
en = en.replace(old_faq4, new_faq4)

old_faq5 = '"name":"PasswordStrong度条代表什么？","acceptedAnswer":{"@type":"Answer","text":"PasswordStrong度基于熵值（Information entropy）Calculate。Weak（红色，&lt;30位）→ Medium（橙色，30-50位）→ Strong（黄色，50-70位）→ VeryStrong（绿色，&gt;70位）。16 chars含所有Types的Password通常为\\"VeryStrong\\"。"}'
new_faq5 = '"name":"What does the strength bar mean?","acceptedAnswer":{"@type":"Answer","text":"Based on entropy. Weak (red, <30 bits) → Medium (orange, 30-50) → Strong (yellow, 50-70) → Very Strong (green, >70). A 16-char password with all types is usually \\"Very Strong\\"."}'
en = en.replace(old_faq5, new_faq5)

# Fix HowTo schema
old_howto = '"description":"免费Online Password Generator。通过3种Mode（Random Password、Passphrase、PIN Code）一键生成高Strong度安全Password。"'
new_howto = '"description":"Free online password generator. Generate strong secure passwords in 3 modes: Random Password, Passphrase, or PIN Code."'
en = en.replace(old_howto, new_howto)

old_howto_step1 = '"text":"SelectRandom Password、Passphrase 或 PIN Code Mode"'
new_howto_step1 = '"text":"Select Random Password, Passphrase, or PIN Code mode"'
en = en.replace(old_howto_step1, new_howto_step1)

old_howto_step2 = '"text":"设置Password Length、Character Types、自定义Charset或Word Count"'
new_howto_step2 = '"text":"Set password length, character types, custom charset, or word count"'
en = en.replace(old_howto_step2, new_howto_step2)

old_howto_step3 = '"text":"一键Copy单个Password，或批量Export所有Generated Password"'
new_howto_step3 = '"text":"One-click copy individual passwords or batch export all generated passwords"'
en = en.replace(old_howto_step3, new_howto_step3)

# Fix BreadcrumbList
old_breadcrumb = '"name":"Password Generator","item":"https://free-toolbase.com/password-generator/"'
new_breadcrumb = '"name":"Password Generator","item":"https://free-toolbase.com/en/password-generator/"'
en = en.replace(old_breadcrumb, new_breadcrumb)

# Hero area
old_hero = 'Free online password generator, supports <strong>Random Password</strong>、<strong>Passphrase</strong>和<strong>PIN Code</strong>三种Mode，丰富Custom Settings，纯前端处理不上传。'
new_hero = 'Free online password generator — supports <strong>Random Password</strong>, <strong>Passphrase</strong>, and <strong>PIN Code</strong> modes. Rich customization, pure frontend — no uploads.'
en = en.replace(old_hero, new_hero)

# Usage section
old_usage = '3-10 random English words, e.g.  <code>correct-horse-battery-staple</code>。Optional separator（hyphen/space/dot/underscore）、Capitalize、Add Number at End，'
new_usage = '3-10 random English words, e.g. <code>correct-horse-battery-staple</code>. Optional separator (hyphen/space/dot/underscore), capitalize first letter, add number at end, '
en = en.replace(old_usage, new_usage)

# Remaining bits
fixes_final = [
    # FAQ text fragments
    ('两者各有优势。Passphrase', 'Passphrases'),
    ('（如 correct-horse-battery-staple）更Easy忆，5个随机单词的Entropy can reach 100+ bits.，安全性极高。Random Password更紧凑但不Easy忆。建议对需要手动输入的场景使用Passphrase，对Password管理器Auto Fill的场景使用Random Password。',
     ' (e.g., correct-horse-battery-staple) are easier to remember — 5 random words = 100+ bits. Random passwords are more compact but harder to remember. Use passphrases for manual entry, random passwords for password managers.'),
    ('Each password shows a memorability rating: <span style="color:#22c55e">Easy</span>(e.g., passphrases, numeric PINs)、<span style="color:#eab308">Medium</span>（字母+Numbers组合）、<span style="color:#ef4444">Hard</span>（含特殊Symbols的随机字符串）。Help您在安全性和可记忆性之间找到平衡。',
     'Each password shows a memorability rating: <span style="color:#22c55e">Easy</span> (passphrases, numeric PINs), <span style="color:#eab308">Medium</span> (letters+numbers), <span style="color:#ef4444">Hard</span> (random strings with symbols). Helps you balance security and memorability.'),
    ('Each password rated  <span style="color:#22c55e">Easy</span>/<span style="color:#eab308">Medium</span>/<span style="color:#ef4444">Hard</span>评分<br>',
     'Each password rated <span style="color:#22c55e">Easy</span> / <span style="color:#eab308">Medium</span> / <span style="color:#ef4444">Hard</span><br>'),
    ('综合考虑长度、Character Types、模式',
     'Considers length, character types, and pattern'),
    ('配置链接Copied！粘贴分享给他人', 'Config link copied! Share with others'),
    
    # Policy descriptions
    ('Suitable for most 网站的16位StrongPassword',
     'Suitable for most websites — 16-char strong password'),
    ('"Microsoft要求8-256 chars，至少3种类型"',
     '"Microsoft requires 8-256 chars, at least 3 types"'),
    ('"Google requires at least 8 chars, ，建议使用混合 chars，至少包含2种类型"',
     '"Google requires at least 8 chars, recommends mixed types, at least 2"'),
    ('"AWS recommends 20+ chars with all char types，包含所有字符类型"',
     '"AWS recommends 20+ chars with all character types"'),
    ('"Apple requires at least 8 chars, s，含大小写和Numbers，不支持特殊字符"',
     '"Apple requires at least 8 chars, uppercase+lowercase+numbers, no special chars"'),
    ('"Banking-grade security: 24 chars, Exclude Similar，所有字符类型"',
     '"Banking-grade security: 24 chars, exclude similar, all character types"'),
]

for old, new in fixes_final:
    en = en.replace(old, new)

# Count remaining Chinese characters
cn_pattern = re.compile(r'[\u4e00-\u9fff]')
remaining = len(cn_pattern.findall(en))

if remaining > 0:
    print(f'Remaining CN chars: {remaining}')
    for i, line in enumerate(en.split('\n'), 1):
        matches = cn_pattern.findall(line)
        if matches:
            print(f'  L{i}: {line.strip()[:150]}')
else:
    print('ALL CHINESE CHARACTERS REMOVED! ✅')

# Ensure lang attribute is en
en = re.sub(r'<html lang="[^"]*"', '<html lang="en"', en)

# Fix canonical URL
en = re.sub(
    r'<link rel="canonical" href="https://free-toolbase\.com/password-generator/"',
    '<link rel="canonical" href="https://free-toolbase.com/en/password-generator/"',
    en
)

# Fix alternate hreflang
en = en.replace(
    '<link rel="alternate" hreflang="zh-CN" href="https://free-toolbase.com/password-generator/">',
    '<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/password-generator/">'
)

# Fix og:locale
en = en.replace('og:locale" content="zh_CN"', 'og:locale" content="en_US"')

# Fix og:url
en = en.replace(
    '<meta property="og:url" content="https://free-toolbase.com/password-generator/">',
    '<meta property="og:url" content="https://free-toolbase.com/en/password-generator/">'
)

# Fix og:image path
en = en.replace('content="../../og-image.svg"', 'content="../og-image.svg"')

with open('en/password-generator/index.html', 'w') as f:
    f.write(en)
print('\nFile written: en/password-generator/index.html')
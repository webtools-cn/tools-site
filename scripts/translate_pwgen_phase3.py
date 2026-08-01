#!/usr/bin/env python3
"""Translate password-generator CN -> EN - Phase 3: catch all remaining"""
import re

with open('en/password-generator/index.html') as f:
    en = f.read()

# Targeted replacements for remaining Chinese
fixes = [
    # Meta/OG
    ('支持CustomPassword Length(8-128位)、大Lowercase/Numbers/Symbols、Exclude Similar、Custom Charset、批量Export TXT/CSV/JSON、QR Code分享、记忆难度评估、泄露检测。纯前端，零上传。"',
     'Supports custom length (8-128 chars), uppercase/lowercase/numbers/symbols, exclude similar, custom charset, batch export TXT/CSV/JSON, QR code sharing, memorability scoring, leak detection. Pure frontend, zero upload."'),
    ('批量Export,Password安全,Password检测,Passphrase Generator,Password工具,免费工具,在线安全工具',
     'batch export,password security,password checker,passphrase generator,password tool,free tool,online security tool'),
    ('免费在线Password Generator，使用crypto.getRandomValues真随机算法生成高Strong度安全Password。支持Random Password、Passphrase、PIN Code三种Mode，Custom Charset、Exclude Similar、批量Export TXT/CSV/JSON、二维码分享、记忆难度评分、泄露检测。纯前端，零上传。',
     'Free online password generator using crypto.getRandomValues for true random passwords. Random, passphrase & PIN code modes, custom charset, exclude similar, batch export TXT/CSV/JSON, QR code sharing, memorability scoring, leak detection. Pure frontend, zero upload.'),
    
    # Header / nav
    ('在线Password Generator', 'Online Password Generator'),
    ('中文', 'EN'),
    ('全部Tools', 'All Tools'),
    
    # Hero
    ('支持<strong>Random Password</strong>、<strong>Passphrase</strong>、<strong>PIN Code</strong>三种Mode，Custom Charset丰富，纯前端不上传。',
     'Supports <strong>Random Password</strong>, <strong>Passphrase</strong>, and <strong>PIN Code</strong> modes. Rich custom charset, pure frontend — no uploads.'),
    
    # Labels
    ('末尾添加Numbers', 'Add Number at End'),
    ('(4-128 chars)和Character Types，勾选"Exclude Similar"可去掉0/O/1/l/I。Drag the slider to',
     '(4-128 chars) and character types. Check "Exclude Similar" to remove 0/O/1/l/I. Drag the slider to'),
    ('3-10 random English words，如',
     '3-10 random English words, e.g. '),
    ('Optional separator（hyphen/space/dot/underscore）、Capitalize、Add Number。Passphrase比Random Password更Easy忆，同时具有极高安全性。',
     'Optional separator (hyphen/space/dot/underscore), capitalize, add number. Passphrases are easier to remember than random passwords while remaining highly secure.'),
    ('Numbers OnlyPIN Code，4-16 digits。支持Plain、四位space分组、四位hyphen分组三种Format。Ideal for bank PINs, security codes, and verification codes.',
     'Numbers Only PIN Code, 4-16 digits. Supports plain, 4-digit space grouping, and 4-digit dash grouping. Ideal for bank PINs, security codes, and verification codes.'),
    ('支持TXT, CSV, or JSON formats。适合批量保存或导入Password管理器。',
     'Supports TXT, CSV, or JSON formats. Great for batch saving or importing to password managers.'),
    
    # FAQ
    ('是的。本Tools使用浏览器的 crypto.getRandomValues() 方法生成真正的Random Password，所有计算在您本地设备的浏览器中完成，Generated Passwords不会通过网络传输或存储在服务器上。',
     'Yes. This tool uses the browser\'s crypto.getRandomValues() for true randomness. All computation happens locally — passwords are never transmitted or stored on any server.'),
    ('Passphrase（如 correct-horse-battery-staple）更Easy忆，5个随机单词的Entropy can reach 100+ bits.，安全性极高。Random Password更紧凑但不易记忆。建议对需要手动输入的场景使用Passphrase，对Password管理器Auto Fill的场景使用Random Password。',
     'Passphrases (e.g., correct-horse-battery-staple) are easier to remember — 5 random words = 100+ bits. Random passwords are more compact but harder to remember. Use passphrases for manual entry, random passwords for password managers.'),
    ('Click 📱按钮，会生成包含该Password的二维码。用手机相机扫描即可获取Password，方便从电脑传输到手机。二维码完全在浏览器本地生成，Password不会上传到任何服务器。',
     'Click 📱 to generate a QR code containing the password. Scan with your phone camera to transfer from desktop to mobile. QR codes are generated entirely in your browser — passwords are never uploaded.'),
    ('（如Passphrase、Numbers OnlyPIN）',
     '(e.g., passphrases, numeric PINs)'),
    
    # Sidebar
    ('Each password rated',
     'Each password rated '),
    ('用手机相机扫描二维码，Password将Auto Copy',
     'Scan QR code with your phone camera — password will be copied automatically'),
    
    # JS strings
    ('万 years', ' millennia'),
    ('亿 years', ' billion years'),
    ('📊 Avg Entropy: : ', '📊 Avg Entropy: '),
    (' bits</span><span>🔓 Weakest crack: : ', ' bits</span><span>🔓 Weakest crack: '),
    ('Please select character types并生成Password', 'Select character types and generate passwords'),
    ('💡 Passphrase比随机 chars更容Easy住且同样安全', '💡 Passphrases are easier to remember and just as secure'),
    ('💡 Password length matters more than complexity.，至少12位', '💡 Password length matters more than complexity — at least 12 chars'),
    ('已CopyPassword', 'Password copied'),
    ('Copy失败', 'Copy failed'),
    ('重新Copy', 'Copy Again'),
    ('已Copy', 'Copied'),
    ('配置链接已Copy！粘贴分享给他人', 'Config link copied! Share with others'),
    ('URL已更新，Copy浏览器地址栏即可分享', 'URL updated — copy the address bar to share'),
    ('至少需要2个 chars', 'needs at least 2 characters'),
    (' chars集大小: ', 'Charset size: '),
    (' 个唯一 chars', ' unique characters'),
    ('已Copy All ', 'Copied all '),
    
    # Policy rules
    ('desc:"适合大多数',
     'desc:"Suitable for most '),
    ('Microsoft要求最少8 chars',
     'Microsoft requires at least 8 chars, '),
    ('Google要求最少8 chars',
     'Google requires at least 8 chars, '),
    ('AWS建议使用20位以上，包含所有Ch',
     'AWS recommends 20+ chars with all ch'),
    ('Apple要求至少8 char',
     'Apple requires at least 8 chars, '),
    ('金融级安全：24位，',
     'Banking-grade security: 24 chars, '),
]

for old, new in fixes:
    if old in en:
        en = en.replace(old, new)

cn_pattern = re.compile(r'[\u4e00-\u9fff]')
remaining = len(cn_pattern.findall(en))

if remaining > 0:
    for i, line in enumerate(en.split('\n'), 1):
        matches = cn_pattern.findall(line)
        if matches:
            print(f'  L{i}: {line.strip()[:150]}')

print(f'\nRemaining CN chars: {remaining}')

with open('en/password-generator/index.html', 'w') as f:
    f.write(en)
print('Written en/password-generator/index.html')
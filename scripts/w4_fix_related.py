#!/usr/bin/env python3
"""W4 P3: 修复 top100 页相关推荐占位，替换为真实相关工具"""
import json, os, re, sys

BASE = '/home/chison/wt/w4'
with open('/tmp/tool_names.json') as f:
    NAMES = json.load(f)

def name(slug):
    return NAMES.get(slug, slug)

def link(slug):
    n = name(slug)
    return f'<a href="/{slug}/" style="color:#06b6d4;text-decoration:none;font-size:14px;display:block;padding:6px 0">{n}</a>'

# 页面 -> 相关工具列表（真实相关）
FIX = {
    # ==== 天气族 ====
    'heat-index-calculator': ['wind-chill-calculator', 'uv-index-calculator', 'wet-bulb-calculator', 'temperature-converter', 'dew-point-calculator'],
    'wind-chill-calculator': ['heat-index-calculator', 'uv-index-calculator', 'wet-bulb-calculator', 'temperature-converter', 'dew-point-calculator'],
    'uv-index-calculator': ['heat-index-calculator', 'wind-chill-calculator', 'wet-bulb-calculator', 'temperature-converter', 'dew-point-calculator'],
    # ==== 工时/时间族 ====
    'timesheet-calculator': ['work-hours-calculator', 'time-card-calculator', 'time-duration-calc', 'overtime-calculator', 'billable-hours-calculator'],
    'time-duration-calc': ['date-difference-calculator', 'time-zone-converter', 'work-hours-calculator', 'date-duration-calculator', 'age-calculator'],
    # ==== 数学族 ====
    'graphing-calculator': ['scientific-calculator', 'trig-calculator', 'matrix-calculator', 'quadratic-formula-calculator', 'percentage-calculator'],
    'trig-calculator': ['scientific-calculator', 'graphing-calculator', 'matrix-calculator', 'quadratic-formula-calculator', 'percentage-calculator'],
    'binary-calculator': ['hex-calculator', 'radix-converter', 'number-base-converter', 'gray-code-converter', 'scientific-notation-converter'],
    'hex-calculator': ['binary-calculator', 'radix-converter', 'number-base-converter', 'gray-code-converter', 'scientific-notation-converter'],
    # ==== 网络/IP 族 ====
    'cidr-calculator': ['ip-subnet-calculator', 'subnet-calculator', 'ip-calculator', 'ip-range-calculator', 'ipv4-ipv6-converter'],
    'subnet-divider': ['cidr-calculator', 'ip-subnet-calculator', 'subnet-calculator', 'ip-calculator', 'ip-range-calculator'],
    'whats-my-ip': ['ip-lookup', 'ip-geolocation', 'mac-address-lookup', 'whois-domain-lookup', 'subnet-calculator'],
    'mac-address-lookup': ['whats-my-ip', 'ip-lookup', 'ip-geolocation', 'whois-domain-lookup', 'subnet-calculator'],
    'ip-lookup': ['whats-my-ip', 'ip-geolocation', 'mac-address-lookup', 'whois-domain-lookup', 'subnet-calculator'],
    # ==== 音频族 ====
    'bpm-tapper': ['metronome', 'metronome-online', 'bpm-delay-time-calculator', 'tempo-changer', 'online-tone-generator'],
    'midi-player': ['drum-machine', 'online-tone-generator', 'sound-frequency-generator', 'audio-speed-changer', 'tempo-changer'],
    'drum-machine': ['midi-player', 'online-tone-generator', 'sound-frequency-generator', 'bpm-tapper', 'metronome'],
    'full-screen-clock': ['online-clock', 'world-clock', 'countdown-clock', 'online-stopwatch', 'online-timer'],
    'metronome-online': ['metronome', 'bpm-tapper', 'bpm-delay-time-calculator', 'tempo-changer', 'online-tone-generator'],
    # ==== 哈希/校验族 ====
    'checksum-calculator': ['file-checksum-calculator', 'file-hash-checker', 'hash-file-checker', 'md5-generator', 'sha256-generator'],
    'file-hash-checker': ['checksum-calculator', 'file-checksum-calculator', 'hash-file-checker', 'md5-generator', 'sha256-generator'],
    'file-checksum-calculator': ['checksum-calculator', 'file-hash-checker', 'hash-file-checker', 'md5-generator', 'sha256-generator'],
    # ==== 税务族 ====
    'tax-refund-calculator': ['tax-calculator', 'tax-bracket-calculator', 'income-tax-calculator', 'take-home-pay', 'payroll-tax-calculator'],
    'tax-bracket-calculator': ['tax-calculator', 'tax-refund-calculator', 'income-tax-calculator', 'take-home-pay', 'payroll-tax-calculator'],
    'kpi-calculator': ['roi-calculator', 'investment-calculator', 'compound-interest-calculator', 'profit-margin-calculator', 'revenue-calculator'],
    'paycheck-calculator': ['tax-calculator', 'take-home-pay', 'payroll-tax-calculator', 'income-tax-calculator', 'tax-refund-calculator'],
    'vat-calculator': ['sales-tax-calculator', 'tax-calculator', 'tax-bracket-calculator', 'vat-number-validator', 'income-tax-calculator'],
    # ==== 文本族 ====
    'rhyme-finder': ['syllable-counter', 'anagram-solver', 'word-frequency', 'palindrome-checker', 'word-counter'],
    'alphabetical-sorter': ['text-sorter', 'text-dedup', 'text-reverser', 'word-frequency', 'line-sorter'],
    # ==== Unicode 族 ====
    'character-unicode-finder': ['unicode-decoder', 'unicode-converter', 'unicode-analyzer', 'unicode-explorer', 'unicode-finder'],
    'unicode-decoder': ['character-unicode-finder', 'unicode-converter', 'unicode-analyzer', 'unicode-explorer', 'unicode-finder'],
    'invisible-character': ['character-unicode-finder', 'unicode-converter', 'unicode-analyzer', 'unicode-explorer', 'unicode-finder'],
    # ==== 正则族 ====
    'regex-101': ['regex-tester', 'regex-generator', 'regex-visualizer', 'regex-explainer', 'regex-cheat-sheet'],
    'regex-crossword': ['regex-101', 'regex-tester', 'regex-generator', 'regex-visualizer', 'regex-cheat-sheet'],
    # ==== 图片族 ====
    'image-histogram': ['color-palette-extractor', 'image-color-picker', 'color-picker', 'color-converter', 'image-tinter'],
    'image-tinter': ['image-histogram', 'color-palette-extractor', 'image-color-picker', 'color-picker', 'image-filter'],
    # ==== 视力族 ====
    'vision-test': ['eye-test', 'visual-acuity-calculator', 'color-converter', 'color-picker', 'monitor-test'],
    'eye-test': ['vision-test', 'visual-acuity-calculator', 'color-converter', 'color-picker', 'monitor-test'],
    # ==== 日记/心情族 ====
    'daily-journal': ['mood-tracker', 'gratitude-journal', 'habit-tracker', 'daily-affirmation-generator', 'todo-list'],
    'mood-tracker': ['daily-journal', 'gratitude-journal', 'habit-tracker', 'daily-affirmation-generator', 'todo-list'],
    # ==== 编码族 ====
    'vin-decoder': ['vin-validator', 'unit-converter', 'base64-encode-decode', 'hex-calculator', 'binary-calculator'],
    'currency-converter': ['unit-converter', 'vat-calculator', 'sales-tax-calculator', 'percentage-calculator', 'tip-calculator'],
    'gray-code-converter': ['binary-calculator', 'hex-calculator', 'radix-converter', 'number-base-converter', 'scientific-notation-converter'],
    'scientific-notation-converter': ['number-base-converter', 'radix-converter', 'binary-calculator', 'hex-calculator', 'gray-code-converter'],
    'cbor-encoder': ['base64-encode-decode', 'json-formatter', 'protobuf-to-json', 'msgpack-viewer', 'hex-calculator'],
    # ==== 生成器族 ====
    'cursive-text-generator': ['fancy-text-generator', 'handwriting-generator', 'text-to-handwriting', 'small-text-generator', 'zalgo-text-generator'],
    'emoji-combiner': ['emoji-kitchen', 'fancy-text-generator', 'small-text-generator', 'ascii-art-generator', 'zalgo-text-generator'],
    'ai-copywriting-generator': ['headline-generator', 'slogan-generator', 'tagline-generator', 'linkedin-post-generator', 'instagram-post-generator'],
    'daily-affirmation-generator': ['gratitude-journal', 'mood-tracker', 'daily-journal', 'habit-tracker', 'random-word-generator'],
    'handwriting-generator': ['text-to-handwriting', 'cursive-text-generator', 'fancy-text-generator', 'signature-generator', 'signature-maker'],
    'random-word-generator': ['random-username-generator', 'random-name-generator', 'random-password-generator', 'random-number-generator', 'random-picker'],
    'checklist-generator': ['todo-list', 'packing-checklist', 'meeting-agenda-generator', 'weekly-planner', 'habit-tracker'],
    'email-signature-generator': ['signature-generator', 'signature-maker', 'online-signature', 'business-card-generator', 'resume-builder'],
    'image-sprite-generator': ['image-histogram', 'image-tinter', 'color-palette-extractor', 'svg-minifier', 'image-resizer'],
    'random-username-generator': ['random-word-generator', 'username-generator', 'random-name-generator', 'random-password-generator', 'random-picker'],
    # ==== 硬件测试族 ====
    'mouse-tester': ['keyboard-tester', 'mouse-click-counter', 'reaction-test', 'monitor-test', 'screen-resolution'],
    'battery-capacity-tester': ['battery-life-calculator', 'power-consumption-calculator', 'electricity-cost-calculator', 'monitor-test', 'screen-resolution'],
    'reaction-test': ['reaction-time-test', 'mouse-click-counter', 'typing-speed-test', 'vision-test', 'monitor-test'],
    'pow-captcha': ['random-number-generator', 'random-picker', 'dice-roll-simulator', 'spin-the-wheel', 'random-team-generator'],
    'speaker-test': ['online-tone-generator', 'sound-frequency-generator', 'metronome', 'bpm-tapper', 'audio-speed-changer'],
    'monitor-test': ['dpi-calculator', 'screen-resolution', 'ppi-calculator', 'color-converter', 'color-picker'],
    'dpi-calculator': ['ppi-calculator', 'monitor-test', 'screen-resolution', 'screen-resolution-checker', 'color-converter'],
    # ==== 睡眠族 ====
    'sleep-calculator': ['sleep-cycle-calculator', 'sleep-debt-calculator', 'sleep-cycles-calculator', 'world-clock', 'online-timer'],
    # ==== 日志/开发族 ====
    'log-viewer': ['log-parser', 'text-diff', 'json-formatter', 'regex-tester', 'api-tester'],
    'web-api-compatibility-checker': ['api-tester', 'json-formatter', 'http-status-codes', 'javascript-playground', 'html-validator'],
    'grammar-checker': ['spell-checker', 'paraphraser', 'text-rewriter', 'sentence-rewriter', 'plagiarism-checker'],
    'bic-checker': ['swift-bic-validation', 'swift-code-validator', 'iban-validator', 'vat-number-validator', 'vat-calculator'],
    'access-log-analyzer': ['log-parser', 'text-diff', 'json-formatter', 'regex-tester', 'ip-lookup'],
    # ==== 密码/编码族 ====
    'atbash': ['atbash-cipher', 'rot13', 'vigenere-cipher', 'caesar-cipher', 'morse-code'],
    'atbash-cipher': ['atbash', 'rot13', 'vigenere-cipher', 'caesar-cipher', 'morse-code'],
    # ==== Markdown 族 ====
    'markdown-table-formatter': ['markdown-table-generator', 'markdown-table-to-csv', 'markdown-editor', 'markdown-to-html', 'text-sorter'],
    # ==== 彩票/随机族 ====
    'lottery-picker': ['random-number-generator', 'random-picker', 'spin-the-wheel', 'dice-roll-simulator', 'random-team-generator'],
    # ==== 蒙特卡洛族 ====
    'monte-carlo-simulator': ['investment-calculator', 'compound-interest-calculator', 'roi-calculator', 'stock-return-calculator', 'mutual-fund-returns'],
}

def fix_page(slug):
    path = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        html = f.read()
    if slug not in FIX:
        return None
    tools = FIX[slug]
    links = ''.join(link(t) for t in tools)
    new_section = f'<section class="related-tools" style="margin:2rem 0;padding:1rem;background:#0f172a;border-radius:8px;"><h2 style="color:#e2e8f0;font-size:18px;margin-bottom:12px">🔗 相关工具推荐</h2>\n{links}</section>'
    # match existing related-tools section
    m = re.search(r'<section class="related-tools"[^>]*>.*?</section>', html, re.S)
    if not m:
        return None
    html = html[:m.start()] + new_section + html[m.end():]
    with open(path, 'w') as f:
        f.write(html)
    return tools

changed = []
for slug in FIX:
    r = fix_page(slug)
    if r:
        changed.append((slug, r))
print(f'fixed {len(changed)} pages')
for slug, tools in changed:
    print(slug, '->', ', '.join(tools))
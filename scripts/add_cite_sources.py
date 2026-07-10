#!/usr/bin/env python3
"""
GEO策略#1: Cite Sources — 批量添加权威引用
v2: 更可靠的FAQ插入策略

用法:
  python3 /tmp/add_cite_sources_v2.py           # 处理所有定义的工具
  python3 /tmp/add_cite_sources_v2.py tool1 tool2  # 指定工具
"""
import sys, os, re

BASE = os.path.expanduser("~/project")

# ====== 引用来源定义 ======
CITE_SOURCES = {
    "json-formatter": {
        "cn": {
            "faq": ("JSON格式的规范标准是什么？",
                    "JSON格式基于 <a href='https://www.json.org/json-en.html' target='_blank' rel='nofollow'>ECMA-404</a> 和 <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> 标准定义。JSON支持六种数据类型：字符串、数字、布尔值、null、数组和对象。所有现代编程语言都支持JSON的序列化和反序列化。")
        },
        "en": {
            "faq": ("What is the JSON format specification?",
                    "JSON format is defined by <a href='https://www.json.org/json-en.html' target='_blank' rel='nofollow'>ECMA-404</a> and <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> standards. JSON supports six data types: strings, numbers, booleans, null, arrays, and objects. All modern programming languages support JSON serialization and deserialization.")
        }
    },
    "json-validator": {
        "cn": {
            "faq": ("JSON验证检查哪些规则？",
                    "JSON验证依据 <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> 标准检查：字符串必须使用双引号、不能有尾随逗号、键名必须为字符串、数值不能有前导零、Unicode字符必须正确转义等。")
        },
        "en": {
            "faq": ("What rules does JSON validation check?",
                    "JSON validation follows <a href='https://datatracker.ietf.org/doc/html/rfc8259' target='_blank' rel='nofollow'>RFC 8259</a> standards: strings must use double quotes, no trailing commas, keys must be strings, numbers cannot have leading zeros, and Unicode characters must be properly escaped.")
        }
    },
    "color-picker": {
        "cn": {
            "faq": ("HEX、RGB和HSL颜色格式有什么区别？",
                    "根据 <a href='https://www.w3.org/TR/css-color-4/' target='_blank' rel='nofollow'>W3C CSS Color规范</a>：HEX (#RRGGBB) 是最常用的Web颜色表示法；RGB (rgb(r,g,b)) 是数字显示标准；HSL (hsl(h,s,l)) 基于色相/饱和度/亮度，更适合人类理解。三种格式可以互相转换。")
        },
        "en": {
            "faq": ("What's the difference between HEX, RGB, and HSL?",
                    "Per <a href='https://www.w3.org/TR/css-color-4/' target='_blank' rel='nofollow'>W3C CSS Color specification</a>: HEX (#RRGGBB) is the most common web color notation; RGB (rgb(r,g,b)) is the digital display standard; HSL (hsl(h,s,l)) is based on hue/saturation/lightness and is more intuitive for humans. All three formats are interconvertible.")
        }
    },
    "password-generator": {
        "cn": {
            "faq": ("什么样的密码算强密码？",
                    "根据 <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> 和 <a href='https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html' target='_blank' rel='nofollow'>OWASP建议</a>：强密码至少12位，包含大小写字母、数字和特殊字符。建议使用密码管理器生成和存储密码。")
        },
        "en": {
            "faq": ("What makes a strong password?",
                    "Per <a href='https://pages.nist.gov/800-63-4/sp800-63b.html' target='_blank' rel='nofollow'>NIST SP 800-63B</a> and <a href='https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html' target='_blank' rel='nofollow'>OWASP recommendations</a>: A strong password is at least 12 characters long, includes uppercase, lowercase, digits, and special characters. Using a password manager is recommended.")
        }
    },
    "hash-generator": {
        "cn": {
            "faq": ("SHA-256和MD5有什么区别？",
                    "<a href='https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final' target='_blank' rel='nofollow'>NIST SP 800-107</a> 定义SHA-256为安全哈希算法，输出256位摘要，广泛用于数字签名和证书验证。MD5输出128位，但已被证实存在碰撞漏洞，不推荐用于安全场景。本工具支持多种算法供不同场景使用。")
        },
        "en": {
            "faq": ("What's the difference between SHA-256 and MD5?",
                    "<a href='https://csrc.nist.gov/publications/detail/sp/800-107/rev-1/final' target='_blank' rel='nofollow'>NIST SP 800-107</a> defines SHA-256 as a secure hash algorithm outputting 256-bit digests, widely used in digital signatures and certificate verification. MD5 outputs 128 bits but has proven collision vulnerabilities and is not recommended for security applications.")
        }
    },
    "base64-encoder": {
        "cn": {
            "faq": ("Base64编码的用途是什么？",
                    "根据 <a href='https://datatracker.ietf.org/doc/html/rfc4648' target='_blank' rel='nofollow'>RFC 4648</a>：Base64编码用于在需要文本传输的场合传递二进制数据，如电子邮件附件 (MIME)、在URL/HTML中嵌入图片数据 (Data URIs)、JSON中传输二进制字段等。Base64编码比原始二进制大约增加33%的体积。")
        },
        "en": {
            "faq": ("What is Base64 encoding used for?",
                    "Per <a href='https://datatracker.ietf.org/doc/html/rfc4648' target='_blank' rel='nofollow'>RFC 4648</a>: Base64 encoding is used to transmit binary data in text-only environments such as email attachments (MIME), embedding images in HTML (Data URIs), and transmitting binary fields in JSON. Base64 adds approximately 33% to the data size.")
        }
    },
    "css-formatter": {
        "cn": {
            "faq": ("CSS格式化应该遵循哪些规范？",
                    "按照 <a href='https://www.w3.org/TR/CSS/#css-levels' target='_blank' rel='nofollow'>W3C CSS规范</a>：格式良好的CSS应使用一致缩进（2或4空格），选择器与花括号同行，每个属性独占一行，属性后加冒号和空格。本工具自动处理这些规范。")
        },
        "en": {
            "faq": ("What standards should CSS formatting follow?",
                    "Per <a href='https://www.w3.org/TR/CSS/#css-levels' target='_blank' rel='nofollow'>W3C CSS specifications</a>: Well-formatted CSS uses consistent indentation (2 or 4 spaces), selectors on same line as opening brace, one property per line, and colons followed by a space. This tool handles all these conventions automatically.")
        }
    },
    "html-formatter": {
        "cn": {
            "faq": ("HTML格式化的最佳实践是什么？",
                    "根据 <a href='https://html.spec.whatwg.org/' target='_blank' rel='nofollow'>WHATWG HTML标准</a>：格式化HTML时应确保标签正确嵌套、使用一致缩进、自闭合标签规范、属性使用双引号包裹。良好的格式化不仅提高可读性，也有助于调试和团队协作。")
        },
        "en": {
            "faq": ("What are HTML formatting best practices?",
                    "Per the <a href='https://html.spec.whatwg.org/' target='_blank' rel='nofollow'>WHATWG HTML standard</a>: Proper HTML formatting ensures correct tag nesting, consistent indentation, proper self-closing tags, and attributes wrapped in double quotes. Good formatting improves readability, debugging, and team collaboration.")
        }
    },
    "qr-code-generator": {
        "cn": {
            "faq": ("二维码能存储多少数据？",
                    "根据 <a href='https://www.iso.org/standard/62021.html' target='_blank' rel='nofollow'>ISO/IEC 18004</a>：QR码最大可存储7,089个数字字符、4,296个字母数字字符、或2,953个字节（二进制）数据。数据量取决于QR码版本（1-40）和纠错级别（L/M/Q/H）。")
        },
        "en": {
            "faq": ("How much data can a QR code store?",
                    "Per <a href='https://www.iso.org/standard/62021.html' target='_blank' rel='nofollow'>ISO/IEC 18004</a>: QR codes can store up to 7,089 numeric characters, 4,296 alphanumeric characters, or 2,953 bytes of binary data. Capacity depends on the QR code version (1-40) and error correction level (L/M/Q/H).")
        }
    },
    "meta-tag-generator": {
        "cn": {
            "faq": ("Meta标签对SEO有多大影响？",
                    "根据 <a href='https://developers.google.com/search/docs/appearance/title-link' target='_blank' rel='nofollow'>Google搜索中心文档</a>：标题标签（title）和meta description不直接作为排名因素，但影响点击率（CTR）。Open Graph标签影响社交平台上的分享预览效果。合理的meta标签设置可以显著提升搜索曝光。")
        },
        "en": {
            "faq": ("How much do meta tags affect SEO?",
                    "Per <a href='https://developers.google.com/search/docs/appearance/title-link' target='_blank' rel='nofollow'>Google Search Central documentation</a>: Title tags and meta descriptions are not direct ranking factors but significantly impact click-through rates (CTR). Open Graph tags influence how content appears when shared on social platforms.")
        }
    },
    "image-resizer": {
        "cn": {
            "faq": ("图片缩放会影响图片质量吗？",
                    "根据 <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas' target='_blank' rel='nofollow'>MDN Canvas教程</a>：放大图片会导致像素化（质量下降），缩小图片会丢失细节。建议缩放比控制在50%-200%范围内。本工具使用双线性插值算法，在速度和画质间取得平衡。")
        },
        "en": {
            "faq": ("Does image resizing affect quality?",
                    "Per <a href='https://developer.mozilla.org/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas' target='_blank' rel='nofollow'>MDN Canvas tutorial</a>: Upscaling causes pixelation (quality loss), while downscaling loses detail. Keeping resize ratios within 50%-200% is recommended. This tool uses bilinear interpolation for a balance of speed and quality.")
        }
    },
    "regex-tester": {
        "cn": {
            "faq": ("正则表达式的性能如何优化？",
                    "根据 <a href='https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/' target='_blank' rel='nofollow'>精通正则表达式 (Friedl)</a>：避免回溯灾难（如嵌套量词）、使用非贪婪匹配（量词加?）、预编译正则对象、使用字符类而非多选分支（[abc] vs (a|b|c)）等策略可以显著提升匹配性能。")
        },
        "en": {
            "faq": ("How to optimize regular expression performance?",
                    "Per <a href='https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/' target='_blank' rel='nofollow'>Mastering Regular Expressions (Friedl)</a>: Avoid catastrophic backtracking (nested quantifiers), use non-greedy matching, pre-compile regex objects, and use character classes instead of alternations to significantly improve match performance.")
        }
    },
    "text-counter": {
        "cn": {
            "faq": ("Unicode文本统计有什么特殊规则？",
                    "根据 <a href='https://www.unicode.org/reports/tr29/' target='_blank' rel='nofollow'>Unicode文本分段规则 (UAX #29)</a>：中英文混合文本的单词边界不同，中文按字计数，英文按空格分词。emoji和组合字符（如带声调的字母）应计为单个字符。本工具遵循Unicode标准进行统计。")
        },
        "en": {
            "faq": ("What special rules apply to Unicode text counting?",
                    "Per <a href='https://www.unicode.org/reports/tr29/' target='_blank' rel='nofollow'>Unicode Text Segmentation rules (UAX #29)</a>: Word boundaries differ between languages — English splits by spaces while CJK characters count individually. Emoji and combining characters should count as single characters. This tool follows Unicode standards for counting.")
        }
    },
    "unit-converter": {
        "cn": {
            "faq": ("国际单位制（SI）是什么？",
                    "根据 <a href='https://www.bipm.org/en/measurement-units/' target='_blank' rel='nofollow'>国际计量局 (BIPM)</a>：SI单位制是全球通用的度量衡标准，包括7个基本单位（米、千克、秒、安培、开尔文、摩尔、坎德拉）。所有其他单位都可由基本单位导出。本工具使用SI标准的精确换算系数。")
        },
        "en": {
            "faq": ("What is the International System of Units (SI)?",
                    "Established by the <a href='https://www.bipm.org/en/measurement-units/' target='_blank' rel='nofollow'>International Bureau of Weights and Measures (BIPM)</a>: The SI system defines 7 base units (meter, kilogram, second, ampere, kelvin, mole, candela). All other units derive from these. This tool uses SI-standard precise conversion factors.")
        }
    },
    "color-contrast-checker": {
        "cn": {
            "faq": ("WCAG AA和AAA标准的最低对比度是多少？",
                    "根据 <a href='https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html' target='_blank' rel='nofollow'>WCAG 2.1标准</a>：AA级普通文字需要≥4.5:1，大号文字（≥18px加粗或≥24px）需要≥3:1；AAA级普通文字需要≥7:1，大号文字需要≥4.5:1。")
        },
        "en": {
            "faq": ("What are the minimum WCAG AA and AAA contrast ratios?",
                    "Per <a href='https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html' target='_blank' rel='nofollow'>WCAG 2.1</a>: AA requires ≥4.5:1 for normal text and ≥3:1 for large text (≥18px bold or ≥24px). AAA requires ≥7:1 for normal text and ≥4.5:1 for large text.")
        }
    },
    "age-calculator": {
        "cn": {
            "faq": ("年龄计算如何处理闰年？",
                    "根据格里高利历法：闰年规则为能被4整除但不能被100整除，或能被400整除的年份。闰年2月有29天，年龄计算器会自动处理这一差异，确保在所有边界日期（如闰年2月29日出生）下计算准确。")
        },
        "en": {
            "faq": ("How does age calculation handle leap years?",
                    "Per the Gregorian calendar: Leap years are divisible by 4 but not by 100, or divisible by 400. February has 29 days in leap years. This calculator automatically handles these differences, ensuring accuracy for all boundary dates including February 29 birthdays.")
        }
    },
    "currency-converter": {
        "cn": {
            "faq": ("汇率是如何确定的？",
                    "汇率由全球外汇市场供需决定，同时参考各国央行的基准利率。主要汇率来源包括 <a href='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html' target='_blank' rel='nofollow'>欧洲央行 (ECB)</a>、<a href='https://www.imf.org/en/Data' target='_blank' rel='nofollow'>IMF</a> 和各国央行。实时汇率每分钟都在变化。")
        },
        "en": {
            "faq": ("How are exchange rates determined?",
                    "Exchange rates are determined by global forex market supply and demand, influenced by central bank base rates. Major rate sources include the <a href='https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html' target='_blank' rel='nofollow'>European Central Bank (ECB)</a> and <a href='https://www.imf.org/en/Data' target='_blank' rel='nofollow'>International Monetary Fund (IMF)</a>.")
        }
    },
    "aes-encrypt": {
        "cn": {
            "faq": ("AES加密算法的安全性如何？",
                    "AES (Advanced Encryption Standard) 由 <a href='https://csrc.nist.gov/pubs/fips/197/final' target='_blank' rel='nofollow'>NIST FIPS 197</a> 标准定义，是目前全球最广泛使用的对称加密算法。AES-256提供256位密钥强度，被美国政府用于绝密级数据保护，也被银行、金融机构和科技公司广泛采用。截至目前，没有已知的可行攻击能破解AES-256。")
        },
        "en": {
            "faq": ("How secure is the AES encryption algorithm?",
                    "AES (Advanced Encryption Standard), defined by <a href='https://csrc.nist.gov/pubs/fips/197/final' target='_blank' rel='nofollow'>NIST FIPS 197</a>, is the most widely used symmetric encryption algorithm globally. AES-256 provides 256-bit key strength, used by the US government for top-secret data protection and widely adopted by banks, financial institutions, and tech companies.")
        }
    }
}


def find_faq_end_position(html):
    """
    Find the position to insert a new FAQ item.
    Strategy: Find the closing </div> of the FAQ wrapper div (just before ad-placeholder).
    """
    # Strategy 1: Find FAQ section heading, then find the closing </div> of FAQ wrapper
    # First locate the FAQ section by its heading
    faq_heading = re.search(r'(<h2>[^<]*?(?:常见问题|FAQ)[^<]*?</h2>)', html)
    if faq_heading:
        # Search from FAQ heading onward for the wrapper close before ad-placeholder
        after_faq = html[faq_heading.end():]
        m = re.search(r'(</div>\s*\n\s*<div class="ad-placeholder")', after_faq)
        if m:
            return faq_heading.end() + m.start(1)
    
    # Strategy 2: Find FAQ section heading, then find </div>\n</div> after last faq-item
    if faq_heading:
        after_faq = html[faq_heading.end():]
        # Find the last </div> that's followed by </div> then ad/footer
        m = re.search(r'(</div>\s*</div>\s*\n\s*(?:<!--|$))', after_faq)
        if m:
            # Return position right after the first </div> (between faq-item close and wrapper close)
            return faq_heading.end() + m.start() + len('</div>')
    
    # Strategy 3: Fallback (before footer)
    m = re.search(r'(</div>\s*\n\s*<div class="footer container">)', html)
    if m:
        before = html[:m.start()]
        if 'faq-item' in before.lower():
            return m.start(1)
    
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
        
        filepath = os.path.join(BASE, tool_dir, 'index.html') if lang == 'cn' else os.path.join(BASE, 'en', tool_dir, 'index.html')
        
        if not os.path.exists(filepath):
            print(f"  ⛔ Not found: {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Check if already has cite source
        if 'target="_blank" rel="nofollow"' in html and ('RFC' in html or 'NIST' in html or 'WCAG' in html or 'ECMA' in html):
            if cite_data[lang]['faq'][0][:20] in html:
                print(f"  ⏭️  Already has this citation")
                continue
        
        faq_q, faq_a = cite_data[lang]['faq']
        insert_pos = find_faq_end_position(html)
        
        if insert_pos is None:
            print(f"  ❌ Could not find FAQ section end")
            continue
        
        faq_html = f"""
    <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
      <h3 itemprop="name">{faq_q}</h3>
      <div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
        <p itemprop="text">{faq_a}</p>
      </div>
    </div>"""
        
        html = html[:insert_pos] + faq_html + html[insert_pos:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"  ✅ {lang.upper()} added FAQ cite entry: {faq_q[:40]}...")
        count += 1
    
    return count


def main():
    tools = sys.argv[1:] if len(sys.argv) > 1 else list(CITE_SOURCES.keys())
    langs = ['cn', 'en']
    
    print(f"📋 Cite-Source Batch Processor v2")
    print(f"   Tools: {len(tools)}, Languages: {langs}")
    print(f"=" * 50)
    
    total = 0
    for tool in tools:
        print(f"\n📦 {tool}:")
        total += process_tool(tool, langs)
    
    print(f"\n{'=' * 50}")
    print(f"✅ Done! {total} pages updated.")

if __name__ == '__main__':
    main()

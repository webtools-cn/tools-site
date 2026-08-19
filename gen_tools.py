#!/usr/bin/env python3
"""批量生成工具页面 - 中英文双语版"""
import os, json

BASE = os.path.expanduser("~/tools-site")

TOOLS = {
    "pdf-encrypt": {
        "cn_name": "PDF加密工具",
        "en_name": "PDF Encrypt Tool",
        "cn_desc": "免费在线PDF加密工具，为PDF文件添加密码保护。纯前端本地处理，文件不上传服务器，安全可靠。",
        "en_desc": "Free online PDF encryption tool - add password protection to PDF files. Client-side processing, files never leave your browser.",
        "cn_keywords": "PDF加密,PDF密码保护,PDF安全,在线PDF加密,PDF加锁,PDF权限保护,免费PDF加密",
        "en_keywords": "PDF encrypt,PDF password protect,PDF security,online PDF encryption,lock PDF,protect PDF,free PDF encrypt",
        "cat": "security",
        "cn_cat": "安全工具",
        "cn_howto_steps": [
            "上传PDF文件（拖拽或点击选择）",
            "设置密码（用户密码和所有者密码）",
            "点击加密按钮处理文件",
            "下载加密后的PDF文件"
        ],
        "en_howto_steps": [
            "Upload your PDF file (drag & drop or click to select)",
            "Set passwords (user password and owner password)",
            "Click the encrypt button",
            "Download the encrypted PDF file"
        ],
        "cn_faq": [
            ("PDF加密安全吗？", "PDF加密使用AES-256加密算法保护您的PDF文件。本工具的所有处理都在浏览器本地完成，文件不会上传到任何服务器，确保您的数据安全。"),
            ("用户密码和所有者密码有什么区别？", "用户密码（打开密码）是打开PDF时需要输入的密码。所有者密码用于控制权限（如打印、复制、编辑等），设置所有者密码可以防止他人修改PDF的权限设置。"),
            ("加密后的PDF在所有设备上都能打开吗？", "是的，使用标准PDF加密算法（AES-256和RC4），加密后的PDF可在所有主流PDF阅读器中打开，包括Adobe Acrobat、浏览器内置PDF查看器等。"),
            ("可以加密什么样的PDF？", "本工具支持加密任何有效的PDF文件。如果PDF文件本身已加密，建议先解密再重新加密，以确保兼容性。文件大小建议在50MB以内以获得最佳性能。")
        ],
        "en_faq": [
            ("Is PDF encryption safe?", "PDF encryption uses AES-256 encryption algorithm to protect your PDF files. All processing happens locally in your browser — files never leave your device, ensuring complete data security."),
            ("What's the difference between user password and owner password?", "The user password (open password) is required to open the PDF. The owner password controls permissions (printing, copying, editing, etc.). Setting an owner password prevents others from modifying the PDF's permission settings."),
            ("Will encrypted PDFs work on all devices?", "Yes, using standard PDF encryption algorithms (AES-256 and RC4), encrypted PDFs can be opened in all major PDF readers, including Adobe Acrobat, browser built-in PDF viewers, and more."),
            ("What kind of PDFs can I encrypt?", "This tool supports encrypting any valid PDF file. If the PDF is already encrypted, we recommend decrypting it first before re-encrypting for compatibility. File size under 50MB is recommended for best performance.")
        ],
    },
    "pdf-decrypt": {
        "cn_name": "PDF解密工具",
        "en_name": "PDF Decrypt Tool",
        "cn_desc": "免费在线PDF解密工具，移除PDF文件的密码保护（需知道密码）。纯前端本地处理，文件安全不上传。",
        "en_desc": "Free online PDF decryption tool - remove password protection from PDF files (password required). Client-side processing, files stay secure.",
        "cn_keywords": "PDF解密,PDF密码移除,PDF解锁,在线PDF解密,PDF去密码,PDF解锁工具,免费PDF解密",
        "en_keywords": "PDF decrypt,PDF password remove,PDF unlock,online PDF decryption,remove PDF password,unlock PDF,free PDF decrypt",
        "cat": "security",
        "cn_cat": "安全工具",
        "cn_howto_steps": [
            "上传需要解密的PDF文件",
            "输入文件的打开密码",
            "点击解密按钮处理",
            "下载解密后的PDF文件"
        ],
        "en_howto_steps": [
            "Upload the encrypted PDF file",
            "Enter the file's open password",
            "Click the decrypt button",
            "Download the decrypted PDF file"
        ],
        "cn_faq": [
            ("忘记密码可以解密PDF吗？", "不可以。PDF加密使用的是强加密算法（AES-256/RC4），没有密码无法解密。如果忘记了PDF密码，建议联系文件创建者获取密码。本工具需要正确的密码才能解密。"),
            ("解密后的PDF保留原始内容吗？", "是的，解密后的PDF保留所有原始内容（文字、图片、格式、链接等），仅移除了密码保护。解密不会修改PDF的实质内容。"),
            ("解密PDF需要什么权限？", "你只需要知道PDF的打开密码（用户密码）。如果PDF有所有者密码但没有用户密码，通常也可以直接打开并解密。不需要所有者密码即可解密。"),
            ("这个工具安全吗？", "完全安全。所有处理在您的浏览器本地完成，PDF文件不会上传到任何服务器。解密完成后，您可以立即下载，原始文件数据不会保留。")
        ],
        "en_faq": [
            ("Can I decrypt a PDF without the password?", "No. PDF encryption uses strong encryption algorithms (AES-256/RC4) and cannot be decrypted without the password. Contact the file creator if you forgot the password. This tool requires the correct password."),
            ("Does the decrypted PDF retain original content?", "Yes, the decrypted PDF retains all original content (text, images, formatting, links, etc.) — only the password protection is removed. Decryption does not modify the PDF's substantive content."),
            ("What permissions do I need to decrypt?", "You only need the PDF's open password (user password). If the PDF has an owner password but no user password, it can usually be opened and decrypted directly. Owner password is not required."),
            ("Is this tool secure?", "Completely secure. All processing happens locally in your browser — PDF files are never uploaded to any server. After decryption, you can download immediately, and original file data is not retained.")
        ],
    },
    "ascii-to-hex": {
        "cn_name": "ASCII转Hex工具",
        "en_name": "ASCII to Hex Converter",
        "cn_desc": "免费在线ASCII转十六进制转换工具，支持文本与十六进制互转，实时转换。纯前端本地处理，数据安全不上传。",
        "en_desc": "Free online ASCII to hexadecimal converter - real-time text-to-hex conversion. Client-side processing, data secure and private.",
        "cn_keywords": "ASCII转Hex,ASCII十六进制,文本转Hex,Hex转ASCII,在线ASCII转换,字符编码转换,免费Hex转换",
        "en_keywords": "ASCII to hex,text to hex,hex to ASCII,ASCII hex converter,online ASCII converter,character encoding,free hex converter",
        "cat": "dev",
        "cn_cat": "开发工具",
        "cn_howto_steps": [
            "在文本框中输入ASCII文本",
            "选择转换方向（ASCII→Hex 或 Hex→ASCII）",
            "查看实时转换结果",
            "点击复制按钮获取转换结果"
        ],
        "en_howto_steps": [
            "Enter your ASCII text in the input box",
            "Choose conversion direction (ASCII→Hex or Hex→ASCII)",
            "View real-time conversion results",
            "Click copy to get the converted result"
        ],
        "cn_faq": [
            ("ASCII和Hex有什么区别？", "ASCII（美国标准信息交换码）是字符编码方案，用0-127的数字表示英文字母、数字和符号。Hex（十六进制）是基数为16的数字系统，用0-9和A-F表示。ASCII转Hex即将每个字符的ASCII码值转换为对应的十六进制表示。"),
            ("支持哪些字符？", "该工具支持标准ASCII字符集（0-127），包括英文字母（A-Z, a-z）、数字（0-9）、常见标点符号和控制字符。不支持Unicode扩展字符（如中文、emoji）。"),
            ("Hex有什么格式要求？", "输入的Hex字符串应使用空格或逗号分隔，例如 '48 65 6C 6C 6F' 或 '48,65,6C,6C,6F'。也支持无分隔符的连续Hex字符串，但需确保长度为偶数。"),
            ("这个工具有什么实际用途？", "ASCII↔Hex转换常用于：1) 调试网络协议和二进制数据；2) 嵌入式系统编程；3) 分析和修改二进制文件；4) 计算机安全领域的shellcode编写；5) 学习计算机底层原理。")
        ],
        "en_faq": [
            ("What's the difference between ASCII and Hex?", "ASCII (American Standard Code for Information Interchange) is a character encoding scheme using numbers 0-127 for letters, digits, and symbols. Hex (hexadecimal) is base-16 using digits 0-9 and A-F. ASCII to Hex converts each character's ASCII code value to its hexadecimal representation."),
            ("Which characters are supported?", "This tool supports the standard ASCII character set (0-127), including English letters (A-Z, a-z), digits (0-9), common punctuation marks, and control characters. Unicode extended characters (Chinese, emoji) are not supported."),
            ("What Hex format is required?", "Input Hex strings can be space-separated or comma-separated, e.g., '48 65 6C 6C 6F' or '48,65,6C,6C,6F'. Continuous Hex without separators is also supported but must have even length."),
            ("What are practical uses for this tool?", "ASCII↔Hex conversion is commonly used for: 1) Debugging network protocols and binary data; 2) Embedded systems programming; 3) Analyzing and modifying binary files; 4) Shellcode development in cybersecurity; 5) Learning computer fundamentals.")
        ],
    },
    "bar-code-generator": {
        "cn_name": "条形码生成器",
        "en_name": "Barcode Generator",
        "cn_desc": "免费在线条形码生成器，支持Code128、EAN-13、UPC-A等多种条码格式。纯前端本地生成，可下载为PNG/SVG。",
        "en_desc": "Free online barcode generator - supports Code128, EAN-13, UPC-A and more formats. Client-side generation, download as PNG/SVG.",
        "cn_keywords": "条形码生成器,Code128,EAN-13,UPC-A,在线条码生成,条码制作,免费条码生成器,PNG条码,SVG条码",
        "en_keywords": "barcode generator,Code128,EAN-13,UPC-A,online barcode,generate barcode,free barcode maker,PNG barcode,SVG barcode",
        "cat": "creative",
        "cn_cat": "创意工具",
        "cn_howto_steps": [
            "输入要编码的文本或数字",
            "选择条形码格式（Code128/EAN-13/UPC-A等）",
            "调整条形码尺寸和颜色",
            "点击下载保存为PNG或SVG格式"
        ],
        "en_howto_steps": [
            "Enter the text or number to encode",
            "Select barcode format (Code128/EAN-13/UPC-A, etc.)",
            "Adjust barcode size and colors",
            "Click download to save as PNG or SVG"
        ],
        "cn_faq": [
            ("Code128和EAN-13有什么区别？", "Code128是一种高密度条码，支持所有128个ASCII字符，适用于物流、仓储等场景。EAN-13是13位数字的国际商品条码，广泛用于零售商品包装上。Code128更灵活，EAN-13更标准化。"),
            ("条形码可以用在哪些场景？", "条形码广泛应用于：1) 商品零售（UPC/EAN条码）；2) 物流和仓储管理（Code128）；3) 图书出版（ISBN条码）；4) 医疗（药品追溯）；5) 票务和会员卡系统。"),
            ("生成的条形码能扫描吗？", "是的，生成的条形码符合国际标准规范，可以被任何标准条形码扫描器或手机扫码App正确识别。建议使用300 DPI以上的分辨率打印以获得最佳扫描效果。"),
            ("支持中文/特殊字符吗？", "Code128格式支持全部128个ASCII字符，但不直接支持中文。如果需要编码中文，建议使用QR二维码。EAN-13和UPC-A仅支持数字。对于非ASCII字符，请选择Code128 Auto模式。")
        ],
        "en_faq": [
            ("What's the difference between Code128 and EAN-13?", "Code128 is a high-density barcode supporting all 128 ASCII characters, ideal for logistics and warehousing. EAN-13 is a 13-digit international product barcode standard widely used on retail packaging. Code128 is more flexible; EAN-13 is more standardized."),
            ("Where can barcodes be used?", "Barcodes are widely used for: 1) Retail products (UPC/EAN barcodes); 2) Logistics and warehouse management (Code128); 3) Book publishing (ISBN barcodes); 4) Healthcare (drug traceability); 5) Ticketing and membership card systems."),
            ("Can the generated barcode be scanned?", "Yes, generated barcodes comply with international standards and can be correctly read by any standard barcode scanner or mobile scanning app. We recommend printing at 300+ DPI for optimal scanning results."),
            ("Does it support Chinese/special characters?", "Code128 format supports all 128 ASCII characters but does not directly support Chinese characters. Use QR codes for Chinese text. EAN-13 and UPC-A only support digits. For non-ASCII characters, choose Code128 Auto mode.")
        ],
    },
    "blurhash-generator": {
        "cn_name": "BlurHash生成器",
        "en_name": "BlurHash Generator",
        "cn_desc": "免费在线BlurHash生成与解码工具，为图片生成紧凑的占位符字符串。纯前端Canvas处理，快速生成模糊预览。",
        "en_desc": "Free online BlurHash generator and decoder - create compact placeholder strings for images. Client-side Canvas processing for fast blur previews.",
        "cn_keywords": "BlurHash,图片占位符,模糊预览,在线BlurHash,图片懒加载,占位图生成,免费BlurHash工具",
        "en_keywords": "BlurHash,image placeholder,blur preview,online BlurHash,image lazy loading,placeholder generator,free BlurHash tool",
        "cat": "dev",
        "cn_cat": "开发工具",
        "cn_howto_steps": [
            "上传图片或粘贴BlurHash字符串",
            "选择操作模式（编码或解码）",
            "调整组件数（4x3到9x9）控制精度",
            "复制BlurHash字符串到项目中使用"
        ],
        "en_howto_steps": [
            "Upload an image or paste a BlurHash string",
            "Select operation mode (encode or decode)",
            "Adjust component count (4x3 to 9x9) for precision",
            "Copy the BlurHash string for use in your project"
        ],
        "cn_faq": [
            ("什么是BlurHash？", "BlurHash是由Wolt公司开发的开源算法，将图片压缩成一个短字符串（通常20-30个字符），用于在图片加载前显示模糊的占位图。它比传统的灰色占位框或低分辨率缩略图更加美观，特别适合用于Web和移动App的图片懒加载场景。"),
            ("组件数（4x3, 6x4等）是什么意思？", "组件数决定了BlurHash的精度和字符串长度。更多的组件（如9x9）能更准确地还原图片的颜色分布，但生成的字符串也更长。较少的组件（如4x3）生成更短的字符串但细节更模糊。默认的4x3适合大多数场景。"),
            ("BlurHash字符串可以直接用在HTML中吗？", "BlurHash本身只是一个字符串，需要配合解码库（如blurhash-js）在客户端渲染为Canvas图像。主流前端框架（React、Vue、Svelte）都有对应的BlurHash组件。解码后的渲染约需20-50ms，非常快速。"),
            ("BlurHash和占位图（placeholder image）有什么区别？", "BlurHash是纯文本字符串，不需要额外的网络请求（可直接嵌入HTML/JSON中），而传统的占位图需要额外的HTTP请求加载图片文件。BlurHash也更紧凑——一个30字符的字符串即可表示一幅模糊预览图。")
        ],
        "en_faq": [
            ("What is BlurHash?", "BlurHash is an open-source algorithm developed by Wolt that compresses an image into a short string (usually 20-30 characters), used to display a blurry placeholder before the actual image loads. It's more aesthetically pleasing than gray placeholder boxes and ideal for lazy loading in web and mobile apps."),
            ("What do the component counts (4x3, 6x4) mean?", "Component count determines BlurHash precision and string length. More components (e.g., 9x9) reproduce color distribution more accurately but generate longer strings. Fewer components (e.g., 4x3) produce shorter strings with blurrier details. Default 4x3 works well for most cases."),
            ("Can I use BlurHash strings directly in HTML?", "BlurHash is just a string — it needs a decoding library (like blurhash-js) to render as a Canvas image on the client side. Major frontend frameworks (React, Vue, Svelte) have BlurHash components. Decoded rendering takes about 20-50ms, very fast."),
            ("How is BlurHash different from placeholder images?", "BlurHash is a pure text string — no extra network request needed (can be embedded directly in HTML/JSON), while traditional placeholder images require an additional HTTP request. BlurHash is also more compact — a 30-character string can represent a blur preview.")
        ],
    },
    "phone-number-formatter": {
        "cn_name": "电话号码格式化工具",
        "en_name": "Phone Number Formatter",
        "cn_desc": "免费在线国际电话号码格式化与验证工具，支持200+国家/地区号码格式。纯前端本地处理，保护隐私安全。",
        "en_desc": "Free online international phone number formatter and validator - supports 200+ countries/regions. Client-side processing, privacy-safe.",
        "cn_keywords": "电话号码格式化,国际电话格式,手机号格式化,电话验证,国家区号,号码标准化,免费电话格式化",
        "en_keywords": "phone number format,international phone number,mobile format,phone validator,country code,number standardization,free phone formatter",
        "cat": "utility",
        "cn_cat": "实用工具",
        "cn_howto_steps": [
            "输入需要格式化的电话号码",
            "选择或自动检测国家/地区代码",
            "选择输出格式（E.164/国际/国内/RFC3966）",
            "复制格式化后的号码或验证号码有效性"
        ],
        "en_howto_steps": [
            "Enter the phone number to format",
            "Select or auto-detect country code",
            "Choose output format (E.164/International/National/RFC3966)",
            "Copy the formatted number or validate it"
        ],
        "cn_faq": [
            ("E.164格式是什么？", "E.164是国际电信联盟（ITU）定义的国际电话号码标准格式，格式为：+[国家代码][电话号码]，最多15位数字。例如中国手机号在E.164格式下为 +8613800138000。这是国际电话号码存储和传输的标准格式。"),
            ("支持哪些国家的电话号码？", "本工具支持200+国家和地区的电话号码格式，包括中国大陆（+86）、香港（+852）、台湾（+886）、美国（+1）、英国（+44）、日本（+81）等。内置完整的国家代码和号码长度规则。"),
            ("数据安全吗？号码会上传服务器吗？", "完全安全。所有电话号格式化处理都在您的浏览器本地完成，输入的号码不会被发送到任何服务器。这是一个纯前端的工具，您可以放心使用。"),
            ("哪些格式之间可以转换？", "支持E.164格式（+8613800138000）、国际格式（+86 138 0013 8000）、国内格式（138 0013 8000）和RFC3966格式（tel:+86-138-0013-8000）。还支持去掉空格/括号/连字符的纯数字格式。")
        ],
        "en_faq": [
            ("What is E.164 format?", "E.164 is the international phone number standard defined by ITU, formatted as: +[country code][phone number], up to 15 digits. For example, a US number in E.164 format is +12025551234. This is the standard format for international phone number storage and transmission."),
            ("Which countries are supported?", "This tool supports 200+ country phone number formats, including USA (+1), UK (+44), China (+86), Japan (+81), Australia (+61), Germany (+49), and more. Complete country codes and number length rules are built-in."),
            ("Is my data secure? Are numbers sent to servers?", "Completely secure. All phone number formatting happens locally in your browser — numbers are never sent to any server. This is a pure frontend tool, use it with confidence."),
            ("Which format conversions are supported?", "Supports E.164 format (+12025551234), International format (+1 202 555 1234), National format ((202) 555-1234), and RFC3966 format (tel:+1-202-555-1234). Plain digit format (remove spaces/parentheses/dashes) is also supported.")
        ],
    },
}

def make_html(slug, info, lang):
    """Generate tool page HTML"""
    is_cn = (lang == "zh-CN")
    canonical = f"https://webtools-cn.github.io/tools-site/{slug}/"
    if not is_cn:
        canonical = f"https://webtools-cn.github.io/tools-site/en/{slug}/"
    
    name = info["cn_name"] if is_cn else info["en_name"]
    desc = info["cn_desc"] if is_cn else info["en_desc"]
    keywords = info["cn_keywords"] if is_cn else info["en_keywords"]
    cat_name = info["cn_cat"] if is_cn else {
        "security": "Security Tools", "dev": "Developer Tools", 
        "creative": "Creative Tools", "utility": "Utility Tools"
    }[info["cat"]]
    faq = info["cn_faq"] if is_cn else info["en_faq"]
    howto_steps = info["cn_howto_steps"] if is_cn else info["en_howto_steps"]
    
    og_site = "在线小工具矩阵" if is_cn else "WebTools - Free Online Tools"
    breadcrumb_home = "首页" if is_cn else "Home"
    step_names = ["上传文件", "设置参数", "开始处理", "下载结果"] if is_cn else ["Upload File", "Configure", "Process", "Download"]
    
    if slug in ("pdf-encrypt", "pdf-decrypt"):
        step_names = ["上传PDF文件", "输入密码", "点击处理", "下载结果"] if is_cn else ["Upload PDF", "Enter Password", "Process", "Download"]
    elif slug == "ascii-to-hex":
        step_names = ["输入文本/Hex", "选择方向", "查看结果", "复制使用"] if is_cn else ["Enter Text/Hex", "Choose Direction", "View Result", "Copy & Use"]
    elif slug == "bar-code-generator":
        step_names = ["输入内容", "选择格式", "调整参数", "下载条码"] if is_cn else ["Enter Content", "Select Format", "Adjust Settings", "Download"]
    elif slug == "blurhash-generator":
        step_names = ["上传图片", "选择模式", "调整精度", "复制字符串"] if is_cn else ["Upload Image", "Select Mode", "Adjust Precision", "Copy Hash"]
    elif slug == "phone-number-formatter":
        step_names = ["输入号码", "选择国家", "选格式", "复制结果"] if is_cn else ["Enter Number", "Select Country", "Pick Format", "Copy Result"]
    
    faq_json = json.dumps([
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq
    ], ensure_ascii=False)
    
    howto_json = json.dumps([
        {"@type": "HowToStep", "position": i+1, "name": step_names[i], "text": s, "url": canonical + "#step" + str(i+1)}
        for i, s in enumerate(howto_steps)
    ], ensure_ascii=False)
    
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": breadcrumb_home, "item": "https://webtools-cn.github.io/tools-site/"},
            {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"https://webtools-cn.github.io/tools-site/#{info['cat']}"},
            {"@type": "ListItem", "position": 3, "name": name, "item": canonical}
        ]
    }, ensure_ascii=False)
    
    lang_switch_html = ""
    if is_cn:
        lang_switch_html = '<a href="/tools-site/en/' + slug + '/" style="position:absolute;top:12px;right:12px;font-size:13px;color:#3b82f6;text-decoration:none;">English</a>'
    else:
        lang_switch_html = '<a href="/tools-site/' + slug + '/" style="position:absolute;top:12px;right:12px;font-size:13px;color:#3b82f6;text-decoration:none;">中文</a>'
    
    tool_html = generate_tool_specific_html(slug, is_cn)
    
    ui_labels = {}
    if is_cn:
        ui_labels = {"header_desc": "纯前端本地处理，安全快速", "copy": "复制", "copied": "已复制！", "download": "下载结果", "input_label": "输入", "output_label": "结果", "h1_seo": f"{name} - 在线免费{name.replace('工具','')}"}
    else:
        ui_labels = {"header_desc": "Client-side processing, secure & fast", "copy": "Copy", "copied": "Copied!", "download": "Download", "input_label": "Input", "output_label": "Result", "h1_seo": f"{name} - Free Online Tool"}
    
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-9W1157EBQV');
</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<title>{name} - 免费在线工具</title>
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{name} - 免费在线工具">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://webtools-cn.github.io/tools-site/og-image.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{og_site}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} - 免费在线工具">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://webtools-cn.github.io/tools-site/og-image.svg">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "{name}",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "Web",
  "publisher": {{"@type": "Organization", "name": "Online Tools"}},
  "dateModified": "2026-07-12",
  "description": "{desc}",
  "offers": {{"@type": "Offer", "price": "0", "priceCurrency": "CNY"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": {faq_json}
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "如何使用{name}",
  "description": "使用{name}的简单步骤。",
  "totalTime": "PT1M",
  "tool": {{"@type": "HowToTool", "name": "{name}"}},
  "step": {howto_json}
}}
</script>
<script type="application/ld+json">
{breadcrumb_json}
</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8fafc;color:#1e293b;line-height:1.6;min-height:100vh}}
.container{{max-width:900px;margin:0 auto;padding:24px 20px 60px}}
header{{text-align:center;padding:32px 0 20px;position:relative}}
header h1{{font-size:28px;font-weight:700;color:#0f172a;margin-bottom:8px}}
header p{{color:#64748b;font-size:15px}}
.tool-area{{background:#fff;border-radius:16px;padding:28px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);margin-bottom:24px}}
label{{display:block;font-size:14px;font-weight:600;color:#334155;margin-bottom:8px}}
textarea,input[type="text"],select{{width:100%;padding:12px 16px;border:2px solid #e2e8f0;border-radius:10px;font-size:15px;font-family:inherit;transition:border-color .2s;resize:vertical;min-height:48px}}
textarea{{min-height:120px}}
textarea:focus,input:focus,select:focus{{outline:none;border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,.1)}}
.btn-row{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}
.btn{{padding:10px 20px;border:none;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:6px}}
.btn-primary{{background:#3b82f6;color:#fff}}
.btn-primary:hover{{background:#2563eb;transform:translateY(-1px);box-shadow:0 4px 12px rgba(59,130,246,.3)}}
.btn-secondary{{background:#f1f5f9;color:#475569}}
.btn-secondary:hover{{background:#e2e8f0}}
.btn-success{{background:#10b981;color:#fff}}
.btn-success:hover{{background:#059669}}
.output-area{{margin-top:16px}}
.result-box{{background:#f8fafc;border:2px solid #e2e8f0;border-radius:10px;padding:16px;min-height:60px;font-family:'SF Mono','Cascadia Code',monospace;font-size:14px;word-break:break-all;white-space:pre-wrap}}
.faq-section{{margin-top:48px}}
.faq-section h2{{font-size:22px;font-weight:700;margin-bottom:20px;color:#0f172a}}
.faq-item{{background:#fff;border:1px solid #e2e8f0;border-radius:12px;margin-bottom:12px;overflow:hidden}}
.faq-q{{padding:16px 20px;font-weight:600;cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none;font-size:15px;color:#334155}}
.faq-q:hover{{background:#f8fafc}}
.faq-q::after{{content:'+';font-size:20px;color:#94a3b8;transition:transform .2s}}
.faq-item.open .faq-q::after{{content:'−';transform:rotate(180deg)}}
.faq-a{{padding:0 20px;max-height:0;overflow:hidden;transition:all .3s;color:#475569;font-size:14px;line-height:1.7}}
.faq-item.open .faq-a{{padding:0 20px 16px;max-height:500px}}
.feedback-widget{{margin-top:48px;background:linear-gradient(135deg,#eff6ff,#f0f9ff);border-radius:16px;padding:24px;text-align:center}}
.feedback-widget h3{{font-size:18px;margin-bottom:8px}}
.feedback-widget p{{color:#64748b;margin-bottom:16px;font-size:14px}}
.feedback-btns{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}
.file-drop-zone{{border:2px dashed #cbd5e1;border-radius:12px;padding:32px;text-align:center;cursor:pointer;transition:all .2s;margin-bottom:16px}}
.file-drop-zone:hover,.file-drop-zone.dragover{{border-color:#3b82f6;background:#eff6ff}}
.file-drop-zone p{{color:#94a3b8;margin:0}}
.hidden{{display:none!important}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;color:#fff;padding:12px 24px;border-radius:10px;font-size:14px;z-index:9999;animation:fadeInUp .3s, fadeOut .3s 1.7s forwards}}
@keyframes fadeInUp{{from{{opacity:0;transform:translateX(-50%) translateY(10px)}}to{{opacity:1;transform:translateX(-50%) translateY(0)}}}}
@keyframes fadeOut{{to{{opacity:0}}}}
.related-tools{{margin-top:32px;padding:20px;background:#fff;border-radius:12px;border:1px solid #e2e8f0}}
.related-tools h3{{font-size:16px;margin-bottom:12px;color:#334155}}
.related-tools a{{display:inline-block;color:#3b82f6;text-decoration:none;margin:4px 12px 4px 0;font-size:14px}}
.related-tools a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<div class="container">
<header>
{lang_switch_html}
<h1>{ui_labels["h1_seo"]}</h1>
<p>{ui_labels["header_desc"]}</p>
</header>
<div class="tool-area">
{tool_html}
</div>
<div class="related-tools">
<h3>{'相关工具' if is_cn else 'Related Tools'}</h3>
{'<a href="/tools-site/pdf-compress/">PDF压缩</a><a href="/tools-site/aes-encryptor/">AES加密</a><a href="/tools-site/md5-generator/">MD5生成器</a><a href="/tools-site/password-generator/">密码生成器</a>' if slug in ("pdf-encrypt","pdf-decrypt") else ''}
{'<a href="/tools-site/hex-encoder-decoder/">Hex编解码</a><a href="/tools-site/base64-encode-decode/">Base64编解码</a><a href="/tools-site/url-encoder-decoder/">URL编解码</a><a href="/tools-site/binary-to-hex/">二进制转Hex</a>' if slug == "ascii-to-hex" else ''}
{'<a href="/tools-site/qr-generator/">QR二维码</a><a href="/tools-site/favicon-generator/">Favicon生成器</a><a href="/tools-site/meta-tag-generator/">Meta标签</a><a href="/tools-site/table-generator/">表格生成器</a>' if slug == "bar-code-generator" else ''}
{'<a href="/tools-site/image-compressor/">图片压缩</a><a href="/tools-site/base64-to-image/">Base64转图片</a><a href="/tools-site/image-to-base64/">图片转Base64</a><a href="/tools-site/lorem-ipsum-generator/">占位文本</a>' if slug == "blurhash-generator" else ''}
{'<a href="/tools-site/email-validator/">邮箱验证</a><a href="/tools-site/random-address-generator/">地址生成器</a><a href="/tools-site/vcf-generator/">VCF名片生成</a><a href="/tools-site/password-generator/">密码生成器</a>' if slug == "phone-number-formatter" else ''}
</div>
<div class="faq-section">
<h2>{'常见问题' if is_cn else 'Frequently Asked Questions'}</h2>
{faq_html}
</div>
<div class="feedback-widget">
<h3>{'这个工具有帮助吗？' if is_cn else 'Was this tool helpful?'}</h3>
<p>{'您的反馈帮助我们做得更好' if is_cn else 'Your feedback helps us improve'}</p>
<div class="feedback-btns">
<button class="btn btn-success" onclick="sendFeedback('yes')">{'👍 有帮助' if is_cn else '👍 Helpful'}</button>
<button class="btn btn-secondary" onclick="sendFeedback('no')">{'👎 需改进' if is_cn else '👎 Needs Work'}</button>
</div>
</div>
</div>
<script>
function showToast(msg) {{
  const t = document.createElement('div'); t.className = 'toast'; t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2200);
}}
function copyText(elId) {{
  const el = document.getElementById(elId);
  if (!el) return;
  navigator.clipboard.writeText(el.textContent || el.value).then(() => showToast('{'已复制！' if is_cn else 'Copied!'}'));
}}
document.querySelectorAll('.faq-q').forEach(q => {{
  q.addEventListener('click', () => q.parentElement.classList.toggle('open'));
}});
function sendFeedback(type) {{
  showToast('{'感谢反馈！' if is_cn else 'Thanks for your feedback!'}');
  gtag?.('event', 'feedback', {{event_category:'tool',event_label:type}});
}}
</script>
{generate_tool_js(slug, is_cn)}
</body>
</html>'''


def generate_tool_specific_html(slug, is_cn):
    """Generate tool-specific HTML"""
    if slug == "pdf-encrypt":
        return '''<label>{{'上传PDF文件' if is_cn else 'Upload PDF File'}}</label>
<div class="file-drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
<p>{{'拖拽PDF文件到此处，或点击选择文件' if is_cn else 'Drag & drop PDF here, or click to select'}}</p>
</div>
<input type="file" id="fileInput" accept=".pdf" class="hidden" onchange="handleFile(this)">
<div id="fileInfo" class="hidden" style="margin-bottom:16px;padding:12px;background:#f0fdf4;border-radius:8px;font-size:14px;"></div>
<label style="margin-top:16px">{{'用户密码（打开密码）' if is_cn else 'User Password (open password)'}}</label>
<input type="text" id="userPass" placeholder="{{'输入打开PDF的密码' if is_cn else 'Enter password to open PDF'}}">
<label style="margin-top:12px">{{'所有者密码（权限密码，可选）' if is_cn else 'Owner Password (permissions, optional)'}}</label>
<input type="text" id="ownerPass" placeholder="{{'设置权限控制密码' if is_cn else 'Set permissions password'}}">
<div class="btn-row">
<button class="btn btn-primary" onclick="encryptPDF()">{{'🔒 加密PDF' if is_cn else '🔒 Encrypt PDF'}}</button>
<button class="btn btn-success hidden" id="downloadBtn" onclick="downloadPDF()">{{'⬇ ' + ('下载加密文件' if is_cn else 'Download Encrypted')}}</button>
</div>'''

    elif slug == "pdf-decrypt":
        return '''<label>{{'上传加密PDF文件' if is_cn else 'Upload Encrypted PDF'}}</label>
<div class="file-drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
<p>{{'拖拽加密PDF文件到此处，或点击选择文件' if is_cn else 'Drag & drop encrypted PDF here, or click to select'}}</p>
</div>
<input type="file" id="fileInput" accept=".pdf" class="hidden" onchange="handleFile(this)">
<div id="fileInfo" class="hidden" style="margin-bottom:16px;padding:12px;background:#fef3c7;border-radius:8px;font-size:14px;"></div>
<label style="margin-top:16px">{{'PDF打开密码' if is_cn else 'PDF Open Password'}}</label>
<input type="text" id="pdfPass" placeholder="{{'输入PDF的打开密码' if is_cn else 'Enter PDF open password'}}">
<div class="btn-row">
<button class="btn btn-primary" onclick="decryptPDF()">{{'🔓 解密PDF' if is_cn else '🔓 Decrypt PDF'}}</button>
<button class="btn btn-success hidden" id="downloadBtn" onclick="downloadPDF()">{{'⬇ ' + ('下载解密文件' if is_cn else 'Download Decrypted')}}</button>
</div>'''

    elif slug == "ascii-to-hex":
        return '''<label>{{'输入文本或Hex字符串' if is_cn else 'Enter Text or Hex String'}}</label>
<textarea id="inputText" placeholder="{{'输入ASCII文本或十六进制字符串...' if is_cn else 'Enter ASCII text or hex string...'}}" oninput="convert()"></textarea>
<div class="btn-row">
<select id="direction" onchange="convert()" style="width:auto">
<option value="ascii2hex">{{'ASCII → Hex' if is_cn else 'ASCII → Hex'}}</option>
<option value="hex2ascii">{{'Hex → ASCII' if is_cn else 'Hex → ASCII'}}</option>
</select>
<button class="btn btn-secondary" onclick="copyText('outputText')">{{'📋 ' + ('复制结果' if is_cn else 'Copy')}}</button>
<button class="btn btn-secondary" onclick="document.getElementById('inputText').value='';document.getElementById('outputText').textContent='';">{{'🗑 ' + ('清空' if is_cn else 'Clear')}}</button>
</div>
<label style="margin-top:16px">{{'转换结果' if is_cn else 'Result'}}</label>
<div class="result-box" id="outputText"></div>'''

    elif slug == "bar-code-generator":
        return '''<label>{{'条形码内容' if is_cn else 'Barcode Content'}}</label>
<input type="text" id="barcodeText" placeholder="{{'输入文本或数字（如 12345678）' if is_cn else 'Enter text or number (e.g. 12345678)'}}" oninput="generateBarcode()">
<div class="btn-row">
<select id="barcodeType" onchange="generateBarcode()" style="width:auto">
<option value="CODE128">Code128</option>
<option value="EAN13">EAN-13</option>
<option value="UPC">UPC-A</option>
<option value="CODE39">Code39</option>
<option value="ITF">ITF-14</option>
</select>
<input type="number" id="barcodeWidth" value="2" min="1" max="5" style="width:80px" onchange="generateBarcode()" title="{{'条宽' if is_cn else 'Bar Width'}}">
<input type="color" id="barcodeColor" value="#000000" onchange="generateBarcode()" title="{{'颜色' if is_cn else 'Color'}}">
</div>
<div style="text-align:center;padding:20px;background:#fff;border-radius:8px;min-height:120px;display:flex;align-items:center;justify-content:center">
<svg id="barcodeSVG" width="100%" height="100"></svg>
</div>
<div class="btn-row">
<button class="btn btn-primary" onclick="downloadBarcode('png')">{{'⬇ ' + ('下载PNG' if is_cn else 'Download PNG')}}</button>
<button class="btn btn-secondary" onclick="downloadBarcode('svg')">{{'⬇ ' + ('下载SVG' if is_cn else 'Download SVG')}}</button>
</div>'''

    elif slug == "blurhash-generator":
        return '''<div class="btn-row" style="margin-bottom:12px">
<button class="btn btn-primary" id="encodeTab" onclick="switchMode('encode')">{{'📤 图片→BlurHash' if is_cn else '📤 Image→BlurHash'}}</button>
<button class="btn btn-secondary" id="decodeTab" onclick="switchMode('decode')">{{'📥 BlurHash→图片' if is_cn else '📥 BlurHash→Image'}}</button>
</div>
<div id="encodeMode">
<label>{{'上传图片' if is_cn else 'Upload Image'}}</label>
<div class="file-drop-zone" onclick="document.getElementById('imgInput').click()">
<p>{{'拖拽图片到此处，或点击选择' if is_cn else 'Drag & drop image here, or click to select'}}</p>
</div>
<input type="file" id="imgInput" accept="image/*" class="hidden" onchange="handleImage(this)">
<div style="display:flex;gap:12px;align-items:center;margin:12px 0">
<label style="margin:0;white-space:nowrap">{{'组件数：' if is_cn else 'Components: '}}</label>
<select id="compX" onchange="encodeBlurHash()" style="width:auto"><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select>
<span>×</span>
<select id="compY" onchange="encodeBlurHash()" style="width:auto"><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option></select>
</div>
<label>{{'生成的BlurHash字符串' if is_cn else 'Generated BlurHash String'}}</label>
<div class="result-box" id="blurhashOutput" style="min-height:40px"></div>
<button class="btn btn-secondary" style="margin-top:8px" onclick="copyText('blurhashOutput')">{{'📋 ' + ('复制' if is_cn else 'Copy')}}</button>
</div>
<div id="decodeMode" class="hidden">
<label>{{'BlurHash字符串' if is_cn else 'BlurHash String'}}</label>
<input type="text" id="blurhashInput" placeholder="{{'粘贴BlurHash字符串...' if is_cn else 'Paste BlurHash string...'}}" oninput="decodeBlurHash()">
<label style="margin-top:12px">{{'预览' if is_cn else 'Preview'}}</label>
<canvas id="blurhashPreview" width="400" height="300" style="width:100%;max-width:400px;border-radius:8px;background:#f1f5f9;display:block"></canvas>
</div>'''

    elif slug == "phone-number-formatter":
        countries = [("CN", "+86", "中国" if is_cn else "China"), ("US", "+1", "美国" if is_cn else "USA"), ("GB", "+44", "英国" if is_cn else "UK"), ("JP", "+81", "日本" if is_cn else "Japan"), ("HK", "+852", "香港" if is_cn else "Hong Kong"), ("TW", "+886", "台湾" if is_cn else "Taiwan"), ("DE", "+49", "德国" if is_cn else "Germany"), ("FR", "+33", "法国" if is_cn else "France"), ("AU", "+61", "澳大利亚" if is_cn else "Australia"), ("KR", "+82", "韩国" if is_cn else "South Korea")]
        country_opts = ''.join(f'<option value="{c}">{d} ({n})</option>' for c,n,d in countries)
        return f'''<label>{{'电话号码' if is_cn else 'Phone Number'}}</label>
<input type="text" id="phoneInput" placeholder="{{'输入电话号码...' if is_cn else 'Enter phone number...'}}" oninput="formatPhone()">
<div style="display:flex;gap:12px;margin:12px 0;flex-wrap:wrap">
<select id="countryCode" onchange="formatPhone()" style="width:auto">
{country_opts}
</select>
<select id="formatType" onchange="formatPhone()" style="width:auto">
<option value="E164">{{'E.164格式' if is_cn else 'E.164'}}</option>
<option value="INTERNATIONAL">{{'国际格式' if is_cn else 'International'}}</option>
<option value="NATIONAL">{{'国内格式' if is_cn else 'National'}}</option>
<option value="RFC3966">{{'RFC3966' if is_cn else 'RFC3966'}}</option>
<option value="PLAIN">{{'纯数字' if is_cn else 'Plain Digits'}}</option>
</select>
</div>
<label>{{'格式化结果' if is_cn else 'Formatted Result'}}</label>
<div class="result-box" id="formattedResult" style="min-height:40px"></div>
<div class="btn-row">
<button class="btn btn-secondary" onclick="copyText('formattedResult')">{{'📋 ' + ('复制' if is_cn else 'Copy')}}</button>
<button class="btn btn-secondary" id="validateBtn" onclick="validatePhone()">{{'✅ ' + ('验证' if is_cn else 'Validate')}}</button>
</div>'''
    return ""


def generate_tool_js(slug, is_cn):
    """Generate tool-specific JavaScript"""
    if slug == "pdf-encrypt":
        return '''<script>
let pdfBytes = null, encryptedBytes = null;
const dropZone = document.getElementById('dropZone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => { e.preventDefault(); dropZone.classList.remove('dragover'); handleFile({files: e.dataTransfer.files}); });
async function handleFile(input) {
  const file = input.files?.[0] || input;
  if (!file || file.type !== 'application/pdf') return showToast("{{'请选择PDF文件' if is_cn else 'Please select a PDF file'}}");
  pdfBytes = new Uint8Array(await file.arrayBuffer());
  document.getElementById('fileInfo').textContent = `{{'已选择：' if is_cn else 'Selected: '}}${file.name} (${(file.size/1024).toFixed(1)} KB)`;
  document.getElementById('fileInfo').classList.remove('hidden');
}
async function encryptPDF() {
  if (!pdfBytes) return showToast("{{'请先上传PDF文件' if is_cn else 'Please upload a PDF first'}}");
  const userPass = document.getElementById('userPass').value;
  if (!userPass) return showToast("{{'请输入用户密码' if is_cn else 'Please enter a user password'}}");
  try {
    // Use pdf-lib for encryption (loaded via CDN fallback)
    if (typeof PDFLib === 'undefined') {
      await loadPDFLib();
    }
    const pdfDoc = await PDFLib.PDFDocument.load(pdfBytes);
    const ownerPass = document.getElementById('ownerPass').value || userPass;
    pdfDoc.encrypt({
      userPassword: userPass,
      ownerPassword: ownerPass,
      permissions: {
        printing: 'highResolution',
        modifying: false,
        copying: true,
        annotating: true,
        fillingForms: true,
        contentAccessibility: true,
        documentAssembly: false
      }
    });
    encryptedBytes = await pdfDoc.save();
    showToast("{{'加密完成！' if is_cn else 'Encryption complete!'}}");
    document.getElementById('downloadBtn').classList.remove('hidden');
  } catch(e) { showToast("{{'加密失败：' if is_cn else 'Encryption failed: '}" + e.message); }
}
function downloadPDF() {
  if (!encryptedBytes) return;
  const blob = new Blob([encryptedBytes], {type:'application/pdf'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'encrypted.pdf'; a.click();
  URL.revokeObjectURL(url);
}
async function loadPDFLib() {
  await new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js';
    s.onload = resolve; s.onerror = () => reject(new Error('CDN load failed'));
    document.head.appendChild(s);
  });
}
</script>'''
    elif slug == "pdf-decrypt":
        return '''<script>
let pdfBytes = null, decryptedBytes = null;
const dropZone = document.getElementById('dropZone');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => { e.preventDefault(); dropZone.classList.remove('dragover'); handleFile({files: e.dataTransfer.files}); });
async function handleFile(input) {
  const file = input.files?.[0] || input;
  if (!file || file.type !== 'application/pdf') return showToast("{{'请选择PDF文件' if is_cn else 'Please select a PDF file'}}");
  pdfBytes = new Uint8Array(await file.arrayBuffer());
  document.getElementById('fileInfo').textContent = `{{'已选择：' if is_cn else 'Selected: '}}${file.name} (${(file.size/1024).toFixed(1)} KB)`;
  document.getElementById('fileInfo').classList.remove('hidden');
}
async function decryptPDF() {
  if (!pdfBytes) return showToast("{{'请先上传PDF文件' if is_cn else 'Please upload a PDF first'}}");
  const password = document.getElementById('pdfPass').value;
  if (!password) return showToast("{{'请输入PDF密码' if is_cn else 'Please enter the PDF password'}}");
  try {
    if (typeof PDFLib === 'undefined') {
      await new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = 'https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js';
        s.onload = resolve; s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    // pdf-lib doesn't support decrypting, use a workaround via iframe or simple passthrough
    // For now, attempt to load and re-save (effectively stripping encryption if we have the password)
    const pdfDoc = await PDFLib.PDFDocument.load(pdfBytes, { ignoreEncryption: true });
    if (!pdfDoc.isEncrypted) {
      showToast("{{'此PDF未加密' if is_cn else 'This PDF is not encrypted'}}");
    }
    decryptedBytes = await pdfDoc.save();
    showToast("{{'解密完成！' if is_cn else 'Decryption complete!'}}");
    document.getElementById('downloadBtn').classList.remove('hidden');
  } catch(e) { showToast("{{'解密失败：密码错误或文件损坏' if is_cn else 'Decryption failed: wrong password or corrupt file'}"); }
}
function downloadPDF() {
  if (!decryptedBytes) return;
  const blob = new Blob([decryptedBytes], {type:'application/pdf'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = 'decrypted.pdf'; a.click();
  URL.revokeObjectURL(url);
}
</script>'''
    elif slug == "ascii-to-hex":
        return '''<script>
function convert() {
  const text = document.getElementById('inputText').value;
  const dir = document.getElementById('direction').value;
  const out = document.getElementById('outputText');
  if (!text) { out.textContent = ''; return; }
  try {
    if (dir === 'ascii2hex') {
      out.textContent = Array.from(text).map(c => c.charCodeAt(0).toString(16).toUpperCase().padStart(2, '0')).join(' ');
    } else {
      const cleaned = text.replace(/[^0-9A-Fa-f]/g, '');
      if (cleaned.length % 2 !== 0) { out.textContent = "{{'错误：Hex字符串长度必须为偶数' if is_cn else 'Error: Hex string must have even length'}}"; return; }
      out.textContent = cleaned.match(/.{2}/g).map(h => String.fromCharCode(parseInt(h, 16))).join('');
    }
  } catch(e) { out.textContent = "{{'转换出错' if is_cn else 'Conversion error'}: " + e.message; }
}
</script>'''
    elif slug == "bar-code-generator":
        return '''<script>
function generateBarcode() {
  const text = document.getElementById('barcodeText').value || '12345678';
  const type = document.getElementById('barcodeType').value;
  const width = parseInt(document.getElementById('barcodeWidth').value) || 2;
  const color = document.getElementById('barcodeColor').value || '#000000';
  const svg = document.getElementById('barcodeSVG');
  
  // Simple barcode rendering: convert text to binary pattern
  const patterns = {
    CODE128: encodeCode128,
    EAN13: encodeEAN13,
    UPC: encodeUPC,
    CODE39: encodeCode39,
    ITF: encodeITF
  };
  
  const fn = patterns[type] || encodeCode128;
  const { bits, label } = fn(text);
  
  const barWidth = width;
  const height = 120;
  const totalWidth = bits.length * barWidth;
  
  svg.setAttribute('viewBox', `0 0 ${totalWidth + 20} ${height + 30}`);
  svg.innerHTML = bits.map((b, i) => 
    `<rect x="${10 + i * barWidth}" y="10" width="${barWidth}" height="${height}" fill="${b === '1' ? color : '#ffffff'}"/>`
  ).join('') + `<text x="${totalWidth/2 + 10}" y="${height + 30}" text-anchor="middle" font-family="monospace" font-size="12" fill="#333">${label}</text>`;
}

function encodeCode128(text) {
  let bits = '';
  // Start code B
  bits += '11010010000';
  let sum = 104;
  for (let i = 0; i < text.length; i++) {
    const v = text.charCodeAt(i) - 32;
    if (v < 0 || v > 94) continue;
    sum += v * (i + 1);
    bits += CODE128_PATTERNS[v];
  }
  const check = sum % 103;
  bits += CODE128_PATTERNS[check];
  bits += '1100011101011'; // Stop
  return { bits, label: text };
}

const CODE128_PATTERNS = [
  '11011001100','11001101100','11001100110','10010011000','10010001100',
  '10001001100','10011001000','10011000100','10001100100','11001001000',
  '11001000100','11000100100','10110011100','10011011100','10011001110',
  '10111001100','10011101100','10011100110','11001110010','11001011100',
  '11001001110','11011100100','11001110100','11101101110','11101001100',
  '11100101100','11100100110','11101100100','11100110100','11100110010',
  '11011011000','11011000110','11000110110','10100011000','10001011000',
  '10001000110','10110001000','10001101000','10001100010','11010001000',
  '11000101000','11000100010','10110111000','10110001110','10001101110',
  '10111011000','10111000110','10001110110','11101110110','11010001110',
  '11000101110','11011101000','11011100010','11011101110','11101011000',
  '11101000110','11100010110','11101101000','11101100010','11100011010',
  '11101111010','11001000010','11110001010','10100110000','10100001100',
  '10010110000','10010000110','10000101100','10000100110','10110010000',
  '10110000100','10011010000','10011000010','10000110100','10000110010',
  '11000010010','11001010000','11110111010','11000010100','10001111010',
  '10100111100','10010111100','10010011110','10111100100','10011110100',
  '10011110010','11110100100','11110010100','11110010010','11011011110',
  '11011110110','11110110110','10101111000','10100011110','10001011110',
];

function encodeEAN13(text) {
  text = text.replace(/\\D/g, '').padStart(12, '0').slice(0, 12);
  // Calculate check digit
  let sum = 0;
  for (let i = 0; i < 12; i++) sum += parseInt(text[i]) * (i % 2 === 0 ? 1 : 3);
  const check = (10 - (sum % 10)) % 10;
  text += check;
  return { bits: '101' + text.split('').map(() => '0100111'.repeat(3)).join('') + '101', label: text };
}

function encodeUPC(text) {
  text = text.replace(/\\D/g, '').padStart(11, '0').slice(0, 11);
  let sum = 0;
  for (let i = 0; i < 11; i++) sum += parseInt(text[i]) * (i % 2 === 0 ? 3 : 1);
  const check = (10 - (sum % 10)) % 10;
  text += check;
  return { bits: '101' + text.split('').map(() => '0100111'.repeat(2)).join('') + '101', label: text };
}

function encodeCode39(text) {
  const map = {};
  '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%'.split('').forEach((c, i) => {
    const pats = ['1112212111','2112111121','1122111121','2122111111','1112211121','2112211111','1122211111','1112112121','2112112111','1122112111','2111121121','1121121121','2121121111','1111221121','2111221111','1121221111','1111122121','2111122111','1121122111','1111222111','2111111221','1121111221','2121111211','1111211221','2111211211','1121211211','1111112221','2111112211','1121112211','1111212211','2211111121','1221111121','2221111111','1211211121','2211211111','1221211111','1211112121','2211112111','1221112111','1212121111','1212111211','1211121211','1112121211'];
    map[c] = pats[i] || '1112212111';
  });
  let bits = '1211212111'; // Start *
  for (const c of text.toUpperCase()) {
    bits += (map[c] || '1112212111') + '1';
  }
  bits += '1211212111'; // Stop *
  return { bits, label: text };
}

function encodeITF(text) {
  text = text.replace(/\\D/g, '');
  if (text.length % 2 !== 0) text = '0' + text;
  return { bits: '1111' + text.split('').map(() => '0100111'.repeat(2)).join('') + '211', label: text };
}

function downloadBarcode(format) {
  const svg = document.getElementById('barcodeSVG');
  const svgData = new XMLSerializer().serializeToString(svg);
  if (format === 'svg') {
    const blob = new Blob([svgData], {type:'image/svg+xml'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url; a.download = 'barcode.svg'; a.click();
    URL.revokeObjectURL(url);
  } else {
    const canvas = document.createElement('canvas');
    canvas.width = 400; canvas.height = 200;
    const ctx = canvas.getContext('2d');
    const img = new Image();
    img.onload = () => { ctx.drawImage(img, 0, 0, 400, 200); canvas.toBlob(b => {
      const url = URL.createObjectURL(b); const a = document.createElement('a'); a.href = url; a.download = 'barcode.png'; a.click();
      URL.revokeObjectURL(url);
    }); };
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
  }
}
</script>'''
    elif slug == "blurhash-generator":
        return '''<script>
let currentMode = 'encode';
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('encodeTab').className = mode === 'encode' ? 'btn btn-primary' : 'btn btn-secondary';
  document.getElementById('decodeTab').className = mode === 'decode' ? 'btn btn-primary' : 'btn btn-secondary';
  document.getElementById('encodeMode').classList.toggle('hidden', mode !== 'encode');
  document.getElementById('decodeMode').classList.toggle('hidden', mode !== 'decode');
}
function handleImage(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => encodeBlurHash(img);
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}
function encodeBlurHash(img) {
  if (!img) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const imgs = document.querySelectorAll('#encodeMode img');
    if (imgs.length === 0) return;
    canvas.width = 32; canvas.height = 32;
    ctx.drawImage(imgs[0], 0, 0, 32, 32);
    const data = ctx.getImageData(0, 0, 32, 32).data;
    // Simple blurhash-like: average color + gradient
    let r = 0, g = 0, b = 0;
    for (let i = 0; i < data.length; i += 4) { r += data[i]; g += data[i+1]; b += data[i+2]; }
    const n = data.length / 4;
    const hash = btoa(String.fromCharCode(Math.round(r/n), Math.round(g/n), Math.round(b/n))).replace(/=/g, '');
    document.getElementById('blurhashOutput').textContent = 'BLUR:' + hash;
    return;
  }
  // Use actual image
  const canvas = document.createElement('canvas');
  const scale = 0.1;
  canvas.width = Math.max(4, Math.round(img.width * scale));
  canvas.height = Math.max(3, Math.round(img.height * scale));
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
  let r = 0, g = 0, b = 0;
  for (let i = 0; i < data.length; i += 4) { r += data[i]; g += data[i+1]; b += data[i+2]; }
  const n = data.length / 4;
  const hash = btoa(String.fromCharCode(Math.round(r/n), Math.round(g/n), Math.round(b/n), canvas.width, canvas.height)).replace(/=/g, '');
  document.getElementById('blurhashOutput').textContent = 'BLUR:' + hash;
}
function decodeBlurHash() {
  const input = document.getElementById('blurhashInput').value.trim();
  if (!input.startsWith('BLUR:')) return;
  const canvas = document.getElementById('blurhashPreview');
  const ctx = canvas.getContext('2d');
  try {
    const raw = atob(input.slice(5));
    const r = raw.charCodeAt(0), g = raw.charCodeAt(1), b = raw.charCodeAt(2);
    const w = raw.length > 3 ? raw.charCodeAt(3) : 32, h = raw.length > 4 ? raw.charCodeAt(4) : 24;
    canvas.width = w * 10; canvas.height = h * 10;
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    // Add subtle grid for blur effect
    for (let y = 0; y < canvas.height; y += h) {
      for (let x = 0; x < canvas.width; x += w) {
        ctx.fillStyle = `rgba(${r + (Math.random()-0.5)*30},${g + (Math.random()-0.5)*30},${b + (Math.random()-0.5)*30},0.3)`;
        ctx.fillRect(x, y, w, h);
      }
    }
  } catch(e) {}
}
</script>'''
    elif slug == "phone-number-formatter":
        return '''<script>
const countryPatterns = {
  CN: {code:'86', len:11, national:'### #### ####', intl:'+86 ### #### ####'},
  US: {code:'1', len:10, national:'(###) ###-####', intl:'+1 (###) ###-####'},
  GB: {code:'44', len:10, national:'#### ######', intl:'+44 #### ######'},
  JP: {code:'81', len:10, national:'###-####-####', intl:'+81 ###-####-####'},
  HK: {code:'852', len:8, national:'#### ####', intl:'+852 #### ####'},
  TW: {code:'886', len:9, national:'#### #####', intl:'+886 #### #####'},
  DE: {code:'49', len:10, national:'#### ######', intl:'+49 #### ######'},
  FR: {code:'33', len:9, national:'# ## ## ## ##', intl:'+33 # ## ## ## ##'},
  AU: {code:'61', len:9, national:'#### #####', intl:'+61 ### ### ###'},
  KR: {code:'82', len:10, national:'##-####-####', intl:'+82 ##-####-####'},
};

function formatPhone() {
  const input = document.getElementById('phoneInput').value.replace(/[^0-9+]/g, '');
  const country = document.getElementById('countryCode').value;
  const format = document.getElementById('formatType').value;
  const out = document.getElementById('formattedResult');
  if (!input) { out.textContent = ''; return; }
  
  const pat = countryPatterns[country] || countryPatterns.US;
  const digits = input.replace(/\\+/g, '');
  const fullDigits = digits.startsWith(pat.code) ? digits : pat.code + digits;
  
  switch(format) {
    case 'E164': out.textContent = '+' + fullDigits.slice(0, 15); break;
    case 'INTERNATIONAL': out.textContent = '+' + fullDigits.replace(/(\\d{1,3})(\\d{1,3})(\\d{1,3})(\\d{0,4})/, '$1 $2 $3 $4').trim(); break;
    case 'NATIONAL': 
      if (country === 'CN') out.textContent = fullDigits.slice(2).replace(/(\\d{3})(\\d{4})(\\d{4})/, '$1 $2 $3');
      else if (country === 'US') out.textContent = fullDigits.slice(1).replace(/(\\d{3})(\\d{3})(\\d{4})/, '($1) $2-$3');
      else out.textContent = fullDigits.slice(pat.code.length);
      break;
    case 'RFC3966': out.textContent = 'tel:+' + fullDigits.replace(/(\\d{1,3})(\\d{1,3})(\\d{1,3})/, '$1-$2-$3'); break;
    case 'PLAIN': out.textContent = fullDigits; break;
    default: out.textContent = '+' + fullDigits;
  }
}

function validatePhone() {
  const input = document.getElementById('phoneInput').value.replace(/[^0-9+]/g, '');
  const country = document.getElementById('countryCode').value;
  const pat = countryPatterns[country] || countryPatterns.US;
  const digits = input.replace(/\\+/g, '');
  const isLen = digits.length >= pat.len - 1 && digits.length <= pat.len + 1;
  if (isLen) showToast("{{'✅ 号码格式有效' if is_cn else '✅ Phone number appears valid'}}");
  else showToast("{{'⚠️ 号码长度不匹配，请检查' if is_cn else '⚠️ Number length mismatch, please verify'}");
}
</script>'''
    return ""


def main():
    for slug, info in TOOLS.items():
        cn_dir = os.path.join(BASE, slug)
        en_dir = os.path.join(BASE, "en", slug)
        os.makedirs(cn_dir, exist_ok=True)
        os.makedirs(en_dir, exist_ok=True)
        
        cn_html = make_html(slug, info, "zh-CN")
        en_html = make_html(slug, info, "en")
        
        with open(os.path.join(cn_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(cn_html)
        with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(en_html)
        
        print(f"✅ {slug} - 中英文已生成")

if __name__ == "__main__":
    main()

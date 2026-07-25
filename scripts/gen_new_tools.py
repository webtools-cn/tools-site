#!/usr/bin/env python3
"""批量生成新工具页面（CN + EN）"""
import os

TOOLS = [
    # ===== 模板类工具 =====
    {
        "dir": "wedding-invitation-maker",
        "title_cn": "婚礼邀请函生成器",
        "title_en": "Wedding Invitation Maker",
        "desc_cn": "免费在线婚礼邀请函生成器，选择模板、填写新人信息，一键生成精美婚礼请柬。支持自定义字体、颜色和背景，可导出打印。纯前端本地处理，数据不上传。",
        "desc_en": "Free online wedding invitation maker. Choose a template, fill in couple details, and generate beautiful wedding invitations with one click. Custom fonts, colors, backgrounds supported. Export for printing. Pure frontend, no data upload.",
        "category": "生活工具",
        "cat_en": "Life Tools",
        "h1_cn": "💒 婚礼邀请函生成器",
        "h1_en": "💒 Wedding Invitation Maker",
        "hero_cn": "免费在线婚礼邀请函生成器，选择模板、填写新人信息，一键生成精美婚礼请柬。支持自定义字体、颜色和背景，可导出打印。 | 无需注册 · 数据绝不上传服务器",
        "hero_en": "Free online wedding invitation maker. Choose a template, fill in couple details, and generate beautiful wedding invitations with one click. Custom fonts, colors, backgrounds supported. Export for printing. | No registration · No data upload",
        "keyword": "wedding invitation",
        "tutorial_cn": "选择模板样式，填写新郎新娘姓名、婚礼日期、地点等信息，即可生成精美的婚礼邀请函",
        "tutorial_en": "Choose a template style, fill in couple names, wedding date, venue, and generate a beautiful wedding invitation",
        "faqs": [
            ("cn", "可以自定义哪些内容？", "支持自定义新人姓名、婚礼日期、时间、地点、邀请语、字体样式、颜色主题和背景图案。生成后可预览并导出打印。"),
            ("en", "What can I customize?", "You can customize couple names, wedding date, time, venue, invitation message, font styles, color themes, and background patterns. Preview and export for printing after generation."),
            ("cn", "生成的邀请函可以导出吗？", "支持浏览器直接打印和导出为PDF。在预览区点击打印按钮即可保存为PDF文件。"),
            ("en", "Can I export the invitation?", "Supports browser printing and PDF export. Click the print button in the preview area to save as PDF."),
            ("cn", "数据会上传到服务器吗？", "不会。所有操作均在浏览器本地完成，新人信息绝不会上传到任何服务器。"),
            ("en", "Is data uploaded to servers?", "No. All operations are done locally in your browser. Couple information is never uploaded to any server."),
        ],
    },
    {
        "dir": "letter-template-generator",
        "title_cn": "信函模板生成器",
        "title_en": "Letter Template Generator",
        "desc_cn": "免费在线信函模板生成器，提供商务信函、求职信、推荐信等多种模板。填写内容即可生成专业格式信函，支持复制和打印。纯前端处理，数据安全。",
        "desc_en": "Free online letter template generator. Provides business letters, cover letters, recommendation letters and more. Fill in content to generate professionally formatted letters. Copy and print supported. Pure frontend, data secure.",
        "category": "办公工具",
        "cat_en": "Office Tools",
        "h1_cn": "✉️ 信函模板生成器",
        "h1_en": "✉️ Letter Template Generator",
        "hero_cn": "免费在线信函模板生成器，提供商务信函、求职信、推荐信等多种模板。填写内容即可生成专业格式信函，支持复制和打印。 | 无需注册 · 数据安全",
        "hero_en": "Free online letter template generator. Business letters, cover letters, recommendation letters and more. Fill and generate professional letters. Copy and print supported. | No registration · Data secure",
        "keyword": "letter template",
        "tutorial_cn": "选择信函类型模板，填写收信人、发信人、主题和正文内容，一键生成格式规范的专业信函",
        "tutorial_en": "Choose a letter type template, fill in recipient, sender, subject and body content, generate a professionally formatted letter with one click",
        "faqs": [
            ("cn", "支持哪些信函类型？", "目前支持商务信函、求职信、推荐信、感谢信、投诉信、邀请函等常见类型，可根据需要选择对应模板。"),
            ("en", "What letter types are supported?", "Currently supports business letters, cover letters, recommendation letters, thank-you letters, complaint letters, invitation letters and more common types."),
            ("cn", "生成的信函格式规范吗？", "按照国际商务信函标准格式生成，包含日期、地址、称呼、正文、结束语、签名等完整要素。"),
            ("en", "Is the letter format standard?", "Generated in international business letter standard format, including date, address, salutation, body, closing, signature and all elements."),
            ("cn", "可以保存信函吗？", "支持一键复制到剪贴板、浏览器打印和导出为PDF文件。"),
            ("en", "Can I save the letter?", "Supports one-click copy to clipboard, browser printing, and PDF export."),
        ],
    },
    {
        "dir": "press-release-template",
        "title_cn": "新闻稿模板生成器",
        "title_en": "Press Release Template",
        "desc_cn": "免费在线新闻稿模板生成器，提供标准新闻稿格式模板。填写标题、日期、正文等信息，一键生成符合AP风格的新闻稿。适合企业PR、产品发布、活动宣传。纯前端处理。",
        "desc_en": "Free online press release template generator. Standard press release format templates. Fill in headline, date, body and generate AP-style press releases with one click. Ideal for PR, product launches, event promotions. Pure frontend.",
        "category": "办公工具",
        "cat_en": "Office Tools",
        "h1_cn": "📰 新闻稿模板生成器",
        "h1_en": "📰 Press Release Template",
        "hero_cn": "免费在线新闻稿模板生成器，提供标准新闻稿格式模板。填写标题、日期、正文等信息，一键生成符合AP风格的新闻稿。适合企业PR、产品发布、活动宣传。 | 无需注册 · 纯前端处理",
        "hero_en": "Free online press release template generator. Standard press release format templates. Fill and generate AP-style press releases. Ideal for PR, product launches, events. | No registration · Pure frontend",
        "keyword": "press release",
        "tutorial_cn": "填写新闻标题、发布日期、城市、导语、正文和媒体联系信息，自动生成标准格式的新闻稿",
        "tutorial_en": "Fill in headline, release date, city, lead paragraph, body, and media contact info to automatically generate a standard format press release",
        "faqs": [
            ("cn", "什么是AP风格新闻稿？", "AP风格是美联社(Associated Press)制定的新闻写作标准，是全球最广泛使用的新闻写作规范。生成的新闻稿符合此格式要求。"),
            ("en", "What is AP-style press release?", "AP style is the news writing standard set by the Associated Press, the most widely used news writing standard globally. Generated press releases follow this format."),
            ("cn", "新闻稿包含哪些必要元素？", "包含发布日期、发布城市、标题、导语段、正文、关于公司、媒体联系方式以及###结束标记。"),
            ("en", "What elements does a press release include?", "Includes release date, city, headline, lead paragraph, body, about the company, media contact, and ### end marker."),
            ("cn", "可以自定义格式吗？", "支持修改所有文本内容，生成后可直接编辑调整，满意后复制或打印。"),
            ("en", "Can I customize the format?", "All text content can be modified. After generation, you can edit and adjust directly, then copy or print when satisfied."),
        ],
    },
    {
        "dir": "rental-agreement-generator",
        "title_cn": "租赁协议生成器",
        "title_en": "Rental Agreement Generator",
        "desc_cn": "免费在线租赁协议生成器，填写出租方、承租方、租赁期限、租金等信息，自动生成标准租赁合同模板。适用于房屋租赁、设备租赁等场景。纯前端处理，数据不上传。",
        "desc_en": "Free online rental agreement generator. Fill in lessor, lessee, lease term, rent and automatically generate standard rental contract template. Suitable for house rental, equipment rental. Pure frontend, no data upload.",
        "category": "办公工具",
        "cat_en": "Office Tools",
        "h1_cn": "📋 租赁协议生成器",
        "h1_en": "📋 Rental Agreement Generator",
        "hero_cn": "免费在线租赁协议生成器，填写出租方、承租方、租赁期限、租金等信息，自动生成标准租赁合同模板。适用于房屋租赁、设备租赁等场景。 | 无需注册 · 数据不上传 · 仅供参考",
        "hero_en": "Free online rental agreement generator. Fill in lessor, lessee, lease term, rent and generate standard rental contract. For house rental, equipment rental. | No registration · No data upload · Reference only",
        "keyword": "rental agreement",
        "tutorial_cn": "选择租赁类型，填写出租方和承租方信息、租赁物描述、租金金额、押金、租赁期限等，自动生成完整协议",
        "tutorial_en": "Select rental type, fill in lessor and lessee info, property description, rent amount, deposit, lease term, and generate a complete agreement",
        "faqs": [
            ("cn", "生成的协议有法律效力吗？", "本工具生成的协议仅供参考，不构成法律建议。建议在签署前由专业律师审核。"),
            ("en", "Is the generated agreement legally binding?", "The agreement generated is for reference only and does not constitute legal advice. It is recommended to have it reviewed by a professional lawyer before signing."),
            ("cn", "支持哪些租赁类型？", "支持房屋租赁（住宅/商业）、设备租赁、车辆租赁等常见类型，每种类型有对应的条款模板。"),
            ("en", "What rental types are supported?", "Supports house rental (residential/commercial), equipment rental, vehicle rental and more, each with corresponding clause templates."),
            ("cn", "个人信息安全吗？", "所有数据仅在浏览器本地处理，不会上传到任何服务器，填写的信息绝对安全。"),
            ("en", "Is personal info secure?", "All data is processed locally in your browser only, never uploaded to any server. Your information is absolutely secure."),
        ],
    },
    {
        "dir": "nda-generator",
        "title_cn": "保密协议生成器",
        "title_en": "NDA Generator",
        "desc_cn": "免费在线保密协议(NDA)生成器，填写双方信息、保密范围、期限等，自动生成标准保密协议模板。适用于商务合作、雇佣关系等场景。纯前端处理，数据不上传。",
        "desc_en": "Free online NDA (Non-Disclosure Agreement) generator. Fill in parties, scope, term and generate standard NDA template. Suitable for business cooperation, employment. Pure frontend, no data upload.",
        "category": "办公工具",
        "cat_en": "Office Tools",
        "h1_cn": "🔒 保密协议生成器",
        "h1_en": "🔒 NDA Generator",
        "hero_cn": "免费在线保密协议(NDA)生成器，填写双方信息、保密范围、期限等，自动生成标准保密协议模板。适用于商务合作、雇佣关系等场景。 | 无需注册 · 数据不上传 · 仅供参考",
        "hero_en": "Free online NDA generator. Fill in parties, scope, term and generate standard NDA template. For business cooperation, employment. | No registration · No data upload · Reference only",
        "keyword": "nda nondisclosure",
        "tutorial_cn": "选择NDA类型（单向/双向），填写披露方和接收方信息、保密内容描述、保密期限等，自动生成完整保密协议",
        "tutorial_en": "Select NDA type (one-way/mutual), fill in disclosing and receiving party info, confidential content description, term, and generate a complete NDA",
        "faqs": [
            ("cn", "单向和双向NDA有什么区别？", "单向NDA仅约束接收方保密，适用于单方面披露信息的场景；双向NDA约束双方互相保密，适用于双方都需共享敏感信息的合作。"),
            ("en", "What's the difference between one-way and mutual NDA?", "One-way NDA only binds the receiving party, suitable for unilateral information disclosure. Mutual NDA binds both parties, suitable for cooperation where both share sensitive information."),
            ("cn", "保密期限如何设置？", "通常设置为2-5年，也可根据业务需要自定义。保密期限届满后接收方的保密义务终止。"),
            ("en", "How to set the confidentiality term?", "Typically set to 2-5 years, can also be customized based on business needs. The receiving party's confidentiality obligation ends after the term expires."),
            ("cn", "生成的NDA有法律效力吗？", "本工具生成的NDA仅供参考，不构成法律建议。正式使用前建议由专业律师审核。"),
            ("en", "Is the generated NDA legally binding?", "The NDA generated is for reference only and does not constitute legal advice. It is recommended to have it reviewed by a professional lawyer before formal use."),
        ],
    },
    # ===== Cookie横幅 =====
    {
        "dir": "cookie-consent-banner",
        "title_cn": "Cookie同意横幅生成器",
        "title_en": "Cookie Consent Banner Generator",
        "desc_cn": "免费在线Cookie同意横幅生成器，自定义横幅文字、按钮颜色、位置等，一键生成HTML/CSS/JS代码。支持GDPR/CCPA合规的多种样式，可直接嵌入网站。纯前端处理。",
        "desc_en": "Free online Cookie consent banner generator. Customize banner text, button colors, position and generate HTML/CSS/JS code with one click. GDPR/CCPA compliant styles, ready to embed. Pure frontend.",
        "category": "开发工具",
        "cat_en": "Dev Tools",
        "h1_cn": "🍪 Cookie同意横幅生成器",
        "h1_en": "🍪 Cookie Consent Banner Generator",
        "hero_cn": "免费在线Cookie同意横幅生成器，自定义横幅文字、按钮颜色、位置等，一键生成HTML/CSS/JS代码。支持GDPR/CCPA合规的多种样式，可直接嵌入网站。 | 无需注册 · 纯前端处理",
        "hero_en": "Free online Cookie consent banner generator. Customize text, colors, position and generate embeddable code. GDPR/CCPA compliant. | No registration · Pure frontend",
        "keyword": "cookie consent banner",
        "tutorial_cn": "自定义横幅文字、按钮样式、颜色主题和显示位置，实时预览效果，一键生成可嵌入网站的完整代码",
        "tutorial_en": "Customize banner text, button styles, color themes and display position. Real-time preview. Generate complete embeddable code with one click.",
        "faqs": [
            ("cn", "什么是GDPR/CCPA合规？", "GDPR是欧盟通用数据保护条例，CCPA是加州消费者隐私法案。两者都要求网站在使用Cookie前获得用户同意。本工具生成的横幅满足基本合规要求。"),
            ("en", "What is GDPR/CCPA compliance?", "GDPR is the EU General Data Protection Regulation, CCPA is the California Consumer Privacy Act. Both require websites to obtain user consent before using cookies. Banners generated meet basic compliance requirements."),
            ("cn", "生成的代码怎么使用？", "复制生成的HTML/CSS/JS代码，粘贴到网站<body>标签内即可。代码自包含，无需额外依赖。"),
            ("en", "How to use the generated code?", "Copy the generated HTML/CSS/JS code and paste it inside your website's <body> tag. The code is self-contained with no external dependencies."),
            ("cn", "支持自定义样式吗？", "支持自定义横幅位置（顶部/底部）、颜色主题（浅色/深色/自定义）、按钮文字和样式。"),
            ("en", "Can I customize styles?", "Supports customizing banner position (top/bottom), color themes (light/dark/custom), button text and styles."),
        ],
    },
    # ===== 文本工具 =====
    {
        "dir": "reverse-text",
        "title_cn": "文本翻转工具",
        "title_en": "Reverse Text Tool",
        "desc_cn": "免费在线文本翻转工具，支持整段翻转、逐词翻转、逐行翻转三种模式。快速将文本顺序反转，操作简单即输即得。纯前端处理，数据不上传。",
        "desc_en": "Free online reverse text tool. Supports full reversal, word-by-word reversal, and line-by-line reversal. Quick text order reversal, instant results. Pure frontend, no data upload.",
        "category": "文本工具",
        "cat_en": "Text Tools",
        "h1_cn": "🔄 文本翻转工具",
        "h1_en": "🔄 Reverse Text Tool",
        "hero_cn": "免费在线文本翻转工具，支持整段翻转、逐词翻转、逐行翻转三种模式。快速将文本顺序反转，操作简单即输即得。 | 无需注册 · 数据不上传",
        "hero_en": "Free online reverse text tool. Full reversal, word-by-word, line-by-line modes. Quick text reversal, instant results. | No registration · No data upload",
        "keyword": "reverse text",
        "tutorial_cn": "在输入框中粘贴文本，选择翻转模式（整段/逐词/逐行），实时查看翻转结果",
        "tutorial_en": "Paste text in the input box, select reversal mode (full/word-by-word/line-by-line), and see the reversed result in real-time",
        "faqs": [
            ("cn", "三种翻转模式有什么区别？", "整段翻转：将所有字符顺序完全反转（abc→cba）。逐词翻转：保持词序不变，反转每个单词内的字符（hello world→olleh dlrow）。逐行翻转：反转每行的字符顺序，保持行序不变。"),
            ("en", "What's the difference between the three modes?", "Full reversal: reverses all characters (abc→cba). Word-by-word: keeps word order, reverses chars in each word (hello world→olleh dlrow). Line-by-line: reverses chars in each line, keeping line order."),
            ("cn", "支持哪些语言？", "支持所有Unicode字符，包括中文、日文、韩文、阿拉伯文等。中文字符也会被逐字翻转。"),
            ("en", "What languages are supported?", "Supports all Unicode characters including Chinese, Japanese, Korean, Arabic, etc. Chinese characters will also be reversed character by character."),
            ("cn", "数据会上传吗？", "不会。所有文本处理完全在浏览器本地完成，数据绝不会离开您的设备。"),
            ("en", "Is data uploaded?", "No. All text processing is done entirely locally in your browser. Data never leaves your device."),
        ],
    },
    {
        "dir": "remove-duplicates",
        "title_cn": "文本去重工具",
        "title_en": "Remove Duplicates Tool",
        "desc_cn": "免费在线文本去重工具，支持按行去重、保留首次出现或最后出现、忽略空行、区分大小写等选项。快速清理重复文本行，适用于列表整理、邮件去重等场景。纯前端处理。",
        "desc_en": "Free online remove duplicates tool. Deduplicate by line, keep first or last occurrence, ignore blank lines, case-sensitive options. Quick cleanup of duplicate text lines. Perfect for lists and emails. Pure frontend.",
        "category": "文本工具",
        "cat_en": "Text Tools",
        "h1_cn": "🧹 文本去重工具",
        "h1_en": "🧹 Remove Duplicates Tool",
        "hero_cn": "免费在线文本去重工具，支持按行去重、保留首次出现或最后出现、忽略空行、区分大小写等选项。快速清理重复文本行，适用于列表整理、邮件去重等场景。 | 无需注册 · 纯前端处理",
        "hero_en": "Free online remove duplicates tool. Deduplicate by line, keep first/last, ignore blanks, case-sensitive. Clean duplicate text lines fast. | No registration · Pure frontend",
        "keyword": "remove duplicates dedupe",
        "tutorial_cn": "粘贴文本到输入框，选择去重选项（保留首次/末次、忽略空行、区分大小写），点击去重按钮即可获得清理后的文本",
        "tutorial_en": "Paste text into the input box, select dedup options (keep first/last, ignore blanks, case-sensitive), click dedup to get cleaned text",
        "faqs": [
            ("cn", "按行去重是什么意思？", "将文本按换行符分割成多行，然后移除重复的行。例如有3行相同的'hello'，去重后只保留1行。"),
            ("en", "What does deduplicate by line mean?", "Splits text by newlines into lines, then removes duplicate lines. For example, if there are 3 identical 'hello' lines, only 1 remains after deduplication."),
            ("cn", "保留首次和保留末次有什么区别？", "保留首次：当出现重复行时，保留第一次出现的行；保留末次：保留最后一次出现的行，即用后面的覆盖前面的。"),
            ("en", "What's the difference between keep first and keep last?", "Keep first: when duplicates appear, keep the first occurrence. Keep last: keep the last occurrence, i.e., later lines override earlier ones."),
            ("cn", "数据安全吗？", "绝对安全。所有文本处理在浏览器本地完成，不会上传到任何服务器。"),
            ("en", "Is data secure?", "Absolutely. All text processing is done locally in your browser and never uploaded to any server."),
        ],
    },
    {
        "dir": "text-stats",
        "title_cn": "文本统计工具",
        "title_en": "Text Stats Tool",
        "desc_cn": "免费在线文本统计工具，实时统计字符数（含/不含空格）、单词数、行数、段落数、中文字数、标点符号数等。支持多语言混合统计，即输即得。纯前端处理，数据不上传。",
        "desc_en": "Free online text stats tool. Real-time character count (with/without spaces), word count, line count, paragraph count, Chinese character count, punctuation count. Multi-language support. Instant results. Pure frontend.",
        "category": "文本工具",
        "cat_en": "Text Tools",
        "h1_cn": "📊 文本统计工具",
        "h1_en": "📊 Text Stats Tool",
        "hero_cn": "免费在线文本统计工具，实时统计字符数（含/不含空格）、单词数、行数、段落数、中文字数、标点符号数等。支持多语言混合统计，即输即得。 | 无需注册 · 数据不上传",
        "hero_en": "Free online text stats tool. Real-time character/word/line/paragraph count. Multi-language support. Instant results. | No registration · No data upload",
        "keyword": "text stats counter",
        "tutorial_cn": "在文本框中输入或粘贴文本，右侧实时显示各项统计数据，包括字符数、单词数、行数、段落数等",
        "tutorial_en": "Type or paste text in the text box. Real-time stats including character count, word count, line count, paragraph count are displayed on the right.",
        "faqs": [
            ("cn", "中文字数如何统计？", "通过Unicode范围识别中文字符（CJK统一表意文字），与英文单词分别统计。中文字数和英文单词数分别显示。"),
            ("en", "How are Chinese characters counted?", "Chinese characters are identified by Unicode range (CJK Unified Ideographs) and counted separately from English words. Both counts are displayed separately."),
            ("cn", "单词数如何计算？", "英文单词按空格和标点分隔计算，连续字母序列计为1个单词。如'hello world'计为2个单词。"),
            ("en", "How is word count calculated?", "English words are separated by spaces and punctuation. Consecutive letter sequences count as 1 word. For example, 'hello world' counts as 2 words."),
            ("cn", "段落数如何计算？", "按连续换行符分隔，连续的非空文本块计为1个段落。单个换行符前后的文本属于同一段落。"),
            ("en", "How are paragraphs counted?", "Separated by consecutive newlines. Consecutive non-empty text blocks count as 1 paragraph. Text before and after a single newline belongs to the same paragraph."),
        ],
    },
    # ===== 转换器 =====
    {
        "dir": "data-unit-converter",
        "title_cn": "数据单位转换器",
        "title_en": "Data Unit Converter",
        "desc_cn": "免费在线数据存储单位转换器，支持Bit、Byte、KB、MB、GB、TB、PB之间任意转换。输入数值即刻显示所有单位换算结果，适合开发者、IT运维日常使用。纯前端处理。",
        "desc_en": "Free online data storage unit converter. Convert between Bit, Byte, KB, MB, GB, TB, PB. Input a value and see all unit conversions instantly. Perfect for developers and IT ops. Pure frontend.",
        "category": "开发工具",
        "cat_en": "Dev Tools",
        "h1_cn": "💾 数据单位转换器",
        "h1_en": "💾 Data Unit Converter",
        "hero_cn": "免费在线数据存储单位转换器，支持Bit、Byte、KB、MB、GB、TB、PB之间任意转换。输入数值即刻显示所有单位换算结果，适合开发者、IT运维日常使用。 | 无需注册 · 纯前端处理",
        "hero_en": "Free online data storage unit converter. Convert between Bit, Byte, KB, MB, GB, TB, PB. Instant results for all units. Perfect for devs and IT ops. | No registration · Pure frontend",
        "keyword": "data converter bits bytes",
        "tutorial_cn": "输入数值并选择单位，下方实时显示所有数据单位的换算结果，支持Bit/Byte/KB/MB/GB/TB/PB",
        "tutorial_en": "Enter a value and select unit. All data unit conversions (Bit/Byte/KB/MB/GB/TB/PB) are displayed in real-time below.",
        "faqs": [
            ("cn", "使用哪种换算标准？", "使用二进制标准：1 KB = 1024 Bytes，1 MB = 1024 KB，以此类推。这是计算机存储的标准换算方式。"),
            ("en", "Which conversion standard is used?", "Uses binary standard: 1 KB = 1024 Bytes, 1 MB = 1024 KB, and so on. This is the standard for computer storage."),
            ("cn", "Bit和Byte的关系？", "1 Byte = 8 Bits。Byte是计算机存储的基本单位，Bit是数据传输的基本单位。"),
            ("en", "What's the relationship between Bit and Byte?", "1 Byte = 8 Bits. Byte is the basic unit of computer storage, Bit is the basic unit of data transmission."),
            ("cn", "支持小数吗？", "支持任意精度的小数输入，结果会保留合适的小数位数以便阅读。"),
            ("en", "Are decimals supported?", "Decimal input with any precision is supported. Results display appropriate decimal places for readability."),
        ],
    },
]

# Template for CN pages
CN_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc_cn}">
<title>{title_cn} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/{dir}/">
<meta property="og:title" content="免费在线{title_cn} | {title_en}">
<meta property="og:description" content="{desc_cn}">
<meta property="og:url" content="https://free-toolbase.com/{dir}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{dir}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{dir}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{dir}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title_cn}","description":"{desc_cn}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"首页","item":"https://free-toolbase.com/"}},{{"@type":"ListItem","position":2,"name":"工具","item":"https://free-toolbase.com/#tools"}},{{"@type":"ListItem","position":3,"name":"{title_cn}","item":"https://free-toolbase.com/{dir}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.hero{{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.hero p{{color:#94a3b8;font-size:.9rem}}
.badge{{display:inline-block;margin-top:8px;padding:2px 10px;border-radius:4px;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.75rem}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.input-row{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:flex-end}}
.input-group{{flex:1;min-width:140px}}
.input-group label{{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
.input-group input,.input-group select,.input-group textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit}}
.input-group input:focus,.input-group select:focus,.input-group textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.input-group textarea{{min-height:120px;resize:vertical}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:16px}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;text-align:center}}
.result-card .label{{font-size:.75rem;color:#64748b;margin-bottom:4px}}
.result-card .value{{font-size:1.3rem;color:#f1f5f9;font-weight:600}}
.result-card .unit{{font-size:.75rem;color:#64748b;margin-top:2px}}
.result-card.highlight .value{{color:#22d3ee}}
.preview-box{{background:#fff;color:#333;border-radius:8px;padding:24px;margin-top:12px;min-height:200px;border:1px solid rgba(148,163,184,.3);white-space:pre-wrap;font-family:Georgia,serif;line-height:1.8}}
.code-box{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.2);font-family:monospace;font-size:.85rem;color:#e2e8f0;white-space:pre-wrap;overflow-x:auto;max-height:400px;overflow-y:auto}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{margin-left:20px;color:#94a3b8;font-size:.9rem}}
.info-section li{{margin-bottom:6px}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem;line-height:1.7}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}.ad-slot.ad-sidebar{{max-width:300px}}
.color-option{{display:inline-block;width:32px;height:32px;border-radius:50%;cursor:pointer;border:2px solid transparent;margin:4px;transition:border-color .2s}}
.color-option.active{{border-color:#22d3ee}}
.color-option:hover{{border-color:#94a3b8}}
.template-select{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}
.template-opt{{padding:8px 16px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;cursor:pointer;font-size:.85rem;color:#94a3b8;transition:all .2s}}
.template-opt.active{{background:rgba(6,182,212,.15);border-color:rgba(6,182,212,.4);color:#22d3ee}}
.stat-row{{display:flex;gap:12px;flex-wrap:wrap}}
.stat-item{{flex:1;min-width:100px;background:#0f172a;border-radius:8px;padding:12px;text-align:center}}
.stat-item .num{{font-size:1.5rem;color:#22d3ee;font-weight:700}}
.stat-item .lbl{{font-size:.75rem;color:#64748b;margin-top:4px}}
@media(max-width:600px){{.input-row{{flex-direction:column;gap:8px}}.input-group{{min-width:100%}}.result-grid{{grid-template-columns:repeat(2,1fr)}}.stat-row{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{h1_cn}</h1><div class="lang-switch"><a href="index.html" class="active">中文</a><a href="../en/{dir}/" class="">EN</a></div></div>
<p class="nav-back"><a href="../index.html">首页</a> &rsaquo; <a href="../index.html#tools">工具</a> &rsaquo; {title_cn}</p>
<div class="hero"><p>{hero_cn}</p><span class="badge">零依赖·可离线使用</span></div>
<!-- CONTENT_PLACEHOLDER_CN -->
<div class="info-section">
  <h2>使用教程</h2>
  <p>{tutorial_cn}</p>
</div>
<div class="info-section">
  <h2>常见问题 FAQ</h2>
{faqs_cn}
</div>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">首页</a>
<a href="../index.html#tools">全部工具</a>
<a href="mailto:dexshuang@google.com">联系我们</a>
<a href="../privacy/">隐私政策</a>
<a href="../terms/">服务条款</a>
<a href="../en/{dir}/">EN</a>
</footer>
<p>{title_cn} | 无需注册 · 数据绝不上传服务器</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">问题反馈: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<!-- JS_PLACEHOLDER_CN -->
</body>
</html>'''

EN_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc_en}">
<title>{title_en} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{dir}/">
<meta property="og:title" content="Free Online {title_en} | {title_cn}">
<meta property="og:description" content="{desc_en}">
<meta property="og:url" content="https://free-toolbase.com/en/{dir}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{dir}/">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{dir}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{dir}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{title_en}","description":"{desc_en}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{title_en}","item":"https://free-toolbase.com/en/{dir}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}
.container{{max-width:900px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}}
.header h1{{font-size:1.6rem;color:#f1f5f9}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}
.nav-back a:hover{{color:#94a3b8}}
.hero{{background:#1e293b;border-radius:12px;padding:16px 20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.hero p{{color:#94a3b8;font-size:.9rem}}
.badge{{display:inline-block;margin-top:8px;padding:2px 10px;border-radius:4px;background:rgba(6,182,212,.15);color:#22d3ee;font-size:.75rem}}
.input-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.input-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.input-row{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px;align-items:flex-end}}
.input-group{{flex:1;min-width:140px}}
.input-group label{{display:block;font-size:.85rem;color:#94a3b8;margin-bottom:4px}}
.input-group input,.input-group select,.input-group textarea{{width:100%;padding:10px 12px;background:#0f172a;color:#e2e8f0;border:1px solid rgba(148,163,184,.2);border-radius:8px;font-size:.9rem;font-family:inherit}}
.input-group input:focus,.input-group select:focus,.input-group textarea:focus{{outline:none;border-color:rgba(6,182,212,.5)}}
.input-group textarea{{min-height:120px;resize:vertical}}
.btn-row{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}
.btn{{padding:8px 20px;border:none;border-radius:6px;font-size:.85rem;cursor:pointer;transition:all .2s}}
.btn-primary{{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}}
.btn-primary:hover{{background:rgba(6,182,212,.3)}}
.btn-secondary{{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}}
.btn-secondary:hover{{background:rgba(148,163,184,.2)}}
.result-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1);display:none}}
.result-section.show{{display:block}}
.result-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:16px}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;text-align:center}}
.result-card .label{{font-size:.75rem;color:#64748b;margin-bottom:4px}}
.result-card .value{{font-size:1.3rem;color:#f1f5f9;font-weight:600}}
.result-card .unit{{font-size:.75rem;color:#64748b;margin-top:2px}}
.result-card.highlight .value{{color:#22d3ee}}
.preview-box{{background:#fff;color:#333;border-radius:8px;padding:24px;margin-top:12px;min-height:200px;border:1px solid rgba(148,163,184,.3);white-space:pre-wrap;font-family:Georgia,serif;line-height:1.8}}
.code-box{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.2);font-family:monospace;font-size:.85rem;color:#e2e8f0;white-space:pre-wrap;overflow-x:auto;max-height:400px;overflow-y:auto}}
.info-section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.info-section h2{{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}}
.info-section h3{{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}}
.info-section p{{color:#94a3b8;font-size:.9rem;margin-bottom:8px}}
.info-section ul{{margin-left:20px;color:#94a3b8;font-size:.9rem}}
.info-section li{{margin-bottom:6px}}
.faq-item{{margin-bottom:16px}}
.faq-item h3{{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}}
.faq-item p{{color:#94a3b8;font-size:.9rem;line-height:1.7}}
.footer{{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}}
.footer a{{color:#64748b;margin:0 8px}}
.footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s}}
.toast.show{{opacity:1}}
.ad-slot{{margin:0 auto;text-align:center;max-width:960px}}.ad-slot:not(:has(ins[frame])){{display:none}}.ad-slot:empty{{display:none}}.ad-slot ins{{display:block}}.ad-slot.ad-sidebar{{max-width:300px}}
.color-option{{display:inline-block;width:32px;height:32px;border-radius:50%;cursor:pointer;border:2px solid transparent;margin:4px;transition:border-color .2s}}
.color-option.active{{border-color:#22d3ee}}
.color-option:hover{{border-color:#94a3b8}}
.template-select{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}}
.template-opt{{padding:8px 16px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;cursor:pointer;font-size:.85rem;color:#94a3b8;transition:all .2s}}
.template-opt.active{{background:rgba(6,182,212,.15);border-color:rgba(6,182,212,.4);color:#22d3ee}}
.stat-row{{display:flex;gap:12px;flex-wrap:wrap}}
.stat-item{{flex:1;min-width:100px;background:#0f172a;border-radius:8px;padding:12px;text-align:center}}
.stat-item .num{{font-size:1.5rem;color:#22d3ee;font-weight:700}}
.stat-item .lbl{{font-size:.75rem;color:#64748b;margin-top:4px}}
@media(max-width:600px){{.input-row{{flex-direction:column;gap:8px}}.input-group{{min-width:100%}}.result-grid{{grid-template-columns:repeat(2,1fr)}}.stat-row{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:640px){{h1{{font-size:1.2rem;word-break:break-word}}.header{{flex-direction:column;gap:8px}}}}
</style>
<meta property="og:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:image" content="https://free-toolbase.com/og-image.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5998441792679372" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="header"><h1>{h1_en}</h1><div class="lang-switch"><a href="../../{dir}/" class="">中文</a><a href="index.html" class="active">EN</a></div></div>
<p class="nav-back"><a href="../index.html">Home</a> &rsaquo; <a href="../index.html#tools">Tools</a> &rsaquo; {title_en}</p>
<div class="hero"><p>{hero_en}</p><span class="badge">Zero dependencies · Works offline</span></div>
<!-- CONTENT_PLACEHOLDER_EN -->
<div class="info-section">
  <h2>Tutorial</h2>
  <p>{tutorial_en}</p>
</div>
<div class="info-section">
  <h2>FAQ</h2>
{faqs_en}
</div>
</div>
<div>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-5998441792679372"
     data-ad-slot="auto"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
<footer class="footer container">
<div style="margin-bottom:12px">
<a href="../index.html">Home</a>
<a href="../index.html#tools">All Tools</a>
<a href="mailto:dexshuang@google.com">Contact</a>
<a href="../privacy/">Privacy Policy</a>
<a href="../terms/">Terms of Service</a>
<a href="../../{dir}/">中文</a>
</footer>
<p>{title_en} | No registration · No data upload</p>
<p style="margin-top:8px;color:#475569;font-size:.8rem">Feedback: dexshuang@google.com</p>
</div>
<div class="toast" id="toast"></div>
<!-- JS_PLACEHOLDER_EN -->
</body>
</html>'''

def gen_faq_html(faqs, lang='cn'):
    """Generate FAQ HTML"""
    parts = []
    for f in faqs:
        if f[0] == lang:
            parts.append(f'  <div class="faq-item"><h3>{f[1]}</h3><p>{f[2]}</p></div>')
    return '\n'.join(parts)

def gen_wedding_content(lang):
    """婚礼邀请函生成器"""
    labels = {
        'cn': {
            'groom': '新郎姓名', 'bride': '新娘姓名', 'date': '婚礼日期',
            'time': '婚礼时间', 'venue': '婚礼地点', 'msg': '邀请语',
            'gen': '✨ 生成邀请函', 'reset': '🔄 重置', 'print': '🖨️ 打印邀请函',
            'preview_title': '邀请函预览',
            'default_msg': '诚挚邀请您出席我们的婚礼，见证我们人生中最幸福的时刻。您的到来将是我们最大的荣幸！',
        },
        'en': {
            'groom': 'Groom Name', 'bride': 'Bride Name', 'date': 'Wedding Date',
            'time': 'Wedding Time', 'venue': 'Wedding Venue', 'msg': 'Invitation Message',
            'gen': '✨ Generate', 'reset': '🔄 Reset', 'print': '🖨️ Print',
            'preview_title': 'Invitation Preview',
            'default_msg': 'We joyfully invite you to celebrate our wedding and witness the happiest moment of our lives. Your presence will be our greatest honor!',
        }
    }
    l = labels[lang]
    tpl_cn = '''<div class="input-section" id="input">
  <h2>邀请函信息</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">填写新人和婚礼信息，选择样式后生成精美邀请函</p>
  <div class="input-row">
    <div class="input-group"><label>{groom}</label><input type="text" id="groom" placeholder="张三" value="张三"></div>
    <div class="input-group"><label>{bride}</label><input type="text" id="bride" placeholder="李四" value="李四"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{date}</label><input type="date" id="wdate" value="2026-10-01"></div>
    <div class="input-group"><label>{time}</label><input type="text" id="wtime" placeholder="12:00" value="12:00"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{venue}</label><input type="text" id="venue" placeholder="XX酒店宴会厅" value="XX酒店宴会厅"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{msg}</label><textarea id="inviteMsg">{default_msg}</textarea></div>
  </div>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">选择样式</p>
  <div class="template-select" id="styleSelect">
    <span class="template-opt active" data-style="classic">经典优雅</span>
    <span class="template-opt" data-style="modern">现代简约</span>
    <span class="template-opt" data-style="floral">花卉浪漫</span>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">{reset}</button>
    <button class="btn btn-primary" id="genBtn">{gen}</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{preview_title}</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="printBtn">{print}</button>
  </div>
</div>'''
    tpl_en = '''<div class="input-section" id="input">
  <h2>Invitation Details</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">Fill in couple and wedding details, choose a style to generate a beautiful invitation</p>
  <div class="input-row">
    <div class="input-group"><label>{groom}</label><input type="text" id="groom" placeholder="John" value="John"></div>
    <div class="input-group"><label>{bride}</label><input type="text" id="bride" placeholder="Jane" value="Jane"></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{date}</label><input type="date" id="wdate" value="2026-10-01"></div>
    <div class="input-group"><label>{time}</label><input type="text" id="wtime" placeholder="12:00 PM" value="12:00 PM"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{venue}</label><input type="text" id="venue" placeholder="Grand Hotel Ballroom" value="Grand Hotel Ballroom"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{msg}</label><textarea id="inviteMsg">{default_msg}</textarea></div>
  </div>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:8px">Choose Style</p>
  <div class="template-select" id="styleSelect">
    <span class="template-opt active" data-style="classic">Classic</span>
    <span class="template-opt" data-style="modern">Modern</span>
    <span class="template-opt" data-style="floral">Floral</span>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">{reset}</button>
    <button class="btn btn-primary" id="genBtn">{gen}</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{preview_title}</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="printBtn">{print}</button>
  </div>
</div>'''
    tpl = tpl_en if lang == 'en' else tpl_cn
    return tpl.format(**l)

def gen_wedding_js(lang):
    js = '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var style="classic";
function getStyleCSS(s){
  if(s==="classic") return "background:linear-gradient(135deg,#fdf6f0,#fef9f3);color:#5d4037;border:3px double #c9a96e;font-family:Georgia,serif;text-align:center;";
  if(s==="modern") return "background:linear-gradient(135deg,#f8fafc,#e2e8f0);color:#1e293b;border:2px solid #475569;font-family:'Helvetica Neue',Arial,sans-serif;text-align:center;";
  return "background:linear-gradient(135deg,#fff5f5,#fce4ec);color:#880e4f;border:2px solid #f48fb1;font-family:Georgia,serif;text-align:center;background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2220%22 height=%2220%22><text x=%220%22 y=%2216%22 font-size=%2216%22>%f0%9f%8c%b8</text></svg>');background-size:30px;";
}
function generate(){
  var g=document.getElementById("groom").value.trim()||"N/A";
  var b=document.getElementById("bride").value.trim()||"N/A";
  var d=document.getElementById("wdate").value||"";
  var t=document.getElementById("wtime").value.trim()||"";
  var v=document.getElementById("venue").value.trim()||"";
  var m=document.getElementById("inviteMsg").value.trim()||"";
  var isEN=document.documentElement.lang==="en";
  var heart=isEN?"♡":"♥";
  var html='<div style="padding:40px 30px;'+getStyleCSS(style)+'">';
  html+='<div style="font-size:3rem;margin-bottom:16px">'+heart+'</div>';
  html+='<h2 style="font-size:2rem;margin-bottom:8px;font-weight:400">'+g+'</h2>';
  html+='<div style="font-size:1.5rem;margin:12px 0;color:inherit;opacity:0.7">'+heart+'</div>';
  html+='<h2 style="font-size:2rem;margin-bottom:8px;font-weight:400">'+b+'</h2>';
  html+='<div style="margin:24px 0;font-size:1.1rem">';
  if(d) html+='<p style="margin:8px 0">'+d+'</p>';
  if(t) html+='<p style="margin:8px 0">'+t+'</p>';
  if(v) html+='<p style="margin:8px 0">'+v+'</p>';
  html+='</div>';
  if(m) html+='<p style="font-style:italic;margin:20px 0;font-size:1rem;max-width:400px;margin-left:auto;margin-right:auto;line-height:1.8">'+m+'</p>';
  html+='<div style="margin-top:24px;font-size:0.9rem;opacity:0.7">'+heart+' '+heart+' '+heart+'</div>';
  html+='</div>';
  document.getElementById("preview").innerHTML=html;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"Invitation generated!":"邀请函已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){
  var isEN=document.documentElement.lang==="en";
  document.getElementById("groom").value=isEN?"John":"张三";
  document.getElementById("bride").value=isEN?"Jane":"李四";
  document.getElementById("wdate").value="2026-10-01";
  document.getElementById("wtime").value=isEN?"12:00 PM":"12:00";
  document.getElementById("venue").value=isEN?"Grand Hotel Ballroom":"XX酒店宴会厅";
  document.getElementById("inviteMsg").value=isEN?"We joyfully invite you to celebrate our wedding and witness the happiest moment of our lives. Your presence will be our greatest honor!":"诚挚邀请您出席我们的婚礼，见证我们人生中最幸福的时刻。您的到来将是我们最大的荣幸！";
  generate();
  showToast(isEN?"Reset!":"已重置！");
});
document.getElementById("printBtn").addEventListener("click",function(){window.print()});
document.getElementById("styleSelect").addEventListener("click",function(e){if(e.target.classList.contains("template-opt")){document.querySelectorAll("#styleSelect .template-opt").forEach(function(el){el.classList.remove("active")});e.target.classList.add("active");style=e.target.dataset.style;generate()}});
generate();
</script>'''
    return js

def gen_letter_content(lang):
    """信函模板生成器"""
    labels = {
        'cn': {
            'tpl': '选择模板', 'business': '商务信函', 'cover': '求职信', 'recommend': '推荐信',
            'sender': '发信人', 'recipient': '收信人', 'subject': '主题',
            'body': '正文内容', 'gen': '✉️ 生成信函', 'reset': '🔄 重置',
            'preview': '信函预览', 'copy': '📋 复制',
            'default_body': '尊敬的先生/女士：\n\n写此信是为了...\n\n期待您的回复。\n\n此致\n敬礼',
        },
        'en': {
            'tpl': 'Template', 'business': 'Business Letter', 'cover': 'Cover Letter', 'recommend': 'Recommendation',
            'sender': 'Sender', 'recipient': 'Recipient', 'subject': 'Subject',
            'body': 'Body', 'gen': '✉️ Generate', 'reset': '🔄 Reset',
            'preview': 'Letter Preview', 'copy': '📋 Copy',
            'default_body': 'Dear Sir/Madam,\n\nI am writing to...\n\nLooking forward to your reply.\n\nSincerely,',
        }
    }
    l = labels[lang]
    tpl_cn = '''<div class="input-section" id="input">
  <h2>信函信息</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{tpl}</p>
  <div class="template-select" id="tplSelect">
    <span class="template-opt active" data-tpl="business">{business}</span>
    <span class="template-opt" data-tpl="cover">{cover}</span>
    <span class="template-opt" data-tpl="recommend">{recommend}</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{sender}</label><input type="text" id="sender" placeholder="张三" value="张三"></div>
    <div class="input-group"><label>{recipient}</label><input type="text" id="recipient" placeholder="李四" value="李四"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{subject}</label><input type="text" id="subject" placeholder="关于..."></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{body}</label><textarea id="body">{default_body}</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">{reset}</button>
    <button class="btn btn-primary" id="genBtn">{gen}</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{preview}</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">{copy}</button>
  </div>
</div>'''
    tpl_en = '''<div class="input-section" id="input">
  <h2>Letter Details</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{tpl}</p>
  <div class="template-select" id="tplSelect">
    <span class="template-opt active" data-tpl="business">{business}</span>
    <span class="template-opt" data-tpl="cover">{cover}</span>
    <span class="template-opt" data-tpl="recommend">{recommend}</span>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{sender}</label><input type="text" id="sender" placeholder="John" value="John"></div>
    <div class="input-group"><label>{recipient}</label><input type="text" id="recipient" placeholder="Jane" value="Jane"></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{subject}</label><input type="text" id="subject" placeholder="About..."></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{body}</label><textarea id="body">{default_body}</textarea></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">{reset}</button>
    <button class="btn btn-primary" id="genBtn">{gen}</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{preview}</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">{copy}</button>
  </div>
</div>'''
    tpl = tpl_en if lang == 'en' else tpl_cn
    return tpl.format(**l)

def gen_letter_js(lang):
    return '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
var tpl="business";
function getDate(){var d=new Date();var m=["January","February","March","April","May","June","July","August","September","October","November","December"];var isEN=document.documentElement.lang==="en";return isEN?m[d.getMonth()]+" "+d.getDate()+", "+d.getFullYear():d.getFullYear()+"年"+(d.getMonth()+1)+"月"+d.getDate()+"日"}
function generate(){
  var s=document.getElementById("sender").value.trim()||"";
  var r=document.getElementById("recipient").value.trim()||"";
  var sub=document.getElementById("subject").value.trim()||"";
  var b=document.getElementById("body").value.trim()||"";
  var isEN=document.documentElement.lang==="en";
  var tplNames={business:isEN?"Business Letter":"商务信函",cover:isEN?"Cover Letter":"求职信",recommend:isEN?"Recommendation Letter":"推荐信"};
  var html='<div style="max-width:650px;margin:0 auto;text-align:left">';
  html+='<div style="text-align:center;margin-bottom:20px"><strong style="font-size:1.2rem">'+tplNames[tpl]+'</strong></div>';
  html+='<p>'+getDate()+'</p><br>';
  if(s) html+='<p><strong>'+(isEN?'From: ':'发信人：')+'</strong>'+s+'</p>';
  if(r) html+='<p><strong>'+(isEN?'To: ':'收信人：')+'</strong>'+r+'</p>';
  if(sub) html+='<p><strong>'+(isEN?'Subject: ':'主题：')+'</strong>'+sub+'</p>';
  html+='<hr style="margin:16px 0;border:none;border-top:1px solid #ddd">';
  html+='<div style="line-height:2">'+b.replace(/\\n/g,'<br>')+'</div>';
  html+='<hr style="margin:16px 0;border:none;border-top:1px solid #ddd">';
  if(s) html+='<p>'+(isEN?'Sincerely,':'此致')+'<br>'+s+'</p>';
  html+='</div>';
  document.getElementById("preview").innerHTML=html;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"Letter generated!":"信函已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){
  var isEN=document.documentElement.lang==="en";
  document.getElementById("sender").value=isEN?"John":"张三";
  document.getElementById("recipient").value=isEN?"Jane":"李四";
  document.getElementById("subject").value="";
  document.getElementById("body").value=isEN?"Dear Sir/Madam,\\n\\nI am writing to...\\n\\nLooking forward to your reply.\\n\\nSincerely,":"尊敬的先生/女士：\\n\\n写此信是为了...\\n\\n期待您的回复。\\n\\n此致\\n敬礼";
  generate();showToast(isEN?"Reset!":"已重置！");
});
document.getElementById("copyBtn").addEventListener("click",function(){var p=document.getElementById("preview").innerText;navigator.clipboard.writeText(p).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
document.getElementById("tplSelect").addEventListener("click",function(e){if(e.target.classList.contains("template-opt")){document.querySelectorAll("#tplSelect .template-opt").forEach(function(el){el.classList.remove("active")});e.target.classList.add("active");tpl=e.target.dataset.tpl;generate()}});
generate();
</script>'''

def gen_press_content(lang):
    """新闻稿模板生成器"""
    labels = {
        'cn': {'headline':'新闻标题','city':'发布城市','lead':'导语段落','body':'正文','company':'关于公司','contact':'媒体联系','gen':'📰 生成新闻稿','reset':'🔄 重置','preview':'新闻稿预览','copy':'📋 复制'},
        'en': {'headline':'Headline','city':'City','lead':'Lead Paragraph','body':'Body','company':'About Company','contact':'Media Contact','gen':'📰 Generate','reset':'🔄 Reset','preview':'Press Release Preview','copy':'📋 Copy'},
    }
    l = labels[lang]
    is_en = lang == 'en'
    default_lead = "Today announced a significant milestone in..." if is_en else "今日宣布了一项重要进展..."
    default_body = "The company continues to expand its offerings..." if is_en else "公司持续扩展其产品线..."
    default_company = "About: A leading provider of innovative solutions." if is_en else "关于我们：领先的创新解决方案提供商。"
    default_contact = "Press Contact: press@example.com" if is_en else "媒体联系：press@example.com"
    tpl = '''<div class="input-section" id="input">
  <h2>{title_label}</h2>
  <p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px">{subtitle}</p>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{headline}</label><input type="text" id="headline" placeholder="..." value=""></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{city}</label><input type="text" id="city" placeholder="..." value=""></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{lead}</label><textarea id="lead">{default_lead}</textarea></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{body}</label><textarea id="body" style="min-height:160px">{default_body}</textarea></div>
  </div>
  <div class="input-row">
    <div class="input-group" style="flex:2"><label>{company}</label><textarea id="company" style="min-height:80px">{default_company}</textarea></div>
  </div>
  <div class="input-row">
    <div class="input-group"><label>{contact}</label><input type="text" id="contact" value="{default_contact}"></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-secondary" id="resetBtn">{reset}</button>
    <button class="btn btn-primary" id="genBtn">{gen}</button>
  </div>
</div>
<div class="result-section show" id="resultSection">
  <h2 style="text-align:center;color:#f1f5f9;margin-bottom:12px">{preview}</h2>
  <div class="preview-box" id="preview"></div>
  <div class="btn-row" style="justify-content:center;margin-top:16px">
    <button class="btn btn-primary" id="copyBtn">{copy}</button>
  </div>
</div>'''
    title_label = '新闻稿信息' if not is_en else 'Press Release Details'
    subtitle = '填写新闻稿各要素，生成标准AP格式新闻稿' if not is_en else 'Fill in press release elements to generate standard AP-style press release'
    return tpl.format(title_label=title_label, subtitle=subtitle, default_lead=default_lead, default_body=default_body, default_company=default_company, default_contact=default_contact, **l)

def gen_press_js(lang):
    return '''<script>
function showToast(m){var t=document.getElementById("toast");t.textContent=m;t.classList.add("show");setTimeout(function(){t.classList.remove("show")},2500)}
function getDate(){var d=new Date();var isEN=document.documentElement.lang==="en";if(isEN)return d.toLocaleDateString("en-US",{year:"numeric",month:"long",day:"numeric"});return d.getFullYear()+"年"+(d.getMonth()+1)+"月"+d.getDate()+"日"}
function generate(){
  var hl=document.getElementById("headline").value.trim();
  var ct=document.getElementById("city").value.trim();
  var ld=document.getElementById("lead").value.trim();
  var bd=document.getElementById("body").value.trim();
  var co=document.getElementById("company").value.trim();
  var cn=document.getElementById("contact").value.trim();
  var isEN=document.documentElement.lang==="en";
  var html='<div style="max-width:650px;margin:0 auto;text-align:left;line-height:1.8">';
  html+='<p style="text-align:center;color:#666;text-transform:uppercase;letter-spacing:2px;font-size:0.85rem">'+(isEN?'FOR IMMEDIATE RELEASE':'即时发布')+'</p>';
  html+='<p>'+getDate()+'</p>';
  if(ct) html+='<p><strong>'+ct+'</strong></p>';
  if(hl) html+='<h2 style="font-size:1.4rem;margin:16px 0;text-align:center">'+hl+'</h2>';
  if(ld) html+='<p>'+ld+'</p>';
  if(bd) html+='<p>'+bd.replace(/\\n/g,'<br>')+'</p>';
  if(co) html+='<p style="margin-top:20px"><strong>'+(isEN?'About':'关于')+'</strong><br>'+co+'</p>';
  if(cn) html+='<p style="margin-top:12px">'+cn+'</p>';
  html+='<p style="text-align:center;margin-top:24px;color:#666">###</p>';
  html+='</div>';
  document.getElementById("preview").innerHTML=html;
}
document.getElementById("genBtn").addEventListener("click",function(){generate();showToast(document.documentElement.lang==="en"?"Press release generated!":"新闻稿已生成！")});
document.getElementById("resetBtn").addEventListener("click",function(){document.querySelectorAll("#input input,#input textarea").forEach(function(el){el.value=""});generate();showToast(document.documentElement.lang==="en"?"Reset!":"已重置！")});
document.getElementById("copyBtn").addEventListener("click",function(){navigator.clipboard.writeText(document.getElementById("preview").innerText).then(function(){showToast(document.documentElement.lang==="en"?"Copied!":"已复制！")})});
generate();
</script>'''

# ===== 批量生成 =====
for t in TOOLS:
    d = t['dir']
    os.makedirs(d, exist_ok=True)
    os.makedirs(f'en/{d}', exist_ok=True)
    
    # FAQ HTML
    faqs_cn = gen_faq_html(t['faqs'], 'cn')
    faqs_en = gen_faq_html(t['faqs'], 'en')
    
    # Generate content and JS based on tool type
    if d == 'wedding-invitation-maker':
        content_cn = gen_wedding_content('cn')
        content_en = gen_wedding_content('en')
        js_cn = gen_wedding_js('cn')
        js_en = gen_wedding_js('en')
    elif d == 'letter-template-generator':
        content_cn = gen_letter_content('cn')
        content_en = gen_letter_content('en')
        js_cn = gen_letter_js('cn')
        js_en = gen_letter_js('en')
    elif d == 'press-release-template':
        content_cn = gen_press_content('cn')
        content_en = gen_press_content('en')
        js_cn = gen_press_js('cn')
        js_en = gen_press_js('en')
    else:
        # Default: will be handled individually below
        content_cn = ''
        content_en = ''
        js_cn = ''
        js_en = ''
    
    # CN page
    cn_html = CN_TEMPLATE.format(dir=d, desc_cn=t['desc_cn'], title_cn=t['title_cn'], title_en=t['title_en'],
                                  h1_cn=t['h1_cn'], hero_cn=t['hero_cn'], tutorial_cn=t['tutorial_cn'],
                                  faqs_cn=faqs_cn)
    cn_html = cn_html.replace('<!-- CONTENT_PLACEHOLDER_CN -->', content_cn)
    cn_html = cn_html.replace('<!-- JS_PLACEHOLDER_CN -->', js_cn)
    
    with open(f'{d}/index.html', 'w', encoding='utf-8') as f:
        f.write(cn_html)
    
    # EN page
    en_html = EN_TEMPLATE.format(dir=d, desc_en=t['desc_en'], title_cn=t['title_cn'], title_en=t['title_en'],
                                  h1_en=t['h1_en'], hero_en=t['hero_en'], tutorial_en=t['tutorial_en'],
                                  faqs_en=faqs_en)
    en_html = en_html.replace('<!-- CONTENT_PLACEHOLDER_EN -->', content_en)
    en_html = en_html.replace('<!-- JS_PLACEHOLDER_EN -->', js_en)
    
    with open(f'en/{d}/index.html', 'w', encoding='utf-8') as f:
        f.write(en_html)
    
    print(f'✅ {d} (CN + EN)')

print(f'\nDone! Generated {len(TOOLS)} tools (20 files)')
#!/usr/bin/env python3
"""
Fix English meta descriptions that are too short (<100 chars) or merged pages.
Reads each en/*/index.html, extracts tool name from title, generates proper 140-160 char description.
"""
import os
import re
import json

BASE = '/home/chison/tools-site'

def get_tool_name(filepath):
    """Extract tool name from <title> tag."""
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<title>(.*?)(?:\s*[-–—|]\s*Free ToolBase)?</title>', content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return None

def get_existing_desc(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if m:
        return m.group(1)
    return None

def get_h1(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if m:
        h1 = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return h1
    return None

# Tool-specific description templates
TOOL_DESCRIPTIONS = {
    'ascii-to-hex': 'Convert ASCII text to hexadecimal instantly with our free online converter. Real-time conversion, client-side processing for data privacy, no registration required.',
    'aes-encryptor': 'Free online AES encryption tool with multiple modes (CBC, ECB, GCM). Encrypt and decrypt text securely in your browser. No signup, no data upload, completely private.',
    'ai-sentence-rewriter': 'Rewrite sentences with AI-powered paraphrasing. Free online tool to improve clarity, tone, and style. Perfect for essays, emails, and content creation.',
    'animated-backgrounds': 'Create beautiful CSS animated backgrounds for your website. Choose from gradients, particles, waves, and more. Free, customizable, no coding required.',
    'annuity-calculator': 'Calculate annuity payments, future value, and present value with our free online annuity calculator. Plan your retirement or investment income easily.',
    'audio-compressor': 'Compress audio files online for free. Reduce MP3, WAV, AAC file sizes without losing quality. Fast browser-based compression, no upload needed.',
    'audio-volume-adjuster': 'Adjust audio volume online for free. Increase or decrease MP3/WAV volume with our browser-based tool. No upload required, instant processing.',
    'audio-waveform-visualizer': 'Visualize audio waveforms online for free. Upload or drag-and-drop audio files to see real-time waveform display. Perfect for podcasters and musicians.',
    'avatar-generator': 'Generate custom avatars online for free. Create unique profile pictures with our avatar maker. Choose styles, colors, and shapes. No signup needed.',
    'babel-config-generator': 'Generate Babel configuration files online for free. Customize presets, plugins, and targets for your JavaScript project. Visual builder with live preview.',
    'banner-generator': 'Create stunning banners for YouTube, social media, and websites. Free online banner maker with customizable templates, text, and colors. No design skills needed.',
    'base64-to-file': 'Decode Base64 strings back to files online for free. Convert Base64-encoded data to images, PDFs, documents. Instant download, no upload needed.',
    'bcrypt-hash-generator': 'Generate bcrypt password hashes online for free. Secure your passwords with adjustable salt rounds. Perfect for developers implementing authentication.',
    'binary-translator': 'Translate binary code to text and vice versa. Free online binary translator with instant conversion. Learn binary or decode messages easily.',
    'binaural-beats-generator': 'Generate binaural beats for focus, relaxation, and sleep. Free online binaural beats generator with adjustable frequencies. Download your custom audio.',
    'birthday-countdown': 'Count down to your next birthday with our free online birthday countdown timer. Real-time display of days, hours, minutes, and seconds remaining.',
    'break-even-calculator': 'Calculate your business break-even point instantly. Free online break-even analysis tool for fixed costs, variable costs, and pricing decisions.',
    'breathing-exercise': 'Practice guided breathing exercises online for free. Reduce stress and anxiety with timed inhale-hold-exhale cycles. Follow the visual guide to relax.',
    'bubble-text-generator': 'Create fun bubble text and speech bubble effects. Free online bubble text generator with multiple styles. Copy and paste anywhere — perfect for social media.',
    'business-name-generator': 'Generate creative business name ideas instantly. Free online business name generator with keyword-based suggestions. Find the perfect name for your startup.',
    'caddy-config-generator': 'Generate Caddy server configuration files online for free. Visual Caddyfile builder with reverse proxy, TLS, and header options. No YAML, just clean config.',
    'certificate-generator': 'Create professional certificates online for free. Customize text, fonts, and borders. Perfect for awards, completion certificates, and recognition.',
    'certificate-parser': 'Parse SSL/TLS certificate details online for free. View expiration dates, issuer info, SANs, and more. Paste or upload your certificate file.',
    'c-formatter': 'Format and beautify C/C++ code online for free. Indent, align, and style your code with customizable formatting options. Perfect for developers.',
    'character-count': 'Count characters, words, and lines in your text. Free online character counter with real-time statistics. Essential for writers and social media posts.',
    'chess-clock': 'Free online chess clock timer with customizable time controls. Perfect for chess games, tournaments, and practice. Supports increment and delay modes.',
    'chord-generator': 'Generate guitar and ukulele chords online for free. Select root notes and chord types to see finger positions and hear the sound. Great for musicians.',
    'circle-calculator': 'Calculate circle area, circumference, diameter, and radius. Free online circle calculator with instant results. Enter any one value to get all others.',
    'code-beautifier': 'Beautify and format your code online for free. Support for JavaScript, HTML, CSS, JSON, and more. Clean indentation and syntax highlighting.',
    'code-compare': 'Compare and diff code side by side online for free. Highlight additions, deletions, and changes. Support for all programming languages.',
    'code-playground': 'Free online code sandbox with live HTML, CSS, and JavaScript preview. Write and test code instantly in your browser. No setup required.',
    'color-contrast-ratio': 'Check color contrast ratios for WCAG accessibility compliance. Free online contrast checker with AA/AAA ratings. Ensure your design is accessible.',
    'color-harmony': 'Generate harmonious color palettes online for free. Explore complementary, analogous, triadic, and monochromatic schemes. Perfect for designers.',
    'confetti-generator': 'Create confetti animation effects for your website. Free online confetti effect generator with customizable colors, speed, and shapes. Copy CSS and JS code.',
    'crc32-calculator': 'Calculate CRC32 checksums for files and text online for free. Verify data integrity with instant hash computation. Essential for developers and IT.',
    'creative': 'Explore free online creative tools — text effects, color generators, CSS animations, and more. Everything you need for web design in one place.',
    'cron-expression-parser': 'Parse and validate cron expressions online for free. Visual breakdown of cron schedule fields. Perfect for developers and system administrators.',
    'crossword-generator': 'Generate custom crossword puzzles online for free. Enter your words and clues to create printable crosswords. Great for teachers and puzzle lovers.',
    'css-animation-generator': 'Create CSS animations visually without coding. Free online CSS animation generator with keyframe editor. Generate smooth transitions, transforms, and more.',
    'css-aurora-effect-generator': 'Create stunning CSS aurora borealis effects for your website. Free online generator with customizable colors and animation speed. Copy ready-to-use code.',
    'css-blend-mode-generator': 'Experiment with CSS blend modes online for free. Visual blend mode preview with live CSS code generation. See how multiply, screen, overlay, and more work.',
    'css-box-model': 'Visualize and calculate CSS box model dimensions. Free online tool showing margin, border, padding, and content area. Essential for web developers.',
    'css-box-shadow-generator': 'Generate CSS box-shadow code visually. Free online generator with multiple layers, blur, spread, and color picker. Copy clean CSS instantly.',
    'css-color-mix-generator': 'Generate CSS color-mix() function values visually. Free online tool to blend colors using the CSS color-mix function. See preview and get code.',
    'css-columns-generator': 'Generate CSS multi-column layouts online for free. Customize column count, gap, and rules. Perfect for magazine-style text layouts.',
    'css-dark-mode-generator': 'Generate CSS dark mode color schemes online for free. Convert your light theme to dark with automatic color adjustments. Preview and copy CSS variables.',
    'css-filter-generator': 'Generate CSS filter effects visually. Free online tool for blur, brightness, contrast, grayscale, and more. See real-time preview and copy CSS code.',
    'css-font-size-calculator': 'Calculate CSS font sizes with our free online tool. Convert between px, rem, em, and pt. Responsive typography made easy.',
    'css-gradient-generator': 'Create stunning CSS gradients visually. Free online gradient generator with linear, radial, and conic options. Copy ready-to-use CSS background code.',
    'css-line-clamp': 'Generate CSS line-clamp code to truncate multi-line text. Free online tool with visual preview. Control the number of lines and ellipsis behavior.',
    'css-list-style-generator': 'Generate CSS list-style code visually. Customize markers, positions, and image bullets. Free online tool for styled HTML lists.',
    'css-marquee-generator': 'Create CSS marquee scrolling text effects. Free online generator with direction, speed, and pause-on-hover options. No JavaScript needed.',
    'css-mask-generator': 'Generate CSS mask-image properties visually. Free online CSS mask generator for creating image masks, gradients, and SVG masks. Preview in real-time.',
    'css-media-query-generator': 'Generate CSS media queries for responsive design. Free online tool supporting min-width, max-width, and device-specific breakpoints. Copy clean CSS.',
    'css-nesting-generator': 'Generate CSS nesting syntax for modern browsers. Free online CSS nesting converter and generator. Write cleaner, more organized stylesheets.',
    'css-overflow-generator': 'Generate CSS overflow properties visually. Free online tool to control scroll, hidden, and auto overflow behavior. See live preview of each option.',
    'css-overlay-generator': 'Create CSS overlay effects for images and sections. Free online generator with color, opacity, and blend mode options. Perfect for hero sections.',
    'css-parallax-generator': 'Generate CSS parallax scrolling effects. Free online tool to create depth and movement on scroll. No JavaScript, pure CSS solution.',
    'css-shadow-generator': 'Generate CSS box-shadow and text-shadow visually. Free online shadow generator with color, blur, and spread controls. Copy clean CSS instantly.',
    'css-shape-generator': 'Create CSS shapes — circles, triangles, trapezoids, and more. Free online CSS shape generator with visual preview. No images, pure CSS.',
    'css-skeleton-loader-generator': 'Generate CSS skeleton screen loading animations. Free online skeleton loader generator for better UX. Customize colors, animation speed, and shapes.',
    'css-specificity': 'Free online CSS specificity calculator. Understand which CSS rules take priority. Visual breakdown of ID, class, and element specificity scores.',
    'css-text-stroke': 'Free online CSS text-stroke generator. Add outline effects to text with customizable width and color. Preview in real-time and copy CSS code.',
    'css-tooltip-generator': 'Create CSS-only tooltips without JavaScript. Free online tooltip generator with position, arrow, and animation options. Copy clean HTML and CSS.',
    'css-transition-generator': 'Generate CSS transition code visually. Free online transition generator with property, duration, timing, and delay controls. See live preview.',
    'css-triangle-generator': 'Create CSS triangles for tooltips, dropdowns, and decorations. Free online CSS triangle generator with direction, size, and color controls.',
    'css-unit-converter': 'Convert between CSS units — px, rem, em, vw, vh, %, pt, cm. Free online CSS unit converter with instant results. Essential for responsive design.',
    'csv-editor': 'Edit CSV files online with our free spreadsheet-like editor. Add, remove, and reorder columns. Sort and filter data. No signup, works in your browser.',
    'csv-to-markdown': 'Free online CSV to Markdown table converter. Transform spreadsheet data into clean Markdown tables. Perfect for README files and documentation.',
    'csv-to-yaml': 'Convert CSV data to YAML format online for free. Transform spreadsheets into structured YAML. Perfect for configuration files and data serialization.',
    'curl-converter': 'Convert cURL commands to Python, JavaScript, Go, and more. Free online cURL converter supporting 20+ languages. Save time on API integration.',
    'data-generator': 'Generate realistic test data online for free. Create names, emails, addresses, phone numbers, and more. Perfect for development and testing.',
    'data-url-converter': 'Convert files to Data URLs (Base64) online for free. Embed images, fonts, and other files directly in HTML/CSS. Instant conversion in your browser.',
    'data-url-generator': 'Generate Data URLs from files online for free. Convert images and other assets to Base64-encoded data URIs. Embed directly in HTML and CSS.',
    'date-calculator': 'Calculate date differences, add/subtract days, and find deadlines. Free online date calculator with business day support. Plan your schedule easily.',
    'device-mockup-generator': 'Generate device mockups for your screenshots. Free online mockup generator for iPhone, Android, laptop, and tablet. Perfect for app presentations.',
    'distance-calculator': 'Calculate distances between cities and coordinates. Free online distance calculator supporting miles and kilometers. Plan your travel routes.',
    'dmarc-checker': 'Check DMARC records for any domain online for free. Verify email authentication and security policies. Essential for domain administrators.',
    'dns-lookup': 'Perform DNS lookups online for free. Query A, AAAA, MX, CNAME, TXT, and NS records. Essential network diagnostic tool for developers and admins.',
    'docker-compose-generator': 'Free online Docker Compose YAML generator. Build multi-container configurations visually. Select services, ports, volumes, and environment variables.',
    'dotenv-editor': 'Edit .env files online for free. Visual environment variable editor with syntax highlighting. Manage your project configuration securely.',
    'drawing-board': 'Free online drawing board with brush, eraser, shapes, and color picker. Draw, sketch, and annotate directly in your browser. No signup required.',
    'email-template-generator': 'Create responsive HTML email templates online for free. Drag-and-drop builder with preview. Export clean HTML for your email campaigns.',
    'email-validator': 'Validate email addresses online for free. Check syntax, domain MX records, and disposable email detection. Ensure your email list is clean.',
    'env-file-generator': 'Generate .env configuration files online for free. Create environment variables with descriptions and default values. Perfect for project setup.',
    'excel-to-html': 'Convert Excel spreadsheets to HTML tables online for free. Preserve formatting, colors, and merged cells. Embed tables directly in your website.',
    'fake-data-generator': 'Generate realistic fake data for testing. Free online tool for names, addresses, emails, credit cards, and more. Customizable fields and formats.',
    'fancy-text-generator': 'Convert plain text to fancy Unicode styles. Free online fancy text generator with 50+ font styles. Copy and paste anywhere — social media, bios, chats.',
    'favicon-downloader': 'Download favicons from any website. Free online favicon downloader supporting multiple sizes. Quick and easy favicon extraction tool.',
    'file-encrypt': 'Encrypt files online for free with AES encryption. Secure your documents, images, and data with password protection. All processing in your browser.',
    'file-to-base64': 'Convert any file to Base64 string online for free. Encode images, documents, and binaries to Base64. Instant conversion, no upload required.',
    'font-face-generator': 'Generate CSS @font-face declarations online for free. Upload fonts, customize font-family, weight, and style. Get cross-browser compatible CSS.',
    'font-pairing': 'Free online font pairing tool for web designers. Discover beautiful Google Font combinations. Preview headings and body text together.',
    'font-size-converter': 'Convert font sizes between px, pt, rem, em, and more. Free online font size converter with visual comparison. Perfect for responsive typography.',
    'freelance-tax-calc': 'Calculate freelance and self-employment taxes with our free online calculator. Estimate federal income tax, self-employment tax, and total tax burden.',
    'gitattributes-generator': 'Generate .gitattributes files online for free. Configure line endings, diff behavior, and merge strategies. Essential for cross-platform Git projects.',
    'go-formatter': 'Format and beautify Go (Golang) code online for free. Standardize indentation, alignment, and imports. Follow Go formatting conventions.',
    'gradient-generator': 'Free online CSS gradient generator. Create stunning linear, radial, and conic gradients visually. Copy ready-to-use CSS background code.',
    'graphql-formatter': 'Format and beautify GraphQL queries online for free. Proper indentation, syntax highlighting, and error detection. Clean up messy GraphQL code.',
    'habit-tracker': 'Track your daily habits online for free. Build streaks, set goals, and monitor progress. Simple visual habit tracker to stay consistent.',
    'hash-file-checker': 'Calculate file hashes online for free. Support for MD5, SHA-1, SHA-256, SHA-512. Verify file integrity and detect tampering instantly.',
    'headline-analyzer': 'Analyze headline quality and emotional impact. Free online headline analyzer with sentiment, power words, and length scoring. Improve your titles.',
    'heatmap-generator': 'Create data heatmaps online for free. Upload CSV data to generate color-coded heatmap visualizations. Perfect for analytics and data science.',
    'height-converter': 'Convert heights between feet, inches, centimeters, and meters. Free online height converter with instant results. Quick and accurate.',
    'hex-converter': 'Convert hexadecimal values to decimal, binary, octal, and text. Free online hex converter with instant multi-format conversion.',
    'html-breadcrumb-generator': 'Generate HTML breadcrumb navigation code. Free online breadcrumb generator with schema.org markup. Improve your website navigation and SEO.',
    'html-button-generator': 'Create styled HTML buttons visually. Free online button generator with CSS customization. Generate clean HTML and CSS for call-to-action buttons.',
    'html-dialog-generator': 'Generate HTML dialog and modal code. Free online dialog generator with title, content, and button customization. No JavaScript framework needed.',
    'html-diff': 'Compare HTML code side by side and see differences. Free online HTML diff checker with visual highlighting. Track changes between versions.',
    'html-iframe-generator': 'Generate HTML iframe embed code online for free. Customize width, height, borders, and sandbox attributes. Preview your iframe before copying.',
    'html-image-map-generator': 'Create HTML image maps with clickable areas. Free online image map generator with visual editor. Define rectangles, circles, and polygons easily.',
    'html-stripper': 'Strip HTML tags from text online for free. Remove all HTML formatting and extract clean plain text. Perfect for content migration and cleaning.',
    'html-to-docx': 'Convert HTML to Word documents online for free. Preserve formatting, tables, and images. Download as .docx file ready for Microsoft Word.',
    'html-validator': 'Validate HTML code for errors and warnings. Free online HTML validator checking against W3C standards. Find and fix markup issues.',
    'html-wysiwyg-editor': 'Free online WYSIWYG HTML editor with rich text formatting. Bold, italic, lists, tables, and more. Export clean HTML instantly.',
    'image-batch-resizer': 'Resize multiple images at once online for free. Batch resize by dimensions or percentage. Maintain aspect ratio. Perfect for photographers.',
    'image-comparison-slider': 'Create before-and-after image comparison sliders. Free online tool with draggable slider. Perfect for photo editing portfolios and product demos.',
    'image-invert': 'Free online image inverter tool. Invert image colors with one click. Create negative photo effects instantly in your browser.',
    'image-round-corners': 'Round image corners online for free. Adjust corner radius visually and download the result. Perfect for avatars, thumbnails, and UI elements.',
    'image-tint-effect': 'Apply tint and color overlay effects to images. Free online image tint tool with color picker. Create Instagram-style filters instantly.',
    'image-to-icon': 'Free online image to ICO icon converter. Convert PNG, JPG to favicon format. Multiple sizes supported. Perfect for website favicons.',
    'image-to-text': 'Free online image to text converter using OCR. Extract text from images, screenshots, and scanned documents. Copy or download recognized text.',
    'ini-to-json': 'Convert INI configuration files to JSON format. Free online INI to JSON converter with instant results. Perfect for config file migration.',
    'investment-calculator': 'Calculate investment returns with compound interest. Free online investment calculator projecting growth over time. Plan your financial future.',
    'isbn-validator': 'Validate ISBN-10 and ISBN-13 numbers online for free. Check checksum, format, and validity. Essential for publishers, libraries, and booksellers.',
    'java-formatter': 'Format and beautify Java code online for free. Proper indentation, bracket alignment, and import organization. Clean up messy Java source code.',
    'javascript-playground': 'Free online JavaScript playground with live preview. Write, run, and test JavaScript code instantly. Console output and error highlighting.',
    'js-beautifier': 'Beautify and format JavaScript code online for free. Clean indentation, semicolons, and spacing. Make minified code readable again.',
    'js-obfuscator': 'Obfuscate JavaScript code to protect your source. Free online JS obfuscator with multiple protection levels. Make your code harder to reverse-engineer.',
    'json-escape': 'Escape and unescape JSON strings online for free. Handle special characters, quotes, and backslashes. Essential for JSON data processing.',
    'json-generator': 'Generate mock JSON data for API testing and development. Free online JSON data generator with customizable fields, arrays, and nested objects.',
    'json-ld-generator': 'Generate JSON-LD structured data for SEO. Free online schema markup generator for articles, products, events, and more. Improve search visibility.',
    'json-patch': 'Apply JSON Patch operations (RFC 6902) online for free. Add, remove, replace, and move JSON properties. Visual diff of changes.',
    'json-schema-diff': 'Free online JSON Schema diff tool. Compare two JSON schemas and see added, removed, and changed properties. Essential for API versioning.',
    'json-schema-to-typescript': 'Convert JSON Schema to TypeScript interfaces online for free. Generate type-safe TypeScript code from your JSON schemas. Save development time.',
    'json-to-html-table': 'Convert JSON data to HTML tables online for free. Visual table builder with nested object support. Generate clean, responsive HTML table code.',
    'json-to-protobuf': 'Convert JSON to Protocol Buffers schema online for free. Generate .proto files from JSON data structures. Perfect for gRPC and microservices.',
    'json-to-swift': 'Free online JSON to Swift struct/codable converter. Generate Swift models from JSON data. Perfect for iOS and macOS app development.',
    'json-to-typescript': 'Free online JSON to TypeScript interface generator. Convert JSON data to type-safe TypeScript interfaces instantly.',
    'jwt-encoder': 'Encode and decode JWT tokens online for free. Create JSON Web Tokens with custom payloads and verify signatures. Essential for API authentication.',
    'kaomoji-generator': 'Browse 500+ Japanese kaomoji emoticons. Free online kaomoji generator organized by emotion. Copy and paste cute text faces anywhere.',
    'keycode-finder': 'Find keyboard key codes online for free. Press any key to see its keyCode, code, and key properties. Essential for JavaScript developers.',
    'kubernetes-yaml-generator': 'Generate Kubernetes YAML manifests online for free. Create deployment, service, and configmap configurations visually. No kubectl required.',
    'lcm-gcd-calculator': 'Calculate LCM and GCD of numbers online for free. Least Common Multiple and Greatest Common Divisor with step-by-step solutions.',
    'less-to-css': 'Compile Less CSS to standard CSS online for free. Convert Less variables, mixins, and nesting to browser-ready CSS. Instant conversion.',
    'line-counter': 'Count lines, words, and characters in your text. Free online line counter with real-time statistics. Essential for code and document analysis.',
    'lucky-number-generator': 'Generate lucky numbers for lottery, games, and more. Free online lucky number generator with customizable range and count.',
    'luhn-checker': 'Validate credit card and ID numbers with the Luhn algorithm. Free online Luhn checker for payment processing and data validation.',
    'meal-planner': 'Plan your weekly meals online for free. Organize breakfast, lunch, and dinner with our simple meal planner. Build healthy eating habits.',
    'meta-tag-analyzer': 'Analyze meta tags of any website. Free online meta tag analyzer checking title, description, OG tags, and more. Improve your SEO.',
    'morse-code-converter': 'Convert text to Morse code and decode Morse to text. Free online Morse code translator with audio playback. Learn and practice Morse code.',
    'morse-code': 'Free online Morse code translator. Convert text to Morse code and decode Morse signals back to text. With audio playback for learning.',
    'morse-to-text': 'Free online Morse code decoder. Convert Morse code dots and dashes back to readable text. Quick and accurate decoding.',
    'mouse-tester': 'Test your mouse buttons, scroll wheel, and movement. Free online mouse tester to diagnose hardware issues. Check click registration and double-click.',
    'neon-text-generator': 'Create glowing neon text effects online for free. Customize colors, glow intensity, and font. Generate CSS neon text for your website.',
    'network-speed-test': 'Test your internet connection speed online for free. Measure download, upload speed, and latency. Quick browser-based speed test.',
    'neumorphism-generator': 'Generate neumorphic UI elements with CSS. Free online neumorphism generator with shadow, color, and shape controls. Create soft UI designs.',
    'nginx-config-validator': 'Validate Nginx configuration files online for free. Check syntax errors, test server blocks, and verify location directives before deployment.',
    'noise-texture-generator': 'Generate SVG noise textures for your designs. Free online noise texture generator with adjustable opacity and scale. Perfect for backgrounds.',
    'npm-dependency-analyzer': 'Analyze npm package dependencies online for free. Check package.json for outdated, vulnerable, or conflicting dependencies.',
    'number-to-words-converter': 'Convert numbers to words in English. Free online number to words converter supporting up to billions. Perfect for checks, invoices, and legal documents.',
    'og-meta-tag-generator': 'Generate Open Graph meta tags for social media sharing. Free online OG tag generator with preview. Optimize how your content appears on Facebook and Twitter.',
    'online-stopwatch': 'Free online stopwatch with lap timing and split tracking. Start, stop, and reset with keyboard shortcuts. Accurate to milliseconds.',
    'open-graph-generator': 'Generate Open Graph meta tags for better social sharing. Free online OG generator with title, description, and image preview. Boost social media engagement.',
    'pdf-reader': 'View PDF files online for free in your browser. No download or installation needed. Read, zoom, and navigate PDF documents easily.',
    'photo-frame': 'Add decorative frames to your photos online for free. Choose from multiple frame styles and colors. Perfect for social media and profile pictures.',
    'php-formatter': 'Format and beautify PHP code online for free. Proper indentation, bracket alignment, and spacing. Clean up messy PHP source code instantly.',
    'pig-latin': 'Translate English to Pig Latin and back. Free online Pig Latin translator with instant conversion. Fun language tool for all ages.',
    'pixel-art-maker': 'Free online pixel art maker and editor. Draw pixel art with grid-based canvas. Choose colors, draw, and export your pixel creations.',
    'png-to-pdf': 'Convert PNG images to PDF documents online for free. Combine multiple images into one PDF. No quality loss, instant download.',
    'port-scanner': 'Scan open ports on any IP address or domain. Free online port scanner checking common service ports. Essential network security tool.',
    'postcss-config-generator': 'Generate PostCSS configuration files online for free. Select plugins like Autoprefixer, CSS Nano, and more. Visual config builder for your build pipeline.',
    'prime-number-checker': 'Check if a number is prime and find prime factors. Free online prime number calculator with factorization. Learn number theory interactively.',
    'protobuf-to-json': 'Convert Protocol Buffers to JSON format online for free. Decode protobuf messages and view structured data. Perfect for gRPC debugging.',
    'pwa-manifest-generator': 'Generate PWA manifest.json for progressive web apps. Free online manifest generator with icons, theme color, and display mode settings.',
    'random-name-picker': 'Pick random names from your list for drawings and giveaways. Free online random name picker with spinning wheel animation. Fair and fun.',
    'random-team-generator': 'Split people into random teams online for free. Enter names and team count to generate balanced groups. Perfect for games and activities.',
    'readability-checker': 'Check text readability scores online for free. Flesch-Kincaid, Gunning Fog, and SMOG indices. Ensure your content is at the right reading level.',
    'remove-empty-lines': 'Remove empty and blank lines from text online for free. Clean up messy text, code, and data. Instant processing in your browser.',
    'resolution-calculator': 'Calculate screen resolution aspect ratios and dimensions. Free online resolution calculator for video, displays, and responsive design.',
    'ring-size-converter': 'Convert ring sizes between US, UK, EU, and Asian standards. Free online ring size converter with measurement guide. Find your perfect fit.',
    'rot13-converter': 'Encode and decode text with ROT13 cipher online for free. Classic letter substitution cipher. Instant encoding/decoding with one click.',
    'rot13-encoder': 'Encode and decode text with ROT13 cipher online for free. Simple letter rotation cipher. Perfect for hiding spoilers and puzzles.',
    'rust-formatter': 'Format and beautify Rust code online for free. Apply rustfmt-style formatting with proper indentation and spacing. Clean up Rust source code.',
    'security': 'Free online security tools — password generators, hash calculators, encryption tools, and more. Keep your data safe with browser-based utilities.',
    'semver-compare': 'Free online semantic version comparator. Compare semver versions and check ranges. Essential for package management and dependency resolution.',
    'sentence-case-converter': 'Convert text to sentence case, title case, uppercase, and lowercase. Free online case converter with instant results. Fix text formatting fast.',
    'seo-analyzer': 'Analyze webpage SEO factors online for free. Check meta tags, headings, keywords, and content quality. Get actionable recommendations.',
    'shoe-size-converter': 'Convert shoe sizes between US, UK, EU, and Asian standards. Free online shoe size converter for men, women, and children.',
    'small-text-generator': 'Generate small text and superscript Unicode characters. Free online small text generator for social media bios, comments, and creative formatting.',
    'sql-formatter': 'Format and beautify SQL queries online for free. Proper indentation, keyword capitalization, and alignment. Support for MySQL, PostgreSQL, and more.',
    'sql-migration-generator': 'Generate SQL migration scripts online for free. Create table schemas, alter statements, and seed data. Perfect for database version control.',
    'square-footage-calculator': 'Calculate square footage and area of rooms and spaces. Free online square footage calculator with instant results. Perfect for real estate and renovation.',
    'ssh-key-generator': 'Generate SSH key pairs (RSA, Ed25519, ECDSA) online for free. Create public and private keys for secure server access. All processing in browser.',
    'stopwatch': 'Free online stopwatch with millisecond precision. Start, stop, lap, and reset with simple controls. Perfect for timing sports and activities.',
    'sudoku-solver': 'Solve Sudoku puzzles online for free. Enter known numbers and get the complete solution instantly. Supports all difficulty levels.',
    'svg-color-changer': 'Change colors in SVG files online for free. Upload your SVG and recolor any element. Perfect for icon customization and branding.',
    'svg-filter-generator': 'Generate SVG filters for visual effects. Free online SVG filter generator with blur, shadow, and color matrix options. Create stunning SVG graphics.',
    'svg-text-path-generator': 'Generate SVG text along curved paths. Free online tool to create text following circles, waves, and custom paths. Perfect for logo design.',
    'svg-to-data-uri': 'Convert SVG files to Data URIs for inline embedding. Free online SVG to Data URI converter. Embed SVG directly in HTML and CSS.',
    'svg-to-font': 'Convert SVG icons to icon font files online for free. Generate TTF/WOFF font from your SVG collection. Perfect for web and app development.',
    'svg-to-jsx': 'Free online SVG to JSX/React component converter. Transform SVG markup into React-ready JSX components instantly.',
    'svg-wave-generator': 'Create beautiful SVG wave patterns online for free. Customize amplitude, frequency, and colors. Generate smooth wave graphics for your designs.',
    'swot-analysis-generator': 'Generate SWOT analysis diagrams online for free. Identify strengths, weaknesses, opportunities, and threats. Perfect for business planning.',
    'tailwind-shadow-generator': 'Generate Tailwind CSS shadow utilities online for free. Visual shadow builder with color, blur, and spread controls. Copy Tailwind classes instantly.',
    'tax-calculator': 'Calculate China individual income tax for 2026. Free online tax calculator with progressive rate brackets. Estimate your take-home pay accurately.',
    'text-analysis': 'Analyze text for word count, character count, reading time, and more. Free online text analysis tool with detailed statistics.',
    'text-analyzer': 'Analyze text with detailed statistics online for free. Word count, character count, reading time, and sentiment analysis in real-time.',
    'text-diff': 'Free online text diff comparison tool. Compare two texts side by side and highlight differences. Perfect for writers and developers.',
    'text-indentation-fixer': 'Fix inconsistent text indentation online for free. Auto-detect and normalize tabs and spaces. Clean up your code and documents.',
    'text-normalizer': 'Normalize text formatting online for free. Standardize line endings, whitespace, and Unicode characters. Clean text for databases and APIs.',
    'text-splitter': 'Split text into chunks by character count, word count, or delimiter. Free online text splitter for processing large texts.',
    'text-to-braille': 'Convert text to Braille characters online for free. Support for Grade 1 English Braille. Perfect for accessibility and learning.',
    'text-to-yaml': 'Convert text data to YAML format online for free. Transform structured text into clean YAML. Perfect for configuration and data serialization.',
    'time-calculator': 'Calculate time differences, add and subtract hours and minutes. Free online time calculator for scheduling and time tracking.',
    'timeline-generator': 'Create visual timelines online for free. Add events with dates and descriptions. Perfect for project planning and history presentations.',
    'timestamp-converter': 'Convert Unix timestamps to human-readable dates and vice versa. Free online timestamp converter supporting seconds and milliseconds.',
    'token-counter': 'Count AI model tokens for GPT-4, GPT-3.5, and Claude. Free online token counter to estimate API costs and prompt length.',
    'toml-to-yaml': 'Convert TOML configuration files to YAML format. Free online TOML to YAML converter with instant results.',
    'tsconfig-generator': 'Generate TypeScript tsconfig.json files online for free. Configure compiler options, paths, and strict mode. Visual config builder.',
    'tsv-to-csv': 'Convert TSV files to CSV format online for free. Tab-separated to comma-separated conversion. Perfect for data processing and Excel import.',
    'uuid-generator': 'Generate UUID v4 identifiers online for free. Create unique universal IDs for databases, APIs, and distributed systems.',
    'video-speed-controller': 'Control video playback speed online for free. Adjust speed from 0.25x to 4x. Perfect for learning, podcasts, and content review.',
    'volume-calculator': 'Calculate volumes of 3D shapes — cubes, spheres, cylinders, and more. Free online volume calculator with instant results.',
    'webhook-tester': 'Test webhooks online for free. Send and inspect HTTP requests with custom payloads. Perfect for API development and debugging.',
    'white-noise-generator': 'Generate white noise, pink noise, and brown noise online for free. Perfect for sleep, focus, and relaxation. Adjustable volume and tone.',
    'whois-lookup': 'Free online WHOIS domain lookup tool. Check domain registration details, expiration dates, and registrar information.',
    'word-counter': 'Count words, characters, and paragraphs online for free. Real-time word counter with detailed text statistics. Perfect for writers and editors.',
    'word-scramble-solver': 'Solve word scramble puzzles online for free. Enter scrambled letters to find all possible words. Perfect for word games and brain training.',
    'xml-to-csv': 'Free online XML to CSV converter. Transform XML data into spreadsheet-ready CSV format. Perfect for data analysis and Excel import.',
    'year-progress': 'Track the year progress with a visual progress bar. Free online year progress tracker showing percentage, days elapsed, and days remaining.',
    'youtube-tag-generator': 'Generate optimized YouTube tags for better video visibility. Free online YouTube tag generator with keyword suggestions and trending tags.',
}

def fix_file(filepath):
    """Fix meta description for a single file."""
    dirname = os.path.basename(os.path.dirname(filepath))
    
    # Try to get a known description first
    new_desc = TOOL_DESCRIPTIONS.get(dirname)
    
    if not new_desc:
        # Fall back to existing description, extend it
        existing = get_existing_desc(filepath)
        if existing:
            # Strip trailing "..." and extend to proper length
            existing = re.sub(r'\.\.\.?$', '', existing).strip()
            if len(existing) < 120:
                # Use h1 for context
                h1 = get_h1(filepath)
                if h1:
                    new_desc = f"{existing} Free online {h1.lower()} tool with instant results. No registration required, works directly in your browser."
                else:
                    new_desc = existing
            else:
                new_desc = existing
        else:
            return False
    
    # Ensure 140-160 chars
    if len(new_desc) < 120:
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace meta description using string replace (avoid re issues with backslashes)
    import html
    safe_desc = html.escape(new_desc, quote=False)
    
    new_content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"',
        lambda m: f'<meta name="description" content="{safe_desc}"',
        content
    )
    
    # Also fix OG description if it exists
    new_content = re.sub(
        r'<meta\s+property="og:description"\s+content="[^"]*"',
        lambda m: f'<meta property="og:description" content="{safe_desc}"',
        new_content
    )
    
    # Also fix twitter description if it exists
    new_content = re.sub(
        r'<meta\s+name="twitter:description"\s+content="[^"]*"',
        lambda m: f'<meta name="twitter:description" content="{safe_desc}"',
        new_content
    )
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    import glob
    files = glob.glob(os.path.join(BASE, 'en/*/index.html'))
    fixed = 0
    for f in sorted(files):
        if fix_file(f):
            fixed += 1
            print(f"Fixed: {f}")
    
    print(f"\nTotal fixed: {fixed}/{len(files)}")

if __name__ == '__main__':
    main()
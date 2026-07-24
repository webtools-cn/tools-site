#!/usr/bin/env python3
"""批量创建10个新工具 - 中英文双语"""
import os

BASE_DIR = "/home/chison/tools-site"

TOOLS = [
    {
        "slug": "prime-number",
        "title_cn": "质数检查器",
        "title_en": "Prime Number Checker",
        "desc_cn": "免费在线质数检查器，支持单数质数判断、区间质数生成。适合数学学习、密码学基础研究，无需注册。",
        "desc_en": "Free online prime number checker. Check if a number is prime, generate prime numbers in a range. Great for math learning and cryptography basics. No signup required.",
        "emoji": "🔢",
        "faq": [
            {"q": "什么是质数？", "a": "质数（素数）是大于1的自然数，且只能被1和自身整除。例如：2、3、5、7、11、13等都是质数。"},
            {"q": "最大的质数是多少？", "a": "目前已知的最大质数有数千万位。本工具支持检查100亿以内的数是否为质数，足以满足日常使用。"},
            {"q": "1是质数吗？", "a": "不是。根据数学定义，质数必须大于1。1既不是质数也不是合数。"},
        ],
        "faq_en": [
            {"q": "What is a prime number?", "a": "A prime number is a natural number greater than 1 that is only divisible by 1 and itself. Examples: 2, 3, 5, 7, 11, 13."},
            {"q": "What is the largest prime number?", "a": "The largest known prime has tens of millions of digits. This tool supports checking numbers up to 10 billion."},
            {"q": "Is 1 a prime number?", "a": "No. By mathematical definition, prime numbers must be greater than 1. 1 is neither prime nor composite."},
        ],
    },
    {
        "slug": "fibonacci",
        "title_cn": "斐波那契数列生成器",
        "title_en": "Fibonacci Sequence Generator",
        "desc_cn": "免费在线斐波那契数列生成器，生成指定长度的斐波那契数列。适合数学教学、算法学习、编程练习，无需注册。",
        "desc_en": "Free online Fibonacci sequence generator. Generate Fibonacci numbers of specified length. Perfect for math teaching, algorithm learning, and programming practice. No signup required.",
        "emoji": "🌀",
        "faq": [
            {"q": "什么是斐波那契数列？", "a": "斐波那契数列以0和1开始，后续每个数都是前两个数之和：0, 1, 1, 2, 3, 5, 8, 13, 21... 由意大利数学家斐波那契在1202年提出。"},
            {"q": "斐波那契数列有什么应用？", "a": "广泛应用于自然界（向日葵种子排列、贝壳螺旋）、金融（斐波那契回调）、计算机科学（斐波那契堆、动态规划）等领域。"},
            {"q": "可以生成多少项？", "a": "本工具支持生成最多100项。由于斐波那契数增长极快，超过100项后数值会非常大。"},
        ],
        "faq_en": [
            {"q": "What is the Fibonacci sequence?", "a": "The Fibonacci sequence starts with 0 and 1, and each subsequent number is the sum of the two preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, 21... It was introduced by Italian mathematician Fibonacci in 1202."},
            {"q": "What are applications of Fibonacci?", "a": "Widely found in nature (sunflower seed patterns, shell spirals), finance (Fibonacci retracements), and computer science (Fibonacci heaps, dynamic programming)."},
            {"q": "How many terms can I generate?", "a": "This tool supports up to 100 terms. Fibonacci numbers grow extremely fast, so values beyond 100 terms become very large."},
        ],
    },
    {
        "slug": "factorial",
        "title_cn": "阶乘计算器",
        "title_en": "Factorial Calculator",
        "desc_cn": "免费在线阶乘计算器，计算任意正整数的阶乘（n!）。适合数学学习、排列组合计算、编程练习，无需注册。",
        "desc_en": "Free online factorial calculator. Calculate the factorial (n!) of any positive integer. Great for math learning, permutation and combination calculations. No signup required.",
        "emoji": "✖️",
        "faq": [
            {"q": "什么是阶乘？", "a": "阶乘用n!表示，等于1×2×3×...×n。例如：5! = 5×4×3×2×1 = 120。特别地，0! = 1。"},
            {"q": "阶乘有什么用？", "a": "阶乘广泛应用于排列组合（P(n,r)、C(n,r)）、概率论、泰勒级数、算法复杂度分析等领域。"},
            {"q": "能算多大的阶乘？", "a": "本工具支持计算0到1000的阶乘。超过170!后结果会非常大，但使用BigInt可精确计算。"},
        ],
        "faq_en": [
            {"q": "What is a factorial?", "a": "Factorial, denoted n!, equals 1×2×3×...×n. For example: 5! = 5×4×3×2×1 = 120. By convention, 0! = 1."},
            {"q": "What are factorials used for?", "a": "Factorials are widely used in permutations and combinations, probability theory, Taylor series, and algorithm complexity analysis."},
            {"q": "How large a factorial can I calculate?", "a": "This tool supports 0 to 1000. Results beyond 170! are extremely large but can be precisely calculated using BigInt."},
        ],
    },
    {
        "slug": "gcd-calculator",
        "title_cn": "最大公约数计算器",
        "title_en": "GCD Calculator",
        "desc_cn": "免费在线最大公约数（GCD）计算器，使用欧几里得算法快速计算。支持批量计算多个数的最大公约数，无需注册。",
        "desc_en": "Free online GCD (Greatest Common Divisor) calculator using the Euclidean algorithm. Support batch calculation of GCD for multiple numbers. No signup required.",
        "emoji": "➗",
        "faq": [
            {"q": "什么是最大公约数？", "a": "最大公约数（GCD）是能同时整除所有给定数的最大正整数。例如：12和18的GCD是6。"},
            {"q": "使用什么算法？", "a": "使用欧几里得算法（辗转相除法），是计算GCD最高效的经典算法，时间复杂度O(log min(a,b))。"},
            {"q": "支持多少个数字？", "a": "支持2到20个数字同时计算。只需用逗号或空格分隔数字即可。"},
        ],
        "faq_en": [
            {"q": "What is GCD?", "a": "The Greatest Common Divisor (GCD) is the largest positive integer that divides all given numbers without remainder. Example: GCD(12,18) = 6."},
            {"q": "What algorithm is used?", "a": "The Euclidean algorithm, the most efficient classical algorithm for computing GCD, with time complexity O(log min(a,b))."},
            {"q": "How many numbers can I input?", "a": "Supports 2 to 20 numbers. Simply separate numbers with commas or spaces."},
        ],
    },
    {
        "slug": "lcm-calculator",
        "title_cn": "最小公倍数计算器",
        "title_en": "LCM Calculator",
        "desc_cn": "免费在线最小公倍数（LCM）计算器，基于GCD快速计算。支持批量计算多个数的最小公倍数，无需注册。",
        "desc_en": "Free online LCM (Least Common Multiple) calculator based on GCD. Support batch calculation for multiple numbers. No signup required.",
        "emoji": "🔗",
        "faq": [
            {"q": "什么是最小公倍数？", "a": "最小公倍数（LCM）是能被所有给定数整除的最小正整数。例如：4和6的LCM是12。"},
            {"q": "如何计算LCM？", "a": "利用公式 LCM(a,b) = |a×b| / GCD(a,b)。先计算最大公约数，再计算最小公倍数，高效准确。"},
            {"q": "支持多少个数字？", "a": "支持2到20个数字同时计算。用逗号或空格分隔数字即可。"},
        ],
        "faq_en": [
            {"q": "What is LCM?", "a": "The Least Common Multiple (LCM) is the smallest positive integer that is divisible by all given numbers. Example: LCM(4,6) = 12."},
            {"q": "How is LCM calculated?", "a": "Using the formula LCM(a,b) = |a×b| / GCD(a,b). First compute GCD, then derive LCM — efficient and accurate."},
            {"q": "How many numbers can I input?", "a": "Supports 2 to 20 numbers. Separate them with commas or spaces."},
        ],
    },
    {
        "slug": "text-to-list",
        "title_cn": "文本转列表",
        "title_en": "Text to List",
        "desc_cn": "免费在线文本转列表工具，支持按行、逗号、空格等多种分隔符转换。可添加编号、引号包裹，一键复制。无需注册。",
        "desc_en": "Free online text to list converter. Convert text using various delimiters (newline, comma, space). Add numbering, quote wrapping, one-click copy. No signup required.",
        "emoji": "📋",
        "faq": [
            {"q": "支持哪些分隔符？", "a": "支持换行、逗号、空格、分号、制表符、自定义分隔符等多种方式，灵活适配各种输入格式。"},
            {"q": "可以添加编号吗？", "a": "可以。支持数字编号（1. 2. 3.）、字母编号（a. b. c.）、项目符号（• -）等多种格式。"},
            {"q": "数据安全吗？", "a": "完全安全。所有转换在浏览器本地完成，数据不会上传到任何服务器。"},
        ],
        "faq_en": [
            {"q": "What delimiters are supported?", "a": "Newline, comma, space, semicolon, tab, and custom delimiters — flexible for various input formats."},
            {"q": "Can I add numbering?", "a": "Yes. Support numeric (1. 2. 3.), alphabetic (a. b. c.), and bullet (• -) formats."},
            {"q": "Is my data safe?", "a": "Completely safe. All conversion happens locally in your browser — no data is uploaded to any server."},
        ],
    },
    {
        "slug": "list-deduplicator",
        "title_cn": "列表去重工具",
        "title_en": "List Deduplicator",
        "desc_cn": "免费在线列表去重工具，快速移除重复项，保留唯一值。支持大小写敏感/不敏感、保留空行等选项。无需注册。",
        "desc_en": "Free online list deduplication tool. Quickly remove duplicates and keep unique values. Case-sensitive/insensitive options, preserve empty lines. No signup required.",
        "emoji": "🧹",
        "faq": [
            {"q": "去重如何工作？", "a": "工具逐行读取输入内容，使用哈希集合检测重复项，只保留首次出现的唯一值，保持原始顺序。"},
            {"q": "大小写敏感是什么意思？", "a": "开启大小写敏感时，'Apple'和'apple'被视为不同；关闭时两者被视为相同，只保留第一次出现的。"},
            {"q": "数据安全吗？", "a": "完全安全。所有去重处理在浏览器本地完成，数据不会上传到任何服务器。"},
        ],
        "faq_en": [
            {"q": "How does deduplication work?", "a": "The tool reads input line by line, uses a hash set to detect duplicates, keeps only the first occurrence, and preserves original order."},
            {"q": "What does case sensitivity mean?", "a": "When enabled, 'Apple' and 'apple' are treated as different. When disabled, they're treated as the same."},
            {"q": "Is my data safe?", "a": "Completely safe. All processing is done locally in your browser — no data is uploaded."},
        ],
    },
    {
        "slug": "list-comparer",
        "title_cn": "列表比较工具",
        "title_en": "List Comparer",
        "desc_cn": "免费在线列表比较工具，快速找出两个列表的交集、差集、并集。支持文本列表对比分析，无需注册。",
        "desc_en": "Free online list comparison tool. Quickly find intersection, difference, and union of two lists. Perfect for text list analysis. No signup required.",
        "emoji": "🔄",
        "faq": [
            {"q": "支持哪些比较模式？", "a": "支持交集（两列表共有）、差集A-B（A有B无）、差集B-A（B有A无）、并集（两列表合并去重）四种模式。"},
            {"q": "比较结果如何排序？", "a": "默认保持原始顺序。也可以选择按字母排序或按出现频率排序。"},
            {"q": "数据安全吗？", "a": "完全安全。所有比较处理在浏览器本地完成，数据不会上传到任何服务器。"},
        ],
        "faq_en": [
            {"q": "What comparison modes are supported?", "a": "Intersection (shared), Difference A-B (in A not B), Difference B-A (in B not A), Union (combined unique)."},
            {"q": "How are results sorted?", "a": "Default preserves original order. Also supports alphabetical sorting or frequency-based sorting."},
            {"q": "Is my data safe?", "a": "Completely safe. All comparison is done locally in your browser — no data is uploaded."},
        ],
    },
    {
        "slug": "screen-resolution",
        "title_cn": "屏幕分辨率检测",
        "title_en": "Screen Resolution Checker",
        "desc_cn": "免费在线屏幕分辨率检测工具，实时显示屏幕尺寸、分辨率、像素比、视口大小。适合前端开发者和设计师使用，无需注册。",
        "desc_en": "Free online screen resolution checker. Real-time display of screen size, resolution, pixel ratio, and viewport dimensions. Perfect for frontend developers and designers. No signup required.",
        "emoji": "🖥️",
        "faq": [
            {"q": "什么是设备像素比？", "a": "设备像素比（DPR）是物理像素与CSS像素的比值。Retina屏幕通常为2，部分高端手机可达3。"},
            {"q": "分辨率和视口有什么区别？", "a": "屏幕分辨率是物理像素（如1920×1080），视口是浏览器可见区域（减去任务栏、书签栏等），通常小于分辨率。"},
            {"q": "为什么要检测这些信息？", "a": "前端开发者需要根据屏幕参数做响应式设计；设计师需要了解目标用户的设备特征；用户购买显示器时也需要参考。"},
        ],
        "faq_en": [
            {"q": "What is device pixel ratio?", "a": "DPR is the ratio of physical pixels to CSS pixels. Retina screens typically have DPR=2, some high-end phones reach 3."},
            {"q": "What's the difference between resolution and viewport?", "a": "Screen resolution is physical pixels (e.g., 1920×1080), viewport is the browser's visible area (minus taskbars, bookmarks), usually smaller."},
            {"q": "Why check this info?", "a": "Frontend developers need screen parameters for responsive design; designers need target user device characteristics; monitor buyers reference it."},
        ],
    },
    {
        "slug": "device-info",
        "title_cn": "设备信息查看器",
        "title_en": "Device Info Viewer",
        "desc_cn": "免费在线设备信息查看器，一键查看浏览器、操作系统、CPU、内存、网络、电池等详细信息。无需注册。",
        "desc_en": "Free online device information viewer. View browser, OS, CPU, memory, network, battery details with one click. No signup required.",
        "emoji": "📱",
        "faq": [
            {"q": "能查看哪些信息？", "a": "可以查看浏览器名称版本、操作系统、CPU核心数、内存大小、网络类型、电池状态、语言、时区、Cookie/LocalStorage状态等。"},
            {"q": "隐私安全吗？", "a": "完全安全。所有信息仅在您的浏览器中显示，不会上传到任何服务器。部分信息（如电池）需要您授权才能获取。"},
            {"q": "为什么有些信息显示'不可用'？", "a": "某些API（如电池状态、网络信息）需要浏览器支持。如果浏览器不支持或用户未授权，则会显示不可用。"},
        ],
        "faq_en": [
            {"q": "What information can I view?", "a": "Browser name/version, OS, CPU cores, RAM, network type, battery status, language, timezone, Cookie/LocalStorage status, and more."},
            {"q": "Is my privacy safe?", "a": "Completely safe. All information is displayed only in your browser. Some info (like battery) requires your permission."},
            {"q": "Why do some items show 'Unavailable'?", "a": "Certain APIs (battery, network info) require browser support. If unsupported or permission denied, they show as unavailable."},
        ],
    },
]

# Pre-built JS for each tool (keyed by slug, separate for CN/EN)
TOOL_JS = {}

# prime-number
TOOL_JS["prime-number"] = {
    "zh": """function isPrime(n){if(n<2)return false;if(n===2)return true;if(n%2===0)return false;for(var i=3;i*i<=n;i+=2)if(n%i===0)return false;return true;}
document.getElementById('checkBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('numInput').value);if(isNaN(n)||n<0){document.getElementById('checkResult').textContent='请输入有效数字';return;}document.getElementById('checkResult').textContent=n+' '+(isPrime(n)?'是质数 ✓':'不是质数 ✗');});
document.getElementById('genBtn').addEventListener('click',function(){var s=parseInt(document.getElementById('rangeStart').value);var e=parseInt(document.getElementById('rangeEnd').value);if(isNaN(s)||isNaN(e)||s>e){document.getElementById('rangeResult').textContent='请输入有效范围';return;}if(e-s>1000000){document.getElementById('rangeResult').textContent='范围太大，请缩小到100万以内';return;}var primes=[];for(var i=Math.max(2,s);i<=e;i++)if(isPrime(i))primes.push(i);document.getElementById('rangeResult').textContent=primes.length+' 个质数: '+primes.join(', ');});""",
    "en": """function isPrime(n){if(n<2)return false;if(n===2)return true;if(n%2===0)return false;for(var i=3;i*i<=n;i+=2)if(n%i===0)return false;return true;}
document.getElementById('checkBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('numInput').value);if(isNaN(n)||n<0){document.getElementById('checkResult').textContent='Please enter a valid number';return;}document.getElementById('checkResult').textContent=n+' '+(isPrime(n)?'is prime \\u2713':'is NOT prime \\u2717');});
document.getElementById('genBtn').addEventListener('click',function(){var s=parseInt(document.getElementById('rangeStart').value);var e=parseInt(document.getElementById('rangeEnd').value);if(isNaN(s)||isNaN(e)||s>e){document.getElementById('rangeResult').textContent='Please enter a valid range';return;}if(e-s>1000000){document.getElementById('rangeResult').textContent='Range too large, limit to 1,000,000';return;}var primes=[];for(var i=Math.max(2,s);i<=e;i++)if(isPrime(i))primes.push(i);document.getElementById('rangeResult').textContent=primes.length+' primes: '+primes.join(', ');});""",
}

# fibonacci
TOOL_JS["fibonacci"] = {
    "zh": """document.getElementById('genBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('nInput').value);if(isNaN(n)||n<1||n>100){document.getElementById('result').textContent='请输入1-100之间的数字';return;}var fib=[0n];if(n>1)fib.push(1n);for(var i=2;i<n;i++)fib.push(fib[i-1]+fib[i-2]);document.getElementById('result').textContent=fib.map(function(x,i){return 'F'+i+' = '+x;}).join('\\n');});""",
    "en": """document.getElementById('genBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('nInput').value);if(isNaN(n)||n<1||n>100){document.getElementById('result').textContent='Please enter a number between 1 and 100';return;}var fib=[0n];if(n>1)fib.push(1n);for(var i=2;i<n;i++)fib.push(fib[i-1]+fib[i-2]);document.getElementById('result').textContent=fib.map(function(x,i){return 'F'+i+' = '+x;}).join('\\n');});""",
}

# factorial
TOOL_JS["factorial"] = {
    "zh": """document.getElementById('calcBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('nInput').value);if(isNaN(n)||n<0||n>1000){document.getElementById('result').textContent='请输入0-1000之间的整数';return;}var r=1n;for(var i=2n;i<=BigInt(n);i++)r*=i;document.getElementById('result').textContent=n+'! = '+r.toString();});""",
    "en": """document.getElementById('calcBtn').addEventListener('click',function(){var n=parseInt(document.getElementById('nInput').value);if(isNaN(n)||n<0||n>1000){document.getElementById('result').textContent='Please enter an integer between 0 and 1000';return;}var r=1n;for(var i=2n;i<=BigInt(n);i++)r*=i;document.getElementById('result').textContent=n+'! = '+r.toString();});""",
}

# gcd-calculator
TOOL_JS["gcd-calculator"] = {
    "zh": """function gcd(a,b){a=BigInt(a);b=BigInt(b);while(b!==0n){var t=b;b=a%b;a=t;}return a;}
document.getElementById('calcBtn').addEventListener('click',function(){var raw=document.getElementById('numInput').value.trim();if(!raw){document.getElementById('result').textContent='请输入数字';return;}var nums=raw.split(/[,\\s]+/).map(Number).filter(function(x){return !isNaN(x)&&Number.isInteger(x)&&x>0;});if(nums.length<2){document.getElementById('result').textContent='请至少输入2个正整数';return;}var g=BigInt(nums[0]);for(var i=1;i<nums.length;i++)g=gcd(g,nums[i]);document.getElementById('result').textContent='GCD('+nums.join(', ')+') = '+g.toString();});""",
    "en": """function gcd(a,b){a=BigInt(a);b=BigInt(b);while(b!==0n){var t=b;b=a%b;a=t;}return a;}
document.getElementById('calcBtn').addEventListener('click',function(){var raw=document.getElementById('numInput').value.trim();if(!raw){document.getElementById('result').textContent='Please enter numbers';return;}var nums=raw.split(/[,\\s]+/).map(Number).filter(function(x){return !isNaN(x)&&Number.isInteger(x)&&x>0;});if(nums.length<2){document.getElementById('result').textContent='Please enter at least 2 positive integers';return;}var g=BigInt(nums[0]);for(var i=1;i<nums.length;i++)g=gcd(g,nums[i]);document.getElementById('result').textContent='GCD('+nums.join(', ')+') = '+g.toString();});""",
}

# lcm-calculator
TOOL_JS["lcm-calculator"] = {
    "zh": """function gcd(a,b){a=BigInt(a);b=BigInt(b);while(b!==0n){var t=b;b=a%b;a=t;}return a;}
function lcm(a,b){return (BigInt(a)*BigInt(b))/gcd(a,b);}
document.getElementById('calcBtn').addEventListener('click',function(){var raw=document.getElementById('numInput').value.trim();if(!raw){document.getElementById('result').textContent='请输入数字';return;}var nums=raw.split(/[,\\s]+/).map(Number).filter(function(x){return !isNaN(x)&&Number.isInteger(x)&&x>0;});if(nums.length<2){document.getElementById('result').textContent='请至少输入2个正整数';return;}var l=BigInt(nums[0]);for(var i=1;i<nums.length;i++)l=lcm(l,nums[i]);document.getElementById('result').textContent='LCM('+nums.join(', ')+') = '+l.toString();});""",
    "en": """function gcd(a,b){a=BigInt(a);b=BigInt(b);while(b!==0n){var t=b;b=a%b;a=t;}return a;}
function lcm(a,b){return (BigInt(a)*BigInt(b))/gcd(a,b);}
document.getElementById('calcBtn').addEventListener('click',function(){var raw=document.getElementById('numInput').value.trim();if(!raw){document.getElementById('result').textContent='Please enter numbers';return;}var nums=raw.split(/[,\\s]+/).map(Number).filter(function(x){return !isNaN(x)&&Number.isInteger(x)&&x>0;});if(nums.length<2){document.getElementById('result').textContent='Please enter at least 2 positive integers';return;}var l=BigInt(nums[0]);for(var i=1;i<nums.length;i++)l=lcm(l,nums[i]);document.getElementById('result').textContent='LCM('+nums.join(', ')+') = '+l.toString();});""",
}

# text-to-list
TOOL_JS["text-to-list"] = {
    "zh": """document.getElementById('convertBtn').addEventListener('click',function(){var text=document.getElementById('textInput').value;var delim=document.getElementById('delimiter').value;var num=document.getElementById('numbering').value;var items=[];if(delim==='newline')items=text.split('\\n');else if(delim==='comma')items=text.split(',');else if(delim==='space')items=text.split(/\\s+/);else if(delim==='semicolon')items=text.split(';');else if(delim==='tab')items=text.split('\\t');items=items.map(function(x){return x.trim();}).filter(function(x){return x;});var result='';for(var i=0;i<items.length;i++){var prefix='';if(num==='numeric')prefix=(i+1)+'. ';else if(num==='bullet')prefix='\\u2022 ';else if(num==='dash')prefix='- ';result+=prefix+items[i]+'\\n';}document.getElementById('result').textContent=result||'无内容';});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
    "en": """document.getElementById('convertBtn').addEventListener('click',function(){var text=document.getElementById('textInput').value;var delim=document.getElementById('delimiter').value;var num=document.getElementById('numbering').value;var items=[];if(delim==='newline')items=text.split('\\n');else if(delim==='comma')items=text.split(',');else if(delim==='space')items=text.split(/\\s+/);else if(delim==='semicolon')items=text.split(';');else if(delim==='tab')items=text.split('\\t');items=items.map(function(x){return x.trim();}).filter(function(x){return x;});var result='';for(var i=0;i<items.length;i++){var prefix='';if(num==='numeric')prefix=(i+1)+'. ';else if(num==='bullet')prefix='\\u2022 ';else if(num==='dash')prefix='- ';result+=prefix+items[i]+'\\n';}document.getElementById('result').textContent=result||'No content';});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
}

# list-deduplicator
TOOL_JS["list-deduplicator"] = {
    "zh": """document.getElementById('dedupBtn').addEventListener('click',function(){var text=document.getElementById('textInput').value;var caseSensitive=document.getElementById('caseSensitive').checked;var preserveEmpty=document.getElementById('preserveEmpty').checked;var lines=text.split('\\n');var seen={};var result=[];for(var i=0;i<lines.length;i++){var line=lines[i];if(!preserveEmpty&&line.trim()==='')continue;var key=caseSensitive?line:line.toLowerCase();if(!(key in seen)){seen[key]=true;result.push(line);}}document.getElementById('result').textContent=result.join('\\n')||'无内容';});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
    "en": """document.getElementById('dedupBtn').addEventListener('click',function(){var text=document.getElementById('textInput').value;var caseSensitive=document.getElementById('caseSensitive').checked;var preserveEmpty=document.getElementById('preserveEmpty').checked;var lines=text.split('\\n');var seen={};var result=[];for(var i=0;i<lines.length;i++){var line=lines[i];if(!preserveEmpty&&line.trim()==='')continue;var key=caseSensitive?line:line.toLowerCase();if(!(key in seen)){seen[key]=true;result.push(line);}}document.getElementById('result').textContent=result.join('\\n')||'No content';});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
}

# list-comparer - use keyed approach for the problematic strings
_list_cn_result_template = "项结果:\\n"
_list_en_result_template = " results:\\n"
TOOL_JS["list-comparer"] = {
    "zh": """document.getElementById('compareBtn').addEventListener('click',function(){var a=document.getElementById('listA').value.split('\\n').map(function(x){return x.trim();}).filter(function(x){return x;});var b=document.getElementById('listB').value.split('\\n').map(function(x){return x.trim();}).filter(function(x){return x;});var caseSensitive=document.getElementById('caseSensitive').checked;var mode=document.getElementById('mode').value;if(!caseSensitive){a=a.map(function(x){return x.toLowerCase();});b=b.map(function(x){return x.toLowerCase();});}var setA={},setB={};a.forEach(function(x){setA[x]=true;});b.forEach(function(x){setB[x]=true;});var result=[];if(mode==='intersection'){for(var k in setA)if(setB[k])result.push(k);}else if(mode==='diffAB'){for(var k in setA)if(!setB[k])result.push(k);}else if(mode==='diffBA'){for(var k in setB)if(!setA[k])result.push(k);}else if(mode==='union'){var u={};a.forEach(function(x){u[x]=true;});b.forEach(function(x){u[x]=true;});for(var k in u)result.push(k);}document.getElementById('result').textContent=result.length+' """ + _list_cn_result_template + """'+result.join('\\n');});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
    "en": """document.getElementById('compareBtn').addEventListener('click',function(){var a=document.getElementById('listA').value.split('\\n').map(function(x){return x.trim();}).filter(function(x){return x;});var b=document.getElementById('listB').value.split('\\n').map(function(x){return x.trim();}).filter(function(x){return x;});var caseSensitive=document.getElementById('caseSensitive').checked;var mode=document.getElementById('mode').value;if(!caseSensitive){a=a.map(function(x){return x.toLowerCase();});b=b.map(function(x){return x.toLowerCase();});}var setA={},setB={};a.forEach(function(x){setA[x]=true;});b.forEach(function(x){setB[x]=true;});var result=[];if(mode==='intersection'){for(var k in setA)if(setB[k])result.push(k);}else if(mode==='diffAB'){for(var k in setA)if(!setB[k])result.push(k);}else if(mode==='diffBA'){for(var k in setB)if(!setA[k])result.push(k);}else if(mode==='union'){var u={};a.forEach(function(x){u[x]=true;});b.forEach(function(x){u[x]=true;});for(var k in u)result.push(k);}document.getElementById('result').textContent=result.length+'""" + _list_en_result_template + """'+result.join('\\n');});
document.getElementById('copyBtn').addEventListener('click',function(){var t=document.getElementById('result').textContent;if(t)copyText(t);});""",
}

# screen-resolution
_scr_cn_na = "不支持"
_scr_en_na = "N/A"
TOOL_JS["screen-resolution"] = {
    "zh": """function update(){document.getElementById('resolution').textContent=screen.width+' x '+screen.height;document.getElementById('availRes').textContent=screen.availWidth+' x '+screen.availHeight;document.getElementById('viewport').textContent=window.innerWidth+' x '+window.innerHeight;document.getElementById('dpr').textContent=window.devicePixelRatio||1;document.getElementById('colorDepth').textContent=screen.colorDepth+' bit';document.getElementById('orientation').textContent=screen.orientation?screen.orientation.type:'""" + _scr_cn_na + """';}update();window.addEventListener('resize',update);screen.orientation&&screen.orientation.addEventListener('change',update);""",
    "en": """function update(){document.getElementById('resolution').textContent=screen.width+' x '+screen.height;document.getElementById('availRes').textContent=screen.availWidth+' x '+screen.availHeight;document.getElementById('viewport').textContent=window.innerWidth+' x '+window.innerHeight;document.getElementById('dpr').textContent=window.devicePixelRatio||1;document.getElementById('colorDepth').textContent=screen.colorDepth+' bit';document.getElementById('orientation').textContent=screen.orientation?screen.orientation.type:'""" + _scr_en_na + """';}update();window.addEventListener('resize',update);screen.orientation&&screen.orientation.addEventListener('change',update);""",
}

# device-info
_dev_cn_unknown = "未知"
_dev_en_unknown = "Unknown"
_dev_cn_online = "在线"
_dev_cn_offline = "离线"
_dev_en_online = "Online"
_dev_en_offline = "Offline"
_dev_cn_enabled = "已启用"
_dev_cn_disabled = "已禁用"
_dev_en_enabled = "Enabled"
_dev_en_disabled = "Disabled"

TOOL_JS["device-info"] = {
    "zh": """function getBrowser(){var ua=navigator.userAgent;if(ua.indexOf('Firefox')>-1)return 'Firefox '+ua.match(/Firefox\\/(\\d+)/)[1];if(ua.indexOf('Edg')>-1)return 'Edge '+ua.match(/Edg\\/(\\d+)/)[1];if(ua.indexOf('Chrome')>-1)return 'Chrome '+ua.match(/Chrome\\/(\\d+)/)[1];if(ua.indexOf('Safari')>-1)return 'Safari '+ua.match(/Version\\/(\\d+)/)[1];return ua;}
function getOS(){var p=navigator.platform||'';if(p.indexOf('Win')>-1)return 'Windows';if(p.indexOf('Mac')>-1)return 'macOS';if(p.indexOf('Linux')>-1)return 'Linux';if(p.indexOf('Android')>-1)return 'Android';if(p.indexOf('iPhone')>-1||p.indexOf('iPad')>-1)return 'iOS';return p;}
function update(){document.getElementById('browser').textContent=getBrowser();document.getElementById('os').textContent=getOS();document.getElementById('cpu').textContent=navigator.hardwareConcurrency||'""" + _dev_cn_unknown + """';document.getElementById('memory').textContent=navigator.deviceMemory?navigator.deviceMemory+' GB':'""" + _dev_cn_unknown + """';document.getElementById('language').textContent=navigator.language||'""" + _dev_cn_unknown + """';document.getElementById('timezone').textContent=Intl.DateTimeFormat().resolvedOptions().timeZone||'""" + _dev_cn_unknown + """';document.getElementById('online').textContent=navigator.onLine?'""" + _dev_cn_online + """':'""" + _dev_cn_offline + """';document.getElementById('cookies').textContent=navigator.cookieEnabled?'""" + _dev_cn_enabled + """':'""" + _dev_cn_disabled + """';}update();document.getElementById('refreshBtn').addEventListener('click',update);""",
    "en": """function getBrowser(){var ua=navigator.userAgent;if(ua.indexOf('Firefox')>-1)return 'Firefox '+ua.match(/Firefox\\/(\\d+)/)[1];if(ua.indexOf('Edg')>-1)return 'Edge '+ua.match(/Edg\\/(\\d+)/)[1];if(ua.indexOf('Chrome')>-1)return 'Chrome '+ua.match(/Chrome\\/(\\d+)/)[1];if(ua.indexOf('Safari')>-1)return 'Safari '+ua.match(/Version\\/(\\d+)/)[1];return ua;}
function getOS(){var p=navigator.platform||'';if(p.indexOf('Win')>-1)return 'Windows';if(p.indexOf('Mac')>-1)return 'macOS';if(p.indexOf('Linux')>-1)return 'Linux';if(p.indexOf('Android')>-1)return 'Android';if(p.indexOf('iPhone')>-1||p.indexOf('iPad')>-1)return 'iOS';return p;}
function update(){document.getElementById('browser').textContent=getBrowser();document.getElementById('os').textContent=getOS();document.getElementById('cpu').textContent=navigator.hardwareConcurrency||'""" + _dev_en_unknown + """';document.getElementById('memory').textContent=navigator.deviceMemory?navigator.deviceMemory+' GB':'""" + _dev_en_unknown + """';document.getElementById('language').textContent=navigator.language||'""" + _dev_en_unknown + """';document.getElementById('timezone').textContent=Intl.DateTimeFormat().resolvedOptions().timeZone||'""" + _dev_en_unknown + """';document.getElementById('online').textContent=navigator.onLine?'""" + _dev_en_online + """':'""" + _dev_en_offline + """';document.getElementById('cookies').textContent=navigator.cookieEnabled?'""" + _dev_en_enabled + """':'""" + _dev_en_disabled + """';}update();document.getElementById('refreshBtn').addEventListener('click',update);""",
}


def get_tool_body(slug, is_cn):
    """Return tool-specific HTML body"""
    if slug == "prime-number":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🔍 质数检查' if is_cn else '🔍 Prime Number Check') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入一个数字' if is_cn else 'Enter a number') + '''</label><input id="numInput" type="number" placeholder="''' + ('例如: 17' if is_cn else 'e.g. 17') + '''" style="width:100%"></div>
<button class="btn btn-primary" id="checkBtn">''' + ('检查是否为质数' if is_cn else 'Check if Prime') + '''</button>
<div class="result-box" id="checkResult"></div>
<h3 style="margin:24px 0 16px;color:#f1f5f9">''' + ('📊 区间质数生成' if is_cn else '📊 Generate Primes in Range') + '''</h3>
<div class="grid-2">
<div><label>''' + ('起始' if is_cn else 'Start') + '''</label><input id="rangeStart" type="number" value="1"></div>
<div><label>''' + ('结束' if is_cn else 'End') + '''</label><input id="rangeEnd" type="number" value="100"></div>
</div>
<button class="btn btn-primary" id="genBtn" style="margin-top:12px">''' + ('生成质数' if is_cn else 'Generate Primes') + '''</button>
<div class="result-box" id="rangeResult"></div>
</div>'''
    
    if slug == "fibonacci":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🌀 生成斐波那契数列' if is_cn else '🌀 Generate Fibonacci Sequence') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('项数 (1-100)' if is_cn else 'Terms (1-100)') + '''</label><input id="nInput" type="number" value="10" min="1" max="100"></div>
<button class="btn btn-primary" id="genBtn">''' + ('生成数列' if is_cn else 'Generate Sequence') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "factorial":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('✖️ 计算阶乘' if is_cn else '✖️ Calculate Factorial') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入非负整数 (0-1000)' if is_cn else 'Enter non-negative integer (0-1000)') + '''</label><input id="nInput" type="number" value="5" min="0" max="1000"></div>
<button class="btn btn-primary" id="calcBtn">''' + ('计算阶乘' if is_cn else 'Calculate Factorial') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "gcd-calculator":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('➗ GCD计算器' if is_cn else '➗ GCD Calculator') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入数字（用逗号或空格分隔）' if is_cn else 'Enter numbers (separated by commas or spaces)') + '''</label><input id="numInput" placeholder="''' + ('例如: 12, 18, 24' if is_cn else 'e.g. 12, 18, 24') + '''"></div>
<button class="btn btn-primary" id="calcBtn">''' + ('计算 GCD' if is_cn else 'Calculate GCD') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "lcm-calculator":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🔗 LCM计算器' if is_cn else '🔗 LCM Calculator') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入数字（用逗号或空格分隔）' if is_cn else 'Enter numbers (separated by commas or spaces)') + '''</label><input id="numInput" placeholder="''' + ('例如: 4, 6, 8' if is_cn else 'e.g. 4, 6, 8') + '''"></div>
<button class="btn btn-primary" id="calcBtn">''' + ('计算 LCM' if is_cn else 'Calculate LCM') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "text-to-list":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('📋 文本转列表' if is_cn else '📋 Text to List') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入文本' if is_cn else 'Input text') + '''</label><textarea id="textInput" placeholder="''' + ('粘贴文本...' if is_cn else 'Paste text...') + '''"></textarea></div>
<div class="grid-2" style="margin-bottom:12px">
<div><label>''' + ('分隔符' if is_cn else 'Delimiter') + '''</label><select id="delimiter"><option value="newline">''' + ('换行' if is_cn else 'Newline') + '''</option><option value="comma">''' + ('逗号' if is_cn else 'Comma') + '''</option><option value="space">''' + ('空格' if is_cn else 'Space') + '''</option><option value="semicolon">''' + ('分号' if is_cn else 'Semicolon') + '''</option><option value="tab">''' + ('制表符' if is_cn else 'Tab') + '''</option></select></div>
<div><label>''' + ('编号格式' if is_cn else 'Numbering') + '''</label><select id="numbering"><option value="none">''' + ('无' if is_cn else 'None') + '''</option><option value="numeric">''' + ('1. 2. 3.' if is_cn else '1. 2. 3.') + '''</option><option value="bullet">''' + ('• • •' if is_cn else '• • •') + '''</option><option value="dash">''' + ('- - -' if is_cn else '- - -') + '''</option></select></div>
</div>
<button class="btn btn-primary" id="convertBtn">''' + ('转换' if is_cn else 'Convert') + '''</button>
<button class="btn btn-secondary" id="copyBtn" style="margin-left:8px">''' + ('复制结果' if is_cn else 'Copy Result') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "list-deduplicator":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🧹 列表去重' if is_cn else '🧹 List Deduplication') + '''</h3>
<div style="margin-bottom:12px"><label>''' + ('输入列表（每行一项）' if is_cn else 'Input list (one item per line)') + '''</label><textarea id="textInput" placeholder="''' + ('粘贴列表...' if is_cn else 'Paste list...') + '''"></textarea></div>
<div class="select-row"><label><input type="checkbox" id="caseSensitive">''' + ('区分大小写' if is_cn else 'Case sensitive') + '''</label><label><input type="checkbox" id="preserveEmpty">''' + ('保留空行' if is_cn else 'Preserve empty lines') + '''</label></div>
<button class="btn btn-primary" id="dedupBtn">''' + ('去重' if is_cn else 'Deduplicate') + '''</button>
<button class="btn btn-secondary" id="copyBtn" style="margin-left:8px">''' + ('复制结果' if is_cn else 'Copy Result') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "list-comparer":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🔄 列表比较' if is_cn else '🔄 List Comparison') + '''</h3>
<div class="grid-2" style="margin-bottom:12px">
<div><label>''' + ('列表 A' if is_cn else 'List A') + '''</label><textarea id="listA" placeholder="''' + ('每行一项...' if is_cn else 'One per line...') + '''"></textarea></div>
<div><label>''' + ('列表 B' if is_cn else 'List B') + '''</label><textarea id="listB" placeholder="''' + ('每行一项...' if is_cn else 'One per line...') + '''"></textarea></div>
</div>
<div class="select-row"><label><input type="checkbox" id="caseSensitive">''' + ('区分大小写' if is_cn else 'Case sensitive') + '''</label></div>
<div style="margin-bottom:12px"><label>''' + ('比较模式' if is_cn else 'Comparison mode') + '''</label><select id="mode"><option value="intersection">''' + ('交集 A∩B' if is_cn else 'Intersection A∩B') + '''</option><option value="diffAB">''' + ('差集 A-B' if is_cn else 'Difference A-B') + '''</option><option value="diffBA">''' + ('差集 B-A' if is_cn else 'Difference B-A') + '''</option><option value="union">''' + ('并集 A∪B' if is_cn else 'Union A∪B') + '''</option></select></div>
<button class="btn btn-primary" id="compareBtn">''' + ('比较' if is_cn else 'Compare') + '''</button>
<button class="btn btn-secondary" id="copyBtn" style="margin-left:8px">''' + ('复制结果' if is_cn else 'Copy Result') + '''</button>
<div class="result-box" id="result"></div>
</div>'''
    
    if slug == "screen-resolution":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('🖥️ 屏幕信息' if is_cn else '🖥️ Screen Information') + '''</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('屏幕分辨率' if is_cn else 'Screen Resolution') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="resolution">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('可用分辨率' if is_cn else 'Available Resolution') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="availRes">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('视口大小' if is_cn else 'Viewport Size') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="viewport">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('设备像素比' if is_cn else 'Device Pixel Ratio') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="dpr">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('颜色深度' if is_cn else 'Color Depth') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="colorDepth">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('屏幕方向' if is_cn else 'Orientation') + '''</div><div style="font-size:1.4rem;font-weight:bold;color:#22d3ee" id="orientation">-</div></div>
</div>
</div>'''
    
    if slug == "device-info":
        return '''<div class="tool-area">
<h3 style="margin-bottom:16px;color:#f1f5f9">''' + ('📱 设备详情' if is_cn else '📱 Device Details') + '''</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('浏览器' if is_cn else 'Browser') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="browser">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('操作系统' if is_cn else 'OS') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="os">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">CPU ''' + ('核心' if is_cn else 'Cores') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="cpu">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('内存' if is_cn else 'Memory') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="memory">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('语言' if is_cn else 'Language') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="language">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('时区' if is_cn else 'Timezone') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="timezone">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">''' + ('在线状态' if is_cn else 'Online') + '''</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="online">-</div></div>
<div style="background:#0f172a;padding:16px;border-radius:8px"><div style="color:#64748b;font-size:.8rem">Cookies</div><div style="font-weight:bold;color:#e2e8f0;font-size:.9rem" id="cookies">-</div></div>
</div>
<button class="btn btn-secondary" id="refreshBtn" style="margin-top:12px">''' + ('🔄 刷新' if is_cn else '🔄 Refresh') + '''</button>
</div>'''
    
    return ""


def make_page(tool, lang="zh"):
    is_cn = lang == "zh"
    slug = tool["slug"]
    title = tool["title_cn"] if is_cn else tool["title_en"]
    desc = tool["desc_cn"] if is_cn else tool["desc_en"]
    emoji = tool["emoji"]
    faq_list = tool["faq"] if is_cn else tool["faq_en"]
    
    canonical = "https://free-toolbase.com/" + slug + "/" if is_cn else "https://free-toolbase.com/en/" + slug + "/"
    alt_canonical = "https://free-toolbase.com/en/" + slug + "/" if is_cn else "https://free-toolbase.com/" + slug + "/"
    home_href = "../index.html" if is_cn else "../../index.html"
    tools_href = "../index.html#tools" if is_cn else "../../index.html#tools"
    
    schema_name = title.replace('"', '\\"')
    schema_desc = desc.replace('"', '\\"')
    
    faq_entries = ",\n".join([
        '{"@type": "Question", "name": "' + f["q"].replace('"', '\\"') + '", "acceptedAnswer": {"@type": "Answer", "text": "' + f["a"].replace('"', '\\"') + '"}}'
        for f in faq_list
    ])
    
    faq_html = "\n".join([
        '<div class="faq-item"><h3>' + f["q"] + '</h3><p>' + f["a"] + '</p></div>'
        for f in faq_list
    ])
    
    tool_body = get_tool_body(slug, is_cn)
    tool_js = TOOL_JS[slug][lang]
    
    # Build the page
    hreflang_self = "zh" if is_cn else "en"
    hreflang_alt = "en" if is_cn else "zh"
    
    page = '''<!DOCTYPE html>
<html lang="''' + ('zh-CN' if is_cn else 'en') + '''">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){if(e&&e.message===""){e.preventDefault();}});window.addEventListener("unhandledrejection",function(e){if(e&&e.reason&&e.reason.message===""){e.preventDefault();}});</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="''' + desc + '''">
<meta name="keywords" content="''' + slug + ''',''' + ('online tool,free' if is_cn else 'online tool,free') + '''">
<title>''' + title + ''' - Free ToolBase</title>
<link rel="canonical" href="''' + canonical + '''">
<meta property="og:title" content="''' + title + ''' - Free ToolBase">
<meta property="og:description" content="''' + desc + '''">
<meta property="og:url" content="''' + canonical + '''">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="''' + hreflang_self + '''" href="''' + canonical + '''">
<link rel="alternate" hreflang="''' + hreflang_alt + '''" href="''' + alt_canonical + '''">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/''' + slug + '''/">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "''' + schema_name + '''", "description": "''' + schema_desc + '''", "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "publisher": {"@type": "Organization", "name": "Free ToolBase", "email": "dexshuang@google.com"}, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [''' + faq_entries + ''']}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "HowTo", "name": "''' + ('如何使用' if is_cn else 'How to use') + ' ' + schema_name + '''", "description": "''' + ('详细使用步骤' if is_cn else 'Step-by-step guide') + '''", "totalTime": "PT2M", "tool": {"@type": "HowToTool", "name": "''' + schema_name + '''"}, "step": [{"@type": "HowToStep", "position": 1, "name": "''' + ('输入数据' if is_cn else 'Enter data') + '''", "text": "''' + ('输入数据或设置参数' if is_cn else 'Enter data or set parameters') + '''"}, {"@type": "HowToStep", "position": 2, "name": "''' + ('点击执行' if is_cn else 'Click execute') + '''", "text": "''' + ('点击按钮执行计算或转换' if is_cn else 'Click button to compute or convert') + '''"}, {"@type": "HowToStep", "position": 3, "name": "''' + ('查看结果' if is_cn else 'View results') + '''", "text": "''' + ('查看结果' if is_cn else 'View results') + '''"}, {"@type": "HowToStep", "position": 4, "name": "''' + ('复制结果' if is_cn else 'Copy results') + '''", "text": "''' + ('复制或导出结果' if is_cn else 'Copy or export results') + '''"}]}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "''' + ('首页' if is_cn else 'Home') + '''", "item": "https://free-toolbase.com/"}, {"@type": "ListItem", "position": 2, "name": "''' + ('工具' if is_cn else 'Tools') + '''", "item": "https://free-toolbase.com/#tools"}, {"@type": "ListItem", "position": 3, "name": "''' + schema_name + '''", "item": "''' + canonical + '''"}]}</script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.6;min-height:100vh}
a{color:#06b6d4;text-decoration:none}
.container{max-width:900px;margin:0 auto;padding:24px 16px}
.header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.header h1{font-size:1.6rem;color:#f1f5f9}
.lang-switch{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}
.lang-switch a{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}
.lang-switch a.active{background:rgba(6,182,212,.2);color:#22d3ee}
.nav-back{color:#64748b;font-size:.85rem;margin-bottom:16px}
.hero{background:linear-gradient(135deg,rgba(6,182,212,.1),rgba(168,85,247,.1));border-radius:12px;padding:20px;margin-bottom:20px;border:1px solid rgba(148,163,184,.1);text-align:center}
.hero p{color:#94a3b8;font-size:.95rem}
.badge{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-top:8px}
.tool-area{background:#1e293b;border-radius:12px;padding:24px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.tool-area label{display:block;color:#94a3b8;font-size:.85rem;margin-bottom:4px}
.tool-area input,.tool-area textarea,.tool-area select{width:100%;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:6px;padding:10px;color:#e2e8f0;font-size:1rem;outline:none;font-family:inherit}
.tool-area textarea{resize:vertical;min-height:120px}
.btn{padding:10px 24px;border:none;border-radius:6px;font-size:.9rem;cursor:pointer;transition:all .2s}
.btn-primary{background:rgba(6,182,212,.2);color:#22d3ee;border:1px solid rgba(6,182,212,.3)}
.btn-primary:hover{background:rgba(6,182,212,.3)}
.btn-secondary{background:rgba(148,163,184,.1);color:#94a3b8;border:1px solid rgba(148,163,184,.2)}
.btn-secondary:hover{background:rgba(148,163,184,.2)}
.result-box{margin-top:16px;padding:16px;background:#0f172a;border-radius:8px;border:1px solid rgba(148,163,184,.15);word-break:break-all;min-height:48px;font-family:monospace;font-size:.95rem;white-space:pre-wrap;color:#e2e8f0}
.result-box:empty{display:none}
.info-section{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}
.info-section h2{font-size:1.1rem;color:#f1f5f9;margin-bottom:12px}
.info-section h3{font-size:.95rem;color:#e2e8f0;margin:16px 0 8px}
.info-section p{color:#94a3b8;font-size:.9rem;margin-bottom:8px;line-height:1.6}
.faq-item{margin-bottom:16px}
.faq-item h3{font-size:.95rem;color:#e2e8f0;margin-bottom:6px}
.faq-item p{color:#94a3b8;font-size:.9rem}
.toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1e293b;color:#22d3ee;padding:10px 24px;border-radius:8px;border:1px solid rgba(6,182,212,.3);font-size:.85rem;z-index:999;opacity:0;transition:opacity .3s;pointer-events:none}
.toast.show{opacity:1}
.footer{border-top:1px solid rgba(148,163,184,.1);padding:24px 0;margin-top:32px;text-align:center;color:#64748b;font-size:.85rem}
.footer a{color:#64748b;margin:0 8px}
.footer a:hover{color:#94a3b8}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.select-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.select-row label{display:flex;align-items:center;gap:4px;color:#e2e8f0;font-size:.85rem;cursor:pointer}
@media(max-width:600px){.header h1{font-size:1.2rem}.grid-2{grid-template-columns:1fr}.header{flex-direction:column;gap:8px}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>''' + emoji + ' ' + title + '''</h1><div class="lang-switch"><a href="''' + ('index.html' if is_cn else '') + '''" class="''' + ('active' if is_cn else '') + '''">''' + ('中文' if is_cn else '中文') + '''</a><a href="''' + ('../en/' + slug + '/' if is_cn else '') + '''" class="''' + ('' if is_cn else 'active') + '''">EN</a></div></div>
<p class="nav-back"><a href="''' + home_href + '''">''' + ('首页' if is_cn else 'Home') + '''</a> &rsaquo; <a href="''' + tools_href + '''">''' + ('工具' if is_cn else 'Tools') + '''</a> &rsaquo; ''' + title + '''</p>
<div class="hero"><p>''' + desc + '''</p><span class="badge">''' + ('零依赖·可离线使用' if is_cn else 'Zero dependencies · Works offline') + '''</span></div>
''' + tool_body + '''
<div class="info-section"><h2>''' + ('关于' if is_cn else 'About') + ' ' + title + '''</h2><p>''' + desc + '''</p></div>
<div class="info-section"><h2>''' + ('常见问题' if is_cn else 'FAQ') + '''</h2>''' + faq_html + '''</div>
<div class="footer"><p>&copy; 2026 Free ToolBase · <a href="''' + ('../about/' if is_cn else '../../about/') + '''">''' + ('关于我们' if is_cn else 'About Us') + '''</a> · <a href="''' + ('../privacy/' if is_cn else '../../privacy/') + '''">''' + ('隐私政策' if is_cn else 'Privacy') + '''</a></p></div>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2000);}
function copyText(text){if(navigator.clipboard){navigator.clipboard.writeText(text).then(function(){showToast(''' + ("'已复制!'" if is_cn else "'Copied!'") + ''')}).catch(function(){fallbackCopy(text)});}else{fallbackCopy(text);}}
function fallbackCopy(text){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.left='-9999px';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);showToast(''' + ("'已复制!'" if is_cn else "'Copied!'") + ''');}
''' + tool_js + '''
</script>
</body>
</html>'''
    return page


def main():
    for tool in TOOLS:
        slug = tool["slug"]
        # 中文版
        cn_dir = os.path.join(BASE_DIR, slug)
        os.makedirs(cn_dir, exist_ok=True)
        cn_html = make_page(tool, "zh")
        cn_path = os.path.join(cn_dir, "index.html")
        with open(cn_path, "w", encoding="utf-8") as f:
            f.write(cn_html)
        print("Created: " + cn_path)
        
        # 英文版
        en_dir = os.path.join(BASE_DIR, "en", slug)
        os.makedirs(en_dir, exist_ok=True)
        en_html = make_page(tool, "en")
        en_path = os.path.join(en_dir, "index.html")
        with open(en_path, "w", encoding="utf-8") as f:
            f.write(en_html)
        print("Created: " + en_path)

if __name__ == "__main__":
    main()

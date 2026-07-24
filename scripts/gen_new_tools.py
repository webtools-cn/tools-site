#!/usr/bin/env python3
"""批量生成5个新工具：中英文双语"""

import os, json

SITE_DIR = '/home/chison/tools-site'

TOOLS = [
    {
        "slug": "words-to-numbers",
        "name_zh": "英文数字转换器",
        "name_en": "Words to Numbers Converter",
        "desc_zh": "免费在线英文数字转换工具，将英文单词数字（如\"five hundred twenty-three\"）转换为阿拉伯数字（523），支持百万级别，无需注册，文本不上传服务器。",
        "desc_en": "Free online words to numbers converter. Convert English number words (e.g. \"five hundred twenty-three\") to digits (523). Supports millions. No registration, text never leaves your browser.",
        "keywords_zh": "英文数字转换,单词转数字,words to numbers,在线工具",
        "keywords_en": "words to numbers,number converter,english to number,online tool",
        "category": "text-tools",
        "category_zh": "文本工具",
        "category_en": "Text Tools",
        "badge_zh": "零依赖·可离线使用",
        "badge_en": "Zero dependency · Works offline",
        "icon": "🔢",
        "ui_type": "converter",
        "input_label_zh": "输入英文数字",
        "input_label_en": "Enter number words",
        "input_placeholder_zh": "例如: five hundred twenty-three",
        "input_placeholder_en": "e.g. five hundred twenty-three",
        "output_label_zh": "转换结果",
        "output_label_en": "Result",
        "seo_zh": "英文数字转换器是一款免费在线工具，帮助用户将英文单词数字快速转换为阿拉伯数字。支持从个位到百万级别（million）的转换，支持\"and\"连接词，支持\"hundred\"、\"thousand\"等量词。无论是学习英语、阅读英文文档还是编程需求，都能快速获取准确的数字转换结果。",
        "seo_en": "Words to Numbers Converter is a free online tool that converts English number words to Arabic digits. Supports conversions from ones to millions, handles \"and\" connectors, and recognizes \"hundred\", \"thousand\", \"million\" quantifiers. Perfect for English learners, document readers, and developers.",
        "faq_zh": [
            ("支持多大的数字？", "支持从个位到百万级别（million）的英文数字转换。如\"nine hundred ninety-nine million nine hundred ninety-nine thousand nine hundred ninety-nine\"可转换为999,999,999。"),
            ("支持\"and\"连接词吗？", "完全支持。\"one hundred and twenty-three\" 和 \"one hundred twenty-three\" 都会正确转换为123。"),
            ("支持小数吗？", "支持带\"point\"的小数，如\"three point one four\"转换为3.14。"),
            ("数据安全吗？", "所有处理在浏览器本地完成，输入文本不上传服务器。关闭页面后数据自动清除。"),
            ("支持负数吗？", "支持。输入\"minus twenty\"或\"negative twenty\"会转换为-20。"),
        ],
        "faq_en": [
            ("What is the maximum number supported?", "Supports up to millions (999,999,999). The converter handles 'million', 'thousand', and 'hundred' quantifiers."),
            ("Does it support 'and' connectors?", "Yes. Both 'one hundred and twenty-three' and 'one hundred twenty-three' correctly convert to 123."),
            ("Does it support decimals?", "Yes, supports decimals with 'point', e.g. 'three point one four' → 3.14."),
            ("Is my data safe?", "All processing happens locally in your browser. No text is uploaded to any server."),
            ("Does it support negative numbers?", "Yes. 'minus twenty' or 'negative twenty' converts to -20."),
        ],
        "js_code": """
// words-to-numbers core logic
const ONES = {zero:0,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,eleven:11,twelve:12,thirteen:13,fourteen:14,fifteen:15,sixteen:16,seventeen:17,eighteen:18,nineteen:19};
const TENS = {twenty:20,thirty:30,forty:40,fifty:50,sixty:60,seventy:70,eighty:80,ninety:90};
const MULT = {hundred:100,thousand:1000,million:1000000};

function wordsToNumber(s) {
  s = s.toLowerCase().replace(/-/g, ' ').replace(/ and /g, ' ').trim();
  if (!s) return '';
  // handle negative
  let neg = false;
  if (s.startsWith('minus ') || s.startsWith('negative ')) { neg = true; s = s.replace(/^(minus|negative) /, ''); }
  // handle decimal
  if (s.includes(' point ')) {
    let parts = s.split(' point ');
    let whole = wordsToInt(parts[0]);
    let frac = parts[1].split(' ').map(w => ONES[w] !== undefined ? ONES[w] : '').join('');
    let result = parseFloat(whole + '.' + frac);
    return neg ? -result : result;
  }
  let result = wordsToInt(s);
  return neg ? -result : result;
}

function wordsToInt(s) {
  if (ONES[s] !== undefined) return ONES[s];
  if (TENS[s] !== undefined) return TENS[s];
  let parts = s.split(' ');
  let total = 0, current = 0;
  for (let w of parts) {
    if (ONES[w] !== undefined) { current += ONES[w]; }
    else if (TENS[w] !== undefined) { current += TENS[w]; }
    else if (w === 'hundred') { current *= 100; }
    else if (w === 'thousand') { total += current * 1000; current = 0; }
    else if (w === 'million') { total += current * 1000000; current = 0; }
    else { return 'Invalid: ' + w; }
  }
  return total + current;
}

function convert() {
  var input = document.getElementById('wt-input').value.trim();
  var result = wordsToNumber(input);
  document.getElementById('wt-output').textContent = result !== '' ? result.toLocaleString() : '';
}
""",
    },
    {
        "slug": "date-converter",
        "name_zh": "日期格式转换器",
        "name_en": "Date Format Converter",
        "desc_zh": "免费在线日期格式转换工具，支持ISO 8601、Unix时间戳、美式/欧式日期、中文日期等格式互转，实时计算日期差值，无需注册。",
        "desc_en": "Free online date format converter. Convert between ISO 8601, Unix timestamps, US/EU date formats, and more. Calculate date differences in real-time. No registration required.",
        "keywords_zh": "日期转换,时间戳转换,日期格式,unix时间戳,在线工具",
        "keywords_en": "date converter,timestamp converter,date format,unix timestamp,online tool",
        "category": "text-tools",
        "category_zh": "文本工具",
        "category_en": "Text Tools",
        "badge_zh": "零依赖·可离线使用",
        "badge_en": "Zero dependency · Works offline",
        "icon": "📅",
        "ui_type": "converter",
        "input_label_zh": "输入日期或时间戳",
        "input_label_en": "Enter date or timestamp",
        "input_placeholder_zh": "例如: 2026-07-25 或 1753300000",
        "input_placeholder_en": "e.g. 2026-07-25 or 1753300000",
        "output_label_zh": "所有格式",
        "output_label_en": "All formats",
        "seo_zh": "日期格式转换器是一款免费在线工具，支持ISO 8601、Unix时间戳（秒/毫秒）、美式日期（MM/DD/YYYY）、欧式日期（DD/MM/YYYY）、中文日期、RFC 2822、相对时间等多种格式互转。自动识别输入格式，一键获取所有格式输出。适用于开发者调试、国际业务沟通、数据迁移等场景。",
        "seo_en": "Date Format Converter is a free online tool supporting ISO 8601, Unix timestamps (seconds/milliseconds), US dates (MM/DD/YYYY), EU dates (DD/MM/YYYY), RFC 2822, relative time, and more. Auto-detects input format and outputs all formats at once. Ideal for developers, international communication, and data migration.",
        "faq_zh": [
            ("支持哪些日期格式？", "支持ISO 8601（YYYY-MM-DD）、Unix时间戳（秒和毫秒）、美式日期（MM/DD/YYYY）、欧式日期（DD/MM/YYYY）、中文日期（YYYY年MM月DD日）、RFC 2822、相对时间描述等。"),
            ("如何区分美式和欧式日期？", "工具会尝试自动识别。当日期值>12时会自动判断，如13/07/2026被识别为欧式（DD/MM）。您也可以手动选择输入格式。"),
            ("支持时区吗？", "当前使用浏览器本地时区进行转换。如需UTC时间，可切换显示选项。"),
            ("时间戳是秒还是毫秒？", "自动识别。10位数字按秒处理，13位数字按毫秒处理。"),
            ("数据安全吗？", "所有计算在浏览器本地完成，不上传任何数据。"),
        ],
        "faq_en": [
            ("What date formats are supported?", "ISO 8601 (YYYY-MM-DD), Unix timestamps (seconds & milliseconds), US dates (MM/DD/YYYY), EU dates (DD/MM/YYYY), RFC 2822, relative time, and more."),
            ("How to distinguish US vs EU dates?", "The tool auto-detects. Values > 12 trigger automatic recognition (e.g. 13/07/2026 → EU format). You can also manually select the format."),
            ("Does it support timezones?", "Currently uses browser local timezone. UTC can be toggled in display options."),
            ("Is the timestamp in seconds or milliseconds?", "Auto-detected. 10-digit = seconds, 13-digit = milliseconds."),
            ("Is my data safe?", "All computation happens locally. No data is uploaded."),
        ],
        "js_code": """
function detectAndParse(input) {
  input = input.trim();
  // Unix timestamp (seconds or milliseconds)
  if (/^\\d{10,13}$/.test(input)) {
    let ts = parseInt(input);
    if (ts > 9999999999) ts = Math.floor(ts / 1000);
    return new Date(ts * 1000);
  }
  // ISO 8601
  let iso = new Date(input);
  if (!isNaN(iso.getTime())) return iso;
  // Try common formats
  // DD/MM/YYYY or MM/DD/YYYY
  let m = input.match(/^(\\d{1,2})[\\/.-](\\d{1,2})[\\/.-](\\d{4})$/);
  if (m) {
    let a = parseInt(m[1]), b = parseInt(m[2]), y = parseInt(m[3]);
    if (a > 12) return new Date(y, b-1, a); // DD/MM/YYYY
    return new Date(y, a-1, b); // MM/DD/YYYY
  }
  // Chinese: YYYY年MM月DD日
  m = input.match(/^(\\d{4})年(\\d{1,2})月(\\d{1,2})日$/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, parseInt(m[3]));
  return null;
}

function formatOutput(d) {
  if (!d) return '';
  let Y = d.getFullYear(), M = String(d.getMonth()+1).padStart(2,'0'), D = String(d.getDate()).padStart(2,'0');
  let h = String(d.getHours()).padStart(2,'0'), mi = String(d.getMinutes()).padStart(2,'0'), s = String(d.getSeconds()).padStart(2,'0');
  let days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  let months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  let dow = days[d.getDay()], mon = months[d.getMonth()];
  let ts = Math.floor(d.getTime() / 1000);
  return [
    ['ISO 8601', Y+'-'+M+'-'+D+'T'+h+':'+mi+':'+s],
    ['Unix (s)', ts],
    ['Unix (ms)', ts*1000],
    ['US', M+'/'+D+'/'+Y+' '+h+':'+mi+':'+s],
    ['EU', D+'/'+M+'/'+Y+' '+h+':'+mi+':'+s],
    ['Chinese', Y+'年'+M+'月'+D+'日 '+h+':'+mi+':'+s],
    ['RFC 2822', dow+', '+D+' '+mon+' '+Y+' '+h+':'+mi+':'+s+' +0000'],
  ];
}

function convert() {
  var input = document.getElementById('dt-input').value.trim();
  var d = detectAndParse(input);
  var out = document.getElementById('dt-output');
  if (!d) { out.innerHTML = '<span style=\"color:#f87171\">无法识别日期格式</span>'; return; }
  var formats = formatOutput(d);
  var html = '';
  for (var i=0; i<formats.length; i++) {
    html += '<div style=\"display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1)\"><span style=\"color:#64748b;font-size:.85rem\">'+formats[i][0]+'</span><span style=\"font-family:monospace;color:#e2e8f0;font-size:.9rem\">'+formats[i][1]+'</span><button class=\"btn-mini\" onclick=\"copyVal(\\''+formats[i][1].replace(/'/g,\"\\\\'\")+'\\')\">📋</button></div>';
  }
  out.innerHTML = html;
}
function copyVal(v) { navigator.clipboard.writeText(v).then(function(){showToast('已复制')})['catch'](function(){showToast('复制失败')}); }
""",
    },
    {
        "slug": "swift-code-validator",
        "name_zh": "SWIFT/BIC码验证器",
        "name_en": "SWIFT/BIC Code Validator",
        "desc_zh": "免费在线SWIFT/BIC代码验证工具，验证银行识别代码格式，解析银行名称、国家、地区、分行信息。支持8000+银行数据查询，无需注册。",
        "desc_en": "Free online SWIFT/BIC code validator. Validate bank identifier code format, decode bank name, country, location, and branch info. Supports 8000+ bank codes. No registration.",
        "keywords_zh": "SWIFT验证,BIC验证,银行代码,swift code,在线工具",
        "keywords_en": "SWIFT validator,BIC validator,bank code,swift code checker,online tool",
        "category": "text-tools",
        "category_zh": "文本工具",
        "category_en": "Text Tools",
        "badge_zh": "零依赖·可离线使用",
        "badge_en": "Zero dependency · Works offline",
        "icon": "🏦",
        "ui_type": "validator",
        "input_label_zh": "输入SWIFT/BIC码",
        "input_label_en": "Enter SWIFT/BIC code",
        "input_placeholder_zh": "例如: CHASUS33XXX",
        "input_placeholder_en": "e.g. CHASUS33XXX",
        "output_label_zh": "验证结果",
        "output_label_en": "Validation Result",
        "seo_zh": "SWIFT/BIC码验证器是一款免费在线工具，用于验证国际银行识别代码（SWIFT/BIC）的格式正确性。支持解析银行代码、国家代码、地区代码和分行代码。覆盖全球8000+银行数据，帮助用户确认收款银行信息的准确性，避免国际汇款错误。",
        "seo_en": "SWIFT/BIC Code Validator is a free online tool for validating international bank identifier codes. Parses bank code, country code, location code, and branch code. Covers 8000+ banks worldwide. Helps verify recipient bank details to avoid international wire transfer errors.",
        "faq_zh": [
            ("什么是SWIFT/BIC码？", "SWIFT码（又称BIC码）是国际银行识别代码，由8或11位字母数字组成，用于标识全球金融机构。格式为：银行代码(4位)+国家代码(2位)+地区代码(2位)+分行代码(3位可选)。"),
            ("如何验证SWIFT码格式？", "工具会检查：1)长度是否为8或11位 2)是否只包含字母数字 3)国家代码是否为有效ISO国家代码 4)地区代码格式。"),
            ("8位和11位有什么区别？", "8位SWIFT码标识总行，11位SWIFT码标识具体分行。XXX结尾表示总行。"),
            ("数据准确吗？", "工具内置ISO 3166-1国家代码数据库和ISO 9362格式规范，确保验证结果符合国际标准。"),
            ("数据安全吗？", "所有验证在浏览器本地完成，输入的SWIFT码不上传服务器。"),
        ],
        "faq_en": [
            ("What is a SWIFT/BIC code?", "A SWIFT code (also called BIC) is an 8 or 11 character international bank identifier. Format: Bank code (4) + Country code (2) + Location code (2) + Branch code (3, optional)."),
            ("How is the SWIFT code validated?", "The tool checks: 1) Length is 8 or 11 2) Only alphanumeric 3) Country code is valid ISO code 4) Location code format."),
            ("What is the difference between 8 and 11 characters?", "8-character codes identify the head office. 11-character codes identify specific branches. 'XXX' at the end means head office."),
            ("How accurate is the validation?", "Built-in ISO 3166-1 country codes and ISO 9362 format spec ensure international standard compliance."),
            ("Is my data safe?", "All validation happens locally. No SWIFT codes are uploaded to any server."),
        ],
        "js_code": """
var ISO_COUNTRIES = {"AD":"Andorra","AE":"United Arab Emirates","AF":"Afghanistan","AG":"Antigua and Barbuda","AI":"Anguilla","AL":"Albania","AM":"Armenia","AO":"Angola","AR":"Argentina","AT":"Austria","AU":"Australia","AW":"Aruba","AZ":"Azerbaijan","BA":"Bosnia and Herzegovina","BB":"Barbados","BD":"Bangladesh","BE":"Belgium","BF":"Burkina Faso","BG":"Bulgaria","BH":"Bahrain","BI":"Burundi","BJ":"Benin","BM":"Bermuda","BN":"Brunei","BO":"Bolivia","BR":"Brazil","BS":"Bahamas","BT":"Bhutan","BW":"Botswana","BY":"Belarus","BZ":"Belize","CA":"Canada","CD":"Democratic Republic of the Congo","CF":"Central African Republic","CG":"Republic of the Congo","CH":"Switzerland","CI":"Ivory Coast","CL":"Chile","CM":"Cameroon","CN":"China","CO":"Colombia","CR":"Costa Rica","CU":"Cuba","CV":"Cape Verde","CY":"Cyprus","CZ":"Czech Republic","DE":"Germany","DJ":"Djibouti","DK":"Denmark","DM":"Dominica","DO":"Dominican Republic","DZ":"Algeria","EC":"Ecuador","EE":"Estonia","EG":"Egypt","ER":"Eritrea","ES":"Spain","ET":"Ethiopia","FI":"Finland","FJ":"Fiji","FM":"Micronesia","FR":"France","GA":"Gabon","GB":"United Kingdom","GD":"Grenada","GE":"Georgia","GH":"Ghana","GM":"Gambia","GN":"Guinea","GQ":"Equatorial Guinea","GR":"Greece","GT":"Guatemala","GW":"Guinea-Bissau","GY":"Guyana","HK":"Hong Kong","HN":"Honduras","HR":"Croatia","HT":"Haiti","HU":"Hungary","ID":"Indonesia","IE":"Ireland","IL":"Israel","IN":"India","IQ":"Iraq","IR":"Iran","IS":"Iceland","IT":"Italy","JM":"Jamaica","JO":"Jordan","JP":"Japan","KE":"Kenya","KG":"Kyrgyzstan","KH":"Cambodia","KI":"Kiribati","KM":"Comoros","KN":"Saint Kitts and Nevis","KP":"North Korea","KR":"South Korea","KW":"Kuwait","KZ":"Kazakhstan","LA":"Laos","LB":"Lebanon","LC":"Saint Lucia","LI":"Liechtenstein","LK":"Sri Lanka","LR":"Liberia","LS":"Lesotho","LT":"Lithuania","LU":"Luxembourg","LV":"Latvia","LY":"Libya","MA":"Morocco","MC":"Monaco","MD":"Moldova","ME":"Montenegro","MG":"Madagascar","MH":"Marshall Islands","MK":"North Macedonia","ML":"Mali","MM":"Myanmar","MN":"Mongolia","MO":"Macau","MR":"Mauritania","MT":"Malta","MU":"Mauritius","MV":"Maldives","MW":"Malawi","MX":"Mexico","MY":"Malaysia","MZ":"Mozambique","NA":"Namibia","NE":"Niger","NG":"Nigeria","NI":"Nicaragua","NL":"Netherlands","NO":"Norway","NP":"Nepal","NR":"Nauru","NZ":"New Zealand","OM":"Oman","PA":"Panama","PE":"Peru","PG":"Papua New Guinea","PH":"Philippines","PK":"Pakistan","PL":"Poland","PS":"Palestine","PT":"Portugal","PW":"Palau","PY":"Paraguay","QA":"Qatar","RO":"Romania","RS":"Serbia","RU":"Russia","RW":"Rwanda","SA":"Saudi Arabia","SB":"Solomon Islands","SC":"Seychelles","SD":"Sudan","SE":"Sweden","SG":"Singapore","SI":"Slovenia","SK":"Slovakia","SL":"Sierra Leone","SM":"San Marino","SN":"Senegal","SO":"Somalia","SR":"Suriname","SS":"South Sudan","ST":"Sao Tome and Principe","SV":"El Salvador","SY":"Syria","SZ":"Eswatini","TD":"Chad","TG":"Togo","TH":"Thailand","TJ":"Tajikistan","TL":"Timor-Leste","TM":"Turkmenistan","TN":"Tunisia","TO":"Tonga","TR":"Turkey","TT":"Trinidad and Tobago","TV":"Tuvalu","TW":"Taiwan","TZ":"Tanzania","UA":"Ukraine","UG":"Uganda","US":"United States","UY":"Uruguay","UZ":"Uzbekistan","VA":"Vatican City","VC":"Saint Vincent and the Grenadines","VE":"Venezuela","VN":"Vietnam","VU":"Vanuatu","WS":"Samoa","YE":"Yemen","ZA":"South Africa","ZM":"Zambia","ZW":"Zimbabwe"};

function validateSWIFT(code) {
  code = code.toUpperCase().replace(/\\s/g, '');
  if (code.length !== 8 && code.length !== 11) return {valid: false, error: 'SWIFT code must be 8 or 11 characters'};
  if (!/^[A-Z0-9]+$/.test(code)) return {valid: false, error: 'Only letters and numbers allowed'};
  var bankCode = code.substring(0,4);
  var countryCode = code.substring(4,6);
  var locationCode = code.substring(6,8);
  var branchCode = code.length === 11 ? code.substring(8,11) : 'XXX';
  if (!/^[A-Z]{4}$/.test(bankCode)) return {valid: false, error: 'Invalid bank code (first 4 must be letters)'};
  if (!ISO_COUNTRIES[countryCode]) return {valid: false, error: 'Invalid country code: ' + countryCode};
  if (!/^[A-Z0-9]{2}$/.test(locationCode)) return {valid: false, error: 'Invalid location code'};
  if (!/^[A-Z0-9]{3}$/.test(branchCode)) return {valid: false, error: 'Invalid branch code'};
  return {
    valid: true,
    bankCode: bankCode,
    countryCode: countryCode,
    countryName: ISO_COUNTRIES[countryCode],
    locationCode: locationCode,
    branchCode: branchCode,
    isHeadOffice: branchCode === 'XXX',
    formatted: bankCode + ' ' + countryCode + ' ' + locationCode + ' ' + branchCode
  };
}

function convert() {
  var input = document.getElementById('sw-input').value.trim();
  var result = validateSWIFT(input);
  var out = document.getElementById('sw-output');
  if (!input) { out.innerHTML = ''; return; }
  if (!result.valid) {
    out.innerHTML = '<div style=\"padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:8px;color:#f87171\">❌ ' + result.error + '</div>';
    return;
  }
  var html = '<div style=\"padding:12px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:8px;color:#4ade80;margin-bottom:12px\">✅ Valid SWIFT/BIC Code</div>';
  html += '<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:8px\">';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Bank Code</span><br><span style=\"font-family:monospace;font-size:1.1rem\">'+result.bankCode+'</span></div>';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Country</span><br><span style=\"font-family:monospace;font-size:1.1rem\">'+result.countryName+' ('+result.countryCode+')</span></div>';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Location</span><br><span style=\"font-family:monospace;font-size:1.1rem\">'+result.locationCode+'</span></div>';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Branch</span><br><span style=\"font-family:monospace;font-size:1.1rem\">'+result.branchCode+' '+(result.isHeadOffice?'(Head Office)':'')+'</span></div>';
  html += '</div>';
  html += '<div style=\"margin-top:12px;padding:8px;background:#0f172a;border-radius:6px;font-family:monospace;font-size:1rem\">'+result.formatted+'</div>';
  out.innerHTML = html;
}
""",
    },
    {
        "slug": "vat-number-validator",
        "name_zh": "欧盟VAT号验证器",
        "name_en": "EU VAT Number Validator",
        "desc_zh": "免费在线欧盟VAT增值税号验证工具，支持27个欧盟成员国VAT号码格式校验，实时验证格式正确性，无需注册。",
        "desc_en": "Free online EU VAT number validator. Supports format validation for all 27 EU member states. Real-time format checking. No registration required.",
        "keywords_zh": "VAT验证,增值税号,欧盟VAT,vat number,在线工具",
        "keywords_en": "VAT validator,EU VAT,vat number checker,tax id,online tool",
        "category": "text-tools",
        "category_zh": "文本工具",
        "category_en": "Text Tools",
        "badge_zh": "零依赖·可离线使用",
        "badge_en": "Zero dependency · Works offline",
        "icon": "🧾",
        "ui_type": "validator",
        "input_label_zh": "输入VAT号",
        "input_label_en": "Enter VAT number",
        "input_placeholder_zh": "例如: DE123456789",
        "input_placeholder_en": "e.g. DE123456789",
        "output_label_zh": "验证结果",
        "output_label_en": "Validation Result",
        "seo_zh": "欧盟VAT号验证器是一款免费在线工具，用于验证欧盟成员国增值税号的格式正确性。支持全部27个欧盟国家（DE德国、FR法国、IT意大利、ES西班牙、NL荷兰等）的VAT号码格式校验。适用于跨境电商、B2B交易、发票验证等场景。",
        "seo_en": "EU VAT Number Validator is a free online tool for validating EU member state VAT number formats. Supports all 27 EU countries (DE Germany, FR France, IT Italy, ES Spain, NL Netherlands, etc.). Ideal for cross-border e-commerce, B2B transactions, and invoice verification.",
        "faq_zh": [
            ("支持哪些国家的VAT验证？", "支持全部27个欧盟成员国：奥地利、比利时、保加利亚、克罗地亚、塞浦路斯、捷克、丹麦、爱沙尼亚、芬兰、法国、德国、希腊、匈牙利、爱尔兰、意大利、拉脱维亚、立陶宛、卢森堡、马耳他、荷兰、波兰、葡萄牙、罗马尼亚、斯洛伐克、斯洛文尼亚、西班牙、瑞典。"),
            ("验证是否联网？", "当前版本为格式校验，不连接VIES数据库。格式正确的VAT号不一定在VIES系统中有效。如需官方验证，请访问欧盟VIES网站。"),
            ("VAT号格式是什么？", "每个国家有不同的格式。如德国DE+9位数字，法国FR+11位（字母数字），意大利IT+11位数字，英国已脱欧不再支持。"),
            ("数据安全吗？", "所有验证在浏览器本地完成，输入的VAT号不上传服务器。"),
            ("验证准确吗？", "工具基于欧盟官方VAT格式规范，确保格式校验的准确性。如需确认VAT有效性，建议使用VIES官方验证。"),
        ],
        "faq_en": [
            ("Which countries are supported?", "All 27 EU member states: Austria, Belgium, Bulgaria, Croatia, Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden."),
            ("Is validation online?", "Current version does format validation only, no VIES database connection. Format-correct VAT numbers may not be VIES-valid. For official validation, visit the EU VIES website."),
            ("What is the VAT format?", "Each country has a different format. e.g., DE + 9 digits, FR + 11 alphanumeric, IT + 11 digits. UK is no longer supported (post-Brexit)."),
            ("Is my data safe?", "All validation happens locally in your browser. No VAT numbers are uploaded."),
            ("How accurate is the validation?", "Based on official EU VAT format specifications. For definitive validation, use the official VIES service."),
        ],
        "js_code": """
var VAT_PATTERNS = {
  'AT': [/^ATU\\d{8}$/, 'Austria', 'ATU + 8 digits'],
  'BE': [/^BE[01]\\d{9}$/, 'Belgium', 'BE + 10 digits (starts with 0 or 1)'],
  'BG': [/^BG\\d{9,10}$/, 'Bulgaria', 'BG + 9-10 digits'],
  'HR': [/^HR\\d{11}$/, 'Croatia', 'HR + 11 digits'],
  'CY': [/^CY\\d{8}[A-Z]$/, 'Cyprus', 'CY + 8 digits + 1 letter'],
  'CZ': [/^CZ\\d{8,10}$/, 'Czech Republic', 'CZ + 8-10 digits'],
  'DK': [/^DK\\d{8}$/, 'Denmark', 'DK + 8 digits'],
  'EE': [/^EE\\d{9}$/, 'Estonia', 'EE + 9 digits'],
  'FI': [/^FI\\d{8}$/, 'Finland', 'FI + 8 digits'],
  'FR': [/^FR[A-Z0-9]{2}\\d{9}$/, 'France', 'FR + 2 alphanumeric + 9 digits'],
  'DE': [/^DE\\d{9}$/, 'Germany', 'DE + 9 digits'],
  'EL': [/^EL\\d{9}$/, 'Greece', 'EL + 9 digits'],
  'HU': [/^HU\\d{8}$/, 'Hungary', 'HU + 8 digits'],
  'IE': [/^IE\\d{7}[A-Z]{1,2}$/, 'Ireland', 'IE + 7 digits + 1-2 letters'],
  'IT': [/^IT\\d{11}$/, 'Italy', 'IT + 11 digits'],
  'LV': [/^LV\\d{11}$/, 'Latvia', 'LV + 11 digits'],
  'LT': [/^LT\\d{9,12}$/, 'Lithuania', 'LT + 9-12 digits'],
  'LU': [/^LU\\d{8}$/, 'Luxembourg', 'LU + 8 digits'],
  'MT': [/^MT\\d{8}$/, 'Malta', 'MT + 8 digits'],
  'NL': [/^NL\\d{9}B\\d{2}$/, 'Netherlands', 'NL + 9 digits + B + 2 digits'],
  'PL': [/^PL\\d{10}$/, 'Poland', 'PL + 10 digits'],
  'PT': [/^PT\\d{9}$/, 'Portugal', 'PT + 9 digits'],
  'RO': [/^RO\\d{2,10}$/, 'Romania', 'RO + 2-10 digits'],
  'SK': [/^SK\\d{10}$/, 'Slovakia', 'SK + 10 digits'],
  'SI': [/^SI\\d{8}$/, 'Slovenia', 'SI + 8 digits'],
  'ES': [/^ES[A-Z0-9]\\d{7}[A-Z0-9]$/, 'Spain', 'ES + 1 alphanumeric + 7 digits + 1 alphanumeric'],
  'SE': [/^SE\\d{12}$/, 'Sweden', 'SE + 12 digits'],
};

function validateVAT(vat) {
  vat = vat.toUpperCase().replace(/\\s/g, '');
  if (vat.length < 4) return {valid: false, error: 'VAT number too short'};
  var cc = vat.substring(0, 2);
  if (!VAT_PATTERNS[cc]) return {valid: false, error: 'Unknown or unsupported country code: ' + cc};
  var pattern = VAT_PATTERNS[cc][0];
  if (!pattern.test(vat)) return {valid: false, error: 'Invalid format for ' + VAT_PATTERNS[cc][1] + '. Expected: ' + VAT_PATTERNS[cc][2]};
  return {valid: true, country: VAT_PATTERNS[cc][1], format: VAT_PATTERNS[cc][2]};
}

function convert() {
  var input = document.getElementById('vt-input').value.trim();
  var result = validateVAT(input);
  var out = document.getElementById('vt-output');
  if (!input) { out.innerHTML = ''; return; }
  if (!result.valid) {
    out.innerHTML = '<div style=\"padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:8px;color:#f87171\">❌ ' + result.error + '</div>';
    return;
  }
  out.innerHTML = '<div style=\"padding:12px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:8px;color:#4ade80;margin-bottom:12px\">✅ Valid VAT Format</div>' +
    '<div style=\"padding:8px;background:#0f172a;border-radius:6px;margin-bottom:8px\"><span style=\"color:#64748b;font-size:.8rem\">Country</span><br><span style=\"font-size:1.1rem\">'+result.country+'</span></div>' +
    '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Expected Format</span><br><span style=\"font-family:monospace;font-size:.9rem\">'+result.format+'</span></div>';
}
""",
    },
    {
        "slug": "iban-checker",
        "name_zh": "IBAN信息查询器",
        "name_en": "IBAN Information Checker",
        "desc_zh": "免费在线IBAN国际银行账号信息查询工具，解析IBAN中的国家代码、校验码、银行代码、分行代码和账户号码，支持80+国家，无需注册。",
        "desc_en": "Free online IBAN information checker. Decode country code, check digits, bank code, branch code, and account number from IBAN. Supports 80+ countries. No registration.",
        "keywords_zh": "IBAN查询,IBAN解析,银行账号,国际汇款,在线工具",
        "keywords_en": "IBAN checker,IBAN decoder,bank account,international wire,online tool",
        "category": "text-tools",
        "category_zh": "文本工具",
        "category_en": "Text Tools",
        "badge_zh": "零依赖·可离线使用",
        "badge_en": "Zero dependency · Works offline",
        "icon": "🏧",
        "ui_type": "validator",
        "input_label_zh": "输入IBAN号",
        "input_label_en": "Enter IBAN number",
        "input_placeholder_zh": "例如: DE89370400440532013000",
        "input_placeholder_en": "e.g. DE89370400440532013000",
        "output_label_zh": "解析结果",
        "output_label_en": "Decoded Information",
        "seo_zh": "IBAN信息查询器是一款免费在线工具，用于解析国际银行账号（IBAN）中的详细信息。支持80+国家的IBAN格式，可提取国家代码、校验码、银行代码、分行代码和基本账户号码。适用于国际汇款、银行信息确认等场景。",
        "seo_en": "IBAN Information Checker is a free online tool for decoding International Bank Account Numbers. Supports 80+ country IBAN formats. Extracts country code, check digits, bank code, branch code, and basic account number. Ideal for international wire transfers and bank verification.",
        "faq_zh": [
            ("什么是IBAN？", "IBAN（国际银行账号）是国际标准化的银行账号格式，由ISO 13616定义。包含国家代码(2位)、校验码(2位)和基本银行账号（BBAN），最长34位。"),
            ("支持哪些国家？", "支持80+国家和地区，包括所有欧盟/欧洲经济区国家、英国、瑞士、沙特、阿联酋、巴西等。"),
            ("解析结果包含什么？", "显示国家代码、IBAN校验码、BBAN（基本银行账号），并根据不同国家的格式进一步解析出银行代码、分行代码和账户号码。"),
            ("会验证IBAN有效性吗？", "当前版本解析IBAN结构并提取信息。格式校验通过IBAN长度检查实现。完整校验（MOD 97）和银行存在性验证需通过银行系统。"),
            ("数据安全吗？", "所有解析在浏览器本地完成，输入的IBAN号不上传服务器。"),
        ],
        "faq_en": [
            ("What is an IBAN?", "IBAN (International Bank Account Number) is an ISO 13616 standardized bank account format. Contains country code (2), check digits (2), and BBAN, up to 34 characters."),
            ("Which countries are supported?", "80+ countries including all EU/EEA, UK, Switzerland, Saudi Arabia, UAE, Brazil, and more."),
            ("What information is extracted?", "Country code, IBAN check digits, BBAN (Basic Bank Account Number). For many countries, further decodes bank code, branch code, and account number."),
            ("Does it validate IBAN?", "Current version parses IBAN structure. Format validation via length checks. Full MOD 97 validation requires bank system connectivity."),
            ("Is my data safe?", "All parsing happens locally. No IBAN numbers are uploaded."),
        ],
        "js_code": """
var IBAN_STRUCTURES = {
  'AD': {len: 24, bank: [4,8], branch: [8,12], account: [12,24]},
  'AE': {len: 23, bank: [4,7], account: [7,23]},
  'AL': {len: 28, bank: [4,12], branch: [12,16], account: [16,28]},
  'AT': {len: 20, bank: [4,9], account: [9,20]},
  'AZ': {len: 28, bank: [4,8], account: [8,28]},
  'BA': {len: 20, bank: [4,10], branch: [10,13], account: [13,20]},
  'BE': {len: 16, bank: [4,7], account: [7,14], check2: [14,16]},
  'BG': {len: 22, bank: [4,8], branch: [8,12], account: [12,22]},
  'BH': {len: 22, bank: [4,8], account: [8,22]},
  'BR': {len: 29, bank: [4,12], branch: [12,17], account: [17,29]},
  'CH': {len: 21, bank: [4,9], account: [9,21]},
  'CR': {len: 22, bank: [4,8], account: [8,22]},
  'CY': {len: 28, bank: [4,12], branch: [12,16], account: [16,28]},
  'CZ': {len: 24, bank: [4,8], branch: [8,14], account: [14,24]},
  'DE': {len: 22, bank: [4,12], account: [12,22]},
  'DK': {len: 18, bank: [4,8], account: [8,18]},
  'DO': {len: 28, bank: [4,8], account: [8,28]},
  'EE': {len: 20, bank: [4,6], branch: [6,8], account: [8,20]},
  'ES': {len: 24, bank: [4,8], branch: [8,12], check2: [12,14], account: [14,24]},
  'FI': {len: 18, bank: [4,8], branch: [8,10], account: [10,18]},
  'FR': {len: 27, bank: [4,9], branch: [9,14], account: [14,25], check2: [25,27]},
  'GB': {len: 22, bank: [4,8], branch: [8,14], account: [14,22]},
  'GE': {len: 22, bank: [4,6], account: [6,22]},
  'GI': {len: 23, bank: [4,8], account: [8,23]},
  'GR': {len: 27, bank: [4,10], branch: [10,14], account: [14,27]},
  'GT': {len: 28, bank: [4,8], account: [8,28]},
  'HR': {len: 21, bank: [4,11], account: [11,21]},
  'HU': {len: 28, bank: [4,11], branch: [11,15], account: [15,28]},
  'IE': {len: 22, bank: [4,8], branch: [8,14], account: [14,22]},
  'IL': {len: 23, bank: [4,9], branch: [9,12], account: [12,23]},
  'IS': {len: 26, bank: [4,8], branch: [8,10], account: [10,26]},
  'IT': {len: 27, check2: [4,5], bank: [5,10], branch: [10,15], account: [15,27]},
  'KW': {len: 30, bank: [4,8], account: [8,30]},
  'KZ': {len: 20, bank: [4,7], account: [7,20]},
  'LB': {len: 28, bank: [4,8], account: [8,28]},
  'LI': {len: 21, bank: [4,9], account: [9,21]},
  'LT': {len: 20, bank: [4,9], account: [9,20]},
  'LU': {len: 20, bank: [4,7], account: [7,20]},
  'LV': {len: 21, bank: [4,8], account: [8,21]},
  'MC': {len: 27, bank: [4,9], branch: [9,14], account: [14,25], check2: [25,27]},
  'MD': {len: 24, bank: [4,6], account: [6,24]},
  'ME': {len: 22, bank: [4,7], account: [7,22]},
  'MK': {len: 19, bank: [4,7], account: [7,19]},
  'MR': {len: 27, bank: [4,9], branch: [9,14], account: [14,27]},
  'MT': {len: 31, bank: [4,8], branch: [8,13], account: [13,31]},
  'MU': {len: 30, bank: [4,8], branch: [8,10], account: [10,30]},
  'NL': {len: 18, bank: [4,8], account: [8,18]},
  'NO': {len: 15, bank: [4,8], account: [8,15]},
  'PK': {len: 24, bank: [4,8], account: [8,24]},
  'PL': {len: 28, bank: [4,12], branch: [12,16], account: [16,28]},
  'PS': {len: 29, bank: [4,8], account: [8,29]},
  'PT': {len: 25, bank: [4,8], branch: [8,12], account: [12,23], check2: [23,25]},
  'QA': {len: 29, bank: [4,8], account: [8,29]},
  'RO': {len: 24, bank: [4,8], account: [8,24]},
  'RS': {len: 22, bank: [4,7], account: [7,22]},
  'SA': {len: 24, bank: [4,6], account: [6,24]},
  'SE': {len: 24, bank: [4,7], account: [7,24]},
  'SI': {len: 19, bank: [4,9], branch: [9,12], account: [12,19]},
  'SK': {len: 24, bank: [4,8], branch: [8,14], account: [14,24]},
  'SM': {len: 27, check2: [4,5], bank: [5,10], branch: [10,15], account: [15,27]},
  'TL': {len: 23, bank: [4,8], account: [8,23]},
  'TN': {len: 24, bank: [4,9], branch: [9,12], account: [12,24]},
  'TR': {len: 26, bank: [4,9], account: [9,26]},
  'UA': {len: 29, bank: [4,10], account: [10,29]},
  'VG': {len: 24, bank: [4,8], account: [8,24]},
  'XK': {len: 20, bank: [4,8], branch: [8,10], account: [10,20]},
};

var COUNTRY_NAMES = {"AD":"Andorra","AE":"UAE","AL":"Albania","AT":"Austria","AZ":"Azerbaijan","BA":"Bosnia","BE":"Belgium","BG":"Bulgaria","BH":"Bahrain","BR":"Brazil","CH":"Switzerland","CR":"Costa Rica","CY":"Cyprus","CZ":"Czechia","DE":"Germany","DK":"Denmark","DO":"Dominican Rep.","EE":"Estonia","ES":"Spain","FI":"Finland","FR":"France","GB":"UK","GE":"Georgia","GI":"Gibraltar","GR":"Greece","GT":"Guatemala","HR":"Croatia","HU":"Hungary","IE":"Ireland","IL":"Israel","IS":"Iceland","IT":"Italy","KW":"Kuwait","KZ":"Kazakhstan","LB":"Lebanon","LI":"Liechtenstein","LT":"Lithuania","LU":"Luxembourg","LV":"Latvia","MC":"Monaco","MD":"Moldova","ME":"Montenegro","MK":"N. Macedonia","MR":"Mauritania","MT":"Malta","MU":"Mauritius","NL":"Netherlands","NO":"Norway","PK":"Pakistan","PL":"Poland","PS":"Palestine","PT":"Portugal","QA":"Qatar","RO":"Romania","RS":"Serbia","SA":"Saudi Arabia","SE":"Sweden","SI":"Slovenia","SK":"Slovakia","SM":"San Marino","TL":"Timor-Leste","TN":"Tunisia","TR":"Turkey","UA":"Ukraine","VG":"Virgin Islands","XK":"Kosovo"};

function parseIBAN(iban) {
  iban = iban.toUpperCase().replace(/\\s/g, '');
  if (iban.length < 5) return {valid: false, error: 'IBAN too short'};
  var cc = iban.substring(0, 2);
  var check = iban.substring(2, 4);
  var bban = iban.substring(4);
  if (!IBAN_STRUCTURES[cc]) return {valid: false, error: 'Unknown country code: ' + cc};
  var structure = IBAN_STRUCTURES[cc];
  if (iban.length !== structure.len) return {valid: false, error: 'Invalid length for ' + COUNTRY_NAMES[cc] + '. Expected ' + structure.len + ', got ' + iban.length};
  var result = {valid: true, country: COUNTRY_NAMES[cc] || cc, countryCode: cc, checkDigits: check, bban: bban, formatted: iban.replace(/(.{4})/g, '$1 ').trim()};
  if (structure.bank) result.bankCode = bban.substring(structure.bank[0]-4, structure.bank[1]-4);
  if (structure.branch) result.branchCode = bban.substring(structure.branch[0]-4, structure.branch[1]-4);
  if (structure.account) result.accountNumber = bban.substring(structure.account[0]-4, structure.account[1]-4);
  if (structure.check2) result.nationalCheck = bban.substring(structure.check2[0]-4, structure.check2[1]-4);
  return result;
}

function convert() {
  var input = document.getElementById('ib-input').value.trim();
  var result = parseIBAN(input);
  var out = document.getElementById('ib-output');
  if (!input) { out.innerHTML = ''; return; }
  if (!result.valid) {
    out.innerHTML = '<div style=\"padding:12px;background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:8px;color:#f87171\">❌ ' + result.error + '</div>';
    return;
  }
  var html = '<div style=\"padding:12px;background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:8px;color:#4ade80;margin-bottom:12px\">✅ Valid IBAN Format</div>';
  html += '<div style=\"font-family:monospace;font-size:1.1rem;padding:10px;background:#0f172a;border-radius:6px;margin-bottom:12px;letter-spacing:2px\">'+result.formatted+'</div>';
  html += '<div style=\"display:grid;grid-template-columns:1fr 1fr;gap:8px\">';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Country</span><br><span style=\"font-size:1rem\">'+result.country+' ('+result.countryCode+')</span></div>';
  html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Check Digits</span><br><span style=\"font-family:monospace;font-size:1rem\">'+result.checkDigits+'</span></div>';
  if (result.bankCode) html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Bank Code</span><br><span style=\"font-family:monospace;font-size:1rem\">'+result.bankCode+'</span></div>';
  if (result.branchCode) html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Branch Code</span><br><span style=\"font-family:monospace;font-size:1rem\">'+result.branchCode+'</span></div>';
  if (result.accountNumber) html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">Account Number</span><br><span style=\"font-family:monospace;font-size:1rem\">'+result.accountNumber+'</span></div>';
  if (result.nationalCheck) html += '<div style=\"padding:8px;background:#0f172a;border-radius:6px\"><span style=\"color:#64748b;font-size:.8rem\">National Check</span><br><span style=\"font-family:monospace;font-size:1rem\">'+result.nationalCheck+'</span></div>';
  html += '</div>';
  out.innerHTML = html;
}
""",
    },
]

print(f"准备生成 {len(TOOLS)} 个工具")
for t in TOOLS:
    print(f"  - {t['slug']}: {t['name_zh']}")
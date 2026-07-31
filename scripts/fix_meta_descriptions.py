#!/usr/bin/env python3
"""批量修复缺失和过短的meta description"""
import os, re

FIXES = {
    # === NO_DESC 缺失页面 ===
    './ai-prompt-generator/index.html': 'AI提示词生成器，为ChatGPT、Claude、Midjourney和DALL-E生成高质量AI提示词。选择任务类型和风格，一键优化Prompt模板，提升AI输出质量。适合内容创作者和AI爱好者，纯前端处理无需注册。',
    './amortization-calculator/index.html': '在线贷款摊销计算器，计算等额本息还款的月供、总利息和还款明细。输入贷款金额、年利率和期限，自动生成逐年还款计划表。适合房贷、车贷和消费贷款规划，纯前端计算无需注册。',
    './apa-citation-generator/index.html': '免费APA第七版引用生成器，为书籍、期刊文章、网页等自动生成标准APA格式参考文献。输入作者、标题、出版年份等信息，一键获取规范引用条目，学术论文写作必备工具。',
    './api-key-generator/index.html': '在线API密钥生成器，快速生成安全的随机API密钥和访问令牌。支持自定义长度、字符集和前缀格式，适用于后端开发和API安全测试。所有密钥在浏览器本地生成，不上传服务器。',
    './area-calculator/index.html': '免费在线面积计算器，计算圆形、三角形、矩形、梯形等多种几何图形的面积。输入边长或半径即可获得精确面积结果，支持常用单位换算，适合学生学习和工程计算使用。',
    './audio-speed-changer/index.html': '在线音频变速播放器，调整MP3等音频文件的播放速度而不改变音调。支持0.5倍到2倍变速，适合语言学习、播客加速收听和音乐练习场景。纯前端Web Audio API处理，不上传服务器。',
    './badge-generator/index.html': '免费在线徽章生成器，可视化创建CSS标签和徽章样式。支持自定义文字、颜色、圆角和边框，实时预览效果并一键复制CSS代码。适合网页开发者和UI设计师快速创建状态标签。',
    './bezier-curve-generator/index.html': '在线贝塞尔曲线生成器，可视化编辑CSS cubic-bezier缓动函数。拖拽控制点实时调整动画曲线，一键复制CSS代码。前端开发者和动画设计师的必备工具，无需注册。',
    './bill-splitter/index.html': '免费账单分摊计算器，输入总金额、人数、小费比例和税率，一键算出每人应付金额。支持自定义分摊比例和舍入设置，适合餐厅聚餐、旅行费用和合租分摊等场景。',
    './binary-calculator/index.html': '在线二进制计算器，支持二进制加法、减法、乘法、除法和位运算。同时提供二进制与十进制、十六进制、八进制互转。适合计算机科学学生和嵌入式开发者日常使用。',
    './body-fat-calculator/index.html': '免费体脂率计算器，基于美国海军方法精确估算身体脂肪百分比。输入颈围、腰围、身高和体重，自动计算体脂率和脂肪重量，帮助健身减脂目标管理。纯前端计算无需注册。',
    './budget-planner/index.html': '免费在线预算规划器，创建月度收支预算并追踪消费。自定义收入和支出类别，可视化预算执行进度。帮助个人和家庭实现财务目标，所有数据本地存储保障隐私安全。',
    './click-speed-test/index.html': '免费点击速度测试，测量每秒点击次数CPS。支持多种测试时长模式，实时显示点击速度和排行榜。挑战你的手速极限，和朋友比试谁更快，纯前端无需下载。',
    './code-diff/index.html': '在线代码差异对比工具，并排显示两份代码的差异。支持语法高亮、行内差异标记和差异导航，适合代码审查和版本对比。纯前端处理保障代码安全，无需注册。',
    './css-border-radius-generator/index.html': '免费CSS圆角生成器，可视化调整border-radius四个角的圆角大小。实时预览效果，一键复制CSS代码。支持圆形、椭圆和胶囊等预设形状，前端开发必备工具。',
    './css-cursor-visualizer/index.html': '免费CSS光标样式可视化工具，预览所有CSS cursor属性值的效果。悬停查看每种光标样式，一键复制cursor CSS代码，适合前端开发者和UI设计师使用。',
    './css-flexbox-playground/index.html': '免费CSS Flexbox交互式练习场，可视化调整flex容器和子元素属性。实时预览布局效果，理解justify-content、align-items等核心概念，前端布局学习利器。',
    './css-has-selector-generator/index.html': '免费CSS :has()选择器生成器，可视化构建现代CSS父选择器规则。选择目标元素和条件，自动生成:has()伪类代码，支持嵌套和组合选择器，前端开发效率工具。',
    './css-layer-generator/index.html': '免费CSS @layer层叠层生成器，可视化管理CSS层叠优先级。创建和排序样式层，预览优先级效果，一键复制@layer CSS代码，解决大型项目样式冲突问题。',
    './css-noise-texture-generator/index.html': '免费CSS噪点纹理生成器，通过纯CSS生成噪点颗粒纹理背景。支持调节噪点密度、透明度和颜色，实时预览效果并复制CSS代码。无需图片，适合网页背景设计。',
    './css-progress-bar-generator/index.html': '免费CSS进度条生成器，可视化创建带动画效果的进度条。自定义颜色、宽度、圆角和动画样式，实时预览并一键复制HTML+CSS代码。适合仪表盘和数据展示UI设计。',
    './css-scroll-driven-animation/index.html': '免费CSS滚动驱动动画生成器，可视化创建scroll()和view()时间线动画。设置触发区间和关键帧，实时预览动画效果，自动生成标准CSS Animation Timeline代码。',
    './css-shape-generator/index.html': '免费CSS形状生成器，通过clip-path属性创建圆形、三角形、多边形和星形等CSS形状。拖拽调整顶点位置，实时预览并复制CSS代码，前端创意设计必备工具。',
    './css-to-scss/index.html': '免费在线CSS转SCSS转换器，将CSS代码智能转换为SCSS嵌套语法。自动提取公共属性生成嵌套结构，支持变量提取和Mixin建议，CSS代码重构效率工具。',
    './css-typography-scale-generator/index.html': '免费CSS排版比例生成器，基于模数比例生成字体大小体系。选择黄金比例、纯四度等经典比例，自动生成h1-h6和正文的字号层级，一键导出CSS变量或Tailwind配置。',
    './data-uri-generator/index.html': '免费Data URI生成器，将图片和文件转换为Base64 Data URI格式。支持拖拽上传，实时预览转换结果，一键复制Data URI代码。适合将小图片内嵌到HTML和CSS中。',
    './deposit-calculator/index.html': '免费存款利息计算器，计算定期存款的到期本息总额和利息收益。支持整存整取、零存整取等多种存款方式，输入本金、年利率和存期即可获得精确结果，理财规划好帮手。',
    './dns-lookup/index.html': '免费DNS查询工具，查询域名DNS记录包括A、AAAA、CNAME、MX、TXT和NS记录。快速诊断域名解析问题，支持多种记录类型，网络管理员和站长必备工具。',
    './domain-name-generator/index.html': '免费在线域名生成器，输入关键词自动生成创意域名建议。支持多种后缀组合，检查域名可用性，帮助创业者快速找到品牌域名。域名搜索和品牌命名一站式工具。',
    './electricity-calculator/index.html': '免费电费计算器，根据电器功率和使用时长计算每日、每月电费。支持多种电器预设，自定义电价，帮助家庭和企业估算用电成本，节能省电好帮手。',

    # en pages
    './en/jwt-debugger/index.html': 'Free online JWT debugger to decode and inspect JSON Web Tokens. View header, payload, and signature details. Supports HS256, RS256 algorithms. Verify signatures with secret key. All processing done in browser.',
    './en/keyboard-event-tester/index.html': 'Free keyboard event tester to inspect JavaScript keyboard events in real time. View key codes, key values, modifier states. Essential for web developers debugging keyboard shortcuts and input handling.',
    './en/open-graph-debugger/index.html': 'Free Open Graph debugger to preview how your page appears on social media. Check OG title, description, and image tags for Facebook, Twitter, and LinkedIn. Validate meta tags without server upload.',
    './en/regex-debugger/index.html': 'Free online regex debugger with real-time matching and explanation. Test regular expressions with syntax highlighting, match groups, and cheat sheet. Essential tool for developers working with text patterns.',
    './en/webhook-debugger/index.html': 'Free webhook debugger to capture and inspect HTTP requests in real time. Generate unique endpoint URLs, view headers and payloads. Perfect for testing webhooks, APIs, and integrations during development.',

    # 更多中文页面
    './expense-tracker/index.html': '免费在线记账本，轻松记录日常收支并自动生成月度统计报表。支持分类管理收入和支出，可视化消费结构分析。帮助个人和家庭掌握财务状况，所有数据本地存储保障隐私。',
    './factorial-calculator/index.html': '免费阶乘计算器，快速计算n!阶乘值和排列组合数。支持大数计算，同时显示阶乘分解过程。适合数学学习、概率统计计算和编程算法验证，纯前端计算无需注册。',
    './file-to-base64/index.html': '免费在线文件转Base64编码工具，将任意文件转换为Base64字符串。支持图片、文档、音频等格式，拖拽上传即可转换，一键复制编码结果。适合API开发和数据嵌入场景。',
    './flashcard-maker/index.html': '免费在线闪卡制作工具，创建自定义学习卡片辅助记忆。支持正面问题和背面答案，分类管理卡片组，适合语言学习、考试复习和知识记忆。纯前端本地存储，无需注册。',
    './fuel-calculator/index.html': '免费油耗计算器，根据行驶里程和油耗量计算百公里油耗和每公里油费。支持多种单位，帮助车主评估出行成本和车辆燃油效率。长途旅行和日常通勤的实用工具。',
    './glitch-text-generator/index.html': '故障文字生成器，将普通文字转换为赛博朋克风格的Glitch特效文字。支持多种故障效果强度，生成可复制粘贴到社交媒体的特殊Unicode字符，创意文案设计利器。',
    './gradient-button-generator/index.html': '免费CSS渐变按钮生成器，可视化创建漂亮的渐变按钮样式。自定义按钮文字、渐变颜色、圆角和阴影效果，实时预览并一键复制HTML+CSS代码，网页UI设计必备。',
    './gradient-palette-generator/index.html': '免费渐变色板生成器，浏览和收集精美的渐变色彩搭配方案。支持线性渐变和径向渐变预览，一键复制CSS渐变代码。适合网页设计、品牌配色和UI界面灵感参考。',
    './gratitude-journal/index.html': '免费感恩日记工具，每天记录三件值得感恩的事，培养积极心态和幸福感。支持日期追踪、心情记录和回顾查看，数据本地存储保障隐私，心理健康自我关怀好帮手。',
    './habit-tracker/index.html': '免费在线习惯追踪器，建立和坚持好习惯的打卡工具。自定义每日习惯，追踪连续打卡天数，可视化月度完成进度。支持周视图和月视图，数据本地存储无需注册。',
    './hashtag-generator/index.html': '免费在线标签生成器，根据关键词自动生成社交媒体热门话题标签。支持Instagram、Twitter、TikTok等平台，提供标签流行度参考。社交媒体运营和内容营销效率工具。',
    './html-button-generator/index.html': '免费HTML按钮生成器，可视化创建漂亮的CSS按钮样式。自定义文字、颜色、大小、圆角和悬停效果，实时预览并复制HTML+CSS代码。前端开发和网页设计必备。',
    './html-email-template/index.html': '免费HTML邮件模板生成器，创建响应式邮件模板。支持多种预设布局，可视化编辑内容和样式，一键导出HTML邮件代码。适合营销邮件、通知邮件和newsletter设计。',
    './html-image-map-generator/index.html': '免费HTML图片热区地图生成器，在图片上创建可点击的交互式热区。支持矩形、圆形和多边形热区，自动生成HTML map标签代码。适合网页导航图和产品展示。',
    './html-table-of-contents/index.html': '免费HTML目录生成器，根据标题层级自动生成文章目录树。支持自定义缩进和编号样式，一键复制HTML目录代码。适合博客文章、文档页面和教程网站的内容导航。',
    './ideal-weight-calculator/index.html': '免费理想体重计算器，基于Devine、Hamwi、Miller和Robinson多种医学公式计算理想体重范围。输入身高和性别，获取个性化健康体重建议，健身减重目标参考。',
    './interval-timer/index.html': '免费间歇计时器，自定义工作和休息时间的循环计时器。支持多组训练、自定义标签和声音提醒。适合HIIT训练、番茄工作法和演讲计时，纯前端无需下载。',
    './investment-calculator/index.html': '免费投资收益计算器，计算复利投资和定投的未来价值。输入初始金额、月投入、年化收益率和投资年限，自动生成本息增长图表。理财规划和退休储蓄的必备工具。',
    './js-obfuscator/index.html': '免费在线JavaScript混淆器，将JS代码转换为难以阅读的混淆版本。支持多种混淆选项，保护前端代码不被轻易复制和篡改。纯前端处理，代码不上传服务器。',
    './json-to-graphql/index.html': '免费JSON转GraphQL工具，根据JSON数据自动生成GraphQL Schema和类型定义。支持嵌套对象和数组，一键复制Schema代码。API开发中快速搭建GraphQL服务的效率工具。',
    './json-to-toml/index.html': '免费JSON转TOML配置格式转换器，将JSON配置文件转换为更简洁的TOML格式。支持嵌套结构和数组，实时预览转换结果。适合Rust、Python项目配置管理。',
    './jwt-generator/index.html': '免费在线JWT Token生成器，创建签名的JSON Web Token。支持HS256、HS384、HS512算法，自定义Payload和过期时间。API认证和授权测试的实用工具。',
    './latex-equation-editor/index.html': '免费在线LaTeX公式编辑器，可视化编辑数学公式并实时预览渲染效果。支持分数、积分、矩阵和希腊字母等常用符号，一键复制LaTeX代码。学术论文和数学作业必备。',
    './license-generator/index.html': '免费开源许可证生成器，一键生成MIT、Apache 2.0、GPLv3、BSD等主流开源协议文本。填写作者和年份信息即可获取标准许可证内容，开源项目发布的必备工具。',
    './margin-calculator/index.html': '免费利润率计算器，计算毛利率、净利率和加价率。输入成本和售价即可获取利润金额和各项利润率百分比，支持反向推算目标售价。电商定价和商业计划书财务测算必备。',
    './meal-planner/index.html': '免费膳食计划器，规划每周每日的饮食菜单。支持自定义餐次和食谱，生成购物清单。帮助家庭合理安排饮食，健康营养管理好帮手，数据本地存储无需注册。',
    './monitor-test/index.html': '免费显示器测试工具，检测屏幕坏点、色彩还原、对比度和响应时间。提供纯色测试、渐变测试和几何测试，帮助评估显示器质量。购买新显示器时的必备检测工具。',
    './mortgage-calculator/index.html': '免费在线房贷计算器，计算等额本息和等额本金两种还款方式的月供和总利息。输入房价、首付比例和贷款年限，自动生成还款计划表。购房贷款决策的必备计算工具。',
    './net-worth-calculator/index.html': '免费净资产计算器，快速计算个人或家庭净资产。输入资产和负债各项金额，自动汇总并分析资产负债结构。个人财务规划和财富管理的基础工具，纯前端计算。',
    './periodic-table/index.html': '免费在线元素周期表，交互式查看118种化学元素的详细信息。点击元素查看原子序数、原子量、电子排布和物理性质。化学学习、教学演示和科学研究参考工具。',
    './pet-age-calculator/index.html': '免费宠物年龄计算器，将猫狗的实际年龄换算为人类等效年龄。基于最新兽医学研究，考虑品种和体型差异。帮助宠物主人了解爱宠的生命阶段和健康需求。',
    './photo-collage/index.html': '免费图片拼贴制作工具，上传多张照片选择网格布局创建拼贴画。支持调整间距、圆角和背景色，一键导出高清拼贴图片。适合社交媒体分享和照片整理展示。',
    './photo-editor/index.html': '免费在线图片编辑器，提供裁剪、滤镜、调整亮度对比度和添加文字等基础编辑功能。支持JPG、PNG、WebP格式，所有处理在浏览器本地完成保障隐私安全。',
    './placeholder-image-generator/index.html': '免费在线占位图生成器，快速生成自定义尺寸和颜色的占位图片。支持纯色、渐变和文字标注，一键下载PNG图片。适合网页原型设计和开发阶段的图片占位需求。',
    './pregnancy-due-date/index.html': '免费预产期计算器，根据末次月经日期或受孕日期计算预产期和当前孕周。基于Naegele规则，提供孕期里程碑时间线，帮助准妈妈了解胎儿发育进程。',
    './pythagorean-calculator/index.html': '免费勾股定理计算器，输入直角三角形任意两条边自动计算第三边长度。支持多种单位，显示计算步骤和公式。数学学习和工程测量中的实用计算工具。',
    './python-formatter/index.html': '免费Python代码格式化工具，按照PEP 8规范自动美化Python代码。支持缩进调整、换行优化和导入排序，一键复制格式化后代码。Python开发者的代码规范利器。',
    './random-name-generator/index.html': '免费随机名字生成器，按性别和风格生成随机姓名。支持中文和英文名字，适合小说角色命名、游戏昵称和测试数据生成。一键生成批量随机名字。',
    './regex-builder/index.html': '免费在线正则表达式测试工具，实时匹配文本并高亮显示结果。支持常用正则模板、语法参考和分组解释。程序员调试正则表达式和文本处理的必备工具。',
    './rem-px-converter/index.html': '免费PX REM EM单位转换器，在前端CSS单位之间快速换算。输入PX值自动转换为REM和EM，支持自定义根字号。响应式设计和CSS布局的实用换算工具。',
    './resolution-calculator/index.html': '免费分辨率计算器，根据屏幕宽度和高度计算纵横比、像素总数和PPI。支持常见设备分辨率预设，适合UI设计师和前端开发者确定屏幕适配方案。',
    './rss-feed-generator/index.html': '免费在线RSS Feed生成器，创建标准RSS 2.0格式的XML订阅源。填写频道信息和文章条目，一键生成RSS XML代码。适合博客和内容网站的订阅源创建。',
    './salary-calculator/index.html': '免费薪资计算器，在时薪、日薪、月薪和年薪之间互相转换。输入任意一项自动计算其他三项，支持自定义工作天数和工时。求职者和HR薪资谈判的实用工具。',
    './savings-calculator/index.html': '免费储蓄计算器，制定储蓄目标并计算达成所需时间和每月存款额。考虑复利收益，可视化储蓄进度。帮助实现购房、旅行和教育等储蓄目标。',
    './screen-resolution-simulator/index.html': '免费屏幕分辨率模拟器，预览网页在不同设备和分辨率下的显示效果。支持手机、平板和桌面等多种设备预设。前端响应式设计测试和调试的实用工具。',
    './shipping-calculator/index.html': '免费运费计算器，根据包裹重量、尺寸和目的地估算运费。支持多种快递公司参考费率，帮助电商卖家和网购用户评估物流成本。',
    './shopping-list-generator/index.html': '免费购物清单生成器，按食品、日用品等分类快速创建购物清单。支持添加数量和备注，勾选已购项目。超市购物和家庭采购的便捷管理工具。',
    './social-card-preview/index.html': '免费社交卡片预览工具，输入URL预览网页在Facebook、Twitter和LinkedIn的分享卡片效果。检测OG标签和Twitter Card元数据，优化社交媒体展示。',
    './statistics-calculator/index.html': '免费在线统计分析计算器，计算均值、中位数、标准差、方差和相关系数等常用统计指标。支持数据导入和结果导出，适合学生和研究人员的数据分析需求。',
    './tailwind-to-css/index.html': '免费在线Tailwind转CSS工具，将Tailwind工具类转换为标准CSS样式。支持颜色、间距、排版等属性映射，帮助从Tailwind迁移到原生CSS的开发者。',
    './team-generator/index.html': '免费随机分组工具，将人员名单随机分配到指定数量的小组中。支持自定义组数和每组人数，一键打乱重新分组。适合团建活动、课堂分组和比赛抽签场景。',
    './text-summarizer/index.html': '免费在线摘要生成器，智能提取文章核心要点生成简洁摘要。支持自定义摘要长度，适合快速阅读长文章和文档。提升阅读效率的信息提取工具。',
    './text-to-binary/index.html': '免费文本与二进制互转工具，支持文本转二进制和二进制转文本。提供UTF-8、ASCII和Unicode多种编码格式，显示十六进制和八进制输出。计算机基础学习工具。',
    './text-to-hex/index.html': '免费文本转十六进制工具，将文本字符串转换为十六进制编码并支持反向解码。支持空格分隔和连续格式，适合编码学习、数据分析和调试场景。',
    './url-builder/index.html': '免费在线URL构建器，可视化构建带查询参数和UTM追踪参数的URL。支持添加多个参数，自动URL编码，一键复制完整URL。营销推广链接构建和API调试工具。',
    './url-decoder/index.html': '免费在线URL解码工具，将百分号编码的URL还原为可读字符串。同时支持URL编码，解析查询参数为键值对。Web开发和SEO优化中的常用工具。',
    './vision-test/index.html': '免费在线视力测试工具，提供标准Snellen视力表和Tumbling E视力表。在家初步评估视力水平，了解是否需要进一步眼科检查。仅供参考，不能替代专业诊断。',
    './volume-calculator/index.html': '免费体积计算器，计算球体、立方体、圆柱体和圆锥体等几何体的体积。输入尺寸参数自动计算，支持多种单位。数学学习和工程计算的实用工具。',
    './water-intake-calculator/index.html': '免费每日饮水量计算器，根据体重、活动水平和气候条件计算每日推荐饮水量。提供科学饮水建议，帮助保持水分平衡和身体健康。健康生活方式的实用小工具。',
    './year-progress/index.html': '免费年度进度条，可视化显示今年已过去的时间百分比。精确到秒的年度倒计时，支持查看本年剩余天数、周数和月数。时间管理和年度目标追踪的激励工具。',

    # === 过短页面优化 (<100 chars) ===
    './athletic-performance-calculator/index.html': '免费在线运动表现计算器，评估BMI、体脂率、基础代谢率和力量Wilks评分。输入年龄、体重和力量数据获取综合体能分析报告，健身爱好者和运动员训练评估工具。纯前端计算无需注册。',
    './ats-resume-checker/index.html': '免费ATS简历检查器，分析简历是否能通过招聘系统筛选。检测关键词匹配度、格式兼容性和可读性评分，提供优化建议提升简历通过率。求职者提高面试邀约率的必备工具。',
    './audio-compressor/index.html': '免费在线音频压缩工具，压缩MP3、WAV、OGG、AAC音频文件大小。可调节比特率和采样率，实时预览压缩效果。适合减少音频存储空间和优化网页加载速度，文件不上传服务器。',
    './audio-crossfade/index.html': '免费在线音频交叉渐变工具，将两段音频平滑过渡拼接。支持线性渐变、等功率渐变和S曲线渐变模式，可调节交叉时长和曲线类型。播客制作和音乐混音的实用音频编辑工具。',
    './audio-echo-effect/index.html': '免费在线音频回声效果工具，为音频添加延迟回声。支持单回声、多重回声和乒乓回声模式，可调节延迟时间、衰减率和反馈量。音乐制作和音效设计的创意工具，纯前端Web Audio API处理。',
    './audio-fade-generator/index.html': '免费在线音频淡入淡出工具，为音频开头和结尾添加平滑过渡效果。支持自定义淡入淡出时长和线性、指数等曲线类型。播客制作和视频配音的音频后期处理必备工具。',
    './audio-loop-maker/index.html': '免费在线音频循环制作工具，将音频片段创建为无缝循环。支持自动检测循环点和手动设置起止位置，交叉渐变平滑衔接。音乐制作、游戏音效和背景音乐循环的实用工具。',
    './audio-pitch-shifter/index.html': '免费在线音频变调工具，调整音频音调而不改变播放速度。支持升降调半音和音分级别微调，实时预览变调效果。音乐练习降调跟唱和创意音效设计的实用工具。',
    './audio-recorder/index.html': '免费在线录音机，使用浏览器麦克风直接录制音频。支持暂停、回放和下载WAV/WebM格式录音文件。无需安装软件，会议记录、课堂笔记和语音备忘录的便捷工具。',
    './audio-reverse-player/index.html': '免费在线音频倒放工具，将音频文件反向播放创造独特音效。支持WAV和MP3格式，可下载反转后的音频。音乐创意制作和隐藏信息发现的趣味音频工具。',
    './audio-reverser/index.html': '免费在线音频倒放器，将MP3、WAV、OGG、M4A音频文件反向播放。一键上传即可获得倒放音频并下载。适合音乐制作、音频分析寻找隐藏信息和创意音效设计。',
    './audio-spectrum-analyzer/index.html': '免费在线音频频谱分析仪，实时显示麦克风输入音频的频率分布。支持FFT频谱分析、波形可视化和频率峰值识别。音频工程调音和声学分析的专业级可视化工具。',
    './audio-visualizer/index.html': '免费在线音频可视化器，实时显示音频频谱和波形动画。支持麦克风输入和本地音频文件，提供频谱、波形和粒子等多种可视化样式。音乐播放和直播场景的视觉增强工具。',
    './audio-volume-adjuster/index.html': '免费在线音频音量调节器，上传音频文件调整整体音量大小。支持实时预览和导出调节后音频。解决音频音量过小或过大的问题，播客和视频制作者的音频后期处理工具。',
    './audio-volume-booster/index.html': '免费在线音频音量增强器，一键放大音频文件音量。支持MP3、WAV、OGG和M4A格式，最大可提升至500%。解决录音音量过低问题，无需注册文件不上传服务器。',
    './audio-waveform-visualizer/index.html': '免费在线音频波形可视化工具，上传音频文件生成实时波形图。支持播放控制、波形颜色自定义、缩放和截图导出。播客和音乐制作的音频分析利器，纯前端处理保护隐私。',
    './auto-refinance-calculator/index.html': '免费在线汽车再融资计算器，对比当前贷款与转贷方案。计算再融资可节省的利息和月供差额，可视化节省金额。帮助车主做出最优贷款再融资决策，纯前端计算无需注册。',
    './babel-config-generator/index.html': '免费在线Babel配置生成器，可视化生成Babel JavaScript编译配置。选择预设、插件和目标浏览器，一键复制babel.config.js代码。前端开发者搭建构建工具链的效率利器。',
    './baby-name-generator/index.html': '免费在线宝宝名字生成器，按性别、首字母和风格生成中文英文名字建议。支持一键收藏喜欢的名字并批量导出。准父母给宝宝取名的灵感工具，纯前端处理。',
    './baby-weight-percentile/index.html': '免费婴儿体重百分位计算器，基于WHO生长标准评估宝宝体重发育水平。输入性别、月龄和体重获取百分位排名。帮助家长科学监测婴儿生长发育状况，纯前端计算。',
    './backdoor-roth-calculator/index.html': '免费Backdoor Roth IRA计算器，计算后门Roth转换金额及税务影响。考虑pro-rata规则精确估算应纳税额。高收入人群退休规划的必备工具，纯前端计算数据不上传。',
    './backlink-checker/index.html': '免费反链检测工具，快速检测网站反向链接状态和搜索引擎索引情况。输入URL查看页面是否可被索引，检测robots.txt规则和meta标签设置。SEO优化诊断工具。',
    './bandwidth-calculator/index.html': '免费在线带宽计算器，计算文件下载时间、所需带宽和数据传输速度。支持Kbps、Mbps和Gbps多种单位。网络工程师和运维人员估算带宽需求的实用计算工具。',
    './bar-chart-maker/index.html': '免费在线柱状图生成器，创建自定义数据的柱状图。Canvas纯前端渲染支持多种配色方案，一键导出PNG高清图片。数据可视化展示和统计对比分析的便捷图表工具。',
    './barcode-reader/index.html': '免费在线条形码阅读器，上传图片识别QR Code、Code 128和Code 39等条形码。纯前端解码处理，图片不上传服务器。快递查件和商品条码识别的实用工具。',
    './barcode-scanner/index.html': '免费在线条码扫描器，使用摄像头实时扫描QR码和条形码。支持多种条码格式，纯前端处理保护隐私。无需下载App，网页端快速扫码解决方案。',
    './basal-metabolic-rate/index.html': '免费基础代谢率BMR计算器，基于Mifflin-St Jeor公式精确计算每日能量消耗。输入年龄、身高、体重和活动水平，获取减肥或增肌所需的热量摄入建议。',
    './base32-encode-decode/index.html': '免费在线Base32编解码工具，支持RFC 4648标准Base32编码和解码。文本与Base32格式互转，纯前端本地处理保障数据安全。编码学习和数据转换实用工具。',
    './base32-encode/index.html': '免费在线Base32编码工具，将文本字符串编码为Base32格式。支持RFC 4648标准编码，一键复制编码结果。数据编码和API开发中的常用转换工具。',
    './base45-encoder/index.html': '免费在线Base45编码解码工具，支持文本与Base45格式互转符合RFC 9285标准。适用于QR码和数字健康证书等场景。纯前端本地处理保障数据安全。',
}

def fix_meta(fp, new_desc):
    try:
        with open(fp, 'r') as f:
            content = f.read()

        if '<meta name="description"' in content:
            content = re.sub(
                r'<meta name="description" content="[^"]*">',
                f'<meta name="description" content="{new_desc}">',
                content
            )
        else:
            content = re.sub(
                r'(<meta charset="[^"]+">)',
                f'\\1\n  <meta name="description" content="{new_desc}">',
                content, count=1
            )

        with open(fp, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f'  ERROR: {fp}: {e}')
        return False

count = 0
for fp, desc in FIXES.items():
    if os.path.exists(fp):
        if fix_meta(fp, desc):
            print(f'✓ {fp}')
            count += 1
    else:
        print(f'✗ NOT FOUND: {fp}')

print(f'\nFixed: {count} pages')

#!/usr/bin/env python3
"""
补齐首页缺失工具card - v2。
生成干净的card HTML并插入到首页。
"""
import os, re

BASE = '/home/chison/tools-site'

SKIP_DIRS = {'en','tests','scripts','quality','tools','docs','css','js','libs',
             'data','network','text','security','media','dev','math','seo','design',
             'creative','time','office','utility','calc','category','convert','converter',
             'blog','about','contact','privacy','terms','privacy-policy','chrome-extension',
             'quality-reports','.gsc-data','.git'}

ICON_MAP = {
    'calculator': '🧮','calc': '🔢','time': '🕐','clock': '⏰','timer': '⏱️','stopwatch': '⏱️',
    'password': '🔑','encrypt': '🔒','decrypt': '🔓','hash': '#️⃣','security': '🔒',
    'json': '📋','xml': '📰','csv': '📊','yaml': '📝','toml': '📝',
    'base64': '🔐','encode': '🔐','decode': '🔓',
    'pdf': '📄','image': '🖼️','photo': '📷','video': '🎬','audio': '🔊',
    'text': '📝','string': '📝','word': '📝','letter': '🔤',
    'css': '🎨','html': '🌐','js': '📜','code': '💻','sql': '🗄️',
    'color': '🎨','gradient': '🌈','palette': '🎨','design': '🎨',
    'format': '✨','beautify': '✨','minify': '📦',
    'qr': '📱','barcode': '📊',
    'convert': '🔄','unit': '📏',
    'check': '✅','test': '🧪','valid': '✅',
    'diff': '🔍','compare': '🔍',
    'regex': '🔍','pattern': '🔍',
    'number': '🔢','random': '🎲','dice': '🎲',
    'date': '📅','calendar': '🗓️',
    'sort': '🔤','filter': '🔍','list': '📋',
    'counter': '🔢','count': '🔢',
    'split': '✂️','merge': '🔗','join': '🔗',
    'translate': '🌐','language': '🗣️','speech': '🎙️',
    'morse': '📡','cipher': '🔐','caesar': '🔐',
    'jwt': '🎫','token': '🎫','uuid': '🆔','id': '🆔',
    'git': '📦','docker': '🐳','npm': '📦',
    'chart': '📊','graph': '📈','diagram': '📐',
    'game': '🎮','fun': '🎮','joke': '😄','meme': '😂',
    'health': '💊','bmi': '⚖️','medical': '🏥',
    'finance': '💰','loan': '🏦','mortgage': '🏠','tax': '🧾',
    'budget': '💵','investment': '📈','stock': '📈','crypto': '₿',
    'saving': '🏦','interest': '💹','retirement': '👴',
    'seo': '🔍','meta': '🏷️','sitemap': '🗺️',
    'dns': '🌐','domain': '🌐','ip': '📍','network': '🌐',
    'ping': '📡','port': '🔌','proxy': '🔄',
    'markdown': '📝','readme': '📖',
    'cron': '⏰','schedule': '📅',
    'url': '🔗','link': '🔗',
    'compress': '🗜️','file': '📁',
    'emoji': '😀','sticker': '😀',
    'note': '📝','memo': '📝','todo': '✅',
    'food': '🍔','recipe': '🍳','cooking': '🍳','coffee': '☕',
    'pet': '🐾','dog': '🐕','cat': '🐱',
    'car': '🚗','travel': '✈️','map': '🗺️',
    'sport': '⚽','fitness': '💪','workout': '🏋️',
    'piano': '🎹','music': '🎵','drum': '🥁',
    'draw': '✏️','paint': '🎨','art': '🎨',
    'signature': '✍️','sign': '✍️',
    'keyboard': '⌨️','mouse': '🖱️','screen': '🖥️',
    'pixel': '📐','resolution': '📐',
    '3d': '🧊','transform': '🔄',
    'age': '🎂','birthday': '🎂',
    'name': '📛','generator': '🪄','maker': '🪄',
    'remove': '🗑️','delete': '🗑️','clean': '🧹',
    'edit': '✏️','view': '👁️','preview': '👁️',
    'record': '🔴','recorder': '🔴',
    'scan': '📡','reader': '📖',
    'upload': '📤','download': '📥',
    'export': '📤','import': '📥',
    'print': '🖨️','copy': '📋','paste': '📋',
    'share': '🔗','social': '🔗',
    'team': '👥','group': '👥',
    'card': '🃏','deck': '🃏',
    'background': '🖼️','gradient': '🌈',
    'icon': '🔣','logo': '🏷️',
    'font': '🔤','typography': '🔤',
    'border': '⬜','shadow': '⬛',
    'loading': '⏳','spinner': '⏳','progress': '📊',
    'animation': '✨','transition': '✨',
    'web': '🌐','site': '🌐','page': '🌐',
    'checklist': '✅','todo': '✅',
}

CAT_KEYWORDS = {
    'dev-tools': ['json','xml','yaml','toml','csv','sql','regex','api','curl','http',
                  'code','format','beautify','minify','diff','jwt','token','uuid',
                  'git','docker','npm','base64','encode','decode','hash','md5','sha',
                  'cron','bash','shell','npm-package','makefile','nginx','apache',
                  'markdown','readme','changelog','license','dockerfile','docker-compose',
                  'unicode','ascii','hex','binary','octal','decimal','byte',
                  'validator','linter','checker','parser','extractor','viewer',
                  'editor','playground','sandbox','tester','debugger',
                  'migration','seeder','mock','stub','dummy',
                  'webhook','websocket','sse','rpc','rest',
                  'csp','csrf','cors','xss','headers','cookie',
                  'prisma','drizzle','sequelize','kysely',
                  'openapi','graphql','swagger',
                  'dotenv','env','config','schema',
                  'webpack','vite','rollup','babel','eslint','prettier',
                  'tsconfig','postcss','tailwind','sass','scss','less',
                  'typescript','javascript','jsx','tsx',
                  'pre-commit','commitlint','husky',
                  'semver','semantic-version',
                  'dev-','debounce','throttle','bookmarklet',
                  'cicd','pipeline','deploy','ci-cd'],
    'finance-tools': ['loan','mortgage','tax','budget','investment','stock',
                      'dividend','annuity','depreciation','amortization',
                      'profit','revenue','cost','expense','income','salary',
                      'paycheck','payroll','commission','bonus','invoice','receipt',
                      'bill','payment','debt','credit','insurance','premium',
                      'valuation','appraisal','worth','equity','asset',
                      'liability','cashflow','balance','ledger','accounting',
                      'fiscal','audit','compliance',
                      'crypto','bitcoin','ethereum','defi','staking',
                      'retirement','pension','saving','interest','dividend',
                      'credit-card','credit-score',
                      'inflation','purchasing-power',
                      'payback','breakeven','break-even',
                      'finance','financial','money','monetary',
                      'fund','funding','capital','venture',
                      'net-worth','wealth','rich','fire',
                      'refinance','refinancing',
                      'down-payment','closing-cost',
                      'apr','apy','cd-ladder',
                      '401k','ira','roth','sep','solo',
                      'rmd','rmd-table','retirement',
                      'nsc','ppf','kisan-vikas','rd-calculator',
                      'swp','swr','safe-withdrawal'],
    'calc-tools': ['calculator','calc-','compute','solver','formula',
                   'math','mathematics','algebra','geometry',
                   'statistic','probability',
                   'percentage','percent','ratio','proportion',
                   'average','mean','median','mode',
                   'standard-deviation','variance',
                   'rounding','round-','sig-fig',
                   'scientific-calculator','scientific-notation',
                   'prime-','factor','gcd','lcm',
                   'fraction','decimal',
                   'square-root','cube-root','power','exponent',
                   'logarithm','log-',
                   'sin-','cos-','tan-','trig',
                   'area','volume','perimeter','surface',
                   'triangle','circle','rectangle','sphere','cylinder',
                   'quadratic','polynomial','equation',
                   'matrix','vector',
                   'pythagorean','pythagoras',
                   'armstrong','collatz','palindrome',
                   'karnaugh','truth-table','logic-gate',
                   'boolean','binary','hex','octal',
                   'bitwise','binary-operations',
                   'combination','permutation',
                   'sequence','series','fibonacci'],
    'health-tools': ['health','medical','bmi','diet','nutrition','calorie',
                     'weight','fitness','exercise','workout',
                     'sleep','stress','anxiety','burnout',
                     'blood','heart','pulse','pressure','cholesterol','glucose',
                     'vitamin','mineral','supplement','medication','dosage',
                     'pregnancy','baby','child','pediatric','growth',
                     'life-expectancy','mortality','longevity',
                     'alcohol','bac','caffeine','smoking','drug',
                     'mental','psychological','therapy',
                     'menstrual','ovulation','period',
                     'macro','macros','macro-nutrient','protein','carb',
                     'tdee','bmr','rmr','energy-expenditure',
                     'body-fat','lean-body','muscle',
                     'waist-hip','body-measurement','body-shape',
                     'vo2max','vo2-max',
                     'water-intake','hydration',
                     'sobriety','addiction',
                     'symptom','checker','diagnosis',
                     'blood-donation','blood-type',
                     'vision','hearing','eye','ear',
                     'kidney','liver','lung','thyroid',
                     'diabetes','a1c','ascvd','framingham',
                     'covid','vaccine','vaccination',
                     'first-aid','cpr','emergency',
                     'metabolism','metabolic',
                     'posture','ergonomics',
                     'reaction-test','reaction-time',
                     'stretching','flexibility','yoga',
                     'meditation','mindfulness','breathing'],
    'design-tools': ['design','color','gradient','palette','font','typography',
                     'icon','logo','brand','style','theme','template',
                     'layout','grid','flexbox','responsive',
                     'animation','transition','transform','effect',
                     'shadow','border','radius','spacing',
                     'background','pattern','texture',
                     'svg','canvas','vector','illustration',
                     'ui','ux','wireframe','mockup','prototype',
                     'css-','stylesheet','style',
                     '3d','3d-transform','perspective',
                     'blob','shape','neumorphism','glassmorphism',
                     'clip-path','mask','filter',
                     'bezier','cubic-bezier','easing',
                     'blend-mode','backdrop','overlay',
                     'aspect-ratio','viewport','container',
                     'neumorphic','neumorphism',
                     'oklch','hsl','rgb','rgba','cmyk','pantone',
                     'box-shadow','text-shadow',
                     'skeleton','loader','loading',
                     'ribbon','badge','tag',
                     'popover','tooltip','toggle',
                     'scrollbar','scroll-','scroll',
                     'cursor','caret','outline',
                     'duotone','monochrome',
                     'glassmorphism','glass',
                     'type-scale','modular-scale'],
    'image-tools': ['image','photo','picture','screenshot','thumbnail',
                    'compress','resize','crop','rotate','flip','filter',
                    'watermark','overlay','frame','border',
                    'jpg','png','gif','webp','svg','bmp','tiff','jpeg',
                    'avif','heic','ico','favicon',
                    'remove','background','extract','metadata','exif',
                    'pixel','resolution','dpi','aspect','ratio',
                    'compare-images','image-comparison',
                    'photo-collage','collage',
                    'photo-effects','photo-editor',
                    'image-to-icon','image-to-base64',
                    'batch-image','batch-watermark',
                    'screenshot-editor','screenshot-tool',
                    'social-media-image','social-media-sizes',
                    'pixelate','blur','sharpen',
                    'color-channel','channel-separator',
                    'placeholder-image',
                    'movie-barcode','barcode-generator',
                    'screen-color-picker','color-picker',
                    'meme-generator','meme-maker',
                    'qr-code','qr-generator',
                    'app-icon','app-icon-generator'],
    'text-tools': ['text','string','word','sentence','paragraph','character',
                   'letter','case','uppercase','lowercase','title','capitalize',
                   'counter','count','length','statistic','frequency',
                   'sort','reverse','shuffle','randomize',
                   'replace','find','search','extract','split','join',
                   'diff','compare','merge','deduplicate',
                   'wrap','truncate','ellipsis','abbreviate',
                   'indent','align','justify',
                   'lorem','ipsum','dummy','placeholder','sample',
                   'spell','grammar','check','proofread',
                   'readability','sentiment','analyze','analysis',
                   'translate','translator','language','bilingual',
                   'generate','generator','maker','creator','builder',
                   'name','username','nickname','password','passphrase',
                   'cipher','encode','decode','encrypt','decrypt',
                   'braille','morse','nato','leet','1337',
                   'upside-down','backwards','reverse','mirror',
                   'bold','italic','cursive','bubble','zalgo',
                   'strikethrough','underline','overline',
                   'small-text','tiny-text','big-text',
                   'vaporwave','aesthetic','glitch',
                   'markdown-to-text','html-to-text',
                   'regex-','pattern-',
                   'acronym','abbreviation','initialism',
                   'alliteration','pangram','anagram',
                   'rhyme','poem','poetry','haiku',
                   'synonym','antonym','thesaurus',
                   'syllable','vowel','consonant',
                   'palindrome','pangram',
                   'typography','font-','type-',
                   'calligraphy','handwriting',
                   'text-to','-to-text',
                   'word-counter','letter-counter',
                   'character-map','symbol','unicode',
                   'text-extractor','text-cleaner',
                   'text-formatter','text-normalizer'],
    'pdf-tools': ['pdf','document'],
    'media-tools': ['audio','video','music','sound','voice','speech',
                    'record','play','player','editor','trimmer','cutter',
                    'merge','split','join','concatenate',
                    'convert','transcode','encode','decode',
                    'compress','reduce','optimize',
                    'waveform','spectrum','visualizer','analyzer',
                    'equalizer','filter','effect','pitch','tempo','speed',
                    'volume','gain','amplify','normalize',
                    'fade','crossfade','loop','reverse',
                    'noise','silence','tone','frequency',
                    'subtitle','caption','lyric','transcript',
                    'youtube','tiktok','instagram',
                    'gif','animation','animated','motion',
                    'mp3','mp4','wav','ogg','flac','aac','wma',
                    'mp4-to-gif','video-to-gif','gif-to-video',
                    'stream','streaming','broadcast','podcast',
                    'webcam','camera','screen','record','capture',
                    'screenshot','screen-recorder',
                    'm3u8','hls','dash',
                    'thumbnail','preview',
                    'youtube-thumbnail','youtube-timestamp',
                    'channel','stereo','mono','surround',
                    'midi','midi-player','beat-maker','beat-sequencer',
                    'vocal-remover','voice-changer',
                    'lofi','ambient','binaural','white-noise','brown-noise',
                    'ringtone','notification','alert'],
    'security-tools': ['security','encrypt','decrypt','cipher','hash','password',
                       'ssl','tls','certificate','key','pem','csr',
                       'auth','oauth','saml','ldap','jwt',
                       'vulnerability','exploit','penetration','scan',
                       'firewall','proxy','vpn','tor','anonymous',
                       'malware','virus','spyware','ransomware',
                       'phishing','spam','fraud','scam',
                       'privacy','anonymous','incognito','tracking',
                       '2fa','mfa','otp','totp','hotp',
                       'bcrypt','scrypt','argon','pbkdf','sha','md5',
                       'entropy','strength','checker','tester',
                       'whois','dns','domain','spf','dkim','dmarc',
                       'ctf','captcha','pow-captcha',
                       'ssh','ssh-key','rsa-key',
                       'mac-address','browser-fingerprint',
                       'certificate-decoder','ssl-checker',
                       'cookie','session','localstorage'],
    'seo-tools': ['seo','meta','keyword','rank','traffic','backlink',
                  'sitemap','robots','schema','structured','rich',
                  'serp','google','bing','search',
                  'optimize','optimization','audit','analysis',
                  'title','description','heading','alt','anchor',
                  'page-speed','core-web','lighthouse',
                  'canonical','hreflang','redirect','broken-link',
                  'og-','open-graph','twitter-card','social',
                  'index','crawl','bot','spider',
                  'meta-tag','meta-description','meta-tags',
                  'serp-preview','social-preview',
                  'keyword-density','keyword-extractor',
                  'site-availability','uptime-checker','website-status',
                  'link-preview','og-preview',
                  'sitemap-checker','sitemap-validator',
                  'robots-txt','robots-txt-tester'],
    'network-tools': ['network','ip','dns','domain','ping','traceroute',
                      'port','socket','proxy','firewall','router',
                      'bandwidth','speed','latency','throughput',
                      'packet','protocol','tcp','udp','http','https',
                      'ftp','sftp','ssh','telnet','rdp','vnc',
                      'subnet','cidr','mask','gateway','dhcp',
                      'whois','lookup','resolve','dig','nslookup',
                      'monitor','analyze','sniff','capture',
                      'status','check','test','scan',
                      'online','offline','uptime','downtime',
                      'connect','disconnect','timeout','retry',
                      'latency-test','speed-test',
                      'port-scanner','port-checker',
                      'redirect-checker','redirect-tracer',
                      'url-unshortener','url-shortener',
                      'dns-records','dns-lookup',
                      'dns-propagation','dns-propagation-checker',
                      'server-status','server-checker',
                      'site-availability','website-uptime',
                      'what-is-my-ip','whats-my-ip',
                      'user-agent','user-agent-parser',
                      'mime-type','mime-type-checker'],
    'productivity-tools': ['productivity','efficiency','workflow','automation',
                           'todo','task','checklist','planner','organizer',
                           'note','memo','journal','diary','log',
                           'timer','stopwatch','countdown','pomodoro',
                           'calendar','schedule','reminder','alarm',
                           'focus','concentrate','distraction','block',
                           'habit','routine','goal','tracker',
                           'project','manage','kanban','scrum','agile',
                           'collaborate','team','share','sync',
                           'clipboard','copy','paste','snippet',
                           'bookmark','favorite','save','pin',
                           'shortcut','hotkey','macro','script',
                           'notepad','notes-app',
                           'meeting','agenda','minutes',
                           'time-tracker','billable-hours',
                           'study-planner','study-timer',
                           'reading-time','reading-speed',
                           'pomodoro-timer','pomodoro-tracker',
                           'focus-timer','focus-session',
                           'weekly-planner','daily-planner',
                           'packing-checklist','shopping-list',
                           'kanban-board','priority-matrix',
                           'decision-matrix','decision-tree',
                           'smart-goal','smart-goal-generator',
                           'okr-generator','action-plan',
                           'bullet-journal','habit-tracker'],
    'creative-tools': ['creative','meme','gif','animation','emoji','sticker',
                       'avatar','profile','character','persona',
                       'story','plot','script','screenplay',
                       'poem','poetry','rhyme','haiku','limerick',
                       'lyric','song','rap','verse',
                       'quote','saying','proverb','aphorism',
                       'joke','pun','riddle','puzzle',
                       'game','quiz','trivia','crossword','sudoku',
                       'fortune','horoscope','tarot','astrology',
                       'magic','spell','witch','wizard',
                       'fantasy','scifi','fiction','novel',
                       'art','draw','sketch','doodle','paint',
                       'craft','diy','handmade','homemade',
                       'meme-generator','meme-maker',
                       'comic','cartoon','illustration',
                       'collage','mood-board','vision-board',
                       'calligraphy','lettering',
                       'pixel-art','pixel-art-creator',
                       'dot-art','ascii-art',
                       'inspiration','idea','brainstorm',
                       'mind-map','mindmap','concept-map',
                       'word-cloud','tag-cloud',
                       'bingo','bingo-card','bingo-cards',
                       'lottery','raffle','lucky',
                       'spin-the-wheel','spin-wheel','wheel-of-names',
                       'yes-no','this-or-that','would-you-rather',
                       'truth-or-dare','never-have-i-ever','most-likely-to',
                       'would-you-rather','what-to-eat',
                       'dream-journal','dream-interpretation',
                       'daily-affirmation','compliment-generator',
                       'acrostic','concrete-poem',
                       'story-generator','story-idea',
                       'writing-prompt','plot-generator'],
    'fun-tools': ['fun','game','play','entertainment','amusement',
                  'joke','meme','gif','emoji','sticker',
                  'quiz','trivia','puzzle','riddle','brain',
                  'fortune','cookie','magic','8-ball',
                  'spin','wheel','random','lottery','raffle',
                  'would-you','never-have','truth-or','this-or',
                  'yes-no','decision','choice','picker',
                  'love','match','compatibility','couple',
                  'prank','troll','mischief','naughty',
                  'cool','awesome','epic','legendary',
                  'weird','strange','odd','bizarre',
                  'nostalgia','retro','vintage','classic',
                  'boredom','kill-time','pass-time','procrastinate',
                  'dice-roller','dice-roll','coin-flip','coin-flipper',
                  'magic-8-ball','yes-no-oracle','yes-no-maybe',
                  'random-fact','random-joke','random-quote',
                  'toss','flip','heads-or-tails',
                  'rock-paper-scissors','tic-tac-toe',
                  'minesweeper','snake-game','2048-game',
                  'memory-game','memory-card-game',
                  'wordle','wordle-solver','word-scramble',
                  'crossword','crossword-solver',
                  'sudoku','sudoku-solver',
                  'tarot','tarot-reading',
                  'chinese-zodiac','zodiac-sign','horoscope',
                  'love-calculator','personality-test',
                  'your-age','how-old','how-old-am-i',
                  'name-meaning','meaning-finder',
                  'baby-name','pet-name','nickname-generator',
                  'what-to-eat','food-picker',
                  'kaomoji','lenny','shrug',
                  'typing-test','typing-speed','typing-race',
                  'click-speed','click-test','reaction-test'],
    'life-tools': ['life','lifestyle','daily','everyday','routine',
                   'home','house','garden','kitchen','cooking',
                   'recipe','food','meal','diet','nutrition',
                   'coffee','tea','drink','beverage','cocktail',
                   'pet','dog','cat','fish','bird',
                   'baby','child','kid','parent','family',
                   'relationship','dating','marriage','wedding',
                   'travel','trip','vacation','holiday','tour',
                   'car','vehicle','drive','commute','transport',
                   'shopping','buy','price','cost','deal',
                   'gift','present','wish','registry',
                   'party','event','celebration','festival',
                   'hobby','interest','passion','collection',
                   'weather','climate','season','temperature',
                   'plant','flower','tree','nature','outdoor',
                   'cooking-converter','kitchen-',
                   'recipe-converter','recipe-scaler','recipe-analyzer',
                   'ingredient','ingredient-substitute',
                   'coffee-brew','coffee-ratio',
                   'cat-age','dog-age','pet-age',
                   'baby-tracker','baby-cost',
                   'tip-calculator','split-bill','bill-splitter',
                   'luggage','luggage-weight',
                   'travel-budget','vacation-budget',
                   'packing','packing-checklist',
                   'time-zone','timezone-converter','world-clock',
                   'currency-converter','currency-exchange',
                   'moon-phase','moon-phase-calendar',
                   'biorhythm','bio-rhythm',
                   'cat-calorie','dog-calorie',
                   'ring-size','shoe-size','bra-size',
                   'gift-suggestion','gift-finder'],
    'education-tools': ['education','learn','study','teach','train',
                        'course','class','lesson','tutorial','workshop',
                        'school','college','university','academic',
                        'student','teacher','professor','instructor',
                        'exam','test','quiz','assessment','grade',
                        'homework','assignment','project','essay',
                        'research','paper','thesis','dissertation',
                        'reference','citation','bibliography','source',
                        'flashcard','memorize','remember','recall',
                        'read','reading','speed','comprehension',
                        'write','writing','essay','composition',
                        'grammar','spell','punctuation','syntax',
                        'vocabulary','dictionary','thesaurus','glossary',
                        'language','english','spanish','french','german',
                        'translate','translator','bilingual','multilingual',
                        'pronounce','pronunciation','phonetic','accent',
                        'math','algebra','geometry','calculus','statistic',
                        'science','physics','chemistry','biology','astronomy',
                        'history','geography','philosophy','psychology',
                        'multiplication-table','times-table',
                        'periodic-table','periodic-table-of-elements',
                        'study-planner','study-timer',
                        'spaced-repetition','flashcard',
                        'reading-time','reading-speed',
                        'vocabulary-builder','vocabulary-test',
                        'pronunciation-guide','phonetic-alphabet',
                        'apa-citation','mla-citation','citation',
                        'katex-editor','latex-editor','equation-editor',
                        'math-equation','math-formula',
                        'algorithm','algorithm-visualizer',
                        'sort-visualization','data-structure',
                        'nato-alphabet','nato-phonetic',
                        'morse-code','morse-code-translator',
                        'spell-checker','grammar-checker'],
    'business-tools': ['business','company','startup','enterprise','corporate',
                       'management','leadership','strategy','planning',
                       'marketing','sales','advertising','promotion',
                       'customer','client','service','support',
                       'hr','human','resource','recruit','hire',
                       'payroll','compensation','benefit','perk',
                       'invoice','billing','payment','subscription',
                       'contract','agreement','proposal','estimate',
                       'meeting','agenda','minutes','presentation',
                       'report','dashboard','kpi','metric','analytics',
                       'brand','logo','identity','reputation',
                       'pitch','deck','investor','funding','venture',
                       'legal','compliance','regulation','policy',
                       'risk','assessment','mitigation','contingency',
                       'swot','pestle','porter','five-forces',
                       'canvas','model','framework','methodology',
                       'nda','non-disclosure','confidentiality',
                       'business-card','business-card-generator',
                       'resume','cv','cover-letter',
                       'invoice-generator','receipt-generator',
                       'proposal','proposal-template',
                       'contract','agreement','terms-of-service',
                       'disclaimer','privacy-policy','return-policy',
                       'press-release','press-release-template',
                       'competitive-analysis','competitor-analysis',
                       'stakeholder-map','stakeholder-analysis',
                       'org-chart','org-chart-maker',
                       'business-model','business-model-canvas',
                       'lean-canvas','value-proposition',
                       'pitch-deck','pitch-deck-outline'],
    'office-tools': ['office','document','spreadsheet','presentation',
                     'word','excel','powerpoint','google-doc',
                     'template','form','letter','resume','cv',
                     'certificate','diploma','award','badge',
                     'label','tag','sticker','stamp',
                     'envelope','letterhead','stationery',
                     'fax','scan','copy','print',
                     'signature','sign','endorse','approve',
                     'convert','export','import','compatible',
                     'format','doc','docx','xls','xlsx','ppt','pptx',
                     'ocr','recognize','extract','digitize',
                     'resume-builder','resume-parser',
                     'cover-letter','cover-letter-generator',
                     'certificate-generator','certificate-maker',
                     'invoice','invoice-generator',
                     'receipt','receipt-generator','receipt-maker',
                     'letter','letter-template','letter-generator',
                     'letterhead','letterhead-generator',
                     'vcard','vcard-generator','vcf-generator',
                     'business-card','business-card-generator',
                     'envelope','envelope-address',
                     'signature-generator','signature-maker',
                     'stamp-maker','stamp-generator'],
    'converter-tools': ['converter','convert','transform','change'],
    'audio-tools': ['audio','sound','music','voice','speech',
                    'mp3','wav','ogg','flac','aac','wma',
                    'record','play','player','editor',
                    'trim','cut','split','merge','join',
                    'convert','transcode','encode','decode',
                    'compress','reduce','optimize',
                    'equalizer','filter','effect','reverb','echo',
                    'pitch','tempo','speed','slow','fast',
                    'volume','gain','amplify','normalize',
                    'fade','crossfade','loop','reverse',
                    'waveform','spectrum','visualizer',
                    'noise','silence','tone','frequency',
                    'beat','rhythm','metronome','bpm',
                    'instrument','piano','guitar','drum',
                    'synthesizer','sampler','sequencer',
                    'podcast','audiobook','narration'],
    'math-tools': ['math','mathematics','algebra','geometry','calculus',
                   'statistic','probability','trigonometry','logarithm',
                   'equation','formula','function','graph','plot',
                   'matrix','vector','tensor','polynomial',
                   'prime','factor','divisor','multiple','gcd','lcm',
                   'fraction','decimal','percent','ratio','proportion',
                   'rounding','round-','ceil','floor','truncate',
                   'scientific','notation','significant','figure',
                   'sequence','series','sum','product',
                   'root','square','cube','power','exponent',
                   'angle','triangle','circle','rectangle','polygon',
                   'area','volume','perimeter','circumference',
                   'coordinate','cartesian','polar','cylindrical',
                   'set','subset','union','intersection','complement',
                   'boolean','logic','gate','truth-table',
                   'binary','octal','hex','numeral','base'],
}

def clean_title(raw):
    """清理标题：去掉免费前缀、英文部分、后缀"""
    t = raw.strip()
    # Remove common suffix patterns
    for pat in ['无需注册', 'No Signup', 'No Registration', '纯前端', 'Client-side',
                'Free ToolBase', 'free-toolbase', 'free-tool-base']:
        t = re.sub(rf'\s*[-–—|]\s*{pat}.*$', '', t, flags=re.I).strip()
    # Split by separators, find best Chinese part
    parts = re.split(r'\s*[-–—|]\s*', t)
    best = parts[0]
    for p in parts:
        if any('\u4e00' <= c <= '\u9fff' for c in p):
            best = p
            break
    t = best.strip()
    # Remove leading redundant words
    t = re.sub(r'^免费在线', '', t).strip()
    t = re.sub(r'^免费', '', t).strip()
    t = re.sub(r'^在线', '', t).strip()
    # Truncate
    if len(t) > 30:
        t = t[:28] + '..'
    return t

def clean_desc(desc):
    """清理描述"""
    desc = desc.strip()
    # 缩短到55字符以内
    if len(desc) > 55:
        # 找句号截断
        idx = desc[:55].rfind('。')
        if idx > 20:
            desc = desc[:idx+1]
        else:
            desc = desc[:52] + '...'
    # 移除"免费在线"前缀
    desc = re.sub(r'^免费在线', '', desc)
    desc = re.sub(r'^免费', '', desc)
    return desc.strip()

def get_category(tool_name):
    name_lower = tool_name.lower()
    scores = {}
    for cat, keywords in CAT_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in name_lower:
                score += len(kw)
        if score > 0:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return 'utility-tools'

def get_icon(tool_name):
    name_lower = tool_name.lower()
    matches = []
    for kw, icon in ICON_MAP.items():
        if kw in name_lower:
            matches.append((len(kw), icon))
    if matches:
        matches.sort(reverse=True)
        return matches[0][1]
    return '🔧'

def extract_tool_info(tool_dir):
    """从工具页面提取中文标题和描述"""
    fpath = os.path.join(BASE, tool_dir, 'index.html')
    if not os.path.exists(fpath):
        return None
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 跳过迁移/重定向页面
    first500 = content[:500]
    if any(x in first500 for x in ['已迁移', '已合并', '已跳转']):
        return None
    if 'window.location' in first500 and 'href' in first500:
        return None

    # 提取title
    title_m = re.search(r'<title>(.+?)</title>', content, re.I)
    if not title_m:
        return None
    raw_title = title_m.group(1).strip()

    # 检查是否有中文
    if not any('\u4e00' <= c <= '\u9fff' for c in raw_title):
        return None

    title = clean_title(raw_title)
    if not title or len(title) < 3:
        return None

    # 提取description
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.I)
    desc = ''
    if desc_m:
        desc = clean_desc(desc_m.group(1).strip())

    if not desc:
        desc = '免费在线工具，纯浏览器端运行。'

    return {'title': title, 'desc': desc, 'dir': tool_dir}

def main():
    all_tools = set()
    for d in os.listdir(BASE):
        if os.path.isdir(os.path.join(BASE, d)) and not d.startswith('.') and d not in SKIP_DIRS:
            if os.path.exists(os.path.join(BASE, d, 'index.html')):
                all_tools.add(d)

    with open(os.path.join(BASE, 'index.html'), 'r', encoding='utf-8', errors='ignore') as f:
        cn_html = f.read()
    cn_hrefs = set(re.findall(r'href="/([^"]+)/"', cn_html))
    cn_existing = cn_hrefs & all_tools
    cn_missing = all_tools - cn_existing

    cards = []
    skipped = 0
    for tool in sorted(cn_missing):
        info = extract_tool_info(tool)
        if not info:
            skipped += 1
            continue

        cat = get_category(tool)
        icon = get_icon(tool)
        title = info['title']
        desc = info['desc']

        card = f'<div class="tool-card" data-cat="{cat}" data-category="{cat}"><span class="tool-icon">{icon}</span><span class="tool-name">{title}</span><span class="tool-desc">{desc}</span><a href="/{tool}/" class="btn">立即使用</a></div>'
        cards.append(card)

    print(f"=== STATS ===")
    print(f"Total tools: {len(all_tools)}")
    print(f"CN existing: {len(cn_existing)}")
    print(f"CN missing: {len(cn_missing)}")
    print(f"Generated: {len(cards)}")
    print(f"Skipped: {skipped}")

    # Output cards
    for c in cards:
        print(c)

if __name__ == '__main__':
    main()
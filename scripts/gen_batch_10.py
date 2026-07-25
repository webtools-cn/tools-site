#!/usr/bin/env python3
"""批量生成10个新工具（中英文）"""
import os

BASE = "/home/chison/tools-site"

tools = [
    {
        "slug": "dns-records",
        "cn_name": "DNS记录查询",
        "en_name": "DNS Records Lookup",
        "cn_desc": "在线DNS记录查询工具，支持A/AAAA/CNAME/MX/NS/TXT/SOA等多种记录类型，快速获取域名解析信息。",
        "en_desc": "Free online DNS records lookup tool. Query A, AAAA, CNAME, MX, NS, TXT, SOA records and more for any domain.",
        "cn_keywords": "DNS查询,DNS记录,域名解析,A记录,MX记录,CNAME,NS记录,TXT记录,在线DNS工具",
        "en_keywords": "DNS lookup,DNS records,domain lookup,A record,MX record,CNAME,NS lookup,online DNS tool",
        "category": "网络工具",
        "en_category": "Network Tools",
        "html_cn": """<div class="input-group">
    <label for="domain-input">输入域名</label>
    <input type="text" id="domain-input" placeholder="例如: example.com" autocomplete="off">
</div>
<div class="btn-row">
    <button id="lookup-btn" class="btn-primary">查询DNS记录</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">查询结果</div>
    <div id="dns-result"></div>
</div>
<div id="loading" style="display:none;text-align:center;padding:20px;">⏳ 查询中...</div>""",
        "html_en": """<div class="input-group">
    <label for="domain-input">Enter Domain</label>
    <input type="text" id="domain-input" placeholder="e.g. example.com" autocomplete="off">
</div>
<div class="btn-row">
    <button id="lookup-btn" class="btn-primary">Lookup DNS</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Results</div>
    <div id="dns-result"></div>
</div>
<div id="loading" style="display:none;text-align:center;padding:20px;">⏳ Looking up...</div>""",
        "js_cn": """document.getElementById('lookup-btn').addEventListener('click', async () => {
    const domain = document.getElementById('domain-input').value.trim();
    if (!domain) { showToast('请输入域名'); return; }
    const result = document.getElementById('result-area');
    const loading = document.getElementById('loading');
    result.style.display = 'none';
    loading.style.display = 'block';
    try {
        const types = ['A','AAAA','CNAME','MX','NS','TXT','SOA'];
        const resp = await fetch('https://dns.google/resolve?name=' + encodeURIComponent(domain) + '&type=ANY');
        if (!resp.ok) throw new Error('DNS查询失败');
        const data = await resp.json();
        let html = '';
        if (data.Answer) {
            for (const r of data.Answer) {
                html += `<div class="dns-record"><strong>${r.type}</strong>: ${r.data}</div>`;
            }
        } else {
            html = '<p>未找到DNS记录。请检查域名是否正确。</p>';
        }
        document.getElementById('dns-result').innerHTML = html;
        result.style.display = 'block';
    } catch(e) {
        document.getElementById('dns-result').innerHTML = `<p style="color:red;">查询出错: ${e.message}</p>`;
        result.style.display = 'block';
    }
    loading.style.display = 'none';
});""",
        "js_en": """document.getElementById('lookup-btn').addEventListener('click', async () => {
    const domain = document.getElementById('domain-input').value.trim();
    if (!domain) { showToast('Please enter a domain'); return; }
    const result = document.getElementById('result-area');
    const loading = document.getElementById('loading');
    result.style.display = 'none';
    loading.style.display = 'block';
    try {
        const resp = await fetch('https://dns.google/resolve?name=' + encodeURIComponent(domain) + '&type=ANY');
        if (!resp.ok) throw new Error('DNS lookup failed');
        const data = await resp.json();
        let html = '';
        if (data.Answer) {
            for (const r of data.Answer) {
                html += `<div class="dns-record"><strong>${r.type}</strong>: ${r.data}</div>`;
            }
        } else {
            html = '<p>No DNS records found. Please check the domain name.</p>';
        }
        document.getElementById('dns-result').innerHTML = html;
        result.style.display = 'block';
    } catch(e) {
        document.getElementById('dns-result').innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
        result.style.display = 'block';
    }
    loading.style.display = 'none';
});""",
    },
    {
        "slug": "email-verifier",
        "cn_name": "邮箱验证器",
        "en_name": "Email Verifier",
        "cn_desc": "在线邮箱格式验证工具，检查邮箱地址是否有效，支持格式校验、域名MX记录检测和常见临时邮箱识别。",
        "en_desc": "Free online email verification tool. Validate email format, check MX records, and detect disposable email addresses.",
        "cn_keywords": "邮箱验证,邮箱格式检查,email验证,邮箱校验,检测邮箱有效性,在线邮箱验证工具",
        "en_keywords": "email verification,email validator,check email,validate email,email format checker,online email tool",
        "category": "文本工具",
        "en_category": "Text Tools",
        "html_cn": """<div class="input-group">
    <label for="email-input">输入邮箱地址</label>
    <input type="email" id="email-input" placeholder="例如: user@example.com" autocomplete="off">
</div>
<div class="btn-row">
    <button id="verify-btn" class="btn-primary">验证邮箱</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">验证结果</div>
    <div id="verify-result"></div>
</div>""",
        "html_en": """<div class="input-group">
    <label for="email-input">Enter Email Address</label>
    <input type="email" id="email-input" placeholder="e.g. user@example.com" autocomplete="off">
</div>
<div class="btn-row">
    <button id="verify-btn" class="btn-primary">Verify Email</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Result</div>
    <div id="verify-result"></div>
</div>""",
        "js_cn": """document.getElementById('verify-btn').addEventListener('click', () => {
    const email = document.getElementById('email-input').value.trim();
    const result = document.getElementById('result-area');
    const div = document.getElementById('verify-result');
    if (!email) { showToast('请输入邮箱地址'); return; }
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    const formatOk = re.test(email);
    const parts = email.split('@');
    const domain = parts[1] || '';
    const disposable = ['mailinator.com','tempmail.com','10minutemail.com','guerrillamail.com','yopmail.com','throwaway.email','temp-mail.org','sharklasers.com','trashmail.com','maildrop.cc'];
    const isDisposable = disposable.includes(domain.toLowerCase());
    let html = '<table class="verify-table">';
    html += `<tr><td>邮箱地址</td><td>${email}</td></tr>`;
    html += `<tr><td>格式检查</td><td class="${formatOk ? 'pass' : 'fail'}">${formatOk ? '✅ 格式正确' : '❌ 格式不正确'}</td></tr>`;
    html += `<tr><td>域名</td><td>${domain}</td></tr>`;
    if (isDisposable) {
        html += `<tr><td>临时邮箱检测</td><td class="warn">⚠️ 可能是临时邮箱</td></tr>`;
    } else {
        html += `<tr><td>临时邮箱检测</td><td class="pass">✅ 非已知临时邮箱</td></tr>`;
    }
    html += '</table>';
    div.innerHTML = html;
    result.style.display = 'block';
});""",
        "js_en": """document.getElementById('verify-btn').addEventListener('click', () => {
    const email = document.getElementById('email-input').value.trim();
    const result = document.getElementById('result-area');
    const div = document.getElementById('verify-result');
    if (!email) { showToast('Please enter an email address'); return; }
    const re = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
    const formatOk = re.test(email);
    const parts = email.split('@');
    const domain = parts[1] || '';
    const disposable = ['mailinator.com','tempmail.com','10minutemail.com','guerrillamail.com','yopmail.com','throwaway.email','temp-mail.org','sharklasers.com','trashmail.com','maildrop.cc'];
    const isDisposable = disposable.includes(domain.toLowerCase());
    let html = '<table class="verify-table">';
    html += `<tr><td>Email</td><td>${email}</td></tr>`;
    html += `<tr><td>Format</td><td class="${formatOk ? 'pass' : 'fail'}">${formatOk ? '✅ Valid format' : '❌ Invalid format'}</td></tr>`;
    html += `<tr><td>Domain</td><td>${domain}</td></tr>`;
    if (isDisposable) {
        html += `<tr><td>Disposable</td><td class="warn">⚠️ Possible disposable email</td></tr>`;
    } else {
        html += `<tr><td>Disposable</td><td class="pass">✅ Not a known disposable email</td></tr>`;
    }
    html += '</table>';
    div.innerHTML = html;
    result.style.display = 'block';
});""",
    },
    {
        "slug": "screen-resolution-checker",
        "cn_name": "屏幕分辨率检测",
        "en_name": "Screen Resolution Checker",
        "cn_desc": "在线检测您的屏幕分辨率、视口尺寸、像素比、色彩深度等显示器参数，无需安装任何软件。",
        "en_desc": "Check your screen resolution, viewport size, device pixel ratio, color depth and more. No installation needed.",
        "cn_keywords": "屏幕分辨率,分辨率检测,屏幕尺寸,显示器参数,像素比,在线检测,屏幕信息",
        "en_keywords": "screen resolution,resolution checker,screen size,display info,pixel ratio,online screen check",
        "category": "开发工具",
        "en_category": "Dev Tools",
        "html_cn": """<div class="btn-row">
    <button id="check-btn" class="btn-primary">检测屏幕信息</button>
    <button id="refresh-btn" class="btn-secondary" style="display:none;">刷新检测</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">屏幕信息</div>
    <div id="screen-result"></div>
</div>""",
        "html_en": """<div class="btn-row">
    <button id="check-btn" class="btn-primary">Check Screen Info</button>
    <button id="refresh-btn" class="btn-secondary" style="display:none;">Refresh</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Screen Information</div>
    <div id="screen-result"></div>
</div>""",
        "js_cn": """function showScreenInfo() {
    const w = window.screen.width;
    const h = window.screen.height;
    const aw = window.screen.availWidth;
    const ah = window.screen.availHeight;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const dpr = window.devicePixelRatio || 1;
    const cd = window.screen.colorDepth;
    const pd = window.screen.pixelDepth;
    const o = window.screen.orientation || {};
    const html = `<table class="verify-table">
<tr><td>屏幕分辨率</td><td>${w} × ${h}</td></tr>
<tr><td>可用分辨率</td><td>${aw} × ${ah}</td></tr>
<tr><td>视口尺寸</td><td>${vw} × ${vh}</td></tr>
<tr><td>设备像素比 (DPR)</td><td>${dpr}</td></tr>
<tr><td>色彩深度</td><td>${cd} bit</td></tr>
<tr><td>像素深度</td><td>${pd} bit</td></tr>
<tr><td>屏幕方向</td><td>${o.type || '未知'}</td></tr>
<tr><td>物理尺寸</td><td>${(w/dpr).toFixed(0)} × ${(h/dpr).toFixed(0)} CSS像素</td></tr>
</table>`;
    document.getElementById('screen-result').innerHTML = html;
    document.getElementById('result-area').style.display = 'block';
    document.getElementById('refresh-btn').style.display = 'inline-block';
}
document.getElementById('check-btn').addEventListener('click', showScreenInfo);
document.getElementById('refresh-btn').addEventListener('click', showScreenInfo);
window.addEventListener('resize', () => {
    if (document.getElementById('result-area').style.display !== 'none') {
        showScreenInfo();
    }
});""",
        "js_en": """function showScreenInfo() {
    const w = window.screen.width;
    const h = window.screen.height;
    const aw = window.screen.availWidth;
    const ah = window.screen.availHeight;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const dpr = window.devicePixelRatio || 1;
    const cd = window.screen.colorDepth;
    const pd = window.screen.pixelDepth;
    const o = window.screen.orientation || {};
    const html = `<table class="verify-table">
<tr><td>Screen Resolution</td><td>${w} × ${h}</td></tr>
<tr><td>Available Resolution</td><td>${aw} × ${ah}</td></tr>
<tr><td>Viewport Size</td><td>${vw} × ${vh}</td></tr>
<tr><td>Device Pixel Ratio (DPR)</td><td>${dpr}</td></tr>
<tr><td>Color Depth</td><td>${cd} bit</td></tr>
<tr><td>Pixel Depth</td><td>${pd} bit</td></tr>
<tr><td>Orientation</td><td>${o.type || 'Unknown'}</td></tr>
<tr><td>Physical Size</td><td>${(w/dpr).toFixed(0)} × ${(h/dpr).toFixed(0)} CSS px</td></tr>
</table>`;
    document.getElementById('screen-result').innerHTML = html;
    document.getElementById('result-area').style.display = 'block';
    document.getElementById('refresh-btn').style.display = 'inline-block';
}
document.getElementById('check-btn').addEventListener('click', showScreenInfo);
document.getElementById('refresh-btn').addEventListener('click', showScreenInfo);
window.addEventListener('resize', () => {
    if (document.getElementById('result-area').style.display !== 'none') {
        showScreenInfo();
    }
});""",
    },
    {
        "slug": "viewport-checker",
        "cn_name": "视口检测器",
        "en_name": "Viewport Checker",
        "cn_desc": "实时检测浏览器视口尺寸，支持拖拽调整窗口查看不同断点下的视口大小，前端开发必备工具。",
        "en_desc": "Real-time viewport size checker. Resize your browser to see viewport dimensions at different breakpoints. Essential for frontend developers.",
        "cn_keywords": "视口检测,viewport,视口尺寸,浏览器窗口,响应式断点,前端开发,在线视口工具",
        "en_keywords": "viewport checker,viewport size,browser window,responsive breakpoints,frontend dev,viewport tool",
        "category": "开发工具",
        "en_category": "Dev Tools",
        "html_cn": """<div class="viewport-display" id="vp-display">
    <div class="vp-size"><span id="vp-width">0</span> × <span id="vp-height">0</span></div>
    <div class="vp-label">视口尺寸 (实时)</div>
</div>
<div class="input-group">
    <label for="width-input">预设宽度</label>
    <input type="number" id="width-input" value="375" min="200" max="3840">
    <span class="unit">px</span>
</div>
<div class="btn-row">
    <button class="preset-btn" data-w="375">375 (手机)</button>
    <button class="preset-btn" data-w="768">768 (平板)</button>
    <button class="preset-btn" data-w="1024">1024 (桌面)</button>
    <button class="preset-btn" data-w="1440">1440 (宽屏)</button>
    <button class="preset-btn" data-w="1920">1920 (全高清)</button>
</div>
<div class="breakpoint-info" id="bp-info"></div>""",
        "html_en": """<div class="viewport-display" id="vp-display">
    <div class="vp-size"><span id="vp-width">0</span> × <span id="vp-height">0</span></div>
    <div class="vp-label">Viewport Size (Live)</div>
</div>
<div class="input-group">
    <label for="width-input">Preset Width</label>
    <input type="number" id="width-input" value="375" min="200" max="3840">
    <span class="unit">px</span>
</div>
<div class="btn-row">
    <button class="preset-btn" data-w="375">375 (Mobile)</button>
    <button class="preset-btn" data-w="768">768 (Tablet)</button>
    <button class="preset-btn" data-w="1024">1024 (Desktop)</button>
    <button class="preset-btn" data-w="1440">1440 (Wide)</button>
    <button class="preset-btn" data-w="1920">1920 (Full HD)</button>
</div>
<div class="breakpoint-info" id="bp-info"></div>""",
        "js_cn": """function updateVP() {
    document.getElementById('vp-width').textContent = window.innerWidth;
    document.getElementById('vp-height').textContent = window.innerHeight;
    const w = window.innerWidth;
    let bp = '';
    if (w < 480) bp = '📱 移动端 (< 480px)';
    else if (w < 768) bp = '📱 大屏手机 (480-767px)';
    else if (w < 1024) bp = '📋 平板 (768-1023px)';
    else if (w < 1440) bp = '💻 桌面端 (1024-1439px)';
    else bp = '🖥️ 大屏 (≥ 1440px)';
    document.getElementById('bp-info').innerHTML = `<strong>当前断点:</strong> ${bp}`;
}
updateVP();
window.addEventListener('resize', updateVP);
document.querySelectorAll('.preset-btn').forEach(b => {
    b.addEventListener('click', () => {
        const w = parseInt(b.dataset.w);
        document.getElementById('width-input').value = w;
        window.resizeTo(w, window.innerHeight);
    });
});
document.getElementById('width-input').addEventListener('change', function() {
    window.resizeTo(parseInt(this.value) || 375, window.innerHeight);
});""",
        "js_en": """function updateVP() {
    document.getElementById('vp-width').textContent = window.innerWidth;
    document.getElementById('vp-height').textContent = window.innerHeight;
    const w = window.innerWidth;
    let bp = '';
    if (w < 480) bp = '📱 Mobile (< 480px)';
    else if (w < 768) bp = '📱 Large Phone (480-767px)';
    else if (w < 1024) bp = '📋 Tablet (768-1023px)';
    else if (w < 1440) bp = '💻 Desktop (1024-1439px)';
    else bp = '🖥️ Large Screen (≥ 1440px)';
    document.getElementById('bp-info').innerHTML = `<strong>Current Breakpoint:</strong> ${bp}`;
}
updateVP();
window.addEventListener('resize', updateVP);
document.querySelectorAll('.preset-btn').forEach(b => {
    b.addEventListener('click', () => {
        const w = parseInt(b.dataset.w);
        document.getElementById('width-input').value = w;
        window.resizeTo(w, window.innerHeight);
    });
});
document.getElementById('width-input').addEventListener('change', function() {
    window.resizeTo(parseInt(this.value) || 375, window.innerHeight);
});""",
    },
    {
        "slug": "cookie-analyzer",
        "cn_name": "Cookie分析器",
        "en_name": "Cookie Analyzer",
        "cn_desc": "查看和管理当前网站的Cookie，支持查看名称、值、域名、路径、过期时间等详细信息，保护您的隐私。",
        "en_desc": "View and manage cookies for the current website. See name, value, domain, path, expiration details and protect your privacy.",
        "cn_keywords": "Cookie分析,Cookie查看,Cookie管理,浏览器Cookie,隐私检查,在线Cookie工具",
        "en_keywords": "cookie analyzer,cookie viewer,cookie manager,browser cookies,privacy check,online cookie tool",
        "category": "开发工具",
        "en_category": "Dev Tools",
        "html_cn": """<div class="btn-row">
    <button id="analyze-btn" class="btn-primary">分析Cookie</button>
    <button id="clear-all-btn" class="btn-danger" style="display:none;">清除所有Cookie</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Cookie列表</div>
    <div id="cookie-result"></div>
</div>""",
        "html_en": """<div class="btn-row">
    <button id="analyze-btn" class="btn-primary">Analyze Cookies</button>
    <button id="clear-all-btn" class="btn-danger" style="display:none;">Clear All Cookies</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Cookie List</div>
    <div id="cookie-result"></div>
</div>""",
        "js_cn": """function showCookies() {
    const cookies = document.cookie.split(';').filter(c => c.trim());
    const result = document.getElementById('result-area');
    const div = document.getElementById('cookie-result');
    if (cookies.length === 0) {
        div.innerHTML = '<p>当前网站没有设置Cookie。</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>名称</th><th>值</th><th>操作</th></tr>';
        cookies.forEach((c, i) => {
            const parts = c.trim().split('=');
            const name = parts[0];
            const value = parts.slice(1).join('=');
            html += `<tr><td>${name}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${value.substring(0,50)}${value.length>50?'...':''}</td><td><button class="del-cookie-btn" data-name="${name}">删除</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('clear-all-btn').style.display = 'inline-block';
    document.querySelectorAll('.del-cookie-btn').forEach(b => {
        b.addEventListener('click', () => {
            const name = b.dataset.name;
            document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            showToast('Cookie已删除: ' + name);
            showCookies();
        });
    });
}
document.getElementById('analyze-btn').addEventListener('click', showCookies);
document.getElementById('clear-all-btn').addEventListener('click', () => {
    document.cookie.split(';').forEach(c => {
        const name = c.trim().split('=')[0];
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    });
    showToast('所有Cookie已清除');
    showCookies();
});""",
        "js_en": """function showCookies() {
    const cookies = document.cookie.split(';').filter(c => c.trim());
    const result = document.getElementById('result-area');
    const div = document.getElementById('cookie-result');
    if (cookies.length === 0) {
        div.innerHTML = '<p>No cookies set for this site.</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>Name</th><th>Value</th><th>Action</th></tr>';
        cookies.forEach((c, i) => {
            const parts = c.trim().split('=');
            const name = parts[0];
            const value = parts.slice(1).join('=');
            html += `<tr><td>${name}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${value.substring(0,50)}${value.length>50?'...':''}</td><td><button class="del-cookie-btn" data-name="${name}">Delete</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('clear-all-btn').style.display = 'inline-block';
    document.querySelectorAll('.del-cookie-btn').forEach(b => {
        b.addEventListener('click', () => {
            const name = b.dataset.name;
            document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
            showToast('Cookie deleted: ' + name);
            showCookies();
        });
    });
}
document.getElementById('analyze-btn').addEventListener('click', showCookies);
document.getElementById('clear-all-btn').addEventListener('click', () => {
    document.cookie.split(';').forEach(c => {
        const name = c.trim().split('=')[0];
        document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    });
    showToast('All cookies cleared');
    showCookies();
});""",
    },
    {
        "slug": "localstorage-viewer",
        "cn_name": "LocalStorage浏览器",
        "en_name": "LocalStorage Viewer",
        "cn_desc": "在线查看和管理浏览器的LocalStorage数据，支持查看键值、修改值、删除条目和导出JSON，前端调试利器。",
        "en_desc": "View and manage browser LocalStorage data. Inspect key-value pairs, edit values, delete entries and export as JSON.",
        "cn_keywords": "LocalStorage,本地存储,浏览器存储,localStorage查看,前端调试,在线存储工具",
        "en_keywords": "localStorage,local storage,browser storage,storage viewer,frontend debug,online storage tool",
        "category": "开发工具",
        "en_category": "Dev Tools",
        "html_cn": """<div class="btn-row">
    <button id="view-btn" class="btn-primary">查看LocalStorage</button>
    <button id="export-btn" class="btn-secondary" style="display:none;">导出JSON</button>
    <button id="clear-ls-btn" class="btn-danger" style="display:none;">清空全部</button>
</div>
<div class="input-group" style="display:none;" id="add-group">
    <input type="text" id="ls-key" placeholder="键名">
    <input type="text" id="ls-value" placeholder="值">
    <button id="add-btn" class="btn-primary">添加</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">LocalStorage 数据</div>
    <div id="ls-result"></div>
</div>""",
        "html_en": """<div class="btn-row">
    <button id="view-btn" class="btn-primary">View LocalStorage</button>
    <button id="export-btn" class="btn-secondary" style="display:none;">Export JSON</button>
    <button id="clear-ls-btn" class="btn-danger" style="display:none;">Clear All</button>
</div>
<div class="input-group" style="display:none;" id="add-group">
    <input type="text" id="ls-key" placeholder="Key">
    <input type="text" id="ls-value" placeholder="Value">
    <button id="add-btn" class="btn-primary">Add</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">LocalStorage Data</div>
    <div id="ls-result"></div>
</div>""",
        "js_cn": """function showLS() {
    const result = document.getElementById('result-area');
    const div = document.getElementById('ls-result');
    const keys = Object.keys(localStorage);
    if (keys.length === 0) {
        div.innerHTML = '<p>LocalStorage为空。</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>键</th><th>值</th><th>操作</th></tr>';
        keys.forEach(k => {
            const v = localStorage.getItem(k);
            html += `<tr><td>${k}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${v.substring(0,60)}${v.length>60?'...':''}</td><td><button class="del-ls-btn" data-key="${k}">删除</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('export-btn').style.display = 'inline-block';
    document.getElementById('clear-ls-btn').style.display = 'inline-block';
    document.getElementById('add-group').style.display = 'flex';
    document.querySelectorAll('.del-ls-btn').forEach(b => {
        b.addEventListener('click', () => {
            localStorage.removeItem(b.dataset.key);
            showToast('已删除: ' + b.dataset.key);
            showLS();
        });
    });
}
document.getElementById('view-btn').addEventListener('click', showLS);
document.getElementById('clear-ls-btn').addEventListener('click', () => {
    localStorage.clear();
    showToast('LocalStorage已清空');
    showLS();
});
document.getElementById('export-btn').addEventListener('click', () => {
    const data = {};
    Object.keys(localStorage).forEach(k => { data[k] = localStorage.getItem(k); });
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'localstorage-export.json';
    a.click();
    showToast('已导出JSON文件');
});
document.getElementById('add-btn').addEventListener('click', () => {
    const key = document.getElementById('ls-key').value.trim();
    const value = document.getElementById('ls-value').value;
    if (!key) { showToast('请输入键名'); return; }
    localStorage.setItem(key, value);
    showToast('已添加');
    showLS();
});""",
        "js_en": """function showLS() {
    const result = document.getElementById('result-area');
    const div = document.getElementById('ls-result');
    const keys = Object.keys(localStorage);
    if (keys.length === 0) {
        div.innerHTML = '<p>LocalStorage is empty.</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>Key</th><th>Value</th><th>Action</th></tr>';
        keys.forEach(k => {
            const v = localStorage.getItem(k);
            html += `<tr><td>${k}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${v.substring(0,60)}${v.length>60?'...':''}</td><td><button class="del-ls-btn" data-key="${k}">Delete</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('export-btn').style.display = 'inline-block';
    document.getElementById('clear-ls-btn').style.display = 'inline-block';
    document.getElementById('add-group').style.display = 'flex';
    document.querySelectorAll('.del-ls-btn').forEach(b => {
        b.addEventListener('click', () => {
            localStorage.removeItem(b.dataset.key);
            showToast('Deleted: ' + b.dataset.key);
            showLS();
        });
    });
}
document.getElementById('view-btn').addEventListener('click', showLS);
document.getElementById('clear-ls-btn').addEventListener('click', () => {
    localStorage.clear();
    showToast('LocalStorage cleared');
    showLS();
});
document.getElementById('export-btn').addEventListener('click', () => {
    const data = {};
    Object.keys(localStorage).forEach(k => { data[k] = localStorage.getItem(k); });
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'localstorage-export.json';
    a.click();
    showToast('JSON file exported');
});
document.getElementById('add-btn').addEventListener('click', () => {
    const key = document.getElementById('ls-key').value.trim();
    const value = document.getElementById('ls-value').value;
    if (!key) { showToast('Please enter a key'); return; }
    localStorage.setItem(key, value);
    showToast('Added');
    showLS();
});""",
    },
    {
        "slug": "sessionstorage-viewer",
        "cn_name": "SessionStorage浏览器",
        "en_name": "SessionStorage Viewer",
        "cn_desc": "在线查看和管理浏览器的SessionStorage数据，支持查看键值对、修改和删除，会话关闭后自动清除。",
        "en_desc": "View and manage browser SessionStorage data. Inspect key-value pairs, edit and delete entries. Automatically cleared when session ends.",
        "cn_keywords": "SessionStorage,会话存储,浏览器存储,sessionStorage查看,前端调试,在线存储工具",
        "en_keywords": "sessionStorage,session storage,browser storage,storage viewer,frontend debug,online storage tool",
        "category": "开发工具",
        "en_category": "Dev Tools",
        "html_cn": """<div class="btn-row">
    <button id="view-btn" class="btn-primary">查看SessionStorage</button>
    <button id="export-btn" class="btn-secondary" style="display:none;">导出JSON</button>
    <button id="clear-ss-btn" class="btn-danger" style="display:none;">清空全部</button>
</div>
<div class="input-group" style="display:none;" id="add-group">
    <input type="text" id="ss-key" placeholder="键名">
    <input type="text" id="ss-value" placeholder="值">
    <button id="add-btn" class="btn-primary">添加</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">SessionStorage 数据</div>
    <div id="ss-result"></div>
</div>""",
        "html_en": """<div class="btn-row">
    <button id="view-btn" class="btn-primary">View SessionStorage</button>
    <button id="export-btn" class="btn-secondary" style="display:none;">Export JSON</button>
    <button id="clear-ss-btn" class="btn-danger" style="display:none;">Clear All</button>
</div>
<div class="input-group" style="display:none;" id="add-group">
    <input type="text" id="ss-key" placeholder="Key">
    <input type="text" id="ss-value" placeholder="Value">
    <button id="add-btn" class="btn-primary">Add</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">SessionStorage Data</div>
    <div id="ss-result"></div>
</div>""",
        "js_cn": """function showSS() {
    const result = document.getElementById('result-area');
    const div = document.getElementById('ss-result');
    const keys = Object.keys(sessionStorage);
    if (keys.length === 0) {
        div.innerHTML = '<p>SessionStorage为空。</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>键</th><th>值</th><th>操作</th></tr>';
        keys.forEach(k => {
            const v = sessionStorage.getItem(k);
            html += `<tr><td>${k}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${v.substring(0,60)}${v.length>60?'...':''}</td><td><button class="del-ss-btn" data-key="${k}">删除</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('export-btn').style.display = 'inline-block';
    document.getElementById('clear-ss-btn').style.display = 'inline-block';
    document.getElementById('add-group').style.display = 'flex';
    document.querySelectorAll('.del-ss-btn').forEach(b => {
        b.addEventListener('click', () => {
            sessionStorage.removeItem(b.dataset.key);
            showToast('已删除: ' + b.dataset.key);
            showSS();
        });
    });
}
document.getElementById('view-btn').addEventListener('click', showSS);
document.getElementById('clear-ss-btn').addEventListener('click', () => {
    sessionStorage.clear();
    showToast('SessionStorage已清空');
    showSS();
});
document.getElementById('export-btn').addEventListener('click', () => {
    const data = {};
    Object.keys(sessionStorage).forEach(k => { data[k] = sessionStorage.getItem(k); });
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'sessionstorage-export.json';
    a.click();
    showToast('已导出JSON文件');
});
document.getElementById('add-btn').addEventListener('click', () => {
    const key = document.getElementById('ss-key').value.trim();
    const value = document.getElementById('ss-value').value;
    if (!key) { showToast('请输入键名'); return; }
    sessionStorage.setItem(key, value);
    showToast('已添加');
    showSS();
});""",
        "js_en": """function showSS() {
    const result = document.getElementById('result-area');
    const div = document.getElementById('ss-result');
    const keys = Object.keys(sessionStorage);
    if (keys.length === 0) {
        div.innerHTML = '<p>SessionStorage is empty.</p>';
    } else {
        let html = '<table class="verify-table"><tr><th>Key</th><th>Value</th><th>Action</th></tr>';
        keys.forEach(k => {
            const v = sessionStorage.getItem(k);
            html += `<tr><td>${k}</td><td style="max-width:200px;overflow:hidden;text-overflow:ellipsis;">${v.substring(0,60)}${v.length>60?'...':''}</td><td><button class="del-ss-btn" data-key="${k}">Delete</button></td></tr>`;
        });
        html += '</table>';
        div.innerHTML = html;
    }
    result.style.display = 'block';
    document.getElementById('export-btn').style.display = 'inline-block';
    document.getElementById('clear-ss-btn').style.display = 'inline-block';
    document.getElementById('add-group').style.display = 'flex';
    document.querySelectorAll('.del-ss-btn').forEach(b => {
        b.addEventListener('click', () => {
            sessionStorage.removeItem(b.dataset.key);
            showToast('Deleted: ' + b.dataset.key);
            showSS();
        });
    });
}
document.getElementById('view-btn').addEventListener('click', showSS);
document.getElementById('clear-ss-btn').addEventListener('click', () => {
    sessionStorage.clear();
    showToast('SessionStorage cleared');
    showSS();
});
document.getElementById('export-btn').addEventListener('click', () => {
    const data = {};
    Object.keys(sessionStorage).forEach(k => { data[k] = sessionStorage.getItem(k); });
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'sessionstorage-export.json';
    a.click();
    showToast('JSON file exported');
});
document.getElementById('add-btn').addEventListener('click', () => {
    const key = document.getElementById('ss-key').value.trim();
    const value = document.getElementById('ss-value').value;
    if (!key) { showToast('Please enter a key'); return; }
    sessionStorage.setItem(key, value);
    showToast('Added');
    showSS();
});""",
    },
    {
        "slug": "tap-code-translator",
        "cn_name": "敲击码翻译器",
        "en_name": "Tap Code Translator",
        "cn_desc": "在线敲击码(Tap Code)编码解码工具，将文本转换为5×5网格敲击码，常用于囚犯通信和密码学学习。",
        "en_desc": "Free online Tap Code encoder and decoder. Convert text to 5×5 grid tap codes, commonly used in prisoner communication and cryptography.",
        "cn_keywords": "敲击码,Tap Code,囚犯密码,密码编码,加密解密,5×5网格,在线密码工具",
        "en_keywords": "tap code,tap cipher,prisoner code,cipher encoder,cryptography,5x5 grid,online cipher tool",
        "category": "加密工具",
        "en_category": "Encryption Tools",
        "html_cn": """<div class="tab-nav">
    <button class="tab-btn active" data-tab="encode">编码 (文本→敲击码)</button>
    <button class="tab-btn" data-tab="decode">解码 (敲击码→文本)</button>
</div>
<div class="input-group">
    <label for="tap-input">输入文本</label>
    <textarea id="tap-input" rows="4" placeholder="输入要编码/解码的文本..."></textarea>
</div>
<div class="btn-row">
    <button id="convert-btn" class="btn-primary">转换</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">转换结果</div>
    <div id="tap-result"></div>
</div>""",
        "html_en": """<div class="tab-nav">
    <button class="tab-btn active" data-tab="encode">Encode (Text → Tap Code)</button>
    <button class="tab-btn" data-tab="decode">Decode (Tap Code → Text)</button>
</div>
<div class="input-group">
    <label for="tap-input">Enter Text</label>
    <textarea id="tap-input" rows="4" placeholder="Enter text to encode or decode..."></textarea>
</div>
<div class="btn-row">
    <button id="convert-btn" class="btn-primary">Convert</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Result</div>
    <div id="tap-result"></div>
</div>""",
        "js_cn": """const TAP_GRID = 'ABCDEFGHIJLMNOPQRSTUVWXYZ';
let mode = 'encode';
document.querySelectorAll('.tab-btn').forEach(b => {
    b.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        mode = b.dataset.tab;
        document.getElementById('result-area').style.display = 'none';
    });
});
document.getElementById('convert-btn').addEventListener('click', () => {
    const input = document.getElementById('tap-input').value.toUpperCase().trim();
    if (!input) { showToast('请输入文本'); return; }
    const result = document.getElementById('result-area');
    const div = document.getElementById('tap-result');
    if (mode === 'encode') {
        let out = [];
        for (const ch of input) {
            if (ch === 'K') { out.push('(C)'); continue; }
            const idx = TAP_GRID.indexOf(ch);
            if (idx === -1) { out.push(ch); continue; }
            const row = Math.floor(idx / 5) + 1;
            const col = (idx % 5) + 1;
            out.push(`${row}·${col}`);
        }
        div.innerHTML = '<p><strong>敲击码:</strong></p><p style="font-size:1.2em;">' + out.join(' ') + '</p>';
    } else {
        const parts = input.split(/[\\s,]+/);
        let out = [];
        for (const p of parts) {
            if (p === '(C)' || p === '(c)') { out.push('K'); continue; }
            const m = p.match(/^(\\d)[·.](\\d)$/);
            if (m) {
                const row = parseInt(m[1]) - 1;
                const col = parseInt(m[2]) - 1;
                if (row >= 0 && row < 5 && col >= 0 && col < 5) {
                    out.push(TAP_GRID[row * 5 + col]);
                    continue;
                }
            }
            out.push(p);
        }
        div.innerHTML = '<p><strong>原文:</strong></p><p style="font-size:1.2em;">' + out.join('') + '</p>';
    }
    result.style.display = 'block';
});""",
        "js_en": """const TAP_GRID = 'ABCDEFGHIJLMNOPQRSTUVWXYZ';
let mode = 'encode';
document.querySelectorAll('.tab-btn').forEach(b => {
    b.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        mode = b.dataset.tab;
        document.getElementById('result-area').style.display = 'none';
    });
});
document.getElementById('convert-btn').addEventListener('click', () => {
    const input = document.getElementById('tap-input').value.toUpperCase().trim();
    if (!input) { showToast('Please enter text'); return; }
    const result = document.getElementById('result-area');
    const div = document.getElementById('tap-result');
    if (mode === 'encode') {
        let out = [];
        for (const ch of input) {
            if (ch === 'K') { out.push('(C)'); continue; }
            const idx = TAP_GRID.indexOf(ch);
            if (idx === -1) { out.push(ch); continue; }
            const row = Math.floor(idx / 5) + 1;
            const col = (idx % 5) + 1;
            out.push(`${row}·${col}`);
        }
        div.innerHTML = '<p><strong>Tap Code:</strong></p><p style="font-size:1.2em;">' + out.join(' ') + '</p>';
    } else {
        const parts = input.split(/[\\s,]+/);
        let out = [];
        for (const p of parts) {
            if (p === '(C)' || p === '(c)') { out.push('K'); continue; }
            const m = p.match(/^(\\d)[·.](\\d)$/);
            if (m) {
                const row = parseInt(m[1]) - 1;
                const col = parseInt(m[2]) - 1;
                if (row >= 0 && row < 5 && col >= 0 && col < 5) {
                    out.push(TAP_GRID[row * 5 + col]);
                    continue;
                }
            }
            out.push(p);
        }
        div.innerHTML = '<p><strong>Decoded:</strong></p><p style="font-size:1.2em;">' + out.join('') + '</p>';
    }
    result.style.display = 'block';
});""",
    },
    {
        "slug": "leet-speak-generator",
        "cn_name": "Leet Speak生成器",
        "en_name": "Leet Speak Generator",
        "cn_desc": "在线Leet Speak(1337)文本转换工具，将普通文本转换为黑客风格的Leet语言，支持多种替换规则。",
        "en_desc": "Free online Leet Speak (1337) text converter. Transform normal text into hacker-style leet language with multiple substitution rules.",
        "cn_keywords": "Leet Speak,1337,黑客语言,文本转换,网络用语,在线转换工具,leet转换",
        "en_keywords": "leet speak,1337,hacker language,text converter,internet slang,leet translator,online text tool",
        "category": "文本工具",
        "en_category": "Text Tools",
        "html_cn": """<div class="input-group">
    <label for="leet-input">输入文本</label>
    <textarea id="leet-input" rows="4" placeholder="输入要转换的文本..."></textarea>
</div>
<div class="btn-row">
    <label style="display:flex;align-items:center;gap:8px;">
        <select id="level-select">
            <option value="basic">基础替换</option>
            <option value="advanced">高级替换</option>
            <option value="extreme">极限替换</option>
        </select>
        <span>替换级别</span>
    </label>
    <button id="convert-btn" class="btn-primary">转换</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">转换结果</div>
    <div id="leet-result"></div>
    <button id="copy-btn" class="btn-secondary" style="margin-top:10px;">复制结果</button>
</div>""",
        "html_en": """<div class="input-group">
    <label for="leet-input">Enter Text</label>
    <textarea id="leet-input" rows="4" placeholder="Enter text to convert..."></textarea>
</div>
<div class="btn-row">
    <label style="display:flex;align-items:center;gap:8px;">
        <select id="level-select">
            <option value="basic">Basic</option>
            <option value="advanced">Advanced</option>
            <option value="extreme">Extreme</option>
        </select>
        <span>Level</span>
    </label>
    <button id="convert-btn" class="btn-primary">Convert</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Result</div>
    <div id="leet-result"></div>
    <button id="copy-btn" class="btn-secondary" style="margin-top:10px;">Copy Result</button>
</div>""",
        "js_cn": """const LEET_MAPS = {
    basic: {A:'4',E:'3',I:'1',O:'0',S:'5',T:'7'},
    advanced: {A:'4',B:'8',E:'3',G:'6',I:'1',L:'1',O:'0',S:'5',T:'7',Z:'2'},
    extreme: {A:'4',B:'|3',C:'(',D:'|)',E:'3',F:'|=',G:'6',H:'|-|',I:'1',J:'_|',K:'|<',L:'|_',M:'|\\\\/|',N:'|\\\\|',O:'0',P:'|*',Q:'0_',R:'|2',S:'5',T:'7',U:'|_|',V:'\\\\/',W:'\\\\/\\\\/',X:'><',Y:'`/',Z:'2'}
};
document.getElementById('convert-btn').addEventListener('click', () => {
    const input = document.getElementById('leet-input').value;
    if (!input.trim()) { showToast('请输入文本'); return; }
    const level = document.getElementById('level-select').value;
    const map = LEET_MAPS[level];
    let result = '';
    for (const ch of input) {
        const upper = ch.toUpperCase();
        result += map[upper] || ch;
    }
    document.getElementById('leet-result').textContent = result;
    document.getElementById('result-area').style.display = 'block';
});
document.getElementById('copy-btn').addEventListener('click', () => {
    const text = document.getElementById('leet-result').textContent;
    navigator.clipboard.writeText(text).then(() => showToast('已复制到剪贴板'));
});""",
        "js_en": """const LEET_MAPS = {
    basic: {A:'4',E:'3',I:'1',O:'0',S:'5',T:'7'},
    advanced: {A:'4',B:'8',E:'3',G:'6',I:'1',L:'1',O:'0',S:'5',T:'7',Z:'2'},
    extreme: {A:'4',B:'|3',C:'(',D:'|)',E:'3',F:'|=',G:'6',H:'|-|',I:'1',J:'_|',K:'|<',L:'|_',M:'|\\\\/|',N:'|\\\\|',O:'0',P:'|*',Q:'0_',R:'|2',S:'5',T:'7',U:'|_|',V:'\\\\/',W:'\\\\/\\\\/',X:'><',Y:'`/',Z:'2'}
};
document.getElementById('convert-btn').addEventListener('click', () => {
    const input = document.getElementById('leet-input').value;
    if (!input.trim()) { showToast('Please enter text'); return; }
    const level = document.getElementById('level-select').value;
    const map = LEET_MAPS[level];
    let result = '';
    for (const ch of input) {
        const upper = ch.toUpperCase();
        result += map[upper] || ch;
    }
    document.getElementById('leet-result').textContent = result;
    document.getElementById('result-area').style.display = 'block';
});
document.getElementById('copy-btn').addEventListener('click', () => {
    const text = document.getElementById('leet-result').textContent;
    navigator.clipboard.writeText(text).then(() => showToast('Copied to clipboard'));
});""",
    },
    {
        "slug": "google-fonts-preview",
        "cn_name": "Google Fonts预览",
        "en_name": "Google Fonts Preview",
        "cn_desc": "在线Google Fonts字体预览工具，支持搜索和预览上千种免费字体，实时调整字重、字号和样式。",
        "en_desc": "Free Google Fonts preview tool. Search and preview thousands of free fonts, adjust weight, size and style in real time.",
        "cn_keywords": "Google Fonts,字体预览,网页字体,免费字体,在线字体预览,字体选择器,前端开发",
        "en_keywords": "google fonts,font preview,web fonts,free fonts,online font preview,font picker,frontend dev",
        "category": "设计工具",
        "en_category": "Design Tools",
        "html_cn": """<div class="input-group">
    <label for="font-search">搜索字体</label>
    <input type="text" id="font-search" placeholder="例如: Roboto, Open Sans, 或输入关键词...">
</div>
<div class="input-group">
    <label for="preview-text">预览文本</label>
    <textarea id="preview-text" rows="2">敏捷的棕色狐狸跳过了懒狗。The quick brown fox jumps over the lazy dog.</textarea>
</div>
<div class="btn-row">
    <label>
        字重: <input type="range" id="weight-range" min="100" max="900" step="100" value="400">
        <span id="weight-val">400</span>
    </label>
    <label>
        字号: <input type="range" id="size-range" min="12" max="72" value="32">
        <span id="size-val">32px</span>
    </label>
</div>
<div class="btn-row">
    <button id="load-btn" class="btn-primary">加载字体</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">字体预览</div>
    <div id="font-preview" style="padding:20px;min-height:100px;word-break:break-word;"></div>
</div>""",
        "html_en": """<div class="input-group">
    <label for="font-search">Search Fonts</label>
    <input type="text" id="font-search" placeholder="e.g. Roboto, Open Sans, or keywords...">
</div>
<div class="input-group">
    <label for="preview-text">Preview Text</label>
    <textarea id="preview-text" rows="2">The quick brown fox jumps over the lazy dog. 敏捷的棕色狐狸跳过了懒狗。</textarea>
</div>
<div class="btn-row">
    <label>
        Weight: <input type="range" id="weight-range" min="100" max="900" step="100" value="400">
        <span id="weight-val">400</span>
    </label>
    <label>
        Size: <input type="range" id="size-range" min="12" max="72" value="32">
        <span id="size-val">32px</span>
    </label>
</div>
<div class="btn-row">
    <button id="load-btn" class="btn-primary">Load Font</button>
</div>
<div id="result-area" class="result-box" style="display:none;">
    <div class="result-header">Font Preview</div>
    <div id="font-preview" style="padding:20px;min-height:100px;word-break:break-word;"></div>
</div>""",
        "js_cn": """const weightRange = document.getElementById('weight-range');
const sizeRange = document.getElementById('size-range');
weightRange.addEventListener('input', () => document.getElementById('weight-val').textContent = weightRange.value);
sizeRange.addEventListener('input', () => document.getElementById('size-val').textContent = sizeRange.value + 'px');

document.getElementById('load-btn').addEventListener('click', () => {
    const fontName = document.getElementById('font-search').value.trim();
    if (!fontName) { showToast('请输入字体名称'); return; }
    const weight = weightRange.value;
    const size = sizeRange.value;
    const preview = document.getElementById('font-preview');
    const text = document.getElementById('preview-text').value;
    const formatted = fontName.replace(/\\s+/g, '+');
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `https://fonts.googleapis.com/css2?family=${formatted}:wght@${weight}&display=swap`;
    link.onload = () => {
        preview.style.fontFamily = `'${fontName}', sans-serif`;
        preview.style.fontWeight = weight;
        preview.style.fontSize = size + 'px';
        preview.textContent = text;
        document.getElementById('result-area').style.display = 'block';
    };
    link.onerror = () => {
        showToast('字体加载失败，请检查字体名称');
    };
    document.head.appendChild(link);
});""",
        "js_en": """const weightRange = document.getElementById('weight-range');
const sizeRange = document.getElementById('size-range');
weightRange.addEventListener('input', () => document.getElementById('weight-val').textContent = weightRange.value);
sizeRange.addEventListener('input', () => document.getElementById('size-val').textContent = sizeRange.value + 'px');

document.getElementById('load-btn').addEventListener('click', () => {
    const fontName = document.getElementById('font-search').value.trim();
    if (!fontName) { showToast('Please enter a font name'); return; }
    const weight = weightRange.value;
    const size = sizeRange.value;
    const preview = document.getElementById('font-preview');
    const text = document.getElementById('preview-text').value;
    const formatted = fontName.replace(/\\s+/g, '+');
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `https://fonts.googleapis.com/css2?family=${formatted}:wght@${weight}&display=swap`;
    link.onload = () => {
        preview.style.fontFamily = `'${fontName}', sans-serif`;
        preview.style.fontWeight = weight;
        preview.style.fontSize = size + 'px';
        preview.textContent = text;
        document.getElementById('result-area').style.display = 'block';
    };
    link.onerror = () => {
        showToast('Font load failed. Please check the font name.');
    };
    document.head.appendChild(link);
});""",
    },
    # 第11个：viewport-checker已经在上面的数组中，再补充一个工具
    {
        "slug": "icon-finder",
        "cn_name": "图标搜索器",
        "en_name": "Icon Finder",
        "cn_desc": "在线Emoji和Unicode符号搜索工具，快速查找并复制各种图标、表情符号和特殊字符，支持分类浏览。",
        "en_desc": "Free online emoji and Unicode symbol search tool. Find and copy icons, emojis and special characters. Browse by category.",
        "cn_keywords": "图标搜索,Emoji搜索,Unicode符号,表情符号,特殊字符,在线图标工具,复制粘贴",
        "en_keywords": "icon finder,emoji search,unicode symbols,special characters,emoji copy,online icon tool",
        "category": "文本工具",
        "en_category": "Text Tools",
        "html_cn": """<div class="input-group">
    <label for="icon-search">搜索图标</label>
    <input type="text" id="icon-search" placeholder="例如: 箭头, 心形, 星星, check...">
</div>
<div class="btn-row">
    <button class="cat-btn active" data-cat="all">全部</button>
    <button class="cat-btn" data-cat="arrows">箭头</button>
    <button class="cat-btn" data-cat="shapes">形状</button>
    <button class="cat-btn" data-cat="math">数学</button>
    <button class="cat-btn" data-cat="currency">货币</button>
    <button class="cat-btn" data-cat="faces">表情</button>
    <button class="cat-btn" data-cat="misc">杂项</button>
</div>
<div id="icon-grid" class="icon-grid"></div>""",
        "html_en": """<div class="input-group">
    <label for="icon-search">Search Icons</label>
    <input type="text" id="icon-search" placeholder="e.g. arrow, heart, star, check...">
</div>
<div class="btn-row">
    <button class="cat-btn active" data-cat="all">All</button>
    <button class="cat-btn" data-cat="arrows">Arrows</button>
    <button class="cat-btn" data-cat="shapes">Shapes</button>
    <button class="cat-btn" data-cat="math">Math</button>
    <button class="cat-btn" data-cat="currency">Currency</button>
    <button class="cat-btn" data-cat="faces">Faces</button>
    <button class="cat-btn" data-cat="misc">Misc</button>
</div>
<div id="icon-grid" class="icon-grid"></div>""",
        "js_cn": """const ICONS = {
    arrows: ['←','→','↑','↓','↔','↕','↖','↗','↘','↙','↩','↪','↶','↷','➔','➜','➝','➞','▲','▼','◄','►','△','▽','◁','▷','⬆','⬇','⬅','➡'],
    shapes: ['●','○','■','□','◆','◇','▲','△','▼','▽','★','☆','♥','♡','♦','♢','♣','♤','♠','♧','✚','✖','✓','✗','☐','☑','⚫','⚪','⬛','⬜'],
    math: ['∞','±','×','÷','≠','≈','≤','≥','∑','∏','√','∝','∫','∂','∇','∈','∉','⊂','⊃','∪','∩','∧','∨','¬','∀','∃','∄','∴','∵'],
    currency: ['$','€','£','¥','₩','₹','₽','₿','¢','₪','₫','₱','₲','₴','₵','₸','₺','₼','₾','﷼'],
    faces: ['😀','😃','😄','😁','😆','😅','🤣','😂','🙂','😊','😇','😍','🤩','😘','😗','😚','😋','😛','😜','🤪','😝','🤑','🤗','🤭','🤫','🤔','🤐','🤨','😐','😑'],
    misc: ['©','®','™','°','‰','µ','¶','§','†','‡','•','…','‽','⁂','※','‿','⁀','⁄','⁒','★']
};
let currentCat = 'all';
function renderIcons(filter = '') {
    const grid = document.getElementById('icon-grid');
    let icons = [];
    if (currentCat === 'all') {
        for (const cat in ICONS) icons = icons.concat(ICONS[cat].map(i => ({icon:i, cat})));
    } else {
        icons = (ICONS[currentCat] || []).map(i => ({icon:i, cat:currentCat}));
    }
    if (filter) {
        const f = filter.toLowerCase();
        icons = icons.filter(i => i.icon.toLowerCase().includes(f) || i.cat.toLowerCase().includes(f));
    }
    grid.innerHTML = icons.map((i, idx) => `<button class="icon-item" data-icon="${i.icon}" title="点击复制">${i.icon}</button>`).join('');
    grid.querySelectorAll('.icon-item').forEach(b => {
        b.addEventListener('click', () => {
            navigator.clipboard.writeText(b.dataset.icon).then(() => showToast('已复制: ' + b.dataset.icon));
        });
    });
}
document.getElementById('icon-search').addEventListener('input', function() {
    renderIcons(this.value);
});
document.querySelectorAll('.cat-btn').forEach(b => {
    b.addEventListener('click', () => {
        document.querySelectorAll('.cat-btn').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        currentCat = b.dataset.cat;
        renderIcons(document.getElementById('icon-search').value);
    });
});
renderIcons();""",
        "js_en": """const ICONS = {
    arrows: ['←','→','↑','↓','↔','↕','↖','↗','↘','↙','↩','↪','↶','↷','➔','➜','➝','➞','▲','▼','◄','►','△','▽','◁','▷','⬆','⬇','⬅','➡'],
    shapes: ['●','○','■','□','◆','◇','▲','△','▼','▽','★','☆','♥','♡','♦','♢','♣','♤','♠','♧','✚','✖','✓','✗','☐','☑','⚫','⚪','⬛','⬜'],
    math: ['∞','±','×','÷','≠','≈','≤','≥','∑','∏','√','∝','∫','∂','∇','∈','∉','⊂','⊃','∪','∩','∧','∨','¬','∀','∃','∄','∴','∵'],
    currency: ['$','€','£','¥','₩','₹','₽','₿','¢','₪','₫','₱','₲','₴','₵','₸','₺','₼','₾','﷼'],
    faces: ['😀','😃','😄','😁','😆','😅','🤣','😂','🙂','😊','😇','😍','🤩','😘','😗','😚','😋','😛','😜','🤪','😝','🤑','🤗','🤭','🤫','🤔','🤐','🤨','😐','😑'],
    misc: ['©','®','™','°','‰','µ','¶','§','†','‡','•','…','‽','⁂','※','‿','⁀','⁄','⁒','★']
};
let currentCat = 'all';
function renderIcons(filter = '') {
    const grid = document.getElementById('icon-grid');
    let icons = [];
    if (currentCat === 'all') {
        for (const cat in ICONS) icons = icons.concat(ICONS[cat].map(i => ({icon:i, cat})));
    } else {
        icons = (ICONS[currentCat] || []).map(i => ({icon:i, cat:currentCat}));
    }
    if (filter) {
        const f = filter.toLowerCase();
        icons = icons.filter(i => i.icon.toLowerCase().includes(f) || i.cat.toLowerCase().includes(f));
    }
    grid.innerHTML = icons.map((i, idx) => `<button class="icon-item" data-icon="${i.icon}" title="Click to copy">${i.icon}</button>`).join('');
    grid.querySelectorAll('.icon-item').forEach(b => {
        b.addEventListener('click', () => {
            navigator.clipboard.writeText(b.dataset.icon).then(() => showToast('Copied: ' + b.dataset.icon));
        });
    });
}
document.getElementById('icon-search').addEventListener('input', function() {
    renderIcons(this.value);
});
document.querySelectorAll('.cat-btn').forEach(b => {
    b.addEventListener('click', () => {
        document.querySelectorAll('.cat-btn').forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        currentCat = b.dataset.cat;
        renderIcons(document.getElementById('icon-search').value);
    });
});
renderIcons();""",
    },
]

# 通用页面模板
def make_page(t, lang):
    """生成完整HTML页面"""
    is_cn = (lang == 'cn')
    lang_attr = 'zh-CN' if is_cn else 'en'
    name = t['cn_name'] if is_cn else t['en_name']
    desc = t['cn_desc'] if is_cn else t['en_desc']
    keywords = t['cn_keywords'] if is_cn else t['en_keywords']
    category = t['category'] if is_cn else t['en_category']
    html_body = t['html_cn'] if is_cn else t['html_en']
    js_code = t['js_cn'] if is_cn else t['js_en']
    slug = t['slug']
    base_url = f'/{slug}/' if is_cn else f'/en/{slug}/'
    canonical = f'https://free-toolbase.com/{slug}/' if is_cn else f'https://free-toolbase.com/en/{slug}/'
    alt_href = f'https://free-toolbase.com/en/{slug}/' if is_cn else f'https://free-toolbase.com/{slug}/'
    alt_lang = 'en' if is_cn else 'zh-CN'
    home_url = '/' if is_cn else '/en/'
    home_label = '首页' if is_cn else 'Home'
    all_tools_label = '全部工具' if is_cn else 'All Tools'
    all_tools_url = '/#tools' if is_cn else '/en/#tools'

    return f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} - Free ToolBase</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="{alt_lang}" href="{alt_href}">
  <link rel="alternate" hreflang="{'zh-CN' if not is_cn else 'en'}" href="{'https://free-toolbase.com/' + slug + '/' if not is_cn else 'https://free-toolbase.com/en/' + slug + '/'}">
  <meta property="og:title" content="{name} - Free ToolBase">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "{name}",
    "description": "{desc}",
    "applicationCategory": "WebApplication",
    "operatingSystem": "Any",
    "url": "{canonical}",
    "offers": {{"@type": "Offer", "price": "0"}}
  }}
  </script>
  <style>
    :root {{
      --primary: #4F46E5;
      --primary-dark: #4338CA;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #1e293b;
      --text-secondary: #64748b;
      --border: #e2e8f0;
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --radius: 12px;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }}
    header {{
      background: var(--card-bg);
      border-bottom: 1px solid var(--border);
      padding: 16px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }}
    header .logo {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--primary);
      text-decoration: none;
    }}
    header nav a {{
      color: var(--text-secondary);
      text-decoration: none;
      margin-left: 20px;
      font-size: 0.95rem;
    }}
    header nav a:hover {{ color: var(--primary); }}
    main {{
      max-width: 800px;
      margin: 0 auto;
      padding: 32px 24px;
    }}
    h1 {{
      font-size: 1.75rem;
      margin-bottom: 8px;
      color: var(--text);
    }}
    .subtitle {{
      color: var(--text-secondary);
      margin-bottom: 24px;
      font-size: 0.95rem;
    }}
    .input-group {{
      margin-bottom: 16px;
    }}
    .input-group label {{
      display: block;
      font-weight: 600;
      margin-bottom: 6px;
      font-size: 0.9rem;
    }}
    .input-group input,
    .input-group textarea,
    .input-group select {{
      width: 100%;
      padding: 12px 16px;
      border: 2px solid var(--border);
      border-radius: var(--radius);
      font-size: 1rem;
      background: var(--card-bg);
      color: var(--text);
      transition: border-color 0.2s;
    }}
    .input-group input:focus,
    .input-group textarea:focus,
    .input-group select:focus {{
      outline: none;
      border-color: var(--primary);
    }}
    .input-group textarea {{ resize: vertical; min-height: 80px; }}
    .btn-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 20px;
      align-items: center;
    }}
    .btn-primary {{
      background: var(--primary);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: var(--radius);
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }}
    .btn-primary:hover {{ background: var(--primary-dark); }}
    .btn-secondary {{
      background: var(--card-bg);
      color: var(--text);
      border: 2px solid var(--border);
      padding: 12px 24px;
      border-radius: var(--radius);
      font-size: 1rem;
      cursor: pointer;
      transition: border-color 0.2s;
    }}
    .btn-secondary:hover {{ border-color: var(--primary); }}
    .btn-danger {{
      background: var(--danger);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: var(--radius);
      font-size: 1rem;
      cursor: pointer;
    }}
    .result-box {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 20px;
      margin-top: 8px;
    }}
    .result-header {{
      font-weight: 700;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border);
      color: var(--primary);
    }}
    .verify-table {{
      width: 100%;
      border-collapse: collapse;
    }}
    .verify-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
    }}
    .verify-table td:first-child {{
      font-weight: 600;
      color: var(--text-secondary);
      width: 40%;
    }}
    .verify-table .pass {{ color: var(--success); font-weight: 600; }}
    .verify-table .fail {{ color: var(--danger); font-weight: 600; }}
    .verify-table .warn {{ color: var(--warning); font-weight: 600; }}
    .verify-table th {{
      padding: 10px 12px;
      text-align: left;
      border-bottom: 2px solid var(--border);
      color: var(--text-secondary);
    }}
    .tab-nav {{ display: flex; gap: 0; margin-bottom: 16px; border-bottom: 2px solid var(--border); }}
    .tab-btn {{
      padding: 10px 20px;
      border: none;
      background: none;
      cursor: pointer;
      font-size: 0.95rem;
      color: var(--text-secondary);
      border-bottom: 2px solid transparent;
      margin-bottom: -2px;
      transition: all 0.2s;
    }}
    .tab-btn.active {{
      color: var(--primary);
      border-bottom-color: var(--primary);
      font-weight: 600;
    }}
    .preset-btn {{
      background: var(--card-bg);
      color: var(--text);
      border: 2px solid var(--border);
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .preset-btn:hover {{ border-color: var(--primary); color: var(--primary); }}
    .viewport-display {{
      text-align: center;
      padding: 24px;
      background: linear-gradient(135deg, #4F46E5, #7C3AED);
      color: white;
      border-radius: var(--radius);
      margin-bottom: 20px;
    }}
    .vp-size {{ font-size: 2rem; font-weight: 700; font-family: monospace; }}
    .vp-label {{ font-size: 0.85rem; opacity: 0.85; margin-top: 4px; }}
    .breakpoint-info {{
      padding: 12px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      text-align: center;
    }}
    .dns-record {{
      padding: 8px 12px;
      background: #f1f5f9;
      border-radius: 6px;
      margin-bottom: 6px;
      font-family: monospace;
      font-size: 0.95rem;
    }}
    .icon-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(48px, 1fr));
      gap: 8px;
      margin-top: 16px;
    }}
    .icon-item {{
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--card-bg);
      cursor: pointer;
      transition: all 0.2s;
    }}
    .icon-item:hover {{ border-color: var(--primary); transform: scale(1.1); background: #EEF2FF; }}
    .cat-btn {{
      background: var(--card-bg);
      border: 2px solid var(--border);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .cat-btn.active {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }}
    .del-cookie-btn, .del-ls-btn, .del-ss-btn {{
      background: var(--danger);
      color: white;
      border: none;
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 0.8rem;
      cursor: pointer;
    }}
    .unit {{ color: var(--text-secondary); font-size: 0.9rem; }}
    .input-group input[type="number"] {{ width: 120px; display: inline-block; }}
    footer {{
      text-align: center;
      padding: 24px;
      color: var(--text-secondary);
      font-size: 0.85rem;
      border-top: 1px solid var(--border);
      margin-top: 40px;
    }}
    footer a {{ color: var(--primary); text-decoration: none; }}
    #toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      color: white;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 0.9rem;
      opacity: 0;
      transition: opacity 0.3s;
      pointer-events: none;
      z-index: 9999;
    }}
    #toast.show {{ opacity: 1; }}
    @media (max-width: 600px) {{
      main {{ padding: 20px 16px; }}
      h1 {{ font-size: 1.4rem; }}
      .btn-row {{ flex-direction: column; }}
      .btn-primary, .btn-secondary, .btn-danger {{ width: 100%; text-align: center; }}
      .vp-size {{ font-size: 1.5rem; }}
    }}
  </style>
</head>
<body>
  <header>
    <a href="{home_url}" class="logo">Free ToolBase</a>
    <nav>
      <a href="{home_url}">{home_label}</a>
      <a href="{all_tools_url}">{all_tools_label}</a>
    </nav>
  </header>
  <main>
    <h1>{name}</h1>
    <p class="subtitle">{desc}</p>
    {html_body}
  </main>
  <footer>
    <p>&copy; 2025 <a href="/">Free ToolBase</a> - {"免费在线工具" if is_cn else "Free Online Tools"}</p>
  </footer>
  <div id="toast"></div>
  <script>
    function showToast(msg) {{
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      clearTimeout(t._timeout);
      t._timeout = setTimeout(() => t.classList.remove('show'), 2500);
    }}
    {js_code}
  </script>
</body>
</html>'''

# 生成所有页面
for t in tools:
    slug = t['slug']
    # 中文版
    cn_path = os.path.join(BASE, slug, 'index.html')
    with open(cn_path, 'w', encoding='utf-8') as f:
        f.write(make_page(t, 'cn'))
    print(f'✅ {slug}/index.html (CN)')
    # 英文版
    en_path = os.path.join(BASE, 'en', slug, 'index.html')
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(make_page(t, 'en'))
    print(f'✅ en/{slug}/index.html (EN)')

print(f'\n共生成 {len(tools)} 个工具 × 2 = {len(tools)*2} 个页面')
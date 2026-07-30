#!/usr/bin/env python3
"""IndexNow自动提交脚本 - 每次push后自动通知Bing/Yandex索引"""
import json, re, subprocess, sys, os

SITE = "free-toolbase.com"
KEY = "4ad7588719f777dfd0c4ce891360e57e"
KEY_URL = f"https://{SITE}/{KEY}.txt"
SITEMAP = f"{SITE}/sitemap.xml"

def get_urls_from_sitemap():
    with open('sitemap.xml') as f:
        return re.findall(r'<loc>(https?://[^<]+)</loc>', f.read())

def get_recently_changed_urls():
    """获取最近git commit修改的URL"""
    r = subprocess.run(['git', 'diff', 'HEAD~1', '--name-only'], 
                      capture_output=True, text=True, timeout=10)
    changed = r.stdout.strip().split('\n') if r.stdout.strip() else []
    urls = []
    for f in changed:
        # CN: tool-name/index.html -> https://free-toolbase.com/tool-name/
        m = re.match(r'^([^/]+)/index\.html$', f)
        if m:
            urls.append(f"https://{SITE}/{m.group(1)}/")
        # EN: en/tool-name/index.html -> https://free-toolbase.com/en/tool-name/
        m = re.match(r'^en/([^/]+)/index\.html$', f)
        if m:
            urls.append(f"https://{SITE}/en/{m.group(1)}/")
    return urls

def submit_indexnow(urls, endpoint="https://api.indexnow.org/IndexNow"):
    if not urls:
        print("No URLs to submit")
        return False
    
    payload = json.dumps({
        "host": SITE,
        "key": KEY,
        "keyLocation": KEY_URL,
        "urlList": urls[:10000]
    })
    
    with open('/tmp/indexnow_payload.json', 'w') as f:
        f.write(payload)
    
    r = subprocess.run(['curl', '-s', '-w', '\nHTTP:%{http_code}', 
                       '-X', 'POST', endpoint,
                       '-H', 'Content-Type: application/json',
                       '-d', '@/tmp/indexnow_payload.json'],
                      capture_output=True, text=True, timeout=60)
    
    output = r.stdout
    print(f"Response: {output[:300]}")
    
    if 'HTTP:200' in output or 'HTTP:202' in output:
        print(f"✅ Submitted {len(urls)} URLs to IndexNow")
        return True
    else:
        print(f"❌ IndexNow submission failed")
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        urls = get_urls_from_sitemap()
        print(f"Submitting all {len(urls)} URLs from sitemap...")
    else:
        urls = get_recently_changed_urls()
        print(f"Submitting {len(urls)} recently changed URLs...")
    
    if urls:
        # Try multiple endpoints
        for ep in ["https://api.indexnow.org/IndexNow", 
                   "https://www.bing.com/IndexNow",
                   "https://yandex.com/indexnow"]:
            print(f"\nTrying {ep}...")
            if submit_indexnow(urls, ep):
                break
    else:
        print("No URLs to submit")

#!/usr/bin/env python3
"""门9：大模型驱动的工具页面结构质检
不写检测规则，让大模型看页面HTML，自动发现所有结构问题。
"""
import os, json, sys, time, subprocess
from pathlib import Path

TOOLS_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = TOOLS_ROOT / 'quality' / 'gate9-issues.json'

SKIP = {'en','assets','scripts','quality','css','js','images','node_modules',
        '.git','.github','fonts','libs','vendor','dist','build','.gsc-data'}

BATCH_SIZE = 15  # 每批发给大模型的工具数
MODEL = "mimo-v2.5-free"

SYSTEM_PROMPT = """你是网页结构审查专家。检查HTML页面的结构问题。

规则：
1. 重复内容：两个或以上高度相似的文本块（标题、段落、FAQ区块），相似度>80%
2. 空白区域：有HTML容器标签但textContent为空或只有空格
3. 结构冗余：不必要的深层嵌套、多余的wrapper

只报告确凿的问题，不要报告正常差异。
返回严格JSON，不要markdown包裹：
{"tools": {"tool-name": [{"type": "重复H1/重复FAQ/空白div/冗余嵌套", "detail": "具体描述", "fix": "修复建议"}]}}
无问题返回: {"tools": {}}"""

def find_tools():
    dirs = []
    for d in sorted(TOOLS_ROOT.iterdir()):
        if d.is_dir() and d.name not in SKIP and (d / 'index.html').exists():
            dirs.append(d.name)
    return dirs

def read_tool_html(name):
    path = TOOLS_ROOT / name / 'index.html'
    with open(path) as f:
        html = f.read()
    # 提取body内容，去掉script/style
    import re
    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
    if not body:
        return html[:3000]
    content = body.group(1)
    # 去掉script和style
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    # 压缩空白
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r' {2,}', ' ', content)
    return content[:2500]  # 限制长度，控制token

def call_llm(prompt):
    """调用本地LLM via zen API"""
    import urllib.request
    url = "https://opencode.ai/zen/v1/chat/completions"
    
    # 获取API key
    key = os.environ.get("OPENCODE_ZEN_KEY1", "")
    if not key:
        # 尝试从config读取
        try:
            import yaml
            cfg_path = os.path.expanduser("~/.hermes/config.yaml")
            with open(cfg_path) as f:
                cfg = yaml.safe_load(f)
            # 找opencode-zen的key配置
            for pname, pcfg in cfg.get('providers', {}).items():
                if 'zen' in pname:
                    key_env = pcfg.get('key_env', '')
                    if key_env:
                        # 尝试从credential_store读
                        cred_file = os.path.expanduser(f"~/.hermes/credentials/{key_env}")
                        if os.path.exists(cred_file):
                            with open(cred_file) as cf:
                                key = cf.read().strip()
        except:
            pass
    
    data = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            content = result['choices'][0]['message']['content']
            return content
    except Exception as e:
        print(f"  API调用失败: {e}", file=sys.stderr)
        return None

def parse_response(text):
    """解析LLM返回的JSON"""
    import re
    # 去掉markdown包裹
    text = re.sub(r'^```(?:json)?\s*', '', text.strip())
    text = re.sub(r'\s*```$', '', text.strip())
    try:
        return json.loads(text)
    except:
        # 尝试提取JSON对象
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except:
                pass
        return None

def main():
    tools = find_tools()
    print(f"门9检测: {len(tools)}个工具, 每批{BATCH_SIZE}个, 共{(len(tools)+BATCH_SIZE-1)//BATCH_SIZE}批")
    
    all_issues = {}
    stats = {'ok': 0, 'with_issues': 0, 'errors': 0}
    
    for batch_start in range(0, len(tools), BATCH_SIZE):
        batch = tools[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1
        
        # 构建批处理prompt
        prompt_parts = []
        for name in batch:
            html = read_tool_html(name)
            prompt_parts.append(f"=== 工具: {name} ===\n{html}")
        
        prompt = "检查以下工具页面的结构问题：\n\n" + "\n\n".join(prompt_parts)
        
        print(f"  批次{batch_num}: {batch[0]}...{batch[-1]} ({len(batch)}个)", end=" ")
        sys.stdout.flush()
        
        result_text = call_llm(prompt)
        if result_text:
            result = parse_response(result_text)
            if result and 'tools' in result:
                tools_result = result['tools']
                for name, issues in tools_result.items():
                    if issues:
                        all_issues[name] = issues
                        stats['with_issues'] += 1
                    else:
                        stats['ok'] += 1
                print(f"✅ 发现{sum(1 for v in tools_result.values() if v)}个有问题")
            else:
                print(f"⚠️ 解析失败")
                stats['errors'] += 1
        else:
            print(f"❌ API失败")
            stats['errors'] += 1
        
        time.sleep(0.5)  # rate limit
    
    # 输出结果
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump({'stats': stats, 'issues': all_issues, 'model': MODEL}, 
                  f, indent=2, ensure_ascii=False)
    
    print(f"\n=== 门9完成 ===")
    print(f"  ✅ 正常: {stats['ok']}")
    print(f"  ❌ 有问题: {stats['with_issues']}")
    print(f"  ⚠️ 检测失败: {stats['errors']}")
    print(f"  结果: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Meta Description 批量扩充脚本 v6 - 最终版
EN策略重写：识别模板描述 → 去掉所有模板后缀 → 保留核心 → 加新后缀
"""
import os, re, sys

CN_SUFFIX = '。纯前端本地处理，数据不上传服务器，完全免费无需注册。'
EN_SUFFIX = ' Works entirely in your browser. Fast, secure, and no registration required.'

CN_EXTRAS = [
    '，操作简单即开即用',
    '，适合日常办公和学习使用',
    '，无需下载安装即可使用',
    '，响应迅速体验流畅',
]

EN_EXTRAS = [
    ' Ideal for developers and everyday users.',
    ' Simple interface with instant results.',
    ' Supports multiple formats and batch processing.',
    ' No downloads or installations needed.',
]


def clean_en_desc(desc):
    """清理EN描述：去除所有模板/营销后缀，只保留核心工具描述"""
    # 去除各种模板后缀模式
    templates = [
        r'\s*Fast,\s*secure,\s*and\s*no\s*registration\s*required\.?',
        r'\s*Works\s*(entirely|locally)?\s*in\s*your\s*browser\.?',
        r'\s*No\s*(signup|registration)\s*(needed|required)\.?',
        r'\s*Completely\s*free\s*(to\s*use)?\.?',
        r'\s*\|\s*no\s*signup\s*tool\.?',
        r'\s*-\s*toolbase\s*tool\.?',
        r'\s*100%\s*free\.?',
        r'\s*No\s*downloads\s*or\s*installations?\.?',
        r'\s*Privacy-friendly\s*and\s*secure\.?',
    ]
    for pat in templates:
        desc = re.sub(pat, '', desc, flags=re.I)
    
    # 清理多余空格和标点
    desc = re.sub(r'\s+', ' ', desc)
    desc = re.sub(r'\s*\.\s*\.', '.', desc)  # 双句号
    desc = desc.strip().rstrip('. ')
    
    return desc


def clean_cn_desc(desc):
    """清理CN描述中的模板后缀 — 循环清理直到稳定"""
    tail_pats = [
        r'[，。]?纯前端本地处理[，。]数据不上传服务器[，。]完全免费[，。]?无需注册[。]?$',
        r'[，。]?纯前端本地处理[，。]数据不上传服务器[，。]无需注册[，。]?完全免费[。]?$',
        r'[，。]?纯前端本地(处理|计算)[，。]数据安全[，。]?有保障[。]?$',
        r'[，。]?纯前端本地(处理|计算)[，。]数据安全[。]?$',
        r'[，。]?纯前端本地处理[，。]无需注册[，。]?完全免费[。]?$',
        r'[，。]?纯前端本地处理[，。]数据安全有保障[。]?$',
        r'[，。]?纯浏览器端本地运行[，。]无需注册[，。]完全免费[。]?$',
        r'[，。]?纯前端本地处理[，。]?不上传数据[，。]?$',
        r'[，。]?无需注册[，。]?完全免费[。]?$',
        r'[，。]?完全免费[，。]?无需注册[。]?$',
        r'[，。]?数据不上传服务器[，。]?$',
        r'[，。]?(代码|数据|文件|内容|信息|输入)不会?上传服务器[，。]?$',
        r'[，。]?(代码|数据|文件|内容|信息|输入)不会?上传[，。]?$',
        r'[，。]?(代码|数据|文件|内容|信息|输入)不(会|离开)(本地|浏览器)[，。]?$',
        r'[，。]?(代码|数据|文件|内容|信息|输入)本地处理[，。]?$',
        r'[，。]?纯前端本地(处理|计算)[。]?$',
        r'[，。]?纯前端(处理|计算)[，。]?$',
        r'[，。]?浏览器端运行[，。]?$',
    ]
    prev = None
    while prev != desc:
        prev = desc
        for pat in tail_pats:
            desc = re.sub(pat, '', desc)
    return desc.strip().rstrip('，,。. ')


def expand_cn(desc):
    if len(desc) >= 120:
        return desc
    desc = desc.strip().rstrip('，,。. ')
    cleaned = clean_cn_desc(desc)
    if len(cleaned) < 20:
        cleaned = desc
    
    if not cleaned.endswith('。'):
        cleaned += '。'
    
    base = cleaned + CN_SUFFIX
    base = re.sub(r'。{2,}', '。', base)
    
    if 120 <= len(base) <= 160:
        return base
    
    if len(base) < 120:
        for extra in CN_EXTRAS:
            ip = cleaned.rstrip('。.')
            candidate = ip + extra + '。' + CN_SUFFIX.lstrip('。')
            candidate = re.sub(r'。{2,}', '。', candidate)
            if 120 <= len(candidate) <= 160:
                return candidate
        # 尝试两个扩充词
        for i, e1 in enumerate(CN_EXTRAS):
            for e2 in CN_EXTRAS[i+1:]:
                ip = cleaned.rstrip('。.')
                candidate = ip + e1 + e2 + CN_SUFFIX
                candidate = re.sub(r'。{2,}', '。', candidate)
                if 120 <= len(candidate) <= 160:
                    return candidate
        # 极端情况：3个扩充词
        for i, e1 in enumerate(CN_EXTRAS):
            for j, e2 in enumerate(CN_EXTRAS[i+1:], i+1):
                for e3 in CN_EXTRAS[j+1:]:
                    ip = cleaned.rstrip('。.')
                    candidate = ip + e1 + e2 + e3 + CN_SUFFIX
                    candidate = re.sub(r'。{2,}', '。', candidate)
                    if 120 <= len(candidate) <= 160:
                        return candidate
        return base
    
    if len(base) > 160:
        short_suffix = '。纯前端本地处理，完全免费无需注册。'
        candidate = cleaned + short_suffix
        candidate = re.sub(r'。{2,}', '。', candidate)
        if 120 <= len(candidate) <= 160:
            return candidate
        max_clean = 160 - len(short_suffix)
        cutoff = cleaned[:max_clean].rfind('。')
        if cutoff > 80:
            return cleaned[:cutoff+1] + short_suffix
    
    return base


def expand_en(desc):
    if len(desc) >= 120:
        return desc
    
    core = clean_en_desc(desc)
    if len(core) < 15:
        core = desc
    
    if not core.endswith('.'):
        core += '.'
    
    # 去双句号
    core = re.sub(r'\.{2,}', '.', core)
    
    base = core + EN_SUFFIX
    if 120 <= len(base) <= 160:
        return base
    
    if len(base) < 120:
        for extra in EN_EXTRAS:
            candidate = core + extra + EN_SUFFIX
            if 120 <= len(candidate) <= 160:
                return candidate
        # 两个扩充词
        for i, e1 in enumerate(EN_EXTRAS):
            for e2 in EN_EXTRAS[i+1:]:
                candidate = core + e1 + e2 + EN_SUFFIX
                if 120 <= len(candidate) <= 160:
                    return candidate
        return base
    
    if len(base) > 160:
        short_suffix = ' Works in your browser. Fast, secure, no registration required.'
        candidate = core + short_suffix
        if 120 <= len(candidate) <= 160:
            return candidate
        max_clean = 160 - len(short_suffix)
        cutoff = core[:max_clean].rfind('.')
        if cutoff > 40:
            return core[:cutoff+1] + short_suffix
    
    return base


def is_en_path(rel):
    if rel.startswith('en/') or rel == 'en':
        return True
    if '/en/' in rel:
        return True
    return False


def process_files(dry_run=True):
    cn_up = en_up = cn_ok = en_ok = 0
    cn_shorter = en_shorter = 0
    cn_samples = en_samples = 0
    
    # 只跳过顶层系统目录，避免子串匹配误伤 json-*/css-* 等工具目录
    SKIP_DIRS = {'scripts', 'quality', 'css', 'js', 'node_modules', '.gsc', '.gsc-data'}
    for root, dirs, files in os.walk('.'):
        rel = os.path.relpath(root, '.')
        if rel == '.':
            pass
        elif rel.split(os.sep)[0] in SKIP_DIRS or any(s in rel.split(os.sep) for s in ('.git', 'node_modules', '.gsc', '.gsc-data')):
            continue
        
        for f in files:
            if f != 'index.html':
                continue
            
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except:
                continue
            
            m = re.search(r'(<meta name="description" content=")(.+?)(">)', content)
            if not m:
                continue
            
            prefix, old_desc, suffix_tag = m.group(1), m.group(2), m.group(3)
            old_len = len(old_desc)
            
            if old_len >= 120:
                if is_en_path(rel):
                    en_ok += 1
                else:
                    cn_ok += 1
                continue
            
            is_en = is_en_path(rel)
            
            if is_en:
                new_desc = expand_en(old_desc)
            else:
                new_desc = expand_cn(old_desc)
            
            new_len = len(new_desc)
            
            if new_len < old_len:
                if is_en:
                    en_shorter += 1
                else:
                    cn_shorter += 1
                new_desc = old_desc
                new_len = old_len
            
            if new_len > 160:
                sep = '.' if is_en else '。'
                cutoff = new_desc.rfind(sep, 0, 160)
                if cutoff > 120:
                    new_desc = new_desc[:cutoff+1]
                else:
                    new_desc = new_desc[:157]
                new_len = len(new_desc)
            
            show = False
            if is_en and en_samples < 8:
                show = True
                en_samples += 1
            elif not is_en and cn_samples < 5:
                show = True
                cn_samples += 1
            
            if dry_run and show:
                print(f"\n{'[EN]' if is_en else '[CN]'} {rel}")
                print(f"  OLD [{old_len}]: {old_desc}")
                print(f"  NEW [{new_len}]: {new_desc}")
            
            if not dry_run:
                new_meta = f'{prefix}{new_desc}{suffix_tag}'
                if new_meta != m.group(0):
                    new_content = content.replace(m.group(0), new_meta, 1)
                    with open(filepath, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
            
            if is_en:
                en_up += 1
            else:
                cn_up += 1
    
    print(f"\n=== Summary {'(DRY RUN)' if dry_run else '(APPLIED)'} ===")
    print(f"CN: {cn_up} to fix, {cn_ok} already OK, {cn_shorter} kept")
    print(f"EN: {en_up} to fix, {en_ok} already OK, {en_shorter} kept")


if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLYING'}")
    print("=" * 60)
    process_files(dry_run=dry_run)
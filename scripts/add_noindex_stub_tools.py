#!/usr/bin/env python3
"""批量给无法实现的空壳工具加noindex标签"""
import re, os

# PDF和视频处理类工具 - 需要pdf-lib/ffmpeg等外部库，纯前端无法实现
noindex_tools = [
    # PDF类
    "pdf-bookmark", "pdf-page-reorder", "pdf-password-protect", "pdf-add-image",
    "pdf-editor", "pdf-rotate", "html-to-pdf", "pdf-rotator", "jpg-to-pdf",
    "pdf-merger", "pdf-to-text", "pdf-add-watermark", "pdf-text-extractor",
    "merge-pdf", "pdf-redact", "png-to-pdf", "pdf-protect", "pdf-to-image",
    # 视频类
    "video-splitter", "video-to-mp4", "video-cropper", "gif-to-mp4",
    "video-speed-controller", "video-rotator",
    # 音频处理类（需要Web Audio API高级功能）
    "audio-recorder", "audio-waveform-visualizer", "voice-changer",
]

changed = 0
skipped = 0
for tool in noindex_tools:
    for lang in ['', 'en/']:
        f = os.path.join(lang + tool, "index.html")
        if not os.path.exists(f):
            continue
        content = open(f, encoding='utf-8').read()
        
        # 检查是否已有noindex
        if 'noindex' in content:
            skipped += 1
            continue
        
        # 替换 robots 标签
        old_pattern = r'<meta\s+name="robots"\s+content="index,\s*follow"\s*/?>'
        new_tag = '<meta name="robots" content="noindex, follow">'
        
        if re.search(old_pattern, content):
            new_content = re.sub(old_pattern, new_tag, content)
            with open(f, 'w', encoding='utf-8') as fw:
                fw.write(new_content)
            print(f"  OK {f}")
            changed += 1
        else:
            # 可能没有robots标签，检查是否有其他格式
            old_pattern2 = r'<meta\s+name="robots"\s+content="([^"]+)"\s*/?>'
            m = re.search(old_pattern2, content)
            if m:
                print(f"  WARN {f}: robots content = '{m.group(1)}' (not standard format)")
            else:
                print(f"  SKIP {f}: no robots tag found")

print(f"\nTotal changed: {changed}, skipped: {skipped}")

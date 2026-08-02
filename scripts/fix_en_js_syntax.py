#!/usr/bin/env python3
"""
批量修复EN版工具页面的JS语法错误：
1. 工具JS末尾多余的 })(;)</script> → 去掉 })();
2. addCopyBtns脚本中 // resultAddCopy 注释吞代码 → 去掉注释
3. })(;)</script> → })();</script> (addCopyBtns IIFE末尾)

使用方式: python3 scripts/fix_en_js_syntax.py [--dry-run]
"""

import os
import re
import sys

dry_run = '--dry-run' in sys.argv

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix 1: 工具JS末尾的 calc();})();</script> 或 convert();})();</script> 等
    # 模式：xxx();})();</script> → xxx();</script>
    # 但不能误改addCopyBtns的 })();</script>
    # addCopyBtns的特征是前面有 obs.observe
    # 工具JS的特征是前面有 calc(); 或 convert(); 等
    
    # Fix: })(;)</script> → })();</script> (addCopyBtns末尾)
    if '})(;)</script>' in content:
        content = content.replace('})(;)</script>', '})();</script>')
        changes.append('fix })(;)</script> → })();</script>')
    
    # Fix: // resultAddCopy var processed → var processed (去掉注释吞代码)
    if '// resultAddCopy var processed' in content:
        content = content.replace('// resultAddCopy var processed', 'var processed')
        changes.append('fix // resultAddCopy comment eating code')
    
    # Fix: 工具JS末尾多余 })(); 
    # 模式：某些调用();})();</script> 但不是addCopyBtns的 })();</script>
    # addCopyBtns的IIFE以 })();</script> 结尾是正确的
    # 工具JS以 })();</script> 结尾是错误的（因为工具JS没有IIFE开头）
    # 但这个很难自动区分，需要看上下文
    
    # 策略：如果 })();</script> 前面紧跟着的是函数调用（如 calc();, convert();），
    # 而不是 } （IIFE闭合），则去掉 })();
    # 更安全的方法：查找 xxx();})();</script> 模式，其中 xxx 是常见函数名
    pattern = r'(calc|convert|update|init|render|parse|format|generate|process|run)\(\);?\}\)\(\);?</script>'
    match = re.search(pattern, content)
    if match:
        # 去掉中间的 })();
        content = re.sub(
            r'((?:calc|convert|update|init|render|parse|format|generate|process|run)\(\);?)\}\)\(\);?</script>',
            r'\1</script>',
            content
        )
        changes.append(f'remove extra }})(); before </script>')
    
    if content != original:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        return changes
    return None

# 扫描所有EN版工具页面
en_tools_dir = 'en'
fixed = 0
errors = []

for tool_name in os.listdir(en_tools_dir):
    tool_path = os.path.join(en_tools_dir, tool_name, 'index.html')
    if not os.path.exists(tool_path):
        continue
    
    changes = fix_file(tool_path)
    if changes:
        fixed += 1
        status = '[DRY]' if dry_run else '[FIXED]'
        print(f"{status} {tool_path}: {', '.join(changes)}")

# Also fix CN version
cn_fix = fix_file('xirr-calculator/index.html')
if cn_fix:
    fixed += 1
    status = '[DRY]' if dry_run else '[FIXED]'
    print(f"{status} xirr-calculator/index.html: {', '.join(cn_fix)}")

print(f"\nTotal: {fixed} files {'would be ' if dry_run else ''}fixed")

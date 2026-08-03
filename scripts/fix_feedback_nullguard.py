#!/usr/bin/env python3
"""Fix dead feedback functions that reference non-existent DOM elements.

These functions are never called (no button triggers them) but reference
getElementById for elements that don't exist. Adding null guards prevents
potential JS errors if Google's renderer tries to execute them.
"""
import re
import os

# Files to fix
files = [
    'gpa-calculator/index.html',
    'compound-interest-calculator/index.html',
    'running-pace-calculator/index.html',
    'metronome-online/index.html',
    'token-estimator/index.html',
    'mac-address-lookup/index.html',
    'checksum-calculator/index.html',
]

# Pattern: toggleFeedback function without null guard
old_toggle = "function toggleFeedback(){const p=document.getElementById('feedback-panel');p.style.display=p.style.display==='none'?'block':'none';}"
new_toggle = "function toggleFeedback(){const p=document.getElementById('feedback-panel');if(!p)return;p.style.display=p.style.display==='none'?'block':'none';}"

# Pattern: submitFeedback - add null guards
old_submit_start = "function submitFeedback(){\nconst type=document.getElementById('feedback-type').value;"
new_submit_start = "function submitFeedback(){\nconst typeEl=document.getElementById('feedback-type');if(!typeEl)return;const type=typeEl.value;"

old_success = "document.getElementById('feedback-success').style.display='block';"
new_success = "var fs=document.getElementById('feedback-success');if(fs)fs.style.display='block';"

fixed = 0
for fpath in files:
    full_path = os.path.join('/home/chison/tools-site', fpath)
    if not os.path.exists(full_path):
        print(f"SKIP  {fpath}: not found")
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # Fix toggleFeedback
    if old_toggle in content:
        content = content.replace(old_toggle, new_toggle)
        changes.append('toggleFeedback null guard')
    elif "toggleFeedback" in content:
        # Try to find and fix variant
        content = re.sub(
            r"function toggleFeedback\(\)\{const p=document\.getElementById\('feedback-panel'\);p\.style\.display=",
            "function toggleFeedback(){const p=document.getElementById('feedback-panel');if(!p)return;p.style.display=",
            content
        )
        if content != original:
            changes.append('toggleFeedback null guard (regex)')
    
    # Fix submitFeedback start
    if old_submit_start in content:
        content = content.replace(old_submit_start, new_submit_start)
        changes.append('submitFeedback null guard')
    
    # Fix feedback-success
    if old_success in content:
        content = content.replace(old_success, new_success)
        changes.append('feedback-success null guard')
    
    if content != original:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"FIXED  {fpath}: {', '.join(changes)}")
        fixed += 1
    else:
        print(f"NOCHANGE  {fpath}")

print(f"\nTotal fixed: {fixed}/{len(files)}")

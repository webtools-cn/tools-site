#!/usr/bin/env python3
import re

with open('en/html-wysiwyg-editor/index.html', 'r') as f:
    content = f.read()

# Find the download function
old_start = "document.getElementById('downloadHtmlBtn').onclick=function(){var h=ism?se.value:ed.innerHTML;var f="
idx = content.find(old_start)
if idx == -1:
    print("Start marker not found")
    exit(1)

print(f"Found at index {idx}")

# Find the semicolon that ends the assignment (the `};` after the function body)
search_from = idx + len(old_start)
# The string starts after `var f=` - find the quote type
if search_from < len(content):
    quote = content[search_from]
    print(f"String delimiter: {repr(quote)}")
    
    # Find end of the entire function: document.getElementById('downloadHtmlBtn').onclick=function(){...};
    # Look for `};` followed by newline or `
    end_marker = "});"
    end_idx = content.find("});", idx)
    if end_idx == -1:
        print("End marker not found")
        exit(1)
    
    # Find the start of the full function call  
    func_start = idx
    func_end = end_idx + len("});")
    
    print(f"Function range: {func_start}-{func_end}")
    
    new_func = "document.getElementById('downloadHtmlBtn').onclick=function(){var h=ism?se.value:ed.innerHTML;var f='<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><title>My Content<\\/title><\\/head><body>'+h+'<\\/body><\\/html>';var b=new Blob([f],{type:'text/html'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='content.html';a.click();};"
    
    content = content[:func_start] + new_func + content[func_end:]
    
    with open('en/html-wysiwyg-editor/index.html', 'w') as f:
        f.write(content)
    print("Written successfully")

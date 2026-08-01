#!/usr/bin/env python3
"""
Fix HowTo/FAQ schemas that have messy tool names (Free Online, long dash suffixes, etc.)
Removes the old HowTo/FAQ schema and re-inserts with cleaned names.
"""
import os, re, json, sys

sys.path.insert(0, 'scripts')
from add_howto_faq_en_batch import (
    detect_category, HOWTO_STEPS, generate_tool_faqs,
    build_howto_schema, build_faq_schema, clean_tool_name, insert_schema
)

def extract_tool_info(content, slug):
    """Extract tool name and description from existing schema/meta tags"""
    sa_match = re.search(r'"SoftwareApplication".*?"name":\s*"([^"]+)"', content)
    raw_name = sa_match.group(1) if sa_match else slug.replace('-', ' ').title()
    tool_name = clean_tool_name(raw_name)
    desc_match = re.search(r'"SoftwareApplication".*?"description":\s*"([^"]+)"', content)
    description = desc_match.group(1) if desc_match else f"Free online {tool_name}"
    return tool_name, description

def has_messy_name(schema_str, schema_type):
    """Check if a schema has a messy tool name"""
    try:
        schema = json.loads(schema_str)
        name = schema.get('name', '')
        # Check for common mess patterns
        if 'Free Online' in name:
            return True
        if schema_type == 'HowTo' and re.search(r'\s*[-–|·]\s*\w+', name) and len(name) > 50:
            return True
        if schema_type == 'FAQ' and 'Free Online' in name:
            return True
        # Check for emoji
        if re.search(r'[^\w\s:]', name[:5]):
            return True
    except:
        pass
    return False

fixed_howto = 0
fixed_faq = 0
errors = 0

for slug in sorted(os.listdir('en')):
    filepath = f'en/{slug}/index.html'
    if not os.path.exists(filepath):
        continue
    with open(filepath) as f:
        content = f.read()
    if 'meta http-equiv="refresh"' in content or len(content) < 500:
        continue
    if slug in ('about', 'privacy', 'terms', 'contact'):
        continue
    
    modified = False
    
    # Check HowTo
    howto_matches = list(re.finditer(
        r'<script type="application/ld\+json">(\{"@context":"[^"]+","@type":"HowTo"[^<]+?)</script>',
        content
    ))
    for m in howto_matches:
        if has_messy_name(m.group(1), 'HowTo'):
            # Remove this schema block
            content = content[:m.start()] + content[m.end():]
            # Re-add with clean name
            tool_name, description = extract_tool_info(content, slug)
            category = detect_category(slug, tool_name)
            new_schema = build_howto_schema(tool_name, description, category)
            content, success = insert_schema(content, new_schema, 'HowTo')
            if success:
                fixed_howto += 1
                modified = True
            break  # Only fix first HowTo
    
    # Check FAQ
    faq_matches = list(re.finditer(
        r'<script type="application/ld\+json">(\{"@context":"[^"]+","@type":"FAQPage"[^<]+?)</script>',
        content
    ))
    for m in faq_matches:
        if has_messy_name(m.group(1), 'FAQ'):
            # Remove this schema block
            content = content[:m.start()] + content[m.end():]
            # Re-add with clean name
            tool_name, description = extract_tool_info(content, slug)
            category = detect_category(slug, tool_name)
            faqs = generate_tool_faqs(slug, tool_name, description, category)
            new_schema = build_faq_schema(tool_name, faqs)
            content, success = insert_schema(content, new_schema, 'FAQ')
            if success:
                fixed_faq += 1
                modified = True
            break  # Only fix first FAQ
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print(f'Fixed HowTo names: {fixed_howto}')
print(f'Fixed FAQ names: {fixed_faq}')
print(f'Errors: {errors}')

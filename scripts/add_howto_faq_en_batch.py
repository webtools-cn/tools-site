#!/usr/bin/env python3
"""
Batch add HowTo + FAQ Schema to EN pages that are missing them.
- HowTo: All real EN pages missing HowTo schema (~1240 pages)
- FAQ: All real EN pages missing FAQ schema (~828 pages)
Skips redirect/stub pages. Skips pages that already have the schema.
"""
import os, re, json, sys

# ─── Category detection (EN version) ────────────────────────────────────────

def detect_category(slug, name):
    """Detect tool category from slug and name"""
    s = slug.lower()
    n = name.lower()
    
    # Direct category matches
    for cat in ['calculator', 'converter', 'generator', 'checker', 'encoder', 'formatter', 'analyzer', 'editor', 'viewer', 'tester']:
        if cat in s or cat in n:
            return cat
    
    # Additional patterns
    if any(w in s for w in ['calc', 'compute', 'count']):
        return 'calculator'
    if any(w in s for w in ['convert', 'transform', 'translate']):
        return 'converter'
    if any(w in s for w in ['generate', 'create', 'make', 'builder']):
        return 'generator'
    if any(w in s for w in ['check', 'verify', 'validate', 'detect']):
        return 'checker'
    if any(w in s for w in ['encode', 'decode', 'encrypt', 'decrypt', 'hash']):
        return 'encoder'
    if any(w in s for w in ['format', 'beautify', 'minify', 'pretty']):
        return 'formatter'
    if any(w in s for w in ['analyz', 'inspect', 'monitor']):
        return 'analyzer'
    if any(w in s for w in ['edit', 'modify', 'design']):
        return 'editor'
    if any(w in s for w in ['view', 'render', 'display', 'visual']):
        return 'viewer'
    if any(w in s for w in ['test', 'benchmark', 'measure', 'speed']):
        return 'tester'
    if any(w in s for w in ['sort', 'filter', 'search', 'find']):
        return 'analyzer'
    if any(w in s for w in ['compare', 'diff']):
        return 'analyzer'
    if any(w in s for w in ['random', 'shuffle']):
        return 'generator'
    if any(w in s for w in ['play', 'player', 'recorder', 'record']):
        return 'editor'
    if any(w in s for w in ['download', 'export', 'import']):
        return 'converter'
    if any(w in s for w in ['color', 'gradient', 'shadow', 'border', 'animation']):
        return 'generator'
    if any(w in s for w in ['extract', 'split', 'merge', 'join', 'combine']):
        return 'converter'
    if any(w in s for w in ['compress', 'decompress', 'zip']):
        return 'converter'
    if any(w in s for w in ['remove', 'delete', 'clean', 'strip']):
        return 'formatter'
    if any(w in s for w in ['scan', 'lookup', 'query']):
        return 'checker'
    if any(w in s for w in ['draw', 'paint', 'sketch']):
        return 'editor'
    if any(w in s for w in ['schedule', 'plan', 'organize']):
        return 'generator'
    if any(w in s for w in ['log', 'trace', 'debug']):
        return 'viewer'
    
    return 'converter'  # default fallback

# ─── HowTo step templates (EN) ──────────────────────────────────────────────

HOWTO_STEPS = {
    'calculator': [
        ('Enter values', 'Input the numbers or values you want to calculate'),
        ('Set parameters', 'Choose calculation mode or adjust options if needed'),
        ('Click Calculate', 'Press the calculate button to get your result'),
        ('View results', 'Review the calculation output and copy if needed'),
    ],
    'converter': [
        ('Enter input', 'Type or paste the value you want to convert'),
        ('Select format', 'Choose the source and target format'),
        ('Click Convert', 'Press the convert button to perform the conversion'),
        ('Copy result', 'View the converted output and copy with one click'),
    ],
    'generator': [
        ('Set options', 'Configure generation parameters (count, format, range, etc.)'),
        ('Click Generate', 'Press the generate button to create your content'),
        ('Preview result', 'Review the generated output'),
        ('Copy or download', 'Copy the result to clipboard or download as a file'),
    ],
    'checker': [
        ('Enter data', 'Input or paste the content you want to check'),
        ('Click Check', 'Press the check button to start the analysis'),
        ('View report', 'Review the check results and detailed report'),
        ('Take action', 'Follow the suggestions or copy the report'),
    ],
    'encoder': [
        ('Enter content', 'Type or paste the text you want to encode or decode'),
        ('Choose direction', 'Select encode or decode operation'),
        ('Execute', 'Click the button to perform the encoding or decoding'),
        ('Copy result', 'View the output and copy to clipboard'),
    ],
    'formatter': [
        ('Paste content', 'Paste the code or text you want to format'),
        ('Set style', 'Choose formatting options (indent size, line breaks, etc.)'),
        ('Click Format', 'Press the format button to process your input'),
        ('Copy output', 'Review the formatted result and copy it'),
    ],
    'analyzer': [
        ('Enter content', 'Input or paste the data you want to analyze'),
        ('Click Analyze', 'Press the analyze button to start processing'),
        ('View results', 'Review the analysis results and statistics'),
        ('Export data', 'Copy or download the analysis output'),
    ],
    'editor': [
        ('Enter content', 'Type or paste your content into the editor'),
        ('Edit and modify', 'Use the toolbar or controls to make changes'),
        ('Preview live', 'See real-time preview of your changes'),
        ('Export result', 'Copy or download the edited content'),
    ],
    'viewer': [
        ('Upload or paste', 'Upload a file or paste content to view'),
        ('Browse content', 'Explore the content and details'),
        ('Analyze', 'Review any automatically generated analysis'),
        ('Export', 'Copy or download the results'),
    ],
    'tester': [
        ('Prepare test', 'Enter test parameters or upload test data'),
        ('Start test', 'Click the start button to run the test'),
        ('View results', 'Review the test results and detailed data'),
        ('Copy report', 'Copy or download the test report'),
    ],
}

# ─── FAQ templates per category ─────────────────────────────────────────────

def generate_tool_faqs(slug, tool_name, description, category):
    """Generate 3 category-specific FAQs for a tool"""
    faqs = []
    
    # FAQ 1: What is / How does it work
    if category == 'calculator':
        faqs.append({
            "question": f"How does the {tool_name} work?",
            "answer": f"Enter your values into the input fields, adjust any parameters, and click Calculate. The tool processes your input instantly and displays accurate results. All calculations happen locally in your browser for privacy and speed."
        })
    elif category == 'converter':
        faqs.append({
            "question": f"How do I use the {tool_name}?",
            "answer": f"Enter or paste your input value, select the source and target formats, then click Convert. The result appears instantly. All conversions run locally in your browser — no data is sent to any server."
        })
    elif category == 'generator':
        faqs.append({
            "question": f"How does the {tool_name} work?",
            "answer": f"Configure your options (quantity, format, range, etc.), then click Generate. The tool creates your content instantly in the browser. You can preview, copy, or download the results."
        })
    elif category == 'checker':
        faqs.append({
            "question": f"How does the {tool_name} check work?",
            "answer": f"Enter or paste the content you want to check, then click the Check button. The tool analyzes your input and provides a detailed report with findings and suggestions. All processing happens locally in your browser."
        })
    elif category == 'encoder':
        faqs.append({
            "question": f"Is the {tool_name} free and secure?",
            "answer": f"Yes, this tool is completely free and all encoding/decoding happens locally in your browser. Your data is never uploaded to any server, ensuring full privacy and security."
        })
    elif category == 'formatter':
        faqs.append({
            "question": f"How do I use the {tool_name}?",
            "answer": f"Paste your code or text into the input area, select your formatting preferences, and click Format. The tool instantly reformats your content according to the selected style. All processing is done locally."
        })
    elif category == 'analyzer':
        faqs.append({
            "question": f"What does the {tool_name} analyze?",
            "answer": f"Enter or paste your data, click Analyze, and the tool provides detailed statistics, patterns, and insights. All analysis runs locally in your browser for instant results and data privacy."
        })
    elif category == 'editor':
        faqs.append({
            "question": f"How do I use the {tool_name}?",
            "answer": f"Enter or paste your content, use the editing controls to make changes, and preview results in real time. When done, copy or download the output. Everything runs locally in your browser."
        })
    elif category == 'viewer':
        faqs.append({
            "question": f"What file formats does the {tool_name} support?",
            "answer": f"Upload or paste your content to view it with detailed analysis. The tool processes everything locally in your browser, so your data stays private. Results can be copied or downloaded."
        })
    elif category == 'tester':
        faqs.append({
            "question": f"How accurate is the {tool_name}?",
            "answer": f"The tool provides precise test results by processing your input locally in the browser. Enter your test parameters, run the test, and review the detailed report. No data is sent to external servers."
        })
    else:
        faqs.append({
            "question": f"How do I use the {tool_name}?",
            "answer": f"Enter your input, configure any options, and click the action button. Results appear instantly. All processing happens locally in your browser for speed and privacy."
        })
    
    # FAQ 2: Privacy / Security / Free
    faqs.append({
        "question": f"Is the {tool_name} free to use?",
        "answer": f"Yes, this tool is completely free with no signup required. All processing happens locally in your browser — your data is never uploaded to any server, ensuring complete privacy and security."
    })
    
    # FAQ 3: Accuracy / Technical question based on category
    if category == 'calculator':
        faqs.append({
            "question": f"Are the {tool_name} results accurate?",
            "answer": f"Yes, the calculator uses standard mathematical formulas and algorithms to ensure accurate results. Calculations are performed using JavaScript's built-in precision. For financial or medical decisions, always verify with a professional."
        })
    elif category == 'converter':
        faqs.append({
            "question": f"Is there a file size limit for the {tool_name}?",
            "answer": f"Since all conversions happen locally in your browser, the limit depends on your device's memory. Most typical inputs are processed instantly. Very large files may take longer but will still work without server upload."
        })
    elif category == 'generator':
        faqs.append({
            "question": f"Can I customize the output from the {tool_name}?",
            "answer": f"Yes, the generator offers various options to customize the output including format, quantity, and style parameters. Adjust the settings before clicking Generate to get results that match your needs."
        })
    elif category == 'checker':
        faqs.append({
            "question": f"What does the {tool_name} report include?",
            "answer": f"The report includes a detailed analysis of your input with specific findings, severity levels, and actionable suggestions. All checks run locally in your browser for instant, private results."
        })
    elif category == 'encoder':
        faqs.append({
            "question": f"What encoding formats does the {tool_name} support?",
            "answer": f"The tool supports standard encoding and decoding formats. All operations are performed locally in your browser using well-established algorithms, ensuring both accuracy and privacy."
        })
    elif category == 'formatter':
        faqs.append({
            "question": f"Does the {tool_name} change my code's functionality?",
            "answer": f"No, the formatter only changes the visual layout and style of your code (indentation, spacing, line breaks). The logic and functionality remain exactly the same. All formatting is done locally in your browser."
        })
    elif category == 'analyzer':
        faqs.append({
            "question": f"Can I export the analysis results from the {tool_name}?",
            "answer": f"Yes, you can copy the analysis results to clipboard or download them. All analysis is performed locally in your browser, so your data never leaves your device."
        })
    elif category == 'editor':
        faqs.append({
            "question": f"Does the {tool_name} save my data?",
            "answer": f"No, the tool does not save or send your data anywhere. All editing happens locally in your browser. When you close the page, your data is gone. Copy or download your work before leaving."
        })
    elif category == 'viewer':
        faqs.append({
            "question": f"Is my data safe with the {tool_name}?",
            "answer": f"Absolutely. All processing happens locally in your browser — your files and data are never uploaded to any server. When you close the tab, all data is automatically cleared from memory."
        })
    elif category == 'tester':
        faqs.append({
            "question": f"Can I use the {tool_name} on mobile devices?",
            "answer": f"Yes, the tool is fully responsive and works on any device with a modern browser. All testing runs locally, so you get the same accuracy and privacy on mobile as on desktop."
        })
    else:
        faqs.append({
            "question": f"Does the {tool_name} work on mobile?",
            "answer": f"Yes, the tool works on any device with a modern web browser. All processing happens locally, so it works offline once loaded and keeps your data private."
        })
    
    return faqs

# ─── Schema builders ────────────────────────────────────────────────────────

def build_howto_schema(tool_name, description, category):
    """Build HowTo JSON-LD schema string"""
    steps = HOWTO_STEPS.get(category, HOWTO_STEPS['converter'])
    
    step_objects = []
    for i, (name, text) in enumerate(steps, 1):
        step_objects.append({
            "@type": "HowToStep",
            "position": i,
            "name": name,
            "text": text
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"How to Use {tool_name}",
        "description": f"Step-by-step guide for using {tool_name}",
        "totalTime": "PT1M",
        "tool": {
            "@type": "HowToTool",
            "name": tool_name
        },
        "step": step_objects
    }
    
    # Compact JSON (no pretty-print, like existing schemas)
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

def build_faq_schema(tool_name, faqs):
    """Build FAQPage JSON-LD schema string"""
    entities = []
    for faq in faqs:
        entities.append({
            "@type": "Question",
            "name": faq["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq["answer"]
            }
        })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "name": f"{tool_name} FAQ",
        "mainEntity": entities
    }
    
    return json.dumps(schema, ensure_ascii=False, separators=(',', ':'))

# ─── Extract tool info from HTML ────────────────────────────────────────────

def clean_tool_name(name):
    """Clean tool name by removing common suffixes and prefixes"""
    # Remove "Free Online" prefix
    name = re.sub(r'^Free Online\s+', '', name)
    # Remove " - ..." suffix (descriptive taglines)
    name = re.sub(r'\s*[-–|·]\s*Free Online.*$', '', name)
    name = re.sub(r'\s*[-–|·]\s*Online.*$', '', name)
    name = re.sub(r'\s*[-–|·]\s*Free.*$', '', name)
    # Remove " | ToolBase" suffix
    name = re.sub(r'\s*\|\s*ToolBase\s*$', '', name)
    name = re.sub(r'\s*\|\s*Free Online.*$', '', name)
    # Remove " - Merged" suffix
    name = re.sub(r'\s*-\s*Merged\s*$', '', name)
    # Remove emoji prefixes
    name = re.sub(r'^[^\w\s]+\s*', '', name)
    # Remove trailing "Tool" if it's redundant
    # name = re.sub(r'\s+Tool$', '', name)
    return name.strip()

def extract_tool_info(content, slug):
    """Extract tool name and description from existing schema/meta tags"""
    # Try SoftwareApplication name
    sa_match = re.search(r'"SoftwareApplication".*?"name":\s*"([^"]+)"', content)
    raw_name = sa_match.group(1) if sa_match else slug.replace('-', ' ').title()
    
    # Clean the name
    tool_name = clean_tool_name(raw_name)
    
    # Try SoftwareApplication description
    desc_match = re.search(r'"SoftwareApplication".*?"description":\s*"([^"]+)"', content)
    description = desc_match.group(1) if desc_match else f"Free online {tool_name}"
    
    return tool_name, description

# ─── Insert schema into HTML ────────────────────────────────────────────────

def insert_schema(content, schema_json, schema_type):
    """Insert a JSON-LD schema into the HTML content.
    
    Strategy:
    1. Try to insert after the last </script> that contains ld+json before </head>
    2. Fallback: insert before </head>
    """
    script_tag = f'<script type="application/ld+json">{schema_json}</script>'
    
    # Find </head> position
    head_end = content.find('</head>')
    if head_end == -1:
        # No </head>, try before </body>
        body_end = content.find('</body>')
        if body_end == -1:
            return content, False
        content = content[:body_end] + '\n' + script_tag + '\n' + content[body_end:]
        return content, True
    
    # Find the last ld+json script before </head>
    last_json_end = -1
    search_pos = 0
    while True:
        match = content.find('</script>', search_pos, head_end)
        if match == -1:
            break
        # Check if this </script> closes an ld+json block
        # Look backwards for the opening
        before = content[max(0, match-500):match+9]
        if 'application/ld+json' in before:
            last_json_end = match + 9  # After </script>
        search_pos = match + 9
    
    if last_json_end > 0:
        # Insert after the last ld+json script
        content = content[:last_json_end] + '\n' + script_tag + '\n' + content[last_json_end:]
    else:
        # No ld+json found before </head>, insert before </head>
        content = content[:head_end] + script_tag + '\n' + content[head_end:]
    
    return content, True

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    howto_added = 0
    howto_skipped = 0
    faq_added = 0
    faq_skipped = 0
    errors = 0
    category_stats = {}
    
    # Process all EN pages
    en_dir = 'en'
    entries = sorted(os.listdir(en_dir))
    
    for i, entry in enumerate(entries):
        filepath = os.path.join(en_dir, entry, 'index.html')
        if not os.path.exists(filepath):
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip redirect/stub pages
            if 'meta http-equiv="refresh"' in content or len(content) < 500:
                continue
            
            # Skip "about" and other non-tool pages
            if entry in ('about', 'privacy', 'terms', 'contact'):
                continue
            
            # Extract tool info
            tool_name, description = extract_tool_info(content, entry)
            category = detect_category(entry, tool_name)
            
            modified = False
            
            # Check and add HowTo
            if '"HowTo"' not in content:
                howto_json = build_howto_schema(tool_name, description, category)
                content, success = insert_schema(content, howto_json, 'HowTo')
                if success:
                    howto_added += 1
                    modified = True
                    category_stats[category] = category_stats.get(category, 0) + 1
                else:
                    howto_skipped += 1
            else:
                howto_skipped += 1
            
            # Check and add FAQ
            if '"FAQPage"' not in content:
                faqs = generate_tool_faqs(entry, tool_name, description, category)
                faq_json = build_faq_schema(tool_name, faqs)
                content, success = insert_schema(content, faq_json, 'FAQ')
                if success:
                    faq_added += 1
                    modified = True
            else:
                faq_skipped += 1
            
            # Write back if modified
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Progress
            if (i + 1) % 200 == 0:
                print(f'Progress: {i+1}/{len(entries)} | HowTo added: {howto_added} | FAQ added: {faq_added}')
                
        except Exception as e:
            errors += 1
            print(f'Error processing {filepath}: {e}', file=sys.stderr)
    
    # Summary
    print('\n' + '='*60)
    print('BATCH SCHEMA ADDITION COMPLETE')
    print('='*60)
    print(f'HowTo Schema added: {howto_added}')
    print(f'HowTo Schema skipped (already exists): {howto_skipped}')
    print(f'FAQ Schema added: {faq_added}')
    print(f'FAQ Schema skipped (already exists): {faq_skipped}')
    print(f'Errors: {errors}')
    print(f'\nHowTo by category:')
    for cat, count in sorted(category_stats.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {count}')

if __name__ == '__main__':
    main()

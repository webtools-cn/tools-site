#!/usr/bin/env python3
"""Fix EN meta descriptions - handle the broken >> pattern."""
import os

# Map: slug -> (old_pattern_in_file, new_full_desc)
# EN pages with broken desc
en_fixes = {
    'en/jensen-alpha-calculator': 'Free online Jensen\'s Alpha calculator to evaluate portfolio excess returns above market benchmarks. Input actual return, risk-free rate, market return and beta to measure active fund manager performance. Essential tool for investment portfolio analysis and finance education. Pure client-side computation, no registration required.',
    'en/ohms-law-calculator': 'Free online Ohm\'s Law calculator to compute voltage, current, resistance and power in electrical circuits. Simply enter any two known electrical values to solve for the remaining two using V=IR and P=VI formulas. Essential for electronics students, Arduino hobbyists and circuit design. Browser-local processing, no data upload.',
    'en/conways-game-of-life': 'Free online Conway\'s Game of Life cellular automaton simulator. Watch fascinating patterns emerge from simple mathematical rules — gliders, oscillators and spaceships evolve in real-time. Customize the grid size, seed initial patterns and control simulation speed. Great for computer science education and mathematical exploration. No registration needed.',
    'en/pet-food-calculator': 'Free online pet food calculator to determine daily feeding portions for dogs and cats based on weight, activity level and calorie needs. Enter your pet\'s details to get personalized daily food recommendations. Helps prevent pet obesity and ensure balanced nutrition. Pure client-side calculation, no registration required.',
    'en/tip-calculator-by-country': 'Free online international tip calculator with tipping customs for 50+ countries worldwide. Calculate appropriate tips based on local dining norms — from US 15-20% to Japan\'s no-tipping culture. Split restaurant bills among multiple diners. Perfect for international travelers and global business meals. No registration needed.',
    'en/voice-to-text': 'Free online voice-to-text speech recognition tool using your browser\'s built-in Web Speech API. Click and speak to convert your spoken words into written text in real-time. Supports multiple languages and continuous dictation mode. Perfect for quick note-taking, drafting emails and accessibility needs. Your voice data never leaves your browser.',
    'en/cat-age-calculator': 'Cat Age Calculator — accurately convert your cat\'s real age to human equivalent years using veterinary science-based formulas. Accounts for rapid feline development in the first two years versus gradual aging afterward. Understand your cat\'s life stage, behavior and health needs at every age. No registration required, 100% browser-based.',
    'en/college-savings-calculator': 'Free College Savings Calculator to plan your child\'s education fund with inflation-adjusted projections. Estimate four-year total costs including tuition, housing and living expenses. Calculate the monthly savings needed to reach your 529 plan or education savings goal. Essential for parents planning college funding strategy.',
    'en/child-height-predictor': 'Online child height predictor to estimate your child\'s future adult height using the mid-parental height formula. Enter both parents\' heights plus child\'s current age, gender and height for a science-based prediction. Helpful for pediatric growth monitoring and understanding genetic height potential. Pure browser, no data upload.',
    'en/gratitude-journal': 'Free online gratitude journal to practice daily positive thinking and mindfulness. Write three things you\'re grateful for each day, track your happiness streaks and reflect on positive moments. Backed by positive psychology research on well-being improvement. All entries stored locally in your browser for complete privacy.',
    'en/cat-calorie-calculator': 'Free online cat calorie calculator to determine your cat\'s ideal daily calorie intake for weight management. Calculate Resting Energy Requirement (RER) based on weight, life stage and body condition score. Supports weight loss, maintenance and growth feeding plans. Veterinary nutrition science-based, pure browser computation.',
    'en/chronotype-quiz': 'Free chronotype quiz to discover your natural sleep-wake biological rhythm. Answer science-based questions about your energy levels, productivity peaks and sleep preferences to determine if you\'re a Morning Lark, Night Owl, Hummingbird or Bear chronotype. Optimize your daily schedule around your natural body clock for better health.',
    'en/dog-calorie-calculator': 'Free online dog calorie calculator to determine your dog\'s daily calorie needs based on weight, breed size, age and activity level. Calculate Resting Energy Requirement (RER) and Daily Energy Requirement (DER) for puppies, adult and senior dogs. Supports weight management and healthy feeding plans. Pure browser, no registration.',
    'en/burn-rate-calculator': 'Free online startup Burn Rate Calculator to analyze your company\'s cash burn and financial runway. Calculate gross burn rate, net burn rate and estimate how many months of cash runway remain before next fundraising round. Essential tool for startup founders, CFOs and investor reporting. Pure client-side, no registration needed.',
    'en/password-pwned-checker': 'Free online password breach checker that uses k-anonymity to securely verify if your passwords have been exposed in known data breaches. Only a partial hash prefix is sent to the HaveIBeenPwned API — your full password never leaves your browser. Stay safe online without compromising your credentials.',
    'en/graham-number-calculator': 'Free online Graham Number Calculator based on Benjamin Graham\'s value investing formula. Input Earnings Per Share (EPS) and Book Value Per Share to calculate the maximum price a defensive investor should pay for a stock. Essential tool for value investors and fundamental stock analysis. No registration required.',
    'en/car-depreciation-calculator': 'Free online car depreciation calculator to estimate your vehicle\'s resale value over time. Model future depreciation using industry-standard curves accounting for vehicle make, model, age, mileage and condition. Compare new versus used car value retention rates. Essential for car buyers planning total ownership costs.',
    'en/business-valuation-calculator': 'Free online business valuation calculator to estimate your company\'s worth using multiple valuation methods. Calculate business value using revenue multiples, EBITDA multiples, discounted cash flow and asset-based approaches. Essential for entrepreneurs planning exit strategies, fundraising and M&A discussions. No registration required.',
    'en/link-preview': 'Free online link preview tool to check how any URL appears when shared on social media platforms. Enter a URL to preview the webpage title, description, image thumbnail and Open Graph meta tags. Test how your content looks on Facebook, Twitter, LinkedIn before publishing. Pure browser-based, no registration needed.',
    'en/nps-calculator': 'Free online NPS (National Pension System) Calculator for India retirement planning. Estimate your retirement corpus from NPS contributions and projected returns. Calculate monthly pension amounts, lump-sum withdrawal options and tax benefits under Section 80CCD. Essential for Indian employees planning retirement through the NPS scheme.',
}

for slug, new_desc in en_fixes.items():
    path = f'./{slug}/index.html'
    if not os.path.exists(path):
        print(f'  SKIP: {path}')
        continue
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find description line with pattern
    import re
    # Find the line containing the meta description
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '<meta name="description"' in line:
            old_line = line
            indent = line[:len(line) - len(line.lstrip())]
            new_line = f'{indent}<meta name="description" content="{new_desc}">'
            lines[i] = new_line
            break
    
    new_content = '\n'.join(lines)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    print(f'  OK: {slug} [{len(new_desc)}]')

print('\nAll EN pages fixed!')
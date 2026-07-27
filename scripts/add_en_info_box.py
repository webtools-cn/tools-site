#!/usr/bin/env python3
"""给EN页面补充英文info-box"""
import os

BASE = '/home/chison/tools-site'

EN_INFO = {
    'cocktail-recipe-generator': '''<div class="info-box">
      <h2>📖 Cocktail Base Spirits Guide</h2>
      <ul>
        <li><strong>Vodka</strong>: Neutral and versatile, perfect for Moscow Mule, Cosmopolitan, Bloody Mary</li>
        <li><strong>Gin</strong>: Juniper-forward with herbal notes. Classics: Martini, Gin & Tonic, Negroni</li>
        <li><strong>Rum</strong>: Sugarcane-based, sweet and smooth. White rum for Mojito/Daiquiri, dark rum for Dark 'n' Stormy</li>
        <li><strong>Tequila</strong>: Agave spirit from Mexico. Stars in Margarita, Tequila Sunrise, Paloma</li>
        <li><strong>Whiskey</strong>: Grain-based, complex. Essential for Old Fashioned, Manhattan, Whiskey Sour</li>
        <li><strong>Brandy</strong>: Distilled from wine, elegant fruity notes. Try Sidecar, Alexander, Mimosa</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ FAQ</h2>
      <p><strong>Q: What's the best cocktail for beginners?</strong></p>
      <p>A: Mojito and Gin & Tonic are great starters — few ingredients, forgiving ratios, and refreshing taste.</p>
      <p><strong>Q: Can I make cocktails without professional tools?</strong></p>
      <p>A: Absolutely. Use a jar with lid as a shaker, a chopstick as a stirrer, and any glass will work. The key is using enough ice and following the ratios.</p>
    </div>''',

    'ingredient-substitute-finder': '''<div class="info-box">
      <h2>📖 Common Ingredient Substitutions</h2>
      <ul>
        <li><strong>Egg substitute</strong>: 1 egg = 1/4 cup applesauce OR 1 tbsp flaxseed meal + 3 tbsp water (baking)</li>
        <li><strong>Butter substitute</strong>: 1 cup butter = 1 cup coconut oil OR 3/4 cup vegetable oil</li>
        <li><strong>Milk substitute</strong>: 1 cup milk = 1 cup soy/almond/oat milk (cooking & baking)</li>
        <li><strong>Flour substitute</strong>: 1 cup all-purpose = 1 cup whole wheat OR 7/8 cup rice flour (gluten-free)</li>
        <li><strong>Sugar substitute</strong>: 1 cup white sugar = 3/4 cup honey (reduce liquid) OR 1 cup coconut sugar</li>
        <li><strong>Cream substitute</strong>: 1 cup cream = 1 cup coconut milk (chilled, scoop solid part) OR Greek yogurt</li>
      </ul>
    </div>
    <div class="info-box">
      <h2>❓ FAQ</h2>
      <p><strong>Q: Will substitutions affect the taste?</strong></p>
      <p>A: Slightly. Similar-category swaps (e.g., different oils) have minimal impact. Cross-category swaps (e.g., applesauce for eggs) change both texture and flavor.</p>
      <p><strong>Q: When should I avoid substituting?</strong></p>
      <p>A: Avoid major substitutions in structurally demanding recipes like macarons or soufflés. Everyday cooking and simple baking are very forgiving.</p>
    </div>''',
}

for tool, info_html in EN_INFO.items():
    fpath = os.path.join(BASE, 'en', tool, 'index.html')
    with open(fpath) as f:
        content = f.read()
    
    if 'class="info-box"' in content:
        print(f"⏭️  en:{tool} — 已有info-box")
        continue
    
    content = content.replace('</main>', f'\n{info_html}\n</main>')
    with open(fpath, 'w') as f:
        f.write(content)
    print(f"✅ en:{tool} — 已添加英文info-box")
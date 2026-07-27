#!/usr/bin/env python3
"""Fix EN versions - regenerate clean English pages"""
import os

TOOLS = {
    "glycemic-index-lookup": {
        "en_title": "Glycemic Index Lookup",
        "en_desc": "Free online Glycemic Index (GI) lookup tool. Search over 300 common foods for their glycemic index and glycemic load (GL) values. Helps diabetics and health-conscious eaters make informed food choices. Pure frontend local search, data never uploaded.",
        "en_keywords": "glycemic index lookup,GI lookup,glycemic load,food GI,diabetes diet,low GI foods",
        "category": "Health",
        "icon": "🩸",
        "en_header": "Glycemic Index Lookup",
        "hero_text": "Free online Glycemic Index (GI) lookup tool. Search over 300 common foods for their glycemic index and glycemic load (GL) values. Helps diabetics and health-conscious eaters make informed food choices. Pure frontend local search, data never uploaded.",
        "input_html": '<div class="form-group"><label>🔍 Search Food Name</label><input type="text" id="food-search" placeholder="Enter food name, e.g.: white rice, apple, whole wheat bread..."></div><div class="form-row"><div class="form-group"><label>📂 Food Category</label><select id="food-category"><option value="all">All</option><option value="grain">Grains</option><option value="fruit">Fruits</option><option value="vegetable">Vegetables</option><option value="dairy">Dairy</option><option value="snack">Snacks & Drinks</option><option value="meat">Meat & Protein</option></select></div></div><button class="btn btn-primary" onclick="searchFood()">🔍 Lookup Glycemic Index</button><div id="food-list" style="margin-top:12px;max-height:400px;overflow-y:auto"></div>',
        "instructions": '<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2"><li>Enter a food name in the search box</li><li>Or filter by food category</li><li>View the GI and GL values</li><li>GI≤55 = Low, 56-69 = Medium, ≥70 = High</li></ol>',
        "knowledge": '<ul class="info-list"><li>Low GI (≤55)<span class="info-val">Best choice</span></li><li>Medium GI (56-69)<span class="info-val">Eat moderately</span></li><li>High GI (≥70)<span class="info-val">Limit intake</span></li><li>GL = GI × Carbs ÷ 100<span class="info-val">More accurate</span></li></ul>',
        "js": 'var giData=[{"name":"White Rice","gi":73,"gl":29,"cat":"grain"},{"name":"Brown Rice","gi":50,"gl":16,"cat":"grain"},{"name":"Whole Wheat Bread","gi":51,"gl":12,"cat":"grain"},{"name":"White Bread","gi":75,"gl":15,"cat":"grain"},{"name":"Steamed Bun","gi":88,"gl":35,"cat":"grain"},{"name":"Noodles (boiled)","gi":55,"gl":14,"cat":"grain"},{"name":"Oatmeal","gi":55,"gl":12,"cat":"grain"},{"name":"Corn","gi":52,"gl":10,"cat":"grain"},{"name":"Millet Porridge","gi":72,"gl":5,"cat":"grain"},{"name":"Buckwheat Noodles","gi":54,"gl":11,"cat":"grain"},{"name":"Apple","gi":36,"gl":6,"cat":"fruit"},{"name":"Banana","gi":51,"gl":13,"cat":"fruit"},{"name":"Watermelon","gi":72,"gl":5,"cat":"fruit"},{"name":"Orange","gi":43,"gl":5,"cat":"fruit"},{"name":"Grapes","gi":59,"gl":11,"cat":"fruit"},{"name":"Mango","gi":51,"gl":8,"cat":"fruit"},{"name":"Kiwi","gi":50,"gl":7,"cat":"fruit"},{"name":"Strawberry","gi":40,"gl":1,"cat":"fruit"},{"name":"Blueberry","gi":53,"gl":5,"cat":"fruit"},{"name":"Cherry","gi":22,"gl":3,"cat":"fruit"},{"name":"Carrot","gi":39,"gl":2,"cat":"vegetable"},{"name":"Potato (boiled)","gi":78,"gl":13,"cat":"vegetable"},{"name":"Sweet Potato","gi":54,"gl":11,"cat":"vegetable"},{"name":"Pumpkin","gi":75,"gl":3,"cat":"vegetable"},{"name":"Broccoli","gi":10,"gl":0,"cat":"vegetable"},{"name":"Spinach","gi":15,"gl":0,"cat":"vegetable"},{"name":"Tomato","gi":30,"gl":1,"cat":"vegetable"},{"name":"Cucumber","gi":15,"gl":0,"cat":"vegetable"},{"name":"Milk","gi":27,"gl":3,"cat":"dairy"},{"name":"Yogurt","gi":35,"gl":5,"cat":"dairy"},{"name":"Ice Cream","gi":61,"gl":13,"cat":"dairy"},{"name":"Cheese","gi":0,"gl":0,"cat":"dairy"},{"name":"Coca-Cola","gi":63,"gl":16,"cat":"snack"},{"name":"Chocolate","gi":49,"gl":12,"cat":"snack"},{"name":"Potato Chips","gi":56,"gl":9,"cat":"snack"},{"name":"Cake","gi":54,"gl":15,"cat":"snack"},{"name":"Cookies","gi":69,"gl":13,"cat":"snack"},{"name":"Honey","gi":61,"gl":12,"cat":"snack"},{"name":"Chicken Breast","gi":0,"gl":0,"cat":"meat"},{"name":"Eggs","gi":0,"gl":0,"cat":"meat"},{"name":"Salmon","gi":0,"gl":0,"cat":"meat"},{"name":"Tofu","gi":15,"gl":1,"cat":"meat"},{"name":"Soy Milk","gi":34,"gl":2,"cat":"meat"}];function searchFood(){var s=document.getElementById("food-search").value.toLowerCase();var c=document.getElementById("food-category").value;var r=giData.filter(function(f){var m=f.name.toLowerCase().indexOf(s)>-1||f.cat.indexOf(s)>-1;if(c!=="all")m=m&&f.cat===c;return m});var h="";if(r.length===0){h=\'<div style="text-align:center;padding:20px;color:#64748b">No matching foods found</div>\'}else{r.forEach(function(f){var gl=parseFloat(f.gl);var glLabel=gl<10?"Low":"Med";var gi=parseInt(f.gi);var giLabel=gi<=55?"Low":gi<=69?"Medium":"High";var giColor=gi<=55?"#22c55e":gi<=69?"#f59e0b":"#ef4444";h+=\'<div class="result-card" style="margin-bottom:8px"><div style="display:flex;justify-content:space-between;align-items:center"><div><strong>\'+f.name+\'</strong><div class="range">Category: \'+f.cat+\'</div></div><div style="text-align:right"><div class="value" style="font-size:1.2rem;color:\'+giColor+\'">GI: \'+f.gi+\' (\'+giLabel+\')</div><div class="range">GL: \'+f.gl+\' (\'+glLabel+\')</div></div></div></div>\'})}document.getElementById("food-list").innerHTML=h;document.getElementById("main-result").textContent=r.length>0?"Found "+r.length+" foods":"Not found";document.getElementById("detail-area").innerHTML=""}searchFood();'
    },
    "calorie-density-calculator": {
        "en_title": "Calorie Density Calculator",
        "en_desc": "Free online calorie density calculator. Enter food calories and weight to automatically calculate calorie density (cal/g). Helps with weight management and healthy eating. Supports metric/imperial units. Pure frontend local calculation.",
        "en_keywords": "calorie density calculator,food calorie density,calorie per gram,weight loss diet,calorie control",
        "category": "Health",
        "icon": "🍎",
        "en_header": "Calorie Density Calculator",
        "hero_text": "Free online calorie density calculator. Enter food calories and weight to automatically calculate calorie density (cal/g). Helps with weight management and healthy eating. Supports metric/imperial units. Pure frontend local calculation.",
        "input_html": '<div class="form-row"><div class="form-group"><label>🔥 Food Calories (kcal)</label><input type="number" id="calories" placeholder="e.g.: 250" min="0" step="1"></div><div class="form-group"><label>⚖️ Food Weight</label><input type="number" id="weight" placeholder="e.g.: 200" min="0.1" step="0.1"></div></div><div class="form-group"><label>📏 Weight Unit</label><select id="unit"><option value="g">Grams (g)</option><option value="oz">Ounces (oz)</option><option value="lb">Pounds (lb)</option></select></div><button class="btn btn-primary" onclick="calcDensity()">📊 Calculate Calorie Density</button><div id="density-result" style="margin-top:12px"></div>',
        "instructions": '<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2"><li>Enter total food calories (kcal)</li><li>Enter food weight</li><li>Select weight unit (g/oz/lb)</li><li>Click calculate to see calorie density</li><li>Density < 1 cal/g = low density food</li></ol>',
        "knowledge": '<ul class="info-list"><li>Very Low < 0.6<span class="info-val">Vegetables & Fruits</span></li><li>Low 0.6-1.5<span class="info-val">Grains & Legumes</span></li><li>Medium 1.5-4.0<span class="info-val">Meat & Dairy</span></li><li>High > 4.0<span class="info-val">Oils & Nuts</span></li></ul>',
        "js": 'function calcDensity(){var c=parseFloat(document.getElementById("calories").value);var w=parseFloat(document.getElementById("weight").value);var u=document.getElementById("unit").value;if(isNaN(c)||isNaN(w)||w<=0){document.getElementById("density-result").innerHTML=\'<div style="color:#ef4444;padding:12px">Please enter valid calorie and weight values</div>\';return}if(u==="oz")w=w*28.35;if(u==="lb")w=w*453.592;var d=c/w;var level=d<0.6?"Very Low":d<1.5?"Low":d<4?"Medium":"High";var color=d<0.6?"#22c55e":d<1.5?"#f59e0b":d<4?"#f97316":"#ef4444";document.getElementById("density-result").innerHTML=\'<div class="result-card"><div class="value" style="color:\'+color+\'">\'+d.toFixed(2)+\' cal/g</div><div class="label">Calorie Density: <span style="color:\'+color+\'">\'+level+\'</span></div><div class="range">\'+c+\' kcal / \'+w.toFixed(1)+\' g</div></div>\';document.getElementById("main-result").textContent=d.toFixed(2)+" cal/g";document.getElementById("detail-area").innerHTML=\'<div class="health-tip">💡 Lower calorie density means larger food volume and better satiety. For weight loss, choose foods with density < 1.5 cal/g.</div>\'}'
    },
    "time-and-a-half-calculator": {
        "en_title": "Time and a Half Calculator",
        "en_desc": "Free online overtime pay calculator. Enter your regular hourly rate and overtime hours to automatically calculate time-and-a-half pay. Supports various overtime rates (1.5x, 2x, 3x). Helps workers verify overtime earnings. Pure frontend local calculation.",
        "en_keywords": "time and a half calculator,overtime pay calculator,overtime rate,hourly wage,overtime earnings",
        "category": "Finance",
        "icon": "💰",
        "en_header": "Time and a Half Calculator",
        "hero_text": "Free online overtime pay calculator. Enter your regular hourly rate and overtime hours to automatically calculate time-and-a-half pay. Supports various overtime rates (1.5x, 2x, 3x). Helps workers verify overtime earnings.",
        "input_html": '<div class="form-row"><div class="form-group"><label>💵 Hourly Rate ($)</label><input type="number" id="hourly-rate" placeholder="e.g.: 20" min="0" step="0.01"></div><div class="form-group"><label>⏱️ Overtime Hours</label><input type="number" id="overtime-hours" placeholder="e.g.: 10" min="0" step="0.5"></div></div><div class="form-group"><label>📈 Overtime Rate</label><select id="overtime-rate"><option value="1.5">1.5x (Time and a Half)</option><option value="2">2x (Double Time)</option><option value="2.5">2.5x</option><option value="3">3x (Triple Time)</option></select></div><button class="btn btn-primary" onclick="calcOvertime()">💰 Calculate Overtime Pay</button>',
        "instructions": '<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2"><li>Enter your regular hourly rate</li><li>Enter overtime hours</li><li>Select overtime multiplier (1.5x/2x/3x)</li><li>Get your total overtime pay</li><li>Works for USD, EUR, GBP and more</li></ol>',
        "knowledge": '<ul class="info-list"><li>China Statutory Holiday<span class="info-val">3x pay</span></li><li>China Rest Day OT<span class="info-val">2x pay</span></li><li>China Weekday Extended<span class="info-val">1.5x pay</span></li><li>US Standard OT<span class="info-val">1.5x rate</span></li></ul>',
        "js": 'function calcOvertime(){var r=parseFloat(document.getElementById("hourly-rate").value);var h=parseFloat(document.getElementById("overtime-hours").value);var m=parseFloat(document.getElementById("overtime-rate").value);if(isNaN(r)||isNaN(h)||r<0||h<0){showToast("Please enter valid hourly rate and overtime hours");return}var ot=r*m*h;var normal=r*h;document.getElementById("main-result").textContent="$"+ot.toFixed(2);document.getElementById("detail-area").innerHTML=\'<div class="result-card"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Hourly Rate:</span><span>$\'+r.toFixed(2)+\'/hr</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Multiplier:</span><span>\'+m+\'x</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Overtime Hours:</span><span>\'+h+\' hrs</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px;font-weight:600"><span>Regular Pay:</span><span>$\'+normal.toFixed(2)+\'</span></div><div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700;color:#22d3ee"><span>Overtime Total:</span><span>$\'+ot.toFixed(2)+\'</span></div></div><div style="text-align:right;margin-top:8px"><button class="btn btn-secondary btn-sm" onclick="copyText(\\\'$\'+ot.toFixed(2)+\'\\\')">📋 Copy Result</button></div>\'}'
    },
    "double-time-calculator": {
        "en_title": "Double Time Calculator",
        "en_desc": "Free online double time pay calculator. Enter your regular hourly rate and hours worked to automatically calculate double-time pay. Ideal for holiday overtime, weekend shifts, and double-pay scenarios. Supports custom multipliers. Pure frontend local calculation.",
        "en_keywords": "double time calculator,double pay calculator,holiday pay,weekend overtime,double overtime",
        "category": "Finance",
        "icon": "💵",
        "en_header": "Double Time Calculator",
        "hero_text": "Free online double time pay calculator. Enter your regular hourly rate and hours worked to automatically calculate double-time pay. Ideal for holiday overtime, weekend shifts, and double-pay scenarios.",
        "input_html": '<div class="form-row"><div class="form-group"><label>💵 Hourly Rate ($)</label><input type="number" id="hourly-rate" placeholder="e.g.: 25" min="0" step="0.01"></div><div class="form-group"><label>⏱️ Hours Worked</label><input type="number" id="work-hours" placeholder="e.g.: 8" min="0" step="0.5"></div></div><div class="form-group"><label>📈 Pay Rate</label><select id="pay-rate"><option value="2">Double Time (2x)</option><option value="1.5">Time and a Half (1.5x)</option><option value="2.5">2.5x</option><option value="3">Triple Time (3x)</option></select></div><button class="btn btn-primary" onclick="calcDoubleTime()">💰 Calculate Pay</button>',
        "instructions": '<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2"><li>Enter your normal hourly rate</li><li>Enter hours worked</li><li>Select pay multiplier</li><li>Get your total pay automatically</li><li>Great for holiday/weekend shift verification</li></ol>',
        "knowledge": '<ul class="info-list"><li>Holiday Overtime<span class="info-val">Typically 2x or more</span></li><li>Sunday/Weekend OT<span class="info-val">Some companies 2x</span></li><li>Legal Holiday<span class="info-val">Triple pay</span></li><li>Company Policy<span class="info-val">Rates may vary</span></li></ul>',
        "js": 'function calcDoubleTime(){var r=parseFloat(document.getElementById("hourly-rate").value);var h=parseFloat(document.getElementById("work-hours").value);var m=parseFloat(document.getElementById("pay-rate").value);if(isNaN(r)||isNaN(h)||r<0||h<0){showToast("Please enter valid hourly rate and hours");return}var total=r*m*h;document.getElementById("main-result").textContent="$"+total.toFixed(2);document.getElementById("detail-area").innerHTML=\'<div class="result-card"><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Hourly Rate:</span><span>$\'+r.toFixed(2)+\'/hr</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Multiplier:</span><span>\'+m+\'x</span></div><div style="display:flex;justify-content:space-between;margin-bottom:8px"><span>Hours Worked:</span><span>\'+h+\' hrs</span></div><div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:700;color:#22d3ee"><span>Total Pay:</span><span>$\'+total.toFixed(2)+\'</span></div></div><div style="text-align:right;margin-top:8px"><button class="btn btn-secondary btn-sm" onclick="copyText(\\\'$\'+total.toFixed(2)+\'\\\')">📋 Copy Result</button></div>\'}'
    },
    "streaming-cost-calculator": {
        "en_title": "Streaming Cost Calculator",
        "en_desc": "Free online streaming subscription cost comparison calculator. Compare monthly/annual fees across Netflix, Disney+, HBO Max, and more. Calculate total multi-platform subscription costs. Helps users optimize streaming plans and save money. Pure frontend local calculation.",
        "en_keywords": "streaming cost calculator,subscription comparison,Netflix cost,Disney+ price,streaming services",
        "category": "Finance",
        "icon": "📺",
        "en_header": "Streaming Cost Calculator",
        "hero_text": "Free online streaming subscription cost comparison calculator. Compare monthly/annual fees across Netflix, Disney+, HBO Max, and more. Calculate total multi-platform subscription costs. Pure frontend local calculation.",
        "input_html": '<div style="margin-bottom:12px;color:#94a3b8;font-size:.85rem">Select your streaming subscriptions:</div><div id="platforms"><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Netflix</label><select class="plan-select" data-name="Netflix" data-monthly="15.49"><option value="6.99">Basic with Ads - $6.99/mo</option><option value="15.49" selected>Standard - $15.49/mo</option><option value="22.99">Premium - $22.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes" selected>Yes</option><option value="no">No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Disney+</label><select class="plan-select" data-name="Disney+" data-monthly="13.99"><option value="9.99">Basic - $9.99/mo</option><option value="13.99" selected>Premium - $13.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes" selected>Yes</option><option value="no">No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>HBO Max</label><select class="plan-select" data-name="HBO Max" data-monthly="16.99"><option value="9.99">With Ads - $9.99/mo</option><option value="16.99" selected>Ad-Free - $16.99/mo</option><option value="20.99">Ultimate - $20.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Amazon Prime Video</label><select class="plan-select" data-name="Amazon Prime Video" data-monthly="14.99"><option value="8.99">Prime Video Only - $8.99/mo</option><option value="14.99" selected>Prime Full - $14.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Hulu</label><select class="plan-select" data-name="Hulu" data-monthly="9.99"><option value="7.99">With Ads - $7.99/mo</option><option value="9.99" selected>No Ads - $9.99/mo</option><option value="18.99">Hulu + Live TV - $18.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Apple TV+</label><select class="plan-select" data-name="Apple TV+" data-monthly="9.99"><option value="9.99" selected>$9.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>YouTube Premium</label><select class="plan-select" data-name="YouTube Premium" data-monthly="13.99"><option value="13.99" selected>$13.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div><div class="form-row" style="align-items:center;margin-bottom:10px"><div class="form-group" style="flex:2"><label>Spotify Premium</label><select class="plan-select" data-name="Spotify" data-monthly="11.99"><option value="10.99">Individual - $10.99/mo</option><option value="11.99" selected>Premium - $11.99/mo</option><option value="16.99">Family - $16.99/mo</option></select></div><div class="form-group" style="flex:1"><label>Active</label><select class="sub-select"><option value="yes">Yes</option><option value="no" selected>No</option></select></div></div></div><button class="btn btn-primary" onclick="calcStreaming()">📊 Calculate Total Cost</button>',
        "instructions": '<ol style="padding-left:20px;color:#94a3b8;font-size:.85rem;line-height:2"><li>Select your active subscriptions</li><li>Choose the plan tier for each platform</li><li>Click calculate to see monthly and yearly costs</li><li>Compare plans to optimize your subscriptions</li></ol>',
        "knowledge": '<ul class="info-list"><li>Netflix Premium<span class="info-val">$22.99/mo</span></li><li>Disney+ Premium<span class="info-val">$13.99/mo</span></li><li>HBO Max Ultimate<span class="info-val">$20.99/mo</span></li><li>All platforms<span class="info-val">~$100+/mo</span></li></ul>',
        "js": 'function calcStreaming(){var ps=document.querySelectorAll("#platforms .form-row");var total=0;var detail="";ps.forEach(function(row){var sub=row.querySelector(".sub-select").value;if(sub==="yes"){var plan=row.querySelector(".plan-select");var name=plan.dataset.name;var price=parseFloat(plan.value);total+=price;detail+=\'<div style="display:flex;justify-content:space-between;margin-bottom:6px"><span>\'+name+\'</span><span>$\'+price.toFixed(2)+\'/mo</span></div>\'}});document.getElementById("main-result").textContent="$"+total.toFixed(2)+"/mo";var yearly=total*12;document.getElementById("detail-area").innerHTML=\'<div class="result-card">\'+detail+\'<div style="border-top:1px solid rgba(148,163,184,.2);padding-top:10px;margin-top:8px;display:flex;justify-content:space-between;font-weight:700"><span>Monthly Total:</span><span style="color:#22d3ee">$\'+total.toFixed(2)+\'/mo</span></div><div style="display:flex;justify-content:space-between;font-weight:700;margin-top:4px"><span>Yearly Total:</span><span style="color:#f1c40f">$\'+yearly.toFixed(2)+\'/yr</span></div></div><div class="health-tip">💡 Yearly cost: $\'+yearly.toFixed(2)+\'. Consider rotating subscriptions or sharing accounts to save over $\'+(yearly*0.3).toFixed(2)+\'!</div>\'}'
    }
}

BASE_DIR = "/home/chison/tools-site"

for name, t in TOOLS.items():
    en_dir = os.path.join(BASE_DIR, "en", name)
    os.makedirs(en_dir, exist_ok=True)
    
    en_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9W1157EBQV"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9W1157EBQV');</script>
<script>window.addEventListener("error",function(e){{if(e&&e.message===""){{e.preventDefault();}}}});window.addEventListener("unhandledrejection",function(e){{if(e&&e.reason&&e.reason.message===""){{e.preventDefault();}}}});</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4712477975146838" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{t['en_desc']}">
<meta name="keywords" content="{t['en_keywords']}">
<title>{t['en_title']} - Free ToolBase</title>
<link rel="canonical" href="https://free-toolbase.com/en/{name}/">
<meta property="og:title" content="{t['en_title']} - Free ToolBase">
<meta property="og:description" content="{t['en_desc']}">
<meta property="og:url" content="https://free-toolbase.com/en/{name}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free ToolBase">
<link rel="alternate" hreflang="zh" href="https://free-toolbase.com/{name}/">
<link rel="alternate" hreflang="en" href="https://free-toolbase.com/en/{name}/">
<link rel="alternate" hreflang="x-default" href="https://free-toolbase.com/en/{name}/">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication","name":"{t['en_title']}","description":"{t['en_desc']}","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","publisher":{{"@type":"Organization","name":"Free ToolBase","email":"dexshuang@google.com"}},"offers":{{"@type":"Offer","price":"0","priceCurrency":"USD"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://free-toolbase.com/en/"}},{{"@type":"ListItem","position":2,"name":"Tools","item":"https://free-toolbase.com/en/#tools"}},{{"@type":"ListItem","position":3,"name":"{t['en_title']}","item":"https://free-toolbase.com/en/{name}/"}}]}}</script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0f172a;color:#e2e8f0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;min-height:100vh}}
a{{color:#06b6d4;text-decoration:none}}a:hover{{color:#22d3ee}}
.container{{max-width:960px;margin:0 auto;padding:24px 16px}}
.header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;flex-wrap:wrap;gap:12px}}
.header h1{{font-size:1.5rem;color:#f1c40f}}
.lang-switch{{display:flex;gap:4px;background:#1e293b;border-radius:8px;padding:4px;border:1px solid rgba(148,163,184,.1)}}
.lang-switch a{{padding:6px 12px;border-radius:5px;font-size:.85rem;color:#94a3b8}}
.lang-switch a.active{{background:rgba(6,182,212,.2);color:#22d3ee}}
.nav-back{{color:#64748b;font-size:.85rem;margin-bottom:16px}}
.nav-back a{{color:#64748b}}.nav-back a:hover{{color:#94a3b8}}
.hero{{margin-bottom:24px}}.hero p{{color:#94a3b8;font-size:1rem;margin-bottom:8px}}
.badge{{display:inline-block;background:rgba(6,182,212,.15);color:#22d3ee;padding:4px 12px;border-radius:20px;font-size:.8rem;margin-bottom:16px}}
.main-grid{{display:grid;grid-template-columns:1fr 300px;gap:24px;margin-bottom:24px}}
@media(max-width:768px){{.main-grid{{grid-template-columns:1fr}}}}
.section{{background:#1e293b;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid rgba(148,163,184,.1)}}
.section h2{{font-size:1.1rem;color:#f1c40f;margin-bottom:12px}}
.form-group{{margin-bottom:14px}}
.form-group label{{display:block;color:#94a3b8;font-size:.9rem;margin-bottom:6px;font-weight:500}}
.form-group input,.form-group select,.form-group textarea{{width:100%;padding:10px 14px;background:#0f172a;border:1px solid rgba(148,163,184,.2);border-radius:8px;color:#e2e8f0;font-size:.9rem;outline:none;transition:all .2s}}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{{border-color:rgba(6,182,212,.4);box-shadow:0 0 0 3px rgba(6,182,212,.1)}}
.form-row{{display:flex;gap:12px;flex-wrap:wrap}}
.form-row .form-group{{flex:1;min-width:140px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:10px 20px;border:none;border-radius:8px;font-size:.9rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:inherit}}
.btn-primary{{background:linear-gradient(135deg,#06b6d4,#3b82f6);color:#fff;width:100%}}
.btn-primary:hover{{transform:translateY(-1px);box-shadow:0 4px 12px rgba(6,182,212,.3)}}
.btn-secondary{{background:#334155;color:#e2e8f0}}
.btn-secondary:hover{{background:#475569}}
.btn-sm{{padding:6px 12px;font-size:.8rem}}
.result-card{{background:#0f172a;border-radius:8px;padding:16px;margin-top:12px;border:1px solid rgba(148,163,184,.1)}}
.result-card .value{{font-size:1.8rem;font-weight:700;color:#22d3ee}}
.result-card .label{{font-size:.85rem;color:#94a3b8;margin-top:4px}}
.result-card .range{{font-size:.75rem;color:#64748b;margin-top:2px}}
.health-tip{{background:rgba(6,182,212,.08);border-left:3px solid #06b6d4;border-radius:0 8px 8px 0;padding:12px 16px;margin-top:16px;font-size:.85rem;color:#94a3b8}}
.info-list{{list-style:none;padding:0;margin-top:12px}}
.info-list li{{padding:8px 0;border-bottom:1px solid rgba(148,163,184,.1);font-size:.85rem;color:#94a3b8;display:flex;justify-content:space-between}}
.info-list li:last-child{{border-bottom:none}}
.info-list .info-val{{color:#e2e8f0;font-weight:500}}
footer{{text-align:center;padding:40px 16px;color:#64748b;font-size:.85rem;border-top:1px solid rgba(148,163,184,.1);margin-top:40px}}
footer a{{color:#64748b}}footer a:hover{{color:#94a3b8}}
.toast{{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#334155;color:#e2e8f0;padding:10px 20px;border-radius:8px;font-size:.85rem;z-index:9999;opacity:0;transition:opacity .3s;pointer-events:none}}
.toast.show{{opacity:1;pointer-events:auto}}
</style>
</head>
<body>
<div class="container">
<header class="header">
<h1>{t['icon']} {t['en_header']}</h1>
<div class="lang-switch">
<a href="/{name}/">中文</a>
<a href="/en/{name}/" class="active">English</a>
</div>
</header>
<nav class="nav-back"><a href="/en/">← Back to Home</a> / <a href="/en/#tools">Tool List</a> / {t['en_title']}</nav>
<div class="hero">
<span class="badge">{t['category']} Tool</span>
<p>{t['hero_text']}</p>
</div>
<div class="main-grid">
<div class="main-col">
<div class="section">
<h2>📊 Input Data</h2>
{t['input_html']}
<div class="section">
<h2>📈 Results</h2>
<div id="result-area">
<div class="result-card"><div class="value" id="main-result">--</div><div class="label">Enter data and click Calculate</div></div>
</div>
<div id="detail-area"></div>
</div>
</div>
<div class="side-col">
<div class="section">
<h2>📖 How to Use</h2>
{t['instructions']}
</div>
<div class="section">
<h2>💡 {t['en_title']} Knowledge</h2>
{t['knowledge']}
</div>
</div>
</div>
<footer>
<p>&copy; 2024 Free ToolBase &middot; All calculations are performed locally in your browser. No data is uploaded to any server. &middot; <a href="/en/about/">About</a> &middot; <a href="/en/privacy/">Privacy</a></p>
</footer>
</div>
<div class="toast" id="toast"></div>
<script>
function showToast(msg){{var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(function(){{t.classList.remove("show")}},2000)}}
function copyText(text){{navigator.clipboard.writeText(text).then(function(){{showToast("Copied to clipboard")}}).catch(function(){{showToast("Copy failed, please copy manually")}})}}
{t['js']}
</script>
</body>
</html>'''
    
    with open(os.path.join(en_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(en_html)
    print(f"✅ EN {name} rewritten")

print("\n✅ All EN versions regenerated!")
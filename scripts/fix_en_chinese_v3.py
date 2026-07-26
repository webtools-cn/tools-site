#!/usr/bin/env python3
"""第三轮修复EN中文 - 更全面的替换"""
import re, os

SITE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(SITE)

# 通用替换
COMMON_FIXES = [
    ('输入您的', 'Enter your '),
    ('输入', 'Enter '),
    ('选择', 'Select '),
    ('查看', 'View '),
    ('计算结果', 'Results'),
    ('设置', 'Set '),
    ('选择日常', 'Select Daily '),
    ('选择目标', 'Select Goal '),
    ('选择减重', 'Select Weight Loss '),
    ('选择单位', 'Select Unit '),
    ('选择持有期限', 'Select Holding Period '),
    ('选择纳税年度', 'Select Tax Year '),
    ('输入个人信息', 'Enter Personal Info'),
    ('输入体重', 'Enter Weight '),
    ('输入交易信息', 'Enter Trade Info'),
    ('输入买入价格', 'Enter Purchase Price'),
    ('输入卖出价格', 'Enter Selling Price'),
    ('输入血脂数据', 'Enter Lipid Data'),
    ('输入总胆固醇', 'Enter Total Cholesterol '),
    ('输入收入信息', 'Enter Income Info'),
    ('输入净自雇收入', 'Enter Net Self-Employment Income'),
    ('输入您的年净自雇收入', 'Enter your annual net self-employment income'),
    ('输入资产的买入价格', 'Enter asset purchase price'),
    ('输入资产的卖出价格', 'Enter asset selling price'),
    ('什么是', 'What is '),
    ('建议', 'Recommended: '),
    ('目标', 'Goal '),
    ('评估', 'Assessment'),
    ('维持', 'Maintain'),
    ('减重', 'Weight Loss'),
    ('增重', 'Weight Gain'),
    ('身高', 'Height'),
    # cal deficit specific
    ('基础代谢率', 'Basal Metabolic Rate'),
    ('每日总能量消耗', 'Total Daily Energy Expenditure'),
    ('是身体在完全静止状态下消耗的热量', 'is the energy your body burns at complete rest'),
    ('加上日常活动和运动消耗的总热量', 'plus calories burned through daily activities and exercise'),
    ('热量缺口是指每日消耗的热量与摄入热量之间的差值', 'Calorie deficit is the difference between calories burned and calories consumed'),
    ('天的缺口可减重约', ' days of deficit leads to ~'),
    ('预计每周体重变化', 'Estimated Weekly Weight Change'),
    ('目标摄入和预计体重变化', 'Target Intake & Expected Weight Change'),
    ('设置热量缺口', 'Set Calorie Deficit'),
    ('维持或增重目标', 'Maintenance or Weight Gain Goal'),
    ('选择减重', 'Select Weight Loss'),
    ('选择日常', 'Select Daily '),
    ('久坐不动', 'Sedentary'),
    ('轻度活动', 'Lightly Active'),
    ('中度活动', 'Moderately Active'),
    ('积极运动', 'Very Active'),
    ('高强度运动', 'Extra Active'),
    # cap gains specific
    ('短期', 'Short-term'),
    ('长期', 'Long-term'),
    ('持有', 'Holding '),
    ('持有期限', 'Holding Period'),
    ('净收益', 'Net Gain'),
    ('联邦税', 'Federal Tax'),
    ('州税', 'State Tax'),
    ('州税率', 'State Tax Rate'),
    ('州税和净收益', 'State Tax & Net Gain'),
    ('享受优惠税率', 'enjoy preferential tax rates'),
    ('按普通所得税率', 'at ordinary income tax rates'),
    ('按普通所得税率征税', 'taxed at ordinary income rates'),
    ('税是对出售资产', 'tax is levied on profits from selling assets'),
    ('所获利润征收的税', 'tax is levied on profits'),
    ('征收', 'levied'),
    ('税率是多少', 'Tax Rate'),
    ('取决于应税收入', 'depends on taxable income'),
    ('成本基础', 'Cost Basis'),
    ('此外', 'Additionally, '),
    ('的净投资收入税', ' Net Investment Income Tax'),
    ('高收入者可能还需缴纳', 'high-income earners may also owe '),
    ('年美国联邦', ' US federal '),
    ('年长期', ' year long-term '),
    ('税率为', 'tax rate: '),
    ('查看计算结果', 'View Results'),
    # cholesterol specific
    ('总胆固醇', 'Total Cholesterol'),
    ('坏胆固醇', 'Bad Cholesterol'),
    ('好胆固醇', 'Good Cholesterol'),
    ('甘油三酯', 'Triglycerides'),
    ('胆固醇', 'Cholesterol'),
    ('和甘油三酯数值', 'and Triglyceride levels'),
    ('的平衡', ' Balance'),
    ('胆固醇比率是评估心血管疾病风险的重要指标', 'Cholesterol ratio is an important indicator for assessing cardiovascular disease risk'),
    ('胆固醇比率综合考虑了', 'Cholesterol ratio comprehensively considers '),
    ('比单独的胆固醇数值更能反映心血管疾病风险', 'providing a better reflection of cardiovascular risk than individual numbers'),
    ('为什么胆固醇比率比单项指标更重要', 'Why Cholesterol Ratio Matters More Than Individual Numbers'),
    ('理想值', 'Ideal value: '),
    ('查看各项胆固醇比率和', 'View cholesterol ratios and '),
    # self-employment specific
    ('自雇税是自由职业者', 'Self-employment tax covers freelancers, '),
    ('独立承包商', 'independent contractors'),
    ('独立承包商等自雇人士需要缴纳的社会保障税和医疗保险税', 'independent contractors, and other self-employed individuals for Social Security and Medicare taxes'),
    ('包括自由职业者', 'including freelancers'),
    ('小型企业主等', 'small business owners, etc.'),
    ('的个人需要缴纳自雇税', ' individuals must pay self-employment tax'),
    ('谁需要缴纳自雇税', 'Who Needs to Pay Self-Employment Tax'),
    ('自雇税合计', 'Total Self-Employment Tax'),
    ('医疗保险税', 'Medicare Tax'),
    ('税后收入', 'After-Tax Income'),
    ('有效税率', 'Effective Tax Rate'),
    ('收入上限', 'Income Cap'),
    ('无上限', 'No Cap'),
    ('纳税年度', 'Tax Year'),
    ('其中社会保障税', 'Social Security tax: '),
    ('医疗保险税和有效税率', 'Medicare Tax & Effective Rate'),
    ('年自雇净收入超过', ' annual net self-employment income exceeding '),
    ('查看社会保障税', 'View Social Security Tax'),
    ('查看计算结果', 'View Results'),
    # JS中的常见中度中文
    ('请输入', 'Please enter '),
    ('复制成功', 'Copied!'),
    ('复制失败', 'Copy failed'),
    ('已复制', 'Copied'),
]

def deep_fix(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    for cn, en in COMMON_FIXES:
        content = content.replace(cn, en)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = [
        'en/a1c-calculator/index.html',
        'en/calorie-deficit-calculator/index.html',
        'en/capital-gains-tax-calculator/index.html',
        'en/cholesterol-ratio-calculator/index.html',
        'en/self-employment-tax-calculator/index.html',
    ]
    
    fixed = 0
    for f in files:
        path = os.path.join(SITE, f)
        if deep_fix(path):
            fixed += 1
            print(f"  ✅ Fixed: {f}")
        else:
            print(f"  ⚠️ No changes: {f}")
    
    print(f"\nFixed {fixed}/{len(files)}")

if __name__ == '__main__':
    main()
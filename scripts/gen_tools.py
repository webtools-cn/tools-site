#!/usr/bin/env python3
"""简化版：批量创建5个金融计算器工具"""
import os

BASE = "/home/chison/tools-site"

# 读取mortgage-calculator模板
with open(os.path.join(BASE, "mortgage-calculator", "index.html"), "r", encoding="utf-8") as f:
    cn_template = f.read()
with open(os.path.join(BASE, "en", "mortgage-calculator", "index.html"), "r", encoding="utf-8") as f:
    en_template = f.read()

# 定义5个工具的替换信息
tools = [
    {
        "slug": "heloc-payment-calculator",
        "cn": {
            "lang": "zh-CN",
            "title": "HELOC还款计算器 - Free ToolBase | 无需注册",
            "desc": "免费在线HELOC（房屋净值信贷额度）还款计算器。快速计算仅付息期和还款期的月供。输入信用额度、利率、提取期和还款期，立即查看每月还款额和总利息。",
            "keywords": "HELOC计算器,房屋净值信贷,还款计算器,在线工具,免费",
            "og_title": "HELOC还款计算器 - Free ToolBase | 无需注册",
            "h1": "💰 HELOC还款计算器",
            "hero": "免费在线HELOC（房屋净值信贷额度）还款计算器。快速计算仅付息期和还款期的月供。输入信用额度、利率、提取期和还款期，立即查看每月还款额和总利息。",
            "canonical": "heloc-payment-calculator",
            "breadcrumb": "HELOC还款计算器",
            "howto_name": "HELOC还款计算器",
        },
        "en": {
            "lang": "en",
            "title": "HELOC Payment Calculator - Free ToolBase | No Registration",
            "desc": "Free online HELOC (Home Equity Line of Credit) payment calculator. Quickly calculate monthly payments during both draw and repayment periods. Enter credit limit, interest rate, draw period and repayment term to see monthly payments and total interest.",
            "keywords": "HELOC calculator,home equity,payment calculator,online tool,free",
            "og_title": "HELOC Payment Calculator - Free ToolBase | No Registration",
            "h1": "💰 HELOC Payment Calculator",
            "hero": "Free online HELOC (Home Equity Line of Credit) payment calculator. Quickly calculate monthly payments during both draw and repayment periods. Enter credit limit, interest rate, draw period and repayment term to see monthly payments and total interest.",
            "canonical": "heloc-payment-calculator",
            "breadcrumb": "HELOC Payment Calculator",
            "howto_name": "HELOC Payment Calculator",
        }
    },
    {
        "slug": "pmi-calculator",
        "cn": {
            "lang": "zh-CN",
            "title": "PMI保险计算器 - Free ToolBase | 无需注册",
            "desc": "免费在线PMI（私人抵押贷款保险）计算器。快速估算每月PMI保费。输入房价、首付比例和贷款金额，立即查看每月PMI费用、何时可以取消PMI。",
            "keywords": "PMI计算器,抵押保险,贷款保险,在线工具,免费",
            "og_title": "PMI保险计算器 - Free ToolBase | 无需注册",
            "h1": "🏠 PMI保险计算器",
            "hero": "免费在线PMI（私人抵押贷款保险）计算器。快速估算每月PMI保费。输入房价、首付比例和贷款金额，立即查看每月PMI费用、何时可以取消PMI。",
            "canonical": "pmi-calculator",
            "breadcrumb": "PMI保险计算器",
            "howto_name": "PMI保险计算器",
        },
        "en": {
            "lang": "en",
            "title": "PMI Insurance Calculator - Free ToolBase | No Registration",
            "desc": "Free online PMI (Private Mortgage Insurance) calculator. Quickly estimate your monthly PMI premium. Enter home price, down payment percentage and loan amount to see monthly PMI cost and when PMI can be canceled.",
            "keywords": "PMI calculator,mortgage insurance,loan insurance,online tool,free",
            "og_title": "PMI Insurance Calculator - Free ToolBase | No Registration",
            "h1": "🏠 PMI Insurance Calculator",
            "hero": "Free online PMI (Private Mortgage Insurance) calculator. Quickly estimate your monthly PMI premium. Enter home price, down payment percentage and loan amount to see monthly PMI cost and when PMI can be canceled.",
            "canonical": "pmi-calculator",
            "breadcrumb": "PMI Insurance Calculator",
            "howto_name": "PMI Insurance Calculator",
        }
    },
]

print("脚本就绪，等待执行...")
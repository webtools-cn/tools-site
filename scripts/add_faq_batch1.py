#!/usr/bin/env python3
import json
import os

def generate_faqs(tool_name):
    """生成针对特定工具的FAQ内容"""
    faqs = [
        {
            "question": f"什么是{tool_name}？",
            "answer": f"{tool_name}是一个实用的在线工具，可以帮助你完成特定任务。无论是计算、转换还是生成，它都能为你提供便捷的服务。"
        },
        {
            "question": f"如何使用{tool_name}？",
            "answer": f"使用{tool_name}非常简单：输入所需参数，然后点击相应的按钮即可获得结果。工具会自动验证输入，确保输出准确无误。"
        },
        {
            "question": f"{tool_name}有什么特点？",
            "answer": f"{tool_name}的特点包括：快速响应、操作简单、结果精确，并且完全免费。所有数据处理都在客户端完成，确保用户隐私安全。"
        }
    ]
    return faqs

def create_faq_section(tool_name, faqs):
    """创建FAQ区块HTML"""
    faq_html = f'''
<div class="info-section">
  <h2>常见问题 (FAQ)</h2>
'''
    
    for i, faq in enumerate(faqs, 1):
        faq_html += f'''
  <div class="faq-item">
    <h3>问题{i}？</h3>
    <p>{faq['answer']}</p>
  </div>
'''
    
    faq_html += '''
</div>
'''
    return faq_html

def create_faq_schema(tool_name, faqs):
    """创建JSON-LD Schema"""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for faq in faqs:
        # 提取问题中的实际问题内容
        question_clean = faq['question'].replace('? ', '').replace('什么', '什么').replace('如何', '如何').replace('有什么', '有什么')
        
        schema["mainEntity"].append({
            "@type": "Question",
            "name": faq['question'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": faq['answer']
            }
        })
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

def process_tools():
    """处理所有工具的FAQ生成"""
    # 读取配置
    config_path = '/home/chison/tools-site/quality/faq-priority-list.json'
    if not os.path.exists(config_path):
        print(f"配置文件 {config_path} 不存在")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    high_priority_tools = config.get('high_priority', [])
    
    print(f"将为 {len(high_priority_tools)} 个工具生成FAQ")
    
    for tool_name in high_priority_tools:
        print(f"\n正在为 {tool_name} 生成FAQ...")
        
        # 生成FAQ
        faqs = generate_faqs(tool_name)
        
        # 创建FAQ区块
        faq_html = create_faq_section(tool_name, faqs)
        
        # 创建Schema
        faq_schema = create_faq_schema(tool_name, faqs)
        
        print(f"✓ {tool_name} FAQ生成完成")
    
    print("\n所有高优先级工具FAQ生成完成！")

if __name__ == "__main__":
    process_tools()
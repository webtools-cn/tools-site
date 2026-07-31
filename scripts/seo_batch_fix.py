#!/usr/bin/env python3
"""SEO meta description batch optimizer - target 140-160 chars"""
import re

PAGES = {
    "ai-agent-workflow-builder": "免费在线AI Agent工作流构建器，可视化拖拽设计多步骤AI代理流程，自由添加条件分支、工具调用、循环节点和变量传递模块。实时预览流程拓扑图，一键导出标准JSON配置用于LangChain或AutoGPT部署。无需注册完全免费，纯前端本地运行数据绝不上传服务器。",
    "ai-api-cost-calculator": "免费在线AI API成本计算器，实时对比OpenAI、Claude、Gemini和DeepSeek等主流大语言模型的API调用价格。支持输入输出Token分别计费，提供批量模型横向对比和月度预算规划功能，精确估算项目API开销帮助研发团队控制成本。纯前端本地计算无需注册。",
    "ai-context-window-comparator": "免费在线LLM上下文窗口对比工具，可视化比较GPT-4o、Claude、Gemini和Llama等主流大模型的上下文长度与Token容量。直观展示各模型可处理的文档页数、代码行数和对话轮次上限，帮助开发者根据业务场景选择最合适的AI模型。无需注册纯前端运行。",
    "ai-detector": "免费在线AI内容检测器，通过多维度统计分析和语言模式识别检测文本是否由AI生成。支持识别GPT、Claude和Gemini等主流模型生成的内容，实时显示AI生成概率和逐句详细分析报告，帮助辨别学术论文、新闻报道和社交媒体内容的真实性。无需注册数据不上传服务器。",
    "ai-fine-tuning-cost-calculator": "免费在线AI微调成本计算器，精准估算GPT-4o、Llama和Mistral等主流模型的微调训练成本。自动计算数据标注费用、训练时长和推理部署成本，支持多模型方案横向对比和成本优化建议。AI项目预算规划必备实用工具，无需注册纯前端本地计算数据安全可靠。",
    "ai-function-call-generator": "免费在线AI函数调用生成器，可视化构建OpenAI、Claude和Gemini的Function Calling JSON配置模板。支持参数类型定义、必填校验、枚举值和嵌套对象设置，实时预览调用示例并导出完整可运行代码。前端开发与AI应用集成必备工具，无需注册完全免费使用。",
    "ai-image-prompt-generator": "免费在线AI图像提示词生成器，专为Midjourney、DALL-E和Stable Diffusion等主流AI绘画平台设计。智能组合艺术风格、光影效果、构图方式和色彩方案等核心参数，一键生成结构化的专业级AI绘画Prompt，有效提升出图质量和风格一致性，无需注册即开即用。",
    "ai-jailbreak-detector": "免费在线AI越狱检测器，自动识别用户输入中的越狱攻击和提示词注入风险。支持DAN、Developer Mode、角色扮演诱导等30+种已知越狱模式检测，实时评估风险等级并标注可疑片段，提供针对性修复建议。AI应用安全防护必备工具，纯前端本地运行数据不上传。",
    "ai-llm-benchmark": "免费在线LLM基准测试对比工具，综合比较GPT-4o、Claude、Gemini和Llama等主流大模型的推理性能、响应速度、API价格和上下文窗口能力。涵盖MMLU、HumanEval、GSM8K等权威评测指标分数横向对比。AI模型选型一站式参考平台，无需注册免费使用。",
    "ai-model-comparator": "免费在线AI模型对比器，横向比较GPT-4o、Claude 3.5、Gemini和Llama等大语言模型的核心能力、API价格、推理速度和上下文窗口。支持多模型并排对比和自定义筛选排序，帮助开发者和企业根据业务需求选择最优AI解决方案。无需注册免费使用纯前端运行。",
    "ai-model-directory": "免费在线AI模型目录，一站式查阅GPT-4o、Claude、Gemini和Llama等主流AI模型的参数规模、API价格、核心能力和最佳适用场景。持续追踪最新模型发布动态和版本更新信息，AI开发者和研究者选型必备参考工具，无需注册免费随时浏览最新资讯。",
    "ai-persona-generator": "免费在线AI角色生成器，一键为AI聊天助手创建完整角色卡。支持性格特征、背景故事、对话风格和外貌描述等多维度自定义设定，适用于Character.AI、ChatGPT角色扮演和虚拟角色创作等场景。生成角色卡可直接复制导入各大AI平台使用，无需注册免费。",
    "ai-prompt-injection-tester": "免费在线AI提示词注入测试器，全面检测提示词中的安全漏洞和注入风险。支持角色扮演攻击检测、系统提示提取检测、越狱提示识别等多种攻击模式。纯前端本地分析数据绝不上传服务器，AI应用安全测试必备工具，无需注册即可免费使用保护你的AI应用安全。",
    "ai-prompt-variable-extractor": "免费在线AI提示词变量提取器，自动识别提示词中的变量占位符并生成结构化模板。支持{{变量}}、{变量}、[变量]等多种格式和自定义分隔符，一键提取所有变量导出为JSON配置。适用于Prompt工程模板管理和批量提示词生成场景，无需注册纯前端本地运行数据安全。",
    "ai-sentence-rewriter": "免费在线AI智能句子改写工具，利用先进人工智能算法优化英文句子表达和语法结构。支持正式、简洁、创意、学术等多种改写风格，一键完成句式重组和词汇替换优化。适用于学术论文润色、商务邮件优化和社交媒体内容创作场景。无需注册完全免费，浏览器本地处理。",
    "ai-system-prompt-builder": "免费在线AI系统提示词构建器，可视化创建和优化ChatGPT、Claude、Gemini的系统级提示词。内置丰富模板库和实时Token计数器，支持结构化构建、多版本管理和一键导出功能。帮助开发者快速构建高质量AI系统指令提升模型表现。无需注册纯前端本地运行安全可靠。",
    "ai-text-chunker": "免费在线AI文本分块器，为RAG检索增强生成场景优化文本分块策略。支持固定大小、句子级、段落级和语义分块四种模式，可调节重叠率和Token计数。适配LangChain和LlamaIndex等主流RAG框架。无需注册纯前端本地处理，数据绝不上传服务器安全可靠。",
    "ai-tool-calling-tester": "免费在线AI函数调用测试器，帮助开发者测试和调试LLM的Function Calling与Tool Use能力。可视化定义工具Schema、模拟多轮对话交互、验证参数提取准确性。支持OpenAI和Anthropic两种格式。AI应用开发调试必备工具，无需注册纯前端运行。",
    "algorithm-visualizer": "免费在线算法可视化器，动态展示排序算法（冒泡/快排/归并/堆排）、搜索算法（二分/BFS/DFS）和路径查找（A*/Dijkstra）的完整执行过程。可调节数组大小和动画播放速度，支持分步调试模式逐步观察算法状态变化。编程教学和算法学习最佳辅助工具无需注册安装。",
    "alliteration-generator": "免费在线押头韵生成器（Alliteration Generator），选择任意英文字母和主题即可自动生成押头韵短语和句子。内置丰富英文词库，支持创意写作、品牌命名、广告标语和诗歌创作等多种应用场景，一键生成多个备选方案并可复制使用。无需注册，纯前端本地运行数据安全绝不上传。",
}

def patch_page(slug, new_desc):
    path = f"{slug}/index.html"
    with open(path) as f:
        content = f.read()
    
    old_meta = re.search(r'<meta name="description" content="([^"]+)"', content)
    if not old_meta:
        print(f"  SKIP {slug}: no meta description")
        return False
    old_desc = old_meta.group(1)
    
    if old_desc == new_desc:
        print(f"  SKIP {slug}: unchanged")
        return False
    
    # Replace both meta description and og:description
    content = content.replace(
        f'<meta name="description" content="{old_desc}"',
        f'<meta name="description" content="{new_desc}"'
    )
    content = content.replace(
        f'<meta property="og:description" content="{old_desc}"',
        f'<meta property="og:description" content="{new_desc}"'
    )
    
    with open(path, 'w') as f:
        f.write(content)
    
    print(f"  OK {slug}: {len(old_desc)} -> {len(new_desc)} chars")
    return True

if __name__ == "__main__":
    changed = 0
    for slug, desc in PAGES.items():
        if patch_page(slug, desc):
            changed += 1
    print(f"\nTotal: {changed} pages updated")
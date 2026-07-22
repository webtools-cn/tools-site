#!/usr/bin/env python3
"""
Batch LLM quality check for B-class tools (items 11-380).
Sends 10 tools per batch to mimo-v2.5-free via API.
Appends results to llm-review-all.json in JSONL format.
"""

import json
import os
import re
import subprocess
import time
import sys

SITE_DIR = "/home/chison/tools-site"
REVIEW_FILE = os.path.join(SITE_DIR, "quality/need-llm-review.json")
OUTPUT_FILE = os.path.join(SITE_DIR, "quality/llm-review-all.json")
API_URL = "https://opencode.ai/zen/v1/chat/completions"
MODEL = "mimo-v2.5-free"

SYSTEM_PROMPT = """你是一个网页质检专家。请检查以下工具页面的HTML内容，只报告确凿的结构问题：
1. 空白区域：div标签内没有任何内容（包括没有文本、子元素为空）
2. 内容重复：相同文本内容在页面中重复出现（排除正常的SEO重复）
3. H2标签超过10个

如果没有确凿问题，请返回 {"issues": []}
如果有问题，返回JSON格式：
{"issues": [{"tool": "工具名", "type": "问题类型", "detail": "问题描述", "fix": "修复建议"}]}

只报告确凿的问题，不要报告模板缺陷或正常设计。"""


def strip_tags(html_text):
    """Remove script, style, svg tags and their content, then return first 1200 chars."""
    html_text = re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
    html_text = re.sub(r'<style[^>]*>.*?</style>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
    html_text = re.sub(r'<svg[^>]*>.*?</svg>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
    html_text = re.sub(r'<noscript[^>]*>.*?</noscript>', '', html_text, flags=re.DOTALL | re.IGNORECASE)
    return html_text[:1200]


def load_tool_content(tool_name):
    """Load and process a tool's index.html."""
    html_path = os.path.join(SITE_DIR, tool_name, "index.html")
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return strip_tags(html)
    except Exception as e:
        return "[ERROR loading: " + str(e) + "]"


def call_api(batch_tools, api_key):
    """Call the LLM API with a batch of tools."""
    parts = []
    for i, (tool_name, content, meta) in enumerate(batch_tools):
        parts.append("--- 工具 " + str(i + 1) + ": " + tool_name + " ---\n" +
                      "元数据: h2=" + str(meta.get('h2', 0)) +
                      ", empty_divs=" + str(meta.get('empty_divs', 0)) +
                      ", h1=" + str(meta.get('h1', 0)) + "\n" +
                      "HTML内容(前1200字符):\n" + content + "\n")

    user_msg = "请检查以下" + str(len(batch_tools)) + "个工具页面，找出确凿的结构问题：\n\n" + "\n".join(parts)

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.1,
        "max_tokens": 2000
    }

    tmp_file = "/tmp/llm_batch_payload.json"
    with open(tmp_file, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)

    auth_header = "Authorization: Bearer {}".format(api_key)

    cmd = [
        "curl", "-s", "--noproxy", "127.0.0.1",
        "-x", "http://127.0.0.1:7890",
        "--max-time", "120",
        "-X", "POST", API_URL,
        "-H", "Content-Type: application/json",
        "-H", auth_header,
        "-d", "@" + tmp_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=130)
        if result.returncode != 0:
            return {"error": "curl failed: " + result.stderr, "issues": []}

        resp = json.loads(result.stdout)
        if "error" in resp:
            return {"error": str(resp["error"]), "issues": []}

        content = resp.get("choices", [{}])[0].get("message", {}).get("content", "")

        content_clean = content.strip()
        if content_clean.startswith("```"):
            content_clean = re.sub(r'^```(?:json)?\s*', '', content_clean)
            content_clean = re.sub(r'\s*```$', '', content_clean)

        try:
            parsed = json.loads(content_clean)
            return parsed
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', content_clean, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group())
                    return parsed
                except json.JSONDecodeError:
                    pass
            return {"raw_response": content, "issues": []}
    except subprocess.TimeoutExpired:
        return {"error": "timeout", "issues": []}
    except Exception as e:
        return {"error": str(e), "issues": []}


def main():
    api_key = os.environ.get("OPENCODE_ZEN_KEY1", "")
    if not api_key:
        print("ERROR: OPENCODE_ZEN_KEY1 not set")
        sys.exit(1)

    with open(REVIEW_FILE, 'r', encoding='utf-8') as f:
        tools = json.load(f)

    total_tools = len(tools)
    print("Total tools in review list: " + str(total_tools))

    start_idx = 10
    remaining = tools[start_idx:]
    print("Processing tools " + str(start_idx + 1) + " to " + str(total_tools) + " (" + str(len(remaining)) + " tools)")

    batch_size = 10
    total_batches = (len(remaining) + batch_size - 1) // batch_size
    print("Total batches: " + str(total_batches))

    print("Loading and processing HTML files...")
    prepared = []
    for i, tool_meta in enumerate(remaining):
        tool_name = tool_meta["tool"]
        content = load_tool_content(tool_name)
        prepared.append((tool_name, content, tool_meta))
        if (i + 1) % 50 == 0:
            print("  Loaded " + str(i + 1) + "/" + str(len(remaining)) + " tools")
    print("  Loaded " + str(len(remaining)) + "/" + str(len(remaining)) + " tools - done")

    all_results = []
    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        end = min(start + batch_size, len(remaining))
        batch = prepared[start:end]

        batch_num = batch_idx + 1
        tool_names = [b[0] for b in batch]
        print("\n--- Batch " + str(batch_num) + "/" + str(total_batches) + ": " + tool_names[0] + " ... " + tool_names[-1] + " ---")

        result = call_api(batch, api_key)

        record = {
            "batch": batch_num,
            "batch_start_index": start_idx + start,
            "tools": tool_names,
            "result": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        issues = result.get("issues", [])
        if issues:
            print("  Found " + str(len(issues)) + " issue(s):")
            for iss in issues:
                detail = iss.get('detail', '')[:80]
                print("    - " + iss.get('tool', '?') + ": " + iss.get('type', '?') + " - " + detail)
        else:
            print("  No issues found.")

        if result.get("error"):
            print("  [WARNING] API error: " + result['error'])

        all_results.append(record)

        if batch_idx < total_batches - 1:
            time.sleep(2)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_issues = 0
    issue_types = {}
    tools_with_issues = []

    for record in all_results:
        issues = record.get("result", {}).get("issues", [])
        for iss in issues:
            total_issues += 1
            t = iss.get("type", "unknown")
            issue_types[t] = issue_types.get(t, 0) + 1
            tools_with_issues.append({
                "tool": iss.get("tool", "?"),
                "type": t,
                "detail": iss.get("detail", ""),
                "fix": iss.get("fix", "")
            })

    print("\nTotal batches processed: " + str(len(all_results)))
    print("Total tools processed: " + str(len(remaining)))
    print("Total issues found: " + str(total_issues))
    print("\nIssue type distribution:")
    for t, c in sorted(issue_types.items(), key=lambda x: -x[1]):
        print("  " + t + ": " + str(c))

    if tools_with_issues:
        print("\nTools with issues:")
        for twi in tools_with_issues:
            print("  - " + twi['tool'] + ": " + twi['type'] + " - " + twi['detail'][:100])

    summary = {
        "total_batches": len(all_results),
        "total_tools": len(remaining),
        "total_issues": total_issues,
        "issue_type_distribution": issue_types,
        "tools_with_issues": tools_with_issues
    }
    summary_file = os.path.join(SITE_DIR, "quality/llm-review-summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("\nSummary saved to: " + summary_file)
    print("Results saved to: " + OUTPUT_FILE)


if __name__ == "__main__":
    main()

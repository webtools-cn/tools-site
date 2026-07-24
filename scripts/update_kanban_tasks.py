#!/usr/bin/env python3
"""Update kanban tasks for batch_fix: 0交互空壳工具 schema/title fixes"""
import json
import datetime

with open("/home/chison/.hermes/kanban/boards/tools-site-pipeline-tasks.json", "r") as f:
    data = json.load(f)

# Tasks completed in this batch
completed = {
    137: "about",
    205: "calc",
    230: "contact",
    231: "converter",
    234: "creative",
    317: "design",
    319: "dev",
}

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

for task in data["tasks"]:
    tid = task.get("id", "")
    if not tid.startswith("T"):
        continue
    try:
        num = int(tid[1:])
    except ValueError:
        continue
    
    if num in completed:
        task["column"] = "dev-in-progress"
        task["updated_at"] = now
        if "messages" not in task:
            task["messages"] = []
        task["messages"].append({
            "from": "dev-cron",
            "to": "all",
            "type": "qa_pass",
            "content": f"Batch fix completed: removed generic HowTo/FAQPage schema (inappropriate for info/directory page), replaced SoftwareApplication→{'AboutPage' if num==137 else 'ContactPage' if num==230 else 'CollectionPage'}, fixed title separator ·→|, fixed og:title duplicate. Tool: {completed[num]}",
            "timestamp": now
        })
        if "rework_count" not in task:
            task["rework_count"] = 0

with open("/home/chison/.hermes/kanban/boards/tools-site-pipeline-tasks.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {len(completed)} tasks: {', '.join(f'T{n}({completed[n]})' for n in sorted(completed.keys()))}")

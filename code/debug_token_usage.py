import json
from ingestion.framework_loader import load_saica_framework

print("Loading framework...")
framework_data = load_saica_framework()

# 1. Measure Training Plan
training_plan = framework_data.get('training_plan', [])
tp_json_full = json.dumps(training_plan, indent=0)
print(f"\n[Training Plan] Full Items: {len(training_plan)}")
print(f"[Training Plan] Char Count: {len(tp_json_full)}")
print(f"[Training Plan] Est. Tokens: {len(tp_json_full) / 4}")

# 2. Measure Context Limit (15k)
MAX_CONTEXT_CHARS = 15000 
context_text = ""
current_chars = 0
for cat_name, cat_files in framework_data.get('additional_context', {}).items():
    if current_chars >= MAX_CONTEXT_CHARS: break
    for fname, ftext in cat_files.items():
        if current_chars >= MAX_CONTEXT_CHARS: break
        snippet = ftext[:3000]
        context_text += f"--- Document: {fname} ---\n{snippet}\n\n"
        current_chars += len(snippet)

print(f"\n[Context] Char Count: {len(context_text)}")

# 3. Minification Test
def minify_plan(plan):
    mini = []
    for item in plan:
        # Keep only essential fields for mapping
        mini.append({
            "code": item.get("competency_code", ""),
            "name": item.get("competency_name", ""),
            # maybe snippet of behavior?
             "desc": (item.get("behavioral_indicators") or "")[:100]
        })
    return mini

tp_mini = minify_plan(training_plan)
tp_json_mini = json.dumps(tp_mini, separators=(',', ':'))
print(f"\n[Training Plan (Minified)] Char Count: {len(tp_json_mini)}")
print(f"[Training Plan (Minified)] Est. Tokens: {len(tp_json_mini) / 4}")

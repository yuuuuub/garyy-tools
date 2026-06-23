#!/usr/bin/env python3
"""Fix remaining blank-on-load tools."""
import os, re

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def add_auto_call(tool_name, func_name):
    """Add auto-call for a function on page load."""
    path = os.path.join(TOOL_DIR, tool_name, 'index.html')
    content = read_file(path)
    
    if re.search(rf'setTimeout.*{func_name}|{func_name}\s*\(\s*\)\s*;', content):
        print(f"  SKIP {tool_name}: already has auto-call")
        return False
    
    auto_code = f"\nsetTimeout(() => {{ try {{ {func_name}(); }} catch(e) {{}} }}, 500);\n"
    last_script = content.rfind('</script>')
    if last_script == -1:
        print(f"  SKIP {tool_name}: no </script> tag")
        return False
    
    content = content[:last_script] + auto_code + content[last_script:]
    write_file(path, content)
    print(f"  FIXED {tool_name}: added auto-call via {func_name}")
    return True

# Remaining AI tools
REMAINING_AI = {
    'ai-fill-mask': 'predict',
    'ai-qna': 'ask',
    'ai-sentiment': 'analyze',
    'ai-summarize': 'summarize',
    'ai-translate': 'translate',
    'ai-zero-shot': 'classify',
}

print("=== Fixing remaining AI tools ===")
fixed = 0
for tool, func in REMAINING_AI.items():
    if add_auto_call(tool, func):
        fixed += 1

# Fix ai-tokenizer (shows stats on input, needs initial call)
print("\n=== Fixing ai-tokenizer ===")
if add_auto_call('ai-tokenizer', 'updateStats'):
    fixed += 1

# Fix ai-job-risk (renders dropdown on load)
print("\n=== Fixing ai-job-risk ===")
path = os.path.join(TOOL_DIR, 'ai-job-risk', 'index.html')
content = read_file(path)
if 'renderDropdown()' not in content:
    auto_code = "\nrenderDropdown();\n"
    last_script = content.rfind('</script>')
    content = content[:last_script] + auto_code + content[last_script:]
    write_file(path, content)
    print("  FIXED ai-job-risk: added renderDropdown()")
    fixed += 1
else:
    print("  SKIP ai-job-risk: already has renderDropdown()")

print(f"\nTotal additional fixes: {fixed}")

#!/usr/bin/env python3
"""Fix tools that show blank on load by adding auto-calc or default display."""
import os, re

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_ai_tool(tool_name):
    """Fix AI tools by auto-generating with defaults on load."""
    path = os.path.join(TOOL_DIR, tool_name, 'index.html')
    content = read_file(path)
    
    # Find the generate function name
    gen_match = re.search(r'function\s+(generate\w*)\s*\(', content)
    if not gen_match:
        print(f"  SKIP {tool_name}: can't find generate function")
        return False
    
    gen_func = gen_match.group(1)
    
    # Check if already auto-generates
    if re.search(rf'{gen_func}\s*\(\s*\)\s*;', content) and 'window.onload' in content:
        print(f"  SKIP {tool_name}: already auto-generates")
        return False
    
    # Add auto-generate on load - insert before </script>
    # But only if there's at least some default input value
    auto_code = f"\n// Auto-generate on load for non-blank experience\nsetTimeout(() => {{ try {{ {gen_func}(); }} catch(e) {{}} }}, 500);\n"
    
    # Find the last </script> tag and insert before it
    last_script = content.rfind('</script>')
    if last_script == -1:
        print(f"  SKIP {tool_name}: no </script> tag found")
        return False
    
    # Don't add if already present
    if 'setTimeout' in content and gen_func in content:
        # Check if there's already a setTimeout with this function
        if re.search(rf'setTimeout.*{gen_func}', content):
            print(f"  SKIP {tool_name}: already has auto-generate")
            return False
    
    content = content[:last_script] + auto_code + content[last_script:]
    write_file(path, content)
    print(f"  FIXED {tool_name}: added auto-generate via {gen_func}")
    return True

def fix_calculator(tool_name):
    """Fix calculators by calling calculate() on load."""
    path = os.path.join(TOOL_DIR, tool_name, 'index.html')
    content = read_file(path)
    
    # Find the calculate function name
    calc_match = re.search(r'function\s+(calc\w*|calculate\w*)\s*\(', content)
    if not calc_match:
        # Try other patterns
        calc_match = re.search(r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*result', content)
    
    if not calc_match:
        print(f"  SKIP {tool_name}: can't find calculate function")
        return False
    
    calc_func = calc_match.group(1)
    
    # Check if already auto-calculates
    if re.search(rf'{calc_func}\s*\(\s*\)\s*;', content.rstrip()):
        print(f"  SKIP {tool_name}: already auto-calculates")
        return False
    
    # Add auto-calc at end of script
    auto_code = f"\n// Auto-calculate on load for non-blank experience\n{calc_func}();\n"
    
    last_script = content.rfind('</script>')
    if last_script == -1:
        print(f"  SKIP {tool_name}: no </script> tag found")
        return False
    
    content = content[:last_script] + auto_code + content[last_script:]
    write_file(path, content)
    print(f"  FIXED {tool_name}: added auto-calc via {calc_func}")
    return True

# Top 20 tools to fix (most impactful)
AI_TOOLS = [
    'ai-bio', 'ai-fill-mask', 'ai-hashtag', 'ai-name-gen', 'ai-poem',
    'ai-qna', 'ai-sentiment', 'ai-story', 'ai-summarize', 'ai-text-gen',
    'ai-tokenizer', 'ai-translate', 'ai-tweet', 'ai-zero-shot', 'ai-job-risk',
]

CALC_TOOLS = [
    'discount-calc', 'compliment-generator', 'unit-converter',
    'baby-name', 'decision-maker',
]

print("=== Fixing AI Tools ===")
ai_fixed = 0
for tool in AI_TOOLS:
    if fix_ai_tool(tool):
        ai_fixed += 1

print(f"\n=== Fixing Calculators ===")
calc_fixed = 0
for tool in CALC_TOOLS:
    if fix_calculator(tool):
        calc_fixed += 1

print(f"\n=== Summary ===")
print(f"AI tools fixed: {ai_fixed}/{len(AI_TOOLS)}")
print(f"Calculator tools fixed: {calc_fixed}/{len(CALC_TOOLS)}")
print(f"Total fixed: {ai_fixed + calc_fixed}")

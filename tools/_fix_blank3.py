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

def add_autocall(tool_name, call_code):
    """Insert auto-call before last </script> tag."""
    path = os.path.join(TOOL_DIR, tool_name, 'index.html')
    content = read_file(path)
    
    last_script = content.rfind('</script>')
    if last_script == -1:
        print(f"  SKIP {tool_name}: no </script> tag")
        return False
    
    # Check if already present
    if call_code.strip() in content:
        print(f"  SKIP {tool_name}: already has auto-call")
        return False
    
    content = content[:last_script] + call_code + "\n" + content[last_script:]
    write_file(path, content)
    print(f"  FIXED {tool_name}")
    return True

fixes = [
    # (tool_name, auto_call_code)
    ('sunscreen-guide', 'calcSPF();'),
    ('pet-summer', 'calcRisk();'),
    ('dice-roller', 'rollDice();'),
    ('xunwu', '// Auto-show search hint on load\nsetTimeout(() => { var r = document.getElementById("result"); if(r && !r.innerHTML.trim()) { r.style.display = "block"; r.innerHTML = "<p style=\\"text-align:center;color:var(--text2)\\">输入汉字，查询五行属性</p>"; } }, 300);'),
    ('phone-cooling', '// Auto-show initial advice\nsetTimeout(() => { var el = document.getElementById("tempResult"); if(el) { el.style.display = "block"; el.innerHTML = "<p style=\\"text-align:center;color:var(--text2)\\">选择当前温度，获取降温建议</p>"; } }, 300);'),
    ('base64-img', '// Auto-show encode output card with placeholder\nsetTimeout(() => { var el = document.getElementById("encodeOutputCard"); if(el) { el.style.display = "block"; el.innerHTML = "<p style=\\"text-align:center;color:var(--text2);padding:20px\\">上传图片或拖拽到左侧区域</p>"; } }, 300);'),
    ('nginx-config', '// Auto-show output with placeholder\nsetTimeout(() => { var el = document.getElementById("outputCard"); if(el) { el.style.display = "block"; el.innerHTML = "<pre style=\\"padding:16px;color:var(--text2)\\"># 选择左侧配置项，自动生成 nginx 配置</pre>"; } }, 300);'),
]

print("=== Fixing remaining tools ===")
fixed = 0
for tool_name, call_code in fixes:
    if add_autocall(tool_name, call_code):
        fixed += 1

print(f"\nTotal fixed: {fixed}")

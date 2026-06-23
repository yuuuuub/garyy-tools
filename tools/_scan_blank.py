#!/usr/bin/env python3
"""Scan tool index.html files for blank-on-load issues."""
import os, re, json

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))

# Already fixed tools - skip these
SKIP = {
    'weather-now', 'air-quality', 'bmi-calculator', 'sleep-quality-calc',
    'diff-checker', 'text-diff',
    # All editors
    'code-editor-cn', 'css-editor-cn', 'html-editor-cn', 'js-editor-cn',
    'json-editor-cn', 'markdown-editor-cn', 'regex-editor-cn', 'sql-editor-cn',
    'text-editor-cn', 'xml-editor-cn', 'yaml-editor-cn', 'docker-editor',
    'nginx-editor', 'json-editor', 'markdown-editor', 'svg-editor',
    # All playgrounds
    'c-playground', 'cpp-playground', 'coffeescript-playground', 'css-playground',
    'dart-playground', 'deno-playground', 'd3-playground', 'elasticsearch-playground',
    'elixir-playground', 'erlang-playground', 'esbuild-playground', 'firestore-playground',
    'gatsby-playground', 'go-playground', 'graphql-playground', 'grpc-playground',
    'haskell-playground', 'hexo-playground', 'html-playground', 'hugo-playground',
    'java-playground', 'jekyll-playground', 'js-playground', 'julia-playground',
    'kafka-playground', 'kotlin-playground', 'lua-playground', 'mathematica-playground',
    'matlab-playground', 'mongodb-playground', 'mqtt-playground', 'mysql-playground',
    'nextjs-playground', 'node-playground', 'nuxt-playground', 'parcel-playground',
    'perl-playground', 'php-playground', 'postgresql-playground', 'python-playground',
    'r-playground', 'react-playground', 'rest-playground', 'rollup-playground',
    'ruby-playground', 'rust-playground', 'scala-playground', 'scratch-card',
    'snowpack-playground', 'soap-playground', 'sqlite-playground', 'svelte-playground',
    'svg-playground', 'swift-playground', 'threejs-playground', 'turbopack-playground',
    'typescript-playground', 'vite-playground', 'vue-playground', 'webgl-playground',
    'webpack-playground', 'websocket-playground',
}

issues = []

for tool_name in sorted(os.listdir(TOOL_DIR)):
    tool_path = os.path.join(TOOL_DIR, tool_name)
    if not os.path.isdir(tool_path) or tool_name.startswith('_'):
        continue
    if tool_name in SKIP:
        continue
    
    html_file = os.path.join(tool_path, 'index.html')
    if not os.path.isfile(html_file):
        continue
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
    
    # Check 1: Empty #app div on load
    # Pattern: <div id="app"></div> with no inner content and no JS that populates it
    app_match = re.search(r'<div\s+id=["\']app["\']\s*>\s*</div>', content)
    if app_match:
        # Check if there's JS that sets innerHTML of #app
        has_app_content = bool(re.search(r"document\.getElementById\s*\(\s*['\"]app['\"]", content))
        has_vue_app = bool(re.search(r"new\s+Vue|createApp|mount\s*\(\s*['\"]#app", content))
        has_react = bool(re.search(r"ReactDOM\.render|createRoot", content))
        
        if not has_app_content and not has_vue_app and not has_react:
            issues.append(('empty-app', tool_name, 'Empty #app div with no JS framework'))
            continue
    
    # Check 2: Result div hidden by default, no auto-calc
    # Look for hidden result divs that never get shown on load
    hidden_results = re.findall(r'<div\s+[^>]*style=["\'][^"\']*display:\s*none[^"\']*["\'][^>]*>([^<]{0,50})', content)
    # Look for result containers
    result_divs = re.findall(r'<div\s+id=["\']result["\']\s*[^>]*>', content)
    result_divs2 = re.findall(r'<div\s+id=["\']output["\']\s*[^>]*>', content)
    result_divs3 = re.findall(r'<div\s+id=["\']outputArea["\']\s*[^>]*>', content)
    output_hidden = re.search(r'id=["\']result["\'][^>]*style=["\'][^"\']*display:\s*none', content)
    output_hidden2 = re.search(r'id=["\']output["\'][^>]*style=["\'][^"\']*display:\s*none', content)
    output_hidden3 = re.search(r'style=["\'][^"\']*display:\s*none[^"\']*["\'][^>]*id=["\']result', content)
    output_hidden4 = re.search(r'style=["\'][^"\']*display:\s*none[^"\']*["\'][^>]*id=["\']output', content)
    
    has_hidden_output = output_hidden or output_hidden2 or output_hidden3 or output_hidden4
    has_result_divs = bool(result_divs or result_divs2 or result_divs3)
    
    # Check 3: Calculator with inputs but no auto-calc on load
    has_inputs = bool(re.search(r'<input[^>]*type=["\'](?:number|text)["\']', content))
    has_calc_button = bool(re.search(r'<button[^>]*>.*?(?:计算|Calculate|Calc|Submit)', content, re.IGNORECASE))
    has_auto_calc = bool(re.search(r'addEventListener\s*\(\s*["\']load', content) or 
                          re.search(r'DOMContentLoaded.*calculate|calculate.*DOMContentLoaded', content) or
                          re.search(r'window\.onload.*calculate|calculate.*window\.onload', content) or
                          re.search(r'\.addEventListener\s*\(\s*["\']input["\']', content))
    
    # Check if the page has a default render / initial content
    has_initial_render = bool(re.search(r'innerHTML\s*=|\.text\s*=|\.html\s*=|\.innerText\s*=', content))
    
    # Check 4: Page with no visible body content (no text nodes in body aside from scripts/styles)
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        # Strip scripts, styles, divs that might be containers
        stripped = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
        stripped = re.sub(r'<style[^>]*>.*?</style>', '', stripped, flags=re.DOTALL)
        stripped = re.sub(r'<!--.*?-->', '', stripped, flags=re.DOTALL)
        # Check if there's any visible text content
        text_content = re.sub(r'<[^>]+>', '', stripped).strip()
        if len(text_content) < 10 and has_result_divs and has_hidden_output:
            issues.append(('hidden-result', tool_name, f'Hidden result div, minimal body text: "{text_content[:30]}"'))
            continue
    
    # Specific pattern: calculators where result starts hidden
    if has_hidden_output and has_inputs and has_calc_button and not has_auto_calc:
        issues.append(('calc-hidden', tool_name, 'Calculator with hidden result, no auto-calc'))
        continue
    
    # Pattern: search tools with empty initial state  
    is_search = bool(re.search(r'(?:搜索|Search|查找|Find|查询|Lookup|Query)', content, re.IGNORECASE))
    if is_search and has_hidden_output and not has_initial_render:
        issues.append(('search-empty', tool_name, 'Search tool with hidden results on load'))
        continue

# Print results
print(f"\n=== Found {len(issues)} potential blank-on-load issues ===\n")
for issue_type, name, desc in sorted(issues, key=lambda x: x[1]):
    print(f"[{issue_type}] {name}: {desc}")

# Output as JSON for further processing
with open(os.path.join(TOOL_DIR, '_blank_issues.json'), 'w') as f:
    json.dump([{'type': t, 'name': n, 'desc': d} for t, n, d in issues], f, indent=2)

print(f"\nJSON saved to _blank_issues.json")

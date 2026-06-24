#!/usr/bin/env python3
"""Batch fix hardcoded dark colors → CSS variables for theme toggle support."""
import re
from pathlib import Path

TOOLS_DIR = Path(__file__).parent

DARK_BGS = [
    '#0d1117', '#161b22', '#111', '#111111', '#121212', '#1a1a1a', '#1e1e1e',
    '#222', '#222222', '#2d2d2d', '#1f2937', '#1a1a2e', '#0f0f0f', '#0d0d0d',
    '#0a0a0a', '#181818', '#1c1c1e', '#18181b', '#202020', '#262626',
    '#2a2a2a', '#191919', '#171717', '#141414', '#232323', '#252525',
    '#1b1b1b', '#1a1b1e', '#1c1c2e', '#0e0e12', '#101018', '#0c0c14',
    '#0f1117', '#0a0f1a', '#0d0a17', '#0f0a17', '#0d0221', '#0a0e1a',
    '#0f0b1e', '#0f0f1e', '#0f0f14', '#0a1a10', '#071a18', '#0f1a18',
    '#1c0505', '#1c1008', '#170a1e', '#1a0a14', '#1c1408', '#1a202c',
    '#1a1510', '#1a1612', '#1a1b1e', '#0d1a0d',
]

TEXT_COLORS = [
    '#e6edf3', '#f0f0f0', '#ffffff', '#fff', '#fafafa', '#f5f5f5',
    '#e5e7eb', '#d1d5db', '#e0e0e0', '#eeeeee', '#e8e8e8', '#f8f8f8',
    '#e0f0e0', '#e8d5c0', '#fde68a', '#fbcfe8', '#fed7aa', '#fecaca',
    '#ddd6fe', '#99f6e4', '#ccfbf1', '#bbf7d0', '#f0abfc',
]

def find_root_ranges(content):
    ranges = []
    i = 0
    while i < len(content):
        m = re.search(r':root\s*\{', content[i:])
        if not m:
            break
        start = i + m.start()
        brace_start = i + m.end() - 1
        depth = 1
        j = brace_start + 1
        while j < len(content) and depth > 0:
            if content[j] == '{':
                depth += 1
            elif content[j] == '}':
                depth -= 1
            j += 1
        ranges.append((start, j))
        i = j
    return ranges

def in_root(pos, root_ranges):
    return any(s <= pos < e for s, e in root_ranges)

def fix_tool(tool_dir):
    idx = tool_dir / "index.html"
    if not idx.exists():
        return 0

    content = idx.read_text(encoding="utf-8", errors="replace")
    original = content
    fixes = 0
    root_ranges = find_root_ranges(content)

    def do_replace(pattern, replacement_fn):
        nonlocal content, fixes, root_ranges
        result = []
        last_end = 0
        changed = False
        for m in re.finditer(pattern, content, re.IGNORECASE):
            if not in_root(m.start(), root_ranges):
                result.append(content[last_end:m.start()])
                result.append(replacement_fn(m))
                last_end = m.end()
                changed = True
        if changed:
            result.append(content[last_end:])
            content = ''.join(result)
            fixes += 1
            root_ranges = find_root_ranges(content)

    for bg in DARK_BGS:
        do_replace(r'(background-color\s*:\s*)(' + re.escape(bg) + r')(\s*;)', lambda m: m.group(1) + 'var(--bg)' + m.group(3))
    for bg in DARK_BGS:
        do_replace(r'(background\s*:\s*)(' + re.escape(bg) + r')(\s*;)', lambda m: m.group(1) + 'var(--bg)' + m.group(3))
    for tc in TEXT_COLORS:
        do_replace(r'((?<![\w-])color\s*:\s*)(' + re.escape(tc) + r')(\s*;)', lambda m: m.group(1) + 'var(--text)' + m.group(3))
    for bg in DARK_BGS:
        do_replace(r'((?:background|background-color)\s*:\s*)(' + re.escape(bg) + r')', lambda m: m.group(1) + 'var(--bg)')
    for tc in TEXT_COLORS:
        do_replace(r'((?<![\w-])color\s*:\s*)(' + re.escape(tc) + r')', lambda m: m.group(1) + 'var(--text)')

    if content != original:
        idx.write_text(content, encoding="utf-8")
    return fixes


tool_dirs = sorted([d for d in TOOLS_DIR.iterdir() if d.is_dir() and (d / "index.html").exists()])
print(f"Scanning {len(tool_dirs)} tools...")

total_fixed = 0
fixed_tools = []

for tool_dir in tool_dirs:
    fixes = fix_tool(tool_dir)
    if fixes > 0:
        total_fixed += fixes
        fixed_tools.append((tool_dir.name, fixes))

print(f"\nTools scanned:      {len(tool_dirs)}")
print(f"Tools needing fix:  {len(fixed_tools)}")
print(f"Tools already OK:   {len(tool_dirs) - len(fixed_tools)}")
print(f"Total replacements: {total_fixed}")

if fixed_tools:
    print(f"\nFixed tools ({len(fixed_tools)}):")
    for name, count in sorted(fixed_tools, key=lambda x: -x[1])[:20]:
        print(f"  {name}: {count}")
    if len(fixed_tools) > 20:
        print(f"  ... and {len(fixed_tools) - 20} more")

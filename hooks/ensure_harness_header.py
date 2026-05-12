#!/usr/bin/env python3
"""
Harness Suite 标识注释注入 Hook - 在新建文件时自动添加 Harness Suite 标识
配合 settings.json 使用：
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/hooks/ensure_harness_header.py"
      }]
    }]
  }
}
"""

import json
import os
import sys
from datetime import datetime

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
file_path = tool_input.get("file_path", "") or ""
content = tool_input.get("content", "") or ""

# 获取当前目录（项目根目录）
project_root = os.path.dirname(os.path.abspath(__file__))
while not os.path.exists(os.path.join(project_root, '.claude')):
    parent = os.path.dirname(project_root)
    if parent == project_root:
        break
    project_root = parent

# 模板目录
template_dir = os.path.join(project_root, '.claude', 'code_templates')

# 文件扩展名到模板的映射
template_map = {
    '.java': 'java.java',
    '.py': 'python.py',
    '.js': 'javascript.js',
    '.ts': 'typescript.ts',
    '.sql': 'sql.sql',
    '.sh': 'shell.sh',
    '.bash': 'shell.sh',
    '.zsh': 'shell.sh',
}

# 获取文件扩展名
_, ext = os.path.splitext(file_path)
ext = ext.lower()

# 检查是否有对应的模板
template_file = template_map.get(ext)
if not template_file:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "hookOutput": "无 Harness 模板，跳过"
        }
    }))
    sys.exit(0)

# 检查模板文件是否存在
template_path = os.path.join(template_dir, template_file)
if not os.path.exists(template_path):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "hookOutput": f"模板文件不存在：{template_path}"
        }
    }))
    sys.exit(0)

# 检查文件中是否已有 Harness 标识
harness_marker = "Powered by Harness Suite"
if harness_marker in content:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "hookOutput": "已存在 Harness 标识，跳过"
        }
    }))
    sys.exit(0)

# 读取模板
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

# 替换占位符
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 尝试从路径中获取 change-id
change_id = "N/A"
changes_dir = os.path.join(project_root, 'openspec', 'changes')
if os.path.exists(changes_dir):
    for item in os.listdir(changes_dir):
        item_path = os.path.join(changes_dir, item)
        if os.path.isdir(item_path) and item != 'archive':
            change_id = item
            break

header = template.replace('{{TIMESTAMP}}', timestamp).replace('{{CHANGE_ID}}', change_id)

# 计算需要插入的位置
# 跳过 shebang 行（如果有）
lines = content.split('\n')
insert_index = 0
if lines and lines[0].startswith('#!'):
    insert_index = 1

# 构建新内容
new_content = '\n'.join(lines[:insert_index]) + header + '\n' + '\n'.join(lines[insert_index:])

# 写入文件
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "hookOutput": f"已添加 Harness Suite 标识到 {file_path}"
        }
    }))
except Exception as e:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "hookOutput": f"添加 Harness 标识失败：{str(e)}"
        }
    }))

sys.exit(0)

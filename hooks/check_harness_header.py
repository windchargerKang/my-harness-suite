#!/usr/bin/env python3
"""
Harness Suite 标识检查 Hook - 检查文件是否包含 Harness Suite 标识
用于评审阶段检查代码规范性

配合 settings.json 使用：
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python3 .claude/hooks/check_harness_header.py --check <file-pattern>"
      }]
    }]
  }
}
"""

import json
import os
import sys
import argparse
import fnmatch

# 文件扩展名到模板的映射（需要检查的文件类型）
check_extensions = {
    '.java', '.py', '.js', '.ts', '.sql', '.sh', '.bash', '.zsh'
}

def check_file(file_path):
    """检查单个文件是否包含 Harness 标识"""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext not in check_extensions:
        return None  # 不需要检查的文件类型

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "Powered by Harness Suite" in content:
            return {"status": "pass", "file": file_path}
        else:
            return {"status": "fail", "file": file_path}
    except Exception as e:
        return {"status": "error", "file": file_path, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='检查文件是否包含 Harness Suite 标识')
    parser.add_argument('--check', type=str, help='文件模式，如 "*.java" 或 "src/main/java/**/*.java"')
    parser.add_argument('--dir', type=str, default='.', help='搜索目录')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')

    args = parser.parse_args()

    results = []

    if args.check:
        # 根据文件模式搜索
        base_dir = args.dir
        pattern = args.check

        # 如果是通配符模式，使用 glob 搜索
        if '*' in pattern or '?' in pattern:
            import glob as glob_module
            files = glob_module.glob(os.path.join(base_dir, pattern), recursive=True)
            for file_path in files:
                if os.path.isfile(file_path):
                    result = check_file(file_path)
                    if result:
                        results.append(result)
        else:
            # 直接检查单个文件
            result = check_file(args.check)
            if result:
                results.append(result)
    else:
        # 检查所有支持的文件类型
        for root, dirs, files in os.walk(args.dir):
            # 跳过常见不需要检查的目录
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'target', 'build', '__pycache__', 'venv'}]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in check_extensions:
                    file_path = os.path.join(root, file)
                    result = check_file(file_path)
                    if result:
                        results.append(result)

    # 输出结果
    if args.json:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "results": results,
                "summary": {
                    "total": len(results),
                    "pass": sum(1 for r in results if r["status"] == "pass"),
                    "fail": sum(1 for r in results if r["status"] == "fail"),
                    "error": sum(1 for r in results if r["status"] == "error")
                }
            }
        }))
    else:
        pass_count = sum(1 for r in results if r["status"] == "pass")
        fail_count = sum(1 for r in results if r["status"] == "fail")
        error_count = sum(1 for r in results if r["status"] == "error")

        print(f"\nHarness Suite 标识检查结果:")
        print(f"  总计：{len(results)} 个文件")
        print(f"  通过：{pass_count}")
        print(f"  缺失：{fail_count}")
        print(f"  错误：{error_count}")

        if fail_count > 0:
            print(f"\n以下文件缺少 Harness Suite 标识:")
            for r in results:
                if r["status"] == "fail":
                    print(f"  - {r['file']}")

    sys.exit(0)

if __name__ == '__main__':
    main()

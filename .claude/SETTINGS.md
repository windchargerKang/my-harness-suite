# Claude Code 配置说明

## 配置文件说明

| 文件 | 用途 | 版本控制 |
|------|------|---------|
| `settings.json` | 主配置（commands、hooks） | ✅ 提交到 git |
| `settings.local.json` | 本地覆盖（权限、路径） | ❌ 忽略 |

## 完整配置示例

### settings.json

```json
{
  "commands": {
    "harness": {
      "setup": "harness-setup",
      "propose": "harness-propose",
      "plan": "harness-plan",
      "apply": "harness-apply",
      "review": "harness-review",
      "archive": "harness-archive",
      "knowledge": "harness-knowledge"
    }
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/ensure_harness_header.py"
          }
        ]
      }
    ]
  }
}
```

### settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir -p openspec/changes openspec/specs)"
    ],
    "additionalDirectories": [
      "/absolute/path/to/openspec"
    ]
  }
}
```

## 配置优先级

`settings.local.json` 中的配置会**覆盖** `settings.json` 中的相同字段。

## Hook 不生效的排查步骤

1. **检查 Hook 文件是否存在**
   ```bash
   ls -la .claude/hooks/ensure_harness_header.py
   ```

2. **检查 settings.json 是否有 hooks 配置**
   ```bash
   cat .claude/settings.json | grep -A 10 '"hooks"'
   ```

3. **检查 Hook 文件执行权限**
   ```bash
   chmod +x .claude/hooks/ensure_harness_header.py
   ```

4. **重启 Claude Code 会话**
   - 配置修改后必须重启才能生效

5. **检查 code_templates 目录**
   ```bash
   ls -la .claude/code_templates/
   ```

## .gitignore 配置

确保 `.gitignore` 包含：

```
.claude/settings.local.json
```

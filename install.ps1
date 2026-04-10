# 快速安装 (PowerShell)

```powershell
irm https://raw.githubusercontent.com/your-repo/harness-suite/main/install.ps1 | iex
```

## 参数

| 参数 | 说明 |
|------|------|
| `-SkipSuperpowers` | 跳过 superpowers 安装检查 |
| `-Force` | 强制覆盖已有文件 |
| `-Target <path>` | 指定安装目标目录 |

## 示例

```powershell
# 安装到当前项目
irm https://raw.githubusercontent.com/your-repo/harness-suite/main/install.ps1 | iex

# 强制覆盖安装
irm https://raw.githubusercontent.com/your-repo/harness-suite/main/install.ps1 | iex -Force

# 安装到指定目录
irm https://raw.githubusercontent.com/your-repo/harness-suite/main/install.ps1 | iex -Target "C:\Projects\MyProject"
```

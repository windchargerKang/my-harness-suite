# Harness Suite

基于 OpenSpec 思想 + Superpowers 工作流的轻量级研发规约框架。

## 理念

**战略设计（OpenSpec）** + **战术执行（Superpowers）** = **高效的 AI 辅助开发**

## 安装

### 一键安装

如果你的仓库在私域 Git 上，推荐直接用 `git clone` 拉取仓库后执行本地安装脚本，这样不会遇到 `archive` 下载到 HTML 页而报错的问题。

```bash
git clone --branch main --depth 1 "http://117.159.24.209:30381/root/my-harness-suite" ".harness-suite-tmp" && bash ".harness-suite-tmp/install.sh" --target "$(pwd)" && rm -rf ".harness-suite-tmp"
```

如果你的私域 Git 需要登录或 Token，把仓库地址替换成你自己的可访问地址即可。

或 PowerShell（Windows）：

```powershell
git clone --branch main --depth 1 "http://117.159.24.209:30381/root/my-harness-suite" ".harness-suite-tmp"; powershell -ExecutionPolicy Bypass -File ".harness-suite-tmp\install.ps1" -Target (Get-Location); Remove-Item -Recurse -Force ".harness-suite-tmp"
```

### 参数


| 参数                   | 说明                  |
| -------------------- | ------------------- |
| `--skip-superpowers` | 跳过 superpowers 安装检查 |
| `--force`            | 强制覆盖已有文件            |
| `--target <path>`    | 指定安装目标目录            |


### 安装后

1. 重启 Claude Code 会话使 commands 生效
2. 执行 `/harness-setup` 初始化项目

## 目录结构（源码）

```
harness-suite/
├── setup/                      # 初始化入口
│   └── SKILL.md
├── workflow/                  # 工作流 Skills
│   ├── propose/               # 创建需求
│   ├── plan/                  # 战略设计 + 任务分解
│   ├── apply/                 # 执行实现
│   ├── review/                # 并行评审
│   └── archive/               # 归档
├── review-skills/             # 专项评审
│   ├── prepare-review/        # 变更摘要
│   ├── spring-architecture-review/
│   └── sql-risk-review/
├── agents/
│   └── reviewer.md            # 评审代理
├── hooks/                     # 安全钩子
│   ├── guard_write.py         # 写保护
│   ├── ensure_change_context.py
│   └── run_checks.sh         # 编译检查
├── docs_template/              # 文档模板
│   ├── architecture/
│   ├── product/
│   └── standards/
├── AGENTS.md                  # 代理行为规范
├── CLAUDE.md                  # 技术规约
└── REVIEW.md                  # 评审标准
```

## 快速开始

### 1. 初始化

```bash
# 在项目根目录执行
/harness-setup
```

这将创建完整的规约骨架，并检测安装 Superpowers。

### 2. 创建需求

```bash
/harness-propose 用户登录功能
```

### 3. 战略设计

```bash
/harness-plan user-login-20260409-01
```

调用 `superpowers:brainstorming` 进行深度设计探索，生成 design.md 和 tasks.md。

### 4. 执行实现

```bash
/harness-apply user-login-20260409-01
```

调用 `superpowers:implementing-plans` 按里程碑执行。

### 5. 并行评审

```bash
/harness-review user-login-20260409-01
```

并行执行多个 Review Skill：

- `superpowers:receive-code-review`
- `prepare-review`
- `spring-architecture-review`
- `sql-risk-review`

### 6. 归档

```bash
/harness-archive user-login-20260409-01
```

归档到 `openspec/changes/archive/`。

### 7. 知识管理

```bash
/harness-knowledge              查看所有知识
/harness-knowledge add          添加新知识
/harness-knowledge edit <id>    编辑知识
/harness-knowledge clean        清理过时知识
```

在 **apply** 和 **review** 阶段会自动捕获隐性知识，也支持手动添加。

## 与 Superpowers 的关系


| 阶段  | 调用                                           | 作用         |
| --- | -------------------------------------------- | ---------- |
| 设计  | `superpowers:brainstorming`                  | 深度探索、权衡分析  |
| 执行  | `superpowers:implementing-plans`             | 计划执行、里程碑管理 |
| 验证  | `superpowers:verification-before-completion` | 里程碑检查      |
| 评审  | `superpowers:receive-code-review`            | 代码质量审查     |
| 提交  | `superpowers:requesting-code-review`         | 最终检查       |


## 核心规约

- **AGENTS.md** - 定义代理行为规范和工作流程
- **CLAUDE.md** - 定义技术规约（分层、测试、事务等）
- **REVIEW.md** - 定义评审标准和检查项

## Hooks 配置

将 hooks 集成到 `settings.json`：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "python3 .claude/hooks/guard_write.py"
        }]
      },
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "python3 .claude/hooks/ensure_change_context.py"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "bash .claude/hooks/run_checks.sh"
        }]
      }
    ]
  }
}
```

## 小白使用手册

- [点这里查看《小白使用手册》](./小白使用手册.md)

## License

MIT
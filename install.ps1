param(
    [switch]$SkipSuperpowers,
    [switch]$Force,
    [string]$Target = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success($msg) { Write-Host "[SUCCESS] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Fail($msg) { Write-Host "[ERROR] $msg" -ForegroundColor Red; exit 1 }

Write-Info "Starting Harness Suite installation..."

$ScriptRoot = $PSScriptRoot
if (-not (Test-Path $ScriptRoot)) {
    Write-Fail "Cannot locate script directory. Please run install.ps1 with -File parameter."
}

# Check resource integrity
$requiredPaths = @(
    (Join-Path $ScriptRoot 'setup/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/propose/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/plan/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/apply/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/review/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/archive/SKILL.md'),
    (Join-Path $ScriptRoot 'workflow/knowledge/SKILL.md'),
    (Join-Path $ScriptRoot 'review-skills/prepare-review/SKILL.md'),
    (Join-Path $ScriptRoot 'review-skills/spring-architecture-review/SKILL.md'),
    (Join-Path $ScriptRoot 'review-skills/sql-risk-review/SKILL.md')
)

foreach ($path in $requiredPaths) {
    if (-not (Test-Path $path)) {
        Write-Fail "Installation resources incomplete: missing $path`nPlease download the full repository first."
    }
}

if (-not (Test-Path $Target)) {
    Write-Fail "Target directory does not exist: $Target"
}

$ClaudeDir = Join-Path $Target '.claude'
$SkillsDir = Join-Path $ClaudeDir 'skills'
$AgentsDir = Join-Path $ClaudeDir 'agents'
$HooksDir = Join-Path $ClaudeDir 'hooks'

New-Item -ItemType Directory -Force -Path $ClaudeDir | Out-Null
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
New-Item -ItemType Directory -Force -Path $AgentsDir | Out-Null
New-Item -ItemType Directory -Force -Path $HooksDir | Out-Null

if (-not $SkipSuperpowers) {
    Write-Info "Checking Superpowers..."
    $superpowersGuide = Join-Path $SkillsDir 'superpowers-guide'
    if (Test-Path $superpowersGuide) {
        Write-Success "Superpowers already installed"
    }
    else {
        Write-Warn "Superpowers not detected, recommend installing manually"
    }
}

Write-Info "Copying Skills..."
$skillMap = @{
    'setup/SKILL.md'                                   = 'harness-setup'
    'workflow/propose/SKILL.md'                        = 'harness-propose'
    'workflow/plan/SKILL.md'                           = 'harness-plan'
    'workflow/apply/SKILL.md'                          = 'harness-apply'
    'workflow/review/SKILL.md'                         = 'harness-review'
    'workflow/archive/SKILL.md'                        = 'harness-archive'
    'workflow/knowledge/SKILL.md'                      = 'harness-knowledge'
    'review-skills/prepare-review/SKILL.md'            = 'prepare-review'
    'review-skills/spring-architecture-review/SKILL.md' = 'spring-architecture-review'
    'review-skills/sql-risk-review/SKILL.md'           = 'sql-risk-review'
}

foreach ($entry in $skillMap.GetEnumerator()) {
    $src = Join-Path $ScriptRoot $entry.Key
    $dstDir = Join-Path $SkillsDir $entry.Value
    $dst = Join-Path $dstDir 'SKILL.md'

    New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
    Copy-Item -Path $src -Destination $dst -Force
    Write-Success "Copied $($entry.Value)"
}

Write-Info "Copying Agent and Hooks..."
Copy-Item -Path (Join-Path $ScriptRoot 'agents/reviewer.md') -Destination (Join-Path $AgentsDir 'reviewer.md') -Force
Write-Success "Copied reviewer agent"

$hookFiles = @('guard_write.py', 'ensure_change_context.py', 'run_checks.sh')
foreach ($hook in $hookFiles) {
    $src = Join-Path $ScriptRoot ("hooks/{0}" -f $hook)
    $dst = Join-Path $HooksDir $hook
    Copy-Item -Path $src -Destination $dst -Force
    Write-Success "Copied $hook"
}

Write-Info "Copying specification files..."
$rootFiles = @('AGENTS.md', 'CLAUDE.md', 'REVIEW.md')
foreach ($file in $rootFiles) {
    $src = Join-Path $ScriptRoot $file
    $dst = Join-Path $Target $file
    if ((Test-Path $dst) -and (-not $Force)) {
        Write-Warn "$file already exists, skipping (use -Force to overwrite)"
    }
    else {
        Copy-Item -Path $src -Destination $dst -Force
        Write-Success "Copied $file"
    }
}

Write-Info "Configuring commands..."
$settingsPath = Join-Path $ClaudeDir 'settings.json'
$settingsJson = @'
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
  }
}
'@

if (-not (Test-Path $settingsPath)) {
    Set-Content -Path $settingsPath -Value $settingsJson -Encoding UTF8
    Write-Success "Created settings.json"
}
else {
    Write-Warn ".claude/settings.json already exists, please merge commands manually"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Harness Suite installation completed! " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Restart Cursor/Claude session to activate commands"
Write-Host "  2. Type /harness-setup in chat to initialize project"

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillSource = Join-Path $RepoRoot "interview-notes"
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$TargetDir = Join-Path $CodexHome "skills\interview-notes"

New-Item -ItemType Directory -Force -Path (Join-Path $CodexHome "skills") | Out-Null
if (Test-Path $TargetDir) {
    Remove-Item -Recurse -Force $TargetDir
}
Copy-Item -Recurse -Force $SkillSource $TargetDir

python -m pip install -r (Join-Path $TargetDir "requirements.txt")

Write-Output "Installed interview-notes to:"
Write-Output "  $TargetDir"
Write-Output ""
Write-Output "Core Python dependencies were installed from:"
Write-Output "  $(Join-Path $TargetDir 'requirements.txt')"
Write-Output ""
Write-Output "For audio support, also run:"
Write-Output "  python -m pip install -r `"$($TargetDir)\requirements-audio.txt`""

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DbPath = Join-Path $Root "runtime\engineering_memory.db"

Write-Host "Environment root: $Root"

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    Write-Host "Python launcher: found"
} else {
    Write-Host "Python launcher: missing"
}

$bd = Get-Command bd -ErrorAction SilentlyContinue
if ($bd) {
    Write-Host "Beads bd: found"
    & bd version
} else {
    Write-Host "Beads bd: not installed or not on PATH"
}

if (Test-Path $DbPath) {
    Write-Host "Graph DB: found at $DbPath"
    if ($python) {
        & py -3 (Join-Path $Root "scripts\bootstrap_graph.py") --check
    }
} else {
    Write-Host "Graph DB: not initialized"
}


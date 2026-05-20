param(
    [Parameter(Mandatory = $true)]
    [string]$Destination,

    [Parameter(Mandatory = $true)]
    [string]$TargetProject,

    [Parameter(Mandatory = $true)]
    [string]$ProjectName
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SourceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DestinationPath = [System.IO.Path]::GetFullPath($Destination)
$SourceRootFull = [System.IO.Path]::GetFullPath($SourceRoot)

if ($DestinationPath.StartsWith($SourceRootFull + [System.IO.Path]::DirectorySeparatorChar)) {
    throw "Destination must not be inside the template directory: $DestinationPath"
}

if (Test-Path $DestinationPath) {
    $existing = Get-ChildItem -LiteralPath $DestinationPath -Force
    if ($existing.Count -gt 0) {
        throw "Destination exists and is not empty: $DestinationPath"
    }
} else {
    New-Item -ItemType Directory -Force -Path $DestinationPath | Out-Null
}

$excludeDirs = @(".git", ".beads", ".demo", ".ruff_cache", ".pytest_cache", "__pycache__", "runtime")
$excludeFiles = @("*.pyc", "*.db", "*.sqlite", "*.sqlite3", "*.log")

Get-ChildItem -LiteralPath $SourceRoot -Force | ForEach-Object {
    if ($excludeDirs -contains $_.Name) {
        return
    }
    Copy-Item -LiteralPath $_.FullName -Destination $DestinationPath -Recurse -Force -Exclude $excludeFiles
}

$bootstrap = Join-Path $DestinationPath "scripts\bootstrap_graph.py"
& py -3 $bootstrap --target-project $TargetProject --project-name $ProjectName

Write-Host "Created instance: $DestinationPath"


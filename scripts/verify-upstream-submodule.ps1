$ErrorActionPreference = "Stop"

$submodulePath = "upstream/pyCycle"

if (-not (Test-Path $submodulePath)) {
    throw "Missing upstream submodule at $submodulePath"
}

$submoduleStatus = git -C $submodulePath status --porcelain
if ($submoduleStatus) {
    Write-Error "The upstream submodule has local changes. Do not edit files under $submodulePath."
    $submoduleStatus
    exit 1
}

git diff --quiet -- $submodulePath
if ($LASTEXITCODE -ne 0) {
    Write-Error "The upstream submodule pointer has unstaged changes. Do not update it unless the owner requested an upstream sync."
    exit 1
}

git diff --cached --quiet -- $submodulePath
if ($LASTEXITCODE -ne 0) {
    Write-Error "The upstream submodule pointer has staged changes. Do not update it unless the owner requested an upstream sync."
    exit 1
}

Write-Host "Upstream submodule is clean and unchanged."


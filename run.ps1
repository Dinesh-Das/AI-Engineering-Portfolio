param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $HubArguments
)
$ErrorActionPreference = 'Stop'
$taskRoot = $PSScriptRoot
$taskCandidates = @()
if ($env:AI_PROJECTS_PYTHON) { $taskCandidates += $env:AI_PROJECTS_PYTHON }
if ($env:VIRTUAL_ENV) { $taskCandidates += (Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe') }
$taskCandidates += (Join-Path $taskRoot '.venv\Scripts\python.exe')
$taskUvRoot = Join-Path $env:APPDATA 'uv\python'
if (Test-Path -LiteralPath $taskUvRoot) {
    $taskCandidates += Get-ChildItem -Directory -LiteralPath $taskUvRoot |
        Where-Object { $_.Name -like 'cpython-3.12*' } |
        Sort-Object Name -Descending |
        ForEach-Object { Join-Path $_.FullName 'python.exe' }
}
$taskCommand = Get-Command python -ErrorAction SilentlyContinue
if ($taskCommand -and $taskCommand.Source -notlike '*WindowsApps*') { $taskCandidates += $taskCommand.Source }
$taskPython = $taskCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
if (-not $taskPython) {
    throw 'Python 3.12 is required for collection tooling. Set AI_PROJECTS_PYTHON to a real python.exe path.'
}
Push-Location -LiteralPath $taskRoot
try {
    $taskAction = if ($HubArguments.Count) { $HubArguments[0] } else { '' }
    $taskRest = if ($HubArguments.Count -gt 1) { $HubArguments[1..($HubArguments.Count - 1)] } else { @() }
    switch ($taskAction) {
        'verify' { & $taskPython -m tools.verify_collection @taskRest; $taskExit = $LASTEXITCODE }
        'evaluate' { & $taskPython -m tools.evaluate @taskRest; $taskExit = $LASTEXITCODE }
        'test' {
            & $taskPython -m unittest discover -s tests -v
            $taskExit = $LASTEXITCODE
            if ($taskExit -eq 0) {
                & $taskPython -m unittest discover -s colbert-rag/tests -v
                $taskExit = $LASTEXITCODE
            }
        }
        default { & $taskPython -m tools.hub @HubArguments; $taskExit = $LASTEXITCODE }
    }
} finally {
    Pop-Location
}
exit $taskExit

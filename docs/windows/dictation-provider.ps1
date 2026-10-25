# Select the provider consumed by the repo-owned AutoHotkey startup script.
param(
    [Parameter(Position = 0)]
    [ValidateSet('status', 'wispr', 'windows')]
    [string]$Provider = 'status'
)

$ErrorActionPreference = 'Stop'
$providerDirectory = Join-Path $env:APPDATA 'TalonDictation'
$providerFile = Join-Path $providerDirectory 'provider.txt'

if ($Provider -eq 'status') {
    $savedProvider = 'windows'
    if (Test-Path -LiteralPath $providerFile) {
        $savedProvider = [System.IO.File]::ReadAllText($providerFile).Trim()
    }
    if ($savedProvider -notin @('wispr', 'windows')) {
        throw 'Invalid saved provider. Select wispr or windows.'
    }
    Write-Output $savedProvider
    exit 0
}

# Replace the whole small file so a simultaneous pedal press never sees a
# partial provider name. Selection is local to this machine, outside Git.
[System.IO.Directory]::CreateDirectory($providerDirectory) | Out-Null
$temporaryFile = Join-Path $providerDirectory ([guid]::NewGuid().ToString() + '.tmp')
try {
    [System.IO.File]::WriteAllText($temporaryFile, "$Provider`n", [System.Text.Encoding]::ASCII)
    if (Test-Path -LiteralPath $providerFile) {
        # Windows PowerShell otherwise coerces $null to an empty backup path.
        [System.IO.File]::Replace($temporaryFile, $providerFile, [NullString]::Value)
    } else {
        [System.IO.File]::Move($temporaryFile, $providerFile)
    }
} finally {
    if (Test-Path -LiteralPath $temporaryFile) {
        Remove-Item -LiteralPath $temporaryFile
    }
}
Write-Output $Provider

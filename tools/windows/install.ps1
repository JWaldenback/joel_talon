# Recreate links from this checkout without copying code outside the repo.
param(
    [string]$DesktopDirectory = [Environment]::GetFolderPath('Desktop'),
    [string]$StartupDirectory = [Environment]::GetFolderPath('Startup'),
    [string]$AutoHotkeyPath = ''
)

$ErrorActionPreference = 'Stop'
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
$dictationScript = Join-Path $repoRoot 'plugin\dictation_router\double_tap_control.ahk'
$launchers = @(
    'Talon - Use Wispr',
    'Talon - Use Windows Dictation',
    'Talon - Dictation Status'
)

# Discover the installed interpreter, not whichever .ahk association a new
# machine happens to have. These scripts require the 1.1 runtime.
if (-not $AutoHotkeyPath) {
    $candidates = @(
        (Join-Path $env:ProgramFiles 'AutoHotkey\AutoHotkey.exe'),
        (Join-Path ${env:ProgramFiles(x86)} 'AutoHotkey\AutoHotkey.exe')
    )
    $AutoHotkeyPath = $candidates | Where-Object {
        (Test-Path -LiteralPath $_ -PathType Leaf) -and
        ([Diagnostics.FileVersionInfo]::GetVersionInfo($_).FileMajorPart -eq 1) -and
        ([Diagnostics.FileVersionInfo]::GetVersionInfo($_).FileMinorPart -eq 1)
    } | Select-Object -First 1
}
if (-not $AutoHotkeyPath -or -not (Test-Path -LiteralPath $AutoHotkeyPath -PathType Leaf)) {
    throw 'Install AutoHotkey 1.1, then rerun setup. You can also supply -AutoHotkeyPath.'
}
$AutoHotkeyPath = (Resolve-Path -LiteralPath $AutoHotkeyPath).Path
$version = [Diagnostics.FileVersionInfo]::GetVersionInfo($AutoHotkeyPath)
if ($version.FileMajorPart -ne 1 -or $version.FileMinorPart -ne 1) {
    throw 'This setup requires AutoHotkey 1.1. Supply its executable with -AutoHotkeyPath.'
}

# Check the complete supported set before writing any Desktop or startup links.
$requiredFiles = @(
    $dictationScript,
    (Join-Path $repoRoot 'plugin\dictation_router\dictation_taps.ahk'),
    (Join-Path $repoRoot 'docs\windows\dictation-provider.ps1'),
    (Join-Path $PSScriptRoot 'README.md')
)
foreach ($name in $launchers) {
    $requiredFiles += Join-Path $PSScriptRoot "launchers\$name.cmd"
}
foreach ($path in $requiredFiles) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required repo file is missing: $path"
    }
}

$desktopTools = Join-Path $DesktopDirectory 'Talon tools'
[System.IO.Directory]::CreateDirectory($desktopTools) | Out-Null
[System.IO.Directory]::CreateDirectory($StartupDirectory) | Out-Null
$shell = New-Object -ComObject WScript.Shell
foreach ($name in $launchers) {
    $shortcut = $shell.CreateShortcut((Join-Path $desktopTools "$name.lnk"))
    $shortcut.TargetPath = Join-Path $PSScriptRoot "launchers\$name.cmd"
    $shortcut.WorkingDirectory = $repoRoot
    $shortcut.Description = 'Select or inspect the dictation provider. Works with Talon closed.'
    $shortcut.Save()
}

# Keep the established startup name so rerunning setup cannot add a duplicate
# instance. Do not launch it here or alter an ongoing recording/provider choice.
$startupLink = Join-Path $StartupDirectory 'double-tap-control-dictation.lnk'
$desktopLink = Join-Path $desktopTools 'Talon - Start dictation shortcuts.lnk'
foreach ($path in @($startupLink, $desktopLink)) {
    $shortcut = $shell.CreateShortcut($path)
    $shortcut.TargetPath = $AutoHotkeyPath
    $shortcut.Arguments = '"' + $dictationScript + '"'
    $shortcut.WorkingDirectory = Split-Path -Parent $dictationScript
    $shortcut.Description = 'Run pedal, double left Alt and double Control shortcuts without Talon.'
    $shortcut.WindowStyle = 7
    $shortcut.Save()
}
$catalog = $shell.CreateShortcut((Join-Path $desktopTools 'Talon - Tools guide.lnk'))
$catalog.TargetPath = Join-Path $env:WINDIR 'System32\notepad.exe'
$catalog.Arguments = '"' + (Join-Path $PSScriptRoot 'README.md') + '"'
$catalog.Description = 'Catalog, setup requirements and optional AutoHotkey tools.'
$catalog.Save()

Write-Output "Desktop tools: $desktopTools"
Write-Output "Startup shortcut: $startupLink"
Write-Output 'Provider choice is unchanged. New PCs default to Windows until you select Wispr.'
Write-Output 'Use Start dictation shortcuts now, or sign in again to start them automatically.'

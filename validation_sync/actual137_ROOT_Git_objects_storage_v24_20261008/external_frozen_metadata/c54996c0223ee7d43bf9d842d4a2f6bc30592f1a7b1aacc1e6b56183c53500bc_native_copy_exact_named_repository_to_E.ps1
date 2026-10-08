$ErrorActionPreference='Stop'
$taskSource='D:\3.Study\数据分析\赛题五_GitHub验证同步_20261005'
$taskTarget='E:\赛题五_GitHub验证同步_20261008\验证发布工作副本'
if ((Get-Item -LiteralPath $taskSource).FullName -ne $taskSource) { throw 'Unexpected source path' }
if ((Get-Item -LiteralPath $taskSource).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source must be a physical directory' }
if (Test-Path -LiteralPath $taskTarget) { throw 'Target already exists' }
New-Item -ItemType Directory -Path 'E:\赛题五_GitHub验证同步_20261008' -Force | Out-Null
Copy-Item -LiteralPath $taskSource -Destination $taskTarget -Recurse -Force

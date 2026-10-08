$ErrorActionPreference='Stop'
$taskSource=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects')
$taskBackup=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects_已核验E迁移备份_20261008')
$taskTarget=[IO.Path]::GetFullPath('E:/赛题五_Git对象库_20261008/root_objects')
$taskGitParent=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git')
if ((Get-Item -LiteralPath $taskSource -Force).FullName -ne $taskSource) { throw 'Wrong source path' }
if ((Get-Item -LiteralPath $taskSource -Force).Parent.FullName -ne $taskGitParent) { throw 'Source is outside the exact workspace Git directory' }
if ((Get-Item -LiteralPath $taskSource -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Source is already a junction' }
if (Test-Path -LiteralPath $taskTarget) { throw 'Target already exists' }
New-Item -ItemType Directory -Path (Split-Path -Parent $taskTarget) -Force | Out-Null
Copy-Item -LiteralPath $taskSource -Destination $taskTarget -Recurse -Force

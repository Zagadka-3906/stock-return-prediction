$ErrorActionPreference='Stop'
$taskSource=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects')
$taskBackup=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects_已核验E迁移备份_20261008')
$taskTarget=[IO.Path]::GetFullPath('E:/赛题五_Git对象库_20261008/root_objects')
$taskGitParent=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git')
if ((Get-Item -LiteralPath $taskSource -Force).FullName -ne $taskSource -or (Get-Item -LiteralPath $taskSource -Force).Parent.FullName -ne $taskGitParent) { throw 'Source path changed' }
if (Test-Path -LiteralPath $taskBackup) { throw 'Backup already exists' }
Rename-Item -LiteralPath $taskSource -NewName 'objects_已核验E迁移备份_20261008'
New-Item -ItemType Junction -Path $taskSource -Target $taskTarget | Out-Null

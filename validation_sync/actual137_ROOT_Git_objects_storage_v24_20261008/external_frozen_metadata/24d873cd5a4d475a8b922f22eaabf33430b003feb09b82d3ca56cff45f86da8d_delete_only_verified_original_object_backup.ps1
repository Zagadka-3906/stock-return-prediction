$ErrorActionPreference='Stop'
$taskSource=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects')
$taskBackup=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git/objects_已核验E迁移备份_20261008')
$taskTarget=[IO.Path]::GetFullPath('E:/赛题五_Git对象库_20261008/root_objects')
$taskGitParent=[IO.Path]::GetFullPath('D:/3.Study/数据分析/赛题五/.git')
$taskItem=Get-Item -LiteralPath $taskBackup -Force
if ($taskItem.FullName -ne $taskBackup -or $taskItem.Parent.FullName -ne $taskGitParent) { throw 'Backup outside exact workspace Git directory' }
if ($taskItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Never recursively delete an object junction' }
$taskLink=Get-Item -LiteralPath $taskSource -Force
if (-not ($taskLink.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $taskLink.Target -ne $taskTarget) { throw 'Verified E object database link missing' }
Remove-Item -LiteralPath $taskBackup -Recurse -Force

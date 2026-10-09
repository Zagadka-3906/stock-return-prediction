$ErrorActionPreference = 'Stop'
$workspace = 'D:\3.Study\数据分析\赛题五'
$manifestPath = Join-Path $workspace 'analysis\historical_inactive_browser_cache_candidates_v78_20261009.json'
$resultPath = Join-Path $workspace 'analysis\historical_inactive_browser_cache_cleanup_v78_20261009.json'
if (Test-Path -LiteralPath $resultPath) { throw 'Cleanup already has a durable result.' }
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$cacheRoot = (Resolve-Path -LiteralPath (Join-Path $workspace 'tmp')).ProviderPath
$prefix = $cacheRoot.TrimEnd('\') + '\'
if ($manifest.cache_root -ne $cacheRoot) { throw 'Unexpected cache root.' }
$commands = @(Get-CimInstance Win32_Process | ForEach-Object { [string]$_.CommandLine })
$before = (Get-PSDrive -Name D).Free
$deleted = @()
$skipped = @()
foreach ($target in $manifest.paths) {
    $absolute = [System.IO.Path]::GetFullPath([string]$target)
    if (-not $absolute.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace cache: $absolute" }
    $relative = $absolute.Substring($prefix.Length)
    if ($relative -notmatch '^ranking_display_qa_v\d+_\d{8}\\round(?<round>\d+)\\codex-model-ranking-qa-[A-Za-z0-9_-]+$' -or [int]$Matches.round -gt 153) { throw "Unexpected historical cache shape: $relative" }
    if (-not (Test-Path -LiteralPath $absolute -PathType Container)) { $skipped += @{path=$absolute;reason='already absent'}; continue }
    $active = @($commands | Where-Object { $_.Replace('/', '\').IndexOf($absolute, [System.StringComparison]::OrdinalIgnoreCase) -ge 0 })
    if ($active.Count) { $skipped += @{path=$absolute;reason='live process uses profile'}; continue }
    $item = Get-Item -LiteralPath $absolute -Force
    $contents = @(Get-ChildItem -LiteralPath $absolute -Recurse -Force)
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -or @($contents | Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }).Count) {
        $skipped += @{path=$absolute;reason='reparse entry requires separate inspection'}; continue
    }
    $bytes = [long](($contents | Where-Object { -not $_.PSIsContainer } | Measure-Object -Property Length -Sum).Sum)
    try {
        Remove-Item -LiteralPath $absolute -Recurse -Force
        if (Test-Path -LiteralPath $absolute) { throw 'Cache still exists.' }
        $deleted += @{path=$absolute;bytes=$bytes}
    } catch { $skipped += @{path=$absolute;reason=$_.Exception.Message} }
}
foreach ($entry in $manifest.protected_evidence_sha256.psobject.Properties) {
    $actual = (Get-FileHash -LiteralPath $entry.Name -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) { throw "Protected evidence changed: $($entry.Name)" }
}
$result = @{status='completed_only_inactive_historical_browser_cache_cleanup';at_local=(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss');deleted=$deleted;skipped=$skipped;D_free_before=$before;D_free_after=(Get-PSDrive -Name D).Free;protected_evidence_sha256=$manifest.protected_evidence_sha256;model_and_score_files_deleted=0;application_processes_stopped=0}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resultPath -Encoding UTF8
@{deleted_profiles=$deleted.Count;skipped_profiles=$skipped.Count;D_free_GiB=$result.D_free_after/1GB} | ConvertTo-Json -Compress

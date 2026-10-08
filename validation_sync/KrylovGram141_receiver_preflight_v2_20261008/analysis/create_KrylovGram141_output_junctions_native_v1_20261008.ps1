param([Parameter(Mandatory=$true)][string]$RequestFile)
$ErrorActionPreference='Stop'
$request=Get-Content -LiteralPath $RequestFile -Raw -Encoding utf8 | ConvertFrom-Json
$workspace=[IO.Path]::GetFullPath($request.workspace).TrimEnd('\')+'\'
$taskBase=[IO.Path]::GetFullPath($request.E_base).TrimEnd('\')+'\'
foreach($item in $request.requests){
    $logical=[IO.Path]::GetFullPath($item.logical)
    $target=[IO.Path]::GetFullPath($item.target)
    if(-not $logical.StartsWith($workspace,[StringComparison]::OrdinalIgnoreCase)){throw 'Logical output escapes workspace'}
    if(-not $target.StartsWith($taskBase,[StringComparison]::OrdinalIgnoreCase)){throw 'Target escapes exact141 base'}
    if((Test-Path -LiteralPath $logical) -or (Test-Path -LiteralPath $target)){throw 'Never reuse an existing output'}
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($logical)) | Out-Null
    [IO.Directory]::CreateDirectory($target) | Out-Null
    New-Item -ItemType Junction -Path $logical -Target $target -ErrorAction Stop | Out-Null
}

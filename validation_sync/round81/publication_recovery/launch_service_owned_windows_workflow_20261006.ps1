param([Parameter(Mandatory=$true)][string]$DefinitionPath)
$ErrorActionPreference = 'Stop'
$taskDefinitionItem = Get-Item -LiteralPath $DefinitionPath
$taskDefinition = Get-Content -LiteralPath $taskDefinitionItem.FullName -Raw | ConvertFrom-Json
$taskRoot = 'D:\3.Study\数据分析\赛题五'
if (-not $taskDefinitionItem.FullName.StartsWith($taskRoot + '\analysis\')) { throw 'Definition outside project analysis directory' }
if (Test-Path -LiteralPath (Join-Path $taskDefinitionItem.DirectoryName 'launch_result.json')) { throw 'Workflow was already submitted' }
$taskBootstrap = Join-Path $taskRoot 'analysis\run_service_owned_windows_workflow_20261006.py'
if ((Get-FileHash -LiteralPath $taskBootstrap -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskDefinition.bootstrap_sha256) { throw 'Bootstrap source changed' }
$taskStartup = New-CimInstance -Namespace root/cimv2 -ClassName Win32_ProcessStartup -ClientOnly -Property @{ CreateFlags = [uint32]150994944; ShowWindow = [uint16]0 }
$taskResult = Invoke-CimMethod -Namespace root/cimv2 -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $taskDefinition.command_line; CurrentDirectory = $taskRoot; ProcessStartupInformation = $taskStartup }
$taskResult | Select-Object ReturnValue,ProcessId | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskDefinitionItem.DirectoryName 'launch_result.json') -Encoding utf8
if ($taskResult.ReturnValue -ne 0) { throw "Native workflow creation failed: $($taskResult.ReturnValue)" }
$taskResult | Select-Object ReturnValue,ProcessId | ConvertTo-Json

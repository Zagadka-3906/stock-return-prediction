param([string]$OutputPath)
$ErrorActionPreference = 'Stop'
$taskCpu = @(Get-CimInstance Win32_Processor | ForEach-Object {
    [ordered]@{name=$_.Name; physical_cores=$_.NumberOfCores; logical_processors=$_.NumberOfLogicalProcessors}
})
$taskMemory = Get-CimInstance Win32_ComputerSystem
$taskDisks = @(Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Name -in @('D','E') } | ForEach-Object {
    [ordered]@{drive=$_.Name; free_GiB=[math]::Round($_.Free/1GB,2); used_GiB=[math]::Round($_.Used/1GB,2)}
})
$taskGpu = [ordered]@{available=$false; inventory=$null; error=$null}
$taskSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($taskSmi) {
    $taskInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $taskInfo.FileName = $taskSmi.Source
    $taskInfo.Arguments = '--query-gpu=name,memory.total,driver_version --format=csv,noheader'
    $taskInfo.UseShellExecute = $false
    $taskInfo.CreateNoWindow = $true
    $taskInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
    $taskInfo.RedirectStandardOutput = $true
    $taskInfo.RedirectStandardError = $true
    $taskProcess = [System.Diagnostics.Process]::new()
    $taskProcess.StartInfo = $taskInfo
    try {
        [void]$taskProcess.Start()
        $taskStdout = $taskProcess.StandardOutput.ReadToEndAsync()
        $taskStderr = $taskProcess.StandardError.ReadToEndAsync()
        if (-not $taskProcess.WaitForExit(15000)) {
            $taskProcess.Kill()
            $taskProcess.WaitForExit()
            $taskGpu.error = 'The hardware inventory command exceeded15seconds; no training process was touched.'
        } else {
            $taskGpu.available = $taskProcess.ExitCode -eq 0
            $taskGpu.inventory = $taskStdout.Result.Trim()
            $taskGpu.error = $taskStderr.Result.Trim()
        }
    } finally { $taskProcess.Dispose() }
}
$taskReport = [ordered]@{
    status='hardware_inventory_only_no_training_or_installation'
    at_local=(Get-Date).ToString('o')
    cpu=$taskCpu
    memory_GiB=[math]::Round($taskMemory.TotalPhysicalMemory/1GB,2)
    nvidia_gpu=$taskGpu
    authorized_data_drives=$taskDisks
    powershell_version=$PSVersionTable.PSVersion.ToString()
    benchmark_performed=$false
}
$taskJson = $taskReport | ConvertTo-Json -Depth 8
if ($OutputPath) {
    $taskTarget = [System.IO.Path]::GetFullPath($OutputPath)
    $taskRoot = [System.IO.Path]::GetPathRoot($taskTarget)
    if ($taskRoot -notin @('D:\','E:\')) { throw 'Save the hardware report onD: orE:.' }
    if (Test-Path -LiteralPath $taskTarget) { throw 'The report already exists; use a new output filename.' }
    [void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($taskTarget))
    [System.IO.File]::WriteAllText($taskTarget,$taskJson+[Environment]::NewLine,[System.Text.UTF8Encoding]::new($false))
}
$taskJson

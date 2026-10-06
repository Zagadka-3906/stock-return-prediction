param(
    [Parameter(Mandatory=$true)][ValidateSet('worker1','worker2')][string]$WorkerId,
    [string]$WorkRoot='D:\赛题五协作',
    [string]$PythonExe
)
$ErrorActionPreference='Stop'
$taskRoot=[System.IO.Path]::GetFullPath($WorkRoot)
$taskDrive=[System.IO.Path]::GetPathRoot($taskRoot)
if ($taskDrive -notin @('D:\','E:\')) { throw 'Use a worker folder on D: or E:.' }
foreach ($taskFolder in @('tmp','pip-cache','data','tasks','results','reports','logs')) {
    [void][System.IO.Directory]::CreateDirectory((Join-Path $taskRoot $taskFolder))
}
# These apply only to this PowerShell session and its child processes.
$env:TEMP=Join-Path $taskRoot 'tmp'
$env:TMP=$env:TEMP
$env:TMPDIR=$env:TEMP
$env:PIP_CACHE_DIR=Join-Path $taskRoot 'pip-cache'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONUTF8='1'
$env:OMP_NUM_THREADS='4'
$env:OPENBLAS_NUM_THREADS='4'
$env:MKL_NUM_THREADS='4'
$env:POLARS_MAX_THREADS='4'
$taskStamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$taskHardware=Join-Path $taskRoot ('reports\'+$WorkerId+'_hardware_'+$taskStamp+'.json')
& (Join-Path $PSScriptRoot 'inspect_worker_hardware.ps1') -OutputPath $taskHardware
$taskVenvPython=Join-Path $taskRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskVenvPython)) {
    if ($PythonExe) {
        if (-not (Test-Path -LiteralPath $PythonExe)) { throw 'The supplied Python executable does not exist.' }
        $taskVersion=& $PythonExe -c 'import sys; print(str(sys.version_info.major)+chr(46)+str(sys.version_info.minor))'
        if ($LASTEXITCODE -ne 0 -or $taskVersion.Trim() -ne '3.12') { throw 'Use Python3.12 64-bit.' }
        & $PythonExe -m venv (Join-Path $taskRoot '.venv')
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3.12 -m venv (Join-Path $taskRoot '.venv')
    } else {
        throw 'Install Python3.12 64-bit, then rerun with -PythonExe D:\Python312\python.exe .'
    }
    if ($LASTEXITCODE -ne 0) { throw 'Python3.12 virtual environment creation failed.' }
}
$taskVersion=& $taskVenvPython -c 'import sys; print(str(sys.version_info.major)+chr(46)+str(sys.version_info.minor)); print(64 if sys.maxsize>2**32 else 32)'
if ($LASTEXITCODE -ne 0 -or $taskVersion[0].Trim() -ne '3.12' -or $taskVersion[1].Trim() -ne '64') {
    throw 'The worker virtual environment must be Python3.12 64-bit.'
}
& $taskVenvPython -m pip install --only-binary=:all: -r (Join-Path $PSScriptRoot 'requirements-worker-core.txt')
if ($LASTEXITCODE -ne 0) { throw 'Core dependency installation failed; retain this output and report it.' }
& $taskVenvPython -m pip install --only-binary=:all: 'torch==2.11.0+cu128' --index-url 'https://download.pytorch.org/whl/cu128'
if ($LASTEXITCODE -ne 0) { throw 'GPU PyTorch installation failed; retain this output and report it.' }
$taskReport=Join-Path $taskRoot ('reports\'+$WorkerId+'_environment_'+$taskStamp+'.json')
& $taskVenvPython -B -X utf8 (Join-Path $PSScriptRoot 'verify_worker_environment.py') --worker-id $WorkerId --output $taskReport
if ($LASTEXITCODE -ne 0) { throw ('Worker environment check failed; send report: '+$taskReport) }
Write-Host ('READY: '+$taskRoot)
Write-Host ('Report: '+$taskReport)
Write-Host 'The worker is prepared; actual training tasks and data will be assigned separately.'

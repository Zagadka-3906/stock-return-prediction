"""Build a portable preparation kit; never install or train on the current host."""
from pathlib import Path
import hashlib
import html
import json
import shutil
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
OUT = A / 'cooperation_worker_usb_v1_20261006'
KIT = OUT / '赛题五双机准备包'
BOOT = A / 'cooperation_worker_bootstrap_20261006'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024**2), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    assert not OUT.exists()
    KIT.mkdir(parents=True)
    boot_manifest = json.loads((BOOT / 'manifest.json').read_text(encoding='utf-8'))
    for name in ('prepare_worker_environment.ps1', 'inspect_worker_hardware.ps1',
                 'verify_worker_environment.py', 'requirements-worker-core.txt',
                 'manifest.json', '准备说明.txt'):
        shutil.copyfile(BOOT / name, KIT / name)
    # Windows PowerShell 5.1 needs a BOM to read Chinese literals consistently.
    for path in KIT.glob('*.ps1'):
        original = path.read_text(encoding='utf-8-sig')
        path.write_text(original, encoding='utf-8-sig', newline='\r\n')
    launcher = r'''param(
    [Parameter(Mandatory=$true)][ValidateSet('worker1','worker2')][string]$WorkerId,
    [string]$WorkRoot='D:\赛题五协作'
)
$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath($WorkRoot)
$taskDrive=[IO.Path]::GetPathRoot($taskRoot)
if ($taskDrive -notin @('D:\','E:\')) { throw 'WorkRoot must be on D: or E:.' }
foreach ($taskName in @('tmp','pip-cache','logs','reports')) {
    [void][IO.Directory]::CreateDirectory((Join-Path $taskRoot $taskName))
}
$env:TEMP=Join-Path $taskRoot 'tmp'
$env:TMP=$env:TEMP
$env:TMPDIR=$env:TEMP
$env:PIP_CACHE_DIR=Join-Path $taskRoot 'pip-cache'
$taskStamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$taskLog=Join-Path $taskRoot ('logs\'+$WorkerId+'_setup_'+$taskStamp+'.log')
$taskTranscript=$false
$taskExit=1
try {
    Start-Transcript -LiteralPath $taskLog -ErrorAction Stop | Out-Null
    $taskTranscript=$true
    $taskManifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'USB文件校验.json') -Encoding UTF8 -Raw | ConvertFrom-Json
    foreach ($taskProperty in $taskManifest.files.PSObject.Properties) {
        $taskFile=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot $taskProperty.Name))
        if (-not $taskFile.StartsWith($PSScriptRoot+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Invalid manifest path.' }
        if ((Get-FileHash -LiteralPath $taskFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskProperty.Value.sha256) { throw ('Package checksum failed: '+$taskProperty.Name) }
    }
    $taskPython=Join-Path $taskDrive 'Python312\python.exe'
    if (-not (Test-Path -LiteralPath $taskPython)) {
        $taskInstaller=Join-Path $PSScriptRoot 'python-3.12.9-amd64.exe'
        $taskSignature=Get-AuthenticodeSignature -LiteralPath $taskInstaller
        if ($taskSignature.Status -ne 'Valid' -or $taskSignature.SignerCertificate.Subject -notmatch 'Python Software Foundation') { throw 'Python installer signature is not valid; send this error.' }
        Write-Host ('Installing Python into '+(Join-Path $taskDrive 'Python312'))
        $taskInstallerArgs=@('/passive','InstallAllUsers=0',('TargetDir='+$taskDrive+'Python312'),
            'Include_launcher=0','Include_test=0','Include_pip=1','PrependPath=0','AssociateFiles=0','Shortcuts=0')
        $taskProcess=Start-Process -FilePath $taskInstaller -ArgumentList $taskInstallerArgs -Wait -PassThru
        if ($taskProcess.ExitCode -notin @(0,3010)) { throw ('Python installation failed: '+$taskProcess.ExitCode) }
        if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Python executable not found after installation. See the running guide.' }
    }
    & (Join-Path $PSScriptRoot 'prepare_worker_environment.ps1') -WorkerId $WorkerId -WorkRoot $taskRoot -PythonExe $taskPython
    Write-Host ('SUCCESS: '+$WorkerId+' is ready. Collect reports using the matching collect CMD file.')
    $taskExit=0
} catch {
    Write-Host ('FAILED: '+$_.Exception.Message) -ForegroundColor Red
    Write-Host ('Keep this log and return it to the main computer: '+$taskLog)
} finally {
    if ($taskTranscript) { Stop-Transcript | Out-Null }
}
exit $taskExit
'''
    (KIT / 'run_worker_setup.ps1').write_text(launcher, encoding='utf-8-sig', newline='\r\n')
    collector = r'''param(
    [Parameter(Mandatory=$true)][ValidateSet('worker1','worker2')][string]$WorkerId,
    [string]$WorkRoot='D:\赛题五协作',
    [string]$UsbDrive
)
$ErrorActionPreference='Stop'
$taskRoot=[IO.Path]::GetFullPath($WorkRoot)
if ([IO.Path]::GetPathRoot($taskRoot) -notin @('D:\','E:\')) { throw 'WorkRoot must be on D: or E:.' }
if (-not $UsbDrive) { $UsbDrive=Read-Host 'USB drive letter on THIS computer (example F)' }
$taskLetter=$UsbDrive.Trim().TrimEnd('\').TrimEnd(':').ToUpperInvariant()
if ($taskLetter -notmatch '^[A-Z]$' -or $taskLetter -in @('C','D','E')) { throw 'Enter the actual USB drive letter, not C/D/E.' }
$taskDevice=$taskLetter+':'
$taskDisk=Get-CimInstance Win32_LogicalDisk -Filter ("DeviceID='"+$taskDevice+"'")
if (-not $taskDisk) { throw 'The drive is not connected.' }
$taskUsb=$taskDisk.DriveType -eq 2
if (-not $taskUsb) {
    $taskPhysical=Get-Partition -DriveLetter $taskLetter | Get-Disk
    $taskUsb=$taskPhysical.BusType -eq 'USB'
}
if (-not $taskUsb) { throw 'The destination is not a removable/USB drive.' }
$taskFolder=Join-Path ($taskDevice+'\') ('赛题五协作回传\'+$WorkerId+'\'+$env:COMPUTERNAME+'_'+(Get-Date -Format 'yyyyMMdd_HHmmss'))
if (Test-Path -LiteralPath $taskFolder) { throw 'Report destination already exists.' }
$taskFiles=@()
foreach ($taskKind in @('hardware','environment')) {
    $taskLatest=Get-ChildItem -LiteralPath (Join-Path $taskRoot 'reports') -Filter ($WorkerId+'_'+$taskKind+'_*.json') -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($taskLatest) { $taskFiles+= $taskLatest } else { Write-Warning ('No '+$taskKind+' report found.') }
}
$taskLatest=Get-ChildItem -LiteralPath (Join-Path $taskRoot 'logs') -Filter ($WorkerId+'_setup_*.log') -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($taskLatest) { $taskFiles+=$taskLatest }
if ($taskFiles.Count -eq 0) { throw 'No reports/logs found. Run preparation first or check WorkRoot.' }
[void][IO.Directory]::CreateDirectory($taskFolder)
foreach ($taskFile in $taskFiles) {
    $taskDestination=Join-Path $taskFolder $taskFile.Name
    Copy-Item -LiteralPath $taskFile.FullName -Destination $taskDestination -ErrorAction Stop
    if ((Get-FileHash -LiteralPath $taskFile.FullName).Hash -ne (Get-FileHash -LiteralPath $taskDestination).Hash) { throw 'Report copy checksum failed.' }
}
Write-Host ('REPORTS COPIED: '+$taskFolder)
Write-Host 'Safely eject the USB drive, then connect it to the main computer.'
'''
    (KIT / 'collect_worker_reports.ps1').write_text(collector, encoding='utf-8-sig', newline='\r\n')
    for worker in ('worker1', 'worker2'):
        for mode, script in (('prepare', 'run_worker_setup.ps1'), ('collect', 'collect_worker_reports.ps1')):
            cmd = (f'@echo off\nsetlocal\npowershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0{script}" -WorkerId {worker}\n'
                   'set "RESULT=%ERRORLEVEL%"\necho.\necho Exit code: %RESULT% (0 means success)\npause\nexit /b %RESULT%\n')
            (KIT / f'{mode}_{worker}.cmd').write_text(cmd, encoding='ascii', newline='\r\n')
    guide = '''赛题五：两台电脑协作准备与运行说明
版本：2026-10-06，USB v1

一、这次需要做什么
把本文件夹复制到两台电脑的 D 盘，分别双击对应的准备入口。
检查成功后，把报告用 U 盘带回主机。环境确认后才会分发正式训练任务。
本包不是正式训练任务包：包含 Python 安装器和环境准备工具；Python 依赖仍需联网下载。

二、电脑编号
电脑1：worker1，R9-8940HX、32GB、RTX5070 Laptop 8GB；用户提供的地址按顺序对应 10.0.0.112。
电脑2：worker2，R9-8940HX、16GB、RTX5060 Laptop 8GB；按顺序对应 10.0.0.162。
如果地址与实际电脑相反，以内存和显卡确定编号，并在回传时说明；地址可能由路由器重新分配。
不要在当前主机运行这两个准备入口。

三、运行前
1. 两台电脑都插电、联网，保持散热；在 Windows 设置→系统→电源和电池→屏幕/睡眠中，把“插电时让设备进入睡眠”改为“从不”。屏幕可以关闭。
2. 将 U 盘中的整个“赛题五双机准备包”文件夹复制到 D:\赛题五双机准备包。
   U 盘在另一台电脑上未必也是 F 盘，以“此电脑”显示为准。
3. 准备过程需要数 GB 下载和更多解压空间。建议 D 盘留出至少 20 GB 用于环境；后续训练所需空间另行按任务测量，尽量保留 50 GB 或更多。
4. 关闭其他占用 GPU 的游戏等程序。同一台电脑一次运行一个准备入口。

四、双击开始
电脑1双击：prepare_worker1.cmd。
电脑2双击：prepare_worker2.cmd。
脚本首先检查整个包的 SHA-256；若缺少 D:\Python312\python.exe，会核验安装器签名并安装 Python3.12.9 64位到 D:\Python312。
随后创建 D:\赛题五协作\.venv，安装固定版本 CPU/数据处理依赖及 torch2.11.0+cu128，并进行一次小型 CUDA 前向/反向检查。
Python 安装界面和一个命令窗口是这一步主动打开的正常界面。下载期间保持窗口开启，等待返回，不要重复启动。
完成时间取决于网络、驱动和硬盘速度，不把准备时间作为训练速度预测。

成功标志：出现 SUCCESS: worker1/worker2 is ready，窗口末尾 Exit code: 0。
失败标志：出现 FAILED 或 Exit code 非0；保留日志，不要删除目录。继续按第五节回传已有报告和日志。
所有项目环境、临时文件、依赖缓存、日志和结果都放在 D:\赛题五协作；Python 安装目录为 D:\Python312。Windows 自身的安装注册信息和系统组件仍由系统管理。
脚本不要求管理员权限；组织策略或安装限制导致失败时回传报错，先不要修改全局执行策略。

五、把报告带回主机
1. 准备窗口结束后，插入 U 盘。
2. 电脑1双击 collect_worker1.cmd，电脑2双击 collect_worker2.cmd。
3. 输入这台电脑实际显示的 U 盘盘符，例如 F，按回车。不要输入 C、D 或 E。
4. 报告会复制到 U 盘的“赛题五协作回传\worker1或worker2\电脑名_时间”目录，并校验复制后的哈希。
   内容为最新硬件报告、最新环境报告和本次安装日志；失败时可能只有其中一部分。
5. 安全弹出 U 盘，带回当前主机插上，告诉我“两台报告已放回 U 盘”。我会读取报告再分发独立任务。
手动回传也可以：复制 D:\赛题五协作\reports 中最新的两个 JSON，以及 logs 中最新的对应 worker 安装日志到 U 盘。

六、如果改用 E 盘
双击入口默认使用 D 盘。要改为 E 盘，在本包文件夹中打开 PowerShell，运行对应命令：
电脑1：powershell -NoProfile -ExecutionPolicy Bypass -File .\run_worker_setup.ps1 -WorkerId worker1 -WorkRoot "E:\赛题五协作"
电脑2：powershell -NoProfile -ExecutionPolicy Bypass -File .\run_worker_setup.ps1 -WorkerId worker2 -WorkRoot "E:\赛题五协作"
回传：powershell -NoProfile -ExecutionPolicy Bypass -File .\collect_worker_reports.ps1 -WorkerId worker1 -WorkRoot "E:\赛题五协作"
电脑2将回传命令中的 worker1 改成 worker2。此时 Python 自动安装到 E:\Python312，项目环境和缓存也在 E 盘。

七、常见问题
下载超时/网络连接失败：保留窗口报错和日志；网络恢复后可重跑同一个准备入口，已有环境会复用，pip 会检查已安装依赖。
包文件校验失败：重新复制整个包，勿只复制某个脚本，也不要修改包内文件。
CUDA unavailable / GPU 检查失败：回传 JSON 和日志，先核实 NVIDIA 驱动；本包不自动改装驱动。
现有 D:\Python312 不是3.12或不是64位：回传报错；不要直接覆盖或删除已有 Python 目录。
PowerShell 窗口关闭太快：CMD入口会暂停；从相应 logs 文件查看完整报错。
没有正式任务运行：环境准备成功只证明环境可用，不代表训练已开始。等待任务包和固定任务编号。

八、后续三台电脑如何分工
当前主机统一分发固定编号的任务，管理训练集内部连续向前验证、官方评分、因果检查、候选冻结、完整榜，以及 GitHub main 提交。
电脑1优先分配内存需求较大的独立训练；电脑2先一次运行一个受内存约束的任务。实际任务需先测量显存、内存和耗时，不能根据显卡型号承诺加速比例。
两台电脑分别写入自己的 tasks/results/logs 子目录；不要同时改同一个结果文件，不自行更改划分、评分或固定参数。
只复制所需的训练数据和固定参数；真实测试标签不分发。只有主机更新 GitHub main，避免多机同时提交冲突。
准备包不需要登录 GitHub，不开启网络共享，不修改防火墙，不复制当前主机的虚拟环境。

九、文件入口速查
prepare_worker1.cmd / prepare_worker2.cmd：准备环境。
collect_worker1.cmd / collect_worker2.cmd：回传检查报告。
运行说明.txt：本说明，可用记事本打开。
运行说明.html：同内容网页，可在浏览器中打开或打印。
USB文件校验.json：全包 SHA-256清单，由准备入口自动校验。
python-3.12.9-amd64.exe：Python 官方64位安装器。

Python 官方来源：https://www.python.org/downloads/release/python-3129/
GPU依赖下载索引：https://download.pytorch.org/whl/cu128
原始准备包已同步 GitHub main：https://github.com/Zagadka-3906/stock-return-prediction/tree/main/validation_sync/cooperation_worker_bootstrap_20261006
'''
    (KIT / '运行说明.txt').write_text(guide, encoding='utf-8-sig', newline='\r\n')
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>赛题五双机准备与运行说明</title><style>body{max-width:900px;margin:32px auto;padding:0 24px;font:16px/1.8 system-ui,"Microsoft YaHei",sans-serif;color:#17202a}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit}@media print{body{margin:0;max-width:none}}</style><body><pre>' + html.escape(guide) + '</pre></body></html>'
    (KIT / '运行说明.html').write_text(document, encoding='utf-8')
    shutil.copyfile(A / 'cooperation_worker_bootstrap_20261006.zip', KIT / '原始准备包.zip')
    (OUT / 'build_preparation.json').write_text(json.dumps({
        'status': 'prepared_sources_and_running_guide_installer_download_pending',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'original_source_sha256': {str(p): sha(p) for p in BOOT.iterdir() if p.is_file()},
        'build_source_sha256': sha(__file__), 'kit': str(KIT),
        'worker_installation_or_training_performed': False,
        'original_bootstrap_manifest': boot_manifest,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print(str(KIT))


if __name__ == '__main__':
    main()

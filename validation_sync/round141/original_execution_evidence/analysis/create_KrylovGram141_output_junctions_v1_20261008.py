"""Create six exact empty141 output junctions with checked D/E boundaries and no deletion."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create

def main():
    from KrylovGram141_storage_v1_20261008 import OUTPUTS,EBASE,empty
    request=A/'KrylovGram141_junction_requests_v1_20261008.json';rows=read(request)['requests']
    assert len(rows)==6 and {(Path(r['logical']),Path(r['target'])) for r in rows}==set(OUTPUTS.items())
    for logical,target in OUTPUTS.items():
        assert logical.is_absolute() and logical.parent.resolve().is_relative_to(ROOT.resolve()) and logical.drive.upper()=='D:'
        assert target.is_absolute() and target.resolve().is_relative_to(EBASE.resolve()) and target.drive.upper()=='E:'
        assert not logical.exists() and not target.exists(),(logical,target)
    script=A/'create_KrylovGram141_output_junctions_native_v1_20261008.ps1';assert not script.exists()
    script.write_text('''param([Parameter(Mandatory=$true)][string]$RequestFile)
$ErrorActionPreference='Stop'
$request=Get-Content -LiteralPath $RequestFile -Raw -Encoding utf8 | ConvertFrom-Json
$workspace=[IO.Path]::GetFullPath($request.workspace).TrimEnd('\\')+'\\'
$taskBase=[IO.Path]::GetFullPath($request.E_base).TrimEnd('\\')+'\\'
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
''',encoding='utf8',newline='\n')
    pwsh=Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
    result=subprocess.run([str(pwsh),'-NoLogo','-NoProfile','-NonInteractive','-File',str(script),str(request)],capture_output=True,text=True,encoding='utf8',errors='replace',timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    assert result.returncode==0,(result.stdout,result.stderr)
    for path in OUTPUTS:empty(path)
    create(A/'KrylovGram141_output_junction_admission_v1_20261008.json',{
        'status':'passed_exact_six_empty_D_logical_E_physical_output_junctions_before_quality',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),script,request,A/'KrylovGram141_storage_v1_20261008.py']},
        'requests':rows,'recursive_deletes_or_moves':0,'visible_windows':0,'new_official_scores':0,'test_labels_read':False})
    print('Six exact empty141 E-output junctions created and independently resolved.',flush=True)

if __name__=='__main__':main()

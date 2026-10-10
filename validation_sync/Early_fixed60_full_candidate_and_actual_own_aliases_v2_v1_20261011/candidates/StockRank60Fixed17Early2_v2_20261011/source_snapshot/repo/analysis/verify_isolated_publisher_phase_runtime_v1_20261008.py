"""Reproduce two real hidden Git processes using the same parent scratch with distinct phases."""
from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
OUT=Path('E:/赛题五_本机临时/isolated_publisher_phase_actual_preflight_v1_20261008')


def child(phase):
    import ctypes
    import verified_TLS_Git_retry_runtime_v2_20261008 as runtime
    from isolated_publisher_phase_runtime_v1_20261008 import installed_phase
    import publish_classifier_consensus_workflows_20261006 as helpers
    original=runtime.installed
    assert ctypes.windll.kernel32.GetConsoleWindow()==0
    with installed_phase(phase):
        with runtime.installed(OUT/'same_parent_scratch'):
            version=helpers.sync.git('--version')
            assert version.startswith('git version ')
    assert runtime.installed is original
    print(json.dumps({'phase':phase,'git_version':version,'actual_native_console_handle':0,'original_TLS_runtime_restored':True}),flush=True)


def main():
    OUT.mkdir(exist_ok=False)
    results=[]
    for phase in ('controls','scores'):
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(Path(__file__)),'--phase',phase],
            cwd=ROOT,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr
        value=json.loads(result.stdout.strip());results.append(value)
        path=OUT/'same_parent_scratch'/('phase_'+phase+'_scope_v1')
        execution=read(path/'execution.json')
        assert len(execution['calls'])==1 and execution['calls'][0]['arguments']==['--version']
        assert execution['calls'][0]['exit_code']==0
        assert read(path/'actual_verified_TLS_transport_retries.json')['TLS_verification_disabled'] is False
    assert results[0]['git_version']==results[1]['git_version']
    pins={str(path):sha(path) for path in (Path(__file__),A/'isolated_publisher_phase_runtime_v1_20261008.py',
        A/'verified_TLS_Git_retry_runtime_v2_20261008.py',A/'file_backed_hidden_git_runtime_20261007.py')}
    proof=OUT/'verification.json'
    create(proof,{'status':'passed_actual_two_hidden_Git_processes_same_parent_scratch_distinct_phase_directories_and_original_TLS_runtime_restored',
        'input_sha256':pins,'records':results,'actual_fresh_native_processes':2,
        'actual_read_only_Git_calls':2,'network_or_remote_write_commands':0,
        'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_isolated_publisher_phase_preflight_v1_20261008.json',{'output':str(OUT),'verification_sha256':sha(proof)})
    print({'status':'two_actual_phase_processes_passed','output':str(OUT)},flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('controls','scores'))
    args=parser.parse_args()
    if args.phase:child(args.phase)
    else:main()

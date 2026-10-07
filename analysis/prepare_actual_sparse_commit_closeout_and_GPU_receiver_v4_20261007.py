"""Launch exact-commit closure and a fresh GPU-evidence receiver; retain both failures."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v2_20261007.py';new=A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v3_20261007.py'
    text=old.read_text(encoding='utf8').replace('actual_sparse_and_isolated_scoring_controls_main_publication_v3','actual_sparse_committed_main_recovery_v4').replace('actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v2_20261007','actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v3_20261007')
    extras=[Path(__file__),old,A/'close_actual_sparse_committed_main_after_server_error_v4_20261007.py',A/'actual_sparse_and_isolated_scoring_controls_github_recovery_v4_20261007/receipt.json']
    for name in ['actual_sparse_and_isolated_scoring_controls_main_publication_v3','actual_GPU_shared_allocation_and_manual_bench_main_publication_v2']:
        folder=A/'service_owned_workflows_20261006'/name;assert read(folder/'service_execution.json')['status']=='failed'
        extras.extend([*folder.glob('*.json'),*folder.glob('*.log')])
    needle='    sources=list(dict.fromkeys(sources));';assert text.count(needle)==1
    text=text.replace(needle,"    sources += ["+','.join('A/'+repr(p.relative_to(A).as_posix()) for p in extras)+"]\n"+needle)
    text=text.replace("'connection','timed out')","'connection','timed out','internal server error','http 500','http 502','http 503')")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    driver=A/'close_actual_sparse_committed_main_after_server_error_v4_20261007.py'
    pins={str(p):sha(p) for p in [Path(__file__),old,new,driver,*[p for p in extras if p.is_file()]]}
    rows={
      'actual_sparse_committed_main_recovery_v4':start('actual_sparse_committed_main_recovery_v4',driver.name,[],pins),
      'actual_GPU_shared_allocation_and_manual_bench_main_publication_v3':start('actual_GPU_shared_allocation_and_manual_bench_main_publication_v3',new.name,[],pins)}
    create(A/'actual_sparse_commit_closeout_and_GPU_receiver_hidden_launches_v4_20261007.json',{'status':'started_exact_local_commit_recovery_and_new_GPU_evidence_receiver','launches':rows,'input_sha256':pins,'new_quality_scores':0})

if __name__=='__main__':main()

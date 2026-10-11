"""Publish measured resource evidence through recovered main before final nightly QA."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def main():
    old=A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v3_20261007.py';new=A/'publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v4_20261007.py'
    text=old.read_text(encoding='utf8').replace('actual_sparse_committed_main_recovery_v4','nonflag_RidgeMicro40_scores_main_publication_v2').replace('actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v3_20261007','actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v4_20261007')
    text=text.replace('actual_sparse_and_isolated_scoring_controls_github_recovery_v4_20261007/receipt.json','sparse_main_API_transport_recovery_20261007/receipt.json')
    extras=[Path(__file__),old,A/'file_backed_hidden_git_runtime_20261007.py',A/'prepare_actual_sparse_API_payload_and_owned_main_lease_20261007.py',A/'hold_idle_main_publisher_for_API_tree_recovery_20261007.py',A/'transfer_pipe_waiting_API_holder_to_file_IO_v2_20261007.py',A/'finish_API_main_exact_tree_with_file_IO_v2_20261007.py',A/'finalize_actual_API_file_IO_contract_v3_20261007.py',A/'finish_API_main_exact_tree_with_file_IO_v3_20261007.py',A/'nonflag_ReverseBayes40_round132_dispatch_deferred_until_manual_continue_20261007.json',A/'nonflag_RidgeMicro131_administrative_publication_recovery_v2_20261007.json']
    extras += [p for p in (A/'sparse_main_API_transport_recovery_20261007').glob('*.json') if not p.name.startswith('packet')]
    for name in ['actual_sparse_committed_main_recovery_v4','actual_sparse_committed_main_full_pack_transport_v5','main_publication_API_tree_recovery_lease_v2','main_publication_API_tree_recovery_lease_v3']:
        folder=A/'service_owned_workflows_20261006'/name
        extras.extend([*folder.glob('*.json'),*folder.glob('*.log')])
    extras=list(dict.fromkeys(extras));assert all(p.is_file() for p in extras)
    needle='    sources=list(dict.fromkeys(sources));';assert text.count(needle)==1
    text=text.replace(needle,"    sources += ["+','.join('A/'+repr(p.relative_to(A).as_posix()) for p in extras)+"]\n"+needle)
    needle="if __name__=='__main__':main()";assert text.count(needle)==1
    text=text.replace(needle,"if __name__=='__main__':\n    from file_backed_hidden_git_runtime_20261007 import installed\n    with installed(A/'GPU_actual_resource_main_file_IO_v4_20261007'):main()")
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [new,*extras]}
    row=start('actual_GPU_shared_allocation_and_manual_bench_main_publication_v4',new.name,[],pins)
    create(A/'actual_GPU_resource_main_v4_hidden_launch_20261007.json',{'status':'started_actual_resource_main_after_recovered131_scores','identity':row,'input_sha256':pins,'new_quality_scores':0})

if __name__=='__main__':main()

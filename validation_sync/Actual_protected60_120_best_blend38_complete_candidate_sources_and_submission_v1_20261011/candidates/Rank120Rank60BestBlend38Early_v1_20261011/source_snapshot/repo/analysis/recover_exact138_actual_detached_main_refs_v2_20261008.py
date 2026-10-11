"""Preserve failed ref assumptions; reconcile the actual detached HEAD and independent main ref."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def save(p,s):
    assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n')
def main():
    old=A/'reconcile_exact138_connected_API_publication_v1_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace("assert git('rev-parse','refs/heads/main').decode().strip()==old","old_branch=git('rev-parse','refs/heads/main').decode().strip();assert old_branch in (old,b['parent_commit'])")
    s=s.replace("git('update-ref','refs/heads/main',commit,old)","git('update-ref','refs/heads/main',commit,old_branch)")
    s=s.replace("source_index_local_only_git_IO'","source_index_local_only_git_IO_v2'").replace("reconciliation_verification.json","reconciliation_verification_v2.json").replace("exact138_connected_API_reconciliation_v1_20261008.json","exact138_connected_API_reconciliation_v2_20261008.json")
    target=A/'reconcile_exact138_connected_API_publication_v2_20261008.py';save(target,s)
    outputs=[]
    for role in ('prepare','seal','run'):
        suffix='round138_full_registration' if role=='run' else 'selected_candidate'
        old=A/f'{role}_BF16reverse40_{suffix}_v16_20261008.py';s=old.read_text(encoding='utf8')
        s=s.replace('exact138_connected_API_publication_reconciliation_v1_20261008','exact138_connected_API_publication_reconciliation_v2_20261008')
        s=s.replace('candidate_preparation_v16_20261008','candidate_preparation_v17_20261008').replace('candidate_sealing_v16_20261008','candidate_sealing_v17_20261008')
        s=s.replace('selected_candidate_v16_20261008.py','selected_candidate_v17_20261008.py').replace('actual_registration_v16_20261008','actual_registration_v17_20261008').replace('full_registration_v16_file_IO_20261008','full_registration_v17_file_IO_20261008')
        if role=='run':
            s=s.replace("        extras.extend([A/'prepare_actual138_verified_API_candidate_registration_v16_20261008.py'", "        extras.extend([A/'recover_exact138_actual_detached_main_refs_v2_20261008.py',A/'exact138_detached_ref_receiver_recovery_v17_20261008.json',A/'reconcile_exact138_connected_API_publication_v2_20261008.py',A/'exact138_connected_API_reconciliation_v2_20261008.json',A/'prepare_actual138_verified_API_candidate_registration_v16_20261008.py'")
            s=s.replace("A/'exact138_connected_API_reconciliation_v1_20261008.json',",'')
        p=A/f'{role}_BF16reverse40_{suffix}_v17_20261008.py';save(p,s);outputs.append(p)
    pins={str(p):sha(p) for p in [Path(__file__),target,*outputs,A/'verified_TLS_Git_retry_runtime_v2_20261008.py']}
    create(A/'exact138_detached_ref_receiver_recovery_v17_20261008.json',{'status':'frozen_actual_detached_HEAD_and_independent_main_ref_recovery_before_new_registration','input_sha256':pins,'original_failed_services_preserved':True,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    rows={};rows['reconciliation']=start('exact138_connected_API_publication_reconciliation_v2_20261008',target.name,[],pins)
    # Dispatch dependent work only after the actual reconciliation passes.
    import time
    from run_dependency_queue_v3_20261006 import owned
    while owned(rows['reconciliation']):time.sleep(2)
    assert read(A/'service_owned_workflows_20261006/exact138_connected_API_publication_reconciliation_v2_20261008/service_execution.json')['status']=='passed'
    names=['BF16reverse40_selected_candidate_preparation_v17_20261008','BF16reverse40_selected_candidate_sealing_v17_20261008','BF16reverse40_round138_full_registration_v17_20261008']
    for n,p in zip(names,outputs):rows[n]=start(n,p.name,[],pins)
    create(A/'exact138_detached_ref_hidden_launches_v17_20261008.json',{'launches':rows,'input_sha256':pins})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()

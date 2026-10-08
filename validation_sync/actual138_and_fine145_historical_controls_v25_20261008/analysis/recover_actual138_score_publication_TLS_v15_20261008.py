"""A network handshake failed before staging; freeze a fresh publisher for the same40 exact official records."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    previous=A/'service_owned_workflows_20261006/BF16reverse40_scores_main_publication_v14_20261008/service_execution.json'
    assert read(previous)['status']=='failed' and 'TLS' in read(previous)['failure']
    old=A/'publish_BF16reverse40_evidence_v14_20261008.py';text=old.read_text(encoding='utf8')
    needle='from file_backed_hidden_git_runtime_20261007 import installed';assert text.count(needle)==1
    text=text.replace(needle,'from verified_TLS_Git_retry_runtime_v1_20261008 import installed')
    needle="out=A/f'BF16reverse40_{phase}_github_v1_20261008'";assert text.count(needle)==1
    text=text.replace(needle,"out=A/f'BF16reverse40_{phase}_github_v2_20261008'")
    target=A/'publish_BF16reverse40_evidence_v15_20261008.py';assert not target.exists();compile(text,str(target),'exec');target.write_text(text,encoding='utf8',newline='\n')
    create(A/'actual138_TLS_score_publication_recovery_v15_20261008.json',{'status':'frozen_fresh15_publication_of_identical40_scores_with_bounded_verified_TLS_retries',
        'input_sha256':{str(p):sha(p) for p in [Path(__file__),old,target,previous,A/'verified_TLS_Git_retry_runtime_v1_20261008.py']},
        'original14_failure_preserved':True,'failed_before_payload_staging':True,'new_quality_scores':0,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16reverse40_scores_main_publication_v15_20261008',target.name,['scores'],{str(p):sha(p) for p in [Path(__file__),target,A/'verified_TLS_Git_retry_runtime_v1_20261008.py']})
    create(A/'actual138_TLS_score_publication_hidden_launch_v15_20261008.json',row)
    print(json.dumps({'service':row['name'],'worker':row['owned_worker_pid']}),flush=True)
if __name__=='__main__':main()

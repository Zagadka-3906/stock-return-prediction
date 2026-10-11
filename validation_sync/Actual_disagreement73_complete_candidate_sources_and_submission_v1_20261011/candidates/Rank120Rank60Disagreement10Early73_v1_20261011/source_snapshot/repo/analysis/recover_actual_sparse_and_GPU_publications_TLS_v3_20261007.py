"""Retain failed pre-write TLS attempt; retry through fresh publishers on clean main."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

def prepare(old_name,new_name,old_out,new_out,gpu=False):
    old=A/old_name;new=A/new_name;text=old.read_text(encoding='utf8').replace(old_out,new_out)
    if gpu:text=text.replace('actual_sparse_and_isolated_scoring_controls_main_publication_v2','actual_sparse_and_isolated_scoring_controls_main_publication_v3')
    failed=[]
    for name in ['actual_sparse_and_isolated_scoring_controls_main_publication_v2','actual_GPU_shared_allocation_and_manual_bench_main_publication']:
        f=A/'service_owned_workflows_20261006'/name;assert not owned(read(f/'native_launch.json')) and read(f/'service_execution.json')['status']=='failed'
        failed.extend([*f.glob('*.json'),*f.glob('*.log')])
    extra=[old,Path(__file__),*failed]
    needle='    sources=list(dict.fromkeys(sources));';assert text.count(needle)==1
    text=text.replace(needle,"    sources += ["+','.join('A/'+repr(p.relative_to(A).as_posix()) for p in extra)+"]\n"+needle)
    assert text.count('def main():')==1;text=text.replace('def main():','def actual_main():')
    begin=text.index("if __name__=='__main__':main()")
    wrapper="""def main():
    original_git=helpers.sync.git;attempts=[]
    def retry(*args,**kwargs):
        for trial in range(3):
            try:return original_git(*args,**kwargs)
            except RuntimeError as error:
                if args[0] not in ('ls-remote','push','fetch') or not any(word in str(error).lower() for word in ('tls','ssl','unable to access','connection','timed out')):raise
                attempts.append({'command':args[0],'attempt':trial+1,'error':str(error)[:1200]})
                if trial==2:raise
                time.sleep(2)
    helpers.sync.git=retry
    try:actual_main()
    finally:
        helpers.sync.git=original_git
        if OUT.exists():create(OUT/'actual_TLS_transport_retries.json',{'attempts':attempts,'TLS_verification_not_disabled':True})

if __name__=='__main__':main()
"""
    text=text[:begin]+wrapper
    compile(text,str(new),'exec');assert not new.exists();new.write_text(text,encoding='utf8',newline='\n');return [old,new,*extra]

def main():
    import publish_classifier_consensus_workflows_20261006 as helpers
    sync=helpers.sync;assert not sync.git('status','--porcelain');helpers.verify_main(sync.git('rev-parse','HEAD'))
    paths=prepare('publish_actual_sparse_and_isolated_scoring_controls_main_v2_20261007.py','publish_actual_sparse_and_isolated_scoring_controls_main_v3_20261007.py',
      'actual_sparse_and_isolated_scoring_controls_github_20261007','actual_sparse_and_isolated_scoring_controls_github_recovery_v3_20261007')
    paths+=prepare('publish_actual_GPU_shared_memory_and_manual_bench_plan_main_20261007.py','publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v2_20261007.py',
      'actual_GPU_shared_memory_and_manual_bench_plan_github_20261007','actual_GPU_shared_memory_and_manual_bench_plan_github_recovery_v2_20261007',True)
    proof=A/'actual_sparse_and_GPU_TLS_publication_recovery_v3_source_preparation_20261007.json'
    create(proof,{'status':'fresh_bounded_TLS_retry_publishers_after_actual_failed_prewrite_attempt_on_clean_remote_main',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in paths},
      'original_failed_sources_and_logs_retained':True,'scientific_score_and_model_bytes_unchanged':True,
      'new_native_fits':0,'new_quality_scores':0,'TLS_verification_not_disabled':True})
    pins={**read(proof)['input_sha256'],str(proof):sha(proof)}
    rows={
      'actual_sparse_and_isolated_scoring_controls_main_publication_v3':start('actual_sparse_and_isolated_scoring_controls_main_publication_v3','publish_actual_sparse_and_isolated_scoring_controls_main_v3_20261007.py',[],pins),
      'actual_GPU_shared_allocation_and_manual_bench_main_publication_v2':start('actual_GPU_shared_allocation_and_manual_bench_main_publication_v2','publish_actual_GPU_shared_memory_and_manual_bench_plan_main_v2_20261007.py',[],pins)}
    create(A/'actual_sparse_GPU_TLS_recovery_actual_hidden_launches_20261007.json',{'status':'started_actual_bounded_TLS_recovery_publishers','launches':rows,'input_sha256':pins})
    print('Clean main verified; fresh bounded TLS retry publishers started',flush=True)

if __name__=='__main__':main()

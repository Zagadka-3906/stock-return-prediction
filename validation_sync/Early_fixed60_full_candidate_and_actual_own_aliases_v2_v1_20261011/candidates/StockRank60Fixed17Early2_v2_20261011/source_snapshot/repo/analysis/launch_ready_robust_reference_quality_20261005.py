"""Freeze and launch all198 complete official comparisons without changing old jobs."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
OUT=A/'ready_robust_reference_quality_followups_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    proofs=[A/name for name in (
        'ready_robust_reference_generator_preflight_20261005/verification.json',
        'ready_robust_reference_execution_preflight_20261005/verification.json',
        'streaming_robust_regression_preflight_20261005/verification.json')]
    for path in proofs:
        value=read(path)
        assert value['status'].startswith('passed')
        for source,digest in value.get('source_sha256',{}).items():assert sha(source)==digest,source
    assert [r['generated_records'] for r in read(proofs[0])['controls']]==[100,98,98]
    import qualified_round_recovery_evidence_v2_20261005 as qualified
    assert qualified.complete_round_evidence(66) is not None
    qualified.close()
    from predict_ready_robust_reference_scheme_20261005 import source_names
    from finalize_main_branch_consolidation_20261005 import owned_pair
    sources=list(dict.fromkeys([Path(__file__),*proofs,A/'ready_robust_reference_complete_plan_20261005.json',A/'streaming_robust_regression_preflight_20261005/verification.json',A/'streaming_robust_regression_direct_router_preflight_20261005/verification.json',
        A/'run_recovery_qualified_workflow_20261005.py',A/'qualified_round_recovery_evidence_20261005.py',
        A/'qualified_round_recovery_evidence_v2_20261005.py',A/'standalone_root_source_adapter_20261005.py',
        A/'streaming_robust_regression_scheme_runtime_20261005.py',A/'streaming_robust_regression_model_sources_20261005.py',
        A/'predict_ready_robust_reference_scheme_20261005.py',A/'streaming_robust_regression_future_codec_adapter_20261005.py',
        A/'train_streaming_robust_regression_bank_20261005.py',A/'frozen_provenance_execution_scope_20261004.py',
        *[A/name for n in (87,88) for name in source_names(n)]]))
    run=A/'ready_robust_reference_quality_run_20261005.json'
    create(run,{'status':'frozen_before_actual_complete_output_quality',
        'explicit_parent_rounds':{'87':86,'88':87},'required_official_records':{'87':100,'88':98},
        'original_rounds67_through86_retained':True,'actual_parent84_not_yet_qualified_quality_waits_for_real_parent':True,'same_validation_and_scorer_and_mature_return_mapping':True,'actual20_annual4_final_fullfuture_qa_required_before_quality':True,
        'input_sha256':{str(path):sha(path) for path in sources},'test_labels_read':False})
    OUT.mkdir()
    jobs=[]
    launcher=A/'run_recovery_qualified_workflow_20261005.py'
    registry_path=A/'resumed_rounds_nystrom_locked_20261004.json'
    registry=read(registry_path)
    assert not any(row['round'] in (87,88) for row in registry)
    env=dict(os.environ)
    scratch=Path(read(A/'streaming_robust_regression_storage_20261005.json')['temporary_directory'])/'ready_robust_reference'
    scratch.mkdir(parents=True,exist_ok=True)
    assert scratch.resolve().drive.upper() in ('D:','E:')
    for variable in ('TMP','TEMP','TMPDIR'):env[variable]=str(scratch)
    for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):env[variable]='8'
    for number in (87,88):
        driver=A/f'run_training_round{number}_v2_pipeline.py'
        bridge=OUT/f'round{number}_recovery_run.json'
        create(bridge,{'original_driver':str(driver),'original_arguments':[],
            'input_sha256':{**read(run)['input_sha256'],str(run):sha(run),str(driver):sha(driver)},
            'complete_explicit_parent':86 if number==87 else 87})
        stdout=A/f'run_logs/round{number}_ready_robust_reference_20261005.stdout.log'
        stderr=A/f'run_logs/round{number}_ready_robust_reference_20261005.stderr.log'
        args=[str(driver),str(bridge)]
        with stdout.open('xb') as output,stderr.open('xb') as error:
            process=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(launcher),*args],
                cwd=ROOT,env=env,stdout=output,stderr=error,creationflags=subprocess.CREATE_NO_WINDOW)
        job={'round':number,'explicit_parent_round':86 if number==87 else 87,
            'pid':process.pid,'script':str(launcher),'script_args':args,'stdout':str(stdout),'stderr':str(stderr),
            'at_local':datetime.datetime.now().isoformat(),'prospective_official_workers':1}
        create(OUT/f'round{number}_launch.json',job)
        time.sleep(3)
        parent,worker=owned_pair(process.pid,launcher,args)
        assert not stderr.read_bytes()
        job.update(owned_worker_pid=worker.pid,owned_worker_creation_time=worker.create_time())
        jobs.append(job);registry.append(job)
    from atomic_optimization_observer_writes_20261005 import write
    write(registry_path,registry)
    create(OUT/'verification.json',{'status':'passed_actual_owned_complete_quality_jobs_launched',
        'quality_rounds':jobs,'source_sha256':read(run)['input_sha256'],
        'original_rounds67_through86_not_restarted_or_removed':True,'required_new_official_records':198,
        'expected20_annual4_final_native_fits_not_claimed_completed_by_controls':True,
        'new_quality_scores_at_launch':0,'test_labels_read':False,'only_git_branch':'main'})
    print(json.dumps({'status':'launched_full_ready_robust_reference_quality','quality_rounds':jobs},ensure_ascii=False),flush=True)


if __name__=='__main__':main()

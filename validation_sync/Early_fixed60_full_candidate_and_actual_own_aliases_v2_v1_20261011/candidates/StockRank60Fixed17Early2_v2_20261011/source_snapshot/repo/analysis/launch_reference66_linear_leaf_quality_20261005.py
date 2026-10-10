"""Freeze and launch all262 complete official comparisons without changing old jobs."""
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
OUT=A/'reference66_linear_leaf_quality_followups_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    proofs=[A/name for name in (
        'reference66_linear_leaf_generator_preflight_v2_20261005/verification.json',
        'reference66_linear_leaf_execution_preflight_20261005/verification.json',
        'linear_leaf_future_qa_20261005/verification.json')]
    for path in proofs:
        value=read(path)
        assert value['status']=='passed'
        for source,digest in value.get('source_sha256',{}).items():assert sha(source)==digest,source
    assert [r['generated_records'] for r in read(proofs[0])['controls']]==[124,138,138]
    import qualified_round_recovery_evidence_v2_20261005 as qualified
    assert qualified.complete_round_evidence(66) is not None
    qualified.close()
    from predict_reference66_linear_leaf_scheme_v2_20261005 import source_names
    from finalize_main_branch_consolidation_20261005 import owned_pair
    sources=list(dict.fromkeys([Path(__file__),*proofs,A/'reference66_linear_leaf_complete_plan_20261005.json',
        A/'run_recovery_qualified_workflow_20261005.py',A/'qualified_round_recovery_evidence_20261005.py',
        A/'qualified_round_recovery_evidence_v2_20261005.py',A/'standalone_root_source_adapter_20261005.py',
        A/'linear_leaf_scheme_runtime_20261005.py',A/'linear_leaf_model_sources_20261005.py',
        A/'predict_linear_leaf_scheme_20261005.py',A/'linear_leaf_future_codec_adapter_20261005.py',
        A/'train_linear_leaf_bank_20261005.py',A/'frozen_provenance_execution_scope_20261004.py',
        *[A/name for n in (81,82) for name in source_names(n)]]))
    run=A/'reference66_linear_leaf_quality_run_20261005.json'
    create(run,{'status':'frozen_before_actual_complete_output_quality',
        'explicit_parent_rounds':{'81':66,'82':81},'required_official_records':{'81':124,'82':138},
        'original_rounds67_through80_retained':True,'same_validation_and_scorer_and_mature_return_mapping':True,
        'input_sha256':{str(path):sha(path) for path in sources},'test_labels_read':False})
    OUT.mkdir()
    jobs=[]
    launcher=A/'run_recovery_qualified_workflow_20261005.py'
    registry_path=A/'resumed_rounds_nystrom_locked_20261004.json'
    registry=read(registry_path)
    assert not any(row['round'] in (81,82) for row in registry)
    env=dict(os.environ)
    scratch=Path(read(A/'linear_leaf_storage_20261005.json')['temporary_directory'])/'reference66'
    scratch.mkdir(parents=True,exist_ok=True)
    assert scratch.resolve().drive.upper() in ('D:','E:')
    for variable in ('TMP','TEMP','TMPDIR'):env[variable]=str(scratch)
    for variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):env[variable]='8'
    for number in (81,82):
        driver=A/f'run_training_round{number}_v2_pipeline.py'
        bridge=OUT/f'round{number}_recovery_run.json'
        create(bridge,{'original_driver':str(driver),'original_arguments':[],
            'input_sha256':{**read(run)['input_sha256'],str(run):sha(run),str(driver):sha(driver)},
            'complete_explicit_parent':66 if number==81 else 81})
        stdout=A/f'run_logs/round{number}_reference66_linear_leaf_20261005.stdout.log'
        stderr=A/f'run_logs/round{number}_reference66_linear_leaf_20261005.stderr.log'
        args=[str(driver),str(bridge)]
        with stdout.open('xb') as output,stderr.open('xb') as error:
            process=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(launcher),*args],
                cwd=ROOT,env=env,stdout=output,stderr=error,creationflags=subprocess.CREATE_NO_WINDOW)
        job={'round':number,'explicit_parent_round':66 if number==81 else 81,
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
        'original_rounds67_through80_not_restarted_or_removed':True,'required_new_official_records':262,
        'existing30_annual6_final_native_fits_not_counted_again':True,
        'new_quality_scores_at_launch':0,'test_labels_read':False,'only_git_branch':'main'})
    print(json.dumps({'status':'launched_full_reference66_quality','quality_rounds':jobs},ensure_ascii=False),flush=True)


if __name__=='__main__':main()

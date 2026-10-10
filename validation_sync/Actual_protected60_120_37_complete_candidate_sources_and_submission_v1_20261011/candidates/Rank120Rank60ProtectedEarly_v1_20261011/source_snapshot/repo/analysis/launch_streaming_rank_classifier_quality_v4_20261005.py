"""Freeze and launch both full198-record official workflows after genuine controls."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

import psutil

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'analysis'
OUT=A/'streaming_rank_classifier_quality_followups_v4_20261005'


def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def create(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:json.dump(value,stream,ensure_ascii=False,indent=2)


def main():
    assert not OUT.exists()
    proofs=[A/f'{folder}/verification.json' for folder in (
        'streaming_rank_classification_preflight_v3_20261005',
        'streaming_rank_classifier_direct_router_preflight_20261005',
        'streaming_rank_classifier_search_generator_preflight_v4_20261005',
        'streaming_rank_classifier_execution_source_preflight_v4_20261005')]
    for path in proofs:
        proof=read(path)
        assert proof['status'].startswith('passed')
        for filename,digest in proof.get('source_sha256',{}).items():assert sha(filename)==digest,filename
    assert read(proofs[1])['actual_checks']==44
    assert [row['generated_records'] for row in read(proofs[2])['controls']]==[100,98,98]
    current=read(A/'streaming_rank_classifier_followups_v3_20261005/verification.json')
    for role in ('native','future'):
        job=current[role]
        worker=psutil.Process(job['owned_worker_pid'])
        assert worker.create_time()==job['owned_worker_creation_time'] and job['script'] in worker.cmdline()
        assert not Path(job['stderr']).read_bytes()
    sources=set(A.glob('*streaming_rank_class*20261005.py'))
    sources.update(A/f'{stem}{number}{suffix}.py' for number in (79,80)
        for stem,suffix in (('optimize_training_round','_v4'),('finalize_training_round','_v4'),('run_training_round','_v4_pipeline')))
    sources.update(proofs)
    sources.update((A/'streaming_rank_classifier_official_search_plan_20261005.json',
        A/'streaming_rank_classifier_runnable_source_recovery_v4_20261005.json',
        A/'streaming_rank_classifier_bank_run_v3_20261005.json',
        A/'streaming_rank_classifier_future_run_v3_20261005.json'))
    run=A/'streaming_rank_classifier_quality_run_v4_20261005.json'
    create(run,{'status':'frozen_before_actual_full_classifier_official_workflows',
        'input_sha256':{str(path):sha(path) for path in sources},'planned_records':{'79':100,'80':98},
        'actual20_annual4_final_full_native_future_controls_required':True,
        'actual_qualified_predecessors78_and79_required':True,
        'same5635800_rows1212_continuous_days_official_S_only':True,
        'all_validation_years_reused_selection_bias_uncorrected':True,
        'test_labels_read':False,'new_quality_scores':0})
    OUT.mkdir()
    env=dict(os.environ)
    scratch=read(A/'streaming_rank_classifier_storage_v3_20261005.json')['temporary_directory']
    for name in ('TMP','TEMP','TMPDIR'):env[name]=scratch
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):env[name]='8'
    launcher=A/'run_recovery_qualified_workflow_20261005.py'
    jobs=[]
    for number in (79,80):
        driver=A/f'run_training_round{number}_v4_pipeline.py'
        frozen=OUT/f'round{number}_run.json'
        inputs=[launcher,driver,run,A/'qualified_round_recovery_evidence_20261005.py',
            A/'qualified_round_recovery_evidence_v2_20261005.py',A/'standalone_root_source_adapter_20261005.py']
        create(frozen,{'original_driver':str(driver),'original_arguments':[],
            'input_sha256':{str(path):sha(path) for path in inputs},'test_labels_read':False})
        stdout=A/f'run_logs/round{number}_streaming_rank_classifier_v4_20261005.stdout.log'
        stderr=A/f'run_logs/round{number}_streaming_rank_classifier_v4_20261005.stderr.log'
        args=[str(driver),str(frozen)]
        with stdout.open('xb') as output,stderr.open('xb') as error:
            p=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-B','-X','utf8',str(launcher),*args],
                cwd=ROOT,env=env,stdout=output,stderr=error,creationflags=subprocess.CREATE_NO_WINDOW)
        jobs.append({'round':number,'pid':p.pid,'script':str(launcher),'script_args':args,
            'stdout':str(stdout),'stderr':str(stderr),'at_local':datetime.datetime.now().isoformat(),
            'expected_scored_records':100 if number==79 else 98,
            'status':'waiting_for_actual20_annual4_final_fullfuture_and_qualified_predecessor'})
        create(OUT/f'round{number}_launch.json',jobs[-1])
    time.sleep(3)
    for job in jobs:
        parent=psutil.Process(job['pid'])
        assert parent.cmdline()[-2:]==job['script_args']
        workers=[p for p in parent.children(recursive=True)
                 if p.name().lower()=='python.exe' and p.cmdline()[1:]==parent.cmdline()[1:]]
        assert len(workers)==1 and not Path(job['stderr']).read_bytes()
        job['owned_worker_pid']=workers[0].pid
    registry=A/'resumed_rounds_nystrom_locked_20261004.json'
    old=read(registry)
    assert not any(row['round'] in (79,80) for row in old)
    temporary=registry.with_suffix('.classifier_registry.tmp')
    temporary.write_text(json.dumps(old+jobs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(registry)
    create(OUT/'verification.json',{'status':'passed_owned_complete_official_quality79_80_waiters_launched',
        'at_local':datetime.datetime.now().isoformat(),'quality_rounds':jobs,
        'complete20_annual4_final_fullfuture_and_qualified78_79_predecessor_required':True,
        'source_sha256':{str(run):sha(run),str(Path(__file__)):sha(Path(__file__))},
        'expected_total_official_records':198,'actual_official_records_at_launch':0,
        'only_publication_branch':'main','prior_jobs_not_stopped_or_restarted':True,
        'test_labels_read':False,'new_quality_scores':0})
    print(json.dumps({'status':'passed','quality_roots':[row['pid'] for row in jobs]},ensure_ascii=False),flush=True)


if __name__=='__main__':main()

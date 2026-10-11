"""Queue15 annual3 final fits and both full official grids with immutable source pins."""
from pathlib import Path
from datetime import datetime
import json
import os
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT),str(A)]
from handoff_recovery_qualified_workflows_20261005 import read,sha,create
from handoff_factorization_machine_repaired_workflows_20261005 import processes
from prepare_gradient_sampling_followups_20261005 import launch


def main():
    out = A / 'memory_efficient_neural_followups_20261005'
    assert not out.exists()
    proofs = [A / f'{name}/verification.json' for name in (
        'memory_efficient_mlp_preflight_20261005','memory_efficient_neural_direct_router_preflight_20261005',
        'memory_efficient_neural_search_generator_preflight_20261005','memory_efficient_neural_workflow_preflight_20261005')]
    for path in proofs:
        proof = read(path)
        assert proof['status'].startswith('passed')
        for source,digest in proof['source_sha256'].items():
            assert sha(source) == digest,source
    assert [row['generated_records'] for row in read(proofs[2])['controls']] == [88,78,78]
    registry_path = A / 'resumed_rounds_nystrom_locked_20261004.json'
    old_registry = read(registry_path)
    assert not any(job['round'] in (77,78) for job in old_registry)
    out.mkdir()
    storage = read(A / 'memory_efficient_neural_storage_20261005.json')
    scratch = Path(storage['temporary_directory'])
    assert scratch.resolve().drive.upper() in ('D:','E:')
    scratch.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ)
    env.pop('CUDA_VISIBLE_DEVICES',None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for key in ('TMP','TEMP','TMPDIR'):
        env[key] = str(scratch)
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
        env[key] = '8'
    sources = set(A.glob('*memory_efficient*20261005.py'))
    sources.update(A / f'{prefix}{number}{suffix}.py' for number in (77,78)
        for prefix,suffix in (('optimize_training_round',''),('finalize_training_round',''),('run_training_round','_pipeline')))
    sources.update((*proofs,A / 'memory_efficient_neural_storage_20261005.json',
        A / 'memory_efficient_neural_complete_search_plan_20261005.json',
        A / 'memory_efficient_neural_source_generation_20261005.json'))
    native_run = A / 'memory_efficient_neural_bank_run_20261005.json'
    create(native_run,{'status':'frozen_before_actual15_complete_annual_memory_layout_fits',
        'input_sha256':{str(path):sha(path) for path in sources},'actual_complete_annual_fits_required':15,
        'actual32epochs_effective32768batch_same168894465parameters_per_model':True,
        'GPU_controls_and_GOSS_attempt_closures_required_before_training':True,
        'test_labels_read':False,'new_quality_scores':0})
    launcher = A / 'run_recovery_qualified_workflow_20261005.py'
    native_driver = A / 'run_memory_efficient_neural_bank_20261005.py'
    launcher_run = out / 'native_launch_run.json'
    create(launcher_run,{'original_driver':str(native_driver),'original_arguments':[],
        'input_sha256':{str(path):sha(path) for path in (launcher,native_driver,native_run,
            A / 'qualified_round_recovery_evidence_20261005.py',A / 'qualified_round_recovery_evidence_v2_20261005.py',
            A / 'standalone_root_source_adapter_20261005.py')},'test_labels_read':False})
    future_driver = A / 'verify_memory_efficient_neural_full_future_20261005.py'
    future_run = A / 'memory_efficient_neural_future_run_20261005.json'
    create(future_run,{'status':'frozen_before_actual3_complete_final_fits_and_full_future_controls',
        'input_sha256':{str(path):sha(path) for path in sources | {native_run,launcher_run}},
        'actual_final_fits_required':3,'epochs_each_final_fit':32,'expected_future_rows':1599600,
        'native_full_reload_and_cold80_day_prefix_required':True,'test_labels_read':False})
    quality_run = A / 'memory_efficient_neural_quality_run_20261005.json'
    create(quality_run,{'status':'frozen_before_actual_complete_official88_and78_schemes',
        'input_sha256':{str(path):sha(path) for path in sources | {native_run,launcher_run,future_run}},
        'planned_records':{'77':88,'78':78},'actual_complete_predecessors_required':[76,77],
        'actual15_annual3_final_fullfuture_controls_required':True,
        'new_quality_scores':0,'test_labels_read':False})
    native = launch(launcher,[str(native_driver),str(launcher_run)],'memory_efficient_neural_native_20261005',env)
    future = launch(future_driver,[],'memory_efficient_neural_full_future_20261005',env)
    jobs = []
    for number in (77,78):
        driver = A / f'run_training_round{number}_pipeline.py'
        run_path = out / f'round{number}_run.json'
        create(run_path,{'original_driver':str(driver),'original_arguments':[],
            'input_sha256':{str(path):sha(path) for path in (launcher,driver,quality_run,
                A / 'qualified_round_recovery_evidence_20261005.py',A / 'qualified_round_recovery_evidence_v2_20261005.py',
                A / 'standalone_root_source_adapter_20261005.py')},'test_labels_read':False})
        job = launch(launcher,[str(driver),str(run_path)],f'round{number}_memory_efficient_neural_20261005',env)
        jobs.append({'round':number,**job,'expected_scored_records':88 if number == 77 else 78,
            'status':'waiting_for_actual15_annual3_final_fullfuture_controls_and_qualified_predecessor'})
    temporary = registry_path.with_suffix('.memory_neural.tmp')
    temporary.write_text(json.dumps(old_registry+jobs,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(registry_path)
    create(out / 'launch.json',{'status':'launched_actual_native_final_and_official_waiters',
        'native':native,'future':future,'quality_rounds':jobs,'original_registry_jobs_preserved':old_registry})
    time.sleep(6)
    for job in (native,future,*jobs):
        processes(job)
        assert not Path(job['stderr']).read_text(encoding='utf-8'),job['stderr']
    assert [job for job in read(registry_path) if job['round'] not in (77,78)] == old_registry
    create(out / 'verification.json',{'status':'passed_owned_full_native_final_and_official_waiters_launched',
        'native':native,'future':future,'quality_rounds':jobs,'all_prior_registry_jobs_unchanged':True,
        'planned_complete_annual_fits':15,'planned_complete_final_fits':3,'planned_official_records':166,
        'actual_new_complete_annual_fits':0,'actual_new_complete_final_fits':0,
        'weights_and_scratch_drive':scratch.drive,'only_publication_branch':'main',
        'source_sha256':{str(path):sha(path) for path in (Path(__file__),native_run,launcher_run,future_run,quality_run)},
        'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'passed','native':native['pid'],'future':future['pid'],
        'quality':[job['pid'] for job in jobs],'scratch_drive':scratch.drive}),flush=True)


if __name__ == '__main__':
    main()

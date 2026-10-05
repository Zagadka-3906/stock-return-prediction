"""Queue eight virtual final models and326 complete schemes, counting native parent fits once."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def launch(script, label, env):
    stdout = ROOT / f'analysis/run_logs/{label}.stdout.log'
    stderr = ROOT / f'analysis/run_logs/{label}.stderr.log'
    with stdout.open('xb') as output, stderr.open('xb') as error:
        process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
            cwd=ROOT, env=env, stdout=output, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
    return {'pid': process.pid, 'script': str(script), 'script_args': [],
        'stdout': str(stdout), 'stderr': str(stderr), 'launched_at_local': datetime.datetime.now().isoformat()}


def main():
    storage = read(ROOT / 'analysis/linear_leaf_ensemble_storage_20261005.json')
    proof_path = ROOT / 'analysis/linear_leaf_ensemble_search_generator_preflight_v2_20261005/verification.json'
    proof = read(proof_path)
    assert proof['status'] == 'passed' and [p['generated_records'] for p in proof['controls']] == [148,178,178]
    codec = ROOT / 'analysis/linear_leaf_ensemble_future_codec_preflight_20261005/verification.json'
    assert read(codec)['status'] == 'passed'
    assert read(codec)['all8_ensemble_and6_linear_and10_nystrom_saved_models_dispatched_exactly']
    native = ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005/verification.json'
    assert read(native)['status'] == 'passed_actual_five_year_mixture_native_reload_and_prefix_controls'
    for evidence in (proof, read(codec), read(native)):
        for source, value in evidence['source_sha256'].items():
            assert sha(source) == value, source
    registry_path = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'
    for number in range(63, 71):
        proto = ROOT / f'analysis/optimization_20261003_r{number}/protocol.json'
        if proto.exists():
            assert str(registry_path) not in read(proto)['input_sha256']
    registry = read(registry_path)
    assert not any(int(row['round']) in (71,72) for row in registry)
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
        env[key] = '8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    future = ROOT / 'analysis/verify_linear_leaf_ensemble_full_future_20261005.py'
    sources = {p for p in (ROOT / 'analysis').glob('*linear_leaf_ensemble*20261005.py')}
    sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py' for number in (71,72)
        for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v2'),
                              ('finalize_training_round',''),('run_training_round','_v2_pipeline')))
    sources.update([proof_path, codec, native, ROOT / 'analysis/linear_leaf_ensemble_complete_search_plan_20261005.json'])
    for source in sources:
        if source.suffix == '.py':
            compile(source.read_text(encoding='utf-8'),str(source),'exec')
    bindings = {str(p):sha(p) for p in sorted(sources)}
    create(ROOT / 'analysis/linear_leaf_ensemble_future_run_20261005.json', {
        'status':'frozen_before_eight_virtual_final_artifacts_and_actual_fullfuture_controls',
        'at_local':datetime.datetime.now().isoformat(),'input_sha256':bindings,
        'planned_virtual_final_artifacts':8,'planned_actual_new_final_fits':0,'required_parent_final_fits':6,'test_labels_read':False})
    create(ROOT / 'analysis/linear_leaf_ensemble_quality_run_20261005.json', {
        'status':'frozen_before_two_full_scheme_quality_waiters','at_local':datetime.datetime.now().isoformat(),
        'input_sha256':bindings,'planned_records':{'71':148,'72':178},
        'actual_full_fits_and_native_future_controls_required_before_quality':True,
        'test_labels_read':False})
    future_record = launch(future,'linear_leaf_ensemble_full_future_20261005',env)
    records=[]
    for number, expected in ((71,148),(72,178)):
        script=ROOT/f'analysis/run_training_round{number}_v2_pipeline.py'
        record={'round':number,**launch(script,f'round{number}_linear_leaf_ensemble_v2_20261005',env),
            'status':'waiting_for_actual40_virtual_annual8_virtual_final_controls_and_qualified_predecessor',
            'expected_scored_records':expected}
        records.append(record)
    registry.extend(records)
    temporary = registry_path.with_suffix('.linear_registry.tmp')
    temporary.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(registry_path)
    create(ROOT / 'analysis/linear_leaf_ensemble_followup_launch_receipt_20261005.json', {
        'status':'passed_source_controls_and_native_future_two_quality_waiters_launched',
        'at_local':datetime.datetime.now().isoformat(),'future':future_record,
        'quality_rounds':records,'planned_virtual_annual_outputs':40,'actual_new_model_fits':0,
        'new_actual_annual_fits_at_launch':0,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'lazy_native_future_and_quality_workflows_launched',
        'future_pid':future_record['pid'],'quality_pids':{row['round']:row['pid'] for row in records}},ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()

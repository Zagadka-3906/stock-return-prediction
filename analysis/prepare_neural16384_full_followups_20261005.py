"""Queue actual final-fit/future controls and102 complete official quality records."""
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
    storage = json.loads((ROOT / 'analysis/neural16384_full_storage_20261005.json').read_text(encoding='utf-8'))
    proof_path = ROOT / 'analysis/neural16384_full_search_generator_preflight_v2_20261005/verification.json'
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed' and [p['generated_records'] for p in proof['controls']] == [64,38,38]
    for source, value in proof['source_sha256'].items():
        assert sha(source) == value, source
    registry_path = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'
    # Frozen running scientific inputs may never be changed to register a waiter.
    for number in (63,64,65,66):
        proto = ROOT / f'analysis/optimization_20261003_r{number}/protocol.json'
        if proto.exists():
            assert str(registry_path) not in json.loads(proto.read_text(encoding='utf-8'))['input_sha256']
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    assert not any(int(row['round']) in (67,68) for row in registry)
    env = os.environ.copy()
    for key in ('TMP', 'TEMP', 'TMPDIR'):
        env[key] = storage['temporary_directory']
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','POLARS_MAX_THREADS'):
        env[key] = '8'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    future = ROOT / 'analysis/verify_neural16384_full_future_20261005.py'
    sources = {p for p in (ROOT / 'analysis').glob('*neural16384*20261005.py')}
    sources.update(ROOT / 'analysis' / f'{prefix}{number}{suffix}.py' for number in (67,68)
        for prefix,suffix in (('optimize_training_round',''),('optimize_training_round','_v2'),
                              ('finalize_training_round',''),('run_training_round','_v2_pipeline')))
    sources.update([proof_path, ROOT / 'analysis/neural16384_full_complete_search_plan_20261005.json'])
    for source in sources:
        if source.suffix == '.py':
            compile(source.read_text(encoding='utf-8'),str(source),'exec')
    bindings = {str(p):sha(p) for p in sorted(sources)}
    create(ROOT / 'analysis/neural16384_full_future_run_20261005.json', {
        'status':'frozen_before_lazy_final_fit_and_native_future_X_controls',
        'at_local':datetime.datetime.now().isoformat(),'input_sha256':bindings,
        'planned_actual_final_fits':1,'epochs_each_fit':32,'test_labels_read':False})
    create(ROOT / 'analysis/neural16384_full_quality_run_20261005.json', {
        'status':'frozen_before_two_full_scheme_quality_waiters','at_local':datetime.datetime.now().isoformat(),
        'input_sha256':bindings,'planned_records':{'67':64,'68':38},
        'actual_full_fits_and_native_future_controls_required_before_quality':True,
        'test_labels_read':False})
    future_record = launch(future,'neural16384_full_future_20261005',env)
    records=[]
    for number, expected in ((67,64),(68,38)):
        script=ROOT/f'analysis/run_training_round{number}_v2_pipeline.py'
        record={'round':number,**launch(script,f'round{number}_neural16384_full_v2_20261005',env),
            'status':'waiting_for_actual_full_fits_native_future_and_qualified_predecessor',
            'expected_scored_records':expected}
        records.append(record)
    registry.extend(records)
    with registry_path.open('w',encoding='utf-8') as stream:
        json.dump(registry,stream,ensure_ascii=False,indent=2)
        stream.write('\n')
    create(ROOT / 'analysis/neural16384_full_followup_launch_receipt_20261005.json', {
        'status':'passed_source_pins_and_native_future_two_quality_waiters_launched',
        'at_local':datetime.datetime.now().isoformat(),'future':future_record,'quality_rounds':records,
        'new_full16384_annual_fits':0,'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'status':'three_lazy_waiters_launched','future_pid':future_record['pid'],
        'quality_pids':{row['round']:row['pid'] for row in records}},ensure_ascii=False),flush=True)


if __name__=='__main__':main()

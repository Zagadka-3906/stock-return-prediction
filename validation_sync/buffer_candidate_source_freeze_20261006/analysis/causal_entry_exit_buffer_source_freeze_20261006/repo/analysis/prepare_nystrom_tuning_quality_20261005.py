"""Freeze corrected full-scheme sources and queue rounds65/66 behind actual evidence."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import datetime
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def create(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def main():
    proof_path = ROOT / 'analysis/nystrom_tuning_search_generator_preflight_v2_20261005/verification.json'
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    assert proof['status'] == 'passed' and proof['new_quality_scores'] == 0
    for source, expected in proof['source_sha256'].items():
        assert digest(source) == expected, source
    assert [case['generated_records'] for case in proof['controls']] == [172, 218, 218]
    registry = ROOT / 'analysis/resumed_rounds_nystrom_locked_20261004.json'
    for number in (63, 64):
        protocol = ROOT / f'analysis/optimization_20261003_r{number}/protocol.json'
        if protocol.exists():
            assert str(registry.resolve()) not in json.loads(protocol.read_text(encoding='utf-8'))['input_sha256']
    records = json.loads(registry.read_text(encoding='utf-8'))
    assert not any(row['round'] in (65, 66) for row in records)
    sources = {Path(__file__), proof_path, ROOT / 'analysis/nystrom_tuning_complete_search_plan_20261005.json',
               ROOT / 'analysis/nystrom_tuning_storage_20261005.json',
               ROOT / 'analysis/nystrom_tuning_future_run_20261005.json'}
    sources.update(Path(path) for path in proof['source_sha256'])
    # The scorer overwrites one CSV per private context; it does not retain390 CSVs.
    observed_csvs = list((ROOT / 'analysis/optimization_20261003_r62').rglob('submission.csv'))
    max_csv = max(path.stat().st_size for path in observed_csvs)
    create(ROOT / 'analysis/nystrom_tuning_quality_run_20261005.json', {
        'status': 'frozen_corrected_sources_before_waiting_quality_controllers',
        'at_local': datetime.datetime.now().isoformat(), 'rounds': [65, 66],
        'records_expected': {'65': 172, '66': 218}, 'input_sha256': {str(path): digest(path) for path in sources},
        'actual_private_scoring_csv_max_bytes_observed_R62': max_csv,
        'scoring_contexts_per_round': 5, 'prediction_csv_overwritten_per_context': True,
        'D_free_bytes': psutil.disk_usage('D:/').free, 'E_free_bytes': psutil.disk_usage('E:/').free,
        'D_currently_sufficient_no_frozen_source_or_asset_migration': True,
        'E_for_new_storage_when_D_insufficient_authorized': True,
        'source_v1_and_failed_generator_control_retained': True,
        'full50_annual10_final_native_controls_and_full_predecessor_required': True,
        'selection_bias_uncorrected': True, 'test_labels_read': False, 'new_quality_scores': 0})
    storage = json.loads((ROOT / 'analysis/nystrom_tuning_storage_20261005.json').read_text(encoding='utf-8'))
    env = os.environ.copy()
    for variable in ('TMP', 'TEMP', 'TMPDIR'):
        env[variable] = storage['temporary_directory']
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for number in (65, 66):
        script = ROOT / f'analysis/run_training_round{number}_v2_pipeline.py'
        stdout = ROOT / f'analysis/run_logs/round{number}_nystrom_tuning_v2_20261005.stdout.log'
        stderr = ROOT / f'analysis/run_logs/round{number}_nystrom_tuning_v2_20261005.stderr.log'
        with stdout.open('xb') as out, stderr.open('xb') as error:
            process = subprocess.Popen([str(ROOT / '.venv/Scripts/python.exe'), '-B', '-X', 'utf8', str(script)],
                cwd=ROOT, env=env, stdout=out, stderr=error, creationflags=subprocess.CREATE_NO_WINDOW)
        records.append({'round': number, 'pid': process.pid, 'script': str(script), 'script_args': [],
            'stdout': str(stdout), 'stderr': str(stderr), 'launched_at_local': datetime.datetime.now().isoformat(),
            'status': 'waiting_for_full_native_and_qualified_predecessor', 'expected_scored_records': 172 if number == 65 else 218})
    temporary = registry.with_suffix('.tuning.tmp')
    temporary.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(registry)
    create(ROOT / 'analysis/nystrom_tuning_quality_queue_adoption_20261005.json', {
        'status': 'passed_source_pins_and_two_lazy_waiters_launched', 'at_local': datetime.datetime.now().isoformat(),
        'new_round_records': records[-2:], 'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    print(json.dumps({'status': 'queued65_66', 'pids': [row['pid'] for row in records[-2:]],
        'official_records_planned': 390}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

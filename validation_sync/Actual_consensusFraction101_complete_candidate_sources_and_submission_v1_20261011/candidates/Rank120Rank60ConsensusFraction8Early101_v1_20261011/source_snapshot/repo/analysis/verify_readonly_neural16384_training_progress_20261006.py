"""Repeat nonblocking reads and report only observed loop positions, not guessed epochs."""
from pathlib import Path
from datetime import datetime
import ast
import json
import subprocess
import sys
import time
import psutil

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from handoff_distribution_views_progress_monitor_20261006 import read, sha, create
from run_dependency_queue_v3_20261006 import owned


def summarize(value):
    threads = value if isinstance(value, list) else value.get('threads', [value])
    fits = []
    for thread in threads:
        frames = thread.get('frames', [])
        for frame in frames:
            if frame.get('name') == 'fit_arrays' and Path(frame['filename']).name == 'train_diverse_backbones_20261003.py':
                values = {local['name']: local['repr'] for local in frame.get('locals', [])}
                epoch, offset = int(values['epoch']), int(values['offset'])
                losses = ast.literal_eval(values['losses'])
                assert len(losses) == epoch and 0 <= epoch < 32
                assert 0 <= offset < 2594048 and offset % 32768 == 0
                fits.append({'epoch_zero_based': epoch, 'actual_current_epoch_one_based': epoch + 1,
                    'actual_completed_epochs': len(losses), 'actual_batch_offset': offset,
                    'actual_current_batch_one_based': offset // 32768 + 1,
                    'observed_completed_epoch_training_losses': losses,
                    'actual_phase_top_frames': [{key: item.get(key) for key in ('name', 'short_filename', 'line')}
                        for item in frames[:7]], 'fit_arrays_source_line': frame['line']})
    assert len(fits) == 1
    return fits[0]


def main():
    out = A / 'neural16384_actual_training_progress_diagnostics_20261006'
    assert not out.exists()
    first = A / 'neural16384_readonly_stack_diagnostics_20261006'
    frozen = read(first / 'frozen_before_actual_readonly_sampling.json')
    row = frozen['actual_owned_trainer']
    assert owned(row)
    for path, digest in frozen['input_sha256'].items():
        assert sha(path) == digest
    receipt = frozen['actual_verified_diagnostic_binary']
    executable = Path(receipt['binary'])
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    options = dict(cwd=ROOT, stdin=subprocess.DEVNULL, startupinfo=startup,
        creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True, text=True,
        encoding='utf-8', errors='replace', timeout=20)
    out.mkdir()
    original = summarize(read(first / 'actual_dump_stdout.json'))
    samples = [{'at_local': read(first / 'actual_sampling_result.json')['at_local'], **original}]
    create(out / 'frozen_before_followup_sampling.json', {
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_owned_trainer': row,
        'input_sha256': {**frozen['input_sha256'], str(Path(__file__).resolve()): sha(__file__)},
        'first_actual_observation': original, 'expected_followup_reads': 3,
        'nonblocking_readonly_sampling_only': True, 'new_model_fits': 0, 'new_quality_scores': 0})
    before_cpu = sum(psutil.Process(row['owned_worker_pid']).cpu_times()[:2])
    for index in range(3):
        assert owned(row)
        result = subprocess.run([str(executable), 'dump', '--pid', str(row['owned_worker_pid']),
            '--nonblocking', '--locals', '--json'], **options)
        (out / f'actual_dump_{index}.json').write_text(result.stdout, encoding='utf-8')
        (out / f'actual_stderr_{index}.txt').write_text(result.stderr, encoding='utf-8')
        assert result.returncode == 0, result.stderr
        sample = {'at_local': datetime.now().isoformat(timespec='seconds'), **summarize(json.loads(result.stdout))}
        samples.append(sample)
        print(json.dumps({key: sample[key] for key in ('at_local', 'actual_current_epoch_one_based',
            'actual_completed_epochs', 'actual_current_batch_one_based')}, ensure_ascii=False), flush=True)
        if index < 2:
            time.sleep(10)
    assert owned(row)
    for path, digest in frozen['input_sha256'].items():
        assert sha(path) == digest
    positions = [(sample['epoch_zero_based'], sample['actual_batch_offset']) for sample in samples]
    assert positions == sorted(positions)
    advanced = len(set(positions)) > 1
    create(out / 'verification.json', {
        'status': 'passed_actual_nonblocking_owned_training_loop_observations',
        'at_local': datetime.now().isoformat(timespec='seconds'), 'actual_owned_trainer': row,
        'actual_samples': samples, 'actual_training_loop_position_advanced': advanced,
        'maximum_observed_current_epoch': max(s['actual_current_epoch_one_based'] for s in samples),
        'maximum_observed_completed_epochs': max(s['actual_completed_epochs'] for s in samples),
        'actual_training_process_CPU_seconds_advanced': sum(psutil.Process(row['owned_worker_pid']).cpu_times()[:2]) - before_cpu,
        'training_source_and_binary_hashes_unchanged': True, 'training_not_paused_restarted_or_modified': True,
        'new_model_fits_by_diagnostics': 0, 'new_quality_scores': 0,
        'full32_epoch2021_model_still_incomplete': True, 'global_resource_boundary_established': False,
        'same_position_in_short_interval_would_not_prove_stall': True,
        'sampling_is_non_atomic_and_observations_are_consistency_checked': True,
        'test_labels_read': False})
    print(json.dumps({'status': 'passed', 'actual_loop_advanced': advanced,
        'observed_current_epoch': samples[-1]['actual_current_epoch_one_based'],
        'completed_epochs': samples[-1]['actual_completed_epochs'],
        'current_batch': samples[-1]['actual_current_batch_one_based'],
        'whole_fit_not_yet_complete': True}), flush=True)


if __name__ == '__main__':
    main()

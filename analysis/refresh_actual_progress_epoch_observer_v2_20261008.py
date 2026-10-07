"""Replace only the exact task-owned lightweight observer with an epoch-aware receiver."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from handoff_ready_goss_full_execution_20261006 import pair
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    old = A / 'monitor_actual_manual_resume_v1_20261008.py'
    new = A / 'monitor_actual_manual_resume_v2_20261008.py'
    text = old.read_text(encoding='utf8').replace('import json\n', 'import json\nimport re\n')
    marker = "    write(A / 'actual_manual_resume_progress_20261008.json', state)"
    assert text.count(marker) == 1
    addition = """    log = A / 'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v2_20261008/stdout.log'
    if log.exists():
        with log.open('rb') as stream:
            stream.seek(max(0, log.stat().st_size - 32768))
            tail = stream.read().decode('utf8', errors='replace')
        epochs = re.findall(r'BF16 micro8192 epoch (\\d+)/(\\d+) loss=([\\d.eE+-]+) fit_seconds=([\\d.]+)', tail)
        saved = re.findall(r'durable_epoch=(\\d+) checkpoint_seconds=([\\d.]+)', tail)
        if epochs:
            epoch, total, loss, seconds = epochs[-1]
            state['new_BF16_latest_actual_epoch'] = {'completed_epoch': int(epoch), 'total_epochs': int(total),
                'training_loss': float(loss), 'fit_seconds': float(seconds),
                'durable_saved_epoch': int(saved[-1][0]) if saved else None,
                'checkpoint_seconds': float(saved[-1][1]) if saved else None,
                'validation_quality_or_full_annual_speedup_not_inferred_from_training_loss': True}
"""
    text = text.replace(marker, addition + marker)
    marker = "    lines += ['', '实际进程：']"
    assert text.count(marker) == 1
    text = text.replace(marker, "    if 'new_BF16_latest_actual_epoch' in state:\n        lines += ['', '最新实际训练轮次：' + json.dumps(state['new_BF16_latest_actual_epoch'], ensure_ascii=False)]\n" + marker)
    compile(text, str(new), 'exec')
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    path = A / 'service_owned_workflows_20261006/actual_manual_resume_progress_monitor_v1_20261008/native_launch.json'
    row = read(path)
    assert owned(row)
    parent, worker = pair(row)
    assert all(p.pid == worker.pid or p.name().lower() == 'conhost.exe' for p in parent.children(recursive=True))
    proof = A / 'actual_progress_epoch_observer_replacement_v2_20261008.json'
    create(proof, {'status': 'replace_only_exact_owned_lightweight_observer_no_model_or_scoring_worker_touched',
        'original_identity': row, 'input_sha256': {str(p): sha(p) for p in [Path(__file__), old, new, path]}})
    worker.terminate()
    worker.wait(timeout=10)
    if parent.is_running(): parent.terminate(); parent.wait(timeout=10)
    assert not owned(row)
    pins = {str(p): sha(p) for p in [new, proof]}
    current = start('actual_manual_resume_progress_monitor_v2_20261008', new.name, [], pins)
    create(A / 'actual_progress_epoch_observer_hidden_launch_v2_20261008.json', {
        'status': 'started_fresh_epoch_aware_hidden_observer', 'identity': current, 'input_sha256': pins})
    print(current['owned_worker_pid'], flush=True)


if __name__ == '__main__': main()

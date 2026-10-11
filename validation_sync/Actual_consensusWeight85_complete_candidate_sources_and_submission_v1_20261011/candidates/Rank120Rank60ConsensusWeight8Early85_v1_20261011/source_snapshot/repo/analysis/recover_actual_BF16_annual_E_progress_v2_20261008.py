"""Retain the pretraining E-path observer failure and start a fresh E-native receiver."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    service = A / 'service_owned_workflows_20261006/actual_neural_BF16_micro8192_bank6_v1_20261008'
    assert not owned(read(service / 'native_launch.json'))
    assert read(service / 'service_execution.json')['status'] == 'failed'
    error = (service / 'stderr.log').read_text(encoding='utf8')
    assert "path.is_relative_to(ROOT/'analysis')" in error
    old = A / 'train_neural_BF16_micro8192_bank6_v1_20261008.py'
    previous = Path('E:/赛题五_本机临时/neural_BF16_micro8192_bank6_20261008')
    assert (previous / '2020/frozen_training_inputs.json').exists()
    assert not list(previous.rglob('*.joblib')) and not list(previous.rglob('raw.parquet'))
    new = A / 'train_neural_BF16_micro8192_bank6_v2_20261008.py'
    text = old.read_text(encoding='utf8')
    before = 'from atomic_optimization_observer_writes_20261005 import write'
    after = """import json
import uuid

def write(path, data):
    path = Path(path).resolve()
    assert path.is_relative_to(OUT.resolve()) and path.drive.upper() == 'E:' and path.suffix == '.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.part')
    with temporary.open('x', encoding='utf8', newline='\\n') as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\\n'); stream.flush(); os.fsync(stream.fileno())
    os.replace(temporary, path)
"""
    assert text.count(before) == 1
    text = text.replace(before, after).replace('neural_BF16_micro8192_bank6_20261008', 'neural_BF16_micro8192_bank6_v2_20261008')
    text = text.replace('actual_BF16_micro8192_bank6_location_20261008.json', 'actual_BF16_micro8192_bank6_location_v2_20261008.json')
    compile(text, str(new), 'exec')
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    paths = [Path(__file__), old, new, service / 'service_execution.json', service / 'stderr.log',
             previous / 'protocol.json', previous / '2020/frozen_training_inputs.json',
             A / 'neural_BF16_micro8192_native_v1_20261008.py',
             A / 'epoch_durable_neural_checkpoint_adapter_v2_20261007.py', A / 'train_diverse_backbones_20261003.py']
    pins = {str(p): sha(p) for p in paths}
    create(A / 'actual_BF16_annual_E_progress_recovery_v2_20261008.json', {
        'status': 'fresh_E_native_observer_receiver_after_actual_pretraining_path_guard_failure',
        'input_sha256': pins, 'actual_native_fits_before_failure': 0,
        'native_BF16_training_and_prediction_source_unchanged': True,
        'old_partial_frozen_training_population_preserved': True, 'test_labels_read': False})
    row = start('actual_neural_BF16_micro8192_bank6_v2_20261008', new.name, [], pins)
    create(A / 'actual_neural_BF16_micro8192_bank6_v2_20261008_hidden_launch.json',
           {'status': 'started_fresh_E_native_annual_receiver', 'identity': row, 'input_sha256': pins, 'new_quality_scores': 0})
    print(row['owned_worker_pid'], flush=True)


if __name__ == '__main__': main()

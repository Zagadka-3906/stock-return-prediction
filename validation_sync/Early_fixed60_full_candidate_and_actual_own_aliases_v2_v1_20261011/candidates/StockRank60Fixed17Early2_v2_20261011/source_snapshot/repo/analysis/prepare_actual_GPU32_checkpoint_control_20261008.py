"""Run the preserved checkpoint adapter in three real GPU processes before wide-fit use."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import sha, create
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start


def main():
    original = A / 'verify_epoch_durable_neural_checkpoint_CPU32_v2_20261007.py'
    new = A / 'verify_epoch_durable_neural_checkpoint_GPU32_v1_20261008.py'
    text = original.read_text(encoding='utf8')
    text = text.replace('Actual fresh-process CPU32 training', 'Actual fresh-process GPU32 small-network training')
    text = text.replace('epoch_durable_CPU32_v2_20261007', 'epoch_durable_GPU32_v1_20261008')
    text = text.replace('epoch_durable_neural_checkpoint_CPU32_preflight_v2_20261007', 'epoch_durable_neural_checkpoint_GPU32_preflight_v1_20261008')
    text = text.replace('import numpy as np,joblib', 'import numpy as np,joblib,torch')
    text = text.replace('import subprocess,joblib,numpy as np', 'import subprocess,joblib,numpy as np,torch')
    needle = "with patch('torch.cuda.is_available',return_value=False):"
    assert text.count(needle) == 2
    text = text.replace(needle, 'with torch.cuda.device(0):')
    needle = '    fit,generated_sha=install(native);x,y=inputs()'
    text = text.replace(needle, "    assert torch.cuda.is_available(), 'No real GPU available; no CPU substitution.'\n" + needle)
    needle = '    assert not OUT.exists();OUT.mkdir();SCRATCH.mkdir(parents=True,exist_ok=True)'
    text = text.replace(needle, "    assert torch.cuda.is_available(), 'No real GPU available; no CPU substitution.'\n" + needle)
    text = text.replace('actual_GPU_equivalence_not_claimed', 'original_wide16384_GPU_equivalence_not_claimed')
    text = text.replace('passed_actual_fresh_process_CPU32_epoch7_restart_all_weights_losses_and_predictions_exact',
                        'passed_actual_fresh_process_GPU32_small_network_epoch7_restart_all_weights_losses_and_predictions_exact')
    text = text.replace("'actual_GPU_equivalence_not_yet_verified':True", "'actual_small_network_GPU_equivalence_verified':True,'GPU_device_name':torch.cuda.get_device_name(0),'original_wide16384_GPU_equivalence_not_claimed':True")
    needle = "for key in ('TEMP','TMP','TMPDIR','MPLCONFIGDIR'):os.environ[key]=str(SCRATCH)"
    assert text.count(needle) == 1
    text = text.replace(needle, needle + "\nfor key in ('TORCH_HOME','TORCHINDUCTOR_CACHE_DIR','TRITON_CACHE_DIR','CUDA_CACHE_PATH'):os.environ[key]=str(SCRATCH/key)\nos.environ['CUDA_CACHE_DISABLE']='1'")
    compile(text, str(new), 'exec')
    assert not new.exists()
    new.write_text(text, encoding='utf8', newline='\n')
    pins = {str(p): sha(p) for p in [Path(__file__), original, new,
        A / 'epoch_durable_neural_checkpoint_adapter_v2_20261007.py', A / 'train_diverse_backbones_20261003.py']}
    row = start('actual_GPU32_checkpoint_fresh_process_control_20261008', new.name, [], pins)
    create(A / 'actual_GPU32_checkpoint_control_hidden_launch_20261008.json', {
        'status': 'started_actual_small_GPU32_original_vs7_plus25_control', 'identity': row,
        'input_sha256': pins, 'actual_wide16384_training_not_started': True,
        'new_quality_scores': 0, 'actual_complete_native_annual_fits_added': 0})
    print('Started actual GPU32 checkpoint controls in hidden fresh processes.', flush=True)


if __name__ == '__main__':
    main()

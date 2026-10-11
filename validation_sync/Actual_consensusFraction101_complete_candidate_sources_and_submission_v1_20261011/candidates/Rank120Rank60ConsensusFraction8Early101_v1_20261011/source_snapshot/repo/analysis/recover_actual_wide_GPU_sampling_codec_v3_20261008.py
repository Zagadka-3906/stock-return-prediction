"""Correct only the failed WDDM file decoder; keep actual partial warmup evidence."""
from pathlib import Path
import codecs
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
from run_dependency_queue_v3_20261006 import read, sha, create, owned
from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start

failed = A / 'service_owned_workflows_20261006/actual_wide_GPU_precision3_resource_benchmark_v2_20261008'
assert not owned(read(failed / 'native_launch.json'))
assert read(failed / 'service_execution.json')['status'] == 'failed'
assert 'unknown encoding: utf8-sig' in (failed / 'stderr.log').read_text(encoding='utf8')
old_output = Path('E:/赛题五_本机临时/GPU实测_20261008/wide16384_micro8192_precision3_v2')
sample = old_output / 'FP32_micro8192_accum4_step0.wddm.json'
assert codecs.lookup('utf-8-sig')
actual = json.loads(sample.read_text(encoding='utf-8-sig'))
assert actual
old = A / 'benchmark_actual_wide_GPU_precision3_v2_20261008.py'
new = A / 'benchmark_actual_wide_GPU_precision3_v3_20261008.py'
text = old.read_text(encoding='utf8')
assert text.count("encoding='utf8-sig'") == 1
text = text.replace("encoding='utf8-sig'", "encoding='utf-8-sig'")
text = text.replace('wide16384_micro8192_precision3_v2', 'wide16384_micro8192_precision3_v3')
text = text.replace("'effective_batch_size': 32768, 'microbatch_size': 8192,", "'effective_batch_size': 32768, 'microbatch_size': 8192,'actual_allow_tf32':torch.backends.cuda.matmul.allow_tf32,'actual_autocast_dtype':'bfloat16' if bf16 else 'float32',")
compile(text, str(new), 'exec')
assert not new.exists()
new.write_text(text, encoding='utf8', newline='\n')
paths = [Path(__file__), old, new, sample, failed / 'service_execution.json', failed / 'stderr.log',
    old_output / 'frozen_before_actual_GPU_benchmark.json']
pins = {str(p): sha(p) for p in paths}
proof = A / 'actual_wide_GPU_WDDM_codec_recovery_v3_20261008.json'
create(proof, {'status': 'actual_sample_JSON_decoder_checked_before_fresh_same_recipe_benchmark',
    'input_sha256': pins, 'preserved_actual_partial_FP32_warmup_WDDM_sample': actual,
    'original_V2_did_not_complete_3_recipe_benchmark': True, 'same_predeclared_training_recipes': True,
    'new_complete_annual_fits': 0, 'new_quality_scores': 0})
pins[str(proof)] = sha(proof)
row = start('actual_wide_GPU_precision3_resource_benchmark_v3_20261008', new.name, [], pins)
create(A / 'actual_wide_GPU_precision3_hidden_launch_v3_20261008.json', {'identity': row, 'input_sha256': pins})
print('Actual sample decoder verified; fresh wide precision3 benchmark launched.', flush=True)

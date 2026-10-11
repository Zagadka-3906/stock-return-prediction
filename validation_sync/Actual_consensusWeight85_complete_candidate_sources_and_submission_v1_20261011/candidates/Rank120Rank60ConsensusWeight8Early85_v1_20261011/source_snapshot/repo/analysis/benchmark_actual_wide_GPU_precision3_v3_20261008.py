"""Bounded past-only wide-network GPU timing; distinct recipes, no annual fit or quality score."""
from pathlib import Path
import gc
import hashlib
import json
import os
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]
OUT = Path('E:/赛题五_本机临时/GPU实测_20261008/wide16384_micro8192_precision3_v3')
for key in ('TEMP', 'TMP', 'TMPDIR', 'MPLCONFIGDIR', 'TORCH_HOME', 'TORCHINDUCTOR_CACHE_DIR', 'TRITON_CACHE_DIR', 'CUDA_CACHE_PATH'):
    os.environ[key] = str(OUT / 'tmp' / key)
os.environ['CUDA_CACHE_DISABLE'] = '1'
os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
from run_dependency_queue_v3_20261006 import read, sha, create


def wddm_sample(tag):
    shell = Path('C:/Users/esesl/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')
    cmd = ("Get-CimInstance Win32_PerfFormattedData_GPUPerformanceCounters_GPUProcessMemory | "
           "Where-Object { $_.Name -like 'pid_" + str(os.getpid()) + "_*' } | "
           "Select-Object Name,DedicatedUsage,SharedUsage,TotalCommitted | ConvertTo-Json -Compress")
    output, errors = OUT / (tag + '.wddm.json'), OUT / (tag + '.wddm.stderr')
    with output.open('wb') as stream, errors.open('wb') as stderr:
        result = subprocess.run([str(shell), '-NoLogo', '-NoProfile', '-Command', cmd], stdout=stream,
            stderr=stderr, stdin=subprocess.DEVNULL, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW, close_fds=True)
    assert result.returncode == 0, errors.read_text(encoding='utf8', errors='replace')
    rows = json.loads(output.read_text(encoding='utf-8-sig'))
    if isinstance(rows, dict): rows = [rows]
    assert rows and all(r['Name'].startswith('pid_' + str(os.getpid()) + '_') for r in rows)
    return {'dedicated_bytes': sum(int(r['DedicatedUsage']) for r in rows),
            'shared_bytes': sum(int(r['SharedUsage']) for r in rows), 'rows': rows}


def main():
    import numpy as np
    import joblib
    import polars as pl
    import psutil
    import torch
    import train_diverse_backbones_20261003 as native
    from run import FEATURE_FILE, MANIFEST, feature_names, fold_cutoff, to_matrix
    from optimize_training_round12 import KEYS
    from contextlib import nullcontext
    assert torch.cuda.is_available(), 'No real GPU; no CPU substitution.'
    assert not OUT.exists()
    OUT.mkdir(parents=True)
    while psutil.virtual_memory().available < 11 * 2**30: time.sleep(10)
    storage = read(A / 'neural16384_full_storage_20261005.json')
    bank = Path(storage['output_directory']) / 'rank16384_drop000_seed07_e32'
    info_path, model_path = bank / 'info_2021.json', bank / 'model_2021.joblib'
    info = read(info_path)
    assert info['status'] == 'passed' and sha(model_path) == info['model_sha256']
    cfg = info['configuration']
    assert cfg['hidden'] == [16384, 8192, 4096] and cfg['dropout'] == 0.0
    cutoff = fold_cutoff(2021)
    assert cutoff == info['training_meta']['cutoff_exclusive']
    features = feature_names()
    assert features == info['training_meta']['features']
    lazy = pl.scan_parquet(FEATURE_FILE)
    frame = native.training_frame(lazy, cutoff, cfg).select(KEYS + features + ['y_rank']).sort('trade_date', 'ts_code').head(65536).collect()
    assert len(frame) == 65536 and int(frame['trade_date'].max()) < cutoff
    dates = lazy.filter(pl.col('is_train')).select('trade_date').unique().sort('trade_date').collect()['trade_date'].to_numpy()
    end = int(dates[np.searchsorted(dates, int(frame['trade_date'].max())) + 1])
    assert end <= cutoff
    x = to_matrix(frame, features)
    y = frame['y_rank'].to_numpy()
    assert np.isfinite(y).all()
    bundle = joblib.load(model_path)
    mean, scale = bundle['mean'].copy(), bundle['scale'].copy()
    del bundle
    gc.collect()
    clean = np.clip((np.where(np.isfinite(x), x, mean) - mean) / scale, -8.0, 8.0).astype(np.float32)
    target = y.astype(np.float32) - .5
    np.save(OUT / 'past_only_features.npy', x)
    np.save(OUT / 'past_only_rank_targets.npy', y)
    paths = [Path(__file__), Path(native.__file__), MANIFEST, info_path, model_path,
             OUT / 'past_only_features.npy', OUT / 'past_only_rank_targets.npy']
    pins = {str(p): sha(p) for p in paths}
    create(OUT / 'frozen_before_actual_GPU_benchmark.json', {
        'input_sha256': pins, 'own_mature_year': 2021, 'rows': len(frame), 'features': features,
        'first_date': int(frame['trade_date'].min()), 'last_date': int(frame['trade_date'].max()),
        'last_label_end': end, 'cutoff_exclusive': cutoff, 'own_full_window_preprocessing_reused': True,
        'architecture': cfg['hidden'], 'original_full_training_rows': info['training_meta']['rows'],
        'outer_batch_size': 32768, 'microbatch_size': 8192, 'warmup_updates': 1, 'timed_updates': 3,
        'recipes': ['FP32_micro8192_accum4', 'BF16_micro8192_accum4', 'FP32_TF32_micro8192_accum4'],
        'recipes_not_claimed_bit_identical_to_original32768': True,
        'training_subset_timing_not_full_annual_or_original_large_batch_speedup': True,
        'test_labels_read': False, 'new_quality_scores': 0})
    del frame, x, y
    gc.collect()
    torch.set_num_threads(8)
    torch.use_deterministic_algorithms(True)
    xt, yt = torch.from_numpy(clean).cuda(), torch.from_numpy(target).cuda()
    records = []
    for recipe in ('FP32_micro8192_accum4', 'BF16_micro8192_accum4', 'FP32_TF32_micro8192_accum4'):
        bf16 = recipe.startswith('BF16')
        if bf16 and not torch.cuda.is_bf16_supported():
            records.append({'recipe': recipe, 'status': 'actual_device_BF16_unsupported'})
            continue
        torch.manual_seed(cfg['seed'])
        torch.cuda.manual_seed_all(cfg['seed'])
        torch.backends.cuda.matmul.allow_tf32 = 'TF32' in recipe
        torch.backends.cudnn.allow_tf32 = False
        model = native.network(len(features), cfg).cuda()
        model.train()
        optimizer = torch.optim.AdamW(model.parameters(), lr=cfg['learning_rate'], weight_decay=cfg['weight_decay'])
        order = torch.randperm(len(clean), device='cuda')
        elapsed, losses, samples = [], [], []
        for step in range(4):
            index = order[(step % 2) * 32768:(step % 2 + 1) * 32768]
            optimizer.zero_grad(set_to_none=True)
            torch.cuda.synchronize()
            if step == 1: torch.cuda.reset_peak_memory_stats()
            started = time.perf_counter()
            total = 0.0
            for offset in range(0, len(index), 8192):
                part = index[offset:offset + 8192]
                context = torch.autocast('cuda', dtype=torch.bfloat16) if bf16 else nullcontext()
                with context: pred = model(xt[part]).squeeze(-1)
                loss = torch.nn.functional.mse_loss(pred.float(), yt[part]) * (len(part) / len(index))
                assert torch.isfinite(loss)
                loss.backward()
                total += float(loss.detach())
            optimizer.step()
            torch.cuda.synchronize()
            seconds = time.perf_counter() - started
            if step:
                elapsed.append(seconds)
                losses.append(total)
            samples.append(wddm_sample(recipe + '_step' + str(step)))
        assert all(torch.isfinite(p).all().item() for p in model.parameters())
        record = {'recipe': recipe, 'status': 'passed_actual_wide3_updates_finite',
            'effective_batch_size': 32768, 'microbatch_size': 8192,'actual_allow_tf32':torch.backends.cuda.matmul.allow_tf32,'actual_autocast_dtype':'bfloat16' if bf16 else 'float32',
            'timed_update_seconds': elapsed, 'median_timed_update_seconds': statistics.median(elapsed),
            'training_losses': losses, 'CUDA_peak_allocated_bytes': torch.cuda.max_memory_allocated(),
            'CUDA_peak_reserved_bytes': torch.cuda.max_memory_reserved(),
            'observed_WDDM_dedicated_max_bytes': max(r['dedicated_bytes'] for r in samples),
            'observed_WDDM_shared_max_bytes': max(r['shared_bytes'] for r in samples),
            'WDDM_observations_not_continuous_peak': samples}
        records.append(record)
        create(OUT / (recipe + '_actual.json'), record)
        print(json.dumps({k: record[k] for k in ('recipe', 'median_timed_update_seconds', 'observed_WDDM_shared_max_bytes')}, ensure_ascii=False), flush=True)
        del model, optimizer
        gc.collect()
        torch.cuda.empty_cache()
    for p, digest in pins.items(): assert sha(p) == digest, p
    create(OUT / 'verification.json', {'status': 'passed_actual_own_mature_subset_wide_GPU_precision3_resource_benchmark',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'input_sha256': pins, 'records': records,
        'GPU_device_name': torch.cuda.get_device_name(0), 'original_configuration': cfg,
        'original_batch32768_recipe_not_rebenchmarked': True,
        'subset_feature_tensor_smaller_than_full_annual_tensor': True,
        'wall_clock_or_memory_differences_do_not_prove_full_annual_speedup': True,
        'new_complete_annual_models': 0, 'new_quality_scores': 0, 'test_labels_read': False})
    create(A / 'actual_wide_GPU_precision3_benchmark_location_20261008.json', {
        'status': 'actual_benchmark_passed_on_authorized_E_drive', 'output': str(OUT),
        'verification_sha256': sha(OUT / 'verification.json'), 'new_quality_scores': 0})


if __name__ == '__main__':
    main()

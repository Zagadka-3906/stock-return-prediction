"""Actual saved composite, parent linear and inherited Nyström codec controls."""
from pathlib import Path
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def main():
    import numpy as np
    import polars as pl
    import build_linear_leaf_ensemble_bank_20261005 as bank
    import fourier_tuning_model_sources_20261004 as legacy
    import train_nystrom_tuning_bank_20261005 as nystrom
    from linear_leaf_ensemble_future_codec_adapter_20261005 import install
    out = ROOT / 'analysis/linear_leaf_ensemble_future_codec_preflight_20261005'
    out.mkdir(exist_ok=True)
    proof = ROOT / 'analysis/linear_leaf_ensemble_complementarity_v2_20261005/verification.json'
    assert bank.read(proof)['status'] == 'passed_actual_five_year_mixture_native_reload_and_prefix_controls'
    for name in bank.CONFIGS:
        path=bank.OUT/name/'model_2020.joblib'
        assert path.exists(),path
    paths = [Path(__file__), ROOT / 'analysis/linear_leaf_ensemble_future_codec_adapter_20261005.py',ROOT / 'analysis/linear_leaf_future_codec_adapter_20261005.py',
        ROOT / 'analysis/nystrom_future_codec_adapter_20261005.py', Path(bank.__file__), proof]
    paths += [bank.OUT/name/'model_2020.joblib' for name in bank.CONFIGS]
    paths += [bank.parent.OUT/name/'model_2020.joblib' for name in bank.parent.CONFIGS]
    bindings = {str(path): bank.sha(path) for path in paths}
    bank.dump(out / 'frozen_before_codec_controls.json', {
        'status': 'frozen_before_native_codec_checks', 'source_sha256': bindings,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    features = bank.engine.feature_names()
    lazy = pl.scan_parquet(bank.engine.FEATURE_FILE)
    frame = bank.engine.training_frame(lazy, bank.engine.fold_cutoff(2020),
        next(iter(bank.CONFIGS.values()))).select(features).head(131).collect()
    x = bank.engine.to_matrix(frame, features)
    original = legacy.predict_arrays
    checks = []
    restore = install()
    try:
        for name in bank.CONFIGS:
            path = bank.OUT/name/'model_2020.joblib'
            bundle = legacy.load_bundle(path)
            assert np.array_equal(legacy.predict_arrays(bundle, x), bank.predict_arrays(bundle, x))
            checks.append({'model': name, 'model_sha256': bank.sha(path),
                           'actual131_row_saved_composite_model_dispatch_exact': True})
        for name in bank.parent.CONFIGS:
            path=bank.parent.OUT/name/'model_2020.joblib'
            bundle=legacy.load_bundle(path)
            assert np.array_equal(legacy.predict_arrays(bundle,x),bank.parent.predict_arrays(bundle,x))
            checks.append({'model':name,'model_sha256':bank.sha(path),'actual131_row_saved_parent_native_dispatch_exact':True})
        proof = bank.read(ROOT / 'analysis/nystrom_tuning_future_qa_20261005/verification.json')
        for row in proof['checks']:
            path = ROOT / f"analysis/nystrom_tuning_future_qa_20261005/{row['model']}.joblib"
            bundle = legacy.load_bundle(path)
            assert np.array_equal(legacy.predict_arrays(bundle, x), nystrom.predict_arrays(bundle, x))
            checks.append({'model': row['model'], 'model_sha256': bank.sha(path),
                           'actual131_row_existing_nystrom_dispatch_exact': True})
    finally:
        restore()
    assert legacy.predict_arrays is original
    for path, expected in bindings.items():
        assert bank.sha(path) == expected, path
    bank.dump(out / 'verification.json', {'status': 'passed',
        'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'), 'source_sha256': bindings,
        'checks': checks, 'all8_ensemble_and6_linear_and10_nystrom_saved_models_dispatched_exactly': True,
        'native_codec_binding_restored': True, 'actual_annual_fits': 0,
        'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print('Passed saved native codec controls for all8 composite,6 parent linear and10 inherited Nyström models.', flush=True)


if __name__ == '__main__':
    main()

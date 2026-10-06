"""Check unhooked GOSS routes and inherited models, then the restored full codec."""
from pathlib import Path
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path[:0] = [str(ROOT), str(A)]


def main():
    import numpy as np
    import polars as pl
    import train_gradient_sampling_bank_20261005 as bank
    import gradient_sampling_model_sources_20261005 as router
    import fourier_tuning_model_sources_20261004 as legacy
    from gradient_sampling_future_codec_adapter_20261005 import install
    import train_factorization_machine_bank_20261005 as fm
    import train_nystrom_tuning_bank_20261005 as nystrom
    import train_linear_leaf_bank_20261005 as leaves
    import build_linear_leaf_ensemble_bank_20261005 as ensemble
    out = A / 'gradient_sampling_direct_router_preflight_20261005'
    out.mkdir(exist_ok=True)
    proof = A / 'gradient_sampling_preflight_20261005/verification.json'
    assert bank.read(proof)['status'] == 'passed_actual_gradient_sampling_maturity_native_reload_and_prefix_controls'
    sources = [Path(__file__), Path(bank.__file__), Path(router.__file__), proof,
        A / 'gradient_sampling_future_codec_adapter_20261005.py']
    bindings = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    bank.dump(out / 'frozen_before_controls.json', {'status': 'frozen_before_actual_direct_and_hooked_checks',
        'input_sha256': bindings, 'new_GOSS_artifacts_are48round_pilots_only': True,
        'inherited_artifacts_are_actual_complete_native_models': True, 'new_quality_scores': 0}, immutable=True)
    features = bank.engine.feature_names()
    frame = bank.engine.training_frame(pl.scan_parquet(bank.engine.FEATURE_FILE), bank.engine.fold_cutoff(2020),
        next(iter(bank.CONFIGS.values()))).select(features).head(131).collect()
    x = bank.engine.to_matrix(frame, features)
    cases = [(name, A / f'gradient_sampling_preflight_20261005/{name}.joblib', bank) for name in bank.CONFIGS]
    for native, folder in ((fm, 'factorization_machine_future_qa_v2_20261005'),
        (nystrom, 'nystrom_tuning_future_qa_20261005'), (leaves, 'linear_leaf_future_qa_20261005'),
        (ensemble, 'linear_leaf_ensemble_future_qa_20261005')):
        inherited = bank.read(A / folder / 'verification.json')
        assert inherited['status'] == 'passed'
        cases.extend((row['model'], A / folder / f"{row['model']}.joblib", native) for row in inherited['checks'])
    original = legacy.predict_arrays
    controls = []
    for name, path, native in cases:
        bundle = router.load_bundle(path)
        actual, expected = router.predict_arrays(bundle, x), native.predict_arrays(bundle, x)
        assert np.array_equal(actual, expected), name
        assert all(np.array_equal(actual[:n], router.predict_arrays(router.load_bundle(path), x[:n])) for n in (1, 80, 130))
        controls.append({'model': name, 'saved_kind': bundle['kind'],
            'model_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'unhooked_direct131_row_route_and_native_prefixes_bit_exact': True,
            'new_GOSS_model_is_pilot': name in bank.CONFIGS})
    assert len(controls) == 36 and legacy.predict_arrays is original
    restore = install()
    try:
        for name, path, native in cases:
            assert np.array_equal(legacy.predict_arrays(legacy.load_bundle(path), x), native.predict_arrays(router.load_bundle(path), x)), name
    finally:
        restore()
    assert legacy.predict_arrays is original
    for source, expected in bindings.items():
        assert hashlib.sha256(Path(source).read_bytes()).hexdigest() == expected, source
    bank.dump(out / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'source_sha256': bindings, 'checks': controls, 'actual_checks': 36,
        'unhooked_direct_routes_and_all_hooked_routes_passed': True, 'legacy_codec_restored': True,
        'new_GOSS_complete_annual_and_future_fits_still_pending': True,
        'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print('Passed actual6 GOSS pilot and30 inherited direct/codec routes', flush=True)


if __name__ == '__main__':
    main()

"""Exercise the actual public router directly, with no legacy codec hook masking it."""
from pathlib import Path
import hashlib
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / 'analysis')]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    import numpy as np
    import polars as pl
    import train_factorization_machine_bank_20261005 as bank
    import factorization_machine_model_sources_v2_20261005 as router
    import factorization_machine_model_sources_20261005 as failed_router
    import fourier_tuning_model_sources_20261004 as legacy
    import train_nystrom_tuning_bank_20261005 as nystrom
    import train_linear_leaf_bank_20261005 as leaves
    import build_linear_leaf_ensemble_bank_20261005 as ensemble

    out = ROOT / 'analysis/factorization_machine_direct_router_preflight_v2_20261005'
    out.mkdir(exist_ok=True)
    assert not (out / 'verification.json').exists()
    sources = [Path(__file__), Path(router.__file__), Path(failed_router.__file__), Path(bank.__file__),
               ROOT / 'analysis/factorization_machine_scheme_runtime_v2_20261005.py',
               ROOT / 'analysis/verify_factorization_machine_full_future_v2_20261005.py',
               ROOT / 'analysis/factorization_machine_future_qa_20261005/resource_summary.json',
               ROOT / 'analysis/factorization_machine_trained_interaction_audit_20261005/verification.json',
               ROOT / 'analysis/run_logs/factorization_machine_full_future_20261005.stderr.log']
    bindings = {str(p.resolve()): sha(p) for p in sources}
    bank.dump(out / 'frozen_before_controls.json', {'status': 'frozen_before_direct_public_dispatch_controls',
              'input_sha256': bindings, 'legacy_codec_hook_not_installed': True,
              'actual32_epoch_annual_FM_artifacts_used': True, 'new_quality_scores': 0,
              'test_labels_read': False}, immutable=True)
    original = legacy.predict_arrays
    features = bank.engine.feature_names()
    frame = bank.engine.training_frame(pl.scan_parquet(bank.engine.FEATURE_FILE),
        bank.engine.fold_cutoff(2020), next(iter(bank.CONFIGS.values()))).select(features).head(131).collect()
    x = bank.engine.to_matrix(frame, features)
    fixture = bank.engine.load_bundle(bank.OUT / 'rank_fm_k0_e32/model_2024.joblib')
    try:
        failed_router.predict_arrays(fixture, x)
    except KeyError as error:
        assert error.args == ('hidden',)
    else:
        raise AssertionError('Expected the preserved wrong-kind dispatcher failure.')
    cases = [(name, bank.OUT / name / 'model_2024.joblib', bank) for name in bank.CONFIGS]
    for family, native, folder in (
        ('nystrom', nystrom, 'nystrom_tuning_future_qa_20261005'),
        ('linear_leaf', leaves, 'linear_leaf_future_qa_20261005'),
        ('linear_leaf_ensemble', ensemble, 'linear_leaf_ensemble_future_qa_20261005')):
        proof = bank.read(ROOT / 'analysis' / folder / 'verification.json')
        assert proof['status'] == 'passed'
        cases.extend((row['model'], ROOT / 'analysis' / folder / f"{row['model']}.joblib", native)
                     for row in proof['checks'])
    checks = []
    for name, path, native in cases:
        bundle = router.load_bundle(path)
        actual = router.predict_arrays(bundle, x)
        expected = native.predict_arrays(bundle, x)
        assert np.array_equal(actual, expected), name
        for count in (1, 80, 130):
            assert np.array_equal(actual[:count], router.predict_arrays(router.load_bundle(path), x[:count])), name
        checks.append({'model': name, 'saved_kind': bundle['kind'], 'model_sha256': sha(path),
                       'direct131_row_public_router_matches_native_bit_exactly': True,
                       'prefix_lengths1_80_130_bit_identical': True})
    assert len(checks) == 30
    assert legacy.predict_arrays is original
    for path, expected in bindings.items():
        assert sha(path) == expected, path
    bank.dump(out / 'verification.json', {'status': 'passed', 'at_local': time.strftime('%Y-%m-%dT%H:%M:%S'),
              'source_sha256': bindings, 'checks': checks,
              'all6_actual32_epoch_FM_and24_inherited_models_directly_dispatched_bit_exactly': True,
              'original_hidden_KeyError_reproduced_before_repair': True,
              'legacy_codec_hook_not_installed_or_changed': True,
              'new_model_fits': 0, 'new_quality_scores': 0, 'test_labels_read': False}, immutable=True)
    print('Passed direct saved-model routing for6 complete FM and24 inherited models.', flush=True)


if __name__ == '__main__':
    main()

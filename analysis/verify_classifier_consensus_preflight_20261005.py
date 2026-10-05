"""Check actual complete parent estimators, embedding, reload and typed routing."""
from pathlib import Path
import gc
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'analysis'
sys.path.insert(0, str(A))
OUT = A / 'classifier_consensus_preflight_20261005'
ROUTES = A / 'classifier_consensus_direct_router_preflight_20261005'


def main():
    import build_classifier_consensus_bank_20261005 as bank
    from locked_read_hash_cache_20261004 import LockedReadHashCache
    import numpy as np
    import pyarrow.dataset as ds
    assert not OUT.exists() and not ROUTES.exists()
    OUT.mkdir()
    ROUTES.mkdir()
    sources = [Path(__file__), bank.PLAN, Path(bank.__file__), bank.SOURCE, bank.parent.SOURCE,
        bank.FEATURE_FILE, bank.MANIFEST,
        A / 'classifier_consensus_model_sources_20261005.py',
        A / 'classifier_consensus_future_codec_adapter_20261005.py',
        A / 'run_classifier_consensus_bank_20261005.py',
        A / 'verify_classifier_consensus_full_future_20261005.py',
        A / 'streaming_rank_classifier_future_qa_v3_20261005/verification.json',
        A / 'streaming_classifier_actual_annual_completion_audit_20261005/verification.json',
        A / 'streaming_classifier_actual_final_completion_audit_20261005/verification.json',
        bank.parent.OUT / 'protocol.json', bank.parent.OUT / 'oof_audit.json',
        bank.parent.OUT / 'training_execution_scope.json']
    for year in (2020, 2025):
        sources += list(bank.parent.OUT.glob(f'*/info_{year}.json'))
        sources += list(bank.parent.OUT.glob(f'*/model_{year}.joblib'))
    inputs = {str(p.resolve()): bank.sha(p) for p in dict.fromkeys(sources)}
    bank.dump(OUT / 'frozen_before_controls.json', {'input_sha256': inputs,
        'all_parent_estimators_are_full_actual32pass_models': True,
        'small_prediction_control_not_substitute_for_fullfuture_or_official_quality': True,
        'new_native_fits': 0, 'test_labels_read': False}, immutable=True)
    checks, route_checks, original_sha = [], [], bank.sha
    try:
        with LockedReadHashCache(inputs) as cache:
            bank.sha = cache.sha
            features = bank.parent.feature_names()
            condition = (ds.field('is_train') == True) & (ds.field('trade_date') >= 20200101) & (ds.field('trade_date') < 20210101)
            batch = next(b for b in bank.parent.core.scanner(bank.KEYS + features, condition) if len(b))
            x = bank.parent.core.matrix(batch.slice(0, 131), features)
            import classifier_consensus_model_sources_20261005 as router
            import fourier_tuning_model_sources_20261004 as legacy
            from classifier_consensus_future_codec_adapter_20261005 import install
            original_route = legacy.predict_arrays
            restore = install()
            try:
                for year in (2020, 2025):
                    for name, cfg in bank.CONFIGS.items():
                        bundle, meta, parents = bank.bundle_from(name, year)
                        model = OUT / f'{name}_{year}.joblib'
                        bank.parent.core.save_bundle(model, bundle)
                        loaded = bank.parent.core.load_bundle(model)
                        values = bank.predict_arrays(bundle, x)
                        assert np.array_equal(values, bank.predict_arrays(loaded, x))
                        oracle = np.zeros(len(x), dtype=np.float64)
                        for member in loaded['members']:
                            native = member['bundle']
                            transformed = bank.parent.core.transform(x, native['mean'], native['scale'], native['config']['clip_z'])
                            probabilities = native['classifier'].predict_proba(transformed)
                            if native['config']['rank_objective'] == 'top10':
                                native_values = probabilities[:, 1]
                            else:
                                centers = (native['classifier'].classes_.astype(np.float64) + .5) / 10
                                native_values = probabilities @ centers
                            oracle += member['weight'] * native_values
                        oracle = cfg['output_sign'] * oracle + cfg['output_offset']
                        error = float(np.max(np.abs(values - oracle)))
                        assert error < 1e-12, (name, year, error)
                        for size in (1, 80, 130):
                            assert np.array_equal(values[:size], bank.predict_arrays(loaded, x[:size]))
                        assert np.array_equal(values, router.predict_arrays(loaded, x))
                        assert np.array_equal(values, legacy.predict_arrays(loaded, x))
                        checks.append({'model': name, 'year': year, 'model_sha256': bank.sha(model),
                            'actual_saved_embedded_parent_reload_bit_identical': True,
                            'actual131_rows_and1_80_130_prefix_bit_identical': True,
                            'independent_sklearn_predict_proba_max_abs_error': error,
                            'mature_training_meta': meta, 'parents': parents,
                            'new_native_fits': 0})
                        route_checks.append({'model': name, 'year': year, 'direct_and_future_routes_bit_identical': True})
                        del bundle, loaded, values, oracle
                        gc.collect()
                for name in bank.parent.CONFIGS:
                    model = bank.parent.core.load_bundle(bank.parent.OUT / name / 'model_2020.joblib')
                    values = bank.parent.core.predict_arrays(model, x)
                    assert np.array_equal(values, router.predict_arrays(model, x))
                    assert np.array_equal(values, legacy.predict_arrays(model, x))
                    route_checks.append({'inherited_native_classifier': name, 'preserved_bit_identical': True})
            finally:
                restore()
                assert legacy.predict_arrays is original_route
            cache.reverify()
    finally:
        bank.sha = original_sha
    bank.dump(OUT / 'verification.json', {'status': 'passed_actual_native_parent_consensus_reload_and_prefix',
        'checks': checks, 'actual12_saved_composite_controls': len(checks), 'input_sha256': inputs,
        'all_hash_bindings_restored': True, 'new_native_fits': 0, 'test_labels_read': False,
        'new_quality_scores': 0, 'full_annual_and_full_future_checks_still_required': True}, immutable=True)
    bank.dump(ROUTES / 'verification.json', {'status': 'passed_actual_consensus_and_inherited_routes',
        'checks': route_checks, 'future_codec_restored_to_original_object': True,
        'input_sha256': inputs, 'new_native_fits': 0, 'new_quality_scores': 0,
        'test_labels_read': False}, immutable=True)
    print(json.dumps({'status': 'passed_consensus12_actual_controls_and16_routes',
                      'new_native_fits': 0}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

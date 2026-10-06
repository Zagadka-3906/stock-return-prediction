"""Replay selected CPU MLP residuals after the full saved parent106 native graph."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import os


def predict(ns, record, candidate, parent_curve_source, mapping_path):
    import numpy as np
    import pandas as pd
    import joblib
    from threadpoolctl import threadpool_limits
    import whole_scheme_future_runtime_20261004 as runtime
    from conditional_residual_mlp_CDF_transform_20261007 import prepare, apply_prepared
    from cpu_conditional_residual_mlp_codec_20261007 import predict_native, predict_decoded
    candidate = Path(candidate)
    candidate.mkdir(parents=True, exist_ok=True)
    spec = record['winner'][ns.GRAPH_FIELD]['conditional_flag_CPU_MLP_residual_CDF']
    assert spec['weight'] > 0 and spec['universe'] == 'all_current_raw_forecasts'
    components = deepcopy(spec['native_components'])
    assert 1 <= len(components) <= 4
    assert [c['name'] for c in components] == spec['ordered_equal_mean_components']
    for component in components:
        for source_key, target_key, hash_key, suffix in (
            ('source_path', 'path', 'sha256', '.joblib'),
            ('independent_state_source_path', 'independent_state_path', 'independent_state_sha256', '.json')):
            source = Path(component[source_key])
            target = candidate / (component['name'] + suffix)
            assert ns.sha(source) == component[hash_key]
            if not target.exists():
                if source.drive.upper() == target.drive.upper():
                    os.link(source, target)
                else:
                    import shutil
                    shutil.copyfile(source, target)
            assert ns.sha(target) == component[hash_key]
            component[target_key] = str(target)
    calls = []
    original_build = runtime.build_context

    def build_with_raw_features(graph, inputs, test, *args, **kwargs):
        context, checks = original_build(graph, inputs, test, *args, **kwargs)
        assert test.select(['ts_code', 'trade_date']).equals(inputs.select(['ts_code', 'trade_date']))
        assert not {'y_ret_1d', 'y_rank'} & set(test.columns)
        features = list(test.columns[2:])
        assert len(features) == 63
        # Preserve missing values for the frozen MLP median, rather than the
        # parent's separate float32 cleaning rule.
        context._CPU_MLP_raw_features = test.select(features).to_numpy().astype(np.float64)
        context._CPU_MLP_raw_feature_names = features
        return context, checks

    def after_parent(context, parent_values):
        cfg = context._whole_graph['conditional_flag_CPU_MLP_residual_CDF']
        assert cfg['weight'] == spec['weight'] and cfg['ordered_equal_mean_components'] == spec['ordered_equal_mean_components']
        selected = context.flags == 1
        prepared = prepare(parent_values, context.dates, context.flags, context.valid, cfg['universe'])
        percentile = np.zeros(len(parent_values), dtype=np.float64)
        for _, positions, p, _, _ in prepared:
            percentile[positions] = p
        independent_p = pd.Series(parent_values).groupby(context.dates, sort=False).rank(method='average', pct=True).to_numpy()
        assert np.array_equal(percentile[selected].view(np.uint64), independent_p[selected].view(np.uint64))
        x = np.column_stack([context._CPU_MLP_raw_features[selected], percentile[selected]])
        independent_x = np.column_stack([context._CPU_MLP_raw_features[selected], independent_p[selected]])
        assert np.array_equal(x.view(np.uint64), independent_x.view(np.uint64))
        combined = np.zeros(int(selected.sum()), dtype=np.float64)
        decoded_combined = np.zeros_like(combined)
        controls = []
        with threadpool_limits(limits=4):
            for component in components:
                info = component['training_info']
                assert info['year'] == 2025 and info['actual_epochs'] == 24
                assert info['last_training_label_date'] < info['exclusive_cutoff'] < int(context.dates.min())
                assert info['last_training_label_end'] <= info['exclusive_cutoff']
                assert info['features'] == [*context._CPU_MLP_raw_feature_names, 'qualified106_current_forecast_average_rank_over_N']
                native = Path(component['path'])
                state = Path(component['independent_state_path'])
                assert ns.sha(native) == component['sha256'] and ns.sha(state) == component['independent_state_sha256']
                bundle = joblib.load(native)
                primary = predict_native(bundle, x)
                replay = predict_native(joblib.load(native), x)
                decoded = predict_decoded(ns.read(state), independent_x)
                assert np.array_equal(primary.view(np.uint64), replay.view(np.uint64))
                assert np.array_equal(primary.view(np.uint64), decoded.view(np.uint64))
                combined += primary
                decoded_combined += decoded
                controls.append({'name': 'conditional_cpu_mlp_' + component['name'], 'sha256': component['sha256'],
                    'reload_exact': True, 'independent_NumPy_decoder_exact': True, 'actual_flagged_rows': len(x),
                    'features': info['features'], 'fixed_padded_inference_batch': 256})
        combined /= len(components)
        decoded_combined /= len(components)
        assert np.array_equal(combined.view(np.uint64), decoded_combined.view(np.uint64))
        residual = np.zeros(len(parent_values), dtype=np.float64)
        residual[selected] = combined
        values = apply_prepared(parent_values, residual, cfg['weight'], prepared)
        independent = np.asarray(parent_values).copy()
        for _, positions, _, knots, ordered in prepared:
            q = independent_p[positions] + float(cfg['weight']) * decoded_combined[np.searchsorted(np.flatnonzero(selected), positions)]
            independent[positions] = np.interp(np.clip(q, knots[0], knots[-1]), knots, ordered)
        assert np.array_equal(values.view(np.uint64), independent.view(np.uint64))
        assert np.array_equal(values[~selected].view(np.uint64), parent_values[~selected].view(np.uint64))
        calls.append({'rows': len(values), 'actual_flagged_rows': int(selected.sum()), 'controls': controls,
            'native_reload_independent_decoder_ordered_mean_and_CDF_raw_bits_exact': True,
            'prediction_numeric_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        return values

    # Retain the full parent15-model replay and its original checks. Route its
    # intermediate report to a distinct path; the final report below also lists
    # every new saved MLP and its independently executed controls.
    original_read, original_dump = ns.read, ns.dump
    intermediate = candidate / 'parent15_native_replay_with_CPU_MLP_route_verification.json'
    final = candidate / 'verification.json'
    proxy = SimpleNamespace(**vars(ns))
    proxy.read = lambda path: original_read(intermediate if Path(path).resolve() == final.resolve() else path)
    def routed_dump(path, data, *args, **kwargs):
        return original_dump(intermediate if Path(path).resolve() == final.resolve() else path, data, *args, **kwargs)
    proxy.dump = routed_dump
    source = ns.ROOT / 'analysis/predict_simplex_residual47_native_scheme_20261006.py'
    text = source.read_text(encoding='utf-8')
    needle = "        calls.append({'rows': len(parent_values), 'actual_flagged_rows': int(selected.sum()),"
    assert text.count(needle) == 1
    text = text.replace(needle, '        values = CPU_MLP_AFTER_PARENT(context, values)\n' + needle)
    namespace = {'__file__': str(source), '__name__': 'actual_selected_CPU_MLP_after_saved_parent106',
        'CPU_MLP_AFTER_PARENT': after_parent}
    exec(compile(text, str(source), 'exec'), namespace)
    runtime.build_context = build_with_raw_features
    try:
        result, storage = namespace['predict'](proxy, record, candidate, parent_curve_source, mapping_path)
    finally:
        runtime.build_context = original_build
    full = [c for c in calls if c['rows'] == 1599600]
    cold = [c for c in calls if c['rows'] == 80 * 4650]
    assert len(full) >= 2 and len(cold) >= 1
    for component in components:
        result['models']['conditional_cpu_mlp_' + component['name']] = component
        storage.append({'key': 'conditional_cpu_mlp_' + component['name'], 'source': component['source_path'],
            'target': component['path'], 'sha256': component['sha256'],
            'samefile': os.path.samefile(component['source_path'], component['path'])})
    result['actual_model_reload_controls'].extend(full[0]['controls'])
    result['actual80_day_prefix_model_controls'].extend(cold[0]['controls'])
    assert len(result['models']) == len(result['actual_model_reload_controls']) == len(result['actual80_day_prefix_model_controls']) == 15 + len(components)
    result.update(actual_CPU_MLP_saved_native_independent_decoder_and_CDF_replay=True,
        selected_CPU_MLP_components=components, original_parent15_intermediate_proof=str(intermediate))
    original_dump(final, result, immutable=True)
    original_dump(candidate / 'CPU_MLP_residual_CDF_native_replay_verification.json', {
        'status': 'passed_actual_parent15_and_selected_CPU_MLP_full_two_replays_independent_decoder_and_cold80',
        'calls': calls, 'actual_native_model_storage': storage,
        'actual_saved_model_count': len(result['models']), 'new_native_fits': 0, 'test_labels_read': False}, immutable=True)
    return result, storage

"""Append a lower-pool operator after an already qualified complete native parent."""
from pathlib import Path
from copy import deepcopy
from types import SimpleNamespace
import hashlib
import os


def parent_source(graph):
    choices = {
        'conditional_flag_CPU_HGB_residual_CDF': 'predict_flagged_CPU_HGB_weighted_quarters_scheme_v2_20261007.py',
        'full_universe_CPU_HGB_rank_CDF': 'predict_full_universe_CPU_HGB_rank_CDF_scheme_20261007.py',
        'full_universe_CPU_ElasticNet_rank_CDF': 'predict_full_universe_CPU_ElasticNet_rank_CDF_scheme_20261007.py',
    }
    selected = [filename for key, filename in choices.items() if key in graph]
    assert len(selected) <= 1, 'Qualified112..114 parents have at most one post-simplex native extension'
    return selected[0] if selected else 'predict_simplex_residual47_native_scheme_20261006.py'


def predict(ns, record, candidate, parent_curve_source, mapping_path):
    import numpy as np
    import pandas as pd
    import joblib
    from threadpoolctl import threadpool_limits
    import whole_scheme_future_runtime_20261004 as runtime
    from protected_upper_pool_HGB_CDF_transform_20261007 import prepare, prepare_heads, apply_prepared
    from cpu_numerical_HGB_large_batch_codec_v2_20261007 import predict_native, predict_decoded
    candidate = Path(candidate)
    candidate.mkdir(parents=True, exist_ok=True)
    graph = record['winner'][ns.GRAPH_FIELD]
    spec = graph['protected_upper_pool_CPU_HGB_CDF']
    assert spec['weight'] > 0. and 0. < spec['lower_fraction'] < 1.
    components = deepcopy(spec['native_components'])
    assert 1 <= len(components) <= 4
    assert [c['name'] for c in components] == spec['ordered_native_components']
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

    def build_with_features(current_graph, inputs, test, *args, **kwargs):
        context, checks = original_build(current_graph, inputs, test, *args, **kwargs)
        assert test.select(['ts_code', 'trade_date']).equals(inputs.select(['ts_code', 'trade_date']))
        assert not {'y_ret_1d', 'y_rank'} & set(test.columns)
        context._lower_HGB_feature_names = list(test.columns[2:])
        assert len(context._lower_HGB_feature_names) == 63
        context._lower_HGB_raw_features = test.select(context._lower_HGB_feature_names).to_numpy().astype(np.float64)
        return context, checks

    def after_complete_parent(context, parent_values):
        cfg = context._whole_graph['protected_upper_pool_CPU_HGB_CDF']
        assert (cfg['weight'], cfg['lower_fraction'], cfg['ordered_native_components']) == (
            spec['weight'], spec['lower_fraction'], spec['ordered_native_components'])
        x = context._lower_HGB_raw_features
        primary_heads, decoded_heads, controls = [], [], []
        with threadpool_limits(limits=4):
            for component in components:
                info = component['training_info']
                meta = info['training_metadata']
                assert info['year'] == 2025 and info['actual_iterations'] == 96
                assert meta['last_training_label_date'] < meta['exclusive_cutoff'] < int(context.dates.min())
                assert meta['last_training_label_end'] <= meta['exclusive_cutoff']
                assert info['features'] == context._lower_HGB_feature_names
                native, state = Path(component['path']), Path(component['independent_state_path'])
                assert ns.sha(native) == component['sha256'] and ns.sha(state) == component['independent_state_sha256']
                first = predict_native(joblib.load(native), x)
                second = predict_native(joblib.load(native), x)
                decoded = predict_decoded(ns.read(state), x)
                assert np.array_equal(first.view('u8'), second.view('u8'))
                assert np.array_equal(first.view('u8'), decoded.view('u8'))
                first[~context.valid] = -1e6
                decoded[~context.valid] = -1e6
                primary_heads.append(first)
                decoded_heads.append(decoded)
                controls.append({'name': 'protected_lower_cpu_hgb_' + component['name'],
                    'sha256': component['sha256'], 'reload_exact': True,
                    'independent_NumPy_decoder_exact': True, 'features': info['features'],
                    'actual_rows': len(x), 'fixed_padded_inference_batch': 8192})
        prepared = prepare(parent_values, context.dates, context.flags, context.valid, cfg['lower_fraction'])
        h = prepare_heads(primary_heads, prepared)
        values = apply_prepared(parent_values, cfg['weight'], prepared, h)
        independent = np.asarray(parent_values).copy()
        selected = np.zeros(len(values), dtype=bool)
        for positions, _, knots, ordered in prepared:
            selected[positions] = True
            p = pd.Series(np.asarray(parent_values[positions])).rank(method='average', pct=True).to_numpy()
            combined = np.zeros(len(positions), dtype=np.float64)
            for head in decoded_heads:
                combined += pd.Series(head[positions]).rank(method='average', pct=True).to_numpy()
            combined /= len(decoded_heads)
            q = (1. - float(cfg['weight'])) * p + float(cfg['weight']) * combined
            independent[positions] = np.interp(np.minimum(np.maximum(q, knots[0]), knots[-1]), knots, ordered)
        assert np.array_equal(values.view('u8'), independent.view('u8'))
        assert np.array_equal(values[~selected].view('u8'), np.asarray(parent_values)[~selected].view('u8'))
        calls.append({'rows': len(values), 'selected_rows': int(selected.sum()), 'controls': controls,
            'native_reload_independent_decoder_and_Pandas_lower_pool_CDF_bits_exact': True,
            'upper_boundary_ties_flags_invalid_bits_unchanged': True,
            'prediction_numeric_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        return values

    original_read, original_dump = ns.read, ns.dump
    final = candidate / 'verification.json'
    intermediate = candidate / 'complete_parent_native_replay_before_lower_pool_verification.json'
    proxy = SimpleNamespace(**vars(ns))
    proxy.read = lambda path: original_read(intermediate if Path(path).resolve() == final.resolve() else path)

    def routed_dump(path, data, *args, **kwargs):
        return original_dump(intermediate if Path(path).resolve() == final.resolve() else path, data, *args, **kwargs)

    proxy.dump = routed_dump
    source = ns.ROOT / 'analysis' / parent_source(graph)
    text = source.read_text(encoding='utf-8')
    needle = '        return values\n'
    assert text.count(needle) == 1
    # All original parent checks and hashes run first. Its returned forecast then
    # passes through the added operator on every full and cold replay.
    text = text.replace(needle, '        return LOWER_AFTER_COMPLETE_PARENT(context, values)\n')
    namespace = {'__file__': str(source), '__name__': 'qualified_complete_parent_with_lower_pool_HGB',
        'LOWER_AFTER_COMPLETE_PARENT': after_complete_parent}
    exec(compile(text, str(source), 'exec'), namespace)
    runtime.build_context = build_with_features
    try:
        result, storage = namespace['predict'](proxy, record, candidate, parent_curve_source, mapping_path)
    finally:
        runtime.build_context = original_build
    full = [c for c in calls if c['rows'] == 1599600]
    cold = [c for c in calls if c['rows'] == 80 * 4650]
    assert len(full) >= 2 and len(cold) >= 1
    union = {component['sha256']: name for name, component in result['models'].items()}
    bindings = []
    for component in components:
        digest = component['sha256']
        key = union.get(digest)
        if key is None:
            key = 'protected_lower_cpu_hgb_' + component['name']
            result['models'][key] = component
            union[digest] = key
            storage.append({'key': key, 'source': component['source_path'], 'target': component['path'],
                'sha256': digest, 'samefile': os.path.samefile(component['source_path'], component['path'])})
            for target, sample in ((result['actual_model_reload_controls'], full[0]),
                (result['actual80_day_prefix_model_controls'], cold[0])):
                control = deepcopy(next(c for c in sample['controls'] if c['sha256'] == digest))
                control['name'] = key
                target.append(control)
        bindings.append({'component': component['name'], 'unique_saved_native_key': key, 'sha256': digest})
    assert len(result['models']) == len(storage) == len(result['actual_model_reload_controls']) == len(result['actual80_day_prefix_model_controls'])
    result.update(actual_protected_upper_pool_HGB_native_independent_CDF_replay=True,
        selected_protected_upper_pool_HGB_components=components,
        protected_HGB_unique_native_bindings=bindings, original_complete_parent_intermediate_proof=str(intermediate))
    original_dump(final, result, immutable=True)
    original_dump(candidate / 'protected_upper_pool_HGB_native_replay_verification.json', {
        'status': 'passed_actual_complete_saved_parent_and_lower_HGB_two_full_replays_independent_decoder_and_cold80',
        'calls': calls, 'unique_native_bindings': bindings, 'actual_native_model_storage': storage,
        'actual_saved_model_count': len(result['models']), 'new_native_fits': 0, 'test_labels_read': False}, immutable=True)
    return result, storage

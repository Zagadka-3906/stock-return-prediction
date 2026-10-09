"""Replay a saved parent graph plus one or more true conditional residual heads."""
from pathlib import Path
from copy import deepcopy
import hashlib
import os


def predict(ns, record, candidate, parent_curve_source, mapping_path):
    import numpy as np
    import pandas as pd
    import lightgbm as lgb
    import whole_scheme_future_runtime_20261004 as runtime
    from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump
    from conditional_flag_residual_extrapolation_transform_20261006 import transform
    from cohort_rank_calibration_v2_20261006 import daily_percentile
    candidate = Path(candidate)
    candidate.mkdir(parents=True, exist_ok=True)
    spec = record['winner'][ns.GRAPH_FIELD]['conditional_flag_residual']
    components = deepcopy(spec['native_components'])
    assert 1 <= len(components) <= 4 and spec['weight'] > 0
    extra_models = {}
    for component in components:
        for field, name, digest in (
            ('source_path', f'{component["name"]}_model.txt', component['sha256']),
            ('independent_dump_source_path', f'{component["name"]}_dump.json', component['independent_dump_sha256'])):
            source, target = Path(component[field]), candidate / name
            assert ns.sha(source) == digest
            if not target.exists():
                if source.drive.upper() == target.drive.upper():
                    os.link(source, target)
                else:
                    import shutil
                    shutil.copyfile(source, target)
            assert ns.sha(target) == digest
            component['path' if field == 'source_path' else 'independent_dump_path'] = str(target)
        extra_models['conditional_residual_' + component['name']] = component
    original_build = runtime.build_context
    calls = []

    def build_with_features(graph, inputs, test, *args, **kwargs):
        context, checks = original_build(graph, inputs, test, *args, **kwargs)
        assert test.select(['ts_code', 'trade_date']).equals(inputs.select(['ts_code', 'trade_date']))
        assert not {'y_ret_1d', 'y_rank'} & set(test.columns)
        features = list(test.columns[2:])
        assert len(features) == 63
        context._residual_supplied_features = clean_matrix(test.select(features).to_numpy())
        context._residual_supplied_feature_names = features
        context._residual_model_checks = checks
        context._residual_control_recorded = False
        return context, checks

    def residual_after_parent(context, raw95, parent_values):
        cfg = context._whole_graph['conditional_flag_residual']
        assert cfg['weight'] == spec['weight'] and cfg['model'] == spec['model']
        selected = context.flags == 1
        p = daily_percentile(raw95, context.dates)
        independent_p = pd.Series(raw95).groupby(context.dates, sort=False).rank(method='average', pct=True).to_numpy()
        assert np.array_equal(p.view(np.uint64), independent_p.view(np.uint64))
        combined = np.zeros(int(selected.sum()), dtype=np.float64)
        independent_combined = np.zeros_like(combined)
        controls = []
        for component in components:
            info = component['training_info']
            assert info['last_training_label_date'] < info['exclusive_cutoff'] < int(context.dates.min())
            assert info['last_training_label_end'] <= info['exclusive_cutoff']
            if info['features'] == ['parent95_oof_percentile']:
                x = clean_matrix(p[selected, None])
                independent_x = clean_matrix(independent_p[selected, None])
            else:
                assert info['features'] == [*context._residual_supplied_feature_names, 'parent95_oof_percentile']
                x = clean_matrix(np.column_stack([context._residual_supplied_features[selected], p[selected]]))
                independent_x = clean_matrix(np.column_stack([context._residual_supplied_features[selected], independent_p[selected]]))
            assert np.array_equal(x.view(np.uint32), independent_x.view(np.uint32))
            path, dump = Path(component['path']), Path(component['independent_dump_path'])
            assert ns.sha(path) == component['sha256'] and ns.sha(dump) == component['independent_dump_sha256']
            model = lgb.Booster(model_str=path.read_text(encoding='utf-8'))
            primary = model.predict(x, num_threads=2) if len(x) else np.empty(0)
            replay = lgb.Booster(model_str=path.read_text(encoding='utf-8')).predict(x, num_threads=2) if len(x) else np.empty(0)
            independent = predict_dump(ns.read(dump), independent_x)
            assert np.array_equal(primary.view(np.uint64), replay.view(np.uint64))
            assert np.array_equal(primary.view(np.uint64), independent.view(np.uint64))
            combined += primary
            independent_combined += independent
            controls.append({'name': 'conditional_residual_' + component['name'],
                'sha256': component['sha256'], 'reload_exact': True, 'independent_tree_decoder_exact': True,
                'actual_flagged_rows': len(x), 'features': info['features']})
        combined /= len(components)
        independent_combined /= len(components)
        assert np.array_equal(combined.view(np.uint64), independent_combined.view(np.uint64))
        residual = np.zeros(len(parent_values), dtype=np.float64)
        residual[selected] = combined
        values = transform(parent_values, context.dates, context.flags, residual, cfg['weight'])
        other = parent_values.copy()
        other[selected] += float(cfg['weight']) * independent_combined
        assert np.array_equal(values.view(np.uint64), other.view(np.uint64))
        assert np.array_equal(values[~selected].view(np.uint64), parent_values[~selected].view(np.uint64))
        if not context._residual_control_recorded:
            context._residual_model_checks.extend(controls)
            context._residual_control_recorded = True
        calls.append({'rows': len(parent_values), 'actual_flagged_rows': int(selected.sum()),
            'native_components': controls, 'native_independent_equal_mean_and_full_transform_bits_exact': True,
            'parent95_feature_percentile_independent_Pandas_bits_exact': True,
            'nonflagged_raw_parent100_predictions_unchanged': True,
            'prediction_numeric_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        return values

    source = ns.ROOT / 'analysis/predict_cohort_calibrated_scheme_20261006.py'
    text = source.read_text(encoding='utf-8')
    before = "        calls.append({'rows': len(raw), 'curve_actual_reload_sha256': ns.sha(curve_path),"
    assert text.count(before) == 1
    text = text.replace(before, '        values = RESIDUAL_AFTER_PARENT(context, raw, values)\n' + before)
    assert text.count('        return copied\n') == 1
    text = text.replace('        return copied\n', '        copied.update(deepcopy(RESIDUAL_NATIVE_MODELS))\n        return copied\n')
    namespace = {'__file__': str(source), '__name__': 'actual_conditional_residual_native_replay',
        'RESIDUAL_AFTER_PARENT': residual_after_parent, 'RESIDUAL_NATIVE_MODELS': extra_models}
    exec(compile(text, str(source), 'exec'), namespace)
    runtime.build_context = build_with_features
    try:
        result, storage = namespace['predict'](ns, record, candidate, parent_curve_source, mapping_path)
    finally:
        runtime.build_context = original_build
    assert len(calls) >= 3 and sum(c['rows'] == 1599600 for c in calls) >= 2
    assert any(c['rows'] == 80 * 4650 for c in calls)
    assert len(result['models']) == len(storage) + len(components) == 13 + len(components)
    for component in components:
        storage.append({'key': 'conditional_residual_' + component['name'],
            'source': component['source_path'], 'target': component['path'], 'sha256': component['sha256'],
            'samefile': os.path.samefile(component['source_path'], component['path'])})
    ns.dump(candidate / 'conditional_residual_native_replay_verification.json', {
        'status': 'passed_actual_saved_parent13_and_selected_residual_heads_full_independent_decoder_and_cold80',
        'calls': calls, 'actual_native_model_storage': storage, 'actual_saved_model_count': len(result['models']),
        'all_parent_curve_native_tree_percentile_and_ensemble_decoders_full_bits_exact': True,
        'new_native_fits': 0, 'test_labels_read': False}, immutable=True)
    return result, storage

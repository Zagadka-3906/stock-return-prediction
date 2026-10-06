"""Replay the actual parent graph and one saved conditional native tree head."""
from pathlib import Path
from copy import deepcopy
import hashlib
import os


def predict(ns, record, candidate, parent_curve_source, common_curve_source, mapping_path):
    import numpy as np
    import pandas as pd
    import lightgbm as lgb
    import whole_scheme_future_runtime_20261004 as runtime
    from conditional_flag_rank_codec_20261006 import clean_matrix, predict_dump
    from conditional_flag_rank_transform_20261006 import transform
    candidate = Path(candidate)
    candidate.mkdir(parents=True, exist_ok=True)
    graph = record['winner'][ns.GRAPH_FIELD]
    spec = graph['conditional_flag_rank']
    native = deepcopy(spec['native_model'])
    files = [('specialist_model.txt', Path(native['source_path']), native['sha256']),
        ('specialist_model_dump.json', Path(native['independent_dump_source_path']), native['independent_dump_sha256']),
        ('conditional_common_curve.json', Path(common_curve_source), spec['future_common_curve']['sha256'])]
    for name, source, digest in files:
        target = candidate / name
        assert ns.sha(source) == digest
        if not target.exists():
            if source.drive.upper() == target.drive.upper():
                os.link(source, target)
            else:
                import shutil
                shutil.copyfile(source, target)
        assert ns.sha(target) == digest
    native.update(path=str(candidate / 'specialist_model.txt'),
        independent_dump_path=str(candidate / 'specialist_model_dump.json'))
    original_build = runtime.build_context
    calls = []

    def build_with_features(graph, inputs, test, *args, **kwargs):
        context, checks = original_build(graph, inputs, test, *args, **kwargs)
        assert test.select(['ts_code', 'trade_date']).equals(inputs.select(['ts_code', 'trade_date']))
        assert not {'y_ret_1d', 'y_rank'} & set(test.columns)
        features = native['training_info']['features']
        assert features == list(test.columns[2:]) and len(features) == 63
        context._conditional_native_features = clean_matrix(test.select(features).to_numpy())
        context._conditional_native_checks = checks
        context._conditional_native_control_recorded = False
        return context, checks

    def conditional_after_parent(context, parent_values):
        cfg = context._whole_graph['conditional_flag_rank']
        assert all(cfg[k] == spec[k] for k in ('model', 'weight', 'first_year_slope'))
        path, dump_path = candidate / 'specialist_model.txt', candidate / 'specialist_model_dump.json'
        assert ns.sha(path) == native['sha256'] and ns.sha(dump_path) == native['independent_dump_sha256']
        training = native['training_info']
        assert training['last_training_label_date'] < training['exclusive_cutoff'] < int(context.dates.min())
        assert training['last_training_label_end'] <= training['exclusive_cutoff']
        selected = context.flags == 1
        test = context._conditional_native_features[selected]
        model = lgb.Booster(model_str=path.read_text(encoding='utf-8'))
        primary = model.predict(test, num_threads=2) if len(test) else np.empty(0)
        saved = lgb.Booster(model_str=path.read_text(encoding='utf-8'))
        replay = saved.predict(test, num_threads=2) if len(test) else np.empty(0)
        independent = predict_dump(ns.read(dump_path), test)
        assert np.array_equal(primary.view(np.uint64), replay.view(np.uint64))
        assert np.array_equal(primary.view(np.uint64), independent.view(np.uint64))
        native_values = np.zeros(len(parent_values), dtype=np.float64)
        native_values[selected] = primary
        curve_path = candidate / 'conditional_common_curve.json'
        assert ns.sha(curve_path) == cfg['future_common_curve']['sha256']
        curve = ns.read(curve_path)['model']
        annual = {str(int(year)): curve for year in np.unique(context.dates // 10000)}
        values = transform(parent_values, context.dates, context.flags, native_values,
            annual, cfg['weight'], cfg['first_year_slope'])
        p = pd.Series(parent_values).groupby(context.dates, sort=False).rank(method='average', pct=True).to_numpy()
        common = np.interp(p, curve['centers'], curve['global_curve'])
        other = common + cfg['weight'] * selected * (np.clip(native_values, 0., 1.) - common) + 1e-9 * p
        assert np.array_equal(values.view(np.uint64), other.view(np.uint64))
        proof = {'name': 'conditional_' + cfg['model'], 'sha256': native['sha256'],
            'reload_exact': True, 'independent_tree_decoder_exact': True,
            'full_rows': len(parent_values), 'actual_flagged_control_rows': len(test),
            'saved_common_curve_and_independent_Pandas_percentile_exact': True}
        if not context._conditional_native_control_recorded:
            context._conditional_native_checks.append(proof)
            context._conditional_native_control_recorded = True
        calls.append({**proof, 'prediction_numeric_sha256': hashlib.sha256(
            memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        return values

    source = ns.ROOT / 'analysis/predict_cohort_calibrated_scheme_20261006.py'
    text = source.read_text(encoding='utf-8')
    before = "        calls.append({'rows': len(raw), 'curve_actual_reload_sha256': ns.sha(curve_path),"
    assert text.count(before) == 1
    text = text.replace(before, '        values = CONDITIONAL_AFTER_PARENT(context, values)\n' + before)
    assert text.count('        return copied\n') == 1
    text = text.replace('        return copied\n', "        copied['conditional_' + CONDITIONAL_NATIVE_NAME] = deepcopy(CONDITIONAL_NATIVE_INFO)\n        return copied\n")
    namespace = {'__file__': str(source), '__name__': 'actual_conditional_native_replay',
        'CONDITIONAL_AFTER_PARENT': conditional_after_parent,
        'CONDITIONAL_NATIVE_NAME': spec['model'], 'CONDITIONAL_NATIVE_INFO': native}
    exec(compile(text, str(source), 'exec'), namespace)
    runtime.build_context = build_with_features
    try:
        result, storage = namespace['predict'](ns, record, candidate, parent_curve_source, mapping_path)
    finally:
        runtime.build_context = original_build
    assert len(calls) >= 3 and sum(c['full_rows'] == 1599600 for c in calls) >= 2
    assert any(c['full_rows'] == 80 * 4650 for c in calls)
    assert len(result['models']) == len(storage) + 1 == 14
    storage.append({'key': 'conditional_' + spec['model'], 'source': native['source_path'],
        'target': native['path'], 'sha256': native['sha256'],
        'samefile': os.path.samefile(native['source_path'], native['path'])})
    ns.dump(candidate / 'conditional_native_replay_verification.json', {
        'status': 'passed_actual14_saved_models_full_independent_conditional_decoder_and_cold80',
        'calls': calls, 'actual_native_model_storage': storage,
        'all_native_tree_and_saved_common_curve_decoders_full_bits_exact': True,
        'actual_parent13_model_replay_preserved': True, 'new_native_fits': 0,
        'test_labels_read': False}, immutable=True)
    return result, storage

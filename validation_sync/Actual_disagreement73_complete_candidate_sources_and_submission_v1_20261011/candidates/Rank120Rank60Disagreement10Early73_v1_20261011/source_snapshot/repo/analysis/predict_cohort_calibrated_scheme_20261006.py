"""Replay the selected native graph, then reload and independently decode its curve."""
from pathlib import Path
from copy import deepcopy
import hashlib
import os


def independent_transform(raw, dates, flags, model, weight):
    import numpy as np
    import pandas as pd
    if float(weight) == 0.:
        return raw.copy()
    p = pd.Series(raw).groupby(dates, sort=False).rank(method='average', pct=True).to_numpy()
    common = np.interp(p, model['centers'], model['global_curve'])
    flagged = np.interp(p, model['centers'], model['flagged_curve'])
    return common + float(weight) * (flags == 1) * (flagged - common) + 1e-9 * p


def predict(ns, record, candidate, curve_source, mapping_path):
    import numpy as np
    import whole_scheme_future_runtime_20261004 as runtime
    from cohort_rank_calibration_20261006 import transform
    from predict_ready_goss_reference_scheme_v2_20261006 import predict as native_predict
    candidate, curve_source = Path(candidate), Path(curve_source)
    candidate.mkdir(parents=True, exist_ok=True)
    curve_path = candidate / 'cohort_curve.json'
    if not curve_path.exists():
        if curve_source.drive.upper() == curve_path.drive.upper():
            os.link(curve_source, curve_path)
        else:
            import shutil
            shutil.copyfile(curve_source, curve_path)
    assert ns.sha(curve_path) == ns.sha(curve_source)
    original_predict, original_copy = runtime.FutureContext.predict, runtime.copy_models
    calls, storage = [], []

    def with_cohort(context, *args, **kwargs):
        raw, stats = original_predict(context, *args, **kwargs)
        spec = context._whole_graph['cohort_rank_calibration']
        assert ns.sha(curve_path) == spec['future_curve_model']['sha256']
        model = ns.read(curve_path)['model']  # Actual serialized curve reload on every replay.
        annual = {str(int(year)): model for year in np.unique(context.dates // 10000)}
        values = transform(raw, context.dates, context.flags, annual, spec['weight'])
        independent = independent_transform(raw, context.dates, context.flags, model, spec['weight'])
        assert np.array_equal(values.view(np.uint64), independent.view(np.uint64))
        assert model['last_training_label_date'] < model['exclusive_cutoff'] < int(context.dates.min())
        calls.append({'rows': len(raw), 'curve_actual_reload_sha256': ns.sha(curve_path),
            'independent_Pandas_percentile_decoder_full_bits_exact': True,
            'prediction_numeric_sha256': hashlib.sha256(memoryview(np.ascontiguousarray(values)).cast('B')).hexdigest()})
        return values, {**stats, 'cohort_rank_calibration': {'weight': spec['weight'],
            'curve_actual_reload_sha256': ns.sha(curve_path), 'labels_used_by_prediction': False}}

    def linked_models(native_sources, root_sources, destination):
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        copied = {}
        for key, info in {**root_sources, **{'whole_' + k: v for k, v in native_sources.items()}}.items():
            if hasattr(ns, 'cohort_saved_models'):
                stored = ns.cohort_saved_models[key]
                assert stored['sha256'] == info['sha256']
                info = {**deepcopy(info), 'path': stored['path']}
            source = Path(info['path']).resolve()
            name = hashlib.sha256(key.encode('utf-8')).hexdigest()[:16] + '__' + source.name
            target = destination / name
            assert ns.sha(source) == info['sha256']
            assert target.resolve().is_relative_to(candidate.resolve())
            if not target.exists():
                if source.drive.upper() == target.drive.upper():
                    os.link(source, target)
                else:
                    import shutil
                    shutil.copyfile(source, target)
            assert ns.sha(target) == info['sha256']
            copied[key] = {**deepcopy(info), 'path': str(target), 'whole_graph_source': str(source)}
            storage.append({'key': key, 'source': str(source), 'target': str(target),
                'sha256': info['sha256'], 'samefile': os.path.samefile(source, target)})
        return copied

    runtime.FutureContext.predict, runtime.copy_models = with_cohort, linked_models
    try:
        native_predict(ns, record, candidate_path=candidate, mapping_path=mapping_path)
        result = ns.read(candidate / 'verification.json')
        assert result['status'] == 'passed'
        assert len(calls) >= 3 and sum(c['rows'] == 1599600 for c in calls) >= 2
        assert any(c['rows'] == 80 * 4650 for c in calls)
        ns.dump(candidate / 'cohort_curve_replay_verification.json', {
            'status': 'passed_actual_curve_reload_and_independent_full_and_cold80_future_decoder',
            'calls': calls, 'curve_model_sha256': ns.sha(curve_path),
            'actual_native_model_storage': storage,
            'new_native_base_model_fits': 0, 'test_labels_read': False}, immutable=True)
        return result, storage
    finally:
        runtime.FutureContext.predict, runtime.copy_models = original_predict, original_copy

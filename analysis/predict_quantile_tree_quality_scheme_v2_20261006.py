"""Infer a copied whole graph with embedded consensus and all ancestor codecs."""
from pathlib import Path
import shutil


def source_names(number):
    assert number in (91, 92)
    from predict_ready_classifier_consensus_reference_scheme_v2_20261006 import source_names as inherited
    return tuple(dict.fromkeys((*inherited(90),
        'quantile_tree_scheme_runtime_20261006.py',
        'quantile_tree_candidate_20261006.py',
        'quantile_tree_future_codec_20261006.py',
        'quantile_tree_future_codec_20261006.py',
        'quantile_tree_quality_search_engine_v2_20261006.py',
        'explicit_parent_release_engine_v3_20261006.py',
        'run_quantile_tree_quality_round_v2_20261006.py',
        'check_quantile_tree_quality_scheme_v2_20261006.py',
        'predict_quantile_tree_quality_scheme_v2_20261006.py',
        'optimize_training_round91_v3.py', 'finalize_training_round91_v3.py',
        f'optimize_training_round{number}_v3.py', f'finalize_training_round{number}_v3.py',
        f'run_training_round{number}_v3_pipeline.py')))


def copy_sources(ns, candidate):
    candidate = Path(candidate)
    assert not (candidate / 'manifest.json').exists(), 'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True, exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT / 'analysis' / name, candidate / name)
        if name.startswith(('optimize_training_round', 'finalize_training_round')) and name.endswith(('_v2.py', '_v3.py')):
            shutil.copyfile(ns.ROOT / 'analysis' / name, candidate / name.replace('_v2.py', '.py').replace('_v3.py', '.py'))


def predict(ns, record, candidate_path=None, mapping_path=None):
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    from quantile_tree_future_codec_20261006 import install
    from agreement_gated_weights_20261005 import context_weight
    candidate = Path(candidate_path) if candidate_path is not None else ns.ROOT / f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_sources(ns, candidate)
    original_weights = runtime.FutureContext.weights_for
    restore = install()

    def weights_for(context, spec):
        return context_weight(context, spec, original_weights(context, spec))

    runtime.FutureContext.weights_for = weights_for
    try:
        original(ns, record, candidate_path=candidate, mapping_path=mapping_path)
    finally:
        runtime.FutureContext.weights_for = original_weights
        restore()
    assert runtime.FutureContext.weights_for is original_weights
    copy_sources(ns, candidate)

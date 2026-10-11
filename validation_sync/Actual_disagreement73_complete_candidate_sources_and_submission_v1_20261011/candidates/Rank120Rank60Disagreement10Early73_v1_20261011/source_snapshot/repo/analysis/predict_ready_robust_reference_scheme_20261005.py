"""Infer the complete classifier graph with actual copied codecs and parent sources."""
from pathlib import Path
import shutil


def source_names(number):
    assert number in (87, 88)
    return (
        'ready_robust_reference_search_engine_20261005.py',
        'ready_classifier_reference_search_engine_20261005.py',
        'optimize_training_round85_v2.py', 'optimize_training_round86_v2.py',
        'streaming_robust_regression_scheme_runtime_20261005.py',
        'streaming_robust_regression_model_sources_20261005.py',
        'streaming_robust_regression_20261005.py',
        'train_streaming_robust_regression_bank_20261005.py',
        'streaming_robust_regression_future_codec_adapter_20261005.py',
        'explicit_parent_release_engine_v2_20261005.py',
        'parallel_candidate_scoring_one_20261005.py',
        'run_ready_robust_reference_round_20261005.py',
        'publish_explicit_parent_training_round_v2_20261005.py',
        'check_ready_robust_reference_scheme_20261005.py',
        'predict_ready_robust_reference_scheme_20261005.py',
        f'optimize_training_round{number}_v2.py', f'finalize_training_round{number}_v2.py',
        f'run_training_round{number}_v2_pipeline.py',
        'optimize_training_round81_v2.py', 'optimize_training_round82_v2.py',
        'optimize_training_round83_v2.py', 'optimize_training_round84_v2.py',
        'linear_leaf_reference66_search_engine_v2_20261005.py',
        'ready_fm_reference_search_engine_20261005.py',
        'streaming_rank_classifier_scheme_runtime_20261005.py',
        'streaming_rank_classifier_model_sources_20261005.py',
        'streaming_rank_classification_v3_20261005.py',
        'train_streaming_rank_classifier_bank_v3_20261005.py',
        'streaming_rank_classifier_future_codec_adapter_20261005.py',
        'memory_efficient_neural_future_codec_adapter_20261005.py',
        'gradient_sampling_future_codec_adapter_20261005.py',
        'factorization_machine_future_codec_adapter_20261005.py',
        'linear_leaf_ensemble_future_codec_adapter_20261005.py',
        'linear_leaf_future_codec_adapter_20261005.py',
        'nystrom_future_codec_adapter_20261005.py',
        'agreement_gated_weights_20261005.py',
        *(() if number == 87 else ('optimize_training_round87_v2.py', 'finalize_training_round87_v2.py')))


def copy_sources(ns, candidate):
    candidate = Path(candidate)
    assert not (candidate / 'manifest.json').exists(), 'A sealed candidate must not be edited.'
    candidate.mkdir(parents=True, exist_ok=True)
    for name in source_names(ns.NUMBER):
        shutil.copyfile(ns.ROOT / 'analysis' / name, candidate / name)
        if name.startswith(('optimize_training_round', 'finalize_training_round')) and name.endswith('_v2.py'):
            shutil.copyfile(ns.ROOT / 'analysis' / name, candidate / name.replace('_v2.py', '.py'))


def predict(ns, record, candidate_path=None, mapping_path=None):
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    from streaming_robust_regression_future_codec_adapter_20261005 import install
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

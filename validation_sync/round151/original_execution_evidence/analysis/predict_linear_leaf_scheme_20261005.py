"""Predict expanded kernels and inherited agreement gates from frozen copied models."""
from pathlib import Path
import shutil


def predict(ns, record, candidate_path=None, mapping_path=None):
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    from linear_leaf_future_codec_adapter_20261005 import install
    from agreement_gated_weights_20261005 import context_weight
    candidate = Path(candidate_path) if candidate_path is not None else ns.ROOT / f'candidates/optimization_20261003_r{ns.NUMBER}'
    candidate.mkdir(parents=True, exist_ok=True)
    for name in ('agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py', 'linear_leaf_future_codec_adapter_20261005.py',
                 'linear_leaf_model_sources_20261005.py', 'linear_leaf_scheme_runtime_20261005.py',
                 'linear_leaf_search_engine_v2_20261005.py', 'predict_linear_leaf_scheme_20261005.py',
                 'check_linear_leaf_scheme_20261005.py', f'optimize_training_round{ns.NUMBER}.py',
                 f'finalize_training_round{ns.NUMBER}.py'):
        shutil.copyfile(ns.ROOT / 'analysis' / name, candidate / name)
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

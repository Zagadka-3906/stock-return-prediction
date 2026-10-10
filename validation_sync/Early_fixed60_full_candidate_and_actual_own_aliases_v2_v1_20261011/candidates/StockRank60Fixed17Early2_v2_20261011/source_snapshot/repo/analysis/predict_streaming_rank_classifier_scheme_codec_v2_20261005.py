"""Infer the complete mapped classification graph and retain actual entrypoints."""
from pathlib import Path
import hashlib
import json

def copy_actual_sources(ns,candidate):
    candidate = Path(candidate).resolve()
    assert candidate.drive.upper() in ('D:', 'E:') and ns.NUMBER in (79,80)
    assert not (candidate/'manifest.json').exists(), 'Published candidate is immutable.'
    names = ('agreement_gated_weights_20261005.py', 'nystrom_future_codec_adapter_20261005.py',
        'streaming_rank_classifier_future_codec_adapter_20261005.py',
        'streaming_rank_classifier_model_sources_20261005.py', 'streaming_rank_classifier_scheme_runtime_20261005.py',
        'streaming_rank_classifier_search_engine_20261005.py', 'predict_streaming_rank_classifier_scheme_v2_20261005.py',
        'check_streaming_rank_classifier_scheme_20261005.py', f'optimize_training_round{ns.NUMBER}.py',
        f'finalize_training_round{ns.NUMBER}.py', f'run_training_round{ns.NUMBER}_pipeline.py',
        'run_streaming_rank_classifier_round_v2_20261005.py', 'streaming_rank_classification_v3_20261005.py',
        'train_streaming_rank_classifier_bank_v3_20261005.py', 'run_streaming_rank_classifier_bank_v3_20261005.py',
        'verify_streaming_rank_classifier_full_future_v3_20261005.py', Path(__file__).name)
    candidate.mkdir(parents=True,exist_ok=True)
    files = {}
    for name in names:
        source = ns.ROOT/'analysis'/name
        destination = name.replace('_v2.py','.py') if name.startswith(('optimize_training_round','finalize_training_round')) else name
        data, target = source.read_bytes(), candidate/destination
        if target.exists() and target.read_bytes() != data:
            assert destination.startswith(('optimize_training_round','finalize_training_round'))
            old = target.read_bytes()
            assert old == (ns.ROOT/'analysis'/destination).read_bytes()
            historical = candidate/'legacy_review_sources'/destination
            historical.parent.mkdir(exist_ok=True)
            if historical.exists(): assert historical.read_bytes() == old
            else: historical.write_bytes(old)
            target.write_bytes(data)
        elif target.exists():
            assert target.read_bytes() == data, name
        else:
            with target.open('xb') as stream: stream.write(data)
        files[destination] = {'project_source':str(source),'sha256':hashlib.sha256(data).hexdigest()}
    record = {'status':'passed','round':ns.NUMBER,'files':files,
        'actual_pipeline':f'run_training_round{ns.NUMBER}_pipeline.py',
        'actual_driver':'run_streaming_rank_classifier_round_v2_20261005.py',
        'actual_canonical_release':f'finalize_training_round{ns.NUMBER}.py',
        'same_actual_pipeline_and_canonical_release':True,'test_labels_read':False}
    data = (json.dumps(record,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    path = candidate/'actual_execution_sources.json'
    if path.exists(): assert path.read_bytes() == data
    else:
        with path.open('xb') as stream: stream.write(data)
    return record

def predict(ns,record,candidate_path=None,mapping_path=None):
    import whole_scheme_future_runtime_20261004 as runtime
    from predict_nystrom_ridge_scheme_20261004 import predict as original
    from streaming_rank_classifier_future_codec_adapter_20261005 import install
    from agreement_gated_weights_20261005 import context_weight
    candidate = Path(candidate_path) if candidate_path is not None else ns.ROOT/f'candidates/optimization_20261003_r{ns.NUMBER}'
    copy_actual_sources(ns,candidate)
    original_weights = runtime.FutureContext.weights_for
    restore = install()
    def weights_for(context,spec): return context_weight(context,spec,original_weights(context,spec))
    runtime.FutureContext.weights_for = weights_for
    try: original(ns,record,candidate_path=candidate,mapping_path=mapping_path)
    finally:
        runtime.FutureContext.weights_for = original_weights
        restore()
    assert runtime.FutureContext.weights_for is original_weights
    copy_actual_sources(ns,candidate)

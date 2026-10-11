"""Execute an already supported complete graph after replacing/removing its flag-HGB node."""
from pathlib import Path
import importlib


def predict(ns,record,candidate,parent_curve_source,mapping_path):
    graph=record['winner'][ns.GRAPH_FIELD]
    if 'protected_upper_pool_CPU_HGB_CDF' in graph:
        module='predict_lower_pool_after_quantile_HGB_scheme_v2_20261007' if 'conditional_flag_CPU_HGB_residual_CDF' in graph else 'predict_protected_upper_pool_CPU_HGB_scheme_20261007'
    elif 'conditional_flag_CPU_HGB_residual_CDF' in graph:
        module='predict_quantile_HGB_residual_CDF_scheme_v2_20261007'
    else:
        module='predict_simplex_residual47_native_scheme_20261006'
    result,storage=importlib.import_module(module).predict(ns,record,candidate,parent_curve_source,mapping_path)
    assert result['status']=='passed' and result['whole_scheme_graph']==graph
    assert (result['rows'],result['days'],result['codes'])==(1599600,344,4650)
    for key in ('model_reload_bit_identical','pipeline_replay_bit_identical','csv_replay_byte_identical','cold80_day_prefix_bit_identical'):assert result[key]
    if 'conditional_flag_CPU_HGB_residual_CDF' in graph:assert result['actual_CPU_HGB_saved_native_independent_decoder_and_CDF_replay']
    if 'protected_upper_pool_CPU_HGB_CDF' in graph:assert result['actual_protected_upper_pool_HGB_native_independent_CDF_replay']
    assert len(result['models'])==len(storage)==len(result['actual_model_reload_controls'])==len(result['actual80_day_prefix_model_controls'])
    ns.dump(Path(candidate)/'refined_quantile_HGB_native_replay_verification.json',{
        'status':'passed_actual_quantile_full_refined_graph_saved_native_independent_two_replays_and_cold80',
        'actual_prediction_backend':module,'actual_saved_models':len(result['models']),
        'flag_HGB_present':'conditional_flag_CPU_HGB_residual_CDF' in graph,
        'original_lower_pool_HGB_preserved':'protected_upper_pool_CPU_HGB_CDF' in graph,
        'actual_native_model_storage':storage,'csv_sha256':result['csv_sha256'],
        'two_full_and_cold80_replay_results_from_actual_supported_backend':True,
        'new_native_fits':0,'test_labels_read':False},immutable=True)
    return result,storage

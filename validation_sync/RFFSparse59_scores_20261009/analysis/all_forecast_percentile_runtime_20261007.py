"""Adopt faster all-row percentiles only after actual full-mapping and uncached8-metric equivalence."""
from pathlib import Path
from contextlib import contextmanager
from functools import cache
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned

@cache
def choice():
    service=A/'service_owned_workflows_20261006/all_forecast_percentiles_full_scoring_benchmark'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
    path=A/'all_forecast_percentiles_full_scoring_benchmark_20261007/verification.json';proof=read(path)
    assert proof['status']=='passed_actual12_uncached_full_official_calls_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders'
    assert proof['actual_uncached_official_evaluation_calls']==len(proof['records'])==12
    for source in (A/'exact_numpy_all_forecast_percentiles_20261007.py',A/'connected_validation_20261002/return_mapping.py',ROOT/'evaluate.py'):
        assert sha(source)==proof['input_sha256'][str(source)],source
    ratio=proof['median_full_mapping_and_official_score_phase_speedup']
    return {'actual_full_equivalence_proof':str(path),'proof_sha256':sha(path),'actual_measured_phase_speedup':ratio,
        'adopted':ratio>1.,'choice_based_on_equal_result_execution_cost_not_model_quality':True}

@contextmanager
def installed():
    decision=dict(choice());restore=None
    if decision['adopted']:
        from exact_numpy_all_forecast_percentiles_20261007 import install
        operator,restore=install()
    try:yield decision
    finally:
        decision['statistics']=restore() if restore else {'original_operator_retained':True}

"""Adopt scoring-only cached ranks only after twelve actual official equivalence calls."""
from pathlib import Path
from contextlib import contextmanager
from functools import cache
import sys
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis'
sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,owned
@cache
def choice():
    service=A/'service_owned_workflows_20261006/cached_official_spearman_full12_benchmark'
    assert not owned(read(service/'native_launch.json')) and read(service/'service_execution.json')['status']=='passed'
    path=A/'cached_official_spearman_full_scoring_benchmark_20261007/verification.json';proof=read(path)
    assert proof['status']=='passed_actual12_uncached_full_official_calls_cached_SciPy_Spearman_all_mapped_bits_CSV_bytes_eight_metrics_and_two_orders'
    assert proof['actual_uncached_official_evaluation_calls']==len(proof['records'])==12
    for source in (A/'exact_cached_official_spearman_v2_20261007.py',A/'exact_cached_validation_spearman_20261007.py',ROOT/'evaluate.py'):
        assert sha(source)==proof['input_sha256'][str(source)],source
    return {'actual_full_equivalence_proof':str(path),'proof_sha256':sha(path),
      'actual_measured_phase_speedup':proof['median_full_mapping_and_official_score_phase_speedup'],
      'adopted':proof['median_full_mapping_and_official_score_phase_speedup']>1.,
      'choice_based_only_on_equal_result_execution_cost':True}
@contextmanager
def installed(target_cache=None):
    decision=dict(choice())
    if decision['adopted']:
        from exact_cached_official_spearman_v2_20261007 import installed as exact
        with exact(target_cache) as events:
            try:yield decision
            finally:decision['statistics']=events
    else:
        try:yield decision
        finally:decision['statistics']={'original_official_SciPy_spearman_retained':True}

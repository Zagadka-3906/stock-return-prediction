"""Preserve the exact selected pipeline; reuse independently verified identical features only."""
from pathlib import Path
import sys,runpy,time
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
def main():
    assert allowed();closed('actual_feature120_verified_memoization_TRAIN344_v1_20261010')
    import exact_verified_feature120_memoization_runtime_v1_20261010 as cache
    pointer=A/'actual_feature120_verified_memoization_TRAIN344_location_v1_20261010.json'
    benchmark=Path(read(pointer)['output'])/'verification.json';proof=read(benchmark);assert proof['adopt'] and proof['rows']==1599600 and len(proof['actual_controls'])==4
    for p,d in proof['input_sha256'].items():assert sha(p)==d,p
    original=A/'prepare_StockRank60Embedding198_selected_candidate_v1_20261011.py'
    pins={str(p):sha(p) for p in [Path(__file__),Path(cache.__file__),original,pointer,benchmark]}
    out=Path('E:/赛题五_本机临时/第198轮_20261010/selected_feature_cache_runtime_v5');out.mkdir(exist_ok=False)
    create(out/'frozen_before_actual_selected_dispatch.json',{'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'actual_future_X_read':False,'cached_scope':'feature120_derivation_only_after_native_and_independent_Pandas_pair','GPU_native_reload_and_independent_saved_tensor_predictions_unchanged':True,'max_cache_bytes':1024**3,'test_labels_read':False})
    with cache.installed() as stats:
        assert allowed();runpy.run_path(str(original),run_name='__main__')
    release=A/'StockRank60Embedding198_selected_release_v1_20261011';ready=read(release/'inference_ready.json')
    if ready['new_inference_claimed']:
        assert stats['hits']>0 and any(r['rows']==1599600 for r in stats['actual_independent_full_pairs']) and any(r['rows']==80*4650 for r in stats['actual_independent_full_pairs'])
    else:assert stats['misses']==stats['hits']==0
    for p,d in pins.items():assert sha(p)==d,p
    row={'status':'passed_exact_existing_selected_pipeline_with_independently_verified_feature120_memoization','input_sha256':pins,'actual_selected_new_inference':ready['new_inference_claimed'],'statistics':stats,'original_all_full_native_reload_independent_tensor_cold80_and_CSV_checks_unchanged':True,'no_model_prediction_cached':True,'feature_only_reuse_after_actual_independent_pair_not_a_new_independent_calculation_per_hit':True,'test_labels_read':False}
    create(out/'verification.json',row)
    if ready['new_inference_claimed']:create(Path(ready['source_candidate'])/'verified_feature120_cache_runtime_v5.json',row)
    print({'actual_selected_feature_cache_runtime_passed':True,'hits':stats['hits'],'new_inference':ready['new_inference_claimed']},flush=True)
if __name__=='__main__':main()

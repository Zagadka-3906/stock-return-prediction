"""Predeclare all86 actual two-seed screen records and qualified175/186 anchors before normalization."""
from pathlib import Path
import sys,importlib
A=Path(__file__).resolve().parent;sys.path[:0]=[str(A.parent),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
from handoff_ready_goss_full_execution_20261006 import start_service

def main():
    assert allowed()
    normal=A/'normalize_completed_rank20_two_seed88_after186_v1_20261011.py'
    qual=A/'qualify_rank20_two_seed88_selected_native14_v1_20261011.py'
    for p in [normal,qual]:compile(p.read_text(encoding='utf8'),str(p),'exec')
    from normalize_completed_rank20_two_seed88_after186_v1_20261011 import RECIPE
    for m in ['rank20_two_seed_after_qualified_parent_native_stage_v1_20261010','rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011']:
        stage=importlib.import_module(m);assert stage.RECIPE==RECIPE and len(stage.BACKENDS[RECIPE])==4
    families=[{'name':'CDF49','actual_service':'actual_rank20_two_seed_after175_complement49_screen_v1_20261010','records':49,
        'output':'E:/赛题五_本机临时/StockRank20TwoSeed_after175_complement49_screen_v1_20261010',
        'main_receipt':'Rank20_two_seed_official49_main_receipt_v1_20261010.json','codecs':['CDF']},
        {'name':'protected37','actual_service':'actual_rank20_two_seed_after175_protected_tail37_screen_v1_20261011','records':37,
        'output':'E:/赛题五_本机临时/StockRank20TwoSeed_after175_protected_tail37_screen_v1_20261011',
        'main_receipt':'Rank20_two_seed_protected37_official37_main_receipt_v1_20261011.json','codecs':['valid_pool_protection_v1','official_Top_protection_v2']}]
    sources=[Path(__file__),normal,qual,A/'rank20_two_seed_complement49_predeclared_plan_v1_20261010.json',
        A/'rank20_two_seed_protected_tail37_predeclared_plan_v1_20261011.json',
        A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json',
        A/'rank20_two_seed_after_qualified_parent_native_stage_v1_20261010.py',
        A/'rank20_two_seed_protected_after_qualified_parent_native_stage_v1_20261011.py']
    assert read(sources[5])['status'].startswith('passed')
    pins={str(p):sha(p) for p in sources}
    plan=A/'rank20_two_seed_complete88_after186_plan_v1_20261011.json'
    create(plan,{'status':'predeclared88_two_existing_TRAIN_screen_families_and175186_anchors_before_normalization',
        'input_sha256':pins,'expected_records':88,'fully_qualified_anchors':[175,186],'families':families,
        'expected_nonidentity_full_controls':84,'expected_nonidentity_prefix_controls':252,
        'selection_only_highest_connected_official_S_then_actual_physical_model_count':True,
        'new_quality_scores':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,
        'full187_candidate_registry_pipeline_pending':True})
    admission=A/'rank20_two_seed_complete88_normalization_native14_sources_admission_v1_20261011.json'
    create(admission,{'status':'compiled88_actual_record_normalization_and_selected14_sources_no_future_dispatch',
        'input_sha256':{**pins,str(plan):sha(plan)},'expected_records':88,'scientific_model_fits_reused':12,
        'full187_candidate_registry_pipeline_pending':True,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    for name,p in [('actual_rank20_two_seed88_after186_normalization_v1_20261011',normal),('actual_rank20_two_seed88_selected_native14_v1_20261011',qual)]:
        assert allowed();row=start_service(name,p.name,[],{str(p):sha(p),str(admission):sha(admission)})
        create(A/(name+'_activation.json'),row)
    print({'normalization88_and_selected_native14_queued':True,'new_scores':0,'future_submission_pipeline_pending':True},flush=True)

if __name__=='__main__':main()

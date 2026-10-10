from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
def main():
    assert allowed()
    from prepare_stock_rank_dual174_full_registry_sources_v1_20261010 import source_paths
    sources=source_paths()+[Path(__file__),A/'run_StockRankDual174_full_registration_v1_20261010.py',A/'run_StockRankDual174_complete_family_v1_20261010.py',A/'prepare_stock_rank_dual174_full_registry_sources_v2_20261010.py']
    for name in ('stock_rank_dual174_candidate_sources_preparation_v1_20261010.json','stock_rank_dual174_full_registry_sources_preparation_v1_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round174.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(174,173,(457,))
    from stock_rank_dual174_storage_v1_20261010 import OUTPUTS
    assert len(OUTPUTS)==6 and A/'optimization_20261003_r174' in OUTPUTS
    folder=Path(read(A/'actual_stock_rank_dual44_selected_native14_location_v1_20261010.json')['output'])
    pilot=read(folder/'pilot44.json');control=read(folder/'verification.json');best=pilot['best'];cfg=best['configuration']
    assert len(pilot['records'])==pilot['expected_scored_records']==44
    assert (pilot['actual_nonidentity_full_controls'],pilot['actual_nonidentity_prefix_controls'])==(40,120)
    assert pilot['actual_comparison_parent_round']==173 and control['best']==best
    assert best==min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    baseline=read(A/'optimization_20261003_r173/calibrated_csv_official.json')['metrics'];assert best['connected_final_score']>=baseline['final_score']
    for row in pilot['records']:
        capsule=Path(row['official_score_cache']['official_metrics_source']);assert sha(capsule)==row['official_metric_capsule_sha256'] and read(capsule)['metrics']==row['metrics'] and row['configuration']['anchor_round'] in (170,173)
    if cfg['stage_kind']=='anchor':
        assert control['status']=='passed_selected_fully_qualified_anchor44_no_new_native_stage_claimed'
        assert read(A/f"optimization_20261003_r{cfg['anchor_round']}/full_registration_execution.json")['status']=='passed'
    else:
        assert control['status']=='passed_selected_protected_tail_six_states14_native_and14_cold_and7_prefit_rejections'
        banks=len(best['native_bank_components']);assert banks in (1,2)
        assert control['actual_saved_states']==6*banks and control['actual_banks']==banks
        assert (len(control['records']),control['actual_historical_cases'],control['actual_calendar_cases'],control['actual_cold_cases'],len(control['prefit_rejections']))==(14,10,4,14,7)
        assert best['connected_final_score']>baseline['final_score']
    for p,d in pilot['input_sha256'].items():assert sha(p)==d,p
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'stock_rank_dual174_full_family_preflight_v1_20261010.json',{'status':'passed_actual44_capsules_selected14_dynamic_saved_states_and_QA85_routes_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [*sources,folder/'pilot44.json',folder/'verification.json']},'actual_stage_kind':cfg['stage_kind'],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
if __name__=='__main__':main()

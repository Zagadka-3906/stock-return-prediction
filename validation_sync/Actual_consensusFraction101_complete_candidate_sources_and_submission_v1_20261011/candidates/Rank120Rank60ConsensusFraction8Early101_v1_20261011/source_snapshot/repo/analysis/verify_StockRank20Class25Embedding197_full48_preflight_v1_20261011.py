"""Admit actual48 completed official records and selected native or pure postprocessing controls."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import prepare_StockRank20Class25Embedding197_complete48_pipeline_v1_20261011 as routes
    for name in ('stock_rank20class25_embedding197_candidate_sources_preparation_v1_20261011.json','stock_rank20class25_embedding197_full_registry_sources_preparation_v1_20261011.json'):
        for path,digest in read(A/name)['input_sha256'].items():assert sha(path)==digest,path
    sources=list(dict.fromkeys([*routes.source_paths(),Path(__file__),A/'run_StockRank20Class25Embedding197_full_registration_v1_20261011.py',A/'run_StockRank20Class25Embedding197_complete_family_v1_20261011.py']))
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    opt=literal_assignments(A/'optimize_training_round197_v1_20261011.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(197,196,(480,))
    import stock_rank20class25_embedding197_storage_v1_20261011 as storage
    assert len(storage.OUTPUTS)==6 and A/'optimization_20261003_r197' in storage.OUTPUTS
    assert 'assert number == 197' in (A/'stock_rank20class25_embedding197_storage_v1_20261011.py').read_text(encoding='utf8')
    folder=Path(read(A/'actual_stock_rank20class25_embedding48_selected_native14_location_v1_20261011.json')['output'])
    pilot=read(folder/'pilot48.json');control=read(folder/'verification.json');best=pilot['best'];cfg=best['configuration']
    assert len(pilot['records'])==pilot['expected_scored_records']==48
    assert (pilot['actual_nonidentity_full_controls'],pilot['actual_nonidentity_prefix_controls'])==(44,132)
    assert pilot['actual_comparison_parent_round']==196 and control['best']==best
    assert best==min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    baseline=read(A/'optimization_20261003_r196/calibrated_csv_official.json')['metrics']
    assert best['connected_final_score']>=baseline['final_score']
    for row in pilot['records']:
        cap=Path(row['official_score_cache']['official_metrics_source'])
        assert sha(cap)==row['official_metric_capsule_sha256'] and read(cap)['metrics']==row['metrics']
        assert row['configuration']['anchor_round'] in (175,196)
    if cfg['stage_kind']=='anchor':
        assert control['status']=='passed_selected_fully_qualified_anchor48_no_new_native_stage_claimed'
        assert read(A/f"optimization_20261003_r{cfg['anchor_round']}/full_registration_execution.json")['status']=='passed'
    else:
        assert control['status']=='passed_selected_protected_tail_six_states14_native_and14_cold_and7_prefit_rejections'
        assert (len(control['records']),control['actual_historical_cases'],control['actual_calendar_cases'],control['actual_cold_cases'])==(14,10,4,14)
        assert control['actual_saved_states']==6 and len(control['prefit_rejections'])==7
        assert best['connected_final_score']>=baseline['final_score']
    for path,digest in pilot['input_sha256'].items():assert sha(path)==digest,path
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'stock_rank20class25_embedding197_full_family_preflight_v1_20261011.json',{'status':'passed_complete48_actual_capsules_selected_stage_and_QA108_routes_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [*sources,folder/'pilot48.json',folder/'verification.json']},'actual_stage_kind':cfg['stage_kind'],'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False})
    print({'admitted_records':48,'QA':108,'stage_kind':cfg['stage_kind'],'future_dispatch_not_started':True},flush=True)

if __name__=='__main__':main()

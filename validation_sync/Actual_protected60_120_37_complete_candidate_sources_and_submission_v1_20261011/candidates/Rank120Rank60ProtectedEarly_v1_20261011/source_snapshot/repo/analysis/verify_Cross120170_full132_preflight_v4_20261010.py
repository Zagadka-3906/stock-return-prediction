"""Admit complete132 measured records and selected native14 or exact qualified anchor."""
from pathlib import Path
import sys,ast
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed

def main():
    assert allowed()
    import prepare_cross120170_full_registry_sources_v1_20261010 as routes
    from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
    proofs=['cross120170_full_registry_source_preparation_v1_20261010.json','cross120170_candidate_actual132_and_own_source_routes_preflight_v2_20261010.json','cross120170_actual_complete169_parent_callback_CPU_controls_v1_20261010.json','cross120_after_complete169_context_encoder_actual_CPU_controls_v2_20261010.json']
    for name in proofs:
        for path,digest in read(A/name)['input_sha256'].items():assert sha(path)==digest,path
    sources=list(dict.fromkeys([*routes.source_paths(),A/'prepare_cross120170_selected_candidate_v4_20261010.py',A/'qualify_cross120_two_target132_selected_native14_v3_20261010.py',A/'normalize_predeclared_cross120_two_target132_v5_20261010.py',A/'frozen_external_official_capsule_publish_guard_runtime_v1_20261010.py',Path(__file__),A/'run_Cross120170_full_registration_v4_20261010.py',A/'run_Cross120170_complete_family_v4_20261010.py',*[A/n for n in proofs]]))
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round170.py')
    assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(170,169,(453,))
    register=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for token in ["'expected_scored_records': 132","'explicit_parent_round': 169","'waves': [453]","r{cfg['anchor_round']}/verification.json","scored_records=132"]:assert token in register,token
    pub=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for token in ['collect(170, 81, 132)',"namespace['snapshot'](170)","'scored_records': 132","'actual_full_QA_version': 81"]:assert token in pub,token
    folder=Path(read(A/'actual_cross120_two_target132_selected_native14_location_v1_20261010.json')['output'])
    pilot=read(folder/'pilot132.json');control=read(folder/'verification.json');best=pilot['best'];cfg=best['configuration']
    assert len(pilot['records'])==pilot['expected_scored_records']==132
    assert (pilot['actual_nonidentity_full_controls'],pilot['actual_nonidentity_prefix_controls'])==(128,384)
    assert pilot['actual_comparison_parent_round']==169 and control['best']==best
    assert best==min(pilot['records'],key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    baseline=read(A/'optimization_20261003_r169/calibrated_csv_official.json')['metrics']
    assert best['connected_final_score']>=baseline['final_score']
    for row in pilot['records']:
        cap=Path(row['official_score_cache']['official_metrics_source'])
        assert sha(cap)==row['official_metric_capsule_sha256'] and read(cap)['metrics']==row['metrics']
        assert row['configuration']['anchor_round'] in (168,169)
        if row['configuration']['model'] is not None:
            assert row['configuration']['anchor_round']==169
            assert row['whole_complete_parent_branches_preserved_before_new_stage'] and row['actual_cold80_260_975_bits_exact']
    if cfg['model'] is None:
        assert control['status']=='passed_selected_fully_qualified_anchor132_no_new_native_stage_claimed'
        assert read(A/f"optimization_20261003_r{cfg['anchor_round']}/full_registration_execution.json")['status']=='passed'
        assert best['metrics']==read(A/f"optimization_20261003_r{cfg['anchor_round']}/calibrated_csv_official.json")['metrics']
        actual_native14=False
    else:
        assert cfg['anchor_round']==169 and cfg['recipe'] in ('cross120recent252forward5huber050','cross120recent252rank5huber050')
        assert (control['actual_saved_states'],control['actual_historical_cases'],control['actual_calendar_cases'],control['actual_cold_cases'])==(6,10,4,14)
        assert len(control['prefit_rejections'])==7 and best['connected_final_score']>baseline['final_score']
        actual_native14=True
    for path,digest in pilot['input_sha256'].items():assert sha(path)==digest,path
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'cross120170_full_family_preflight_v4_20261010.json',{'status':'passed_complete132_measured_capsules_source_routes_QA81_and_selected120_native14_or_exact_qualified_anchor_before_future_dispatch',
        'input_sha256':{str(p):sha(p) for p in [*sources,folder/'pilot132.json',folder/'verification.json']},
        'actual_new_selected_native14_passed':actual_native14,'qualified_anchor_reuse':not actual_native14,
        'new_native_fits':0,'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,
        'new_full170_inference_if_selected_then_registry_QA81_main_pending':True})
    print({'admitted_records':132,'QA':81,'new_selected_native14_passed':actual_native14,'future_dispatch_not_started':True},flush=True)

if __name__=='__main__':main()

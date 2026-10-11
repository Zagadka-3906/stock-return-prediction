"""Admit exact own recent252 bank, parent167 graph, original65 scores and new168 routes."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments

def main():
    from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed
    assert allowed()
    import prepare_protected168_full_registry_sources_v1_20261010 as routes
    for name in ('protected168_candidate_sources_preparation_v2_20261010.json','protected168_full_registry_source_preparation_v1_20261010.json','RecentReturn252Protected168_actual_own_bank_pointer_correction_v1_20261010.json','RecentReturn252_after167_selected_native14_source_admission_v1_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    extras=['prepare_protected168_full_registry_sources_v1_20261010.py','prepare_protected168_selected_candidate_v4_20261010.py','run_RecentReturn252Protected168_full_registration_v1_20261010.py','run_RecentReturn252Protected168_complete_family_v1_20261010.py','RecentReturn252Protected168_actual_own_bank_pointer_correction_v1_20261010.json']
    sources=list(dict.fromkeys([*routes.source_paths(),*[A/n for n in extras],Path(__file__)]))
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round168.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(168,167,(451,))
    register=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for text in ("'expected_scored_records': 67","'explicit_parent_round': 167","'waves': [451]"):assert text in register,text
    publisher=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for text in ('collect(168, 79, 67)',"namespace['snapshot'](168)","'scored_records': 67","'actual_full_QA_version': 79"):assert text in publisher,text
    prep=(A/'prepare_protected168_selected_candidate_v4_20261010.py').read_text(encoding='utf8')
    own='actual_BF16RecentReturn252Huber050169_full5_independent_location_v1_20261009.json'
    assert own in prep and 'actual_BF16RecentReturn252Huber050166_full5' not in prep
    import protected_RecentReturn252_after167_native_stage_v1_20261010 as stage
    import predict_protected_RecentReturn252_after167_complete_scheme_v2_20261010 as predictor
    assert predictor.PARENT_FILENAME=='predict_protected_Return_after163_complete_scheme_v4_20261010.py'
    assert stage.GRAPH_KEY=='protected_RecentReturn252_after_complete167_native_v1_20261010'
    assert stage.BACKENDS['recent252returnhuber050'][0]=='neural_BF16_medium2048_recent252returnhuber050_seed09_e64_native_v1_20261009'
    proofpath=Path('E:/赛题五_本机临时/RecentReturn252_after167_high_impact65_screen_v1_20261010/verification.json')
    proof=read(proofpath)
    assert len(proof['records'])==65 and proof['actual_nonidentity_full_controls']==64 and proof['actual_nonidentity_prefix_controls']==192
    for row in proof['records']:
        p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics']
    receipt=read(A/'high_impact_priority_huber65_main_receipt_v19_20261010.json');assert receipt['status']=='pushed_and_remote_head_verified'
    nativefolder=Path(read(A/'actual_protected_RecentReturn252_selected_native14_location_v1_20261010.json')['output'])
    controls=read(nativefolder/'verification.json')
    assert (controls['actual_saved_states'],controls['actual_historical_cases'],controls['actual_calendar_cases'],controls['actual_cold_cases'])==(6,10,4,14)
    assert len(controls['prefit_rejections'])==7
    pilot=read(nativefolder/'pilot67.json')
    assert len(pilot['records'])==67 and pilot['actual_scheme_base_round']==pilot['actual_comparison_parent_round']==167
    assert pilot['best']['connected_final_score']>=proof['best']['connected_final_score']
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'protected168_full_family_preflight_v1_20261010.json',{'status':'passed_actual65_capsules67_routes_QA79_actual_own169_bank_and_selected_native14_before_future_dispatch','input_sha256':{str(p):sha(p) for p in [*sources,proofpath,nativefolder/'pilot67.json',nativefolder/'verification.json']},'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'selected_future_inference_pending':True})
    print('PASS original65 capsules, own recent252 six-state14 and entire167 graph routes for QA79',flush=True)
if __name__=='__main__':main()

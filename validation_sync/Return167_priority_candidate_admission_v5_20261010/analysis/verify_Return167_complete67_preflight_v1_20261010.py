"""Admit all actual65 capsules and corrected whole163 graph routes before native/candidate dispatch."""
from pathlib import Path
import sys
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
def main():
    import prepare_protected167_full_registry_sources_v1_20261010 as routes
    for name in ('protected167_candidate_sources_preparation_v2_20261010.json','protected167_full_registry_source_preparation_v1_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    extra=['run_Return167_complete_family_admitted_v2_20261010.py','run_Return167_full_registration_admitted_v2_20261010.py','prepare_protected167_selected_candidate_v3_20261010.py','predict_protected_Return_after163_complete_scheme_v4_20261010.py','Return167_actual_parent163_source_and_callback_controls_v2_20261010.json']
    sources=routes.source_paths()+[A/n for n in extra]+[Path(__file__)]
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round167.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(167,166,(450,))
    text=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for needle in ("'expected_scored_records': 67","'explicit_parent_round': 166","'waves': [450]"):assert needle in text,needle
    text=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for needle in ('collect(167, 78, 67)',"namespace['snapshot'](167)","'scored_records': 67","'actual_full_QA_version': 78"):assert needle in text,needle
    prep=(A/'prepare_protected167_selected_candidate_v3_20261010.py').read_text(encoding='utf8');assert 'actual_BF16ReturnHuber050166_full5_independent_location_v1_20261009.json' in prep
    import protected_Return_after163_native_stage_v3_20261010 as stage
    assert 'returnhuber050' in stage.BACKENDS and 'CDF' in stage.CODECS
    screenpath=Path('E:/赛题五_本机临时/Return_after163_high_impact65_screen_v1_20261010/verification.json');screen=read(screenpath)
    assert len(screen['records'])==65 and screen['actual_nonidentity_full_controls']==64 and screen['actual_nonidentity_prefix_controls']==192
    for row in screen['records']:
        p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics']
    for p,d in read(A/'Return167_actual_parent163_source_and_callback_controls_v2_20261010.json')['input_sha256'].items():assert sha(p)==d,p
    assert screen['best']['score_gain_over_qualified_parent']>0,'Priority round requires an actual improvement'
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    create(A/'protected167_full_family_preflight_v1_20261010.json',{'status':'passed_actual65_capsules67_complete_routes_QA78_and_original163_AST_preservation_before_dispatch','input_sha256':{str(p):sha(p) for p in [*sources,screenpath]},'new_quality_scores':0,'actual_future_X_read':False,'test_labels_read':False,'actual_native14_and_candidate_inference_pending':True})
    print('PASS actual65 capsules, corrected complete163 callbacks and67 routes for QA78',flush=True)
if __name__=='__main__':main()

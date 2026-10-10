"""Check exact67 routes and controls before any163 native or future dispatch."""
from pathlib import Path
import sys,ast,time
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from verify_protected162_full_family_preflight_v1_20261010 import literal_assignments
def main():
    import prepare_protected163_full_registry_sources_v1_20261010 as routes
    for name in ('protected163_candidate_sources_preparation_v2_20261010.json','protected163_full_registry_source_preparation_v1_20261010.json'):
        for p,d in read(A/name)['input_sha256'].items():assert sha(p)==d,p
    sources=routes.source_paths()+[A/'run_Huber163_complete_family_admitted_v2_20261010.py',A/'run_Huber163_full_registration_cleanup_v2_20261010.py',Path(__file__)]
    for p in sources:
        assert p.is_file(),p
        if p.suffix=='.py':compile(p.read_text(encoding='utf8'),str(p),'exec')
    opt=literal_assignments(A/'optimize_training_round163.py');assert (opt['NUMBER'],opt['PREVIOUS_NUMBER'],opt['WAVES'])==(163,162,(446,))
    text=(A/routes.NAMES[0]).read_text(encoding='utf8')
    for needle in ("'expected_scored_records': 67","'explicit_parent_round': 162","'waves': [446]"):assert needle in text,needle
    text=(A/routes.NAMES[1]).read_text(encoding='utf8')
    for needle in ('collect(163, 74, 67)',"namespace['snapshot'](163)","'scored_records': 67","'actual_full_QA_version': 74"):assert needle in text,needle
    prep=(A/'prepare_protected163_selected_candidate_v2_20261010.py').read_text(encoding='utf8');assert 'actual_BF16Huber010161_full5_independent_location_v1_20261009.json' in prep
    import protected_tail_after157_native_stage_v2_20261010 as stage
    assert 'huber010' in stage.BACKENDS and 'CDF' in stage.CODECS
    source=Path('E:/赛题五_本机临时/Huber010_high_impact65_screen_v1_20261010/verification.json');screen=read(source)
    assert len(screen['records'])==65 and screen['actual_nonidentity_full_controls']==64 and screen['actual_nonidentity_prefix_controls']==192
    for row in screen['records']:
        p=Path(row['official_score_cache']['official_metrics_source']);assert sha(p)==row['official_metric_capsule_sha256'] and read(p)['metrics']==row['metrics']
    assert screen['best']['configuration']['kind']=='valid_pool_protection_v1'
    assert sha(ROOT/'.git/index')=='ed2fa41598113343f7cf84c4ff16f7685c9ed3e079c16edf869c2c32019d3406'
    pins={str(p):sha(p) for p in [*sources,source]}
    create(A/'protected163_full_family_preflight_v1_20261010.json',{'status':'passed67_actual65_controls_capsules_and_exact_full_routes_QA74_before_dispatch','input_sha256':pins,'new_quality_scores':0,'future_X_read':False,'test_labels_read':False,'process_local_nested_adapter_cleanup_fixed_before_outer_scope_exit':True,'original_compiled_sources_unchanged':True})
    descriptor=A/'HuberProtected163_full67_ready_dispatch_v1_20261010.json'
    create(descriptor,{'round':163,'quality_cases':67,'QA':74,'driver':'run_Huber163_complete_family_admitted_v2_20261010.py','service_name':'HuberProtected163_complete67_family_v2_20261010','arguments':[],'input_sha256':{**pins,str(A/'protected163_full_family_preflight_v1_20261010.json'):sha(A/'protected163_full_family_preflight_v1_20261010.json')},'new_quality_scores_by_dispatch':0})
    print('PASS67 real65 capsules, compiled full routes, QA74, source-preserving corrections',flush=True)
if __name__=='__main__':main()

"""Dispatch150 after actual149 qualification and its own55-case prior forecast audit."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('SparseAfter148152_complete_prospective_controls_v1_20261009')
    closed('RFFSparse59_round151_full_registration_v1_20261009')
    closed('SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009')
    proof=A/'SparseAfter14829_prospective_routes_v1_20261009.json';p=read(proof)
    for path,d in p['input_sha256'].items():assert sha(path)==d,path
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('SparseAfter14829_round152_source_admission_v1_20261009','verify_SparseAfter14829_round152_sources_v1_20261009.py',[]),
        ('SparseAfter14829_controls_main_publication_v1_20261009','publish_SparseAfter14829_evidence_v1_20261009.py',['controls']),
        ('SparseAfter14829_official_comparison_v1_20261009','run_SparseAfter14829_official_comparison_v2_20261009.py',[]),
        ('SparseAfter14829_scores_main_publication_v1_20261009','publish_SparseAfter14829_evidence_v1_20261009.py',['scores']),
        ('SparseAfter14829_selected_candidate_preparation_v1_20261009','prepare_SparseAfter14829_selected_candidate_v2_20261009.py',[]),
        ('SparseAfter14829_selected_candidate_sealing_v1_20261009','seal_SparseAfter14829_selected_candidate_v2_20261009.py',[]),
        ('SparseAfter14829_round152_full_registration_v1_20261009','run_SparseAfter14829_round152_full_registration_v2_20261009.py',[])]
    pins={str(Path(__file__)):sha(__file__),str(proof):sha(proof)};rows={}
    for name,driver,args in specs:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
    create(A/'SparseAfter148152_complete_hidden_launches_v1_20261009.json',{'status':'started_seven_preflighted150_receivers_after_actual149_full_qualification_and_actual55_duplicates','launches':rows,'input_sha256':pins,
        'stage_base_round':148,'expected_official_cases':29,'QA_version':63,'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()

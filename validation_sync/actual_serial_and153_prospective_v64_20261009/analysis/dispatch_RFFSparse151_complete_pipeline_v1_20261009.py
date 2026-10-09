"""Dispatch all151 recipients after actual150 qualification, own duplicates and complete source controls."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned

def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name

def main():
    closed('RFFSparse151_complete_prospective_controls_v1_20261009')
    closed('HuberSparse59_round150_full_registration_v1_20261008')
    closed('RFFSparse151_prior_complete_forecast_duplicate_audit_v1_20261009')
    p=A/'RFFSparse59_prospective_routes_v1_20261009.json';proof=read(p)
    for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('RFFSparse59_round151_source_admission_v1_20261009','verify_RFFSparse59_round151_sources_v1_20261009.py',[]),
        ('RFFSparse59_controls_main_publication_v1_20261009','publish_RFFSparse59_evidence_v2_20261009.py',['controls']),
        ('RFFSparse59_official_comparison_v1_20261009','run_RFFSparse59_official_comparison_v3_20261009.py',[]),
        ('RFFSparse59_scores_main_publication_v1_20261009','publish_RFFSparse59_evidence_v2_20261009.py',['scores']),
        ('RFFSparse59_selected_candidate_preparation_v1_20261009','prepare_RFFSparse59_selected_candidate_v3_20261009.py',[]),
        ('RFFSparse59_selected_candidate_sealing_v1_20261009','seal_RFFSparse59_selected_candidate_v3_20261009.py',[]),
        ('RFFSparse59_round151_full_registration_v1_20261009','run_RFFSparse59_round151_full_registration_v3_20261009.py',[])]
    pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}
    for name,driver,args in specs:rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
    create(A/'RFFSparse151_complete_hidden_launches_v1_20261009.json',{'status':'started_seven_preflighted151_receivers_after_actual150_full_and_own55_forecast_audit','launches':rows,
        'input_sha256':pins,'stage_base_round':134,'expected_official_cases':59,'QA_version':62,'new_quality_scores_by_dispatch':0,'new_native_fits':0,'test_labels_read':False})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()

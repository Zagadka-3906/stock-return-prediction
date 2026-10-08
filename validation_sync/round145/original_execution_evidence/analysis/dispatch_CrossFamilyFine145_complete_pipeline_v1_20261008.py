"""Dispatch only after all complete prospective source controls and the actual preceding141 round qualify."""
from pathlib import Path
import sys,time,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
def closed(name):
    folder=A/'service_owned_workflows_20261006'/name
    while not (folder/'native_launch.json').exists() or owned(read(folder/'native_launch.json')):time.sleep(10)
    assert read(folder/'service_execution.json')['status']=='passed',name
def main():
    closed('CrossFamilyFine145_complete_prospective_controls_v1_20261008')
    p=A/'CrossFamilyFine125_prospective_routes_v1_20261008.json';proof=read(p)
    for path,d in proof['input_sha256'].items():assert sha(path)==d,path
    closed('KrylovGram52_round141_full_registration_v18_20261008')
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    specs=[('CrossFamilyFine125_round145_source_admission_v1_20261008','verify_CrossFamilyFine125_round145_sources_v1_20261008.py',[]),
        ('CrossFamilyFine125_controls_main_publication_v1_20261008','publish_CrossFamilyFine125_evidence_v1_20261008.py',['controls']),
        ('CrossFamilyFine125_official_comparison_v1_20261008','run_CrossFamilyFine125_official_comparison_v1_20261008.py',[]),
        ('CrossFamilyFine125_scores_main_publication_v1_20261008','publish_CrossFamilyFine125_evidence_v1_20261008.py',['scores']),
        ('CrossFamilyFine125_selected_candidate_preparation_v1_20261008','prepare_CrossFamilyFine125_selected_candidate_v1_20261008.py',[]),
        ('CrossFamilyFine125_selected_candidate_sealing_v1_20261008','seal_CrossFamilyFine125_selected_candidate_v1_20261008.py',[]),
        ('CrossFamilyFine125_round145_full_registration_v2_20261008','run_CrossFamilyFine125_round145_full_registration_v2_20261008.py',[])]
    pins={str(Path(__file__)):sha(__file__),str(p):sha(p)};rows={}
    for name,driver,args in specs:
        rows[name]=start(name,driver,args,{**pins,str(A/driver):sha(A/driver)})
    create(A/'CrossFamilyFine145_complete_hidden_launches_v1_20261008.json',{'status':'started_seven_preflighted145_receivers_after_actual141_full_qualification','launches':rows,'input_sha256':pins,
        'stage_base_round':134,'expected_official_cases':125,'QA_version':56,'new_fits':0,'new_quality_scores_by_dispatch':0,'test_labels_read':False})
    print(json.dumps({'started':list(rows)}),flush=True)
if __name__=='__main__':main()

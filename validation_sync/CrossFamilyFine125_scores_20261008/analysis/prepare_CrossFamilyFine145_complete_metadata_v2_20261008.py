"""Finalize fresh full2 and actual20/121/363/30 publisher surfaces; preserve every original draft."""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_CrossFamilyFine145_complete_receivers_v1_20261008 import convert
def save(p,s):
    assert not p.exists(),p;compile(s,str(p),'exec');p.write_text(s,encoding='utf8',newline='\n')
def main():
    old=A/'run_CrossFamilyFine125_round145_full_registration_v1_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace('prepare_CrossFamilyFine125_round145_sources_v1_20261008','prepare_CrossFamilyFine125_round145_sources_v2_20261008')
    s=s.replace('actual_registration_v1_20261008','actual_registration_v2_20261008').replace('full_registration_v1_file_IO_20261008','full_registration_v2_file_IO_20261008')
    s=s.replace('lossless_ranking_runtime_adapter_round145_20261007','lossless_ranking_runtime_adapter_round145_v2_20261008')
    full=A/'run_CrossFamilyFine125_round145_full_registration_v2_20261008.py';save(full,s)
    original=A/'publish_CrossFamily94_evidence_v5_20261008.py';s=convert(original.read_text(encoding='utf8'))
    s=s.replace('prepare_CrossFamilyFine125_round145_sources_v1_20261008','prepare_CrossFamilyFine125_round145_sources_v2_20261008')
    s=s.replace("    closed('ConeRidgeAlpha100_round144_full_registration_v12_20261008')","    closed('KrylovGram52_round141_full_registration_v18_20261008')")
    s=s.replace("    closed('BF16wide40_round135_full_registration_v7_20261008')\n",'')
    s=s.replace('CrossFamily91_current_parent_controls_v2_20261008','CrossFamilyFine121_actual_full_historical_controls_v1_20261008')
    s=s.replace('actual_CrossFamily15_native_hooks_location_v2_20261008','actual_CrossFamilyFine30_native_hooks_location_v1_20261008')
    s=s.replace('passed_actual30_heads91_current_CDF273cold15_historical_native_hooks','passed_actual20_heads121_fixed_base_CDF363cold30_historical_native_hooks')
    s=s.replace("'actual_existing_native_head_audits':30","'actual_existing_native_head_audits':20").replace("'actual_full_native_OOF_heads':6","'actual_full_native_OOF_heads':4")
    s=s.replace("'actual_full_CDF_controls':91","'actual_full_CDF_controls':121").replace("'actual_cold_CDF_controls':273","'actual_cold_CDF_controls':363").replace("'actual_historical_native_hooks':15","'actual_historical_native_hooks':30")
    s=s.replace('CrossFamilyFine125_{phase}_github_v2_20261008','CrossFamilyFine125_{phase}_github_v1_20261008')
    s=s.replace('from file_backed_hidden_git_runtime_20261007 import installed','from verified_TLS_Git_retry_runtime_v2_20261008 import installed')
    publisher=A/'publish_CrossFamilyFine125_evidence_v1_20261008.py';save(publisher,s)
    import CrossFamilyFine145_storage_v1_20261008 as storage
    import subprocess
    for path,target in storage.OUTPUTS.items():
        assert path.resolve().is_relative_to(ROOT.resolve()),path
        assert target.resolve().is_relative_to(Path('E:/赛题五_本机临时/第145轮_20261008').resolve()),target
        assert not path.exists(),path;target.mkdir(parents=True,exist_ok=False)
        # Native PowerShell only; no composed shell deletes/moves or visible windows.
        command="New-Item -ItemType Junction -Path '"+str(path).replace("'","''")+"' -Target '"+str(target).replace("'","''")+"' | Out-Null"
        result=subprocess.run(['pwsh','-NoProfile','-Command',command],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
        assert result.returncode==0,result.stderr;storage.empty(path)
    pins={str(p):sha(p) for p in [Path(__file__),old,original,full,publisher,A/'prepare_CrossFamilyFine125_round145_sources_v1_20261008.py',A/'prepare_CrossFamilyFine125_round145_sources_v2_20261008.py',A/'CrossFamilyFine145_receiver_drafts_v1_20261008.json']}
    create(A/'CrossFamilyFine145_receiver_preparation_v2_20261008.json',{'status':'prepared_complete_noncolliding145_receivers_with_physical_outputs_before_prospective_controls',
        'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':pins,'original_draft1_QA_files_preserved_not_used_for_final145':True,
        'scoped_round_QA_and_case_numeric_guards_corrected_before_scientific_admission':True,'all_large_outputs_on_E':True,'quality_scoring_cache_on_D':True,
        'stage_base_round':134,'comparison_anchors':[134,136,141,144],'new_quality_scores':0,'test_labels_read':False})
    print(json.dumps({'completed_full_registration_receiver_version':2,'prospective_checks_still_required':True,'quality_not_started':True}),flush=True)
if __name__=='__main__':main()

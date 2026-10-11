"""Publish the complete pre-score145 contract and retain every draft before unscored anchor141 qualification."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
def main():
    old=A/'publish_actual138_and_fine145_historical_controls_main_v25_20261008.py';s=old.read_text(encoding='utf8')
    s=s.replace("for name in ('BF16reverse40_round138_full_registration_v17_20261008','CrossFamilyFine30_actual_native_historical_controls_v1_20261008',\n        'CrossFamilyFine121_actual_full_historical_controls_v1_20261008','HuberCrossFamily112_controls_main_publication_v18_20261008')", "for name in ('CrossFamilyFine145_complete_prospective_controls_v1_20261008','actual138_fine145_historical_controls_main_publication_v25_20261008')")
    s=s.replace('actual138_and_fine145_historical_controls_main_v25_20261008','actual145_complete_prospective_main_v27_20261008').replace('actual138_and_fine145_historical_controls_v25_20261008','actual145_complete_prospective_v27_20261008')
    s=s.replace('datetime.datetime(2026,10,8,17,11)','datetime.datetime(2026,10,8,18,15)')
    s=s.replace("sources=[Path(__file__),A/'github_validation_sync_main_20261005/round138_receipt.json',A/'optimization_20261003_r138/full_registration_execution.json']", "sources=[Path(__file__),A/'CrossFamilyFine125_prospective_routes_v1_20261008.json',A/'CrossFamilyFine145_receiver_drafts_v1_20261008.json',A/'CrossFamilyFine145_receiver_preparation_v2_20261008.json',A/'CrossFamilyFine125_round145_plan_v2_20261008.json',A/'CrossFamilyFine125_round145_plan_v1_20261008.json',A/'CrossFamilyFine145_D_scoring_scope_v1_20261008.json',A/'actual138_fine145_historical_controls_main_v25_receipt_20261008.json']")
    needle="        payload[(prefix/'.gitattributes').as_posix()]=b'* -text\\n'";assert needle in s
    s=s.replace(needle,"        prospective=read(A/'CrossFamilyFine125_prospective_routes_v1_20261008.json');assert prospective['actual_prospective_sources']==32 and prospective['actual_graph_controls']==968\n"+needle)
    s=s.replace("'all145_score_candidate_registry_prospective_receivers_still_required':True", "'actual145_prospective_sources':32,'actual145_graph_controls':968,'actual145_baseline_controls':12,'actual145_signed_tie_controls':8,'actual145_collector_controls':4,'all145_receivers_prepared_and_preflighted_before_quality':True,'actual141_full_qualification_still_required_before_quality':True")
    s=s.replace('actual138_full_qualification_and_new_signed145_historical_controls_with_all_failures_distinct','actual145_complete_pre_score_sources_native_and_full_historical_controls_with_all_drafts_distinct')
    s=s.replace('同步138轮完整验证、145轮细权重历史控制和全部恢复记录','同步145轮完整125项选模流程、32路径968图控制及草稿记录')
    s=s.replace('actual138_fine145_historical_controls_main_v25_receipt_20261008.json\',receipt','actual145_complete_prospective_main_v27_receipt_20261008.json\',receipt')
    target=A/'publish_actual145_complete_prospective_main_v27_20261008.py';assert not target.exists();compile(s,str(target),'exec');target.write_text(s,encoding='utf8',newline='\n')
    pins={str(p):sha(p) for p in [Path(__file__),old,target,A/'CrossFamilyFine125_prospective_routes_v1_20261008.json']}
    create(A/'actual145_complete_prospective_publication_preparation_v27_20261008.json',{'status':'prepared_actual32_968_before_quality_main_publication','input_sha256':pins,'new_quality_scores':0})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('actual145_complete_prospective_main_publication_v27_20261008',target.name,[],pins)
    create(A/'actual145_complete_prospective_publication_hidden_launch_v27_20261008.json',{'launch':row,'input_sha256':pins})
    print(json.dumps({'publication_worker':row['owned_worker_pid'],'official_quality_not_started':True}),flush=True)
if __name__=='__main__':main()

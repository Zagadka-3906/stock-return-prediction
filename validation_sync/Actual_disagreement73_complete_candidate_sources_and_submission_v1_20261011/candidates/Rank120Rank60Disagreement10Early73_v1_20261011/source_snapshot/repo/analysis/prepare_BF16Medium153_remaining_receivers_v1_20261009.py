"""Prepare truthful duplicate audit and safe publication from the current152 receiver contracts."""
from pathlib import Path
import sys,time
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import sha,create

def save(name,s):
    p=A/name;compile(s,str(p),'exec')
    with p.open('x',encoding='utf8') as f:f.write(s)
    return p

def main():
    old=A/'verify_SparseAfter148152_prior_complete_forecast_duplicate_audit_v1_20261009.py';s=old.read_text(encoding='utf8')
    mapping={'SparseAfter148152':'BF16Medium153','RFFSparse59_round151_full_registration_v1_20261009':'SparseAfter14829_round152_full_registration_v1_20261009',
      'round151':'round152','_r151':'_r152','actual_SparseAfter14825_parent148_location_v1_20261009':'actual_BF16Medium153_full73_training_location_v1_20261009',
      'SparseAfter14829_round152_proposal_v1_20261009':'BF16Medium78_round153_proposal_v1_20261009',
      "current['records']":"current['controls']","cfg['amplitude']":"cfg['weight']",'actual134':'actual148',
      'passed_actual25_SparseAfter148_full_training_CDF_and75_cold_controls_with_exact148_identity':'passed_actual73_full5635800_medium153_signed_rank_mix_and219_cold_prefixes',
      "len(current['controls'])==25":"len(current['controls'])==73", "'actual_current_cases':25":"'actual_current_cases':73",
      'passed_actual55_forecast_hash_audit_against_prior_available_complete_scheme_hashes_and1_zero134_control':'passed_actual73_medium153_forecast_hash_audit_and1_zero148_control'}
    for before,after in mapping.items():
        assert before in s,before;s=s.replace(before,after)
    # Count73 is tested against the same immutable proposal used by the full oracle.
    dup=save('verify_BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009.py',s)
    pubold=A/'publish_SparseAfter14829_evidence_v1_20261009.py';s=pubold.read_text(encoding='utf8')
    for before,after in [('RFFSparse59_round151_full_registration_v1_20261009','SparseAfter14829_round152_full_registration_v1_20261009'),
      ('SparseAfter14855_full_historical_controls_v1_20261009','BF16Medium153_actual_full73_training_v1_20261009'),
      ('SparseAfter14829','BF16Medium78'),('SparseAfter148152','BF16Medium153'),('full152','full153'),('round152','round153'),('第152轮','第153轮'),('QA63','QA64')]:s=s.replace(before,after)
    s=s.replace('actual_SparseAfter14825_parent148_location_v1_20261009','actual_BF16Medium153_full73_training_location_v1_20261009')
    s=s.replace('actual_SparseAfter14860_native_calendar_location_v1_20261009','actual_BF16Medium153_native42_calendar_location_v1_20261009')
    s=s.replace('passed_actual10_states25_fixed_base_CDF75cold60_native_calendar_controls','passed_actual6_medium153_states42_native73_full219_cold_controls')
    s=s.replace("'round':152","'round':153").replace("'actual_existing_native_head_audits':10","'actual_existing_native_head_audits':6")
    s=s.replace("'actual_full_native_OOF_heads':4","'actual_full_native_OOF_heads':1").replace("'actual_full_CDF_controls':25","'actual_full_CDF_controls':73")
    s=s.replace("'actual_cold_CDF_controls':75","'actual_cold_CDF_controls':219").replace("'actual_historical_native_hooks':48","'actual_historical_native_hooks':30").replace("'actual_cold_native_hooks':60","'actual_cold_native_hooks':42")
    s=s.replace("==29","==78").replace("29 if phase=='scores' else 0","78 if phase=='scores' else 0")
    s=s.replace('passed_actual29_SparseAfter148_complete_parent_full_official_comparisons','passed_actual78_BF16_medium2048_seed09_complete_parent_rank_CDF_full_official_comparisons')
    s=s.replace('同步第153轮Huber与稀疏模型集成实际证据','同步第153轮中型神经排序融合实际证据')
    # The large-report/source-index/TLS guards are process-scoped and verified already.
    needle="    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));main(parser.parse_args().phase)";assert s.count(needle)==1
    s=s.replace(needle,"""    import os
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('controls','scores'));phase=parser.parse_args().phase
    count=int(os.environ.get('GIT_CONFIG_COUNT','0'))
    for offset,(key,value) in enumerate((('http.proxy','http://127.0.0.1:7897'),('http.version','HTTP/1.1'))):
        os.environ[f'GIT_CONFIG_KEY_{count+offset}']=key;os.environ[f'GIT_CONFIG_VALUE_{count+offset}']=value
    os.environ['GIT_CONFIG_COUNT']=str(count+2)
    from lossless_chunked_safe_main_runtime_v1_20261009 import installed as safe
    with safe(Path('E:/赛题五_本机临时/第153轮_20261009')/('safe_'+phase+'_main_v1')):main(phase)""")
    publisher=save('publish_BF16Medium78_evidence_v1_20261009.py',s)
    create(A/'BF16Medium153_remaining_receiver_preparation_v1_20261009.json',{'status':'prepared_medium153_duplicate_and_safe_evidence_publication_receivers_not_quality_admitted',
      'at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),'input_sha256':{str(p):sha(p) for p in (Path(__file__),old,pubold,dup,publisher)},
      'previous_complete_board_round':152,'actual_training_cases_expected':73,'quality_scores_expected':78,'test_labels_read':False})
    from start_nonflag_RFF128Low76_actual_admission_v4_20261007 import start
    row=start('BF16Medium153_prior_complete_forecast_duplicate_audit_v1_20261009',dup.name,[],{str(dup):sha(dup)})
    create(A/'BF16Medium153_duplicate_hidden_launch_v1_20261009.json',row);print(row['owned_worker_pid'],flush=True)

if __name__=='__main__':main()

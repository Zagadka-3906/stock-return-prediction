"""Audit55 measured complete forecasts against prior observed hashes, with explicit zero134 proof."""
from pathlib import Path
import sys,time,json,re
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'analysis';sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create,owned
OUT=Path('E:/赛题五_本机临时/BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009')

def closed(n):
    p=A/'service_owned_workflows_20261006'/n
    while not (p/'service_execution.json').exists():time.sleep(10)
    while owned(read(p/'native_launch.json')):time.sleep(1)
    assert read(p/'service_execution.json')['status']=='passed',n

def main():
    closed('BF16TwoSeed79_round154_full_registration_v1_20261009')
    closed('BF16Seed10_155_actual_full73_training_v2_20261009')
    import psutil
    while psutil.virtual_memory().available<3*2**30:time.sleep(15)
    from build_lossless_ranking_display_v2_20261006 import unpack_report
    display=A/'lossless_ranking_display_v2_20261006/round154';proof=read(display/'verification.json');page=display/'complete_rankings_lossless.html'
    assert proof['status']=='passed_all_original_report_values_and_six_views_lossless_roundtrip' and sha(page)==proof['lossless_HTML_sha256']
    match=re.search(r'<script\s+id="data"\s+type="application/json">(.*?)</script>',page.read_text(encoding='utf8'),re.S);assert match
    report=unpack_report(json.loads(match.group(1)));del match
    assert len(report['connected'])==proof['connected_records']
    pointer=A/'actual_BF16Seed10_155_full73_training_location_v1_20261009.json';full=Path(read(pointer)['output'])/'verification.json'
    assert sha(full)==read(pointer)['verification_sha256'];current=read(full)
    assert current['status']=='passed_actual73_full5635800_seed10_155_signed_rank_mix_and219_cold_prefixes' and len(current['controls'])==73
    proposal_path=A/'BF16Seed10_80_round155_proposal_v1_20261009.json';proposal=read(proposal_path)
    prior={};unavailable=[];ineligible=[];scanned=0
    for row in report['connected']:
        scanned+=1
        if row.get('known_restriction'):ineligible.append(row['id']);continue
        params=row.get('parameters',{});control=params.get('actual_full_conditional_residual_control',{})
        digest=params.get('original_numeric_prediction_sha256',control.get('prediction_numeric_bytes_sha256'))
        complete=bool(control.get('whole_complete_parent_branches_preserved_before_new_stage') or control.get('qualified_anchor_all8_metrics_exact'))
        if not digest or not complete:
            unavailable.append({'id':row['id'],'hash_available':bool(digest),'complete_graph_hash_proof_available':complete});continue
        assert re.fullmatch('[0-9a-f]{64}',digest)
        prior.setdefault(digest,[]).append({'id':row['id'],'source':row['source'],'source_pointer':row['source_pointer'],'score':row['score'],'metrics':row['metrics'],'all8_metrics':control.get('metrics')})
    import numpy as np,hashlib
    base=A/'optimization_20261003_r148/selected_validation.npy';arr=np.load(base,mmap_mode='r')
    base_sha=hashlib.sha256(memoryview(np.ascontiguousarray(arr)).cast('B')).hexdigest();del arr
    base_metrics_path=A/'optimization_20261003_r148/calibrated_csv_official.json';metrics=read(base_metrics_path)['metrics']
    rows=[];known=[]
    for row in current['controls']:
        cfg=row['configuration'];digest=row['numeric_sha256']
        assert cfg==proposal['new_cases'][row['case']]
        if not cfg['weight']:
            assert digest==base_sha and digest in prior
            for previous in prior[digest]:
                assert all(metrics[k]==v for k,v in previous['metrics'].items())
                if previous['all8_metrics'] is not None:assert previous['all8_metrics']==metrics
            known.append({'control_case':row['case'],'actual148_complete_forecast_sha256':base_sha,'actual148_all8_metrics':metrics})
        rows.append({'control_case':row['case'],'configuration':cfg,'numeric_sha256':digest,'prior_full_board_matches':prior.get(digest,[]),'has_prior_observed_forecast_duplicate':digest in prior})
    assert len(known)==1
    inputs=[Path(__file__),display/'verification.json',page,pointer,full,proposal_path,base,base_metrics_path,A/'optimization_20261003_r154/full_registration_execution.json',A/'github_validation_sync_main_20261005/round154_receipt.json']
    OUT.mkdir(exist_ok=False)
    create(OUT/'verification.json',{'status':'passed_actual73_seed10_155_forecast_hash_audit_and1_zero148_control','at_local':time.strftime('%Y-%m-%dT%H:%M:%S'),
        'input_sha256':{str(p):sha(p) for p in inputs},'actual_prior_full_board_records_scanned':scanned,'eligible_prior_numeric_hashes':len(prior),'prior_rows_without_sufficient_complete_forecast_hash_proof':unavailable,'ineligible_restricted_rows':ineligible,
        'actual_current_cases':73,'known_zero_control_count':1,'known_controls':known,'records':rows,'remaining_cases_without_observed_prior_duplicate':sum(not r['has_prior_observed_forecast_duplicate'] for r in rows),
        'no_global_semantic_uniqueness_or_exhaustion_claimed':True,'all8_official_metrics_of_zero_previous_matches_crosschecked':True,'new_quality_scores':0,'new_model_fits':0,'test_labels_read':False})
    create(A/'actual_BF16Seed10_155_prior_complete_forecast_duplicate_audit_v1_20261009.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'new_quality_scores':0})
    print({'actual_cases':25,'known_controls':1,'board_records':scanned},flush=True)
if __name__=='__main__':main()

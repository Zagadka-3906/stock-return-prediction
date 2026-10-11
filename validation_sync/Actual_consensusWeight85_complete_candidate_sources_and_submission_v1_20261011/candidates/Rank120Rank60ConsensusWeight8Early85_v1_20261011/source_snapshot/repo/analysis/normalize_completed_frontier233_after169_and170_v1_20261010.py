"""Compare all completed193+19+19 actual TRAIN records with both fully qualified anchors."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/frontier233_after169_and170_v1_20261010')

def main():
    assert allowed();planpath=A/'frontier233_after169_and170_complete_comparison_predeclared_plan_v1_20261010.json';plan=read(planpath)
    assert plan['expected_records']==233 and plan['fully_qualified_anchors']==[169,170]
    for family in plan['families']:
        closed(family['actual_service']);receipt=A/family['main_receipt']
        while not receipt.exists():assert allowed();time.sleep(15)
        r=read(receipt);assert r['status']=='pushed_and_remote_head_verified' and r['branch']=='main'
    import numpy as np
    from normalize_predeclared_cross120_two_target132_v5_20261010 import RECIPES
    paths=[Path(__file__),planpath,A/'normalize_predeclared_cross120_two_target132_v5_20261010.py'];pins={str(p):sha(p) for p in paths}
    records=[];model_hashes={};anchor_by_round={}
    for number in (169,170):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        assert read(release/'full_registration_execution.json')['status']=='passed'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json';assert read(receipt)['status']=='pushed_and_remote_head_verified'
        metrics=read(release/'calibrated_csv_official.json')['metrics'];selection=read(release/'selection.json')['winner'];assert selection['metrics']==metrics
        physical=read(candidate/'verification.json')['models'];model_hashes[number]={row['sha256'] for row in physical.values()};assert len(model_hashes[number])==len(physical)
        raw=np.load(release/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()
        cache=selection['official_score_cache'];capsule=Path(cache['official_metrics_source']);assert read(capsule)['metrics']==metrics
        record={'case':len(records),'configuration':{'stage_kind':'anchor','anchor_round':number,'weight':0.,'sign':1.,'native_models':[]},
            'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(physical),
            'prediction_numeric_bytes_sha256':numeric,'official_score_cache':cache,'official_metric_capsule_sha256':sha(capsule),
            'ordered_native_components':[],'qualified_anchor_all8_metrics_exact':True,'test_labels_read':False}
        records.append(record);anchor_by_round[number]=record
        for p in [release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',release/'selected_validation.npy',candidate/'verification.json',receipt,capsule]:pins[str(p)]=sha(p)
    leaves=[];bank_pins={}
    for recipe in ('cross120recent252forward5huber050','cross120recent252rank5huber050'):
        name,bankname=RECIPES[recipe];bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json')
        assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['epochs']==64
        leaves.append({'name':name,'recipe':recipe,'bank':str(bank),'sha256':info['model_sha256']})
        for p in [bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:bank_pins[str(p)]=sha(p)
    full_count=prefix_count=0
    for family in plan['families']:
        folder=Path('E:/赛题五_本机临时')/(family['name']+'_screen_v1_20261010');proofpath=folder/'verification.json';proof=read(proofpath)
        count=family['records'];assert len(proof['records'])==proof['new_quality_score_records']==count
        assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
        full_count+=count-1;prefix_count+=3*(count-1)
        for path,digest in proof['input_sha256'].items():assert sha(path)==digest,path
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[str(A/family['main_receipt'])]=sha(A/family['main_receipt'])
        base=family['base_round'];is_dual=family['records']==193
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration']);cfg.update(anchor_round=base)
            stage='anchor' if identity else 'dual120_rank_consensus' if is_dual else 'parent_only_budget_stability'
            cfg.update(stage_kind=stage,native_models=[] if identity or not is_dual else [leaf['name'] for leaf in leaves])
            extra={leaf['sha256'] for leaf in leaves} if not identity and is_dual else set()
            if identity:
                assert original['metrics']==anchor_by_round[base]['metrics'] and original['prediction_numeric_sha256']==anchor_by_round[base]['prediction_numeric_bytes_sha256']
            recordpath=folder/f"case{original['case']:03d}_official.json";control=folder/f"case{original['case']:03d}_controls.json";capsule=Path(original['official_score_cache']['official_metrics_source'])
            assert read(recordpath)==original and sha(control)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256']
            assert read(capsule)['metrics']==original['metrics']
            records.append({**original,'case':len(records),'configuration':cfg,'family':family['name'],'original_screen_case':original['case'],
                'original_screen_record':str(recordpath),'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],
                'expected_unique_native_models':len(model_hashes[base]|extra),'ordered_native_components':cfg['native_models'],
                'qualified_anchor_all8_metrics_exact':identity,'postprocessing_only_no_additional_native_models':not identity and not is_dual,
                'native_bank_components':leaves if not identity and is_dual else [],'submission_qualified':identity,'test_labels_read':False})
            for p in [recordpath,control,capsule]:pins[str(p)]=sha(p)
    pins.update(bank_pins)
    assert (len(records),full_count,prefix_count)==(233,228,684)
    best=min(records,key=lambda row:(-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case']))
    assert best['connected_final_score']>=anchor_by_round[170]['connected_final_score']
    for path,digest in pins.items():assert sha(path)==digest,path
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot233.json',{'status':'passed_normalized233_actual_TRAIN_official_records_selected_stage_and_frozen_full_inference_pending',
        'records':records,'best':best,'input_sha256':pins,'expected_scored_records':233,'actual_nonidentity_full_controls':228,'actual_nonidentity_prefix_controls':684,
        'actual_comparison_parent_round':170,'actual_scheme_base_round':best['configuration']['anchor_round'],'new_quality_scores_by_normalization':0,
        'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_complete233_actual_TRAIN_records_without_future_features','pilot_sha256':sha(OUT/'pilot233.json'),'best':best,
        'full_candidate_qualification_and_ranking_registration_pending':True,'new_native_fits':0,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_frontier233_after169_and170_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'pilot_sha256':sha(OUT/'pilot233.json')})
    print({'records':233,'best_S':best['connected_final_score'],'stage':best['configuration']['stage_kind'],'full_new_scheme_qualification_pending':True},flush=True)

if __name__=='__main__':main()

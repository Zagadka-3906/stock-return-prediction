"""Normalize actual CDF49 and protected37 against qualified175/186, without rerunning scores."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/rank20_two_seed_complete88_after186_v1_20261011')
PLAN=A/'rank20_two_seed_complete88_after186_plan_v1_20261011.json'
RECIPE='stock_rank20_two_seed_ID16_cross120_recent252_e64'
BANKS=[Path('E:/赛题五_本机临时')/(n+'_small512_BF16_bank6_v1_20261010') for n in ('stock_rank20_embedding','stock_rank20seed10_embedding')]

def best_key(row):
    return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])

def main():
    assert allowed();plan=read(PLAN)
    assert plan['expected_records']==88 and plan['fully_qualified_anchors']==[175,186]
    closed('StockRank20Seed10Embedding186_complete48_family_v2_20261011')
    closed('actual_rank20_two_seed_native84_v1_20261010')
    for family in plan['families']:
        closed(family['actual_service'])
        receipt=A/family['main_receipt']
        while not receipt.exists():assert allowed();time.sleep(15)
        assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main'
    import numpy as np
    proofpaths=[A/'rank20_two_seed_actual_six_population_and_weights_CPU_v1_20261010.json',
        A/'rank20_two_seed_raw_signal_actual_CPU_controls_v1_20261010.json',
        A/'actual_rank20_two_seed_native84_location_v1_20261010.json']
    nativeproof=Path(read(proofpaths[-1])['output'])/'verification.json';proofpaths.append(nativeproof)
    assert read(nativeproof)['actual_native_cases']==84 and read(nativeproof)['actual_cold_cases']==84
    pins={str(p):sha(p) for p in [Path(__file__),PLAN,*proofpaths]};records=[];anchors={};model_hashes={}
    for number in (175,186):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(release/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        winner=read(release/'selection.json')['winner'];metrics=read(release/'calibrated_csv_official.json')['metrics'];assert winner['metrics']==metrics
        physical=read(candidate/'verification.json')['models'];hashes={m['sha256'] for m in physical.values()};assert len(hashes)==len(physical)
        model_hashes[number]=hashes
        raw=np.load(release/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest()
        capsule=Path(winner['official_score_cache']['official_metrics_source']);assert read(capsule)['metrics']==metrics
        row={'case':len(records),'configuration':{'stage_kind':'anchor','anchor_round':number,'model':None,'recipe':None,'codec':None,'weight':0.,'sign':1.,'decay':None},
            'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(physical),
            'prediction_numeric_bytes_sha256':numeric,'official_score_cache':winner['official_score_cache'],'official_metric_capsule_sha256':sha(capsule),
            'actual_return_mapping':winner['causal_return_mapping'],'ordered_native_components':[],'native_bank_components':[],
            'qualified_anchor_all8_metrics_exact':True,'submission_qualified':True,'test_labels_read':False}
        records.append(row);anchors[number]=row
        for p in [receipt,release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',release/'selected_validation.npy',candidate/'verification.json',capsule]:pins[str(p)]=sha(p)
        del raw
    leaves=[]
    for i,bank in enumerate(BANKS):
        assert read(bank/'verification.json')['actual_native_fits']==6
        info=read(bank/'2025/info.json');assert info['configuration']['seed']==(20261009,20261010)[i] and info['configuration']['epochs']==64
        leaves.append({'name':f'Rank20_ID16_Cross120_seed{(20261009,20261010)[i]}_e64','bank':str(bank),'sha256':info['model_sha256'],'seed':(20261009,20261010)[i]})
        for p in [bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:pins[str(p)]=sha(p)
    assert leaves[0]['sha256']!=leaves[1]['sha256']
    full_count=prefix_count=0
    for family in plan['families']:
        folder=Path(family['output']);proofpath=folder/'verification.json';proof=read(proofpath);count=family['records']
        assert len(proof['records'])==proof['new_quality_score_records']==count
        assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
        full_count+=count-1;prefix_count+=3*(count-1)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[str(A/family['main_receipt'])]=sha(A/family['main_receipt'])
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration'])
            if not identity:
                assert original['recipe']==RECIPE and cfg['second_seed_weight'] in (.25,.5,.75)
                assert cfg['kind'] in family['codecs']
            cfg.update(stage_kind='anchor' if identity else 'rank20_two_seed_raw_average' if cfg['kind']=='CDF' else 'rank20_two_seed_raw_average_protected_tail',
                anchor_round=175,model=None if identity else 'Rank20TwoSeed_ID16_cross120_e64',recipe=None if identity else RECIPE,
                codec=None if identity else cfg['kind'],decay=None,first2020_active=not identity)
            if identity:assert original['metrics']==anchors[175]['metrics'] and original['prediction_numeric_sha256']==anchors[175]['prediction_numeric_bytes_sha256']
            recordpath=folder/f"case{original['case']:03d}_official.json";controlpath=folder/f"case{original['case']:03d}_controls.json"
            capsule=Path(original['official_score_cache']['official_metrics_source']);control=read(controlpath)
            assert read(recordpath)==original and sha(controlpath)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256']
            assert read(capsule)['metrics']==original['metrics'] and control['numeric_sha256']==original['prediction_numeric_sha256']
            if not identity:assert control['full_independent_Pandas_exact'] and [p['days'] for p in control['prefix_controls']]==[80,260,975]
            physical=len(model_hashes[175]|({leaf['sha256'] for leaf in leaves} if not identity else set()))
            records.append({**original,'case':len(records),'configuration':cfg,'family':family['name'],
                'original_screen_case':original['case'],'original_screen_record':str(recordpath),
                'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':physical,
                'ordered_native_components':[] if identity else [leaf['name'] for leaf in leaves],
                'native_bank_components':[] if identity else leaves,'physical_models_for_signal':0 if identity else 2,
                'qualified_anchor_all8_metrics_exact':identity,'submission_qualified':identity,'test_labels_read':False})
            for p in [recordpath,controlpath,capsule]:pins[str(p)]=sha(p)
    assert (len(records),full_count,prefix_count)==(88,84,252)
    best=min(records,key=best_key);assert best['connected_final_score']>=anchors[186]['connected_final_score']
    for p,d in pins.items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot88.json',{'status':'passed_normalized88_actual_TRAIN_official_records_selected_native_and_full_future_pending',
        'records':records,'best':best,'input_sha256':pins,'expected_scored_records':88,
        'actual_nonidentity_full_controls':84,'actual_nonidentity_prefix_controls':252,
        'actual_comparison_parent_round':186,'actual_scheme_base_round':best['configuration']['anchor_round'],
        'new_quality_scores_by_normalization':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_complete88_actual_TRAIN_records_without_future_features','best':best,
        'pilot_sha256':sha(OUT/'pilot88.json'),'full_selected_qualification_and_registration_pending':True,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_rank20_two_seed_complete88_after186_location_v1_20261011.json',{'output':str(OUT),'pilot_sha256':sha(OUT/'pilot88.json'),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_records':88,'best_S':best['connected_final_score'],'stage_kind':best['configuration']['stage_kind'],'future_dispatch_not_started':True},flush=True)

if __name__=='__main__':main()

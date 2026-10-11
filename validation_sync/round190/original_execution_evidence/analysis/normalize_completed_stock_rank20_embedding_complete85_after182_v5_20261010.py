"""Compare actual81 one-day and49 persistence records with fully qualified169/170/174 anchors."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/stock_rank20_embedding_complete85_after182_v1_20261010')
RECIPES={'stock_rank20_embedding16_cross120_rank20mean_recent252_small512_BF16_e64':('rank_MLP512_StockEmbedding16_Cross120Recent252Rank20Mean_seed09_e64','stock_rank20_embedding_small512_BF16_bank6_v1_20261010')}

def main():
    assert allowed();planpath=A/'stock_rank20_embedding_complete85_after182_selection_plan_v1_20261010.json';plan=read(planpath)
    assert plan['expected_records']==85 and plan['fully_qualified_anchors']==[174,175,182]
    closed('StockRank20Embedding182_complete63_family_v6_20261010')
    closed('actual_stock_rank20_embedding_six_state_native42_v1_20261010')
    for family in plan['families']:
        actual_aliases={}
        closed(actual_aliases.get(family['actual_service'],family['actual_service']));receipt=A/family['main_receipt']
        while not receipt.exists():assert allowed();time.sleep(15)
        assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main'
    import numpy as np
    pins={str(p):sha(p) for p in [Path(__file__),planpath,A/'stock_rank20_embedding_actual_eleven_parent_callbacks_CPU_controls_v1_20261010.json']};records=[];model_hashes={};anchors={}
    for number in (174,175,182):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(release/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        selection=read(release/'selection.json')['winner'];metrics=read(release/'calibrated_csv_official.json')['metrics'];assert selection['metrics']==metrics
        physical=read(candidate/'verification.json')['models'];model_hashes[number]={row['sha256'] for row in physical.values()};assert len(model_hashes[number])==len(physical)
        raw=np.load(release/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(raw)).cast('B')).hexdigest();cache=selection['official_score_cache'];capsule=Path(cache['official_metrics_source']);assert read(capsule)['metrics']==metrics
        row={'case':len(records),'configuration':{'stage_kind':'anchor','anchor_round':number,'model':None,'recipe':None,'codec':None,'weight':0.,'sign':1.,'decay':None},'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(physical),'prediction_numeric_bytes_sha256':numeric,'official_score_cache':cache,'official_metric_capsule_sha256':sha(capsule),'actual_return_mapping':selection['causal_return_mapping'],'ordered_native_components':[],'qualified_anchor_all8_metrics_exact':True,'test_labels_read':False}
        records.append(row);anchors[number]=row
        for p in [release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',release/'selected_validation.npy',candidate/'verification.json',receipt,capsule]:pins[str(p)]=sha(p)
    leaves={}
    for recipe,(name,bankname) in RECIPES.items():
        bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json');assert read(bank/'verification.json')['actual_native_fits']==6 and info['configuration']['epochs']==64
        leaves[recipe]={'name':name,'recipe':recipe,'bank':str(bank),'sha256':info['model_sha256']}
        for p in [bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:pins[str(p)]=sha(p)
    full_count=prefix_count=0
    for family in plan['families']:
        folder=Path('E:/赛题五_本机临时')/(family['name']+'_screen_v1_20261010');proofpath=folder/'verification.json';proof=read(proofpath);count=family['records'];base=family['base_round']
        assert len(proof['records'])==proof['new_quality_score_records']==count
        assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
        full_count+=count-1;prefix_count+=3*(count-1)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[str(A/family['main_receipt'])]=sha(A/family['main_receipt'])
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration']);recipe=None if identity else cfg.get('recipe','stock_rank20_embedding16_cross120_rank20mean_recent252_small512_BF16_e64');leaf=None if identity else leaves[recipe]
            cfg.update(stage_kind='anchor' if identity else family['stage_kind'],anchor_round=base,model=None if identity else leaf['name'],recipe=recipe,codec=None if identity else cfg['kind'],decay=cfg.get('decay'),first2020_active=not identity)
            if identity:assert original['metrics']==anchors[base]['metrics'] and original['prediction_numeric_sha256']==anchors[base]['prediction_numeric_bytes_sha256']
            recordpath=folder/f"case{original['case']:03d}_official.json";control=folder/f"case{original['case']:03d}_controls.json";capsule=Path(original['official_score_cache']['official_metrics_source'])
            assert read(recordpath)==original and sha(control)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256'] and read(capsule)['metrics']==original['metrics']
            records.append({**original,'case':len(records),'configuration':cfg,'family':family['name'],'original_screen_case':original['case'],'original_screen_record':str(recordpath),'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':len(model_hashes[base]|({leaf['sha256']} if leaf else set())),'ordered_native_components':[leaf['name']] if leaf else [],'native_bank_components':[leaf] if leaf else [],'qualified_anchor_all8_metrics_exact':identity,'submission_qualified':identity,'test_labels_read':False})
            for p in [recordpath,control,capsule]:pins[str(p)]=sha(p)
    assert (len(records),full_count,prefix_count)==(85,80,240)
    best=min(records,key=lambda row:(-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case']))
    assert best['connected_final_score']>=anchors[182]['connected_final_score']
    for p,d in pins.items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot85.json',{'status':'passed_normalized48_actual_TRAIN_official_records_selected_stage_and_full_inference_pending','records':records,'best':best,'input_sha256':pins,'expected_scored_records':85,'actual_nonidentity_full_controls':80,'actual_nonidentity_prefix_controls':240,'actual_comparison_parent_round':182,'actual_scheme_base_round':best['configuration']['anchor_round'],'new_quality_scores_by_normalization':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_complete85_actual_TRAIN_records_without_future_features','pilot_sha256':sha(OUT/'pilot85.json'),'best':best,'full_selected_qualification_and_registration_pending':True,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_stock_rank20_embedding_complete85_after182_location_v1_20261010.json',{'output':str(OUT),'pilot_sha256':sha(OUT/'pilot85.json'),'verification_sha256':sha(OUT/'verification.json')})
    print({'actual_records':85,'best_S':best['connected_final_score'],'stage_kind':best['configuration']['stage_kind'],'future_dispatch_not_started':True},flush=True)

if __name__=='__main__':main()

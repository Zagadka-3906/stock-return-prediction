"""Normalize37 measured TRAIN comparisons and qualified183/204 anchors, without re-scoring."""
from pathlib import Path
import sys,time,hashlib,importlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/rank60_two_seed_protected_complete39_after204_v1_20261011')
PLAN=A/'rank60_two_seed_protected_complete39_after204_plan_v2_20261011.json'
def best_key(row):return (-row['connected_final_score'],row['expected_unique_native_models'],abs(row['configuration']['weight']),row['case'])
def main():
    assert allowed();plan=read(PLAN);assert plan['expected_records']==39 and plan['fully_qualified_anchors']==[183,204]
    closed(plan['actual_previous_complete_family'])
    for family in plan['families']:
        closed(family['actual_service']);receipt=A/family['main_receipt']
        while not receipt.exists():assert allowed();time.sleep(15)
        assert read(receipt)['status']=='pushed_and_remote_head_verified' and read(receipt)['branch']=='main'
    import numpy as np
    paths=[Path(__file__),PLAN,A/'rank60_two_seed_after183_protected37_predeclared_sources_admission_v1_20261011.json',A/'rank60_two_seed_protected_actual_twelve_parent_callbacks_CPU_controls_v1_20261011.json']
    pins={str(p):sha(p) for p in paths};records=[];anchors={};hashes={}
    for number in (183,204):
        release=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}';receipt=A/f'github_validation_sync_main_20261005/round{number}_receipt.json'
        assert read(release/'full_registration_execution.json')['status']=='passed' and read(receipt)['status']=='pushed_and_remote_head_verified'
        winner=read(release/'selection.json')['winner'];metrics=read(release/'calibrated_csv_official.json')['metrics'];assert winner['metrics']==metrics
        models=read(candidate/'verification.json')['models'];hashes[number]={r['sha256'] for r in models.values()};assert len(hashes[number])==len(models)
        value=np.load(release/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(value)).cast('B')).hexdigest();del value
        capsule=Path(winner['official_score_cache']['official_metrics_source']);assert read(capsule)['metrics']==metrics
        row={'case':len(records),'configuration':{'stage_kind':'anchor','anchor_round':number,'model':None,'recipe':None,'codec':None,'weight':0.,'sign':1.,'decay':None},'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(models),'prediction_numeric_bytes_sha256':numeric,'official_score_cache':winner['official_score_cache'],'official_metric_capsule_sha256':sha(capsule),'actual_return_mapping':winner['causal_return_mapping'],'ordered_native_components':[],'native_bank_components':[],'qualified_anchor_all8_metrics_exact':True,'submission_qualified':True,'test_labels_read':False}
        records.append(row);anchors[number]=row
        for p in [receipt,release/'full_registration_execution.json',release/'selection.json',release/'calibrated_csv_official.json',release/'selected_validation.npy',candidate/'verification.json',capsule]:pins[str(p)]=sha(p)
    full_count=prefix_count=0
    for family in plan['families']:
        stage=importlib.import_module(family['native_stage_module']);leaves=[]
        assert len(stage.BACKENDS[stage.RECIPE])==4
        for i,bankname in enumerate(family['banks']):
            bank=Path('E:/赛题五_本机临时')/bankname;assert read(bank/'verification.json')['actual_native_fits']==6
            info=read(bank/'2025/info.json');cfg=info['configuration'];assert cfg['seed']==family['seeds'][i] and cfg['epochs']==64
            assert cfg['label_horizon_trading_days']==family['label_horizons'][i] and cfg['training_calendar_window']==family['training_windows'][i]
            leaves.append({'name':family['member_names'][i],'bank':str(bank),'sha256':info['model_sha256'],'seed':family['seeds'][i],'label_horizon_trading_days':cfg['label_horizon_trading_days'],'training_calendar_window':cfg['training_calendar_window']})
            for p in [bank/'verification.json',*[bank/str(y)/n for y in range(2020,2026) for n in ('info.json','model.joblib')]]:pins[str(p)]=sha(p)
        assert leaves[0]['sha256']!=leaves[1]['sha256'];pins[str(A/(stage.__name__+'.py'))]=sha(A/(stage.__name__+'.py'))
        folder=Path(family['output']);proofpath=folder/'verification.json';proof=read(proofpath)
        assert len(proof['records'])==proof['new_quality_score_records']==37
        assert (proof['actual_nonidentity_full_controls'],proof['actual_nonidentity_prefix_controls'])==(36,108)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[str(A/family['main_receipt'])]=sha(A/family['main_receipt']);full_count+=36;prefix_count+=108
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration'])
            if not identity:assert cfg['kind']=='valid_pool_protection_v1' and cfg[family['component_weight_field']] in family['component_weights']
            cfg.update(stage_kind='anchor' if identity else family['stage_kind'],anchor_round=183,model=None if identity else family['signal_name'],recipe=None if identity else stage.RECIPE,codec=None if identity else cfg['kind'],decay=None,first2020_active=not identity)
            if identity:assert original['metrics']==anchors[183]['metrics'] and original['prediction_numeric_sha256']==anchors[183]['prediction_numeric_bytes_sha256']
            recordpath=folder/f"case{original['case']:03d}_official.json";controlpath=folder/f"case{original['case']:03d}_controls.json";capsule=Path(original['official_score_cache']['official_metrics_source']);control=read(controlpath)
            assert read(recordpath)==original and sha(controlpath)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256']
            assert read(capsule)['metrics']==original['metrics'] and control['numeric_sha256']==original['prediction_numeric_sha256']
            if not identity:assert control['full_independent_Pandas_exact'] and [p['days'] for p in control['prefix_controls']]==[80,260,975]
            physical=len(hashes[183]|({leaf['sha256'] for leaf in leaves} if not identity else set()))
            records.append({**original,'case':len(records),'configuration':cfg,'family':family['name'],'native_stage_module':stage.__name__,'native_graph_key':stage.GRAPH_KEY,'original_screen_case':original['case'],'original_screen_record':str(recordpath),'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':physical,'ordered_native_components':[] if identity else [leaf['name'] for leaf in leaves],'native_bank_components':[] if identity else leaves,'physical_models_for_signal':0 if identity else 2,'qualified_anchor_all8_metrics_exact':identity,'submission_qualified':identity,'test_labels_read':False})
            for p in [recordpath,controlpath,capsule]:pins[str(p)]=sha(p)
    assert (len(records),full_count,prefix_count)==(39,36,108)
    best=min(records,key=best_key);assert best['connected_final_score']>=anchors[204]['connected_final_score']
    for p,d in pins.items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot39.json',{'status':'passed_normalized39_actual_TRAIN_official_records_selected_native_and_full_future_pending','records':records,'best':best,'input_sha256':pins,'expected_scored_records':39,'actual_nonidentity_full_controls':36,'actual_nonidentity_prefix_controls':108,'actual_comparison_parent_round':204,'actual_scheme_base_round':best['configuration']['anchor_round'],'new_quality_scores_by_normalization':0,'new_native_fits':0,'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_complete39_actual_TRAIN_records_without_future_features','best':best,'pilot_sha256':sha(OUT/'pilot39.json'),'full_selected_qualification_and_registration_pending':True,'new_quality_scores':0,'test_labels_read':False})
    create(A/'actual_rank60_two_seed_protected_complete39_after204_location_v1_20261011.json',{'output':str(OUT),'pilot_sha256':sha(OUT/'pilot39.json'),'verification_sha256':sha(OUT/'verification.json')})
if __name__=='__main__':main()

"""Wait for both frozen TRAIN-only screens, then compare all132 actual records together."""
from pathlib import Path
import sys,time,hashlib
A=Path(__file__).resolve().parent;ROOT=A.parent;sys.path[:0]=[str(ROOT),str(A)]
from run_dependency_queue_v3_20261006 import read,sha,create
from prepare_protected_tail_pilot76_and_selected_native14_v1_20261010 import allowed,closed
OUT=Path('E:/赛题五_本机临时/cross120_two_target132_v1_20261010')
SERVICES={
 'Cross120Recent252Forward5_after169_high_impact65':'actual_Cross120Recent252Forward5_after169_high_impact65_screen_v1_20261010',
 'Cross120Recent252Rank5_after169_high_impact65':'actual_Cross120Recent252Rank5_after169_high_impact65_screen_v1_20261010'}
RECIPES={
 'cross120recent252forward5huber050':('rank_MLP2048_BF16_Cross120Recent252Forward5Huber050_seed09_e64','neural_BF16_medium2048_cross120recent252forward5huber050_seed09_e62_bank6_v1_20261009'),
 'cross120recent252rank5huber050':('rank_MLP2048_BF16_Cross120Recent252Rank5Huber050_seed09_e64','neural_BF16_medium2048_cross120recent252rank5huber050_seed09_e62_bank6_v1_20261009')}

def main():
    assert allowed();planpath=A/'cross120_two_target132_complete_comparison_selection_plan_v1_20261010.json';plan=read(planpath)
    assert plan['expected_records']==132 and plan['fully_qualified_anchors']==[168,169]
    # Never select a winner from a partially completed family.
    for family in plan['families']:
        closed(SERVICES[family['stem']])
        while not Path(family['publisher_receipt']).exists():assert allowed();time.sleep(15)
        receipt=read(family['publisher_receipt']);assert receipt['status']=='pushed_and_remote_head_verified' and receipt['branch']=='main'
    import numpy as np
    pins={str(p):sha(p) for p in [Path(__file__),planpath]};records=[];models={};full_count=prefix_count=0
    for number in (168,169):
        folder=A/f'optimization_20261003_r{number}';candidate=ROOT/f'candidates/optimization_20261003_r{number}'
        assert read(folder/'full_registration_execution.json')['status']=='passed'
        release=read(A/f'github_validation_sync_main_20261005/round{number}_receipt.json');assert release['status']=='pushed_and_remote_head_verified'
        selection=read(folder/'selection.json')['winner'];metrics=read(folder/'calibrated_csv_official.json')['metrics'];assert selection['metrics']==metrics
        models[number]=read(candidate/'verification.json')['models'];assert len({x['sha256'] for x in models[number].values()})==len(models[number])
        cache=selection['official_score_cache'];capsule=Path(cache['official_metrics_source']);assert read(capsule)['metrics']==metrics
        pred=np.load(folder/'selected_validation.npy',mmap_mode='r');numeric=hashlib.sha256(memoryview(np.ascontiguousarray(pred)).cast('B')).hexdigest()
        cfg={'anchor_round':number,'model':None,'recipe':None,'codec':None,'role':None,'weight':0.,'sign':1.,'protect_fraction':None,'universe':None}
        records.append({'case':len(records),'configuration':cfg,'metrics':metrics,'connected_final_score':metrics['final_score'],'expected_unique_native_models':len(models[number]),
            'prediction_numeric_bytes_sha256':numeric,'official_score_cache':cache,'official_metric_capsule_sha256':sha(capsule),'qualified_anchor_all8_metrics_exact':True,'ordered_native_components':[],
            'actual_return_mapping':selection.get('causal_return_mapping',{}),'test_labels_read':False})
        for p in [folder/'selection.json',folder/'selected_validation.npy',folder/'calibrated_csv_official.json',folder/'full_registration_execution.json',candidate/'verification.json',capsule,A/f'github_validation_sync_main_20261005/round{number}_receipt.json']:pins[str(p)]=sha(p)
    anchor169=records[1]
    for family in plan['families']:
        assert allowed();folder=Path('E:/赛题五_本机临时')/(family['stem']+'_screen_v1_20261010');proofpath=folder/'verification.json';proof=read(proofpath)
        count=family['records'];assert len(proof['records'])==count and proof['new_quality_score_records']==count
        assert proof['actual_nonidentity_full_controls']==count-1 and proof['actual_nonidentity_prefix_controls']==3*(count-1)
        full_count+=count-1;prefix_count+=3*(count-1)
        for p,d in proof['input_sha256'].items():assert sha(p)==d,p
        pins.update(proof['input_sha256']);pins[str(proofpath)]=sha(proofpath);pins[family['publisher_receipt']]=sha(family['publisher_receipt'])
        model,bankname=RECIPES[family['recipe']];bank=Path('E:/赛题五_本机临时')/bankname;info=read(bank/'2025/info.json')
        assert read(bank/'verification.json')['actual_native_fits']==6 and info['status']=='passed_actual_complete_mature_BF16_micro_annual_model'
        pins[str(bank/'2025/info.json')]=sha(bank/'2025/info.json');pins[str(bank/'verification.json')]=sha(bank/'verification.json')
        for original in proof['records']:
            identity=original['case']==0;cfg=dict(original['configuration']);base=169 if identity else family['scheme_base_round']
            cfg.update(anchor_round=base,model=None if identity else model,recipe=None if identity else family['recipe'],codec=None if identity else cfg['kind'],universe=None if identity else 'all_current_raw_forecasts')
            if identity:
                assert original['metrics']==anchor169['metrics'] and original['prediction_numeric_sha256']==anchor169['prediction_numeric_bytes_sha256']
            physical=len({x['sha256'] for x in models[base].values()}|({info['model_sha256']} if not identity else set()))
            originalpath=folder/f"case{original['case']:03d}_official.json";control=folder/f"case{original['case']:03d}_controls.json";capsule=Path(original['official_score_cache']['official_metrics_source'])
            assert read(originalpath)==original and sha(control)==original['control_sha256'] and sha(capsule)==original['official_metric_capsule_sha256']
            assert read(capsule)['metrics']==original['metrics']
            record={**original,'case':len(records),'configuration':cfg,'original_screen_case':original['case'],'original_screen_record':str(originalpath),'family':family['stem'],
                'prediction_numeric_bytes_sha256':original['prediction_numeric_sha256'],'expected_unique_native_models':physical,'qualified_anchor_all8_metrics_exact':identity,
                'ordered_native_components':[] if identity else [model],'whole_complete_parent_branches_preserved_before_new_stage':not identity,
                'invalid_and_declared_unselected_raw_bits_preserved':not identity,'actual_cold80_260_975_bits_exact':not identity,'first2020_active':not identity}
            records.append(record)
            for p in [originalpath,control,capsule]:pins[str(p)]=sha(p)
    assert (len(records),full_count,prefix_count)==(132,128,384)
    best=min(records,key=lambda r:(-r['connected_final_score'],r['expected_unique_native_models'],abs(r['configuration']['weight']),r['case']))
    assert best['connected_final_score']>=anchor169['connected_final_score']
    for p,d in pins.items():assert sha(p)==d,p
    OUT.mkdir(exist_ok=False)
    create(OUT/'pilot132.json',{'status':'passed_normalized132_actual_training_only_official_records_native14_and_full_inference_pending','records':records,'best':best,'input_sha256':pins,
        'actual_scheme_base_round':best['configuration']['anchor_round'],'actual_comparison_parent_round':169,'expected_scored_records':132,
        'actual_nonidentity_full_controls':128,'actual_nonidentity_prefix_controls':384,'new_quality_scores_by_normalization':0,'selected_native14_pending':True,
        'actual_future_X_read':False,'test_labels_read':False,'submission_qualified':False})
    create(OUT/'verification.json',{'status':'passed_complete132_actual_official_records_selection_without_future_features','pilot_sha256':sha(OUT/'pilot132.json'),'best':best,'selected_native14_and_frozen_full_inference_and_registration_pending':True,'new_native_fits':0,'new_quality_scores':0,'submission_qualified':False,'test_labels_read':False})
    create(A/'actual_cross120_two_target132_location_v1_20261010.json',{'output':str(OUT),'verification_sha256':sha(OUT/'verification.json'),'pilot_sha256':sha(OUT/'pilot132.json')})
    print({'records':132,'best_S':best['connected_final_score'],'selected_family':best.get('family'),'native14_and_full170_still_required':True},flush=True)
if __name__=='__main__':main()
